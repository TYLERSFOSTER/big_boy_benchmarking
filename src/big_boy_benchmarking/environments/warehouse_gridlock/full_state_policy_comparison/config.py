"""Configuration for Warehouse full-state/full-action trainable policy comparison."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.warehouse_gridlock.ids import (
    WAREHOUSE_GRIDLOCK_ENVIRONMENT_FAMILY_ID,
    WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.config import (
    CANDIDATE_MIX_COORDINATION_READY,
)
from big_boy_benchmarking.environments.warehouse_gridlock.policies import (
    MODEL_FAMILY_ID,
    POLICY_CONTRACT_ID,
    PROJECTION_STRATEGY_ID,
)

EVALUATION_ID = "warehouse_gridlock_full_state_full_action_trainable_policy_v001"
ARTIFACT_SCHEMA_VERSION_ID = ARTIFACT_SCHEMA_VERSION

DIRECT_ARM_ID = "warehouse_direct_full_state_policy_masked"
TOWER_ARM_ID = "warehouse_tower_full_state_policy_live_lift_masked"
ACTIVE_ARM_IDS = (DIRECT_ARM_ID, TOWER_ARM_ID)

DEFAULT_RUN_LABEL = "policy_contract_smoke_001"
DEFAULT_EPISODES_PER_ARM = 4
DEFAULT_REPLICATES_PER_ARM = 1
DEFAULT_SCHEMA_SEEDS = 1
DEFAULT_MAX_SECONDS_PER_EPISODE = 128
DEFAULT_LEARNING_RATE = 0.01
DEFAULT_BASELINE_RATE = 0.05
DEFAULT_TEMPERATURE_INITIAL = 1.0
DEFAULT_TEMPERATURE_FLOOR = 0.1
DEFAULT_TEMPERATURE_DECAY_PER_EPISODE = 0.995
DEFAULT_PROJECTION_ATTEMPT_BUDGET = 64
DEFAULT_PROGRESS_EVERY_EPISODES = 1
DEFAULT_SEED = 0
DEFAULT_CANDIDATE_PROPOSALS_PER_STEP = 64
DEFAULT_MAX_ACTIVE_ROBOTS = 3


@dataclass(frozen=True)
class FullStatePolicyComparisonConfig:
    repo_root: Path
    artifact_root: Path
    readiness_source: Path
    run_label: str = DEFAULT_RUN_LABEL
    locked_by: str = "unknown"
    instance_id: str = WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID
    environment_family_id: str = WAREHOUSE_GRIDLOCK_ENVIRONMENT_FAMILY_ID
    episodes_per_arm: int = DEFAULT_EPISODES_PER_ARM
    replicates_per_arm: int = DEFAULT_REPLICATES_PER_ARM
    schema_seeds: int = DEFAULT_SCHEMA_SEEDS
    max_seconds_per_episode: int = DEFAULT_MAX_SECONDS_PER_EPISODE
    max_seconds_schedule_start: int | None = None
    max_seconds_schedule_end: int | None = None
    max_seconds_schedule_span_episodes: int | None = None
    learning_rate: float = DEFAULT_LEARNING_RATE
    baseline_rate: float = DEFAULT_BASELINE_RATE
    temperature_initial: float = DEFAULT_TEMPERATURE_INITIAL
    temperature_floor: float = DEFAULT_TEMPERATURE_FLOOR
    temperature_decay_per_episode: float = DEFAULT_TEMPERATURE_DECAY_PER_EPISODE
    projection_attempt_budget: int = DEFAULT_PROJECTION_ATTEMPT_BUDGET
    progress_every_episodes: int = DEFAULT_PROGRESS_EVERY_EPISODES
    seed: int = DEFAULT_SEED
    candidate_proposals_per_step: int = DEFAULT_CANDIDATE_PROPOSALS_PER_STEP
    max_active_robots: int = DEFAULT_MAX_ACTIVE_ROBOTS
    candidate_mix_id: str = CANDIDATE_MIX_COORDINATION_READY
    active_arm_ids: tuple[str, ...] = ACTIVE_ARM_IDS
    progress_to_stderr: bool = True

    def __post_init__(self) -> None:
        if not self.active_arm_ids:
            raise ValueError("active_arm_ids must contain at least one arm id")
        unknown = set(self.active_arm_ids) - set(ACTIVE_ARM_IDS)
        if unknown:
            raise ValueError(f"unknown Warehouse policy arm ids: {sorted(unknown)}")
        schedule_values = (
            self.max_seconds_schedule_start,
            self.max_seconds_schedule_end,
            self.max_seconds_schedule_span_episodes,
        )
        if any(value is not None for value in schedule_values) and not all(
            value is not None for value in schedule_values
        ):
            raise ValueError(
                "max-seconds curriculum requires start, end, and span episode values"
            )
        if (
            self.max_seconds_schedule_span_episodes is not None
            and self.max_seconds_schedule_span_episodes <= 0
        ):
            raise ValueError("max_seconds_schedule_span_episodes must be positive")

    @property
    def run_mode(self) -> str:
        return "trainable_policy_smoke" if "smoke" in self.run_label else "trainable_policy_pilot"

    def max_seconds_for_episode(self, episode_index: int) -> int:
        if (
            self.max_seconds_schedule_start is None
            or self.max_seconds_schedule_end is None
            or self.max_seconds_schedule_span_episodes is None
        ):
            return self.max_seconds_per_episode
        span = max(1, self.max_seconds_schedule_span_episodes)
        fraction = min(max(episode_index, 0), span) / span
        scheduled = self.max_seconds_schedule_start + (
            self.max_seconds_schedule_end - self.max_seconds_schedule_start
        ) * fraction
        return max(1, int(round(scheduled)))

    def to_manifest(self) -> dict[str, object]:
        return {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION_ID,
            "evaluation_id": EVALUATION_ID,
            "run_label": self.run_label,
            "run_mode": self.run_mode,
            "locked_by": self.locked_by,
            "instance_id": self.instance_id,
            "environment_family_id": self.environment_family_id,
            "episodes_per_arm": self.episodes_per_arm,
            "replicates_per_arm": self.replicates_per_arm,
            "schema_seeds": self.schema_seeds,
            "max_seconds_per_episode": self.max_seconds_per_episode,
            "max_seconds_schedule_start": self.max_seconds_schedule_start,
            "max_seconds_schedule_end": self.max_seconds_schedule_end,
            "max_seconds_schedule_span_episodes": self.max_seconds_schedule_span_episodes,
            "learning_rate": self.learning_rate,
            "baseline_rate": self.baseline_rate,
            "temperature_initial": self.temperature_initial,
            "temperature_floor": self.temperature_floor,
            "temperature_decay_per_episode": self.temperature_decay_per_episode,
            "projection_attempt_budget": self.projection_attempt_budget,
            "projection_strategy_id": PROJECTION_STRATEGY_ID,
            "policy_contract_id": POLICY_CONTRACT_ID,
            "model_family_id": MODEL_FAMILY_ID,
            "progress_every_episodes": self.progress_every_episodes,
            "seed": self.seed,
            "candidate_proposals_per_step": self.candidate_proposals_per_step,
            "max_active_robots": self.max_active_robots,
            "candidate_mix_id": self.candidate_mix_id,
            "active_arm_ids": list(self.active_arm_ids),
        }
