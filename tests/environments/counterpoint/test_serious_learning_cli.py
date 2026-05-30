import json

import pytest

from big_boy_benchmarking.cli.main import main


def test_serious_learning_cli_help_includes_command_family(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["counterpoint", "serious-learning", "--help"])

    assert exc_info.value.code == 0
    assert "calibrate" in capsys.readouterr().out


def test_serious_learning_tiny_smoke_cli_path_writes_outputs(tmp_path, capsys) -> None:
    assert main(
        [
            "counterpoint",
            "serious-learning",
            "calibrate",
            "--artifact-root",
            str(tmp_path),
            "--instance-id",
            "tiny",
            "--episodes",
            "1",
            "--replicates",
            "1",
            "--schema-seeds",
            "1",
        ]
    ) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["status"] == "smoke_non_evidence"
    assert (
        tmp_path
        / "evaluations"
        / "counterpoint_first_serious_learning_v001"
        / "calibration_summary.json"
    ).exists()


def test_serious_learning_summarize_cli_writes_docs(tmp_path, capsys) -> None:
    assert main(
        [
            "counterpoint",
            "serious-learning",
            "calibrate",
            "--artifact-root",
            str(tmp_path),
            "--instance-id",
            "tiny",
            "--episodes",
            "1",
            "--replicates",
            "1",
            "--schema-seeds",
            "1",
        ]
    ) == 0
    assert main(
        [
            "counterpoint",
            "serious-learning",
            "summarize",
            "--artifact-root",
            str(tmp_path),
            "--docs-root",
            str(tmp_path / "docs"),
        ]
    ) == 0

    assert (tmp_path / "docs" / "README.md").exists()
    capsys.readouterr()

    assert main(
        [
            "counterpoint",
            "serious-learning",
            "summarize",
            "--artifact-root",
            str(tmp_path),
        ]
    ) == 0
    payload = json.loads(capsys.readouterr().out)

    default_readme = (
        tmp_path
        / "evaluations"
        / "counterpoint_first_serious_learning_v001"
        / "docs"
        / "README.md"
    )
    assert payload["docs"]["README.md"] == str(default_readme)
    assert default_readme.exists()


def test_serious_learning_reserved_linearization_mode_fails(tmp_path) -> None:
    with pytest.raises(ValueError, match="reserved linearization mode"):
        main(
            [
                "counterpoint",
                "serious-learning",
                "calibrate",
                "--artifact-root",
                str(tmp_path),
                "--instance-id",
                "tiny",
                "--linearization-mode",
                "tensor_enabled_cpu",
            ]
        )
