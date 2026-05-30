"""Budget and seed-suite contracts for serious counterpoint learning."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any

from big_boy_benchmarking.artifacts.manifests import to_json_dict
from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.counterpoint.instances import SMALL_INSTANCE_ID
from big_boy_benchmarking.environments.counterpoint.serious_learning.arms import (
    REQUIRED_SERIOUS_LEARNING_ARM_IDS,
    validate_serious_learning_arm_set,
)
from big_boy_benchmarking.seeds.bundles import SeedBundle


@dataclass(frozen=True)
class SchemaSeedSuite:
    schema_seeds: tuple[int, ...]

    def __post_init__(self) -> None:
        if not self.schema_seeds:
            raise ValueError("schema seed suite must be nonempty")
        if len(set(self.schema_seeds)) != len(self.schema_seeds):
            raise ValueError("schema seeds must be unique")
        if any(seed < 0 for seed in self.schema_seeds):
            raise ValueError("schema seeds must be nonnegative")

    def to_dict(self) -> dict[str, Any]:
        return {"schema_seeds": list(self.schema_seeds)}


@dataclass(frozen=True)
class SeedBundleSuite:
    seed_bundles: tuple[SeedBundle, ...]

    def __post_init__(self) -> None:
        if not self.seed_bundles:
            raise ValueError("seed bundle suite must be nonempty")
        ids = tuple(seed_bundle.seed_bundle_id for seed_bundle in self.seed_bundles)
        if len(set(ids)) != len(ids):
            raise ValueError("seed bundle ids must be unique")

    @property
    def seed_bundle_ids(self) -> tuple[str, ...]:
        return tuple(seed_bundle.seed_bundle_id for seed_bundle in self.seed_bundles)

    def to_dict(self) -> dict[str, Any]:
        return {
            "seed_bundle_ids": list(self.seed_bundle_ids),
            "seed_bundles": [seed_bundle.to_dict() for seed_bundle in self.seed_bundles],
        }


@dataclass(frozen=True)
class CalibrationBudget:
    environment_instance_id: str = SMALL_INSTANCE_ID
    episode_count: int = 1
    max_steps_per_episode: int = 8
    replicate_count: int = 1
    random_schema_seed_count: int = 1
    smoke: bool = False

    def __post_init__(self) -> None:
        _require_positive(self.episode_count, "episode_count")
        _require_positive(self.max_steps_per_episode, "max_steps_per_episode")
        _require_positive(self.replicate_count, "replicate_count")
        _require_positive(self.random_schema_seed_count, "random_schema_seed_count")

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(self)


@dataclass(frozen=True)
class SeriousLearningBudgetLock:
    environment_instance_id: str
    arm_ids: tuple[str, ...]
    episode_count: int
    max_steps_per_episode: int
    replicate_count: int
    random_schema_seed_count: int
    schema_seed_suite: SchemaSeedSuite
    seed_bundle_ids: tuple[str, ...]
    controller_config_id: str
    learner_config_id: str
    linearization_mode_id: str = "tensor_available_disabled"
    artifact_schema_version: str = ARTIFACT_SCHEMA_VERSION
    calibration_artifact_root: str | None = None
    locked_by: str = "unknown"
    locked_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    calibration_only: bool = False

    def __post_init__(self) -> None:
        validate_serious_learning_arm_set(self.arm_ids)
        _require_positive(self.episode_count, "episode_count")
        _require_positive(self.max_steps_per_episode, "max_steps_per_episode")
        _require_positive(self.replicate_count, "replicate_count")
        _require_positive(self.random_schema_seed_count, "random_schema_seed_count")
        if not self.seed_bundle_ids:
            raise ValueError("seed_bundle_ids must be nonempty")
        if self.linearization_mode_id != "tensor_available_disabled":
            raise ValueError("serious learning budget lock requires tensor_available_disabled")
        if self.artifact_schema_version != ARTIFACT_SCHEMA_VERSION:
            raise ValueError("artifact schema version mismatch")
        if not self.calibration_only and self.environment_instance_id != SMALL_INSTANCE_ID:
            raise ValueError("serious learning budget lock must use the small fixture")
        if not self.calibration_only and self.random_schema_seed_count < 2:
            raise ValueError("serious budget lock requires at least two random schema seeds")
        if self.random_schema_seed_count != len(self.schema_seed_suite.schema_seeds):
            raise ValueError("random_schema_seed_count must match schema seed suite")

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(asdict(self))


def default_serious_arm_ids() -> tuple[str, ...]:
    return REQUIRED_SERIOUS_LEARNING_ARM_IDS


def _require_positive(value: int, field_name: str) -> None:
    if value <= 0:
        raise ValueError(f"{field_name} must be positive")
