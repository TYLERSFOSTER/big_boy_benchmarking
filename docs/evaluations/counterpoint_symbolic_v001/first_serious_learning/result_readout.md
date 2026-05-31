# Counterpoint First Serious Learning Evaluation - Human Readout

## One-Screen Verdict

All required arms produced artifact rows, and the run index marks all `44` runs
as `success`. That means the harness ran and wrote artifacts. Behavioral
success has to be read from the episode, controller, quotient, and lift-fiber
evidence.

The direct arms and empty-schema tower executed real 8-step episodes with 100%
episode success. Their mean returns sit in the same narrow band: direct masked
random at `12.790`, direct tabular Q at `12.696`, and empty-schema tower at
`12.710`.

The structured-motion and bad/adversarial tower arms also executed 8-step
episodes with mean return `12.710`, but they should not be read as ordinary
successful tower-control comparisons. Their first projections are fully
collapsed structural-limit cases.

The random tower arms are schema-seed dependent structural diagnostics. Random
balanced has 33% episode success: schema seeds `0` and `1` produce zero-step
episodes, while schema seed `2` executes normally. Random unbalanced has 67%
episode success: schema seed `1` fails, while schema seeds `0` and `2` execute
normally. The failing random-schema runs record
`no_lift_candidate_from_current_state`.

This artifact set supports a bounded diagnostic claim. It does not support a
tower-superiority claim, and it should not be summarized as ordinary mixed
non-performance. Broad/full-graph contraction schemas over this fixture can
collapse the first quotient projection so aggressively that learner-performance
language is blocked unless the evaluation explicitly controls for that
collapse.

## Run Identity

| Field | Value |
| --- | --- |
| Repo readout surface | `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning` |
| Source artifact root | `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/pi0_h_evaluation_001` |
| Source evaluation root | `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/pi0_h_evaluation_001/evaluations/counterpoint_first_serious_learning_v001` |
| Evaluation id | `counterpoint_first_serious_learning_v001` |
| Environment instance | `counterpoint_symbolic_n3_small_v001` |
| Artifact schema version | `bbb.v001` |
| Source durability | repo-resident artifact path under the evaluation readout surface |
| Linearization mode | `tensor_available_disabled` |
| Budget lock | `evaluation_budget_lock.json` |
| Locked by | `foster` |
| Locked at | `2026-05-31T16:50:08.227034+00:00` |
| Episodes per run | `16` |
| Max steps per episode | `8` |
| Replicates | `4` |
| Random schema seeds | `3` |
| Run count | `44` |

## Claim Boundary

This readout may claim:

- the locked serious-learning run completed all required arms;
- all required aggregate/result tables exist and parse;
- direct baselines and the empty-schema tower execute real 8-step episodes;
- random balanced and random unbalanced are schema-seed dependent under this
  budget;
- failing random-schema runs show `no_lift_candidate_from_current_state`;
- non-empty tower behavior is dominated by full or near-full first-projection
  quotient collapse and lift/action-realization effects.

This readout may not claim:

- tensor-enabled performance;
- CUDA or GPU performance;
- general tower superiority or inferiority;
- structured-motion advantage over the empty-schema tower;
- that the bad/adversarial arm is currently a useful negative control;
- ordinary learner-performance conclusions for non-empty tower arms without
  controlling for first-projection collapse;
- musical quality;
- production performance;
- a result beyond `counterpoint_symbolic_n3_small_v001`;
- a result beyond the recorded budget and seed policy.

## Reader-Facing Result Table

| Arm | Artifact status | Behavior status | Runs | Episodes | Mean return | Mean steps | Success rate | Delta vs direct Q | Main warning |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Direct masked random | complete | succeeded | 4 | 64 | 12.790 | 8.0 | 100% | +0.094 | Non-learning floor is slightly above direct Q in this short budget. |
| Direct tabular Q | complete | succeeded | 4 | 64 | 12.696 | 8.0 | 100% | +0.000 | Primary direct baseline; no advantage over masked random here. |
| Empty-schema tower | complete | succeeded | 4 | 64 | 12.710 | 8.0 | 100% | +0.013 | Tower shell baseline. |
| Random balanced tower | complete | structural_limit | 12 | 192 | 4.237 | 2.7 | 33% | -8.460 | Seeds `0` and `1` fail with no lift candidate; seed `2` executes. |
| Random unbalanced tower | complete | structural_limit | 12 | 192 | 8.473 | 5.3 | 67% | -4.223 | Seed `1` fails with no lift candidate; seeds `0` and `2` execute. |
| Structured motion tower | complete | structural_limit | 4 | 64 | 12.710 | 8.0 | 100% | +0.013 | Executes under full first-projection collapse; no advantage shown. |
| Bad/adversarial tower | complete | structural_limit | 4 | 64 | 12.710 | 8.0 | 100% | +0.013 | Executes under full first-projection collapse; not a valid negative-control result here. |

## Structural Diagnostic Findings

### Finding 1: First Projection Collapse Controls Interpretation

The central diagnostic is structural. Non-empty tower arms either fully collapse
the first quotient projection or create a giant tier-`1` fiber that contains
most tier-`0` states. That means ordinary learner-performance language is
blocked unless a later evaluation explicitly controls for quotient collapse.

This readout therefore classifies the non-empty tower result as a
structural-limit diagnostic, not as ordinary mixed non-performance.

### Finding 2: Random Schemas Are Schema-Seed Dependent Under The Structural Limit

| Arm | Schema seed | Tower shape | Mean return | Mean steps | Episode success | Lift/action result |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| Random balanced tower | 0 | `(108, 3, 1, 1, 1)` | 0.000 | 0.0 | 0% | `no_lift_candidate_from_current_state` |
| Random balanced tower | 1 | `(108, 8, 2, 1, 1)` | 0.000 | 0.0 | 0% | `no_lift_candidate_from_current_state` |
| Random balanced tower | 2 | `(108, 1, 1, 1, 1)` | 12.710 | 8.0 | 100% | Executes at base tier. |
| Random unbalanced tower | 0 | `(108, 1, 1)` | 12.710 | 8.0 | 100% | Executes at base tier. |
| Random unbalanced tower | 1 | `(108, 2, 1)` | 0.000 | 0.0 | 0% | `no_lift_candidate_from_current_state` |
| Random unbalanced tower | 2 | `(108, 1, 1)` | 12.710 | 8.0 | 100% | Executes at base tier. |

Random-arm means are mixtures over successful and failed schema seeds, not
smooth learning curves within each schema. This should be read as
lift/action-realization evidence under collapsed or near-collapsed quotient
structure, not as ordinary mixed learner performance.

### Finding 3: Structured Motion And Bad/Adversarial Execute Under Full Collapse

| Arm | Tower shape | Mean return | Delta vs empty tower |
| --- | --- | ---: | ---: |
| Empty-schema tower | `(108,)` | 12.710 | +0.000 |
| Structured motion tower | `(108, 1, 1, 1, 1)` | 12.710 | +0.000 |
| Bad/adversarial tower | `(108, 1)` | 12.710 | +0.000 |

The structured-motion and bad/adversarial arms execute 8-step episodes, but
they do so under fully collapsed first projections. Their execution therefore
does not separate useful tower control from the collapsed schema/runtime
condition.

## Artifact Gaps

The required result tables are present, but several files expected by the
current artifact/readout contract are absent:

- `evaluation_manifest.json`
- `evaluation_arm_manifest.json`
- `results/tower_shape_summary.csv`
- `results/tier_occupancy_summary.csv`
- `results/lift_failure_by_tier.csv`

The run can still be interpreted from the budget lock, run index, aggregate
tables, result tables, and per-run artifacts. The missing promoted tower tables
are an artifact-contract gap: the readout reconstructs tower shape and lift
failure detail from per-run files.

## Timing Readout

The timing table records `algorithm_online`, `linearization_setup`, and `total`
categories. It is descriptive only. It should not be used as a speed claim
because this run is fixture-local, tensor execution is disabled, and non-empty
tower arms are structural-limit diagnostics rather than ordinary performance
comparisons.

| Arm | Mean total seconds | Mean algorithm-online seconds | Mean linearization setup seconds |
| --- | ---: | ---: | ---: |
| Direct masked random | 0.078030 | 0.077439 | 0.000592 |
| Direct tabular Q | 0.012335 | 0.011891 | 0.000444 |
| Empty-schema tower | 0.267029 | 0.263408 | 0.003621 |
| Random balanced tower | 0.415845 | 0.387888 | 0.027957 |
| Random unbalanced tower | 0.458017 | 0.422194 | 0.035823 |
| Structured motion tower | 0.483324 | 0.434323 | 0.049001 |
| Bad/adversarial tower | 0.510866 | 0.458775 | 0.052091 |

## Evidence Map

Primary evidence:

- `evaluation_budget_lock.json`: locked budget, arms, seed bundles, schema seed suite, linearization mode.
- `evaluation_run_index.csv`: run ids, arm ids, run statuses, timestamps.
- `evaluation_aggregate_table.csv`: aggregate returns, confidence intervals, baseline deltas.
- `results/learning_curves.csv`: per-episode returns, steps, and success flags.
- `results/timing_summary.csv`: timing categories by run.
- `results/controller_summary.csv`: tower controller action counts.
- `results/schema_diagnostic_summary.csv`: schema ids, tower tier counts, edge counts.
- per-run `quotient_summary.json`: tower shape reconstruction.
- per-run `lift_fiber_events.csv`: lift/action-realization successes and failures.

## Classification

```text
artifact_status: partial
behavior_status: structural_limit
claim_status: diagnostic_evidence / no positive tower-performance claim
```
