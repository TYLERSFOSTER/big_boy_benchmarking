"""Small import probe proving that state_collapser is a first-class dependency."""

from __future__ import annotations

from typing import TypedDict

import state_collapser
from state_collapser.tower.control import (
    ActiveTierController,
    ActiveTierState,
    ControlAction,
    FrozenLowerContext,
    LiftResolveExecutor,
    TierLearner,
    TierSignalState,
)
from state_collapser.tower.partition import PartitionTower, RewardAggregator
from state_collapser.tower.runtime import ExploitExploreTowerRuntime
from state_collapser.training import (
    ActionDecision,
    ActionSelectionInput,
    EncodingRegistry,
    FiberConditionedStage,
    FrozenQuotientBehavior,
    LinearizationConfig,
    LinearizationReport,
    LinearizationState,
    NumericBackend,
    PathFiber,
    TabularQLearner,
    TensorDeviceKind,
    TrainingTransition,
    build_linearization_report,
)


class DependencyReport(TypedDict):
    """Resolved dependency metadata used by smoke tests and setup checks."""

    state_collapser_version: str
    partition_tower_import: str
    reward_aggregator_import: str
    action_decision_import: str
    action_selection_input_import: str
    encoding_registry_import: str
    linearization_config_import: str
    linearization_report_import: str
    linearization_state_import: str
    numeric_backend_import: str
    tensor_device_kind_import: str
    build_linearization_report_import: str
    tabular_q_learner_import: str
    training_transition_import: str
    fiber_conditioned_stage_import: str
    frozen_quotient_behavior_import: str
    path_fiber_import: str
    active_tier_controller_import: str
    active_tier_state_import: str
    control_action_import: str
    frozen_lower_context_import: str
    lift_resolve_executor_import: str
    tier_learner_import: str
    tier_signal_state_import: str
    exploit_explore_tower_runtime_import: str


def dependency_report() -> DependencyReport:
    """Return import metadata for the state_collapser surfaces this repo benchmarks."""

    return {
        "state_collapser_version": state_collapser.__version__,
        "partition_tower_import": PartitionTower.__name__,
        "reward_aggregator_import": RewardAggregator.__name__,
        "action_decision_import": ActionDecision.__name__,
        "action_selection_input_import": ActionSelectionInput.__name__,
        "encoding_registry_import": EncodingRegistry.__name__,
        "linearization_config_import": LinearizationConfig.__name__,
        "linearization_report_import": LinearizationReport.__name__,
        "linearization_state_import": LinearizationState.__name__,
        "numeric_backend_import": NumericBackend.__name__,
        "tensor_device_kind_import": TensorDeviceKind.__name__,
        "build_linearization_report_import": build_linearization_report.__name__,
        "tabular_q_learner_import": TabularQLearner.__name__,
        "training_transition_import": TrainingTransition.__name__,
        "fiber_conditioned_stage_import": FiberConditionedStage.__name__,
        "frozen_quotient_behavior_import": FrozenQuotientBehavior.__name__,
        "path_fiber_import": PathFiber.__name__,
        "active_tier_controller_import": ActiveTierController.__name__,
        "active_tier_state_import": ActiveTierState.__name__,
        "control_action_import": ControlAction.__name__,
        "frozen_lower_context_import": FrozenLowerContext.__name__,
        "lift_resolve_executor_import": LiftResolveExecutor.__name__,
        "tier_learner_import": TierLearner.__name__,
        "tier_signal_state_import": TierSignalState.__name__,
        "exploit_explore_tower_runtime_import": ExploitExploreTowerRuntime.__name__,
    }
