"""Legal action masks and mask-density diagnostics."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from big_boy_benchmarking.environments.counterpoint.actions import (
    CounterpointAction,
    enumerate_raw_actions,
)
from big_boy_benchmarking.environments.counterpoint.legality import validate_edge_legality
from big_boy_benchmarking.environments.counterpoint.specs import CounterpointInstanceSpec
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState
from big_boy_benchmarking.environments.counterpoint.transition import construct_next_state


@dataclass(frozen=True)
class ActionMask:
    raw_actions: tuple[CounterpointAction, ...]
    mask: tuple[bool, ...]

    def legal_actions(self) -> tuple[CounterpointAction, ...]:
        return tuple(
            action
            for action, is_legal in zip(self.raw_actions, self.mask, strict=True)
            if is_legal
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "raw_actions": [action.to_dict() for action in self.raw_actions],
            "mask": self.mask,
        }


@dataclass(frozen=True)
class MaskDensityDiagnostics:
    raw_action_count: int
    legal_action_count: int
    mask_density: float
    dead_end: bool
    single_action: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def legal_action_mask(spec: CounterpointInstanceSpec, state: CounterpointState) -> ActionMask:
    raw_actions = enumerate_raw_actions(spec)
    mask = []
    for action in raw_actions:
        candidate = construct_next_state(spec, state, action)
        mask.append(validate_edge_legality(spec, state, action, candidate).is_legal)
    return ActionMask(raw_actions=raw_actions, mask=tuple(mask))


def mask_density_diagnostics(mask: ActionMask) -> MaskDensityDiagnostics:
    raw_count = len(mask.raw_actions)
    legal_count = sum(1 for is_legal in mask.mask if is_legal)
    density = legal_count / raw_count if raw_count else 0.0
    return MaskDensityDiagnostics(
        raw_action_count=raw_count,
        legal_action_count=legal_count,
        mask_density=density,
        dead_end=legal_count == 0,
        single_action=legal_count == 1,
    )
