# Counterpoint First Serious Learning Evaluation Implementation Workplan

Date: 2026-05-29

Status: implementation workplan, not yet executed

Repository:

```text
<repo-root>
```

Source blueprint:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_001_counterpoint_first_serious_learning_evaluation_blueprint.md
```

## Purpose

This workplan translates the first serious counterpoint learning evaluation
blueprint into Phase.Stage.Action implementation work.

The target is not another smoke runner.

The target is a serious learning/control evaluation harness for:

```text
counterpoint_symbolic_n3_small_v001
```

with:

- direct masked-random baseline;
- direct environment tabular-Q baseline;
- active-tier exploit/explore tower-control tabular-Q with empty schema;
- active-tier exploit/explore tower-control tabular-Q with random balanced
  schema;
- active-tier exploit/explore tower-control tabular-Q with random unbalanced
  schema;
- active-tier exploit/explore tower-control tabular-Q with structured motion
  schema;
- active-tier exploit/explore tower-control tabular-Q with bad/adversarial
  schema;
- calibration before locked serious budget;
- evaluation-level artifacts and docs;
- tensor-capable-disabled linearization metadata.

## Execution Authority Status

This document is not approval to implement.

The Project Owner asked for this workplan:

```text
Ok use that bluerint to make Phase.Stage.Action workplan follow prime directive
```

Therefore this document may be created now.

Source, test, CLI, artifact-schema, and result-doc implementation must not begin
until the Project Owner explicitly approves execution of this exact workplan.

## Source Authority

This workplan follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/git_practices.md`
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`
- `docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md`
- `docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md`
- `docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_001_counterpoint_first_serious_learning_evaluation_blueprint.md`
- `docs/design/first_counterpoint_environment/01_002_counterpoint_hidden_graph_and_contraction_schema_benchmark_blueprint.md`
- `docs/design/first_counterpoint_environment/01_004_counterpoint_hidden_graph_and_contraction_schema_implementation_log.md`
- `docs/design/first_infrastructure_slice/01_001_initial_benchmarking_goals_discussion.md`
- `docs/design/first_infrastructure_slice/01_002_state_collapser_read_only_reconnaissance.md`
- `docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md`
- `docs/design/shared_benchmark_machinery/01_003_shared_benchmark_machinery_implementation_log.md`
- `docs/design/shared_benchmark_machinery/01_006_state_collapser_v0_7_tensorization_integration_implementation_log.md`
- `docs/methods/artifact_contract.md`
- `docs/methods/benchmark_modes.md`
- `docs/methods/seed_bundles.md`
- `docs/methods/timing_and_readout_discipline.md`
- `docs/environments/counterpoint_symbolic_v001.md`
- read-only current `state_collapser` docs and source for training,
  fiber-conditioned stages, active-tier control, and tensorization

## Fixed Implementation Decisions

These decisions are fixed for this workplan.

### Serious Fixture

Use:

```text
counterpoint_symbolic_n3_small_v001
```

for calibration and serious evaluation.

Use:

```text
counterpoint_symbolic_n3_tiny_v001
```

only for smoke and command validation.

### First Learner

Use upstream:

```text
state_collapser.training.TabularQLearner
```

for serious direct tabular and serious tower-control tabular arms.

Existing BBB local dictionary-Q code may remain for smoke compatibility, but
the serious learning evaluation must not use it as the serious tabular learner.

### First Tower-Control Mode

Use the existing global mode id:

```text
tower_exploit_explore
```

as the first serious active-tier tower-control execution mode.

Schema-specific arm ids distinguish empty, random, structured, and bad schema
arms.

Keep these existing registry modes reserved unless implementation research
proves a direct need to make them runnable in this slice:

```text
tower_fiber_conditioned_stage
tower_control_with_fiber_conditioned_substages
```

`FiberConditionedStage`, `FrozenQuotientBehavior`, and `PathFiber` may be used
inside the exploit/explore lift/resolve executor without changing the execution
mode id.

If this representation is false to the actual runtime behavior, stop and report
before implementing a substitute mode.

### Linearization Mode

Default serious evaluation runs use:

```text
tensor_available_disabled
```

Do not make `tensor_enabled_cpu` or `tensor_enabled_cuda` runnable in this
workplan.

### Artifact Schema Version

Keep:

```text
bbb.v001
```

unless implementation discovers that existing validators require additional
category metadata. If metadata is added, do not claim a published schema
migration unless the Project Owner explicitly authorizes a version bump.

### Result Docs Home

Create human-facing evaluation docs under:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/
```

Do not move design docs out of `docs/design`.

## Global Stop Conditions

Stop and ask the Project Owner if:

- explicit approval to execute this workplan has not been received;
- the branch or dirty status at execution time differs in a way that could mix
  unrelated source/test changes into this work;
- any action would require editing `<state-collapser-repo>`;
- active-tier exploit/explore surfaces cannot be imported from the installed
  pinned `state_collapser`;
- `state_collapser.training.TabularQLearner` cannot be used for the serious
  direct or tower-control learner without changing upstream;
- active-tier exploit/explore control cannot be bound to counterpoint without
  silently replacing it with ordinary tower-position-key Q-learning;
- lift/fiber resolution cannot produce executable counterpoint primitive
  actions without upstream changes;
- compatibility readouts or morphism construction become required in the online
  hot path without an explicit mode contract;
- random schema construction would use reward outcomes, terminal outcomes,
  learned values, future episode information, or evaluation statistics for an
  online-eligible schema;
- direct and tower arms cannot share the same legality and action-mask
  contracts;
- calibration shows `small` cannot run even a meaningful provisional full-arm
  matrix;
- a serious budget would need to be shrunk until it is just smoke;
- a phase would require simplifying, approximating, or substituting a weaker
  implementation for an action in this workplan;
- tests only pass by making CPU/CUDA tensor modes runnable;
- the implementation would need to reorder phases in a way not authorized by
  this document.

## Required Branch Discipline

After Project Owner approval and before implementation edits, create and switch
to:

```text
codex/counterpoint-serious-learning-eval
```

Do not execute this workplan directly on `main`.

## Required Running Implementation Log

Create and maintain:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_003_counterpoint_first_serious_learning_evaluation_implementation_log.md
```

The log must record:

- approval to execute this workplan;
- starting branch and status;
- every completed Phase.Stage.Action;
- exact commands run;
- validation outcomes;
- blockers and PO clarifications;
- any stop condition encountered;
- final git status.

## Phase 0: Execution Authority And Reality Binding

### Stage 0.1: Confirm Approval

#### Action 0.1.1

Confirm that the Project Owner explicitly approved execution of this exact file:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_002_counterpoint_first_serious_learning_evaluation_implementation_workplan.md
```

Acceptance criteria:

- approval is recorded in the implementation log;
- no source/test/CLI/artifact-schema implementation edits occur before this
  approval.

#### Action 0.1.2

Re-read Prime Directive files:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/git_practices.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md
```

Acceptance criteria:

- implementation log records the re-read;
- no contradiction is found between this workplan and the Prime Directive.

### Stage 0.2: Inspect Git State And Branch

#### Action 0.2.1

Run:

```bash
git status --short --branch
```

Acceptance criteria:

- current branch and dirty state are recorded;
- any unrelated source/test dirty files stop execution.

#### Action 0.2.2

Create and switch to:

```text
codex/counterpoint-serious-learning-eval
```

Acceptance criteria:

- branch exists;
- implementation log records the branch;
- workplan and design docs remain present.

### Stage 0.3: Bind Source Reality

#### Action 0.3.1

Read the blueprint and discussion source:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_001_counterpoint_first_serious_learning_evaluation_blueprint.md
```

Acceptance criteria:

- implementation log records that both files were read;
- no unresolved design question is discovered.

#### Action 0.3.2

Read current BBB counterpoint and shared machinery surfaces:

```text
src/big_boy_benchmarking/environments/counterpoint/runners.py
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
src/big_boy_benchmarking/environments/counterpoint/schemas.py
src/big_boy_benchmarking/environments/counterpoint/instances.py
src/big_boy_benchmarking/environments/counterpoint/masks.py
src/big_boy_benchmarking/environments/counterpoint/transition.py
src/big_boy_benchmarking/environments/counterpoint/rewards.py
src/big_boy_benchmarking/environments/counterpoint/ids.py
src/big_boy_benchmarking/modes/registry.py
src/big_boy_benchmarking/modes/contracts.py
src/big_boy_benchmarking/modes/linearization.py
src/big_boy_benchmarking/metrics/events.py
src/big_boy_benchmarking/metrics/timing.py
src/big_boy_benchmarking/metrics/bootstrap.py
src/big_boy_benchmarking/artifacts/manifests.py
src/big_boy_benchmarking/artifacts/paths.py
src/big_boy_benchmarking/artifacts/writers.py
src/big_boy_benchmarking/cli/main.py
```

Acceptance criteria:

- implementation log records the current code surfaces;
- any mismatch with this workplan stops execution.

#### Action 0.3.3

Read current upstream `state_collapser` surfaces read-only:

```text
<state-collapser-repo>/src/state_collapser/training/inputs.py
<state-collapser-repo>/src/state_collapser/training/learners.py
<state-collapser-repo>/src/state_collapser/training/transitions.py
<state-collapser-repo>/src/state_collapser/training/stages.py
<state-collapser-repo>/src/state_collapser/tower/runtime.py
<state-collapser-repo>/src/state_collapser/tower/control/controller.py
<state-collapser-repo>/src/state_collapser/tower/control/learner.py
<state-collapser-repo>/src/state_collapser/tower/control/executor.py
<state-collapser-repo>/src/state_collapser/tower/control/active_tier.py
```

Acceptance criteria:

- implementation log records read-only inspection;
- no upstream files are edited.

## Phase 1: Import Gates And Upstream Surface Tests

### Stage 1.1: Add Import Gate Tests

#### Action 1.1.1

Extend dependency/import tests to require these upstream serious-learning
surfaces:

```text
state_collapser.training.ActionDecision
state_collapser.training.ActionSelectionInput
state_collapser.training.TabularQLearner
state_collapser.training.TrainingTransition
state_collapser.training.FiberConditionedStage
state_collapser.training.FrozenQuotientBehavior
state_collapser.training.PathFiber
state_collapser.tower.control.ActiveTierController
state_collapser.tower.control.ActiveTierState
state_collapser.tower.control.ControlAction
state_collapser.tower.control.FrozenLowerContext
state_collapser.tower.control.LiftResolveExecutor
state_collapser.tower.control.TierLearner
state_collapser.tower.control.TierSignalState
state_collapser.tower.runtime.ExploitExploreTowerRuntime
```

Likely files:

```text
tests/test_state_collapser_dependency.py
tests/upstream/test_state_collapser_dependency_state.py
src/big_boy_benchmarking/state_collapser_probe.py
```

Acceptance criteria:

- tests prove the pinned installed package exposes the active-tier/fiber
  surfaces;
- tests do not require Torch;
- tests do not import from `<state-collapser-repo>` as an editable path.

#### Action 1.1.2

Run focused import-gate tests.

Expected command:

```bash
uv run pytest tests/test_state_collapser_dependency.py tests/upstream/test_state_collapser_dependency_state.py
```

Acceptance criteria:

- tests pass;
- installed `state_collapser` remains `0.7.0`.

## Phase 2: Serious Learning Contracts

### Stage 2.1: Create Serious Learning Package

#### Action 2.1.1

Create package:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/
```

with:

```text
__init__.py
arms.py
budgets.py
config.py
events.py
evaluation_paths.py
```

Acceptance criteria:

- package imports without side effects;
- no runner execution occurs at import time;
- no Torch import occurs at import time.

#### Action 2.1.2

Define serious learning arm contracts in:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/arms.py
```

Required arm ids:

```text
direct_masked_random
direct_tabular_q
tower_empty_exploit_explore_tabular_q
tower_random_balanced_exploit_explore_tabular_q
tower_random_unbalanced_exploit_explore_tabular_q
tower_motion_exploit_explore_tabular_q
tower_bad_exploit_explore_tabular_q
```

Required fields:

```text
arm_id
mode_id
schema_id
schema_family_id
controller_regime
training_surface
learner_id
purpose
requires_tower
requires_schema_seed
online_eligible
```

Acceptance criteria:

- all seven arms are represented;
- tower arms use `mode_id = tower_exploit_explore`;
- direct arms use existing direct mode ids;
- schema is the only intentional varying knob across tower arms.

#### Action 2.1.3

Add tests for arm contracts.

Likely file:

```text
tests/environments/counterpoint/test_serious_learning_arms.py
```

Acceptance criteria:

- all required arm ids are present;
- direct and tower arms are distinguishable;
- tower arms all share controller regime `exploit_explore`;
- random arms require schema seeds;
- projection-audit schema is not part of the serious arm list.

### Stage 2.2: Add Budget And Seed-Suite Contracts

#### Action 2.2.1

Define budget and seed-suite dataclasses in:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/budgets.py
```

Required concepts:

```text
CalibrationBudget
SeriousLearningBudgetLock
SchemaSeedSuite
SeedBundleSuite
```

Required budget-lock fields:

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

Acceptance criteria:

- budget lock serializes to JSON-safe dict;
- budget lock rejects missing required arms;
- budget lock rejects `tiny` as serious instance;
- budget lock defaults linearization mode to `tensor_available_disabled`;
- seed bundle suite preserves separate environment/schema/learner/controller
  seeds.

#### Action 2.2.2

Add tests for budget and seed-suite contracts.

Likely file:

```text
tests/environments/counterpoint/test_serious_learning_budgets.py
```

Acceptance criteria:

- valid calibration budget can be serialized;
- valid budget lock can be serialized;
- invalid serious fixture fails;
- missing arm fails;
- single random schema seed in a serious lock fails unless explicitly marked
  calibration.

### Stage 2.3: Add Controller And Learner Config Contracts

#### Action 2.3.1

Define controller and learner config dataclasses in:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/config.py
```

Required concepts:

```text
ExploitExploreControllerConfig
TabularQLearnerConfig
SeriousLearningRunConfig
```

Acceptance criteria:

- configs serialize to JSON-safe dicts;
- controller config records tier-control thresholds and training interval;
- learner config records alpha/gamma/epsilon/action-count policy;
- run config records linearization mode and readout/morphism policies.

#### Action 2.3.2

Add tests for config serialization and validation.

Likely file:

```text
tests/environments/counterpoint/test_serious_learning_config.py
```

Acceptance criteria:

- defaults are deterministic;
- invalid epsilon/alpha/gamma ranges fail;
- reserved linearization modes fail by default.

## Phase 3: Event Rows, Paths, And Manifest Extensions

### Stage 3.1: Add Serious Evaluation Paths

#### Action 3.1.1

Implement evaluation-level path helpers in:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/evaluation_paths.py
```

Required paths:

```text
evaluation_manifest.json
evaluation_arm_manifest.json
evaluation_run_index.csv
evaluation_budget_lock.json
evaluation_aggregate_summary.json
evaluation_aggregate_table.csv
calibration_summary.json
calibration_run_index.csv
calibration_recommendation.md
docs/
results/
```

Acceptance criteria:

- paths are rooted under explicit artifact root;
- current working directory does not affect path meaning;
- tests cover path construction.

#### Action 3.1.2

Add tests for evaluation-level paths.

Likely file:

```text
tests/environments/counterpoint/test_serious_learning_paths.py
```

Acceptance criteria:

- all required paths resolve under artifact root;
- path construction is deterministic.

### Stage 3.2: Add Serious Event Row Types

#### Action 3.2.1

Add row dataclasses in:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/events.py
```

Required rows:

```text
SeriousEpisodeRow
SeriousStepRow
ControllerEventRow
LiftFiberEventRow
EvaluationRunIndexRow
ArmSummaryRow
```

Required fields follow the blueprint's event row contract.

Acceptance criteria:

- rows expose stable `fieldnames()`;
- rows expose JSON/CSV-safe `to_flat_dict()`;
- controller rows include active tier and control action;
- lift/fiber rows include candidate counts and failure/departure reasons;
- direct rows do not require tower fields.

#### Action 3.2.2

Add tests for serious event rows.

Likely file:

```text
tests/environments/counterpoint/test_serious_learning_events.py
```

Acceptance criteria:

- every row serializes;
- required field order is stable;
- optional tower fields remain blank or `None` for direct arms.

### Stage 3.3: Add Evaluation Manifests

#### Action 3.3.1

Add evaluation-level manifest dataclasses.

Preferred location:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/manifests.py
```

Required manifests:

```text
SeriousLearningEvaluationManifest
SeriousLearningArmManifest
CalibrationSummary
CalibrationRecommendation
AggregateSummary
```

Acceptance criteria:

- manifests serialize to JSON-safe dictionaries;
- evaluation manifest records blueprint path and artifact schema version;
- arm manifest records all seven arms and their mode/schema/controller fields;
- calibration recommendation records measured runtime/artifact/noise summary
  and proposed budget.

#### Action 3.3.2

Add tests for evaluation manifests.

Likely file:

```text
tests/environments/counterpoint/test_serious_learning_manifests.py
```

Acceptance criteria:

- required keys are present;
- schema ids and mode ids are preserved;
- manifest serialization is stable.

## Phase 4: Direct Serious Learning Runner

### Stage 4.1: Build Upstream Tabular Direct Handoff

#### Action 4.1.1

Implement direct serious-learning input/transition helpers.

Preferred file:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/direct.py
```

Required behavior:

- build upstream `ActionSelectionInput` objects for direct counterpoint states;
- expose legal action masks as upstream action masks;
- map counterpoint actions to integer action ids for `TabularQLearner`;
- provide a direct key function based on concrete counterpoint state, not tower
  position;
- build upstream `TrainingTransition` objects with correct termination,
  truncation, reward, bootstrap, and action-mask data.

Acceptance criteria:

- no tower runtime is constructed for direct arms;
- direct tabular-Q uses upstream `TabularQLearner`;
- action id to `CounterpointAction` mapping is deterministic;
- legal mask semantics match existing counterpoint mask tests.

#### Action 4.1.2

Add tests for direct upstream tabular handoff.

Likely file:

```text
tests/environments/counterpoint/test_serious_learning_direct.py
```

Acceptance criteria:

- direct `ActionSelectionInput` has legal action mask;
- upstream `TabularQLearner.act()` returns a legal action id;
- transition update changes learner state;
- direct key function distinguishes concrete counterpoint states;
- no tower timing segments are recorded for direct runner.

### Stage 4.2: Implement Direct Serious Runner

#### Action 4.2.1

Implement direct serious runner functions in:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/direct.py
```

Required runners:

```text
run_serious_direct_masked_random(...)
run_serious_direct_tabular_q(...)
```

Required behavior:

- run multiple episodes under a seed bundle;
- write serious episode and step rows;
- write run/mode/dependency/seed/linearization/timing artifacts;
- write direct summaries;
- keep tower costs absent;
- default `linearization_mode_id` to `tensor_available_disabled`.

Acceptance criteria:

- masked-random remains non-learning floor;
- direct tabular-Q uses upstream `TabularQLearner`;
- artifacts include linearization manifest;
- timing includes environment/learner segments and excludes tower/controller
  segments.

#### Action 4.2.2

Add tests for direct serious runner.

Likely file:

```text
tests/environments/counterpoint/test_serious_learning_direct_runner.py
```

Acceptance criteria:

- tiny smoke run succeeds;
- small one-episode calibration-scale run succeeds;
- artifacts exist;
- no tower timing rows appear;
- upstream learner id is recorded.

## Phase 5: Tower-Control Counterpoint Binding

### Stage 5.1: Build Tower-Control State Adapter

#### Action 5.1.1

Implement active-tier state adapter helpers.

Preferred file:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
```

Required behavior:

- construct a counterpoint partition tower from the selected schema;
- initialize `ActiveTierState`;
- compute deepest known tier from the partition tower;
- map current concrete state to active-tier state cell;
- implement `move_down` and `move_up` callbacks for
  `ExploitExploreTowerRuntime`;
- record active-tier trace fields without compatibility readout materialization.

Acceptance criteria:

- empty schema produces the no-contraction tower-shell condition;
- nonempty schemata produce tower-control conditions;
- active tier direction follows upstream tier direction;
- no compatibility `QuotientTierView` readout is used by default.

#### Action 5.1.2

Add tests for active-tier state adapter.

Likely file:

```text
tests/environments/counterpoint/test_serious_learning_tower_control.py
```

Acceptance criteria:

- adapter initializes for empty schema;
- adapter initializes for motion schema;
- `move_down` and `move_up` preserve valid tier bounds;
- active tier trace fields are JSON-safe.

### Stage 5.2: Build Tier Learner Adapter

#### Action 5.2.1

Implement a counterpoint tier learner adapter satisfying upstream
`TierLearner`.

Preferred file:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
```

Required behavior:

- wrap upstream `TabularQLearner`;
- implement `behavior_action(state, mode)`;
- implement `observe(transition, frozen_context=...)`;
- implement `should_train(event_index)`;
- implement `train(frozen_context=...)`;
- return upstream control `LearnerUpdateSummary`;
- keep tabular behavior inspectable and deterministic by seed.

Acceptance criteria:

- adapter satisfies `isinstance(adapter, TierLearner)` if runtime-checkable;
- action choices are deterministic under fixed seed;
- learner update summaries include TD error and success;
- training interval is configurable.

#### Action 5.2.2

Add tests for tier learner adapter.

Acceptance criteria:

- adapter produces behavior actions in explore and exploit modes;
- `should_train` follows config;
- `observe` and `train` produce summaries;
- no neural/Torch dependency is introduced.

### Stage 5.3: Build Lift/Resolve Executor

#### Action 5.3.1

Implement counterpoint lift/resolve executor satisfying upstream
`LiftResolveExecutor`.

Preferred file:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
```

Required behavior:

- resolve active-tier abstract choices to concrete counterpoint primitive
  actions;
- use `PartitionTower` local queries and path/fiber machinery where available;
- use `FiberConditionedStage`, `FrozenQuotientBehavior`, and `PathFiber` when a
  frozen coarse behavior is available and executable;
- step the concrete counterpoint environment;
- return upstream `ActiveTierTransition`;
- record lift success/failure and fiber departure data.

Acceptance criteria:

- concrete primitive actions remain legal under the original counterpoint mask;
- lift failure is recorded as an event, not hidden;
- executor does not require editing upstream;
- executor does not use compatibility readouts by default.

#### Action 5.3.2

Add tests for lift/resolve executor.

Acceptance criteria:

- executor can realize an empty-schema tier-0 action;
- executor can realize or explicitly fail a nonempty-schema action with a
  recorded reason;
- realized action is legal;
- failure rows are emitted when no lift candidate exists.

### Stage 5.4: Bind Exploit/Explore Runtime

#### Action 5.4.1

Implement tower-control episode loop.

Preferred file:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
```

Required behavior:

- instantiate `ExploitExploreTowerRuntime`;
- provide active-tier state, tier configs, controller, tier learner, executor,
  frozen contexts, `move_down`, and `move_up`;
- run episode event loop up to configured horizon;
- record controller rows;
- record lift/fiber rows;
- record episode and step summaries;
- time controller decision, lift/resolve, learner action/update, tower
  reset/update, environment reset/step, artifact logging separately.

Acceptance criteria:

- empty schema tower-control smoke succeeds on tiny;
- motion schema tower-control smoke succeeds or stops with a real binding
  failure;
- online timing excludes compatibility readout and morphism construction by
  default;
- mode manifest records `tower_exploit_explore`.

#### Action 5.4.2

Add tests for tower-control episode loop.

Acceptance criteria:

- one tiny empty-schema tower-control episode writes controller rows;
- one tiny motion-schema tower-control episode writes controller rows or a
  clearly expected lift-failure row;
- active control actions are counted;
- `uses_compatibility_readout` remains false.

## Phase 6: Serious Learning Matrix Runner

### Stage 6.1: Implement Arm Runner Dispatcher

#### Action 6.1.1

Implement arm dispatch in:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/runner.py
```

Required behavior:

- dispatch direct arms to direct serious runners;
- dispatch tower arms to tower-control runner;
- apply schema ids and schema seed suites;
- apply seed bundle suite;
- write per-run artifacts;
- write evaluation run index rows.

Acceptance criteria:

- all seven arms can be dispatched;
- direct and tower dispatch stay separate;
- missing schema seed for random schema arm fails clearly;
- run ids are deterministic and include arm/replicate/schema-seed identity.

#### Action 6.1.2

Add tests for arm dispatch.

Acceptance criteria:

- each arm dispatches to expected runner kind;
- random schema arms expand over schema seed suite;
- run ids are stable;
- artifact paths are under artifact root.

### Stage 6.2: Implement Calibration Runner

#### Action 6.2.1

Implement calibration runner in:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/runner.py
```

Required behavior:

- run all seven arms on `small` with a provisional calibration budget;
- record timing, artifact volume, curve-noise proxies, completion/success
  rarity, lift/resolve failure frequency, and random-schema variability;
- write `calibration_summary.json`;
- write `calibration_run_index.csv`;
- write `calibration_recommendation.md`;
- propose a locked serious budget.

Acceptance criteria:

- calibration cannot use `tiny` as serious calibration unless explicitly marked
  smoke;
- calibration includes every arm;
- calibration recommendation is generated from measured outputs;
- calibration does not silently omit failed arms.

#### Action 6.2.2

Add tests for calibration runner using minimal budgets.

Acceptance criteria:

- tiny smoke calibration path works for tests only;
- small one-episode provisional calibration works or stops with measured cost
  reason;
- calibration artifacts exist;
- recommendation contains all arms.

### Stage 6.3: Implement Budget-Locked Serious Runner

#### Action 6.3.1

Implement serious run from budget lock.

Preferred file:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/runner.py
```

Required behavior:

- read or receive `SeriousLearningBudgetLock`;
- execute all locked arms;
- refuse to run if arm list is incomplete;
- refuse to run if serious fixture is not `small`;
- refuse to run if linearization mode is reserved;
- write evaluation-level artifacts.

Acceptance criteria:

- locked run cannot mutate budget during execution;
- all arms receive the same episode/replicate budget;
- failed arms are recorded with explicit status;
- no serious run proceeds from ad hoc CLI flags alone.

#### Action 6.3.2

Add tests for budget-locked run validation.

Acceptance criteria:

- complete lock passes validation;
- incomplete lock fails;
- `tiny` lock fails;
- reserved linearization mode fails;
- single random schema seed in serious lock fails unless marked exploratory.

## Phase 7: Aggregation And Statistics

### Stage 7.1: Implement Aggregators

#### Action 7.1.1

Implement aggregation helpers in:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/aggregation.py
```

Required outputs:

```text
evaluation_aggregate_summary.json
evaluation_aggregate_table.csv
results/learning_curves.csv
results/timing_summary.csv
results/controller_summary.csv
results/schema_diagnostic_summary.csv
```

Required statistics:

- per-arm mean;
- per-arm standard deviation;
- confidence interval over seed-bundle replicates;
- bootstrap interval where sample size supports it;
- pairwise deltas against direct tabular-Q;
- pairwise deltas against empty-schema tower-control;
- random schema family summaries across schema seeds and run seed bundles.

Acceptance criteria:

- aggregation reads artifact rows rather than terminal output;
- small sample sizes are marked appropriately;
- missing arms cause incomplete status;
- random schema summaries do not hide schema-seed variance.

#### Action 7.1.2

Add aggregation tests.

Likely file:

```text
tests/environments/counterpoint/test_serious_learning_aggregation.py
```

Acceptance criteria:

- aggregate table is deterministic;
- confidence/bootstrap fields are present or explicitly unavailable;
- pairwise deltas are computed against correct baselines.

## Phase 8: Evaluation Docs Writer

### Stage 8.1: Create Evaluation Docs Skeleton

#### Action 8.1.1

Implement docs writer in:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/docs_writer.py
```

Target folder:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/
```

Required files:

```text
README.md
method.md
runbook.md
artifact_index.md
results/summary.md
```

Acceptance criteria:

- docs are generated from evaluation artifacts;
- docs include exact claim boundary;
- docs include artifact root and command lines;
- docs do not claim tensor-enabled/CUDA/general superiority results.

#### Action 8.1.2

Add docs writer tests.

Acceptance criteria:

- docs writer creates expected files in a temp docs root;
- generated docs contain evaluation id and artifact root;
- generated docs do not include forbidden claim language.

## Phase 9: CLI Integration

### Stage 9.1: Add CLI Commands

#### Action 9.1.1

Update:

```text
src/big_boy_benchmarking/cli/main.py
```

Add command family:

```text
counterpoint serious-learning calibrate
counterpoint serious-learning run
counterpoint serious-learning summarize
```

Acceptance criteria:

- calibration command writes calibration artifacts;
- run command requires or creates a budget-lock artifact;
- summarize command reads artifacts and writes aggregate/docs outputs;
- `--linearization-mode` defaults to `tensor_available_disabled`;
- reserved linearization modes fail clearly.

#### Action 9.1.2

Add CLI tests.

Likely file:

```text
tests/cli/test_cli.py
```

or:

```text
tests/environments/counterpoint/test_serious_learning_cli.py
```

Acceptance criteria:

- CLI help includes command family;
- tiny smoke command path works for tests;
- small minimal calibration command writes expected outputs;
- reserved linearization mode fails.

### Stage 9.2: Update Contract Validation

#### Action 9.2.1

Update `validate-contracts` to include serious learning arm contracts and
budget/config validators.

Acceptance criteria:

- output includes serious learning arm count;
- output includes active tower-control mode availability;
- existing mode and linearization counts remain present.

#### Action 9.2.2

Update contract validation tests.

Acceptance criteria:

- expected serious arm count is asserted;
- existing validate-contracts tests still pass.

## Phase 10: Artifact And Method Documentation

### Stage 10.1: Update Method Docs

#### Action 10.1.1

Update or add method docs:

```text
docs/methods/counterpoint_serious_learning.md
docs/methods/benchmark_modes.md
docs/methods/artifact_contract.md
docs/methods/timing_and_readout_discipline.md
docs/methods/seed_bundles.md
```

Acceptance criteria:

- docs distinguish smoke, calibration, budget lock, and serious run;
- docs distinguish direct, empty-schema tower-control, and nonempty-schema
  tower-control;
- docs explain `tower_exploit_explore`;
- docs explain tensor-capable-disabled default;
- docs preserve hot-path readout discipline.

### Stage 10.2: Update Environment Docs

#### Action 10.2.1

Update:

```text
docs/environments/counterpoint_symbolic_v001.md
```

Acceptance criteria:

- environment doc points to serious learning evaluation design;
- doc states `small` is first serious fixture;
- doc states `tiny` is smoke only;
- doc does not claim a serious result has been run until artifacts exist.

### Stage 10.3: Update Design Continuity

#### Action 10.3.1

Append a short note to:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
```

Acceptance criteria:

- note points to this workplan;
- note does not rewrite the discussion history;
- PO corrections remain attributed.

## Phase 11: Validation And Smoke Runs

### Stage 11.1: Focused Unit Tests

#### Action 11.1.1

Run focused new tests:

```bash
uv run pytest tests/environments/counterpoint/test_serious_learning_arms.py tests/environments/counterpoint/test_serious_learning_budgets.py tests/environments/counterpoint/test_serious_learning_config.py tests/environments/counterpoint/test_serious_learning_events.py tests/environments/counterpoint/test_serious_learning_paths.py tests/environments/counterpoint/test_serious_learning_manifests.py
```

Acceptance criteria:

- focused contract tests pass.

#### Action 11.1.2

Run focused runner tests:

```bash
uv run pytest tests/environments/counterpoint/test_serious_learning_direct.py tests/environments/counterpoint/test_serious_learning_direct_runner.py tests/environments/counterpoint/test_serious_learning_tower_control.py tests/environments/counterpoint/test_serious_learning_aggregation.py
```

Acceptance criteria:

- focused runner tests pass;
- tower-control tests do not require compatibility readouts by default.

### Stage 11.2: CLI And Contract Validation

#### Action 11.2.1

Run:

```bash
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Acceptance criteria:

- command exits 0;
- output includes serious learning arm count;
- output still includes execution mode and linearization mode counts.

#### Action 11.2.2

Run CLI smoke on `tiny` into `<tmp-dir>`.

Expected shape:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning calibrate --artifact-root <tmp-dir>/bbb-counterpoint-serious-learning-tiny-smoke --instance-id tiny --episodes 1 --replicates 1 --schema-seeds 1
```

Acceptance criteria:

- command succeeds;
- output is explicitly labelled smoke/non-evidence;
- artifacts include linearization manifest and controller rows for tower arms.

### Stage 11.3: Small Calibration Validation

#### Action 11.3.1

Run minimal calibration on `small` into `<tmp-dir>`.

Expected shape:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning calibrate --artifact-root <tmp-dir>/bbb-counterpoint-serious-learning-small-calibration --instance-id small --episodes 1 --replicates 1 --schema-seeds 1
```

Acceptance criteria:

- command succeeds or stops with a measured, logged reason;
- calibration artifacts exist if command succeeds;
- all seven arms are represented;
- artifact output is not called a serious result.

### Stage 11.4: Full Test And Lint

#### Action 11.4.1

Run:

```bash
uv run pytest
```

Acceptance criteria:

- full test suite passes.

#### Action 11.4.2

Run:

```bash
uv run ruff check .
```

Acceptance criteria:

- ruff passes.

## Phase 12: Completion Audit

### Stage 12.1: Complete Implementation Log

#### Action 12.1.1

Complete:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_003_counterpoint_first_serious_learning_evaluation_implementation_log.md
```

Acceptance criteria:

- every Phase.Stage.Action is marked complete, blocked, or explicitly skipped
  by PO instruction;
- validation commands and outcomes are recorded;
- any stop condition is recorded honestly;
- final claim boundary is recorded.

### Stage 12.2: Final Status

#### Action 12.2.1

Run:

```bash
git status --short --branch
```

Acceptance criteria:

- final status is recorded in the implementation log;
- unexpected files are investigated before final report.

## Completion Criteria

This workplan is complete when:

- serious learning arm contracts exist and validate;
- serious budget and seed-suite contracts exist and validate;
- direct serious masked-random and direct serious upstream-tabular-Q runners
  exist;
- active-tier exploit/explore tower-control counterpoint runner exists or a
  stop condition has been reached and recorded;
- empty-schema and nonempty-schema tower-control arms remain separate;
- random schema arms use schema seed suites;
- calibration runner writes calibration artifacts and recommendation;
- budget-lock runner validates serious locks;
- aggregation writes serious summary tables;
- evaluation docs writer creates the first human-facing docs home under
  `docs/evaluations/...`;
- CLI exposes calibration/run/summarize commands;
- validation commands pass or a stop condition is recorded;
- implementation log is complete.

## Explicit Non-Completion Cases

The work is not complete if:

- tower arms are implemented as ordinary tower-position-key tabular-Q while
  being called exploit/explore tower-control;
- direct tabular serious runner uses the old BBB local dictionary-Q in place of
  upstream `TabularQLearner`;
- `small` is replaced by `tiny` for the serious path;
- all random schema evidence uses a single unmarked random schema seed;
- CPU/CUDA tensor modes are made runnable to satisfy tests;
- compatibility readout cost is hidden inside learner/controller online timing;
- result docs claim more than the allowed first-result boundary.
