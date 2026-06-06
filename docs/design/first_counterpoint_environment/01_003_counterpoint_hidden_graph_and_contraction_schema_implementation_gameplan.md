# Counterpoint Hidden Graph And Contraction Schema Implementation Workplan

Status: initial Phase.Stage.Action implementation blueprint

Created: 2026-05-28

Repository: `/Users/foster/big_boy_benchmarking`

Source blueprint:

- `docs/design/first_counterpoint_environment/01_002_counterpoint_hidden_graph_and_contraction_schema_benchmark_blueprint.md`

Supporting design context:

- `docs/design/first_counterpoint_environment/01_001_counterpoint_environment_design_discussion.md`
- `docs/design/first_infrastructure_slice/01_001_initial_benchmarking_goals_discussion.md`
- `docs/design/first_infrastructure_slice/01_002_state_collapser_read_only_reconnaissance.md`
- `docs/design/first_infrastructure_slice/01_003_benchmark_system_and_artifact_contract_blueprint.md`
- `docs/design/first_infrastructure_slice/01_004_benchmark_system_artifact_contract_implementation_workplan.md`

## Workplan Scope

This workplan implements the first serious counterpoint benchmark family described by the source blueprint:

```text
counterpoint-like finite hidden graph family
+ versioned legality, reward, and label contracts
+ action masks
+ exact tiny graph/path diagnostics
+ schema families as experimental controls
+ artifact-first benchmark outputs
+ direct and tower-ready mode surfaces
```

The central experimental object is not "a music generator."

The central experimental object is a benchmark-owned hidden state/action graph whose underlying RL problem stays fixed while contraction schemas vary.

## Required Execution Discipline

This workplan uses `Phase.Stage.Action` format.

If the Project Owner later approves implementation, implementation must execute actions as written, in order, unless the Project Owner explicitly authorizes a change.

Silent simplification is not allowed.

Silent scope reduction is not allowed.

Silent reordering is not allowed.

Silent substitution of "a small first pass" for a concrete action is not allowed.

If an action cannot be completed exactly as written, the implementation must stop and ask the Project Owner for guidance.

## Prime Directive Compliance Contract

This workplan must be executed under the repository Prime Directive.

Prime Directive source files:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_001.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md
docs/prime_directive/consultant_tricks.md
docs/prime_directive/git_practices.md
```

Operational consequences for this workplan:

1. Do not implement before explicit Project Owner approval.
2. Do not treat creation of this workplan as implementation approval.
3. Before source/test implementation work, create or switch to a dedicated implementation branch.
4. Reconstruct global repo state before edits.
5. Treat this workplan as law during implementation.
6. Re-read each `Phase.Stage.Action` before executing it.
7. Maintain a running implementation log.
8. Stop on ambiguity, surprise, failed baseline, unresolved PO decision, missing prerequisite infrastructure, or need for simplification.
9. Do not edit upstream `/Users/foster/state_collapser`.
10. Do not use git destructively.
11. Do not silently absorb the first infrastructure-slice workplan into this workplan.

The implementation branch should be:

```text
codex/counterpoint-hidden-graph-schema-benchmark
```

unless the Project Owner explicitly names a different branch.

## Current Repo Baseline At Workplan Creation

Observed current package files:

```text
pyproject.toml
README.md
src/big_boy_benchmarking/__init__.py
src/big_boy_benchmarking/_version.py
src/big_boy_benchmarking/state_collapser_probe.py
tests/test_state_collapser_dependency.py
```

Observed current package facts:

- package name in `pyproject.toml`: `big-boy-benchmarking`
- import package: `big_boy_benchmarking`
- upstream dependency pinned to `state-collapser[rl]` at public tag `v0.6.0`
- dev tools include `pytest` and `ruff`
- current source package is still a small dependency probe
- current observed implementation does not yet show the first infrastructure-slice modules

This baseline is only the observed state when this workplan was written. Execution must re-check reality before edits.

## Prerequisite Warning

The source blueprint depends on infrastructure contracts from the first infrastructure slice:

- artifact paths and writers,
- mode registry,
- seed bundles,
- timing segments,
- event rows,
- readout discipline,
- human-facing docs folders,
- and runner skeletons.

At workplan creation time, those modules were not observed in `src/`.

Therefore this workplan contains an explicit prerequisite gate.

If the infrastructure slice has not been implemented by the time this plan is executed, implementation must stop and ask the Project Owner whether to:

- execute `docs/design/first_infrastructure_slice/01_004_benchmark_system_artifact_contract_implementation_workplan.md` first,
- or write an amended combined workplan that explicitly includes the missing prerequisite work.

The implementer must not silently implement infrastructure work as an unnamed side effect of this counterpoint workplan.

## Pause Marker: 2026-05-28 Prerequisite Gate

This workplan was executed through `Phase 0.7.1` on branch:

```text
codex/counterpoint-hidden-graph-schema-benchmark
```

The implementation stopped exactly where this workplan requires it to stop:

```text
Phase 0.7.1: Prerequisite Infrastructure Gate
```

Observed blocker:

```text
The shared benchmark machinery is not yet implemented in source.
```

Missing prerequisite machinery:

- artifact writers;
- mode registry;
- seed bundles;
- metric/event rows;
- timing helpers;
- runner skeletons;
- upstream integration;
- CLI.

Owner decision after the stop:

```text
Pause this counterpoint implementation here.
Design and implement the shared benchmark machinery first.
Return to this workplan afterward.
```

Where to pick back up:

1. Finish the shared benchmark machinery design and implementation in its own approved design/workplan flow.
2. Return to this counterpoint branch or a fresh counterpoint implementation branch, as directed by the Project Owner.
3. Re-open the implementation log:

```text
docs/design/first_counterpoint_environment/01_004_counterpoint_hidden_graph_and_contraction_schema_implementation_log.md
```

4. Re-run `Phase 0.5` global state reconstruction.
5. Re-run `Phase 0.6` baseline validation.
6. Re-run `Phase 0.7.1` prerequisite infrastructure gate.
7. If the infrastructure gate passes, continue at:

```text
Phase 0.8: Execution Method Lock
```

Do not resume at Phase 1 until `Phase 0.7.1` passes in the actual repo state.

## Implementation Non-Goals

Do not implement:

- a new version of old `rl_counterpoint`,
- a human music-quality benchmark,
- a neural learner baseline,
- a hidden history-dependent reward system,
- an unversioned legality system,
- an unversioned reward system,
- an unversioned schema system,
- large-scale final benchmark claims,
- external artifact storage integration,
- a full paper-results matrix,
- or an upstream `state_collapser` change.

Do not edit:

```text
/Users/foster/state_collapser
```

except for read-only inspection or explicitly approved command execution.

## Target End State

When fully executed, this workplan should leave the repo with:

- a benchmark-owned counterpoint environment package;
- versioned instance, state, action, legality, reward, label, mask, and terminal contracts;
- deterministic tiny and small instance specs;
- deterministic legal action enumeration and masks;
- local/action-local reward bundle v001;
- edge label contract v001;
- exact tiny graph enumeration;
- exact tiny path-volume diagnostics;
- mask-density diagnostics;
- reward-fiber diagnostics;
- lift-fiber diagnostics;
- schema manifest contracts;
- empty, random balanced, random unbalanced, structured motion, projection-audit, and bad schema families;
- direct-env runner surfaces;
- tower-ready adapter surfaces gated by verified `state_collapser` API compatibility;
- artifact writers for environment-specific outputs;
- human-facing docs under `docs/environments`, `docs/experiments`, and `docs/methods`;
- tests covering contracts, determinism, diagnostics, schemas, artifact validation, and hot-path readout discipline;
- no serious benchmark performance claim yet.

## Phase 0: Prime Directive Setup, Approval, Branch, And Reality Lock

### Stage 0.1: Rebind Prime Directive Authority

#### Action 0.1.1

Re-read every Prime Directive file:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_001.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md
docs/prime_directive/consultant_tricks.md
docs/prime_directive/git_practices.md
```

Acceptance:

- implementation log explicitly confirms all six files were re-read.
- implementation log records these obligations:
  - explicit PO approval before source/test implementation;
  - dedicated branch before source/test edits;
  - global state reconstruction;
  - workplan-as-law execution;
  - stop on ambiguity, surprise, failed baseline, missing prerequisite, or required simplification.

#### Action 0.1.2

Re-read the source blueprint:

```text
docs/design/first_counterpoint_environment/01_002_counterpoint_hidden_graph_and_contraction_schema_benchmark_blueprint.md
```

Acceptance:

- implementation log confirms the blueprint was re-read.
- implementation log records that the schema-family experiment is the central spine of the work.

#### Action 0.1.3

Re-read the counterpoint discussion source:

```text
docs/design/first_counterpoint_environment/01_001_counterpoint_environment_design_discussion.md
```

Acceptance:

- implementation log confirms the discussion was re-read.
- implementation log records the PO decisions that constrain implementation:
  - all substantive work stays in `big_boy_benchmarking`;
  - family is `n`-voice by design;
  - first reward is local/action-local;
  - masks are shared across comparable modes;
  - old `rl_counterpoint` is conceptual memory, not implementation baseline;
  - contraction schemas are the main experiment knob.

#### Action 0.1.4

Re-read infrastructure design context:

```text
docs/design/first_infrastructure_slice/01_001_initial_benchmarking_goals_discussion.md
docs/design/first_infrastructure_slice/01_002_state_collapser_read_only_reconnaissance.md
docs/design/first_infrastructure_slice/01_003_benchmark_system_and_artifact_contract_blueprint.md
docs/design/first_infrastructure_slice/01_004_benchmark_system_artifact_contract_implementation_workplan.md
```

Acceptance:

- implementation log confirms all four files were re-read.
- implementation log records the inherited artifact, mode, metric, timing, and readout-discipline obligations.

### Stage 0.2: Project Owner Approval Gate

#### Action 0.2.1

Confirm explicit Project Owner approval to implement this exact workplan.

Acceptance:

- approval statement is recorded in the implementation log.

Stop condition:

- if approval is absent or ambiguous, stop and ask.

### Stage 0.3: Dedicated Implementation Branch

#### Action 0.3.1

Inspect current git state:

```bash
git status --short --branch
```

Acceptance:

- current branch is recorded in the implementation log.
- dirty state is recorded in the implementation log.

Stop condition:

- if unrelated dirty files overlap implementation paths, stop and ask.

#### Action 0.3.2

Create or switch to the dedicated implementation branch:

```bash
git checkout -b codex/counterpoint-hidden-graph-schema-benchmark
```

If the branch already exists, use a non-destructive switch command instead.

Acceptance:

- implementation branch is active before source/test edits.
- branch creation or switch is recorded in the implementation log.

Stop condition:

- if branch creation or switch fails, stop and ask.

### Stage 0.4: Create Implementation Log

#### Action 0.4.1

Create:

```text
docs/design/first_counterpoint_environment/01_004_counterpoint_hidden_graph_and_contraction_schema_implementation_log.md
```

The log must include:

- source workplan path;
- source blueprint path;
- approval statement;
- starting git status;
- starting file inventory;
- prerequisite infrastructure check;
- baseline validation results;
- validation command log;
- Phase.Stage.Action completion log;
- PO clarifications;
- stop/resume events.

Acceptance:

- file exists before source/test implementation begins.

### Stage 0.5: Global State Reconstruction

#### Action 0.5.1

Record global repo state:

```bash
pwd
git status --short --branch
rg --files
find . -maxdepth 3 -type d -print
```

Acceptance:

- implementation log records working directory, branch, dirty state, tracked file inventory, and directory shape.

#### Action 0.5.2

Read current package and test files:

```text
pyproject.toml
README.md
src/big_boy_benchmarking/__init__.py
src/big_boy_benchmarking/_version.py
src/big_boy_benchmarking/state_collapser_probe.py
tests/test_state_collapser_dependency.py
```

Acceptance:

- implementation log records current package shape.
- implementation log records current dependency and dev-tool configuration.

#### Action 0.5.3

Record upstream dependency state without editing upstream:

```bash
uv run python -c "import state_collapser; print(state_collapser.__version__)"
```

Acceptance:

- implementation log records installed upstream version.
- no upstream files are edited.

### Stage 0.6: Baseline Validation

#### Action 0.6.1

Run baseline checks:

```bash
uv run pytest
uv run ruff check .
```

Acceptance:

- results are recorded in the implementation log.

Stop condition:

- if baseline checks fail for unrelated existing reasons, stop and ask before proceeding.

### Stage 0.7: Prerequisite Infrastructure Gate

#### Action 0.7.1

Inspect whether the first infrastructure slice exists in source code:

```text
src/big_boy_benchmarking/artifacts/
src/big_boy_benchmarking/modes/
src/big_boy_benchmarking/metrics/
src/big_boy_benchmarking/seeds/
src/big_boy_benchmarking/runners/
src/big_boy_benchmarking/upstream/
src/big_boy_benchmarking/cli/
```

Acceptance:

- implementation log records which infrastructure modules exist.
- implementation log records whether artifact writers, mode registry, seed bundles, event row types, timing segments, and runner skeletons are present.

Stop condition:

- if the infrastructure slice is absent or incomplete, stop and ask the Project Owner whether to execute the infrastructure workplan first or authorize an amended combined workplan.

Resume condition:

- after the shared benchmark machinery exists, re-run this gate against the current repo state.
- if all required infrastructure modules and surfaces are present, record the pass in the implementation log and continue to `Phase 0.8`.
- if any required infrastructure remains absent, stop again before Phase 1.

### Stage 0.8: Execution Method Lock

#### Action 0.8.1

Record in the implementation log:

```text
Implementation will proceed by Phase.Stage.Action order.
Each action text will be re-read before implementation.
No action may be marked complete if implemented only as a weaker substitute.
Any ambiguity, surprise, missing prerequisite, or required simplification triggers a stop.
```

Acceptance:

- implementation log contains the execution method lock before Phase 1 begins.

## Phase 1: PO Decision Lock And Benchmark Identity

### Stage 1.1: Resolve Open Turn Questions

#### Action 1.1.1

Resolve Turn Question 01 from the source blueprint:

```text
family id
```

Default recommendation:

```text
counterpoint_symbolic_v001
```

Acceptance:

- implementation log records the chosen family id.
- if PO chooses a different id, all later file names and manifests use the chosen id.

Stop condition:

- if family id is unresolved, stop and ask.

#### Action 1.1.2

Resolve Turn Question 02 from the source blueprint:

```text
reward direct-image aggregator defaults
```

Default recommendation:

```text
record multiple cheap diagnostics, treat mean and variance as primary
```

Acceptance:

- implementation log records primary and secondary reward aggregator choices.
- reward diagnostics implementation later follows this recorded decision.

Stop condition:

- if aggregator policy is unresolved, stop and ask.

#### Action 1.1.3

Resolve Turn Question 03 from the source blueprint:

```text
projection convention
```

Default recommendation:

```text
all-drop-one posthoc diagnostics, no online projection default until tiny/small evidence
```

Acceptance:

- implementation log records projection convention.
- projection schema implementation later follows this recorded decision.

Stop condition:

- if projection convention is unresolved, stop and ask.

#### Action 1.1.4

Resolve Turn Question 04 from the source blueprint:

```text
first learner staging
```

Default recommendation:

```text
random/masked policy for graph and artifact smoke, then tabular Q for first learning comparison
```

Acceptance:

- implementation log records learner staging.
- runner implementation later follows this recorded decision.

Stop condition:

- if first learner staging is unresolved, stop and ask.

#### Action 1.1.5

Resolve Turn Question 05 from the source blueprint:

```text
first concrete fixture selection method
```

Default recommendation:

```text
use a small enumeration/search utility to hit target state/edge/path-count ranges
```

Acceptance:

- implementation log records fixture selection method.
- tiny/small fixture work later follows this recorded decision.

Stop condition:

- if fixture selection method is unresolved, stop and ask.

### Stage 1.2: Lock Canonical Ids

#### Action 1.2.1

Create a canonical id list in the implementation log.

Required ids:

```text
environment_family_id
legality_contract_id
reward_bundle_id
edge_label_contract_id
initial_state_policy_id
terminal_policy_id
action_mask_policy_id
empty_schema_id
random_balanced_schema_family_id
random_unbalanced_schema_family_id
structured_motion_schema_id
projection_audit_schema_id
bad_schema_id
```

Acceptance:

- all ids are recorded before source implementation.
- ids are stable and versioned.

#### Action 1.2.2

Use the following ids unless PO decisions require different ones:

```text
environment_family_id: counterpoint_symbolic_v001
legality_contract_id: counterpoint_legality_local_v001
reward_bundle_id: counterpoint_reward_local_v001
edge_label_contract_id: counterpoint_edge_labels_local_v001
initial_state_policy_id: counterpoint_initial_states_v001
terminal_policy_id: counterpoint_terminal_horizon_v001
action_mask_policy_id: counterpoint_legal_action_mask_v001
empty_schema_id: counterpoint_empty_schema_v001
random_balanced_schema_family_id: counterpoint_random_balanced_schema_v001
random_unbalanced_schema_family_id: counterpoint_random_unbalanced_schema_v001
structured_motion_schema_id: counterpoint_motion_schema_v001
projection_audit_schema_id: counterpoint_projection_audit_schema_v001
bad_schema_id: counterpoint_bad_schema_v001
```

Acceptance:

- implementation log records final id table.
- no implementation file invents a conflicting id.

### Stage 1.3: Define First Fixture Targets

#### Action 1.3.1

Record target ranges for tiny and small fixture search.

Tiny target:

```text
voice_count: 3
exact graph enumeration required
exact path-volume enumeration required
small enough for unit tests
nonzero branching in most reachable states
nontrivial but inspectable legality constraints
```

Small target:

```text
voice_count: 3
exact or bounded graph diagnostics preferred
learning smoke feasible
schema comparisons feasible
nontrivial path-volume growth
```

Acceptance:

- implementation log records target ranges before fixture search implementation.

#### Action 1.3.2

Record medium/large/stress as reserved, not first-slice claims.

Acceptance:

- implementation log states that first implementation must not make performance claims about medium/large/stress unless explicitly added by later PO-approved workplan.

## Phase 2: Counterpoint Package Skeleton

### Stage 2.1: Create Environment Package

#### Action 2.1.1

Create package directory:

```text
src/big_boy_benchmarking/environments/counterpoint/
```

Acceptance:

- directory exists.
- directory contains `__init__.py`.
- no implementation detail is exported publicly yet except stable constants if needed.

#### Action 2.1.2

Create module skeletons:

```text
src/big_boy_benchmarking/environments/counterpoint/ids.py
src/big_boy_benchmarking/environments/counterpoint/specs.py
src/big_boy_benchmarking/environments/counterpoint/state.py
src/big_boy_benchmarking/environments/counterpoint/actions.py
src/big_boy_benchmarking/environments/counterpoint/legality.py
src/big_boy_benchmarking/environments/counterpoint/rewards.py
src/big_boy_benchmarking/environments/counterpoint/labels.py
src/big_boy_benchmarking/environments/counterpoint/masks.py
src/big_boy_benchmarking/environments/counterpoint/transition.py
src/big_boy_benchmarking/environments/counterpoint/instances.py
src/big_boy_benchmarking/environments/counterpoint/graph.py
src/big_boy_benchmarking/environments/counterpoint/path_volume.py
src/big_boy_benchmarking/environments/counterpoint/schemas.py
src/big_boy_benchmarking/environments/counterpoint/projection.py
src/big_boy_benchmarking/environments/counterpoint/diagnostics.py
src/big_boy_benchmarking/environments/counterpoint/artifacts.py
src/big_boy_benchmarking/environments/counterpoint/runners.py
```

Acceptance:

- modules exist.
- imports are acyclic or intentionally layered.
- `ruff` passes after skeleton creation.

### Stage 2.2: Create Test Package Skeleton

#### Action 2.2.1

Create test directories:

```text
tests/environments/
tests/environments/counterpoint/
```

Acceptance:

- directories exist.
- Python test package conventions match existing repo style.

#### Action 2.2.2

Create initial test file skeletons:

```text
tests/environments/counterpoint/test_ids.py
tests/environments/counterpoint/test_specs.py
tests/environments/counterpoint/test_state_action.py
tests/environments/counterpoint/test_legality.py
tests/environments/counterpoint/test_rewards.py
tests/environments/counterpoint/test_labels.py
tests/environments/counterpoint/test_masks.py
tests/environments/counterpoint/test_transition.py
tests/environments/counterpoint/test_instances.py
tests/environments/counterpoint/test_graph.py
tests/environments/counterpoint/test_path_volume.py
tests/environments/counterpoint/test_schemas.py
tests/environments/counterpoint/test_projection.py
tests/environments/counterpoint/test_artifacts.py
tests/environments/counterpoint/test_runners.py
```

Acceptance:

- tests import successfully.
- empty placeholder tests are not counted as completed contract coverage.

## Phase 3: Versioned Specs, State, And Action Contracts

### Stage 3.1: Id Constants

#### Action 3.1.1

Implement `ids.py` with canonical constants for all locked ids.

Acceptance:

- every id from Phase 1 appears exactly once as a canonical constant.
- no module duplicates string ids by hand when it can import the constant.
- tests verify id values.

### Stage 3.2: Instance Spec

#### Action 3.2.1

Implement `CounterpointInstanceSpec` in `specs.py`.

Required fields:

```text
environment_family_id
environment_instance_id
family_version
voice_count
pitch_min
pitch_max
tonic_pitch_class
measure_size
horizon_steps
max_step_size
allow_stationary_voice
require_strict_voice_order
allowed_adjacent_interval_classes
allowed_outer_interval_classes
allowed_root_interval_classes
forbidden_parallel_interval_classes
max_outer_span
legality_contract_id
reward_bundle_id
edge_label_contract_id
initial_state_policy_id
terminal_policy_id
action_mask_policy_id
```

Acceptance:

- spec is immutable or treated as immutable.
- spec serializes to JSON-safe dict.
- spec validation rejects invalid pitch bands, voice counts, beat sizes, horizons, and interval classes.
- tests cover valid and invalid specs.

#### Action 3.2.2

Implement spec validation errors with clear messages.

Acceptance:

- validation failures identify the bad field.
- validation does not depend on ambient working directory, environment variables, or global random state.

### Stage 3.3: State Contract

#### Action 3.3.1

Implement `CounterpointState` in `state.py`.

Required shape:

```text
pitches: tuple[int, ...]
beat_index: int
```

Acceptance:

- state serializes to JSON-safe dict or tuple representation.
- state is hashable.
- state validation checks voice count, pitch band, strict order, and beat index when given a spec.
- tests cover serialization, hashing, and validation.

### Stage 3.4: Action Contract

#### Action 3.4.1

Implement `CounterpointAction` in `actions.py`.

Required shape:

```text
deltas: tuple[int, ...]
```

Acceptance:

- action serializes to JSON-safe representation.
- action is hashable.
- action validation checks voice count and delta bounds.
- stationary action handling follows `allow_stationary_voice`.
- tests cover valid and invalid actions.

#### Action 3.4.2

Implement deterministic raw action enumeration.

Acceptance:

- enumeration order is stable.
- raw action count matches the action lattice implied by `max_step_size`, `voice_count`, and stationary policy.
- tests cover counts for at least two voice counts and two step sizes.

## Phase 4: Legality, Transition, Rewards, Labels, And Masks

### Stage 4.1: Legality Contract

#### Action 4.1.1

Implement node legality in `legality.py`.

Required checks:

- pitch band;
- strict voice order when enabled;
- adjacent interval class membership;
- outer interval class membership;
- max outer span;
- root/tonic interval class when enabled;
- beat index validity.

Acceptance:

- function returns structured legality result, not only a bare boolean.
- structured result includes failure reasons.
- tests cover each required check.

#### Action 4.1.2

Implement edge legality in `legality.py`.

Required checks:

- action delta bounds;
- stationary voice policy;
- candidate node legality;
- forbidden parallel interval classes;
- local movement-shape constraints if represented in spec.

Acceptance:

- function returns structured legality result with failure reasons.
- no hidden path history is read.
- tests cover each required edge check.

### Stage 4.2: Transition Function

#### Action 4.2.1

Implement deterministic transition candidate construction in `transition.py`.

Acceptance:

- applying an action to a state produces candidate next pitches and next beat index.
- beat index advances modulo `measure_size`.
- tests cover pitch update and beat wrap.

#### Action 4.2.2

Implement legal transition evaluation in `transition.py`.

Acceptance:

- legal transition returns next state, reward result, labels, terminal/truncation flags, and legality metadata.
- illegal transition returns structured failure metadata for diagnostic modes.
- primary masked modes can avoid illegal transitions entirely.
- tests cover legal and illegal cases.

### Stage 4.3: Reward Bundle v001

#### Action 4.3.1

Implement reward term specification types in `rewards.py`.

Required fields:

```text
reward_term_id
reward_term_version
weight
enabled
input_scope
locality_class
output_range
diagnostic_fields
```

Acceptance:

- reward term specs serialize to JSON-safe dicts.
- first-version scopes are limited to current state, action, next state, beat index, and instance parameters.
- tests verify no term declares path-history scope in v001.

#### Action 4.3.2

Implement `counterpoint_reward_local_v001`.

Required first terms:

- valid transition bonus;
- adjacent interval preference;
- outer interval preference;
- movement-size preference or leap penalty;
- motion-shape preference;
- range comfort penalty;
- beat-phase local preference if enabled by spec;
- terminal completion bonus if terminal predicate is enabled.

Acceptance:

- each term has stable id and version.
- reward output includes total reward and term-level diagnostics.
- reward computation is deterministic.
- reward computation reads no hidden history.
- tests cover each term and weighted bundle composition.

### Stage 4.4: Edge Labels v001

#### Action 4.4.1

Implement edge label emission in `labels.py`.

Required label families:

- beat phase before transition;
- beat phase after transition;
- per-voice delta;
- per-voice movement class;
- global motion direction pattern;
- adjacent interval classes before;
- adjacent interval classes after;
- outer interval class before;
- outer interval class after;
- interval change classes;
- root interval class before;
- root interval class after;
- forbidden-parallel check result;
- max-span bucket;
- terminal candidate marker.

Acceptance:

- labels are deterministic and JSON-safe.
- labels are not reward outcomes.
- tests cover representative transitions.

#### Action 4.4.2

Implement movement class thresholds.

Acceptance:

- thresholds are versioned by the edge-label contract.
- tests cover `down_leap`, `down_step`, `stationary`, `up_step`, and `up_leap`.

### Stage 4.5: Action Masks

#### Action 4.5.1

Implement legal action mask construction in `masks.py`.

Acceptance:

- mask uses the active legality contract.
- mask is deterministic.
- mask exposes legal actions in the same order as raw action enumeration.
- tests cover mask count, mask order, and mask consistency with edge legality.

#### Action 4.5.2

Implement mask-density diagnostics.

Acceptance:

- diagnostics include raw action count, legal action count, mask density, dead-end flag, and single-action flag.
- tests cover at least one dead-end or near-dead-end fixture if feasible.

## Phase 5: Instances, Fixture Search, And Hidden Graphs

### Stage 5.1: Instance Registry

#### Action 5.1.1

Implement deterministic instance constructors in `instances.py`.

Required constructors:

```text
tiny_candidate_specs()
small_candidate_specs()
default_tiny_spec()
default_small_spec()
```

Acceptance:

- constructors return validated `CounterpointInstanceSpec` objects.
- default ids match Phase 1 id policy.
- tests verify constructors are deterministic.

### Stage 5.2: Fixture Search

#### Action 5.2.1

Implement fixture search utility if Phase 1 selected enumeration-based fixture choice.

Suggested location:

```text
src/big_boy_benchmarking/environments/counterpoint/fixture_search.py
```

Acceptance:

- search evaluates candidate tiny and small specs.
- search records reachable state count, edge count, branch-factor summary, dead-end count, and exact path-volume feasibility.
- search has deterministic ordering.
- tests cover search on a small candidate set.

Stop condition:

- if hand-picked fixture selection was chosen instead, do not implement search utility unless PO authorizes it.

#### Action 5.2.2

Select `default_tiny_spec()` using recorded Phase 1 method.

Acceptance:

- selected tiny fixture satisfies exact graph and path-volume feasibility.
- implementation log records selected parameters and diagnostic counts.

#### Action 5.2.3

Select `default_small_spec()` using recorded Phase 1 method.

Acceptance:

- selected small fixture satisfies first learning-smoke feasibility.
- implementation log records selected parameters and diagnostic counts.

### Stage 5.3: Hidden Graph Enumeration

#### Action 5.3.1

Implement exact reachable graph enumeration in `graph.py`.

Acceptance:

- graph enumeration starts from the active initial state policy.
- graph enumeration follows legal masked actions.
- graph nodes are `CounterpointState`.
- graph edges include action, next state, reward result, and labels.
- enumeration is deterministic.
- tests cover tiny exact state and edge counts.

#### Action 5.3.2

Implement graph summary diagnostics.

Required fields:

- state count;
- edge count;
- reachable start count;
- dead-end count;
- branch-factor min/mean/max;
- mask-density min/mean/max;
- horizon setting;
- legality contract id;
- reward bundle id;
- edge label contract id.

Acceptance:

- summary serializes to JSON-safe dict.
- tests cover summary consistency.

### Stage 5.4: Path-Volume Diagnostics

#### Action 5.4.1

Implement exact path-volume counting for tiny instances in `path_volume.py`.

Acceptance:

- exact count supports paths of exactly length `K`.
- exact count supports paths up to length `K`.
- count uses legal graph transitions.
- tests cover a tiny manually understood fixture.

#### Action 5.4.2

Implement sampled path-volume estimates for larger instances.

Acceptance:

- sampling is deterministic given `diagnostic_sampling_seed`.
- artifact output states that the value is sampled, not exact.
- tests verify deterministic sampling.

#### Action 5.4.3

Implement policy-effective path-volume hook.

Acceptance:

- interface records policy id and sampling seed.
- random legal policy can be used for first implementation.
- learner-policy checkpoints are reserved for later but interface does not preclude them.
- tests cover random legal policy sampling.

## Phase 6: Environment-Specific Artifact Contracts

### Stage 6.1: Manifest Types

#### Action 6.1.1

Implement environment-specific manifest builders in `artifacts.py`.

Required manifests:

```text
environment_family_manifest.json
environment_instance_manifest.json
legality_manifest.json
reward_bundle_manifest.json
edge_label_manifest.json
initial_state_manifest.json
action_mask_manifest.json
```

Acceptance:

- each manifest serializes to JSON-safe dict.
- each manifest includes relevant ids from Phase 1.
- tests verify required keys.

#### Action 6.1.2

Implement graph and path artifact builders.

Required artifacts:

```text
graph_summary.json
mask_density.csv
path_volume_summary.json
path_volume_samples.jsonl
```

Acceptance:

- writers use infrastructure artifact utilities if available.
- writers do not infer output roots from ambient current working directory.
- tests write to explicit temporary roots.

### Stage 6.2: Schema and Diagnostic Artifacts

#### Action 6.2.1

Implement schema artifact builders.

Required artifacts:

```text
schema_manifest.json
schema_diagnostics.jsonl
quotient_summary.json
quotient_cells.csv
address_traces.jsonl
```

Acceptance:

- schema artifacts are explicit about schema id, schema seed, environment instance id, and construction method.
- tests verify JSON/CSV shape for empty and random schemas.

#### Action 6.2.2

Implement lift and reward diagnostic artifact builders.

Required artifacts:

```text
lift_fiber_summary.csv
lift_attempts.jsonl
reward_fiber_variance.csv
reward_term_diagnostics.jsonl
```

Acceptance:

- artifacts can represent no-data cases without crashing.
- no-data cases follow the Prime Directive diagnostic continuity amendment if global infra defines one.
- tests cover no-data and small-data cases.

## Phase 7: Contraction Schema Families

### Stage 7.1: Schema Contract Types

#### Action 7.1.1

Implement schema spec and manifest types in `schemas.py`.

Required fields:

```text
schema_id
schema_family_id
schema_version
environment_family_id
environment_instance_id
schema_seed
construction_method
source_label_families
state_partition_description
action_partition_description
expected_tower_depth
expected_compression_target
leakage_risk_statement
intended_role
online_eligible
diagnostic_only
```

Acceptance:

- schemas serialize to JSON-safe dicts.
- schema validation rejects missing leakage-risk statement.
- tests cover serialization and validation.

### Stage 7.2: Empty Schema

#### Action 7.2.1

Implement `counterpoint_empty_schema_v001`.

Acceptance:

- schema has intended role `baseline_empty`.
- schema is deterministic.
- schema creates no fake semantic contraction.
- tests verify manifest and construction output.

### Stage 7.3: Random Balanced Schema

#### Action 7.3.1

Implement random balanced schema construction.

Acceptance:

- construction is deterministic given `schema_seed`.
- construction does not use reward labels, terminal outcomes, learned values, or future information.
- construction targets balanced cell sizes where feasible.
- manifest records target compression.
- tests verify deterministic same-seed output and different output for different seeds.

### Stage 7.4: Random Unbalanced Schema

#### Action 7.4.1

Implement random unbalanced schema construction.

Acceptance:

- construction is deterministic given `schema_seed`.
- construction intentionally creates giant-cell or singleton-heavy pathology.
- manifest marks intended role as control/pathology.
- tests verify that cell-size distribution differs from balanced schema.

### Stage 7.5: Structured Motion Schema

#### Action 7.5.1

Implement `counterpoint_motion_schema_v001`.

Source labels may include:

- direction pattern;
- per-voice step/leap movement class;
- adjacent interval class before and after;
- outer interval class before and after;
- beat phase;
- span bucket.

Acceptance:

- schema uses only labels from the versioned edge-label contract.
- schema does not read reward outcomes.
- schema does not read future episode outcome.
- manifest records all source label families.
- tests verify nontrivial grouping on tiny graph.

### Stage 7.6: Projection-Audit Schema

#### Action 7.6.1

Implement projection-audit schema according to Phase 1 projection decision.

Acceptance:

- projection convention is explicit in manifest.
- diagnostic-only status is recorded if online eligibility is not approved.
- tests verify projected state keys for representative `n`-voice states.

Stop condition:

- if Phase 1 projection decision was all-drop-one diagnostics but no single online schema, do not create an online projection schema without PO approval.

### Stage 7.7: Bad or Adversarial Schema

#### Action 7.7.1

Implement `counterpoint_bad_schema_v001`.

Acceptance:

- manifest marks intended role as `bad_control` or `adversarial_diagnostic`.
- construction is explicit about whether it uses reward diagnostics.
- if it uses reward diagnostics, it is not marked as fair online-eligible.
- tests verify high reward variance or another declared pathology on tiny graph.

## Phase 8: Projection, Reward-Fiber, Lift-Fiber, And Address Diagnostics

### Stage 8.1: Projection Diagnostics

#### Action 8.1.1

Implement projection diagnostic functions in `projection.py`.

Required diagnostics:

- projected state key;
- projected transition key;
- fine states per projected state;
- fine transitions per projected transition;
- projection cell size distribution.

Acceptance:

- diagnostics follow Phase 1 projection convention.
- diagnostics are deterministic.
- tests cover `n=3` and at least one reserved `n=4` case.

### Stage 8.2: Reward-Fiber Diagnostics

#### Action 8.2.1

Implement reward-fiber variance diagnostics in `diagnostics.py`.

Required fields:

- schema id;
- quotient or schema cell id;
- fine transition count;
- reward mean;
- reward variance;
- reward min;
- reward max;
- term-level variance where feasible.

Acceptance:

- diagnostics follow Phase 1 reward aggregator policy.
- tests verify zero variance for uniform cells and nonzero variance for mixed cells.

### Stage 8.3: Lift-Fiber Diagnostics

#### Action 8.3.1

Implement lift-fiber size and entropy diagnostics.

Required fields:

- cell id or coarse address;
- fine candidate count;
- entropy;
- valid lift count;
- failed lift count;
- failed lift reason counts.

Acceptance:

- diagnostics can operate on tiny graph exactly.
- diagnostics can operate on sampled larger data.
- tests cover empty/no-data case and nonempty case.

### Stage 8.4: Balanced Addressability Diagnostics

#### Action 8.4.1

Implement balanced addressability diagnostics.

Required fields:

- address count;
- address frequency distribution;
- largest cell share;
- singleton cell share;
- effective number of cells;
- entropy;
- path coverage by address if path samples are available.

Acceptance:

- diagnostics distinguish balanced random schema from unbalanced random schema on a tiny or synthetic graph.
- tests cover expected distinction.

## Phase 9: Runner Surfaces And State Collapser Integration

### Stage 9.1: Direct Environment Runner

#### Action 9.1.1

Implement a direct masked random-policy runner in `runners.py`.

Acceptance:

- runner accepts explicit instance spec, seed bundle, artifact root, horizon, and policy id.
- runner does not infer artifact root from current working directory.
- runner emits episode rows and summary artifacts through infrastructure writers.
- tests verify deterministic output with fixed seed.

#### Action 9.1.2

Implement direct tabular Q runner only if Phase 1 learner staging authorized it.

Acceptance:

- learner id is stable.
- learner uses legal action masks.
- learner seed is separated from environment and schema seeds.
- runner emits episode returns, success/completion metrics if defined, and timing segments.
- tests cover deterministic smoke behavior.

Stop condition:

- if tabular Q implementation would require unapproved design choices, stop and ask.

### Stage 9.2: Upstream API Reconnaissance

#### Action 9.2.1

Inspect installed `state_collapser` APIs needed for tower integration.

Required surfaces to verify:

- hidden graph or environment adapter expectations;
- partition schema construction expectations;
- `PartitionTower`;
- `RewardAggregator`;
- training action-decision surfaces;
- compatibility readout methods to avoid on hot path.

Acceptance:

- implementation log records verified import paths and call signatures.
- no upstream files are edited.

Stop condition:

- if installed API does not match the planned adapter, stop and ask before implementing tower adapter.

### Stage 9.3: Tower Adapter Surface

#### Action 9.3.1

Implement tower-ready adapter surface for counterpoint hidden graph.

Acceptance:

- adapter is compatible with verified `state_collapser` API.
- adapter exposes versioned state/action/edge labels.
- adapter can be instantiated on tiny graph.
- adapter does not call rich compatibility readouts during default online steps.
- tests monkeypatch readout methods to verify default hot-path discipline.

#### Action 9.3.2

Implement tower empty-schema smoke runner.

Acceptance:

- runner uses `counterpoint_empty_schema_v001`.
- runner writes mode manifest and timing segments.
- runner is clearly marked smoke, not benchmark evidence.
- tests verify artifacts and readout discipline.

#### Action 9.3.3

Implement tower nonempty-schema smoke runner for structured motion and random balanced schemas.

Acceptance:

- runner accepts explicit schema id and schema seed.
- runner writes schema manifest.
- runner writes quotient, reward-fiber, and lift-fiber diagnostics where available.
- tests verify one structured and one random schema smoke on tiny fixture.

## Phase 10: CLI Or Script Entry Points

### Stage 10.1: Fixture Search Entry

#### Action 10.1.1

Create a CLI or script entry for fixture search if fixture search was authorized.

Suggested command shape:

```text
python -m big_boy_benchmarking.cli counterpoint search-fixtures ...
```

Acceptance:

- command accepts explicit output root.
- command writes fixture-search artifacts.
- command handles no candidate found as a clear nonzero or no-data outcome according to repo diagnostic policy.
- tests cover parser or callable entry surface.

### Stage 10.2: Diagnostics Entry

#### Action 10.2.1

Create a CLI or script entry for tiny graph diagnostics.

Suggested command shape:

```text
python -m big_boy_benchmarking.cli counterpoint graph-diagnostics ...
```

Acceptance:

- command runs tiny graph enumeration and path-volume diagnostics.
- command writes environment manifests, graph summary, mask density, and path-volume summary.
- command accepts explicit artifact root.
- smoke test covers command or callable runner.

### Stage 10.3: Runner Entry

#### Action 10.3.1

Create a CLI or script entry for direct masked random-policy smoke.

Acceptance:

- command accepts explicit instance id, seed, horizon, and artifact root.
- command writes run artifacts.
- tests cover command or callable runner.

#### Action 10.3.2

Create CLI or script entries for tower smoke only after Stage 9 tower adapter acceptance passes.

Acceptance:

- command accepts explicit schema id and schema seed.
- command writes mode and schema artifacts.
- command preserves hot-path readout discipline.

Stop condition:

- if tower adapter is blocked, do not create fake tower CLI entries.

## Phase 11: Human-Facing Documentation

### Stage 11.1: Environment Doc

#### Action 11.1.1

Create or update:

```text
docs/environments/counterpoint_symbolic_v001.md
```

If Phase 1 chose a different family id, use that id in the filename.

Acceptance:

- doc records family id.
- doc describes hidden geometry.
- doc defines state/action/transition.
- doc defines legality and reward contracts.
- doc explains why flat search is wasteful.
- doc explains quotient/projection hypothesis.
- doc lists scale ladder.
- doc lists schema candidates and leakage risks.
- doc lists artifact fields.
- doc states artifacts are source of truth.

### Stage 11.2: Method Docs

#### Action 11.2.1

Create or update:

```text
docs/methods/counterpoint_schema_diagnostics.md
docs/methods/counterpoint_path_volume.md
docs/methods/counterpoint_reward_fibers.md
docs/methods/counterpoint_lift_fibers.md
```

Acceptance:

- each method doc links back to the source blueprint and this workplan.
- each method doc distinguishes exact, sampled, online, and posthoc diagnostics.

### Stage 11.3: Experiment Doc

#### Action 11.3.1

Create or update:

```text
docs/experiments/counterpoint_symbolic_v001_first_matrix.md
```

If Phase 1 chose a different family id, use that id in the filename.

Acceptance:

- doc lists first matrix arms:
  - direct masked random or direct tabular;
  - tower empty schema;
  - tower random balanced schema;
  - tower structured motion schema;
  - reserved random unbalanced;
  - reserved projection audit;
  - reserved bad/adversarial schema.
- doc states which arms are implemented and which are reserved.
- doc does not claim final results.

### Stage 11.4: Results Stub

#### Action 11.4.1

Create or update:

```text
docs/results/counterpoint_symbolic_v001_first_smoke.md
```

If Phase 1 chose a different family id, use that id in the filename.

Acceptance:

- doc is a results stub only until real artifacts exist.
- doc lists artifact bundle locations when smoke runs are produced.
- doc states no serious benchmark claim yet.

## Phase 12: Contract And Regression Tests

### Stage 12.1: Spec, State, Action Tests

#### Action 12.1.1

Complete tests for ids, specs, states, and actions.

Acceptance:

- valid specs pass.
- invalid specs fail with clear errors.
- state/action serialization is stable.
- action enumeration counts are correct.

### Stage 12.2: Legality, Transition, Reward, Label, Mask Tests

#### Action 12.2.1

Complete tests for legality, transition, rewards, labels, and masks.

Acceptance:

- each node legality check has a direct test.
- each edge legality check has a direct test.
- reward bundle emits term diagnostics.
- labels are deterministic.
- masks match legality results.

### Stage 12.3: Graph And Path Tests

#### Action 12.3.1

Complete tests for graph enumeration and path-volume diagnostics.

Acceptance:

- tiny graph exact state/edge counts are stable.
- exact path-volume counts are stable.
- sampled path-volume is deterministic by seed.
- no-data cases do not crash diagnostic writers.

### Stage 12.4: Schema Tests

#### Action 12.4.1

Complete tests for schema families.

Acceptance:

- empty schema is deterministic.
- random balanced schema is deterministic by seed.
- random unbalanced schema creates declared imbalance.
- structured motion schema creates nontrivial grouping.
- projection audit follows Phase 1 convention.
- bad schema exhibits declared pathology.
- all schema manifests include leakage-risk statements.

### Stage 12.5: Artifact Tests

#### Action 12.5.1

Complete tests for environment-specific artifacts.

Acceptance:

- all required manifests serialize.
- JSONL writers emit valid lines.
- CSV writers emit stable headers.
- artifact paths use explicit roots.
- artifact tests do not rely on ambient current working directory.

### Stage 12.6: Runner And Readout Discipline Tests

#### Action 12.6.1

Complete direct runner smoke tests.

Acceptance:

- fixed seeds produce stable smoke outputs.
- timing segments are recorded.
- summaries include mode, instance, seed, and artifact ids.

#### Action 12.6.2

Complete tower runner smoke tests if tower adapter was implemented.

Acceptance:

- empty schema tower smoke runs.
- structured motion tower smoke runs.
- random balanced tower smoke runs.
- monkeypatch tests prove default hot path does not call compatibility readout or morphism readout methods.

Stop condition:

- if tower adapter was blocked by upstream API mismatch, record blocker and do not fake passing tower tests.

## Phase 13: Validation Runs And Artifact Inspection

### Stage 13.1: Full Test Suite

#### Action 13.1.1

Run:

```bash
uv run pytest
uv run ruff check .
```

Acceptance:

- both commands pass.
- implementation log records command outputs or summarized results.

Stop condition:

- if any failure appears that was not predicted by the current action, stop and perform Prime Directive reality-break recovery.

### Stage 13.2: Tiny Diagnostics Smoke

#### Action 13.2.1

Run tiny graph diagnostics through the approved entry surface.

Acceptance:

- manifests are written.
- graph summary is written.
- mask-density artifact is written.
- path-volume summary is written.
- exact counts are recorded in implementation log.
- no benchmark performance claim is made.

### Stage 13.3: Direct Runner Smoke

#### Action 13.3.1

Run direct masked random or direct tabular smoke according to Phase 1 learner staging.

Acceptance:

- run artifacts are written.
- episode summary is written.
- timing segments are written.
- seed bundle is recorded.
- implementation log records artifact root.

### Stage 13.4: Schema Smoke

#### Action 13.4.1

Run schema diagnostics on tiny fixture for:

- empty schema;
- random balanced schema;
- structured motion schema;
- random unbalanced schema;
- bad schema;
- projection audit schema if authorized.

Acceptance:

- schema manifests are written.
- quotient summaries are written where applicable.
- reward-fiber diagnostics are written.
- lift-fiber diagnostics are written.
- balanced addressability diagnostics are written.

### Stage 13.5: Tower Smoke

#### Action 13.5.1

Run tower smoke only if Stage 9 tower adapter and tests passed.

Acceptance:

- empty-schema tower smoke completes.
- nonempty structured-motion tower smoke completes.
- random-balanced tower smoke completes.
- readout discipline flags are recorded.
- timing segments distinguish online and posthoc cost.

Stop condition:

- if tower integration is not ready, record that tower smoke is blocked and stop before claiming completion of tower phases.

## Phase 14: Completion Review

### Stage 14.1: Workplan Compliance Audit

#### Action 14.1.1

Review every Phase.Stage.Action item in this workplan against the implementation log.

Acceptance:

- each item is marked one of:
  - completed exactly as specified;
  - blocked pending PO guidance;
  - not started;
  - explicitly superseded by PO-approved amendment.
- no item is marked complete if implemented only as a weaker substitute.

### Stage 14.2: Artifact Contract Audit

#### Action 14.2.1

Verify required artifact families exist for completed modes.

Acceptance:

- environment manifests exist.
- graph/path diagnostics exist.
- schema manifests exist for completed schemas.
- reward/lift diagnostics exist where schemas were run.
- learning/run artifacts exist for completed runners.
- no-data artifacts are explicit rather than crashes.

### Stage 14.3: Documentation Audit

#### Action 14.3.1

Verify human-facing docs match implemented reality.

Acceptance:

- environment doc does not claim unimplemented features.
- experiment doc separates implemented arms from reserved arms.
- results stub links only to real artifacts.
- method docs match diagnostics actually implemented.

### Stage 14.4: Final Validation

#### Action 14.4.1

Run final validation:

```bash
uv run pytest
uv run ruff check .
git status --short --branch
```

Acceptance:

- validation results are recorded in implementation log.
- final dirty state is recorded.
- implementation status is ready for PO review.

### Stage 14.5: Completion Report

#### Action 14.5.1

Report completion to the Project Owner.

Required report contents:

- branch name;
- completed phases;
- blocked or deferred phases;
- validation results;
- artifact roots produced;
- exact files changed;
- any PO decisions used;
- any unresolved risks.

Acceptance:

- report distinguishes completed exact actions from blocked or deferred actions.
- report does not claim serious benchmark results unless explicitly produced by this workplan.

## Mandatory Stop Conditions

Stop and ask the Project Owner if:

- explicit implementation approval is absent;
- current git state is unclear;
- branch creation or switch fails;
- first infrastructure slice is absent or incomplete;
- any PO turn question remains unresolved;
- a source action would require editing `/Users/foster/state_collapser`;
- installed `state_collapser` API does not match planned adapter;
- a test baseline fails before implementation;
- a new error appears that was not predicted by the active action;
- an action would require a design decision not already authorized;
- an action would require simplifying, approximating, or substituting the plan;
- exact tiny graph/path diagnostics are infeasible under chosen fixture;
- tower integration would require fake or placeholder completion;
- artifact writers would need ambient path inference;
- default online path would call rich compatibility or morphism readouts.

## Authorized Simplifications

None.

Any simplification must be explicitly authorized by the Project Owner and recorded in the implementation log.

## Reserved Future Work

The following are intentionally not part of this workplan unless separately approved:

- medium/large/stress benchmark result claims;
- deep RL learners;
- full exploit/explore tower controller;
- fiber-conditioned substages;
- external artifact storage;
- paper-style result tables;
- upstream `state_collapser` changes;
- import of old `rl_counterpoint` code.

## Workplan Close

This document converts the counterpoint hidden-graph and contraction-schema benchmark blueprint into an executable Phase.Stage.Action implementation plan.

It should be treated as law only after explicit Project Owner approval to execute it.

Until then, it is a design artifact.
