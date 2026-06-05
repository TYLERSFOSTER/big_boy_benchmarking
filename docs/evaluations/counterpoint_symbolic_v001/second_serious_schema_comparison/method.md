# Method

This evaluation compares two schema classes inside the same active-tier tower-control training harness. Schema 0 is no contraction. Schema 1 is a selected one-drop noisy-rate quotient candidate from the existing full-tower training diagnostic source.

The run uses `state_collapser_v072_pointwise` semantics from `state_collapser` v0.7.2: tower action masks and tier executability are based on concrete lifts executable from the current base state, not merely quotient-level outgoing action cells. Quotient action availability still appears in shape and diagnostic tables as structural support evidence. Pointwise executable liftability is the runtime criterion.

Invariant preflight status: `passed`. Lift failure rows reported in the aggregate readout: `0`.

Artifact root:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/v072_pointwise_r013_001
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
  "episodes_per_replicate": 8,
  "evaluation_id": "counterpoint_second_serious_schema_comparison_v001",
  "evaluation_run_family_id": "counterpoint_symbolic_v001_second_serious_schema_comparison_v001",
  "linearization_mode_id": "tensor_available_disabled",
  "locked_by": "foster",
  "required_count": 4,
  "run_mode": "smoke_schema_comparison_first_sustained_hit",
  "schema1_tower_source": "full_iterated_noisy_rate",
  "serious_run_authorized": false,
  "target_candidate_ids": [],
  "threshold_policy_id": "counterpoint_total_space_sustained_reward_v001",
  "threshold_value": 13.0,
  "tier_jump_policy_id": "counterpoint_active_tier_observed_transition_v001",
  "tier_jump_reward_cutoff": 13.0,
  "training_replicates_per_arm": 1,
  "window_length": 5
}
```
