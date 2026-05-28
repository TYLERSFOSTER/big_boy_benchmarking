"""Path-volume diagnostics for counterpoint hidden graphs."""

from __future__ import annotations

import random
from dataclasses import asdict, dataclass
from typing import Any

from big_boy_benchmarking.environments.counterpoint.graph import (
    ReachableGraph,
    enumerate_reachable_graph,
)
from big_boy_benchmarking.environments.counterpoint.specs import CounterpointInstanceSpec


@dataclass(frozen=True)
class PathVolumeSummary:
    environment_instance_id: str
    length: int
    exact_or_sampled: str
    exactly_length_count: int | None
    up_to_length_count: int | None
    sample_count: int | None
    completed_sample_count: int | None
    diagnostic_sampling_seed: int | None
    policy_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def exact_path_volume(
    spec: CounterpointInstanceSpec,
    *,
    length: int,
    graph: ReachableGraph | None = None,
) -> PathVolumeSummary:
    if length < 0:
        raise ValueError("length must be nonnegative")
    active_graph = graph or enumerate_reachable_graph(spec)
    outgoing = active_graph.outgoing_edges()
    current = {state: 1 for state in active_graph.start_states}
    exactly = 1 if length == 0 else 0
    up_to = exactly
    for _step in range(1, length + 1):
        next_counts = {state: 0 for state in active_graph.states}
        for state, count in current.items():
            for edge in outgoing.get(state, ()):
                next_counts[edge.target] = next_counts.get(edge.target, 0) + count
        current = next_counts
        exactly = sum(current.values())
        up_to += exactly
    return PathVolumeSummary(
        environment_instance_id=spec.environment_instance_id,
        length=length,
        exact_or_sampled="exact",
        exactly_length_count=exactly,
        up_to_length_count=up_to,
        sample_count=None,
        completed_sample_count=None,
        diagnostic_sampling_seed=None,
    )


def sampled_path_volume(
    spec: CounterpointInstanceSpec,
    *,
    length: int,
    sample_count: int,
    diagnostic_sampling_seed: int,
    graph: ReachableGraph | None = None,
) -> PathVolumeSummary:
    if length < 0:
        raise ValueError("length must be nonnegative")
    if sample_count < 0:
        raise ValueError("sample_count must be nonnegative")
    rng = random.Random(diagnostic_sampling_seed)
    active_graph = graph or enumerate_reachable_graph(spec)
    outgoing = active_graph.outgoing_edges()
    completed = 0
    for _ in range(sample_count):
        if not active_graph.start_states:
            break
        state = rng.choice(active_graph.start_states)
        survived = True
        for _step in range(length):
            candidates = outgoing.get(state, ())
            if not candidates:
                survived = False
                break
            state = rng.choice(candidates).target
        if survived:
            completed += 1
    return PathVolumeSummary(
        environment_instance_id=spec.environment_instance_id,
        length=length,
        exact_or_sampled="sampled",
        exactly_length_count=None,
        up_to_length_count=None,
        sample_count=sample_count,
        completed_sample_count=completed,
        diagnostic_sampling_seed=diagnostic_sampling_seed,
    )


def random_legal_policy_path_volume(
    spec: CounterpointInstanceSpec,
    *,
    length: int,
    sample_count: int,
    diagnostic_sampling_seed: int,
    policy_id: str = "random_legal_policy_v001",
) -> PathVolumeSummary:
    summary = sampled_path_volume(
        spec,
        length=length,
        sample_count=sample_count,
        diagnostic_sampling_seed=diagnostic_sampling_seed,
    )
    return PathVolumeSummary(
        **{**summary.to_dict(), "policy_id": policy_id},
    )
