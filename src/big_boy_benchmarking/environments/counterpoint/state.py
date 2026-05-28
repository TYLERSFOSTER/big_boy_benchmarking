"""State contract for counterpoint hidden graphs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from big_boy_benchmarking.environments.counterpoint.specs import (
    CounterpointInstanceSpec,
    interval_class,
)


@dataclass(frozen=True)
class CounterpointState:
    """Finite graph state: ordered voice pitches plus beat phase."""

    pitches: tuple[int, ...]
    beat_index: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_iterable(
        cls,
        pitches: tuple[int, ...] | list[int],
        beat_index: int,
    ) -> CounterpointState:
        return cls(pitches=tuple(pitches), beat_index=beat_index)


def validate_state(spec: CounterpointInstanceSpec, state: CounterpointState) -> None:
    if len(state.pitches) != spec.voice_count:
        raise ValueError("pitches must have voice_count entries")
    if state.beat_index < 0 or state.beat_index >= spec.measure_size:
        raise ValueError("beat_index must be in 0..measure_size-1")
    for pitch in state.pitches:
        if pitch < spec.pitch_min or pitch > spec.pitch_max:
            raise ValueError("pitches must lie inside pitch_min..pitch_max")
    if spec.require_strict_voice_order:
        for lower, upper in zip(state.pitches, state.pitches[1:], strict=False):
            if lower >= upper:
                raise ValueError("pitches must be strictly ordered")
    for lower, upper in zip(state.pitches, state.pitches[1:], strict=False):
        if interval_class(lower, upper) not in spec.allowed_adjacent_interval_classes:
            raise ValueError("adjacent interval class is not allowed")
    if (
        interval_class(state.pitches[0], state.pitches[-1])
        not in spec.allowed_outer_interval_classes
    ):
        raise ValueError("outer interval class is not allowed")
    if state.pitches[-1] - state.pitches[0] > spec.max_outer_span:
        raise ValueError("outer span exceeds max_outer_span")
    if spec.allowed_root_interval_classes:
        root_ic = (state.pitches[0] - spec.tonic_pitch_class) % 12
        if root_ic not in spec.allowed_root_interval_classes:
            raise ValueError("root interval class is not allowed")
