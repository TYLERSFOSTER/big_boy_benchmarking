# Environments

Human-facing environment notes live here. Machine-readable artifacts remain the
source of truth for executed runs.

This folder owns the first step of the BBB workflow:

```text
1. Construct an environment.
```

Environment docs should describe:

- what is being run;
- which fixtures are smoke, calibration, or serious targets;
- legality, reward, action-mask, initial-state, and terminal contracts;
- diagnostics and readiness surfaces;
- what the environment is meant to validate;
- what the environment is not meant to prove;
- which evaluations use it.

## Current Environment Families

| Environment | Status | Docs | Evaluations |
| --- | --- | --- | --- |
| Counterpoint Symbolic v001 | Active calibration/smoke environment | [counterpoint_symbolic_v001.md](counterpoint_symbolic_v001.md) | first serious learning, one-third diagnostics, fraction sweep, noisy-rate diagnostics, full-tower training health, schema comparison, threshold frontier, small paired replicate |
| PlateSupport 5x5 Default v001 | Active constrained robotics-style calibration/smoke environment | [plate_support_5x5_default_v001.md](plate_support_5x5_default_v001.md) | environment readiness and standard gauntlet |

## Upstream Smoke Pages

These are integration/readout-discipline pages, not first-class environment
readiness surfaces:

- [upstream smoke PlateSupport](upstream_smoke_plate_support.md)
- [upstream smoke rl_counterpoint_v3](upstream_smoke_rl_counterpoint_v3.md)

## Protocol

Follow:

```text
docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md
```

