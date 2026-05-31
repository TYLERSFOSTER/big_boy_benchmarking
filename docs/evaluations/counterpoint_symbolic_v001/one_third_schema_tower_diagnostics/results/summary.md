# Results Summary

The one-third schema diagnostic completed the locked small/medium artifact run.
All `24` run rows are `success`, all required evaluation-level result tables
exist, and the aggregate summary classifies all `24` runs as
`full_first_projection_collapse`.

Key numbers:

- completed runs: `24` / `24`;
- instances: `counterpoint_symbolic_n3_small_v001`,
  `counterpoint_symbolic_n3_medium_v001`;
- schema seeds: `0,1,2`;
- replicates per schema seed: `4`;
- episodes: `384` total;
- concrete steps: `3840`;
- lift attempts/successes/failures: `3840` / `3840` / `0`;
- ABC events/action-consistent events: `4800` / `4800`;
- no-available-action events: `0`;
- zero-concrete-step runs: `0`;
- timing total: `26.743908` seconds across all run timing summaries.

Main interpretation:

The one-third schema produces a full first-projection collapse on both
counterpoint fixtures. That blocks ordinary tower-performance interpretation.
At the same time, base-tier lift and concrete execution are healthy: all lift
attempts succeeded, and all episodes emitted concrete steps.

Primary evidence:

```text
artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/evaluation_aggregate_table.csv
artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/results/tower_shape_summary.csv
artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/results/abc_selection_summary.csv
artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/results/lift_failure_by_tier.csv
artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/results/concrete_step_summary.csv
```
