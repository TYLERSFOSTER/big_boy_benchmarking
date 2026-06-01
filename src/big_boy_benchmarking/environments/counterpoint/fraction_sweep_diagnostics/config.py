"""Configuration constants for counterpoint contraction fraction sweep diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from big_boy_benchmarking.artifacts.manifests import to_json_dict

EVALUATION_ID = "counterpoint_contraction_fraction_sweep_diagnostics_v001"
EVALUATION_RUN_FAMILY_ID = (
    "counterpoint_symbolic_v001_contraction_fraction_sweep_diagnostics_v001"
)
DEFAULT_SCHEMA_FAMILY_ID = "counterpoint_outgoing_fraction_sweep_schema_v001"
DEFAULT_NUMERATORS = (1, 2, 3, 4, 5, 6)
DEFAULT_DENOMINATOR = 18
DEFAULT_INSTANCE_IDS = ("small", "medium")
DEFAULT_SCHEMA_SEEDS = (0, 1, 2)
DEFAULT_REPLICATES_PER_SCHEMA_SEED = 4
DEFAULT_EPISODES_PER_REPLICATE = 16
DEFAULT_CONTROLLER_EVENT_CEILING_POLICY = "max(64, 8 * horizon)"
DEFAULT_LINEARIZATION_MODE_ID = "tensor_available_disabled"
DEFAULT_MODE_ID = "tower_exploit_explore"
RUN_MODE_ID = "diagnostic_contraction_fraction_sweep_tower_abc"
NEAR_FULL_COLLAPSE_THRESHOLD = 0.90
NO_CONTRACTION_ARM_ID = "no_contraction_control"


def fraction_arm_id(numerator: int, denominator: int = DEFAULT_DENOMINATOR) -> str:
    return f"n{numerator:02d}_over_{denominator}"


@dataclass(frozen=True)
class FractionSweepDiagnosticsBudget:
    """Locked contraction fraction sweep diagnostic budget."""

    instance_ids: tuple[str, ...]
    numerators: tuple[int, ...] = DEFAULT_NUMERATORS
    denominator: int = DEFAULT_DENOMINATOR
    include_no_contraction_control: bool = True
    schema_seeds: tuple[int, ...] = DEFAULT_SCHEMA_SEEDS
    replicates_per_schema_seed: int = DEFAULT_REPLICATES_PER_SCHEMA_SEED
    episodes_per_replicate: int = DEFAULT_EPISODES_PER_REPLICATE
    horizon_by_instance_id: dict[str, int] | None = None
    controller_event_ceiling_policy: str = DEFAULT_CONTROLLER_EVENT_CEILING_POLICY
    controller_event_ceiling_override: int | None = None
    linearization_mode_id: str = DEFAULT_LINEARIZATION_MODE_ID
    base_seed: int = 0
    locked_by: str = "cli"

    def __post_init__(self) -> None:
        if not self.instance_ids:
            raise ValueError("fraction sweep diagnostics require at least one instance")
        if any("tiny" in instance_id for instance_id in self.instance_ids):
            raise ValueError("tiny is not part of fraction sweep diagnostics")
        if self.denominator <= 0:
            raise ValueError("denominator must be positive")
        if not self.numerators:
            raise ValueError("fraction sweep diagnostics require at least one numerator")
        if any(numerator < 1 or numerator > self.denominator for numerator in self.numerators):
            raise ValueError("numerators must be between 1 and denominator")
        if tuple(sorted(self.numerators)) != tuple(self.numerators):
            raise ValueError("numerators must be sorted")
        if self.replicates_per_schema_seed <= 0:
            raise ValueError("replicates_per_schema_seed must be positive")
        if self.episodes_per_replicate <= 0:
            raise ValueError("episodes_per_replicate must be positive")
        if not self.schema_seeds:
            raise ValueError("fraction sweep diagnostics require at least one schema seed")
        if self.controller_event_ceiling_override is not None:
            if self.controller_event_ceiling_override <= 0:
                raise ValueError("controller_event_ceiling_override must be positive")
        if self.linearization_mode_id != DEFAULT_LINEARIZATION_MODE_ID:
            raise ValueError(
                "fraction sweep diagnostics use tensor_available_disabled; "
                f"reserved linearization mode rejected: {self.linearization_mode_id}"
            )

    def max_controller_events(self, horizon: int) -> int:
        if self.controller_event_ceiling_override is not None:
            return self.controller_event_ceiling_override
        return max(64, 8 * horizon)

    def arm_ids(self) -> tuple[str, ...]:
        arms = tuple(fraction_arm_id(numerator, self.denominator) for numerator in self.numerators)
        if self.include_no_contraction_control:
            return (NO_CONTRACTION_ARM_ID, *arms)
        return arms

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(self)

