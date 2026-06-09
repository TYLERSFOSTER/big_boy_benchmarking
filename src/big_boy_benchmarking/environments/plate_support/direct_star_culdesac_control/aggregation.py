"""Aggregation for the PlateSupport direct-star cul-de-sac diagnostic."""

from __future__ import annotations

from collections import defaultdict

from .config import (
    CLAIM_BOUNDARY,
    DIRECT_INVALID_GUARD_ARM_ID,
    DIRECT_NONSELF_GUARD_ARM_ID,
    DIRECT_RAW_ARM_ID,
    TOWER_SELECTED_CANDIDATE_ARM_ID,
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
from .manifests import ARM_MANIFEST_FIELDS, DirectStarArm

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
    "interpretation_summary": (
        "interpretation_case",
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


def build_direct_star_tables(
    *,
    arms: tuple[DirectStarArm, ...],
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
    """Build result tables for the direct-star diagnostic."""

    arm_rows = [arm.to_row() for arm in arms]
    arm_summary = _arm_summary(arm_rows, episode_rows, step_rows, guard_rows)
    paired_guard = _paired_guard_comparison(episode_rows, step_rows)
    interpretation = _interpretation_summary(arm_summary)
    return {
        "paired_seed_bundle_summary": seed_rows,
        "evaluation_run_index": run_index_rows,
        "evaluation_arm_manifest": arm_rows,
        "arm_summary": arm_summary,
        "guard_filter_summary": _guard_filter_summary(guard_rows),
        "self_loop_summary": _self_loop_summary(step_rows),
        "invalid_vs_self_loop_summary": _invalid_vs_self_loop_summary(step_rows),
        "paired_guard_comparison": paired_guard,
        "action_surface_summary": _action_surface_summary(guard_rows),
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
        (TOWER_SELECTED_CANDIDATE_ARM_ID, DIRECT_RAW_ARM_ID),
        (TOWER_SELECTED_CANDIDATE_ARM_ID, DIRECT_INVALID_GUARD_ARM_ID),
        (TOWER_SELECTED_CANDIDATE_ARM_ID, DIRECT_NONSELF_GUARD_ARM_ID),
        (DIRECT_INVALID_GUARD_ARM_ID, DIRECT_RAW_ARM_ID),
        (DIRECT_NONSELF_GUARD_ARM_ID, DIRECT_INVALID_GUARD_ARM_ID),
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


def _interpretation_summary(
    arm_summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    rate = {
        str(row["arm_id"]): float(row["target_hit_rate"])
        for row in arm_summary
    }
    tower_vs_raw = rate.get(TOWER_SELECTED_CANDIDATE_ARM_ID, 0.0) - rate.get(
        DIRECT_RAW_ARM_ID, 0.0
    )
    tower_vs_invalid = rate.get(TOWER_SELECTED_CANDIDATE_ARM_ID, 0.0) - rate.get(
        DIRECT_INVALID_GUARD_ARM_ID, 0.0
    )
    tower_vs_nonself = rate.get(TOWER_SELECTED_CANDIDATE_ARM_ID, 0.0) - rate.get(
        DIRECT_NONSELF_GUARD_ARM_ID, 0.0
    )
    if tower_vs_raw > 0 and tower_vs_invalid <= 0:
        case = "validity_filtering_explains_signal"
        allowed = (
            "ordinary one-step validity filtering explains most of the original "
            "tower signal"
        )
        blocked = "tower hierarchy beat direct learning on an equivalent decision surface"
    elif tower_vs_invalid > 0 and tower_vs_nonself <= 0:
        case = "self_loop_filtering_explains_remaining_signal"
        allowed = "self-loop/internal-edge filtering explains most of the remaining signal"
        blocked = "tower advantage is independent of local one-hop action filtering"
    elif tower_vs_nonself > 0:
        case = "tower_survives_nonself_guard"
        allowed = (
            "selected tower candidate outperformed direct after direct received "
            "a one-step non-self-action guard"
        )
        blocked = "general tower superiority is proven"
    elif tower_vs_nonself < 0:
        case = "nonself_guard_above_tower"
        allowed = (
            "guarded direct is a strong baseline and should be included in later "
            "benchmarking comparisons"
        )
        blocked = "the tower signal failed for all meaningful reasons"
    else:
        case = "inconclusive_or_tied"
        allowed = "the control surfaces are implemented but need larger or sharper budget"
        blocked = "the diagnostic resolves tower-vs-direct advantage"
    return [
        {
            "interpretation_case": case,
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


def _mean(values: object) -> float:
    materialized = list(values)
    return 0.0 if not materialized else sum(materialized) / len(materialized)


def _truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}

