import pytest

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.counterpoint.instances import (
    SMALL_INSTANCE_ID,
    TINY_INSTANCE_ID,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.arms import (
    REQUIRED_SERIOUS_LEARNING_ARM_IDS,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.budgets import (
    CalibrationBudget,
    SchemaSeedSuite,
    SeedBundleSuite,
    SeriousLearningBudgetLock,
)
from big_boy_benchmarking.seeds.bundles import generate_seed_bundles


def test_calibration_budget_serializes() -> None:
    budget = CalibrationBudget()

    assert budget.to_dict()["environment_instance_id"] == SMALL_INSTANCE_ID
    assert budget.to_dict()["random_schema_seed_count"] == 1


def test_seed_bundle_suite_preserves_separate_seed_types() -> None:
    bundles = generate_seed_bundles(base_seed=123, replicate_count=2)
    suite = SeedBundleSuite(bundles)
    payload = suite.to_dict()

    assert payload["seed_bundle_ids"] == list(suite.seed_bundle_ids)
    assert {
        "environment_seed",
        "schema_seed",
        "learner_seed",
        "controller_seed",
    }.issubset(payload["seed_bundles"][0])


def test_valid_budget_lock_serializes_to_json_safe_dict() -> None:
    bundles = generate_seed_bundles(base_seed=456, replicate_count=2)
    lock = SeriousLearningBudgetLock(
        environment_instance_id=SMALL_INSTANCE_ID,
        arm_ids=REQUIRED_SERIOUS_LEARNING_ARM_IDS,
        episode_count=4,
        max_steps_per_episode=8,
        replicate_count=2,
        random_schema_seed_count=2,
        schema_seed_suite=SchemaSeedSuite((11, 12)),
        seed_bundle_ids=tuple(bundle.seed_bundle_id for bundle in bundles),
        controller_config_id="controller",
        learner_config_id="learner",
        calibration_artifact_root="/private/tmp/calibration",
        locked_by="test",
        locked_at="2026-05-29T00:00:00+00:00",
    )
    payload = lock.to_dict()

    assert payload["artifact_schema_version"] == ARTIFACT_SCHEMA_VERSION
    assert payload["linearization_mode_id"] == "tensor_available_disabled"
    assert payload["schema_seed_suite"]["schema_seeds"] == [11, 12]


def test_budget_lock_rejects_tiny_as_serious_instance() -> None:
    with pytest.raises(ValueError, match="small fixture"):
        SeriousLearningBudgetLock(
            environment_instance_id=TINY_INSTANCE_ID,
            arm_ids=REQUIRED_SERIOUS_LEARNING_ARM_IDS,
            episode_count=1,
            max_steps_per_episode=4,
            replicate_count=1,
            random_schema_seed_count=2,
            schema_seed_suite=SchemaSeedSuite((1, 2)),
            seed_bundle_ids=("seed-a",),
            controller_config_id="controller",
            learner_config_id="learner",
        )


def test_budget_lock_rejects_missing_arm() -> None:
    with pytest.raises(ValueError, match="missing required serious learning arms"):
        SeriousLearningBudgetLock(
            environment_instance_id=SMALL_INSTANCE_ID,
            arm_ids=REQUIRED_SERIOUS_LEARNING_ARM_IDS[:-1],
            episode_count=1,
            max_steps_per_episode=8,
            replicate_count=1,
            random_schema_seed_count=2,
            schema_seed_suite=SchemaSeedSuite((1, 2)),
            seed_bundle_ids=("seed-a",),
            controller_config_id="controller",
            learner_config_id="learner",
        )


def test_single_random_schema_seed_requires_calibration_mark() -> None:
    with pytest.raises(ValueError, match="at least two random schema seeds"):
        SeriousLearningBudgetLock(
            environment_instance_id=SMALL_INSTANCE_ID,
            arm_ids=REQUIRED_SERIOUS_LEARNING_ARM_IDS,
            episode_count=1,
            max_steps_per_episode=8,
            replicate_count=1,
            random_schema_seed_count=1,
            schema_seed_suite=SchemaSeedSuite((1,)),
            seed_bundle_ids=("seed-a",),
            controller_config_id="controller",
            learner_config_id="learner",
        )

    exploratory = SeriousLearningBudgetLock(
        environment_instance_id=TINY_INSTANCE_ID,
        arm_ids=REQUIRED_SERIOUS_LEARNING_ARM_IDS,
        episode_count=1,
        max_steps_per_episode=4,
        replicate_count=1,
        random_schema_seed_count=1,
        schema_seed_suite=SchemaSeedSuite((1,)),
        seed_bundle_ids=("seed-a",),
        controller_config_id="controller",
        learner_config_id="learner",
        calibration_only=True,
    )
    assert exploratory.calibration_only
