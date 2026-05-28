"""Deterministic counterpoint fixture constructors."""

from __future__ import annotations

from itertools import combinations

from big_boy_benchmarking.environments.counterpoint.legality import validate_node_legality
from big_boy_benchmarking.environments.counterpoint.specs import (
    CounterpointInstanceSpec,
    make_instance_spec,
)
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState

TINY_INSTANCE_ID = "counterpoint_symbolic_n3_tiny_v001"
SMALL_INSTANCE_ID = "counterpoint_symbolic_n3_small_v001"


def tiny_candidate_specs() -> tuple[CounterpointInstanceSpec, ...]:
    return (
        make_instance_spec(
            environment_instance_id=TINY_INSTANCE_ID,
            voice_count=3,
            pitch_min=60,
            pitch_max=67,
            measure_size=4,
            horizon_steps=4,
            max_step_size=2,
            max_outer_span=8,
        ),
        make_instance_spec(
            environment_instance_id="counterpoint_symbolic_n3_tiny_compact_v001",
            voice_count=3,
            pitch_min=60,
            pitch_max=66,
            measure_size=4,
            horizon_steps=4,
            max_step_size=1,
            max_outer_span=7,
        ),
    )


def small_candidate_specs() -> tuple[CounterpointInstanceSpec, ...]:
    return (
        make_instance_spec(
            environment_instance_id=SMALL_INSTANCE_ID,
            voice_count=3,
            pitch_min=60,
            pitch_max=72,
            measure_size=4,
            horizon_steps=8,
            max_step_size=2,
            max_outer_span=12,
        ),
        make_instance_spec(
            environment_instance_id="counterpoint_symbolic_n3_small_wide_v001",
            voice_count=3,
            pitch_min=58,
            pitch_max=72,
            measure_size=4,
            horizon_steps=8,
            max_step_size=2,
            max_outer_span=14,
        ),
    )


def default_tiny_spec() -> CounterpointInstanceSpec:
    return tiny_candidate_specs()[0]


def default_small_spec() -> CounterpointInstanceSpec:
    return small_candidate_specs()[0]


def candidate_initial_states(spec: CounterpointInstanceSpec) -> tuple[CounterpointState, ...]:
    """Return deterministic legal beat-zero states sorted by compact tonic proximity."""

    legal_states: list[CounterpointState] = []
    for pitches in combinations(range(spec.pitch_min, spec.pitch_max + 1), spec.voice_count):
        state = CounterpointState(tuple(pitches), 0)
        if validate_node_legality(spec, state).is_legal:
            legal_states.append(state)

    center = spec.pitch_min + (spec.pitch_max - spec.pitch_min) / 2

    def sort_key(state: CounterpointState) -> tuple[float, int, tuple[int, ...]]:
        tonic_distance = abs((state.pitches[0] - spec.tonic_pitch_class) % 12)
        center_distance = sum(abs(pitch - center) for pitch in state.pitches)
        span = state.pitches[-1] - state.pitches[0]
        return (tonic_distance + center_distance, span, state.pitches)

    return tuple(sorted(legal_states, key=sort_key))


def initial_states(spec: CounterpointInstanceSpec) -> tuple[CounterpointState, ...]:
    """Active v001 initial-state policy: first four legal compact states."""

    return candidate_initial_states(spec)[:4]
