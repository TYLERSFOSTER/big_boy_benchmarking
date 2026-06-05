import csv
import json
from pathlib import Path

import pytest

from big_boy_benchmarking.cli.main import main
from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.actions import CounterpointAction
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics import (
    paths as paths_module,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.aggregation import (
    aggregate_fraction_sweep_diagnostics_results,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.config import (
    FractionSweepDiagnosticsBudget,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.docs_writer import (
    write_fraction_sweep_diagnostics_docs,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.runner import (
    _active_action_cell_count,
    _endpoint_coalescence_summary,
    fraction_sweep_spec_for_instance,
    run_fraction_sweep_diagnostics,
)
from big_boy_benchmarking.environments.counterpoint.graph import (
    GraphEdge,
    enumerate_reachable_graph,
)
from big_boy_benchmarking.environments.counterpoint.instances import default_small_spec
from big_boy_benchmarking.environments.counterpoint.schemas import (
    legacy_one_third_equivalence_report,
    selected_fraction_edge_keys,
    source_local_fraction_quota,
)
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState
from big_boy_benchmarking.environments.counterpoint.tower_adapter import (
    build_counterpoint_partition_tower,
)


def test_fraction_sweep_budget_rejects_tiny() -> None:
    with pytest.raises(ValueError, match="tiny"):
        FractionSweepDiagnosticsBudget(instance_ids=("tiny",))


def test_fraction_sweep_instance_resolver_supports_small_and_medium() -> None:
    small = fraction_sweep_spec_for_instance("small")
    medium = fraction_sweep_spec_for_instance("medium")

    assert small.environment_instance_id == "counterpoint_symbolic_n3_small_v001"
    assert medium.environment_instance_id == "counterpoint_symbolic_n3_medium_v001"


def test_fraction_quota_is_ceil_with_minimum_one() -> None:
    assert source_local_fraction_quota(0, numerator=1, denominator=18) == 0
    assert source_local_fraction_quota(1, numerator=1, denominator=18) == 1
    assert source_local_fraction_quota(18, numerator=1, denominator=18) == 1
    assert source_local_fraction_quota(19, numerator=1, denominator=18) == 2
    assert source_local_fraction_quota(18, numerator=6, denominator=18) == 6


def test_fraction_selected_edges_are_nested_and_n06_matches_legacy_first_block() -> None:
    graph = enumerate_reachable_graph(default_small_spec())
    previous = frozenset()
    for numerator in range(1, 7):
        selected = selected_fraction_edge_keys(
            graph,
            numerator=numerator,
            denominator=18,
            schema_seed=0,
        )
        assert previous <= selected
        previous = selected

    report = legacy_one_third_equivalence_report(
        graph,
        numerator=6,
        denominator=18,
        schema_seed=0,
    )
    assert report["equivalent"] is True


def test_endpoint_coalescence_summary_tracks_useful_and_redundant_edges() -> None:
    states = (
        CounterpointState((60, 64, 67), 0),
        CounterpointState((61, 64, 67), 0),
        CounterpointState((62, 64, 67), 0),
    )
    action = CounterpointAction((1, 0, 0))
    edges = (
        GraphEdge(states[0], action, states[1], 0.0, {}),
        GraphEdge(states[1], action, states[2], 0.0, {}),
        GraphEdge(states[0], action, states[2], 0.0, {}),
    )

    summary = _endpoint_coalescence_summary(states, edges)

    assert summary["processed_edge_count"] == 3
    assert summary["useful_coalescence_count"] == 2
    assert summary["redundant_or_internal_edge_count"] == 1
    assert summary["state_cell_count_after_block"] == 1
    assert summary["processed_edge_index_at_first_singleton"] == 2


def test_active_action_cell_count_handles_cleaned_upstream_records() -> None:
    build = build_counterpoint_partition_tower(
        default_small_spec(),
        schema_id=ids.ONE_THIRD_OUTGOING_SCHEMA_ID,
        schema_seed=0,
    )
    raw_tier_one = len(build.tower.action_layers[1].edge_ids_by_action_cell)
    active_tier_one = _active_action_cell_count(build.tower, 1)

    assert raw_tier_one >= active_tier_one
    assert raw_tier_one == 0
    assert active_tier_one == 0


def test_fraction_sweep_runner_aggregation_and_docs_write_repo_readout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    readout_surface = (
        repo_root
        / "docs"
        / "evaluations"
        / "counterpoint_symbolic_v001"
        / "contraction_fraction_sweep_diagnostics"
    )
    artifact_root = readout_surface / "artifacts" / "pytest_001"
    monkeypatch.setattr(paths_module, "REPO_ROOT", repo_root)
    monkeypatch.setattr(paths_module, "DEFAULT_REPO_READOUT_SURFACE", readout_surface)

    run_result = run_fraction_sweep_diagnostics(
        artifact_root=artifact_root,
        instance_ids=("small",),
        numerators=(1, 6),
        denominator=18,
        schema_seeds=(0,),
        replicates_per_schema_seed=1,
        episodes_per_replicate=1,
        controller_event_ceiling=8,
    )
    summary = aggregate_fraction_sweep_diagnostics_results(artifact_root)
    docs = write_fraction_sweep_diagnostics_docs(artifact_root=artifact_root)

    assert run_result["status"] == "complete"
    assert summary["status"] == "complete"
    assert (readout_surface / "readout_source.json").exists()
    assert (readout_surface / "README.md").exists()
    assert "README.md" in docs

    source = json.loads((readout_surface / "readout_source.json").read_text())
    assert source["run_mode"] == "diagnostic_contraction_fraction_sweep_tower_abc"
    assert "collapse_threshold_summary" in source["source_files"]

    threshold_csv = (
        artifact_root
        / "evaluations"
        / summary["evaluation_id"]
        / "results"
        / "collapse_threshold_summary.csv"
    )
    rows = list(csv.DictReader(threshold_csv.open()))
    assert rows


def test_fraction_sweep_cli_run_and_summarize(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = tmp_path / "repo"
    readout_surface = (
        repo_root
        / "docs"
        / "evaluations"
        / "counterpoint_symbolic_v001"
        / "contraction_fraction_sweep_diagnostics"
    )
    artifact_root = readout_surface / "artifacts" / "cli_001"
    monkeypatch.setattr(paths_module, "REPO_ROOT", repo_root)
    monkeypatch.setattr(paths_module, "DEFAULT_REPO_READOUT_SURFACE", readout_surface)

    assert (
        main(
            [
                "counterpoint",
                "fraction-sweep",
                "run",
                "--artifact-root",
                str(artifact_root),
                "--instances",
                "small",
                "--numerators",
                "1,6",
                "--denominator",
                "18",
                "--schema-seeds",
                "0",
                "--replicates",
                "1",
                "--episodes",
                "1",
                "--controller-event-ceiling",
                "8",
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
                "fraction-sweep",
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
