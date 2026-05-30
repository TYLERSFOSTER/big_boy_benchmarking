import pytest

from big_boy_benchmarking.environments.counterpoint.serious_learning.config import (
    ExploitExploreControllerConfig,
    SeriousLearningRunConfig,
    TabularQLearnerConfig,
)


def test_config_defaults_are_deterministic_and_json_safe() -> None:
    first = SeriousLearningRunConfig().to_dict()
    second = SeriousLearningRunConfig().to_dict()

    assert first == second
    assert first["linearization_mode_id"] == "tensor_available_disabled"
    assert first["controller_config"]["training_interval"] == 4
    assert first["learner_config"]["action_count_policy"] == "counterpoint_raw_action_count"


@pytest.mark.parametrize(
    ("kwargs", "match"),
    [
        ({"epsilon": -0.1}, "epsilon"),
        ({"epsilon": 1.1}, "epsilon"),
        ({"min_visit_count": 0}, "min_visit_count"),
        ({"training_interval": 0}, "training_interval"),
    ],
)
def test_controller_config_validates_ranges(kwargs, match) -> None:
    with pytest.raises(ValueError, match=match):
        ExploitExploreControllerConfig(**kwargs)


@pytest.mark.parametrize("field_name", ["alpha", "gamma", "epsilon"])
def test_learner_config_validates_probability_ranges(field_name: str) -> None:
    with pytest.raises(ValueError, match=field_name):
        TabularQLearnerConfig(**{field_name: 1.5})


def test_reserved_linearization_modes_fail_by_default() -> None:
    with pytest.raises(ValueError, match="reserved linearization"):
        SeriousLearningRunConfig(linearization_mode_id="tensor_enabled_cpu")
