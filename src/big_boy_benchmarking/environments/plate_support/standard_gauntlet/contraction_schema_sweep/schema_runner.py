"""Tower probe execution for constructed PlateSupport schema sweep arms."""

from __future__ import annotations

import json
from dataclasses import dataclass

from state_collapser.examples.tower_depth_probe import continuous_probe
from state_collapser.examples.tower_depth_probe import (
    build_contraction_schema as build_probe_schema,
)

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
from big_boy_benchmarking.environments.plate_support.upstream import import_plate_support_surface


@dataclass(frozen=True)
class SchemaTowerDiagnostics:
    """Tower diagnostics for a constructed schema arm."""

    tower_shape_rows: tuple[dict[str, object], ...]
    tier_occupancy_rows: tuple[dict[str, object], ...]
    tier_executability_rows: tuple[dict[str, object], ...]
    endpoint_coalescence_rows: tuple[dict[str, object], ...]
    timing_rows: tuple[dict[str, object], ...]


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
