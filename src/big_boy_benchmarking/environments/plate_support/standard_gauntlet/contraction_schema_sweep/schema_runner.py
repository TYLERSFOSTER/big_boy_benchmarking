"""Tower probe execution for constructed PlateSupport schema sweep arms."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from state_collapser.core.edges import BaseEdge
from state_collapser.examples.tower_depth_probe import continuous_probe
from state_collapser.examples.tower_depth_probe import (
    build_contraction_schema as build_probe_schema,
)
from state_collapser.tower.partition.tower import build_partition_tower_full

from big_boy_benchmarking.environments.plate_support.ids import UPSTREAM_SMOKE_ID
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.config import (
    SchemaSweepConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.schema_builders import (
    SchemaConstructionResult,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.schema_families import (
    SchemaArm,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.source_local_ratio_schema import (
    IteratedSourceLocalOutgoingRatioSchema,
    SourceLocalOutgoingRatioSchema,
)
from big_boy_benchmarking.environments.plate_support.upstream import import_plate_support_surface


@dataclass(frozen=True)
class PlateSupportGraphInputs:
    """Exact full-graph inputs for BBB-owned PlateSupport schema construction."""

    surface: object
    core_states: tuple[Any, ...]
    edges: tuple[BaseEdge, ...]
    current_base_state: Any


@dataclass(frozen=True)
class SchemaTowerDiagnostics:
    """Tower diagnostics for a constructed schema arm."""

    tower_shape_rows: tuple[dict[str, object], ...]
    tier_occupancy_rows: tuple[dict[str, object], ...]
    tier_executability_rows: tuple[dict[str, object], ...]
    endpoint_coalescence_rows: tuple[dict[str, object], ...]
    timing_rows: tuple[dict[str, object], ...]
    iterated_plan_rows: tuple[dict[str, object], ...] = ()
    iterated_schema_stop_rows: tuple[dict[str, object], ...] = ()
    many_tier_candidate_signal_rows: tuple[dict[str, object], ...] = ()


def run_schema_tower_diagnostics(
    *,
    arm: SchemaArm,
    construction: SchemaConstructionResult,
    config: SchemaSweepConfig,
) -> SchemaTowerDiagnostics:
    """Run tower diagnostics for one constructed arm."""

    if construction.construction_status != "constructed":
        empty = _blocked_rows(arm=arm, construction=construction)
        return SchemaTowerDiagnostics(
            tower_shape_rows=(empty["tower_shape"],),
            tier_occupancy_rows=(empty["tier_occupancy"],),
            tier_executability_rows=(empty["tier_executability"],),
            endpoint_coalescence_rows=(empty["endpoint_coalescence"],),
            timing_rows=(empty["timing"],),
        )

    if arm.schema_mode == "source_local_ratio":
        return _run_source_local_ratio_tower_diagnostics(arm=arm)
    if arm.schema_mode == "source_local_ratio_iterated":
        return _run_source_local_ratio_iterated_tower_diagnostics(
            arm=arm,
            config=config,
        )

    depth_probe = continuous_probe(
        env_name=UPSTREAM_SMOKE_ID,
        steps=config.tower_probe_steps,
        seed=arm.schema_seed,
        sample_size=config.tower_probe_sample_size,
        use_contraction_policy=True,
        reset_on_terminal=True,
        schema_mode=arm.schema_mode,
    )
    surface = import_plate_support_surface()
    if arm.schema_mode == "default":
        runtime = surface.create_runtime(schema=surface.default_plate_support_schema())
    else:
        runtime = surface.create_runtime(schema=build_probe_schema(schema_mode=arm.schema_mode))
    reset_result = runtime.reset(seed=config.smoke_seed + arm.schema_seed)
    partition_tower = runtime.tower_runtime.partition_tower
    current_positions = reset_result.runtime_snapshot.current_position_at_every_tier
    current_base_state = reset_result.runtime_snapshot.current_base_state

    tower_shape_rows: list[dict[str, object]] = []
    tier_occupancy_rows: list[dict[str, object]] = []
    tier_executability_rows: list[dict[str, object]] = []
    endpoint_rows: list[dict[str, object]] = []
    for tier_index, state_layer in enumerate(partition_tower.state_layers):
        action_layer = partition_tower.action_layers[tier_index]
        state_member_counts = [
            len(members) for members in state_layer.members_by_cell_id.values()
        ]
        total_state_members = sum(state_member_counts)
        largest_share = (
            0.0 if total_state_members == 0 else max(state_member_counts) / total_state_members
        )
        singleton_share = (
            0.0
            if total_state_members == 0
            else sum(1 for count in state_member_counts if count == 1) / len(state_member_counts)
        )
        current_cell = current_positions[tier_index]
        outgoing = partition_tower.outgoing_action_cells(tier_index, current_cell)
        executable = partition_tower.executable_action_cells(
            tier_index,
            current_cell,
            current_base_state,
        )
        action_cell_count = len(action_layer.edge_ids_by_action_cell)
        endpoint_pairs = {
            (
                str(action_layer.source_cell_by_action_cell.get(action_cell)),
                str(action_layer.target_cell_by_action_cell.get(action_cell)),
            )
            for action_cell in action_layer.edge_ids_by_action_cell
        }
        tower_shape_rows.append(
            {
                "schema_id": arm.schema_id,
                "schema_family_id": arm.schema_family_id,
                "schema_seed": arm.schema_seed,
                "tier_index": tier_index,
                "max_depth": int(depth_probe.max_depth),
                "state_cell_count": len(state_layer.members_by_cell_id),
                "action_cell_count": action_cell_count,
                "largest_cell_share": largest_share,
                "singleton_cell_share": singleton_share,
                "scheduled_assignment_count": int(depth_probe.scheduled_assignment_count),
                "unscheduled_assignment_count": int(depth_probe.unscheduled_assignment_count),
                "depth_curve": json.dumps(depth_probe.depth_curve, separators=(",", ":")),
                "reset_event_count": len(depth_probe.reset_events),
                "diagnostic_status": "ok",
            }
        )
        tier_occupancy_rows.append(
            {
                "schema_id": arm.schema_id,
                "schema_family_id": arm.schema_family_id,
                "schema_seed": arm.schema_seed,
                "tier_index": tier_index,
                "current_state_cell": str(current_cell),
                "state_cell_count": len(state_layer.members_by_cell_id),
                "outgoing_action_cell_count": len(outgoing),
                "active_action_cell_count": len(executable),
                "diagnostic_status": "ok",
            }
        )
        tier_executability_rows.append(
            {
                "schema_id": arm.schema_id,
                "schema_family_id": arm.schema_family_id,
                "schema_seed": arm.schema_seed,
                "tier_index": tier_index,
                "tier_executable_from_current_state": partition_tower.tier_is_executable_from_state(
                    tier_index,
                    current_base_state,
                ),
                "lift_success_probe_count": len(executable),
                "lift_failure_probe_count": 0 if executable else 1,
                "active_action_cell_count": len(executable),
                "diagnostic_status": "ok",
            }
        )
        endpoint_rows.append(
            {
                "schema_id": arm.schema_id,
                "schema_family_id": arm.schema_family_id,
                "schema_seed": arm.schema_seed,
                "tier_index": tier_index,
                "action_cell_count": action_cell_count,
                "endpoint_pair_count": len(endpoint_pairs),
                "endpoint_coalescence_count": max(0, action_cell_count - len(endpoint_pairs)),
                "diagnostic_status": "ok",
            }
        )

    return SchemaTowerDiagnostics(
        tower_shape_rows=tuple(tower_shape_rows),
        tier_occupancy_rows=tuple(tier_occupancy_rows),
        tier_executability_rows=tuple(tier_executability_rows),
        endpoint_coalescence_rows=tuple(endpoint_rows),
        timing_rows=(
            {
                "schema_id": arm.schema_id,
                "schema_family_id": arm.schema_family_id,
                "schema_seed": arm.schema_seed,
                "timing_category": "compatibility_readout_probe",
                "duration_seconds": "not_measured",
                "diagnostic_status": "not_measured",
            },
        ),
    )


def _run_source_local_ratio_tower_diagnostics(*, arm: SchemaArm) -> SchemaTowerDiagnostics:
    numerator, denominator = _source_local_ratio_parts(arm)
    graph = _plate_support_graph_inputs()
    partition_tower = build_partition_tower_full(
        states=graph.core_states,
        edges=graph.edges,
        current_state=graph.current_base_state,
        schema=SourceLocalOutgoingRatioSchema(
            numerator=numerator,
            denominator=denominator,
            seed=arm.schema_seed,
        ),
    )
    current_positions = partition_tower.current_position_at_every_tier(
        graph.current_base_state
    )
    update_result = partition_tower.last_update_result
    scheduled_assignment_count = len(partition_tower.schema_assignment_store.scheduled_edge_ids())
    unscheduled_assignment_count = (
        0
        if update_result is None
        else max(0, update_result.diagnostics.discovered_edge_count - scheduled_assignment_count)
    )
    max_depth = len(partition_tower.state_layers)

    return _full_graph_tower_diagnostics(
        arm=arm,
        partition_tower=partition_tower,
        current_base_state=graph.current_base_state,
        current_positions=current_positions,
        max_depth=max_depth,
        scheduled_assignment_count=scheduled_assignment_count,
        unscheduled_assignment_count=unscheduled_assignment_count,
        depth_curve=(max_depth,),
        reset_event_count=0,
        timing_category="full_graph_source_local_ratio_probe",
    )


def _run_source_local_ratio_iterated_tower_diagnostics(
    *,
    arm: SchemaArm,
    config: SchemaSweepConfig,
) -> SchemaTowerDiagnostics:
    numerator, denominator = _source_local_ratio_parts(arm)
    max_iterations = (
        config.iterated_source_local_max_iterations
        if arm.max_iterations is None
        else arm.max_iterations
    )
    selector_rule_id = arm.selector_rule_id
    selection_mode = arm.selection_mode
    graph = _plate_support_graph_inputs()
    schema = IteratedSourceLocalOutgoingRatioSchema(
        numerator=numerator,
        denominator=denominator,
        seed=arm.schema_seed,
        selector_rule_id=selector_rule_id,
        max_iterations=max_iterations,
        selection_mode=selection_mode,
    )
    partition_tower = build_partition_tower_full(
        states=graph.core_states,
        edges=graph.edges,
        current_state=graph.current_base_state,
        schema=schema,
    )
    current_positions = partition_tower.current_position_at_every_tier(
        graph.current_base_state
    )
    update_result = partition_tower.last_update_result
    scheduled_assignment_count = len(partition_tower.schema_assignment_store.scheduled_edge_ids())
    unscheduled_assignment_count = (
        0
        if update_result is None
        else max(0, update_result.diagnostics.discovered_edge_count - scheduled_assignment_count)
    )
    max_depth = len(partition_tower.state_layers)
    base_diagnostics = _full_graph_tower_diagnostics(
        arm=arm,
        partition_tower=partition_tower,
        current_base_state=graph.current_base_state,
        current_positions=current_positions,
        max_depth=max_depth,
        scheduled_assignment_count=scheduled_assignment_count,
        unscheduled_assignment_count=unscheduled_assignment_count,
        depth_curve=(max_depth,),
        reset_event_count=0,
        timing_category="full_graph_source_local_ratio_iterated_probe",
    )
    iterated_plan_rows = tuple(
        {
            "schema_id": arm.schema_id,
            "schema_family_id": arm.schema_family_id,
            "schema_seed": arm.schema_seed,
            "selector_rule_id": selector_rule_id,
            "selection_mode": selection_mode,
            "ratio_numerator": numerator,
            "ratio_denominator": denominator,
            "max_iterations": max_iterations,
            **row,
        }
        for row in schema.plan_diagnostics()
    )
    stop_summary = schema.stop_summary()
    many_tier = _many_tier_candidate_signal_row(
        arm=arm,
        tower_rows=list(base_diagnostics.tower_shape_rows),
        executability_rows=list(base_diagnostics.tier_executability_rows),
        numerator=numerator,
        denominator=denominator,
        max_iterations=max_iterations,
        selector_rule_id=selector_rule_id,
        selection_mode=selection_mode,
        near_full_collapse_threshold=config.iterated_near_full_collapse_threshold,
        min_nontrivial_tiers=config.iterated_min_nontrivial_tiers,
    )
    stop_row = {
        "schema_id": arm.schema_id,
        "schema_family_id": arm.schema_family_id,
        "schema_seed": arm.schema_seed,
        "selector_rule_id": selector_rule_id,
        "selection_mode": selection_mode,
        "ratio_numerator": numerator,
        "ratio_denominator": denominator,
        "max_iterations": max_iterations,
        **stop_summary,
        "max_depth": max_depth,
        "nontrivial_tier_count": many_tier["nontrivial_tier_count"],
        "largest_cell_share_final": _largest_cell_share_final(
            list(base_diagnostics.tower_shape_rows)
        ),
        "near_full_collapse_threshold": config.iterated_near_full_collapse_threshold,
    }
    return SchemaTowerDiagnostics(
        tower_shape_rows=base_diagnostics.tower_shape_rows,
        tier_occupancy_rows=base_diagnostics.tier_occupancy_rows,
        tier_executability_rows=base_diagnostics.tier_executability_rows,
        endpoint_coalescence_rows=base_diagnostics.endpoint_coalescence_rows,
        timing_rows=base_diagnostics.timing_rows,
        iterated_plan_rows=iterated_plan_rows,
        iterated_schema_stop_rows=(stop_row,),
        many_tier_candidate_signal_rows=(many_tier,),
    )


def _plate_support_graph_inputs() -> PlateSupportGraphInputs:
    surface = import_plate_support_surface()
    to_core_state = surface.module.plate_support_state_to_core_state
    to_core_action = surface.module.action_index_to_primitive_action
    valid_states = tuple(surface.all_valid_states())
    core_states = tuple(to_core_state(state) for state in valid_states)
    core_by_state = dict(zip(valid_states, core_states, strict=True))
    edges: list[BaseEdge] = []
    for source_state in valid_states:
        source = core_by_state[source_state]
        for action_index in range(surface.ACTION_COUNT):
            transition = surface.primitive_transition(source_state, action_index)
            if not transition.valid_transition:
                continue
            edges.append(
                BaseEdge(
                    source=source,
                    action=to_core_action(action_index),
                    target=core_by_state[transition.next_state],
                    labels=("plate-support-transition",),
                )
            )
    return PlateSupportGraphInputs(
        surface=surface,
        core_states=core_states,
        edges=tuple(edges),
        current_base_state=core_by_state[surface.START_STATE],
    )


def _full_graph_tower_diagnostics(
    *,
    arm: SchemaArm,
    partition_tower: Any,
    current_base_state: Any,
    current_positions: tuple[Any, ...],
    max_depth: int,
    scheduled_assignment_count: int,
    unscheduled_assignment_count: int,
    depth_curve: tuple[int, ...],
    reset_event_count: int,
    timing_category: str,
) -> SchemaTowerDiagnostics:
    tower_shape_rows: list[dict[str, object]] = []
    tier_occupancy_rows: list[dict[str, object]] = []
    tier_executability_rows: list[dict[str, object]] = []
    endpoint_rows: list[dict[str, object]] = []
    for tier_index, state_layer in enumerate(partition_tower.state_layers):
        action_layer = partition_tower.action_layers[tier_index]
        state_member_counts = [
            len(members) for members in state_layer.members_by_cell_id.values()
        ]
        total_state_members = sum(state_member_counts)
        largest_share = (
            0.0 if total_state_members == 0 else max(state_member_counts) / total_state_members
        )
        singleton_share = (
            0.0
            if total_state_members == 0
            else sum(1 for count in state_member_counts if count == 1) / len(state_member_counts)
        )
        current_cell = current_positions[tier_index]
        outgoing = (
            ()
            if current_cell is None
            else partition_tower.outgoing_action_cells(tier_index, current_cell)
        )
        executable = (
            ()
            if current_cell is None
            else partition_tower.executable_action_cells(
                tier_index,
                current_cell,
                current_base_state,
            )
        )
        action_cell_count = len(action_layer.edge_ids_by_action_cell)
        endpoint_pairs = {
            (
                str(action_layer.source_cell_by_action_cell.get(action_cell)),
                str(action_layer.target_cell_by_action_cell.get(action_cell)),
            )
            for action_cell in action_layer.edge_ids_by_action_cell
        }
        tower_shape_rows.append(
            {
                "schema_id": arm.schema_id,
                "schema_family_id": arm.schema_family_id,
                "schema_seed": arm.schema_seed,
                "tier_index": tier_index,
                "max_depth": max_depth,
                "state_cell_count": len(state_layer.members_by_cell_id),
                "action_cell_count": action_cell_count,
                "largest_cell_share": largest_share,
                "singleton_cell_share": singleton_share,
                "scheduled_assignment_count": scheduled_assignment_count,
                "unscheduled_assignment_count": unscheduled_assignment_count,
                "depth_curve": json.dumps(depth_curve, separators=(",", ":")),
                "reset_event_count": reset_event_count,
                "diagnostic_status": "ok",
            }
        )
        tier_occupancy_rows.append(
            {
                "schema_id": arm.schema_id,
                "schema_family_id": arm.schema_family_id,
                "schema_seed": arm.schema_seed,
                "tier_index": tier_index,
                "current_state_cell": str(current_cell),
                "state_cell_count": len(state_layer.members_by_cell_id),
                "outgoing_action_cell_count": len(outgoing),
                "active_action_cell_count": len(executable),
                "diagnostic_status": "ok",
            }
        )
        tier_executability_rows.append(
            {
                "schema_id": arm.schema_id,
                "schema_family_id": arm.schema_family_id,
                "schema_seed": arm.schema_seed,
                "tier_index": tier_index,
                "tier_executable_from_current_state": partition_tower.tier_is_executable_from_state(
                    tier_index,
                    current_base_state,
                ),
                "lift_success_probe_count": len(executable),
                "lift_failure_probe_count": 0 if executable else 1,
                "active_action_cell_count": len(executable),
                "diagnostic_status": "ok",
            }
        )
        endpoint_rows.append(
            {
                "schema_id": arm.schema_id,
                "schema_family_id": arm.schema_family_id,
                "schema_seed": arm.schema_seed,
                "tier_index": tier_index,
                "action_cell_count": action_cell_count,
                "endpoint_pair_count": len(endpoint_pairs),
                "endpoint_coalescence_count": max(0, action_cell_count - len(endpoint_pairs)),
                "diagnostic_status": "ok",
            }
        )

    return SchemaTowerDiagnostics(
        tower_shape_rows=tuple(tower_shape_rows),
        tier_occupancy_rows=tuple(tier_occupancy_rows),
        tier_executability_rows=tuple(tier_executability_rows),
        endpoint_coalescence_rows=tuple(endpoint_rows),
        timing_rows=(
            {
                "schema_id": arm.schema_id,
                "schema_family_id": arm.schema_family_id,
                "schema_seed": arm.schema_seed,
                "timing_category": timing_category,
                "duration_seconds": "not_measured",
                "diagnostic_status": "not_measured",
            },
        ),
    )


def _many_tier_candidate_signal_row(
    *,
    arm: SchemaArm,
    tower_rows: list[dict[str, object]],
    executability_rows: list[dict[str, object]],
    numerator: int,
    denominator: int,
    max_iterations: int,
    selector_rule_id: str,
    selection_mode: str,
    near_full_collapse_threshold: float,
    min_nontrivial_tiers: int,
) -> dict[str, object]:
    nonbase_rows = [
        row for row in tower_rows if str(row.get("tier_index")) not in ("0", "not_applicable")
    ]
    nonbase_executability = [
        row
        for row in executability_rows
        if str(row.get("tier_index")) not in ("0", "not_applicable")
    ]
    nontrivial_rows = [
        row
        for row in nonbase_rows
        if int(row.get("state_cell_count", 0)) > 1
        and float(row.get("largest_cell_share", 1.0)) < near_full_collapse_threshold
    ]
    first_nonbase = nonbase_rows[0] if nonbase_rows else {}
    active_counts = [
        int(row.get("active_action_cell_count", 0)) for row in nonbase_executability
    ]
    has_empty_executable_tier = bool(active_counts) and min(active_counts) <= 0
    has_immediate_collapse = bool(first_nonbase) and (
        int(first_nonbase.get("state_cell_count", 0)) <= 1
        or float(first_nonbase.get("largest_cell_share", 1.0))
        >= near_full_collapse_threshold
    )
    max_depth = max((int(row.get("max_depth", 0)) for row in tower_rows), default=0)
    max_largest_cell_share = max(
        (float(row.get("largest_cell_share", 0.0)) for row in nonbase_rows),
        default=0.0,
    )
    min_nonbase_state_cell_count = min(
        (int(row.get("state_cell_count", 0)) for row in nonbase_rows),
        default=0,
    )
    max_nonbase_state_cell_count = max(
        (int(row.get("state_cell_count", 0)) for row in nonbase_rows),
        default=0,
    )
    min_nonbase_active_action_cell_count = min(active_counts, default=0)
    nontrivial_tier_count = len(nontrivial_rows)
    if max_depth < 4:
        candidate_signal = "shallow_iterated_tower"
        reason = "iterated schema did not reach required tower depth"
    elif nontrivial_tier_count < min_nontrivial_tiers:
        candidate_signal = "insufficient_nontrivial_tiers"
        reason = "iterated schema did not produce enough non-collapsed tiers"
    elif has_immediate_collapse:
        candidate_signal = "immediate_near_collapse"
        reason = "first nonbase tier is already near-collapsed"
    elif has_empty_executable_tier:
        candidate_signal = "nonexecutable_iterated_tier"
        reason = "at least one nonbase iterated tier has no executable actions"
    elif max_largest_cell_share >= near_full_collapse_threshold:
        candidate_signal = "late_near_collapse"
        reason = "a nonbase iterated tier exceeds the near-collapse threshold"
    else:
        candidate_signal = "many_tier_executable_candidate"
        reason = "iterated schema produced enough executable non-collapsed tiers"
    return {
        "schema_id": arm.schema_id,
        "schema_family_id": arm.schema_family_id,
        "schema_seed": arm.schema_seed,
        "selector_rule_id": selector_rule_id,
        "selection_mode": selection_mode,
        "ratio_numerator": numerator,
        "ratio_denominator": denominator,
        "max_iterations": max_iterations,
        "max_depth": max_depth,
        "nontrivial_tier_count": nontrivial_tier_count,
        "min_required_nontrivial_tiers": min_nontrivial_tiers,
        "has_immediate_collapse": has_immediate_collapse,
        "has_empty_executable_tier": has_empty_executable_tier,
        "max_largest_cell_share": max_largest_cell_share,
        "min_nonbase_state_cell_count": min_nonbase_state_cell_count,
        "max_nonbase_state_cell_count": max_nonbase_state_cell_count,
        "min_nonbase_active_action_cell_count": min_nonbase_active_action_cell_count,
        "candidate_signal": candidate_signal,
        "candidate_signal_reason": reason,
        "near_full_collapse_threshold": near_full_collapse_threshold,
        "diagnostic_status": "ok",
    }


def _largest_cell_share_final(tower_rows: list[dict[str, object]]) -> float:
    if not tower_rows:
        return 0.0
    final = max(tower_rows, key=lambda row: int(row.get("tier_index", 0)))
    return float(final.get("largest_cell_share", 0.0))


def _source_local_ratio_parts(arm: SchemaArm) -> tuple[int, int]:
    if arm.ratio_numerator is not None and arm.ratio_denominator is not None:
        return arm.ratio_numerator, arm.ratio_denominator
    numerator, denominator = arm.selection_rate.split("/", maxsplit=1)
    return int(numerator), int(denominator)


def _blocked_rows(
    *,
    arm: SchemaArm,
    construction: SchemaConstructionResult,
) -> dict[str, dict[str, object]]:
    base = {
        "schema_id": arm.schema_id,
        "schema_family_id": arm.schema_family_id,
        "schema_seed": arm.schema_seed,
        "tier_index": "not_applicable",
        "diagnostic_status": construction.construction_status,
    }
    return {
        "tower_shape": {
            **base,
            "max_depth": 0,
            "state_cell_count": 0,
            "action_cell_count": 0,
            "largest_cell_share": 0.0,
            "singleton_cell_share": 0.0,
            "scheduled_assignment_count": 0,
            "unscheduled_assignment_count": 0,
            "depth_curve": "[]",
            "reset_event_count": 0,
        },
        "tier_occupancy": {
            **base,
            "current_state_cell": "not_applicable",
            "state_cell_count": 0,
            "outgoing_action_cell_count": 0,
            "active_action_cell_count": 0,
        },
        "tier_executability": {
            **base,
            "tier_executable_from_current_state": False,
            "lift_success_probe_count": 0,
            "lift_failure_probe_count": 0,
            "active_action_cell_count": 0,
        },
        "endpoint_coalescence": {
            **base,
            "action_cell_count": 0,
            "endpoint_pair_count": 0,
            "endpoint_coalescence_count": 0,
        },
        "timing": {
            "schema_id": arm.schema_id,
            "schema_family_id": arm.schema_family_id,
            "schema_seed": arm.schema_seed,
            "timing_category": "schema_construction",
            "duration_seconds": "not_measured",
            "diagnostic_status": construction.construction_status,
        },
    }
