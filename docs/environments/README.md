# Environments

Human-facing environment notes live here.

These pages describe environment families, smoke environments, and eventually
serious benchmark environments in prose. Machine-readable artifacts remain the
source of truth for executed runs.

This folder is stage 1 of the benchmark workflow: environment construction.

Environment docs should say:

- what is being run;
- which fixtures are smoke, calibration, or serious targets;
- what legality, reward, action-mask, initial-state, and terminal contracts
  apply;
- what diagnostics exist;
- what the environment is meant to validate;
- what it is not meant to prove;
- which evaluations use it.

Follow:

```text
docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md
```

## Current Environment Pages

- [Counterpoint symbolic v001](counterpoint_symbolic_v001.md): benchmark-owned
  symbolic hidden-graph environment used by the current counterpoint evaluation
  suite.
- [PlateSupport 5x5 default v001](plate_support_5x5_default_v001.md):
  first-class BBB environment-readiness surface for the upstream constrained
  robotics-style PlateSupport example.
- [Upstream smoke PlateSupport](upstream_smoke_plate_support.md): smoke-only
  upstream import/readout-discipline page, not the first-class environment
  readiness surface.
- [Upstream smoke rl_counterpoint_v3](upstream_smoke_rl_counterpoint_v3.md):
  smoke-only upstream import/readout-discipline page.
