from pathlib import Path

from big_boy_benchmarking.environments.counterpoint.serious_learning.evaluation_paths import (
    build_serious_learning_evaluation_paths,
)


def test_serious_learning_paths_resolve_under_artifact_root(tmp_path) -> None:
    paths = build_serious_learning_evaluation_paths(tmp_path)

    required = [
        paths.evaluation_manifest,
        paths.evaluation_arm_manifest,
        paths.evaluation_run_index_csv,
        paths.evaluation_budget_lock,
        paths.evaluation_aggregate_summary,
        paths.evaluation_aggregate_table_csv,
        paths.calibration_summary,
        paths.calibration_run_index_csv,
        paths.calibration_recommendation_md,
        paths.docs_dir,
        paths.results_dir,
    ]

    assert paths.root == tmp_path / "evaluations" / "counterpoint_first_serious_learning_v001"
    assert all(Path(path).is_relative_to(tmp_path) for path in required)


def test_serious_learning_path_construction_is_deterministic(tmp_path) -> None:
    first = build_serious_learning_evaluation_paths(tmp_path, evaluation_id="eval")
    second = build_serious_learning_evaluation_paths(tmp_path, evaluation_id="eval")

    assert first == second
    assert first.evaluation_manifest.name == "evaluation_manifest.json"
    assert first.results_dir.name == "results"
