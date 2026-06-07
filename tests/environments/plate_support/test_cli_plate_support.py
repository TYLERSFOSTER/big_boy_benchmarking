import json
from pathlib import Path

from big_boy_benchmarking.cli.main import build_parser, main


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


def test_plate_support_graph_stats_cli_prints_and_writes_json(
    tmp_path: Path,
    capsys,
) -> None:
    output_path = tmp_path / "graph_stats.json"

    assert (
        main(
            [
                "plate-support",
                "graph-stats",
                "--output",
                str(output_path),
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "ok"
    assert payload["state_space"]["valid_state_count"] == 89
    assert payload["transition_space"]["valid_nonself_edge_count"] == 388
    assert output_path.exists()


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


def test_plate_support_schema_sweep_iterated_flags_parse() -> None:
    args = build_parser().parse_args(
        [
            "plate-support",
            "standard-gauntlet",
            "schema-sweep",
            "run",
            "--repo-root",
            "/tmp/repo",
            "--artifact-root",
            "/tmp/artifacts",
            "--stage1-source",
            "/tmp/stage1/readout_source.json",
            "--locked-by",
            "pytest",
            "--include-iterated-source-local-ratio",
            "--iterated-source-local-ratio-denominator",
            "144",
            "--iterated-source-local-ratio-denominator",
            "72",
            "--iterated-source-local-schema-seed",
            "3",
            "--iterated-source-local-max-iterations",
            "32",
        ]
    )

    assert args.include_iterated_source_local_ratio is True
    assert args.iterated_source_local_ratio_denominator == [144, 72]
    assert args.iterated_source_local_schema_seed == [3]
    assert args.iterated_source_local_max_iterations == 32
