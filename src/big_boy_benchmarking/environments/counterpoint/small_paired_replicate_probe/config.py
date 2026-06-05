"""Configuration for the counterpoint small paired replicate probe."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.manifests import to_json_dict
from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    DEFAULT_CONTROLLER_EVENT_CEILING_POLICY,
    DEFAULT_LINEARIZATION_MODE_ID,
    DEFAULT_REQUIRED_COUNT,
    DEFAULT_THRESHOLD_POLICY_ID,
    DEFAULT_TIER_JUMP_POLICY_ID,
    DEFAULT_WINDOW_LENGTH,
    SCHEMA1_TOWER_SOURCE_FULL_ITERATED,
    SCHEMA1_TOWER_SOURCE_IDS,
)

EVALUATION_ID = ids.SMALL_PAIRED_REPLICATE_PROBE_EVALUATION_ID
EVALUATION_RUN_FAMILY_ID = ids.SMALL_PAIRED_REPLICATE_PROBE_RUN_FAMILY_ID
SMOKE_RUN_MODE_ID = ids.SMALL_PAIRED_REPLICATE_PROBE_SMOKE_MODE_ID
SELECTED_THRESHOLD_RUN_MODE_ID = ids.SMALL_PAIRED_REPLICATE_PROBE_SELECTED_MODE_ID
SCHEMA0_CLASS_ID = ids.SECOND_SERIOUS_SCHEMA0_CLASS_ID
SCHEMA1_CLASS_ID = ids.SECOND_SERIOUS_SCHEMA1_CLASS_ID
DEFAULT_ENVIRONMENT_INSTANCE_ID = "counterpoint_symbolic_n3_wide_20_108_span18_v001"
DEFAULT_CANDIDATE_CAP = 1
DEFAULT_REPLICATES_PER_ARM = 8
DEFAULT_EPISODES_PER_REPLICATE = 16
DEFAULT_BASE_SEED = 0
DEFAULT_SCHEMA1_TOWER_SOURCE = SCHEMA1_TOWER_SOURCE_FULL_ITERATED
RUN_MODE_IDS = (SMOKE_RUN_MODE_ID, SELECTED_THRESHOLD_RUN_MODE_ID)


@dataclass(frozen=True)
class SmallPairedReplicateProbeBudget:
    """Locked budget/configuration for the paired replicate probe."""

    environment_instance_id: str = DEFAULT_ENVIRONMENT_INSTANCE_ID
    candidate_readout_source: Path | str = ""
    candidate_cap: int = DEFAULT_CANDIDATE_CAP
    target_candidate_ids: tuple[str, ...] = ()
    schema1_tower_source: str = DEFAULT_SCHEMA1_TOWER_SOURCE
    episodes_per_replicate: int = DEFAULT_EPISODES_PER_REPLICATE
    training_replicates_per_arm: int = DEFAULT_REPLICATES_PER_ARM
    base_seed: int = DEFAULT_BASE_SEED
    locked_by: str = "cli"
    run_mode: str = SMOKE_RUN_MODE_ID
    threshold_policy_id: str = DEFAULT_THRESHOLD_POLICY_ID
    threshold_value: float | None = None
    threshold_frontier_readout_source: Path | str | None = None
    window_length: int = DEFAULT_WINDOW_LENGTH
    required_count: int = DEFAULT_REQUIRED_COUNT
    tier_jump_policy_id: str = DEFAULT_TIER_JUMP_POLICY_ID
    tier_jump_reward_cutoff: float | None = None
    controller_event_ceiling_policy: str = DEFAULT_CONTROLLER_EVENT_CEILING_POLICY
    controller_event_ceiling_override: int | None = None
    linearization_mode_id: str = DEFAULT_LINEARIZATION_MODE_ID

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
                f"schema1_tower_source must be one of {', '.join(SCHEMA1_TOWER_SOURCE_IDS)}"
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
                "small paired replicate probe uses tensor_available_disabled; "
                f"reserved linearization mode rejected: {self.linearization_mode_id}"
            )
        if self.run_mode not in RUN_MODE_IDS:
            raise ValueError(f"run_mode must be one of {', '.join(RUN_MODE_IDS)}")
        if (
            self.run_mode == SELECTED_THRESHOLD_RUN_MODE_ID
            and self.threshold_value is None
            and self.threshold_frontier_readout_source is None
        ):
            raise ValueError(
                "threshold-frontier-selected run requires a threshold value or "
                "threshold frontier readout source"
            )

    def max_controller_events(self, horizon: int) -> int:
        if self.controller_event_ceiling_override is not None:
            if self.controller_event_ceiling_override <= 0:
                raise ValueError("controller_event_ceiling_override must be positive")
            return self.controller_event_ceiling_override
        return max(64, 8 * horizon)

    def to_dict(self) -> dict[str, Any]:
        payload = to_json_dict(self)
        payload["candidate_readout_source"] = str(self.candidate_readout_source)
        payload["threshold_frontier_readout_source"] = (
            None
            if self.threshold_frontier_readout_source is None
            else str(self.threshold_frontier_readout_source)
        )
        return payload
