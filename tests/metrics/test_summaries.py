from big_boy_benchmarking.metrics.summaries import summarize_replicates


def test_summary_records_seed_count() -> None:
    summary = summarize_replicates("reward", [1.0, 2.0], seed=3)

    assert summary["seed_count"] == 2
    assert summary["replicate_count"] == 2
