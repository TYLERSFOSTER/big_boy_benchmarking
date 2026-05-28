from big_boy_benchmarking.environments.counterpoint.actions import CounterpointAction
from big_boy_benchmarking.environments.counterpoint.labels import emit_edge_labels, movement_class
from big_boy_benchmarking.environments.counterpoint.legality import validate_edge_legality
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState
from big_boy_benchmarking.environments.counterpoint.transition import construct_next_state


def test_movement_class_thresholds_are_versioned_contract_behavior() -> None:
    assert movement_class(-3) == "down_leap"
    assert movement_class(-1) == "down_step"
    assert movement_class(0) == "stationary"
    assert movement_class(1) == "up_step"
    assert movement_class(3) == "up_leap"


def test_edge_labels_are_deterministic_and_not_reward_outcomes(tiny_spec) -> None:
    state = CounterpointState((60, 64, 67), 0)
    action = CounterpointAction((0, -1, 0))
    next_state = construct_next_state(tiny_spec, state, action)
    legality = validate_edge_legality(tiny_spec, state, action, next_state)

    labels = emit_edge_labels(tiny_spec, state, action, next_state, legality, terminal=False)

    assert labels["beat_phase_before"] == 0
    assert labels["beat_phase_after"] == 1
    assert labels["per_voice_movement_class"] == ("stationary", "down_step", "stationary")
    assert "reward" not in labels
