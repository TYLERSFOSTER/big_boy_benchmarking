from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.serious_learning.manifests import (
    AggregateSummary,
    CalibrationRecommendation,
    CalibrationSummary,
    SeriousLearningArmManifest,
    SeriousLearningEvaluationManifest,
)


def test_evaluation_manifest_records_blueprint_and_schema_version() -> None:
    payload = SeriousLearningEvaluationManifest().to_dict()

    assert payload["artifact_schema_version"] == ARTIFACT_SCHEMA_VERSION
    assert payload["blueprint_path"].endswith(
        "01_001_counterpoint_first_serious_learning_evaluation_blueprint.md"
    )
    assert payload["environment_family_id"] == ids.ENVIRONMENT_FAMILY_ID


def test_arm_manifest_preserves_mode_and_schema_ids() -> None:
    payload = SeriousLearningArmManifest().to_dict()
    arms = {arm["arm_id"]: arm for arm in payload["arms"]}

    assert len(arms) == 7
    assert arms["tower_motion_exploit_explore_tabular_q"]["mode_id"] == "tower_exploit_explore"
    assert (
        arms["tower_motion_exploit_explore_tabular_q"]["schema_id"]
        == ids.STRUCTURED_MOTION_SCHEMA_ID
    )


def test_calibration_recommendation_records_measured_summary_and_budget() -> None:
    summary = CalibrationSummary(
        evaluation_id="eval",
        status="complete",
        arm_count=7,
        run_count=7,
        measured_runtime_seconds=1.5,
        artifact_bytes=1024,
        curve_noise_proxy=0.1,
        completion_rate=1.0,
        lift_failure_rate=0.0,
        random_schema_variability=0.2,
    )
    recommendation = CalibrationRecommendation(
        evaluation_id="eval",
        measured_summary=summary,
        proposed_episode_count=16,
        proposed_replicate_count=4,
        proposed_random_schema_seed_count=3,
        rationale="measured budget is affordable",
    )

    payload = recommendation.to_dict()

    assert payload["measured_summary"]["arm_count"] == 7
    assert payload["proposed_random_schema_seed_count"] == 3


def test_aggregate_summary_serializes_result_paths() -> None:
    payload = AggregateSummary(
        evaluation_id="eval",
        status="complete",
        arm_count=7,
        complete_arm_count=7,
        baseline_arm_id="direct_tabular_q",
        empty_tower_baseline_arm_id="tower_empty_exploit_explore_tabular_q",
        table_path="evaluation_aggregate_table.csv",
        result_paths=("results/learning_curves.csv",),
    ).to_dict()

    assert payload["baseline_arm_id"] == "direct_tabular_q"
    assert payload["result_paths"] == ["results/learning_curves.csv"]
