"""Aggregation helpers for PlateSupport gauntlet Stage 1."""

from __future__ import annotations

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    LINEARIZATION_MODE_ID,
    STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
    SUITE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.status import (
    CLAIM_STATUS_DIAGNOSTIC_COMPLETE,
    CLAIM_STATUS_PROTOCOL_BLOCKED,
)


def build_stage_aggregate_row(
    *,
    artifact_root: str,
    downstream_row: dict[str, object],
    warning_count: int,
    state_collapser_dependency_status: str,
) -> dict[str, object]:
    """Build the Stage 1 aggregate/status row."""

    ready = bool(downstream_row["ready_for_schema_sweep"])
    claim_status = CLAIM_STATUS_DIAGNOSTIC_COMPLETE if ready else CLAIM_STATUS_PROTOCOL_BLOCKED
    return {
        "suite_id": SUITE_ID,
        "stage_id": STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "artifact_root": artifact_root,
        "status": "complete" if ready else "blocked",
        "claim_status": claim_status,
        "claim_boundary": "diagnostic-only; schema-sweep readiness if pass criteria hold",
        "source_stage_ids": "",
        "source_artifact_paths": "",
        "linearization_mode_id": LINEARIZATION_MODE_ID,
        "state_collapser_dependency_status": state_collapser_dependency_status,
        "warning_count": warning_count,
        "ready_for_schema_sweep": ready,
        "blocking_reason": downstream_row["blocking_reason"],
    }


def build_stage_aggregate_summary(aggregate_row: dict[str, object]) -> dict[str, object]:
    """Build a JSON summary from the aggregate row."""

    return {
        "status": aggregate_row["status"],
        "claim_status": aggregate_row["claim_status"],
        "stage_id": aggregate_row["stage_id"],
        "ready_for_schema_sweep": aggregate_row["ready_for_schema_sweep"],
        "blocking_reason": aggregate_row["blocking_reason"],
        "claim_boundary": aggregate_row["claim_boundary"],
    }
