import pytest

from big_boy_benchmarking.environments.warehouse_gridlock.actions import (
    DirectionOrStay,
    WarehouseGridlockAction,
    forbid_full_action_enumeration,
    stay_action,
    validate_action,
)
from big_boy_benchmarking.environments.warehouse_gridlock.graph import GridNode
from big_boy_benchmarking.environments.warehouse_gridlock.instances import load_instance
from big_boy_benchmarking.environments.warehouse_gridlock.state import (
    WarehouseGridlockState,
    validate_state,
)


def test_state_round_trips_through_json_payload() -> None:
    instance = load_instance()

    payload = instance.start_state.to_dict()
    restored = WarehouseGridlockState.from_dict(payload)

    assert restored.stable_id == instance.start_state.stable_id


def test_state_validation_rejects_robot_box_overlap() -> None:
    instance = load_instance()
    robots = dict(instance.start_state.robot_positions)
    boxes = dict(instance.start_state.box_positions)
    boxes["B01"] = robots["R01"]
    state = WarehouseGridlockState(robot_positions=robots, box_positions=boxes, time_step=0)

    report = validate_state(
        state,
        graph=instance.graph,
        required_robot_ids=instance.manifest.robot_ids,
        required_box_ids=instance.manifest.box_ids,
    )

    assert not report.ok
    assert any("robot-box overlap" in error for error in report.errors)


def test_state_validation_rejects_blocked_occupancy() -> None:
    instance = load_instance()
    robots = dict(instance.start_state.robot_positions)
    robots["R01"] = GridNode(4, 4)
    state = WarehouseGridlockState(
        robot_positions=robots,
        box_positions=instance.start_state.box_positions,
        time_step=0,
    )

    report = validate_state(
        state,
        graph=instance.graph,
        required_robot_ids=instance.manifest.robot_ids,
        required_box_ids=instance.manifest.box_ids,
    )

    assert not report.ok
    assert any("blocked node" in error for error in report.errors)


def test_action_validation_and_enumeration_guard() -> None:
    instance = load_instance()
    action = stay_action(instance.manifest.robot_ids)

    assert validate_action(action, required_robot_ids=instance.manifest.robot_ids).ok

    missing = WarehouseGridlockAction(commands={"R01": DirectionOrStay.STAY})
    assert not validate_action(missing, required_robot_ids=instance.manifest.robot_ids).ok

    with pytest.raises(RuntimeError, match="flat enumeration is forbidden"):
        forbid_full_action_enumeration(len(instance.manifest.robot_ids))
