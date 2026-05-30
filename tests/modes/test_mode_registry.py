import pytest

from big_boy_benchmarking.modes.contracts import validate_mode_contract
from big_boy_benchmarking.modes.registry import (
    get_mode_contract,
    iter_mode_contracts,
    require_runnable_mode,
)


def test_known_modes_validate() -> None:
    for contract in iter_mode_contracts():
        validate_mode_contract(contract, allow_reserved=True)


def test_unknown_mode_raises() -> None:
    with pytest.raises(KeyError):
        get_mode_contract("unknown")


def test_exploit_explore_mode_is_runnable_for_serious_learning() -> None:
    contract = get_mode_contract("tower_exploit_explore")

    assert contract.runnable
    assert contract.controller_regime == "exploit_explore"
    assert "controller_decision" in contract.online_costs_included
    assert "compatibility_readout" in contract.online_costs_excluded
    assert require_runnable_mode(contract.mode_id) == contract


def test_direct_and_tower_costs_are_distinct() -> None:
    direct = get_mode_contract("direct_env_tabular")
    tower = get_mode_contract("tower_empty_schema_tabular")

    assert "tower_update" not in direct.online_costs_included
    assert "tower_update" in tower.online_costs_included
