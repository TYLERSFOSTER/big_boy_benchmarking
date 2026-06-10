import json
from pathlib import Path

from big_boy_benchmarking.cli.main import main
from big_boy_benchmarking.environments.warehouse_gridlock.runner import (
    build_readiness_docs,
    run_transition_smoke,
)


def test_transition_smoke_writes_required_artifacts(tmp_path: Path) -> None:
    result = run_transition_smoke(artifact_root=tmp_path / "artifacts")

    assert result.status == "ok"
    for key in (
        "environment_instance_manifest",
        "graph_manifest",
        "transition_smoke_summary",
        "invalid_action_summary",
        "discovery_coverage_summary",
        "admissibility_budget_summary",
    ):
        assert Path(result.artifact_paths[key]).exists(), key


def test_readiness_docs_write_repo_side_readout_source(tmp_path: Path) -> None:
    result = build_readiness_docs(
        repo_root=tmp_path,
        artifact_root=tmp_path
        / "docs"
        / "evaluations"
        / "warehouse_gridlock_001"
        / "environment_readiness"
        / "artifacts"
        / "smoke_001",
    )

    readout_source = (
        tmp_path
        / "docs"
        / "evaluations"
        / "warehouse_gridlock_001"
        / "environment_readiness"
        / "readout_source.json"
    )
    assert result.status == "ok"
    assert readout_source.exists()
    payload = json.loads(readout_source.read_text())
    assert payload["environment_instance_id"] == "warehouse_gridlock_16x16_v001"
    assert "artifact_tables" in payload


def test_warehouse_gridlock_cli_commands(tmp_path: Path, capsys) -> None:
    artifact_root = tmp_path / "artifacts"

    assert (
        main(
            [
                "warehouse-gridlock",
                "graph-diagnostics",
                "--artifact-root",
                str(artifact_root),
            ]
        )
        == 0
    )
    graph_payload = json.loads(capsys.readouterr().out)
    assert graph_payload["status"] == "ok"
    assert graph_payload["robot_count"] == 32

    assert (
        main(
            [
                "warehouse-gridlock",
                "transition-smoke",
                "--artifact-root",
                str(artifact_root),
            ]
        )
        == 0
    )
    transition_payload = json.loads(capsys.readouterr().out)
    assert transition_payload["transition_case_count"] == 7

    assert (
        main(
            [
                "warehouse-gridlock",
                "readiness-docs",
                "--artifact-root",
                str(artifact_root),
                "--repo-root",
                str(tmp_path),
            ]
        )
        == 0
    )
    docs_payload = json.loads(capsys.readouterr().out)
    assert docs_payload["status"] == "ok"
