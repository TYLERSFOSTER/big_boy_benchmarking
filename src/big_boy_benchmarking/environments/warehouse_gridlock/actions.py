"""Structured ensemble actions for Warehouse Gridlock."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum


class DirectionOrStay(StrEnum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    STAY = "stay"


COMMAND_VALUES = tuple(command.value for command in DirectionOrStay)


@dataclass(frozen=True)
class WarehouseGridlockAction:
    commands: Mapping[str, DirectionOrStay]

    def to_dict(self) -> dict[str, str]:
        return {robot_id: command.value for robot_id, command in sorted(self.commands.items())}

    @classmethod
    def from_dict(cls, payload: Mapping[str, str]) -> WarehouseGridlockAction:
        return cls(
            commands={
                str(robot_id): DirectionOrStay(str(command))
                for robot_id, command in payload.items()
            }
        )

    @property
    def stable_id(self) -> str:
        return ",".join(
            f"{robot_id}:{command.value}" for robot_id, command in sorted(self.commands.items())
        )


@dataclass(frozen=True)
class ActionValidationReport:
    status: str
    errors: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, object]:
        return {"status": self.status, "errors": list(self.errors)}


def validate_action(
    action: WarehouseGridlockAction,
    *,
    required_robot_ids: tuple[str, ...],
) -> ActionValidationReport:
    errors: list[str] = []
    expected = set(required_robot_ids)
    actual = set(action.commands)
    if actual != expected:
        errors.append(
            "robot command id mismatch: "
            f"missing={sorted(expected - actual)} unknown={sorted(actual - expected)}"
        )
    for robot_id, command in action.commands.items():
        if not isinstance(command, DirectionOrStay):
            errors.append(f"invalid command for {robot_id}: {command!r}")
    return ActionValidationReport(status="ok" if not errors else "error", errors=tuple(errors))


def stay_action(required_robot_ids: tuple[str, ...]) -> WarehouseGridlockAction:
    return WarehouseGridlockAction(
        commands={robot_id: DirectionOrStay.STAY for robot_id in required_robot_ids}
    )


def forbid_full_action_enumeration(robot_count: int) -> None:
    if robot_count >= 32:
        raise RuntimeError(
            "flat enumeration is forbidden for Warehouse Gridlock full instances; "
            f"received robot_count={robot_count}, action_count=5^{robot_count}"
        )
