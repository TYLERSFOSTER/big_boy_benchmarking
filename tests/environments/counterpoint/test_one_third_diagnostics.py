import json
from pathlib import Path

import pytest
from state_collapser.tower.control import (
    ActiveTierState,
    FrozenLowerContext,
    TierControlConfig,
    TierSignalState,
)

from big_boy_benchmarking.cli.main import main
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics import (
    paths as paths_module,
)
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.aggregation import (
    aggregate_one_third_diagnostics_results,
)
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.config import (
    DEFAULT_SCHEMA_ID,
    OneThirdDiagnosticsBudget,
)
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.docs_writer import (
    write_one_third_diagnostics_docs,
)
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.runner import (
    DiagnosticActiveTierController,
    counterpoint_one_third_spec_for_instance,
    run_one_third_diagnostics,
)
from big_boy_benchmarking.metrics.timing import TimingRecorder


def test_one_third_budget_rejects_tiny() -> None:
    with pytest.raises(ValueError, match="tiny"):
        OneThirdDiagnosticsBudget(instance_ids=("tiny",))


def test_one_third_instance_resolver_supports_small_and_medium() -> None:
    small = counterpoint_one_third_spec_for_instance("small")
    medium = counterpoint_one_third_spec_for_instance("medium")

    assert small.environment_instance_id == "counterpoint_symbolic_n3_small_v001"
    assert medium.environment_instance_id == "counterpoint_symbolic_n3_medium_v001"


def test_diagnostic_controller_records_upstream_abc_helper_context() -> None:
    controller = DiagnosticActiveTierController(TimingRecorder.create("abc-test"))
    active = ActiveTierState(
        active_tier=0,
        tier_state="tier0",
        context_version="test",
        event_index=0,
        deepest_known_tier=1,
    )
    signals = {
        0: TierSignalState(visit_count=10, success_count=10),
        1: TierSignalState(),
    }
    configs = {
        0: TierControlConfig(min_visit_count=5, success_threshold=0.6),
        1: TierControlConfig(min_visit_count=5, success_threshold=0.6),
    }

    decision = controller.decide(
        active,
        signals[0],
        configs[0],
        signals_by_tier=signals,
        tier_configs=configs,
        frozen_context=FrozenLowerContext(supporting_tier=1),
        training_due=False,
        tier_is_executable=lambda tier: True,
    )

    assert decision.action.value == "descend"
    assert controller.snapshots[0].selected_tier == 1
    assert controller.snapshots[0].predicted_movement_direction == "descend"
    assert controller.snapshots[0].tier_signals[1].unclosed


def test_one_third_runner_aggregation_and_docs_write_repo_readout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    readout_surface = (
        repo_root
        / "docs"
        / "evaluations"
        / "counterpoint_symbolic_v001"
        / "one_third_schema_tower_diagnostics"
    )
    artifact_root = readout_surface / "artifacts" / "pytest_001"
    monkeypatch.setattr(paths_module, "REPO_ROOT", repo_root)
    monkeypatch.setattr(paths_module, "DEFAULT_REPO_READOUT_SURFACE", readout_surface)

    run_result = run_one_third_diagnostics(
        artifact_root=artifact_root,
        instance_ids=("small",),
        schema_seeds=(0,),
        replicates_per_schema_seed=1,
        episodes_per_replicate=1,
        controller_event_ceiling=8,
    )
    summary = aggregate_one_third_diagnostics_results(artifact_root)
    docs = write_one_third_diagnostics_docs(artifact_root=artifact_root)

    assert run_result["status"] == "complete"
    assert summary["status"] == "complete"
    assert (readout_surface / "readout_source.json").exists()
    assert (readout_surface / "README.md").exists()
    assert (artifact_root / "evaluations" / summary["evaluation_id"]).exists()
    assert "README.md" in docs


def test_one_third_cli_run_summarize_and_reject_tiny(
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
        / "one_third_schema_tower_diagnostics"
    )
    artifact_root = readout_surface / "artifacts" / "cli_001"
    monkeypatch.setattr(paths_module, "REPO_ROOT", repo_root)
    monkeypatch.setattr(paths_module, "DEFAULT_REPO_READOUT_SURFACE", readout_surface)

    assert (
        main(
            [
                "counterpoint",
                "one-third-diagnostics",
                "run",
                "--artifact-root",
                str(artifact_root),
                "--instance-ids",
                "small",
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
                "one-third-diagnostics",
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

    with pytest.raises(ValueError, match="tiny"):
        main(
            [
                "counterpoint",
                "one-third-diagnostics",
                "run",
                "--artifact-root",
                str(readout_surface / "artifacts" / "tiny_bad"),
                "--instance-ids",
                "tiny",
                "--schema-seeds",
                "0",
                "--replicates",
                "1",
                "--episodes",
                "1",
            ]
        )


def test_one_third_default_schema_id_is_locked() -> None:
    assert DEFAULT_SCHEMA_ID == "counterpoint_one_third_outgoing_schema_v001"
