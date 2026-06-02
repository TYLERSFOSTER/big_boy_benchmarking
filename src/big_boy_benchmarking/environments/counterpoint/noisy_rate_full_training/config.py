"""Configuration for noisy-rate full-tower training diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.manifests import to_json_dict
from big_boy_benchmarking.environments.counterpoint import ids

EVALUATION_ID = ids.NOISY_RATE_FULL_TOWER_TRAINING_EVALUATION_ID
EVALUATION_RUN_FAMILY_ID = ids.NOISY_RATE_FULL_TOWER_TRAINING_RUN_FAMILY_ID
RUN_MODE_ID = ids.NOISY_RATE_FULL_TOWER_TRAINING_RUN_MODE_ID
DEFAULT_MODE_ID = "tower_exploit_explore"
DEFAULT_LINEARIZATION_MODE_ID = "tensor_available_disabled"
DEFAULT_TRAINING_REPLICATES_PER_CANDIDATE = 4
DEFAULT_EPISODES_PER_REPLICATE = 64
SMOKE_CANDIDATE_CAP = 2
SMOKE_TRAINING_REPLICATES_PER_CANDIDATE = 1
SMOKE_EPISODES_PER_REPLICATE = 4
DEFAULT_CONTROLLER_EVENT_CEILING_POLICY = "max(64, 8 * horizon)"
ZERO_STEP_EPISODE_SHARE_WARNING = 0.10
SELECTED_TIER_NON_EXECUTABILITY_WARNING_COUNT = 1
MINIMUM_CONCRETE_STEP_COUNT_FOR_CLEAN = 1
MINIMUM_LIFT_SUCCESS_COUNT_FOR_CLEAN = 1
MINIMUM_LEARNER_UPDATE_COUNT_FOR_CLEAN = 1
NO_CONTRACTION_ARM_ID = "no_contraction_control"


@dataclass(frozen=True)
class NoisyRateFullTrainingBudget:
    """Locked budget for full-tower training health diagnostics."""

    parent_candidate_readout_source: Path | str
    include_runtime_anchor: bool = False
    candidate_cap: int | None = None
    training_replicates_per_candidate: int = DEFAULT_TRAINING_REPLICATES_PER_CANDIDATE
    episodes_per_replicate: int = DEFAULT_EPISODES_PER_REPLICATE
    horizon_by_instance_id: dict[str, int] | None = None
    controller_event_ceiling_policy: str = DEFAULT_CONTROLLER_EVENT_CEILING_POLICY
    controller_event_ceiling_override: int | None = None
    linearization_mode_id: str = DEFAULT_LINEARIZATION_MODE_ID
    base_seed: int = 0
    locked_by: str = "cli"

    def __post_init__(self) -> None:
        if self.candidate_cap is not None and self.candidate_cap <= 0:
            raise ValueError("candidate_cap must be positive when provided")
        if self.training_replicates_per_candidate <= 0:
            raise ValueError("training_replicates_per_candidate must be positive")
        if self.episodes_per_replicate <= 0:
            raise ValueError("episodes_per_replicate must be positive")
        if self.controller_event_ceiling_override is not None:
            if self.controller_event_ceiling_override <= 0:
                raise ValueError("controller_event_ceiling_override must be positive")
        if self.linearization_mode_id != DEFAULT_LINEARIZATION_MODE_ID:
            raise ValueError(
                "noisy-rate full-tower training uses tensor_available_disabled; "
                f"reserved linearization mode rejected: {self.linearization_mode_id}"
            )
        if not str(self.parent_candidate_readout_source):
            raise ValueError("parent_candidate_readout_source must be nonempty")

    def max_controller_events(self, horizon: int) -> int:
        if self.controller_event_ceiling_override is not None:
            return self.controller_event_ceiling_override
        return max(64, 8 * horizon)

    def to_dict(self) -> dict[str, Any]:
        payload = to_json_dict(self)
        payload["parent_candidate_readout_source"] = str(
            self.parent_candidate_readout_source
        )
        return payload

