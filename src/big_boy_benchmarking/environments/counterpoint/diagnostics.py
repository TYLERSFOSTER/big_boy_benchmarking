"""Reward, lift, and address diagnostics for counterpoint schemas."""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from statistics import mean, pvariance
from typing import Any

from big_boy_benchmarking.environments.counterpoint.graph import ReachableGraph
from big_boy_benchmarking.environments.counterpoint.schemas import (
    SchemaConstruction,
    edge_key,
)


@dataclass(frozen=True)
class RewardFiberDiagnostic:
    schema_id: str
    cell_id: str
    fine_transition_count: int
    reward_mean: float
    reward_variance: float
    reward_min: float
    reward_max: float
    term_variance: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LiftFiberDiagnostic:
    cell_id: str
    fine_candidate_count: int
    entropy: float
    valid_lift_count: int
    failed_lift_count: int
    failed_lift_reason_counts: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AddressabilityDiagnostics:
    address_count: int
    address_frequency_distribution: dict[str, int]
    largest_cell_share: float
    singleton_cell_share: float
    effective_number_of_cells: float
    entropy: float
    path_coverage_by_address: dict[str, int] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def reward_fiber_diagnostics(
    graph: ReachableGraph,
    schema: SchemaConstruction,
) -> tuple[RewardFiberDiagnostic, ...]:
    grouped: dict[str, list[tuple[float, dict[str, float]]]] = defaultdict(list)
    for edge in graph.edges:
        cell = schema.edge_partition[edge_key(edge)]
        grouped[cell].append(
            (
                edge.reward.total_reward,
                {term.reward_term_id: term.weighted_value for term in edge.reward.terms},
            )
        )

    diagnostics: list[RewardFiberDiagnostic] = []
    for cell_id in sorted(grouped):
        rewards = [item[0] for item in grouped[cell_id]]
        term_values: dict[str, list[float]] = defaultdict(list)
        for _reward, terms in grouped[cell_id]:
            for term_id, value in terms.items():
                term_values[term_id].append(value)
        diagnostics.append(
            RewardFiberDiagnostic(
                schema_id=schema.spec.schema_id,
                cell_id=cell_id,
                fine_transition_count=len(rewards),
                reward_mean=mean(rewards) if rewards else 0.0,
                reward_variance=pvariance(rewards) if len(rewards) > 1 else 0.0,
                reward_min=min(rewards) if rewards else 0.0,
                reward_max=max(rewards) if rewards else 0.0,
                term_variance={
                    term_id: pvariance(values) if len(values) > 1 else 0.0
                    for term_id, values in sorted(term_values.items())
                },
            )
        )
    return tuple(diagnostics)


def lift_fiber_diagnostics(schema: SchemaConstruction) -> tuple[LiftFiberDiagnostic, ...]:
    counts = Counter(schema.edge_partition.values())
    return tuple(
        LiftFiberDiagnostic(
            cell_id=cell_id,
            fine_candidate_count=count,
            entropy=math.log2(count) if count > 0 else 0.0,
            valid_lift_count=count,
            failed_lift_count=0,
            failed_lift_reason_counts={},
        )
        for cell_id, count in sorted(counts.items())
    )


def balanced_addressability_diagnostics(
    schema: SchemaConstruction,
    *,
    path_addresses: tuple[str, ...] | None = None,
) -> AddressabilityDiagnostics:
    counts = Counter(schema.edge_partition.values())
    total = sum(counts.values())
    probabilities = [count / total for count in counts.values()] if total else []
    entropy = -sum(probability * math.log2(probability) for probability in probabilities)
    effective = (
        1 / sum(probability * probability for probability in probabilities) if total else 0.0
    )
    path_coverage = Counter(path_addresses) if path_addresses is not None else None
    return AddressabilityDiagnostics(
        address_count=len(counts),
        address_frequency_distribution=dict(sorted(counts.items())),
        largest_cell_share=max(probabilities) if probabilities else 0.0,
        singleton_cell_share=(
            sum(1 for count in counts.values() if count == 1) / len(counts) if counts else 0.0
        ),
        effective_number_of_cells=effective,
        entropy=entropy,
        path_coverage_by_address=dict(sorted(path_coverage.items())) if path_coverage else None,
    )
