import csv
import json
from importlib import import_module
from pathlib import Path

STAGE_BASE = "big_boy_benchmarking.environments.plate_support.standard_gauntlet"

candidate_config = import_module(f"{STAGE_BASE}.candidate_discovery.config")
candidate_runner = import_module(f"{STAGE_BASE}.candidate_discovery.runner")
schema_config = import_module(f"{STAGE_BASE}.contraction_schema_sweep.config")
schema_runner = import_module(f"{STAGE_BASE}.contraction_schema_sweep.runner")
structural_config = import_module(f"{STAGE_BASE}.structural_and_tower_diagnostics.config")
structural_runner = import_module(f"{STAGE_BASE}.structural_and_tower_diagnostics.runner")
training_classification = import_module(f"{STAGE_BASE}.tower_training_health.classification")
training_config = import_module(f"{STAGE_BASE}.tower_training_health.config")
training_runner = import_module(f"{STAGE_BASE}.tower_training_health.runner")

CandidateDiscoveryConfig = candidate_config.CandidateDiscoveryConfig
SchemaSweepConfig = schema_config.SchemaSweepConfig
StructuralDiagnosticsConfig = structural_config.StructuralDiagnosticsConfig
TowerTrainingHealthConfig = training_config.TowerTrainingHealthConfig
RESULT_TABLE_FIELDNAMES = training_runner.RESULT_TABLE_FIELDNAMES
classify_training_health = training_classification.classify_training_health
run_candidate_discovery = candidate_runner.run_candidate_discovery
run_contraction_schema_sweep = schema_runner.run_contraction_schema_sweep
run_structural_and_tower_diagnostics = (
    structural_runner.run_structural_and_tower_diagnostics
)
run_tower_training_health = training_runner.run_tower_training_health


def test_tower_training_health_writes_required_tables_and_trainable_candidate(
    tmp_path: Path,
) -> None:
    candidate_source = _create_stage3_source(tmp_path)
    result = run_tower_training_health(
        TowerTrainingHealthConfig(
            artifact_root=_artifact_root(tmp_path),
            run_label="smoke_001",
            candidate_source_path=candidate_source,
            locked_by="pytest",
            candidate_cap=1,
            training_replicates_per_candidate=1,
            episodes_per_replicate=2,
            max_steps_per_episode=8,
        ),
        repo_root=tmp_path,
    )

    assert result.status == "complete"
    stage_root = result.stage_root
    for table_name, expected_fields in RESULT_TABLE_FIELDNAMES.items():
        table_path = stage_root / "results" / f"{table_name}.csv"
        assert table_path.exists(), table_name
        with table_path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            assert tuple(reader.fieldnames or ()) == expected_fields

    health_rows = _read_csv(stage_root / "results" / "candidate_training_health_summary.csv")
    assert len(health_rows) == 1
    assert health_rows[0]["health_status"] == "trainable_clean"
    assert int(health_rows[0]["concrete_step_count"]) > 0
    assert int(health_rows[0]["lift_success_count"]) > 0
    assert int(health_rows[0]["learner_update_count"]) > 0

    downstream_rows = _read_csv(
        stage_root / "results" / "downstream_comparison_input_summary.csv"
    )
    assert downstream_rows
    assert downstream_rows[0]["stage5_threshold_frontier_calibration"] == "allowed"

    with result.readout_source_path.open(encoding="utf-8") as handle:
        readout_source = json.load(handle)
    assert readout_source["evaluation_id"] == (
        "plate_support_gauntlet_tower_training_health_v001"
    )


def test_tower_training_health_blocks_without_selected_candidate(tmp_path: Path) -> None:
    candidate_source = _create_stage3_source(tmp_path)
    downstream = (
        _artifact_root(tmp_path)
        / "stages"
        / "candidate_discovery"
        / "results"
        / "downstream_training_health_input_summary.csv"
    )
    with downstream.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "candidate_id",
                "schema_id",
                "schema_family_id",
                "schema_seed",
                "selection_status",
                "allowed_downstream_stage",
                "source_artifact_root",
            ]
        )

    result = run_tower_training_health(
        TowerTrainingHealthConfig(
            artifact_root=_artifact_root(tmp_path),
            run_label="smoke_001",
            candidate_source_path=candidate_source,
            locked_by="pytest",
            candidate_cap=1,
            training_replicates_per_candidate=1,
            episodes_per_replicate=1,
            max_steps_per_episode=2,
        ),
        repo_root=tmp_path,
    )

    assert result.status == "blocked"
    assert "no selected training candidate" in str(result.failure_reason)


def test_tower_training_health_can_train_iterated_source_local_candidate(
    tmp_path: Path,
) -> None:
    candidate_source = _create_iterated_stage3_source(tmp_path)
    result = run_tower_training_health(
        TowerTrainingHealthConfig(
            artifact_root=_artifact_root(tmp_path),
            run_label="iterated_001",
            candidate_source_path=candidate_source,
            locked_by="pytest",
            candidate_cap=1,
            training_replicates_per_candidate=1,
            episodes_per_replicate=1,
            max_steps_per_episode=4,
        ),
        repo_root=tmp_path,
    )

    assert result.status == "complete"
    with (result.stage_root / "candidate_manifest.json").open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    candidate = manifest["candidates"][0]
    assert candidate["schema_mode"] == "source_local_ratio_iterated"
    assert candidate["ratio_denominator"] == 144
    assert candidate["max_iterations"] == 32
    assert candidate["nontrivial_tier_count"] >= 3

    health_rows = _read_csv(
        result.stage_root / "results" / "candidate_training_health_summary.csv"
    )
    assert health_rows[0]["schema_mode"] == "source_local_ratio_iterated"
    assert health_rows[0]["health_status"] in {
        "trainable_clean",
        "trainable_warning",
    }
    assert int(health_rows[0]["concrete_step_count"]) > 0
    assert int(health_rows[0]["lift_success_count"]) > 0


def test_training_health_classifier_distinguishes_failure_modes() -> None:
    clean = {
        "runtime_failure_count": 0,
        "artifact_complete": 1,
        "concrete_step_count": 1,
        "lift_success_count": 1,
        "learner_update_count": 1,
        "blocked_controller_step_count": 0,
    }

    assert classify_training_health(clean)[0] == "trainable_clean"
    assert (
        classify_training_health({**clean, "blocked_controller_step_count": 1})[0]
        == "trainable_warning"
    )
    assert (
        classify_training_health({**clean, "runtime_failure_count": 1})[0]
        == "untrainable_runtime_failure"
    )
    assert (
        classify_training_health({**clean, "artifact_complete": 0})[0]
        == "artifact_incomplete"
    )
    assert (
        classify_training_health({**clean, "concrete_step_count": 0})[0]
        == "untrainable_no_concrete_steps"
    )
    assert (
        classify_training_health({**clean, "lift_success_count": 0})[0]
        == "untrainable_no_lift_success"
    )
    assert (
        classify_training_health({**clean, "learner_update_count": 0})[0]
        == "untrainable_no_learner_updates"
    )


def _create_stage3_source(repo_root: Path) -> Path:
    schema_sweep_source = _create_stage2_source(repo_root)
    result = run_candidate_discovery(
        CandidateDiscoveryConfig(
            artifact_root=_artifact_root(repo_root),
            run_label="smoke_001",
            schema_sweep_source_path=schema_sweep_source,
            locked_by="pytest",
        ),
        repo_root=repo_root,
    )
    assert result.status == "complete"
    return result.readout_source_path


def _create_iterated_stage3_source(repo_root: Path) -> Path:
    schema_sweep_source = _create_iterated_stage2_source(repo_root)
    result = run_candidate_discovery(
        CandidateDiscoveryConfig(
            artifact_root=_artifact_root(repo_root),
            run_label="iterated_001",
            schema_sweep_source_path=schema_sweep_source,
            locked_by="pytest",
        ),
        repo_root=repo_root,
    )
    assert result.status == "complete"
    downstream_rows = _read_csv(
        result.stage_root / "results" / "downstream_training_health_input_summary.csv"
    )
    assert downstream_rows[0]["schema_mode"] == "source_local_ratio_iterated"
    return result.readout_source_path


def _create_stage2_source(repo_root: Path) -> Path:
    stage1_source = _create_stage1_source(repo_root)
    result = run_contraction_schema_sweep(
        SchemaSweepConfig(
            artifact_root=_artifact_root(repo_root),
            run_label="smoke_001",
            stage1_readout_source_path=stage1_source,
            locked_by="pytest",
            tower_probe_steps=3,
            tower_probe_sample_size=4,
        ),
        repo_root=repo_root,
    )
    assert result.status == "complete"
    return result.readout_source_path


def _create_iterated_stage2_source(repo_root: Path) -> Path:
    stage1_source = _create_stage1_source(repo_root)
    result = run_contraction_schema_sweep(
        SchemaSweepConfig(
            artifact_root=_artifact_root(repo_root),
            run_label="iterated_001",
            stage1_readout_source_path=stage1_source,
            locked_by="pytest",
            schema_families=("source_local_ratio_iterated",),
            schema_seeds=(0,),
            iterated_source_local_ratio_denominators=(144,),
            iterated_source_local_max_iterations=32,
            tower_probe_steps=3,
            tower_probe_sample_size=4,
        ),
        repo_root=repo_root,
    )
    assert result.status == "complete"
    return result.readout_source_path


def _create_stage1_source(repo_root: Path) -> Path:
    readiness_source = _write_fake_readiness_source(repo_root)
    result = run_structural_and_tower_diagnostics(
        StructuralDiagnosticsConfig(
            artifact_root=_artifact_root(repo_root),
            run_label="smoke_001",
            readiness_source_path=readiness_source,
            locked_by="pytest",
            random_policy_episode_count=3,
            tower_probe_steps=3,
            tower_probe_sample_size=4,
        ),
        repo_root=repo_root,
    )
    assert result.status == "complete"
    return result.readout_source_path


def _write_fake_readiness_source(repo_root: Path) -> Path:
    (repo_root / "pyproject.toml").write_text("[project]\nname = 'fake-bbb'\n", encoding="utf-8")
    artifact_root = (
        repo_root
        / "docs"
        / "environments"
        / "plate_support_5x5_default_v001"
        / "readiness"
        / "dev_001"
    )
    artifact_root.mkdir(parents=True, exist_ok=True)
    environment_doc = repo_root / "docs" / "environments" / "plate_support_5x5_default_v001.md"
    environment_doc.parent.mkdir(parents=True, exist_ok=True)
    environment_doc.write_text("# fake env doc\n", encoding="utf-8")
    summary = artifact_root / "runs" / "plate_support_environment_readiness_v001" / "summaries"
    summary.mkdir(parents=True, exist_ok=True)
    summary_path = summary / "summary.json"
    summary_path.write_text("{}", encoding="utf-8")
    source = artifact_root / "readout_source.json"
    source.write_text(
        json.dumps(
            {
                "artifact_root": str(artifact_root),
                "environment_doc": str(environment_doc),
                "environment_family_id": "plate_support",
                "environment_instance_id": "plate_support_5x5_default_v001",
                "run_family_summary": str(summary_path),
                "source_type": "environment_readiness",
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return source


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


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))
