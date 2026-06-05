# Method

This evaluation composes second-serious schema-comparison subruns, one per threshold. Each subrun writes its own raw artifacts under `threshold_runs/<threshold-label>/`; the top-level threshold-frontier evaluation writes the human-facing frontier tables.

The run uses `state_collapser_v072_pointwise` semantics and `tensor_available_disabled` linearization.

Locked budget:

```json
{
  "artifact_schema_version": "bbb.v001",
  "base_seed": 0,
  "candidate_cap": 1,
  "candidate_readout_source": "docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json",
  "controller_event_ceiling_override": null,
  "controller_event_ceiling_policy": "max(64, 8 * horizon)",
  "environment_instance_id": "counterpoint_symbolic_n3_wide_20_108_span18_v001",
  "episodes_per_replicate": 4,
  "evaluation_id": "counterpoint_threshold_frontier_probe_v001",
  "evaluation_run_family_id": "counterpoint_symbolic_v001_threshold_frontier_probe_v001",
  "linearization_mode_id": "tensor_available_disabled",
  "locked_by": "foster",
  "required_count": 4,
  "run_mode": "threshold_frontier_probe_v001",
  "schema1_tower_source": "full_iterated_noisy_rate",
  "target_candidate_ids": [],
  "threshold_policy_id": "counterpoint_total_space_sustained_reward_v001",
  "threshold_values": [
    12.0,
    13.0
  ],
  "training_replicates_per_arm": 1,
  "window_length": 5
}
```

Artifact root:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts/smoke_001
```
