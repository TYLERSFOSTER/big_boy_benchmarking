import json
from pathlib import Path

from big_boy_benchmarking.cli.main import main


def test_plate_support_readiness_cli_writes_artifacts(tmp_path: Path) -> None:
    assert (
        main(
            [
                "plate-support",
                "readiness",
                "--artifact-root",
                str(tmp_path / "readiness"),
                "--random-policy-episodes",
                "3",
                "--tower-probe-steps",
                "3",
                "--tower-probe-sample-size",
                "10",
                "--docs-path",
                str(tmp_path / "plate_support.md"),
            ]
        )
        == 0
    )

    assert (tmp_path / "readiness" / "readout_source.json").exists()
    assert (tmp_path / "plate_support.md").exists()


def test_plate_support_standard_gauntlet_inspect_architecture_cli(capsys) -> None:
    repo_root = Path(__file__).resolve().parents[3]

    assert (
        main(
            [
                "plate-support",
                "standard-gauntlet",
                "inspect-architecture",
                "--repo-root",
                str(repo_root),
                "--run-label",
                "smoke_001",
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "ok"
    assert payload["suite_id"] == "plate_support_standard_gauntlet_v001"
    assert payload["paths"]["repo_readout_surface"].endswith(
        "docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet"
    )
    assert payload["paths"]["source_artifact_root"].endswith(
        "docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001"
    )
    assert "gates" in payload
