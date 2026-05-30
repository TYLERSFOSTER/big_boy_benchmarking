import csv
import json
from pathlib import Path

from big_boy_benchmarking.environments.counterpoint.instances import (
    default_small_spec,
    default_tiny_spec,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.direct import (
    run_serious_direct_masked_random,
    run_serious_direct_tabular_q,
)
from big_boy_benchmarking.seeds.bundles import generate_seed_bundles


def test_serious_direct_masked_random_tiny_smoke_writes_artifacts(tmp_path) -> None:
    seed_bundle = generate_seed_bundles(base_seed=11, replicate_count=1)[0]
    result = run_serious_direct_masked_random(
        spec=default_tiny_spec(),
        seed_bundle=seed_bundle,
        artifact_root=tmp_path,
        episode_count=1,
    )

    assert result.status == "success"
    assert Path(result.artifact_paths["episodes_csv"]).exists()
    assert Path(result.artifact_paths["step_events_csv"]).exists()
    assert Path(result.artifact_paths["linearization_manifest"]).exists()


def test_serious_direct_tabular_q_uses_upstream_learner_and_no_tower_timing(tmp_path) -> None:
    seed_bundle = generate_seed_bundles(base_seed=12, replicate_count=1)[0]
    result = run_serious_direct_tabular_q(
        spec=default_tiny_spec(),
        seed_bundle=seed_bundle,
        artifact_root=tmp_path,
        episode_count=1,
    )
    run_manifest = json.loads(Path(result.artifact_paths["run_manifest"]).read_text())
    timing_rows = list(
        csv.DictReader(Path(result.artifact_paths["timing_segments_csv"]).open())
    )

    assert result.status == "success"
    assert run_manifest["learner_id"] == "tabular_q"
    assert "state_collapser.training.TabularQLearner" in str(run_manifest["budget"])
    assert not any(row["segment_name"].startswith("tower_") for row in timing_rows)


def test_serious_direct_small_one_episode_calibration_scale_run_succeeds(tmp_path) -> None:
    seed_bundle = generate_seed_bundles(base_seed=13, replicate_count=1)[0]
    result = run_serious_direct_tabular_q(
        spec=default_small_spec(),
        seed_bundle=seed_bundle,
        artifact_root=tmp_path,
        episode_count=1,
    )

    assert result.status == "success"
    assert Path(result.summary_path).exists()
