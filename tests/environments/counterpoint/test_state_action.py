import pytest

from big_boy_benchmarking.environments.counterpoint.actions import (
    CounterpointAction,
    enumerate_raw_actions,
    validate_action,
)
from big_boy_benchmarking.environments.counterpoint.specs import make_instance_spec
from big_boy_benchmarking.environments.counterpoint.state import (
    CounterpointState,
    validate_state,
)


def test_state_serialization_hashing_and_validation(tiny_spec) -> None:
    state = CounterpointState((60, 64, 67), 0)

    assert hash(state)
    assert state.to_dict() == {"pitches": (60, 64, 67), "beat_index": 0}
    validate_state(tiny_spec, state)


@pytest.mark.parametrize(
    ("bad_state", "message"),
    [
        (CounterpointState((60, 64), 0), "voice_count"),
        (CounterpointState((59, 64, 67), 0), "pitch"),
        (CounterpointState((60, 60, 67), 0), "strictly ordered"),
        (CounterpointState((60, 61, 67), 0), "adjacent"),
        (CounterpointState((60, 64, 67), 4), "beat_index"),
    ],
)
def test_state_validation_rejects_invalid_states(tiny_spec, bad_state, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        validate_state(tiny_spec, bad_state)


def test_action_serialization_hashing_and_validation(tiny_spec) -> None:
    action = CounterpointAction((-1, 0, 1))

    assert hash(action)
    assert action.to_dict() == {"deltas": (-1, 0, 1)}
    validate_action(tiny_spec, action)


def test_action_enumeration_counts_stationary_policy() -> None:
    with_stationary = make_instance_spec(
        environment_instance_id="with_stationary",
        voice_count=2,
        pitch_min=60,
        pitch_max=64,
        measure_size=4,
        horizon_steps=4,
        max_step_size=1,
        allow_stationary_voice=True,
    )
    without_stationary = make_instance_spec(
        environment_instance_id="without_stationary",
        voice_count=2,
        pitch_min=60,
        pitch_max=64,
        measure_size=4,
        horizon_steps=4,
        max_step_size=1,
        allow_stationary_voice=False,
    )

    assert len(enumerate_raw_actions(with_stationary)) == 9
    assert len(enumerate_raw_actions(without_stationary)) == 4


def test_action_validation_rejects_delta_and_stationary_policy() -> None:
    spec = make_instance_spec(
        environment_instance_id="without_stationary",
        voice_count=2,
        pitch_min=60,
        pitch_max=64,
        measure_size=4,
        horizon_steps=4,
        max_step_size=1,
        allow_stationary_voice=False,
    )

    with pytest.raises(ValueError, match="stationary"):
        validate_action(spec, CounterpointAction((0, 1)))
    with pytest.raises(ValueError, match="max_step_size"):
        validate_action(spec, CounterpointAction((2, 1)))
