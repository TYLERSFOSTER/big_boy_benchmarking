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
