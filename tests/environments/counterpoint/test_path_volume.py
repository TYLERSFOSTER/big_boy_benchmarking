from big_boy_benchmarking.environments.counterpoint.instances import default_tiny_spec
from big_boy_benchmarking.environments.counterpoint.path_volume import (
    exact_path_volume,
    random_legal_policy_path_volume,
    sampled_path_volume,
)


def test_exact_path_volume_counts_tiny_fixture() -> None:
    spec = default_tiny_spec()
    summary = exact_path_volume(spec, length=spec.horizon_steps)

    assert summary.exact_or_sampled == "exact"
    assert summary.exactly_length_count == 32
    assert summary.up_to_length_count == 60


def test_sampled_path_volume_is_deterministic() -> None:
    spec = default_tiny_spec()
    first = sampled_path_volume(
        spec,
        length=spec.horizon_steps,
        sample_count=12,
        diagnostic_sampling_seed=123,
    )
    second = sampled_path_volume(
        spec,
        length=spec.horizon_steps,
        sample_count=12,
        diagnostic_sampling_seed=123,
    )

    assert first == second
    assert first.exact_or_sampled == "sampled"


def test_policy_effective_path_volume_records_policy_id() -> None:
    summary = random_legal_policy_path_volume(
        default_tiny_spec(),
        length=2,
        sample_count=4,
        diagnostic_sampling_seed=321,
    )

    assert summary.policy_id == "random_legal_policy_v001"
