"""Candidate eligibility normalization and classification."""

from __future__ import annotations

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.candidate_ids import (
    candidate_id_for_row,
)


def normalize_candidate_rows(
    signal_rows: list[dict[str, str]],
    *,
    source_artifact_root: str,
) -> list[dict[str, object]]:
    """Normalize Stage 2 signal rows into candidate-discovery input rows."""

    normalized: list[dict[str, object]] = []
    for index, row in enumerate(signal_rows):
        candidate_row: dict[str, object] = {
            **row,
            "source_row_id": f"stage2_signal_row_{index:04d}",
            "source_artifact_root": source_artifact_root,
            "source_stage_id": "plate_support_gauntlet_contraction_schema_sweep_v001",
            "source_trace_status": "complete" if source_artifact_root else "blocked_missing_source",
        }
        candidate_row["candidate_id"] = candidate_id_for_row(candidate_row)
        normalized.append(candidate_row)
    return normalized


def classify_candidate(row: dict[str, object]) -> dict[str, object]:
    """Assign role, score, and eligibility explanation to one normalized row."""

    signal = str(row["candidate_signal"])
    structural_class = str(row["structural_class"])
    max_depth = int(row.get("max_depth", 0))
    active_min = float(row.get("active_action_cell_min", 0.0))
    if signal == "control_anchor":
        role = "selected_control_anchor"
        score = 0
        reason = "control anchor retained for downstream diagnostics"
        allowed = "diagnostic_control"
    elif signal == "eligible_signal" and structural_class == "nonflat_structured":
        role = "eligible_clean_candidate"
        score = 100 + max_depth + int(active_min)
        reason = "nonflat structured schema with executable action surface"
        allowed = "stage4_training_health"
    elif signal == "warning_signal":
        role = "warning_candidate"
        score = 40 + max_depth
        reason = f"warning candidate: {row.get('candidate_signal_reason', '')}"
        allowed = "stage4_requires_warning_authorization"
    elif signal == "degeneracy_anchor":
        role = "degeneracy_anchor"
        score = -10
        reason = "diagnostic degeneracy anchor retained for interpretation only"
        allowed = "diagnostic_only"
    else:
        role = "blocked_candidate"
        score = -100
        reason = f"blocked: {row.get('blocking_reason') or row.get('candidate_signal_reason')}"
        allowed = "none"
    return {
        **row,
        "candidate_role": role,
        "eligibility_score": score,
        "eligibility_reason": reason,
        "allowed_downstream_stage": allowed,
    }
