"""state_collapser tower adapter for counterpoint hidden graphs."""

from __future__ import annotations

import math
import random
from collections.abc import Hashable, Iterable
from dataclasses import dataclass

from state_collapser.core.action import PrimitiveAction
from state_collapser.core.edges import BaseEdge
from state_collapser.core.state import State
from state_collapser.graph.hidden_graph import HiddenGraph
from state_collapser.tower.partition import PartitionTower, RewardAggregator
from state_collapser.tower.partition.base_registry import BaseGraphRegistry
from state_collapser.tower.partition.ids import EdgeId, SchemaBlockId
from state_collapser.tower.partition.schema import (
    ContractionSchema,
    DimensionwiseSchema,
    NoContractionSchema,
    SeededRandomRateSchema,
)

from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.actions import (
    CounterpointAction,
    enumerate_raw_actions,
)
from big_boy_benchmarking.environments.counterpoint.graph import (
    GraphEdge,
    ReachableGraph,
    enumerate_reachable_graph,
)
from big_boy_benchmarking.environments.counterpoint.masks import legal_action_mask
from big_boy_benchmarking.environments.counterpoint.specs import CounterpointInstanceSpec
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState
from big_boy_benchmarking.environments.counterpoint.transition import evaluate_transition


def counterpoint_state_to_core_state(state: CounterpointState) -> State:
    return State(
        payload=state,
        identity=("counterpoint_symbolic_v001_state", state.pitches, state.beat_index),
    )


def core_state_to_counterpoint_state(state: State) -> CounterpointState:
    if not isinstance(state.payload, CounterpointState):
        raise ValueError(f"unsupported state payload: {state.payload!r}")
    return state.payload


def counterpoint_action_to_primitive_action(action: CounterpointAction) -> PrimitiveAction:
    return PrimitiveAction(
        payload=action,
        identity=("counterpoint_symbolic_v001_action", action.deltas),
        labels=tuple(_action_labels(action)),
    )


def primitive_action_to_counterpoint_action(action: PrimitiveAction) -> CounterpointAction:
    if not isinstance(action.payload, CounterpointAction):
        raise ValueError(f"unsupported action payload: {action.payload!r}")
    return action.payload


def _action_labels(action: CounterpointAction) -> tuple[Hashable, ...]:
    return (
        "counterpoint_action",
        ("counterpoint_delta_tuple", action.deltas),
    )


def _edge_labels(edge: GraphEdge) -> tuple[Hashable, ...]:
    return (
        "counterpoint_transition",
        ("counterpoint_direction_pattern", edge.labels["global_motion_direction_pattern"]),
        ("counterpoint_movement_classes", edge.labels["per_voice_movement_class"]),
        ("counterpoint_outer_interval_after", edge.labels["outer_interval_class_after"]),
        ("counterpoint_span_bucket", edge.labels["max_span_bucket"]),
    )


def graph_edge_to_base_edge(edge: GraphEdge) -> BaseEdge:
    return BaseEdge(
        source=counterpoint_state_to_core_state(edge.source),
        action=counterpoint_action_to_primitive_action(edge.action),
        target=counterpoint_state_to_core_state(edge.target),
        labels=_edge_labels(edge),
    )


class CounterpointHiddenGraph(HiddenGraph):
    """HiddenGraph binding for the benchmark-owned counterpoint environment."""

    def __init__(self, spec: CounterpointInstanceSpec) -> None:
        self.spec = spec
        self._graph = enumerate_reachable_graph(spec)
        self._state_set = frozenset(self._graph.states)
        self._action_set = frozenset(enumerate_raw_actions(spec))

    def is_valid_state(self, state: State) -> bool:
        try:
            return core_state_to_counterpoint_state(state) in self._state_set
        except ValueError:
            return False

    def is_valid_action(self, action: PrimitiveAction) -> bool:
        try:
            return primitive_action_to_counterpoint_action(action) in self._action_set
        except ValueError:
            return False

    def apply_action(self, state: State, action: PrimitiveAction) -> State | None:
        try:
            source = core_state_to_counterpoint_state(state)
            counterpoint_action = primitive_action_to_counterpoint_action(action)
        except ValueError:
            return None
        transition = evaluate_transition(self.spec, source, counterpoint_action)
        if not transition.legality.is_legal:
            return None
        return counterpoint_state_to_core_state(transition.next_state)

    def is_valid_edge(self, edge: BaseEdge) -> bool:
        return self.apply_action(edge.source, edge.action) == edge.target

    def out_actions(self, state: State) -> Iterable[PrimitiveAction]:
        try:
            source = core_state_to_counterpoint_state(state)
        except ValueError:
            return ()
        return tuple(
            counterpoint_action_to_primitive_action(action)
            for action in legal_action_mask(self.spec, source).legal_actions()
        )

    def out_neighbors(self, state: State) -> Iterable[State]:
        return tuple(
            target
            for action in self.out_actions(state)
            if (target := self.apply_action(state, action)) is not None
        )

    def out_edges(self, state: State) -> Iterable[BaseEdge]:
        try:
            source = core_state_to_counterpoint_state(state)
        except ValueError:
            return ()
        edges = []
        for action in legal_action_mask(self.spec, source).legal_actions():
            transition = evaluate_transition(self.spec, source, action)
            if not transition.legality.is_legal or transition.reward is None:
                continue
            graph_edge = GraphEdge(
                source=source,
                action=action,
                target=transition.next_state,
                reward=transition.reward,
                labels=transition.labels,
            )
            edges.append(graph_edge_to_base_edge(graph_edge))
        return tuple(edges)


@dataclass(frozen=True, slots=True)
class CounterpointOutgoingThirdsSchema:
    """Source-local one-third contraction schema for counterpoint diagnostics."""

    schema_seed: int = 0
    block_count: int = 3

    def __post_init__(self) -> None:
        if self.block_count != 3:
            raise ValueError("CounterpointOutgoingThirdsSchema.block_count must be exactly 3")

    def assign_edge(
        self,
        edge_id: EdgeId,
        registry: BaseGraphRegistry,
    ) -> SchemaBlockId | None:
        source_id = registry.source_state_id(edge_id)
        outgoing = sorted(registry.outgoing_edge_ids(source_id), key=lambda item: item.value)
        shuffled = list(outgoing)
        random.Random(f"{self.schema_seed}:{source_id.value}").shuffle(shuffled)

        remaining = list(shuffled)
        for block_index in range(self.block_count):
            if not remaining:
                return None
            block_size = max(1, math.ceil(len(remaining) / 3))
            current_block = remaining[:block_size]
            if edge_id in current_block:
                return self._block_id(block_index)
            remaining = remaining[block_size:]
        return None

    def ordered_blocks(self) -> tuple[SchemaBlockId, ...]:
        return tuple(self._block_id(index) for index in range(self.block_count))

    @staticmethod
    def _block_id(block_index: int) -> SchemaBlockId:
        return SchemaBlockId(("counterpoint_one_third", block_index))


def contraction_schema_for_id(
    schema_id: str,
    *,
    schema_seed: int | None = None,
) -> ContractionSchema:
    if schema_id == ids.EMPTY_SCHEMA_ID:
        return NoContractionSchema()
    if schema_id == ids.STRUCTURED_MOTION_SCHEMA_ID:
        return DimensionwiseSchema(
            (
                "counterpoint_transition",
                ("counterpoint_span_bucket", "compact"),
                ("counterpoint_span_bucket", "medium"),
                ("counterpoint_span_bucket", "wide"),
            )
        )
    if schema_id.startswith(ids.RANDOM_BALANCED_SCHEMA_FAMILY_ID):
        return SeededRandomRateSchema(seed=0 if schema_seed is None else schema_seed, block_count=4)
    if schema_id.startswith(ids.RANDOM_UNBALANCED_SCHEMA_FAMILY_ID):
        return SeededRandomRateSchema(seed=0 if schema_seed is None else schema_seed, block_count=2)
    if schema_id == ids.ONE_THIRD_OUTGOING_SCHEMA_ID:
        return CounterpointOutgoingThirdsSchema(
            schema_seed=0 if schema_seed is None else schema_seed
        )
    if schema_id == ids.BAD_SCHEMA_ID:
        return DimensionwiseSchema(("counterpoint_transition",))
    raise ValueError(f"unsupported tower schema id: {schema_id}")


@dataclass(frozen=True)
class CounterpointTowerBuildResult:
    graph: ReachableGraph
    hidden_graph: CounterpointHiddenGraph
    tower: PartitionTower


def build_counterpoint_partition_tower(
    spec: CounterpointInstanceSpec,
    *,
    schema_id: str,
    schema_seed: int | None = None,
) -> CounterpointTowerBuildResult:
    graph = enumerate_reachable_graph(spec)
    hidden_graph = CounterpointHiddenGraph(spec)
    tower = PartitionTower(
        schema=contraction_schema_for_id(schema_id, schema_seed=schema_seed),
        reward_aggregator=RewardAggregator("mean"),
    )
    states = tuple(counterpoint_state_to_core_state(state) for state in graph.states)
    edges = tuple(graph_edge_to_base_edge(edge) for edge in graph.edges)
    current_state = (
        counterpoint_state_to_core_state(graph.start_states[0]) if graph.start_states else None
    )
    tower.initialize(initial_states=states, initial_edges=edges, current_state=current_state)
    return CounterpointTowerBuildResult(graph=graph, hidden_graph=hidden_graph, tower=tower)
