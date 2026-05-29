import pytest

from big_boy_benchmarking.metrics.timing import TimingRecorder
from big_boy_benchmarking.upstream.linearization import (
    build_linearization_artifact_payload,
)


def test_none_control_flow_report_label() -> None:
    recorder = TimingRecorder.create("run")

    payload = build_linearization_artifact_payload(
        linearization_mode_id="none_control_flow",
        recorder=recorder,
    )

    assert payload.report.benchmark_label == "none_control_flow"
    assert payload.report.enabled is False
    assert payload.config_dict["derived_benchmark_label"] == "none_control_flow"


def test_tensor_available_disabled_report_label_does_not_require_torch() -> None:
    recorder = TimingRecorder.create("run")

    payload = build_linearization_artifact_payload(
        linearization_mode_id="tensor_available_disabled",
        recorder=recorder,
    )

    assert payload.report.benchmark_label == "tensor_available_disabled"
    assert payload.report.enabled is False
    assert payload.report_dict["torch_available"] in {True, False}


def test_reserved_modes_are_rejected_by_default() -> None:
    recorder = TimingRecorder.create("run")

    with pytest.raises(ValueError, match="reserved"):
        build_linearization_artifact_payload(
            linearization_mode_id="tensor_enabled_cpu",
            recorder=recorder,
        )


def test_disabled_tower_payload_records_registry() -> None:
    from big_boy_benchmarking.environments.counterpoint.instances import default_tiny_spec
    from big_boy_benchmarking.environments.counterpoint.tower_adapter import (
        build_counterpoint_partition_tower,
    )

    recorder = TimingRecorder.create("run")
    build = build_counterpoint_partition_tower(
        default_tiny_spec(),
        schema_id="counterpoint_empty_schema_v001",
    )

    payload = build_linearization_artifact_payload(
        linearization_mode_id="tensor_available_disabled",
        recorder=recorder,
        tower=build.tower,
    )

    assert payload.report.encoder_registry_id
    assert {row.segment_name for row in recorder.rows} == {
        "encoding_registry_build",
        "linearization_report_build",
    }
