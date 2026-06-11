# Warehouse Gridlock Full-State Policy Comparison

![artifacts_complete](badges/artifacts_complete.svg) ![learning_signal](badges/learning_signal.svg) ![scope_policy](badges/scope_policy.svg) ![no_lookahead](badges/no_lookahead.svg) ![provenance_repo_artifacts](badges/provenance_repo_artifacts.svg)

## Status At A Glance

- Evaluation id: `warehouse_gridlock_full_state_full_action_trainable_policy_v001`.
- Run label: `tower_curriculum_train_2024_001`.
- Learning contract status: `passed`.
- Score direction: `tie`.
- No-lookahead status: `passed`.

## Summary of Goals Behind this Evaluation

This evaluation corrects the previous Warehouse masked direct vs. live-lift
tower diagnostic by replacing candidate-id keyed nominal updates with a real
trainable policy contract.

The Project Owner's active model contract is:

```text
full system configuration + current second -> full simultaneous action vector
```

Both arms use `warehouse_linear_factorized_softmax_policy_v001`. This is a trainable linear/factorized model,
not neural backprop.

## Summary of Methodology Behind this Evaluation

The direct arm is `warehouse_direct_full_state_policy_masked`. It receives full concrete Warehouse state,
the current second, and emits a full concrete action vector before the shared
immediate-admissibility resolver selects a valid concrete vector.

The tower arm is `warehouse_tower_full_state_policy_live_lift_masked`. It preserves live state-lift hygiene and uses
the scoped generated/discovered tower surface, but concrete action selection is
scored through reusable feature weights rather than opaque candidate ids.

Neither arm uses one-hop successor-state cul-de-sac lookahead.

## Claim Boundary

This run may support policy-contract and learning-health claims only. It may
not claim Warehouse is solved, tower is better in general, backprop happened,
or the full serious MDP was enumerated.

## Evidence Map

- `readout_source.json`: source binding for human-readable regeneration.
- `artifacts/tower_curriculum_train_2024_001/results/learning_health_summary.csv`: whether updates
  became real reusable learning.
- `artifacts/tower_curriculum_train_2024_001/results/policy_reuse_summary.csv`: prior-signal reuse.
- `artifacts/tower_curriculum_train_2024_001/results/no_lookahead_audit_summary.csv`: no-lookahead
  audit.
- `artifacts/tower_curriculum_train_2024_001/results/arm_summary.csv`: arm-level behavior.
