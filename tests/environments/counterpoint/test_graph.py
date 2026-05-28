from big_boy_benchmarking.environments.counterpoint.graph import (
    enumerate_reachable_graph,
    summarize_graph,
)
from big_boy_benchmarking.environments.counterpoint.instances import default_tiny_spec


def test_tiny_graph_enumeration_has_stable_exact_counts() -> None:
    graph = enumerate_reachable_graph(default_tiny_spec())
    summary = summarize_graph(graph)

    assert summary.state_count == 8
    assert summary.edge_count == 16
    assert summary.reachable_start_count == 2
    assert summary.dead_end_count == 0
    assert summary.to_dict()["reward_bundle_id"] == "counterpoint_reward_local_v001"


def test_graph_edges_include_reward_and_labels() -> None:
    graph = enumerate_reachable_graph(default_tiny_spec())

    assert graph.edges
    edge = graph.edges[0]
    assert edge.reward.total_reward != 0
    assert "global_motion_direction_pattern" in edge.labels
