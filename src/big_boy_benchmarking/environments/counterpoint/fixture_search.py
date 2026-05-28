"""Deterministic fixture search for first counterpoint benchmark instances."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from big_boy_benchmarking.environments.counterpoint.graph import (
    enumerate_reachable_graph,
    summarize_graph,
)
from big_boy_benchmarking.environments.counterpoint.path_volume import exact_path_volume
from big_boy_benchmarking.environments.counterpoint.specs import CounterpointInstanceSpec


@dataclass(frozen=True)
class FixtureSearchResult:
    environment_instance_id: str
    state_count: int
    edge_count: int
    branch_factor_min: int
    branch_factor_mean: float
    branch_factor_max: int
    dead_end_count: int
    exact_path_volume_feasible: bool
    exact_horizon_path_count: int
    selected: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_fixture_candidate(spec: CounterpointInstanceSpec) -> FixtureSearchResult:
    graph = enumerate_reachable_graph(spec)
    summary = summarize_graph(graph)
    path_summary = exact_path_volume(spec, length=spec.horizon_steps, graph=graph)
    exact_count = path_summary.exactly_length_count or 0
    return FixtureSearchResult(
        environment_instance_id=spec.environment_instance_id,
        state_count=summary.state_count,
        edge_count=summary.edge_count,
        branch_factor_min=summary.branch_factor_min,
        branch_factor_mean=summary.branch_factor_mean,
        branch_factor_max=summary.branch_factor_max,
        dead_end_count=summary.dead_end_count,
        exact_path_volume_feasible=summary.state_count <= 5_000 and summary.edge_count <= 100_000,
        exact_horizon_path_count=exact_count,
    )


def search_fixture_candidates(
    candidates: tuple[CounterpointInstanceSpec, ...],
) -> tuple[FixtureSearchResult, ...]:
    results = [evaluate_fixture_candidate(spec) for spec in candidates]
    selected_index = next(
        (
            index
            for index, result in enumerate(results)
            if result.exact_path_volume_feasible
            and result.state_count > 0
            and result.edge_count > 0
            and result.dead_end_count < result.state_count
        ),
        None,
    )
    return tuple(
        FixtureSearchResult(**{**result.to_dict(), "selected": index == selected_index})
        for index, result in enumerate(results)
    )
