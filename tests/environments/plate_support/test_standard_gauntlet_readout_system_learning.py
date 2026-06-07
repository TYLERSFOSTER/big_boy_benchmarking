import csv
import json
from importlib import import_module
from pathlib import Path

import pytest

STAGE_BASE = "big_boy_benchmarking.environments.plate_support.standard_gauntlet"

readout_config = import_module(f"{STAGE_BASE}.readout_system_learning.config")
readout_runner = import_module(f"{STAGE_BASE}.readout_system_learning.runner")

ReadoutSystemLearningConfig = readout_config.ReadoutSystemLearningConfig
build_readout_system_learning = readout_runner.build_readout_system_learning


def test_readout_build_requires_explicit_readout_source_name() -> None:
    with pytest.raises(ValueError, match="readout_source.json"):
        ReadoutSystemLearningConfig(readout_source_path=Path("README.md"))


def test_readout_build_generates_suite_docs_and_preserves_turns(tmp_path: Path) -> None:
    source = _write_suite_fixture(tmp_path)
    readme = source.parent / "README.md"
    readme.write_text(
        "\n".join(
            [
                "# Existing",
                "",
                "## Clarifying Turns",
                "",
                "### Evaluator Turn 1",
                "",
                "This is a real evaluator note.",
                "",
                "### Codex Turn 1",
                "",
                "This is a real Codex reply.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    result = build_readout_system_learning(ReadoutSystemLearningConfig(source))

    assert result.status == "complete"
    assert result.suite_status == "complete_limited_signal"
    generated = readme.read_text(encoding="utf-8")
    assert "paired_comparison_negative_signal" in generated
    assert "![Suite: Limited Signal](badges/suite_status.svg)" in generated
    assert "![Paired: Negative Signal](badges/paired_comparison.svg)" in generated
    assert "![Suite: complete_limited_signal]" not in generated
    assert "| 7 | readout_and_system_learning | complete | readout_complete |" in generated
    assert "This is a real evaluator note." in generated
    assert (source.parent / "badges" / "suite_status.svg").exists()
    suite_badge = (source.parent / "badges" / "suite_status.svg").read_text(encoding="utf-8")
    assert 'height="20"' in suite_badge
    assert 'fill="#555"' in suite_badge
    assert "Limited Signal" in suite_badge

    stage_status_rows = _read_csv(source.parent / "results" / "stage_status_summary.csv")
    assert stage_status_rows[-1]["claim_status"] == "readout_complete"

    updated_source = json.loads(source.read_text(encoding="utf-8"))
    assert updated_source["run_mode"] == "smoke_stage_1_to_7_readout_complete"
    assert updated_source["expected_files"]["pending_not_yet_run"] == []
    assert "Stage 7" in updated_source["claim_boundary"][0]

    parent_status_rows = _read_csv(
        source.parent
        / "artifacts"
        / "smoke_001"
        / "evaluations"
        / "plate_support_standard_gauntlet_v001"
        / "stage_status_summary.csv"
    )
    assert parent_status_rows[-1]["stage_id"] == (
        "plate_support_gauntlet_readout_system_learning_v001"
    )


def _write_suite_fixture(repo_root: Path) -> Path:
    (repo_root / "pyproject.toml").write_text("[project]\nname='fake-bbb'\n", encoding="utf-8")
    (repo_root / "src").mkdir()
    surface = (
        repo_root
        / "docs"
        / "evaluations"
        / "plate_support_5x5_default_v001"
        / "standard_gauntlet"
    )
    suite_eval = (
        surface
        / "artifacts"
        / "smoke_001"
        / "evaluations"
        / "plate_support_standard_gauntlet_v001"
    )
    suite_eval.mkdir(parents=True)
    stage_sources = _write_stage_sources(surface)
    _write_csv(
        suite_eval / "stage_status_summary.csv",
        (
            "suite_id",
            "stage_id",
            "environment_family_id",
            "environment_instance_id",
            "artifact_root",
            "status",
            "claim_status",
            "claim_boundary",
            "source_stage_ids",
            "source_artifact_paths",
            "linearization_mode_id",
            "state_collapser_dependency_status",
        ),
        [
            _stage_status_row(surface, "structural_tower_diagnostics", 1, "diagnostic_complete"),
            _stage_status_row(surface, "contraction_schema_sweep", 2, "diagnostic_complete"),
            _stage_status_row(surface, "candidate_discovery", 3, "candidate_found"),
            _stage_status_row(surface, "tower_training_health", 4, "trainable_clean"),
            _stage_status_row(surface, "threshold_frontier_calibration", 5, "threshold_calibrated"),
            _stage_status_row(
                surface,
                "paired_replicate_comparison",
                6,
                "paired_comparison_negative_signal",
            ),
        ],
    )
    _write_csv(
        suite_eval / "stage_run_index.csv",
        ("suite_id", "stage_id", "run_label", "artifact_root", "status"),
        [],
    )
    source = surface / "readout_source.json"
    _write_json(
        source,
        {
            "artifact_schema_version": "bbb.v001",
            "source_binding_type": "evaluation_readout_source",
            "repo_readout_surface": str(surface),
            "source_artifact_root": str(surface / "artifacts" / "smoke_001"),
            "source_evaluation_root": str(suite_eval),
            "evaluation_id": "plate_support_standard_gauntlet_v001",
            "environment_family_id": "plate_support",
            "environment_instance_id": "plate_support_5x5_default_v001",
            "artifact_run_label": "smoke_001",
            "source_files": {
                "aggregate_table": str(suite_eval / "stage_status_summary.csv"),
                "run_index": str(suite_eval / "stage_run_index.csv"),
            },
            "expected_files": {
                "pending_not_yet_run": [
                    "stage_status_summary.csv",
                    "stage_run_index.csv",
                ],
            },
            "stage_readout_source_paths": [str(path) for path in stage_sources],
        },
    )
    return source


def _write_stage_sources(surface: Path) -> list[Path]:
    stage_ids = [
        (
            "structural_and_tower_diagnostics",
            "plate_support_gauntlet_structural_tower_diagnostics_v001",
        ),
        ("contraction_schema_sweep", "plate_support_gauntlet_contraction_schema_sweep_v001"),
        ("candidate_discovery", "plate_support_gauntlet_candidate_discovery_v001"),
        ("tower_training_health", "plate_support_gauntlet_tower_training_health_v001"),
        (
            "threshold_frontier_calibration",
            "plate_support_gauntlet_threshold_frontier_calibration_v001",
        ),
        ("paired_replicate_comparison", "plate_support_gauntlet_paired_replicate_comparison_v001"),
    ]
    paths = []
    for short_name, stage_id in stage_ids:
        readout_surface = surface / short_name
        artifact_root = surface / "artifacts" / "smoke_001" / "stages" / short_name
        results = artifact_root / "results"
        results.mkdir(parents=True, exist_ok=True)
        source_files = {}
        if short_name == "structural_and_tower_diagnostics":
            source_files = _write_stage1_tables(results)
        if short_name == "paired_replicate_comparison":
            source_files = _write_stage6_tables(results)
        source = readout_surface / "readout_source.json"
        _write_json(
            source,
            {
                "evaluation_id": stage_id,
                "repo_readout_surface": str(readout_surface),
                "source_artifact_root": str(artifact_root),
                "source_evaluation_root": str(artifact_root),
                "source_files": {key: str(path) for key, path in source_files.items()},
            },
        )
        paths.append(source)
    return paths


def _write_stage1_tables(results: Path) -> dict[str, Path]:
    tables = {
        "state_space_summary": results / "state_space_summary.csv",
        "shortest_path_summary": results / "shortest_path_summary.csv",
        "random_policy_recon_summary": results / "random_policy_recon_summary.csv",
    }
    _write_csv(tables["state_space_summary"], ("valid_state_count",), [{"valid_state_count": 89}])
    _write_csv(
        tables["shortest_path_summary"],
        ("shortest_path_length",),
        [{"shortest_path_length": 6}],
    )
    _write_csv(
        tables["random_policy_recon_summary"],
        ("success_rate",),
        [{"success_rate": 0.024}],
    )
    return tables


def _write_stage6_tables(results: Path) -> dict[str, Path]:
    tables = {
        "comparison_claim_summary": results / "comparison_claim_summary.csv",
        "arm_summary": results / "arm_summary.csv",
    }
    _write_csv(
        tables["comparison_claim_summary"],
        (
            "claim_status",
            "bounded_claim",
            "claim_boundary",
        ),
        [
            {
                "claim_status": "paired_comparison_negative_signal",
                "bounded_claim": "Tower is below direct on target-hit rate.",
                "claim_boundary": "bounded smoke comparison",
            }
        ],
    )
    _write_csv(
        tables["arm_summary"],
        ("arm_type", "mean_total_reward", "invalid_move_count"),
        [
            {
                "arm_type": "direct_concrete_baseline",
                "mean_total_reward": -80.0,
                "invalid_move_count": 20,
            },
            {
                "arm_type": "selected_tower_candidate",
                "mean_total_reward": -40.0,
                "invalid_move_count": 0,
            },
        ],
    )
    return tables


def _stage_status_row(
    surface: Path,
    short_name: str,
    stage_number: int,
    claim_status: str,
) -> dict[str, str]:
    stage_ids = {
        1: "plate_support_gauntlet_structural_tower_diagnostics_v001",
        2: "plate_support_gauntlet_contraction_schema_sweep_v001",
        3: "plate_support_gauntlet_candidate_discovery_v001",
        4: "plate_support_gauntlet_tower_training_health_v001",
        5: "plate_support_gauntlet_threshold_frontier_calibration_v001",
        6: "plate_support_gauntlet_paired_replicate_comparison_v001",
    }
    return {
        "suite_id": "plate_support_standard_gauntlet_v001",
        "stage_id": stage_ids[stage_number],
        "environment_family_id": "plate_support",
        "environment_instance_id": "plate_support_5x5_default_v001",
        "artifact_root": str(surface / "artifacts" / "smoke_001" / "stages" / short_name),
        "status": "complete",
        "claim_status": claim_status,
        "claim_boundary": "test boundary",
        "source_stage_ids": "",
        "source_artifact_paths": "",
        "linearization_mode_id": "tensor_available_disabled",
        "state_collapser_dependency_status": "ok",
    }


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))
