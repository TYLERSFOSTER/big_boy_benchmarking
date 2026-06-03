# Artifact Index

This index maps the human-readable claim to the raw evidence files for
`artifacts/r000_001`.

- Evaluation manifest: `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001/evaluations/counterpoint_second_serious_schema_comparison_v001/evaluation_manifest.json`
- Arm manifest: `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001/evaluations/counterpoint_second_serious_schema_comparison_v001/evaluation_arm_manifest.json`
- Budget lock: `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001/evaluations/counterpoint_second_serious_schema_comparison_v001/evaluation_budget_lock.json`
- Threshold policy: `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001/evaluations/counterpoint_second_serious_schema_comparison_v001/threshold_policy_manifest.json`
- Candidate manifest: `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001/evaluations/counterpoint_second_serious_schema_comparison_v001/candidate_manifest.json`
- Parent source manifest: `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001/evaluations/counterpoint_second_serious_schema_comparison_v001/parent_source_manifest.json`
- Run index: `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001/evaluations/counterpoint_second_serious_schema_comparison_v001/evaluation_run_index.csv`
- Aggregate table: `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001/evaluations/counterpoint_second_serious_schema_comparison_v001/evaluation_aggregate_table.csv`
- Aggregate summary: `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001/evaluations/counterpoint_second_serious_schema_comparison_v001/evaluation_aggregate_summary.json`
- Results directory: `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001/evaluations/counterpoint_second_serious_schema_comparison_v001/results`

## Files To Inspect First

- `results/first_sustained_hit_summary.csv`: shows both arms as
  `transient_hit_only`.
- `results/paired_schema_comparison.csv`: shows the pair as
  `blocked_or_non_sustained`.
- `results/threshold_window_summary.csv`: shows why persistence failed at
  threshold `13.0`.
- `results/tower_shape_summary.csv`: shows the Schema 1 quotient is not a
  one-cell collapse.
- `results/tier_occupancy_summary.csv`: shows the Schema 1 run used both tier
  0 and tier 1.
- `results/lift_success_by_tier.csv`: shows successful lift/action-realization
  records and no recorded failure reason.
