from big_boy_benchmarking.environments.counterpoint.actions import CounterpointAction
from big_boy_benchmarking.environments.counterpoint.legality import validate_edge_legality
from big_boy_benchmarking.environments.counterpoint.rewards import (
    evaluate_reward,
    reward_term_specs,
)
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState
from big_boy_benchmarking.environments.counterpoint.transition import construct_next_state


def test_reward_terms_are_action_local_in_v001() -> None:
    for term in reward_term_specs():
        assert "path_history" not in term.input_scope
        assert term.locality_class == "action_local"


def test_reward_bundle_is_deterministic_and_term_level(tiny_spec) -> None:
    state = CounterpointState((60, 64, 67), 0)
    action = CounterpointAction((0, -1, 0))
    next_state = construct_next_state(tiny_spec, state, action)
    legality = validate_edge_legality(tiny_spec, state, action, next_state)

    first = evaluate_reward(tiny_spec, state, action, next_state, legality, terminated=True)
    second = evaluate_reward(tiny_spec, state, action, next_state, legality, terminated=True)

    assert first == second
    assert first.total_reward == sum(term.weighted_value for term in first.terms)
    assert {term.reward_term_id for term in first.terms} == {
        term.reward_term_id for term in reward_term_specs()
    }
