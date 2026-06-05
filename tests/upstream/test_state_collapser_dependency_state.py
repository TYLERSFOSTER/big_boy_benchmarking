import inspect

from state_collapser.tower.runtime import ExploitExploreTowerRuntime

from big_boy_benchmarking.upstream.state_collapser import (
    REQUIRED_LINEARIZATION_SYMBOLS,
    REQUIRED_SERIOUS_TRAINING_SYMBOLS,
    REQUIRED_TOWER_CONTROL_SYMBOLS,
    REQUIRED_TOWER_PARTITION_SYMBOLS,
    REQUIRED_TOWER_RUNTIME_SYMBOLS,
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


def test_dependency_state_collects_serious_learning_imports() -> None:
    state = collect_state_collapser_dependency_state()

    assert state.import_version == "0.7.2"
    assert state.serious_training_import_status == "ok"
    assert state.serious_training_symbols == REQUIRED_SERIOUS_TRAINING_SYMBOLS
    assert state.tower_control_import_status == "ok"
    assert state.tower_control_symbols == REQUIRED_TOWER_CONTROL_SYMBOLS
    assert state.tower_runtime_import_status == "ok"
    assert state.tower_runtime_symbols == REQUIRED_TOWER_RUNTIME_SYMBOLS
    assert state.tower_partition_import_status == "ok"
    assert state.tower_partition_symbols == REQUIRED_TOWER_PARTITION_SYMBOLS


def test_exploit_explore_runtime_exposes_executable_tier_predicate() -> None:
    signature = inspect.signature(ExploitExploreTowerRuntime)

    assert "tier_is_executable" in signature.parameters


def test_dependency_state_records_optional_torch_state_without_requiring_torch() -> None:
    state = collect_state_collapser_dependency_state()

    assert state.torch_import_status in {
        "ok",
        "missing",
        "state_collapser_torch_import_failed:ModuleNotFoundError:"
        "No module named 'state_collapser.training.torch'",
    } or state.torch_import_status.startswith("torch_import_failed:")
    assert state.cuda_available in {True, False, None}
