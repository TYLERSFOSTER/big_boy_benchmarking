"""Aggregation helpers for PlateSupport gauntlet Stage 5."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from ..ids import (
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    LINEARIZATION_MODE_ID,
    STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
    SUITE_ID,
    THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
    TOWER_TRAINING_HEALTH_STAGE_ID,
)
from ..status import (
    CLAIM_STATUS_THRESHOLD_CALIBRATED,
    CLAIM_STATUS_THRESHOLD_UNRESOLVED,
)
from .calibration_arms import CalibrationArm, build_calibration_arms
from .config import ThresholdFrontierCalibrationConfig
from .feasibility import build_recommended_target_rows, unresolved_target_row
from .stage_sources import Stage1StructuralContext, Stage4TrainingHealthSource
from .target_policies import CLAIM_BOUNDARY, sustained_hit_target_policy_id
from .threshold_grid import build_threshold_grid

RESULT_TABLE_FIELDNAMES = {
    "calibration_episode_summary": (
        "calibration_arm_id",
        "calibration_arm_type",
        "candidate_id",
        "schema_id",
        "source_stage_id",
        "trace_source",
        "source_run_id",
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
    ),
    "calibration_arm_summary": (
        "calibration_arm_id",
        "calibration_arm_type",
        "candidate_id",
        "schema_id",
        "schema_mode",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "selector_rule_id",
        "selection_mode",
        "max_depth",
        "nontrivial_tier_count",
        "episode_count",
        "replicate_count",
        "success_count",
        "success_rate",
        "mean_total_reward",
        "median_total_reward",
        "min_total_reward",
        "max_total_reward",
        "mean_step_count",
        "first_hit_episode_global",
        "trace_source",
    ),
    "success_rate_summary": (
        "calibration_arm_id",
        "replicate_index",
        "episode_count",
        "success_count",
        "success_rate",
        "claim_boundary",
    ),
    "first_hit_summary": (
        "calibration_arm_id",
        "replicate_index",
        "episode_count",
        "hit_observed",
        "first_hit_episode_index",
        "first_hit_episode_seed",
        "censored",
        "reason",
    ),
    "sustained_hit_feasibility_summary": (
        "target_policy_id",
        "calibration_arm_id",
        "window_length",
        "required_count",
        "episodes_available_per_replicate_min",
        "budget_feasible",
        "hit_replicate_count",
        "total_replicate_count",
        "feasibility_status",
        "reason",
    ),
    "return_distribution_summary": (
        "calibration_arm_id",
        "candidate_id",
        "schema_id",
        "episode_count",
        "min_total_reward",
        "p25_total_reward",
        "median_total_reward",
        "p75_total_reward",
        "p90_total_reward",
        "max_total_reward",
        "mean_total_reward",
        "random_policy_mean_reward",
        "total_shortest_path_reward",
        "claim_boundary",
    ),
    "threshold_grid_construction": (
        "threshold_id",
        "threshold_value",
        "source_metric",
        "source_arm",
        "source_quantile",
        "construction_reason",
    ),
    "threshold_frontier_summary": (
        "threshold_id",
        "threshold_value",
        "calibration_arm_id",
        "episode_count",
        "hit_count",
        "hit_rate",
        "triviality_status",
        "feasibility_status",
        "reason",
    ),
    "recommended_comparison_target": (
        "target_policy_id",
        "target_type",
        "threshold_value",
        "window_length",
        "required_count",
        "episodes_required_minimum",
        "recommended_episodes_per_replicate",
        "recommended_replicates_per_arm",
        "baseline_feasibility",
        "candidate_feasibility",
        "calibration_status",
        "claim_boundary",
        "reason",
    ),
    "downstream_paired_comparison_input_summary": (
        "target_policy_id",
        "target_type",
        "threshold_value",
        "window_length",
        "required_count",
        "recommended_episodes_per_replicate",
        "recommended_replicates_per_arm",
        "stage6_paired_replicate_comparison",
        "blocking_reason",
        "source_recommended_target_table",
    ),
}


def build_stage5_tables(
    *,
    config: ThresholdFrontierCalibrationConfig,
    stage4_source: Stage4TrainingHealthSource,
    structural_context: Stage1StructuralContext,
) -> tuple[dict[str, list[dict[str, object]]], tuple[CalibrationArm, ...]]:
    """Build all Stage 5 result tables."""

    arms = build_calibration_arms(config=config, stage4_source=stage4_source)
    episode_rows = _calibration_episode_rows(stage4_source, arms)
    arm_summary = _calibration_arm_summary(episode_rows, arms)
    success_rate_summary = _success_rate_summary(episode_rows)
    first_hit_summary = _first_hit_summary(episode_rows)
    sustained_summary = _sustained_hit_feasibility_summary(
        episode_rows,
        windows=config.sustained_windows,
    )
    return_distribution = _return_distribution_summary(
        episode_rows,
        structural_context=structural_context,
    )
    threshold_grid = build_threshold_grid(
        calibration_episode_rows=episode_rows,
        structural_context=structural_context,
        quantiles=config.threshold_quantiles,
    )
    frontier_summary = _threshold_frontier_summary(episode_rows, threshold_grid)
    recommended_target = build_recommended_target_rows(
        config=config,
        calibration_arm_summary=arm_summary,
        first_hit_summary=first_hit_summary,
        threshold_frontier_summary=frontier_summary,
    )
    if not recommended_target:
        recommended_target = [
            unresolved_target_row(
                "No binary, first-hit, or return-threshold target was feasible "
                "from the observed Stage 4 traces."
            )
        ]
    downstream_summary = _downstream_paired_comparison_input_summary(recommended_target)
    return (
        {
            "calibration_episode_summary": episode_rows,
            "calibration_arm_summary": arm_summary,
            "success_rate_summary": success_rate_summary,
            "first_hit_summary": first_hit_summary,
            "sustained_hit_feasibility_summary": sustained_summary,
            "return_distribution_summary": return_distribution,
            "threshold_grid_construction": threshold_grid,
            "threshold_frontier_summary": frontier_summary,
            "recommended_comparison_target": recommended_target,
            "downstream_paired_comparison_input_summary": downstream_summary,
        },
        arms,
    )


def build_stage5_aggregate_row(
    *,
    artifact_root: str,
    tables: dict[str, list[dict[str, object]]],
    stage1_source_path: str,
    stage4_source_path: str,
    state_collapser_dependency_status: str,
) -> dict[str, object]:
    """Build suite status row for Stage 5."""

    target_row = tables["recommended_comparison_target"][0]
    calibrated = target_row["calibration_status"] == CLAIM_STATUS_THRESHOLD_CALIBRATED
    status = "complete" if calibrated else "blocked"
    blocking_reason = "" if calibrated else str(target_row["reason"])
    return {
        "suite_id": SUITE_ID,
        "stage_id": THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "status": status,
        "claim_status": (
            CLAIM_STATUS_THRESHOLD_CALIBRATED
            if calibrated
            else CLAIM_STATUS_THRESHOLD_UNRESOLVED
        ),
        "claim_boundary": CLAIM_BOUNDARY,
        "artifact_root": artifact_root,
        "source_stage_ids": (
            f"{STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID};{TOWER_TRAINING_HEALTH_STAGE_ID}"
        ),
        "source_artifact_paths": f"{stage1_source_path};{stage4_source_path}",
        "linearization_mode_id": LINEARIZATION_MODE_ID,
        "state_collapser_dependency_status": state_collapser_dependency_status,
        "calibration_arm_count": len(tables["calibration_arm_summary"]),
        "target_policy_count": len(tables["recommended_comparison_target"]),
        "recommended_target_policy_id": target_row["target_policy_id"],
        "recommended_stage6_episodes_per_replicate": (
            target_row["recommended_episodes_per_replicate"]
        ),
        "recommended_stage6_replicates_per_arm": (
            target_row["recommended_replicates_per_arm"]
        ),
        "blocking_reason": blocking_reason,
    }


def build_stage5_summary(aggregate_row: dict[str, object]) -> dict[str, object]:
    """Build JSON summary payload for Stage 5."""

    return {
        "stage_id": aggregate_row["stage_id"],
        "status": aggregate_row["status"],
        "claim_status": aggregate_row["claim_status"],
        "calibration_arm_count": aggregate_row["calibration_arm_count"],
        "recommended_target_policy_id": aggregate_row["recommended_target_policy_id"],
        "recommended_stage6_episodes_per_replicate": (
            aggregate_row["recommended_stage6_episodes_per_replicate"]
        ),
        "recommended_stage6_replicates_per_arm": (
            aggregate_row["recommended_stage6_replicates_per_arm"]
        ),
        "blocking_reason": aggregate_row["blocking_reason"],
    }


def _calibration_episode_rows(
    stage4_source: Stage4TrainingHealthSource,
    arms: tuple[CalibrationArm, ...],
) -> list[dict[str, object]]:
    arm_by_candidate = {arm.candidate_id: arm for arm in arms}
    rows: list[dict[str, object]] = []
    for row in stage4_source.tables["training_episode_summary"]:
        arm = arm_by_candidate.get(row["candidate_id"])
        if arm is None:
            continue
        rows.append(
            {
                "calibration_arm_id": arm.calibration_arm_id,
                "calibration_arm_type": arm.calibration_arm_type,
                "candidate_id": row["candidate_id"],
                "schema_id": row["schema_id"],
                "source_stage_id": arm.source_stage_id,
                "trace_source": arm.trace_source,
                "source_run_id": row["run_id"],
                "replicate_index": int(row["replicate_index"]),
                "episode_index": int(row["episode_index"]),
                "episode_seed": int(row["episode_seed"]),
                "status": row["status"],
                "step_count": int(row["step_count"]),
                "total_reward": float(row["total_reward"]),
                "terminated": row["terminated"],
                "truncated": row["truncated"],
                "goal_reached": "1" if _truthy(row["goal_reached"]) else "0",
                "blocked_reason": row["blocked_reason"],
            }
        )
    return rows


def _calibration_arm_summary(
    episode_rows: list[dict[str, object]],
    arms: tuple[CalibrationArm, ...],
) -> list[dict[str, object]]:
    grouped = _group_by_arm(episode_rows)
    rows = []
    for arm in arms:
        arm_rows = grouped.get(arm.calibration_arm_id, [])
        rewards = [float(row["total_reward"]) for row in arm_rows]
        step_counts = [float(row["step_count"]) for row in arm_rows]
        successes = [row for row in arm_rows if _truthy(row["goal_reached"])]
        first_hit = min(
            (int(row["episode_index"]) for row in successes),
            default=-1,
        )
        rows.append(
            {
                "calibration_arm_id": arm.calibration_arm_id,
                "calibration_arm_type": arm.calibration_arm_type,
                "candidate_id": arm.candidate_id,
                "schema_id": arm.schema_id,
                "schema_mode": arm.schema_mode,
                "ratio_numerator": arm.ratio_numerator,
                "ratio_denominator": arm.ratio_denominator,
                "max_iterations": arm.max_iterations,
                "selector_rule_id": arm.selector_rule_id,
                "selection_mode": arm.selection_mode,
                "max_depth": arm.max_depth,
                "nontrivial_tier_count": arm.nontrivial_tier_count,
                "episode_count": len(arm_rows),
                "replicate_count": len({row["replicate_index"] for row in arm_rows}),
                "success_count": len(successes),
                "success_rate": _ratio(len(successes), len(arm_rows)),
                "mean_total_reward": _mean(rewards),
                "median_total_reward": _quantile(sorted(rewards), 0.5) if rewards else 0.0,
                "min_total_reward": min(rewards) if rewards else 0.0,
                "max_total_reward": max(rewards) if rewards else 0.0,
                "mean_step_count": _mean(step_counts),
                "first_hit_episode_global": "" if first_hit < 0 else first_hit,
                "trace_source": arm.trace_source,
            }
        )
    return rows


def _success_rate_summary(
    episode_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    groups: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in episode_rows:
        groups[(str(row["calibration_arm_id"]), str(row["replicate_index"]))].append(row)
        groups[(str(row["calibration_arm_id"]), "all")].append(row)
    rows = []
    for (arm_id, replicate_index), group_rows in sorted(groups.items()):
        success_count = sum(_truthy(row["goal_reached"]) for row in group_rows)
        rows.append(
            {
                "calibration_arm_id": arm_id,
                "replicate_index": replicate_index,
                "episode_count": len(group_rows),
                "success_count": success_count,
                "success_rate": _ratio(success_count, len(group_rows)),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def _first_hit_summary(
    episode_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    groups: dict[tuple[str, int], list[dict[str, object]]] = defaultdict(list)
    for row in episode_rows:
        groups[(str(row["calibration_arm_id"]), int(row["replicate_index"]))].append(row)
    rows = []
    for (arm_id, replicate_index), group_rows in sorted(groups.items()):
        ordered = sorted(group_rows, key=lambda row: int(row["episode_index"]))
        hit = next((row for row in ordered if _truthy(row["goal_reached"])), None)
        rows.append(
            {
                "calibration_arm_id": arm_id,
                "replicate_index": replicate_index,
                "episode_count": len(ordered),
                "hit_observed": "1" if hit is not None else "0",
                "first_hit_episode_index": "" if hit is None else hit["episode_index"],
                "first_hit_episode_seed": "" if hit is None else hit["episode_seed"],
                "censored": "0" if hit is not None else "1",
                "reason": (
                    "goal hit observed"
                    if hit is not None
                    else "no hit observed within available episodes"
                ),
            }
        )
    return rows


def _sustained_hit_feasibility_summary(
    episode_rows: list[dict[str, object]],
    *,
    windows: tuple[tuple[int, int], ...],
) -> list[dict[str, object]]:
    groups: dict[tuple[str, int], list[dict[str, object]]] = defaultdict(list)
    for row in episode_rows:
        groups[(str(row["calibration_arm_id"]), int(row["replicate_index"]))].append(row)
    arm_ids = sorted({row["calibration_arm_id"] for row in episode_rows})
    rows = []
    for arm_id in arm_ids:
        arm_groups = {
            replicate: sorted(rows, key=lambda row: int(row["episode_index"]))
            for (group_arm, replicate), rows in groups.items()
            if group_arm == arm_id
        }
        min_episodes = min((len(rows) for rows in arm_groups.values()), default=0)
        for required_count, window_length in windows:
            budget_feasible = min_episodes >= window_length
            hit_count = 0
            if budget_feasible:
                hit_count = sum(
                    _window_hit_observed(rows, required_count, window_length)
                    for rows in arm_groups.values()
                )
            rows.append(
                {
                    "target_policy_id": sustained_hit_target_policy_id(
                        required_count,
                        window_length,
                    ),
                    "calibration_arm_id": arm_id,
                    "window_length": window_length,
                    "required_count": required_count,
                    "episodes_available_per_replicate_min": min_episodes,
                    "budget_feasible": "1" if budget_feasible else "0",
                    "hit_replicate_count": hit_count,
                    "total_replicate_count": len(arm_groups),
                    "feasibility_status": (
                        "feasible_observed"
                        if hit_count
                        else "feasible_not_observed"
                        if budget_feasible
                        else "blocked_window_exceeds_budget"
                    ),
                    "reason": _sustained_reason(
                        budget_feasible=budget_feasible,
                        hit_count=hit_count,
                        required_count=required_count,
                        window_length=window_length,
                    ),
                }
            )
    return rows


def _return_distribution_summary(
    episode_rows: list[dict[str, object]],
    *,
    structural_context: Stage1StructuralContext,
) -> list[dict[str, object]]:
    groups = _group_by_arm(episode_rows)
    rows = []
    for arm_id, group_rows in sorted(groups.items()):
        rewards = sorted(float(row["total_reward"]) for row in group_rows)
        first_row = group_rows[0]
        rows.append(
            {
                "calibration_arm_id": arm_id,
                "candidate_id": first_row["candidate_id"],
                "schema_id": first_row["schema_id"],
                "episode_count": len(group_rows),
                "min_total_reward": min(rewards),
                "p25_total_reward": _quantile(rewards, 0.25),
                "median_total_reward": _quantile(rewards, 0.5),
                "p75_total_reward": _quantile(rewards, 0.75),
                "p90_total_reward": _quantile(rewards, 0.9),
                "max_total_reward": max(rewards),
                "mean_total_reward": _mean(rewards),
                "random_policy_mean_reward": structural_context.random_policy_mean_reward,
                "total_shortest_path_reward": structural_context.total_shortest_path_reward,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def _threshold_frontier_summary(
    episode_rows: list[dict[str, object]],
    threshold_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    groups = _group_by_arm(episode_rows)
    rows = []
    for threshold in threshold_rows:
        threshold_value = float(threshold["threshold_value"])
        for arm_id, group_rows in sorted(groups.items()):
            hit_count = sum(float(row["total_reward"]) >= threshold_value for row in group_rows)
            episode_count = len(group_rows)
            hit_rate = _ratio(hit_count, episode_count)
            if hit_count == 0:
                triviality = "none_hit"
                status = "blocked_none_hit"
                reason = "threshold is above all observed returns for this arm"
            elif hit_count == episode_count:
                triviality = "all_hit"
                status = "blocked_all_hit"
                reason = "threshold is below or equal to all observed returns for this arm"
            else:
                triviality = "nontrivial"
                status = "feasible_nontrivial"
                reason = "threshold separates observed episodes into hit and miss rows"
            rows.append(
                {
                    "threshold_id": threshold["threshold_id"],
                    "threshold_value": threshold_value,
                    "calibration_arm_id": arm_id,
                    "episode_count": episode_count,
                    "hit_count": hit_count,
                    "hit_rate": hit_rate,
                    "triviality_status": triviality,
                    "feasibility_status": status,
                    "reason": reason,
                }
            )
    return rows


def _downstream_paired_comparison_input_summary(
    recommended_target_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    target = recommended_target_rows[0]
    calibrated = target["calibration_status"] == CLAIM_STATUS_THRESHOLD_CALIBRATED
    return [
        {
            "target_policy_id": target["target_policy_id"],
            "target_type": target["target_type"],
            "threshold_value": target["threshold_value"],
            "window_length": target["window_length"],
            "required_count": target["required_count"],
            "recommended_episodes_per_replicate": (
                target["recommended_episodes_per_replicate"]
            ),
            "recommended_replicates_per_arm": target["recommended_replicates_per_arm"],
            "stage6_paired_replicate_comparison": (
                "allowed" if calibrated else "blocked"
            ),
            "blocking_reason": "" if calibrated else target["reason"],
            "source_recommended_target_table": "results/recommended_comparison_target.csv",
        }
    ]


def _group_by_arm(
    rows: Iterable[dict[str, object]],
) -> dict[str, list[dict[str, object]]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["calibration_arm_id"])].append(row)
    return grouped


def _window_hit_observed(
    ordered_rows: list[dict[str, object]],
    required_count: int,
    window_length: int,
) -> bool:
    goal_flags = [_truthy(row["goal_reached"]) for row in ordered_rows]
    for start_index in range(0, len(goal_flags) - window_length + 1):
        window = goal_flags[start_index : start_index + window_length]
        if sum(window) >= required_count:
            return True
    return False


def _sustained_reason(
    *,
    budget_feasible: bool,
    hit_count: int,
    required_count: int,
    window_length: int,
) -> str:
    if not budget_feasible:
        return (
            f"{required_count}-of-{window_length} cannot be evaluated because the "
            "available per-replicate episode count is smaller than the window"
        )
    if hit_count:
        return f"{required_count}-of-{window_length} observed in at least one replicate"
    return f"{required_count}-of-{window_length} is budget-feasible but not observed"


def _quantile(sorted_values: list[float], quantile: float) -> float:
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = quantile * (len(sorted_values) - 1)
    lower_index = int(position)
    upper_index = min(lower_index + 1, len(sorted_values) - 1)
    fraction = position - lower_index
    return sorted_values[lower_index] * (1.0 - fraction) + sorted_values[upper_index] * fraction


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def _ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def _truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}
