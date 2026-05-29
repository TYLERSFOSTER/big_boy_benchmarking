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
