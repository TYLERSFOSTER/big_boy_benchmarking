from big_boy_benchmarking import dependency_report


def test_state_collapser_is_a_first_class_dependency() -> None:
    report = dependency_report()

    assert report["state_collapser_version"]
    assert report["partition_tower_import"] == "PartitionTower"
    assert report["reward_aggregator_import"] == "RewardAggregator"
    assert report["action_decision_import"] == "ActionDecision"
    assert report["action_selection_input_import"] == "ActionSelectionInput"
    assert report["encoding_registry_import"] == "EncodingRegistry"
    assert report["linearization_config_import"] == "LinearizationConfig"
    assert report["linearization_report_import"] == "LinearizationReport"
    assert report["linearization_state_import"] == "LinearizationState"
    assert report["numeric_backend_import"] == "NumericBackend"
    assert report["tensor_device_kind_import"] == "TensorDeviceKind"
    assert report["build_linearization_report_import"] == "build_linearization_report"
    assert report["tabular_q_learner_import"] == "TabularQLearner"
    assert report["training_transition_import"] == "TrainingTransition"
    assert report["fiber_conditioned_stage_import"] == "FiberConditionedStage"
    assert report["frozen_quotient_behavior_import"] == "FrozenQuotientBehavior"
    assert report["path_fiber_import"] == "PathFiber"
    assert report["active_tier_controller_import"] == "ActiveTierController"
    assert report["active_tier_state_import"] == "ActiveTierState"
    assert report["control_action_import"] == "ControlAction"
    assert report["frozen_lower_context_import"] == "FrozenLowerContext"
    assert report["lift_resolve_executor_import"] == "LiftResolveExecutor"
    assert report["tier_learner_import"] == "TierLearner"
    assert report["tier_signal_state_import"] == "TierSignalState"
    assert report["exploit_explore_tower_runtime_import"] == "ExploitExploreTowerRuntime"
