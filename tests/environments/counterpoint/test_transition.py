from big_boy_benchmarking.environments.counterpoint.actions import CounterpointAction
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState
from big_boy_benchmarking.environments.counterpoint.transition import (
    construct_next_state,
    evaluate_transition,
)


def test_transition_candidate_updates_pitches_and_wraps_beat(tiny_spec) -> None:
    state = CounterpointState((60, 64, 67), 3)
    action = CounterpointAction((1, -1, 0))

    assert construct_next_state(tiny_spec, state, action) == CounterpointState((61, 63, 67), 0)


def test_transition_evaluation_reports_legal_and_illegal_paths(tiny_spec) -> None:
    state = CounterpointState((60, 64, 67), 0)
    legal = evaluate_transition(tiny_spec, state, CounterpointAction((0, -1, 0)), step_index=3)
    illegal = evaluate_transition(tiny_spec, state, CounterpointAction((-2, 0, 0)))

    assert legal.legality.is_legal
    assert legal.reward is not None
    assert legal.terminated
    assert not illegal.legality.is_legal
    assert illegal.reward is None
