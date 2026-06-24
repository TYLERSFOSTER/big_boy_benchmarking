"""Record contracts for Warehouse full-tower PPO."""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Any

from .ids import (
    WAREHOUSE_GRIDLOCK_DECISION_CONTEXT_SCHEMA_VERSION,
    WAREHOUSE_GRIDLOCK_GEOMETRY_RECORD_SCHEMA_VERSION,
    WAREHOUSE_GRIDLOCK_ROLLOUT_SAMPLE_SCHEMA_VERSION,
    WAREHOUSE_GRIDLOCK_TIER_DIRECTION_CONVENTION,
)

MUTABLE_GEOMETRY_FIELDS = {
    "episode_index",
    "current_second",
    "remaining_seconds",
    "old_log_prob",
    "new_log_prob",
    "value_estimate",
    "advantage",
    "return",
    "reward",
    "terminated",
    "truncated",
    "selected_action",
    "rollout_update_index",
    "controller_event_index",
    "ppo_sample_index",
}


class GeometryRecordValidationError(ValueError):
    """Raised when mutable rollout data enters immutable geometry records."""


@dataclass(frozen=True)
class TierStateGeometryRecord:
    geometry_record_id: str
    graph_snapshot_id: str
    tower_snapshot_id: str
    tier_index: int
    state_cell_id: str
    state_coset_member_ids: tuple[str, ...]
    parent_state_cell_id: str | None
    child_state_cell_ids: tuple[str, ...]
    outgoing_action_cell_ids: tuple[str, ...]
    quotient_adjacency_summary: str
    known_one_hop_geometry: str
    geometry_source_manifest_ref: str
    schema_version: str = WAREHOUSE_GRIDLOCK_GEOMETRY_RECORD_SCHEMA_VERSION
    tier_direction_convention: str = WAREHOUSE_GRIDLOCK_TIER_DIRECTION_CONVENTION

    def __post_init__(self) -> None:
        _reject_mutable_fields(self)

    @property
    def state_coset_size(self) -> int:
        return len(self.state_coset_member_ids)

    @property
    def outgoing_action_count(self) -> int:
        return len(self.outgoing_action_cell_ids)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["state_coset_size"] = self.state_coset_size
        payload["outgoing_action_count"] = self.outgoing_action_count
        return payload


@dataclass(frozen=True)
class TierActionGeometryRecord:
    geometry_record_id: str
    graph_snapshot_id: str
    tower_snapshot_id: str
    tier_index: int
    action_cell_id: str
    source_state_cell_id: str
    target_state_cell_id: str
    member_edge_ids: tuple[str, ...]
    lower_or_child_action_cell_ids: tuple[str, ...]
    representative_edge_ids_for_readout_only: tuple[str, ...]
    out_hom_summary: str
    action_hom_summary: str
    geometry_source_manifest_ref: str
    schema_version: str = WAREHOUSE_GRIDLOCK_GEOMETRY_RECORD_SCHEMA_VERSION

    def __post_init__(self) -> None:
        _reject_mutable_fields(self)

    @property
    def member_edge_count(self) -> int:
        return len(self.member_edge_ids)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["member_edge_count"] = self.member_edge_count
        return payload


@dataclass(frozen=True)
class DecisionContextRecord:
    decision_context_id: str
    episode_id: str
    replicate_index: int
    schema_seed: int
    arm_id: str
    tier_index: int
    ppo_sample_index: int
    controller_event_index_start: int
    controller_event_index_end: int
    environment_second: int
    active_tier: int
    current_concrete_state_digest: str
    current_position_at_every_tier: tuple[str | None, ...]
    tower_position_key: str
    runtime_snapshot_id: str
    schema_arm_id: str
    graph_snapshot_id: str
    tower_snapshot_id: str
    state_geometry_record_id: str
    candidate_action_ids_ordered: tuple[str, ...]
    candidate_local_indices: tuple[int, ...]
    candidate_mask: tuple[bool, ...]
    mask_kind: str
    mask_semantics_id: str
    state_collapser_source_ref: str
    controller_event_refs: tuple[str, ...]
    schema_version: str = WAREHOUSE_GRIDLOCK_DECISION_CONTEXT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not self.candidate_action_ids_ordered:
            raise ValueError("decision context requires nonempty candidate surface")
        if len(self.candidate_mask) != len(self.candidate_action_ids_ordered):
            raise ValueError("candidate mask length mismatch")
        if len(self.candidate_local_indices) != len(self.candidate_action_ids_ordered):
            raise ValueError("candidate local index length mismatch")
        if not any(self.candidate_mask):
            raise ValueError("all candidates are masked")
        if self.mask_kind != "pointwise_executable":
            raise ValueError("mask_kind must be pointwise_executable")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class RolloutSampleRecord:
    rollout_sample_id: str
    decision_context_id: str
    tier_index: int
    policy_snapshot_id: str
    rollout_policy_snapshot_id: str
    state_history_ref: str
    action_history_ref: str
    candidate_action_ids_ordered: tuple[str, ...]
    candidate_mask: tuple[bool, ...]
    selected_local_index: int
    selected_action_cell_id: str
    old_log_prob: float
    value_estimate: float
    entropy: float
    resolved_concrete_action_digest: str
    lift_candidate_id: str
    lift_candidate_digest: str
    lift_semantics_id: str
    reward: float
    next_decision_context_id: str | None
    terminated: bool
    truncated: bool
    bootstrap_value: float | None
    diagnostic_failure_code: str | None
    schema_version: str = WAREHOUSE_GRIDLOCK_ROLLOUT_SAMPLE_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not self.rollout_policy_snapshot_id:
            raise ValueError("rollout_policy_snapshot_id is required")
        if self.old_log_prob is None:
            raise ValueError("old_log_prob is required")
        if self.selected_local_index < 0:
            raise ValueError("selected_local_index must be nonnegative")
        if self.selected_local_index >= len(self.candidate_action_ids_ordered):
            raise ValueError("selected index outside candidate surface")
        if not self.candidate_mask[self.selected_local_index]:
            raise ValueError("selected candidate is masked")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _reject_mutable_fields(instance: object) -> None:
    present = {field.name for field in fields(instance)}
    unsafe = present & MUTABLE_GEOMETRY_FIELDS
    if unsafe:
        raise GeometryRecordValidationError(
            f"mutable fields forbidden in geometry record: {sorted(unsafe)}"
        )


def ensure_no_mutable_geometry_payload(payload: dict[str, Any]) -> None:
    unsafe = set(payload) & MUTABLE_GEOMETRY_FIELDS
    if unsafe:
        raise GeometryRecordValidationError(
            f"mutable fields forbidden in geometry payload: {sorted(unsafe)}"
        )
