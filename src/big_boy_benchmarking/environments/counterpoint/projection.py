"""Projection diagnostics for counterpoint hidden graphs."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from typing import Any

from big_boy_benchmarking.environments.counterpoint.graph import GraphEdge, ReachableGraph
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState


def projected_state_key(state: CounterpointState, *, drop_voice_index: int) -> str:
    if drop_voice_index < 0 or drop_voice_index >= len(state.pitches):
        raise ValueError("drop_voice_index must address an existing voice")
    remaining = tuple(
        pitch for index, pitch in enumerate(state.pitches) if index != drop_voice_index
    )
    return f"drop{drop_voice_index}:beat{state.beat_index}:pitches{remaining}"


def all_drop_one_state_keys(state: CounterpointState) -> tuple[str, ...]:
    return tuple(
        projected_state_key(state, drop_voice_index=index) for index in range(len(state.pitches))
    )


def projected_transition_key(edge: GraphEdge, *, drop_voice_index: int) -> str:
    source = projected_state_key(edge.source, drop_voice_index=drop_voice_index)
    target = projected_state_key(edge.target, drop_voice_index=drop_voice_index)
    action = tuple(
        delta for index, delta in enumerate(edge.action.deltas) if index != drop_voice_index
    )
    return f"{source}|action{action}|{target}"


def all_drop_one_transition_keys(edge: GraphEdge) -> tuple[str, ...]:
    return tuple(
        projected_transition_key(edge, drop_voice_index=index)
        for index in range(len(edge.source.pitches))
    )


@dataclass(frozen=True)
class ProjectionDiagnostics:
    projection_convention: str
    projected_state_count: int
    projected_transition_count: int
    fine_states_per_projected_state: dict[str, int]
    fine_transitions_per_projected_transition: dict[str, int]
    projection_cell_size_distribution: dict[int, int]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def projection_diagnostics(graph: ReachableGraph) -> ProjectionDiagnostics:
    state_counter: Counter[str] = Counter()
    transition_counter: Counter[str] = Counter()
    for state in graph.states:
        state_counter.update(all_drop_one_state_keys(state))
    for edge in graph.edges:
        transition_counter.update(all_drop_one_transition_keys(edge))
    cell_distribution = Counter(state_counter.values())
    return ProjectionDiagnostics(
        projection_convention="all_drop_one_posthoc",
        projected_state_count=len(state_counter),
        projected_transition_count=len(transition_counter),
        fine_states_per_projected_state=dict(state_counter),
        fine_transitions_per_projected_transition=dict(transition_counter),
        projection_cell_size_distribution=dict(sorted(cell_distribution.items())),
    )
