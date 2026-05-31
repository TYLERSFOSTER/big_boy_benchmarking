"""Contraction schema families for counterpoint hidden graphs."""

from __future__ import annotations

import math
import random
from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Any

from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.graph import GraphEdge, ReachableGraph
from big_boy_benchmarking.environments.counterpoint.projection import (
    all_drop_one_state_keys,
    all_drop_one_transition_keys,
)
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState


def state_key(state: CounterpointState) -> str:
    return f"beat{state.beat_index}:pitches{state.pitches}"


def edge_key(edge: GraphEdge) -> str:
    return f"{state_key(edge.source)}|action{edge.action.deltas}|{state_key(edge.target)}"


@dataclass(frozen=True)
class SchemaSpec:
    schema_id: str
    schema_family_id: str
    schema_version: str
    environment_family_id: str
    environment_instance_id: str
    schema_seed: int | None
    construction_method: str
    source_label_families: tuple[str, ...]
    state_partition_description: str
    action_partition_description: str
    expected_tower_depth: int
    expected_compression_target: str
    leakage_risk_statement: str
    intended_role: str
    online_eligible: bool
    diagnostic_only: bool

    def __post_init__(self) -> None:
        if not self.leakage_risk_statement:
            raise ValueError("leakage_risk_statement must be nonempty")
        if self.online_eligible and self.diagnostic_only:
            raise ValueError("online_eligible and diagnostic_only cannot both be true")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SchemaConstruction:
    spec: SchemaSpec
    state_partition: dict[str, str]
    edge_partition: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec": self.spec.to_dict(),
            "state_partition": self.state_partition,
            "edge_partition": self.edge_partition,
        }


def _schema_spec(
    graph: ReachableGraph,
    *,
    schema_id: str,
    schema_family_id: str,
    schema_seed: int | None,
    construction_method: str,
    source_label_families: tuple[str, ...],
    state_partition_description: str,
    action_partition_description: str,
    expected_compression_target: str,
    leakage_risk_statement: str,
    intended_role: str,
    online_eligible: bool,
    diagnostic_only: bool,
    expected_tower_depth: int = 1,
) -> SchemaSpec:
    return SchemaSpec(
        schema_id=schema_id,
        schema_family_id=schema_family_id,
        schema_version="v001",
        environment_family_id=graph.spec.environment_family_id,
        environment_instance_id=graph.spec.environment_instance_id,
        schema_seed=schema_seed,
        construction_method=construction_method,
        source_label_families=source_label_families,
        state_partition_description=state_partition_description,
        action_partition_description=action_partition_description,
        expected_tower_depth=expected_tower_depth,
        expected_compression_target=expected_compression_target,
        leakage_risk_statement=leakage_risk_statement,
        intended_role=intended_role,
        online_eligible=online_eligible,
        diagnostic_only=diagnostic_only,
    )


def build_empty_schema(graph: ReachableGraph) -> SchemaConstruction:
    spec = _schema_spec(
        graph,
        schema_id=ids.EMPTY_SCHEMA_ID,
        schema_family_id=ids.EMPTY_SCHEMA_ID,
        schema_seed=None,
        construction_method="identity_no_contraction",
        source_label_families=(),
        state_partition_description="one cell per fine state",
        action_partition_description="one cell per fine transition",
        expected_compression_target="none",
        leakage_risk_statement=(
            "No reward, terminal, learned value, or future outcome labels are used."
        ),
        intended_role="baseline_empty",
        online_eligible=True,
        diagnostic_only=False,
    )
    return SchemaConstruction(
        spec=spec,
        state_partition={state_key(state): state_key(state) for state in graph.states},
        edge_partition={edge_key(edge): edge_key(edge) for edge in graph.edges},
    )


def _balanced_partition(
    keys: list[str],
    *,
    cell_count: int,
    seed: int,
    prefix: str,
) -> dict[str, str]:
    shuffled = list(keys)
    random.Random(seed).shuffle(shuffled)
    return {
        key: f"{prefix}_{index % max(1, cell_count):03d}" for index, key in enumerate(shuffled)
    }


def build_random_balanced_schema(
    graph: ReachableGraph,
    *,
    schema_seed: int,
    target_cell_count: int = 4,
) -> SchemaConstruction:
    spec = _schema_spec(
        graph,
        schema_id=f"{ids.RANDOM_BALANCED_SCHEMA_FAMILY_ID}_seed{schema_seed}",
        schema_family_id=ids.RANDOM_BALANCED_SCHEMA_FAMILY_ID,
        schema_seed=schema_seed,
        construction_method="random_balanced_key_partition",
        source_label_families=(),
        state_partition_description="seeded balanced random partition of state keys",
        action_partition_description="seeded balanced random partition of edge keys",
        expected_compression_target=f"about {target_cell_count} cells",
        leakage_risk_statement="Uses only stable fine state/action keys, not rewards or outcomes.",
        intended_role="random_balanced_control",
        online_eligible=True,
        diagnostic_only=False,
    )
    return SchemaConstruction(
        spec=spec,
        state_partition=_balanced_partition(
            [state_key(state) for state in graph.states],
            cell_count=target_cell_count,
            seed=schema_seed,
            prefix="state_random_balanced",
        ),
        edge_partition=_balanced_partition(
            [edge_key(edge) for edge in graph.edges],
            cell_count=target_cell_count,
            seed=schema_seed + 1,
            prefix="edge_random_balanced",
        ),
    )


def build_random_unbalanced_schema(
    graph: ReachableGraph,
    *,
    schema_seed: int,
) -> SchemaConstruction:
    spec = _schema_spec(
        graph,
        schema_id=f"{ids.RANDOM_UNBALANCED_SCHEMA_FAMILY_ID}_seed{schema_seed}",
        schema_family_id=ids.RANDOM_UNBALANCED_SCHEMA_FAMILY_ID,
        schema_seed=schema_seed,
        construction_method="random_unbalanced_giant_cell_partition",
        source_label_families=(),
        state_partition_description="seeded random partition with intentional giant cells",
        action_partition_description="seeded random partition with intentional giant cells",
        expected_compression_target="pathological giant cell plus singletons",
        leakage_risk_statement=(
            "Uses only stable fine keys; pathology is structural, not reward-derived."
        ),
        intended_role="control_pathology",
        online_eligible=True,
        diagnostic_only=False,
    )

    def partition(keys: list[str], *, prefix: str, seed: int) -> dict[str, str]:
        shuffled = list(keys)
        random.Random(seed).shuffle(shuffled)
        giant_cutoff = max(1, int(len(shuffled) * 0.8))
        result: dict[str, str] = {}
        for index, key in enumerate(shuffled):
            result[key] = (
                f"{prefix}_giant" if index < giant_cutoff else f"{prefix}_singleton_{index}"
            )
        return result

    return SchemaConstruction(
        spec=spec,
        state_partition=partition(
            [state_key(state) for state in graph.states],
            prefix="state_random_unbalanced",
            seed=schema_seed,
        ),
        edge_partition=partition(
            [edge_key(edge) for edge in graph.edges],
            prefix="edge_random_unbalanced",
            seed=schema_seed + 1,
        ),
    )


def build_structured_motion_schema(graph: ReachableGraph) -> SchemaConstruction:
    source_labels = (
        "global_motion_direction_pattern",
        "per_voice_movement_class",
        "adjacent_interval_classes_after",
        "outer_interval_class_after",
        "beat_phase_after",
        "max_span_bucket",
    )
    spec = _schema_spec(
        graph,
        schema_id=ids.STRUCTURED_MOTION_SCHEMA_ID,
        schema_family_id=ids.STRUCTURED_MOTION_SCHEMA_ID,
        schema_seed=None,
        construction_method="versioned_edge_label_motion_partition",
        source_label_families=source_labels,
        state_partition_description="beat phase and compactness bucket",
        action_partition_description="motion and interval label tuple",
        expected_compression_target="semantic motion cells",
        leakage_risk_statement=(
            "Uses only v001 edge labels, not reward outcomes or future episode results."
        ),
        intended_role="structured_motion",
        online_eligible=True,
        diagnostic_only=False,
    )
    state_partition = {
        state_key(state): f"beat{state.beat_index}_span{state.pitches[-1] - state.pitches[0]}"
        for state in graph.states
    }
    edge_partition = {
        edge_key(edge): "|".join(str(edge.labels[label]) for label in source_labels)
        for edge in graph.edges
    }
    return SchemaConstruction(
        spec=spec,
        state_partition=state_partition,
        edge_partition=edge_partition,
    )


def build_projection_audit_schema(graph: ReachableGraph) -> SchemaConstruction:
    spec = _schema_spec(
        graph,
        schema_id=ids.PROJECTION_AUDIT_SCHEMA_ID,
        schema_family_id=ids.PROJECTION_AUDIT_SCHEMA_ID,
        schema_seed=None,
        construction_method="all_drop_one_posthoc_projection_diagnostic",
        source_label_families=("all_drop_one_projection",),
        state_partition_description="all drop-one projected state keys recorded posthoc",
        action_partition_description="all drop-one projected transition keys recorded posthoc",
        expected_compression_target="diagnostic only",
        leakage_risk_statement=(
            "Uses coordinate projection only; no reward or outcome labels are used."
        ),
        intended_role="projection_diagnostic",
        online_eligible=False,
        diagnostic_only=True,
    )
    return SchemaConstruction(
        spec=spec,
        state_partition={
            state_key(state): "|".join(all_drop_one_state_keys(state)) for state in graph.states
        },
        edge_partition={
            edge_key(edge): "|".join(all_drop_one_transition_keys(edge)) for edge in graph.edges
        },
    )


def build_bad_schema(graph: ReachableGraph) -> SchemaConstruction:
    spec = _schema_spec(
        graph,
        schema_id=ids.BAD_SCHEMA_ID,
        schema_family_id=ids.BAD_SCHEMA_ID,
        schema_seed=None,
        construction_method="giant_cell_pathology",
        source_label_families=(),
        state_partition_description="all states collapse into one bad cell",
        action_partition_description="all transitions collapse into one bad cell",
        expected_compression_target="pathological overcompression",
        leakage_risk_statement=(
            "Does not use reward values; declared pathology is excessive mixing."
        ),
        intended_role="bad_control",
        online_eligible=True,
        diagnostic_only=False,
    )
    return SchemaConstruction(
        spec=spec,
        state_partition={state_key(state): "bad_state_giant_cell" for state in graph.states},
        edge_partition={edge_key(edge): "bad_edge_giant_cell" for edge in graph.edges},
    )


def build_one_third_outgoing_schema(
    graph: ReachableGraph,
    *,
    schema_seed: int,
) -> SchemaConstruction:
    spec = _schema_spec(
        graph,
        schema_id=ids.ONE_THIRD_OUTGOING_SCHEMA_ID,
        schema_family_id=ids.ONE_THIRD_SCHEMA_FAMILY_ID,
        schema_seed=schema_seed,
        construction_method="seeded_source_local_outgoing_one_third_contraction",
        source_label_families=(),
        state_partition_description="identity state keys; runtime contraction is edge-driven",
        action_partition_description=(
            "seeded source-local recursive one-third partition of outgoing edge keys"
        ),
        expected_compression_target="three one-third contraction blocks plus base tier",
        leakage_risk_statement=(
            "Uses only stable source states and outgoing edge identities, not rewards, "
            "terminal outcomes, learned values, or future episode results."
        ),
        intended_role="one_third_tower_diagnostic",
        online_eligible=True,
        diagnostic_only=False,
        expected_tower_depth=4,
    )
    edges_by_source: dict[str, list[GraphEdge]] = defaultdict(list)
    for edge in graph.edges:
        edges_by_source[state_key(edge.source)].append(edge)

    edge_partition: dict[str, str] = {}
    for source, source_edges in sorted(edges_by_source.items()):
        shuffled = sorted(source_edges, key=edge_key)
        random.Random(f"{schema_seed}:{source}").shuffle(shuffled)
        remaining = list(shuffled)
        for block_index in range(3):
            if not remaining:
                break
            block_size = max(1, math.ceil(len(remaining) / 3))
            current_block = remaining[:block_size]
            for edge in current_block:
                edge_partition[edge_key(edge)] = f"one_third_block_{block_index}"
            remaining = remaining[block_size:]
        for edge in remaining:
            edge_partition[edge_key(edge)] = "one_third_unscheduled"

    return SchemaConstruction(
        spec=spec,
        state_partition={state_key(state): state_key(state) for state in graph.states},
        edge_partition=edge_partition,
    )


def build_schema_for_id(
    graph: ReachableGraph,
    *,
    schema_id: str,
    schema_seed: int | None = None,
) -> SchemaConstruction:
    if schema_id == ids.EMPTY_SCHEMA_ID:
        return build_empty_schema(graph)
    if schema_id == ids.STRUCTURED_MOTION_SCHEMA_ID:
        return build_structured_motion_schema(graph)
    if schema_id == ids.PROJECTION_AUDIT_SCHEMA_ID:
        return build_projection_audit_schema(graph)
    if schema_id == ids.BAD_SCHEMA_ID:
        return build_bad_schema(graph)
    if schema_id.startswith(ids.RANDOM_BALANCED_SCHEMA_FAMILY_ID):
        return build_random_balanced_schema(
            graph,
            schema_seed=0 if schema_seed is None else schema_seed,
        )
    if schema_id.startswith(ids.RANDOM_UNBALANCED_SCHEMA_FAMILY_ID):
        return build_random_unbalanced_schema(
            graph,
            schema_seed=0 if schema_seed is None else schema_seed,
        )
    if schema_id == ids.ONE_THIRD_OUTGOING_SCHEMA_ID:
        return build_one_third_outgoing_schema(
            graph,
            schema_seed=0 if schema_seed is None else schema_seed,
        )
    raise ValueError(f"unsupported schema id: {schema_id}")
