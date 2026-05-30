# Benchmark Modes

Benchmark modes are contracts, not prose labels.

Each mode binds environment coupling, schema regime, controller regime,
training surface, learner id, timing profile, diagnostic profile, readout
policy, morphism policy, and runnable/reserved status.

Tensorization is a companion condition, not a replacement for execution mode.
An execution mode such as `direct_env_tabular` answers what run shape was used.
A linearization mode answers which `state_collapser` semantic-to-numeric
boundary condition was active.

The first linearization modes are:

```text
none_control_flow
tensor_available_disabled
tensor_enabled_cpu
tensor_enabled_cuda
```

`none_control_flow` and `tensor_available_disabled` are runnable in the first
BBB integration slice. CPU and CUDA tensor-enabled modes are reserved until BBB
has a real tensor-consuming runner and local device validation.

Reserved modes may appear in the registry before they are runnable. Ordinary
runners must reject reserved modes unless explicitly allowed by the caller.

The first serious counterpoint learning slice makes this mode runnable:

```text
tower_exploit_explore
```

It is the active-tier exploit/explore tower-control mode. It is distinct from
`tower_empty_schema_tabular` and `tower_nonempty_schema_tabular`, which remain
smoke/diagnostic tower-construction surfaces rather than the serious online
control runner.

See also:

```text
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
docs/methods/counterpoint_serious_learning.md
```
