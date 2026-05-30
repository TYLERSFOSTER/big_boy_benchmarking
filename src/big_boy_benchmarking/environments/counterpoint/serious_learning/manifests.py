"""Evaluation-level manifests for serious counterpoint learning."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from big_boy_benchmarking.artifacts.manifests import to_json_dict
from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.instances import SMALL_INSTANCE_ID
from big_boy_benchmarking.environments.counterpoint.serious_learning.arms import (
    SeriousLearningArm,
    iter_serious_learning_arms,
)

BLUEPRINT_PATH = (
    "docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/"
    "01_001_counterpoint_first_serious_learning_evaluation_blueprint.md"
)


@dataclass(frozen=True)
class SeriousLearningEvaluationManifest:
    evaluation_id: str = "counterpoint_first_serious_learning_v001"
    environment_family_id: str = ids.ENVIRONMENT_FAMILY_ID
    environment_instance_id: str = SMALL_INSTANCE_ID
    blueprint_path: str = BLUEPRINT_PATH
    artifact_schema_version: str = ARTIFACT_SCHEMA_VERSION
    claim_boundary: str = (
        "first serious counterpoint learning/control evaluation; no tensor-enabled, "
        "CUDA, music-quality, or general superiority claim"
    )
    linearization_mode_id: str = "tensor_available_disabled"

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(self)


@dataclass(frozen=True)
class SeriousLearningArmManifest:
    evaluation_id: str = "counterpoint_first_serious_learning_v001"
    arms: tuple[SeriousLearningArm, ...] = field(default_factory=iter_serious_learning_arms)
    artifact_schema_version: str = ARTIFACT_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(
            {
                "evaluation_id": self.evaluation_id,
                "arms": [arm.to_dict() for arm in self.arms],
                "artifact_schema_version": self.artifact_schema_version,
            }
        )


@dataclass(frozen=True)
class CalibrationSummary:
    evaluation_id: str
    status: str
    arm_count: int
    run_count: int
    measured_runtime_seconds: float
    artifact_bytes: int
    curve_noise_proxy: float | None
    completion_rate: float | None
    lift_failure_rate: float | None
    random_schema_variability: float | None

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(self)


@dataclass(frozen=True)
class CalibrationRecommendation:
    evaluation_id: str
    measured_summary: CalibrationSummary
    proposed_episode_count: int
    proposed_replicate_count: int
    proposed_random_schema_seed_count: int
    rationale: str
    status: str = "proposed"

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(asdict(self))


@dataclass(frozen=True)
class AggregateSummary:
    evaluation_id: str
    status: str
    arm_count: int
    complete_arm_count: int
    baseline_arm_id: str
    empty_tower_baseline_arm_id: str
    table_path: str
    result_paths: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(self)
