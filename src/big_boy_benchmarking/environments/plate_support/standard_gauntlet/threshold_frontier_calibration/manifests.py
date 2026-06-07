"""Manifest payloads for PlateSupport gauntlet Stage 5."""

from __future__ import annotations

from datetime import UTC, datetime

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION

from ..ids import (
    STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
    SUITE_ID,
    THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
    TOWER_TRAINING_HEALTH_STAGE_ID,
)
from .calibration_arms import CalibrationArm
from .config import ThresholdFrontierCalibrationConfig
from .stage_sources import Stage1StructuralContext, Stage4TrainingHealthSource


def stage_manifest(config: ThresholdFrontierCalibrationConfig) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
        "stage_number": 5,
        "short_name": "threshold_frontier_calibration",
        "status": "run_requested",
        "run_label": config.run_label,
        "locked_by": config.locked_by,
        "created_at": _now(),
        "claim_boundary": "threshold calibration evidence only",
    }


def stage_budget_lock(config: ThresholdFrontierCalibrationConfig) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
        "run_label": config.run_label,
        "candidate_cap": config.candidate_cap,
        "allow_warning_candidates": config.allow_warning_candidates,
        "calibration_arms": list(config.calibration_arms),
        "target_types": list(config.target_types),
        "sustained_windows": [
            {"required_count": count, "window_length": length}
            for count, length in config.sustained_windows
        ],
        "threshold_grid_policy": {
            "construction": "observed_quantiles_success_boundary_and_stage1_context",
            "quantiles": list(config.threshold_quantiles),
            "hard_coded_threshold_values": [],
        },
        "recommended_episodes_per_replicate": config.recommended_episodes_per_replicate,
        "recommended_replicates_per_arm": config.recommended_replicates_per_arm,
        "include_baseline_arm": config.include_baseline_arm,
        "linearization_mode_id": config.linearization_mode_id,
    }


def stage_input_manifest(
    *,
    stage4_source: Stage4TrainingHealthSource,
    structural_context: Stage1StructuralContext,
) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
        "stage1_source": str(structural_context.path),
        "stage4_training_health_source": str(stage4_source.path),
        "source_stage_ids": [
            STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
            TOWER_TRAINING_HEALTH_STAGE_ID,
        ],
        "stage1_source_files": {
            key: str(path) for key, path in structural_context.source_files.items()
        },
        "stage4_source_files": {
            key: str(path) for key, path in stage4_source.source_files.items()
        },
        "selected_candidate_count": len(stage4_source.trainable_candidates),
    }


def threshold_policy_manifest(
    recommended_target_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
        "recommended_target": recommended_target_rows[0] if recommended_target_rows else {},
        "claim_boundary": "target policy only; no paired comparison claim",
    }


def calibration_arm_manifest(arms: tuple[CalibrationArm, ...]) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
        "arms": [
            {
                "calibration_arm_id": arm.calibration_arm_id,
                "calibration_arm_type": arm.calibration_arm_type,
                "candidate_id": arm.candidate_id,
                "schema_id": arm.schema_id,
                "health_status": arm.health_status,
                "trace_source": arm.trace_source,
                "source_stage_id": arm.source_stage_id,
            }
            for arm in arms
        ],
    }


def parent_training_health_manifest(
    stage4_source: Stage4TrainingHealthSource,
) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
        "parent_stage_id": TOWER_TRAINING_HEALTH_STAGE_ID,
        "parent_readout_source": str(stage4_source.path),
        "parent_artifact_root": str(stage4_source.source_artifact_root),
    }


def stage_output_manifest(output_paths: dict[str, str]) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
        "output_paths": output_paths,
    }


def _now() -> str:
    return datetime.now(UTC).isoformat()
