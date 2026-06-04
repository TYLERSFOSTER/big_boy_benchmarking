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
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.runner import (
    run_noisy_rate_full_training,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison import (
    paths as second_paths,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.aggregation import (
    aggregate_second_serious_comparison_results,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.candidates import (
    load_schema1_candidates,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    EVALUATION_ID,
    SCHEMA0_CLASS_ID,
    SCHEMA1_CLASS_ID,
    SCHEMA1_TOWER_SOURCE_FULL_ITERATED,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.docs_writer import (
    write_second_serious_comparison_docs,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.runner import (
    comparison_spec_for_instance,
    run_second_serious_comparison,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.thresholds import (
    ThresholdPolicy,
    compute_first_hit,
)


def test_second_serious_ids_are_exported_and_distinct() -> None:
    assert (
        ids.CANONICAL_IDS["second_serious_schema_comparison_evaluation_id"]
        == "counterpoint_second_serious_schema_comparison_v001"
    )
    assert ids.SECOND_SERIOUS_SCHEMA0_CLASS_ID == SCHEMA0_CLASS_ID
    assert ids.SECOND_SERIOUS_SCHEMA1_CLASS_ID == SCHEMA1_CLASS_ID
    assert (
        ids.SECOND_SERIOUS_SCHEMA_COMPARISON_EVALUATION_ID
        != ids.NOISY_RATE_FULL_TOWER_TRAINING_EVALUATION_ID
    )


def test_second_serious_resolver_supports_wide_span18_instance() -> None:
    spec = comparison_spec_for_instance("wide_span18")

    assert spec.environment_instance_id == "counterpoint_symbolic_n3_wide_20_108_span18_v001"
    assert spec.pitch_min == 20
    assert spec.pitch_max == 108
    assert spec.max_outer_span == 18
    assert spec.allowed_outer_interval_classes == (0, 3, 4, 5, 7, 8, 9)


def test_second_serious_paths_reject_outside_repo(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    monkeypatch.setattr(second_paths, "REPO_ROOT", repo_root)

    with pytest.raises(ValueError, match="repo-resident"):
        second_paths.validate_repo_resident_artifact_root(tmp_path / "outside")


def test_first_sustained_hit_statuses() -> None:
    policy = ThresholdPolicy(threshold_value=1.0, window_length=5, required_count=4)

    sustained = compute_first_hit((0, 1, 1, 1, 1), threshold_policy=policy)
    transient = compute_first_hit((0, 1, 0, 0, 0), threshold_policy=policy)
    never = compute_first_hit((0, 0, 0, 0, 0), threshold_policy=policy)
    incomplete = compute_first_hit((), threshold_policy=policy)

    assert sustained.hit_status == "sustained_hit"
    assert sustained.first_sustained_hit_episode_index == 4
    assert transient.hit_status == "transient_hit_only"
    assert never.hit_status == "never_hit"
    assert incomplete.hit_status == "artifact_incomplete"


def test_second_serious_candidate_loader_and_medium_gate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    full_readout, _ = _build_full_training_readout(tmp_path, monkeypatch)

    selection = load_schema1_candidates(
        full_readout,
        instance_id="counterpoint_symbolic_n3_small_v001",
        candidate_cap=1,
    )

    assert len(selection.selected) == 1
    assert selection.selected[0].candidate_eligible
    assert selection.selected[0].parent_training_health_class == "trainable_clean"
    target_id = selection.selected[0].candidate_id
    targeted = load_schema1_candidates(
        full_readout,
        instance_id="counterpoint_symbolic_n3_small_v001",
        candidate_cap=1,
        target_candidate_ids=(target_id,),
    )

    assert tuple(row.candidate_id for row in targeted.selected) == (target_id,)

    with pytest.raises(ValueError, match="not found"):
        load_schema1_candidates(
            full_readout,
            instance_id="counterpoint_symbolic_n3_small_v001",
            candidate_cap=1,
            target_candidate_ids=("missing-candidate",),
        )

    artifact_root = full_readout.parents[0] / "second" / "artifacts" / "serious_001"
    with pytest.raises(ValueError, match="four eligible medium"):
        run_second_serious_comparison(
            artifact_root=artifact_root,
            candidate_readout_source=full_readout,
            instance_id="medium",
            candidate_cap=4,
            episodes_per_replicate=256,
            threshold_value=-999.0,
            run_mode="serious_schema_comparison_first_sustained_hit",
            serious_run_authorized=True,
        )


def test_second_serious_runner_aggregation_and_docs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    full_readout, repo_root = _build_full_training_readout(tmp_path, monkeypatch)
    readout_surface = (
        repo_root
        / "docs"
        / "evaluations"
        / "counterpoint_symbolic_v001"
        / "second_serious_schema_comparison"
    )
    artifact_root = readout_surface / "artifacts" / "pytest_001"
    monkeypatch.setattr(second_paths, "DEFAULT_REPO_READOUT_SURFACE", readout_surface)
    monkeypatch.setattr(second_paths, "DEFAULT_CANDIDATE_READOUT_SOURCE", full_readout)

    run_result = run_second_serious_comparison(
        artifact_root=artifact_root,
        candidate_readout_source=full_readout,
        instance_id="small",
        candidate_cap=1,
        training_replicates_per_arm=1,
        episodes_per_replicate=5,
        threshold_value=-999.0,
        controller_event_ceiling=16,
    )
    summary = aggregate_second_serious_comparison_results(artifact_root)
    docs = write_second_serious_comparison_docs(artifact_root=artifact_root)

    assert run_result["status"] == "complete"
    assert summary["status"] == "complete"
    assert summary["run_count"] == 2
    assert (readout_surface / "readout_source.json").exists()
    assert (readout_surface / "README.md").exists()
    assert "README.md" in docs
    assert "results/paired_comparison_readout.md" in docs

    source = json.loads((readout_surface / "readout_source.json").read_text())
    assert source["evaluation_id"] == EVALUATION_ID
    assert "paired_schema_comparison" in source["source_files"]
    readme = (readout_surface / "README.md").read_text()
    assert "Summary of Goals Behind this Evaluation" in readme
    assert (
        "execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at" in readme
    )


def test_second_serious_full_iterated_schema1_records_runtime_tower_sequence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    full_readout, repo_root = _build_full_training_readout(tmp_path, monkeypatch)
    readout_surface = (
        repo_root
        / "docs"
        / "evaluations"
        / "counterpoint_symbolic_v001"
        / "second_serious_schema_comparison"
    )
    artifact_root = readout_surface / "artifacts" / "full_iterated_001"
    monkeypatch.setattr(second_paths, "DEFAULT_REPO_READOUT_SURFACE", readout_surface)
    monkeypatch.setattr(second_paths, "DEFAULT_CANDIDATE_READOUT_SOURCE", full_readout)

    run_result = run_second_serious_comparison(
        artifact_root=artifact_root,
        candidate_readout_source=full_readout,
        instance_id="small",
        candidate_cap=1,
        schema1_tower_source=SCHEMA1_TOWER_SOURCE_FULL_ITERATED,
        training_replicates_per_arm=1,
        episodes_per_replicate=5,
        threshold_value=-999.0,
        controller_event_ceiling=16,
    )
    aggregate_second_serious_comparison_results(artifact_root)

    assert run_result["status"] == "complete"
    paths = second_paths.build_second_serious_comparison_paths(artifact_root)
    candidate_summary_path = paths.results_dir / "candidate_summary.csv"
    candidate_rows = list(csv.DictReader(candidate_summary_path.open()))
    selected = next(row for row in candidate_rows if row["selected"] == "True")
    source_shape = json.loads(
        next(
            row
            for row in json.loads(paths.candidate_manifest.read_text())[
                "selected_schema1_candidates"
            ]
            if row["candidate_id"] == selected["schema1_candidate_id"]
        )["tier_state_cell_count_sequence"]
    )
    runtime_shape = json.loads(selected["tier_state_cell_count_sequence"])

    assert runtime_shape[: len(source_shape)] == source_shape
    assert len(runtime_shape) > len(source_shape)


def test_second_serious_cli_run_and_summarize(
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
        / "second_serious_schema_comparison"
    )
    artifact_root = readout_surface / "artifacts" / "cli_001"
    monkeypatch.setattr(second_paths, "DEFAULT_REPO_READOUT_SURFACE", readout_surface)
    monkeypatch.setattr(second_paths, "DEFAULT_CANDIDATE_READOUT_SOURCE", full_readout)
    candidate_id = load_schema1_candidates(
        full_readout,
        instance_id="counterpoint_symbolic_n3_small_v001",
        candidate_cap=1,
    ).selected[0].candidate_id

    assert (
        main(
            [
                "counterpoint",
                "second-serious-comparison",
                "run",
                "--artifact-root",
                str(artifact_root),
                "--candidate-readout-source",
                str(full_readout),
                "--candidate-cap",
                "1",
                "--candidate-id",
                candidate_id,
                "--instance-id",
                "small",
                "--episodes",
                "5",
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
                "second-serious-comparison",
                "summarize",
                "--artifact-root",
                str(artifact_root),
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "complete"
    assert (readout_surface / "readout_source.json").exists()


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
