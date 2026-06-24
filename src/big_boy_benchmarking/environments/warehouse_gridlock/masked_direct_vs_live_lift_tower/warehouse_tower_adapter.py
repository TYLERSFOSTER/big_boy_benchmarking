"""Scoped `state_collapser` adapter for Warehouse Gridlock generated surfaces."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from state_collapser.core.action import PrimitiveAction
from state_collapser.core.edges import BaseEdge
from state_collapser.core.state import State
from state_collapser.graph.hidden_graph import HiddenGraph

from big_boy_benchmarking.environments.warehouse_gridlock.actions import (
    DirectionOrStay,
    WarehouseGridlockAction,
)
from big_boy_benchmarking.environments.warehouse_gridlock.graph import GridNode
from big_boy_benchmarking.environments.warehouse_gridlock.state import (
    WarehouseGridlockState,
)


def warehouse_state_to_core_state(state: WarehouseGridlockState) -> State:
    payload = _state_payload(state)
    return State(
        payload=payload,
        identity=("warehouse_gridlock_001_state", state.stable_id),
    )


def core_state_to_warehouse_state(state: State) -> WarehouseGridlockState:
    if isinstance(state.payload, WarehouseGridlockState):
        return state.payload
    if not (
        isinstance(state.payload, tuple)
        and len(state.payload) == 4
        and state.payload[0] == "warehouse_gridlock_001_state"
    ):
        raise ValueError(f"unsupported Warehouse state payload: {state.payload!r}")
    _, time_step, robot_items, box_items = state.payload
    return WarehouseGridlockState(
        robot_positions={
            str(robot_id): GridNode(int(row), int(col))
            for robot_id, row, col in tuple(robot_items)
        },
        box_positions={
            str(box_id): GridNode(int(row), int(col))
            for box_id, row, col in tuple(box_items)
        },
        time_step=int(time_step),
    )


def warehouse_action_to_primitive_action(action: WarehouseGridlockAction) -> PrimitiveAction:
    payload = _action_payload(action)
    return PrimitiveAction(
        payload=payload,
        identity=("warehouse_gridlock_001_generated_action", action.stable_id),
        labels=(
            "warehouse_gridlock_action",
            ("generated_candidate_surface", True),
        ),
    )


def primitive_action_to_warehouse_action(action: PrimitiveAction) -> WarehouseGridlockAction:
    if isinstance(action.payload, WarehouseGridlockAction):
        return action.payload
    if not (
        isinstance(action.payload, tuple)
        and len(action.payload) == 2
        and action.payload[0] == "warehouse_gridlock_001_action"
    ):
        raise ValueError(f"unsupported Warehouse action payload: {action.payload!r}")
    _, command_items = action.payload
    return WarehouseGridlockAction(
        commands={
            str(robot_id): DirectionOrStay(str(command))
            for robot_id, command in tuple(command_items)
        }
    )


def _state_payload(state: WarehouseGridlockState) -> tuple[object, ...]:
    return (
        "warehouse_gridlock_001_state",
        state.time_step,
        tuple(
            (robot_id, node.row, node.col)
            for robot_id, node in sorted(state.robot_positions.items())
        ),
        tuple(
            (box_id, node.row, node.col)
            for box_id, node in sorted(state.box_positions.items())
        ),
    )


def _action_payload(action: WarehouseGridlockAction) -> tuple[object, ...]:
    return (
        "warehouse_gridlock_001_action",
        tuple(
            (robot_id, command.value)
            for robot_id, command in sorted(action.commands.items())
        ),
    )


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
