"""Configuration for the second serious counterpoint schema comparison."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.manifests import to_json_dict
from big_boy_benchmarking.environments.counterpoint import ids

EVALUATION_ID = ids.SECOND_SERIOUS_SCHEMA_COMPARISON_EVALUATION_ID
EVALUATION_RUN_FAMILY_ID = ids.SECOND_SERIOUS_SCHEMA_COMPARISON_RUN_FAMILY_ID
CALIBRATION_MODE_ID = ids.SECOND_SERIOUS_SCHEMA_COMPARISON_CALIBRATION_MODE_ID
SERIOUS_MODE_ID = ids.SECOND_SERIOUS_SCHEMA_COMPARISON_SERIOUS_MODE_ID
SMOKE_MODE_ID = ids.SECOND_SERIOUS_SCHEMA_COMPARISON_SMOKE_MODE_ID
SCHEMA0_CLASS_ID = ids.SECOND_SERIOUS_SCHEMA0_CLASS_ID
SCHEMA1_CLASS_ID = ids.SECOND_SERIOUS_SCHEMA1_CLASS_ID
DEFAULT_RUNTIME_MODE_ID = "tower_exploit_explore"
DEFAULT_LINEARIZATION_MODE_ID = "tensor_available_disabled"
SCHEMA1_TOWER_SOURCE_ONE_DROP = "one_drop_candidate"
SCHEMA1_TOWER_SOURCE_FULL_ITERATED = "full_iterated_noisy_rate"
SCHEMA1_TOWER_SOURCE_IDS = (
    SCHEMA1_TOWER_SOURCE_ONE_DROP,
    SCHEMA1_TOWER_SOURCE_FULL_ITERATED,
)
DEFAULT_THRESHOLD_POLICY_ID = "counterpoint_total_space_sustained_reward_v001"
DEFAULT_TIER_JUMP_POLICY_ID = "counterpoint_active_tier_observed_transition_v001"
METRIC_ID = "episode_total_reward"
PERSISTENCE_RULE_ID = "4_of_5"
DEFAULT_WINDOW_LENGTH = 5
DEFAULT_REQUIRED_COUNT = 4
DEFAULT_SMOKE_INSTANCE_ID = "small"
DEFAULT_SERIOUS_INSTANCE_ID = "medium"
DEFAULT_SMOKE_CANDIDATE_CAP = 1
DEFAULT_SERIOUS_CANDIDATE_CAP = 4
DEFAULT_SMOKE_REPLICATES = 1
DEFAULT_SERIOUS_REPLICATES = 4
DEFAULT_SMOKE_EPISODES = 8
DEFAULT_CALIBRATION_EPISODES = 32
DEFAULT_SERIOUS_EPISODES = 256
DEFAULT_CONTROLLER_EVENT_CEILING_POLICY = "max(64, 8 * horizon)"


@dataclass(frozen=True)
class SecondSeriousComparisonBudget:
    """Locked budget/configuration for this schema comparison evaluation."""

    environment_instance_id: str
    candidate_readout_source: Path | str
    candidate_cap: int = DEFAULT_SMOKE_CANDIDATE_CAP
    target_candidate_ids: tuple[str, ...] = ()
    schema1_tower_source: str = SCHEMA1_TOWER_SOURCE_ONE_DROP
    episodes_per_replicate: int = DEFAULT_SMOKE_EPISODES
    training_replicates_per_arm: int = DEFAULT_SMOKE_REPLICATES
    base_seed: int = 0
    locked_by: str = "cli"
    run_mode: str = SMOKE_MODE_ID
    threshold_policy_id: str = DEFAULT_THRESHOLD_POLICY_ID
    threshold_value: float | None = None
    window_length: int = DEFAULT_WINDOW_LENGTH
    required_count: int = DEFAULT_REQUIRED_COUNT
    tier_jump_policy_id: str = DEFAULT_TIER_JUMP_POLICY_ID
    tier_jump_reward_cutoff: float | None = None
    controller_event_ceiling_policy: str = DEFAULT_CONTROLLER_EVENT_CEILING_POLICY
    controller_event_ceiling_override: int | None = None
    linearization_mode_id: str = DEFAULT_LINEARIZATION_MODE_ID
    serious_run_authorized: bool = False

    def __post_init__(self) -> None:
        if not self.environment_instance_id:
            raise ValueError("environment_instance_id must be nonempty")
        if not str(self.candidate_readout_source):
            raise ValueError("candidate_readout_source must be nonempty")
        if self.candidate_cap <= 0:
            raise ValueError("candidate_cap must be positive")
        if any(not item for item in self.target_candidate_ids):
            raise ValueError("target_candidate_ids cannot contain empty ids")
        if self.schema1_tower_source not in SCHEMA1_TOWER_SOURCE_IDS:
            raise ValueError(
                "schema1_tower_source must be one of "
                f"{', '.join(SCHEMA1_TOWER_SOURCE_IDS)}"
            )
        if self.episodes_per_replicate <= 0:
            raise ValueError("episodes_per_replicate must be positive")
        if self.training_replicates_per_arm <= 0:
            raise ValueError("training_replicates_per_arm must be positive")
        if self.window_length <= 0:
            raise ValueError("window_length must be positive")
        if self.required_count <= 0:
            raise ValueError("required_count must be positive")
        if self.required_count > self.window_length:
            raise ValueError("required_count cannot exceed window_length")
        if self.linearization_mode_id != DEFAULT_LINEARIZATION_MODE_ID:
            raise ValueError(
                "second serious schema comparison uses tensor_available_disabled; "
                f"reserved linearization mode rejected: {self.linearization_mode_id}"
            )
        if self.run_mode == SERIOUS_MODE_ID:
            if self.threshold_value is None:
                raise ValueError("serious run requires explicit locked threshold_value")
            if not self.serious_run_authorized:
                raise ValueError("serious run requires explicit Project Owner authorization")

    def max_controller_events(self, horizon: int) -> int:
        if self.controller_event_ceiling_override is not None:
            if self.controller_event_ceiling_override <= 0:
                raise ValueError("controller_event_ceiling_override must be positive")
            return self.controller_event_ceiling_override
        return max(64, 8 * horizon)

    def to_dict(self) -> dict[str, Any]:
        payload = to_json_dict(self)
        payload["candidate_readout_source"] = str(self.candidate_readout_source)
        return payload
