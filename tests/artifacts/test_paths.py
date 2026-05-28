from pathlib import Path

from big_boy_benchmarking.artifacts.paths import build_run_family_paths, build_run_paths


def test_path_builders_are_deterministic_and_explicit(tmp_path: Path, monkeypatch) -> None:
    artifact_root = tmp_path / "artifacts"
    first = build_run_paths(artifact_root, "family", "run")
    monkeypatch.chdir(tmp_path)
    second = build_run_paths(artifact_root, "family", "run")

    assert first == second
    assert first.root == artifact_root / "runs" / "family" / "runs" / "run"
    assert first.episodes_csv.name == "episodes.csv"


def test_run_family_layout_matches_contract(tmp_path: Path) -> None:
    paths = build_run_family_paths(tmp_path, "family")

    assert paths.root == tmp_path / "runs" / "family"
    assert paths.run_index.name == "run_index.jsonl"
    assert paths.summary_json == paths.summaries_dir / "summary.json"
