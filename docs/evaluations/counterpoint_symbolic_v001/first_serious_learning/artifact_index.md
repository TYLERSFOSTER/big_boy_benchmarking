# Artifact Index

This index lists the evidence used by the human readout and what each file is
for.

## Source Binding

Repo readout surface:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning
```

Raw artifact root:

```text
/private/tmp/bbb-counterpoint-serious-learning-serious-001
```

Raw evaluation root:

```text
/private/tmp/bbb-counterpoint-serious-learning-serious-001/evaluations/counterpoint_first_serious_learning_v001
```

The repo surface is the command target. The raw artifact root is evidence
metadata used by this readout.

## Evaluation-Level Files

| File | Purpose | Status |
| --- | --- | --- |
| `evaluation_budget_lock.json` | Locked arms, episode budget, replicate count, schema seeds, seed bundles, controller config, learner config, linearization mode. | present |
| `evaluation_run_index.csv` | Run ids, arm ids, schema seeds, replicate indices, run statuses, timestamps. | present |
| `evaluation_aggregate_summary.json` | Aggregate status and pointers to result tables. | present |
| `evaluation_aggregate_table.csv` | Per-arm return summaries, confidence intervals, deltas versus baselines. | present |
| `evaluation_manifest.json` | Intended evaluation-level provenance manifest. | missing |
| `evaluation_arm_manifest.json` | Intended arm contract manifest. | missing |
| `calibration_summary.json` | Calibration runtime/artifact/noise summary. | missing |
| `calibration_run_index.csv` | Calibration run index. | missing |
| `calibration_recommendation.md` | Calibration-based budget recommendation. | missing |

## Result Tables

| File | Purpose |
| --- | --- |
| `results/learning_curves.csv` | Per-episode total reward, step count, and success status. |
| `results/timing_summary.csv` | Per-run timing categories. |
| `results/controller_summary.csv` | Counts of controller actions per tower run. |
| `results/schema_diagnostic_summary.csv` | Schema ids, tier counts, and edge counts. |

## Per-Run Evidence

Direct-run family:

```text
runs/counterpoint_symbolic_v001_first_serious_learning_direct_v001/runs/<run-id>/
```

Tower-run family:

```text
runs/counterpoint_symbolic_v001_first_serious_learning_tower_v001/runs/<run-id>/
```

Important per-run files:

| File | Purpose |
| --- | --- |
| `run_manifest.json` | Run command family, budget, mode, schema, linearization, status. |
| `linearization_manifest.json` | Tensorization-disabled condition and backend report. |
| `episodes.csv` | Per-episode behavioral outcome. |
| `step_events.csv` | Step-level environment events when steps occur. |
| `control_events.csv` | Tower controller decisions and active-tier movement. |
| `lift_fiber_events.csv` | Tower lift/action-realization attempts and failures. |
| `timing_summary.json` | Run-level timing category summary. |
| `warnings.jsonl` | Run-level warnings, if any. |

## Most Important Audit Path

To verify the main finding:

1. Read `evaluation_aggregate_table.csv`.
2. Confirm non-empty tower arms have `mean_return=0.0`.
3. Read `results/learning_curves.csv`.
4. Confirm those arms have `step_count=0` and `success=False`.
5. Open representative per-run `lift_fiber_events.csv` files.
6. Confirm repeated `invalid_action_index` failures.
7. Open `results/controller_summary.csv`.
8. Confirm non-empty tower arms descend and explore but do not execute/train.
