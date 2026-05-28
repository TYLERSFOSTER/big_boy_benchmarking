"""Edge labels for counterpoint hidden-graph transitions."""

from __future__ import annotations

from typing import Any

from big_boy_benchmarking.environments.counterpoint.actions import CounterpointAction
from big_boy_benchmarking.environments.counterpoint.legality import LegalityResult
from big_boy_benchmarking.environments.counterpoint.specs import (
    CounterpointInstanceSpec,
    interval_class,
)
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState


def movement_class(delta: int) -> str:
    if delta <= -3:
        return "down_leap"
    if delta < 0:
        return "down_step"
    if delta == 0:
        return "stationary"
    if delta <= 2:
        return "up_step"
    return "up_leap"


def _direction(delta: int) -> str:
    if delta < 0:
        return "down"
    if delta > 0:
        return "up"
    return "stay"


def _adjacent_interval_classes(pitches: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        interval_class(lower, upper) for lower, upper in zip(pitches, pitches[1:], strict=False)
    )


def _span_bucket(span: int, max_outer_span: int) -> str:
    if span <= max(1, max_outer_span // 3):
        return "compact"
    if span <= max(2, (2 * max_outer_span) // 3):
        return "medium"
    return "wide"


def emit_edge_labels(
    spec: CounterpointInstanceSpec,
    state: CounterpointState,
    action: CounterpointAction,
    next_state: CounterpointState,
    legality_result: LegalityResult,
    *,
    terminal: bool = False,
) -> dict[str, Any]:
    before_adjacent = _adjacent_interval_classes(state.pitches)
    after_adjacent = _adjacent_interval_classes(next_state.pitches)
    before_outer = interval_class(state.pitches[0], state.pitches[-1])
    after_outer = interval_class(next_state.pitches[0], next_state.pitches[-1])
    before_root = (state.pitches[0] - spec.tonic_pitch_class) % 12
    after_root = (next_state.pitches[0] - spec.tonic_pitch_class) % 12
    movement_classes = tuple(movement_class(delta) for delta in action.deltas)
    return {
        "beat_phase_before": state.beat_index,
        "beat_phase_after": next_state.beat_index,
        "per_voice_delta": action.deltas,
        "per_voice_movement_class": movement_classes,
        "global_motion_direction_pattern": tuple(_direction(delta) for delta in action.deltas),
        "adjacent_interval_classes_before": before_adjacent,
        "adjacent_interval_classes_after": after_adjacent,
        "outer_interval_class_before": before_outer,
        "outer_interval_class_after": after_outer,
        "interval_change_classes": tuple(
            (after - before) % 12
            for before, after in zip(before_adjacent, after_adjacent, strict=False)
        ),
        "root_interval_class_before": before_root,
        "root_interval_class_after": after_root,
        "forbidden_parallel_check_result": (
            "fail"
            if any(
                reason.startswith("forbidden_parallel")
                for reason in legality_result.failure_reasons
            )
            else "pass"
        ),
        "max_span_bucket": _span_bucket(
            next_state.pitches[-1] - next_state.pitches[0],
            spec.max_outer_span,
        ),
        "terminal_candidate_marker": terminal,
    }
