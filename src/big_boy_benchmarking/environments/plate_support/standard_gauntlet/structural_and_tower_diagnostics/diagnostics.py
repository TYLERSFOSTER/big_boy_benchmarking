"""Stage 1 diagnostic row construction."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from big_boy_benchmarking.environments.plate_support.actions import action_table_rows
from big_boy_benchmarking.environments.plate_support.diagnostics import (
    collect_plate_support_structural_diagnostics,
)
from big_boy_benchmarking.environments.plate_support.ids import (
    DEFAULT_SCHEMA_ID,
    NO_CONTRACTION_SCHEMA_ID,
    UPSTREAM_MODULE,
    UPSTREAM_SMOKE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    LINEARIZATION_MODE_ID,
    STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
    SUITE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.config import (
    StructuralDiagnosticsConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.readiness_source import (
    ReadinessSource,
)
from big_boy_benchmarking.environments.plate_support.tower_probe import (
    run_plate_support_tower_probe,
)
from big_boy_benchmarking.environments.plate_support.upstream import import_plate_support_surface


def collect_stage1_diagnostics(
    *,
    config: StructuralDiagnosticsConfig,
    readiness: ReadinessSource,
    dependency_state: dict[str, object],
) -> dict[str, object]:
    """Collect all Stage 1 machine rows from computed PlateSupport evidence."""

    surface = import_plate_support_surface()
    tower_probe_records = run_plate_support_tower_probe(
        steps=config.tower_probe_steps,
        seed=config.random_policy_seed,
        sample_size=config.tower_probe_sample_size,
    )
    diagnostics = collect_plate_support_structural_diagnostics(
        surface=surface,
        random_policy_episodes=config.random_policy_episode_count,
        random_policy_seed=config.random_policy_seed,
        tower_probe_records=tower_probe_records,
    )
    graph = diagnostics.graph.graph_summary
    shortest_rows = [record.to_dict() for record in diagnostics.graph.shortest_path_records]
    reward_sequence = [
        float(row["reward"]) for row in shortest_rows if row.get("reward") is not None
    ]
    action_labels = [
        str(row["action_label"])
        for row in shortest_rows
        if str(row.get("action_label", "")) != "terminal"
    ]
    tower_rows = [
        {
            **record.to_dict(),
            "claim_boundary": "tower shape diagnostic only; not tower benefit evidence",
        }
        for record in diagnostics.tower_probe_records
    ]
    random_policy = {
        **diagnostics.random_policy_recon.to_dict(),
        "claim_boundary": (
            "structural difficulty reconnaissance only; not an official learning baseline"
        ),
    }

    return {
        "identity_summary": [
            {
                "suite_id": SUITE_ID,
                "stage_id": STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
                "run_label": config.run_label,
                "environment_family_id": ENVIRONMENT_FAMILY_ID,
                "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
                "upstream_smoke_id": UPSTREAM_SMOKE_ID,
                "upstream_module": UPSTREAM_MODULE,
                "linearization_mode_id": LINEARIZATION_MODE_ID,
                "readiness_source": str(readiness.path),
                "readiness_artifact_root": str(readiness.source_artifact_root),
                "environment_doc": str(readiness.environment_doc),
                "artifact_root": str(Path(config.artifact_root).resolve()),
                "state_collapser_dependency_status": str(
                    dependency_state.get("inspection_status", "unknown")
                ),
            }
        ],
        "state_space_summary": [
            {
                "candidate_state_count": graph["candidate_state_count"],
                "valid_state_count": graph["valid_state_count"],
                "reachable_state_count": graph["reachable_state_count"],
                "reachable_from_start": graph["reachable_from_start"],
                "start_state_id": graph["start_state_id"],
                "goal_state_id": graph["goal_state_id"],
                "start_valid": graph["start_valid"],
                "goal_valid": graph["goal_valid"],
            }
        ],
        "action_table": action_table_rows(),
        "transition_summary": [
            record.to_dict() for record in diagnostics.graph.transition_records
        ],
        "shortest_path_summary": [
            {
                "shortest_path_length": graph["shortest_path_length"],
                "goal_one_step_from_start": graph["goal_one_step_from_start"],
                "action_labels": "|".join(action_labels),
                "reward_sequence": "|".join(str(reward) for reward in reward_sequence),
                "total_shortest_path_reward": sum(reward_sequence),
                "terminal_state_id": graph["goal_state_id"],
                "claim_boundary": "shortest path task anchor only",
            }
        ],
        "validity_predicate_summary": diagnostics.validity_predicate_summary,
        "geometry_summary": _geometry_rows(diagnostics),
        "random_policy_recon_summary": [random_policy],
        "tower_shape_summary": tower_rows,
        "training_surface_availability": [
            {
                "surface_name": name,
                "available": available,
                "required_for_later_stages": True,
            }
            for name, available in sorted(diagnostics.training_surface_availability.items())
        ],
        "graph_summary": graph,
        "distribution_rows": {
            "outgoing_action_count_summary": diagnostics.graph.outgoing_action_count_summary,
            "invalid_action_summary": diagnostics.graph.invalid_action_summary,
            "self_transition_summary": diagnostics.graph.self_transition_summary,
        },
        "downstream_readiness_summary": [
            _downstream_readiness_row(
                graph=graph,
                tower_rows=tower_rows,
                training_surface_availability=diagnostics.training_surface_availability,
            )
        ],
    }


def _geometry_rows(diagnostics: Any) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in diagnostics.support_pattern_summary:
        rows.append(
            {
                "geometry_domain": "support_pattern",
                "label": row["support_pattern"],
                "valid_state_count": row["valid_state_count"],
                "share": row["share"],
            }
        )
    for row in diagnostics.reachability_pattern_summary:
        rows.append(
            {
                "geometry_domain": "reachability_pattern",
                "label": row["reachability_pattern"],
                "valid_state_count": row["valid_state_count"],
                "share": row["share"],
            }
        )
    for row in diagnostics.orientation_summary:
        rows.append(
            {
                "geometry_domain": "orientation",
                "label": row["theta_idx"],
                "valid_state_count": row["valid_state_count"],
                "share": row["share"],
            }
        )
    for row in diagnostics.position_summary:
        rows.append(
            {
                "geometry_domain": "position",
                "label": f"{row['x_idx']},{row['y_idx']}",
                "valid_state_count": row["valid_state_count"],
                "share": row["share"],
            }
        )
    return rows


def _downstream_readiness_row(
    *,
    graph: dict[str, object],
    tower_rows: list[dict[str, object]],
    training_surface_availability: dict[str, bool],
) -> dict[str, object]:
    default_depth = _tower_depth(tower_rows, DEFAULT_SCHEMA_ID)
    flat_depth = _tower_depth(tower_rows, NO_CONTRACTION_SCHEMA_ID)
    training_available = all(bool(value) for value in training_surface_availability.values())
    ready_for_schema_sweep = (
        bool(graph["reachable_from_start"])
        and bool(graph["start_valid"])
        and bool(graph["goal_valid"])
        and graph["shortest_path_length"] is not None
        and int(graph["shortest_path_length"]) > 1
        and default_depth is not None
        and flat_depth is not None
        and training_available
    )
    blocking_reason = "" if ready_for_schema_sweep else "stage1_pass_criteria_not_met"
    return {
        "suite_id": SUITE_ID,
        "stage_id": STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "ready_for_schema_sweep": ready_for_schema_sweep,
        "ready_for_candidate_discovery": False,
        "ready_for_training_health": False,
        "ready_for_threshold_calibration": False,
        "ready_for_paired_comparison": False,
        "blocking_reason": blocking_reason,
        "candidate_state_count": graph["candidate_state_count"],
        "valid_state_count": graph["valid_state_count"],
        "reachable_state_count": graph["reachable_state_count"],
        "valid_nonself_edge_count": graph["valid_nonself_edge_count"],
        "invalid_move_count": graph["invalid_move_count"],
        "valid_self_transition_count": graph["valid_self_transition_count"],
        "shortest_path_length": graph["shortest_path_length"],
        "default_schema_max_depth": default_depth,
        "flat_schema_max_depth": flat_depth,
        "training_surfaces_available": training_available,
        "claim_boundary": "Stage 1 diagnostic readiness only; no learning claim",
    }


def _tower_depth(rows: list[dict[str, object]], schema_id: str) -> int | None:
    for row in rows:
        if row["schema_id"] == schema_id:
            return int(row["max_depth"])
    return None
