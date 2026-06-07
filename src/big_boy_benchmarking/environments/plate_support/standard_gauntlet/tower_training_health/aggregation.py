"""Aggregation helpers for PlateSupport gauntlet Stage 4."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable

from ..ids import (
    CANDIDATE_DISCOVERY_STAGE_ID,
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    LINEARIZATION_MODE_ID,
    SUITE_ID,
    TOWER_TRAINING_HEALTH_STAGE_ID,
)
from ..status import (
    CLAIM_STATUS_TRAINABLE_CLEAN,
    CLAIM_STATUS_TRAINABLE_WARNING,
    CLAIM_STATUS_TRAINING_HEALTH_BLOCKED,
)
from .candidate_source import (
    TrainingCandidate,
)
from .classification import (
    classify_training_health,
)


def build_stage4_tables(
    *,
    candidates: Iterable[TrainingCandidate],
    episode_rows: list[dict[str, object]],
    concrete_step_rows: list[dict[str, object]],
    lift_rows: list[dict[str, object]],
    tier_rows: list[dict[str, object]],
    controller_rows: list[dict[str, object]],
    learner_rows: list[dict[str, object]],
    timing_rows: list[dict[str, object]],
    runtime_failure_rows: list[dict[str, object]],
) -> dict[str, list[dict[str, object]]]:
    """Build all Stage 4 aggregate tables from raw event rows."""

    candidate_list = list(candidates)
    return {
        "training_episode_summary": episode_rows,
        "training_curve_summary": _training_curve_summary(episode_rows),
        "concrete_step_summary": _concrete_step_summary(concrete_step_rows, candidate_list),
        "lift_success_by_tier": _lift_success_by_tier(lift_rows),
        "lift_failure_by_tier": _lift_failure_by_tier(lift_rows),
        "tier_occupancy_summary": _tier_occupancy_summary(tier_rows),
        "tier_executability_summary": _tier_executability_summary(tier_rows),
        "controller_action_summary": _controller_action_summary(controller_rows),
        "learner_update_summary": _learner_update_summary(learner_rows, candidate_list),
        "candidate_training_health_summary": _candidate_training_health_summary(
            candidates=candidate_list,
            episode_rows=episode_rows,
            concrete_step_rows=concrete_step_rows,
            lift_rows=lift_rows,
            learner_rows=learner_rows,
            tier_rows=tier_rows,
            runtime_failure_rows=runtime_failure_rows,
        ),
        "downstream_comparison_input_summary": _downstream_comparison_input_summary(
            candidates=candidate_list,
            health_rows=_candidate_training_health_summary(
                candidates=candidate_list,
                episode_rows=episode_rows,
                concrete_step_rows=concrete_step_rows,
                lift_rows=lift_rows,
                learner_rows=learner_rows,
                tier_rows=tier_rows,
                runtime_failure_rows=runtime_failure_rows,
            ),
        ),
        "timing_summary": _timing_summary(timing_rows),
    }


def build_stage4_aggregate_row(
    *,
    artifact_root: str,
    health_rows: list[dict[str, object]],
    state_collapser_dependency_status: str,
) -> dict[str, object]:
    """Build the suite status row for Stage 4."""

    trainable = [
        row
        for row in health_rows
        if row["health_status"] in {"trainable_clean", "trainable_warning"}
    ]
    status = "complete" if health_rows else "blocked"
    has_warning = any(row["health_status"] == "trainable_warning" for row in trainable)
    claim_status = (
        CLAIM_STATUS_TRAINABLE_WARNING
        if has_warning
        else CLAIM_STATUS_TRAINABLE_CLEAN
        if trainable
        else CLAIM_STATUS_TRAINING_HEALTH_BLOCKED
    )
    blocking_reason = "" if trainable else "training_health_not_established"
    return {
        "suite_id": SUITE_ID,
        "stage_id": TOWER_TRAINING_HEALTH_STAGE_ID,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "status": status,
        "claim_status": claim_status,
        "claim_boundary": "tower-only training health evidence; no flat comparison claim",
        "artifact_root": artifact_root,
        "source_stage_ids": CANDIDATE_DISCOVERY_STAGE_ID,
        "source_artifact_paths": "",
        "linearization_mode_id": LINEARIZATION_MODE_ID,
        "state_collapser_dependency_status": state_collapser_dependency_status,
        "trained_candidate_count": len(health_rows),
        "trainable_candidate_count": len(trainable),
        "blocking_reason": blocking_reason,
    }


def build_stage4_summary(aggregate_row: dict[str, object]) -> dict[str, object]:
    """Build JSON summary payload for Stage 4."""

    return {
        "stage_id": aggregate_row["stage_id"],
        "status": aggregate_row["status"],
        "claim_status": aggregate_row["claim_status"],
        "trained_candidate_count": aggregate_row["trained_candidate_count"],
        "trainable_candidate_count": aggregate_row["trainable_candidate_count"],
        "blocking_reason": aggregate_row["blocking_reason"],
    }


def _training_curve_summary(
    episode_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, int], list[dict[str, object]]] = defaultdict(list)
    for row in episode_rows:
        key = (
            str(row["candidate_id"]),
            str(row["schema_id"]),
            int(row["episode_index"]),
        )
        grouped[key].append(row)
    results = []
    for (candidate_id, schema_id, episode_index), rows in sorted(grouped.items()):
        results.append(
            {
                "candidate_id": candidate_id,
                "schema_id": schema_id,
                "episode_index": episode_index,
                "episode_count": len(rows),
                "mean_total_reward": _mean(float(row["total_reward"]) for row in rows),
                "success_rate": _mean(1.0 if _truthy(row["goal_reached"]) else 0.0 for row in rows),
                "mean_step_count": _mean(float(row["step_count"]) for row in rows),
            }
        )
    return results


def _concrete_step_summary(
    concrete_step_rows: list[dict[str, object]],
    candidates: list[TrainingCandidate],
) -> list[dict[str, object]]:
    rows = []
    for candidate in candidates:
        candidate_rows = [
            row for row in concrete_step_rows if row["candidate_id"] == candidate.candidate_id
        ]
        rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "schema_id": candidate.schema_id,
                "run_count": len({row["run_id"] for row in candidate_rows}),
                "concrete_step_count": len(candidate_rows),
                "valid_step_count": sum(
                    _truthy(row["valid_transition"]) for row in candidate_rows
                ),
                "invalid_move_count": sum(_truthy(row["invalid_move"]) for row in candidate_rows),
                "self_transition_count": sum(
                    _truthy(row["self_transition"]) for row in candidate_rows
                ),
                "terminal_step_count": sum(_truthy(row["terminated"]) for row in candidate_rows),
            }
        )
    return rows


def _lift_success_by_tier(
    lift_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, int], list[dict[str, object]]] = defaultdict(list)
    for row in lift_rows:
        if row["lift_status"] == "success":
            grouped[(str(row["candidate_id"]), str(row["schema_id"]), int(row["tier"]))].append(row)
    return [
        {
            "candidate_id": candidate_id,
            "schema_id": schema_id,
            "tier": tier,
            "lift_success_count": len(rows),
            "mean_executable_lift_count": _mean(
                float(row["executable_lift_count"]) for row in rows
            ),
        }
        for (candidate_id, schema_id, tier), rows in sorted(grouped.items())
    ]


def _lift_failure_by_tier(
    lift_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, int], list[dict[str, object]]] = defaultdict(list)
    for row in lift_rows:
        if row["lift_status"] != "success":
            grouped[(str(row["candidate_id"]), str(row["schema_id"]), int(row["tier"]))].append(row)
    return [
        {
            "candidate_id": candidate_id,
            "schema_id": schema_id,
            "tier": tier,
            "lift_failure_count": len(rows),
            "failure_reasons": ";".join(sorted({str(row["failure_reason"]) for row in rows})),
        }
        for (candidate_id, schema_id, tier), rows in sorted(grouped.items())
    ]


def _tier_occupancy_summary(
    tier_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in tier_rows:
        grouped[(str(row["candidate_id"]), str(row["schema_id"]))].append(row)
    results = []
    for (candidate_id, schema_id), rows in grouped.items():
        counts = Counter(int(row["tier_before"]) for row in rows if str(row["tier_before"]) != "")
        total = sum(counts.values()) or 1
        for tier, count in sorted(counts.items()):
            results.append(
                {
                    "candidate_id": candidate_id,
                    "schema_id": schema_id,
                    "tier": tier,
                    "controller_step_count": count,
                    "controller_step_share": count / total,
                }
            )
    return results


def _tier_executability_summary(
    tier_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, int], list[int]] = defaultdict(list)
    for row in tier_rows:
        if str(row["tier_before"]) == "":
            continue
        grouped[(str(row["candidate_id"]), str(row["schema_id"]), int(row["tier_before"]))].append(
            int(row["active_action_cell_count"])
        )
    return [
        {
            "candidate_id": candidate_id,
            "schema_id": schema_id,
            "tier": tier,
            "controller_step_count": len(values),
            "min_active_action_cell_count": min(values),
            "mean_active_action_cell_count": _mean(float(value) for value in values),
            "max_active_action_cell_count": max(values),
        }
        for (candidate_id, schema_id, tier), values in sorted(grouped.items())
    ]


def _controller_action_summary(
    controller_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    counts = Counter(
        (
            str(row["candidate_id"]),
            str(row["schema_id"]),
            int(row["tier"]),
            str(row["action_index"]),
            str(row["action_cell_id"]),
        )
        for row in controller_rows
    )
    return [
        {
            "candidate_id": candidate_id,
            "schema_id": schema_id,
            "tier": tier,
            "action_index": action_index,
            "action_cell_id": action_cell_id,
            "selection_count": count,
        }
        for (
            candidate_id,
            schema_id,
            tier,
            action_index,
            action_cell_id,
        ), count in sorted(counts.items())
    ]


def _learner_update_summary(
    learner_rows: list[dict[str, object]],
    candidates: list[TrainingCandidate],
) -> list[dict[str, object]]:
    rows = []
    for candidate in candidates:
        candidate_rows = [
            row for row in learner_rows if row["candidate_id"] == candidate.candidate_id
        ]
        abs_errors = [abs(float(row["td_error"])) for row in candidate_rows]
        rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "schema_id": candidate.schema_id,
                "learner_update_count": len(candidate_rows),
                "mean_abs_td_error": _mean(abs_errors),
                "max_abs_td_error": max(abs_errors) if abs_errors else 0.0,
            }
        )
    return rows


def _candidate_training_health_summary(
    *,
    candidates: list[TrainingCandidate],
    episode_rows: list[dict[str, object]],
    concrete_step_rows: list[dict[str, object]],
    lift_rows: list[dict[str, object]],
    learner_rows: list[dict[str, object]],
    tier_rows: list[dict[str, object]],
    runtime_failure_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    results = []
    for candidate in candidates:
        candidate_episode_rows = [
            row for row in episode_rows if row["candidate_id"] == candidate.candidate_id
        ]
        candidate_step_rows = [
            row for row in concrete_step_rows if row["candidate_id"] == candidate.candidate_id
        ]
        candidate_lift_rows = [
            row for row in lift_rows if row["candidate_id"] == candidate.candidate_id
        ]
        candidate_learner_rows = [
            row for row in learner_rows if row["candidate_id"] == candidate.candidate_id
        ]
        candidate_tier_rows = [
            row for row in tier_rows if row["candidate_id"] == candidate.candidate_id
        ]
        candidate_failure_rows = [
            row for row in runtime_failure_rows if row["candidate_id"] == candidate.candidate_id
        ]
        base_row = {
            "candidate_id": candidate.candidate_id,
            "schema_id": candidate.schema_id,
            "schema_mode": candidate.schema_mode,
            "ratio_numerator": candidate.ratio_numerator,
            "ratio_denominator": candidate.ratio_denominator,
            "max_iterations": candidate.max_iterations,
            "selector_rule_id": candidate.selector_rule_id,
            "selection_mode": candidate.selection_mode,
            "max_depth": candidate.max_depth,
            "nontrivial_tier_count": candidate.nontrivial_tier_count,
            "episode_count": len(candidate_episode_rows),
            "success_count": sum(_truthy(row["goal_reached"]) for row in candidate_episode_rows),
            "concrete_step_count": len(candidate_step_rows),
            "lift_success_count": sum(
                row["lift_status"] == "success" for row in candidate_lift_rows
            ),
            "learner_update_count": len(candidate_learner_rows),
            "runtime_failure_count": len(candidate_failure_rows),
            "blocked_controller_step_count": sum(
                bool(str(row["blocked_reason"])) for row in candidate_tier_rows
            ),
            "artifact_complete": 1,
        }
        status, reason = classify_training_health(base_row)
        results.append(
            {
                **base_row,
                "health_status": status,
                "health_reason": reason,
            }
        )
    return results


def _downstream_comparison_input_summary(
    *,
    candidates: list[TrainingCandidate],
    health_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    by_id = {candidate.candidate_id: candidate for candidate in candidates}
    rows = []
    for health in health_rows:
        if health["health_status"] not in {"trainable_clean", "trainable_warning"}:
            continue
        candidate = by_id[str(health["candidate_id"])]
        rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "schema_id": candidate.schema_id,
                "schema_mode": candidate.schema_mode,
                "ratio_numerator": candidate.ratio_numerator,
                "ratio_denominator": candidate.ratio_denominator,
                "max_iterations": candidate.max_iterations,
                "selector_rule_id": candidate.selector_rule_id,
                "selection_mode": candidate.selection_mode,
                "max_depth": candidate.max_depth,
                "nontrivial_tier_count": candidate.nontrivial_tier_count,
                "health_status": health["health_status"],
                "allowed_downstream_stage": "stage5_threshold_frontier_calibration",
                "stage5_threshold_frontier_calibration": "allowed",
                "stage6_paired_replicate_comparison": "allowed_after_stage5",
                "source_artifact_root": str(candidate.source_artifact_root),
            }
        )
    return rows


def _timing_summary(
    timing_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    return [
        {
            "candidate_id": row["candidate_id"],
            "schema_id": row["schema_id"],
            "run_id": row["run_id"],
            "total_duration_seconds": row["duration_seconds"],
        }
        for row in timing_rows
        if row["segment_name"] == "run_total"
    ]


def _mean(values: Iterable[float]) -> float:
    materialized = list(values)
    if not materialized:
        return 0.0
    return sum(materialized) / len(materialized)


def _truthy(value: object) -> bool:
    return str(value).lower() in {"1", "true", "yes"}
