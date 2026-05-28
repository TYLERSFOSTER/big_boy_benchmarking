import pytest

from big_boy_benchmarking.metrics.bootstrap import mean_std, percentile_bootstrap_interval


def test_bootstrap_interval_is_deterministic() -> None:
    first = percentile_bootstrap_interval([1.0, 2.0, 3.0], seed=7)
    second = percentile_bootstrap_interval([1.0, 2.0, 3.0], seed=7)

    assert first == second


def test_empty_data_rejected() -> None:
    with pytest.raises(ValueError):
        mean_std([])
