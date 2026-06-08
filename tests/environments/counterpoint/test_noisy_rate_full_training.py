import csv
import json
from pathlib import Path

import pytest

from big_boy_benchmarking.cli.main import main
from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics import (
    paths as parent_paths,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.aggregation import (
    aggregate_noisy_rate_diagnostics_results,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.runner import (
    run_noisy_rate_diagnostics,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training import (
    paths as full_paths,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.aggregation import (
    aggregate_noisy_rate_full_training_results,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.candidate_selection import (
    load_candidate_selection,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.docs_writer import (
    write_noisy_rate_full_training_docs,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.runner import (
    run_noisy_rate_full_training,
)


def test_full_training_ids_are_exported_and_distinct() -> None:
    assert (
        ids.CANONICAL_IDS["noisy_rate_full_tower_training_evaluation_id"]
        == "counterpoint_noisy_rate_full_tower_training_diagnostic_v001"
    )
    assert (
        ids.NOISY_RATE_FULL_TOWER_TRAINING_EVALUATION_ID
        != ids.NOISY_RATE_CONTRACTION_EVALUATION_ID
    )


def test_full_training_paths_reject_outside_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root = tmp_path / "repo"
    monkeypatch.setattr(full_paths, "REPO_ROOT", repo_root)

    with pytest.raises(ValueError, match="repo-resident"):
        full_paths.validate_repo_resident_artifact_root(tmp_path / "outside")


def test_candidate_selection_excludes_control_and_caps(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    parent_readout, _ = _build_parent_noisy_rate_readout(tmp_path, monkeypatch)

    selection = load_candidate_selection(parent_readout, candidate_cap=1)

    assert len(selection.selected) == 1
    assert selection.selected[0].arm_id != "no_contraction_control"
    assert selection.selected[0].candidate_eligible
    assert any(row.arm_id == "no_contraction_control" for row in selection.excluded)


def test_noisy_rate_full_training_runner_aggregation_and_docs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    parent_readout, repo_root = _build_parent_noisy_rate_readout(tmp_path, monkeypatch)
    full_readout_surface = (
        repo_root
        / "docs"
        / "evaluations"
        / "counterpoint_symbolic_v001"
        / "noisy_rate_full_tower_training_diagnostic"
    )
    artifact_root = full_readout_surface / "artifacts" / "pytest_001"
    monkeypatch.setattr(full_paths, "DEFAULT_REPO_READOUT_SURFACE", full_readout_surface)
    monkeypatch.setattr(full_paths, "DEFAULT_PARENT_CANDIDATE_READOUT_SOURCE", parent_readout)

    run_result = run_noisy_rate_full_training(
        artifact_root=artifact_root,
        parent_candidate_readout_source=parent_readout,
        candidate_cap=1,
        training_replicates_per_candidate=1,
        episodes_per_replicate=4,
        controller_event_ceiling=16,
    )
    summary = aggregate_noisy_rate_full_training_results(artifact_root)
    docs = write_noisy_rate_full_training_docs(artifact_root=artifact_root)

    assert run_result["status"] == "complete"
    assert summary["status"] == "complete"
    assert (full_readout_surface / "readout_source.json").exists()
    assert (full_readout_surface / "README.md").exists()
    assert (full_readout_surface / "result_readout.md").exists()
    assert (full_readout_surface / "results" / "human_summary.md").exists()
    assert (full_readout_surface / "results" / "arm_readout_table.md").exists()
    assert (full_readout_surface / "results" / "diagnostic_findings.md").exists()
    assert (full_readout_surface / "results" / "timing_readout.md").exists()
    assert "README.md" in docs
    assert "result_readout.md" in docs

    source = json.loads((full_readout_surface / "readout_source.json").read_text())
    assert source["run_mode"] == "diagnostic_noisy_rate_full_tower_training"
    assert "training_health_summary" in source["source_files"]

    readme = (full_readout_surface / "README.md").read_text()
    assert "#### Project Owner / Evaluator Turn" not in readme
    assert "#### Embedded Engineering Consultant / Codex Turn" not in readme
    assert "_No active public clarification turns are recorded for this readout._" in readme
    assert "not a direct-vs-tower comparison" in readme

    health_csv = (
        artifact_root
        / "evaluations"
        / summary["evaluation_id"]
        / "results"
        / "training_health_summary.csv"
    )
    rows = list(csv.DictReader(health_csv.open()))
    assert rows
    assert rows[0]["candidate_id"]


def test_noisy_rate_full_training_cli_run_and_summarize(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    parent_readout, repo_root = _build_parent_noisy_rate_readout(tmp_path, monkeypatch)
    full_readout_surface = (
        repo_root
        / "docs"
        / "evaluations"
        / "counterpoint_symbolic_v001"
        / "noisy_rate_full_tower_training_diagnostic"
    )
    artifact_root = full_readout_surface / "artifacts" / "cli_001"
    monkeypatch.setattr(full_paths, "DEFAULT_REPO_READOUT_SURFACE", full_readout_surface)
    monkeypatch.setattr(full_paths, "DEFAULT_PARENT_CANDIDATE_READOUT_SOURCE", parent_readout)

    assert (
        main(
            [
                "counterpoint",
                "noisy-rate-full-train",
                "run",
                "--artifact-root",
                str(artifact_root),
                "--candidate-readout-source",
                str(parent_readout),
                "--candidate-cap",
                "1",
                "--training-replicates",
                "1",
                "--episodes",
                "4",
                "--controller-event-ceiling",
                "16",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "complete"

    assert (
        main(
            [
                "counterpoint",
                "noisy-rate-full-train",
                "summarize",
                "--artifact-root",
                str(artifact_root),
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "complete"
    assert (full_readout_surface / "readout_source.json").exists()


def _build_parent_noisy_rate_readout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[Path, Path]:
    repo_root = tmp_path / "repo"
    parent_readout_surface = (
        repo_root
        / "docs"
        / "evaluations"
        / "counterpoint_symbolic_v001"
        / "noisy_rate_contraction_diagnostics"
    )
    artifact_root = parent_readout_surface / "artifacts" / "parent_001"
    monkeypatch.setattr(parent_paths, "REPO_ROOT", repo_root)
    monkeypatch.setattr(parent_paths, "DEFAULT_REPO_READOUT_SURFACE", parent_readout_surface)
    monkeypatch.setattr(full_paths, "REPO_ROOT", repo_root)

    run_noisy_rate_diagnostics(
        artifact_root=artifact_root,
        instance_ids=("small",),
        rates=((1, 36),),
        schema_seeds=(0,),
        replicates_per_schema_seed=1,
        episodes_per_replicate=1,
        controller_event_ceiling=8,
    )
    aggregate_noisy_rate_diagnostics_results(artifact_root)
    return parent_readout_surface / "readout_source.json", repo_root
