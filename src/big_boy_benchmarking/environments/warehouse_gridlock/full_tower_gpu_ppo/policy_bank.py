"""Per-tier policy bank for Warehouse full-tower PPO."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any

from .config import WarehousePolicyCapacityConfig, WarehousePPOHyperparameters
from .models import TierCandidateActorCritic, parameter_count


@dataclass
class TierPolicyEntry:
    tier_index: int
    hidden_dim: int
    policy: Any
    rollout_policy: Any
    optimizer: Any
    policy_snapshot_id: str
    rollout_policy_snapshot_id: str
    optimizer_steps: int = 0

    def refresh_rollout_snapshot(self, *, update_index: int) -> None:
        self.rollout_policy.load_state_dict(copy.deepcopy(self.policy.state_dict()))
        self.rollout_policy.eval()
        for parameter in self.rollout_policy.parameters():
            parameter.requires_grad_(False)
        self.policy_snapshot_id = f"tier{self.tier_index}-policy-update{update_index}"
        self.rollout_policy_snapshot_id = (
            f"tier{self.tier_index}-rollout-update{update_index}"
        )

    def to_manifest(self) -> dict[str, object]:
        return {
            "tier_index": self.tier_index,
            "hidden_dim": self.hidden_dim,
            "policy_snapshot_id": self.policy_snapshot_id,
            "rollout_policy_snapshot_id": self.rollout_policy_snapshot_id,
            "optimizer_steps": self.optimizer_steps,
            "parameter_count": parameter_count(self.policy),
        }


@dataclass
class TierPolicyBank:
    capacity: WarehousePolicyCapacityConfig
    ppo: WarehousePPOHyperparameters
    device: str = "cpu"
    entries: dict[int, TierPolicyEntry] = field(default_factory=dict)

    def entry_for_tier(self, tier_index: int) -> TierPolicyEntry:
        if tier_index not in self.entries:
            self.entries[tier_index] = self._create_entry(tier_index)
        return self.entries[tier_index]

    def _create_entry(self, tier_index: int) -> TierPolicyEntry:
        torch = _require_torch()
        hidden_dim = self.capacity.capacity_for_tier(tier_index)
        policy = TierCandidateActorCritic(hidden_dim=hidden_dim).to(self.device)
        rollout_policy = TierCandidateActorCritic(hidden_dim=hidden_dim).to(self.device)
        optimizer = torch.optim.AdamW(policy.parameters(), lr=self.ppo.learning_rate)
        entry = TierPolicyEntry(
            tier_index=tier_index,
            hidden_dim=hidden_dim,
            policy=policy,
            rollout_policy=rollout_policy,
            optimizer=optimizer,
            policy_snapshot_id=f"tier{tier_index}-policy-init",
            rollout_policy_snapshot_id=f"tier{tier_index}-rollout-init",
        )
        entry.refresh_rollout_snapshot(update_index=0)
        return entry

    def to_manifest(self) -> dict[str, object]:
        return {
            "capacity": self.capacity.to_manifest(),
            "device": self.device,
            "entries": [entry.to_manifest() for _, entry in sorted(self.entries.items())],
            "parameter_sharing": "none",
        }


def _require_torch() -> Any:
    try:
        import torch
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("torch is required for Warehouse full-tower PPO") from exc
    return torch
