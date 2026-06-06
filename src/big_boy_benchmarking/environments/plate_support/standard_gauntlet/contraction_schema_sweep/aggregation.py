"""Aggregation helpers for Stage 2 schema sweep."""

from __future__ import annotations

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    LINEARIZATION_MODE_ID,
    SUITE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.status import (
    CLAIM_STATUS_DIAGNOSTIC_COMPLETE,
    CLAIM_STATUS_PROTOCOL_BLOCKED,
)


def build_stage2_aggregate_row(
    *,
    artifact_root: str,
    candidate_rows: list[dict[str, object]],
    mandatory_failures: list[str],
    warning_count: int,
    state_collapser_dependency_status: str,
) -> dict[str, object]:
    """Build Stage 2 aggregate/status row."""

    eligible_count = sum(
        1 for row in candidate_rows if row["candidate_signal"] == "eligible_signal"
    )
    status = "blocked" if mandatory_failures else "complete"
    return {
        "suite_id": SUITE_ID,
        "stage_id": CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "artifact_root": artifact_root,
        "status": status,
        "claim_status": (
            CLAIM_STATUS_DIAGNOSTIC_COMPLETE
            if status == "complete"
            else CLAIM_STATUS_PROTOCOL_BLOCKED
        ),
        "claim_boundary": "schema structural diagnostics and candidate signals only",
        "source_stage_ids": "plate_support_gauntlet_structural_tower_diagnostics_v001",
        "source_artifact_paths": "",
        "linearization_mode_id": LINEARIZATION_MODE_ID,
        "state_collapser_dependency_status": state_collapser_dependency_status,
        "warning_count": warning_count,
        "schema_arm_count": len(candidate_rows),
        "eligible_signal_count": eligible_count,
        "blocking_reason": "|".join(mandatory_failures),
    }


def build_stage2_summary(aggregate_row: dict[str, object]) -> dict[str, object]:
    """Build JSON aggregate summary for Stage 2."""

    return {
        "status": aggregate_row["status"],
        "claim_status": aggregate_row["claim_status"],
        "stage_id": aggregate_row["stage_id"],
        "schema_arm_count": aggregate_row["schema_arm_count"],
        "eligible_signal_count": aggregate_row["eligible_signal_count"],
        "blocking_reason": aggregate_row["blocking_reason"],
        "claim_boundary": aggregate_row["claim_boundary"],
    }
