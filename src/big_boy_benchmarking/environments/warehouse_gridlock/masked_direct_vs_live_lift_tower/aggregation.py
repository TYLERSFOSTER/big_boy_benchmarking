"""Aggregation for Warehouse masked direct/live-lift tower diagnostics."""

from __future__ import annotations

from collections import defaultdict
from statistics import mean, median
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.config import (
    DIRECT_ARM_ID,
    EVALUATION_ID,
    TOWER_ARM_ID,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.events import (
    ADMISSIBILITY_QUERY_SUMMARY_FIELDNAMES,
    ARM_SUMMARY_FIELDNAMES,
    CANDIDATE_FAMILY_SUMMARY_FIELDNAMES,
    NO_LOOKAHEAD_AUDIT_FIELDNAMES,
    PAIRED_SUMMARY_FIELDNAMES,
    TARGET_PROGRESS_FIELDNAMES,
    TOWER_LIVE_LIFT_SUMMARY_FIELDNAMES,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.paths import (
    EvaluationPaths,
)


def aggregate_results(
    *,
    paths: EvaluationPaths,
    run_label: str,
    episode_rows: list[dict[str, object]],
    direct_candidate_rows: list[dict[str, object]],
    direct_mask_rows: list[dict[str, object]],
    tower_lift_rows: list[dict[str, object]],
    no_lookahead_rows: list[dict[str, object]],
) -> dict[str, object]:
    arm_summary = _arm_summary(episode_rows, direct_mask_rows)
    paired_summary = _paired_summary(episode_rows, direct_mask_rows)
    target_summary = _target_progress_summary(episode_rows)
    candidate_family_summary = _candidate_family_summary(direct_candidate_rows)
    admissibility_summary = _admissibility_query_summary(direct_mask_rows)
    live_lift_summary = _tower_live_lift_summary(tower_lift_rows)
    no_lookahead_summary = _no_lookahead_summary(no_lookahead_rows)

    write_csv(paths.results_dir / "arm_summary.csv", arm_summary, ARM_SUMMARY_FIELDNAMES, create_parents=True)
    write_csv(
        paths.results_dir / "paired_summary.csv",
        paired_summary,
        PAIRED_SUMMARY_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        paths.results_dir / "target_progress_summary.csv",
        target_summary,
        TARGET_PROGRESS_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        paths.results_dir / "admissibility_query_summary.csv",
        admissibility_summary,
        ADMISSIBILITY_QUERY_SUMMARY_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        paths.results_dir / "candidate_family_summary.csv",
        candidate_family_summary,
        CANDIDATE_FAMILY_SUMMARY_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        paths.results_dir / "direct_mask_summary.csv",
        [row for row in admissibility_summary if row["arm_id"] == DIRECT_ARM_ID],
        ADMISSIBILITY_QUERY_SUMMARY_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        paths.results_dir / "tower_live_lift_summary.csv",
        live_lift_summary,
        TOWER_LIVE_LIFT_SUMMARY_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        paths.results_dir / "no_lookahead_audit_summary.csv",
        no_lookahead_summary,
        NO_LOOKAHEAD_AUDIT_FIELDNAMES,
        create_parents=True,
    )

    score_direction = _score_direction(arm_summary, no_lookahead_summary)
    summary = {
        "evaluation_id": EVALUATION_ID,
        "run_label": run_label,
        "status": "success",
        "score_direction": score_direction,
        "active_arms": [DIRECT_ARM_ID, TOWER_ARM_ID],
        "fairness_audit_status": _fairness_status(admissibility_summary, no_lookahead_summary),
        "no_lookahead_status": "pass"
        if all(_as_bool(row["no_lookahead_pass"]) for row in no_lookahead_summary)
        else "fail",
        "mask_scope_summary": "candidate_set",
        "tower_surface_scope_summary": "generated_discovered_surface",
        "candidate_family_status": _candidate_family_status(candidate_family_summary),
        "claim_boundary": [
            "diagnostic evidence only",
            "candidate-set masks, not full action-space masks",
            "no one-step successor-state cul-de-sac lookahead",
        ],
        "main_result_sentence": _main_result_sentence(score_direction, arm_summary),
        "blocked_claims": [
            "final benchmark significance",
            "broad tower superiority",
            "full serious-MDP tower coverage",
            "Abdul-style one-hop direct-star/tower-star cul-de-sac control",
        ],
    }
    write_json(paths.aggregate_summary, summary, create_parents=True)
    write_csv(
        paths.aggregate_table,
        [
            {
                "evaluation_id": EVALUATION_ID,
                "run_label": run_label,
                "status": summary["status"],
                "score_direction": score_direction,
                "fairness_audit_status": summary["fairness_audit_status"],
                "no_lookahead_status": summary["no_lookahead_status"],
                "mask_scope_summary": summary["mask_scope_summary"],
            "tower_surface_scope_summary": summary["tower_surface_scope_summary"],
            "candidate_family_status": summary["candidate_family_status"],
        }
    ],
        (
            "evaluation_id",
            "run_label",
            "status",
            "score_direction",
            "fairness_audit_status",
            "no_lookahead_status",
            "mask_scope_summary",
            "tower_surface_scope_summary",
            "candidate_family_status",
        ),
        create_parents=True,
    )
    return summary


def _arm_summary(
    episode_rows: list[dict[str, object]],
    mask_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    by_arm = _group_by(episode_rows, "arm_id")
    masks_by_arm = _group_by(mask_rows, "arm_id")
    for arm_id, arm_rows in sorted(by_arm.items()):
        rewards = [_as_float(row["total_reward"]) for row in arm_rows]
        masks = masks_by_arm.get(arm_id, [])
        rows.append(
            {
                "arm_id": arm_id,
                "run_count": len({row["run_id"] for row in arm_rows}),
                "episode_count": len(arm_rows),
                "mean_total_reward": mean(rewards) if rewards else 0.0,
                "median_total_reward": median(rewards) if rewards else 0.0,
                "terminal_success_count": sum(_as_bool(row["terminal_success"]) for row in arm_rows),
                "mean_final_correct_box_count": _mean_field(arm_rows, "final_correct_box_count"),
                "mean_final_correct_robot_count": _mean_field(arm_rows, "final_correct_robot_count"),
                "mean_valid_selected_step_count": _mean_field(arm_rows, "valid_selected_step_count"),
                "mean_invalid_selected_step_count": _mean_field(arm_rows, "invalid_selected_step_count"),
                "mean_candidate_count_before_mask": _mean_field(masks, "candidate_count_before_mask"),
                "mean_candidate_count_after_mask": _mean_field(masks, "candidate_count_after_mask"),
                "mean_admissibility_query_count": _mean_field(masks, "admissibility_query_count"),
            }
        )
    return rows


def _paired_summary(
    episode_rows: list[dict[str, object]],
    mask_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    by_key: dict[tuple[int, int, int], dict[str, dict[str, object]]] = defaultdict(dict)
    for row in episode_rows:
        key = (
            int(row["replicate_index"]),
            int(row["schema_seed"]),
            int(row["episode_index"]),
        )
        by_key[key][str(row["arm_id"])] = row
    masks_by_run = _group_by(mask_rows, "run_id")
    rows: list[dict[str, object]] = []
    for index, (key, pair) in enumerate(sorted(by_key.items())):
        if DIRECT_ARM_ID not in pair or TOWER_ARM_ID not in pair:
            continue
        direct = pair[DIRECT_ARM_ID]
        tower = pair[TOWER_ARM_ID]
        direct_masks = masks_by_run.get(str(direct["run_id"]), [])
        tower_masks = masks_by_run.get(str(tower["run_id"]), [])
        reward_delta = _as_float(tower["total_reward"]) - _as_float(direct["total_reward"])
        box_delta = _as_float(tower["final_correct_box_count"]) - _as_float(
            direct["final_correct_box_count"]
        )
        robot_delta = _as_float(tower["final_correct_robot_count"]) - _as_float(
            direct["final_correct_robot_count"]
        )
        terminal_delta = int(_as_bool(tower["terminal_success"])) - int(
            _as_bool(direct["terminal_success"])
        )
        rows.append(
            {
                "pair_id": f"pair_{index:04d}",
                "direct_run_id": direct["run_id"],
                "tower_run_id": tower["run_id"],
                "reward_delta_tower_minus_direct": reward_delta,
                "correct_box_delta_tower_minus_direct": box_delta,
                "correct_robot_delta_tower_minus_direct": robot_delta,
                "terminal_success_delta": terminal_delta,
                "valid_step_delta": _as_float(tower["valid_selected_step_count"])
                - _as_float(direct["valid_selected_step_count"]),
                "candidate_count_delta": _sum_field(tower_masks, "candidate_count_before_mask")
                - _sum_field(direct_masks, "candidate_count_before_mask"),
                "query_count_delta": _sum_field(tower_masks, "admissibility_query_count")
                - _sum_field(direct_masks, "admissibility_query_count"),
                "score_direction": _direction(reward_delta, box_delta, robot_delta, terminal_delta),
            }
        )
    return rows


def _target_progress_summary(episode_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for arm_id, arm_rows in sorted(_group_by(episode_rows, "arm_id").items()):
        rows.append(
            {
                "arm_id": arm_id,
                "mean_initial_correct_boxes": _mean_field(arm_rows, "initial_correct_box_count"),
                "mean_final_correct_boxes": _mean_field(arm_rows, "final_correct_box_count"),
                "mean_box_progress": _mean_field(arm_rows, "final_correct_box_count")
                - _mean_field(arm_rows, "initial_correct_box_count"),
                "mean_initial_correct_robots": _mean_field(arm_rows, "initial_correct_robot_count"),
                "mean_final_correct_robots": _mean_field(arm_rows, "final_correct_robot_count"),
                "mean_robot_progress": _mean_field(arm_rows, "final_correct_robot_count")
                - _mean_field(arm_rows, "initial_correct_robot_count"),
                "terminal_success_count": sum(_as_bool(row["terminal_success"]) for row in arm_rows),
            }
        )
    return rows


def _admissibility_query_summary(mask_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for arm_id, arm_rows in sorted(_group_by(mask_rows, "arm_id").items()):
        rows.append(
            {
                "arm_id": arm_id,
                "candidate_generation_policy_id": arm_rows[0]["candidate_generation_policy_id"],
                "mask_scope": arm_rows[0]["mask_scope"],
                "total_candidates_before_mask": _sum_field(arm_rows, "candidate_count_before_mask"),
                "total_candidates_after_mask": _sum_field(arm_rows, "candidate_count_after_mask"),
                "total_inadmissible_candidates": _sum_field(arm_rows, "inadmissible_candidate_count"),
                "total_admissibility_queries": _sum_field(arm_rows, "admissibility_query_count"),
                "total_cache_hits": _sum_field(arm_rows, "cache_hit_count"),
                "mean_candidates_before_mask_per_step": _mean_field(
                    arm_rows, "candidate_count_before_mask"
                ),
                "mean_candidates_after_mask_per_step": _mean_field(
                    arm_rows, "candidate_count_after_mask"
                ),
            }
        )
    return rows


def _candidate_family_summary(candidate_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    grouped: dict[tuple[str, str, int, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in candidate_rows:
        key = (
            str(row.get("arm_id", "")),
            str(row.get("candidate_family", "")),
            int(_as_float(row.get("active_robot_count", 0))),
            str(row.get("candidate_mix_id", "")),
            str(row.get("max_active_robots", "")),
        )
        grouped[key].append(row)
    for (arm_id, family, active_count, mix_id, max_active_robots), family_rows in sorted(
        grouped.items()
    ):
        rows.append(
            {
                "arm_id": arm_id,
                "candidate_family": family,
                "active_robot_count": active_count,
                "candidate_count": len(family_rows),
                "mean_candidate_rank": _mean_field(family_rows, "candidate_rank"),
                "candidate_mix_id": mix_id,
                "max_active_robots": max_active_robots,
            }
        )
    return rows


def _candidate_family_status(candidate_family_rows: list[dict[str, object]]) -> str:
    active_counts = {
        int(_as_float(row["active_robot_count"]))
        for row in candidate_family_rows
        if _as_float(row.get("candidate_count", 0)) > 0
    }
    if any(active_count >= 2 for active_count in active_counts):
        return "coordination_ready"
    if 1 in active_counts:
        return "one_active_only"
    if active_counts == {0}:
        return "all_stay_only"
    return "unknown"


def _tower_live_lift_summary(rows_in: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for (arm_id, tier), group in sorted(_group_by_multi(rows_in, ("arm_id", "tier")).items()):
        rows.append(
            {
                "arm_id": arm_id,
                "tier": tier,
                "total_fiber_candidates": _sum_field(group, "fiber_candidate_count"),
                "total_live_lift_candidates": _sum_field(group, "live_lift_candidate_count"),
                "total_dead_lift_candidates": _sum_field(group, "dead_lift_candidate_count"),
                "live_lift_failure_count": sum(_as_bool(row["lift_failure"]) for row in group),
                "mean_selected_lift_out_count": _mean_field(group, "selected_lift_out_count"),
                "out_scope": group[0]["out_scope"],
            }
        )
    return rows


def _no_lookahead_summary(rows_in: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for arm_id, group in sorted(_group_by(rows_in, "arm_id").items()):
        used = _sum_field(group, "successor_out_count_used_for_selection")
        observed = sum(row.get("successor_out_count_observed") not in ("", None) for row in group)
        rows.append(
            {
                "arm_id": arm_id,
                "selected_step_count": len(group),
                "successor_out_observed_count": observed,
                "successor_out_used_for_selection_count": used,
                "no_lookahead_pass": used == 0,
            }
        )
    return rows


def _score_direction(
    arm_summary: list[dict[str, object]],
    no_lookahead_summary: list[dict[str, object]],
) -> str:
    if any(not _as_bool(row["no_lookahead_pass"]) for row in no_lookahead_summary):
        return "blocked"
    by_arm = {row["arm_id"]: row for row in arm_summary}
    if DIRECT_ARM_ID not in by_arm or TOWER_ARM_ID not in by_arm:
        return "blocked"
    delta = _as_float(by_arm[TOWER_ARM_ID]["mean_total_reward"]) - _as_float(
        by_arm[DIRECT_ARM_ID]["mean_total_reward"]
    )
    if abs(delta) < 1e-9:
        return "tie"
    return "tower" if delta > 0 else "direct"


def _fairness_status(
    admissibility_summary: list[dict[str, object]],
    no_lookahead_summary: list[dict[str, object]],
) -> str:
    arms = {row["arm_id"] for row in admissibility_summary}
    if {DIRECT_ARM_ID, TOWER_ARM_ID} - arms:
        return "blocked"
    if any(not _as_bool(row["no_lookahead_pass"]) for row in no_lookahead_summary):
        return "blocked"
    return "pass"


def _main_result_sentence(score_direction: str, arm_summary: list[dict[str, object]]) -> str:
    by_arm = {row["arm_id"]: row for row in arm_summary}
    if score_direction == "blocked":
        return "The diagnostic is blocked because required fairness evidence is missing or failed."
    if DIRECT_ARM_ID not in by_arm or TOWER_ARM_ID not in by_arm:
        return "The diagnostic did not produce both active arms."
    direct_reward = by_arm[DIRECT_ARM_ID]["mean_total_reward"]
    tower_reward = by_arm[TOWER_ARM_ID]["mean_total_reward"]
    return (
        f"Score direction is {score_direction}: mean reward direct={direct_reward}, "
        f"tower={tower_reward} under the checked budget."
    )


def _direction(reward_delta: float, box_delta: float, robot_delta: float, terminal_delta: int) -> str:
    if terminal_delta > 0:
        return "tower"
    if terminal_delta < 0:
        return "direct"
    if reward_delta > 0:
        return "tower"
    if reward_delta < 0:
        return "direct"
    if box_delta + robot_delta > 0:
        return "tower"
    if box_delta + robot_delta < 0:
        return "direct"
    return "tie"


def _group_by(rows: list[dict[str, object]], key: str) -> dict[str, list[dict[str, object]]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row[key])].append(row)
    return grouped


def _group_by_multi(
    rows: list[dict[str, object]],
    keys: tuple[str, ...],
) -> dict[tuple[Any, ...], list[dict[str, object]]]:
    grouped: dict[tuple[Any, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    return grouped


def _mean_field(rows: list[dict[str, object]], key: str) -> float:
    values = [_as_float(row.get(key, 0.0)) for row in rows]
    return mean(values) if values else 0.0


def _sum_field(rows: list[dict[str, object]], key: str) -> float:
    return sum(_as_float(row.get(key, 0.0)) for row in rows)


def _as_float(value: object) -> float:
    if isinstance(value, bool):
        return float(int(value))
    if value in ("", None):
        return 0.0
    if isinstance(value, str) and value.lower() in {"true", "false"}:
        return 1.0 if value.lower() == "true" else 0.0
    return float(value)


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in {"true", "1", "yes"}
    return bool(value)
