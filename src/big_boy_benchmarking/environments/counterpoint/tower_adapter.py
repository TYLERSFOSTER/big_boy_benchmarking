"""state_collapser tower adapter for counterpoint hidden graphs."""

from __future__ import annotations

import math
import random
from collections.abc import Hashable, Iterable
from dataclasses import dataclass, field
from typing import Any

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
from big_boy_benchmarking.environments.counterpoint.liftability import (
    STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID,
)
from big_boy_benchmarking.environments.counterpoint.masks import legal_action_mask
from big_boy_benchmarking.environments.counterpoint.schemas import (
    DEFAULT_NOISY_RATE_SELECTOR_RULE_ID,
    stable_noisy_rate_score,
    state_key,
)
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


def base_edge_to_counterpoint_edge_key(edge: BaseEdge) -> str:
    source = core_state_to_counterpoint_state(edge.source)
    action = primitive_action_to_counterpoint_action(edge.action)
    target = core_state_to_counterpoint_state(edge.target)
    return f"{state_key(source)}|action{action.deltas}|{state_key(target)}"


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


@dataclass(frozen=True, slots=True)
class CounterpointOutgoingFractionSchema:
    """Single-block source-local outgoing fraction schema for diagnostics."""

    numerator: int
    denominator: int
    schema_seed: int = 0

    def __post_init__(self) -> None:
        if self.denominator <= 0:
            raise ValueError("CounterpointOutgoingFractionSchema.denominator must be positive")
        if self.numerator < 1 or self.numerator > self.denominator:
            raise ValueError(
                "CounterpointOutgoingFractionSchema.numerator must be between 1 and denominator"
            )

    def assign_edge(
        self,
        edge_id: EdgeId,
        registry: BaseGraphRegistry,
    ) -> SchemaBlockId | None:
        source_id = registry.source_state_id(edge_id)
        outgoing = sorted(registry.outgoing_edge_ids(source_id), key=lambda item: item.value)
        shuffled = list(outgoing)
        random.Random(f"{self.schema_seed}:{source_id.value}").shuffle(shuffled)
        if not shuffled:
            return None
        quota = max(1, math.ceil(len(shuffled) * self.numerator / self.denominator))
        if edge_id in shuffled[:quota]:
            return self._block_id()
        return None

    def ordered_blocks(self) -> tuple[SchemaBlockId, ...]:
        return (self._block_id(),)

    def _block_id(self) -> SchemaBlockId:
        return SchemaBlockId(
            ("counterpoint_outgoing_fraction", self.numerator, self.denominator)
        )


@dataclass(frozen=True, slots=True)
class CounterpointNoisyRateSchema:
    """Single-block edge-global noisy-rate schema for diagnostics."""

    instance_id: str
    numerator: int
    denominator: int
    schema_seed: int = 0
    selector_rule_id: str = DEFAULT_NOISY_RATE_SELECTOR_RULE_ID

    def __post_init__(self) -> None:
        if self.denominator <= 0:
            raise ValueError("CounterpointNoisyRateSchema.denominator must be positive")
        if self.numerator < 1 or self.numerator > self.denominator:
            raise ValueError(
                "CounterpointNoisyRateSchema.numerator must be between 1 and denominator"
            )
        if not self.selector_rule_id:
            raise ValueError("CounterpointNoisyRateSchema.selector_rule_id must be nonempty")

    def assign_edge(
        self,
        edge_id: EdgeId,
        registry: BaseGraphRegistry,
    ) -> SchemaBlockId | None:
        edge = registry.edge_for_id(edge_id)
        score = stable_noisy_rate_score(
            selector_rule_id=self.selector_rule_id,
            instance_id=self.instance_id,
            schema_seed=self.schema_seed,
            canonical_edge_key=base_edge_to_counterpoint_edge_key(edge),
        )
        if score < self.numerator / self.denominator:
            return self._block_id()
        return None

    def ordered_blocks(self) -> tuple[SchemaBlockId, ...]:
        return (self._block_id(),)

    def _block_id(self) -> SchemaBlockId:
        return SchemaBlockId(
            (
                "counterpoint_noisy_rate",
                self.numerator,
                self.denominator,
                self.selector_rule_id,
            )
        )


@dataclass(slots=True)
class CounterpointIteratedNoisyRateSchema:
    """Repeated noisy-rate contraction schema for full multi-tier towers.

    Tier 1 uses the same base-edge noisy-rate selection as
    `CounterpointNoisyRateSchema`, so an iterated `1/18` run starts with the
    same `[108, 54]` first drop as the one-drop diagnostic. Later tiers resample
    representative quotient edges at the same rate and schedule one contraction
    block per successful iteration.
    """

    instance_id: str
    numerator: int
    denominator: int
    schema_seed: int = 0
    selector_rule_id: str = DEFAULT_NOISY_RATE_SELECTOR_RULE_ID
    max_iterations: int = 32
    _planned_edge_signature: tuple[int, ...] = field(
        default=(),
        init=False,
        repr=False,
        compare=False,
    )
    _assignment_by_edge_id: dict[EdgeId, SchemaBlockId | None] = field(
        default_factory=dict,
        init=False,
        repr=False,
        compare=False,
    )
    _ordered_blocks: tuple[SchemaBlockId, ...] = field(
        default=(),
        init=False,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        if self.denominator <= 0:
            raise ValueError(
                "CounterpointIteratedNoisyRateSchema.denominator must be positive"
            )
        if self.numerator < 1 or self.numerator > self.denominator:
            raise ValueError(
                "CounterpointIteratedNoisyRateSchema.numerator must be between "
                "1 and denominator"
            )
        if self.max_iterations <= 0:
            raise ValueError(
                "CounterpointIteratedNoisyRateSchema.max_iterations must be positive"
            )
        if not self.selector_rule_id:
            raise ValueError(
                "CounterpointIteratedNoisyRateSchema.selector_rule_id must be nonempty"
            )

    def assign_edge(
        self,
        edge_id: EdgeId,
        registry: BaseGraphRegistry,
    ) -> SchemaBlockId | None:
        self._ensure_plan(registry)
        return self._assignment_by_edge_id.get(edge_id)

    def ordered_blocks(self) -> tuple[SchemaBlockId, ...]:
        return self._ordered_blocks

    def _ensure_plan(self, registry: BaseGraphRegistry) -> None:
        edge_signature = tuple(edge_id.value for edge_id in registry.edge_ids)
        if edge_signature == self._planned_edge_signature:
            return
        assignment, ordered_blocks = _iterated_noisy_rate_plan(
            registry=registry,
            instance_id=self.instance_id,
            numerator=self.numerator,
            denominator=self.denominator,
            schema_seed=self.schema_seed,
            selector_rule_id=self.selector_rule_id,
            max_iterations=self.max_iterations,
        )
        self._planned_edge_signature = edge_signature
        self._assignment_by_edge_id = assignment
        self._ordered_blocks = ordered_blocks


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
    if schema_id.startswith(ids.OUTGOING_FRACTION_SWEEP_SCHEMA_ID):
        return CounterpointOutgoingFractionSchema(
            numerator=1,
            denominator=18,
            schema_seed=0 if schema_seed is None else schema_seed,
        )
    if schema_id.startswith(ids.NOISY_RATE_CONTRACTION_SCHEMA_ID):
        return CounterpointNoisyRateSchema(
            instance_id=ids.ENVIRONMENT_FAMILY_ID,
            numerator=1,
            denominator=36,
            schema_seed=0 if schema_seed is None else schema_seed,
        )
    if schema_id == ids.BAD_SCHEMA_ID:
        return DimensionwiseSchema(("counterpoint_transition",))
    raise ValueError(f"unsupported tower schema id: {schema_id}")


@dataclass(frozen=True)
class CounterpointTowerBuildResult:
    graph: ReachableGraph
    hidden_graph: CounterpointHiddenGraph
    tower: PartitionTower


def serialize_partition_invariant_issue(issue: object) -> dict[str, Any]:
    return {
        "tier": getattr(issue, "tier", None),
        "code": str(getattr(issue, "code", "")),
        "message": str(getattr(issue, "message", "")),
        "state_cell_id": _optional_repr(getattr(issue, "state_cell_id", None)),
        "action_collection_id": _optional_repr(
            getattr(issue, "action_collection_id", None)
        ),
        "action_cell_id": _optional_repr(getattr(issue, "action_cell_id", None)),
        "edge_id": _optional_repr(getattr(issue, "edge_id", None)),
    }


def serialize_partition_invariant_report(
    report: object,
    *,
    allow_dirty: bool = False,
) -> dict[str, Any]:
    issues = tuple(getattr(report, "issues", ()))
    return {
        "ok": bool(getattr(report, "ok", False)),
        "allow_dirty": allow_dirty,
        "issue_count": len(issues),
        "issues": [serialize_partition_invariant_issue(issue) for issue in issues],
    }


def collect_counterpoint_tower_invariant_report(
    build: CounterpointTowerBuildResult,
    *,
    allow_dirty: bool = False,
) -> dict[str, Any]:
    report = build.tower.invariant_report(allow_dirty=allow_dirty)
    return serialize_partition_invariant_report(report, allow_dirty=allow_dirty)


def assert_counterpoint_tower_consistent(
    build: CounterpointTowerBuildResult,
    *,
    allow_dirty: bool = False,
) -> None:
    build.tower.assert_consistent(allow_dirty=allow_dirty)


def counterpoint_tower_invariant_artifact_payload(
    build: CounterpointTowerBuildResult,
    *,
    allow_dirty: bool = False,
) -> dict[str, Any]:
    import state_collapser

    payload = collect_counterpoint_tower_invariant_report(
        build,
        allow_dirty=allow_dirty,
    )
    payload["state_collapser_version"] = str(getattr(state_collapser, "__version__", ""))
    payload["liftability_semantics_id"] = (
        STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID
    )
    return payload


def _optional_repr(value: object | None) -> str | None:
    if value is None:
        return None
    return repr(value)


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
    tower.assert_consistent()
    return CounterpointTowerBuildResult(graph=graph, hidden_graph=hidden_graph, tower=tower)


def build_counterpoint_fraction_partition_tower(
    spec: CounterpointInstanceSpec,
    *,
    numerator: int,
    denominator: int,
    schema_seed: int | None = None,
) -> CounterpointTowerBuildResult:
    graph = enumerate_reachable_graph(spec)
    hidden_graph = CounterpointHiddenGraph(spec)
    tower = PartitionTower(
        schema=CounterpointOutgoingFractionSchema(
            numerator=numerator,
            denominator=denominator,
            schema_seed=0 if schema_seed is None else schema_seed,
        ),
        reward_aggregator=RewardAggregator("mean"),
    )
    states = tuple(counterpoint_state_to_core_state(state) for state in graph.states)
    edges = tuple(graph_edge_to_base_edge(edge) for edge in graph.edges)
    current_state = (
        counterpoint_state_to_core_state(graph.start_states[0]) if graph.start_states else None
    )
    tower.initialize(initial_states=states, initial_edges=edges, current_state=current_state)
    tower.assert_consistent()
    return CounterpointTowerBuildResult(graph=graph, hidden_graph=hidden_graph, tower=tower)


def build_counterpoint_noisy_rate_partition_tower(
    spec: CounterpointInstanceSpec,
    *,
    numerator: int,
    denominator: int,
    schema_seed: int | None = None,
    selector_rule_id: str = DEFAULT_NOISY_RATE_SELECTOR_RULE_ID,
) -> CounterpointTowerBuildResult:
    graph = enumerate_reachable_graph(spec)
    hidden_graph = CounterpointHiddenGraph(spec)
    tower = PartitionTower(
        schema=CounterpointNoisyRateSchema(
            instance_id=graph.spec.environment_instance_id,
            numerator=numerator,
            denominator=denominator,
            schema_seed=0 if schema_seed is None else schema_seed,
            selector_rule_id=selector_rule_id,
        ),
        reward_aggregator=RewardAggregator("mean"),
    )
    states = tuple(counterpoint_state_to_core_state(state) for state in graph.states)
    edges = tuple(graph_edge_to_base_edge(edge) for edge in graph.edges)
    current_state = (
        counterpoint_state_to_core_state(graph.start_states[0]) if graph.start_states else None
    )
    tower.initialize(initial_states=states, initial_edges=edges, current_state=current_state)
    tower.assert_consistent()
    return CounterpointTowerBuildResult(graph=graph, hidden_graph=hidden_graph, tower=tower)


def build_counterpoint_iterated_noisy_rate_partition_tower(
    spec: CounterpointInstanceSpec,
    *,
    numerator: int,
    denominator: int,
    schema_seed: int | None = None,
    selector_rule_id: str = DEFAULT_NOISY_RATE_SELECTOR_RULE_ID,
    max_iterations: int = 32,
) -> CounterpointTowerBuildResult:
    graph = enumerate_reachable_graph(spec)
    hidden_graph = CounterpointHiddenGraph(spec)
    tower = PartitionTower(
        schema=CounterpointIteratedNoisyRateSchema(
            instance_id=graph.spec.environment_instance_id,
            numerator=numerator,
            denominator=denominator,
            schema_seed=0 if schema_seed is None else schema_seed,
            selector_rule_id=selector_rule_id,
            max_iterations=max_iterations,
        ),
        reward_aggregator=RewardAggregator("mean"),
    )
    states = tuple(counterpoint_state_to_core_state(state) for state in graph.states)
    edges = tuple(graph_edge_to_base_edge(edge) for edge in graph.edges)
    current_state = (
        counterpoint_state_to_core_state(graph.start_states[0]) if graph.start_states else None
    )
    tower.initialize(initial_states=states, initial_edges=edges, current_state=current_state)
    tower.assert_consistent()
    return CounterpointTowerBuildResult(graph=graph, hidden_graph=hidden_graph, tower=tower)


def assigned_counterpoint_edge_keys(tower: PartitionTower) -> frozenset[str]:
    """Return canonical edge keys that received a non-null schema assignment."""

    selected: set[str] = set()
    for edge_id, block_id in tower.schema_assignment_store.assignment_by_edge_id.items():
        if block_id is None:
            continue
        selected.add(base_edge_to_counterpoint_edge_key(tower.registry.edge_for_id(edge_id)))
    return frozenset(selected)


def _iterated_noisy_rate_plan(
    *,
    registry: BaseGraphRegistry,
    instance_id: str,
    numerator: int,
    denominator: int,
    schema_seed: int,
    selector_rule_id: str,
    max_iterations: int,
) -> tuple[dict[EdgeId, SchemaBlockId | None], tuple[SchemaBlockId, ...]]:
    edge_ids = tuple(sorted(registry.edge_ids, key=lambda item: item.value))
    state_ids = tuple(registry.state_ids)
    parent = {state_id: state_id for state_id in state_ids}
    assignment: dict[EdgeId, SchemaBlockId | None] = {edge_id: None for edge_id in edge_ids}
    ordered_blocks: list[SchemaBlockId] = []

    for iteration_index in range(max_iterations):
        if _component_count(parent) <= 1:
            break
        selected = _selected_iterated_noisy_rate_edges(
            registry=registry,
            edge_ids=edge_ids,
            parent=parent,
            instance_id=instance_id,
            numerator=numerator,
            denominator=denominator,
            schema_seed=schema_seed,
            selector_rule_id=selector_rule_id,
            iteration_index=iteration_index,
        )
        if not selected:
            break
        block_id = _iterated_noisy_rate_block_id(
            numerator=numerator,
            denominator=denominator,
            selector_rule_id=selector_rule_id,
            iteration_index=iteration_index,
        )
        changed = False
        for edge_id in selected:
            assignment[edge_id] = block_id
            changed = (
                _union(
                    parent,
                    registry.source_state_id(edge_id),
                    registry.target_state_id(edge_id),
                )
                or changed
            )
        if not changed:
            break
        ordered_blocks.append(block_id)
    return assignment, tuple(ordered_blocks)


def _selected_iterated_noisy_rate_edges(
    *,
    registry: BaseGraphRegistry,
    edge_ids: tuple[EdgeId, ...],
    parent: dict[object, object],
    instance_id: str,
    numerator: int,
    denominator: int,
    schema_seed: int,
    selector_rule_id: str,
    iteration_index: int,
) -> tuple[EdgeId, ...]:
    if iteration_index == 0:
        candidates = tuple(
            edge_id
            for edge_id in edge_ids
            if _find(parent, registry.source_state_id(edge_id))
            != _find(parent, registry.target_state_id(edge_id))
        )
    else:
        candidates = _quotient_representative_edges(
            registry=registry,
            edge_ids=edge_ids,
            parent=parent,
        )

    selected = []
    for edge_id in candidates:
        base_key = base_edge_to_counterpoint_edge_key(registry.edge_for_id(edge_id))
        score_key = (
            base_key
            if iteration_index == 0
            else f"iterated_tier={iteration_index}|{base_key}"
        )
        score = stable_noisy_rate_score(
            selector_rule_id=selector_rule_id,
            instance_id=instance_id,
            schema_seed=schema_seed,
            canonical_edge_key=score_key,
        )
        if score < numerator / denominator:
            selected.append(edge_id)
    return tuple(selected)


def _quotient_representative_edges(
    *,
    registry: BaseGraphRegistry,
    edge_ids: tuple[EdgeId, ...],
    parent: dict[object, object],
) -> tuple[EdgeId, ...]:
    representatives: dict[tuple[int, int], EdgeId] = {}
    representative_keys: dict[tuple[int, int], str] = {}
    for edge_id in edge_ids:
        source_root = _find(parent, registry.source_state_id(edge_id))
        target_root = _find(parent, registry.target_state_id(edge_id))
        if source_root == target_root:
            continue
        pair = tuple(sorted((source_root.value, target_root.value)))
        base_key = base_edge_to_counterpoint_edge_key(registry.edge_for_id(edge_id))
        current_key = representative_keys.get(pair)
        if current_key is None or base_key < current_key:
            representatives[pair] = edge_id
            representative_keys[pair] = base_key
    return tuple(
        representatives[pair]
        for pair in sorted(
            representatives,
            key=lambda item: representative_keys[item],
        )
    )


def _iterated_noisy_rate_block_id(
    *,
    numerator: int,
    denominator: int,
    selector_rule_id: str,
    iteration_index: int,
) -> SchemaBlockId:
    return SchemaBlockId(
        (
            "counterpoint_iterated_noisy_rate",
            numerator,
            denominator,
            selector_rule_id,
            iteration_index,
        )
    )


def _find(parent: dict[object, object], item: object) -> object:
    current = item
    while parent[current] != current:
        parent[current] = parent[parent[current]]
        current = parent[current]
    return current


def _union(parent: dict[object, object], left: object, right: object) -> bool:
    left_root = _find(parent, left)
    right_root = _find(parent, right)
    if left_root == right_root:
        return False
    if right_root.value < left_root.value:
        left_root, right_root = right_root, left_root
    parent[right_root] = left_root
    return True


def _component_count(parent: dict[object, object]) -> int:
    return len({_find(parent, item) for item in parent})
