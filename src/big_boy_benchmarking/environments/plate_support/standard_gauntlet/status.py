"""Shared status vocabulary for the PlateSupport standard gauntlet."""

from __future__ import annotations

from dataclasses import dataclass

CLAIM_STATUS_ENVIRONMENT_READY = "environment_ready"
CLAIM_STATUS_DIAGNOSTIC_COMPLETE = "diagnostic_complete"
CLAIM_STATUS_DIAGNOSTIC_BLOCKED = "diagnostic_blocked"
CLAIM_STATUS_CANDIDATE_FOUND = "candidate_found"
CLAIM_STATUS_CANDIDATE_NOT_FOUND = "candidate_not_found"
CLAIM_STATUS_TRAINABLE_CLEAN = "trainable_clean"
CLAIM_STATUS_TRAINABLE_WARNING = "trainable_warning"
CLAIM_STATUS_TRAINING_HEALTH_BLOCKED = "training_health_blocked"
CLAIM_STATUS_THRESHOLD_CALIBRATED = "threshold_calibrated"
CLAIM_STATUS_THRESHOLD_UNRESOLVED = "threshold_unresolved"
CLAIM_STATUS_PAIRED_COMPARISON_POSITIVE_SIGNAL = "paired_comparison_positive_signal"
CLAIM_STATUS_PAIRED_COMPARISON_NEGATIVE_SIGNAL = "paired_comparison_negative_signal"
CLAIM_STATUS_PAIRED_COMPARISON_INCONCLUSIVE = "paired_comparison_inconclusive"
CLAIM_STATUS_READOUT_COMPLETE = "readout_complete"
CLAIM_STATUS_ARTIFACT_INCOMPLETE = "artifact_incomplete"
CLAIM_STATUS_PROTOCOL_BLOCKED = "protocol_blocked"

CLAIM_STATUS_VOCABULARY = (
    CLAIM_STATUS_ENVIRONMENT_READY,
    CLAIM_STATUS_DIAGNOSTIC_COMPLETE,
    CLAIM_STATUS_DIAGNOSTIC_BLOCKED,
    CLAIM_STATUS_CANDIDATE_FOUND,
    CLAIM_STATUS_CANDIDATE_NOT_FOUND,
    CLAIM_STATUS_TRAINABLE_CLEAN,
    CLAIM_STATUS_TRAINABLE_WARNING,
    CLAIM_STATUS_TRAINING_HEALTH_BLOCKED,
    CLAIM_STATUS_THRESHOLD_CALIBRATED,
    CLAIM_STATUS_THRESHOLD_UNRESOLVED,
    CLAIM_STATUS_PAIRED_COMPARISON_POSITIVE_SIGNAL,
    CLAIM_STATUS_PAIRED_COMPARISON_NEGATIVE_SIGNAL,
    CLAIM_STATUS_PAIRED_COMPARISON_INCONCLUSIVE,
    CLAIM_STATUS_READOUT_COMPLETE,
    CLAIM_STATUS_ARTIFACT_INCOMPLETE,
    CLAIM_STATUS_PROTOCOL_BLOCKED,
)

STAGE_STATUS_FIELDS = (
    "suite_id",
    "stage_id",
    "environment_family_id",
    "environment_instance_id",
    "artifact_root",
    "status",
    "claim_status",
    "claim_boundary",
    "source_stage_ids",
    "source_artifact_paths",
    "linearization_mode_id",
    "state_collapser_dependency_status",
)


@dataclass(frozen=True)
class StageStatusRow:
    """Shared row shape every gauntlet stage can emit."""

    suite_id: str
    stage_id: str
    environment_family_id: str
    environment_instance_id: str
    artifact_root: str
    status: str
    claim_status: str
    claim_boundary: str
    source_stage_ids: tuple[str, ...]
    source_artifact_paths: tuple[str, ...]
    linearization_mode_id: str
    state_collapser_dependency_status: str

    def to_row(self) -> dict[str, object]:
        """Return a JSON/CSV-friendly row mapping."""

        return {
            "suite_id": self.suite_id,
            "stage_id": self.stage_id,
            "environment_family_id": self.environment_family_id,
            "environment_instance_id": self.environment_instance_id,
            "artifact_root": self.artifact_root,
            "status": self.status,
            "claim_status": self.claim_status,
            "claim_boundary": self.claim_boundary,
            "source_stage_ids": list(self.source_stage_ids),
            "source_artifact_paths": list(self.source_artifact_paths),
            "linearization_mode_id": self.linearization_mode_id,
            "state_collapser_dependency_status": self.state_collapser_dependency_status,
        }


def validate_claim_status(claim_status: str) -> str:
    """Return a claim status after checking it against the shared vocabulary."""

    if claim_status not in CLAIM_STATUS_VOCABULARY:
        raise ValueError(f"unknown PlateSupport gauntlet claim status: {claim_status}")
    return claim_status
