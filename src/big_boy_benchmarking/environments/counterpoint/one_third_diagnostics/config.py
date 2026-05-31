"""Configuration constants for one-third counterpoint tower diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from big_boy_benchmarking.artifacts.manifests import to_json_dict
from big_boy_benchmarking.environments.counterpoint import ids

EVALUATION_ID = "counterpoint_one_third_schema_tower_diagnostics_v001"
EVALUATION_RUN_FAMILY_ID = (
    "counterpoint_symbolic_v001_one_third_schema_tower_diagnostics_v001"
)
DEFAULT_SCHEMA_ID = ids.ONE_THIRD_OUTGOING_SCHEMA_ID
DEFAULT_SCHEMA_SEEDS = (0, 1, 2)
DEFAULT_REPLICATES_PER_SCHEMA_SEED = 4
DEFAULT_EPISODES_PER_REPLICATE = 16
DEFAULT_CONTROLLER_EVENT_CEILING_POLICY = "max(64, 8 * horizon)"
DEFAULT_LINEARIZATION_MODE_ID = "tensor_available_disabled"
NEAR_FULL_COLLAPSE_THRESHOLD = 0.90
DEFAULT_MODE_ID = "tower_exploit_explore"


@dataclass(frozen=True)
class OneThirdDiagnosticsBudget:
    """Locked one-third diagnostic budget."""

    instance_ids: tuple[str, ...]
    schema_id: str = DEFAULT_SCHEMA_ID
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
            raise ValueError("one-third diagnostics require at least one instance")
        if any("tiny" in instance_id for instance_id in self.instance_ids):
            raise ValueError("tiny is not part of one-third diagnostics")
        if self.schema_id != DEFAULT_SCHEMA_ID:
            raise ValueError(f"unsupported one-third diagnostic schema id: {self.schema_id}")
        if not self.schema_seeds:
            raise ValueError("one-third diagnostics require at least one schema seed")
        if self.replicates_per_schema_seed <= 0:
            raise ValueError("replicates_per_schema_seed must be positive")
        if self.episodes_per_replicate <= 0:
            raise ValueError("episodes_per_replicate must be positive")
        if self.controller_event_ceiling_override is not None:
            if self.controller_event_ceiling_override <= 0:
                raise ValueError("controller_event_ceiling_override must be positive")
        if self.linearization_mode_id != DEFAULT_LINEARIZATION_MODE_ID:
            raise ValueError(
                "one-third diagnostics use tensor_available_disabled; "
                f"reserved linearization mode rejected: {self.linearization_mode_id}"
            )

    def max_controller_events(self, horizon: int) -> int:
        if self.controller_event_ceiling_override is not None:
            return self.controller_event_ceiling_override
        return max(64, 8 * horizon)

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(self)
