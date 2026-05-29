from big_boy_benchmarking.upstream.state_collapser import (
    REQUIRED_LINEARIZATION_SYMBOLS,
    collect_state_collapser_dependency_state,
)


def test_dependency_state_collects_version() -> None:
    state = collect_state_collapser_dependency_state()

    assert state.import_version
    assert state.inspection_status == "ok"


def test_dependency_state_collects_linearization_imports() -> None:
    state = collect_state_collapser_dependency_state()

    assert state.linearization_import_status == "ok"
    assert state.linearization_symbols == REQUIRED_LINEARIZATION_SYMBOLS


def test_dependency_state_records_optional_torch_state_without_requiring_torch() -> None:
    state = collect_state_collapser_dependency_state()

    assert state.torch_import_status in {
        "ok",
        "missing",
        "state_collapser_torch_import_failed:ModuleNotFoundError:"
        "No module named 'state_collapser.training.torch'",
    } or state.torch_import_status.startswith("torch_import_failed:")
    assert state.cuda_available in {True, False, None}
