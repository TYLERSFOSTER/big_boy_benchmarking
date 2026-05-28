from big_boy_benchmarking.environments.counterpoint.actions import CounterpointAction
from big_boy_benchmarking.environments.counterpoint.legality import (
    validate_edge_legality,
    validate_node_legality,
)
from big_boy_benchmarking.environments.counterpoint.specs import make_instance_spec
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState
from big_boy_benchmarking.environments.counterpoint.transition import construct_next_state


def test_node_legality_reports_required_failure_reasons(tiny_spec) -> None:
    cases = [
        (CounterpointState((59, 64, 67), 0), "pitch_band_violation"),
        (CounterpointState((60, 60, 67), 0), "strict_voice_order_violation"),
        (CounterpointState((60, 61, 67), 0), "adjacent_interval_class_violation"),
        (CounterpointState((60, 63, 66), 0), "outer_interval_class_violation"),
        (CounterpointState((60, 64, 67), 4), "beat_index_out_of_range"),
    ]

    for state, reason in cases:
        assert reason in validate_node_legality(tiny_spec, state).failure_reasons


def test_node_legality_reports_span_and_root_failures() -> None:
    span_spec = make_instance_spec(
        environment_instance_id="span",
        voice_count=3,
        pitch_min=60,
        pitch_max=70,
        measure_size=4,
        horizon_steps=4,
        max_step_size=2,
        max_outer_span=6,
    )
    root_spec = make_instance_spec(
        environment_instance_id="root",
        voice_count=3,
        pitch_min=60,
        pitch_max=70,
        measure_size=4,
        horizon_steps=4,
        max_step_size=2,
        allowed_root_interval_classes=(0,),
    )

    assert "max_outer_span_violation" in validate_node_legality(
        span_spec,
        CounterpointState((60, 64, 67), 0),
    ).failure_reasons
    assert "root_interval_class_violation" in validate_node_legality(
        root_spec,
        CounterpointState((62, 65, 69), 0),
    ).failure_reasons


def test_edge_legality_reports_required_failure_reasons(tiny_spec) -> None:
    state = CounterpointState((60, 64, 67), 0)

    too_large = CounterpointAction((3, 0, 0))
    candidate = construct_next_state(tiny_spec, state, too_large)
    assert "action_delta_bound_violation" in validate_edge_legality(
        tiny_spec,
        state,
        too_large,
        candidate,
    ).failure_reasons

    band = CounterpointAction((-2, 0, 0))
    candidate = construct_next_state(tiny_spec, state, band)
    assert "candidate_pitch_band_violation" in validate_edge_legality(
        tiny_spec,
        state,
        band,
        candidate,
    ).failure_reasons


def test_edge_legality_reports_stationary_and_parallel_failures() -> None:
    no_stationary = make_instance_spec(
        environment_instance_id="no_stationary",
        voice_count=3,
        pitch_min=60,
        pitch_max=70,
        measure_size=4,
        horizon_steps=4,
        max_step_size=2,
        allow_stationary_voice=False,
    )
    state = CounterpointState((60, 64, 67), 0)
    action = CounterpointAction((-1, 0, 1))
    candidate = construct_next_state(no_stationary, state, action)
    assert "stationary_voice_violation" in validate_edge_legality(
        no_stationary,
        state,
        action,
        candidate,
    ).failure_reasons

    parallel_spec = make_instance_spec(
        environment_instance_id="parallel",
        voice_count=3,
        pitch_min=60,
        pitch_max=70,
        measure_size=4,
        horizon_steps=4,
        max_step_size=2,
        allowed_root_interval_classes=(0, 1, 2, 4, 5, 7, 9, 11),
    )
    parallel = CounterpointAction((1, 1, 1))
    candidate = construct_next_state(parallel_spec, state, parallel)
    assert "forbidden_parallel_interval_class_7" in validate_edge_legality(
        parallel_spec,
        state,
        parallel,
        candidate,
    ).failure_reasons
