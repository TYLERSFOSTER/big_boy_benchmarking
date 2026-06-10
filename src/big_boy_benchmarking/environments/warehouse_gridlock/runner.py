"""Readiness runners for Warehouse Gridlock."""

from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.environments.warehouse_gridlock.actions import (
    DirectionOrStay,
    WarehouseGridlockAction,
    stay_action,
)
from big_boy_benchmarking.environments.warehouse_gridlock.docs_writer import (
    existing_core_artifact_paths,
    write_core_readiness_artifacts,
    write_human_docs,
    write_readout_source,
)
from big_boy_benchmarking.environments.warehouse_gridlock.graph import GridNode
from big_boy_benchmarking.environments.warehouse_gridlock.ids import (
    WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID,
)
from big_boy_benchmarking.environments.warehouse_gridlock.instances import load_instance
from big_boy_benchmarking.environments.warehouse_gridlock.state import (
    WarehouseGridlockState,
)
from big_boy_benchmarking.environments.warehouse_gridlock.transition import (
    action_from_overrides,
    step,
)
from big_boy_benchmarking.environments.warehouse_gridlock.validation import validate_readiness


@dataclass(frozen=True)
class WarehouseGridlockRunResult:
    status: str
    artifact_paths: dict[str, str]
    summary: dict[str, object]


def run_graph_diagnostics(
    *,
    artifact_root: Path | str,
    instance_id: str = WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID,
    run_label: str = "smoke_001",
) -> WarehouseGridlockRunResult:
    instance = load_instance(instance_id=instance_id)
    artifact_paths = write_core_readiness_artifacts(
        instance=instance,
        artifact_root=artifact_root,
        run_label=run_label,
    )
    readiness = validate_readiness(instance)
    return WarehouseGridlockRunResult(
        status=readiness.status,
        artifact_paths=artifact_paths,
        summary=readiness.summary,
    )


def run_state_diagnostics(
    *,
    artifact_root: Path | str,
    instance_id: str = WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID,
    run_label: str = "smoke_001",
) -> WarehouseGridlockRunResult:
    return run_graph_diagnostics(
        artifact_root=artifact_root,
        instance_id=instance_id,
        run_label=run_label,
    )


def run_transition_smoke(
    *,
    artifact_root: Path | str,
    instance_id: str = WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID,
    run_label: str = "smoke_001",
) -> WarehouseGridlockRunResult:
    instance = load_instance(instance_id=instance_id)
    cases = _transition_smoke_cases(instance)
    rows: list[dict[str, object]] = []
    invalid_reasons: Counter[str] = Counter()
    discovery_events = []
    for case_id, state, action in cases:
        result = step(instance=instance, state=state, action=action)
        rows.append(result.to_summary_row(case_id))
        invalid_reasons.update(result.invalid_reasons)
        discovery_events.extend(result.discovery_events)
    invalid_rows = [
        {"invalid_reason": reason, "count": count}
        for reason, count in sorted(invalid_reasons.items())
    ]
    artifact_paths = write_core_readiness_artifacts(
        instance=instance,
        artifact_root=artifact_root,
        run_label=run_label,
        transition_rows=rows,
        invalid_rows=invalid_rows,
        discovery_events=discovery_events,
    )
    readiness = validate_readiness(instance)
    return WarehouseGridlockRunResult(
        status=readiness.status,
        artifact_paths=artifact_paths,
        summary={
            **readiness.summary,
            "transition_case_count": len(rows),
            "invalid_reason_count": len(invalid_rows),
        },
    )


def run_random_rollout(
    *,
    artifact_root: Path | str,
    instance_id: str = WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID,
    run_label: str = "smoke_001",
    seconds: int = 8,
    seed: int = 0,
) -> WarehouseGridlockRunResult:
    instance = load_instance(instance_id=instance_id)
    rng = random.Random(seed)
    state = instance.start_state
    rows: list[dict[str, object]] = []
    invalid_reasons: Counter[str] = Counter()
    discovery_events = []
    commands = tuple(DirectionOrStay)
    for index in range(seconds):
        action = WarehouseGridlockAction(
            commands={robot_id: rng.choice(commands) for robot_id in instance.manifest.robot_ids}
        )
        result = step(instance=instance, state=state, action=action, max_seconds=seconds)
        rows.append(result.to_summary_row(f"random_{index:03d}"))
        invalid_reasons.update(result.invalid_reasons)
        discovery_events.extend(result.discovery_events)
        state = result.next_state
        if result.terminated or result.truncated:
            break
    artifact_paths = write_core_readiness_artifacts(
        instance=instance,
        artifact_root=artifact_root,
        run_label=run_label,
        transition_rows=rows,
        invalid_rows=[
            {"invalid_reason": reason, "count": count}
            for reason, count in sorted(invalid_reasons.items())
        ],
        discovery_events=discovery_events,
    )
    readiness = validate_readiness(instance)
    return WarehouseGridlockRunResult(
        status=readiness.status,
        artifact_paths=artifact_paths,
        summary={**readiness.summary, "rollout_steps_recorded": len(rows)},
    )


def build_readiness_docs(
    *,
    repo_root: Path | str,
    artifact_root: Path | str,
    instance_id: str = WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID,
    run_label: str = "smoke_001",
) -> WarehouseGridlockRunResult:
    instance = load_instance(instance_id=instance_id)
    artifacts = existing_core_artifact_paths(artifact_root)
    if "environment_instance_manifest" not in artifacts:
        artifacts = write_core_readiness_artifacts(
            instance=instance,
            artifact_root=artifact_root,
            run_label=run_label,
        )
    readout_source = write_readout_source(
        repo_root=repo_root,
        artifact_root=artifact_root,
        artifact_paths=artifacts,
        instance=instance,
    )
    docs = write_human_docs(
        repo_root=repo_root,
        artifact_root=artifact_root,
        readout_source=readout_source,
        artifact_paths=artifacts,
        instance=instance,
    )
    readiness = validate_readiness(instance)
    return WarehouseGridlockRunResult(
        status=readiness.status,
        artifact_paths={**artifacts, "readout_source": str(readout_source), **docs},
        summary=readiness.summary,
    )


def _transition_smoke_cases(
    instance,
) -> list[tuple[str, WarehouseGridlockState, WarehouseGridlockAction]]:
    ids = instance.manifest.robot_ids
    start = instance.start_state
    cases: list[tuple[str, WarehouseGridlockState, WarehouseGridlockAction]] = [
        ("all_stay", start, stay_action(ids)),
        (
            "single_robot_empty_move",
            start,
            action_from_overrides(ids, {"R17": DirectionOrStay.SOUTH}),
        ),
        (
            "single_robot_push_box",
            start,
            action_from_overrides(ids, {"R19": DirectionOrStay.SOUTH}),
        ),
        (
            "shared_node_conflict",
            _micro_state(instance, {"R01": GridNode(5, 5), "R02": GridNode(5, 7)}, {}),
            action_from_overrides(ids, {"R01": DirectionOrStay.EAST, "R02": DirectionOrStay.WEST}),
        ),
        (
            "head_on_swap_conflict",
            _micro_state(instance, {"R01": GridNode(6, 6), "R02": GridNode(6, 7)}, {}),
            action_from_overrides(ids, {"R01": DirectionOrStay.EAST, "R02": DirectionOrStay.WEST}),
        ),
        (
            "blocked_column_attempt",
            _micro_state(instance, {"R01": GridNode(4, 3)}, {}),
            action_from_overrides(ids, {"R01": DirectionOrStay.EAST}),
        ),
        (
            "invalid_push_destination",
            _micro_state(
                instance,
                {"R01": GridNode(6, 6), "R02": GridNode(6, 8)},
                {"B01": GridNode(6, 7)},
            ),
            action_from_overrides(ids, {"R01": DirectionOrStay.EAST}),
        ),
    ]
    return cases


def _micro_state(
    instance,
    robot_overrides: dict[str, GridNode],
    box_overrides: dict[str, GridNode],
) -> WarehouseGridlockState:
    robots = dict(instance.start_state.robot_positions)
    boxes = dict(instance.start_state.box_positions)
    robots.update(robot_overrides)
    boxes.update(box_overrides)
    return WarehouseGridlockState(robot_positions=robots, box_positions=boxes, time_step=0)
