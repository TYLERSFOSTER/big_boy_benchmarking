"""Stable identifiers for the PlateSupport standard gauntlet suite."""

from __future__ import annotations

from dataclasses import dataclass

from big_boy_benchmarking.environments.plate_support.ids import (
    DEFAULT_INSTANCE_ID,
    ENVIRONMENT_FAMILY_ID,
)

SUITE_ID = "plate_support_standard_gauntlet_v001"
SUITE_RUN_FAMILY_ID = "plate_support_standard_gauntlet_v001"
ENVIRONMENT_INSTANCE_ID = DEFAULT_INSTANCE_ID
LINEARIZATION_MODE_ID = "tensor_available_disabled"

STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID = (
    "plate_support_gauntlet_structural_tower_diagnostics_v001"
)
CONTRACTION_SCHEMA_SWEEP_STAGE_ID = "plate_support_gauntlet_contraction_schema_sweep_v001"
CANDIDATE_DISCOVERY_STAGE_ID = "plate_support_gauntlet_candidate_discovery_v001"
TOWER_TRAINING_HEALTH_STAGE_ID = "plate_support_gauntlet_tower_training_health_v001"
THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID = (
    "plate_support_gauntlet_threshold_frontier_calibration_v001"
)
PAIRED_REPLICATE_COMPARISON_STAGE_ID = (
    "plate_support_gauntlet_paired_replicate_comparison_v001"
)
READOUT_SYSTEM_LEARNING_STAGE_ID = "plate_support_gauntlet_readout_system_learning_v001"

SUPPORTED_RUN_LABELS = ("smoke_001", "dev_001", "calibration_001", "serious_001")


@dataclass(frozen=True)
class StageDefinition:
    """Data-only stage identity and dependency declaration."""

    stage_number: int
    stage_id: str
    short_name: str
    required_predecessor_stage_ids: tuple[str, ...]


STAGE_DEFINITIONS = (
    StageDefinition(
        stage_number=1,
        stage_id=STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
        short_name="structural_and_tower_diagnostics",
        required_predecessor_stage_ids=(),
    ),
    StageDefinition(
        stage_number=2,
        stage_id=CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
        short_name="contraction_schema_sweep",
        required_predecessor_stage_ids=(STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,),
    ),
    StageDefinition(
        stage_number=3,
        stage_id=CANDIDATE_DISCOVERY_STAGE_ID,
        short_name="candidate_discovery",
        required_predecessor_stage_ids=(CONTRACTION_SCHEMA_SWEEP_STAGE_ID,),
    ),
    StageDefinition(
        stage_number=4,
        stage_id=TOWER_TRAINING_HEALTH_STAGE_ID,
        short_name="tower_training_health",
        required_predecessor_stage_ids=(CANDIDATE_DISCOVERY_STAGE_ID,),
    ),
    StageDefinition(
        stage_number=5,
        stage_id=THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
        short_name="threshold_frontier_calibration",
        required_predecessor_stage_ids=(
            STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
            TOWER_TRAINING_HEALTH_STAGE_ID,
        ),
    ),
    StageDefinition(
        stage_number=6,
        stage_id=PAIRED_REPLICATE_COMPARISON_STAGE_ID,
        short_name="paired_replicate_comparison",
        required_predecessor_stage_ids=(
            CANDIDATE_DISCOVERY_STAGE_ID,
            TOWER_TRAINING_HEALTH_STAGE_ID,
            THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
        ),
    ),
    StageDefinition(
        stage_number=7,
        stage_id=READOUT_SYSTEM_LEARNING_STAGE_ID,
        short_name="readout_and_system_learning",
        required_predecessor_stage_ids=(),
    ),
)

STAGE_IDS = tuple(stage.stage_id for stage in STAGE_DEFINITIONS)


def stage_definition_by_id(stage_id: str) -> StageDefinition:
    """Return the stable stage definition for a stage id."""

    for stage in STAGE_DEFINITIONS:
        if stage.stage_id == stage_id:
            return stage
    raise KeyError(f"unknown PlateSupport gauntlet stage id: {stage_id}")
