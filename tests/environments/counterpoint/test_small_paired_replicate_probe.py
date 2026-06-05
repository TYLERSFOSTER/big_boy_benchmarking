import csv
import json
from pathlib import Path

import pytest

from big_boy_benchmarking.cli.main import main
from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint import (
    small_paired_replicate_probe as paired_probe,
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
from big_boy_benchmarking.environments.counterpoint.small_paired_replicate_probe import (
    paths as paired_paths,
)
from big_boy_benchmarking.environments.counterpoint.small_paired_replicate_probe import (
    threshold_source,
)


def test_small_paired_replicate_ids_are_exported_and_distinct() -> None:
    assert (
        ids.CANONICAL_IDS["small_paired_replicate_probe_evaluation_id"]
        == paired_probe.EVALUATION_ID
    )
    assert ids.CANONICAL_IDS["small_paired_replicate_probe_run_family_id"] == (
        paired_probe.EVALUATION_RUN_FAMILY_ID
    )
    assert ids.CANONICAL_IDS["small_paired_replicate_probe_smoke_mode_id"] == (
        paired_probe.SMOKE_RUN_MODE_ID
    )
    assert ids.CANONICAL_IDS["small_paired_replicate_probe_selected_mode_id"] == (
        paired_probe.SELECTED_THRESHOLD_RUN_MODE_ID
    )
    assert paired_probe.EVALUATION_ID != ids.SECOND_SERIOUS_SCHEMA_COMPARISON_EVALUATION_ID


def test_small_paired_paths_reject_outside_repo(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    monkeypatch.setattr(paired_paths, "REPO_ROOT", repo_root)

    with pytest.raises(ValueError, match="repo-resident"):
        paired_paths.validate_repo_resident_artifact_root(tmp_path / "outside")


def test_threshold_source_resolves_explicit_and_frontier_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    monkeypatch.setattr(paired_paths, "REPO_ROOT", repo_root)
    readout_surface = (
        repo_root
        / "docs"
        / "evaluations"
        / "counterpoint_symbolic_v001"
        / "threshold_frontier_probe"
    )
    result_path = readout_surface / "artifacts" / "frontier_001" / "frontier_summary.csv"
    result_path.parent.mkdir(parents=True)
    result_path.write_text(
        "recommended_replicate_probe_threshold\n13.25\n",
        encoding="utf-8",
    )
    source_path = readout_surface / "readout_source.json"
    source_path.write_text(
        json.dumps({"source_files": {"frontier_summary": str(result_path)}}),
        encoding="utf-8",
    )

    explicit = threshold_source.resolve_threshold(
        threshold_value=13.0, threshold_frontier_readout_source=None
    )
    frontier = threshold_source.resolve_threshold(
        threshold_value=None,
        threshold_frontier_readout_source=source_path,
    )

    assert explicit.threshold_value == 13.0
    assert explicit.threshold_source_type == "explicit_cli_threshold"
    assert frontier.threshold_value == 13.25
    assert frontier.threshold_source_type == "threshold_frontier_readout"


def test_small_paired_runner_aggregation_docs_and_cli(
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
        / "small_paired_replicate_probe"
    )
    artifact_root = readout_surface / "artifacts" / "pytest_001"
    monkeypatch.setattr(paired_paths, "REPO_ROOT", repo_root)
    monkeypatch.setattr(paired_paths, "DEFAULT_REPO_READOUT_SURFACE", readout_surface)
    monkeypatch.setattr(paired_paths, "DEFAULT_CANDIDATE_READOUT_SOURCE", full_readout)

    run_result = paired_probe.run_small_paired_replicate_probe(
        artifact_root=artifact_root,
        candidate_readout_source=full_readout,
        instance_id="small",
        candidate_cap=1,
        training_replicates_per_arm=1,
        episodes_per_replicate=4,
        threshold_value=-999.0,
        controller_event_ceiling=16,
    )
    summary = paired_probe.aggregate_small_paired_replicate_probe_results(artifact_root)
    docs = paired_probe.write_small_paired_replicate_probe_docs(artifact_root=artifact_root)

    assert run_result["status"] == "complete"
    assert run_result["run_count"] == 2
    assert run_result["pair_count"] == 1
    assert summary["status"] == "complete"
    assert summary["pair_count"] == 1
    assert (readout_surface / "readout_source.json").exists()
    assert "README.md" in docs
    assert "results/paired_replicate_readout.md" in docs

    paths = paired_paths.build_small_paired_replicate_probe_paths(artifact_root)
    source = json.loads((readout_surface / "readout_source.json").read_text())
    assert source["evaluation_id"] == paired_probe.EVALUATION_ID
    assert source["source_files"]["replicate_pair_summary"].endswith("replicate_pair_summary.csv")
    run_rows = list(csv.DictReader(paths.evaluation_run_index_csv.open()))
    assert {row["evaluation_id"] for row in run_rows} == {paired_probe.EVALUATION_ID}
    pair_rows = list(csv.DictReader((paths.results_dir / "replicate_pair_summary.csv").open()))
    assert pair_rows[0]["pair_status"] in {
        "schema1_faster",
        "schema1_slower",
        "schema1_margin_higher",
        "schema1_margin_lower",
        "same_margin",
        "blocked_or_non_sustained",
    }
    seed_rows = list(csv.DictReader((paths.results_dir / "seed_bundle_summary.csv").open()))
    assert Path(seed_rows[0]["schema0_seed_bundle_path"]).exists()
    assert Path(seed_rows[0]["schema1_seed_bundle_path"]).exists()
    run_manifest = json.loads(
        (
            artifact_root
            / "runs"
            / paired_probe.EVALUATION_RUN_FAMILY_ID
            / "runs"
            / run_rows[0]["run_id"]
            / "run_manifest.json"
        ).read_text()
    )
    assert run_manifest["run_family_id"] == paired_probe.EVALUATION_RUN_FAMILY_ID

    cli_artifact_root = readout_surface / "artifacts" / "cli_001"
    assert (
        main(
            [
                "counterpoint",
                "paired-replicate-probe",
                "run",
                "--artifact-root",
                str(cli_artifact_root),
                "--candidate-readout-source",
                str(full_readout),
                "--instance-id",
                "small",
                "--candidate-cap",
                "1",
                "--episodes",
                "4",
                "--replicates",
                "1",
                "--threshold-value",
                "-999",
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
                "paired-replicate-probe",
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
