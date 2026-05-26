"""Small import probe proving that state_collapser is a first-class dependency."""

from __future__ import annotations

from typing import TypedDict

import state_collapser
from state_collapser.tower.partition import PartitionTower, RewardAggregator
from state_collapser.training import ActionDecision, ActionSelectionInput


class DependencyReport(TypedDict):
    """Resolved dependency metadata used by smoke tests and setup checks."""

    state_collapser_version: str
    partition_tower_import: str
    reward_aggregator_import: str
    action_decision_import: str
    action_selection_input_import: str


def dependency_report() -> DependencyReport:
    """Return import metadata for the state_collapser surfaces this repo benchmarks."""

    return {
        "state_collapser_version": state_collapser.__version__,
        "partition_tower_import": PartitionTower.__name__,
        "reward_aggregator_import": RewardAggregator.__name__,
        "action_decision_import": ActionDecision.__name__,
        "action_selection_input_import": ActionSelectionInput.__name__,
    }
