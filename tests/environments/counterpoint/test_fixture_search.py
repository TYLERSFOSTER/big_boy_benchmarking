from big_boy_benchmarking.environments.counterpoint.fixture_search import (
    evaluate_fixture_candidate,
    search_fixture_candidates,
)
from big_boy_benchmarking.environments.counterpoint.instances import (
    default_tiny_spec,
    tiny_candidate_specs,
)


def test_fixture_search_evaluates_candidate_counts() -> None:
    result = evaluate_fixture_candidate(default_tiny_spec())

    assert result.state_count == 8
    assert result.edge_count == 16
    assert result.exact_path_volume_feasible
    assert result.exact_horizon_path_count == 32


def test_fixture_search_selects_first_feasible_candidate_deterministically() -> None:
    results = search_fixture_candidates(tiny_candidate_specs())

    assert results == search_fixture_candidates(tiny_candidate_specs())
    assert [result.selected for result in results].count(True) == 1
    assert results[0].selected
