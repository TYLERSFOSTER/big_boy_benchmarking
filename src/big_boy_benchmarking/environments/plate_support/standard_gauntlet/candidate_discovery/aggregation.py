"""Aggregation helpers for Stage 3 candidate discovery."""

from __future__ import annotations

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    CANDIDATE_DISCOVERY_STAGE_ID,
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    LINEARIZATION_MODE_ID,
    SUITE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.status import (
    CLAIM_STATUS_CANDIDATE_FOUND,
    CLAIM_STATUS_CANDIDATE_NOT_FOUND,
)


def build_stage3_aggregate_row(
    *,
    artifact_root: str,
    selected_rows: list[dict[str, object]],
    state_collapser_dependency_status: str,
) -> dict[str, object]:
    """Build the Stage 3 aggregate/status row."""

    selected_training_count = sum(
        1 for row in selected_rows if row["selection_status"] == "selected_training_candidate"
    )
    warning_count = sum(
        1 for row in selected_rows if row["selection_status"] == "selected_warning_candidate"
    )
    return {
        "suite_id": SUITE_ID,
        "stage_id": CANDIDATE_DISCOVERY_STAGE_ID,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "artifact_root": artifact_root,
        "status": "complete",
        "claim_status": (
            CLAIM_STATUS_CANDIDATE_FOUND
            if selected_training_count > 0
            else CLAIM_STATUS_CANDIDATE_NOT_FOUND
        ),
        "claim_boundary": "candidate classification only; no training or comparison claim",
        "source_stage_ids": "plate_support_gauntlet_contraction_schema_sweep_v001",
        "source_artifact_paths": "",
        "linearization_mode_id": LINEARIZATION_MODE_ID,
        "state_collapser_dependency_status": state_collapser_dependency_status,
        "selected_training_candidate_count": selected_training_count,
        "selected_warning_candidate_count": warning_count,
        "total_candidate_row_count": len(selected_rows),
        "blocking_reason": "" if selected_training_count else "candidate_not_found",
    }


def build_stage3_summary(aggregate_row: dict[str, object]) -> dict[str, object]:
    """Build JSON aggregate summary for Stage 3."""

    return {
        "status": aggregate_row["status"],
        "claim_status": aggregate_row["claim_status"],
        "selected_training_candidate_count": aggregate_row[
            "selected_training_candidate_count"
        ],
        "selected_warning_candidate_count": aggregate_row[
            "selected_warning_candidate_count"
        ],
        "blocking_reason": aggregate_row["blocking_reason"],
        "claim_boundary": aggregate_row["claim_boundary"],
    }
