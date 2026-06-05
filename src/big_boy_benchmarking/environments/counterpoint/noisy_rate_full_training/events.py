"""Flat row contracts for noisy-rate full-tower training diagnostics."""

from __future__ import annotations

from dataclasses import dataclass

from big_boy_benchmarking.metrics.events import FlatRow


@dataclass(frozen=True)
class FullTrainingEvaluationRunIndexRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
    schema_seed: int
    seed_bundle_id: str
    training_replicate_index: int
    status: str
    artifact_root: str
    started_at: str
    ended_at: str | None
    failure_reason: str | None = None


@dataclass(frozen=True)
class FullTrainingCandidateSummaryRow(FlatRow):
    evaluation_id: str
    candidate_id: str
    parent_evaluation_id: str
    parent_artifact_run_label: str
    parent_run_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
    schema_seed: int
    selected_edge_count: int
    selected_edge_share: float
    selected_source_share: float | None
    zero_selected_source_count: int
    tier_state_cell_count_sequence: str
    tier_active_action_cell_count_sequence: str
    deepest_tier_index: int
    deepest_tier_state_cell_count: int
    deepest_tier_active_action_cell_count: int
    largest_state_cell_share: float
    endpoint_useful_coalescence_count: int
    candidate_eligible: bool
    candidate_exclusion_reason: str | None
    candidate_liftability_evidence_source: str = ""
    candidate_liftability_compatibility_note: str = ""


@dataclass(frozen=True)
class FullTrainingEpisodeRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    seed_bundle_id: str
    training_replicate_index: int
    episode_index: int
    total_reward: float
    concrete_step_count: int
    controller_event_count: int
    lift_attempt_count: int
    lift_success_count: int
    learner_update_count: int
    terminated: bool
    truncated: bool
    final_state: str


@dataclass(frozen=True)
class FullTrainingStepRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    seed_bundle_id: str
    training_replicate_index: int
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
class FullTrainingControlEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    seed_bundle_id: str
    training_replicate_index: int
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
class FullTrainingLiftFiberEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    seed_bundle_id: str
    training_replicate_index: int
    episode_index: int
    controller_event_index: int
    active_tier: int | None
    abstract_action: str
    realized_action: str | None
    candidate_count: int
    success: bool
    failure_reason: str | None
    fiber_departure_reason: str | None
    liftability_semantics_id: str = ""
    representative_candidate_count: int = 0
    pointwise_candidate_count: int = 0
    selected_lift_index: int | None = None
    selected_lift_source_matches_current: bool | None = None
    selected_lift_target_repr: str | None = None
    quotient_action_cell_count: int = 0
    pointwise_executable_action_cell_count: int = 0


@dataclass(frozen=True)
class FullTrainingABCSelectionEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    seed_bundle_id: str
    training_replicate_index: int
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
class FullTrainingABCTierSignalEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    seed_bundle_id: str
    training_replicate_index: int
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
    liftability_semantics_id: str = ""
    executable_semantics: str = ""
    quotient_action_cell_count: int = 0
    pointwise_executable_action_cell_count: int = 0


@dataclass(frozen=True)
class FullTrainingLearnerUpdateEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    seed_bundle_id: str
    training_replicate_index: int
    episode_index: int
    controller_event_index: int
    active_tier: int | None
    success: bool
    td_error: float | None
    update_reason: str


@dataclass(frozen=True)
class FullTrainingTowerShapeSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    training_replicate_index: int
    tier_index: int
    state_cell_count: int
    active_action_cell_count: int
    raw_historical_action_cell_record_count: int
    largest_state_cell_share: float
    full_collapse: bool
    liftability_semantics_id: str = ""
    executable_semantics: str = ""
    raw_action_cell_storage_count: int = 0


@dataclass(frozen=True)
class FullTrainingCurveSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    training_replicate_index: int
    episode_window_start: int
    episode_window_end: int
    mean_total_reward: float | None
    mean_concrete_step_count: float | None
    mean_lift_success_share: float | None
    mean_selected_deepest_tier_share: float | None
    mean_deepest_tier_concrete_step_share: float | None
    zero_step_episode_count: int
    learner_update_count: int


@dataclass(frozen=True)
class FullTrainingTierOccupancySummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    training_replicate_index: int
    tier_index: int | None
    control_action: str
    event_count: int
    event_share: float
    concrete_step_count: int
    concrete_step_share: float
    mean_reward_on_concrete_steps: float | None


@dataclass(frozen=True)
class FullTrainingTierExecutabilitySummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    training_replicate_index: int
    tier_index: int
    event_count: int
    executable_event_count: int
    executable_event_share: float | None
    selected_event_count: int


@dataclass(frozen=True)
class FullTrainingLiftByTierRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    training_replicate_index: int
    active_tier: int | None
    failure_reason: str | None
    fiber_departure_reason: str | None
    lift_attempt_count: int
    lift_success_count: int
    lift_failure_count: int
    mean_candidate_count: float | None


@dataclass(frozen=True)
class FullTrainingConcreteStepSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    training_replicate_index: int
    episode_count: int
    concrete_step_count: int
    zero_step_episode_count: int
    mean_reward: float | None
    terminated_count: int
    truncated_count: int
    final_state_summary: str


@dataclass(frozen=True)
class FullTrainingControlActionSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    training_replicate_index: int
    control_action: str
    event_count: int
    event_share: float


@dataclass(frozen=True)
class FullTrainingABCSelectionSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    training_replicate_index: int
    selected_tier: int | None
    predicted_movement_direction: str
    control_action: str
    blocked_reason: str | None
    event_count: int
    action_consistent_count: int
    action_consistent_share: float | None


@dataclass(frozen=True)
class FullTrainingABCTierSignalSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    training_replicate_index: int
    tier_index: int
    event_count: int
    executable_event_share: float | None
    unclosed_event_share: float | None
    mean_productive_learning_pressure: float | None
    selected_event_count: int
    active_event_count: int


@dataclass(frozen=True)
class FullTrainingLearnerUpdateSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    training_replicate_index: int
    update_count: int
    successful_update_count: int
    mean_td_error: float | None


@dataclass(frozen=True)
class FullTrainingHealthSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    status: str
    training_health_class: str
    artifact_complete: bool
    tower_noncollapsed: bool
    deepest_tier_executable: bool
    concrete_steps_positive: bool
    lift_successes_positive: bool
    learner_updates_positive: bool
    zero_step_episode_share: float | None
    no_available_action_event_count: int
    selected_tier_non_executability_count: int
    claim_if_met: str
    claim_if_not_met: str


@dataclass(frozen=True)
class FullTrainingAggregateTableRow(FlatRow):
    evaluation_id: str
    run_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    training_replicate_index: int
    status: str
    training_health_class: str
    concrete_step_count: int
    lift_success_count: int
    learner_update_count: int
    zero_step_episode_share: float | None
    selected_tier_non_executability_count: int
    no_available_action_event_count: int
    artifact_root: str
    failure_reason: str | None
