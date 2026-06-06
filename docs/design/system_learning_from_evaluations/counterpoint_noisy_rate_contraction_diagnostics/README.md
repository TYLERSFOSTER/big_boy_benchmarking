# Counterpoint Noisy-Rate Contraction Diagnostics

This folder preserves the design thread for a proposed noisy-rate contraction
diagnostic prompted by the `1/18` collapse observed in the source-local
fraction sweep smoke run.

The diagnostic now has a first smoke-verified implementation in
`big_boy_benchmarking`. It should still be treated as a diagnostic evaluation,
not as a learning-performance comparison. Its first purpose is to test whether
the observed `1/18` singleton collapse was driven by the previous
source-local minimum-one quota rule:

```text
max(1, ceil(out_degree * n / denominator))
```

The key proposed change is to replace source-covering deterministic quotas
with a noisy expected-rate selector that allows many sources to contribute zero
scheduled edges.

## Source Readout

- Source readout: `docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/README.md`
- Parent diagnostic archive: `docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/README.md`
- Implementation log: `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/04_counterpoint_noisy_rate_contraction_diagnostics_implementation_log.md`
- Repo readout surface: `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/`
- Smoke artifact run: `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/artifacts/smoke_001/`
- Current status: smoke run complete; full small+medium validation remains behind the Phase 8 Project Owner decision lock.

## Local Files

- [Fraction Sweep Readout Conversation Archive](01_fraction_sweep_readout_conversation_archive.md)
- [Noisy-Rate Contraction Diagnostics Blueprint](02_counterpoint_noisy_rate_contraction_diagnostics_blueprint.md)
- [Noisy-Rate Contraction Diagnostics Implementation Workplan](03_counterpoint_noisy_rate_contraction_diagnostics_implementation_workplan.md)
- [Noisy-Rate Contraction Diagnostics Implementation Log](04_counterpoint_noisy_rate_contraction_diagnostics_implementation_log.md)

## Initial Design Hypothesis

The `1/18` source-local fraction sweep did not behave like a globally tiny
edge-budget. It scheduled at least one outgoing edge from every source state.
That gave the scheduled block full source coverage, and repeated endpoint
coalescence then had enough useful identifications to collapse the small
fixture into one first-tier state cell.

A noisy-rate diagnostic should separate these variables:

- expected selected edge rate;
- realized selected edge count;
- realized source coverage;
- zero-selected-source count;
- endpoint-coalescence collapse behavior;
- active executable tier surface after tower construction.

The likely first design question is whether to use edge Bernoulli selection,
source-local binomial selection, or another seeded random-rate selector.
