"""Event-table schemas for PlateSupport gauntlet Stage 4."""

from __future__ import annotations

EPISODE_FIELDS = (
    "candidate_id",
    "schema_id",
    "run_id",
    "replicate_index",
    "episode_index",
    "episode_seed",
    "status",
    "step_count",
    "total_reward",
    "terminated",
    "truncated",
    "goal_reached",
    "blocked_reason",
)

CONCRETE_STEP_FIELDS = (
    "candidate_id",
    "schema_id",
    "run_id",
    "replicate_index",
    "episode_index",
    "step_index",
    "source_state",
    "action_index",
    "target_state",
    "reward",
    "terminated",
    "truncated",
    "valid_transition",
    "invalid_move",
    "self_transition",
    "lift_status",
)

LIFT_FIBER_FIELDS = (
    "candidate_id",
    "schema_id",
    "run_id",
    "replicate_index",
    "episode_index",
    "step_index",
    "tier",
    "state_cell_id",
    "action_cell_id",
    "candidate_lift_count",
    "executable_lift_count",
    "selected_lift_source",
    "selected_lift_target",
    "selected_action_index",
    "lift_status",
    "failure_reason",
)

TIER_TRANSITION_FIELDS = (
    "candidate_id",
    "schema_id",
    "run_id",
    "replicate_index",
    "episode_index",
    "step_index",
    "tier_before",
    "tier_after",
    "state_cell_before",
    "state_cell_after",
    "active_action_cell_count",
    "blocked_reason",
)

CONTROLLER_ACTION_FIELDS = (
    "candidate_id",
    "schema_id",
    "run_id",
    "replicate_index",
    "episode_index",
    "step_index",
    "tier",
    "state_cell_id",
    "action_cell_id",
    "action_index",
    "selection_mode",
    "q_value_before",
)

LEARNER_UPDATE_FIELDS = (
    "candidate_id",
    "schema_id",
    "run_id",
    "replicate_index",
    "episode_index",
    "step_index",
    "learner_state_key",
    "learner_action_key",
    "reward",
    "next_state_best_value",
    "td_error",
    "old_value",
    "new_value",
    "update_applied",
)

TIMING_FIELDS = (
    "candidate_id",
    "schema_id",
    "run_id",
    "segment_name",
    "duration_seconds",
)
