"""Configuration constants for counterpoint noisy-rate contraction diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from big_boy_benchmarking.artifacts.manifests import to_json_dict
from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.schemas import (
    DEFAULT_NOISY_RATE_SELECTOR_RULE_ID,
    noisy_rate_arm_id,
)

EVALUATION_ID = ids.NOISY_RATE_CONTRACTION_EVALUATION_ID
EVALUATION_RUN_FAMILY_ID = (
    "counterpoint_symbolic_v001_noisy_rate_contraction_diagnostics_v001"
)
DEFAULT_SCHEMA_FAMILY_ID = ids.NOISY_RATE_CONTRACTION_SCHEMA_FAMILY_ID
DEFAULT_SCHEMA_ID_PREFIX = ids.NOISY_RATE_CONTRACTION_SCHEMA_ID
DEFAULT_SELECTOR_RULE_ID = DEFAULT_NOISY_RATE_SELECTOR_RULE_ID
DEFAULT_RATES = (
    (1, 288),
    (1, 144),
    (1, 72),
    (1, 36),
    (1, 24),
    (1, 18),
    (1, 12),
    (1, 9),
)
SMOKE_RATES = ((1, 144), (1, 36), (1, 18))
DEFAULT_INSTANCE_IDS = ("small", "medium")
DEFAULT_SCHEMA_SEEDS = tuple(range(32))
SMOKE_SCHEMA_SEEDS = (0, 1, 2)
DEFAULT_REPLICATES_PER_SCHEMA_SEED = 4
SMOKE_REPLICATES_PER_SCHEMA_SEED = 1
DEFAULT_EPISODES_PER_REPLICATE = 16
SMOKE_EPISODES_PER_REPLICATE = 1
DEFAULT_CONTROLLER_EVENT_CEILING_POLICY = "max(64, 8 * horizon)"
DEFAULT_LINEARIZATION_MODE_ID = "tensor_available_disabled"
DEFAULT_MODE_ID = "tower_exploit_explore"
RUN_MODE_ID = "diagnostic_noisy_rate_contraction_tower_abc"
NEAR_FULL_COLLAPSE_THRESHOLD = 0.90
HIGH_SOURCE_COVERAGE_THRESHOLD = 0.75
NO_CONTRACTION_ARM_ID = "no_contraction_control"


@dataclass(frozen=True, order=True)
class RateSpec:
    """A locked requested noisy-rate arm."""

    numerator: int
    denominator: int

    def __post_init__(self) -> None:
        if self.denominator <= 0:
            raise ValueError("denominator must be positive")
        if self.numerator < 1 or self.numerator > self.denominator:
            raise ValueError("numerator must be between 1 and denominator")

    @property
    def requested_rate(self) -> float:
        return self.numerator / self.denominator

    @property
    def requested_fraction(self) -> Fraction:
        return Fraction(self.numerator, self.denominator)

    @property
    def arm_id(self) -> str:
        return noisy_rate_arm_id(self.numerator, self.denominator)

    def to_dict(self) -> dict[str, Any]:
        return {
            "numerator": self.numerator,
            "denominator": self.denominator,
            "requested_rate": self.requested_rate,
            "arm_id": self.arm_id,
        }


def normalize_rate_specs(
    rates: tuple[RateSpec | tuple[int, int], ...],
) -> tuple[RateSpec, ...]:
    normalized = tuple(
        rate if isinstance(rate, RateSpec) else RateSpec(rate[0], rate[1])
        for rate in rates
    )
    if not normalized:
        raise ValueError("noisy-rate diagnostics require at least one rate")
    if len({rate.requested_fraction for rate in normalized}) != len(normalized):
        raise ValueError("rates must be unique")
    return tuple(sorted(normalized, key=lambda rate: rate.requested_fraction))


def parse_rate_spec(text: str) -> RateSpec:
    parts = text.strip().split("/")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError(f"expected rate shaped as numerator/denominator, got {text!r}")
    return RateSpec(int(parts[0]), int(parts[1]))


def parse_rate_list(text: str) -> tuple[RateSpec, ...]:
    items = tuple(item.strip() for item in text.split(",") if item.strip())
    if not items:
        raise ValueError("expected at least one comma-separated rate")
    return normalize_rate_specs(tuple(parse_rate_spec(item) for item in items))


@dataclass(frozen=True)
class NoisyRateDiagnosticsBudget:
    """Locked noisy-rate contraction diagnostic budget."""

    instance_ids: tuple[str, ...]
    rates: tuple[RateSpec | tuple[int, int], ...] = DEFAULT_RATES
    include_no_contraction_control: bool = True
    schema_seeds: tuple[int, ...] = DEFAULT_SCHEMA_SEEDS
    replicates_per_schema_seed: int = DEFAULT_REPLICATES_PER_SCHEMA_SEED
    episodes_per_replicate: int = DEFAULT_EPISODES_PER_REPLICATE
    horizon_by_instance_id: dict[str, int] | None = None
    controller_event_ceiling_policy: str = DEFAULT_CONTROLLER_EVENT_CEILING_POLICY
    controller_event_ceiling_override: int | None = None
    linearization_mode_id: str = DEFAULT_LINEARIZATION_MODE_ID
    selector_rule_id: str = DEFAULT_SELECTOR_RULE_ID
    base_seed: int = 0
    locked_by: str = "cli"

    def __post_init__(self) -> None:
        object.__setattr__(self, "rates", normalize_rate_specs(self.rates))
        if not self.instance_ids:
            raise ValueError("noisy-rate diagnostics require at least one instance")
        if any("tiny" in instance_id for instance_id in self.instance_ids):
            raise ValueError("tiny is not part of noisy-rate diagnostics")
        if self.replicates_per_schema_seed <= 0:
            raise ValueError("replicates_per_schema_seed must be positive")
        if self.episodes_per_replicate <= 0:
            raise ValueError("episodes_per_replicate must be positive")
        if not self.schema_seeds:
            raise ValueError("noisy-rate diagnostics require at least one schema seed")
        if self.controller_event_ceiling_override is not None:
            if self.controller_event_ceiling_override <= 0:
                raise ValueError("controller_event_ceiling_override must be positive")
        if self.linearization_mode_id != DEFAULT_LINEARIZATION_MODE_ID:
            raise ValueError(
                "noisy-rate diagnostics use tensor_available_disabled; "
                f"reserved linearization mode rejected: {self.linearization_mode_id}"
            )
        if not self.selector_rule_id:
            raise ValueError("selector_rule_id must be nonempty")

    def max_controller_events(self, horizon: int) -> int:
        if self.controller_event_ceiling_override is not None:
            return self.controller_event_ceiling_override
        return max(64, 8 * horizon)

    def arm_ids(self) -> tuple[str, ...]:
        arms = tuple(rate.arm_id for rate in self.rates)
        if self.include_no_contraction_control:
            return (NO_CONTRACTION_ARM_ID, *arms)
        return arms

    def to_dict(self) -> dict[str, Any]:
        payload = to_json_dict(self)
        payload["rates"] = [rate.to_dict() for rate in self.rates]
        return payload
