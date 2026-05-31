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

Artifacts are read from `<artifact-root>`.
