"""Aggregation helpers for PlateSupport gauntlet Stage 6."""

from __future__ import annotations

from collections import Counter, defaultdict

from ..ids import (
    CANDIDATE_DISCOVERY_STAGE_ID,
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    LINEARIZATION_MODE_ID,
    PAIRED_REPLICATE_COMPARISON_STAGE_ID,
    SUITE_ID,
    THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
    TOWER_TRAINING_HEALTH_STAGE_ID,
)
from .claim_logic import classify_paired_claim
from .events import (
    COMPARISON_CONTROLLER_FIELDS,
    COMPARISON_EPISODE_FIELDS,
    COMPARISON_LEARNER_FIELDS,
    COMPARISON_LIFT_FIELDS,
    COMPARISON_STEP_FIELDS,
    COMPARISON_TIER_FIELDS,
    COMPARISON_TIMING_FIELDS,
)
from .target_policy import CLAIM_BOUNDARY

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
    "comparison_run_index": (
        "run_id",
        "pair_id",
        "arm_id",
        "arm_type",
        "candidate_id",
        "schema_id",
        "replicate_index",
        "status",
        "episode_count",
        "target_hit_count",
        "artifact_root",
    ),
    "paired_unit_summary": (
        "pair_id",
        "replicate_index",
        "active_arm_count",
        "completed_arm_count",
        "pair_complete",
        "incomplete_reason",
        "shared_environment_seed",
        "shared_exploration_seed",
        "shared_target_policy_id",
    ),
    "arm_summary": (
        "arm_id",
        "arm_type",
        "candidate_id",
        "schema_id",
        "status",
        "replicate_count",
        "episode_count",
        "target_hit_count",
        "target_hit_rate",
        "goal_success_count",
        "goal_success_rate",
        "mean_total_reward",
        "mean_step_count",
        "invalid_move_count",
        "claim_boundary",
    ),
    "baseline_summary": (
        "arm_id",
        "arm_type",
        "baseline_role",
        "status",
        "episode_count",
        "target_hit_rate",
        "mean_total_reward",
        "unavailable_reason",
    ),
    "candidate_comparison_arm_summary": (
        "arm_id",
        "candidate_id",
        "schema_id",
        "episode_count",
        "target_hit_rate",
        "mean_total_reward",
        "comparison_role",
    ),
    "target_hit_summary": (
        "arm_id",
        "replicate_index",
        "episode_count",
        "target_hit_count",
        "target_hit_rate",
        "target_policy_id",
    ),
    "success_rate_summary": (
        "arm_id",
        "replicate_index",
        "episode_count",
        "goal_success_count",
        "goal_success_rate",
    ),
    "first_hit_summary": (
        "arm_id",
        "replicate_index",
        "episode_count",
        "hit_observed",
        "first_hit_episode_index",
        "first_hit_episode_seed",
        "censored",
        "reason",
    ),
    "reward_distribution_summary": (
        "arm_id",
        "episode_count",
        "min_total_reward",
        "mean_total_reward",
        "max_total_reward",
    ),
    "step_efficiency_summary": (
        "arm_id",
        "episode_count",
        "mean_step_count",
        "mean_steps_per_target_hit",
    ),
    "invalid_move_summary": (
        "arm_id",
        "concrete_step_count",
        "invalid_move_count",
        "invalid_move_rate",
    ),
    "lift_success_by_tier": (
        "arm_id",
        "candidate_id",
        "schema_id",
        "tier",
        "lift_success_count",
        "mean_executable_lift_count",
    ),
    "lift_failure_by_tier": (
        "arm_id",
        "candidate_id",
        "schema_id",
        "tier",
        "lift_failure_count",
        "failure_reasons",
    ),
    "tier_occupancy_summary": (
        "arm_id",
        "candidate_id",
        "schema_id",
        "tier",
        "controller_step_count",
        "controller_step_share",
    ),
    "training_health_carryforward": (
        "candidate_id",
        "schema_id",
        "health_status",
        "episode_count",
        "success_count",
        "source_training_health_stage",
    ),
    "timing_summary": (
        "arm_id",
        "run_id",
        "total_duration_seconds",
    ),
    "artifact_completeness_summary": (
        "arm_id",
        "run_id",
        "required_file_count",
        "present_file_count",
        "artifact_complete",
    ),
    "paired_schema_comparison": (
        "pair_id",
        "replicate_index",
        "baseline_arm_id",
        "candidate_arm_id",
        "pair_complete",
        "baseline_target_hit_rate",
        "candidate_target_hit_rate",
        "target_hit_rate_delta",
        "baseline_mean_total_reward",
        "candidate_mean_total_reward",
        "mean_total_reward_delta",
        "baseline_mean_step_count",
        "candidate_mean_step_count",
        "mean_step_count_delta",
        "claim_boundary",
    ),
    "comparison_claim_summary": (
        "claim_status",
        "direction",
        "complete_pair_count",
        "mean_target_hit_rate_delta",
        "bounded_claim",
        "claim_boundary",
    ),
    "comparison_episode_summary": COMPARISON_EPISODE_FIELDS,
    "comparison_step_summary": COMPARISON_STEP_FIELDS,
    "controller_action_summary": COMPARISON_CONTROLLER_FIELDS,
    "learner_update_summary": COMPARISON_LEARNER_FIELDS,
    "lift_fiber_summary": COMPARISON_LIFT_FIELDS,
    "tier_transition_summary": COMPARISON_TIER_FIELDS,
    "timing_segments": COMPARISON_TIMING_FIELDS,
}


def build_stage6_tables(
    *,
    arms: tuple[object, ...],
    seed_rows: list[dict[str, object]],
    episode_rows: list[dict[str, object]],
    step_rows: list[dict[str, object]],
    controller_rows: list[dict[str, object]],
    learner_rows: list[dict[str, object]],
    lift_rows: list[dict[str, object]],
    tier_rows: list[dict[str, object]],
    timing_rows: list[dict[str, object]],
    run_index_rows: list[dict[str, object]],
    health_rows: list[dict[str, str]],
    target_policy_id: str,
    direct_arm_id: str,
    candidate_arm_id: str,
) -> dict[str, list[dict[str, object]]]:
    """Build all Stage 6 result tables."""

    arm_rows = [arm.to_row() for arm in arms]  # type: ignore[attr-defined]
    active_arm_ids = {row["arm_id"] for row in arm_rows if row["status"] == "active"}
    pair_summary = _paired_unit_summary(
        seed_rows,
        episode_rows,
        active_arm_ids=active_arm_ids,
        target_policy_id=target_policy_id,
    )
    arm_summary = _arm_summary(arm_rows, episode_rows, step_rows)
    paired_comparison = _paired_schema_comparison(
        episode_rows,
        direct_arm_id=direct_arm_id,
        candidate_arm_id=candidate_arm_id,
    )
    claim = classify_paired_claim(
        paired_rows=paired_comparison,
        direct_arm_id=direct_arm_id,
        candidate_arm_id=candidate_arm_id,
    )
    return {
        "paired_seed_bundle_summary": seed_rows,
        "comparison_run_index": run_index_rows,
        "paired_unit_summary": pair_summary,
        "arm_summary": arm_summary,
        "baseline_summary": _baseline_summary(arm_rows, arm_summary),
        "candidate_comparison_arm_summary": _candidate_arm_summary(arm_rows, arm_summary),
        "target_hit_summary": _target_hit_summary(episode_rows, target_policy_id),
        "success_rate_summary": _success_rate_summary(episode_rows),
        "first_hit_summary": _first_hit_summary(episode_rows),
        "reward_distribution_summary": _reward_distribution_summary(episode_rows),
        "step_efficiency_summary": _step_efficiency_summary(episode_rows),
        "invalid_move_summary": _invalid_move_summary(step_rows),
        "lift_success_by_tier": _lift_success_by_tier(lift_rows),
        "lift_failure_by_tier": _lift_failure_by_tier(lift_rows),
        "tier_occupancy_summary": _tier_occupancy_summary(tier_rows),
        "training_health_carryforward": _training_health_carryforward(health_rows),
        "timing_summary": _timing_summary(timing_rows),
        "artifact_completeness_summary": _artifact_completeness_summary(run_index_rows),
        "paired_schema_comparison": paired_comparison,
        "comparison_claim_summary": [claim],
        "comparison_episode_summary": episode_rows,
        "comparison_step_summary": step_rows,
        "controller_action_summary": controller_rows,
        "learner_update_summary": learner_rows,
        "lift_fiber_summary": lift_rows,
        "tier_transition_summary": tier_rows,
        "timing_segments": timing_rows,
    }


def build_stage6_aggregate_row(
    *,
    artifact_root: str,
    tables: dict[str, list[dict[str, object]]],
    source_paths: tuple[str, str, str],
    state_collapser_dependency_status: str,
) -> dict[str, object]:
    """Build the suite status row for Stage 6."""

    claim = tables["comparison_claim_summary"][0]
    status = "complete" if tables["comparison_run_index"] else "blocked"
    return {
        "suite_id": SUITE_ID,
        "stage_id": PAIRED_REPLICATE_COMPARISON_STAGE_ID,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "status": status,
        "claim_status": claim["claim_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "artifact_root": artifact_root,
        "source_stage_ids": (
            f"{CANDIDATE_DISCOVERY_STAGE_ID};{TOWER_TRAINING_HEALTH_STAGE_ID};"
            f"{THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID}"
        ),
        "source_artifact_paths": ";".join(source_paths),
        "linearization_mode_id": LINEARIZATION_MODE_ID,
        "state_collapser_dependency_status": state_collapser_dependency_status,
        "complete_pair_count": claim["complete_pair_count"],
        "mean_target_hit_rate_delta": claim["mean_target_hit_rate_delta"],
        "blocking_reason": "" if status == "complete" else "no_stage6_runs",
    }


def build_stage6_summary(aggregate_row: dict[str, object]) -> dict[str, object]:
    """Build JSON summary payload for Stage 6."""

    return {
        "stage_id": aggregate_row["stage_id"],
        "status": aggregate_row["status"],
        "claim_status": aggregate_row["claim_status"],
        "complete_pair_count": aggregate_row["complete_pair_count"],
        "mean_target_hit_rate_delta": aggregate_row["mean_target_hit_rate_delta"],
        "blocking_reason": aggregate_row["blocking_reason"],
    }


def _paired_unit_summary(
    seed_rows: list[dict[str, object]],
    episode_rows: list[dict[str, object]],
    *,
    active_arm_ids: set[object],
    target_policy_id: str,
) -> list[dict[str, object]]:
    rows = []
    by_pair: dict[str, set[object]] = defaultdict(set)
    for row in episode_rows:
        by_pair[str(row["pair_id"])].add(row["arm_id"])
    for seed in seed_rows:
        pair_id = str(seed["pair_id"])
        completed = by_pair.get(pair_id, set())
        missing = sorted(str(arm_id) for arm_id in active_arm_ids - completed)
        rows.append(
            {
                "pair_id": pair_id,
                "replicate_index": seed["replicate_index"],
                "active_arm_count": len(active_arm_ids),
                "completed_arm_count": len(completed),
                "pair_complete": "1" if not missing else "0",
                "incomplete_reason": "" if not missing else "missing:" + ";".join(missing),
                "shared_environment_seed": seed["environment_seed"],
                "shared_exploration_seed": seed["exploration_seed"],
                "shared_target_policy_id": target_policy_id,
            }
        )
    return rows


def _arm_summary(
    arm_rows: list[dict[str, object]],
    episode_rows: list[dict[str, object]],
    step_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    episodes_by_arm = _group_by(episode_rows, "arm_id")
    steps_by_arm = _group_by(step_rows, "arm_id")
    rows = []
    for arm in arm_rows:
        arm_id = str(arm["arm_id"])
        episodes = episodes_by_arm.get(arm_id, [])
        steps = steps_by_arm.get(arm_id, [])
        hits = sum(_truthy(row["target_hit"]) for row in episodes)
        goals = sum(_truthy(row["goal_reached"]) for row in episodes)
        rows.append(
            {
                "arm_id": arm_id,
                "arm_type": arm["arm_type"],
                "candidate_id": arm["candidate_id"],
                "schema_id": arm["schema_id"],
                "status": arm["status"],
                "replicate_count": len({row["replicate_index"] for row in episodes}),
                "episode_count": len(episodes),
                "target_hit_count": hits,
                "target_hit_rate": _ratio(hits, len(episodes)),
                "goal_success_count": goals,
                "goal_success_rate": _ratio(goals, len(episodes)),
                "mean_total_reward": _mean(float(row["total_reward"]) for row in episodes),
                "mean_step_count": _mean(float(row["step_count"]) for row in episodes),
                "invalid_move_count": sum(_truthy(row["invalid_move"]) for row in steps),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def _baseline_summary(
    arm_rows: list[dict[str, object]],
    arm_summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    summary_by_id = {row["arm_id"]: row for row in arm_summary}
    rows = []
    for arm in arm_rows:
        if arm["baseline_role"] not in {"primary_baseline", "engineering_control"}:
            continue
        summary = summary_by_id.get(arm["arm_id"], {})
        rows.append(
            {
                "arm_id": arm["arm_id"],
                "arm_type": arm["arm_type"],
                "baseline_role": arm["baseline_role"],
                "status": arm["status"],
                "episode_count": summary.get("episode_count", 0),
                "target_hit_rate": summary.get("target_hit_rate", 0.0),
                "mean_total_reward": summary.get("mean_total_reward", 0.0),
                "unavailable_reason": arm.get("unavailable_reason", ""),
            }
        )
    return rows


def _candidate_arm_summary(
    arm_rows: list[dict[str, object]],
    arm_summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    summary_by_id = {row["arm_id"]: row for row in arm_summary}
    rows = []
    for arm in arm_rows:
        if arm["baseline_role"] != "candidate":
            continue
        summary = summary_by_id.get(arm["arm_id"], {})
        rows.append(
            {
                "arm_id": arm["arm_id"],
                "candidate_id": arm["candidate_id"],
                "schema_id": arm["schema_id"],
                "episode_count": summary.get("episode_count", 0),
                "target_hit_rate": summary.get("target_hit_rate", 0.0),
                "mean_total_reward": summary.get("mean_total_reward", 0.0),
                "comparison_role": "selected_tower_candidate",
            }
        )
    return rows


def _target_hit_summary(
    episode_rows: list[dict[str, object]],
    target_policy_id: str,
) -> list[dict[str, object]]:
    rows = []
    for (arm_id, replicate_index), group in _group_by_many(
        episode_rows, ("arm_id", "replicate_index")
    ).items():
        hit_count = sum(_truthy(row["target_hit"]) for row in group)
        rows.append(
            {
                "arm_id": arm_id,
                "replicate_index": replicate_index,
                "episode_count": len(group),
                "target_hit_count": hit_count,
                "target_hit_rate": _ratio(hit_count, len(group)),
                "target_policy_id": target_policy_id,
            }
        )
    return rows


def _success_rate_summary(episode_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for (arm_id, replicate_index), group in _group_by_many(
        episode_rows, ("arm_id", "replicate_index")
    ).items():
        goal_count = sum(_truthy(row["goal_reached"]) for row in group)
        rows.append(
            {
                "arm_id": arm_id,
                "replicate_index": replicate_index,
                "episode_count": len(group),
                "goal_success_count": goal_count,
                "goal_success_rate": _ratio(goal_count, len(group)),
            }
        )
    return rows


def _first_hit_summary(episode_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for (arm_id, replicate_index), group in _group_by_many(
        episode_rows, ("arm_id", "replicate_index")
    ).items():
        ordered = sorted(group, key=lambda row: int(row["episode_index"]))
        hit = next((row for row in ordered if _truthy(row["target_hit"])), None)
        rows.append(
            {
                "arm_id": arm_id,
                "replicate_index": replicate_index,
                "episode_count": len(ordered),
                "hit_observed": "1" if hit is not None else "0",
                "first_hit_episode_index": "" if hit is None else hit["episode_index"],
                "first_hit_episode_seed": "" if hit is None else hit["episode_seed"],
                "censored": "0" if hit is not None else "1",
                "reason": "target hit observed" if hit is not None else "no target hit observed",
            }
        )
    return rows


def _reward_distribution_summary(episode_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for arm_id, group in _group_by(episode_rows, "arm_id").items():
        rewards = [float(row["total_reward"]) for row in group]
        rows.append(
            {
                "arm_id": arm_id,
                "episode_count": len(group),
                "min_total_reward": min(rewards) if rewards else 0.0,
                "mean_total_reward": _mean(rewards),
                "max_total_reward": max(rewards) if rewards else 0.0,
            }
        )
    return rows


def _step_efficiency_summary(episode_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for arm_id, group in _group_by(episode_rows, "arm_id").items():
        hits = sum(_truthy(row["target_hit"]) for row in group)
        step_count = sum(float(row["step_count"]) for row in group)
        rows.append(
            {
                "arm_id": arm_id,
                "episode_count": len(group),
                "mean_step_count": _mean(float(row["step_count"]) for row in group),
                "mean_steps_per_target_hit": "" if hits == 0 else step_count / hits,
            }
        )
    return rows


def _invalid_move_summary(step_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for arm_id, group in _group_by(step_rows, "arm_id").items():
        invalid = sum(_truthy(row["invalid_move"]) for row in group)
        rows.append(
            {
                "arm_id": arm_id,
                "concrete_step_count": len(group),
                "invalid_move_count": invalid,
                "invalid_move_rate": _ratio(invalid, len(group)),
            }
        )
    return rows


def _lift_success_by_tier(lift_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str, int], list[dict[str, object]]] = defaultdict(list)
    for row in lift_rows:
        if row["lift_status"] == "success":
            grouped[
                (
                    str(row["arm_id"]),
                    str(row["candidate_id"]),
                    str(row["schema_id"]),
                    int(row["tier"]),
                )
            ].append(row)
    return [
        {
            "arm_id": arm_id,
            "candidate_id": candidate_id,
            "schema_id": schema_id,
            "tier": tier,
            "lift_success_count": len(rows),
            "mean_executable_lift_count": _mean(
                float(row["executable_lift_count"]) for row in rows
            ),
        }
        for (arm_id, candidate_id, schema_id, tier), rows in sorted(grouped.items())
    ]


def _lift_failure_by_tier(lift_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str, int], list[dict[str, object]]] = defaultdict(list)
    for row in lift_rows:
        if row["lift_status"] != "success":
            grouped[
                (
                    str(row["arm_id"]),
                    str(row["candidate_id"]),
                    str(row["schema_id"]),
                    int(row["tier"] or 0),
                )
            ].append(row)
    return [
        {
            "arm_id": arm_id,
            "candidate_id": candidate_id,
            "schema_id": schema_id,
            "tier": tier,
            "lift_failure_count": len(rows),
            "failure_reasons": ";".join(sorted({str(row["failure_reason"]) for row in rows})),
        }
        for (arm_id, candidate_id, schema_id, tier), rows in sorted(grouped.items())
    ]


def _tier_occupancy_summary(tier_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped = _group_by_many(tier_rows, ("arm_id", "candidate_id", "schema_id"))
    results = []
    for (arm_id, candidate_id, schema_id), rows in grouped.items():
        counts = Counter(int(row["tier_before"]) for row in rows if str(row["tier_before"]) != "")
        total = sum(counts.values()) or 1
        for tier, count in sorted(counts.items()):
            results.append(
                {
                    "arm_id": arm_id,
                    "candidate_id": candidate_id,
                    "schema_id": schema_id,
                    "tier": tier,
                    "controller_step_count": count,
                    "controller_step_share": count / total,
                }
            )
    return results


def _training_health_carryforward(
    health_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    rows = []
    for row in health_rows:
        rows.append(
            {
                "candidate_id": row["candidate_id"],
                "schema_id": row["schema_id"],
                "health_status": row["health_status"],
                "episode_count": row["episode_count"],
                "success_count": row["success_count"],
                "source_training_health_stage": TOWER_TRAINING_HEALTH_STAGE_ID,
            }
        )
    return rows


def _timing_summary(timing_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for (arm_id, run_id), group in _group_by_many(timing_rows, ("arm_id", "run_id")).items():
        rows.append(
            {
                "arm_id": arm_id,
                "run_id": run_id,
                "total_duration_seconds": sum(float(row["duration_seconds"]) for row in group),
            }
        )
    return rows


def _artifact_completeness_summary(
    run_index_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    return [
        {
            "arm_id": row["arm_id"],
            "run_id": row["run_id"],
            "required_file_count": row.get("required_file_count", 0),
            "present_file_count": row.get("present_file_count", 0),
            "artifact_complete": row.get("artifact_complete", "0"),
        }
        for row in run_index_rows
    ]


def _paired_schema_comparison(
    episode_rows: list[dict[str, object]],
    *,
    direct_arm_id: str,
    candidate_arm_id: str,
) -> list[dict[str, object]]:
    rows = []
    by_pair_arm = _group_by_many(episode_rows, ("pair_id", "replicate_index", "arm_id"))
    pair_keys = sorted({(pair_id, replicate) for pair_id, replicate, _arm in by_pair_arm})
    for pair_id, replicate_index in pair_keys:
        baseline = by_pair_arm.get((pair_id, replicate_index, direct_arm_id), [])
        candidate = by_pair_arm.get((pair_id, replicate_index, candidate_arm_id), [])
        complete = bool(baseline and candidate)
        baseline_hit_rate = _hit_rate(baseline)
        candidate_hit_rate = _hit_rate(candidate)
        rows.append(
            {
                "pair_id": pair_id,
                "replicate_index": replicate_index,
                "baseline_arm_id": direct_arm_id,
                "candidate_arm_id": candidate_arm_id,
                "pair_complete": "1" if complete else "0",
                "baseline_target_hit_rate": baseline_hit_rate,
                "candidate_target_hit_rate": candidate_hit_rate,
                "target_hit_rate_delta": candidate_hit_rate - baseline_hit_rate,
                "baseline_mean_total_reward": _mean(
                    float(row["total_reward"]) for row in baseline
                ),
                "candidate_mean_total_reward": _mean(
                    float(row["total_reward"]) for row in candidate
                ),
                "mean_total_reward_delta": _mean(
                    float(row["total_reward"]) for row in candidate
                )
                - _mean(float(row["total_reward"]) for row in baseline),
                "baseline_mean_step_count": _mean(float(row["step_count"]) for row in baseline),
                "candidate_mean_step_count": _mean(
                    float(row["step_count"]) for row in candidate
                ),
                "mean_step_count_delta": _mean(float(row["step_count"]) for row in candidate)
                - _mean(float(row["step_count"]) for row in baseline),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def _hit_rate(rows: list[dict[str, object]]) -> float:
    return _ratio(sum(_truthy(row["target_hit"]) for row in rows), len(rows))


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
