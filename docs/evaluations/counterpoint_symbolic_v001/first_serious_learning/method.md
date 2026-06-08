# Method

The first serious evaluation compares direct environment arms against active-tier exploit/explore tower-control arms under shared seed, budget, mask, artifact, timing, and linearization discipline.

Default linearization condition: `tensor_available_disabled`.

Direct arms:

- `direct_masked_random`
- `direct_tabular_q`

Tower-control arms:

- `tower_empty_exploit_explore_tabular_q`
- `tower_random_balanced_exploit_explore_tabular_q`
- `tower_random_unbalanced_exploit_explore_tabular_q`
- `tower_motion_exploit_explore_tabular_q`
- `tower_bad_exploit_explore_tabular_q`

This checked-in folder is the repo-side human readout surface. The source
machine-readable tables for the current regenerated run are read from:

```text
<repo-root>/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/pi0_h_evaluation_001/evaluations/counterpoint_first_serious_learning_v001/
```

The source binding for the repo readout is recorded in `readout_source.json`.
