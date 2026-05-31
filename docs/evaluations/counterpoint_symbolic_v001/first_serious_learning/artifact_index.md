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
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/v071_002_clean
```

Raw evaluation root:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/v071_002_clean/evaluations/counterpoint_first_serious_learning_v001
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
| `evaluation_manifest.json` | Intended evaluation-level provenance manifest. | `expected_missing_gap` |
| `evaluation_arm_manifest.json` | Intended arm contract manifest. | `expected_missing_gap` |
| `calibration_summary.json` | Calibration runtime/artifact/noise summary. | `conditional_absent` |
| `calibration_run_index.csv` | Calibration run index. | `conditional_absent` |
| `calibration_recommendation.md` | Calibration-based budget recommendation. | `conditional_absent` |

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
2. Confirm direct, empty-schema, structured-motion, and bad/adversarial arms
   have mean returns around `12.7`.
3. Read `results/learning_curves.csv`.
4. Confirm random balanced has `33%` episode success and random unbalanced has
   `67%` episode success because only some schema seeds execute.
5. Open representative per-run `lift_fiber_events.csv` files for random
   balanced schema seeds `0`, `1`, and `2`, and random unbalanced schema seed
   `1`.
6. Confirm repeated `no_lift_candidate_from_current_state` failures on the
   failing random schema seeds.
7. Open `results/controller_summary.csv`.
8. Confirm successful tower arms record `exploit_execute`, `explore`, and
   `train`, while failing random-schema runs spend their control budget around
   non-executable lift choices.
