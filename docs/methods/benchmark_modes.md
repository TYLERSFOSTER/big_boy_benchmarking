# Benchmark Modes

Benchmark modes are contracts, not prose labels.

Each mode binds environment coupling, schema regime, controller regime,
training surface, learner id, timing profile, diagnostic profile, readout
policy, morphism policy, and runnable/reserved status.

Reserved modes may appear in the registry before they are runnable. Ordinary
runners must reject reserved modes unless explicitly allowed by the caller.

See also:

```text
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
```
