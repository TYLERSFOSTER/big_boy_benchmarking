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
    executability_rows: list[dict[str, object]],
    near_full_collapse_threshold: float,
    iterated_min_nontrivial_tiers: int = 3,
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
            executability_rows=executability_rows,
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
        (int(row.get("active_action_cell_count", 0)) for row in executability_rows),
        default=0,
    )
    nontrivial_tier_count = _nontrivial_tier_count(
        tower_rows=tower_rows,
        near_full_collapse_threshold=near_full_collapse_threshold,
    )
    nonbase_active_min = _nonbase_active_min(executability_rows)
    if arm.expected_role == "flat_control":
        structural_class = "flat_control"
        candidate_signal = "control_anchor"
        reason = "no-contraction control anchor"
        recommended = False
        blocking_reason = ""
    elif arm.schema_family_id == "source_local_ratio_iterated":
        if max_depth < 4:
            structural_class = "shallow_iterated_tower"
            candidate_signal = "warning_signal"
            reason = "iterated schema did not reach required tower depth"
            recommended = False
            blocking_reason = "shallow_iterated_tower"
        elif nontrivial_tier_count < iterated_min_nontrivial_tiers:
            structural_class = "insufficient_nontrivial_tiers"
            candidate_signal = "warning_signal"
            reason = "iterated schema did not produce enough non-collapsed tiers"
            recommended = False
            blocking_reason = "insufficient_nontrivial_tiers"
        elif largest_nonbase_share >= near_full_collapse_threshold:
            structural_class = "near_full_collapse"
            candidate_signal = "warning_signal"
            reason = "largest non-base tier cell share exceeds threshold"
            recommended = False
            blocking_reason = "near_full_collapse"
        elif nonbase_active_min <= 0:
            structural_class = "runtime_unexecutable"
            candidate_signal = "blocked_signal"
            reason = "at least one non-base iterated tier has no executable action cells"
            recommended = False
            blocking_reason = "runtime_unexecutable"
        else:
            structural_class = "nonflat_structured"
            candidate_signal = "eligible_signal"
            reason = "many-tier iterated tower with executable action surface"
            recommended = True
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
        executability_rows=executability_rows,
        near_full_collapse_threshold=near_full_collapse_threshold,
        blocking_reason=blocking_reason,
        nontrivial_tier_count=nontrivial_tier_count,
    )


def _classification_row(
    *,
    arm: SchemaArm,
    structural_class: str,
    candidate_signal: str,
    candidate_signal_reason: str,
    recommended: bool,
    tower_rows: list[dict[str, object]],
    executability_rows: list[dict[str, object]],
    near_full_collapse_threshold: float,
    blocking_reason: str,
    nontrivial_tier_count: int | None = None,
) -> dict[str, object]:
    nonbase_rows = [
        row for row in tower_rows if str(row.get("tier_index")) not in ("0", "not_applicable")
    ]
    first_nonbase = nonbase_rows[0] if nonbase_rows else {}
    active_counts = [
        int(row.get("active_action_cell_count", 0))
        for row in executability_rows
        if str(row.get("active_action_cell_count", "")).isdigit()
    ]
    lift_success_counts = [
        int(row.get("lift_success_probe_count", 0))
        for row in executability_rows
        if str(row.get("lift_success_probe_count", "")).isdigit()
    ]
    lift_failure_counts = [
        int(row.get("lift_failure_probe_count", 0))
        for row in executability_rows
        if str(row.get("lift_failure_probe_count", "")).isdigit()
    ]
    selected_edge_count = arm.selection_count
    zero_selected_source_count: object = "not_available"
    if nontrivial_tier_count is None:
        nontrivial_tier_count = _nontrivial_tier_count(
            tower_rows=tower_rows,
            near_full_collapse_threshold=near_full_collapse_threshold,
        )
    if arm.schema_family_id in ("source_local_ratio", "source_local_ratio_iterated"):
        selected_edge_count = max(
            (
                int(row.get("scheduled_assignment_count", 0))
                for row in tower_rows
                if str(row.get("scheduled_assignment_count", "")).isdigit()
            ),
            default=0,
        )
        zero_selected_source_count = (
            0 if arm.schema_family_id == "source_local_ratio" else "not_available"
        )
    return {
        "schema_id": arm.schema_id,
        "schema_family_id": arm.schema_family_id,
        "schema_seed": arm.schema_seed,
        "structural_class": structural_class,
        "candidate_signal": candidate_signal,
        "candidate_signal_reason": candidate_signal_reason,
        "schema_mode": arm.schema_mode,
        "selection_rate": arm.selection_rate,
        "ratio_numerator": "" if arm.ratio_numerator is None else arm.ratio_numerator,
        "ratio_denominator": "" if arm.ratio_denominator is None else arm.ratio_denominator,
        "max_iterations": "" if arm.max_iterations is None else arm.max_iterations,
        "selector_rule_id": arm.selector_rule_id,
        "selection_mode": arm.selection_mode,
        "max_depth": max((int(row.get("max_depth", 0)) for row in tower_rows), default=0),
        "nontrivial_tier_count": nontrivial_tier_count,
        "first_nonbase_tier_state_cell_count": first_nonbase.get("state_cell_count", 0),
        "largest_cell_share": max(
            (float(row.get("largest_cell_share", 0.0)) for row in tower_rows),
            default=0.0,
        ),
        "active_action_cell_min": min(active_counts, default=0),
        "active_action_cell_mean": (
            0.0 if not active_counts else sum(active_counts) / len(active_counts)
        ),
        "lift_success_probe_count": sum(lift_success_counts),
        "lift_failure_probe_count": sum(lift_failure_counts),
        "selected_edge_count": selected_edge_count,
        "zero_selected_source_count": zero_selected_source_count,
        "recommended_for_candidate_discovery": recommended,
        "blocking_reason": blocking_reason,
        "near_full_collapse_threshold": near_full_collapse_threshold,
    }


def _nontrivial_tier_count(
    *,
    tower_rows: list[dict[str, object]],
    near_full_collapse_threshold: float,
) -> int:
    return sum(
        1
        for row in tower_rows
        if str(row.get("tier_index")) not in ("0", "not_applicable")
        and int(row.get("state_cell_count", 0)) > 1
        and float(row.get("largest_cell_share", 1.0)) < near_full_collapse_threshold
    )


def _nonbase_active_min(executability_rows: list[dict[str, object]]) -> int:
    counts = [
        int(row.get("active_action_cell_count", 0))
        for row in executability_rows
        if str(row.get("tier_index")) not in ("0", "not_applicable")
        and str(row.get("active_action_cell_count", "")).isdigit()
    ]
    return min(counts, default=0)
