"""One-step tower-star action surfaces for PlateSupport."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .config import INVALID_GUARD, NONSELF_GUARD, RAW_GUARD


@dataclass(frozen=True)
class TransitionClassification:
    """Local one-step classification for a primitive PlateSupport action."""

    action_index: int
    source_state_id: str
    next_state_id: str
    invalid_move: bool
    self_loop: bool
    valid_clipped_self_loop: bool
    nonself_transition: bool


@dataclass(frozen=True)
class GuardSummary:
    """Action counts exposed by one direct guard at one state."""

    guard_type: str
    available_action_count_before_guard: int
    available_action_count_after_guard: int
    guarded_action_count: int
    invalid_guard_filtered_count: int
    self_loop_guard_filtered_count: int
    all_actions_filtered_count: int
    available_actions: tuple[int, ...]


VALID_GUARD_TYPES = (RAW_GUARD, INVALID_GUARD, NONSELF_GUARD)


def classify_primitive_transition(
    surface: Any,
    state: Any,
    action: int,
) -> TransitionClassification:
    """Classify one primitive action without using reward or lookahead."""

    domain_state = _domain_state(state)
    transition = surface.primitive_transition(domain_state, int(action))
    next_state = transition.next_state
    invalid_move = bool(getattr(transition, "invalid_move", False))
    self_loop = next_state == domain_state
    return TransitionClassification(
        action_index=int(action),
        source_state_id=_state_text(domain_state),
        next_state_id=_state_text(next_state),
        invalid_move=invalid_move,
        self_loop=self_loop,
        valid_clipped_self_loop=self_loop and not invalid_move,
        nonself_transition=not self_loop,
    )


def available_direct_actions(
    surface: Any,
    state: Any,
    guard_type: str,
) -> tuple[int, ...]:
    """Return the direct primitive actions offered by a guard."""

    return summarize_guard(surface, state, guard_type).available_actions


def summarize_guard(surface: Any, state: Any, guard_type: str) -> GuardSummary:
    """Summarize guard filtering at one concrete state."""

    if guard_type not in VALID_GUARD_TYPES:
        raise ValueError(f"unknown guard_type: {guard_type!r}")
    classifications = tuple(
        classify_primitive_transition(surface, state, action)
        for action in range(int(surface.ACTION_COUNT))
    )
    if guard_type == RAW_GUARD:
        available = tuple(classification.action_index for classification in classifications)
    elif guard_type == INVALID_GUARD:
        available = tuple(
            classification.action_index
            for classification in classifications
            if not classification.invalid_move
        )
    else:
        available = tuple(
            classification.action_index
            for classification in classifications
            if not classification.self_loop
        )
    invalid_filtered = sum(classification.invalid_move for classification in classifications)
    self_filtered = sum(classification.self_loop for classification in classifications)
    return GuardSummary(
        guard_type=guard_type,
        available_action_count_before_guard=len(classifications),
        available_action_count_after_guard=len(available),
        guarded_action_count=len(available),
        invalid_guard_filtered_count=invalid_filtered if guard_type != RAW_GUARD else 0,
        self_loop_guard_filtered_count=self_filtered if guard_type == NONSELF_GUARD else 0,
        all_actions_filtered_count=1 if not available else 0,
        available_actions=available,
    )


def _domain_state(state: Any) -> Any:
    return getattr(state, "payload", state)


def _state_text(state: Any) -> str:
    return repr(_domain_state(state))

