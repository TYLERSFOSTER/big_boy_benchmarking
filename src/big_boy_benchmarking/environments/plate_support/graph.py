"""Exact valid-state graph diagnostics for PlateSupport."""

from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from typing import Any

from big_boy_benchmarking.environments.plate_support.actions import action_label
from big_boy_benchmarking.environments.plate_support.states import state_id
from big_boy_benchmarking.environments.plate_support.types import (
    ShortestPathRecord,
    TransitionRecord,
)
from big_boy_benchmarking.environments.plate_support.upstream import (
    ImportedPlateSupportSurface,
    import_plate_support_surface,
)


@dataclass(frozen=True)
class PlateSupportGraphDiagnostics:
    graph_summary: dict[str, object]
    transition_records: tuple[TransitionRecord, ...]
    shortest_path_records: tuple[ShortestPathRecord, ...]
    outgoing_action_count_summary: tuple[dict[str, object], ...]
    invalid_action_summary: tuple[dict[str, object], ...]
    self_transition_summary: tuple[dict[str, object], ...]


def build_plate_support_graph_diagnostics(
    *,
    surface: ImportedPlateSupportSurface | None = None,
) -> PlateSupportGraphDiagnostics:
    surface = surface or import_plate_support_surface()
    valid_states = tuple(surface.all_valid_states())
    candidate_states = tuple(surface.all_candidate_states())
    transitions = tuple(
        _transition_record(surface=surface, source_state=source_state, action_index=action_index)
        for source_state in valid_states
        for action_index in range(surface.ACTION_COUNT)
    )
    adjacency = _adjacency_by_state(valid_states, transitions)
    reachable = _reachable_state_ids(state_id(surface.START_STATE), adjacency)
    shortest_path = _shortest_path_records(surface=surface, adjacency=adjacency)
    per_state_counts = _per_state_counts(valid_states, transitions)
    graph_summary = {
        "environment_instance_id": "plate_support_5x5_default_v001",
        "candidate_state_count": len(candidate_states),
        "valid_state_count": len(valid_states),
        "reachable_state_count": len(reachable),
        "reachable_from_start": len(reachable) == len(valid_states),
        "action_count": surface.ACTION_COUNT,
        "transition_row_count": len(transitions),
        "valid_nonself_edge_count": sum(
            1
            for record in transitions
            if record.valid_transition and record.next_state_id != record.source_state_id
        ),
        "invalid_move_count": sum(1 for record in transitions if record.invalid_move),
        "valid_self_transition_count": sum(
            1 for record in transitions if record.valid_self_transition
        ),
        "self_loop_transition_count": sum(
            1 for record in transitions if record.next_state_id == record.source_state_id
        ),
        "start_state_id": state_id(surface.START_STATE),
        "goal_state_id": state_id(surface.CANDIDATE_GOAL_STATE),
        "start_valid": bool(surface.is_valid_state(surface.START_STATE)),
        "goal_valid": bool(surface.is_valid_state(surface.CANDIDATE_GOAL_STATE)),
        "goal_one_step_from_start": _goal_one_step_from_start(surface),
        "shortest_path_length": max(0, len(shortest_path) - 1) if shortest_path else None,
        "outgoing_nonself_min": min(
            row["valid_nonself_outgoing_count"] for row in per_state_counts
        ),
        "outgoing_nonself_max": max(
            row["valid_nonself_outgoing_count"] for row in per_state_counts
        ),
        "outgoing_nonself_mean": _mean(
            row["valid_nonself_outgoing_count"] for row in per_state_counts
        ),
        "invalid_action_mean": _mean(row["invalid_action_count"] for row in per_state_counts),
        "self_transition_mean": _mean(
            row["self_loop_transition_count"] for row in per_state_counts
        ),
    }
    return PlateSupportGraphDiagnostics(
        graph_summary=graph_summary,
        transition_records=transitions,
        shortest_path_records=tuple(shortest_path),
        outgoing_action_count_summary=tuple(
            _count_summary_rows(
                row["valid_nonself_outgoing_count"] for row in per_state_counts
            )
        ),
        invalid_action_summary=tuple(
            _count_summary_rows(row["invalid_action_count"] for row in per_state_counts)
        ),
        self_transition_summary=tuple(
            _self_transition_rows(per_state_counts)
        ),
    )


def _transition_record(
    *,
    surface: ImportedPlateSupportSurface,
    source_state: Any,
    action_index: int,
) -> TransitionRecord:
    result = surface.primitive_transition(source_state, action_index)
    next_state = result.next_state
    return TransitionRecord(
        source_state_id=state_id(source_state),
        action_index=action_index,
        action_label=action_label(action_index),
        candidate_state_id=state_id(result.candidate_state),
        next_state_id=state_id(next_state),
        candidate_valid=bool(result.candidate_valid),
        valid_transition=bool(result.valid_transition),
        invalid_move=bool(result.invalid_move),
        valid_self_transition=bool(result.valid_self_transition),
        reward=float(surface.transition_reward(source_state, action_index, next_state)),
        terminated=bool(surface.transition_terminated(next_state)),
        truncated_at_one_step=bool(
            surface.transition_truncated(1, surface.transition_terminated(next_state))
        ),
    )


def _adjacency_by_state(
    valid_states: tuple[Any, ...],
    transitions: tuple[TransitionRecord, ...],
) -> dict[str, tuple[TransitionRecord, ...]]:
    by_source: dict[str, list[TransitionRecord]] = {state_id(state): [] for state in valid_states}
    for record in transitions:
        if record.valid_transition and record.next_state_id != record.source_state_id:
            by_source[record.source_state_id].append(record)
    return {key: tuple(value) for key, value in by_source.items()}


def _reachable_state_ids(
    start_id: str,
    adjacency: dict[str, tuple[TransitionRecord, ...]],
) -> set[str]:
    seen = {start_id}
    queue: deque[str] = deque([start_id])
    while queue:
        current = queue.popleft()
        for record in adjacency.get(current, ()):
            if record.next_state_id not in seen:
                seen.add(record.next_state_id)
                queue.append(record.next_state_id)
    return seen


def _shortest_path_records(
    *,
    surface: ImportedPlateSupportSurface,
    adjacency: dict[str, tuple[TransitionRecord, ...]],
) -> list[ShortestPathRecord]:
    start = state_id(surface.START_STATE)
    goal = state_id(surface.CANDIDATE_GOAL_STATE)
    parents: dict[str, tuple[str, TransitionRecord] | None] = {start: None}
    queue: deque[str] = deque([start])
    while queue and goal not in parents:
        current = queue.popleft()
        for record in adjacency.get(current, ()):
            if record.next_state_id not in parents:
                parents[record.next_state_id] = (current, record)
                queue.append(record.next_state_id)
    if goal not in parents:
        return ()
    path_edges: list[TransitionRecord] = []
    current = goal
    while parents[current] is not None:
        previous, edge = parents[current]
        path_edges.append(edge)
        current = previous
    path_edges.reverse()
    records: list[ShortestPathRecord] = []
    current_state_id = start
    for index, edge in enumerate(path_edges):
        records.append(
            ShortestPathRecord(
                step_index=index,
                state_id=current_state_id,
                action_index=edge.action_index,
                action_label=edge.action_label,
                next_state_id=edge.next_state_id,
                reward=edge.reward,
            )
        )
        current_state_id = edge.next_state_id
    records.append(
        ShortestPathRecord(
            step_index=len(path_edges),
            state_id=goal,
            action_index=None,
            action_label="terminal",
            next_state_id=goal,
            reward=None,
        )
    )
    return records


def _per_state_counts(
    valid_states: tuple[Any, ...],
    transitions: tuple[TransitionRecord, ...],
) -> list[dict[str, object]]:
    by_source: dict[str, list[TransitionRecord]] = {state_id(state): [] for state in valid_states}
    for record in transitions:
        by_source[record.source_state_id].append(record)
    rows: list[dict[str, object]] = []
    for source_id, records in by_source.items():
        invalid_count = sum(1 for record in records if record.invalid_move)
        valid_self_count = sum(1 for record in records if record.valid_self_transition)
        self_count = sum(1 for record in records if record.next_state_id == source_id)
        nonself_count = sum(
            1
            for record in records
            if record.valid_transition and record.next_state_id != source_id
        )
        rows.append(
            {
                "state_id": source_id,
                "invalid_action_count": invalid_count,
                "valid_self_transition_count": valid_self_count,
                "self_loop_transition_count": self_count,
                "valid_nonself_outgoing_count": nonself_count,
            }
        )
    return rows


def _count_summary_rows(counts: Any) -> list[dict[str, object]]:
    counter = Counter(counts)
    total = sum(counter.values())
    rows: list[dict[str, object]] = []
    for count_value in sorted(counter):
        state_count = int(counter[count_value])
        rows.append(
            {
                "count_value": int(count_value),
                "state_count": state_count,
                "share": 0.0 if total == 0 else state_count / total,
            }
        )
    return rows


def _self_transition_rows(per_state_counts: list[dict[str, object]]) -> list[dict[str, object]]:
    counter = Counter(
        (
            row["valid_self_transition_count"],
            row["invalid_action_count"],
            row["self_loop_transition_count"],
        )
        for row in per_state_counts
    )
    total = sum(counter.values())
    rows: list[dict[str, object]] = []
    for (valid_self_count, invalid_count, self_count), state_count in sorted(counter.items()):
        rows.append(
            {
                "valid_self_transition_count": valid_self_count,
                "invalid_self_loop_count": invalid_count,
                "total_self_transition_count": self_count,
                "state_count": state_count,
                "share": 0.0 if total == 0 else state_count / total,
            }
        )
    return rows


def _goal_one_step_from_start(surface: ImportedPlateSupportSurface) -> bool:
    goal = state_id(surface.CANDIDATE_GOAL_STATE)
    return any(
        state_id(next_state) == goal
        for _, next_state in surface.valid_outgoing_transitions(surface.START_STATE)
    )


def _mean(values: Any) -> float:
    values = list(values)
    if not values:
        return 0.0
    return sum(float(value) for value in values) / len(values)
