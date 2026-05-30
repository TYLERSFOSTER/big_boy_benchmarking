import csv
from pathlib import Path

import pytest

from big_boy_benchmarking.environments.counterpoint.instances import (
    SMALL_INSTANCE_ID,
    TINY_INSTANCE_ID,
    default_tiny_spec,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.arms import (
    REQUIRED_SERIOUS_LEARNING_ARM_IDS,
    get_serious_learning_arm,
    iter_serious_learning_arms,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.budgets import (
    CalibrationBudget,
    SchemaSeedSuite,
    SeedBundleSuite,
    SeriousLearningBudgetLock,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.runner import (
    dispatch_serious_learning_arm,
    expand_arm_seed_work,
    run_budget_locked_serious_learning,
    run_calibration,
)
from big_boy_benchmarking.seeds.bundles import generate_seed_bundles


def test_arm_dispatch_sends_direct_and_tower_arms_to_expected_runner_kind(tmp_path) -> None:
    seed_bundle = generate_seed_bundles(base_seed=31, replicate_count=1)[0]
    direct = dispatch_serious_learning_arm(
        arm=get_serious_learning_arm("direct_masked_random"),
        spec=default_tiny_spec(),
        seed_bundle=seed_bundle,
        artifact_root=tmp_path / "direct",
        schema_seed=None,
        episode_count=1,
        max_steps_per_episode=4,
    )
    tower = dispatch_serious_learning_arm(
        arm=get_serious_learning_arm("tower_empty_exploit_explore_tabular_q"),
        spec=default_tiny_spec(),
        seed_bundle=seed_bundle,
        artifact_root=tmp_path / "tower",
        schema_seed=None,
        episode_count=1,
        max_steps_per_episode=4,
    )

    assert "direct_masked_random" in direct.run_id
    assert "tower_empty_exploit_explore_tabular_q" in tower.run_id
    assert "control_events_csv" in tower.artifact_paths


def test_random_schema_arms_expand_over_schema_seed_suite() -> None:
    seed_bundles = generate_seed_bundles(base_seed=32, replicate_count=2)
    work = expand_arm_seed_work(
        seed_bundles=seed_bundles,
        schema_seed_suite=SchemaSeedSuite((101, 102, 103)),
    )
    random_work = [
        item for item in work if item[0].arm_id.startswith("tower_random")
    ]

    assert len(random_work) == 2 * 2 * 3
    assert {schema_seed for _, _, schema_seed in random_work} == {101, 102, 103}


def test_run_ids_are_stable_for_same_arm_and_seed(tmp_path) -> None:
    seed_bundle = generate_seed_bundles(base_seed=33, replicate_count=1)[0]
    arm = get_serious_learning_arm("direct_tabular_q")

    first = dispatch_serious_learning_arm(
        arm=arm,
        spec=default_tiny_spec(),
        seed_bundle=seed_bundle,
        artifact_root=tmp_path / "first",
        schema_seed=None,
        episode_count=1,
        max_steps_per_episode=4,
    )
    second = dispatch_serious_learning_arm(
        arm=arm,
        spec=default_tiny_spec(),
        seed_bundle=seed_bundle,
        artifact_root=tmp_path / "second",
        schema_seed=None,
        episode_count=1,
        max_steps_per_episode=4,
    )

    assert first.run_id == second.run_id


def test_tiny_calibration_path_requires_smoke_mark_and_writes_artifacts(tmp_path) -> None:
    with pytest.raises(ValueError, match="explicitly marked smoke"):
        run_calibration(
            artifact_root=tmp_path / "bad",
            budget=CalibrationBudget(environment_instance_id=TINY_INSTANCE_ID),
        )

    result = run_calibration(
        artifact_root=tmp_path / "ok",
        budget=CalibrationBudget(
            environment_instance_id=TINY_INSTANCE_ID,
            episode_count=1,
            max_steps_per_episode=4,
            replicate_count=1,
            random_schema_seed_count=1,
            smoke=True,
        ),
    )

    assert result["status"] == "smoke_non_evidence"
    assert Path(result["calibration_summary"]).exists()
    assert Path(result["calibration_recommendation"]).exists()
    rows = list(
        csv.DictReader(
            (
                tmp_path
                / "ok"
                / "evaluations"
                / "counterpoint_first_serious_learning_v001"
                / "calibration_run_index.csv"
            ).open()
        )
    )
    assert {row["arm_id"] for row in rows} == set(REQUIRED_SERIOUS_LEARNING_ARM_IDS)


def test_budget_locked_run_validation_and_execution(tmp_path) -> None:
    seed_bundles = generate_seed_bundles(base_seed=34, replicate_count=2)
    lock = SeriousLearningBudgetLock(
        environment_instance_id=SMALL_INSTANCE_ID,
        arm_ids=tuple(arm.arm_id for arm in iter_serious_learning_arms()),
        episode_count=1,
        max_steps_per_episode=4,
        replicate_count=2,
        random_schema_seed_count=2,
        schema_seed_suite=SchemaSeedSuite((1, 2)),
        seed_bundle_ids=tuple(bundle.seed_bundle_id for bundle in seed_bundles),
        controller_config_id="controller",
        learner_config_id="learner",
    )

    with pytest.raises(ValueError, match="seed bundle suite ids"):
        run_budget_locked_serious_learning(
            artifact_root=tmp_path / "bad",
            budget_lock=lock,
            seed_bundle_suite=SeedBundleSuite(seed_bundles[:1]),
        )

    result = run_budget_locked_serious_learning(
        artifact_root=tmp_path / "ok",
        budget_lock=lock,
        seed_bundle_suite=SeedBundleSuite(seed_bundles),
    )

    assert result["status"] in {"complete", "incomplete"}
    assert Path(result["evaluation_run_index"]).exists()
