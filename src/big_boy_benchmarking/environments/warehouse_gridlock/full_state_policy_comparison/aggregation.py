"""Aggregation for Warehouse full-state policy comparison artifacts."""

from __future__ import annotations

from collections import defaultdict
from statistics import mean, median
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.environments.warehouse_gridlock.full_state_policy_comparison.config import (
    DIRECT_ARM_ID,
    EVALUATION_ID,
    TOWER_ARM_ID,
)
from big_boy_benchmarking.environments.warehouse_gridlock.full_state_policy_comparison.paths import (
    EvaluationPaths,
)


def aggregate_results(
    *,
    paths: EvaluationPaths,
    run_label: str,
    episode_rows: list[dict[str, object]],
    policy_decision_rows: list[dict[str, object]],
    policy_update_rows: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    no_lookahead_rows: list[dict[str, object]],
    tower_lift_rows: list[dict[str, object]],
    tower_shape_rows: list[dict[str, object]],
    timing_rows: list[dict[str, object]],
) -> dict[str, object]:
    arm_summary = _arm_summary(episode_rows)
    learning_health = _learning_health(policy_decision_rows, policy_update_rows)
    learning_curve = _learning_curve(episode_rows)
    policy_reuse = _policy_reuse(policy_decision_rows)
    decision_summary = _decision_summary(policy_decision_rows)
    update_summary = _update_summary(policy_update_rows)
    projection_summary = _projection_summary(projection_rows)
    no_lookahead_summary = _no_lookahead_summary(no_lookahead_rows)
    tower_live_lift = _tower_live_lift_summary(tower_lift_rows)
    timing_summary = _timing_summary(timing_rows)
    paired_summary = _paired_summary(episode_rows)
    aggregate = _aggregate_summary(
        run_label=run_label,
        arm_summary=arm_summary,
        learning_health=learning_health,
        no_lookahead_summary=no_lookahead_summary,
        paired_summary=paired_summary,
    )
    write_csv(paths.results_dir / "arm_summary.csv", arm_summary, _fieldnames(arm_summary), create_parents=True)
    write_csv(paths.results_dir / "paired_summary.csv", paired_summary, _fieldnames(paired_summary), create_parents=True)
    write_csv(paths.results_dir / "learning_health_summary.csv", learning_health, _fieldnames(learning_health), create_parents=True)
    write_csv(paths.results_dir / "learning_curve_summary.csv", learning_curve, _fieldnames(learning_curve), create_parents=True)
    write_csv(paths.results_dir / "policy_reuse_summary.csv", policy_reuse, _fieldnames(policy_reuse), create_parents=True)
    write_csv(paths.results_dir / "policy_decision_summary.csv", decision_summary, _fieldnames(decision_summary), create_parents=True)
    write_csv(paths.results_dir / "policy_update_summary.csv", update_summary, _fieldnames(update_summary), create_parents=True)
    write_csv(paths.results_dir / "mask_projection_summary.csv", projection_summary, _fieldnames(projection_summary), create_parents=True)
    write_csv(paths.results_dir / "no_lookahead_audit_summary.csv", no_lookahead_summary, _fieldnames(no_lookahead_summary), create_parents=True)
    write_csv(paths.results_dir / "tower_live_lift_summary.csv", tower_live_lift, _fieldnames(tower_live_lift), create_parents=True)
    write_csv(paths.results_dir / "tower_shape_summary.csv", tower_shape_rows, _fieldnames(tower_shape_rows), create_parents=True)
    write_csv(paths.results_dir / "timing_summary.csv", timing_summary, _fieldnames(timing_summary), create_parents=True)
    write_json(paths.aggregate_summary, aggregate, create_parents=True)
    write_csv(paths.aggregate_table, [aggregate], _fieldnames([aggregate]), create_parents=True)
    return aggregate


def _arm_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    by_arm = _group(rows, "arm_id")
    output = []
    for arm_id, arm_rows in sorted(by_arm.items()):
        rewards = [_float(row["total_reward"]) for row in arm_rows]
        output.append(
            {
                "arm_id": arm_id,
                "episode_count": len(arm_rows),
                "mean_total_reward": mean(rewards) if rewards else 0.0,
                "median_total_reward": median(rewards) if rewards else 0.0,
                "terminal_success_count": sum(_bool(row["terminal_success"]) for row in arm_rows),
                "mean_final_correct_box_count": _mean_key(arm_rows, "final_correct_box_count"),
                "mean_final_correct_robot_count": _mean_key(arm_rows, "final_correct_robot_count"),
                "mean_valid_selected_step_count": _mean_key(arm_rows, "valid_selected_step_count"),
                "mean_projection_attempt_count": _mean_key(arm_rows, "projection_attempt_count"),
            }
        )
    return output


def _learning_health(
    decision_rows: list[dict[str, object]],
    update_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    decisions_by_arm = _group(decision_rows, "arm_id")
    updates_by_arm = _group(update_rows, "arm_id")
    arms = sorted(set(decisions_by_arm) | set(updates_by_arm))
    output = []
    for arm_id in arms:
        decisions = decisions_by_arm.get(arm_id, [])
        updates = updates_by_arm.get(arm_id, [])
        non_noop = [row for row in updates if _bool(row["non_noop_update"])]
        nonzero_prior = [row for row in decisions if _bool(row["prior_signal_used"])]
        hash_before = updates[0]["parameter_state_hash_before"] if updates else ""
        hash_after = updates[-1]["parameter_state_hash_after"] if updates else ""
        if not updates:
            status = "no_updates"
        elif not non_noop or not nonzero_prior:
            status = "nominal_updates_only"
        elif hash_before != hash_after:
            status = "real_learning_signal_present"
        else:
            status = "failed"
        output.append(
            {
                "arm_id": arm_id,
                "run_count": len(set(row["run_id"] for row in decisions)),
                "episode_count": len(set((row["run_id"], row["episode_index"]) for row in decisions)),
                "decision_count": len(decisions),
                "update_count": len(updates),
                "non_noop_update_count": len(non_noop),
                "mean_update_norm": _mean_key(updates, "update_norm_or_change_count"),
                "parameter_state_changes": len(
                    {
                        (
                            row["parameter_state_hash_before"],
                            row["parameter_state_hash_after"],
                        )
                        for row in updates
                        if row["parameter_state_hash_before"] != row["parameter_state_hash_after"]
                    }
                ),
                "nonzero_prior_signal_decision_count": len(nonzero_prior),
                "reused_feature_signal_decision_count": len(nonzero_prior),
                "policy_state_hash_initial": hash_before,
                "policy_state_hash_final": hash_after,
                "learning_status": status,
            }
        )
    return output


def _learning_curve(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "arm_id": row["arm_id"],
            "replicate_index": row["replicate_index"],
            "schema_seed": row["schema_seed"],
            "episode_index": row["episode_index"],
            "episode_total_reward": row["total_reward"],
            "terminal_success": row["terminal_success"],
            "final_correct_boxes": row["final_correct_box_count"],
            "final_correct_robots": row["final_correct_robot_count"],
            "selected_valid_steps": row["valid_selected_step_count"],
            "raw_invalid_proposal_count": "",
            "projection_attempt_count": row["projection_attempt_count"],
            "policy_update_count": row["policy_update_count"],
            "non_noop_update_count": row["non_noop_update_count"],
            "parameter_delta_norm": "",
        }
        for row in rows
    ]


def _policy_reuse(decision_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output = []
    for arm_id, rows in sorted(_group(decision_rows, "arm_id").items()):
        prior = [row for row in rows if _bool(row["prior_signal_used"])]
        output.append(
            {
                "arm_id": arm_id,
                "model_family_id": rows[0]["model_family_id"] if rows else "",
                "feature_namespace": "warehouse_full_state_linear_features",
                "decision_count": len(rows),
                "decisions_using_nonzero_prior_signal": len(prior),
                "decisions_with_prior_policy_state_hash_seen_before": len(prior),
                "unique_feature_keys_or_parameter_groups_touched": "feature_weight_vector",
                "mean_prior_score_abs": "",
                "median_prior_score_abs": "",
                "reuse_status": "reused_prior_signal" if prior else "no_prior_signal_reuse",
            }
        )
    return output


def _decision_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output = []
    for arm_id, arm_rows in sorted(_group(rows, "arm_id").items()):
        output.append(
            {
                "arm_id": arm_id,
                "decision_count": len(arm_rows),
                "raw_valid_count": sum(_bool(row["raw_valid"]) for row in arm_rows),
                "selected_valid_count": sum(_bool(row["selected_valid"]) for row in arm_rows),
                "prior_signal_used_count": sum(_bool(row["prior_signal_used"]) for row in arm_rows),
            }
        )
    return output


def _update_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output = []
    for arm_id, arm_rows in sorted(_group(rows, "arm_id").items()):
        output.append(
            {
                "arm_id": arm_id,
                "update_count": len(arm_rows),
                "non_noop_update_count": sum(_bool(row["non_noop_update"]) for row in arm_rows),
                "mean_update_norm": _mean_key(arm_rows, "update_norm_or_change_count"),
            }
        )
    return output


def _projection_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output = []
    for arm_id, arm_rows in sorted(_group(rows, "arm_id").items()):
        output.append(
            {
                "arm_id": arm_id,
                "projection_count": len(arm_rows),
                "raw_valid_count": sum(_bool(row["raw_valid"]) for row in arm_rows),
                "selected_valid_count": sum(_bool(row["selected_valid"]) for row in arm_rows),
                "fallback_used_count": sum(_bool(row["fallback_used"]) for row in arm_rows),
                "mean_projection_attempt_count": _mean_key(arm_rows, "projection_attempt_count"),
            }
        )
    return output


def _no_lookahead_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output = []
    for arm_id, arm_rows in sorted(_group(rows, "arm_id").items()):
        output.append(
            {
                "arm_id": arm_id,
                "selected_action_count": len(arm_rows),
                "successor_out_count_used_for_selection_count": sum(
                    _bool(row["successor_out_count_used_for_selection"]) for row in arm_rows
                ),
                "successor_out_count_observed_for_diagnosis_count": sum(
                    1 for row in arm_rows if str(row.get("successor_out_count_observed", "")) != ""
                ),
            }
        )
    return output


def _tower_live_lift_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    if not rows:
        return []
    return [
        {
            "arm_id": TOWER_ARM_ID,
            "lift_event_count": len(rows),
            "live_lift_candidate_count": sum(_int(row["live_lift_candidate_count"]) for row in rows),
            "dead_lift_candidate_count": sum(_int(row["dead_lift_candidate_count"]) for row in rows),
            "lift_failure_count": sum(_bool(row["lift_failure"]) for row in rows),
        }
    ]


def _timing_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return rows


def _paired_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    by_key: dict[tuple[str, str, str], dict[str, dict[str, object]]] = defaultdict(dict)
    for row in rows:
        key = (str(row["replicate_index"]), str(row["schema_seed"]), str(row["episode_index"]))
        by_key[key][str(row["arm_id"])] = row
    output = []
    for key, pair in sorted(by_key.items()):
        if DIRECT_ARM_ID not in pair or TOWER_ARM_ID not in pair:
            continue
        direct = pair[DIRECT_ARM_ID]
        tower = pair[TOWER_ARM_ID]
        reward_delta = _float(tower["total_reward"]) - _float(direct["total_reward"])
        output.append(
            {
                "pair_id": f"rep{key[0]}-schema{key[1]}-episode{key[2]}",
                "direct_run_id": direct["run_id"],
                "tower_run_id": tower["run_id"],
                "reward_delta_tower_minus_direct": reward_delta,
                "correct_box_delta_tower_minus_direct": _float(tower["final_correct_box_count"])
                - _float(direct["final_correct_box_count"]),
                "correct_robot_delta_tower_minus_direct": _float(tower["final_correct_robot_count"])
                - _float(direct["final_correct_robot_count"]),
                "terminal_success_delta": int(_bool(tower["terminal_success"]))
                - int(_bool(direct["terminal_success"])),
                "score_direction": "tower" if reward_delta > 0 else "direct" if reward_delta < 0 else "tie",
            }
        )
    return output


def _aggregate_summary(
    *,
    run_label: str,
    arm_summary: list[dict[str, object]],
    learning_health: list[dict[str, object]],
    no_lookahead_summary: list[dict[str, object]],
    paired_summary: list[dict[str, object]],
) -> dict[str, object]:
    learning_ok = all(row["learning_status"] == "real_learning_signal_present" for row in learning_health)
    no_lookahead_ok = all(
        _int(row["successor_out_count_used_for_selection_count"]) == 0
        for row in no_lookahead_summary
    )
    tower_positive = sum(1 for row in paired_summary if row["score_direction"] == "tower")
    direct_positive = sum(1 for row in paired_summary if row["score_direction"] == "direct")
    direction = "tie"
    if tower_positive > direct_positive:
        direction = "tower"
    elif direct_positive > tower_positive:
        direction = "direct"
    return {
        "evaluation_id": EVALUATION_ID,
        "run_label": run_label,
        "status": "complete",
        "learning_contract_status": "passed" if learning_ok else "failed",
        "no_lookahead_status": "passed" if no_lookahead_ok else "failed",
        "score_direction": direction,
        "arm_count": len(arm_summary),
        "paired_episode_count": len(paired_summary),
        "claim_boundary": [
            "trainable policy contract smoke/pilot evidence only",
            "no broad Warehouse benchmark claim",
            "no backprop claim",
            "no statistical significance claim",
        ],
    }


def _group(rows: list[dict[str, object]], key: str) -> dict[str, list[dict[str, object]]]:
    output: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        output[str(row[key])].append(row)
    return output


def _fieldnames(rows: list[dict[str, object]]) -> tuple[str, ...]:
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    return tuple(keys) if keys else ("empty",)


def _mean_key(rows: list[dict[str, object]], key: str) -> float:
    values = [_float(row[key]) for row in rows if str(row.get(key, "")) != ""]
    return mean(values) if values else 0.0


def _float(value: object) -> float:
    return float(value)


def _int(value: object) -> int:
    return int(float(value))


def _bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"1", "true", "yes"}
