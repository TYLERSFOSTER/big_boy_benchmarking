"""Event table schemas for Warehouse full-tower PPO."""

RUN_INDEX_FIELDNAMES = [
    "run_id",
    "arm_id",
    "replicate_index",
    "schema_seed",
    "seed",
    "status",
    "run_root",
]

EPISODE_FIELDNAMES = [
    "run_id",
    "arm_id",
    "replicate_index",
    "schema_seed",
    "episode_index",
    "max_seconds",
    "seconds_elapsed",
    "step_count",
    "total_reward",
    "terminated",
    "truncated",
    "failure_reason",
    "ppo_sample_count",
    "controller_event_count",
    "pointwise_surface_count",
    "empty_actor_surface_count",
    "tier_indices_seen",
    "retained_trace_count",
    "optimizer_steps",
]

STEP_FIELDNAMES = [
    "run_id",
    "arm_id",
    "replicate_index",
    "schema_seed",
    "episode_index",
    "step_index",
    "state_id",
    "selected_action_id",
    "selected_action_vector_hash",
    "selected_action_summary",
    "valid",
    "reward",
    "terminated",
    "truncated",
    "next_state_id",
    "correct_box_count",
    "correct_robot_count",
    "invalid_reasons",
    "tier_index",
    "selected_local_index",
    "candidate_action_count",
]

CONTROLLER_EVENT_FIELDNAMES = [
    "run_id",
    "arm_id",
    "episode_index",
    "controller_event_index",
    "event_type",
    "tier_index",
    "state_cell_id",
    "candidate_action_count",
    "details",
]

POINTWISE_SURFACE_FIELDNAMES = [
    "run_id",
    "arm_id",
    "episode_index",
    "step_index",
    "schema_id",
    "schema_seed",
    "tier_index",
    "state_cell_id",
    "candidate_action_count",
    "generated_candidate_count",
    "valid_candidate_count",
    "invalid_candidate_count",
    "surface_scope",
    "mask_kind",
    "semantics_id",
    "tier_direction_convention",
    "current_position_at_every_tier",
]

ROLLOUT_SAMPLE_FIELDNAMES = [
    "rollout_sample_id",
    "decision_context_id",
    "run_id",
    "arm_id",
    "episode_index",
    "tier_index",
    "policy_snapshot_id",
    "rollout_policy_snapshot_id",
    "selected_local_index",
    "selected_action_cell_id",
    "old_log_prob",
    "value_estimate",
    "entropy",
    "reward",
    "terminated",
    "truncated",
    "diagnostic_failure_code",
]

PPO_UPDATE_FIELDNAMES = [
    "run_id",
    "arm_id",
    "global_update_index",
    "tier_index",
    "sample_count",
    "optimizer_steps",
    "policy_loss",
    "value_loss",
    "entropy",
    "approx_kl",
    "clip_fraction",
    "grad_norm",
    "device",
    "skipped",
    "skip_reason",
]

TIER_POLICY_FIELDNAMES = [
    "run_id",
    "arm_id",
    "tier_index",
    "hidden_dim",
    "policy_snapshot_id",
    "rollout_policy_snapshot_id",
    "optimizer_steps",
    "parameter_count",
]

TIMING_FIELDNAMES = [
    "run_id",
    "arm_id",
    "duration_seconds",
    "episode_count",
]

TRACE_INDEX_FIELDNAMES = [
    "run_id",
    "arm_id",
    "replicate_index",
    "schema_seed",
    "episode_index",
    "trace_path",
    "reason_retained",
    "step_count",
    "renderability_status",
]
