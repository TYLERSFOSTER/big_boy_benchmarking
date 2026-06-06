# PlateSupport BBB Environment Build Blueprint

## Status

Status: initial environment-build blueprint.

This is a blueprint, not an implementation workplan.

The implementation workplan should be generated next, in Phase.Stage.Action
form, after Project Owner review or approval.

Expected next files:

```text
docs/design/first_plate_support_environment/01_002_plate_support_environment_bbb_build_implementation_workplan.md
docs/design/first_plate_support_environment/01_003_plate_support_environment_bbb_build_implementation_log.md
```

## Source Inputs

This blueprint is derived from:

- `docs/design/first_plate_support_environment/README.md`;
- `docs/design/first_plate_support_environment/design_discussion.md`;
- `docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md`;
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`;
- local BBB shared benchmark machinery under `src/big_boy_benchmarking`;
- upstream `state_collapser.examples.plate_support_env`;
- upstream PlateSupport tests under `/Users/foster/state_collapser/tests/examples`;
- upstream `state_collapser.examples.tower_depth_probe`;
- BBB upstream smoke adapter and runner.

## Attribution Discipline

This blueprint does not invent Project Owner turns.

Project Owner supplied the following design direction in conversation and in the
design discussion:

- move on from counterpoint for now;
- use a more robotics-based constrained example;
- prefer the existing plate examples as the natural next candidate;
- find an environment where training need is large enough to measure clearly;
- avoid treating PlateSupport as merely a counterpoint-shaped package;
- start an environment-build design area now;
- do not create an evaluation folder yet.

Codex supplied:

- the upstream reconnaissance;
- structural facts measured from the installed upstream package;
- the proposed BBB package shape;
- the proposed artifact surfaces;
- the proposed CLI/docs/test design;
- the open questions and recommendations below.

Any section labeled `Consultant Recommendation` is Codex-authored and should not
be treated as a Project Owner decision unless the Project Owner later approves
it.

## Executive Summary

BBB should build a first-class PlateSupport environment family that wraps the
already-existing upstream `state_collapser.examples.plate_support_env` surface
and emits BBB-native environment-readiness artifacts.

This build should not create a serious learning evaluation yet.

The purpose of this build is to make PlateSupport ready for later serious
evaluation by defining:

- stable environment ids and fixture roles;
- state/action/transition/reward contracts in BBB language;
- structural diagnostics for the constrained feasible graph;
- tower-depth diagnostics for default schema versus flat schema;
- runtime/readout/linearization metadata;
- human-readable environment docs under `docs/environments`;
- tests that prevent later evaluations from inferring intent only from code.

The guiding motivation is that counterpoint's recent positive signal was real
but tiny. PlateSupport is a better next candidate because it is a discrete
constrained robotics-style problem where naive action choice visibly struggles.

## Problem Statement

BBB currently has two relevant facts in tension:

1. PlateSupport exists upstream in `state_collapser` as a mature constrained
   reference environment.
2. BBB only knows PlateSupport as an upstream smoke id, not as a first-class
   environment family with environment-level diagnostics, contracts, docs, and
   artifact surfaces.

The existing BBB upstream smoke support proves:

- import works;
- a runtime can be constructed;
- one reset/step can be executed;
- readout/timing/linearization discipline can be recorded.

It does not prove:

- PlateSupport is structurally appropriate for serious benchmarking;
- BBB can explain the task to future engineers;
- BBB can record PlateSupport-specific feasibility and tower diagnostics;
- later evaluations can rely on stable PlateSupport fixture ids;
- later human-readable reports can distinguish environment sanity from method
  performance.

The build must close that gap.

## Primary Goal

Create a BBB-side PlateSupport environment family surface that can support
future serious evaluations.

The build should allow a future engineer to run an environment-level diagnostic
command and answer:

- what PlateSupport is;
- which upstream package/version it came from;
- what fixed instance/fixture was used;
- what the state and action spaces mean;
- what counts as a legal transition;
- what invalid actions do;
- what reward means;
- whether the start/goal pair is nontrivial;
- whether the hidden feasible graph is connected/reachable from start;
- how much invalid/self-loop pressure exists;
- whether the default schema creates non-flat tower structure;
- whether the explicit flat schema stays flat;
- what cannot be claimed yet.

## Explicit Non-Goals

This build must not:

- design a serious learning evaluation;
- run flat-versus-tower learning comparisons as a claim-bearing result;
- create `docs/evaluations/...` for PlateSupport;
- create a new upstream PlateSupport variant;
- modify upstream `state_collapser`;
- treat tower depth as proof of learning benefit;
- treat the existing BBB upstream smoke as a serious benchmark;
- copy counterpoint-specific threshold-frontier or schema-comparison logic;
- assert that PlateSupport already demonstrates tower improvement inside BBB.

## Relationship To Benchmark Workflow Protocol

The repo's benchmark workflow is:

```text
1. Construct an environment.
2. Construct evaluations for that environment.
3. Process run artifacts into repo-side human-readable readouts.
```

This blueprint only covers step 1.

It should satisfy the environment-construction protocol by providing:

- stable ids;
- fixture policy;
- state/action/transition contract;
- reward and claim contract;
- diagnostics;
- structural limit notes;
- artifact support;
- human docs seed;
- tests.

## Why PlateSupport Is The Right Next Candidate

PlateSupport is robotics-flavored while remaining inspectable.

The upstream state is:

```text
PlateSupportState(x_idx, y_idx, theta_idx, e1, e2, e3)
```

Conceptually:

- `(x_idx, y_idx)` is plate center position on a finite grid;
- `theta_idx` is plate orientation;
- `e1`, `e2`, `e3` are arm extension/support states;
- fixed support sockets must remain in bounds;
- engaged arms must be able to reach their sockets;
- the support pattern must satisfy stability rules.

This gives BBB a constrained robot-like problem:

- finite and enumerable;
- hidden feasible subset inside a larger ambient state space;
- meaningful invalid moves;
- a nontrivial start-goal path;
- a default upstream tower schema;
- tower/runtime/training surfaces already implemented upstream.

## Verified Upstream Facts

The current installed upstream package exposes:

- ambient candidate states: `2700`;
- valid constrained states: `89`;
- reachable valid states from configured start: `89`;
- primitive actions: `12`;
- shortest valid start-to-goal path length: `6`;
- configured goal is not one primitive action from start;
- valid outgoing non-self transition count range: `1` to `10`;
- mean valid outgoing non-self transition count: about `4.36`;
- mean invalid action count per valid state: about `5.57`;
- valid clipped self-transition count range: `0` to `3`;
- uniform random policy reconnaissance:
  - `1000` episodes;
  - `21` successes;
  - success rate about `0.021`;
  - mean reward about `-105.67`.

The random-policy number is not a benchmark result. It is a structural
reconnaissance signal that unguided action choice does not trivially solve the
task.

## Shortest Known Start-To-Goal Path

One shortest valid action path is:

```text
start: PlateSupportState(x_idx=2, y_idx=2, theta_idx=0, e1=1, e2=1, e3=1)

action 1  -> move plate left
action 6  -> extend arm 1
action 8  -> extend arm 2
action 10 -> extend arm 3
action 3  -> move plate down
action 4  -> rotate plate

goal: PlateSupportState(x_idx=1, y_idx=1, theta_idx=1, e1=2, e2=2, e3=2)
```

This path should appear in structural artifacts and human docs because it gives
future readers a concrete anchor for the task.

## Upstream Contracts To Preserve

The BBB build must preserve the following upstream distinctions.

### State Contract

PlateSupport states are immutable and hashable.

The state fields are:

```text
x_idx
y_idx
theta_idx
e1
e2
e3
```

BBB should record them as structured values in artifacts, not only as Python
repr strings.

### Observation Contract

Upstream observations are NumPy arrays with shape `(6,)` and integer fields:

```text
[x_idx, y_idx, theta_idx, e1, e2, e3]
```

BBB should not make observation encoding the primary human-facing state display.
Docs should explain the semantic fields.

### Action Contract

The upstream action count is `12`.

Known action categories:

- plate translation actions;
- plate rotation actions;
- arm extension/de-extension actions.

The blueprint does not require inventing new action names, but implementation
should provide a stable action table in BBB artifacts and docs.

Consultant Recommendation:

Define BBB-local action labels for human readability:

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

These labels should be documented as BBB display labels derived from upstream
semantics, not as upstream canonical ids.

### Transition Contract

Upstream computes:

- candidate state;
- realized next state;
- candidate validity;
- valid transition flag;
- invalid move flag;
- valid self-transition flag.

BBB must preserve these fields in diagnostics.

The key distinction:

- invalid moves self-loop because the candidate state violates feasibility;
- valid clipped self-transitions self-loop because the candidate is valid but
  equal to the source after clipping/saturation.

These cases must not be collapsed into one generic self-loop count.

### Validity Contract

The validity predicate includes:

- plate center in bounds;
- all support sockets in bounds;
- minimum engaged supports;
- stable support pattern;
- reachability for each engaged arm.

BBB should emit predicate-level summaries. A future evaluation readout should
not have to reverse-engineer why a candidate move failed.

### Reward Contract

Upstream reward semantics:

- goal-reaching transition: `100.0`;
- valid non-goal move: `-1.0`;
- self-looping move: `-3.0`.

BBB should document this as a benchmark reward proxy, not as a real robotics
quality metric.

Allowed reward claims at environment-build stage:

- reward is local to one primitive transition;
- reward distinguishes goal, ordinary motion, and self-loop pressure;
- random-policy reward can indicate rough difficulty.

Disallowed reward claims at environment-build stage:

- tower method is better;
- exploit/explore control is better;
- the reward proves domain-quality robot behavior;
- a tiny smoke run establishes learning performance.

### Terminal And Truncation Contract

Upstream terminates on reaching the configured goal.

Upstream truncates at `MAX_STEPS` when the goal has not been reached.

The current upstream `MAX_STEPS` is `50`.

BBB should record terminal/truncation semantics in:

- environment docs;
- readiness manifest;
- run manifests for diagnostics;
- future evaluation configs.

## Proposed BBB Environment Identity

### Environment Family Id

Consultant Recommendation:

```text
plate_support
```

Reason:

This is intended to become a first-class BBB environment family, not merely an
upstream smoke id.

### Upstream Smoke Id

Existing smoke id remains:

```text
plate_support_env
```

The environment build should retain this as provenance, not as the BBB family
id.

### First Instance Id

Consultant Recommendation:

```text
plate_support_5x5_default_v001
```

Reason:

The current upstream environment is a fixed 5x5 workspace with a fixed start,
goal, support-socket geometry, three arms, four orientations, and twelve
primitive actions.

### Fixture Roles

The first build should define these fixture roles:

```text
smoke fixture:
  plate_support_5x5_default_smoke_v001

structural fixture:
  plate_support_5x5_default_v001

future serious fixture:
  plate_support_5x5_default_serious_candidate_v001
```

Consultant Recommendation:

The smoke and structural fixture can point at the same upstream fixed instance,
but their claim boundaries must differ.

Smoke fixture may claim:

- imports work;
- reset/step works;
- artifacts write;
- readout discipline works.

Structural fixture may claim:

- graph/validity/reachability/tower-depth diagnostics were recorded.

Future serious fixture may claim nothing until an evaluation folder exists.

## Proposed Package Layout

Create:

```text
src/big_boy_benchmarking/environments/plate_support/
```

Suggested files:

```text
__init__.py
ids.py
upstream.py
types.py
actions.py
states.py
geometry.py
graph.py
diagnostics.py
tower_probe.py
manifests.py
paths.py
runner.py
docs_writer.py
```

### `__init__.py`

Purpose:

- expose stable package-level names;
- avoid heavy work at import time.

Expected exports:

- ids;
- runner entrypoint;
- docs writer entrypoint if needed.

### `ids.py`

Purpose:

- define stable BBB ids.

Expected constants:

```python
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

These ids should appear in artifacts and docs.

### `upstream.py`

Purpose:

- centralize upstream imports;
- fail with clear messages if upstream surfaces are unavailable;
- avoid scattering `state_collapser.examples.plate_support_env` imports across
  the package.

Expected behavior:

- import `PlateSupportEnv`, runtime, constants, helper functions;
- expose a small `ImportedPlateSupportSurface` record;
- include training-surface availability booleans;
- collect upstream dependency version through existing BBB dependency helpers.

Stop condition:

If current installed `state_collapser` lacks required PlateSupport surfaces,
implementation should stop and report dependency mismatch. It should not silently
fall back to local `/Users/foster/state_collapser` imports.

### `types.py`

Purpose:

- define BBB-owned dataclasses for structured diagnostic rows and payloads.

Possible records:

```text
PlateSupportInstanceSpec
PlateSupportStateRecord
PlateSupportActionRecord
PlateSupportTransitionRecord
PlateSupportValidityBreakdown
PlateSupportGraphSummary
PlateSupportTowerProbeSummary
PlateSupportReadinessSummary
```

These should be JSON/CSV friendly.

### `actions.py`

Purpose:

- provide human-readable action labels and categories;
- map action indices to labels;
- write action table artifacts.

Expected action table columns:

```text
action_index
action_label
action_category
upstream_identity
description
```

Action categories:

```text
plate_translation
plate_rotation
arm_extension
arm_retraction
```

### `states.py`

Purpose:

- convert upstream `PlateSupportState` into stable JSON records;
- avoid repr-only artifacts.

Expected state record fields:

```text
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

### `geometry.py`

Purpose:

- summarize validity and support geometry.

Expected outputs:

- support-pattern count table;
- reachability-pattern count table;
- orientation count table;
- position count table;
- validity predicate summary;
- socket geometry summary;
- start/goal geometry record.

### `graph.py`

Purpose:

- enumerate the upstream valid graph;
- compute reachability and shortest path;
- count transitions and transition classes.

Expected functions:

```text
enumerate_valid_states()
enumerate_transition_records()
reachable_from_start()
shortest_path_to_goal()
summarize_outgoing_counts()
summarize_invalid_actions()
summarize_self_transitions()
```

The graph enumeration should rely on upstream helper functions where available:

- `all_candidate_states`;
- `all_valid_states`;
- `valid_outgoing_transitions`;
- `primitive_transition`.

### `diagnostics.py`

Purpose:

- build all structural diagnostic tables in one place.

Expected diagnostic surfaces:

```text
instance_summary.json
graph_summary.json
state_summary.csv
action_table.csv
transition_summary.csv
transition_samples.csv
validity_predicate_summary.csv
support_pattern_summary.csv
reachability_pattern_summary.csv
orientation_summary.csv
position_summary.csv
outgoing_action_count_summary.csv
invalid_action_summary.csv
self_transition_summary.csv
shortest_path.csv
random_policy_recon_summary.csv
training_surface_availability.json
```

The random-policy reconnaissance should be optional and explicitly labeled
`recon`, not `evaluation`.

Default recommendation:

- include a small deterministic random-policy reconnaissance in environment
  readiness with `episodes=1000`, `seed=0`, `horizon=50`;
- label it as difficulty reconnaissance;
- do not make method-performance claims from it.

### `tower_probe.py`

Purpose:

- run structural tower-depth probes for default schema and no-contraction schema.

Expected arms:

```text
schema_mode_default
schema_mode_none
```

Expected output table:

```text
schema_mode
steps
seed
sample_size
use_contraction_policy
reset_on_terminal
depth_curve
max_depth
scheduled_assignment_count
unscheduled_assignment_count
reset_event_count
```

Implementation options:

1. Call upstream `state_collapser.examples.tower_depth_probe.continuous_probe`.
2. Reimplement a narrow PlateSupport-specific version locally using upstream
   runtime surfaces.

Consultant Recommendation:

Use upstream `continuous_probe` for first implementation. It is already tested
upstream across schema-enabled examples and handles default-vs-none semantics.

Risk:

Calling upstream `continuous_probe` hides some details of runtime construction.
Mitigation: also write the BBB instance/tower manifests and dependency state.

### `manifests.py`

Purpose:

- build environment-specific manifest payloads.

Expected manifests:

```text
plate_support_environment_manifest.json
plate_support_instance_manifest.json
plate_support_legality_contract.json
plate_support_reward_contract.json
plate_support_action_contract.json
plate_support_diagnostic_manifest.json
plate_support_tower_probe_manifest.json
```

These should supplement existing shared BBB manifests, not replace them.

### `paths.py`

Purpose:

- centralize repo-side default output paths.

Expected defaults:

```text
docs/environments/plate_support_5x5_default_v001.md
docs/environments/plate_support_5x5_default_v001/
```

Consultant Recommendation:

For environment-readiness artifacts, use a repo-resident environment docs
subfolder rather than `docs/evaluations`, because this is not an evaluation.

Potential shape:

```text
docs/environments/plate_support_5x5_default_v001.md
docs/environments/plate_support_5x5_default_v001/
  readiness/
    readout_source.json
    instance_summary.json
    graph_summary.json
    ...
```

Open Question For Project Owner:

Should environment-readiness machine tables live under `docs/environments/...`
as above, or should they live under a separate `docs/environment_readiness/...`
area?

Consultant Recommendation:

Use `docs/environments/plate_support_5x5_default_v001/` because the environment
protocol asks for environment docs under `docs/environments`, and this avoids
confusing readiness artifacts with evaluation results.

### `runner.py`

Purpose:

- provide one top-level environment-readiness runner.

Expected entrypoint:

```python
run_plate_support_environment_readiness(...)
```

Suggested parameters:

```text
artifact_root: Path
instance_id: str = DEFAULT_INSTANCE_ID
tower_probe_steps: int = 20
tower_probe_seed: int = 0
tower_probe_sample_size: int = 1
random_policy_episodes: int = 1000
random_policy_seed: int = 0
linearization_mode_id: str = "tensor_available_disabled"
request_compatibility_readout: bool = True
```

Expected return:

```text
status
environment_family_id
instance_id
artifact_paths
summary
warning_count
```

### `docs_writer.py`

Purpose:

- write a human-readable environment page and readiness index.

Expected primary doc:

```text
docs/environments/plate_support_5x5_default_v001.md
```

Expected content:

- what PlateSupport is;
- why BBB is adding it;
- what upstream package supplies;
- fixture ids and claim boundaries;
- state/action/reward/terminal contracts;
- structural diagnostic highlights;
- tower-depth diagnostic highlights;
- non-claims;
- commands to regenerate readiness artifacts;
- links to readiness artifact tables.

This docs writer should not generate evaluation badges. Evaluation result badges
belong under `docs/evaluations`.

## Proposed CLI

Add top-level subcommand:

```bash
uv run python -m big_boy_benchmarking.cli plate-support readiness \
  --artifact-root docs/environments/plate_support_5x5_default_v001/readiness/run_001
```

Consultant Recommendation:

Use a new `plate-support` command group, not `run-upstream-smoke`.

Reason:

`run-upstream-smoke` is a harness validation command. The new command is an
environment-readiness diagnostic command.

Proposed parser shape:

```text
plate-support
  readiness
    --artifact-root PATH
    --instance-id plate_support_5x5_default_v001
    --tower-probe-steps INT
    --tower-probe-seed INT
    --tower-probe-sample-size INT
    --random-policy-episodes INT
    --random-policy-seed INT
    --linearization-mode tensor_available_disabled
```

Possible future commands, out of scope for first implementation:

```text
plate-support run-direct
plate-support tower-training
plate-support exploit-explore
plate-support serious-learning
```

## Proposed Artifact Layout

Because this is not an evaluation, artifacts should not go under
`docs/evaluations`.

Recommended default:

```text
docs/environments/plate_support_5x5_default_v001.md
docs/environments/plate_support_5x5_default_v001/
  readiness/
    run_001/
      runs/
        plate_support_environment_readiness_v001/
          family_manifest.json
          matrix_manifest.json
          environment_family_manifest.json
          dependency_manifest.json
          run_index.jsonl
          summaries/
            summary.json
            summary.csv
          runs/
            plate_support_5x5_default_v001-readiness-seed0/
              run_manifest.json
              seed_bundle.json
              mode_manifest.json
              linearization_manifest.json
              timing_summary.json
              timing_segments.csv
              warnings.jsonl
              external_artifacts.json
              structural_diagnostics.jsonl
              instance_summary.json
              graph_summary.json
              action_table.csv
              state_summary.csv
              transition_summary.csv
              shortest_path.csv
              support_pattern_summary.csv
              reachability_pattern_summary.csv
              tower_probe_summary.csv
              random_policy_recon_summary.csv
              training_surface_availability.json
      readout_source.json
      artifact_index.md
```

The exact generated subpaths can follow existing BBB path helpers where
possible, but environment-specific tables should be colocated with the run
artifacts and indexed by the environment docs.

## Shared Artifact Machinery Use

The implementation should reuse existing BBB machinery:

- `build_run_family_paths`;
- `build_run_paths`;
- `ensure_artifact_dirs`;
- `write_json`;
- `write_csv`;
- `append_jsonl`;
- `TimingRecorder`;
- `summarize_timing_segments`;
- `RunIndexRow`;
- `WarningRow`;
- `SeedBundle`;
- `generate_seed_bundles`;
- `collect_state_collapser_dependency_state`;
- `build_linearization_artifact_payload`.

Implementation should not hand-roll:

- run-family paths;
- seed json;
- timing csv;
- dependency manifests;
- linearization reports;
- artifact schema version metadata.

## Linearization And Tensorization Metadata

Even though this is a structural readiness diagnostic, the build should record
linearization metadata.

Default mode:

```text
tensor_available_disabled
```

Reason:

This repo has repeatedly learned that tensorization conditions must be explicit
even when tensor execution is disabled.

Expected behavior:

- build a linearization report against the current tower where applicable;
- record `max_tower_depth`;
- record `max_action_count`;
- record benchmark label;
- do not claim tensor speedup.

## Readout Policy

There are two different readout concepts:

1. Environment docs under `docs/environments`.
2. Evaluation readouts under `docs/evaluations`.

This blueprint creates only the first.

The environment readiness command may write a `readout_source.json` to bind
human environment docs to machine evidence, but it should not use the evaluation
artifact-table readout protocol unless later explicitly adapted for
environment-readiness surfaces.

Consultant Recommendation:

Write an environment-specific docs writer for this first build instead of
forcing the existing evaluation readout protocol onto environment readiness.

Reason:

The evaluation readout protocol expects evaluation result surfaces. PlateSupport
environment readiness needs contracts, diagnostics, and claim boundaries, not
method-performance interpretation.

## Environment Docs Requirements

Create or update:

```text
docs/environments/plate_support_5x5_default_v001.md
```

Minimum sections:

```text
# PlateSupport 5x5 Default v001

## Status
## Purpose
## Upstream Source
## Fixture Roles
## State Contract
## Action Contract
## Transition Contract
## Validity Contract
## Reward Contract
## Terminal And Truncation Contract
## Structural Diagnostics
## Tower-Depth Diagnostics
## Training Surfaces Available Upstream
## What This Environment Can Support Later
## What This Environment Does Not Yet Claim
## Regeneration Command
## Artifact Index
```

The page should explicitly state:

- this is an environment-readiness page;
- it is not a serious evaluation result;
- learning evaluations will be designed later;
- tower depth does not imply tower benefit;
- random-policy reconnaissance is a difficulty indicator, not a method result.

## Machine Tables

### `instance_summary.json`

Required fields:

```text
environment_family_id
instance_id
fixture_role
upstream_module
upstream_smoke_id
workspace_width
workspace_height
theta_count
support_socket_count
arm_count
action_count
max_steps
start_state
goal_state
goal_differs_from_start
goal_changes_plate_pose
goal_changes_support_configuration
goal_one_step_from_start
reward_bundle_id
legality_contract_id
action_label_contract_id
```

### `graph_summary.json`

Required fields:

```text
ambient_candidate_state_count
valid_state_count
reachable_from_start_count
reachable_from_start_share
goal_reachable_from_start
shortest_path_length
valid_nonself_edge_count
transition_record_count
invalid_action_count_total
valid_self_transition_count_total
outgoing_nonself_min
outgoing_nonself_mean
outgoing_nonself_max
```

### `state_summary.csv`

Required fields:

```text
state_id
x_idx
y_idx
theta_idx
e1
e2
e3
is_start
is_goal
support_pattern
reachability_pattern
plate_center_in_bounds
all_sockets_in_bounds
minimum_engaged_supports
stable_support_pattern
valid_outgoing_nonself_count
invalid_action_count
valid_self_transition_count
reachable_from_start
shortest_distance_from_start
```

### `action_table.csv`

Required fields:

```text
action_index
action_label
action_category
description
upstream_identity
```

### `transition_summary.csv`

Required fields:

```text
source_state_id
action_index
action_label
candidate_state_id
next_state_id
candidate_valid
valid_transition
invalid_move
valid_self_transition
reward
next_is_goal
```

This table may be complete because the state/action space is small:

```text
89 valid states * 12 actions = 1068 transition records
```

### `shortest_path.csv`

Required fields:

```text
path_step_index
source_state_id
action_index
action_label
next_state_id
next_state_record
reward
```

### `support_pattern_summary.csv`

Required fields:

```text
support_pattern
state_count
state_share
```

### `reachability_pattern_summary.csv`

Required fields:

```text
reachability_pattern
state_count
state_share
```

### `validity_predicate_summary.csv`

Required fields:

```text
predicate_name
valid_state_true_count
valid_state_false_count
ambient_true_count
ambient_false_count
interpretation
```

### `tower_probe_summary.csv`

Required fields:

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

### `random_policy_recon_summary.csv`

Required fields:

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

The `claim_boundary` field should say that this is difficulty reconnaissance,
not method evaluation.

### `training_surface_availability.json`

Required fields:

```text
run_tower_training_available
run_exploit_explore_training_available
plate_support_exploit_explore_runtime_available
fiber_conditioned_stage_supported_by_upstream_tests
default_schema_available
no_contraction_schema_available
notes
```

## Structural Limit And Claim Boundary Notes

This environment can have non-flat tower structure, but first implementation
must document claim boundaries.

Allowed environment-build claims:

- BBB can import and bind upstream PlateSupport.
- BBB can enumerate the constrained feasible graph.
- BBB can record state/action/transition/reward contracts.
- BBB can distinguish invalid self-loops from valid clipped self-transitions.
- BBB can compute reachability and shortest path.
- BBB can record default schema vs flat schema tower-depth behavior.
- BBB can write environment docs and artifacts.

Disallowed environment-build claims:

- tower learning improves performance;
- exploit/explore improves performance;
- fiber-conditioned training improves performance;
- PlateSupport is definitely the final robotics benchmark;
- the observed random-policy success rate is a baseline comparison result.

## Test Plan

Create:

```text
tests/environments/plate_support/
```

Suggested tests:

```text
test_ids.py
test_upstream_surface.py
test_state_action_records.py
test_graph_diagnostics.py
test_tower_probe.py
test_runner_artifacts.py
test_docs_writer.py
test_cli_plate_support.py
```

### `test_ids.py`

Assertions:

- stable family id is `plate_support`;
- stable instance id is `plate_support_5x5_default_v001`;
- reward/legality/action/schema ids are nonempty;
- ids are unique where uniqueness matters.

### `test_upstream_surface.py`

Assertions:

- required upstream imports are available;
- upstream action count is `12`;
- upstream valid state count is `89`;
- start and goal are valid;
- goal is not one primitive step from start.

### `test_state_action_records.py`

Assertions:

- state record conversion is JSON safe;
- action labels cover all `12` actions;
- action labels are stable;
- start and goal records preserve all fields.

### `test_graph_diagnostics.py`

Assertions:

- graph diagnostics report `2700` ambient states;
- graph diagnostics report `89` valid states;
- goal is reachable;
- shortest path length is `6`;
- transition record count is `89 * 12`;
- invalid moves are counted;
- valid clipped self-transitions are counted separately.

### `test_tower_probe.py`

Assertions:

- default schema mode reaches depth at least `2`;
- no-contraction schema mode stays depth `1`;
- default schema mode reports scheduled assignments greater than `0`;
- no-contraction schema mode reports scheduled assignments `0`.

### `test_runner_artifacts.py`

Assertions:

- readiness runner writes shared manifests;
- readiness runner writes PlateSupport-specific tables;
- dependency manifest includes state_collapser state;
- linearization manifest exists and reports `tensor_available_disabled` by
  default;
- warnings file exists even when empty;
- summary json includes allowed claim boundaries.

### `test_docs_writer.py`

Assertions:

- environment doc is written;
- environment doc includes fixture roles;
- environment doc includes state/action/reward/terminal contracts;
- environment doc states this is not an evaluation result;
- environment doc links to readiness artifacts.

### `test_cli_plate_support.py`

Assertions:

- `plate-support readiness` command runs into a temporary artifact root;
- output JSON includes status, run family id, instance id, and artifact paths;
- command rejects unknown instance ids.

## Implementation Constraints

### Use `apply_patch` For Manual Edits

All manual code/doc edits should use `apply_patch`.

### Do Not Modify Upstream

This implementation should not edit `/Users/foster/state_collapser`.

If the installed upstream surface is missing required behavior, stop and report
the dependency issue.

### Do Not Create Evaluation Folders

Do not create:

```text
docs/evaluations/plate_support...
```

in this build.

### Do Not Run Long Serious Budgets

Environment readiness may run bounded structural diagnostics and optional
random-policy reconnaissance. It should not run serious learning budgets.

### Keep Counterpoint Logic Local

Do not import counterpoint-specific modules from the PlateSupport package.

Acceptable shared imports:

- artifact writers;
- manifests;
- timing;
- seeds;
- upstream dependency state;
- mode/linearization contracts.

Unacceptable dependencies:

- counterpoint schema builders;
- counterpoint threshold-frontier code;
- counterpoint serious comparison code;
- counterpoint-specific docs writers.

## Proposed Validation Commands

After implementation, run:

```bash
uv run pytest tests/environments/plate_support tests/upstream/test_smoke_envs.py tests/runners/test_upstream_smoke_runner.py
```

Run contract validation:

```bash
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Run a readiness smoke:

```bash
uv run python -m big_boy_benchmarking.cli plate-support readiness \
  --artifact-root docs/environments/plate_support_5x5_default_v001/readiness/dev_001
```

If the command writes repo artifacts during a final implementation run, use a
clean run label that does not imply serious evaluation, for example:

```text
readiness_001
```

## Readiness Acceptance Criteria

The environment build is complete when all are true:

- `src/big_boy_benchmarking/environments/plate_support` exists;
- stable ids are defined and tested;
- upstream PlateSupport is imported through one local surface;
- structural diagnostics can enumerate and summarize the fixed upstream
  instance;
- transition diagnostics preserve invalid self-loops and valid clipped
  self-transitions separately;
- default-vs-flat tower-depth probe artifacts are written;
- shared BBB manifests/timing/seed/dependency/linearization artifacts are
  written;
- human environment docs exist under `docs/environments`;
- CLI exposes `plate-support readiness`;
- tests cover ids, upstream binding, diagnostics, artifacts, docs, and CLI;
- docs explicitly state this is not a serious evaluation result;
- no PlateSupport evaluation folder has been created.

## Stop Conditions

Stop before implementation completion if:

- installed upstream `state_collapser` does not expose required PlateSupport
  surfaces;
- upstream structural facts differ from this blueprint in a way that changes
  environment meaning;
- default schema no longer gives non-flat tower depth;
- no-contraction schema no longer stays flat;
- transition semantics cannot distinguish invalid self-loop from valid clipped
  self-transition;
- artifact location becomes ambiguous between environment docs and evaluation
  readouts;
- implementation would require changing upstream `state_collapser`;
- PO changes scope to serious evaluation before environment build is complete.

## Open Questions For Project Owner

These are consultant-authored questions. They are not Project Owner decisions.

### Question 1: Artifact Location

Should PlateSupport environment-readiness artifacts live under:

```text
docs/environments/plate_support_5x5_default_v001/readiness/<run_label>/
```

or under a new area such as:

```text
docs/environment_readiness/plate_support_5x5_default_v001/<run_label>/
```

Consultant Recommendation:

Use `docs/environments/plate_support_5x5_default_v001/readiness/<run_label>/`.

### Question 2: Random-Policy Reconnaissance

Should the first readiness command include the deterministic random-policy
reconnaissance by default?

Consultant Recommendation:

Yes, but label it as reconnaissance and keep it out of evaluation claims.

### Question 3: First Instance Id

Is the proposed instance id acceptable?

```text
plate_support_5x5_default_v001
```

Consultant Recommendation:

Use it. It is specific enough to survive future larger PlateSupport variants.

### Question 4: Package Name

Is the proposed package name acceptable?

```text
src/big_boy_benchmarking/environments/plate_support
```

Consultant Recommendation:

Use it. Avoid `upstream_plate_support` because this is intended to be a BBB
environment family, not just a smoke import.

### Question 5: Training Surface Availability

Should the environment docs mention upstream tower/exploit-explore/fiber
training surfaces before BBB has serious evaluations for them?

Consultant Recommendation:

Yes, but only in a section labeled `Training Surfaces Available Upstream` with a
clear statement that availability is not evaluation evidence.

## Later Work After This Build

After this environment build lands, the next design folder should be an
evaluation folder for PlateSupport.

Likely first serious evaluation direction:

- direct tabular or masked-random baseline;
- tower-aware training;
- exploit/explore tower control;
- enough episodes/seeds to make success-rate and return changes legible;
- active-tier/tower-use diagnostics;
- flat/default schema structural controls.

That later evaluation should be designed under the evaluation construction
protocol and should create its own design, blueprint, workplan, logs, run
artifacts, and human-readable readout.

