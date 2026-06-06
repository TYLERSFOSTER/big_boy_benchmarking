from big_boy_benchmarking.environments.plate_support.graph import (
    build_plate_support_graph_diagnostics,
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
