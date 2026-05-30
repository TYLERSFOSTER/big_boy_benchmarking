from state_collapser.training import TabularQLearner

from big_boy_benchmarking.environments.counterpoint.instances import (
    default_tiny_spec,
    initial_states,
)
from big_boy_benchmarking.environments.counterpoint.masks import legal_action_mask
from big_boy_benchmarking.environments.counterpoint.serious_learning.direct import (
    build_direct_action_selection_input,
    build_direct_runtime_context,
    build_direct_training_transition,
    direct_state_key,
)
from big_boy_benchmarking.environments.counterpoint.transition import evaluate_transition


def test_direct_action_selection_input_has_legal_action_mask() -> None:
    spec = default_tiny_spec()
    context = build_direct_runtime_context(spec)
    state = initial_states(spec)[0]
    action_input = build_direct_action_selection_input(context, state)

    assert action_input.current_base_state == state
    assert action_input.tower_position_key == ()
    assert action_input.action_mask == legal_action_mask(spec, state).mask


def test_upstream_tabular_learner_returns_legal_action_id() -> None:
    spec = default_tiny_spec()
    context = build_direct_runtime_context(spec)
    state = initial_states(spec)[0]
    action_input = build_direct_action_selection_input(context, state)
    learner = TabularQLearner(
        action_count=len(context.raw_actions),
        epsilon=0.0,
        seed=1,
        key_fn=direct_state_key,
    )

    decision = learner.act(action_input, mode="train")

    assert action_input.action_mask[decision.chosen_action]


def test_direct_training_transition_update_changes_learner_state() -> None:
    spec = default_tiny_spec()
    context = build_direct_runtime_context(spec)
    state = initial_states(spec)[0]
    action_input = build_direct_action_selection_input(context, state)
    learner = TabularQLearner(
        action_count=len(context.raw_actions),
        alpha=0.5,
        gamma=0.9,
        epsilon=0.0,
        seed=2,
        key_fn=direct_state_key,
    )
    decision = learner.act(action_input, mode="train")
    transition = evaluate_transition(
        spec,
        state,
        context.raw_actions[decision.chosen_action],
        step_index=0,
    )
    reward = 0.0 if transition.reward is None else transition.reward.total_reward
    target_input = build_direct_action_selection_input(context, transition.next_state)
    training_transition = build_direct_training_transition(
        source_input=action_input,
        chosen_action=decision.chosen_action,
        reward=reward,
        target_input=target_input,
        terminated=transition.terminated,
        truncated=transition.truncated,
    )

    learner.observe(training_transition)
    summary = learner.update()

    assert summary.updated
    assert learner.q_table[direct_state_key(action_input)][decision.chosen_action] != 0.0


def test_direct_key_function_distinguishes_concrete_states() -> None:
    spec = default_tiny_spec()
    context = build_direct_runtime_context(spec)
    first, second = initial_states(spec)[:2]

    assert direct_state_key(build_direct_action_selection_input(context, first)) != (
        direct_state_key(build_direct_action_selection_input(context, second))
    )
