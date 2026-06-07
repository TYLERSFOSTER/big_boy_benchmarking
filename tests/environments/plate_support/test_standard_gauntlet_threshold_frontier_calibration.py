import csv
import json
from importlib import import_module
from pathlib import Path

STAGE_BASE = "big_boy_benchmarking.environments.plate_support.standard_gauntlet"

threshold_config = import_module(f"{STAGE_BASE}.threshold_frontier_calibration.config")
threshold_runner = import_module(f"{STAGE_BASE}.threshold_frontier_calibration.runner")

ThresholdFrontierCalibrationConfig = threshold_config.ThresholdFrontierCalibrationConfig
RESULT_TABLE_FIELDNAMES = threshold_runner.RESULT_TABLE_FIELDNAMES
run_threshold_frontier_calibration = threshold_runner.run_threshold_frontier_calibration


def test_threshold_calibration_writes_required_tables_and_binary_target(
    tmp_path: Path,
) -> None:
    training_source = _write_stage_sources(tmp_path)

    result = run_threshold_frontier_calibration(
        ThresholdFrontierCalibrationConfig(
            artifact_root=_artifact_root(tmp_path),
            run_label="smoke_001",
            training_health_source_path=training_source,
            locked_by="pytest",
        ),
        repo_root=tmp_path,
    )

    assert result.status == "complete"
    assert result.recommended_target_policy_id == "plate_support_binary_goal_success_v001"
    for table_name, expected_fields in RESULT_TABLE_FIELDNAMES.items():
        table_path = result.stage_root / "results" / f"{table_name}.csv"
        assert table_path.exists(), table_name
        with table_path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            assert tuple(reader.fieldnames or ()) == expected_fields

    target_rows = _read_csv(result.stage_root / "results" / "recommended_comparison_target.csv")
    assert len(target_rows) == 1
    assert target_rows[0]["target_type"] == "binary_success"
    assert target_rows[0]["calibration_status"] == "threshold_calibrated"

    downstream_rows = _read_csv(
        result.stage_root / "results" / "downstream_paired_comparison_input_summary.csv"
    )
    assert downstream_rows[0]["stage6_paired_replicate_comparison"] == "allowed"


def test_threshold_calibration_blocks_without_trainable_candidate(tmp_path: Path) -> None:
    training_source = _write_stage_sources(tmp_path, health_status="untrainable_no_lift_success")

    result = run_threshold_frontier_calibration(
        ThresholdFrontierCalibrationConfig(
            artifact_root=_artifact_root(tmp_path),
            run_label="smoke_001",
            training_health_source_path=training_source,
            locked_by="pytest",
        ),
        repo_root=tmp_path,
    )

    assert result.status == "blocked"
    assert "no trainable candidate" in str(result.failure_reason)


def test_threshold_calibration_records_window_blocks_and_threshold_provenance(
    tmp_path: Path,
) -> None:
    training_source = _write_stage_sources(tmp_path)

    result = run_threshold_frontier_calibration(
        ThresholdFrontierCalibrationConfig(
            artifact_root=_artifact_root(tmp_path),
            run_label="smoke_001",
            training_health_source_path=training_source,
            locked_by="pytest",
            sustained_windows=((4, 5),),
        ),
        repo_root=tmp_path,
    )

    sustained_rows = _read_csv(
        result.stage_root / "results" / "sustained_hit_feasibility_summary.csv"
    )
    assert sustained_rows[0]["feasibility_status"] == "blocked_window_exceeds_budget"

    threshold_rows = _read_csv(
        result.stage_root / "results" / "threshold_grid_construction.csv"
    )
    assert threshold_rows
    assert all(row["construction_reason"] for row in threshold_rows)
    assert all(row["source_metric"] for row in threshold_rows)


def _write_stage_sources(
    repo_root: Path,
    *,
    health_status: str = "trainable_clean",
) -> Path:
    (repo_root / "pyproject.toml").write_text("[project]\nname = 'fake-bbb'\n", encoding="utf-8")
    stage1_source = _write_stage1_source(repo_root)
    stage4_source = _write_stage4_source(repo_root, health_status=health_status)
    assert stage1_source.exists()
    return stage4_source


def _write_stage1_source(repo_root: Path) -> Path:
    readout_surface = (
        repo_root
        / "docs"
        / "evaluations"
        / "plate_support_5x5_default_v001"
        / "standard_gauntlet"
        / "structural_and_tower_diagnostics"
    )
    artifact_root = (
        repo_root
        / "docs"
        / "evaluations"
        / "plate_support_5x5_default_v001"
        / "standard_gauntlet"
        / "artifacts"
        / "smoke_001"
        / "stages"
        / "structural_and_tower_diagnostics"
    )
    results = artifact_root / "results"
    results.mkdir(parents=True, exist_ok=True)
    _write_csv(
        results / "shortest_path_summary.csv",
        ("shortest_path_length", "total_shortest_path_reward"),
        [{"shortest_path_length": 6, "total_shortest_path_reward": 95.0}],
    )
    _write_csv(
        results / "random_policy_recon_summary.csv",
        (
            "max_steps_per_episode",
            "success_rate",
            "mean_total_reward",
            "invalid_move_rate",
        ),
        [
            {
                "max_steps_per_episode": 50,
                "success_rate": 0.024,
                "mean_total_reward": -105.748,
                "invalid_move_rate": 0.452,
            }
        ],
    )
    _write_csv(
        results / "state_space_summary.csv",
        ("valid_state_count", "reachable_state_count"),
        [{"valid_state_count": 89, "reachable_state_count": 89}],
    )
    _write_csv(
        results / "transition_summary.csv",
        ("valid_transition", "invalid_move", "valid_self_transition"),
        [
            {"valid_transition": "True", "invalid_move": "False", "valid_self_transition": "False"},
            {"valid_transition": "False", "invalid_move": "True", "valid_self_transition": "False"},
            {"valid_transition": "True", "invalid_move": "False", "valid_self_transition": "True"},
        ],
    )
    source = readout_surface / "readout_source.json"
    source.parent.mkdir(parents=True, exist_ok=True)
    _write_json(
        source,
        {
            "evaluation_id": "plate_support_gauntlet_structural_tower_diagnostics_v001",
            "repo_readout_surface": str(readout_surface),
            "source_artifact_root": str(artifact_root),
            "source_files": {
                "shortest_path_summary": str(results / "shortest_path_summary.csv"),
                "random_policy_recon_summary": str(results / "random_policy_recon_summary.csv"),
                "state_space_summary": str(results / "state_space_summary.csv"),
                "transition_summary": str(results / "transition_summary.csv"),
            },
        },
    )
    return source


def _write_stage4_source(repo_root: Path, *, health_status: str) -> Path:
    readout_surface = (
        repo_root
        / "docs"
        / "evaluations"
        / "plate_support_5x5_default_v001"
        / "standard_gauntlet"
        / "tower_training_health"
    )
    artifact_root = _artifact_root(repo_root) / "stages" / "tower_training_health"
    results = artifact_root / "results"
    results.mkdir(parents=True, exist_ok=True)
    candidate_id = "plate_support_candidate:source_local_ratio:0:abc"
    schema_id = "plate_support_schema_source_local_ratio_001_over_018_v001"
    _write_csv(
        results / "training_episode_summary.csv",
        (
            "candidate_id",
            "schema_id",
            "run_id",
            "replicate_index",
            "episode_index",
            "episode_seed",
            "status",
            "step_count",
            "total_reward",
            "terminated",
            "truncated",
            "goal_reached",
            "blocked_reason",
        ),
        [
            _episode_row(candidate_id, schema_id, 0, 0, 0, 34, 67.0, True),
            _episode_row(candidate_id, schema_id, 0, 1, 1, 50, -50.0, False),
            _episode_row(candidate_id, schema_id, 0, 2, 2, 50, -50.0, False),
            _episode_row(candidate_id, schema_id, 0, 3, 3, 12, 89.0, True),
        ],
    )
    _write_csv(
        results / "training_curve_summary.csv",
        (
            "candidate_id",
            "schema_id",
            "episode_index",
            "episode_count",
            "mean_total_reward",
            "success_rate",
            "mean_step_count",
        ),
        [
            {
                "candidate_id": candidate_id,
                "schema_id": schema_id,
                "episode_index": 0,
                "episode_count": 1,
                "mean_total_reward": 67.0,
                "success_rate": 1.0,
                "mean_step_count": 34,
            }
        ],
    )
    _write_csv(
        results / "concrete_step_summary.csv",
        (
            "candidate_id",
            "schema_id",
            "run_count",
            "concrete_step_count",
            "valid_step_count",
            "invalid_move_count",
            "self_transition_count",
            "terminal_step_count",
        ),
        [
            {
                "candidate_id": candidate_id,
                "schema_id": schema_id,
                "run_count": 1,
                "concrete_step_count": 146,
                "valid_step_count": 146,
                "invalid_move_count": 0,
                "self_transition_count": 0,
                "terminal_step_count": 2,
            }
        ],
    )
    _write_csv(
        results / "candidate_training_health_summary.csv",
        (
            "candidate_id",
            "schema_id",
            "episode_count",
            "success_count",
            "concrete_step_count",
            "lift_success_count",
            "learner_update_count",
            "runtime_failure_count",
            "blocked_controller_step_count",
            "artifact_complete",
            "health_status",
            "health_reason",
        ),
        [
            {
                "candidate_id": candidate_id,
                "schema_id": schema_id,
                "episode_count": 4,
                "success_count": 2,
                "concrete_step_count": 146,
                "lift_success_count": 146,
                "learner_update_count": 146,
                "runtime_failure_count": 0,
                "blocked_controller_step_count": 0,
                "artifact_complete": 1,
                "health_status": health_status,
                "health_reason": "synthetic test row",
            }
        ],
    )
    _write_csv(
        results / "downstream_comparison_input_summary.csv",
        (
            "candidate_id",
            "schema_id",
            "health_status",
            "allowed_downstream_stage",
            "stage5_threshold_frontier_calibration",
            "stage6_paired_replicate_comparison",
            "source_artifact_root",
        ),
        [
            {
                "candidate_id": candidate_id,
                "schema_id": schema_id,
                "health_status": health_status,
                "allowed_downstream_stage": "stage5_threshold_frontier_calibration",
                "stage5_threshold_frontier_calibration": "allowed",
                "stage6_paired_replicate_comparison": "allowed_after_stage5",
                "source_artifact_root": str(artifact_root),
            }
        ],
    )
    source = readout_surface / "readout_source.json"
    source.parent.mkdir(parents=True, exist_ok=True)
    source_files = {
        "training_episode_summary": str(results / "training_episode_summary.csv"),
        "training_curve_summary": str(results / "training_curve_summary.csv"),
        "concrete_step_summary": str(results / "concrete_step_summary.csv"),
        "candidate_training_health_summary": str(
            results / "candidate_training_health_summary.csv"
        ),
        "downstream_comparison_input_summary": str(
            results / "downstream_comparison_input_summary.csv"
        ),
    }
    _write_json(
        source,
        {
            "evaluation_id": "plate_support_gauntlet_tower_training_health_v001",
            "repo_readout_surface": str(readout_surface),
            "source_artifact_root": str(artifact_root),
            "source_files": source_files,
        },
    )
    return source


def _episode_row(
    candidate_id: str,
    schema_id: str,
    replicate_index: int,
    episode_index: int,
    episode_seed: int,
    step_count: int,
    total_reward: float,
    goal_reached: bool,
) -> dict[str, object]:
    return {
        "candidate_id": candidate_id,
        "schema_id": schema_id,
        "run_id": f"run-{replicate_index}",
        "replicate_index": replicate_index,
        "episode_index": episode_index,
        "episode_seed": episode_seed,
        "status": "complete",
        "step_count": step_count,
        "total_reward": total_reward,
        "terminated": str(goal_reached),
        "truncated": str(not goal_reached),
        "goal_reached": str(goal_reached),
        "blocked_reason": "",
    }


def _artifact_root(repo_root: Path) -> Path:
    return (
        repo_root
        / "docs"
        / "evaluations"
        / "plate_support_5x5_default_v001"
        / "standard_gauntlet"
        / "artifacts"
        / "smoke_001"
    )


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
