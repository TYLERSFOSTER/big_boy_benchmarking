"""Calibration arm construction for PlateSupport gauntlet Stage 5."""

from __future__ import annotations

from dataclasses import dataclass

from .config import ThresholdFrontierCalibrationConfig
from .stage_sources import Stage4TrainingHealthSource, Stage5SourceError


@dataclass(frozen=True)
class CalibrationArm:
    """One trace-producing arm used only for target calibration."""

    calibration_arm_id: str
    calibration_arm_type: str
    candidate_id: str
    schema_id: str
    health_status: str
    trace_source: str
    source_stage_id: str


def build_calibration_arms(
    *,
    config: ThresholdFrontierCalibrationConfig,
    stage4_source: Stage4TrainingHealthSource,
) -> tuple[CalibrationArm, ...]:
    """Build calibration arms from validated upstream candidates."""

    if config.include_baseline_arm:
        raise Stage5SourceError(
            "baseline calibration arm is not implemented in the Stage 5 smoke path; "
            "rerun with selected Stage 4 traces only or design baseline semantics first"
        )
    if "selected_trainable_candidate" not in config.calibration_arms:
        raise Stage5SourceError(
            "Stage 5 currently requires the selected_trainable_candidate calibration arm"
        )
    arms = []
    for arm_index, candidate in enumerate(stage4_source.trainable_candidates):
        arms.append(
            CalibrationArm(
                calibration_arm_id=f"tower_candidate_{arm_index}",
                calibration_arm_type="selected_trainable_candidate_reused_stage4_trace",
                candidate_id=candidate.candidate_id,
                schema_id=candidate.schema_id,
                health_status=candidate.health_status,
                trace_source="stage4_training_health",
                source_stage_id="plate_support_gauntlet_tower_training_health_v001",
            )
        )
    return tuple(arms)
