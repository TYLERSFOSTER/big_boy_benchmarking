from state_collapser.core.edges import BaseEdge
from state_collapser.tower.partition import PartitionTower

from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.actions import CounterpointAction
from big_boy_benchmarking.environments.counterpoint.instances import default_tiny_spec
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState
from big_boy_benchmarking.environments.counterpoint.tower_adapter import (
    CounterpointHiddenGraph,
    build_counterpoint_partition_tower,
    counterpoint_action_to_primitive_action,
    counterpoint_state_to_core_state,
    graph_edge_to_base_edge,
)


def test_hidden_graph_adapter_exposes_states_actions_and_edges() -> None:
    spec = default_tiny_spec()
    hidden_graph = CounterpointHiddenGraph(spec)
    state = counterpoint_state_to_core_state(CounterpointState((60, 64, 67), 0))

    actions = tuple(hidden_graph.out_actions(state))
    edges = tuple(hidden_graph.out_edges(state))

    assert hidden_graph.is_valid_state(state)
    assert actions
    assert all(hidden_graph.is_valid_action(action) for action in actions)
    assert all(isinstance(edge, BaseEdge) for edge in edges)


def test_partition_tower_builds_without_compatibility_readout(monkeypatch) -> None:
    def fail_readout(self):  # noqa: ANN001
        raise AssertionError("compatibility readout should not be called")

    monkeypatch.setattr(PartitionTower, "to_quotient_tier_views", fail_readout)

    result = build_counterpoint_partition_tower(
        default_tiny_spec(),
        schema_id=ids.STRUCTURED_MOTION_SCHEMA_ID,
    )

    assert len(result.tower.state_layers) > 1
    assert result.tower.last_update_result is not None


def test_adapter_identity_surfaces_are_stable() -> None:
    state = CounterpointState((60, 64, 67), 0)
    action = CounterpointAction((0, -1, 0))
    core_state = counterpoint_state_to_core_state(state)
    primitive_action = counterpoint_action_to_primitive_action(action)

    assert core_state.canonical_identity == (
        "counterpoint_symbolic_v001_state",
        state.pitches,
        state.beat_index,
    )
    assert primitive_action.canonical_identity == (
        "counterpoint_symbolic_v001_action",
        action.deltas,
    )


def test_base_edge_labels_are_hashable() -> None:
    build = build_counterpoint_partition_tower(default_tiny_spec(), schema_id=ids.EMPTY_SCHEMA_ID)
    edge = graph_edge_to_base_edge(build.graph.edges[0])

    assert hash(edge)
    assert "counterpoint_transition" in edge.labels
