"""Actor-critic training helpers for Warehouse transformer policies."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .config import OptimizerConfig
from .torch_runtime import require_torch


@dataclass
class EpisodeRolloutBuffer:
    log_probabilities: list[Any] = field(default_factory=list)
    values: list[Any] = field(default_factory=list)
    rewards: list[float] = field(default_factory=list)
    entropies: list[Any] = field(default_factory=list)

    def append(
        self,
        *,
        log_probability: Any,
        value: Any,
        reward: float,
        entropy: Any,
    ) -> None:
        self.log_probabilities.append(log_probability)
        self.values.append(value)
        self.rewards.append(float(reward))
        self.entropies.append(entropy)

    @property
    def step_count(self) -> int:
        return len(self.rewards)


@dataclass(frozen=True)
class TrainingStepResult:
    optimizer_steps: int
    policy_loss: float
    value_loss: float
    entropy: float
    total_loss: float
    grad_norm: float

    def to_row(self, *, run_id: str, arm_id: str, episode_index: int) -> dict[str, object]:
        return {
            "run_id": run_id,
            "arm_id": arm_id,
            "episode_index": episode_index,
            "optimizer_steps": self.optimizer_steps,
            "policy_loss": self.policy_loss,
            "value_loss": self.value_loss,
            "entropy": self.entropy,
            "total_loss": self.total_loss,
            "grad_norm": self.grad_norm,
        }


def apply_actor_critic_update(
    *,
    model: Any,
    optimizer: Any,
    buffer: EpisodeRolloutBuffer,
    config: OptimizerConfig,
    optimizer_steps_before: int,
) -> TrainingStepResult | None:
    if buffer.step_count == 0:
        return None
    torch = require_torch()
    device = buffer.values[0].device
    returns = _discounted_returns(buffer.rewards, gamma=config.gamma, torch=torch, device=device)
    values = torch.stack(buffer.values)
    log_probabilities = torch.stack(buffer.log_probabilities)
    entropies = torch.stack(buffer.entropies)
    advantages = returns - values
    policy_loss = -(log_probabilities * advantages.detach()).mean()
    value_loss = advantages.pow(2).mean()
    entropy = entropies.mean()
    total_loss = policy_loss + config.value_coef * value_loss - config.entropy_coef * entropy
    optimizer.zero_grad()
    total_loss.backward()
    grad_norm_tensor = torch.nn.utils.clip_grad_norm_(model.parameters(), config.max_grad_norm)
    optimizer.step()
    return TrainingStepResult(
        optimizer_steps=optimizer_steps_before + 1,
        policy_loss=float(policy_loss.detach().cpu()),
        value_loss=float(value_loss.detach().cpu()),
        entropy=float(entropy.detach().cpu()),
        total_loss=float(total_loss.detach().cpu()),
        grad_norm=float(grad_norm_tensor.detach().cpu()),
    )


def _discounted_returns(
    rewards: list[float],
    *,
    gamma: float,
    torch: Any,
    device: Any,
) -> Any:
    running = 0.0
    values: list[float] = []
    for reward in reversed(rewards):
        running = reward + gamma * running
        values.append(running)
    values.reverse()
    return torch.tensor(values, dtype=torch.float32, device=device)
