"""Human-scale graph statistics for the BBB PlateSupport environment."""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from collections.abc import Iterable
from typing import Any

from big_boy_benchmarking.environments.plate_support.graph import (
    PlateSupportGraphDiagnostics,
    build_plate_support_graph_diagnostics,
)
from big_boy_benchmarking.environments.plate_support.upstream import (
    ImportedPlateSupportSurface,
)


def summarize_plate_support_graph(
    *,
    surface: ImportedPlateSupportSurface | None = None,
    diagnostics: PlateSupportGraphDiagnostics | None = None,
) -> dict[str, object]:
    """Return exact graph statistics for the current PlateSupport instance."""

    diagnostics = diagnostics or build_plate_support_graph_diagnostics(surface=surface)
    graph_summary = diagnostics.graph_summary
    transition_records = diagnostics.transition_records
    state_ids = tuple(sorted({record.source_state_id for record in transition_records}))
    valid_nonself_edges = tuple(
        record
        for record in transition_records
        if record.valid_transition and record.next_state_id != record.source_state_id
    )
    valid_self_edges = tuple(record for record in transition_records if record.valid_self_transition)
    invalid_edges = tuple(record for record in transition_records if record.invalid_move)
    terminal_state_ids = tuple(
        sorted({record.next_state_id for record in transition_records if record.terminated})
    )

    out_neighbors: dict[str, set[str]] = {state_id: set() for state_id in state_ids}
    in_neighbors: dict[str, set[str]] = {state_id: set() for state_id in state_ids}
    weak_neighbors: dict[str, set[str]] = {state_id: set() for state_id in state_ids}
    for record in valid_nonself_edges:
        out_neighbors.setdefault(record.source_state_id, set()).add(record.next_state_id)
        in_neighbors.setdefault(record.next_state_id, set()).add(record.source_state_id)
        weak_neighbors.setdefault(record.source_state_id, set()).add(record.next_state_id)
        weak_neighbors.setdefault(record.next_state_id, set()).add(record.source_state_id)

    out_degree = {state_id: len(out_neighbors.get(state_id, ())) for state_id in state_ids}
    in_degree = {state_id: len(in_neighbors.get(state_id, ())) for state_id in state_ids}
    weak_component_sizes = _weak_component_sizes(state_ids, weak_neighbors)
    strongly_connected_component_sizes = _strong_component_sizes(state_ids, out_neighbors)
    start_state_id = str(graph_summary["start_state_id"])
    goal_state_id = str(graph_summary["goal_state_id"])
    reachable_from_start = _reachable_count(start_state_id, out_neighbors)
    can_reach_goal = _reachable_count(goal_state_id, in_neighbors)
    state_count = len(state_ids)
    possible_directed_nonself_edges = state_count * max(0, state_count - 1)
    action_count = int(graph_summary["action_count"])
    transition_row_count = len(transition_records)

    return {
        "status": "ok",
        "environment_instance_id": graph_summary["environment_instance_id"],
        "state_space": {
            "ambient_candidate_state_count": graph_summary["candidate_state_count"],
            "valid_state_count": graph_summary["valid_state_count"],
            "reachable_state_count": graph_summary["reachable_state_count"],
            "reachable_from_start": graph_summary["reachable_from_start"],
            "terminal_state_count": len(terminal_state_ids),
            "terminal_state_ids": terminal_state_ids,
            "start_state_id": start_state_id,
            "goal_state_id": goal_state_id,
        },
        "transition_space": {
            "action_count": action_count,
            "transition_row_count": transition_row_count,
            "valid_nonself_edge_count": len(valid_nonself_edges),
            "valid_self_transition_count": len(valid_self_edges),
            "invalid_move_count": len(invalid_edges),
            "valid_action_row_count": len(valid_nonself_edges) + len(valid_self_edges),
            "valid_nonself_edge_density": _safe_ratio(
                len(valid_nonself_edges),
                possible_directed_nonself_edges,
            ),
            "valid_action_row_density": _safe_ratio(
                len(valid_nonself_edges) + len(valid_self_edges),
                transition_row_count,
            ),
            "invalid_move_density": _safe_ratio(len(invalid_edges), transition_row_count),
            "valid_self_transition_density": _safe_ratio(
                len(valid_self_edges),
                transition_row_count,
            ),
        },
        "degree": {
            "out_degree": _degree_summary(out_degree.values()),
            "in_degree": _degree_summary(in_degree.values()),
            "dead_end_state_count": sum(1 for value in out_degree.values() if value == 0),
            "source_like_state_count": sum(1 for value in in_degree.values() if value == 0),
        },
        "connectivity": {
            "directed_reachable_from_start_count": reachable_from_start,
            "can_reach_goal_count": can_reach_goal,
            "weak_component_count": len(weak_component_sizes),
            "weak_component_sizes": weak_component_sizes,
            "strongly_connected_component_count": len(strongly_connected_component_sizes),
            "strongly_connected_component_sizes": strongly_connected_component_sizes,
            "largest_weak_component_share": _largest_share(weak_component_sizes, state_count),
            "largest_strong_component_share": _largest_share(
                strongly_connected_component_sizes,
                state_count,
            ),
        },
        "task_anchor": {
            "goal_one_step_from_start": graph_summary["goal_one_step_from_start"],
            "shortest_path_length": graph_summary["shortest_path_length"],
            "shortest_path_record_count": len(diagnostics.shortest_path_records),
        },
    }


def _degree_summary(values: Iterable[int]) -> dict[str, object]:
    values = tuple(int(value) for value in values)
    histogram = Counter(values)
    return {
        "min": min(values) if values else 0,
        "max": max(values) if values else 0,
        "mean": _mean(values),
        "histogram": [
            {"degree": degree, "state_count": state_count}
            for degree, state_count in sorted(histogram.items())
        ],
    }


def _weak_component_sizes(
    state_ids: tuple[str, ...],
    weak_neighbors: dict[str, set[str]],
) -> list[int]:
    seen: set[str] = set()
    sizes: list[int] = []
    for state_id in state_ids:
        if state_id in seen:
            continue
        queue: deque[str] = deque([state_id])
        seen.add(state_id)
        size = 0
        while queue:
            current = queue.popleft()
            size += 1
            for neighbor in weak_neighbors.get(current, ()):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def _strong_component_sizes(
    state_ids: tuple[str, ...],
    out_neighbors: dict[str, set[str]],
) -> list[int]:
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    component_sizes: list[int] = []

    def visit(state_id: str) -> None:
        nonlocal index
        indices[state_id] = index
        lowlinks[state_id] = index
        index += 1
        stack.append(state_id)
        on_stack.add(state_id)
        for neighbor in out_neighbors.get(state_id, ()):
            if neighbor not in indices:
                visit(neighbor)
                lowlinks[state_id] = min(lowlinks[state_id], lowlinks[neighbor])
            elif neighbor in on_stack:
                lowlinks[state_id] = min(lowlinks[state_id], indices[neighbor])
        if lowlinks[state_id] != indices[state_id]:
            return
        size = 0
        while True:
            member = stack.pop()
            on_stack.remove(member)
            size += 1
            if member == state_id:
                break
        component_sizes.append(size)

    for state_id in state_ids:
        if state_id not in indices:
            visit(state_id)
    return sorted(component_sizes, reverse=True)


def _reachable_count(start_state_id: str, neighbors: dict[str, set[str]]) -> int:
    seen = {start_state_id}
    queue: deque[str] = deque([start_state_id])
    while queue:
        current = queue.popleft()
        for neighbor in neighbors.get(current, ()):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen)


def _largest_share(component_sizes: list[int], state_count: int) -> float:
    if not component_sizes or state_count == 0:
        return 0.0
    return max(component_sizes) / state_count


def _safe_ratio(numerator: int, denominator: int) -> float:
    return 0.0 if denominator == 0 else numerator / denominator


def _mean(values: Iterable[int]) -> float:
    values = tuple(values)
    if not values:
        return 0.0
    return sum(float(value) for value in values) / len(values)
