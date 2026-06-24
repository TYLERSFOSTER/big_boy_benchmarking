"""PPO buffers and update code for Warehouse full-tower PPO."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .gae import compute_gae, normalize
from .policy_bank import TierPolicyEntry
from .records import DecisionContextRecord, RolloutSampleRecord
from .tokenization import EncodedDecisionSurface


@dataclass
class PPOSample:
    context: DecisionContextRecord
    encoded: EncodedDecisionSurface
    sample: RolloutSampleRecord


@dataclass
class TierRolloutBuffer:
    tier_index: int
    samples: list[PPOSample] = field(default_factory=list)
    carry_forward_samples: list[PPOSample] = field(default_factory=list)

    def append(self, sample: PPOSample) -> None:
        self.samples.append(sample)

    def ready_count(self) -> int:
        return len(self.samples) + len(self.carry_forward_samples)

    def take_ready_samples(self) -> list[PPOSample]:
        ready = [*self.carry_forward_samples, *self.samples]
        self.carry_forward_samples = []
        self.samples = []
        return ready

    def carry_forward(self) -> None:
        self.carry_forward_samples.extend(self.samples)
        self.samples = []


@dataclass(frozen=True)
class PPOUpdateResult:
    tier_index: int
    sample_count: int
    optimizer_steps: int
    policy_loss: float
    value_loss: float
    entropy: float
    approx_kl: float
    clip_fraction: float
    grad_norm: float
    skipped: bool = False
    skip_reason: str = ""

    def to_row(
        self,
        *,
        run_id: str,
        arm_id: str,
        global_update_index: int,
        device: str,
    ) -> dict[str, object]:
        return {
            "run_id": run_id,
            "arm_id": arm_id,
            "global_update_index": global_update_index,
            "tier_index": self.tier_index,
            "sample_count": self.sample_count,
            "optimizer_steps": self.optimizer_steps,
            "policy_loss": self.policy_loss,
            "value_loss": self.value_loss,
            "entropy": self.entropy,
            "approx_kl": self.approx_kl,
            "clip_fraction": self.clip_fraction,
            "grad_norm": self.grad_norm,
            "device": device,
            "skipped": self.skipped,
            "skip_reason": self.skip_reason,
        }


def update_tier_policy(
    *,
    entry: TierPolicyEntry,
    samples: list[PPOSample],
    gamma: float,
    gae_lambda: float,
    clip_epsilon: float,
    value_coef: float,
    entropy_coef: float,
    max_grad_norm: float,
    ppo_epochs: int,
    minibatch_size: int,
) -> PPOUpdateResult:
    if not samples:
        return PPOUpdateResult(
            tier_index=entry.tier_index,
            sample_count=0,
            optimizer_steps=entry.optimizer_steps,
            policy_loss=0.0,
            value_loss=0.0,
            entropy=0.0,
            approx_kl=0.0,
            clip_fraction=0.0,
            grad_norm=0.0,
            skipped=True,
            skip_reason="no_samples",
        )
    torch = _require_torch()
    rewards = [sample.sample.reward for sample in samples]
    values = [sample.sample.value_estimate for sample in samples]
    terminated = [sample.sample.terminated for sample in samples]
    advantages, returns = compute_gae(
        rewards=rewards,
        values=values,
        bootstrap_value=0.0,
        terminated=terminated,
        gamma=gamma,
        gae_lambda=gae_lambda,
    )
    advantages = normalize(advantages)
    policy_losses = []
    value_losses = []
    entropies = []
    kls = []
    clip_flags = []
    grad_norm_value = 0.0
    indices = list(range(len(samples)))
    optimizer_steps = entry.optimizer_steps
    for _epoch in range(ppo_epochs):
        for start in range(0, len(indices), minibatch_size):
            batch_indices = indices[start : start + minibatch_size]
            if not batch_indices:
                continue
            loss_terms = []
            value_terms = []
            entropy_terms = []
            kl_terms = []
            clip_terms = []
            for index in batch_indices:
                ppo_sample = samples[index]
                output = entry.policy.forward_encoded(ppo_sample.encoded)
                selected = ppo_sample.sample.selected_local_index
                new_log_prob = output.log_probs[selected]
                old_log_prob = torch.tensor(
                    ppo_sample.sample.old_log_prob,
                    dtype=torch.float32,
                    device=new_log_prob.device,
                )
                ratio = (new_log_prob - old_log_prob).exp()
                advantage = torch.tensor(
                    advantages[index],
                    dtype=torch.float32,
                    device=new_log_prob.device,
                )
                ret = torch.tensor(
                    returns[index],
                    dtype=torch.float32,
                    device=new_log_prob.device,
                )
                unclipped = ratio * advantage
                clipped = torch.clamp(
                    ratio,
                    1.0 - clip_epsilon,
                    1.0 + clip_epsilon,
                ) * advantage
                loss_terms.append(-torch.minimum(unclipped, clipped))
                value_terms.append((output.value - ret).pow(2))
                entropy_terms.append(output.entropy)
                kl_terms.append(old_log_prob - new_log_prob)
                clip_terms.append((ratio - 1.0).abs() > clip_epsilon)
            policy_loss = torch.stack(loss_terms).mean()
            value_loss = torch.stack(value_terms).mean()
            entropy = torch.stack(entropy_terms).mean()
            loss = policy_loss + value_coef * value_loss - entropy_coef * entropy
            entry.optimizer.zero_grad()
            loss.backward()
            grad_norm = torch.nn.utils.clip_grad_norm_(
                entry.policy.parameters(),
                max_grad_norm,
            )
            entry.optimizer.step()
            optimizer_steps += 1
            policy_losses.append(float(policy_loss.detach().cpu()))
            value_losses.append(float(value_loss.detach().cpu()))
            entropies.append(float(entropy.detach().cpu()))
            kls.append(float(torch.stack(kl_terms).mean().detach().cpu()))
            clip_flags.append(
                sum(bool(flag.detach().cpu()) for flag in clip_terms) / len(clip_terms)
            )
            grad_norm_value = float(grad_norm.detach().cpu())
    entry.optimizer_steps = optimizer_steps
    return PPOUpdateResult(
        tier_index=entry.tier_index,
        sample_count=len(samples),
        optimizer_steps=optimizer_steps,
        policy_loss=_mean(policy_losses),
        value_loss=_mean(value_losses),
        entropy=_mean(entropies),
        approx_kl=_mean(kls),
        clip_fraction=_mean(clip_flags),
        grad_norm=grad_norm_value,
    )


def _mean(values: list[float]) -> float:
    return 0.0 if not values else sum(values) / len(values)


def _require_torch() -> Any:
    try:
        import torch
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("torch is required for Warehouse full-tower PPO") from exc
    return torch
