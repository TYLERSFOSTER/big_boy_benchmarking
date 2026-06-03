"""Flat row contracts for the second serious schema comparison."""

from __future__ import annotations

from dataclasses import dataclass

from big_boy_benchmarking.metrics.events import FlatRow


@dataclass(frozen=True)
class ComparisonRunIndexRow(FlatRow):
    evaluation_id: str
    run_id: str
    run_mode: str
    candidate_group_id: str
    schema_class_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    seed_bundle_id: str
    training_replicate_index: int
    status: str
    artifact_root: str
    started_at: str
    ended_at: str | None
    failure_reason: str | None = None


@dataclass(frozen=True)
class ComparisonCandidateSummaryRow(FlatRow):
    evaluation_id: str
    candidate_group_id: str
    schema1_candidate_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
    schema_seed: int
    tier_state_cell_count_sequence: str
    tier_active_action_cell_count_sequence: str
    parent_training_health_class: str
    parent_concrete_step_count: int
    parent_learner_update_count: int
    selected: bool
    exclusion_reason: str | None


@dataclass(frozen=True)
class ComparisonEpisodeRow(FlatRow):
    evaluation_id: str
    run_id: str
    run_mode: str
    candidate_group_id: str
    schema_class_id: str
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
class ComparisonStepRow(FlatRow):
    evaluation_id: str
    run_id: str
    run_mode: str
    candidate_group_id: str
    schema_class_id: str
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
class ComparisonControlEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    run_mode: str
    candidate_group_id: str
    schema_class_id: str
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
class ComparisonLiftFiberEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    run_mode: str
    candidate_group_id: str
    schema_class_id: str
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


@dataclass(frozen=True)
class ComparisonABCSelectionEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    run_mode: str
    candidate_group_id: str
    schema_class_id: str
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
class ComparisonABCTierSignalEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    run_mode: str
    candidate_group_id: str
    schema_class_id: str
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


@dataclass(frozen=True)
class ComparisonLearnerUpdateEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    run_mode: str
    candidate_group_id: str
    schema_class_id: str
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
class ComparisonTierTransitionEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    run_mode: str
    candidate_group_id: str
    schema_class_id: str
    candidate_id: str
    episode_index: int
    controller_event_index: int
    active_tier_before: int | None
    active_tier_after: int | None
    tier_jump_policy_id: str
    tier_jump_reward_cutoff: float | None
    transition_observed: bool
    applicability: str


@dataclass(frozen=True)
class ComparisonTowerShapeSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    run_mode: str
    candidate_group_id: str
    schema_class_id: str
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


@dataclass(frozen=True)
class ThresholdWindowEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    run_mode: str
    candidate_group_id: str
    schema_class_id: str
    candidate_id: str
    training_replicate_index: int
    episode_window_start: int
    episode_window_end: int
    threshold_policy_id: str
    threshold_value: float
    threshold_hit_count: int
    required_count: int
    window_length: int
    window_met: bool
    window_mean_total_reward: float | None
    window_min_total_reward: float | None


@dataclass(frozen=True)
class FirstSustainedHitSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    run_mode: str
    candidate_group_id: str
    schema_class_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    training_replicate_index: int
    threshold_policy_id: str
    hit_metric_id: str
    hit_threshold_value: float
    hit_persistence_rule_id: str
    hit_persistence_window_length: int
    hit_persistence_required_count: int
    first_hit_episode_index: int | None
    first_sustained_hit_episode_index: int | None
    first_sustained_hit_training_step: int | None
    hit_status: str
    episodes_to_sustained_hit: int | None
    training_steps_to_sustained_hit: int | None
    post_hit_window_mean: float | None
    post_hit_window_min: float | None
    post_hit_window_success_count: int | None
    hit_failure_reason: str | None


@dataclass(frozen=True)
class ComparisonAggregateTableRow(FlatRow):
    evaluation_id: str
    run_id: str
    run_mode: str
    candidate_group_id: str
    schema_class_id: str
    candidate_id: str
    instance_id: str
    arm_id: str
    schema_seed: int
    training_replicate_index: int
    status: str
    hit_status: str
    first_sustained_hit_episode_index: int | None
    episodes_to_sustained_hit: int | None
    mean_total_reward: float | None
    concrete_step_count: int
    lift_success_count: int
    learner_update_count: int
    structural_limit_classification: str
    artifact_root: str
    failure_reason: str | None


@dataclass(frozen=True)
class ArmSummaryRow(FlatRow):
    evaluation_id: str
    schema_class_id: str
    run_count: int
    sustained_hit_count: int
    transient_hit_count: int
    never_hit_count: int
    artifact_incomplete_count: int
    sustained_hit_rate: float | None
    median_episodes_to_sustained_hit: float | None


@dataclass(frozen=True)
class PairedSchemaComparisonRow(FlatRow):
    evaluation_id: str
    candidate_group_id: str
    seed_bundle_id: str
    training_replicate_index: int
    schema0_run_id: str
    schema1_run_id: str
    schema0_hit_status: str
    schema1_hit_status: str
    schema0_episodes_to_hit: int | None
    schema1_episodes_to_hit: int | None
    schema1_minus_schema0_episodes_to_hit: int | None
    pair_status: str
    claim_blocked: bool
    interpretation: str


@dataclass(frozen=True)
class ComparisonClaimSummaryRow(FlatRow):
    evaluation_id: str
    run_mode: str
    pair_count: int
    unblocked_pair_count: int
    schema1_faster_pair_count: int
    schema1_slower_pair_count: int
    same_status_pair_count: int
    blocked_pair_count: int
    claim_status: str
    bounded_claim_text: str
