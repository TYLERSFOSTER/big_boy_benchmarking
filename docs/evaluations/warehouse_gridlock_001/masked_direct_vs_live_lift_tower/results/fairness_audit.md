# Fairness Audit

The required fairness evidence lives in:

- `results/admissibility_query_summary.csv`
- `results/direct_mask_summary.csv`
- `results/tower_live_lift_summary.csv`
- `results/no_lookahead_audit_summary.csv`

Both active arms must appear in the admissibility summary. Both active arms
must report zero successor-Out uses for selection.
