from big_boy_benchmarking.environments.counterpoint.instances import default_tiny_spec
from big_boy_benchmarking.environments.counterpoint.runners import (
    run_direct_masked_random,
    run_direct_tabular_q,
    run_tower_schema_smoke,
)
from big_boy_benchmarking.seeds.bundles import generate_seed_bundles


def test_direct_masked_random_runner_writes_deterministic_artifacts(tmp_path) -> None:
    seed_bundle = generate_seed_bundles(base_seed=1, replicate_count=1)[0]
    first = run_direct_masked_random(
        spec=default_tiny_spec(),
        seed_bundle=seed_bundle,
        artifact_root=tmp_path / "first",
        episode_count=2,
    )
    second = run_direct_masked_random(
        spec=default_tiny_spec(),
        seed_bundle=seed_bundle,
        artifact_root=tmp_path / "second",
        episode_count=2,
    )

    assert first.status == "success"
    assert second.status == "success"
    assert "episodes_csv" in first.artifact_paths
    assert (tmp_path / "first").exists()


def test_direct_tabular_q_runner_writes_timing_and_episode_artifacts(tmp_path) -> None:
    seed_bundle = generate_seed_bundles(base_seed=2, replicate_count=1)[0]
    result = run_direct_tabular_q(
        spec=default_tiny_spec(),
        seed_bundle=seed_bundle,
        artifact_root=tmp_path,
        episode_count=2,
    )

    assert result.status == "success"
    assert "timing_segments_csv" in result.artifact_paths
    assert result.summary_path is not None


def test_tower_schema_smoke_runner_writes_schema_artifacts(tmp_path) -> None:
    seed_bundle = generate_seed_bundles(base_seed=3, replicate_count=1)[0]
    result = run_tower_schema_smoke(
        spec=default_tiny_spec(),
        schema_id="counterpoint_empty_schema_v001",
        seed_bundle=seed_bundle,
        artifact_root=tmp_path,
    )

    assert result.status == "success"
    assert "schema_manifest" in result.artifact_paths
    assert "reward_fiber_variance" in result.artifact_paths
