# Counterpoint First Serious Learning Evaluation Blueprint

Date: 2026-05-29

Status: draft blueprint

Repository:

```text
<repo-root>
```

Design folder:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/
```

## Status And Authority

This is a design blueprint.

This is not an implementation workplan.

This is not approval to edit source code.

This blueprint exists to convert the discussion in:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
```

into a coherent benchmark design for the first serious counterpoint learning
evaluation.

A later Phase.Stage.Action implementation workplan must translate this
blueprint into executable work before code changes begin.

## Source Authority

This blueprint follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/git_practices.md`
- `docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md`
- `docs/design/first_counterpoint_environment/01_002_counterpoint_hidden_graph_and_contraction_schema_benchmark_blueprint.md`
- `docs/design/first_counterpoint_environment/01_004_counterpoint_hidden_graph_and_contraction_schema_implementation_log.md`
- `docs/design/first_infrastructure_slice/01_001_initial_benchmarking_goals_discussion.md`
- `docs/design/first_infrastructure_slice/01_002_state_collapser_read_only_reconnaissance.md`
- `docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md`
- `docs/design/shared_benchmark_machinery/01_003_shared_benchmark_machinery_implementation_log.md`
- `docs/design/shared_benchmark_machinery/01_004_state_collapser_tensorization_resume_note.md`
- `docs/design/shared_benchmark_machinery/01_006_state_collapser_v0_7_tensorization_integration_implementation_log.md`
- `docs/methods/artifact_contract.md`
- `docs/methods/benchmark_modes.md`
- `docs/methods/seed_bundles.md`
- `docs/methods/timing_and_readout_discipline.md`
- `docs/environments/counterpoint_symbolic_v001.md`
- `<state-collapser-repo>/docs/usage/01_002_tower_runtime_mental_model.md`
- `<state-collapser-repo>/docs/usage/01_003_training_surface_quickstart.md`
- `<state-collapser-repo>/docs/usage/01_004_fiber_conditioned_training.md`
- `<state-collapser-repo>/docs/usage/01_005_using_your_own_training_loop.md`
- `<state-collapser-repo>/docs/usage/01_010_tensorization_boundary.md`
- read-only inspection of current `state_collapser` tower control and training
  surfaces

## Prime Directive Alignment

The Project Owner has already corrected the direction of this block:

- do one learning test;
- do not drift back into another structural-only evaluation;
- use `small` as the serious fixture;
- keep `tiny` as smoke only;
- treat tower evaluation as active-tier tower-control learning, not tower
  construction or loose tower metadata;
- keep direct training, empty-schema tower training, and nonempty-schema tower
  training separate;
- include all named baselines;
- choose budget through calibration, not arbitrary PO questioning;
- put human-facing result documentation under a clear parent folder in `docs`.

This blueprint encodes those decisions.

It does not reopen them as questions.

## Executive Design

The first serious counterpoint benchmark is:

```text
a controlled learning evaluation on counterpoint_symbolic_n3_small_v001
```

The main benchmark object is learning/control behavior.

Structural diagnostics are still required, but they are support evidence. They
explain why an arm behaved the way it did. They are not the organizing claim of
this evaluation.

The first serious benchmark asks:

```text
Does active-tier tower-control learning with counterpoint contraction schemata
improve learning behavior on counterpoint_symbolic_n3_small_v001 relative to
direct tabular-Q, random schema controls, and bad or degenerate schema controls,
under the same seed, budget, artifact, and linearization-mode discipline?
```

The initial claim boundary is narrow:

- one environment family;
- one serious fixture;
- one first learner family;
- one active tower-control regime;
- one tensor-capable-disabled default condition;
- no CUDA claim;
- no tensor-enabled claim;
- no musical-quality claim;
- no general `state_collapser` superiority claim.

## Settled Decisions

### Decision 1: First Serious Layer

The first serious counterpoint evaluation is a learning/control evaluation.

It is not structural-only.

Structural and schema diagnostics still run as support artifacts for every
schema/tower arm.

### Decision 2: Fixture

The serious fixture is:

```text
counterpoint_symbolic_n3_small_v001
```

The `tiny` fixture remains for:

- CI;
- smoke;
- manual command sanity checks;
- fast artifact-contract tests.

Any `tiny` result in this block is non-evidence for the first serious benchmark.

### Decision 3: First Learner Family

The first learner is the current upstream tabular Q learner surface:

```text
state_collapser.training.TabularQLearner
```

The benchmark should not build a neural learner, Stable-Baselines3 integration,
or custom heavyweight learner in this first slice.

The benchmark should leave a clean learner id boundary so later learner families
can be added without rewriting the evaluation contract.

### Decision 4: Linearization Condition

BBB now integrates `state_collapser v0.7.0`.

The first serious evaluation should default to:

```text
linearization_mode_id: tensor_available_disabled
```

This is the correct control condition after the Project Owner's tensorization
correction:

```text
tensor-capable package, tensor path present but disabled
```

The run may include explicit `none_control_flow` smoke checks if useful, but the
serious evaluation matrix should not mix `none_control_flow` into the evidence
set unless a later design explicitly creates a pre-linearization comparison.

Reserved modes remain reserved:

```text
tensor_enabled_cpu
tensor_enabled_cuda
```

No tensor-enabled, CUDA, or GPU performance claim belongs in this benchmark.

### Decision 5: Tower Evaluation Semantics

For this evaluation, `tower evaluation` means:

```text
active-tier exploit/explore tower-control learning bound to the counterpoint
environment
```

It does not mean:

- tower construction only;
- posthoc diagnostics only;
- direct tabular-Q with tower metadata attached;
- compatibility-readout-driven learning;
- unnamed tower-conditioned learning;
- ordinary tower-position-key Q-learning presented as the serious tower result.

The active tower-control regime should be grounded in current upstream surfaces:

- `ActiveTierState`;
- `ActiveTierController`;
- `ControlAction`;
- `ExploitExploreTowerRuntime`;
- `TierLearner`;
- `LiftResolveExecutor`;
- `FrozenLowerContext`;
- `TierSignalState`;
- `TierControlMetrics`;
- `FiberConditionedStage`;
- `FrozenQuotientBehavior`;
- `PathFiber`.

The controller action vocabulary is:

```text
EXPLORE
TRAIN
DESCEND
LIFT
EXPLOIT_EXECUTE
```

The first implementation must bind this regime to counterpoint in BBB. It must
not edit `<state-collapser-repo>` unless the Project Owner explicitly
authorizes upstream work.

### Decision 6: Direct, Empty-Schema Tower, And Nonempty-Schema Tower Stay Separate

The benchmark must keep these separate:

1. direct environment training;
2. tower-control training with empty/no-contraction schema;
3. tower-control training with nonempty contraction schemata.

The empty-schema tower arm is not direct training.

It is the tower-shell/no-contraction control. It measures the cost and behavior
of the tower runtime, active-tier control, masks, metadata, and learning
handoff when no nontrivial contraction is supplied.

The nonempty-schema tower arms are the actual contraction/tower comparison.

### Decision 7: Result Docs Home

Human-facing evaluation documents should live under:

```text
docs/evaluations/
```

The first counterpoint evaluation block should use:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/
```

Design and implementation planning remain under:

```text
docs/design/
```

## Non-Goals

This blueprint does not authorize:

- editing `<state-collapser-repo>`;
- building a new environment family;
- changing the counterpoint hidden graph contract;
- treating `tiny` as serious evidence;
- claiming musical quality;
- claiming CUDA or GPU performance;
- claiming tensor-enabled performance;
- replacing the first learner with a neural learner;
- treating structural diagnostics as the main result;
- making compatibility readouts part of the default hot path;
- using reward outcomes or future episode information to build online-eligible
  schemata;
- collapsing direct env, empty-schema tower, and nonempty-schema tower into one
  vague "tower" condition.

## Environment Scope

Environment family:

```text
counterpoint_symbolic_v001
```

Serious instance:

```text
counterpoint_symbolic_n3_small_v001
```

Smoke instance:

```text
counterpoint_symbolic_n3_tiny_v001
```

The environment is a benchmark-owned finite symbolic hidden graph. The object
is not to generate beautiful music. The object is to create a controlled RL
graph where direct methods and tower/control methods can be compared under a
fixed legality, reward, action-mask, and artifact contract.

The environment contracts in force are:

```text
legality_contract_id: counterpoint_legality_local_v001
reward_bundle_id: counterpoint_reward_local_v001
edge_label_contract_id: counterpoint_edge_labels_local_v001
initial_state_policy_id: counterpoint_initial_states_v001
terminal_policy_id: counterpoint_terminal_horizon_v001
action_mask_policy_id: counterpoint_legal_action_mask_v001
```

The reward remains local/action-local for this first serious learning
evaluation.

If later work needs path history, the state or reward contract must be
versioned. This blueprint does not allow hidden path-history reward state.

## Benchmark Arms

The first serious learning matrix consists of direct arms and tower-control
arms.

### Arm Table

| Arm id | Coupling | Schema | Controller regime | Training surface | Learner | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `direct_masked_random` | direct env | none | none | environment | masked random | non-learning floor |
| `direct_tabular_q` | direct env | none | none | environment | tabular Q | no-abstraction learning baseline |
| `tower_empty_exploit_explore_tabular_q` | tower runtime | empty/no-contraction | exploit/explore | tower control | tabular Q | tower-shell/control baseline |
| `tower_random_balanced_exploit_explore_tabular_q` | tower runtime | random balanced | exploit/explore | tower control | tabular Q | compression control |
| `tower_random_unbalanced_exploit_explore_tabular_q` | tower runtime | random unbalanced | exploit/explore | tower control | tabular Q | balance/pathology control |
| `tower_motion_exploit_explore_tabular_q` | tower runtime | structured motion | exploit/explore | tower control | tabular Q | intended structured positive arm |
| `tower_bad_exploit_explore_tabular_q` | tower runtime | bad/adversarial | exploit/explore | tower control | tabular Q | negative/pathology control |

### Schema Ids

The first serious learning evaluation should use the existing schema families:

```text
counterpoint_empty_schema_v001
counterpoint_random_balanced_schema_v001
counterpoint_random_unbalanced_schema_v001
counterpoint_motion_schema_v001
counterpoint_bad_schema_v001
```

Projection-audit schema remains diagnostic-only for this evaluation unless a
later design explicitly promotes it:

```text
counterpoint_projection_audit_schema_v001
```

### Random Schema Suites

Random balanced and random unbalanced arms must not be represented by one lucky
draw.

The implementation workplan should define a deterministic schema-seed suite for
each random family.

The calibration pass may determine how large the random schema suite can be
without making the first serious run unwieldy. A serious run with a single
random schema seed should be treated as incomplete evidence.

### Arm Equality Rule

All tower-control arms must share:

- controller regime;
- controller configuration family;
- learner family;
- learner hyperparameter family;
- episode budget;
- seed-bundle protocol;
- linearization mode;
- online timing discipline;
- artifact requirements.

The schema is the experimental knob.

If other knobs vary, the run must record them and the result must not be read as
a schema comparison.

## Tower-Control Binding Design

The implementation must build a BBB counterpoint binding around the upstream
active-tier control surfaces.

### Required Binding Objects

The implementation should introduce BBB-owned adapter surfaces that bind:

- counterpoint runtime reset/step;
- current state and legal action mask;
- partition tower view;
- active tier state;
- tier configs;
- frozen lower context;
- tier learner;
- lift/resolve executor;
- controller decision events;
- learner update events;
- run/event artifacts.

The adapter names are implementation details. The blueprint-level contract is
that tower arms must be visibly active-tier controller arms, not ordinary tower
metadata arms.

### Active Tier State

Tier direction follows upstream:

```text
tier 0      finest / total discovered graph
tier 1      coarser quotient
tier 2      still coarser quotient
...
```

The active-tier state must record:

- current active tier;
- tier-local state;
- event index;
- deepest known tier;
- context version if applicable.

The implementation must record active tier traces in artifacts.

### Controller

The first controller is:

```text
state_collapser.tower.control.ActiveTierController
```

The first runtime control shape is:

```text
state_collapser.tower.runtime.ExploitExploreTowerRuntime
```

The controller must be the same across empty, random, structured, and bad
schema tower arms.

### Tier Learner

The tower-control learner binding must satisfy the upstream `TierLearner`
surface:

```text
behavior_action(state, mode)
observe(transition, frozen_context=...)
should_train(event_index)
train(frozen_context=...)
```

The first learner should be tabular and inspectable. It should wrap or reuse the
upstream `TabularQLearner` where possible instead of inventing a hidden learner
framework.

### Lift/Resolve Executor

The executor must satisfy the upstream `LiftResolveExecutor` surface:

```text
execute(active_tier_state, action, frozen_context=..., mode=...)
```

It must realize active-tier choices as concrete primitive actions in the
counterpoint environment.

The preferred first executor should use partition tower and path-fiber
machinery where it is available:

```text
PartitionTower
FrozenQuotientBehavior
PathFiber
FiberConditionedStage
```

If implementation research shows this cannot be bound to counterpoint without
upstream changes, the implementation workplan must stop and record that
condition. It must not silently substitute ordinary tower-position-key
tabular-Q as the serious tower result.

### Fiber-Conditioned Stage Role

`FiberConditionedStage` is stage-local.

It is not the whole active-tier controller.

Its role in this benchmark is to support the executor when a coarse active-tier
choice must be lifted into admissible fine actions over a frozen quotient
behavior.

The benchmark should record fiber departures and lift failures as first-class
events.

### Compatibility Readout Rule

Default learning runs must not call rich compatibility readouts in the hot path.

If any arm needs a compatibility readout online, the arm must:

- declare `uses_compatibility_readout`;
- time it separately;
- explain why it is algorithmically required;
- not compare its online timing as if it were readout-free.

Posthoc diagnostics may use readouts, but their cost belongs under posthoc or
diagnostic timing, not learner/controller online timing.

## Calibration And Serious Run Protocol

Budget is not a PO questionnaire in this block.

Budget is an engineering calibration output.

The evaluation flow has three protocol phases.

### Protocol Phase A: Calibration

Calibration runs the full arm list on `counterpoint_symbolic_n3_small_v001` at
small provisional budgets.

Calibration measures:

- wall-clock runtime by timing segment;
- artifact volume;
- episode curve noisiness;
- completion/success rarity;
- tower depth and control-action event volume;
- lift/resolve failure frequency;
- fiber departure frequency;
- random-schema variability;
- whether any arm is too broken to include as serious evidence.

Calibration output must include:

```text
calibration_summary.json
calibration_run_index.csv
calibration_recommendation.md
```

The calibration recommendation proposes the locked serious budget.

### Protocol Phase B: Budget Lock

The serious budget is frozen into an artifact before the serious run.

Budget lock fields should include:

```text
environment_instance_id
arm_ids
episode_count
max_steps_per_episode
replicate_count
random_schema_seed_count
schema_seed_suite
seed_bundle_ids
controller_config_id
learner_config_id
linearization_mode_id
artifact_schema_version
calibration_artifact_root
locked_by
locked_at
```

All serious arms must use the same locked budget.

If calibration proves the proposed evaluation is too expensive, the workplan
must stop and report the measured cause. It should not quietly shrink the run
until it becomes another smoke test.

### Protocol Phase C: Serious Run

The serious run executes the locked matrix and writes:

- one run bundle per arm per seed bundle;
- aggregate tables;
- learning curves;
- timing summaries;
- controller summaries;
- schema diagnostic sidecars;
- result documentation under `docs/evaluations/...`.

The serious result is not valid unless every arm in the locked matrix either:

- completes successfully; or
- fails under a recorded, benchmark-meaningful failure mode that is included in
  the result summary.

## Metrics

Metrics are divided by purpose and cost.

### Learning Metrics

Every learning arm should report:

- episode return;
- cumulative return;
- mean return over replicate windows;
- completion/success rate;
- terminated count;
- truncated count;
- episode length;
- legal action failure count, if applicable;
- invalid action attempt count, if applicable;
- sample efficiency to configured return/completion thresholds, if thresholds
  become meaningful after calibration;
- area under learning curve, if supported by the aggregator.

### Direct Baseline Metrics

Direct arms should report:

- environment reset time;
- environment step time;
- action mask construction time;
- learner action time;
- learner update time;
- direct event logging time.

Direct arms must not include tower reset/update or controller costs.

### Tower-Control Metrics

Tower-control arms should report:

- active tier trace;
- active-tier dwell counts;
- control action counts;
- controller decision timing;
- `EXPLORE` count;
- `TRAIN` count;
- `DESCEND` count;
- `LIFT` count;
- `EXPLOIT_EXECUTE` count;
- lift/resolve timing;
- lift success count;
- lift failure count;
- lift failure reason counts;
- fiber departure count;
- fiber departure reason counts;
- tower reset timing;
- tower update timing;
- schema assignment counts;
- deepest known tier over time;
- current tower depth over time;
- learner action timing;
- learner update timing.

### Schema Diagnostic Sidecar Metrics

These support interpretation of learning results:

- quotient state count per tier;
- quotient action count per tier;
- compression ratio per tier;
- cell size distribution;
- lift-fiber size distribution;
- lift-fiber entropy;
- reward variance inside quotient fibers;
- reward term variance;
- reward-incompatible cell count;
- balanced addressability metrics;
- path/address coverage;
- sampled address traces.

These diagnostics must be timed separately from online learner/controller
segments unless they are genuinely used online by the algorithm.

### Linearization Metrics

Every serious run must write:

```text
linearization_manifest.json
```

Every serious run must record:

- linearization mode id;
- upstream linearization config;
- upstream linearization report;
- whether conversion records were exported;
- `linearization_report_build` timing;
- `encoding_registry_build` timing where a tower is supplied.

Tensor-enabled timing segments remain reserved unless a later design explicitly
activates tensor-consuming runners.

### Artifact Completeness Metrics

Every run should be checkable for:

- run manifest;
- mode manifest;
- dependency manifest;
- seed bundle;
- linearization manifest;
- timing rows;
- episode rows where applicable;
- controller rows for tower-control arms;
- metric summary;
- artifact index.

## Event Rows And Tables

The implementation should prefer append-only event rows for runtime traces.

### Required Episode Rows

Episode rows should include:

```text
run_id
arm_id
replicate_index
seed_bundle_id
episode_index
episode_return
episode_length
terminated
truncated
success
completion_flag
final_state_id
linearization_mode_id
```

### Required Step Rows

Step rows should include:

```text
run_id
arm_id
episode_index
step_index
state_id
action_id
reward
terminated
truncated
mask_density
learner_action_time_seconds
learner_update_time_seconds
environment_step_time_seconds
```

Step rows may be sampled if full step logging becomes too heavy, but sampling
must be declared in the diagnostic profile.

### Required Controller Rows

Tower-control arms should include:

```text
run_id
arm_id
episode_index
event_index
active_tier
deepest_known_tier
control_action
pressure
training_due
controller_decision_time_seconds
lift_resolve_time_seconds
success
td_error
reward_residual
```

### Required Lift/Fiber Rows

When lift/fiber machinery is used, rows should include:

```text
run_id
arm_id
episode_index
event_index
fine_tier
coarse_tier
frozen_behavior_id
source_cell
action_cell
target_cell
candidate_count
selected_candidate
lift_success
failure_reason
fiber_departure_reason
```

## Statistics And Aggregation

The first serious result should report uncertainty.

Minimum statistical outputs:

- per-arm mean;
- per-arm standard deviation;
- confidence interval over seed-bundle replicates;
- bootstrap interval where sample size supports it;
- pairwise deltas against direct tabular-Q;
- pairwise deltas against empty-schema tower-control;
- random schema family summaries across schema seeds and run seed bundles.

The result should not over-read small sample sizes.

If calibration shows high variance, the serious run should either increase
replicates or mark the result as exploratory.

## Artifacts

The artifact root is supplied by the runner or CLI.

The current working directory must not change artifact meaning.

### Per-Run Artifacts

Every run should write the shared machinery files already established by BBB,
including:

- run manifest;
- mode manifest;
- dependency manifest;
- seed bundle;
- timing rows;
- metric rows;
- event rows;
- summary;
- linearization manifest.

### Evaluation-Level Artifacts

The serious evaluation should add an evaluation-level index:

```text
evaluation_manifest.json
evaluation_arm_manifest.json
evaluation_run_index.csv
evaluation_budget_lock.json
evaluation_aggregate_summary.json
evaluation_aggregate_table.csv
```

Calibration should write:

```text
calibration_summary.json
calibration_run_index.csv
calibration_recommendation.md
```

### Human-Facing Docs

The result-facing docs should live at:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/
```

Recommended files:

```text
README.md
method.md
runbook.md
artifact_index.md
results/summary.md
results/learning_curves.csv
results/timing_summary.csv
results/controller_summary.csv
results/schema_diagnostic_summary.csv
```

`README.md` should be the quick human entry point.

`method.md` should describe the protocol and claim boundary.

`runbook.md` should record exact commands and artifact roots.

`artifact_index.md` should map human-readable result claims to machine-readable
artifacts.

## CLI Surface

The implementation should add one explicit first serious evaluation CLI surface
rather than asking users to manually compose many smoke commands.

Recommended command family:

```text
python -m big_boy_benchmarking.cli counterpoint serious-learning calibrate
python -m big_boy_benchmarking.cli counterpoint serious-learning run
python -m big_boy_benchmarking.cli counterpoint serious-learning summarize
```

The future reserved console command remains:

```text
bbb
```

The exact command names can be refined in the implementation workplan, but the
user-facing workflow should keep calibration, serious run, and summarization
distinct.

### Required CLI Inputs

Commands should accept:

```text
--artifact-root
--instance-id small
--linearization-mode tensor_available_disabled
--budget-lock <path>
--seed-bundle-suite <id-or-path>
--schema-seed-suite <id-or-path>
--controller-config <id-or-path>
--learner-config <id-or-path>
```

Calibration may accept provisional budget inputs.

Serious run should require or create a budget-lock artifact so evidence is not
silently produced under ad hoc settings.

## Benchmark Mode Registry Implications

The current mode registry already reserves:

```text
tower_exploit_explore
tower_fiber_conditioned_stage
tower_control_with_fiber_conditioned_substages
```

This blueprint requires making the active tower-control learning path real for
counterpoint.

The implementation workplan should decide whether to:

1. make `tower_exploit_explore` runnable for counterpoint;
2. add counterpoint-specific arm ids while preserving the global mode id;
3. introduce a new mode id for exploit/explore with fiber-conditioned lift
   resolution if the existing reserved id is too broad.

That is implementation discovery, not a new PO-level design question.

The registry must continue to distinguish execution mode from linearization
mode.

## Timing Discipline

Timing must separate algorithm cost from benchmark bookkeeping.

Required timing segments include:

- environment reset;
- environment step;
- action mask construction;
- tower reset;
- tower update;
- controller decision;
- lift/resolve;
- learner action;
- learner update;
- linearization report build;
- encoding registry build;
- artifact logging;
- compatibility readout if requested;
- morphism construction if requested;
- posthoc diagnostics;
- summary generation.

The hot-path rule is:

```text
Default serious learning runs must not materialize compatibility quotient
readouts or morphisms unless the mode explicitly declares that the algorithm
requires them online.
```

If readouts or morphisms are used for diagnostics, their costs are diagnostic
costs.

## Seed Discipline

The seed bundle is the unit of reproducible stochastic identity.

The replicate is the unit of uncertainty.

Seed bundles should include separate seeds for:

- environment;
- schema;
- learner;
- controller;
- diagnostic sampling;
- artifact sampling.

The implementation should not collapse all randomness into a lone integer.

Random schema seed suites should be named and recorded separately from run
replicate seed bundles.

## Claim Boundary

Allowed first-result statements:

- On `counterpoint_symbolic_n3_small_v001`, this active tower-control schema arm
  produced higher or lower return than direct tabular-Q under the locked
  budget.
- On `counterpoint_symbolic_n3_small_v001`, this schema family produced better
  or worse completion/sample-efficiency behavior than empty-schema
  tower-control.
- Empty-schema tower-control had measurable overhead relative to direct
  tabular-Q.
- Structured motion schema behaved differently from random balanced, random
  unbalanced, or bad schema controls under the same tower-control regime.
- Lift/fiber failures or active-tier traces explain part of the observed
  learning behavior.

Disallowed first-result statements:

- `state_collapser` is generally superior to direct RL.
- Tower methods generally beat flat methods.
- The method scales to large RL problems.
- Tensor-enabled execution is beneficial.
- CUDA execution is beneficial.
- The benchmark proves musical quality.
- A structural diagnostic alone proves learning benefit.

## Implementation Stop Conditions

The implementation workplan must stop and report if:

- active-tier exploit/explore surfaces cannot be bound to the counterpoint
  environment without upstream changes;
- fiber/lift resolution cannot produce executable primitive actions for
  counterpoint without changing `<state-collapser-repo>`;
- the implementation would need to edit `<state-collapser-repo>`;
- compatibility readouts become required in the online hot path without an
  explicit mode declaration;
- direct and tower arms cannot share the same legality/action-mask contract;
- random schema construction uses reward outcomes, learned values, terminal
  outcomes, or future episode information for an online-eligible schema;
- calibration shows `small` is too expensive for any meaningful multi-arm run;
- the serious run budget would need to shrink below the point where it is
  distinguishable from smoke;
- `state_collapser v0.7.0` tensorization metadata cannot be recorded;
- CPU/CUDA tensor modes would need to become runnable to make tests pass.

## Blueprint Acceptance Criteria

This blueprint is complete enough to become an implementation workplan when the
Project Owner accepts these design commitments:

- the serious fixture is `small`;
- the evaluation is learning/control first;
- tower arms use active-tier exploit/explore tower-control;
- direct, empty-schema tower, and nonempty-schema tower conditions remain
  separate;
- all named baselines are included;
- budget is chosen by calibration and frozen before the serious run;
- result docs live under `docs/evaluations/...`;
- the implementation must stop rather than silently demote tower-control to
  ordinary tower-position-key tabular-Q.

## Workplan Requirements

The next implementation workplan should use Phase.Stage.Action discipline.

It should include at least:

1. source authority re-read;
2. branch creation;
3. current code reality binding;
4. active-tier counterpoint adapter design;
5. direct baseline runner integration;
6. tower empty-schema exploit/explore runner integration;
7. tower nonempty-schema exploit/explore runner integration;
8. lift/fiber executor integration or explicit stop;
9. calibration runner;
10. budget-lock artifact;
11. serious run matrix runner;
12. aggregation and statistics;
13. evaluation docs writer;
14. CLI commands;
15. tests for arm contracts, artifact completeness, hot-path readout guards,
    and calibration outputs;
16. smoke validation on `tiny`;
17. calibration validation on `small`;
18. final lint/test run;
19. implementation log.

No source implementation should begin until that workplan exists and the
Project Owner approves execution.
