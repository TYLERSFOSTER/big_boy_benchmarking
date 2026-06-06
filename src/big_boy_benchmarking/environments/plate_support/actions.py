"""Stable PlateSupport primitive action contract."""

from __future__ import annotations

from big_boy_benchmarking.environments.plate_support.types import ActionRecord

ACTION_RECORDS: tuple[ActionRecord, ...] = (
    ActionRecord(
        0,
        "plate_x_plus",
        "plate_translation",
        "Move the plate center one grid unit in positive x.",
        "upstream_action_0",
    ),
    ActionRecord(
        1,
        "plate_x_minus",
        "plate_translation",
        "Move the plate center one grid unit in negative x.",
        "upstream_action_1",
    ),
    ActionRecord(
        2,
        "plate_y_plus",
        "plate_translation",
        "Move the plate center one grid unit in positive y.",
        "upstream_action_2",
    ),
    ActionRecord(
        3,
        "plate_y_minus",
        "plate_translation",
        "Move the plate center one grid unit in negative y.",
        "upstream_action_3",
    ),
    ActionRecord(
        4,
        "theta_plus",
        "plate_rotation",
        "Advance the discrete plate orientation.",
        "upstream_action_4",
    ),
    ActionRecord(
        5,
        "theta_minus",
        "plate_rotation",
        "Reverse the discrete plate orientation.",
        "upstream_action_5",
    ),
    ActionRecord(
        6,
        "arm1_extend",
        "arm_extension",
        "Increase arm 1 extension by one discrete unit.",
        "upstream_action_6",
    ),
    ActionRecord(
        7,
        "arm1_retract",
        "arm_extension",
        "Decrease arm 1 extension by one discrete unit.",
        "upstream_action_7",
    ),
    ActionRecord(
        8,
        "arm2_extend",
        "arm_extension",
        "Increase arm 2 extension by one discrete unit.",
        "upstream_action_8",
    ),
    ActionRecord(
        9,
        "arm2_retract",
        "arm_extension",
        "Decrease arm 2 extension by one discrete unit.",
        "upstream_action_9",
    ),
    ActionRecord(
        10,
        "arm3_extend",
        "arm_extension",
        "Increase arm 3 extension by one discrete unit.",
        "upstream_action_10",
    ),
    ActionRecord(
        11,
        "arm3_retract",
        "arm_extension",
        "Decrease arm 3 extension by one discrete unit.",
        "upstream_action_11",
    ),
)


def action_label(action_index: int) -> str:
    try:
        return ACTION_RECORDS[action_index].action_label
    except IndexError as exc:
        raise ValueError(f"unknown PlateSupport action index: {action_index}") from exc


def action_table_rows() -> list[dict[str, object]]:
    return [record.to_dict() for record in ACTION_RECORDS]
