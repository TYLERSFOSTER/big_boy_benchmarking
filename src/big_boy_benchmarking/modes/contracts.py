"""Mode contracts and validation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class OnlineCostPolicy:
    included: tuple[str, ...]
    excluded: tuple[str, ...]


@dataclass(frozen=True)
class ReadoutPolicy:
    requested: bool
    allowed: bool
    reason: str


@dataclass(frozen=True)
class MorphismPolicy:
    requested: bool
    allowed: bool
    reason: str


@dataclass(frozen=True)
class TimingProfile:
    profile_id: str
    include_readout: bool = False
    include_morphism: bool = False


@dataclass(frozen=True)
class DiagnosticProfile:
    profile_id: str
    structural_diagnostics: str = "none"


@dataclass(frozen=True)
class BenchmarkModeContract:
    mode_id: str
    environment_coupling: str
    schema_mode: str
    controller_regime: str
    training_surface: str
    learner_id: str
    diagnostic_profile: DiagnosticProfile
    timing_profile: TimingProfile
    online_costs_included: tuple[str, ...]
    online_costs_excluded: tuple[str, ...]
    readout_policy: ReadoutPolicy
    morphism_policy: MorphismPolicy
    runnable: bool = True
    reserved_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_mode_contract(
    contract: BenchmarkModeContract, *, allow_reserved: bool = False
) -> None:
    errors: list[str] = []

    if not contract.runnable and not allow_reserved:
        errors.append(f"mode is reserved: {contract.mode_id}")

    if not contract.runnable and not contract.reserved_reason:
        errors.append("reserved mode must include reserved_reason")

    if contract.environment_coupling == "direct_env":
        tower_costs = [
            cost for cost in contract.online_costs_included if cost.startswith("tower_")
        ]
        if tower_costs:
            errors.append(f"direct env mode includes tower costs: {tower_costs}")

    if "nonempty" in contract.mode_id and contract.schema_mode in {"none", "empty", "direct"}:
        errors.append("nonempty schema mode requires explicit nonempty schema_mode")

    if not isinstance(contract.readout_policy, ReadoutPolicy):
        errors.append("readout_policy must be explicit")

    if not isinstance(contract.morphism_policy, MorphismPolicy):
        errors.append("morphism_policy must be explicit")

    if not isinstance(contract.timing_profile, TimingProfile):
        errors.append("timing_profile must be explicit")

    if contract.timing_profile.include_readout and not contract.readout_policy.requested:
        errors.append("timing profile includes readout but readout_policy.requested is false")

    if contract.timing_profile.include_morphism and not contract.morphism_policy.requested:
        errors.append("timing profile includes morphism but morphism_policy.requested is false")

    if errors:
        raise ValueError("; ".join(errors))
