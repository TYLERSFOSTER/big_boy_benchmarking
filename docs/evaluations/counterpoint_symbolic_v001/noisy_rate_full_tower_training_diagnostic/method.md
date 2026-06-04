# Method

This diagnostic selects candidates from the parent noisy-rate contraction diagnostic readout. It excludes `no_contraction_control` by default, rebuilds each selected candidate tower, verifies the tier state-cell sequence, and runs tower-only active-tier training.

A real training replicate preserves learner state across all episodes inside that replicate while resetting the environment/runtime episode state between episodes.

Artifact root:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts/cap7_001
```

Locked budget:

```json
{
  "artifact_schema_version": "bbb.v001",
  "base_seed": 0,
  "candidate_cap": 7,
  "controller_event_ceiling_override": null,
  "controller_event_ceiling_policy": "max(64, 8 * horizon)",
  "episodes_per_replicate": 4,
  "evaluation_id": "counterpoint_noisy_rate_full_tower_training_diagnostic_v001",
  "evaluation_run_family_id": "counterpoint_symbolic_v001_noisy_rate_full_tower_training_diagnostic_v001",
  "horizon_by_instance_id": null,
  "include_runtime_anchor": false,
  "linearization_mode_id": "tensor_available_disabled",
  "locked_by": "codex",
  "parent_candidate_readout_source": "/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json",
  "training_replicates_per_candidate": 1
}
```
