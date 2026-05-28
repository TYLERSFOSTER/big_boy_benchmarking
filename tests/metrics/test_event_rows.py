from big_boy_benchmarking.metrics.events import EpisodeRow, StructuralDiagnosticRow


def test_event_rows_serialize_to_flat_dicts() -> None:
    row = EpisodeRow(
        run_id="run",
        episode_index=0,
        seed_bundle_id="seed",
        total_reward=1.0,
        step_count=1,
        terminated=False,
        truncated=False,
    )

    assert row.to_flat_dict()["total_reward"] == 1.0
    assert EpisodeRow.fieldnames()[0] == "run_id"


def test_structural_row_records_readout_lifecycle() -> None:
    row = StructuralDiagnosticRow(
        run_id="run",
        diagnostic_name="compression",
        lifecycle="posthoc",
        exact_or_sampled="sampled",
        readout_backed=True,
        tier_index=1,
        schema_id="schema",
        value="{}",
    )

    assert row.to_flat_dict()["readout_backed"] is True
