import csv
import json
from pathlib import Path

import pytest

from big_boy_benchmarking.cli.main import main
from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint import (
    threshold_frontier_probe as frontier,
)
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
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.runner import (
    run_noisy_rate_full_training,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison import (
    paths as second_paths,
)
from big_boy_benchmarking.environments.counterpoint.threshold_frontier_probe import (
    paths as frontier_paths,
)


def test_threshold_frontier_ids_and_threshold_labels_are_exported() -> None:
    assert ids.CANONICAL_IDS["threshold_frontier_probe_evaluation_id"] == (frontier.EVALUATION_ID)
    assert ids.CANONICAL_IDS["threshold_frontier_probe_run_family_id"] == (
        frontier.EVALUATION_RUN_FAMILY_ID
    )
    assert ids.CANONICAL_IDS["threshold_frontier_probe_run_mode_id"] == (frontier.RUN_MODE_ID)
    assert frontier.threshold_label(12.0) == "r012000"
    assert frontier.threshold_label(13.25) == "r013250"
    assert frontier.parse_threshold_values("12.0,13.0") == (12.0, 13.0)
    with pytest.raises(ValueError, match="unique"):
        frontier.parse_threshold_values("12.0,12.0")
    with pytest.raises(ValueError, match="sorted"):
        frontier.parse_threshold_values("13.0,12.0")


def test_threshold_frontier_paths_reject_outside_repo(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    monkeypatch.setattr(frontier_paths, "REPO_ROOT", repo_root)

    with pytest.raises(ValueError, match="repo-resident"):
        frontier_paths.validate_repo_resident_artifact_root(tmp_path / "outside")


def test_threshold_frontier_runner_aggregation_docs_and_cli(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    full_readout, repo_root = _build_full_training_readout(tmp_path, monkeypatch)
    readout_surface = (
        repo_root
        / "docs"
        / "evaluations"
        / "counterpoint_symbolic_v001"
        / "threshold_frontier_probe"
    )
    artifact_root = readout_surface / "artifacts" / "pytest_001"
    monkeypatch.setattr(frontier_paths, "REPO_ROOT", repo_root)
    monkeypatch.setattr(frontier_paths, "DEFAULT_REPO_READOUT_SURFACE", readout_surface)
    monkeypatch.setattr(frontier_paths, "DEFAULT_CANDIDATE_READOUT_SOURCE", full_readout)

    run_result = frontier.run_threshold_frontier_probe(
        artifact_root=artifact_root,
        candidate_readout_source=full_readout,
        instance_id="small",
        candidate_cap=1,
        threshold_values=(-999.0, -998.0),
        training_replicates_per_arm=1,
        episodes_per_replicate=3,
        controller_event_ceiling=16,
    )
    summary = frontier.aggregate_threshold_frontier_probe_results(artifact_root)
    docs = frontier.write_threshold_frontier_probe_docs(artifact_root=artifact_root)

    assert run_result["status"] == "complete"
    assert run_result["threshold_count"] == 2
    assert run_result["run_count"] == 4
    assert summary["status"] == "complete"
    assert summary["threshold_count"] == 2
    assert "recommended_replicate_probe_threshold" in summary
    assert (readout_surface / "readout_source.json").exists()
    assert "README.md" in docs
    assert "results/frontier_readout.md" in docs

    paths = frontier_paths.build_threshold_frontier_probe_paths(artifact_root)
    source = json.loads((readout_surface / "readout_source.json").read_text())
    assert source["evaluation_id"] == frontier.EVALUATION_ID
    assert source["source_files"]["frontier_summary"].endswith("frontier_summary.csv")
    run_rows = list(csv.DictReader(paths.evaluation_run_index_csv.open()))
    assert {row["evaluation_id"] for row in run_rows} == {frontier.EVALUATION_ID}
    threshold_manifest = json.loads(paths.threshold_run_manifest.read_text())
    assert len(threshold_manifest["threshold_runs"]) == 2
    frontier_rows = list(csv.DictReader((paths.results_dir / "frontier_summary.csv").open()))
    assert frontier_rows[0]["claim_status"] in {
        "schema1_frontier_advantage_observed",
        "schema1_margin_advantage_only",
        "no_frontier_separation_observed",
        "schema1_frontier_disadvantage_observed",
        "frontier_blocked_by_artifacts",
        "frontier_blocked_by_liftability",
        "frontier_inconclusive",
    }
    second_readout = (
        repo_root
        / "docs"
        / "evaluations"
        / "counterpoint_symbolic_v001"
        / "second_serious_schema_comparison"
        / "readout_source.json"
    )
    assert not second_readout.exists()

    cli_artifact_root = readout_surface / "artifacts" / "cli_001"
    assert (
        main(
            [
                "counterpoint",
                "threshold-frontier",
                "run",
                "--artifact-root",
                str(cli_artifact_root),
                "--candidate-readout-source",
                str(full_readout),
                "--instance-id",
                "small",
                "--candidate-cap",
                "1",
                "--threshold-values=-999.0,-998.0",
                "--episodes",
                "3",
                "--replicates",
                "1",
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
                "threshold-frontier",
                "summarize",
                "--artifact-root",
                str(cli_artifact_root),
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "complete"


def _build_full_training_readout(
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
    parent_artifact_root = parent_readout_surface / "artifacts" / "parent_001"
    full_readout_surface = (
        repo_root
        / "docs"
        / "evaluations"
        / "counterpoint_symbolic_v001"
        / "noisy_rate_full_tower_training_diagnostic"
    )
    full_artifact_root = full_readout_surface / "artifacts" / "full_001"
    monkeypatch.setattr(parent_paths, "REPO_ROOT", repo_root)
    monkeypatch.setattr(parent_paths, "DEFAULT_REPO_READOUT_SURFACE", parent_readout_surface)
    monkeypatch.setattr(full_paths, "REPO_ROOT", repo_root)
    monkeypatch.setattr(full_paths, "DEFAULT_REPO_READOUT_SURFACE", full_readout_surface)
    monkeypatch.setattr(second_paths, "REPO_ROOT", repo_root)

    run_noisy_rate_diagnostics(
        artifact_root=parent_artifact_root,
        instance_ids=("small",),
        rates=((1, 36),),
        schema_seeds=(0,),
        replicates_per_schema_seed=1,
        episodes_per_replicate=1,
        controller_event_ceiling=8,
    )
    aggregate_noisy_rate_diagnostics_results(parent_artifact_root)
    parent_readout = parent_readout_surface / "readout_source.json"
    run_noisy_rate_full_training(
        artifact_root=full_artifact_root,
        parent_candidate_readout_source=parent_readout,
        candidate_cap=1,
        training_replicates_per_candidate=1,
        episodes_per_replicate=4,
        controller_event_ceiling=16,
    )
    aggregate_noisy_rate_full_training_results(full_artifact_root)
    return full_readout_surface / "readout_source.json", repo_root
