"""Reusable full-state feature encoder for Warehouse Gridlock policies."""

from __future__ import annotations

from math import copysign

from big_boy_benchmarking.environments.warehouse_gridlock.actions import DirectionOrStay
from big_boy_benchmarking.environments.warehouse_gridlock.policies.contracts import (
    WarehouseFullSystemConfig,
)
from big_boy_benchmarking.environments.warehouse_gridlock.policies.serialization import (
    feature_key,
)

MOVE_DELTAS: dict[DirectionOrStay, tuple[int, int]] = {
    DirectionOrStay.NORTH: (-1, 0),
    DirectionOrStay.SOUTH: (1, 0),
    DirectionOrStay.EAST: (0, 1),
    DirectionOrStay.WEST: (0, -1),
    DirectionOrStay.STAY: (0, 0),
}


def command_features(
    *,
    config: WarehouseFullSystemConfig,
    robot_id: str,
    command: DirectionOrStay,
    second: int,
) -> dict[str, float]:
    robot_position = _parse_node(config.dynamic.robot_positions[robot_id])
    robot_target = _parse_node(config.static.robot_target_map[robot_id])
    box_positions = {
        box_id: _parse_node(node_key) for box_id, node_key in config.dynamic.box_positions.items()
    }
    box_targets = {
        box_id: _parse_node(node_key) for box_id, node_key in config.static.box_target_map.items()
    }
    next_position = _move(robot_position, command)
    nearest_box_id, nearest_box = _nearest(robot_position, box_positions)
    blocked_nodes = set(config.static.blocked_nodes)
    edge_set = set(tuple(edge) for edge in config.static.traversable_edges)
    target_delta_before = _manhattan(robot_position, robot_target)
    target_delta_after = _manhattan(next_position, robot_target)
    features: dict[str, float] = {
        feature_key("bias", command.value): 1.0,
        feature_key("command", command.value): 1.0,
        feature_key("robot_to_robot_target_delta", command.value): float(
            target_delta_before - target_delta_after
        ),
        feature_key("second_fraction_remaining"): _second_fraction_remaining(config, second),
        feature_key("correct_robot_indicator", command.value): float(robot_position == robot_target),
        feature_key("edge_exists_indicator", command.value): float(
            command == DirectionOrStay.STAY
            or (_node_key(robot_position), _node_key(next_position)) in edge_set
        ),
        feature_key("blocked_direction_indicator", command.value): float(
            command != DirectionOrStay.STAY and _node_key(next_position) in blocked_nodes
        ),
        feature_key("local_occupancy_around_robot", command.value): float(
            _node_key(next_position) in set(config.dynamic.robot_positions.values())
            or _node_key(next_position) in set(config.dynamic.box_positions.values())
        ),
    }
    if nearest_box_id is not None and nearest_box is not None:
        box_target = box_targets[nearest_box_id]
        features[feature_key("robot_to_nearest_box_delta", command.value)] = float(
            _manhattan(robot_position, nearest_box) - _manhattan(next_position, nearest_box)
        )
        features[feature_key("box_to_box_target_delta", command.value)] = float(
            _manhattan(nearest_box, box_target)
        )
        features[feature_key("box_to_target_alignment", command.value)] = _alignment(
            source=robot_position,
            waypoint=nearest_box,
            target=box_target,
        )
        features[feature_key("robot_to_pushable_box_alignment", command.value)] = _push_alignment(
            robot=robot_position,
            box=nearest_box,
            box_target=box_target,
            command=command,
        )
        features[feature_key("local_occupancy_around_box", command.value)] = float(
            _neighbor_occupancy_count(nearest_box, config) / 4.0
        )
        features[feature_key("correct_box_indicator", command.value)] = float(nearest_box == box_target)
    else:
        features[feature_key("robot_to_nearest_box_delta", command.value)] = 0.0
        features[feature_key("box_to_box_target_delta", command.value)] = 0.0
        features[feature_key("box_to_target_alignment", command.value)] = 0.0
        features[feature_key("robot_to_pushable_box_alignment", command.value)] = 0.0
        features[feature_key("local_occupancy_around_box", command.value)] = 0.0
        features[feature_key("correct_box_indicator", command.value)] = 0.0
    return features


def score_features(weights: dict[str, float], features: dict[str, float]) -> float:
    return sum(weights.get(key, 0.0) * value for key, value in features.items())


def _parse_node(node_key: str) -> tuple[int, int]:
    return int(node_key[1:3]), int(node_key[4:6])


def _node_key(node: tuple[int, int]) -> str:
    row, col = node
    return f"r{row:02d}c{col:02d}"


def _move(node: tuple[int, int], command: DirectionOrStay) -> tuple[int, int]:
    dr, dc = MOVE_DELTAS[command]
    return node[0] + dr, node[1] + dc


def _manhattan(source: tuple[int, int], target: tuple[int, int]) -> int:
    return abs(source[0] - target[0]) + abs(source[1] - target[1])


def _nearest(
    source: tuple[int, int],
    positions: dict[str, tuple[int, int]],
) -> tuple[str | None, tuple[int, int] | None]:
    if not positions:
        return None, None
    box_id, node = min(
        positions.items(),
        key=lambda item: (_manhattan(source, item[1]), item[0]),
    )
    return box_id, node


def _alignment(
    *,
    source: tuple[int, int],
    waypoint: tuple[int, int],
    target: tuple[int, int],
) -> float:
    before = _manhattan(source, waypoint) + _manhattan(waypoint, target)
    direct = _manhattan(source, target)
    return float(direct - before)


def _push_alignment(
    *,
    robot: tuple[int, int],
    box: tuple[int, int],
    box_target: tuple[int, int],
    command: DirectionOrStay,
) -> float:
    if command == DirectionOrStay.STAY:
        return 0.0
    dr, dc = MOVE_DELTAS[command]
    if (robot[0] + dr, robot[1] + dc) != box:
        return 0.0
    after = (box[0] + dr, box[1] + dc)
    return float(_manhattan(box, box_target) - _manhattan(after, box_target))


def _neighbor_occupancy_count(
    node: tuple[int, int],
    config: WarehouseFullSystemConfig,
) -> int:
    occupied = set(config.dynamic.robot_positions.values()) | set(config.dynamic.box_positions.values())
    return sum(
        1
        for command in (
            DirectionOrStay.NORTH,
            DirectionOrStay.SOUTH,
            DirectionOrStay.EAST,
            DirectionOrStay.WEST,
        )
        if _node_key(_move(node, command)) in occupied
    )


def _second_fraction_remaining(config: WarehouseFullSystemConfig, second: int) -> float:
    max_seconds = max(1, config.static.max_seconds_per_episode)
    remaining = max(0, max_seconds - second)
    value = remaining / max_seconds
    return float(copysign(min(abs(value), 1.0), value))
