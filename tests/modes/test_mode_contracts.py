import pytest

from big_boy_benchmarking.modes.contracts import (
    BenchmarkModeContract,
    DiagnosticProfile,
    MorphismPolicy,
    ReadoutPolicy,
    TimingProfile,
    validate_mode_contract,
)


def test_direct_env_mode_cannot_claim_tower_costs() -> None:
    contract = BenchmarkModeContract(
        mode_id="direct_env_tabular",
        environment_coupling="direct_env",
        schema_mode="none",
        controller_regime="none",
        training_surface="environment",
        learner_id="tabular",
        diagnostic_profile=DiagnosticProfile("smoke"),
        timing_profile=TimingProfile("default"),
        online_costs_included=("tower_update",),
        online_costs_excluded=(),
        readout_policy=ReadoutPolicy(False, False, "none"),
        morphism_policy=MorphismPolicy(False, False, "none"),
    )

    with pytest.raises(ValueError, match="tower costs"):
        validate_mode_contract(contract)


def test_timing_profile_cannot_include_unrequested_readout() -> None:
    contract = BenchmarkModeContract(
        mode_id="tower_empty_schema_tabular",
        environment_coupling="tower_runtime",
        schema_mode="empty",
        controller_regime="none",
        training_surface="tower",
        learner_id="tabular",
        diagnostic_profile=DiagnosticProfile("diagnostic"),
        timing_profile=TimingProfile("bad", include_readout=True),
        online_costs_included=("tower_update",),
        online_costs_excluded=(),
        readout_policy=ReadoutPolicy(False, False, "none"),
        morphism_policy=MorphismPolicy(False, False, "none"),
    )

    with pytest.raises(ValueError, match="readout"):
        validate_mode_contract(contract)
