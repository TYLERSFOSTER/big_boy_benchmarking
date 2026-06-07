from big_boy_benchmarking.environments.plate_support.graph import (
    build_plate_support_graph_diagnostics,
)
from big_boy_benchmarking.environments.plate_support.graph_stats import (
    summarize_plate_support_graph,
)


def test_plate_support_graph_diagnostics_match_upstream_contract_facts() -> None:
    diagnostics = build_plate_support_graph_diagnostics()
    summary = diagnostics.graph_summary

    assert summary["candidate_state_count"] == 2700
    assert summary["valid_state_count"] == 89
    assert summary["reachable_state_count"] == 89
    assert summary["reachable_from_start"] is True
    assert summary["action_count"] == 12
    assert summary["shortest_path_length"] == 6
    assert summary["goal_one_step_from_start"] is False
    assert len(diagnostics.transition_records) == 89 * 12
    assert summary["invalid_move_count"] > 0
    assert summary["valid_self_transition_count"] > 0
    assert summary["valid_nonself_edge_count"] > 0


def test_plate_support_graph_stats_summarize_connectivity() -> None:
    stats = summarize_plate_support_graph()

    assert stats["status"] == "ok"
    assert stats["state_space"]["valid_state_count"] == 89
    assert stats["transition_space"]["valid_nonself_edge_count"] == 388
    assert stats["connectivity"]["directed_reachable_from_start_count"] == 89
    assert stats["connectivity"]["weak_component_count"] == 1
    assert stats["connectivity"]["largest_weak_component_share"] == 1.0
    assert stats["task_anchor"]["shortest_path_length"] == 6
