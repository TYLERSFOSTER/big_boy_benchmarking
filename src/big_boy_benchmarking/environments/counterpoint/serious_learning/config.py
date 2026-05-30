"""Config contracts for the first serious counterpoint learning evaluation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from big_boy_benchmarking.artifacts.manifests import to_json_dict


@dataclass(frozen=True)
class ExploitExploreControllerConfig:
    controller_config_id: str = "exploit_explore_controller_v001"
    epsilon: float = 0.2
    min_visit_count: int = 5
    td_error_threshold: float = 0.5
    success_threshold: float = 0.6
    reward_residual_threshold: float | None = None
    training_interval: int = 4
    batch_size: int = 8

    def __post_init__(self) -> None:
        _require_probability(self.epsilon, "epsilon")
        _require_probability(self.success_threshold, "success_threshold")
        _require_nonnegative(self.td_error_threshold, "td_error_threshold")
        if self.reward_residual_threshold is not None:
            _require_nonnegative(self.reward_residual_threshold, "reward_residual_threshold")
        _require_positive(self.min_visit_count, "min_visit_count")
        _require_positive(self.training_interval, "training_interval")
        _require_positive(self.batch_size, "batch_size")

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(self)


@dataclass(frozen=True)
class TabularQLearnerConfig:
    learner_config_id: str = "tabular_q_v001"
    alpha: float = 0.4
    gamma: float = 0.9
    epsilon: float = 0.2
    action_count_policy: str = "counterpoint_raw_action_count"

    def __post_init__(self) -> None:
        _require_probability(self.alpha, "alpha")
        _require_probability(self.gamma, "gamma")
        _require_probability(self.epsilon, "epsilon")
        if not self.action_count_policy:
            raise ValueError("action_count_policy must be nonempty")

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(self)


@dataclass(frozen=True)
class SeriousLearningRunConfig:
    run_config_id: str = "counterpoint_first_serious_learning_v001"
    linearization_mode_id: str = "tensor_available_disabled"
    readout_policy: str = "hot_path_readout_forbidden"
    morphism_policy: str = "hot_path_morphism_forbidden"
    artifact_schema_version: str = "bbb.v001"
    controller_config: ExploitExploreControllerConfig = field(
        default_factory=ExploitExploreControllerConfig
    )
    learner_config: TabularQLearnerConfig = field(default_factory=TabularQLearnerConfig)

    def __post_init__(self) -> None:
        if self.linearization_mode_id != "tensor_available_disabled":
            raise ValueError("serious learning defaults reject reserved linearization modes")
        if self.readout_policy != "hot_path_readout_forbidden":
            raise ValueError("serious learning hot path forbids compatibility readouts")
        if self.morphism_policy != "hot_path_morphism_forbidden":
            raise ValueError("serious learning hot path forbids morphism construction")

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(asdict(self))


def _require_probability(value: float, field_name: str) -> None:
    if value < 0.0 or value > 1.0:
        raise ValueError(f"{field_name} must be between 0 and 1")


def _require_nonnegative(value: float, field_name: str) -> None:
    if value < 0.0:
        raise ValueError(f"{field_name} must be nonnegative")


def _require_positive(value: int, field_name: str) -> None:
    if value <= 0:
        raise ValueError(f"{field_name} must be positive")
