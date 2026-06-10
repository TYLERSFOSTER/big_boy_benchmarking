"""CSV schemas for Warehouse masked direct/live-lift tower artifacts."""

EPISODE_FIELDNAMES = (
    "run_id",
    "arm_id",
    "replicate_index",
    "schema_seed",
    "episode_index",
    "status",
    "failure_reason",
    "total_reward",
    "initial_correct_box_count",
    "final_correct_box_count",
    "initial_correct_robot_count",
    "final_correct_robot_count",
    "terminal_success",
    "terminated",
    "truncated",
    "selected_step_count",
    "valid_selected_step_count",
    "invalid_selected_step_count",
)

STEP_FIELDNAMES = (
    "run_id",
    "arm_id",
    "replicate_index",
    "schema_seed",
    "episode_index",
    "step_index",
    "state_id",
    "selected_action_id",
    "selected_action_summary",
    "valid",
    "reward",
    "terminated",
    "truncated",
    "next_state_id",
    "correct_box_count",
    "correct_robot_count",
    "invalid_reasons",
)

DIRECT_CANDIDATE_FIELDNAMES = (
    "run_id",
    "arm_id",
    "episode_index",
    "step_index",
    "state_id",
    "candidate_id",
    "candidate_generation_policy_id",
    "candidate_generation_scope",
    "candidate_generation_budget",
    "candidate_rank",
    "candidate_action_id",
    "candidate_action_summary",
    "is_all_stay",
    "active_robot_count",
    "candidate_family",
    "candidate_mix_id",
    "max_active_robots",
    "generation_complete_for_scope",
)

DIRECT_MASK_FIELDNAMES = (
    "run_id",
    "arm_id",
    "episode_index",
    "step_index",
    "state_id",
    "candidate_generation_policy_id",
    "candidate_count_before_mask",
    "candidate_count_after_mask",
    "inadmissible_candidate_count",
    "admissibility_query_count",
    "cache_hit_count",
    "selected_action_id",
    "selected_action_admissible",
    "mask_scope",
    "mask_policy_id",
    "successor_out_count_used_for_selection",
)

TOWER_STATE_LIFT_FIELDNAMES = (
    "run_id",
    "arm_id",
    "episode_index",
    "step_index",
    "downstairs_state_id",
    "tier",
    "state_cell_id",
    "fiber_candidate_count",
    "live_lift_candidate_count",
    "dead_lift_candidate_count",
    "selected_lift_state_id",
    "selected_lift_out_count",
    "lift_failure",
    "failure_reason",
    "out_scope",
    "lift_policy_id",
)

TOWER_ACTION_MASK_FIELDNAMES = (
    "run_id",
    "arm_id",
    "episode_index",
    "step_index",
    "tier",
    "state_cell_id",
    "tower_candidate_action_count_before_mask",
    "tower_candidate_action_count_after_mask",
    "inadmissible_tower_action_count",
    "selected_tower_action_id",
    "selected_concrete_action_id",
    "selected_concrete_action_admissible",
    "mask_scope",
    "mask_policy_id",
    "successor_out_count_used_for_selection",
)

SUCCESSOR_DIAGNOSTIC_FIELDNAMES = (
    "run_id",
    "arm_id",
    "episode_index",
    "step_index",
    "selected_action_id",
    "successor_state_id",
    "successor_out_count_observed",
    "successor_out_scope",
    "successor_out_count_used_for_selection",
    "selection_policy_id",
    "selection_policy_description",
)

LEARNER_UPDATE_FIELDNAMES = (
    "run_id",
    "arm_id",
    "episode_index",
    "step_index",
    "learner_key",
    "previous_value",
    "reward",
    "next_estimate",
    "new_value",
    "controller_policy_id",
)

TIMING_SEGMENT_FIELDNAMES = (
    "run_id",
    "arm_id",
    "segment",
    "duration_seconds",
)

RUN_INDEX_FIELDNAMES = (
    "run_id",
    "arm_id",
    "replicate_index",
    "schema_seed",
    "episode_count",
    "max_seconds_per_episode",
    "candidate_proposals_per_step",
    "max_active_robots",
    "candidate_mix_id",
    "run_root",
    "status",
    "failure_reason",
)

ARM_SUMMARY_FIELDNAMES = (
    "arm_id",
    "run_count",
    "episode_count",
    "mean_total_reward",
    "median_total_reward",
    "terminal_success_count",
    "mean_final_correct_box_count",
    "mean_final_correct_robot_count",
    "mean_valid_selected_step_count",
    "mean_invalid_selected_step_count",
    "mean_candidate_count_before_mask",
    "mean_candidate_count_after_mask",
    "mean_admissibility_query_count",
)

PAIRED_SUMMARY_FIELDNAMES = (
    "pair_id",
    "direct_run_id",
    "tower_run_id",
    "reward_delta_tower_minus_direct",
    "correct_box_delta_tower_minus_direct",
    "correct_robot_delta_tower_minus_direct",
    "terminal_success_delta",
    "valid_step_delta",
    "candidate_count_delta",
    "query_count_delta",
    "score_direction",
)

TARGET_PROGRESS_FIELDNAMES = (
    "arm_id",
    "mean_initial_correct_boxes",
    "mean_final_correct_boxes",
    "mean_box_progress",
    "mean_initial_correct_robots",
    "mean_final_correct_robots",
    "mean_robot_progress",
    "terminal_success_count",
)

ADMISSIBILITY_QUERY_SUMMARY_FIELDNAMES = (
    "arm_id",
    "candidate_generation_policy_id",
    "mask_scope",
    "total_candidates_before_mask",
    "total_candidates_after_mask",
    "total_inadmissible_candidates",
    "total_admissibility_queries",
    "total_cache_hits",
    "mean_candidates_before_mask_per_step",
    "mean_candidates_after_mask_per_step",
)

CANDIDATE_FAMILY_SUMMARY_FIELDNAMES = (
    "arm_id",
    "candidate_family",
    "active_robot_count",
    "candidate_count",
    "mean_candidate_rank",
    "candidate_mix_id",
    "max_active_robots",
)

TOWER_LIVE_LIFT_SUMMARY_FIELDNAMES = (
    "arm_id",
    "tier",
    "total_fiber_candidates",
    "total_live_lift_candidates",
    "total_dead_lift_candidates",
    "live_lift_failure_count",
    "mean_selected_lift_out_count",
    "out_scope",
)

NO_LOOKAHEAD_AUDIT_FIELDNAMES = (
    "arm_id",
    "selected_step_count",
    "successor_out_observed_count",
    "successor_out_used_for_selection_count",
    "no_lookahead_pass",
)

TOWER_SURFACE_SCOPE_FIELDNAMES = (
    "run_id",
    "schema_seed",
    "surface_scope",
    "surface_generation_policy_id",
    "surface_generation_budget",
    "max_active_robots",
    "candidate_mix_id",
    "state_count",
    "generated_candidate_count",
    "valid_edge_count",
    "invalid_candidate_count",
    "complete_full_action_surface",
    "complete_generated_candidate_surface",
)

TOWER_SHAPE_FIELDNAMES = (
    "run_id",
    "schema_seed",
    "schema_id",
    "schema_mode",
    "ratio_numerator",
    "ratio_denominator",
    "max_iterations",
    "tier_count",
    "tier",
    "state_cell_count",
    "action_cell_count",
    "valid_edge_count",
    "surface_scope",
    "complete_full_action_surface",
)
