# Artifact Index

## Source Binding

| File | Purpose |
| --- | --- |
| `readout_source.json` | Binds this repo readout surface to the repo-resident artifact root and source evaluation root. |

## Evaluation-Level Evidence

All paths below are relative to:

```text
artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/
```

| File | Purpose |
| --- | --- |
| `evaluation_manifest.json` | Evaluation identity, claim boundary, goal criteria, structural checks, expected-file policy. |
| `evaluation_budget_lock.json` | Instances, horizons, schema seeds, replicates, episodes, base seed, linearization mode. |
| `evaluation_run_index.csv` | One row per expected run with status and artifact root. |
| `evaluation_aggregate_table.csv` | Per-run structural classifications and high-level warning fields. |
| `evaluation_aggregate_summary.json` | Complete run count, classification counts, and result-table paths. |
| `results/schema_block_summary.csv` | Source-local one-third block sizes and shares. |
| `results/tower_shape_summary.csv` | State/action cell counts by tier and full-collapse evidence. |
| `results/tier_executability_summary.csv` | Per-tier executable event counts and selected event counts. |
| `results/control_action_summary.csv` | Explore, exploit/execute, and train event counts. |
| `results/abc_selection_summary.csv` | Upstream ABC selected-tier and blocked-reason summary. |
| `results/abc_tier_signal_summary.csv` | Per-tier executable/unclosed/active/selected ABC signal summary. |
| `results/tier_occupancy_summary.csv` | Active tier/control-action occupancy and concrete-step shares. |
| `results/lift_failure_by_tier.csv` | Lift attempts, successes, failures, active tier, and candidate counts. |
| `results/concrete_step_summary.csv` | Episodes, concrete steps, rewards, terminations, and truncations. |

## Per-Run Evidence

Per-run artifacts live under:

```text
artifacts/small_medium_validation_001/runs/counterpoint_symbolic_v001_one_third_schema_tower_diagnostics_v001/runs/<run-id>/
```

Representative files:

| File | Purpose |
| --- | --- |
| `run_manifest.json` | Run identity, budget, learner/controller config, schema id, status. |
| `seed_bundle.json` | Seed bundle used for the replicate. |
| `schema_manifest.json` | Schema identity and fingerprint. |
| `schema_construction.json` | Full edge-to-block assignment for the one-third schema. |
| `quotient_summary.json` | Per-run tower shape and block summary. |
| `mode_manifest.json` | Runtime mode contract, included/excluded timing costs, controller regime. |
| `linearization_manifest.json` | `tensor_available_disabled` report and conversion-record status. |
| `control_events.csv` | Raw controller events. |
| `abc_selection_events.csv` | Raw upstream ABC selection diagnostics. |
| `abc_tier_signal_events.csv` | Raw tier signal rows used by ABC interpretation. |
| `lift_fiber_events.csv` | Raw lift/candidate/failure information. |
| `episodes.csv` | Per-episode outcomes. |
| `step_events.csv` | Per-step concrete execution events. |
| `timing_summary.json` | Per-run timing summary. |
| `timing_segments.csv` | Per-run timing segment rows. |
