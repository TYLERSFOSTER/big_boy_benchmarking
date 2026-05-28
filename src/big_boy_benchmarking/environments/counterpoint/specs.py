"""Versioned instance specifications for counterpoint hidden graphs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from big_boy_benchmarking.environments.counterpoint import ids


def _normalize_interval_classes(values: tuple[int, ...], field_name: str) -> tuple[int, ...]:
    normalized = tuple(sorted({int(value) % 12 for value in values}))
    for value in values:
        if not isinstance(value, int):
            raise ValueError(f"{field_name} must contain integers")
        if value < 0 or value > 11:
            raise ValueError(f"{field_name} must contain interval classes in 0..11")
    return normalized


def interval_class(lower_pitch: int, upper_pitch: int) -> int:
    """Return the pitch-class interval from lower pitch to upper pitch."""

    return (upper_pitch - lower_pitch) % 12


@dataclass(frozen=True)
class CounterpointInstanceSpec:
    """Immutable-ish instance contract for one finite counterpoint graph."""

    environment_family_id: str
    environment_instance_id: str
    family_version: str
    voice_count: int
    pitch_min: int
    pitch_max: int
    tonic_pitch_class: int
    measure_size: int
    horizon_steps: int
    max_step_size: int
    allow_stationary_voice: bool
    require_strict_voice_order: bool
    allowed_adjacent_interval_classes: tuple[int, ...]
    allowed_outer_interval_classes: tuple[int, ...]
    allowed_root_interval_classes: tuple[int, ...]
    forbidden_parallel_interval_classes: tuple[int, ...]
    max_outer_span: int
    legality_contract_id: str
    reward_bundle_id: str
    edge_label_contract_id: str
    initial_state_policy_id: str
    terminal_policy_id: str
    action_mask_policy_id: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "allowed_adjacent_interval_classes",
            _normalize_interval_classes(
                self.allowed_adjacent_interval_classes,
                "allowed_adjacent_interval_classes",
            ),
        )
        object.__setattr__(
            self,
            "allowed_outer_interval_classes",
            _normalize_interval_classes(
                self.allowed_outer_interval_classes,
                "allowed_outer_interval_classes",
            ),
        )
        object.__setattr__(
            self,
            "allowed_root_interval_classes",
            _normalize_interval_classes(
                self.allowed_root_interval_classes,
                "allowed_root_interval_classes",
            ),
        )
        object.__setattr__(
            self,
            "forbidden_parallel_interval_classes",
            _normalize_interval_classes(
                self.forbidden_parallel_interval_classes,
                "forbidden_parallel_interval_classes",
            ),
        )
        self.validate()

    def validate(self) -> CounterpointInstanceSpec:
        if self.environment_family_id != ids.ENVIRONMENT_FAMILY_ID:
            raise ValueError("environment_family_id must match the locked family id")
        if not self.environment_instance_id:
            raise ValueError("environment_instance_id must be nonempty")
        if not self.family_version:
            raise ValueError("family_version must be nonempty")
        if self.voice_count < 2:
            raise ValueError("voice_count must be at least 2")
        if self.pitch_min > self.pitch_max:
            raise ValueError("pitch_min must be <= pitch_max")
        if self.pitch_max - self.pitch_min + 1 < self.voice_count:
            raise ValueError("pitch band must contain at least voice_count pitches")
        if self.tonic_pitch_class < 0 or self.tonic_pitch_class > 11:
            raise ValueError("tonic_pitch_class must be in 0..11")
        if self.measure_size <= 0:
            raise ValueError("measure_size must be positive")
        if self.horizon_steps <= 0:
            raise ValueError("horizon_steps must be positive")
        if self.max_step_size <= 0:
            raise ValueError("max_step_size must be positive")
        if not self.allowed_adjacent_interval_classes:
            raise ValueError("allowed_adjacent_interval_classes must be nonempty")
        if not self.allowed_outer_interval_classes:
            raise ValueError("allowed_outer_interval_classes must be nonempty")
        if self.max_outer_span <= 0:
            raise ValueError("max_outer_span must be positive")
        if self.legality_contract_id != ids.LEGALITY_CONTRACT_ID:
            raise ValueError("legality_contract_id must match the locked id")
        if self.reward_bundle_id != ids.REWARD_BUNDLE_ID:
            raise ValueError("reward_bundle_id must match the locked id")
        if self.edge_label_contract_id != ids.EDGE_LABEL_CONTRACT_ID:
            raise ValueError("edge_label_contract_id must match the locked id")
        if self.initial_state_policy_id != ids.INITIAL_STATE_POLICY_ID:
            raise ValueError("initial_state_policy_id must match the locked id")
        if self.terminal_policy_id != ids.TERMINAL_POLICY_ID:
            raise ValueError("terminal_policy_id must match the locked id")
        if self.action_mask_policy_id != ids.ACTION_MASK_POLICY_ID:
            raise ValueError("action_mask_policy_id must match the locked id")
        return self

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def make_instance_spec(
    *,
    environment_instance_id: str,
    voice_count: int,
    pitch_min: int,
    pitch_max: int,
    measure_size: int,
    horizon_steps: int,
    max_step_size: int,
    tonic_pitch_class: int = 0,
    allow_stationary_voice: bool = True,
    require_strict_voice_order: bool = True,
    allowed_adjacent_interval_classes: tuple[int, ...] = (3, 4, 5, 7, 8, 9),
    allowed_outer_interval_classes: tuple[int, ...] = (0, 3, 4, 5, 7, 8, 9),
    allowed_root_interval_classes: tuple[int, ...] = (0, 2, 4, 5, 7, 9, 11),
    forbidden_parallel_interval_classes: tuple[int, ...] = (0, 7),
    max_outer_span: int = 12,
) -> CounterpointInstanceSpec:
    """Build a spec using the locked v001 contract ids."""

    return CounterpointInstanceSpec(
        environment_family_id=ids.ENVIRONMENT_FAMILY_ID,
        environment_instance_id=environment_instance_id,
        family_version="v001",
        voice_count=voice_count,
        pitch_min=pitch_min,
        pitch_max=pitch_max,
        tonic_pitch_class=tonic_pitch_class,
        measure_size=measure_size,
        horizon_steps=horizon_steps,
        max_step_size=max_step_size,
        allow_stationary_voice=allow_stationary_voice,
        require_strict_voice_order=require_strict_voice_order,
        allowed_adjacent_interval_classes=allowed_adjacent_interval_classes,
        allowed_outer_interval_classes=allowed_outer_interval_classes,
        allowed_root_interval_classes=allowed_root_interval_classes,
        forbidden_parallel_interval_classes=forbidden_parallel_interval_classes,
        max_outer_span=max_outer_span,
        legality_contract_id=ids.LEGALITY_CONTRACT_ID,
        reward_bundle_id=ids.REWARD_BUNDLE_ID,
        edge_label_contract_id=ids.EDGE_LABEL_CONTRACT_ID,
        initial_state_policy_id=ids.INITIAL_STATE_POLICY_ID,
        terminal_policy_id=ids.TERMINAL_POLICY_ID,
        action_mask_policy_id=ids.ACTION_MASK_POLICY_ID,
    )
