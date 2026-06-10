"""Synchronous Warehouse Gridlock transition engine."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from big_boy_benchmarking.environments.warehouse_gridlock.actions import (
    DirectionOrStay,
    WarehouseGridlockAction,
    validate_action,
)
from big_boy_benchmarking.environments.warehouse_gridlock.collisions import (
    EntityMovement,
    head_on_swap_conflicts,
    shared_node_conflicts,
)
from big_boy_benchmarking.environments.warehouse_gridlock.discovery import DiscoveryEvent
from big_boy_benchmarking.environments.warehouse_gridlock.graph import (
    Direction,
    GridNode,
    WarehouseGraph,
)
from big_boy_benchmarking.environments.warehouse_gridlock.instances import (
    WarehouseGridlockInstance,
)
from big_boy_benchmarking.environments.warehouse_gridlock.rewards import (
    compute_reward,
    is_terminal,
)
from big_boy_benchmarking.environments.warehouse_gridlock.state import (
    WarehouseGridlockState,
)

COMMAND_TO_DIRECTION: dict[DirectionOrStay, Direction] = {
    DirectionOrStay.NORTH: Direction.NORTH,
    DirectionOrStay.SOUTH: Direction.SOUTH,
    DirectionOrStay.EAST: Direction.EAST,
    DirectionOrStay.WEST: Direction.WEST,
}


@dataclass(frozen=True)
class WarehouseGridlockStepResult:
    next_state: WarehouseGridlockState
    reward: float
    terminated: bool
    truncated: bool
    valid: bool
    moved_robots: tuple[EntityMovement, ...]
    moved_boxes: tuple[EntityMovement, ...]
    invalid_reasons: tuple[str, ...]
    discovery_events: tuple[DiscoveryEvent, ...]

    def to_summary_row(self, case_id: str) -> dict[str, object]:
        return {
            "case_id": case_id,
            "valid": self.valid,
            "reward": self.reward,
            "terminated": self.terminated,
            "truncated": self.truncated,
            "time_step": self.next_state.time_step,
            "moved_robot_count": len(self.moved_robots),
            "moved_box_count": len(self.moved_boxes),
            "invalid_reasons": "|".join(self.invalid_reasons),
        }


def step(
    *,
    instance: WarehouseGridlockInstance,
    state: WarehouseGridlockState,
    action: WarehouseGridlockAction,
    max_seconds: int | None = None,
    reward_mode_id: str | None = None,
) -> WarehouseGridlockStepResult:
    manifest = instance.manifest
    action_report = validate_action(action, required_robot_ids=manifest.robot_ids)
    robot_positions = dict(state.robot_positions)
    box_positions = dict(state.box_positions)
    robot_at = {node: robot_id for robot_id, node in robot_positions.items()}
    box_at = {node: box_id for box_id, node in box_positions.items()}
    robot_moves: list[EntityMovement] = []
    box_moves: list[EntityMovement] = []
    invalid_reasons: list[str] = list(action_report.errors)
    pushed_boxes: set[str] = set()

    for robot_id, command in sorted(action.commands.items()):
        source = robot_positions[robot_id]
        if command == DirectionOrStay.STAY:
            robot_moves.append(EntityMovement(robot_id, "robot", source, source))
            continue
        direction = COMMAND_TO_DIRECTION[command]
        target = _neighbor_if_traversable(instance.graph, source, direction)
        if target is None:
            invalid_reasons.append(f"blocked_or_off_graph_robot_move:{robot_id}:{command.value}")
            robot_moves.append(EntityMovement(robot_id, "robot", source, source))
            continue
        if target in box_at:
            box_id = box_at[target]
            box_target = _neighbor_if_traversable(instance.graph, target, direction)
            if box_target is None:
                invalid_reasons.append(
                    f"invalid_push_destination:{robot_id}:{box_id}:{command.value}"
                )
                robot_moves.append(EntityMovement(robot_id, "robot", source, source))
                continue
            if box_target in box_at or box_target in robot_at:
                invalid_reasons.append(
                    f"occupied_push_destination:{robot_id}:{box_id}:{box_target.key}"
                )
                robot_moves.append(EntityMovement(robot_id, "robot", source, source))
                continue
            if box_id in pushed_boxes:
                invalid_reasons.append(f"box_pushed_by_multiple_robots:{box_id}")
                robot_moves.append(EntityMovement(robot_id, "robot", source, source))
                continue
            pushed_boxes.add(box_id)
            robot_moves.append(EntityMovement(robot_id, "robot", source, target))
            box_moves.append(EntityMovement(box_id, "box", target, box_target))
            continue
        robot_moves.append(EntityMovement(robot_id, "robot", source, target))

    for box_id, source in sorted(box_positions.items()):
        if box_id not in pushed_boxes:
            box_moves.append(EntityMovement(box_id, "box", source, source))

    invalid_reasons.extend(shared_node_conflicts(robot_moves + box_moves))
    invalid_reasons.extend(head_on_swap_conflicts(robot_moves + box_moves))
    invalid_reasons = sorted(set(invalid_reasons))

    valid = not invalid_reasons
    if valid:
        next_robots = {movement.entity_id: movement.target for movement in robot_moves}
        next_boxes = {movement.entity_id: movement.target for movement in box_moves}
        next_state = WarehouseGridlockState(
            robot_positions=next_robots,
            box_positions=next_boxes,
            time_step=state.time_step + 1,
        )
    else:
        next_state = state

    terminated = is_terminal(
        next_state,
        robot_targets=manifest.robot_target_map(),
        box_targets=manifest.box_target_map(),
    )
    truncated = max_seconds is not None and next_state.time_step >= max_seconds and not terminated
    reward = compute_reward(
        state=next_state,
        robot_targets=manifest.robot_target_map(),
        box_targets=manifest.box_target_map(),
        policy=manifest.reward_policy,
        valid_transition=valid,
        reward_mode_id=reward_mode_id,
    )
    discovery = DiscoveryEvent(
        event_type="valid_ensemble" if valid else "invalid_ensemble",
        state_id=state.stable_id,
        action_id=action.stable_id,
        valid=valid,
        invalid_reasons=tuple(invalid_reasons),
    )
    return WarehouseGridlockStepResult(
        next_state=next_state,
        reward=reward,
        terminated=terminated,
        truncated=truncated,
        valid=valid,
        moved_robots=tuple(
            movement for movement in robot_moves if movement.source != movement.target
        ),
        moved_boxes=tuple(movement for movement in box_moves if movement.source != movement.target),
        invalid_reasons=tuple(invalid_reasons),
        discovery_events=(discovery,),
    )


def _neighbor_if_traversable(
    graph: WarehouseGraph,
    node: GridNode,
    direction: Direction,
) -> GridNode | None:
    target = graph.neighbor(node, direction)
    if target is None:
        return None
    if not graph.is_traversable_node(target):
        return None
    if not graph.has_edge(node, target):
        return None
    return target


def action_from_overrides(
    robot_ids: tuple[str, ...],
    overrides: Mapping[str, DirectionOrStay],
) -> WarehouseGridlockAction:
    commands = {robot_id: DirectionOrStay.STAY for robot_id in robot_ids}
    commands.update(overrides)
    return WarehouseGridlockAction(commands=commands)
