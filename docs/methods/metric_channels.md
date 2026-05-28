# Metric Channels

Metrics are separated by lifecycle and cost.

Default online channels should remain cheap enough for smoke and ordinary
benchmark runs. Structural diagnostics may be exact, sampled, online, or
posthoc, but that status must be explicit in the recorded row.

The first machine-readable channels are expected to include run index rows,
episode rows, step event rows, control event rows, timing segment rows,
structural diagnostic rows, warning rows, and bootstrap interval rows.

See also:

```text
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
```
