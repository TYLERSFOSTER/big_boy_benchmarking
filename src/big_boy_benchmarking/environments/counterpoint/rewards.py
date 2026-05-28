"""Local reward bundle v001 for counterpoint hidden graphs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from big_boy_benchmarking.environments.counterpoint.actions import CounterpointAction
from big_boy_benchmarking.environments.counterpoint.legality import LegalityResult
from big_boy_benchmarking.environments.counterpoint.specs import (
    CounterpointInstanceSpec,
    interval_class,
)
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState


@dataclass(frozen=True)
class RewardTermSpec:
    reward_term_id: str
    reward_term_version: str
    weight: float
    enabled: bool
    input_scope: tuple[str, ...]
    locality_class: str
    output_range: tuple[float, float]
    diagnostic_fields: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RewardTermDiagnostic:
    reward_term_id: str
    raw_value: float
    weighted_value: float
    diagnostic_fields: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RewardResult:
    reward_bundle_id: str
    total_reward: float
    terms: tuple[RewardTermDiagnostic, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


REWARD_TERM_SPECS = (
    RewardTermSpec(
        "valid_transition_bonus",
        "v001",
        1.0,
        True,
        ("state", "action", "next_state"),
        "action_local",
        (0.0, 1.0),
        ("is_legal",),
    ),
    RewardTermSpec(
        "adjacent_interval_preference",
        "v001",
        0.4,
        True,
        ("next_state", "instance_parameters"),
        "action_local",
        (0.0, 1.0),
        ("allowed_adjacent_fraction",),
    ),
    RewardTermSpec(
        "outer_interval_preference",
        "v001",
        0.3,
        True,
        ("next_state", "instance_parameters"),
        "action_local",
        (0.0, 1.0),
        ("outer_interval_class",),
    ),
    RewardTermSpec(
        "movement_size_preference",
        "v001",
        0.35,
        True,
        ("action", "instance_parameters"),
        "action_local",
        (-1.0, 0.0),
        ("mean_abs_delta",),
    ),
    RewardTermSpec(
        "motion_shape_preference",
        "v001",
        0.2,
        True,
        ("action",),
        "action_local",
        (-1.0, 1.0),
        ("direction_pattern",),
    ),
    RewardTermSpec(
        "range_comfort_penalty",
        "v001",
        0.2,
        True,
        ("next_state", "instance_parameters"),
        "action_local",
        (-1.0, 0.0),
        ("mean_center_distance",),
    ),
    RewardTermSpec(
        "beat_phase_local_preference",
        "v001",
        0.1,
        True,
        ("next_state", "beat_index"),
        "action_local",
        (0.0, 1.0),
        ("beat_index",),
    ),
    RewardTermSpec(
        "terminal_completion_bonus",
        "v001",
        1.0,
        True,
        ("terminal_flag",),
        "action_local",
        (0.0, 1.0),
        ("terminated",),
    ),
)


def reward_term_specs() -> tuple[RewardTermSpec, ...]:
    return REWARD_TERM_SPECS


def _weighted(term_id: str, raw_value: float, fields: dict[str, Any]) -> RewardTermDiagnostic:
    spec = next(term_spec for term_spec in REWARD_TERM_SPECS if term_spec.reward_term_id == term_id)
    return RewardTermDiagnostic(
        reward_term_id=term_id,
        raw_value=raw_value,
        weighted_value=raw_value * spec.weight if spec.enabled else 0.0,
        diagnostic_fields=fields,
    )


def evaluate_reward(
    spec: CounterpointInstanceSpec,
    state: CounterpointState,
    action: CounterpointAction,
    next_state: CounterpointState,
    legality_result: LegalityResult,
    *,
    terminated: bool = False,
) -> RewardResult:
    adjacent_classes = [
        interval_class(lower, upper)
        for lower, upper in zip(next_state.pitches, next_state.pitches[1:], strict=False)
    ]
    allowed_adjacent_fraction = (
        sum(
            1
            for adjacent in adjacent_classes
            if adjacent in spec.allowed_adjacent_interval_classes
        )
        / len(adjacent_classes)
        if adjacent_classes
        else 1.0
    )
    outer = interval_class(next_state.pitches[0], next_state.pitches[-1])
    mean_abs_delta = sum(abs(delta) for delta in action.deltas) / len(action.deltas)
    normalized_move_penalty = -mean_abs_delta / spec.max_step_size
    nonzero_directions = {delta > 0 for delta in action.deltas if delta != 0}
    motion_shape_value = 0.5 if len(nonzero_directions) > 1 else 0.0
    center = (spec.pitch_min + spec.pitch_max) / 2
    half_band = max(1.0, (spec.pitch_max - spec.pitch_min) / 2)
    mean_center_distance = (
        sum(abs(pitch - center) for pitch in next_state.pitches) / len(next_state.pitches)
    ) / half_band
    beat_value = 1.0 if next_state.beat_index == 0 else 0.0
    direction_pattern = tuple(-1 if delta < 0 else 1 if delta > 0 else 0 for delta in action.deltas)
    terms = (
        _weighted(
            "valid_transition_bonus",
            1.0 if legality_result.is_legal else 0.0,
            {"is_legal": legality_result.is_legal},
        ),
        _weighted(
            "adjacent_interval_preference",
            allowed_adjacent_fraction,
            {"allowed_adjacent_fraction": allowed_adjacent_fraction},
        ),
        _weighted(
            "outer_interval_preference",
            1.0 if outer in spec.allowed_outer_interval_classes else 0.0,
            {"outer_interval_class": outer},
        ),
        _weighted(
            "movement_size_preference",
            normalized_move_penalty,
            {"mean_abs_delta": mean_abs_delta},
        ),
        _weighted(
            "motion_shape_preference",
            motion_shape_value,
            {"direction_pattern": direction_pattern},
        ),
        _weighted(
            "range_comfort_penalty",
            -mean_center_distance,
            {"mean_center_distance": mean_center_distance},
        ),
        _weighted(
            "beat_phase_local_preference",
            beat_value,
            {"beat_index": next_state.beat_index},
        ),
        _weighted(
            "terminal_completion_bonus",
            1.0 if terminated else 0.0,
            {"terminated": terminated},
        ),
    )
    return RewardResult(
        reward_bundle_id=spec.reward_bundle_id,
        total_reward=sum(term.weighted_value for term in terms),
        terms=terms,
    )
