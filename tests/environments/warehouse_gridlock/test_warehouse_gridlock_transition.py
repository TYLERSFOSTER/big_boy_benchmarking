from big_boy_benchmarking.environments.warehouse_gridlock.actions import DirectionOrStay
from big_boy_benchmarking.environments.warehouse_gridlock.graph import GridNode
from big_boy_benchmarking.environments.warehouse_gridlock.instances import load_instance
from big_boy_benchmarking.environments.warehouse_gridlock.state import WarehouseGridlockState
from big_boy_benchmarking.environments.warehouse_gridlock.transition import (
    action_from_overrides,
    step,
)


def _state_with(
    robot_overrides: dict[str, GridNode] | None = None,
    box_overrides: dict[str, GridNode] | None = None,
) -> WarehouseGridlockState:
    instance = load_instance()
    robots = dict(instance.start_state.robot_positions)
    boxes = dict(instance.start_state.box_positions)
    robots.update(robot_overrides or {})
    boxes.update(box_overrides or {})
    return WarehouseGridlockState(robot_positions=robots, box_positions=boxes, time_step=0)


def test_valid_move_advances_time() -> None:
    instance = load_instance()
    action = action_from_overrides(instance.manifest.robot_ids, {"R17": DirectionOrStay.SOUTH})

    result = step(instance=instance, state=instance.start_state, action=action)

    assert result.valid
    assert result.next_state.time_step == 1
    assert result.next_state.robot_positions["R17"] == GridNode(2, 1)


def test_valid_push_moves_robot_and_box() -> None:
    instance = load_instance()
    action = action_from_overrides(instance.manifest.robot_ids, {"R19": DirectionOrStay.SOUTH})

    result = step(instance=instance, state=instance.start_state, action=action)

    assert result.valid
    assert result.next_state.robot_positions["R19"] == GridNode(2, 3)
    assert result.next_state.box_positions["B19"] == GridNode(3, 3)


def test_invalid_blocked_column_attempt_self_loops_without_time() -> None:
    instance = load_instance()
    state = _state_with({"R01": GridNode(4, 3)})
    action = action_from_overrides(instance.manifest.robot_ids, {"R01": DirectionOrStay.EAST})

    result = step(instance=instance, state=state, action=action)

    assert not result.valid
    assert result.next_state.stable_id == state.stable_id
    assert result.next_state.time_step == 0
    assert any("blocked_or_off_graph" in reason for reason in result.invalid_reasons)


def test_invalid_shared_node_and_head_on_conflicts_are_recorded() -> None:
    instance = load_instance()
    shared_state = _state_with({"R01": GridNode(5, 5), "R02": GridNode(5, 7)})
    shared_action = action_from_overrides(
        instance.manifest.robot_ids,
        {"R01": DirectionOrStay.EAST, "R02": DirectionOrStay.WEST},
    )
    shared_result = step(instance=instance, state=shared_state, action=shared_action)

    assert not shared_result.valid
    assert any("shared_node" in reason for reason in shared_result.invalid_reasons)

    head_on_state = _state_with({"R01": GridNode(6, 6), "R02": GridNode(6, 7)})
    head_on_action = action_from_overrides(
        instance.manifest.robot_ids,
        {"R01": DirectionOrStay.EAST, "R02": DirectionOrStay.WEST},
    )
    head_on_result = step(instance=instance, state=head_on_state, action=head_on_action)

    assert not head_on_result.valid
    assert any("head_on_swap" in reason for reason in head_on_result.invalid_reasons)


def test_terminal_condition_requires_exact_robots_and_boxes() -> None:
    instance = load_instance()
    action = action_from_overrides(instance.manifest.robot_ids, {})

    boxes_only = WarehouseGridlockState(
        robot_positions=instance.start_state.robot_positions,
        box_positions=instance.manifest.box_target_map(),
        time_step=0,
    )
    boxes_only_result = step(instance=instance, state=boxes_only, action=action)
    assert not boxes_only_result.terminated

    robots_only = WarehouseGridlockState(
        robot_positions=instance.manifest.robot_target_map(),
        box_positions=instance.start_state.box_positions,
        time_step=0,
    )
    robots_only_result = step(instance=instance, state=robots_only, action=action)
    assert not robots_only_result.terminated

    solved = WarehouseGridlockState(
        robot_positions=instance.manifest.robot_target_map(),
        box_positions=instance.manifest.box_target_map(),
        time_step=0,
    )
    solved_result = step(instance=instance, state=solved, action=action)
    assert solved_result.terminated
