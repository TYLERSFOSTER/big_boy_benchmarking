import csv
import json
from pathlib import Path

import pytest

from big_boy_benchmarking.cli.main import main
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics import (
    paths as paths_module,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.aggregation import (
    aggregate_noisy_rate_diagnostics_results,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.config import (
    NoisyRateDiagnosticsBudget,
    parse_rate_list,
    parse_rate_spec,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.docs_writer import (
    write_noisy_rate_diagnostics_docs,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.runner import (
    _endpoint_coalescence_summary,
    noisy_rate_spec_for_instance,
    run_noisy_rate_diagnostics,
)
from big_boy_benchmarking.environments.counterpoint.actions import CounterpointAction
from big_boy_benchmarking.environments.counterpoint.graph import (
    GraphEdge,
    enumerate_reachable_graph,
)
from big_boy_benchmarking.environments.counterpoint.instances import default_small_spec
from big_boy_benchmarking.environments.counterpoint.schemas import (
    noisy_rate_monotonicity_report,
    noisy_rate_source_coverage_report,
    selected_noisy_rate_edge_keys,
    stable_noisy_rate_score,
)
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState
from big_boy_benchmarking.environments.counterpoint.tower_adapter import (
    assigned_counterpoint_edge_keys,
    build_counterpoint_noisy_rate_partition_tower,
)


def test_noisy_rate_budget_rejects_tiny() -> None:
    with pytest.raises(ValueError, match="tiny"):
        NoisyRateDiagnosticsBudget(instance_ids=("tiny",))


def test_noisy_rate_instance_resolver_supports_small_and_medium() -> None:
    small = noisy_rate_spec_for_instance("small")
    medium = noisy_rate_spec_for_instance("medium")

    assert small.environment_instance_id == "counterpoint_symbolic_n3_small_v001"
    assert medium.environment_instance_id == "counterpoint_symbolic_n3_medium_v001"


def test_rate_parser_uses_explicit_denominators() -> None:
    assert parse_rate_spec("1/144").arm_id == "p001_over_144"
    rates = parse_rate_list("1/144,1/36,1/18")

    assert [rate.arm_id for rate in rates] == [
        "p001_over_144",
        "p001_over_036",
        "p001_over_018",
    ]


def test_stable_noisy_rate_score_is_deterministic_and_seeded() -> None:
    edge_key = "beat0:pitches(60, 64, 67)|action(1, 0, 0)|beat1:pitches(61, 64, 67)"
    first = stable_noisy_rate_score(
        selector_rule_id="test_selector",
        instance_id="test_instance",
        schema_seed=0,
        canonical_edge_key=edge_key,
    )
    second = stable_noisy_rate_score(
        selector_rule_id="test_selector",
        instance_id="test_instance",
        schema_seed=0,
        canonical_edge_key=edge_key,
    )
    third = stable_noisy_rate_score(
        selector_rule_id="test_selector",
        instance_id="test_instance",
        schema_seed=1,
        canonical_edge_key=edge_key,
    )

    assert 0.0 <= first < 1.0
    assert first == second
    assert first != third


def test_noisy_rate_edges_are_nested_and_can_leave_sources_unselected() -> None:
    graph = enumerate_reachable_graph(default_small_spec())
    previous = frozenset()
    for numerator, denominator in ((1, 144), (1, 36), (1, 18)):
        selected = selected_noisy_rate_edge_keys(
            graph,
            numerator=numerator,
            denominator=denominator,
            schema_seed=0,
        )
        assert previous <= selected
        previous = selected

    coverage = noisy_rate_source_coverage_report(
        graph,
        numerator=1,
        denominator=144,
        schema_seed=0,
    )
    assert coverage["zero_selected_source_count"] > 0


def test_noisy_rate_monotonicity_report_records_rate_pairs() -> None:
    graph = enumerate_reachable_graph(default_small_spec())
    rows = noisy_rate_monotonicity_report(
        graph,
        rates=((1, 144), (1, 36), (1, 18)),
        schema_seed=0,
    )

    assert rows
    assert all(row["subset_pass"] for row in rows)
    assert rows[0]["from_arm_id"] == "p001_over_144"


def test_metadata_and_runtime_selected_edges_match() -> None:
    spec = default_small_spec()
    graph = enumerate_reachable_graph(spec)
    metadata_selected = selected_noisy_rate_edge_keys(
        graph,
        numerator=1,
        denominator=36,
        schema_seed=0,
    )
    build = build_counterpoint_noisy_rate_partition_tower(
        spec,
        numerator=1,
        denominator=36,
        schema_seed=0,
    )

    assert assigned_counterpoint_edge_keys(build.tower) == metadata_selected


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


def test_noisy_rate_runner_aggregation_and_docs_write_repo_readout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    readout_surface = (
        repo_root
        / "docs"
        / "evaluations"
        / "counterpoint_symbolic_v001"
        / "noisy_rate_contraction_diagnostics"
    )
    artifact_root = readout_surface / "artifacts" / "pytest_001"
    monkeypatch.setattr(paths_module, "REPO_ROOT", repo_root)
    monkeypatch.setattr(paths_module, "DEFAULT_REPO_READOUT_SURFACE", readout_surface)

    run_result = run_noisy_rate_diagnostics(
        artifact_root=artifact_root,
        instance_ids=("small",),
        rates=((1, 144), (1, 36)),
        schema_seeds=(0, 1),
        replicates_per_schema_seed=1,
        episodes_per_replicate=1,
        controller_event_ceiling=8,
    )
    summary = aggregate_noisy_rate_diagnostics_results(artifact_root)
    docs = write_noisy_rate_diagnostics_docs(artifact_root=artifact_root)

    assert run_result["status"] == "complete"
    assert summary["status"] == "complete"
    assert (readout_surface / "readout_source.json").exists()
    assert (readout_surface / "README.md").exists()
    assert "README.md" in docs

    source = json.loads((readout_surface / "readout_source.json").read_text())
    assert source["run_mode"] == "diagnostic_noisy_rate_contraction_tower_abc"
    assert "noisy_rate_source_coverage_summary" in source["source_files"]

    threshold_csv = (
        artifact_root
        / "evaluations"
        / summary["evaluation_id"]
        / "results"
        / "noisy_rate_threshold_summary.csv"
    )
    rows = list(csv.DictReader(threshold_csv.open()))
    assert rows


def test_noisy_rate_cli_run_and_summarize(
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
        / "noisy_rate_contraction_diagnostics"
    )
    artifact_root = readout_surface / "artifacts" / "cli_001"
    monkeypatch.setattr(paths_module, "REPO_ROOT", repo_root)
    monkeypatch.setattr(paths_module, "DEFAULT_REPO_READOUT_SURFACE", readout_surface)

    assert (
        main(
            [
                "counterpoint",
                "noisy-rate",
                "run",
                "--artifact-root",
                str(artifact_root),
                "--instances",
                "small",
                "--rates",
                "1/144,1/36",
                "--schema-seeds",
                "0,1",
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
                "noisy-rate",
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
