# Counterpoint First Serious Learning Evaluation - Human Readout

## One-Screen Verdict

All required arms produced artifact rows and the run index marks every run as
`success`. That means the harness ran and wrote artifacts.

Behaviorally, the run splits into two groups:

- `direct_masked_random`, `direct_tabular_q`, and
  `tower_empty_exploit_explore_tabular_q` executed 8-step episodes, reached
  `100%` episode success, and received mean returns around `12.8`.
- `tower_random_balanced_exploit_explore_tabular_q`,
  `tower_random_unbalanced_exploit_explore_tabular_q`,
  `tower_motion_exploit_explore_tabular_q`, and
  `tower_bad_exploit_explore_tabular_q` completed artifact runs but produced
  `0.0` mean return, `0.0` mean step count, and `0%` episode success.

The diagnostic explanation is visible in the per-run lift-fiber artifacts:
the non-empty tower arms repeatedly failed action realization with
`invalid_action_index`. Their controller summaries show descent into the tower
followed by exploration, but no successful `exploit_execute` or `train`
actions.

This is therefore diagnostic evidence about the current non-empty tower
control/action-realization path. It does not support a positive
tower-performance claim.

## Run Identity

| Field | Value |
| --- | --- |
| Repo readout surface | `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning` |
| Source artifact root | `/private/tmp/bbb-counterpoint-serious-learning-serious-001` |
| Source evaluation root | `/private/tmp/bbb-counterpoint-serious-learning-serious-001/evaluations/counterpoint_first_serious_learning_v001` |
| Evaluation id | `counterpoint_first_serious_learning_v001` |
| Environment instance | `counterpoint_symbolic_n3_small_v001` |
| Artifact schema version | `bbb.v001` |
| Source durability | local temporary artifact path; not a durable artifact archive |
| Linearization mode | `tensor_available_disabled` |
| Linearization state | `PRESENT_DISABLED` |
| Tensor execution | disabled |
| Numeric backend in linearization report | `NUMPY` |
| CUDA available in sampled report | `false` |
| Torch available in sampled report | `false` |
| Budget lock | `evaluation_budget_lock.json` |
| Locked by | `foster` |
| Locked at | `2026-05-30T02:00:45.373189+00:00` |
| Episodes per run | `16` |
| Max steps per episode | `8` |
| Replicates | `4` |
| Random schema seeds | `3` |

## Claim Boundary

This readout may claim:

- the artifact harness completed all required arms;
- direct and empty-schema tower arms behaved successfully under this budget;
- non-empty tower arms failed behaviorally under this budget;
- the observed failure mechanism is repeated `invalid_action_index` lift/action
  realization failure.

This readout may not claim:

- tensor-enabled performance;
- CUDA or GPU performance;
- general tower superiority or inferiority;
- musical quality;
- production performance;
- a result beyond `counterpoint_symbolic_n3_small_v001`;
- a result beyond the recorded budget and seed policy.

## Arm Legend

| Arm id | Human label | Role |
| --- | --- | --- |
| `direct_masked_random` | Direct masked random | Non-learning direct environment floor. |
| `direct_tabular_q` | Direct tabular Q | Direct environment tabular Q baseline. |
| `tower_empty_exploit_explore_tabular_q` | Empty-schema tower | Active-tier tower shell with no nontrivial contraction. |
| `tower_random_balanced_exploit_explore_tabular_q` | Random balanced tower | Tower controller with seeded balanced random contraction. |
| `tower_random_unbalanced_exploit_explore_tabular_q` | Random unbalanced tower | Tower controller with seeded unbalanced random contraction. |
| `tower_motion_exploit_explore_tabular_q` | Structured motion tower | Tower controller with structured motion contraction. |
| `tower_bad_exploit_explore_tabular_q` | Bad/adversarial tower | Tower controller with intentionally bad overcompression. |

## Reader-Facing Result Table

| Arm | Artifact status | Behavior status | Episodes | Mean return | Mean steps | Success rate | Delta vs direct Q | Main warning |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Direct masked random | complete | succeeded | 64 | 12.807 | 8.0 | 100% | -0.069 | Baseline floor, not a learner claim. |
| Direct tabular Q | complete | succeeded | 64 | 12.876 | 8.0 | 100% | 0.000 | Primary direct baseline. |
| Empty-schema tower | complete | succeeded | 64 | 12.830 | 8.0 | 100% | -0.046 | Tower shell works when no nontrivial contraction is present. |
| Random balanced tower | complete | failed | 192 | 0.000 | 0.0 | 0% | -12.876 | 11,520 `invalid_action_index` lift failures. |
| Random unbalanced tower | complete | failed | 192 | 0.000 | 0.0 | 0% | -12.876 | 11,904 `invalid_action_index` lift failures. |
| Structured motion tower | complete | failed | 64 | 0.000 | 0.0 | 0% | -12.876 | 3,840 `invalid_action_index` lift failures. |
| Bad/adversarial tower | complete | failed | 64 | 0.000 | 0.0 | 0% | -12.876 | 4,032 `invalid_action_index` lift failures. |

## Diagnostic Findings

The main diagnostic finding is not subtle: non-empty tower arms did not realize
valid environment actions.

Evidence:

- `evaluation_aggregate_table.csv` records all non-empty tower arms with
  `mean_return=0.0`.
- `results/learning_curves.csv` records those same arms with `step_count=0`
  and `success=False` for every episode.
- Per-run `lift_fiber_events.csv` files record only `invalid_action_index`
  failures for the non-empty tower arms.
- `results/controller_summary.csv` shows non-empty tower arms repeatedly
  `descend` and `explore`, but never records `exploit_execute` or `train`.
- The empty-schema tower arm has 512 successful lift-fiber events and records
  `exploit_execute`, `explore`, and `train` controller actions.

This pattern means the artifact pipeline and controller loop are running, but
the non-empty tower action-realization path is not behaviorally healthy in this
run.

## Timing Readout

The timing table records `algorithm_online`, `linearization_setup`, and `total`
categories. It does not justify a performance-speed claim because several arms
failed behaviorally and because artifact/logging categories are not the focus of
this readout.

Mean total seconds by arm:

| Arm | Mean total seconds | Mean algorithm-online seconds | Mean linearization setup seconds |
| --- | ---: | ---: | ---: |
| Direct masked random | 0.072260 | 0.071745 | 0.000516 |
| Direct tabular Q | 0.011114 | 0.010854 | 0.000260 |
| Empty-schema tower | 0.253078 | 0.249751 | 0.003327 |
| Random balanced tower | 0.371513 | 0.343495 | 0.028018 |
| Random unbalanced tower | 0.377663 | 0.346880 | 0.030783 |
| Structured motion tower | 0.393001 | 0.348180 | 0.044821 |
| Bad/adversarial tower | 0.387559 | 0.342590 | 0.044969 |

## Evidence Map

Primary evidence:

- `evaluation_budget_lock.json`: locked budget, arms, seed bundles, schema seed suite, linearization mode.
- `evaluation_run_index.csv`: run ids, arm ids, run statuses, timestamps.
- `evaluation_aggregate_summary.json`: aggregate status and result file pointers.
- `evaluation_aggregate_table.csv`: per-arm mean return, confidence intervals, baseline deltas.
- `results/learning_curves.csv`: per-episode return, step count, and success.
- `results/controller_summary.csv`: per-run controller action counts.
- `results/schema_diagnostic_summary.csv`: schema ids, tier counts, and edge counts.
- `results/timing_summary.csv`: timing category rows.
- Per-run `episodes.csv`: detailed episode rows.
- Per-run `control_events.csv`: active-tier controller trace.
- Per-run `lift_fiber_events.csv`: lift/action-realization successes and failures.
- Per-run `linearization_manifest.json`: tensorization-disabled condition and backend report.

Provenance status:

| File | Classification | Interpretation |
| --- | --- | --- |
| `evaluation_manifest.json` | `expected_missing_gap` | Expected evaluation-level provenance is absent. |
| `evaluation_arm_manifest.json` | `expected_missing_gap` | Expected arm-contract provenance is absent. |
| `calibration_summary.json` | `conditional_absent` | Calibration-path file; not necessarily expected for this locked serious run. |
| `calibration_run_index.csv` | `conditional_absent` | Calibration-path file; not necessarily expected for this locked serious run. |
| `calibration_recommendation.md` | `conditional_absent` | Calibration-path file; not necessarily expected for this locked serious run. |
