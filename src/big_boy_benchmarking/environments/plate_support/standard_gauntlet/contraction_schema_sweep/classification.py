"""Collapse classification and candidate-signal logic for Stage 2."""

from __future__ import annotations

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.schema_builders import (
    SchemaConstructionResult,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.schema_families import (
    SchemaArm,
)


def classify_schema_arm(
    *,
    arm: SchemaArm,
    construction: SchemaConstructionResult,
    tower_rows: list[dict[str, object]],
    near_full_collapse_threshold: float,
) -> dict[str, object]:
    """Classify one schema arm from table-backed evidence."""

    if construction.construction_status != "constructed":
        structural_class = "construction_failed"
        candidate_signal = (
            "degeneracy_anchor"
            if arm.schema_family_id == "controlled_degeneracy"
            else "blocked_signal"
        )
        reason = construction.blocking_reason
        return _classification_row(
            arm=arm,
            structural_class=structural_class,
            candidate_signal=candidate_signal,
            candidate_signal_reason=reason,
            recommended=False,
            tower_rows=tower_rows,
            near_full_collapse_threshold=near_full_collapse_threshold,
            blocking_reason=reason,
        )

    max_depth = max(int(row["max_depth"]) for row in tower_rows)
    nonbase_rows = [row for row in tower_rows if int(row["tier_index"]) > 0]
    largest_nonbase_share = max(
        (float(row["largest_cell_share"]) for row in nonbase_rows),
        default=0.0,
    )
    active_min = min(
        (int(row.get("active_action_cell_count", 0)) for row in tower_rows),
        default=0,
    )
    if arm.expected_role == "flat_control":
        structural_class = "flat_control"
        candidate_signal = "control_anchor"
        reason = "no-contraction control anchor"
        recommended = False
        blocking_reason = ""
    elif max_depth <= 1:
        structural_class = "near_flat"
        candidate_signal = "warning_signal"
        reason = "schema remained flat or nearly flat"
        recommended = False
        blocking_reason = "near_flat"
    elif largest_nonbase_share >= 1.0:
        structural_class = "full_first_projection_collapse"
        candidate_signal = "blocked_signal"
        reason = "first non-base tier collapses all observed states"
        recommended = False
        blocking_reason = "full_first_projection_collapse"
    elif largest_nonbase_share >= near_full_collapse_threshold:
        structural_class = "near_full_collapse"
        candidate_signal = "warning_signal"
        reason = "largest non-base tier cell share exceeds threshold"
        recommended = False
        blocking_reason = "near_full_collapse"
    elif active_min <= 0:
        structural_class = "runtime_unexecutable"
        candidate_signal = "blocked_signal"
        reason = "at least one observed tier has no executable action cells"
        recommended = False
        blocking_reason = "runtime_unexecutable"
    else:
        structural_class = "nonflat_structured"
        candidate_signal = "eligible_signal"
        reason = "non-flat tower with executable action surface in smoke probe"
        recommended = True
        blocking_reason = ""
    return _classification_row(
        arm=arm,
        structural_class=structural_class,
        candidate_signal=candidate_signal,
        candidate_signal_reason=reason,
        recommended=recommended,
        tower_rows=tower_rows,
        near_full_collapse_threshold=near_full_collapse_threshold,
        blocking_reason=blocking_reason,
    )


def _classification_row(
    *,
    arm: SchemaArm,
    structural_class: str,
    candidate_signal: str,
    candidate_signal_reason: str,
    recommended: bool,
    tower_rows: list[dict[str, object]],
    near_full_collapse_threshold: float,
    blocking_reason: str,
) -> dict[str, object]:
    nonbase_rows = [
        row for row in tower_rows if str(row.get("tier_index")) not in ("0", "not_applicable")
    ]
    first_nonbase = nonbase_rows[0] if nonbase_rows else {}
    active_counts = [
        int(row.get("active_action_cell_count", 0))
        for row in tower_rows
        if str(row.get("active_action_cell_count", "")).isdigit()
    ]
    return {
        "schema_id": arm.schema_id,
        "schema_family_id": arm.schema_family_id,
        "schema_seed": arm.schema_seed,
        "structural_class": structural_class,
        "candidate_signal": candidate_signal,
        "candidate_signal_reason": candidate_signal_reason,
        "max_depth": max((int(row.get("max_depth", 0)) for row in tower_rows), default=0),
        "first_nonbase_tier_state_cell_count": first_nonbase.get("state_cell_count", 0),
        "largest_cell_share": max(
            (float(row.get("largest_cell_share", 0.0)) for row in tower_rows),
            default=0.0,
        ),
        "active_action_cell_min": min(active_counts, default=0),
        "active_action_cell_mean": (
            0.0 if not active_counts else sum(active_counts) / len(active_counts)
        ),
        "lift_success_probe_count": sum(active_counts),
        "lift_failure_probe_count": sum(1 for count in active_counts if count == 0),
        "selected_edge_count": arm.selection_count,
        "zero_selected_source_count": "not_available",
        "recommended_for_candidate_discovery": recommended,
        "blocking_reason": blocking_reason,
        "near_full_collapse_threshold": near_full_collapse_threshold,
    }
