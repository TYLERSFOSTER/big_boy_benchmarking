"""Target feasibility and recommendation rules for Stage 5."""

from __future__ import annotations

from .config import ThresholdFrontierCalibrationConfig
from .target_policies import (
    BINARY_SUCCESS_TARGET_POLICY_ID,
    CLAIM_BOUNDARY,
    FIRST_HIT_TARGET_POLICY_ID,
    RETURN_THRESHOLD_TARGET_POLICY_ID,
)


def build_recommended_target_rows(
    *,
    config: ThresholdFrontierCalibrationConfig,
    calibration_arm_summary: list[dict[str, object]],
    first_hit_summary: list[dict[str, object]],
    threshold_frontier_summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Return zero or one recommended comparison target rows."""

    if "binary_success" in config.target_types:
        row = _binary_success_target(config, calibration_arm_summary)
        if row is not None:
            return [row]

    if "first_hit" in config.target_types:
        row = _first_hit_target(config, first_hit_summary)
        if row is not None:
            return [row]

    if "return_threshold" in config.target_types:
        row = _return_threshold_target(config, threshold_frontier_summary)
        if row is not None:
            return [row]

    return []


def unresolved_target_row(reason: str) -> dict[str, object]:
    """Build a blocked target row for summaries that allow no recommendation."""

    return {
        "target_policy_id": "",
        "target_type": "unresolved",
        "threshold_value": "",
        "window_length": "",
        "required_count": "",
        "episodes_required_minimum": "",
        "recommended_episodes_per_replicate": "",
        "recommended_replicates_per_arm": "",
        "baseline_feasibility": "unresolved",
        "candidate_feasibility": "unresolved",
        "calibration_status": "threshold_unresolved",
        "claim_boundary": CLAIM_BOUNDARY,
        "reason": reason,
    }


def _binary_success_target(
    config: ThresholdFrontierCalibrationConfig,
    arm_rows: list[dict[str, object]],
) -> dict[str, object] | None:
    candidate_rows = [
        row
        for row in arm_rows
        if str(row["calibration_arm_type"]).startswith("selected_trainable_candidate")
    ]
    for row in candidate_rows:
        success_count = int(row["success_count"])
        episode_count = int(row["episode_count"])
        if 0 < success_count < episode_count:
            return {
                "target_policy_id": BINARY_SUCCESS_TARGET_POLICY_ID,
                "target_type": "binary_success",
                "threshold_value": "",
                "window_length": "",
                "required_count": "1",
                "episodes_required_minimum": "1",
                "recommended_episodes_per_replicate": (
                    config.recommended_episodes_per_replicate
                ),
                "recommended_replicates_per_arm": config.recommended_replicates_per_arm,
                "baseline_feasibility": "not_required_for_binary_success_definition",
                "candidate_feasibility": (
                    f"feasible_sparse_success_{success_count}_of_{episode_count}"
                ),
                "calibration_status": "threshold_calibrated",
                "claim_boundary": CLAIM_BOUNDARY,
                "reason": (
                    "Stage 4 traces contain both goal hits and misses for a "
                    "trainable candidate, so goal_reached is a table-backed target. "
                    "Success is sparse, so Stage 6 should use a larger paired budget."
                ),
            }
        if success_count == episode_count and episode_count > 0:
            return {
                "target_policy_id": BINARY_SUCCESS_TARGET_POLICY_ID,
                "target_type": "binary_success",
                "threshold_value": "",
                "window_length": "",
                "required_count": "1",
                "episodes_required_minimum": "1",
                "recommended_episodes_per_replicate": (
                    config.recommended_episodes_per_replicate
                ),
                "recommended_replicates_per_arm": config.recommended_replicates_per_arm,
                "baseline_feasibility": "not_required_for_binary_success_definition",
                "candidate_feasibility": "feasible_all_observed_episodes_succeed",
                "calibration_status": "threshold_calibrated",
                "claim_boundary": CLAIM_BOUNDARY,
                "reason": (
                    "Stage 4 traces show candidate success on every observed episode. "
                    "Binary success is valid, but Stage 6 should verify this is not a "
                    "smoke-budget artifact."
                ),
            }
    return None


def _first_hit_target(
    config: ThresholdFrontierCalibrationConfig,
    first_hit_rows: list[dict[str, object]],
) -> dict[str, object] | None:
    hit_rows = [row for row in first_hit_rows if str(row["hit_observed"]) == "1"]
    if not hit_rows:
        return None
    min_required = min(int(row["first_hit_episode_index"]) + 1 for row in hit_rows)
    return {
        "target_policy_id": FIRST_HIT_TARGET_POLICY_ID,
        "target_type": "first_hit",
        "threshold_value": "",
        "window_length": "",
        "required_count": "1",
        "episodes_required_minimum": min_required,
        "recommended_episodes_per_replicate": config.recommended_episodes_per_replicate,
        "recommended_replicates_per_arm": config.recommended_replicates_per_arm,
        "baseline_feasibility": "not_required_for_first_hit_definition",
        "candidate_feasibility": f"feasible_first_hit_observed_in_{len(hit_rows)}_replicate_rows",
        "calibration_status": "threshold_calibrated",
        "claim_boundary": CLAIM_BOUNDARY,
        "reason": (
            "At least one calibration replicate reached the goal, so first-hit is "
            "a valid secondary target. Binary success remains preferred when it has "
            "both hit and miss variation."
        ),
    }


def _return_threshold_target(
    config: ThresholdFrontierCalibrationConfig,
    frontier_rows: list[dict[str, object]],
) -> dict[str, object] | None:
    feasible_rows = [
        row
        for row in frontier_rows
        if row["feasibility_status"] == "feasible_nontrivial"
    ]
    if not feasible_rows:
        return None
    chosen = min(feasible_rows, key=lambda row: abs(float(row["hit_rate"]) - 0.25))
    return {
        "target_policy_id": RETURN_THRESHOLD_TARGET_POLICY_ID,
        "target_type": "return_threshold",
        "threshold_value": chosen["threshold_value"],
        "window_length": "",
        "required_count": "1",
        "episodes_required_minimum": "1",
        "recommended_episodes_per_replicate": config.recommended_episodes_per_replicate,
        "recommended_replicates_per_arm": config.recommended_replicates_per_arm,
        "baseline_feasibility": "not_calibrated_in_stage5_smoke",
        "candidate_feasibility": (
            f"feasible_nontrivial_hit_rate_{float(chosen['hit_rate']):.6f}"
        ),
        "calibration_status": "threshold_calibrated",
        "claim_boundary": CLAIM_BOUNDARY,
        "reason": (
            "No simpler success target was selected, so the return target falls "
            "back to an observed nontrivial reward threshold with provenance in "
            "threshold_grid_construction.csv."
        ),
    }
