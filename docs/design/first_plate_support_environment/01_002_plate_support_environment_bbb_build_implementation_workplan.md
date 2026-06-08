# PlateSupport BBB Environment Build Implementation Workplan

## Status

Status: initial implementation workplan.

This document is generated from:

```text
docs/design/first_plate_support_environment/01_001_plate_support_environment_bbb_build_blueprint.md
```

This workplan uses `Phase.Stage.Action` discipline.

This workplan is not an execution approval. Execution requires explicit Project
Owner instruction.

## Prime Directive Compliance Notes

This workplan follows:

- `docs/prime_directive/prime_directive.md`;
- `docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md`;
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`;
- the Prime Directive corrective amendment on workplan rewrite during
  implementation;
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`;
- `docs/prime_directive/git_practices.md`.

Operational consequences:

- Do not execute this workplan until the Project Owner explicitly approves
  execution.
- Once approved, execute actions in order unless the Project Owner explicitly
  authorizes reordering.
- Do not silently simplify, collapse, or reinterpret actions.
- Stop and ask if an action is ambiguous, conflicts with repo reality, requires
  upstream edits, or would require a scope reduction.
- Record execution in:

```text
docs/design/first_plate_support_environment/01_003_plate_support_environment_bbb_build_implementation_log.md
```

## Authority And Attribution

Project Owner direction already established:

- move on from counterpoint for now;
- use a more robotics-based constrained example;
- use the existing plate examples as the natural next candidate;
- find an environment where training need is large enough to measure clearly;
- do not frame PlateSupport as merely a counterpoint-shaped package;
- create the environment-build design area now;
- do not create the evaluation folder yet.

Consultant-authored assumptions pending Project Owner override:

- environment-readiness artifacts live under
  `docs/environments/plate_support_5x5_default_v001/readiness/<run_label>/`;
- random-policy reconnaissance is included by default but labeled as
  non-evaluation reconnaissance;
- first BBB instance id is `plate_support_5x5_default_v001`;
- package path is `src/big_boy_benchmarking/environments/plate_support`;
- environment docs mention upstream training surfaces but state clearly that
  availability is not evaluation evidence.

If the Project Owner rejects any assumption, revise this workplan before
execution.

## Decision Locks Before Implementation

These locks are binding for execution unless explicitly changed by the Project
Owner.

- This is an environment build, not an evaluation build.
- Do not create `docs/evaluations/plate_support...`.
- Do not edit `<state-collapser-repo>`.
- Do not copy counterpoint-specific evaluation logic.
- Do not run serious learning budgets.
- Do not claim tower benefit.
- Use shared BBB artifact/timing/seed/dependency/linearization machinery.
- Preserve PlateSupport-specific contract distinctions:
  - invalid self-loop;
  - valid clipped self-transition;
  - candidate state versus realized next state;
  - support pattern;
  - reachability pattern;
  - stability predicates;
  - default schema versus no-contraction schema.

## Expected Final Deliverables

Implementation should produce:

```text
src/big_boy_benchmarking/environments/plate_support/
tests/environments/plate_support/
docs/environments/plate_support_5x5_default_v001.md
docs/environments/plate_support_5x5_default_v001/readiness/<run_label>/
docs/design/first_plate_support_environment/01_003_plate_support_environment_bbb_build_implementation_log.md
```

The CLI should expose:

```bash
uv run python -m big_boy_benchmarking.cli plate-support readiness \
  --artifact-root docs/environments/plate_support_5x5_default_v001/readiness/dev_001
```

## Workplan

### Phase 0: Execution Setup And Reality Binding

#### Phase 0.Stage 1: Re-anchor Repository State

##### Phase 0.Stage 1.Action 1: Verify working tree and branch

Action:

- run `git status --short --branch`;
- record branch name and dirty files in the implementation log.

Completion criteria:

- current branch is known;
- worktree state is recorded before edits.

Stop condition:

- stop if unrelated dirty files would be overwritten or confused with this
  work.

##### Phase 0.Stage 1.Action 2: Create implementation branch

Action:

- create or switch to a dedicated branch:

```text
codex/plate-support-environment-build
```

Completion criteria:

- implementation branch is active;
- branch creation/switch is recorded in the implementation log.

Stop condition:

- stop if branch creation would discard or overwrite existing work.

##### Phase 0.Stage 1.Action 3: Re-read controlling documents

Action:

- re-read:
  - this workplan;
  - the PlateSupport blueprint;
  - the PlateSupport design discussion;
  - `environment_construction_for_benchmark_evaluations_protocol.md`;
  - `git_practices.md`.

Completion criteria:

- implementation log records the source documents read.

Stop condition:

- stop if a newer design document contradicts this workplan.

#### Phase 0.Stage 2: Create Running Implementation Log

##### Phase 0.Stage 2.Action 1: Create implementation log file

Action:

- create:

```text
docs/design/first_plate_support_environment/01_003_plate_support_environment_bbb_build_implementation_log.md
```

Minimum initial sections:

```text
# PlateSupport BBB Environment Build Implementation Log

## Status
## Branch And Repo State
## Source Documents
## Phase.Stage.Action Progress
## Commands Run
## Files Changed
## Tests And Validation
## Surprises / Stop Conditions
## Final Summary
```

Completion criteria:

- log exists before source implementation starts.

Stop condition:

- stop if the log file path conflicts with an existing unrelated file.

##### Phase 0.Stage 2.Action 2: Add progress table to log

Action:

- add a table with columns:

```text
Phase.Stage.Action
Status
Evidence
Notes
```

Completion criteria:

- log can track each action as `pending`, `in_progress`, `completed`, or
  `blocked`.

Stop condition:

- stop if logging would require changing this approved workplan.

### Phase 1: PlateSupport Package Skeleton And Stable Identity

#### Phase 1.Stage 1: Create Package Directory

##### Phase 1.Stage 1.Action 1: Create package and test directories

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/
tests/environments/plate_support/
```

Completion criteria:

- directories exist;
- no evaluation directory is created.

Stop condition:

- stop if `plate_support` already exists with unrelated content.

##### Phase 1.Stage 1.Action 2: Add package `__init__.py`

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/__init__.py
```

Content requirements:

- short module docstring;
- export stable ids and the readiness runner only after those modules exist;
- avoid heavy upstream imports at package import time if possible.

Completion criteria:

- importing `big_boy_benchmarking.environments.plate_support` is cheap and
  side-effect-light.

#### Phase 1.Stage 2: Define Stable Ids

##### Phase 1.Stage 2.Action 1: Implement `ids.py`

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/ids.py
```

Required constants:

```text
ENVIRONMENT_FAMILY_ID = "plate_support"
UPSTREAM_SMOKE_ID = "plate_support_env"
UPSTREAM_MODULE = "state_collapser.examples.plate_support_env"
DEFAULT_INSTANCE_ID = "plate_support_5x5_default_v001"
SMOKE_FIXTURE_ID = "plate_support_5x5_default_smoke_v001"
STRUCTURAL_FIXTURE_ID = "plate_support_5x5_default_v001"
READINESS_RUN_FAMILY_ID = "plate_support_environment_readiness_v001"
DEFAULT_SCHEMA_ID = "upstream_default_plate_support_schema_v001"
NO_CONTRACTION_SCHEMA_ID = "no_contraction_schema_v001"
REWARD_BUNDLE_ID = "plate_support_goal_self_loop_penalty_v001"
LEGALITY_CONTRACT_ID = "plate_support_validity_predicates_v001"
ACTION_LABEL_CONTRACT_ID = "plate_support_action_labels_v001"
```

Completion criteria:

- constants are defined in one place;
- constants are importable by tests and docs writer.

Stop condition:

- stop if implementation reveals an existing conflicting id convention.

##### Phase 1.Stage 2.Action 2: Implement id tests

Action:

- create:

```text
tests/environments/plate_support/test_ids.py
```

Assertions:

- ids equal blueprint values;
- ids are nonempty strings;
- schema ids differ;
- fixture ids differ where roles differ.

Completion criteria:

- focused id test passes.

### Phase 2: Upstream Surface Binding

#### Phase 2.Stage 1: Centralize Upstream Imports

##### Phase 2.Stage 1.Action 1: Implement `upstream.py`

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/upstream.py
```

Required behavior:

- import the upstream module named in `ids.UPSTREAM_MODULE`;
- expose an `ImportedPlateSupportSurface` dataclass or equivalent;
- require:
  - `PlateSupportEnv`;
  - `PlateSupportState`;
  - `PlateSupportEnvRuntime`;
  - `PlateSupportExploitExploreRuntime`;
  - `PlateSupportLiftResolveExecutor`;
  - `PlateSupportTierLearner`;
  - `TowerTrainingConfig`;
  - `ExploitExploreTrainingConfig`;
  - `run_tower_training`;
  - `run_exploit_explore_training`;
  - `default_plate_support_schema`;
  - `ACTION_COUNT`;
  - `MAX_STEPS`;
  - `START_STATE`;
  - `CANDIDATE_GOAL_STATE`;
  - `all_candidate_states`;
  - `all_valid_states`;
  - `valid_outgoing_transitions`;
  - `primitive_transition`;
  - validity and geometry helper functions used by diagnostics.

Completion criteria:

- one local function can return all required upstream handles;
- missing surfaces raise a clear PlateSupport-specific error.

Stop condition:

- stop if installed `state_collapser` lacks required surfaces.

##### Phase 2.Stage 1.Action 2: Add upstream surface tests

Action:

- create:

```text
tests/environments/plate_support/test_upstream_surface.py
```

Assertions:

- required surface imports;
- action count `12`;
- max steps `50`;
- valid state count `89`;
- candidate state count `2700`;
- start and goal are valid;
- goal is not one primitive action from start.

Completion criteria:

- test passes against installed dependency.

Stop condition:

- stop if upstream structural facts differ from blueprint values.

#### Phase 2.Stage 2: Record Dependency Expectations

##### Phase 2.Stage 2.Action 1: Bind state_collapser dependency state usage

Action:

- confirm PlateSupport runner will use:

```text
big_boy_benchmarking.upstream.state_collapser.collect_state_collapser_dependency_state
```

and not custom dependency introspection.

Completion criteria:

- dependency collection is referenced in runner design or implementation.

Stop condition:

- stop if dependency helper cannot be imported.

### Phase 3: State, Action, And Contract Records

#### Phase 3.Stage 1: Implement Action Contract

##### Phase 3.Stage 1.Action 1: Implement `actions.py`

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/actions.py
```

Required action labels:

```text
0: plate_x_plus
1: plate_x_minus
2: plate_y_plus
3: plate_y_minus
4: theta_plus
5: theta_minus
6: arm1_extend
7: arm1_retract
8: arm2_extend
9: arm2_retract
10: arm3_extend
11: arm3_retract
```

Required fields per action:

```text
action_index
action_label
action_category
description
upstream_identity
```

Completion criteria:

- all `12` actions are covered;
- labels are stable and JSON/CSV safe.

Stop condition:

- stop if upstream action semantics conflict with these labels.

##### Phase 3.Stage 1.Action 2: Add action contract tests

Action:

- add tests in:

```text
tests/environments/plate_support/test_state_action_records.py
```

Assertions:

- exactly `12` action records;
- indices are `0..11`;
- labels are unique;
- categories are nonempty;
- upstream identities are nonempty.

Completion criteria:

- action tests pass.

#### Phase 3.Stage 2: Implement State Record Contract

##### Phase 3.Stage 2.Action 1: Implement `states.py`

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/states.py
```

Required conversion:

- upstream `PlateSupportState` to JSON-safe record.

Required fields:

```text
state_id
x_idx
y_idx
theta_idx
e1
e2
e3
support_pattern
reachability_pattern
stable_support_pattern
plate_center_in_bounds
all_sockets_in_bounds
minimum_engaged_supports
ordered_socket_positions
is_goal
is_start
```

Completion criteria:

- records are JSON safe;
- records do not rely only on Python repr;
- start/goal flags are correct.

Stop condition:

- stop if upstream helper functions cannot provide required predicate fields.

##### Phase 3.Stage 2.Action 2: Add state record tests

Action:

- extend:

```text
tests/environments/plate_support/test_state_action_records.py
```

Assertions:

- start state record has expected coordinates/extensions;
- goal state record has expected coordinates/extensions;
- support and reachability patterns are present;
- record is JSON serializable.

Completion criteria:

- state tests pass.

#### Phase 3.Stage 3: Implement Type Records

##### Phase 3.Stage 3.Action 1: Implement `types.py`

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/types.py
```

Expected dataclasses or typed records:

```text
PlateSupportInstanceSpec
PlateSupportTransitionRecord
PlateSupportGraphSummary
PlateSupportTowerProbeSummary
PlateSupportReadinessSummary
```

Completion criteria:

- type records support `dict` conversion directly or via shared manifest
  `to_json_dict`;
- no non-serializable upstream objects leak into artifact payloads.

Stop condition:

- stop if type design would duplicate shared manifest classes unnecessarily.

### Phase 4: Graph, Geometry, And Transition Diagnostics

#### Phase 4.Stage 1: Implement Geometry Summaries

##### Phase 4.Stage 1.Action 1: Implement `geometry.py`

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/geometry.py
```

Required summaries:

- support-pattern counts;
- reachability-pattern counts;
- orientation counts;
- position counts;
- validity predicate summary over ambient and valid states;
- start and goal geometry records.

Completion criteria:

- functions return JSON/CSV-safe row dictionaries;
- predicate names are stable.

Stop condition:

- stop if ambient predicate evaluation is ambiguous or too costly.

##### Phase 4.Stage 1.Action 2: Add geometry tests

Action:

- add geometry coverage in:

```text
tests/environments/plate_support/test_graph_diagnostics.py
```

Assertions:

- support/reachability pattern summaries include `(1,1,1)` and `(1,0,1)`;
- orientation summary includes all observed theta values;
- validity predicate rows include required predicate names.

Completion criteria:

- geometry tests pass.

#### Phase 4.Stage 2: Implement Graph Enumeration

##### Phase 4.Stage 2.Action 1: Implement `graph.py`

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/graph.py
```

Required functions:

```text
enumerate_valid_states()
enumerate_transition_records()
reachable_from_start()
shortest_path_to_goal()
summarize_outgoing_counts()
summarize_invalid_actions()
summarize_self_transitions()
```

Required behavior:

- enumerate all `89 * 12 = 1068` state/action transition records;
- preserve candidate state and realized next state;
- distinguish invalid moves from valid clipped self-transitions.

Completion criteria:

- graph summary reproduces blueprint facts.

Stop condition:

- stop if transition count or shortest path length differs from blueprint in a
  way that changes interpretation.

##### Phase 4.Stage 2.Action 2: Add graph diagnostics tests

Action:

- create or extend:

```text
tests/environments/plate_support/test_graph_diagnostics.py
```

Assertions:

- ambient count `2700`;
- valid count `89`;
- reachable count `89`;
- goal reachable;
- shortest path length `6`;
- transition record count `1068`;
- invalid move count greater than zero;
- valid clipped self-transition count greater than zero.

Completion criteria:

- graph diagnostics tests pass.

#### Phase 4.Stage 3: Implement Structural Diagnostics Composer

##### Phase 4.Stage 3.Action 1: Implement `diagnostics.py`

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/diagnostics.py
```

Required outputs as in-memory payloads:

```text
instance_summary
graph_summary
state_summary_rows
action_table_rows
transition_summary_rows
shortest_path_rows
validity_predicate_summary_rows
support_pattern_summary_rows
reachability_pattern_summary_rows
orientation_summary_rows
position_summary_rows
outgoing_action_count_summary_rows
invalid_action_summary_rows
self_transition_summary_rows
random_policy_recon_summary_rows
training_surface_availability
```

Completion criteria:

- one function can build the complete structural diagnostic payload.

Stop condition:

- stop if random-policy reconnaissance begins to look like a learning
  evaluation or requires long budgets.

##### Phase 4.Stage 3.Action 2: Implement optional random-policy reconnaissance

Action:

- implement deterministic uniform random policy reconnaissance with defaults:

```text
episodes = 1000
seed = 0
horizon = upstream MAX_STEPS
```

Required output fields:

```text
policy_id
episodes
seed
horizon
success_count
success_rate
mean_steps
mean_reward
mean_invalid_moves
mean_valid_transition_flags
success_steps_min
success_steps_mean
claim_boundary
```

Completion criteria:

- output includes claim boundary stating reconnaissance is not method
  evaluation.

Stop condition:

- stop if this diagnostic becomes slow enough to compromise normal test/runtime
  usage.

### Phase 5: Tower Probe And Linearization Metadata

#### Phase 5.Stage 1: Implement Tower Probe

##### Phase 5.Stage 1.Action 1: Implement `tower_probe.py`

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/tower_probe.py
```

Required behavior:

- run upstream `continuous_probe` for:
  - `schema_mode="default"`;
  - `schema_mode="none"`;
- default steps `20`;
- default seed `0`;
- default sample size `1`;
- contraction policy enabled;
- reset on terminal enabled.

Required row fields:

```text
schema_mode
steps
seed
sample_size
use_contraction_policy
reset_on_terminal
depth_curve_json
max_depth
scheduled_assignment_count
unscheduled_assignment_count
reset_event_count
```

Completion criteria:

- default schema reaches depth at least `2`;
- no-contraction schema stays depth `1`.

Stop condition:

- stop if upstream tower-depth behavior differs from blueprint assumptions.

##### Phase 5.Stage 1.Action 2: Add tower probe tests

Action:

- create:

```text
tests/environments/plate_support/test_tower_probe.py
```

Assertions:

- default mode max depth `>= 2`;
- no-contraction mode max depth `== 1`;
- default scheduled assignments `> 0`;
- no-contraction scheduled assignments `== 0`.

Completion criteria:

- tower probe tests pass.

#### Phase 5.Stage 2: Integrate Linearization Metadata

##### Phase 5.Stage 2.Action 1: Plan runner linearization call

Action:

- ensure readiness runner will call:

```text
build_linearization_artifact_payload(
    linearization_mode_id="tensor_available_disabled",
    tower=<current partition tower>,
    max_action_count=12,
)
```

Completion criteria:

- runner has a concrete source for the tower object and max action count.

Stop condition:

- stop if tower object is unavailable after readiness reset.

### Phase 6: Artifact Paths, Manifests, And Runner

#### Phase 6.Stage 1: Implement Path Helpers

##### Phase 6.Stage 1.Action 1: Implement `paths.py`

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/paths.py
```

Required behavior:

- default environment doc path:

```text
docs/environments/plate_support_5x5_default_v001.md
```

- default readiness root helper:

```text
docs/environments/plate_support_5x5_default_v001/readiness/<run_label>
```

Completion criteria:

- helpers use explicit repo/environment roots;
- no behavior depends on ambient `cwd` except CLI path resolution.

Stop condition:

- stop if artifact root semantics conflict with shared path helpers.

#### Phase 6.Stage 2: Implement Manifest Builders

##### Phase 6.Stage 2.Action 1: Implement `manifests.py`

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/manifests.py
```

Required payload builders:

```text
plate_support_environment_manifest
plate_support_instance_manifest
plate_support_legality_contract
plate_support_reward_contract
plate_support_action_contract
plate_support_diagnostic_manifest
plate_support_tower_probe_manifest
```

Completion criteria:

- payloads are JSON safe;
- stable ids appear in each relevant manifest.

Stop condition:

- stop if a manifest duplicates existing shared manifest semantics in a
  confusing way.

#### Phase 6.Stage 3: Implement Readiness Runner

##### Phase 6.Stage 3.Action 1: Implement `runner.py`

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/runner.py
```

Required entrypoint:

```text
run_plate_support_environment_readiness(...)
```

Required parameters:

```text
artifact_root
instance_id = DEFAULT_INSTANCE_ID
tower_probe_steps = 20
tower_probe_seed = 0
tower_probe_sample_size = 1
random_policy_episodes = 1000
random_policy_seed = 0
linearization_mode_id = "tensor_available_disabled"
request_compatibility_readout = True
```

Required shared artifacts:

- family manifest;
- matrix manifest;
- environment family manifest;
- dependency manifest;
- seed bundle;
- mode manifest;
- linearization manifest;
- timing summary;
- timing segments;
- warnings jsonl;
- external artifacts;
- run index;
- summary json/csv where appropriate.

Required PlateSupport-specific artifacts:

- `instance_summary.json`;
- `graph_summary.json`;
- `state_summary.csv`;
- `action_table.csv`;
- `transition_summary.csv`;
- `shortest_path.csv`;
- `validity_predicate_summary.csv`;
- `support_pattern_summary.csv`;
- `reachability_pattern_summary.csv`;
- `orientation_summary.csv`;
- `position_summary.csv`;
- `outgoing_action_count_summary.csv`;
- `invalid_action_summary.csv`;
- `self_transition_summary.csv`;
- `tower_probe_summary.csv`;
- `random_policy_recon_summary.csv`;
- `training_surface_availability.json`;
- `readout_source.json`;
- `artifact_index.md`.

Completion criteria:

- runner writes all required artifacts under supplied artifact root;
- runner returns structured status and artifact paths.

Stop condition:

- stop if runner would need to create an evaluation-style readout or evaluation
  root.

##### Phase 6.Stage 3.Action 2: Preserve readout discipline

Action:

- ensure readiness `readout_source.json` is explicitly environment-readiness
  source binding, not an evaluation readout source binding;
- include claim boundaries and artifact index paths.

Completion criteria:

- future readers can distinguish environment readiness from evaluation results.

Stop condition:

- stop if existing artifact-table readout protocol is required but incompatible
  with environment-readiness shape.

### Phase 7: Human Environment Docs

#### Phase 7.Stage 1: Implement Docs Writer

##### Phase 7.Stage 1.Action 1: Implement `docs_writer.py`

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/docs_writer.py
```

Required output:

```text
docs/environments/plate_support_5x5_default_v001.md
```

Required sections:

```text
Status
Purpose
Upstream Source
Fixture Roles
State Contract
Action Contract
Transition Contract
Validity Contract
Reward Contract
Terminal And Truncation Contract
Structural Diagnostics
Tower-Depth Diagnostics
Training Surfaces Available Upstream
What This Environment Can Support Later
What This Environment Does Not Yet Claim
Regeneration Command
Artifact Index
```

Completion criteria:

- doc states this is environment readiness, not an evaluation;
- doc includes links to readiness artifacts;
- doc includes explicit non-claims.

Stop condition:

- stop if docs writer would need to invent evaluation results.

##### Phase 7.Stage 1.Action 2: Add docs writer tests

Action:

- create:

```text
tests/environments/plate_support/test_docs_writer.py
```

Assertions:

- doc is written;
- fixture roles are present;
- state/action/reward/terminal contracts are present;
- "not an evaluation result" or equivalent claim-boundary text is present;
- artifact index link is present.

Completion criteria:

- docs writer tests pass.

### Phase 8: CLI Integration

#### Phase 8.Stage 1: Add CLI Parser

##### Phase 8.Stage 1.Action 1: Add `plate-support` command group

Action:

- modify:

```text
src/big_boy_benchmarking/cli/main.py
```

Required command:

```text
plate-support readiness
```

Required arguments:

```text
--artifact-root PATH
--instance-id
--tower-probe-steps
--tower-probe-seed
--tower-probe-sample-size
--random-policy-episodes
--random-policy-seed
--linearization-mode
```

Completion criteria:

- command parses and dispatches to readiness runner.

Stop condition:

- stop if CLI shape conflicts with existing parser conventions.

##### Phase 8.Stage 1.Action 2: Add CLI execution branch

Action:

- modify CLI `main` dispatch to call readiness runner;
- print JSON with:

```text
status
environment_family_id
instance_id
run_family_id
artifact_root
artifact_count
```

Completion criteria:

- CLI returns `0` on success;
- unknown instance id returns nonzero with clear error.

#### Phase 8.Stage 2: Add CLI Tests

##### Phase 8.Stage 2.Action 1: Implement CLI tests

Action:

- create:

```text
tests/environments/plate_support/test_cli_plate_support.py
```

Assertions:

- readiness command runs into `tmp_path`;
- output JSON includes status and instance id;
- expected artifacts exist;
- unknown instance id fails.

Completion criteria:

- CLI tests pass.

### Phase 9: Runner Artifact Tests

#### Phase 9.Stage 1: Test Artifact Completeness

##### Phase 9.Stage 1.Action 1: Implement runner artifact tests

Action:

- create:

```text
tests/environments/plate_support/test_runner_artifacts.py
```

Assertions:

- shared manifests are written;
- PlateSupport-specific tables are written;
- dependency manifest includes state_collapser state;
- linearization manifest exists;
- default linearization label is `tensor_available_disabled`;
- warnings file exists;
- summary json includes claim boundaries;
- no evaluation folder is created by runner.

Completion criteria:

- artifact completeness tests pass.

#### Phase 9.Stage 2: Test Machine Table Contents

##### Phase 9.Stage 2.Action 1: Assert core artifact values

Action:

- extend runner artifact tests to assert:

```text
instance_summary.action_count == 12
graph_summary.valid_state_count == 89
graph_summary.shortest_path_length == 6
tower_probe_summary has default and none rows
random_policy_recon_summary.claim_boundary is nonempty
```

Completion criteria:

- generated artifact values match blueprint expectations.

Stop condition:

- stop if generated values differ in a way that suggests upstream version drift.

### Phase 10: Contract Validation And Smoke Runs

#### Phase 10.Stage 1: Focused Test Runs

##### Phase 10.Stage 1.Action 1: Run PlateSupport tests

Action:

- run:

```bash
uv run pytest tests/environments/plate_support
```

Completion criteria:

- all PlateSupport tests pass.

Stop condition:

- stop on unexpected failure and diagnose before proceeding.

##### Phase 10.Stage 1.Action 2: Run upstream smoke regression tests

Action:

- run:

```bash
uv run pytest tests/upstream/test_smoke_envs.py tests/runners/test_upstream_smoke_runner.py
```

Completion criteria:

- existing upstream smoke tests still pass.

Stop condition:

- stop if PlateSupport changes break upstream smoke behavior.

#### Phase 10.Stage 2: Contract Validation

##### Phase 10.Stage 2.Action 1: Run BBB contract validation

Action:

- run:

```bash
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Completion criteria:

- command returns success.

Stop condition:

- stop if mode/linearization/smoke contract validation fails unexpectedly.

#### Phase 10.Stage 3: Readiness CLI Smoke

##### Phase 10.Stage 3.Action 1: Run readiness command into repo docs path

Action:

- run:

```bash
uv run python -m big_boy_benchmarking.cli plate-support readiness \
  --artifact-root docs/environments/plate_support_5x5_default_v001/readiness/dev_001
```

Completion criteria:

- command succeeds;
- artifacts are written under `docs/environments`;
- no `docs/evaluations/plate_support...` path appears.

Stop condition:

- stop if command writes to the wrong artifact surface.

##### Phase 10.Stage 3.Action 2: Inspect readiness docs and artifact index

Action:

- inspect generated environment doc and artifact index;
- verify docs state environment-readiness/non-evaluation claim boundary.

Completion criteria:

- human docs are readable and linked to machine artifacts.

### Phase 11: Documentation And Root Reference Updates

#### Phase 11.Stage 1: Update Design Implementation Log

##### Phase 11.Stage 1.Action 1: Complete implementation log

Action:

- update implementation log with:
  - files changed;
  - commands run;
  - test results;
  - generated artifact locations;
  - surprises;
  - unresolved follow-up work.

Completion criteria:

- log is complete enough for future engineer continuity.

Stop condition:

- stop if implementation log conflicts with actual git diff.

#### Phase 11.Stage 2: Update Root/Index Docs If Needed

##### Phase 11.Stage 2.Action 1: Update docs index references

Action:

- update root or docs index only where necessary to mention the new PlateSupport
  environment readiness page.

Candidate files:

```text
README.md
docs/README.md
```

Completion criteria:

- repo-level docs do not falsely claim a PlateSupport evaluation exists;
- docs can point to the environment readiness page.

Stop condition:

- stop if root documentation update would imply evaluation results.

### Phase 12: Final Verification And Handoff

#### Phase 12.Stage 1: Final Status Inspection

##### Phase 12.Stage 1.Action 1: Inspect git status and diff summary

Action:

- run:

```bash
git status --short --branch
git diff --stat
```

Completion criteria:

- changed files match expected implementation scope;
- no unrelated files are included.

Stop condition:

- stop if unrelated changes are present and ask how to handle them.

#### Phase 12.Stage 2: Final Test Bundle

##### Phase 12.Stage 2.Action 1: Run final required validation bundle

Action:

- run:

```bash
uv run pytest tests/environments/plate_support tests/upstream/test_smoke_envs.py tests/runners/test_upstream_smoke_runner.py
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Completion criteria:

- all required validations pass.

Stop condition:

- stop if either validation fails.

#### Phase 12.Stage 3: Completion Report

##### Phase 12.Stage 3.Action 1: Report completion

Action:

- report:
  - what was implemented;
  - where artifacts/docs live;
  - validation commands and results;
  - any unresolved questions;
  - next likely design step.

Completion criteria:

- Project Owner can decide whether to commit, review, or proceed to evaluation
  design.

## Global Stop Conditions

Stop immediately if:

- installed upstream `state_collapser` lacks required PlateSupport surfaces;
- upstream counts differ from blueprint assumptions in a meaning-changing way;
- implementation would require editing upstream `state_collapser`;
- implementation would require creating a PlateSupport evaluation folder;
- runner artifact path semantics become ambiguous;
- transition semantics cannot preserve invalid versus valid self-loop
  distinction;
- default-vs-flat tower probe does not behave as expected;
- tests reveal that environment docs cannot satisfy the environment protocol;
- a simplified substitute implementation seems necessary.

## Non-Claim Requirements

Every generated doc or summary must preserve these non-claims:

- this is not a serious evaluation result;
- random-policy reconnaissance is not a baseline comparison;
- tower depth is not tower benefit;
- upstream training-surface availability is not evidence of performance;
- PlateSupport is a candidate for future serious evaluation, not yet a proven
  benchmark win.

## Workplan Completion Definition

This workplan is complete only when:

- every Phase.Stage.Action above is either completed exactly as written or
  explicitly superseded by Project Owner instruction;
- implementation log records every completed or blocked action;
- tests and validation commands have been run and recorded;
- generated docs and artifacts exist in the approved environment-readiness
  surface;
- no evaluation folder has been created.
