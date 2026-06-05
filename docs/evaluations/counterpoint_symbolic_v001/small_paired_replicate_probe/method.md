# Method

This evaluation reuses the corrected second-serious per-arm tower-control runtime while giving the run a paired-replicate-specific evaluation identity and result surface.

The run uses `state_collapser_v072_pointwise` semantics. Schema 0 and Schema 1 are paired by seed bundle for each training replicate.

Threshold policy:

```json
{
  "applies_to_schema_classes": [
    "schema0_no_contraction",
    "schema1_noisy_rate_one_drop"
  ],
  "comparison": "greater_than_or_equal",
  "metric_id": "episode_total_reward",
  "required_count": 4,
  "scope": "total_space",
  "threshold_policy_id": "counterpoint_total_space_sustained_reward_v001",
  "threshold_source_field": "recommended_replicate_probe_threshold",
  "threshold_source_readout": "/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/readout_source.json",
  "threshold_source_type": "threshold_frontier_readout",
  "threshold_value": 13.0,
  "window_length": 5
}
```

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
  "episodes_per_replicate": 16,
  "evaluation_id": "counterpoint_small_paired_replicate_probe_v001",
  "evaluation_run_family_id": "counterpoint_symbolic_v001_small_paired_replicate_probe_v001",
  "linearization_mode_id": "tensor_available_disabled",
  "locked_by": "foster",
  "required_count": 4,
  "run_mode": "threshold_frontier_selected_small_paired_replicate_probe",
  "schema1_tower_source": "full_iterated_noisy_rate",
  "target_candidate_ids": [],
  "threshold_frontier_readout_source": "docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/readout_source.json",
  "threshold_policy_id": "counterpoint_total_space_sustained_reward_v001",
  "threshold_value": null,
  "tier_jump_policy_id": "counterpoint_active_tier_observed_transition_v001",
  "tier_jump_reward_cutoff": null,
  "training_replicates_per_arm": 1,
  "window_length": 5
}
```

Artifact root:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts/episodes16_from_frontier_001
```
