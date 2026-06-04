from big_boy_benchmarking.environments.counterpoint.artifacts import (
    environment_instance_manifest,
)
from big_boy_benchmarking.environments.counterpoint.graph import enumerate_reachable_graph
from big_boy_benchmarking.environments.counterpoint.instances import (
    default_medium_spec,
    default_small_spec,
    default_tiny_spec,
    default_wide_span18_spec,
    initial_states,
    medium_candidate_specs,
    small_candidate_specs,
    tiny_candidate_specs,
    wide_span18_candidate_specs,
)
from big_boy_benchmarking.environments.counterpoint.legality import validate_node_legality
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState


def test_instance_constructors_are_deterministic() -> None:
    assert tiny_candidate_specs() == tiny_candidate_specs()
    assert small_candidate_specs() == small_candidate_specs()
    assert medium_candidate_specs() == medium_candidate_specs()
    assert wide_span18_candidate_specs() == wide_span18_candidate_specs()
    assert default_tiny_spec().environment_instance_id == "counterpoint_symbolic_n3_tiny_v001"
    assert default_small_spec().environment_instance_id == "counterpoint_symbolic_n3_small_v001"
    assert (
        default_medium_spec().environment_instance_id
        == "counterpoint_symbolic_n3_medium_v001"
    )
    assert (
        default_wide_span18_spec().environment_instance_id
        == "counterpoint_symbolic_n3_wide_20_108_span18_v001"
    )


def test_initial_state_policy_returns_legal_states() -> None:
    spec = default_tiny_spec()
    starts = initial_states(spec)

    assert starts
    assert starts == initial_states(spec)
    assert all(validate_node_legality(spec, state).is_legal for state in starts)


def test_medium_fixture_has_initial_states_and_reachable_graph() -> None:
    spec = default_medium_spec()
    starts = initial_states(spec)
    graph = enumerate_reachable_graph(spec)
    manifest = environment_instance_manifest(spec)

    assert starts
    assert all(validate_node_legality(spec, state).is_legal for state in starts)
    assert graph.states
    assert graph.edges
    assert manifest["spec"]["environment_instance_id"] == "counterpoint_symbolic_n3_medium_v001"
    assert manifest["spec"]["environment_family_id"] == "counterpoint_symbolic_v001"


def test_wide_span18_fixture_contract_and_graph_size() -> None:
    spec = default_wide_span18_spec()
    starts = initial_states(spec)
    graph = enumerate_reachable_graph(spec)

    assert spec.voice_count == 3
    assert spec.pitch_min == 20
    assert spec.pitch_max == 108
    assert spec.measure_size == 4
    assert spec.max_outer_span == 18
    assert spec.allowed_outer_interval_classes == (0, 3, 4, 5, 7, 8, 9)
    assert len(graph.states) == 3580
    assert len(graph.edges) == 49172
    assert starts == (
        CounterpointState.from_iterable((60, 64, 67), 0),
        CounterpointState.from_iterable((60, 63, 67), 0),
        CounterpointState.from_iterable((60, 64, 68), 0),
        CounterpointState.from_iterable((60, 63, 68), 0),
    )
