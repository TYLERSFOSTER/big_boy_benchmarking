# Artifact Index

Source artifact root:

```text
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/masked_8ep_001
```

Key files:

| Path | Purpose |
| --- | --- |
| `readout_source.json` | Source binding copied into the artifact root. |
| `evaluation_budget_lock.json` | Locked budget and policy settings. |
| `evaluation_manifest.json` | Evaluation identity and claim boundary. |
| `evaluation_input_manifest.json` | Environment and readiness-source facts. |
| `dependency_manifest.json` | `state_collapser` dependency state. |
| `arm_manifest.json` | Active arm definitions. |
| `candidate_generation_manifest.json` | Generated candidate policy, budget, and active-robot cap. |
| `admissibility_policy_manifest.json` | Immediate mask policy definitions. |
| `live_lift_policy_manifest.json` | Tower live-lift rule. |
| `no_lookahead_policy_manifest.json` | No successor-state selection policy. |
| `tower_construction_manifest.json` | Scoped tower construction settings. |
| `tower_surface_scope_manifest.json` | Full-action-surface exclusion and generated-surface scope. |
| `run_index.csv` | Four run roots: direct/tower across two replicates. |
| `evaluation_aggregate_summary.json` | Machine-readable result summary. |
| `evaluation_aggregate_table.csv` | One-row aggregate status table. |
| `results/arm_summary.csv` | Arm-level means and selected-step counts. |
| `results/paired_summary.csv` | Per-pair direct-vs-tower deltas. |
| `results/target_progress_summary.csv` | Box and robot target progress. |
| `results/admissibility_query_summary.csv` | Candidate-set mask totals. |
| `results/candidate_family_summary.csv` | Candidate family and active-robot proposal counts. |
| `results/no_lookahead_audit_summary.csv` | Successor `Out` selection audit. |
| `results/tower_live_lift_summary.csv` | Tower lift liveness and failure counts. |
| `results/tower_shape_summary.csv` | Per-step scoped tower shape rows. |
| `results/tower_surface_scope_summary.csv` | Per-step generated surface size and validity counts. |
| `progress_events.jsonl` | Episode-level progress and completion events. |
