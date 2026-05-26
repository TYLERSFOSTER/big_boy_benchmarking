from big_boy_benchmarking import dependency_report


def test_state_collapser_is_a_first_class_dependency() -> None:
    report = dependency_report()

    assert report["state_collapser_version"]
    assert report["partition_tower_import"] == "PartitionTower"
    assert report["reward_aggregator_import"] == "RewardAggregator"
    assert report["action_decision_import"] == "ActionDecision"
    assert report["action_selection_input_import"] == "ActionSelectionInput"
