"""Flat rows for counterpoint noisy-rate contraction diagnostics."""

from __future__ import annotations

from dataclasses import dataclass

from big_boy_benchmarking.metrics.events import FlatRow


@dataclass(frozen=True)
class NoisyRateEvaluationRunIndexRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
    schema_seed: int
    seed_bundle_id: str
    replicate_index: int
    status: str
    artifact_root: str
    started_at: str
    ended_at: str | None
    failure_reason: str | None = None


@dataclass(frozen=True)
class NoisyRateEpisodeRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
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
class NoisyRateStepRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
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
class NoisyRateControlEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
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
class NoisyRateLiftFiberEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
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
class NoisyRateABCSelectionEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
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
class NoisyRateABCTierSignalEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
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
class NoisyRateSelectionSummaryRow(FlatRow):
    evaluation_id: str
    environment_family_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
    schema_seed: int
    base_state_count: int
    base_edge_count: int
    selected_edge_count: int
    realized_selected_edge_share: float
    expected_selected_edge_count: float
    selected_edge_count_residual_from_expectation: float
    construction_rule: str
    block_id: str


@dataclass(frozen=True)
class NoisyRateSourceCoverageSummaryRow(FlatRow):
    evaluation_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
    schema_seed: int
    source_count_with_outgoing_edges: int
    source_count_with_selected_edges: int
    zero_selected_source_count: int
    selected_source_share: float | None
    realized_zero_source_share: float | None
    min_selected_edges_per_source: int | None
    mean_selected_edges_per_source: float | None
    max_selected_edges_per_source: int | None
    selected_edge_count_histogram_by_source: str
    source_out_degree_histogram: str
    selected_source_out_degree_histogram: str
    expected_zero_source_share: float | None
    source_coverage_class: str


@dataclass(frozen=True)
class NoisyRateSelectionConsistencySummaryRow(FlatRow):
    evaluation_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
    schema_seed: int
    metadata_selected_edge_count: int
    runtime_selected_edge_count: int
    selection_sets_equal: bool
    missing_from_runtime_count: int
    extra_in_runtime_count: int
    missing_from_runtime_examples: str
    extra_in_runtime_examples: str


@dataclass(frozen=True)
class NoisyRateMonotonicitySummaryRow(FlatRow):
    evaluation_id: str
    instance_id: str
    selector_rule_id: str
    schema_seed: int
    from_arm_id: str
    to_arm_id: str
    from_numerator: int
    from_denominator: int
    to_numerator: int
    to_denominator: int
    from_requested_rate: float
    to_requested_rate: float
    subset_pass: bool
    missing_nested_edge_count: int
    example_offending_edge_keys: str


@dataclass(frozen=True)
class NoisyRateThresholdSummaryRow(FlatRow):
    evaluation_id: str
    instance_id: str
    selector_rule_id: str
    schema_seed: int
    first_full_collapse_arm_id: str | None
    first_full_collapse_rate: float | None
    first_near_collapse_arm_id: str | None
    first_near_collapse_rate: float | None
    last_nontrivial_arm_id: str | None
    last_nontrivial_rate: float | None
    first_high_source_coverage_arm_id: str | None
    first_high_source_coverage_rate: float | None
    source_coverage_at_first_full_collapse: float | None
    selected_edge_share_at_first_full_collapse: float | None
    selected_edge_count_at_first_full_collapse: int | None
    useful_coalescence_count_at_first_full_collapse: int | None
    first_singleton_edge_index_at_first_full_collapse: int | None
    sweep_verdict: str


@dataclass(frozen=True)
class NoisyRateTowerShapeSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
    schema_seed: int
    replicate_index: int
    tier_index: int
    state_cell_count: int
    active_action_cell_count: int
    raw_historical_action_cell_record_count: int
    base_state_count: int
    base_edge_count: int
    state_compression_ratio: float
    largest_state_cell_size: int
    largest_state_cell_share: float
    singleton_state_cell_count: int
    singleton_base_state_share: float
    state_cell_size_histogram: str
    full_collapse: bool
    near_collapse: bool
    degeneracy_class: str


@dataclass(frozen=True)
class EndpointCoalescenceSummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
    schema_seed: int
    replicate_index: int
    selected_edge_count: int
    source_count_with_selected_edges: int
    zero_selected_source_count: int
    realized_source_coverage: float | None
    processed_edge_count: int
    useful_coalescence_count: int
    redundant_or_internal_edge_count: int
    state_cell_count_after_block: int
    largest_coalesced_cell_size: int
    largest_coalesced_cell_share: float
    processed_edge_index_at_first_singleton: int | None
    collapse_required_most_of_block: bool | None


@dataclass(frozen=True)
class TierExecutabilitySummaryRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
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
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
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
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
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
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
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
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
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
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
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
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
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
class NoisyRateAggregateTableRow(FlatRow):
    evaluation_id: str
    run_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
    schema_seed: int
    replicate_index: int
    status: str
    selected_edge_count: int | None
    selected_edge_share: float | None
    selected_source_share: float | None
    zero_selected_source_count: int | None
    selection_sets_equal: bool | None
    first_projection_largest_state_cell_share: float | None
    full_first_projection_collapse: bool
    near_full_first_projection_collapse: bool
    selected_tier_non_executability_count: int
    no_available_action_count: int
    zero_concrete_steps: bool
    missing_abc_context: bool
    structural_limit_classification: str
