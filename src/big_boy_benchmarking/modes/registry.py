"""Canonical first mode registry."""

from __future__ import annotations

from big_boy_benchmarking.modes.contracts import (
    BenchmarkModeContract,
    DiagnosticProfile,
    MorphismPolicy,
    ReadoutPolicy,
    TimingProfile,
    validate_mode_contract,
)


def _no_readout(reason: str = "default hot path excludes compatibility readouts") -> ReadoutPolicy:
    return ReadoutPolicy(requested=False, allowed=False, reason=reason)


def _no_morphism(reason: str = "default hot path excludes morphism construction") -> MorphismPolicy:
    return MorphismPolicy(requested=False, allowed=False, reason=reason)


_MODES: dict[str, BenchmarkModeContract] = {
    "direct_env_tabular": BenchmarkModeContract(
        mode_id="direct_env_tabular",
        environment_coupling="direct_env",
        schema_mode="none",
        controller_regime="none",
        training_surface="environment",
        learner_id="tabular_q",
        diagnostic_profile=DiagnosticProfile("smoke"),
        timing_profile=TimingProfile("default_online"),
        online_costs_included=("environment_reset", "environment_step", "learner_act"),
        online_costs_excluded=(
            "tower_reset",
            "tower_update",
            "compatibility_readout",
            "morphism_construction",
        ),
        readout_policy=_no_readout(),
        morphism_policy=_no_morphism(),
    ),
    "tower_empty_schema_tabular": BenchmarkModeContract(
        mode_id="tower_empty_schema_tabular",
        environment_coupling="tower_runtime",
        schema_mode="empty",
        controller_regime="none",
        training_surface="tower",
        learner_id="tabular_q",
        diagnostic_profile=DiagnosticProfile("smoke"),
        timing_profile=TimingProfile("default_online"),
        online_costs_included=(
            "environment_reset",
            "environment_step",
            "tower_reset",
            "tower_update",
            "learner_act",
        ),
        online_costs_excluded=("compatibility_readout", "morphism_construction"),
        readout_policy=_no_readout(),
        morphism_policy=_no_morphism(),
    ),
    "tower_nonempty_schema_tabular": BenchmarkModeContract(
        mode_id="tower_nonempty_schema_tabular",
        environment_coupling="tower_runtime",
        schema_mode="dimensionwise",
        controller_regime="none",
        training_surface="tower",
        learner_id="tabular_q",
        diagnostic_profile=DiagnosticProfile("diagnostic", structural_diagnostics="sampled"),
        timing_profile=TimingProfile("diagnostic_readout", include_readout=True),
        online_costs_included=(
            "environment_reset",
            "environment_step",
            "tower_reset",
            "tower_update",
            "learner_act",
        ),
        online_costs_excluded=("morphism_construction",),
        readout_policy=ReadoutPolicy(
            requested=True,
            allowed=True,
            reason="diagnostic mode explicitly requests compatibility readout",
        ),
        morphism_policy=_no_morphism(),
    ),
    "tower_exploit_explore": BenchmarkModeContract(
        mode_id="tower_exploit_explore",
        environment_coupling="tower_runtime",
        schema_mode="schema_configured",
        controller_regime="exploit_explore",
        training_surface="tower",
        learner_id="tabular_q",
        diagnostic_profile=DiagnosticProfile("reserved"),
        timing_profile=TimingProfile("reserved"),
        online_costs_included=("tower_reset", "tower_update", "controller_decision"),
        online_costs_excluded=("compatibility_readout", "morphism_construction"),
        readout_policy=_no_readout("reserved mode has no readout policy execution yet"),
        morphism_policy=_no_morphism("reserved mode has no morphism policy execution yet"),
        runnable=False,
        reserved_reason="controller runner is not implemented in the first shared slice",
    ),
    "tower_fiber_conditioned_stage": BenchmarkModeContract(
        mode_id="tower_fiber_conditioned_stage",
        environment_coupling="tower_runtime",
        schema_mode="schema_configured",
        controller_regime="fiber_conditioned_stage",
        training_surface="fiber_conditioned",
        learner_id="tabular_q",
        diagnostic_profile=DiagnosticProfile("reserved"),
        timing_profile=TimingProfile("reserved"),
        online_costs_included=("tower_reset", "tower_update", "controller_decision"),
        online_costs_excluded=("compatibility_readout", "morphism_construction"),
        readout_policy=_no_readout("reserved mode has no readout policy execution yet"),
        morphism_policy=_no_morphism("reserved mode has no morphism policy execution yet"),
        runnable=False,
        reserved_reason="fiber-conditioned runner is not implemented in this slice",
    ),
    "tower_control_with_fiber_conditioned_substages": BenchmarkModeContract(
        mode_id="tower_control_with_fiber_conditioned_substages",
        environment_coupling="tower_runtime",
        schema_mode="schema_configured",
        controller_regime="tier_control",
        training_surface="fiber_conditioned",
        learner_id="tabular_q",
        diagnostic_profile=DiagnosticProfile("reserved"),
        timing_profile=TimingProfile("reserved"),
        online_costs_included=("tower_reset", "tower_update", "controller_decision"),
        online_costs_excluded=("compatibility_readout", "morphism_construction"),
        readout_policy=_no_readout("reserved mode has no readout policy execution yet"),
        morphism_policy=_no_morphism("reserved mode has no morphism policy execution yet"),
        runnable=False,
        reserved_reason="control/substage runner is not implemented in this slice",
    ),
}


def iter_mode_contracts() -> tuple[BenchmarkModeContract, ...]:
    return tuple(_MODES.values())


def get_mode_contract(mode_id: str) -> BenchmarkModeContract:
    try:
        return _MODES[mode_id]
    except KeyError as exc:
        raise KeyError(f"unknown benchmark mode: {mode_id}") from exc


def require_runnable_mode(mode_id: str) -> BenchmarkModeContract:
    contract = get_mode_contract(mode_id)
    validate_mode_contract(contract)
    return contract


for _contract in _MODES.values():
    validate_mode_contract(_contract, allow_reserved=True)
