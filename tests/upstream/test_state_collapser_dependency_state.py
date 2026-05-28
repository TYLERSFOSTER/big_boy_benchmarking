from big_boy_benchmarking.upstream.state_collapser import (
    collect_state_collapser_dependency_state,
)


def test_dependency_state_collects_version() -> None:
    state = collect_state_collapser_dependency_state()

    assert state.import_version
    assert state.inspection_status == "ok"
