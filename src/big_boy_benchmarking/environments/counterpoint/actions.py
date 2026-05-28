"""Action contract and deterministic raw action enumeration."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import product
from typing import Any

from big_boy_benchmarking.environments.counterpoint.specs import CounterpointInstanceSpec


@dataclass(frozen=True)
class CounterpointAction:
    """One simultaneous pitch delta per voice."""

    deltas: tuple[int, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_iterable(cls, deltas: tuple[int, ...] | list[int]) -> CounterpointAction:
        return cls(deltas=tuple(deltas))


def validate_action(spec: CounterpointInstanceSpec, action: CounterpointAction) -> None:
    if len(action.deltas) != spec.voice_count:
        raise ValueError("deltas must have voice_count entries")
    for delta in action.deltas:
        if delta < -spec.max_step_size or delta > spec.max_step_size:
            raise ValueError("delta exceeds max_step_size")
        if not spec.allow_stationary_voice and delta == 0:
            raise ValueError("stationary voice is not allowed")


def enumerate_raw_actions(spec: CounterpointInstanceSpec) -> tuple[CounterpointAction, ...]:
    """Return stable lexicographic action lattice for the active spec."""

    delta_values = range(-spec.max_step_size, spec.max_step_size + 1)
    actions = [
        CounterpointAction(tuple(deltas))
        for deltas in product(delta_values, repeat=spec.voice_count)
        if spec.allow_stationary_voice or all(delta != 0 for delta in deltas)
    ]
    return tuple(actions)
