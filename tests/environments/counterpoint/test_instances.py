from big_boy_benchmarking.environments.counterpoint.instances import (
    default_small_spec,
    default_tiny_spec,
    initial_states,
    small_candidate_specs,
    tiny_candidate_specs,
)
from big_boy_benchmarking.environments.counterpoint.legality import validate_node_legality


def test_instance_constructors_are_deterministic() -> None:
    assert tiny_candidate_specs() == tiny_candidate_specs()
    assert small_candidate_specs() == small_candidate_specs()
    assert default_tiny_spec().environment_instance_id == "counterpoint_symbolic_n3_tiny_v001"
    assert default_small_spec().environment_instance_id == "counterpoint_symbolic_n3_small_v001"


def test_initial_state_policy_returns_legal_states() -> None:
    spec = default_tiny_spec()
    starts = initial_states(spec)

    assert starts
    assert starts == initial_states(spec)
    assert all(validate_node_legality(spec, state).is_legal for state in starts)
