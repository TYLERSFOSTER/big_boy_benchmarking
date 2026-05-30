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
