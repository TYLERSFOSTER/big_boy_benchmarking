"""Aggregation for the PlateSupport tower-star guarded lift diagnostic."""

from __future__ import annotations

from collections import defaultdict

from .config import (
    CLAIM_BOUNDARY,
    DIRECT_INVALID_GUARD_ARM_ID,
    DIRECT_NONSELF_GUARD_ARM_ID,
    DIRECT_RAW_ARM_ID,
    TOWER_INVALID_GUARD_ARM_ID,
    TOWER_LIFT_EXECUTABLE_CURRENT_ARM_ID,
    TOWER_NONSELF_GUARD_ARM_ID,
)
from .events import (
    CONTROLLER_FIELDS,
    EPISODE_FIELDS,
    GUARD_EVENT_FIELDS,
    LEARNER_FIELDS,
    LIFT_FIELDS,
    STEP_FIELDS,
    TIER_FIELDS,
    TIMING_FIELDS,
)
from .manifests import ARM_MANIFEST_FIELDS, TowerStarArm

RESULT_TABLE_FIELDNAMES = {
    "paired_seed_bundle_summary": (
        "pair_id",
        "replicate_index",
        "environment_seed",
        "learner_seed",
        "exploration_seed",
        "initial_state_seed",
        "tie_break_seed",
    ),
    "evaluation_run_index": (
        "run_id",
        "pair_id",
        "arm_id",
        "arm_type",
        "guard_type",
        "candidate_id",
        "schema_id",
        "replicate_index",
        "status",
        "episode_count",
        "target_hit_count",
        "artifact_root",
        "required_file_count",
        "present_file_count",
        "artifact_complete",
    ),
    "evaluation_arm_manifest": ARM_MANIFEST_FIELDS,
    "arm_summary": (
        "arm_id",
        "arm_type",
        "guard_type",
        "candidate_id",
        "schema_id",
        "replicate_count",
        "episode_count",
        "target_hit_count",
        "target_hit_rate",
        "goal_success_count",
        "goal_success_rate",
        "mean_total_reward",
        "mean_step_count",
        "total_concrete_steps",
        "invalid_move_count",
        "invalid_move_rate",
        "self_transition_count",
        "self_transition_rate",
        "valid_clipped_self_transition_count",
        "nonself_transition_count",
        "blocked_episode_count",
        "guard_fallback_count",
        "claim_boundary",
    ),
    "guard_filter_summary": (
        "arm_id",
        "guard_type",
        "information_mode",
        "event_count",
        "mean_available_before_guard",
        "mean_available_after_guard",
        "mean_invalid_filtered",
        "mean_self_loop_filtered",
        "min_available_after_guard",
        "max_available_after_guard",
        "all_actions_filtered_count",
        "guard_fallback_count",
    ),
    "self_loop_summary": (
        "arm_id",
        "invalid_self_loop_count",
        "valid_clipped_self_loop_count",
        "total_self_loop_count",
        "total_self_loop_rate",
        "states_with_self_loop_events",
        "top_self_loop_states",
    ),
    "invalid_vs_self_loop_summary": (
        "arm_id",
        "concrete_step_count",
        "invalid_move_count",
        "valid_clipped_self_transition_count",
        "valid_nonself_transition_count",
        "invalid_move_rate",
        "valid_clipped_self_transition_rate",
        "valid_nonself_transition_rate",
    ),
    "paired_guard_comparison": (
        "pair_id",
        "replicate_index",
        "baseline_arm_id",
        "comparison_arm_id",
        "pair_complete",
        "baseline_target_hit_rate",
        "comparison_target_hit_rate",
        "target_hit_rate_delta",
        "baseline_mean_total_reward",
        "comparison_mean_total_reward",
        "mean_total_reward_delta",
        "baseline_invalid_move_rate",
        "comparison_invalid_move_rate",
        "invalid_move_rate_delta",
        "baseline_self_transition_rate",
        "comparison_self_transition_rate",
        "self_transition_rate_delta",
        "claim_boundary",
    ),
    "paired_star_comparison": (
        "comparison_id",
        "left_arm_id",
        "right_arm_id",
        "metric",
        "left_value",
        "right_value",
        "delta_right_minus_left",
        "direction",
        "interpretation_flag",
    ),
    "action_surface_summary": (
        "arm_id",
        "guard_type",
        "information_mode",
        "mean_available_action_count",
        "min_available_action_count",
        "max_available_action_count",
        "mean_invalid_filtered_count",
        "mean_self_loop_filtered_count",
        "event_count",
    ),
    "direct_guard_filter_summary": (
        "arm_id",
        "guard_type",
        "information_mode",
        "event_count",
        "mean_available_before_guard",
        "mean_available_after_guard",
        "mean_invalid_filtered",
        "mean_self_loop_filtered",
        "min_available_after_guard",
        "max_available_after_guard",
        "all_actions_filtered_count",
        "guard_fallback_count",
    ),
    "tower_lift_guard_summary": LIFT_FIELDS,
    "tower_action_cell_surface_summary": (
        "arm_id",
        "tier_index",
        "decision_count",
        "mean_action_cells_before_star",
        "mean_action_cells_after_star",
        "mean_action_cells_removed_by_star",
        "max_action_cells_removed_by_star",
        "states_with_no_cells_before_star",
        "states_with_no_cells_after_star",
        "blocked_decision_count",
        "blocked_decision_rate",
    ),
    "lift_pool_mixing_summary": (
        "arm_id",
        "tier_index",
        "action_cell_count",
        "all_clean_cell_count",
        "mixed_clean_and_bad_cell_count",
        "only_invalid_cell_count",
        "only_self_loop_cell_count",
        "only_bad_cell_count",
        "mean_clean_lift_fraction",
        "mean_nonself_lift_fraction",
    ),
    "star_surface_blockage_summary": (
        "arm_id",
        "blocked_episode_count",
        "blocked_decision_count",
        "first_blocked_step_min",
        "first_blocked_step_median",
        "blocked_reason",
        "comparison_usable",
    ),
    "interpretation_summary": (
        "evaluation_id",
        "run_label",
        "primary_interpretation_case",
        "interpretation_case",
        "primary_target_comparison",
        "primary_target_delta",
        "tower_star_surface_blocked",
        "tower_current_star_clean_flag",
        "direct_star_still_explains_signal_flag",
        "tower_survives_star_control_flag",
        "tower_vs_raw_delta",
        "tower_vs_invalid_guard_delta",
        "tower_vs_nonself_guard_delta",
        "allowed_claim",
        "blocked_claim",
        "information_parity_warning",
    ),
    "badge_summary": (
        "badge_id",
        "label",
        "value",
        "color",
        "reason",
        "source",
    ),
    "timing_summary": (
        "arm_id",
        "run_id",
        "total_duration_seconds",
    ),
    "guard_events": GUARD_EVENT_FIELDS,
    "episode_summary": EPISODE_FIELDS,
    "step_summary": STEP_FIELDS,
    "controller_action_summary": CONTROLLER_FIELDS,
    "learner_update_summary": LEARNER_FIELDS,
    "lift_fiber_summary": LIFT_FIELDS,
    "tier_transition_summary": TIER_FIELDS,
    "timing_segments": TIMING_FIELDS,
}


def build_tower_star_tables(
    *,
    arms: tuple[TowerStarArm, ...],
    seed_rows: list[dict[str, object]],
    run_index_rows: list[dict[str, object]],
    episode_rows: list[dict[str, object]],
    step_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    controller_rows: list[dict[str, object]],
    learner_rows: list[dict[str, object]],
    lift_rows: list[dict[str, object]],
    tier_rows: list[dict[str, object]],
    timing_rows: list[dict[str, object]],
) -> dict[str, list[dict[str, object]]]:
    """Build result tables for the tower-star diagnostic."""

    arm_rows = [arm.to_row() for arm in arms]
    arm_summary = _arm_summary(arm_rows, episode_rows, step_rows, guard_rows)
    paired_guard = _paired_guard_comparison(episode_rows, step_rows)
    paired_star = _paired_star_comparison(arm_summary)
    blockage = _star_surface_blockage_summary(episode_rows, guard_rows)
    interpretation = _interpretation_summary(arm_summary, blockage)
    guard_filter = _guard_filter_summary(guard_rows)
    return {
        "paired_seed_bundle_summary": seed_rows,
        "evaluation_run_index": run_index_rows,
        "evaluation_arm_manifest": arm_rows,
        "arm_summary": arm_summary,
        "guard_filter_summary": guard_filter,
        "self_loop_summary": _self_loop_summary(step_rows),
        "invalid_vs_self_loop_summary": _invalid_vs_self_loop_summary(step_rows),
        "paired_guard_comparison": paired_guard,
        "paired_star_comparison": paired_star,
        "action_surface_summary": _action_surface_summary(guard_rows),
        "direct_guard_filter_summary": [
            row for row in guard_filter if str(row.get("arm_id", "")).startswith("direct_")
        ],
        "tower_lift_guard_summary": lift_rows,
        "tower_action_cell_surface_summary": _tower_action_cell_surface_summary(lift_rows),
        "lift_pool_mixing_summary": _lift_pool_mixing_summary(lift_rows),
        "star_surface_blockage_summary": blockage,
        "interpretation_summary": interpretation,
        "badge_summary": _badge_summary(interpretation, guard_rows, run_index_rows),
        "timing_summary": _timing_summary(timing_rows),
        "guard_events": guard_rows,
        "episode_summary": episode_rows,
        "step_summary": step_rows,
        "controller_action_summary": controller_rows,
        "learner_update_summary": learner_rows,
        "lift_fiber_summary": lift_rows,
        "tier_transition_summary": tier_rows,
        "timing_segments": timing_rows,
    }


def _arm_summary(
    arm_rows: list[dict[str, object]],
    episode_rows: list[dict[str, object]],
    step_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    episodes_by_arm = _group_by(episode_rows, "arm_id")
    steps_by_arm = _group_by(step_rows, "arm_id")
    guards_by_arm = _group_by(guard_rows, "arm_id")
    rows: list[dict[str, object]] = []
    for arm in arm_rows:
        arm_id = str(arm["arm_id"])
        episodes = episodes_by_arm.get(arm_id, [])
        steps = steps_by_arm.get(arm_id, [])
        guards = guards_by_arm.get(arm_id, [])
        hits = sum(_truthy(row.get("target_hit")) for row in episodes)
        goals = sum(_truthy(row.get("goal_reached")) for row in episodes)
        invalid = sum(_truthy(row.get("invalid_move")) for row in steps)
        self_transitions = sum(_truthy(row.get("self_transition")) for row in steps)
        clipped = sum(_truthy(row.get("valid_clipped_self_transition")) for row in steps)
        blocked = sum(str(row.get("status")) == "controller_blocked" for row in episodes)
        guard_fallback = sum(_truthy(row.get("guard_fallback_used")) for row in guards)
        rows.append(
            {
                "arm_id": arm_id,
                "arm_type": arm["arm_type"],
                "guard_type": arm["guard_type"],
                "candidate_id": arm["candidate_id"],
                "schema_id": arm["schema_id"],
                "replicate_count": len({row["replicate_index"] for row in episodes}),
                "episode_count": len(episodes),
                "target_hit_count": hits,
                "target_hit_rate": _ratio(hits, len(episodes)),
                "goal_success_count": goals,
                "goal_success_rate": _ratio(goals, len(episodes)),
                "mean_total_reward": _mean(float(row["total_reward"]) for row in episodes),
                "mean_step_count": _mean(float(row["step_count"]) for row in episodes),
                "total_concrete_steps": len(steps),
                "invalid_move_count": invalid,
                "invalid_move_rate": _ratio(invalid, len(steps)),
                "self_transition_count": self_transitions,
                "self_transition_rate": _ratio(self_transitions, len(steps)),
                "valid_clipped_self_transition_count": clipped,
                "nonself_transition_count": len(steps) - self_transitions,
                "blocked_episode_count": blocked,
                "guard_fallback_count": guard_fallback,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def _guard_filter_summary(
    guard_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for arm_id, group in _group_by(guard_rows, "arm_id").items():
        after = [float(row["available_action_count_after_guard"]) for row in group]
        rows.append(
            {
                "arm_id": arm_id,
                "guard_type": group[0].get("guard_type", "") if group else "",
                "information_mode": group[0].get("information_mode", "") if group else "",
                "event_count": len(group),
                "mean_available_before_guard": _mean(
                    float(row["available_action_count_before_guard"]) for row in group
                ),
                "mean_available_after_guard": _mean(after),
                "mean_invalid_filtered": _mean(
                    float(row["invalid_guard_filtered_count"]) for row in group
                ),
                "mean_self_loop_filtered": _mean(
                    float(row["self_loop_guard_filtered_count"]) for row in group
                ),
                "min_available_after_guard": min(after) if after else 0,
                "max_available_after_guard": max(after) if after else 0,
                "all_actions_filtered_count": sum(
                    int(row["all_actions_filtered_count"]) for row in group
                ),
                "guard_fallback_count": sum(
                    _truthy(row["guard_fallback_used"]) for row in group
                ),
            }
        )
    return rows


def _self_loop_summary(step_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for arm_id, group in _group_by(step_rows, "arm_id").items():
        invalid_self = [
            row
            for row in group
            if _truthy(row.get("invalid_move")) and _truthy(row.get("self_transition"))
        ]
        clipped = [row for row in group if _truthy(row.get("valid_clipped_self_transition"))]
        self_rows = [row for row in group if _truthy(row.get("self_transition"))]
        state_counts: dict[str, int] = defaultdict(int)
        for row in self_rows:
            state_counts[str(row.get("source_state", ""))] += 1
        top_states = ";".join(
            f"{state}:{count}"
            for state, count in sorted(
                state_counts.items(), key=lambda item: (-item[1], item[0])
            )[:5]
        )
        rows.append(
            {
                "arm_id": arm_id,
                "invalid_self_loop_count": len(invalid_self),
                "valid_clipped_self_loop_count": len(clipped),
                "total_self_loop_count": len(self_rows),
                "total_self_loop_rate": _ratio(len(self_rows), len(group)),
                "states_with_self_loop_events": len(state_counts),
                "top_self_loop_states": top_states,
            }
        )
    return rows


def _invalid_vs_self_loop_summary(
    step_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for arm_id, group in _group_by(step_rows, "arm_id").items():
        invalid = sum(_truthy(row.get("invalid_move")) for row in group)
        clipped = sum(_truthy(row.get("valid_clipped_self_transition")) for row in group)
        nonself = sum(not _truthy(row.get("self_transition")) for row in group)
        rows.append(
            {
                "arm_id": arm_id,
                "concrete_step_count": len(group),
                "invalid_move_count": invalid,
                "valid_clipped_self_transition_count": clipped,
                "valid_nonself_transition_count": nonself,
                "invalid_move_rate": _ratio(invalid, len(group)),
                "valid_clipped_self_transition_rate": _ratio(clipped, len(group)),
                "valid_nonself_transition_rate": _ratio(nonself, len(group)),
            }
        )
    return rows


def _paired_guard_comparison(
    episode_rows: list[dict[str, object]],
    step_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    pairs = (
        (TOWER_LIFT_EXECUTABLE_CURRENT_ARM_ID, DIRECT_RAW_ARM_ID),
        (TOWER_INVALID_GUARD_ARM_ID, DIRECT_INVALID_GUARD_ARM_ID),
        (TOWER_NONSELF_GUARD_ARM_ID, DIRECT_NONSELF_GUARD_ARM_ID),
        (DIRECT_INVALID_GUARD_ARM_ID, DIRECT_RAW_ARM_ID),
        (DIRECT_NONSELF_GUARD_ARM_ID, DIRECT_INVALID_GUARD_ARM_ID),
        (TOWER_INVALID_GUARD_ARM_ID, TOWER_LIFT_EXECUTABLE_CURRENT_ARM_ID),
        (TOWER_NONSELF_GUARD_ARM_ID, TOWER_INVALID_GUARD_ARM_ID),
    )
    by_pair_arm = _group_by_many(episode_rows, ("pair_id", "replicate_index", "arm_id"))
    steps_by_pair_arm = _group_by_many(step_rows, ("pair_id", "replicate_index", "arm_id"))
    pair_keys = sorted({(pair_id, replicate) for pair_id, replicate, _arm in by_pair_arm})
    rows: list[dict[str, object]] = []
    for pair_id, replicate_index in pair_keys:
        for comparison_arm_id, baseline_arm_id in pairs:
            baseline = by_pair_arm.get((pair_id, replicate_index, baseline_arm_id), [])
            comparison = by_pair_arm.get((pair_id, replicate_index, comparison_arm_id), [])
            baseline_steps = steps_by_pair_arm.get(
                (pair_id, replicate_index, baseline_arm_id), []
            )
            comparison_steps = steps_by_pair_arm.get(
                (pair_id, replicate_index, comparison_arm_id), []
            )
            complete = bool(baseline and comparison)
            baseline_hit = _hit_rate(baseline)
            comparison_hit = _hit_rate(comparison)
            baseline_invalid = _rate_by_flag(baseline_steps, "invalid_move")
            comparison_invalid = _rate_by_flag(comparison_steps, "invalid_move")
            baseline_self = _rate_by_flag(baseline_steps, "self_transition")
            comparison_self = _rate_by_flag(comparison_steps, "self_transition")
            rows.append(
                {
                    "pair_id": pair_id,
                    "replicate_index": replicate_index,
                    "baseline_arm_id": baseline_arm_id,
                    "comparison_arm_id": comparison_arm_id,
                    "pair_complete": "1" if complete else "0",
                    "baseline_target_hit_rate": baseline_hit,
                    "comparison_target_hit_rate": comparison_hit,
                    "target_hit_rate_delta": comparison_hit - baseline_hit,
                    "baseline_mean_total_reward": _mean(
                        float(row["total_reward"]) for row in baseline
                    ),
                    "comparison_mean_total_reward": _mean(
                        float(row["total_reward"]) for row in comparison
                    ),
                    "mean_total_reward_delta": _mean(
                        float(row["total_reward"]) for row in comparison
                    )
                    - _mean(float(row["total_reward"]) for row in baseline),
                    "baseline_invalid_move_rate": baseline_invalid,
                    "comparison_invalid_move_rate": comparison_invalid,
                    "invalid_move_rate_delta": comparison_invalid - baseline_invalid,
                    "baseline_self_transition_rate": baseline_self,
                    "comparison_self_transition_rate": comparison_self,
                    "self_transition_rate_delta": comparison_self - baseline_self,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def _action_surface_summary(
    guard_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for arm_id, group in _group_by(guard_rows, "arm_id").items():
        counts = [float(row["available_action_count_after_guard"]) for row in group]
        rows.append(
            {
                "arm_id": arm_id,
                "guard_type": group[0].get("guard_type", "") if group else "",
                "information_mode": group[0].get("information_mode", "") if group else "",
                "mean_available_action_count": _mean(counts),
                "min_available_action_count": min(counts) if counts else 0,
                "max_available_action_count": max(counts) if counts else 0,
                "mean_invalid_filtered_count": _mean(
                    float(row["invalid_guard_filtered_count"]) for row in group
                ),
                "mean_self_loop_filtered_count": _mean(
                    float(row["self_loop_guard_filtered_count"]) for row in group
                ),
                "event_count": len(group),
            }
        )
    return rows


def _paired_star_comparison(
    arm_summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    by_arm = {str(row.get("arm_id", "")): row for row in arm_summary}
    pairs = (
        (
            "direct_raw_vs_tower_current",
            DIRECT_RAW_ARM_ID,
            TOWER_LIFT_EXECUTABLE_CURRENT_ARM_ID,
        ),
        (
            "direct_invalid_vs_tower_invalid",
            DIRECT_INVALID_GUARD_ARM_ID,
            TOWER_INVALID_GUARD_ARM_ID,
        ),
        (
            "direct_nonself_vs_tower_nonself",
            DIRECT_NONSELF_GUARD_ARM_ID,
            TOWER_NONSELF_GUARD_ARM_ID,
        ),
        (
            "tower_current_vs_tower_invalid",
            TOWER_LIFT_EXECUTABLE_CURRENT_ARM_ID,
            TOWER_INVALID_GUARD_ARM_ID,
        ),
        (
            "tower_current_vs_tower_nonself",
            TOWER_LIFT_EXECUTABLE_CURRENT_ARM_ID,
            TOWER_NONSELF_GUARD_ARM_ID,
        ),
        (
            "direct_invalid_vs_direct_nonself",
            DIRECT_INVALID_GUARD_ARM_ID,
            DIRECT_NONSELF_GUARD_ARM_ID,
        ),
        (
            "tower_invalid_vs_tower_nonself",
            TOWER_INVALID_GUARD_ARM_ID,
            TOWER_NONSELF_GUARD_ARM_ID,
        ),
    )
    rows: list[dict[str, object]] = []
    for comparison_id, left_arm, right_arm in pairs:
        left_value = float(by_arm.get(left_arm, {}).get("target_hit_rate", 0.0) or 0.0)
        right_value = float(by_arm.get(right_arm, {}).get("target_hit_rate", 0.0) or 0.0)
        delta = right_value - left_value
        rows.append(
            {
                "comparison_id": comparison_id,
                "left_arm_id": left_arm,
                "right_arm_id": right_arm,
                "metric": "target_hit_rate",
                "left_value": left_value,
                "right_value": right_value,
                "delta_right_minus_left": delta,
                "direction": "right_higher" if delta > 0 else "left_higher" if delta < 0 else "tie",
                "interpretation_flag": _comparison_flag(comparison_id, delta),
            }
        )
    return rows


def _tower_action_cell_surface_summary(
    lift_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for (arm_id, tier), group in _group_by_many(lift_rows, ("arm_id", "tier")).items():
        decisions = _group_by_many(group, ("run_id", "episode_index", "step_index"))
        before_counts: list[float] = []
        after_counts: list[float] = []
        removed_counts: list[float] = []
        no_before = 0
        no_after = 0
        for decision_rows in decisions.values():
            before = sum(_truthy(row.get("action_cell_available_before_star")) for row in decision_rows)
            if str(arm_id) == TOWER_INVALID_GUARD_ARM_ID:
                after = sum(
                    _truthy(row.get("action_cell_available_after_invalid_star"))
                    for row in decision_rows
                )
            elif str(arm_id) == TOWER_NONSELF_GUARD_ARM_ID:
                after = sum(
                    _truthy(row.get("action_cell_available_after_nonself_star"))
                    for row in decision_rows
                )
            else:
                after = before
            before_counts.append(float(before))
            after_counts.append(float(after))
            removed_counts.append(float(before - after))
            no_before += 1 if before == 0 else 0
            no_after += 1 if after == 0 else 0
        rows.append(
            {
                "arm_id": arm_id,
                "tier_index": tier,
                "decision_count": len(decisions),
                "mean_action_cells_before_star": _mean(before_counts),
                "mean_action_cells_after_star": _mean(after_counts),
                "mean_action_cells_removed_by_star": _mean(removed_counts),
                "max_action_cells_removed_by_star": max(removed_counts) if removed_counts else 0,
                "states_with_no_cells_before_star": no_before,
                "states_with_no_cells_after_star": no_after,
                "blocked_decision_count": no_after,
                "blocked_decision_rate": _ratio(no_after, len(decisions)),
            }
        )
    return rows


def _lift_pool_mixing_summary(
    lift_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for (arm_id, tier), group in _group_by_many(lift_rows, ("arm_id", "tier")).items():
        all_clean = mixed = only_invalid = only_self = only_bad = 0
        clean_fracs: list[float] = []
        nonself_fracs: list[float] = []
        for row in group:
            executable = int(float(row.get("executable_lift_count") or 0))
            invalid_ok = int(float(row.get("invalid_guard_compatible_lift_count") or 0))
            nonself_ok = int(float(row.get("nonself_guard_compatible_lift_count") or 0))
            clean_fracs.append(_ratio(invalid_ok, executable))
            nonself_fracs.append(_ratio(nonself_ok, executable))
            if executable > 0 and nonself_ok == executable:
                all_clean += 1
            elif nonself_ok > 0 and nonself_ok < executable:
                mixed += 1
            elif executable > 0 and invalid_ok == 0:
                only_invalid += 1
                only_bad += 1
            elif executable > 0 and nonself_ok == 0:
                only_self += 1
                only_bad += 1
        rows.append(
            {
                "arm_id": arm_id,
                "tier_index": tier,
                "action_cell_count": len(group),
                "all_clean_cell_count": all_clean,
                "mixed_clean_and_bad_cell_count": mixed,
                "only_invalid_cell_count": only_invalid,
                "only_self_loop_cell_count": only_self,
                "only_bad_cell_count": only_bad,
                "mean_clean_lift_fraction": _mean(clean_fracs),
                "mean_nonself_lift_fraction": _mean(nonself_fracs),
            }
        )
    return rows


def _star_surface_blockage_summary(
    episode_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for arm_id, episodes in _group_by(episode_rows, "arm_id").items():
        blocked_episodes = [
            row for row in episodes if str(row.get("status", "")) == "controller_blocked"
        ]
        blocked_guards = [
            row
            for row in guard_rows
            if str(row.get("arm_id", "")) == str(arm_id)
            and _truthy(row.get("guard_fallback_used"))
        ]
        steps = [int(float(row.get("step_index") or 0)) for row in blocked_guards]
        rows.append(
            {
                "arm_id": arm_id,
                "blocked_episode_count": len(blocked_episodes),
                "blocked_decision_count": len(blocked_guards),
                "first_blocked_step_min": min(steps) if steps else "",
                "first_blocked_step_median": _median(steps) if steps else "",
                "blocked_reason": blocked_episodes[0].get("blocked_reason", "")
                if blocked_episodes
                else "",
                "comparison_usable": "0"
                if str(arm_id).startswith("tower_") and blocked_episodes
                else "1",
            }
        )
    return rows


def _interpretation_summary(
    arm_summary: list[dict[str, object]],
    blockage_summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    rate = {
        str(row["arm_id"]): float(row["target_hit_rate"])
        for row in arm_summary
    }
    tower_vs_raw = rate.get(TOWER_LIFT_EXECUTABLE_CURRENT_ARM_ID, 0.0) - rate.get(
        DIRECT_RAW_ARM_ID, 0.0
    )
    tower_vs_invalid = rate.get(TOWER_INVALID_GUARD_ARM_ID, 0.0) - rate.get(
        DIRECT_INVALID_GUARD_ARM_ID, 0.0
    )
    tower_vs_nonself = rate.get(TOWER_NONSELF_GUARD_ARM_ID, 0.0) - rate.get(
        DIRECT_NONSELF_GUARD_ARM_ID, 0.0
    )
    current_vs_nonself = rate.get(TOWER_NONSELF_GUARD_ARM_ID, 0.0) - rate.get(
        TOWER_LIFT_EXECUTABLE_CURRENT_ARM_ID, 0.0
    )
    tower_blocked = any(
        str(row.get("arm_id", "")).startswith("tower_")
        and str(row.get("comparison_usable", "")) == "0"
        for row in blockage_summary
    )
    tower_current_star_clean = abs(current_vs_nonself) < 1e-12
    if tower_blocked:
        case = "tower_star_surface_blocked"
        allowed = "tower-star surface blockage was detected and reported as diagnostic evidence"
        blocked = "behavioral tower-star comparison is usable without qualification"
    elif tower_vs_nonself > 0:
        case = "tower_survives_star_control"
        allowed = (
            "the selected tower candidate outperformed direct after both sides "
            "received one-step nonself star controls"
        )
        blocked = "general tower superiority is proven"
    elif tower_vs_nonself < 0:
        case = "direct_star_still_explains_signal"
        allowed = (
            "the prior PlateSupport signal is not yet separated from one-step "
            "local action filtering under this budget"
        )
        blocked = "the tower signal failed for all meaningful reasons"
    else:
        case = "inconclusive_small_margin"
        allowed = "the control surfaces are implemented but need larger or sharper budget"
        blocked = "the diagnostic resolves tower-vs-direct advantage"
    return [
        {
            "evaluation_id": "plate_support_tower_star_guarded_lift_comparison_v001",
            "run_label": "",
            "primary_interpretation_case": case,
            "interpretation_case": case,
            "primary_target_comparison": "direct_nonself_guard_vs_tower_nonself_guard",
            "primary_target_delta": tower_vs_nonself,
            "tower_star_surface_blocked": "1" if tower_blocked else "0",
            "tower_current_star_clean_flag": "1" if tower_current_star_clean else "0",
            "direct_star_still_explains_signal_flag": "1"
            if case == "direct_star_still_explains_signal"
            else "0",
            "tower_survives_star_control_flag": "1"
            if case == "tower_survives_star_control"
            else "0",
            "tower_vs_raw_delta": tower_vs_raw,
            "tower_vs_invalid_guard_delta": tower_vs_invalid,
            "tower_vs_nonself_guard_delta": tower_vs_nonself,
            "allowed_claim": allowed,
            "blocked_claim": blocked,
            "information_parity_warning": (
                "Guarded direct uses oracle one-step local transition masks; this "
                "diagnoses invalid/self-loop filtering but does not prove perfect "
                "action-surface parity with tower."
            ),
        }
    ]


def _badge_summary(
    interpretation: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    run_index_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    interp = interpretation[0] if interpretation else {}
    blocked = sum(_truthy(row.get("guard_fallback_used")) for row in guard_rows)
    artifacts_complete = all(_truthy(row.get("artifact_complete")) for row in run_index_rows)
    tower_delta = float(interp.get("tower_vs_nonself_guard_delta", 0.0) or 0.0)
    return [
        {
            "badge_id": "artifacts_complete",
            "label": "Artifacts",
            "value": "Complete" if artifacts_complete else "Incomplete",
            "color": "green" if artifacts_complete else "red",
            "reason": "Required run and summary artifacts were generated.",
            "source": "evaluation_run_index.csv",
        },
        {
            "badge_id": "guarded_direct",
            "label": "Guarded Direct",
            "value": "Complete" if guard_rows else "Missing",
            "color": "green" if guard_rows else "red",
            "reason": "Guard event rows expose raw, invalid-guard, and nonself-guard surfaces.",
            "source": "guard_events.csv",
        },
        {
            "badge_id": "self_loop_confound",
            "label": "Self-loop",
            "value": str(interp.get("interpretation_case", "Unknown")).replace("_", " ").title(),
            "color": "yellow",
            "reason": "Interpretation comes from the guarded comparison grid.",
            "source": "interpretation_summary.csv",
        },
        {
            "badge_id": "tower_vs_nonself",
            "label": "Tower vs Nonself",
            "value": "Positive" if tower_delta > 0 else "Not Positive",
            "color": "green" if tower_delta > 0 else "yellow",
            "reason": "Compares tower target-hit rate to direct_nonself_guard.",
            "source": "arm_summary.csv",
        },
        {
            "badge_id": "blocked_guard_states",
            "label": "Blocked Guards",
            "value": str(blocked),
            "color": "green" if blocked == 0 else "yellow",
            "reason": "Nonzero blocked guard states require inspection.",
            "source": "guard_filter_summary.csv",
        },
        {
            "badge_id": "claim_boundary",
            "label": "Claim",
            "value": "Diagnostic",
            "color": "blue",
            "reason": CLAIM_BOUNDARY,
            "source": "readout_source.json",
        },
    ]


def _timing_summary(timing_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for (arm_id, run_id), group in _group_by_many(timing_rows, ("arm_id", "run_id")).items():
        rows.append(
            {
                "arm_id": arm_id,
                "run_id": run_id,
                "total_duration_seconds": sum(float(row["duration_seconds"]) for row in group),
            }
        )
    return rows


def _comparison_flag(comparison_id: str, delta: float) -> str:
    if comparison_id == "direct_nonself_vs_tower_nonself":
        if delta > 0:
            return "tower_nonself_above_direct_nonself"
        if delta < 0:
            return "direct_nonself_above_tower_nonself"
        return "primary_pair_tied"
    if delta > 0:
        return "right_arm_higher"
    if delta < 0:
        return "left_arm_higher"
    return "arms_tied"


def _hit_rate(rows: list[dict[str, object]]) -> float:
    return _ratio(sum(_truthy(row.get("target_hit")) for row in rows), len(rows))


def _rate_by_flag(rows: list[dict[str, object]], flag: str) -> float:
    return _ratio(sum(_truthy(row.get(flag)) for row in rows), len(rows))


def _group_by(
    rows: list[dict[str, object]],
    key: str,
) -> dict[str, list[dict[str, object]]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row[key])].append(row)
    return grouped


def _group_by_many(
    rows: list[dict[str, object]],
    keys: tuple[str, ...],
) -> dict[tuple[object, ...], list[dict[str, object]]]:
    grouped: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    return grouped


def _ratio(numerator: float, denominator: float) -> float:
    return 0.0 if denominator == 0 else numerator / denominator


def _median(values: list[int]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[midpoint])
    return (ordered[midpoint - 1] + ordered[midpoint]) / 2.0


def _mean(values: object) -> float:
    materialized = list(values)
    return 0.0 if not materialized else sum(materialized) / len(materialized)


def _truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}
