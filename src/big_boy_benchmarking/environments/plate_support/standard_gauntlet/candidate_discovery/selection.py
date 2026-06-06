"""Deterministic candidate selection for Stage 3."""

from __future__ import annotations

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.config import (
    CandidateDiscoveryConfig,
)


def select_candidates(
    classified_rows: list[dict[str, object]],
    *,
    config: CandidateDiscoveryConfig,
) -> list[dict[str, object]]:
    """Apply deterministic caps and final selection roles."""

    selected: list[dict[str, object]] = []
    control_rows = _sorted_rows(
        row for row in classified_rows if row["candidate_role"] == "selected_control_anchor"
    )
    clean_rows = _sorted_rows(
        row for row in classified_rows if row["candidate_role"] == "eligible_clean_candidate"
    )
    warning_rows = _sorted_rows(
        row for row in classified_rows if row["candidate_role"] == "warning_candidate"
    )
    degeneracy_rows = _sorted_rows(
        row for row in classified_rows if row["candidate_role"] == "degeneracy_anchor"
    )
    blocked_rows = _sorted_rows(
        row for row in classified_rows if row["candidate_role"] == "blocked_candidate"
    )
    for row in control_rows[:1]:
        selected.append({**row, "selection_status": "selected_control_anchor"})
    for row in clean_rows[: config.clean_candidate_cap]:
        selected.append({**row, "selection_status": "selected_training_candidate"})
    if config.allow_warning_selection:
        for row in warning_rows[: config.warning_candidate_cap]:
            selected.append({**row, "selection_status": "selected_warning_candidate"})
    for row in degeneracy_rows[: config.degeneracy_anchor_cap]:
        selected.append({**row, "selection_status": "selected_degeneracy_anchor"})
    selected_ids = {row["candidate_id"] for row in selected}
    for row in [*clean_rows, *warning_rows, *degeneracy_rows, *blocked_rows]:
        if row["candidate_id"] not in selected_ids:
            selected.append({**row, "selection_status": "not_selected"})
    return selected


def _sorted_rows(rows) -> list[dict[str, object]]:
    return sorted(
        rows,
        key=lambda row: (
            -int(row.get("eligibility_score", 0)),
            str(row.get("schema_family_id", "")),
            str(row.get("schema_id", "")),
            str(row.get("schema_seed", "")),
        ),
    )
