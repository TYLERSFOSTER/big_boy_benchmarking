# Counterpoint Noisy-Rate Full-Tower Training Diagnostic

This folder is the design surface for a proposed counterpoint evaluation that
trains on each non-collapsed noisy-rate tower identified by the current
diagnostic readout.

The intended evaluation is not a direct-vs-tower comparison and not yet a
learning-advantage claim. It is a tower-training health diagnostic:

```text
For each selected non-collapsed noisy-rate counterpoint tower, build the full
available tower and run a real tower-only training budget on it.
```

## Status

- Design discussion opened.
- Draft blueprint written.
- Implementation workplan written.
- Implementation smoke completed on
  `codex/noisy-rate-full-tower-training-diagnostic`.
- Repo readout surface generated at:
  `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/`
- Main full diagnostic budget remains decision-locked pending explicit Project
  Owner authorization.

## Source Context

- Parent diagnostic design:
  `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/`
- Parent evaluation readout:
  `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/`

The parent diagnostic established smoke-level evidence that some noisy-rate
contraction examples remain non-collapsed. This folder asks whether those
examples can support actual tower-only training runs with usable runtime
traces.

## Local Files

- [Design Discussion](design_discussion.md)
- [Blueprint](01_counterpoint_noisy_rate_full_tower_training_diagnostic_blueprint.md)
- [Implementation Workplan](02_counterpoint_noisy_rate_full_tower_training_diagnostic_implementation_workplan.md)
- [Implementation Log](03_counterpoint_noisy_rate_full_tower_training_diagnostic_implementation_log.md)
