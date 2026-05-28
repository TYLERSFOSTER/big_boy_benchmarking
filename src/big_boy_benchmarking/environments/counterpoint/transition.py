"""Deterministic transition construction and evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from big_boy_benchmarking.environments.counterpoint.actions import CounterpointAction
from big_boy_benchmarking.environments.counterpoint.labels import emit_edge_labels
from big_boy_benchmarking.environments.counterpoint.legality import (
    LegalityResult,
    validate_edge_legality,
)
from big_boy_benchmarking.environments.counterpoint.rewards import (
    RewardResult,
    evaluate_reward,
)
from big_boy_benchmarking.environments.counterpoint.specs import CounterpointInstanceSpec
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState


@dataclass(frozen=True)
class TransitionResult:
    state: CounterpointState
    action: CounterpointAction
    next_state: CounterpointState
    legality: LegalityResult
    reward: RewardResult | None
    labels: dict[str, Any]
    terminated: bool
    truncated: bool


def construct_next_state(
    spec: CounterpointInstanceSpec,
    state: CounterpointState,
    action: CounterpointAction,
) -> CounterpointState:
    return CounterpointState(
        pitches=tuple(
            pitch + delta for pitch, delta in zip(state.pitches, action.deltas, strict=False)
        ),
        beat_index=(state.beat_index + 1) % spec.measure_size,
    )


def evaluate_transition(
    spec: CounterpointInstanceSpec,
    state: CounterpointState,
    action: CounterpointAction,
    *,
    step_index: int = 0,
) -> TransitionResult:
    next_state = construct_next_state(spec, state, action)
    legality = validate_edge_legality(spec, state, action, next_state)
    terminated = step_index + 1 >= spec.horizon_steps
    reward = (
        evaluate_reward(spec, state, action, next_state, legality, terminated=terminated)
        if legality.is_legal
        else None
    )
    labels = emit_edge_labels(spec, state, action, next_state, legality, terminal=terminated)
    return TransitionResult(
        state=state,
        action=action,
        next_state=next_state,
        legality=legality,
        reward=reward,
        labels=labels,
        terminated=terminated if legality.is_legal else False,
        truncated=False,
    )
