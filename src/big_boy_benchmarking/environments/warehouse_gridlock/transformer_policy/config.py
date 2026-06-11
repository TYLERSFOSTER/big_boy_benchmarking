"""Configuration for Warehouse Gridlock transformer policy training."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION

from ..ids import (
    WAREHOUSE_GRIDLOCK_ENVIRONMENT_FAMILY_ID,
    WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID,
)
from ..masked_direct_vs_live_lift_tower.config import CANDIDATE_MIX_COORDINATION_READY

EVALUATION_ID = "warehouse_gridlock_transformer_policy_v001"
MODEL_FAMILY_ID = "warehouse_transformer_actor_critic_policy_v001"
POLICY_CONTRACT_ID = "warehouse_full_state_full_action_policy_contract_v001"

TOWER_ARM_ID = "warehouse_tower_transformer_live_lift_masked"
DIRECT_ARM_ID = "warehouse_direct_transformer_admissible_masked"
ACTIVE_ARM_IDS = (TOWER_ARM_ID,)
SUPPORTED_ARM_IDS = (TOWER_ARM_ID, DIRECT_ARM_ID)

DEFAULT_RUN_LABEL = "tower_transformer_curriculum_smoke_001"
DEFAULT_EPISODES = 2
DEFAULT_REPLICATES = 1
DEFAULT_SCHEMA_SEEDS = 1
DEFAULT_SEED = 0
DEFAULT_MAX_SECONDS_START = 2
DEFAULT_MAX_SECONDS_END = 64
DEFAULT_CURRICULUM_RAMP_EPISODES = 1024
DEFAULT_CANDIDATE_PROPOSALS_PER_STEP = 64
DEFAULT_MAX_ACTIVE_ROBOTS = 3
DEFAULT_PROJECTION_ATTEMPT_BUDGET = 64
DEFAULT_PROGRESS_EVERY_EPISODES = 1
DEFAULT_CHECKPOINT_EVERY_EPISODES = 100
DEFAULT_TRACE_EVERY_EPISODES = 0
DEFAULT_SOFT_ARTIFACT_BUDGET_BYTES = 500 * 1024 * 1024
DEFAULT_HARD_ARTIFACT_BUDGET_BYTES = 2 * 1024 * 1024 * 1024


@dataclass(frozen=True)
class TransformerModelConfig:
    d_model: int = 128
    n_layers: int = 2
    n_heads: int = 4
    mlp_hidden: int = 256
    dropout: float = 0.0
    activation: str = "gelu"
    max_rows: int = 16
    max_cols: int = 16
    max_entities: int = 64
    primitive_action_count: int = 5
    model_family_id: str = MODEL_FAMILY_ID

    def to_manifest(self) -> dict[str, object]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class OptimizerConfig:
    optimizer_id: str = "adamw"
    learning_rate: float = 3.0e-4
    gamma: float = 0.99
    value_coef: float = 0.5
    entropy_coef: float = 0.01
    max_grad_norm: float = 1.0

    def to_manifest(self) -> dict[str, object]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class CurriculumConfig:
    max_seconds_start: int = DEFAULT_MAX_SECONDS_START
    max_seconds_end: int = DEFAULT_MAX_SECONDS_END
    ramp_episodes: int = DEFAULT_CURRICULUM_RAMP_EPISODES

    def max_seconds_for_episode(self, episode_index: int) -> int:
        span = max(1, self.ramp_episodes)
        fraction = min(max(episode_index, 0), span) / span
        scheduled = self.max_seconds_start + (
            self.max_seconds_end - self.max_seconds_start
        ) * fraction
        return max(1, int(round(scheduled)))

    def to_manifest(self) -> dict[str, object]:
        return {
            "schedule_type": "linear_then_flat",
            "max_seconds_start": self.max_seconds_start,
            "max_seconds_end": self.max_seconds_end,
            "ramp_episodes": self.ramp_episodes,
        }


@dataclass(frozen=True)
class CheckpointConfig:
    checkpoint_every_episodes: int = DEFAULT_CHECKPOINT_EVERY_EPISODES
    keep_last_n_checkpoints: int = 5
    keep_best_n_checkpoints: int = 3

    def to_manifest(self) -> dict[str, object]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class TraceRetentionConfig:
    trace_episode_indices: tuple[int | str, ...] = ("0", "final")
    trace_every_episodes: int = DEFAULT_TRACE_EVERY_EPISODES
    soft_artifact_budget_bytes: int = DEFAULT_SOFT_ARTIFACT_BUDGET_BYTES
    hard_artifact_budget_bytes: int = DEFAULT_HARD_ARTIFACT_BUDGET_BYTES

    def normalized_trace_indices(self) -> tuple[int | str, ...]:
        normalized: list[int | str] = []
        for item in self.trace_episode_indices:
            if isinstance(item, int):
                normalized.append(item)
                continue
            text = str(item)
            if text == "final":
                normalized.append(text)
            else:
                normalized.append(int(text))
        return tuple(normalized)

    def to_manifest(self) -> dict[str, object]:
        return {
            "trace_episode_indices": [str(item) for item in self.trace_episode_indices],
            "trace_every_episodes": self.trace_every_episodes,
            "soft_artifact_budget_bytes": self.soft_artifact_budget_bytes,
            "hard_artifact_budget_bytes": self.hard_artifact_budget_bytes,
            "default_policy": "summary_first_selected_traces_only",
        }


@dataclass(frozen=True)
class WarehouseTransformerPolicyRunConfig:
    repo_root: Path
    artifact_root: Path
    readiness_source: Path
    run_label: str = DEFAULT_RUN_LABEL
    locked_by: str = "unknown"
    instance_id: str = WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID
    environment_family_id: str = WAREHOUSE_GRIDLOCK_ENVIRONMENT_FAMILY_ID
    episodes: int = DEFAULT_EPISODES
    replicates: int = DEFAULT_REPLICATES
    schema_seeds: int = DEFAULT_SCHEMA_SEEDS
    seed: int = DEFAULT_SEED
    active_arm_ids: tuple[str, ...] = ACTIVE_ARM_IDS
    model: TransformerModelConfig = field(default_factory=TransformerModelConfig)
    optimizer: OptimizerConfig = field(default_factory=OptimizerConfig)
    curriculum: CurriculumConfig = field(default_factory=CurriculumConfig)
    checkpoint: CheckpointConfig = field(default_factory=CheckpointConfig)
    trace_retention: TraceRetentionConfig = field(default_factory=TraceRetentionConfig)
    candidate_proposals_per_step: int = DEFAULT_CANDIDATE_PROPOSALS_PER_STEP
    max_active_robots: int = DEFAULT_MAX_ACTIVE_ROBOTS
    candidate_mix_id: str = CANDIDATE_MIX_COORDINATION_READY
    projection_attempt_budget: int = DEFAULT_PROJECTION_ATTEMPT_BUDGET
    progress_every_episodes: int = DEFAULT_PROGRESS_EVERY_EPISODES
    progress_to_stderr: bool = True
    device: str = "cpu"

    def __post_init__(self) -> None:
        if self.episodes <= 0:
            raise ValueError("episodes must be positive")
        if self.replicates <= 0:
            raise ValueError("replicates must be positive")
        if self.schema_seeds <= 0:
            raise ValueError("schema_seeds must be positive")
        if not self.active_arm_ids:
            raise ValueError("active_arm_ids must contain at least one arm id")
        unknown = set(self.active_arm_ids) - set(SUPPORTED_ARM_IDS)
        if unknown:
            raise ValueError(f"unknown Warehouse transformer arm ids: {sorted(unknown)}")

    @property
    def run_mode(self) -> str:
        return (
            "transformer_policy_smoke"
            if "smoke" in self.run_label
            else "transformer_policy_training"
        )

    def to_manifest(self) -> dict[str, object]:
        return {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            "evaluation_id": EVALUATION_ID,
            "model_family_id": MODEL_FAMILY_ID,
            "policy_contract_id": POLICY_CONTRACT_ID,
            "run_label": self.run_label,
            "run_mode": self.run_mode,
            "locked_by": self.locked_by,
            "instance_id": self.instance_id,
            "environment_family_id": self.environment_family_id,
            "episodes": self.episodes,
            "replicates": self.replicates,
            "schema_seeds": self.schema_seeds,
            "seed": self.seed,
            "active_arm_ids": list(self.active_arm_ids),
            "model": self.model.to_manifest(),
            "optimizer": self.optimizer.to_manifest(),
            "curriculum": self.curriculum.to_manifest(),
            "checkpoint": self.checkpoint.to_manifest(),
            "trace_retention": self.trace_retention.to_manifest(),
            "candidate_proposals_per_step": self.candidate_proposals_per_step,
            "max_active_robots": self.max_active_robots,
            "candidate_mix_id": self.candidate_mix_id,
            "projection_attempt_budget": self.projection_attempt_budget,
            "progress_every_episodes": self.progress_every_episodes,
            "device": self.device,
        }
