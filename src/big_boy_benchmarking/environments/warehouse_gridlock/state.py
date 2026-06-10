"""State model for Warehouse Gridlock."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from big_boy_benchmarking.environments.warehouse_gridlock.graph import GridNode, WarehouseGraph


@dataclass(frozen=True)
class WarehouseGridlockState:
    robot_positions: Mapping[str, GridNode]
    box_positions: Mapping[str, GridNode]
    time_step: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "robot_positions": {
                robot_id: node.to_dict() for robot_id, node in sorted(self.robot_positions.items())
            },
            "box_positions": {
                box_id: node.to_dict() for box_id, node in sorted(self.box_positions.items())
            },
            "time_step": self.time_step,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> WarehouseGridlockState:
        robots = {
            str(robot_id): GridNode.from_dict(node)  # type: ignore[arg-type]
            for robot_id, node in dict(payload["robot_positions"]).items()
        }
        boxes = {
            str(box_id): GridNode.from_dict(node)  # type: ignore[arg-type]
            for box_id, node in dict(payload["box_positions"]).items()
        }
        return cls(robot_positions=robots, box_positions=boxes, time_step=int(payload["time_step"]))

    @property
    def stable_id(self) -> str:
        robot_bits = ",".join(
            f"{robot_id}:{node.key}" for robot_id, node in sorted(self.robot_positions.items())
        )
        box_bits = ",".join(
            f"{box_id}:{node.key}" for box_id, node in sorted(self.box_positions.items())
        )
        return f"t{self.time_step}|robots={robot_bits}|boxes={box_bits}"


@dataclass(frozen=True)
class StateValidationReport:
    status: str
    errors: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, object]:
        return {"status": self.status, "errors": list(self.errors)}


def validate_state(
    state: WarehouseGridlockState,
    *,
    graph: WarehouseGraph,
    required_robot_ids: tuple[str, ...],
    required_box_ids: tuple[str, ...],
) -> StateValidationReport:
    errors: list[str] = []
    robot_ids = set(state.robot_positions)
    box_ids = set(state.box_positions)
    expected_robot_ids = set(required_robot_ids)
    expected_box_ids = set(required_box_ids)
    if robot_ids != expected_robot_ids:
        errors.append(
            "robot id mismatch: "
            f"missing={sorted(expected_robot_ids - robot_ids)} "
            f"unknown={sorted(robot_ids - expected_robot_ids)}"
        )
    if box_ids != expected_box_ids:
        errors.append(
            "box id mismatch: "
            f"missing={sorted(expected_box_ids - box_ids)} "
            f"unknown={sorted(box_ids - expected_box_ids)}"
        )
    if state.time_step < 0:
        errors.append("time_step must be nonnegative")
    _validate_positions("robot", state.robot_positions, graph, errors)
    _validate_positions("box", state.box_positions, graph, errors)
    robot_nodes = list(state.robot_positions.values())
    box_nodes = list(state.box_positions.values())
    if len(set(robot_nodes)) != len(robot_nodes):
        errors.append("duplicate robot occupancy")
    if len(set(box_nodes)) != len(box_nodes):
        errors.append("duplicate box occupancy")
    overlap = sorted(set(robot_nodes) & set(box_nodes))
    if overlap:
        errors.append(f"robot-box overlap at {[node.key for node in overlap]}")
    return StateValidationReport(status="ok" if not errors else "error", errors=tuple(errors))


def _validate_positions(
    label: str,
    positions: Mapping[str, GridNode],
    graph: WarehouseGraph,
    errors: list[str],
) -> None:
    for entity_id, node in sorted(positions.items()):
        if not graph.is_known_node(node):
            errors.append(f"{label} {entity_id} occupies unknown node {node.key}")
        elif not graph.is_traversable_node(node):
            errors.append(f"{label} {entity_id} occupies blocked node {node.key}")
