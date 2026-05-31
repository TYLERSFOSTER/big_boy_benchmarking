# Counterpoint One-Third Schema Tower Diagnostics - Human Readout

## Run Identity

| Field | Value |
| --- | --- |
| Evaluation id | `counterpoint_one_third_schema_tower_diagnostics_v001` |
| Run family | `counterpoint_symbolic_v001_one_third_schema_tower_diagnostics_v001` |
| Artifact run label | `small_medium_validation_001` |
| Environment family | `counterpoint_symbolic_v001` |
| Instances | `counterpoint_symbolic_n3_small_v001`, `counterpoint_symbolic_n3_medium_v001` |
| Schema | `counterpoint_one_third_outgoing_schema_v001` |
| Mode | `tower_exploit_explore` |
| Linearization | `tensor_available_disabled` |
| Artifact schema | `bbb.v001` |
| Repo readout surface | `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics` |
| Source artifact root | `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/small_medium_validation_001` |
| Source evaluation root | `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001` |

## Verdict

The run completed as a diagnostic artifact set. The run index contains `24`
successful rows, and the aggregate summary reports `24` complete runs.

The one-third schema is structurally visible but immediately degenerate above
the base tier. The base tier is the concrete hidden graph. For the small
instance it has `108` state cells and `1140` base edges; for the medium instance
it has `228` state cells and `2732` base edges. In every run, tier `1` has one
state cell with largest state-fiber share `1.0`, and tiers `2` and `3` also have
one state cell. That is full first-projection collapse.

Runtime execution still works at the base tier. Across the full run there are
`3840` concrete steps, `3840` lift attempts, `3840` lift successes, and `0`
lift failures. All `384` episodes terminated normally and `0` truncated.

The correct interpretation is therefore not "the environment failed" and not
"the tower learned well." The correct interpretation is: this source-local
one-third schema produces a full-collapse tower geometry on these counterpoint
fixtures while preserving base-tier lift/execution.

## Reader-Facing Diagnostic Table

| Instance | Runs | Episodes | Horizon | Base states | Base edges | State cells by tier | First projection | Concrete steps | Lift failures | Mean of run mean rewards | Behavioral status |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | --- |
| Small | 12 | 192 | 8 | 108 | 1140 | `(108, 1, 1, 1)` | full collapse | 1536 | 0 | 1.588715 | base-tier executable, quotient collapsed |
| Medium | 12 | 192 | 12 | 228 | 2732 | `(228, 1, 1, 1)` | full collapse | 2304 | 0 | 1.594629 | base-tier executable, quotient collapsed |

The reward numbers are descriptive only. They are not a direct-learning
comparison and not a tower-performance claim.

## Schema Geometry

The schema construction rule is `seeded_source_local_recursive_ceil_one_third`.
For each source state, outgoing edges are deterministically assigned to three
recursive one-third blocks plus an explicit unscheduled remainder. The aggregate
counts below are the same for schema seeds `0`, `1`, and `2`; the exact edge
membership can still be seed-dependent even when the counts match.

| Instance | Block | Scheduled edges | Edge share | Sources with block | Mean local edge count |
| --- | --- | ---: | ---: | ---: | ---: |
| Small | `one_third_block_0` | 408 | 0.357895 | 108 | 3.777778 |
| Small | `one_third_block_1` | 272 | 0.238596 | 108 | 2.518519 |
| Small | `one_third_block_2` | 204 | 0.178947 | 108 | 1.888889 |
| Small | `one_third_unscheduled` | 256 | 0.224561 | 104 | 2.461538 |
| Medium | `one_third_block_0` | 980 | 0.358712 | 228 | 4.298246 |
| Medium | `one_third_block_1` | 644 | 0.235725 | 228 | 2.824561 |
| Medium | `one_third_block_2` | 444 | 0.162518 | 228 | 1.947368 |
| Medium | `one_third_unscheduled` | 664 | 0.243045 | 208 | 3.192308 |

## Tower Shape

Tier `0` is the base/fine hidden graph. Higher tier indices are coarser quotient
tiers.

| Instance | Tier | State cells | Action cells | Largest fiber share | Singleton fiber share | Degeneracy class |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Small | 0 | 108 | 1140 | 0.009259 | 1.0 | `identity_or_base` |
| Small | 1 | 1 | 15888-17147 | 1.0 | 0.0 | `full_collapse` |
| Small | 2 | 1 | 0 | 1.0 | 0.0 | `full_collapse` |
| Small | 3 | 1 | 0 | 1.0 | 0.0 | `full_collapse` |
| Medium | 0 | 228 | 2732 | 0.004386 | 1.0 | `identity_or_base` |
| Medium | 1 | 1 | 68181-74173 | 1.0 | 0.0 | `full_collapse` |
| Medium | 2 | 1 | 0 | 1.0 | 0.0 | `full_collapse` |
| Medium | 3 | 1 | 0 | 1.0 | 0.0 | `full_collapse` |

The variable tier-`1` action-cell counts are schema-seed effects. They do not
change the main interpretation because the tier-`1` state projection is fully
collapsed in every run.

## ABC And Controller Behavior

The aggregate ABC selection table contains `4800` events and `4800`
action-consistent events.

| Selection condition | Controller action | Events | Interpretation |
| --- | --- | ---: | --- |
| `at_selected` | `explore` | 2418 | ABC selected an executable base-tier context and the controller explored. |
| `at_selected` | `train` | 384 | ABC selected an executable base-tier context and the controller trained. |
| `at_selected` | `exploit_execute` | 84 | ABC selected an executable base-tier context and the controller executed. |
| `no_executable_unclosed` | `exploit_execute` | 1338 | No higher unclosed executable target existed; the runtime still executed through the base-tier path. |
| `no_executable_unclosed` | `train` | 576 | No higher unclosed executable target existed; the runtime still trained through the base-tier path. |

Control action totals:

| Instance | Explore | Exploit/execute | Train | Total events |
| --- | ---: | ---: | ---: | ---: |
| Small | 1101 | 435 | 384 | 1920 |
| Medium | 1317 | 987 | 576 | 2880 |
| Total | 2418 | 1422 | 960 | 4800 |

ABC tier signals show why ordinary tower-control language is blocked. Tier `0`
has executable-event share `1.0` on both instances. Tiers `1`, `2`, and `3`
have executable-event share `0.0` and unclosed-event share `1.0`; they are
present as collapsed quotient tiers but do not serve as executable control
tiers in this run.

## Lift And Concrete Execution

| Instance | Lift attempts | Lift successes | Lift failures | Active tier | Mean candidate count | Concrete steps | Terminated episodes | Truncated episodes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Small | 1536 | 1536 | 0 | 0 | 1.0 | 1536 | 192 | 0 |
| Medium | 2304 | 2304 | 0 | 0 | 1.0 | 2304 | 192 | 0 |
| Total | 3840 | 3840 | 0 | 0 | 1.0 | 3840 | 384 | 0 |

This separates two facts that are easy to conflate:

- quotient geometry is structurally limiting because tier `1` fully collapses
  the base graph;
- concrete execution is healthy for the base-tier path because no lift attempts
  failed.

## Timing

The per-run timing summaries contain three categories:

| Timing category | Total seconds | Mean per run | Small mean | Medium mean | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| `linearization_setup` | 2.311357 | 0.096307 | 0.038582 | 0.154031 | Setup/report path under `tensor_available_disabled`; no tensor conversion records are exported. |
| `algorithm_online` | 24.432552 | 1.018023 | 0.457611 | 1.578435 | Online controller/environment/learner path. |
| `total` | 26.743908 | 1.114330 | 0.496193 | 1.732466 | Recorded setup plus online time for each run. |

The mode manifest says online timing includes environment reset/step,
tower reset/update, controller decision, lift resolution, learner action, and
learner update. It excludes morphism construction and compatibility readouts.
Do not use these rows as a general performance comparison.

## Claim Boundary

Allowed claims:

- the one-third diagnostic artifact run completed;
- the source-local one-third schema produced the recorded block schedules;
- the first projection fully collapsed the base graph in every run;
- upstream ABC evidence was recorded and action-consistent;
- base-tier lift and concrete execution succeeded with no lift failures;
- this is diagnostic evidence about schema/runtime geometry.

Blocked claims:

- direct-vs-tower learning comparison;
- tower advantage or tower disadvantage;
- tensor-enabled, CUDA, or GPU behavior;
- musical quality;
- production performance;
- generalization beyond the recorded fixtures, seeds, and budget.

## Evidence Map

| Evidence | Path | What it supports |
| --- | --- | --- |
| Source binding | `readout_source.json` | Connects this repo readout surface to the artifact root and source evaluation root. |
| Evaluation manifest | `artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/evaluation_manifest.json` | Claim boundary, goal criteria, structural checks, expected-file policy. |
| Budget lock | `artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/evaluation_budget_lock.json` | Instances, schema seeds, replicates, episodes, horizons, linearization mode. |
| Run index | `artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/evaluation_run_index.csv` | Run count and completion status. |
| Aggregate table | `artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/evaluation_aggregate_table.csv` | Per-run structural classifications and zero/no-available/missing signals. |
| Aggregate summary | `artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/evaluation_aggregate_summary.json` | Complete run count and classification counts. |
| Schema block summary | `artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/results/schema_block_summary.csv` | One-third block sizes and shares. |
| Tower shape summary | `artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/results/tower_shape_summary.csv` | State/action cells by tier and full-collapse evidence. |
| ABC selection summary | `artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/results/abc_selection_summary.csv` | ABC selected-tier and blocked-reason interpretation. |
| ABC tier signal summary | `artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/results/abc_tier_signal_summary.csv` | Executable/unclosed/active tier evidence. |
| Control action summary | `artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/results/control_action_summary.csv` | Explore, train, and execute event counts. |
| Lift failure by tier | `artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/results/lift_failure_by_tier.csv` | Lift attempts, successes, failures, and active tier. |
| Concrete step summary | `artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/results/concrete_step_summary.csv` | Episodes, concrete steps, rewards, and termination/truncation counts. |
| Per-run manifests | `artifacts/small_medium_validation_001/runs/counterpoint_symbolic_v001_one_third_schema_tower_diagnostics_v001/runs/*/` | Timing, mode, linearization, schema construction, quotient summaries, and raw event rows. |
