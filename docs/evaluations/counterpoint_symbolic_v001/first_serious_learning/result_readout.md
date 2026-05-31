# Counterpoint First Serious Learning Evaluation - Human Readout

## One-Screen Verdict

All required arms produced artifact rows, and the run index marks all `44` runs
as `success`. That means the harness ran and wrote artifacts. Behavioral
success has to be read from the episode, controller, and lift-fiber tables.

The direct arms, empty-schema tower, structured-motion tower, and
bad/adversarial tower all executed real 8-step episodes with 100% episode
success. Their mean returns sit in the same narrow band: direct masked random
at `12.790`, direct tabular Q at `12.696`, and empty/schema-motion/bad tower
arms at `12.710`.

The random tower arms are mixed because behavior depends on schema seed. Random
balanced has 33% episode success: schema seeds `0` and `1` produce zero-step
episodes, while schema seed `2` executes normally. Random unbalanced has 67%
episode success: schema seed `1` fails, while schema seeds `0` and `2` execute
normally. The failing random-schema runs record
`no_lift_candidate_from_current_state`.

This artifact set supports a bounded diagnostic claim. It does not support a
tower-superiority claim. Structured motion does not beat the empty-schema tower,
random schemas are seed-sensitive, and the bad/adversarial control does not
degrade under this budget.

## Run Identity

| Field | Value |
| --- | --- |
| Repo readout surface | `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning` |
| Source artifact root | `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/v071_002_clean` |
| Source evaluation root | `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/v071_002_clean/evaluations/counterpoint_first_serious_learning_v001` |
| Evaluation id | `counterpoint_first_serious_learning_v001` |
| Environment instance | `counterpoint_symbolic_n3_small_v001` |
| Artifact schema version | `bbb.v001` |
| Source durability | repo-resident artifact path under the evaluation readout surface |
| Linearization mode | `tensor_available_disabled` |
| Linearization state | `PRESENT_DISABLED` |
| Tensor execution | disabled |
| Numeric backend in sampled report | `NUMPY` |
| CUDA available in sampled report | `false` |
| Torch available in sampled report | `false` |
| Budget lock | `evaluation_budget_lock.json` |
| Locked by | `foster` |
| Locked at | `2026-05-31T02:08:29.802819+00:00` |
| Episodes per run | `16` |
| Max steps per episode | `8` |
| Replicates | `4` |
| Random schema seeds | `3` |
| Run count | `44` |

## Claim Boundary

This readout may claim:

- the locked serious-learning run completed all required arms;
- all required aggregate/result tables exist and parse;
- the direct baselines, empty-schema tower, structured-motion tower, and
  bad/adversarial tower executed 8-step episodes with 100% episode success;
- the random balanced and random unbalanced tower arms are schema-seed
  dependent under this budget;
- failing random-schema runs show `no_lift_candidate_from_current_state`.

This readout may not claim:

- tensor-enabled performance;
- CUDA or GPU performance;
- general tower superiority or inferiority;
- structured-motion advantage over the empty-schema tower;
- that the bad/adversarial arm is currently a useful negative control;
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

| Arm | Artifact status | Behavior status | Runs | Episodes | Mean return | Mean steps | Success rate | Delta vs direct Q | Main warning |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Direct masked random | complete | succeeded | 4 | 64 | 12.790 | 8.0 | 100% | +0.094 | Non-learning floor is slightly above direct Q in this short budget. |
| Direct tabular Q | complete | succeeded | 4 | 64 | 12.696 | 8.0 | 100% | +0.000 | Primary direct baseline; no advantage over masked random here. |
| Empty-schema tower | complete | succeeded | 4 | 64 | 12.710 | 8.0 | 100% | +0.013 | Tower shell baseline; matches motion and bad arms. |
| Random balanced tower | complete | mixed | 12 | 192 | 4.237 | 2.7 | 33% | -8.460 | Seeds `0` and `1` fail with no lift candidate; seed `2` executes. |
| Random unbalanced tower | complete | mixed | 12 | 192 | 8.473 | 5.3 | 67% | -4.223 | Seed `1` fails with no lift candidate; seeds `0` and `2` execute. |
| Structured motion tower | complete | succeeded | 4 | 64 | 12.710 | 8.0 | 100% | +0.013 | Matches empty-schema tower; no advantage shown. |
| Bad/adversarial tower | complete | succeeded | 4 | 64 | 12.710 | 8.0 | 100% | +0.013 | Negative control did not degrade; control semantics need scrutiny. |

## Diagnostic Findings

### Finding 1: Random Schemas Are Schema-Seed Dependent

Random balanced and random unbalanced arms are mixed because schema seeds
produce different execution surfaces.

| Arm | Schema seed | Mean return | Mean steps | Episode success | Lift failure |
| --- | ---: | ---: | ---: | ---: | --- |
| Random balanced tower | 0 | 0.000 | 0.0 | 0% | `no_lift_candidate_from_current_state` |
| Random balanced tower | 1 | 0.000 | 0.0 | 0% | `no_lift_candidate_from_current_state` |
| Random balanced tower | 2 | 12.710 | 8.0 | 100% | none observed |
| Random unbalanced tower | 0 | 12.710 | 8.0 | 100% | none observed |
| Random unbalanced tower | 1 | 0.000 | 0.0 | 0% | `no_lift_candidate_from_current_state` |
| Random unbalanced tower | 2 | 12.710 | 8.0 | 100% | none observed |

This means the random-arm means are mixtures over successful and failed schema
seeds, not smooth learning curves within each schema.

### Finding 2: Structured Motion And Bad/Adversarial Match Empty Schema

The empty-schema, structured-motion, and bad/adversarial arms have identical
aggregate means in this run:

```text
12.709722222222222
```

That is good news for executability, but it is not evidence that the
structured-motion contraction improves learning. It also weakens the current
bad/adversarial arm as a negative control: under this budget, it does not
behave worse than the empty tower.

### Finding 3: Artifact Provenance Is Still Partial

The required result tables are present, but two expected provenance files are
absent:

- `evaluation_manifest.json`
- `evaluation_arm_manifest.json`

The run can be interpreted from the budget lock, run index, aggregate tables,
result tables, and per-run artifacts, but the artifact contract is still
missing these evaluation-level manifests.

## Timing Readout

The timing table records `algorithm_online`, `linearization_setup`, and `total`
categories. It is descriptive only. It should not be used as a speed claim
because this run is fixture-local, tensor execution is disabled, and some arms
are behavior-mixed.

Mean total seconds by arm:

| Arm | Mean total seconds | Mean algorithm-online seconds | Mean linearization setup seconds |
| --- | ---: | ---: | ---: |
| Direct masked random | 0.070866 | 0.070372 | 0.000494 |
| Direct tabular Q | 0.011411 | 0.011154 | 0.000256 |
| Empty-schema tower | 0.254612 | 0.251285 | 0.003327 |
| Random balanced tower | 0.402994 | 0.375936 | 0.027058 |
| Random unbalanced tower | 0.432385 | 0.398726 | 0.033659 |
| Structured motion tower | 0.458044 | 0.414122 | 0.043921 |
| Bad/adversarial tower | 0.451407 | 0.407782 | 0.043625 |

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
