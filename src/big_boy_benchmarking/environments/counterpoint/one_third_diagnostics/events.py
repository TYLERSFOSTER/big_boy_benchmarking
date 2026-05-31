"""Flat rows for one-third counterpoint tower diagnostics."""

from __future__ import annotations

from dataclasses import dataclass

from big_boy_benchmarking.metrics.events import FlatRow


@dataclass(frozen=True)
class OneThirdEvaluationRunIndexRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    seed_bundle_id: str
    replicate_index: int
    status: str
    artifact_root: str
    started_at: str
    ended_at: str | None
    failure_reason: str | None = None


@dataclass(frozen=True)
class OneThirdEpisodeRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    seed_bundle_id: str
    replicate_index: int
    episode_index: int
    total_reward: float
    concrete_step_count: int
    controller_event_count: int
    terminated: bool
    truncated: bool
    final_state: str


@dataclass(frozen=True)
class OneThirdStepRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    seed_bundle_id: str
    replicate_index: int
    episode_index: int
    step_index: int
    controller_event_index: int
    source_state: str
    action_repr: str
    reward: float
    target_state: str
    terminated: bool
    truncated: bool
    active_tier_before: int | None
    active_tier_after: int | None


@dataclass(frozen=True)
class OneThirdControlEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    seed_bundle_id: str
    replicate_index: int
    episode_index: int
    controller_event_index: int
    active_tier_before: int | None
    active_tier_after: int | None
    control_action: str
    pressure: float | None
    learner_updated: bool | None
    td_error: float | None
    success: bool | None


@dataclass(frozen=True)
class OneThirdLiftFiberEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    seed_bundle_id: str
    replicate_index: int
    episode_index: int
    controller_event_index: int
    active_tier: int | None
    abstract_action: str
    realized_action: str | None
    candidate_count: int
    success: bool
    failure_reason: str | None
    fiber_departure_reason: str | None


@dataclass(frozen=True)
class ABCSelectionEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    seed_bundle_id: str
    replicate_index: int
    episode_index: int
    controller_event_index: int
    active_tier_before: int
    active_tier_after: int | None
    deepest_known_tier: int
    selected_tier: int | None
    selected_tier_executable: bool | None
    predicted_movement_direction: str
    control_action: str
    decision_pressure: float
    training_due: bool
    action_consistent: bool
    blocked_reason: str | None
    concrete_step_emitted: bool
    lift_attempt_emitted: bool


@dataclass(frozen=True)
class ABCTierSignalEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    seed_bundle_id: str
    replicate_index: int
    episode_index: int
    controller_event_index: int
    active_tier_before: int
    selected_tier: int | None
    tier_index: int
    executable: bool
    visit_count: int
    td_error_ema: float
    success_count: int
    failure_count: int
    success_rate: float
    reward_residual_ema: float
    has_reward_residual: bool
    productive_learning_pressure: float
    unclosed: bool
    selected: bool
    active: bool


@dataclass(frozen=True)
class SchemaBlockSummaryRow(FlatRow):
    evaluation_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    block_id: str
    scheduled_edge_count: int
    scheduled_edge_share: float
    source_count_with_block: int
    mean_source_local_edge_count: float | None
    construction_rule: str


@dataclass(frozen=True)
class TowerShapeSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    replicate_index: int
    tier_index: int
    state_cell_count: int
    action_cell_count: int
    base_state_count: int
    base_edge_count: int
    state_compression_ratio: float
    largest_state_fiber_share: float
    singleton_state_fiber_share: float
    degeneracy_class: str


@dataclass(frozen=True)
class TierExecutabilitySummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    replicate_index: int
    tier_index: int
    event_count: int
    executable_event_count: int
    executable_event_share: float | None
    selected_event_count: int


@dataclass(frozen=True)
class ControlActionSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    replicate_index: int
    control_action: str
    event_count: int
    event_share: float


@dataclass(frozen=True)
class ABCSelectionSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    replicate_index: int
    selected_tier: int | None
    predicted_movement_direction: str
    control_action: str
    blocked_reason: str | None
    event_count: int
    action_consistent_count: int
    action_consistent_share: float | None


@dataclass(frozen=True)
class ABCTierSignalSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    replicate_index: int
    tier_index: int
    event_count: int
    executable_event_share: float | None
    unclosed_event_share: float | None
    mean_productive_learning_pressure: float | None
    selected_event_count: int
    active_event_count: int


@dataclass(frozen=True)
class TierOccupancySummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    replicate_index: int
    tier_index: int | None
    control_action: str
    event_count: int
    event_share: float
    concrete_step_count: int
    concrete_step_share: float
    mean_reward_on_concrete_steps: float | None


@dataclass(frozen=True)
class LiftFailureByTierRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    replicate_index: int
    active_tier: int | None
    failure_reason: str | None
    fiber_departure_reason: str | None
    lift_attempt_count: int
    lift_success_count: int
    lift_failure_count: int
    mean_candidate_count: float | None


@dataclass(frozen=True)
class ConcreteStepSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    replicate_index: int
    episode_count: int
    concrete_step_count: int
    zero_step_episode_count: int
    mean_reward: float | None
    terminated_count: int
    truncated_count: int
    final_state_summary: str


@dataclass(frozen=True)
class AggregateTableRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    schema_id: str
    schema_seed: int
    replicate_index: int
    status: str
    first_projection_largest_state_fiber_share: float | None
    full_first_projection_collapse: bool
    near_full_first_projection_collapse: bool
    selected_tier_non_executability_count: int
    no_available_action_count: int
    zero_concrete_steps: bool
    missing_abc_context: bool
    structural_limit_classification: str
