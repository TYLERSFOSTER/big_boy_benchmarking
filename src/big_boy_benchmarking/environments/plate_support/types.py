"""Typed records for BBB PlateSupport environment diagnostics."""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Any


class PlateSupportFlatRecord:
    """Small helper for stable CSV field order."""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def fieldnames(cls) -> tuple[str, ...]:
        return tuple(field.name for field in fields(cls))


@dataclass(frozen=True)
class ActionRecord(PlateSupportFlatRecord):
    action_index: int
    action_label: str
    action_category: str
    description: str
    upstream_identity: str


@dataclass(frozen=True)
class StateRecord(PlateSupportFlatRecord):
    state_id: str
    x_idx: int
    y_idx: int
    theta_idx: int
    e1: int
    e2: int
    e3: int
    support_pattern: str
    socket_positions: str
    reachability_pattern: str
    minimum_engaged_supports: bool
    stable_support_pattern: bool
    sockets_in_bounds: bool
    valid_state: bool
    coarse_position: str
    fine_position: str
    role: str


@dataclass(frozen=True)
class TransitionRecord(PlateSupportFlatRecord):
    source_state_id: str
    action_index: int
    action_label: str
    candidate_state_id: str
    next_state_id: str
    candidate_valid: bool
    valid_transition: bool
    invalid_move: bool
    valid_self_transition: bool
    reward: float
    terminated: bool
    truncated_at_one_step: bool


@dataclass(frozen=True)
class ShortestPathRecord(PlateSupportFlatRecord):
    step_index: int
    state_id: str
    action_index: int | None
    action_label: str
    next_state_id: str
    reward: float | None


@dataclass(frozen=True)
class TowerProbeRecord(PlateSupportFlatRecord):
    schema_id: str
    upstream_schema_mode: str
    env_name: str
    steps: int
    sample_size: int
    seed: int
    use_contraction_policy: bool
    reset_on_terminal: bool
    max_depth: int
    scheduled_assignment_count: int
    unscheduled_assignment_count: int
    depth_curve: str
    reset_event_count: int


@dataclass(frozen=True)
class RandomPolicyReconRecord(PlateSupportFlatRecord):
    policy_id: str
    seed: int
    episode_count: int
    max_steps_per_episode: int
    success_count: int
    success_rate: float
    mean_total_reward: float
    mean_step_count: float
    invalid_move_count: int
    invalid_move_rate: float
