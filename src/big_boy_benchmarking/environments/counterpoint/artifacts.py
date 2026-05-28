"""Environment-specific artifact builders for counterpoint benchmarks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.writers import append_jsonl, write_csv, write_json
from big_boy_benchmarking.environments.counterpoint.graph import (
    ReachableGraph,
    summarize_graph,
)
from big_boy_benchmarking.environments.counterpoint.instances import initial_states
from big_boy_benchmarking.environments.counterpoint.masks import (
    legal_action_mask,
    mask_density_diagnostics,
)
from big_boy_benchmarking.environments.counterpoint.path_volume import PathVolumeSummary
from big_boy_benchmarking.environments.counterpoint.rewards import reward_term_specs
from big_boy_benchmarking.environments.counterpoint.schemas import SchemaConstruction
from big_boy_benchmarking.environments.counterpoint.specs import CounterpointInstanceSpec


def environment_family_manifest(specs: tuple[CounterpointInstanceSpec, ...]) -> dict[str, Any]:
    family_id = specs[0].environment_family_id if specs else "counterpoint_symbolic_v001"
    return {
        "environment_family_id": family_id,
        "environment_instance_ids": [spec.environment_instance_id for spec in specs],
        "description": "Counterpoint-like finite hidden state/action graph family.",
    }


def environment_instance_manifest(spec: CounterpointInstanceSpec) -> dict[str, Any]:
    return {"manifest_type": "environment_instance", "spec": spec.to_dict()}


def legality_manifest(spec: CounterpointInstanceSpec) -> dict[str, Any]:
    return {
        "legality_contract_id": spec.legality_contract_id,
        "checks": [
            "pitch_band",
            "strict_voice_order",
            "adjacent_interval_class",
            "outer_interval_class",
            "root_interval_class",
            "forbidden_parallel_interval_class",
        ],
    }


def reward_bundle_manifest(spec: CounterpointInstanceSpec) -> dict[str, Any]:
    return {
        "reward_bundle_id": spec.reward_bundle_id,
        "terms": [term.to_dict() for term in reward_term_specs()],
    }


def edge_label_manifest(spec: CounterpointInstanceSpec) -> dict[str, Any]:
    return {
        "edge_label_contract_id": spec.edge_label_contract_id,
        "label_families": [
            "beat_phase",
            "per_voice_delta",
            "movement_class",
            "direction_pattern",
            "interval_classes",
            "root_interval_class",
            "span_bucket",
            "terminal_candidate",
        ],
    }


def initial_state_manifest(spec: CounterpointInstanceSpec) -> dict[str, Any]:
    return {
        "initial_state_policy_id": spec.initial_state_policy_id,
        "initial_states": [state.to_dict() for state in initial_states(spec)],
    }


def action_mask_manifest(spec: CounterpointInstanceSpec) -> dict[str, Any]:
    return {
        "action_mask_policy_id": spec.action_mask_policy_id,
        "raw_action_order": "lexicographic_delta_tuple",
        "uses_legality_contract_id": spec.legality_contract_id,
    }


def mask_density_rows(graph: ReachableGraph) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for state in graph.states:
        diagnostics = mask_density_diagnostics(legal_action_mask(graph.spec, state))
        rows.append({"state": state.to_dict(), **diagnostics.to_dict()})
    return rows


def graph_summary_artifact(graph: ReachableGraph) -> dict[str, Any]:
    return summarize_graph(graph).to_dict()


def path_volume_summary_artifact(summary: PathVolumeSummary) -> dict[str, Any]:
    return summary.to_dict()


def schema_manifest(schema: SchemaConstruction) -> dict[str, Any]:
    return schema.spec.to_dict()


def schema_diagnostics_rows(schema: SchemaConstruction) -> list[dict[str, Any]]:
    state_cell_count = len(set(schema.state_partition.values()))
    edge_cell_count = len(set(schema.edge_partition.values()))
    return [
        {
            "schema_id": schema.spec.schema_id,
            "diagnostic_name": "state_cell_count",
            "value": state_cell_count,
        },
        {
            "schema_id": schema.spec.schema_id,
            "diagnostic_name": "edge_cell_count",
            "value": edge_cell_count,
        },
    ]


def quotient_summary(schema: SchemaConstruction) -> dict[str, Any]:
    return {
        "schema_id": schema.spec.schema_id,
        "state_cell_count": len(set(schema.state_partition.values())),
        "edge_cell_count": len(set(schema.edge_partition.values())),
        "fine_state_count": len(schema.state_partition),
        "fine_edge_count": len(schema.edge_partition),
    }


def quotient_cell_rows(schema: SchemaConstruction) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fine_key, cell_id in sorted(schema.state_partition.items()):
        rows.append(
            {
                "schema_id": schema.spec.schema_id,
                "kind": "state",
                "fine_key": fine_key,
                "cell_id": cell_id,
            }
        )
    for fine_key, cell_id in sorted(schema.edge_partition.items()):
        rows.append(
            {
                "schema_id": schema.spec.schema_id,
                "kind": "edge",
                "fine_key": fine_key,
                "cell_id": cell_id,
            }
        )
    return rows


def address_trace_rows(schema: SchemaConstruction) -> list[dict[str, Any]]:
    return [
        {"schema_id": schema.spec.schema_id, "fine_edge_key": fine_key, "address": cell_id}
        for fine_key, cell_id in sorted(schema.edge_partition.items())
    ]


def write_environment_artifacts(
    root: Path | str,
    *,
    graph: ReachableGraph,
    path_summary: PathVolumeSummary,
) -> dict[str, str]:
    target = Path(root)
    write_json(
        target / "environment_instance_manifest.json",
        environment_instance_manifest(graph.spec),
        create_parents=True,
    )
    write_json(
        target / "legality_manifest.json",
        legality_manifest(graph.spec),
        create_parents=True,
    )
    write_json(
        target / "reward_bundle_manifest.json",
        reward_bundle_manifest(graph.spec),
        create_parents=True,
    )
    write_json(
        target / "edge_label_manifest.json",
        edge_label_manifest(graph.spec),
        create_parents=True,
    )
    write_json(
        target / "initial_state_manifest.json",
        initial_state_manifest(graph.spec),
        create_parents=True,
    )
    write_json(
        target / "action_mask_manifest.json",
        action_mask_manifest(graph.spec),
        create_parents=True,
    )
    write_json(target / "graph_summary.json", graph_summary_artifact(graph), create_parents=True)
    write_csv(
        target / "mask_density.csv",
        mask_density_rows(graph),
        [
            "state",
            "raw_action_count",
            "legal_action_count",
            "mask_density",
            "dead_end",
            "single_action",
        ],
        create_parents=True,
    )
    write_json(
        target / "path_volume_summary.json",
        path_volume_summary_artifact(path_summary),
        create_parents=True,
    )
    append_jsonl(target / "path_volume_samples.jsonl", path_summary.to_dict(), create_parents=True)
    return {path.name: str(path) for path in target.iterdir() if path.is_file()}


def write_schema_artifacts(root: Path | str, *, schema: SchemaConstruction) -> dict[str, str]:
    target = Path(root)
    write_json(target / "schema_manifest.json", schema_manifest(schema), create_parents=True)
    for row in schema_diagnostics_rows(schema):
        append_jsonl(target / "schema_diagnostics.jsonl", row, create_parents=True)
    write_json(target / "quotient_summary.json", quotient_summary(schema), create_parents=True)
    write_csv(
        target / "quotient_cells.csv",
        quotient_cell_rows(schema),
        ["schema_id", "kind", "fine_key", "cell_id"],
        create_parents=True,
    )
    for row in address_trace_rows(schema):
        append_jsonl(target / "address_traces.jsonl", row, create_parents=True)
    return {path.name: str(path) for path in target.iterdir() if path.is_file()}
