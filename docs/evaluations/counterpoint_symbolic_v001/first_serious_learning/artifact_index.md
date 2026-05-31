# Artifact Index

## Repo Readout Surface

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning
```

## Source Artifact Root

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/pi0_h_evaluation_001
```

## Source Evaluation Root

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/pi0_h_evaluation_001/evaluations/counterpoint_first_serious_learning_v001
```

## Primary Source Files

| File | Purpose | Status |
| --- | --- | --- |
| `evaluation_budget_lock.json` | Locked budget, arms, seeds, linearization mode. | present |
| `evaluation_run_index.csv` | One row per run with status and artifact paths. | present |
| `evaluation_aggregate_summary.json` | Aggregate summary metadata and result paths. | present |
| `evaluation_aggregate_table.csv` | Arm-level return, interval, and delta summary. | present |
| `results/learning_curves.csv` | Per-episode reward, step count, and success rows. | present |
| `results/timing_summary.csv` | Timing rows by run and category. | present |
| `results/controller_summary.csv` | Tower controller action counts. | present |
| `results/schema_diagnostic_summary.csv` | Schema id, tier count, and edge count rows. | present |

## Expected Gaps

| File | Classification | Meaning |
| --- | --- | --- |
| `evaluation_manifest.json` | expected missing gap | Evaluation-level provenance manifest is not yet emitted. |
| `evaluation_arm_manifest.json` | expected missing gap | Arm-contract manifest is not yet emitted. |
| `results/tower_shape_summary.csv` | expected missing gap | Tower shape has to be reconstructed from per-run `quotient_summary.json`. |
| `results/tier_occupancy_summary.csv` | expected missing gap | Tier occupancy has to be reconstructed from per-run event files. |
| `results/lift_failure_by_tier.csv` | expected missing gap | Lift failures have to be reconstructed from per-run `lift_fiber_events.csv`. |

## Per-Run Evidence

Per-run directories live under:

```text
artifacts/pi0_h_evaluation_001/runs/
```

Important per-run files include:

| File | Purpose |
| --- | --- |
| `episodes.csv` | Episode-level returns and success. |
| `step_events.csv` | Concrete environment steps. |
| `control_events.csv` | Tower controller actions and active-tier movement. |
| `lift_fiber_events.csv` | Lift/action-realization candidates and failures. |
| `quotient_summary.json` | Tower state/action cell counts by tier. |
| `linearization_manifest.json` | Linearization/backend condition for the run. |
| `run_manifest.json` | Run identity and mode metadata. |

## Repo-Side Human Files

| File | Purpose |
| --- | --- |
| `README.md` | Front-page human readout. |
| `result_readout.md` | Full narrative readout. |
| `results/summary.md` | Compact result summary. |
| `results/human_summary.md` | Short explanation for a human reader. |
| `results/arm_readout_table.md` | Reader-facing arm table. |
| `results/diagnostic_findings.md` | Structural-limit and lift/action diagnostics. |
| `results/timing_readout.md` | Timing table with claim boundary. |
| `glossary.md` | Field and status definitions. |
| `runbook.md` | Rerun and regeneration instructions. |
