"""Contraction schema families for counterpoint hidden graphs."""

from __future__ import annotations

import hashlib
import math
import random
from collections import defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
from typing import Any

from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.graph import GraphEdge, ReachableGraph
from big_boy_benchmarking.environments.counterpoint.projection import (
    all_drop_one_state_keys,
    all_drop_one_transition_keys,
)
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState

DEFAULT_NOISY_RATE_SELECTOR_RULE_ID = "counterpoint_sha256_edge_threshold_v001"


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


@dataclass(frozen=True)
class SourceLocalFractionSelection:
    """Selected outgoing edges for one source under a fixed fraction arm."""

    source_key: str
    out_degree: int
    selected_edge_keys: tuple[str, ...]

    @property
    def selected_count(self) -> int:
        return len(self.selected_edge_keys)


@dataclass(frozen=True)
class NoisyRateEdgeSelection:
    """Selected outgoing edges for one source under an edge-global rate arm."""

    source_key: str
    out_degree: int
    selected_edge_keys: tuple[str, ...]

    @property
    def selected_count(self) -> int:
        return len(self.selected_edge_keys)


def noisy_rate_arm_id(numerator: int, denominator: int) -> str:
    _validate_rate(numerator=numerator, denominator=denominator)
    return f"p{numerator:03d}_over_{denominator:03d}"


def _validate_rate(*, numerator: int, denominator: int) -> None:
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    if numerator < 1 or numerator > denominator:
        raise ValueError("numerator must be between 1 and denominator")


def stable_noisy_rate_score(
    *,
    selector_rule_id: str,
    instance_id: str,
    schema_seed: int,
    canonical_edge_key: str,
) -> float:
    """Return a stable per-edge score in [0, 1)."""

    material = "\x1f".join(
        (selector_rule_id, instance_id, str(schema_seed), canonical_edge_key)
    )
    digest = hashlib.sha256(material.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") / 2**64


def noisy_rate_edge_selected(
    *,
    selector_rule_id: str,
    instance_id: str,
    schema_seed: int,
    canonical_edge_key: str,
    numerator: int,
    denominator: int,
) -> bool:
    _validate_rate(numerator=numerator, denominator=denominator)
    return stable_noisy_rate_score(
        selector_rule_id=selector_rule_id,
        instance_id=instance_id,
        schema_seed=schema_seed,
        canonical_edge_key=canonical_edge_key,
    ) < numerator / denominator


def noisy_rate_edge_selections(
    graph: ReachableGraph,
    *,
    numerator: int,
    denominator: int,
    schema_seed: int,
    selector_rule_id: str = DEFAULT_NOISY_RATE_SELECTOR_RULE_ID,
) -> tuple[NoisyRateEdgeSelection, ...]:
    """Select stable edge-global Bernoulli-threshold edges grouped by source."""

    _validate_rate(numerator=numerator, denominator=denominator)
    edges_by_source: dict[str, list[GraphEdge]] = defaultdict(list)
    for edge in graph.edges:
        edges_by_source[state_key(edge.source)].append(edge)

    selections: list[NoisyRateEdgeSelection] = []
    for source, source_edges in sorted(edges_by_source.items()):
        selected = tuple(
            edge_key(edge)
            for edge in sorted(source_edges, key=edge_key)
            if noisy_rate_edge_selected(
                selector_rule_id=selector_rule_id,
                instance_id=graph.spec.environment_instance_id,
                schema_seed=schema_seed,
                canonical_edge_key=edge_key(edge),
                numerator=numerator,
                denominator=denominator,
            )
        )
        selections.append(
            NoisyRateEdgeSelection(
                source_key=source,
                out_degree=len(source_edges),
                selected_edge_keys=selected,
            )
        )
    return tuple(selections)


def selected_noisy_rate_edge_keys(
    graph: ReachableGraph,
    *,
    numerator: int,
    denominator: int,
    schema_seed: int,
    selector_rule_id: str = DEFAULT_NOISY_RATE_SELECTOR_RULE_ID,
) -> frozenset[str]:
    selected: set[str] = set()
    for selection in noisy_rate_edge_selections(
        graph,
        numerator=numerator,
        denominator=denominator,
        schema_seed=schema_seed,
        selector_rule_id=selector_rule_id,
    ):
        selected.update(selection.selected_edge_keys)
    return frozenset(selected)


def noisy_rate_selection_report(
    graph: ReachableGraph,
    *,
    numerator: int,
    denominator: int,
    schema_seed: int,
    selector_rule_id: str = DEFAULT_NOISY_RATE_SELECTOR_RULE_ID,
) -> dict[str, object]:
    selections = noisy_rate_edge_selections(
        graph,
        numerator=numerator,
        denominator=denominator,
        schema_seed=schema_seed,
        selector_rule_id=selector_rule_id,
    )
    selected_counts = [selection.selected_count for selection in selections]
    selected_count = sum(selected_counts)
    requested_rate = numerator / denominator
    return {
        "instance_id": graph.spec.environment_instance_id,
        "arm_id": noisy_rate_arm_id(numerator, denominator),
        "numerator": numerator,
        "denominator": denominator,
        "requested_rate": requested_rate,
        "schema_seed": schema_seed,
        "selector_rule_id": selector_rule_id,
        "base_state_count": len(graph.states),
        "base_edge_count": len(graph.edges),
        "selected_edge_count": selected_count,
        "selected_edge_share": selected_count / max(1, len(graph.edges)),
        "expected_selected_edge_count": len(graph.edges) * requested_rate,
        "selected_edge_count_residual_from_expectation": selected_count
        - (len(graph.edges) * requested_rate),
        "source_count_with_outgoing_edges": len(selections),
        "source_count_with_selected_edges": sum(count > 0 for count in selected_counts),
        "zero_selected_source_count": sum(count == 0 for count in selected_counts),
    }


def noisy_rate_source_coverage_report(
    graph: ReachableGraph,
    *,
    numerator: int,
    denominator: int,
    schema_seed: int,
    selector_rule_id: str = DEFAULT_NOISY_RATE_SELECTOR_RULE_ID,
) -> dict[str, object]:
    selections = noisy_rate_edge_selections(
        graph,
        numerator=numerator,
        denominator=denominator,
        schema_seed=schema_seed,
        selector_rule_id=selector_rule_id,
    )
    selected_counts = [selection.selected_count for selection in selections]
    out_degrees = [selection.out_degree for selection in selections]
    selected_source_degrees = [
        selection.out_degree for selection in selections if selection.selected_count > 0
    ]
    source_count = len(selections)
    selected_sources = sum(count > 0 for count in selected_counts)
    requested_rate = numerator / denominator
    expected_zero_source_share = (
        sum((1 - requested_rate) ** degree for degree in out_degrees) / source_count
        if source_count
        else None
    )
    return {
        "source_count_with_outgoing_edges": source_count,
        "source_count_with_selected_edges": selected_sources,
        "zero_selected_source_count": source_count - selected_sources,
        "selected_source_share": selected_sources / source_count if source_count else None,
        "realized_zero_source_share": (source_count - selected_sources) / source_count
        if source_count
        else None,
        "min_selected_edges_per_source": min(selected_counts) if selected_counts else None,
        "mean_selected_edges_per_source": sum(selected_counts) / source_count
        if source_count
        else None,
        "max_selected_edges_per_source": max(selected_counts) if selected_counts else None,
        "selected_edge_count_histogram_by_source": dict(
            sorted(
                (str(count), selected_counts.count(count))
                for count in set(selected_counts)
            )
        ),
        "source_out_degree_histogram": dict(
            sorted((str(degree), out_degrees.count(degree)) for degree in set(out_degrees))
        ),
        "selected_source_out_degree_histogram": dict(
            sorted(
                (str(degree), selected_source_degrees.count(degree))
                for degree in set(selected_source_degrees)
            )
        ),
        "expected_zero_source_share": expected_zero_source_share,
    }


def noisy_rate_monotonicity_report(
    graph: ReachableGraph,
    *,
    rates: tuple[tuple[int, int], ...],
    schema_seed: int,
    selector_rule_id: str = DEFAULT_NOISY_RATE_SELECTOR_RULE_ID,
) -> tuple[dict[str, object], ...]:
    ordered_rates = tuple(
        sorted(rates, key=lambda item: Fraction(item[0], item[1]))
    )
    rows: list[dict[str, object]] = []
    previous_rate: tuple[int, int] | None = None
    previous_selected: frozenset[str] | None = None
    for numerator, denominator in ordered_rates:
        selected = selected_noisy_rate_edge_keys(
            graph,
            numerator=numerator,
            denominator=denominator,
            schema_seed=schema_seed,
            selector_rule_id=selector_rule_id,
        )
        if previous_selected is not None and previous_rate is not None:
            missing = tuple(sorted(previous_selected - selected))
            from_numerator, from_denominator = previous_rate
            rows.append(
                {
                    "instance_id": graph.spec.environment_instance_id,
                    "schema_seed": schema_seed,
                    "from_arm_id": noisy_rate_arm_id(from_numerator, from_denominator),
                    "to_arm_id": noisy_rate_arm_id(numerator, denominator),
                    "from_numerator": from_numerator,
                    "from_denominator": from_denominator,
                    "to_numerator": numerator,
                    "to_denominator": denominator,
                    "from_requested_rate": from_numerator / from_denominator,
                    "to_requested_rate": numerator / denominator,
                    "subset_pass": not missing,
                    "missing_nested_edge_count": len(missing),
                    "example_offending_edge_keys": ";".join(missing[:5]),
                    "selector_rule_id": selector_rule_id,
                }
            )
        previous_rate = (numerator, denominator)
        previous_selected = selected
    return tuple(rows)


def noisy_rate_selection_consistency_report(
    *,
    metadata_selected_edge_keys: frozenset[str],
    runtime_selected_edge_keys: frozenset[str],
) -> dict[str, object]:
    missing_from_runtime = tuple(
        sorted(metadata_selected_edge_keys - runtime_selected_edge_keys)
    )
    extra_in_runtime = tuple(
        sorted(runtime_selected_edge_keys - metadata_selected_edge_keys)
    )
    return {
        "metadata_selected_edge_count": len(metadata_selected_edge_keys),
        "runtime_selected_edge_count": len(runtime_selected_edge_keys),
        "selection_sets_equal": not missing_from_runtime and not extra_in_runtime,
        "missing_from_runtime_count": len(missing_from_runtime),
        "extra_in_runtime_count": len(extra_in_runtime),
        "missing_from_runtime_examples": ";".join(missing_from_runtime[:5]),
        "extra_in_runtime_examples": ";".join(extra_in_runtime[:5]),
    }


def source_local_fraction_quota(
    out_degree: int,
    *,
    numerator: int,
    denominator: int,
) -> int:
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    if numerator < 1 or numerator > denominator:
        raise ValueError("numerator must be between 1 and denominator")
    if out_degree <= 0:
        return 0
    return max(1, math.ceil(out_degree * numerator / denominator))


def source_local_fraction_selections(
    graph: ReachableGraph,
    *,
    numerator: int,
    denominator: int,
    schema_seed: int,
) -> tuple[SourceLocalFractionSelection, ...]:
    """Select a stable source-local outgoing-edge prefix for a fraction arm."""

    edges_by_source: dict[str, list[GraphEdge]] = defaultdict(list)
    for edge in graph.edges:
        edges_by_source[state_key(edge.source)].append(edge)

    selections: list[SourceLocalFractionSelection] = []
    for source, source_edges in sorted(edges_by_source.items()):
        shuffled = sorted(source_edges, key=edge_key)
        random.Random(f"{schema_seed}:{source}").shuffle(shuffled)
        quota = source_local_fraction_quota(
            len(shuffled),
            numerator=numerator,
            denominator=denominator,
        )
        selections.append(
            SourceLocalFractionSelection(
                source_key=source,
                out_degree=len(shuffled),
                selected_edge_keys=tuple(edge_key(edge) for edge in shuffled[:quota]),
            )
        )
    return tuple(selections)


def selected_fraction_edge_keys(
    graph: ReachableGraph,
    *,
    numerator: int,
    denominator: int,
    schema_seed: int,
) -> frozenset[str]:
    selected: set[str] = set()
    for selection in source_local_fraction_selections(
        graph,
        numerator=numerator,
        denominator=denominator,
        schema_seed=schema_seed,
    ):
        selected.update(selection.selected_edge_keys)
    return frozenset(selected)


def legacy_one_third_first_block_edge_keys(
    graph: ReachableGraph,
    *,
    schema_seed: int,
) -> frozenset[str]:
    """Return the old recursive one-third schema's first scheduled block."""

    schema = build_one_third_outgoing_schema(graph, schema_seed=schema_seed)
    return frozenset(
        key for key, block_id in schema.edge_partition.items() if block_id == "one_third_block_0"
    )


def fraction_selection_monotonicity_report(
    graph: ReachableGraph,
    *,
    numerators: tuple[int, ...],
    denominator: int,
    schema_seed: int,
) -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    previous_numerator: int | None = None
    previous_selected: frozenset[str] | None = None
    for numerator in numerators:
        selected = selected_fraction_edge_keys(
            graph,
            numerator=numerator,
            denominator=denominator,
            schema_seed=schema_seed,
        )
        if previous_selected is not None and previous_numerator is not None:
            missing = tuple(sorted(previous_selected - selected))
            rows.append(
                {
                    "from_numerator": previous_numerator,
                    "to_numerator": numerator,
                    "denominator": denominator,
                    "subset_pass": not missing,
                    "missing_nested_edge_count": len(missing),
                    "example_missing_nested_edges": ";".join(missing[:5]),
                }
            )
        previous_numerator = numerator
        previous_selected = selected
    return tuple(rows)


def legacy_one_third_equivalence_report(
    graph: ReachableGraph,
    *,
    numerator: int,
    denominator: int,
    schema_seed: int,
) -> dict[str, object]:
    fraction_edges = selected_fraction_edge_keys(
        graph,
        numerator=numerator,
        denominator=denominator,
        schema_seed=schema_seed,
    )
    legacy_edges = legacy_one_third_first_block_edge_keys(graph, schema_seed=schema_seed)
    missing_from_fraction = tuple(sorted(legacy_edges - fraction_edges))
    extra_in_fraction = tuple(sorted(fraction_edges - legacy_edges))
    return {
        "numerator": numerator,
        "denominator": denominator,
        "schema_seed": schema_seed,
        "equivalent": not missing_from_fraction and not extra_in_fraction,
        "fraction_edge_count": len(fraction_edges),
        "legacy_edge_count": len(legacy_edges),
        "missing_from_fraction_count": len(missing_from_fraction),
        "extra_in_fraction_count": len(extra_in_fraction),
        "missing_from_fraction_examples": ";".join(missing_from_fraction[:5]),
        "extra_in_fraction_examples": ";".join(extra_in_fraction[:5]),
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


def build_outgoing_fraction_schema(
    graph: ReachableGraph,
    *,
    schema_seed: int,
    numerator: int,
    denominator: int,
) -> SchemaConstruction:
    source_local_fraction_quota(1, numerator=numerator, denominator=denominator)
    schema_id = f"{ids.OUTGOING_FRACTION_SWEEP_SCHEMA_ID}_n{numerator:02d}_over_{denominator}"
    spec = _schema_spec(
        graph,
        schema_id=schema_id,
        schema_family_id=ids.OUTGOING_FRACTION_SWEEP_SCHEMA_FAMILY_ID,
        schema_seed=schema_seed,
        construction_method="seeded_source_local_outgoing_fraction_single_block_contraction",
        source_label_families=(),
        state_partition_description="identity state keys; runtime contraction is edge-driven",
        action_partition_description=(
            "seeded source-local single scheduled outgoing-edge fraction block"
        ),
        expected_compression_target=(
            f"one scheduled {numerator}/{denominator} contraction block plus base tier"
        ),
        leakage_risk_statement=(
            "Uses only stable source states and outgoing edge identities, not rewards, "
            "terminal outcomes, learned values, or future episode results."
        ),
        intended_role="contraction_fraction_sweep_diagnostic",
        online_eligible=True,
        diagnostic_only=False,
        expected_tower_depth=2,
    )
    selected = selected_fraction_edge_keys(
        graph,
        numerator=numerator,
        denominator=denominator,
        schema_seed=schema_seed,
    )
    scheduled_block = f"fraction_n{numerator:02d}_over_{denominator}_block_0"
    edge_partition = {
        edge_key(edge): scheduled_block
        if edge_key(edge) in selected
        else f"fraction_n{numerator:02d}_over_{denominator}_unscheduled"
        for edge in graph.edges
    }
    return SchemaConstruction(
        spec=spec,
        state_partition={state_key(state): state_key(state) for state in graph.states},
        edge_partition=edge_partition,
    )


def build_noisy_rate_contraction_schema(
    graph: ReachableGraph,
    *,
    schema_seed: int,
    numerator: int,
    denominator: int,
    selector_rule_id: str = DEFAULT_NOISY_RATE_SELECTOR_RULE_ID,
) -> SchemaConstruction:
    _validate_rate(numerator=numerator, denominator=denominator)
    arm_id = noisy_rate_arm_id(numerator, denominator)
    schema_id = f"{ids.NOISY_RATE_CONTRACTION_SCHEMA_ID}_{arm_id}"
    spec = _schema_spec(
        graph,
        schema_id=schema_id,
        schema_family_id=ids.NOISY_RATE_CONTRACTION_SCHEMA_FAMILY_ID,
        schema_seed=schema_seed,
        construction_method="seeded_edge_global_noisy_rate_single_block_contraction",
        source_label_families=(),
        state_partition_description="identity state keys; runtime contraction is edge-driven",
        action_partition_description=(
            "single scheduled edge block selected by coupled SHA-256 threshold scores"
        ),
        expected_compression_target=(
            f"one expected-rate {numerator}/{denominator} contraction block plus base tier"
        ),
        leakage_risk_statement=(
            "Uses only stable instance id, schema seed, selector rule id, and edge identities; "
            "it does not use rewards, terminal outcomes, learned values, or future episode results."
        ),
        intended_role="noisy_rate_contraction_diagnostic",
        online_eligible=True,
        diagnostic_only=False,
        expected_tower_depth=2,
    )
    selected = selected_noisy_rate_edge_keys(
        graph,
        numerator=numerator,
        denominator=denominator,
        schema_seed=schema_seed,
        selector_rule_id=selector_rule_id,
    )
    scheduled_block = f"noisy_rate_{arm_id}_block_0"
    return SchemaConstruction(
        spec=spec,
        state_partition={state_key(state): state_key(state) for state in graph.states},
        edge_partition={
            edge_key(edge): scheduled_block
            if edge_key(edge) in selected
            else f"noisy_rate_{arm_id}_unscheduled"
            for edge in graph.edges
        },
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
    if schema_id.startswith(ids.OUTGOING_FRACTION_SWEEP_SCHEMA_ID):
        return build_outgoing_fraction_schema(
            graph,
            schema_seed=0 if schema_seed is None else schema_seed,
            numerator=1,
            denominator=18,
        )
    if schema_id.startswith(ids.NOISY_RATE_CONTRACTION_SCHEMA_ID):
        return build_noisy_rate_contraction_schema(
            graph,
            schema_seed=0 if schema_seed is None else schema_seed,
            numerator=1,
            denominator=36,
        )
    raise ValueError(f"unsupported schema id: {schema_id}")
