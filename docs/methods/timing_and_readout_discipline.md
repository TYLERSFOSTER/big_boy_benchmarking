# Timing And Readout Discipline

Timing must distinguish algorithm cost from benchmark bookkeeping.

Artifact logging, compatibility readouts, morphism construction, posthoc
diagnostics, and summary generation are separate timing categories.

Compatibility readouts and morphism construction are not default hot-path
costs. A run must record whether readout or morphism construction was requested
and whether either actually occurred.

See also:

```text
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
```
