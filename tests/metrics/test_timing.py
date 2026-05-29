from big_boy_benchmarking.metrics.timing import TimingRecorder, summarize_timing_segments


def test_timing_recorder_records_segments() -> None:
    recorder = TimingRecorder.create("run")

    with recorder.segment("artifact_logging"):
        pass

    assert recorder.rows[0].segment_name == "artifact_logging"
    assert recorder.rows[0].category == "benchmark_online"


def test_linearization_timing_segments_have_dedicated_categories() -> None:
    recorder = TimingRecorder.create("run")

    with recorder.segment("encoding_registry_build"):
        pass
    with recorder.segment("linearize_action_selection"):
        pass

    assert recorder.rows[0].category == "linearization_setup"
    assert recorder.rows[1].category == "conversion_online"


def test_timing_summary_separates_categories() -> None:
    recorder = TimingRecorder.create("run")

    with recorder.segment("environment_step"):
        pass
    with recorder.segment("artifact_logging"):
        pass

    summary = summarize_timing_segments(recorder.rows)

    assert "algorithm_online" in summary
    assert "benchmark_online" in summary
