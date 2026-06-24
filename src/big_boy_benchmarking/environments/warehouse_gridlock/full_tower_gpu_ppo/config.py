"""Configuration objects for Warehouse Gridlock full-tower PPO."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.warehouse_gridlock.ids import (
    WAREHOUSE_GRIDLOCK_ENVIRONMENT_FAMILY_ID,
    WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.config import (
    CANDIDATE_MIX_COORDINATION_READY,
)

from .ids import (
    WAREHOUSE_GRIDLOCK_DIRECT_NO_CONTRACTION_ARM_ID,
    WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_ACTIVE_ARM_IDS,
    WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_EVALUATION_ID,
    WAREHOUSE_GRIDLOCK_NO_CONTRACTION_SCHEMA_ID,
    WAREHOUSE_GRIDLOCK_SOURCE_LOCAL_RATIO_SCHEMA_ID,
    WAREHOUSE_GRIDLOCK_TOWER_FIRST_NONTRIVIAL_ARM_ID,
)

DEFAULT_RUN_LABEL = "smoke_cpu_001"
DEFAULT_EPISODES_PER_ARM = 2
DEFAULT_REPLICATES_PER_ARM = 1
DEFAULT_SCHEMA_SEEDS = 1
DEFAULT_MAX_SECONDS_PER_EPISODE = 8
DEFAULT_CANDIDATE_PROPOSALS_PER_STEP = 32
DEFAULT_MAX_ACTIVE_ROBOTS = 3
DEFAULT_SEED = 0


@dataclass(frozen=True)
class WarehousePPOHyperparameters:
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_epsilon: float = 0.2
    entropy_coef: float = 0.01
    value_coef: float = 0.5
    target_kl: float = 0.03
    learning_rate: float = 3.0e-4
    max_grad_norm: float = 0.5
    ppo_epochs: int = 2
    minibatch_size: int = 32
    update_interval_samples: int = 8
    min_tier_update_samples: int = 2

    def __post_init__(self) -> None:
        if self.gamma <= 0.0 or self.gamma > 1.0:
            raise ValueError("gamma must be in (0, 1]")
        if self.gae_lambda < 0.0 or self.gae_lambda > 1.0:
            raise ValueError("gae_lambda must be in [0, 1]")
        if self.clip_epsilon <= 0.0:
            raise ValueError("clip_epsilon must be positive")
        if self.ppo_epochs <= 0:
            raise ValueError("ppo_epochs must be positive")
        if self.minibatch_size <= 0:
            raise ValueError("minibatch_size must be positive")
        if self.update_interval_samples <= 0:
            raise ValueError("update_interval_samples must be positive")

    def to_manifest(self) -> dict[str, object]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class WarehousePolicyCapacityConfig:
    capacity_0: int = 128
    gamma_capacity: float = 0.85
    min_capacity: int = 32
    max_history_length: int = 64

    def __post_init__(self) -> None:
        if self.capacity_0 <= 0:
            raise ValueError("capacity_0 must be positive")
        if self.gamma_capacity <= 0.0:
            raise ValueError("gamma_capacity must be positive")
        if self.min_capacity <= 0:
            raise ValueError("min_capacity must be positive")
        if self.max_history_length <= 0:
            raise ValueError("max_history_length must be positive")

    def capacity_for_tier(self, tier_index: int) -> int:
        return max(
            self.min_capacity,
            round(self.capacity_0 * (self.gamma_capacity ** max(0, tier_index))),
        )

    def to_manifest(self) -> dict[str, object]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class WarehouseDeviceConfig:
    device: str = "cpu"
    allow_cuda_fallback: bool = False
    dtype: str = "float32"
    mixed_precision: bool = False

    def __post_init__(self) -> None:
        if self.device not in {"cpu", "cuda", "auto"}:
            raise ValueError("device must be one of: cpu, cuda, auto")
        if self.mixed_precision:
            raise ValueError("mixed precision is not enabled for v001")

    def to_manifest(self) -> dict[str, object]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class WarehouseRetentionConfig:
    profile_id: str = "smoke_debug"
    retain_first_episode: bool = True
    retain_last_episode: bool = True
    retain_first_success: bool = True
    retain_best_reward: bool = True
    retain_every_n_episodes: int = 0

    def __post_init__(self) -> None:
        if self.profile_id not in {"smoke_debug", "serious_train", "full_debug"}:
            raise ValueError(f"unknown retention profile: {self.profile_id!r}")
        if self.retain_every_n_episodes < 0:
            raise ValueError("retain_every_n_episodes must be nonnegative")

    def to_manifest(self) -> dict[str, object]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class WarehouseCheckpointConfig:
    checkpoint_every_updates: int = 1
    keep_last_n_checkpoints: int = 3
    resume_from_checkpoint: Path | None = None

    def __post_init__(self) -> None:
        if self.checkpoint_every_updates <= 0:
            raise ValueError("checkpoint_every_updates must be positive")

    def to_manifest(self) -> dict[str, object | None]:
        return {
            "checkpoint_every_updates": self.checkpoint_every_updates,
            "keep_last_n_checkpoints": self.keep_last_n_checkpoints,
            "resume_from_checkpoint": (
                None if self.resume_from_checkpoint is None else str(self.resume_from_checkpoint)
            ),
        }


@dataclass(frozen=True)
class WarehouseFullTowerPPOArmConfig:
    arm_id: str
    schema_id: str
    label: str
    nontrivial_schema: bool

    def to_manifest(self) -> dict[str, object]:
        return self.__dict__.copy()


def default_arm_configs() -> tuple[WarehouseFullTowerPPOArmConfig, ...]:
    return (
        WarehouseFullTowerPPOArmConfig(
            arm_id=WAREHOUSE_GRIDLOCK_DIRECT_NO_CONTRACTION_ARM_ID,
            schema_id=WAREHOUSE_GRIDLOCK_NO_CONTRACTION_SCHEMA_ID,
            label="Direct no-contraction PPO",
            nontrivial_schema=False,
        ),
        WarehouseFullTowerPPOArmConfig(
            arm_id=WAREHOUSE_GRIDLOCK_TOWER_FIRST_NONTRIVIAL_ARM_ID,
            schema_id=WAREHOUSE_GRIDLOCK_SOURCE_LOCAL_RATIO_SCHEMA_ID,
            label="Tower first-nontrivial PPO",
            nontrivial_schema=True,
        ),
    )


@dataclass(frozen=True)
class WarehouseFullTowerPPOConfig:
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
    candidate_proposals_per_step: int = DEFAULT_CANDIDATE_PROPOSALS_PER_STEP
    max_active_robots: int = DEFAULT_MAX_ACTIVE_ROBOTS
    candidate_mix_id: str = CANDIDATE_MIX_COORDINATION_READY
    seed: int = DEFAULT_SEED
    active_arm_ids: tuple[str, ...] = WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_ACTIVE_ARM_IDS
    arms: tuple[WarehouseFullTowerPPOArmConfig, ...] = field(default_factory=default_arm_configs)
    ppo: WarehousePPOHyperparameters = field(default_factory=WarehousePPOHyperparameters)
    capacity: WarehousePolicyCapacityConfig = field(default_factory=WarehousePolicyCapacityConfig)
    device: WarehouseDeviceConfig = field(default_factory=WarehouseDeviceConfig)
    retention: WarehouseRetentionConfig = field(default_factory=WarehouseRetentionConfig)
    checkpoint: WarehouseCheckpointConfig = field(default_factory=WarehouseCheckpointConfig)
    profile_id: str = "smoke_cpu"
    progress_every_episodes: int = 1
    confirm_long_run: bool = False

    def __post_init__(self) -> None:
        if self.episodes_per_arm <= 0:
            raise ValueError("episodes_per_arm must be positive")
        if self.replicates_per_arm <= 0:
            raise ValueError("replicates_per_arm must be positive")
        if self.schema_seeds <= 0:
            raise ValueError("schema_seeds must be positive")
        if self.max_seconds_per_episode <= 0:
            raise ValueError("max_seconds_per_episode must be positive")
        if self.candidate_proposals_per_step <= 0:
            raise ValueError("candidate_proposals_per_step must be positive")
        if self.max_active_robots <= 0:
            raise ValueError("max_active_robots must be positive")
        if not self.readiness_source:
            raise ValueError("readiness_source is required")
        known = {arm.arm_id for arm in self.arms}
        unknown = set(self.active_arm_ids) - known
        if unknown:
            raise ValueError(f"unknown Warehouse full-tower PPO arm ids: {sorted(unknown)}")
        for arm in self.arms:
            if (
                arm.arm_id == WAREHOUSE_GRIDLOCK_DIRECT_NO_CONTRACTION_ARM_ID
                and arm.schema_id != WAREHOUSE_GRIDLOCK_NO_CONTRACTION_SCHEMA_ID
            ):
                raise ValueError("direct arm must use no-contraction schema")
        if self.profile_id == "serious_gpu" and not self.confirm_long_run:
            raise ValueError("serious_gpu requires confirm_long_run=True")

    @property
    def artifact_schema_version(self) -> str:
        return ARTIFACT_SCHEMA_VERSION

    @property
    def evaluation_id(self) -> str:
        return WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_EVALUATION_ID

    def active_arms(self) -> tuple[WarehouseFullTowerPPOArmConfig, ...]:
        by_id = {arm.arm_id: arm for arm in self.arms}
        return tuple(by_id[arm_id] for arm_id in self.active_arm_ids)

    def to_manifest(self) -> dict[str, object]:
        return {
            "artifact_schema_version": self.artifact_schema_version,
            "evaluation_id": self.evaluation_id,
            "run_label": self.run_label,
            "locked_by": self.locked_by,
            "instance_id": self.instance_id,
            "environment_family_id": self.environment_family_id,
            "episodes_per_arm": self.episodes_per_arm,
            "replicates_per_arm": self.replicates_per_arm,
            "schema_seeds": self.schema_seeds,
            "max_seconds_per_episode": self.max_seconds_per_episode,
            "candidate_proposals_per_step": self.candidate_proposals_per_step,
            "max_active_robots": self.max_active_robots,
            "candidate_mix_id": self.candidate_mix_id,
            "seed": self.seed,
            "active_arm_ids": list(self.active_arm_ids),
            "arms": [arm.to_manifest() for arm in self.arms],
            "ppo": self.ppo.to_manifest(),
            "capacity": self.capacity.to_manifest(),
            "device": self.device.to_manifest(),
            "retention": self.retention.to_manifest(),
            "checkpoint": self.checkpoint.to_manifest(),
            "profile_id": self.profile_id,
            "progress_every_episodes": self.progress_every_episodes,
            "confirm_long_run": self.confirm_long_run,
        }
