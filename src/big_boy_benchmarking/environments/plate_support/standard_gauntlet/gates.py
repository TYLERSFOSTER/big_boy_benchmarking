"""Data-only gate definitions for the PlateSupport standard gauntlet."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    CANDIDATE_DISCOVERY_STAGE_ID,
    CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
    PAIRED_REPLICATE_COMPARISON_STAGE_ID,
    READOUT_SYSTEM_LEARNING_STAGE_ID,
    STAGE_IDS,
    STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
    THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
    TOWER_TRAINING_HEALTH_STAGE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.status import (
    CLAIM_STATUS_CANDIDATE_FOUND,
    CLAIM_STATUS_DIAGNOSTIC_COMPLETE,
    CLAIM_STATUS_THRESHOLD_CALIBRATED,
    CLAIM_STATUS_TRAINABLE_CLEAN,
    CLAIM_STATUS_TRAINABLE_WARNING,
)


@dataclass(frozen=True)
class StageGate:
    """Inspectable gate contract for one gauntlet stage."""

    stage_id: str
    required_predecessor_statuses: Mapping[str, tuple[str, ...]]
    required_source_artifact_roles: tuple[str, ...]
    claim_boundary: str
    allow_any_prior_artifact: bool = False

    def missing_requirements(
        self,
        completed_statuses: Mapping[str, str],
        available_artifact_roles: set[str],
    ) -> tuple[str, ...]:
        """Return human-readable missing requirements for this gate."""

        missing: list[str] = []
        for stage_id, accepted_statuses in self.required_predecessor_statuses.items():
            status = completed_statuses.get(stage_id)
            if status not in accepted_statuses:
                missing.append(
                    f"{stage_id} status must be one of {accepted_statuses}, got {status!r}"
                )
        for role in self.required_source_artifact_roles:
            if role not in available_artifact_roles:
                missing.append(f"missing source artifact role: {role}")
        if self.allow_any_prior_artifact and not available_artifact_roles:
            missing.append("at least one prior artifact-producing stage is required")
        return tuple(missing)

    def can_run(
        self,
        completed_statuses: Mapping[str, str],
        available_artifact_roles: set[str],
    ) -> bool:
        """Return whether this data-only gate is satisfied."""

        return not self.missing_requirements(completed_statuses, available_artifact_roles)


STAGE_GATES = {
    STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID: StageGate(
        stage_id=STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
        required_predecessor_statuses={},
        required_source_artifact_roles=(
            "environment_readiness_source",
            "environment_instance_doc",
            "state_collapser_dependency_state",
        ),
        claim_boundary="diagnostic-only structural and tower readiness evidence",
    ),
    CONTRACTION_SCHEMA_SWEEP_STAGE_ID: StageGate(
        stage_id=CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
        required_predecessor_statuses={
            STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID: (CLAIM_STATUS_DIAGNOSTIC_COMPLETE,),
        },
        required_source_artifact_roles=("stage1_structural_tables", "stage1_tower_tables"),
        claim_boundary="candidate-producing structural sweep evidence only",
    ),
    CANDIDATE_DISCOVERY_STAGE_ID: StageGate(
        stage_id=CANDIDATE_DISCOVERY_STAGE_ID,
        required_predecessor_statuses={
            CONTRACTION_SCHEMA_SWEEP_STAGE_ID: (CLAIM_STATUS_DIAGNOSTIC_COMPLETE,),
        },
        required_source_artifact_roles=("stage2_schema_sweep_tables",),
        claim_boundary="candidate eligibility evidence only",
    ),
    TOWER_TRAINING_HEALTH_STAGE_ID: StageGate(
        stage_id=TOWER_TRAINING_HEALTH_STAGE_ID,
        required_predecessor_statuses={
            CANDIDATE_DISCOVERY_STAGE_ID: (CLAIM_STATUS_CANDIDATE_FOUND,),
        },
        required_source_artifact_roles=("stage3_candidate_manifest",),
        claim_boundary="tower-only training health evidence, not comparison evidence",
    ),
    THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID: StageGate(
        stage_id=THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
        required_predecessor_statuses={
            STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID: (CLAIM_STATUS_DIAGNOSTIC_COMPLETE,),
            TOWER_TRAINING_HEALTH_STAGE_ID: (
                CLAIM_STATUS_TRAINABLE_CLEAN,
                CLAIM_STATUS_TRAINABLE_WARNING,
            ),
        },
        required_source_artifact_roles=(
            "stage1_reward_scale_tables",
            "stage4_training_health_tables",
        ),
        claim_boundary="threshold calibration evidence only",
    ),
    PAIRED_REPLICATE_COMPARISON_STAGE_ID: StageGate(
        stage_id=PAIRED_REPLICATE_COMPARISON_STAGE_ID,
        required_predecessor_statuses={
            CANDIDATE_DISCOVERY_STAGE_ID: (CLAIM_STATUS_CANDIDATE_FOUND,),
            TOWER_TRAINING_HEALTH_STAGE_ID: (
                CLAIM_STATUS_TRAINABLE_CLEAN,
                CLAIM_STATUS_TRAINABLE_WARNING,
            ),
            THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID: (
                CLAIM_STATUS_THRESHOLD_CALIBRATED,
            ),
        },
        required_source_artifact_roles=(
            "stage3_candidate_manifest",
            "stage4_training_health_summary",
            "stage5_threshold_policy",
            "matched_seed_policy",
        ),
        claim_boundary="bounded paired comparison evidence",
    ),
    READOUT_SYSTEM_LEARNING_STAGE_ID: StageGate(
        stage_id=READOUT_SYSTEM_LEARNING_STAGE_ID,
        required_predecessor_statuses={},
        required_source_artifact_roles=(),
        claim_boundary="human-readable synthesis and system-learning archive",
        allow_any_prior_artifact=True,
    ),
}


def gate_for_stage(stage_id: str) -> StageGate:
    """Return the gate contract for a stage id."""

    if stage_id not in STAGE_IDS:
        raise KeyError(f"unknown PlateSupport gauntlet stage id: {stage_id}")
    return STAGE_GATES[stage_id]
