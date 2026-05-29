import subprocess
import sys

from big_boy_benchmarking.cli.main import main


def test_validate_contracts_command_works(capsys) -> None:
    assert main(["validate-contracts"]) == 0
    assert "linearization_mode_count" in capsys.readouterr().out


def test_module_help_works() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "big_boy_benchmarking.cli", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "validate-contracts" in result.stdout


def test_unknown_command_exits_nonzero() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "big_boy_benchmarking.cli", "nope"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0


def test_counterpoint_fixture_search_command_writes_artifacts(tmp_path) -> None:
    assert main(
        [
            "counterpoint",
            "search-fixtures",
            "--artifact-root",
            str(tmp_path),
            "--scale",
            "tiny",
        ]
    ) == 0

    assert (
        tmp_path / "counterpoint" / "fixture_search" / "tiny_fixture_search_summary.json"
    ).exists()


def test_counterpoint_graph_diagnostics_command_writes_artifacts(tmp_path) -> None:
    assert main(
        [
            "counterpoint",
            "graph-diagnostics",
            "--artifact-root",
            str(tmp_path),
            "--instance-id",
            "tiny",
        ]
    ) == 0

    assert (
        tmp_path
        / "counterpoint"
        / "graph_diagnostics"
        / "counterpoint_symbolic_n3_tiny_v001"
        / "graph_summary.json"
    ).exists()


def test_counterpoint_direct_and_tower_commands_run(tmp_path) -> None:
    assert main(
        [
            "counterpoint",
            "run-direct",
            "--artifact-root",
            str(tmp_path / "direct"),
            "--policy",
            "masked-random",
        ]
    ) == 0
    assert main(
        [
            "counterpoint",
            "tower-smoke",
            "--artifact-root",
            str(tmp_path / "tower"),
            "--schema-id",
            "counterpoint_empty_schema_v001",
        ]
    ) == 0


def test_counterpoint_schema_diagnostics_command_writes_artifacts(tmp_path) -> None:
    assert main(
        [
            "counterpoint",
            "schema-diagnostics",
            "--artifact-root",
            str(tmp_path),
            "--schema-id",
            "counterpoint_projection_audit_schema_v001",
        ]
    ) == 0

    assert (
        tmp_path
        / "counterpoint"
        / "schema_diagnostics"
        / "counterpoint_projection_audit_schema_v001"
        / "balanced_addressability.json"
    ).exists()
