import csv
import json
from pathlib import Path

from big_boy_benchmarking.environments.plate_support.runner import (
    run_plate_support_environment_readiness,
)


def test_plate_support_readiness_runner_writes_core_artifacts(tmp_path: Path) -> None:
    result = run_plate_support_environment_readiness(
        artifact_root=tmp_path / "readiness",
        random_policy_episodes=5,
        random_policy_seed=3,
        tower_probe_steps=5,
        tower_probe_sample_size=10,
        docs_path=tmp_path / "plate_support.md",
    )

    assert result.status == "success"
    paths = result.artifact_paths
    for key in (
        "run_manifest",
        "dependency_manifest",
        "linearization_manifest",
        "graph_summary",
        "state_summary",
        "transition_summary",
        "tower_probe_summary",
        "random_policy_recon_summary",
        "readout_source",
        "artifact_index",
        "environment_doc",
    ):
        assert Path(paths[key]).exists(), key

    graph = json.loads(Path(paths["graph_summary"]).read_text())
    assert graph["valid_state_count"] == 89
    assert graph["shortest_path_length"] == 6
    with Path(paths["state_summary"]).open() as handle:
        assert len(list(csv.DictReader(handle))) == 89
    with Path(paths["transition_summary"]).open() as handle:
        assert len(list(csv.DictReader(handle))) == 89 * 12


def test_plate_support_readiness_runner_rejects_evaluation_artifact_root(
    tmp_path: Path,
) -> None:
    try:
        run_plate_support_environment_readiness(
            artifact_root=tmp_path / "docs" / "evaluations" / "plate_support",
            random_policy_episodes=1,
            docs_path=tmp_path / "plate_support.md",
        )
    except ValueError as exc:
        assert "docs/evaluations" in str(exc)
    else:
        raise AssertionError("expected evaluation-path rejection")
