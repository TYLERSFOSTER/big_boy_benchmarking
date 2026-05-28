"""Reachable hidden graph enumeration for counterpoint fixtures."""

from __future__ import annotations

from collections import deque
from dataclasses import asdict, dataclass
from typing import Any

from big_boy_benchmarking.environments.counterpoint.actions import CounterpointAction
from big_boy_benchmarking.environments.counterpoint.instances import initial_states
from big_boy_benchmarking.environments.counterpoint.masks import (
    legal_action_mask,
    mask_density_diagnostics,
)
from big_boy_benchmarking.environments.counterpoint.rewards import RewardResult
from big_boy_benchmarking.environments.counterpoint.specs import CounterpointInstanceSpec
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState
from big_boy_benchmarking.environments.counterpoint.transition import evaluate_transition


@dataclass(frozen=True)
class GraphEdge:
    source: CounterpointState
    action: CounterpointAction
    target: CounterpointState
    reward: RewardResult
    labels: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source.to_dict(),
            "action": self.action.to_dict(),
            "target": self.target.to_dict(),
            "reward": self.reward.to_dict(),
            "labels": self.labels,
        }


@dataclass(frozen=True)
class ReachableGraph:
    spec: CounterpointInstanceSpec
    start_states: tuple[CounterpointState, ...]
    states: tuple[CounterpointState, ...]
    edges: tuple[GraphEdge, ...]

    def outgoing_edges(self) -> dict[CounterpointState, tuple[GraphEdge, ...]]:
        grouped: dict[CounterpointState, list[GraphEdge]] = {state: [] for state in self.states}
        for edge in self.edges:
            grouped.setdefault(edge.source, []).append(edge)
        return {state: tuple(edges) for state, edges in grouped.items()}


@dataclass(frozen=True)
class GraphSummary:
    state_count: int
    edge_count: int
    reachable_start_count: int
    dead_end_count: int
    branch_factor_min: int
    branch_factor_mean: float
    branch_factor_max: int
    mask_density_min: float
    mask_density_mean: float
    mask_density_max: float
    horizon_steps: int
    legality_contract_id: str
    reward_bundle_id: str
    edge_label_contract_id: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def enumerate_reachable_graph(spec: CounterpointInstanceSpec) -> ReachableGraph:
    starts = initial_states(spec)
    discovered = set(starts)
    queue: deque[CounterpointState] = deque(starts)
    edges: list[GraphEdge] = []

    while queue:
        state = queue.popleft()
        for action in legal_action_mask(spec, state).legal_actions():
            transition = evaluate_transition(spec, state, action)
            if transition.reward is None:
                continue
            edge = GraphEdge(
                source=state,
                action=action,
                target=transition.next_state,
                reward=transition.reward,
                labels=transition.labels,
            )
            edges.append(edge)
            if transition.next_state not in discovered:
                discovered.add(transition.next_state)
                queue.append(transition.next_state)

    return ReachableGraph(
        spec=spec,
        start_states=starts,
        states=tuple(sorted(discovered, key=lambda item: (item.beat_index, item.pitches))),
        edges=tuple(edges),
    )


def summarize_graph(graph: ReachableGraph) -> GraphSummary:
    outgoing = graph.outgoing_edges()
    branch_factors = [len(outgoing.get(state, ())) for state in graph.states]
    densities = [
        mask_density_diagnostics(legal_action_mask(graph.spec, state)).mask_density
        for state in graph.states
    ]
    return GraphSummary(
        state_count=len(graph.states),
        edge_count=len(graph.edges),
        reachable_start_count=len(graph.start_states),
        dead_end_count=sum(1 for count in branch_factors if count == 0),
        branch_factor_min=min(branch_factors) if branch_factors else 0,
        branch_factor_mean=sum(branch_factors) / len(branch_factors) if branch_factors else 0.0,
        branch_factor_max=max(branch_factors) if branch_factors else 0,
        mask_density_min=min(densities) if densities else 0.0,
        mask_density_mean=sum(densities) / len(densities) if densities else 0.0,
        mask_density_max=max(densities) if densities else 0.0,
        horizon_steps=graph.spec.horizon_steps,
        legality_contract_id=graph.spec.legality_contract_id,
        reward_bundle_id=graph.spec.reward_bundle_id,
        edge_label_contract_id=graph.spec.edge_label_contract_id,
    )
