"""Scoped `state_collapser` adapter for Warehouse Gridlock generated surfaces."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from state_collapser.core.action import PrimitiveAction
from state_collapser.core.edges import BaseEdge
from state_collapser.core.state import State
from state_collapser.graph.hidden_graph import HiddenGraph

from big_boy_benchmarking.environments.warehouse_gridlock.actions import (
    WarehouseGridlockAction,
)
from big_boy_benchmarking.environments.warehouse_gridlock.state import (
    WarehouseGridlockState,
)


def warehouse_state_to_core_state(state: WarehouseGridlockState) -> State:
    return State(
        payload=state,
        identity=("warehouse_gridlock_001_state", state.stable_id),
    )


def core_state_to_warehouse_state(state: State) -> WarehouseGridlockState:
    if not isinstance(state.payload, WarehouseGridlockState):
        raise ValueError(f"unsupported Warehouse state payload: {state.payload!r}")
    return state.payload


def warehouse_action_to_primitive_action(action: WarehouseGridlockAction) -> PrimitiveAction:
    return PrimitiveAction(
        payload=action,
        identity=("warehouse_gridlock_001_generated_action", action.stable_id),
        labels=(
            "warehouse_gridlock_action",
            ("generated_candidate_surface", True),
        ),
    )


def primitive_action_to_warehouse_action(action: PrimitiveAction) -> WarehouseGridlockAction:
    if not isinstance(action.payload, WarehouseGridlockAction):
        raise ValueError(f"unsupported Warehouse action payload: {action.payload!r}")
    return action.payload


@dataclass(frozen=True)
class WarehouseGeneratedEdge:
    source: WarehouseGridlockState
    action: WarehouseGridlockAction
    target: WarehouseGridlockState
    reward: float
    labels: tuple[object, ...]

    @property
    def stable_id(self) -> str:
        return f"{self.source.stable_id}|{self.action.stable_id}|{self.target.stable_id}"


def warehouse_edge_to_base_edge(edge: WarehouseGeneratedEdge) -> BaseEdge:
    return BaseEdge(
        source=warehouse_state_to_core_state(edge.source),
        action=warehouse_action_to_primitive_action(edge.action),
        target=warehouse_state_to_core_state(edge.target),
        labels=edge.labels,
    )


class WarehouseGeneratedHiddenGraph(HiddenGraph):
    """HiddenGraph over a bounded generated/discovered Warehouse surface."""

    def __init__(self, edges: Iterable[WarehouseGeneratedEdge]) -> None:
        self._edges = tuple(edges)
        self._states = {edge.source.stable_id: edge.source for edge in self._edges}
        self._states.update({edge.target.stable_id: edge.target for edge in self._edges})
        self._actions = {edge.action.stable_id: edge.action for edge in self._edges}
        self._out_edges: dict[str, list[WarehouseGeneratedEdge]] = {}
        for edge in self._edges:
            self._out_edges.setdefault(edge.source.stable_id, []).append(edge)

    def is_valid_state(self, state: State) -> bool:
        try:
            warehouse_state = core_state_to_warehouse_state(state)
        except ValueError:
            return False
        return warehouse_state.stable_id in self._states

    def is_valid_action(self, action: PrimitiveAction) -> bool:
        try:
            warehouse_action = primitive_action_to_warehouse_action(action)
        except ValueError:
            return False
        return warehouse_action.stable_id in self._actions

    def apply_action(self, state: State, action: PrimitiveAction) -> State | None:
        try:
            source = core_state_to_warehouse_state(state)
            warehouse_action = primitive_action_to_warehouse_action(action)
        except ValueError:
            return None
        for edge in self._out_edges.get(source.stable_id, []):
            if edge.action.stable_id == warehouse_action.stable_id:
                return warehouse_state_to_core_state(edge.target)
        return None

    def is_valid_edge(self, edge: BaseEdge) -> bool:
        target = self.apply_action(edge.source, edge.action)
        return target == edge.target

    def out_actions(self, state: State) -> Iterable[PrimitiveAction]:
        try:
            source = core_state_to_warehouse_state(state)
        except ValueError:
            return ()
        return tuple(
            warehouse_action_to_primitive_action(edge.action)
            for edge in self._out_edges.get(source.stable_id, [])
        )

    def out_neighbors(self, state: State) -> Iterable[State]:
        try:
            source = core_state_to_warehouse_state(state)
        except ValueError:
            return ()
        return tuple(
            warehouse_state_to_core_state(edge.target)
            for edge in self._out_edges.get(source.stable_id, [])
        )

    def out_edges(self, state: State) -> Iterable[BaseEdge]:
        try:
            source = core_state_to_warehouse_state(state)
        except ValueError:
            return ()
        return tuple(
            warehouse_edge_to_base_edge(edge)
            for edge in self._out_edges.get(source.stable_id, [])
        )
