"""Versioned node and edge legality for counterpoint hidden graphs."""

from __future__ import annotations

from dataclasses import dataclass

from big_boy_benchmarking.environments.counterpoint.actions import CounterpointAction
from big_boy_benchmarking.environments.counterpoint.specs import (
    CounterpointInstanceSpec,
    interval_class,
)
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState


@dataclass(frozen=True)
class LegalityResult:
    """Structured legality result with stable diagnostic reasons."""

    is_legal: bool
    failure_reasons: tuple[str, ...] = ()

    def require_legal(self) -> None:
        if not self.is_legal:
            raise ValueError("; ".join(self.failure_reasons))


def validate_node_legality(
    spec: CounterpointInstanceSpec,
    state: CounterpointState,
) -> LegalityResult:
    reasons: list[str] = []
    if len(state.pitches) != spec.voice_count:
        reasons.append("voice_count_mismatch")
    if state.beat_index < 0 or state.beat_index >= spec.measure_size:
        reasons.append("beat_index_out_of_range")
    for pitch in state.pitches:
        if pitch < spec.pitch_min or pitch > spec.pitch_max:
            reasons.append("pitch_band_violation")
            break
    if spec.require_strict_voice_order:
        for lower, upper in zip(state.pitches, state.pitches[1:], strict=False):
            if lower >= upper:
                reasons.append("strict_voice_order_violation")
                break
    if len(state.pitches) >= 2:
        for lower, upper in zip(state.pitches, state.pitches[1:], strict=False):
            if interval_class(lower, upper) not in spec.allowed_adjacent_interval_classes:
                reasons.append("adjacent_interval_class_violation")
                break
        if interval_class(state.pitches[0], state.pitches[-1]) not in (
            spec.allowed_outer_interval_classes
        ):
            reasons.append("outer_interval_class_violation")
        if state.pitches[-1] - state.pitches[0] > spec.max_outer_span:
            reasons.append("max_outer_span_violation")
        if spec.allowed_root_interval_classes:
            root_ic = (state.pitches[0] - spec.tonic_pitch_class) % 12
            if root_ic not in spec.allowed_root_interval_classes:
                reasons.append("root_interval_class_violation")
    return LegalityResult(is_legal=not reasons, failure_reasons=tuple(reasons))


def _parallel_interval_failures(
    spec: CounterpointInstanceSpec,
    state: CounterpointState,
    action: CounterpointAction,
    candidate_state: CounterpointState,
) -> tuple[str, ...]:
    failures: list[str] = []
    pairs = list(zip(range(spec.voice_count - 1), range(1, spec.voice_count), strict=False))
    pairs.append((0, spec.voice_count - 1))
    for lower_index, upper_index in pairs:
        before = interval_class(state.pitches[lower_index], state.pitches[upper_index])
        after = interval_class(
            candidate_state.pitches[lower_index],
            candidate_state.pitches[upper_index],
        )
        lower_delta = action.deltas[lower_index]
        upper_delta = action.deltas[upper_index]
        same_motion = lower_delta != 0 and upper_delta != 0 and (
            lower_delta > 0
        ) == (upper_delta > 0)
        if before == after and after in spec.forbidden_parallel_interval_classes and same_motion:
            failures.append(f"forbidden_parallel_interval_class_{after}")
    return tuple(failures)


def validate_edge_legality(
    spec: CounterpointInstanceSpec,
    state: CounterpointState,
    action: CounterpointAction,
    candidate_state: CounterpointState,
) -> LegalityResult:
    reasons: list[str] = []
    if len(action.deltas) != spec.voice_count:
        reasons.append("action_voice_count_mismatch")
    for delta in action.deltas:
        if delta < -spec.max_step_size or delta > spec.max_step_size:
            reasons.append("action_delta_bound_violation")
            break
        if not spec.allow_stationary_voice and delta == 0:
            reasons.append("stationary_voice_violation")
            break

    node_result = validate_node_legality(spec, candidate_state)
    reasons.extend(f"candidate_{reason}" for reason in node_result.failure_reasons)
    reasons.extend(_parallel_interval_failures(spec, state, action, candidate_state))
    return LegalityResult(is_legal=not reasons, failure_reasons=tuple(reasons))
