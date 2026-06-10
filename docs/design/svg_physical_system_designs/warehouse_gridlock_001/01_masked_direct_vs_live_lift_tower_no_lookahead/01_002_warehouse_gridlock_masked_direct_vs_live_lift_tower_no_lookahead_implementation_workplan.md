# Warehouse Gridlock Masked Direct vs Live-Lift Tower No-Lookahead Implementation Workplan

## Status

Initial implementation workplan.

This workplan is derived from:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_masked_direct_vs_live_lift_tower_no_lookahead/01_001_warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_001_warehouse_gridlock_environment_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_002_warehouse_gridlock_environment_implementation_workplan.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_003_warehouse_gridlock_environment_implementation_log.md
docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json
```

This workplan uses `Phase.Stage.Action` discipline.

This workplan is not execution approval by itself. Execution begins only when
the Project Owner explicitly asks to execute this workplan.

## Prime Directive Binding

This workplan follows:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/artifact_table_to_readable_document_protocol.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
docs/prime_directive/common_failure_mode_005_umbrella_workplan_fragmentation.md
docs/prime_directive/git_practices.md
```

Implementation must not silently simplify this workplan.

If an action cannot be implemented as written, the engineer must stop, record
the exact `Phase.Stage.Action` item, explain the blocker, and ask the Project
Owner for guidance.

This workplan must not invent Project Owner decisions. Attribution must remain:

- The Project Owner authored the Warehouse Gridlock SVG/design concept and the
  active Warehouse mechanics.
- Abdul Malik, project PM, raised the broader fairness concern that tower
  machinery can look better than direct control if direct wastes budget in
  immediately invalid or locally dead regions.
- The Project Owner specified the current Warehouse diagnostic boundary:
  immediate inadmissibility masking for both arms, no one-hop cul-de-sac
  lookahead for either arm, and tower live state-lift hygiene only.
- Codex authored the engineering decomposition and consultant recommendations
  in the blueprint and in this workplan.

## Decision Locks Before Implementation

These locks are authoritative for v001 unless the Project Owner changes them.

```text
evaluation_id: warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_v001
cli_family: warehouse-gridlock masked-direct-vs-live-lift-tower
implementation_branch: codex/warehouse-gridlock-masked-direct-live-lift
source_package: src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/
test_file: tests/environments/warehouse_gridlock/test_masked_direct_vs_live_lift_tower.py
design_folder: docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_masked_direct_vs_live_lift_tower_no_lookahead/
repo_readout_surface: docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/
artifact_root_template: docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/<run_label>/
readiness_source: docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json
smoke_run_label: smoke_001
first_diagnostic_run_label: masked_001
environment_family_id: warehouse_gridlock_001
environment_instance_id: warehouse_gridlock_16x16_v001
```

The active v001 arms are exactly:

```text
warehouse_direct_admissible_masked
warehouse_tower_live_lift_masked
```

The active fairness boundary is exactly:

```text
Both arms receive immediate inadmissibility masking over their generated
candidate sets.

Neither arm uses one-step successor-state cul-de-sac lookahead.

The tower arm filters candidate state lifts to live upstairs representatives:
pr(s') = s and Out(s') != empty.
```

The active candidate-generation boundary is:

```text
Direct candidates are bounded concrete synchronous ensemble-action proposals.
Tower candidates are bounded tower lift, tower action, and concrete realization
proposals.
Neither arm may claim full action-surface masking unless that is actually
proved and recorded.
```

The action-space prohibition is:

```text
Never flat-enumerate the full Warehouse primitive ensemble action surface.
The full primitive surface is 5^32.
```

## Explicit Non-Goals

Do not:

- change Warehouse Gridlock environment mechanics;
- change the SVG-derived Warehouse manifest;
- create official tiny Warehouse instances;
- edit `state_collapser`;
- implement Abdul-style direct-star or tower-star one-hop cul-de-sac guards;
- implement shortest-path planning, global search, or a privileged solver;
- compare against raw random direct over `5^32`;
- claim direct has the full admissible action set when it only has a generated
  candidate set;
- claim tower has the full abstract action surface when it only has a generated
  tower candidate set;
- hide admissibility query counts, cache counts, proposal counts, or mask
  scopes;
- write raw artifacts outside the repo as the canonical readout source;
- overwrite environment readiness artifacts;
- overwrite PlateSupport or Counterpoint artifacts;
- produce a score-only readout without the fairness audits directly below it;
- claim benchmark significance from this diagnostic.

## True Stop Conditions

Stop execution if:

- the Warehouse environment readiness source is missing or malformed;
- the installed `state_collapser` dependency cannot be verified as v0.7.2 or a
  compatible pointwise-liftability successor;
- Warehouse tower construction would require flat enumeration of the full
  `5^32` primitive ensemble action surface;
- tower construction cannot be scoped to a bounded/generated/discovered action
  surface while honestly reporting that scope;
- direct candidate generation cannot produce any admissible selected actions
  from the initial state under the smoke budget;
- tower live-lift selection cannot be implemented without using successor-state
  deadness of a candidate action;
- immediate admissibility masking cannot be distinguished in code from
  one-step successor-state lookahead;
- the tower arm cannot record live/dead lift counts;
- either arm cannot record candidate counts before and after masking;
- selected-action audit rows cannot prove
  `successor_out_count_used_for_selection=false`;
- generated `readout_source.json` would canonically point at `/private/tmp` or
  another machine-local artifact root;
- result tables cannot distinguish direct candidate masking from tower live
  lift filtering;
- tests reveal that invalid ensemble transitions advance Warehouse time;
- tests reveal that invalid ensemble transitions partially execute;
- the implementation would need an unapproved change to the Warehouse reward
  or transition contract.

## Tower Construction Policy For This Workplan

The Project Owner explicitly expects this workplan to specify tower
construction based on already completed Counterpoint and PlateSupport work.

The implementation must use those prior patterns, but it must not transplant
their assumptions blindly.

### Prior Patterns To Reuse

Reuse the following architectural ideas:

- Counterpoint owns an explicit environment-to-`state_collapser` adapter for
  `State`, `PrimitiveAction`, `BaseEdge`, `HiddenGraph`, and partition-tower
  construction.
- Counterpoint schema diagnostics record tower shape, tier counts, and
  contraction behavior as evaluation-level tables.
- PlateSupport tower training uses runtime tower snapshots and asks the tower
  surface for executable action cells and concrete lift candidates before
  selection.
- PlateSupport v0.7.2 integration treats pointwise liftability as a required
  dependency fact and records it in manifests/readouts.

### Warehouse-Specific Correction

Do not reuse the finite Counterpoint assumption that the full graph can be
enumerated.

Warehouse Gridlock must introduce a bounded tower surface:

```text
Warehouse generated/discovered graph surface
  states: Warehouse states reached or proposed under the configured exploration
          and candidate-generation policy
  actions: generated concrete ensemble-action proposals, not the full 5^32
           primitive surface
  edges: valid immediate transitions observed or admitted by the Warehouse
         transition engine for generated candidates
```

The first Warehouse tower must therefore be a scoped tower over a bounded
generated/discovered graph surface. It may not claim to be the tower over the
complete serious MDP.

### Required Tower Construction Artifacts

The implementation must write enough evidence for readers to know exactly what
the tower was built from:

```text
tower_construction_manifest.json
tower_surface_scope_manifest.json
results/tower_shape_summary.csv
results/tower_surface_scope_summary.csv
results/tower_live_lift_summary.csv
```

At minimum, these artifacts must report:

- state surface count;
- generated primitive candidate count;
- valid edge count;
- invalid candidate count;
- schema id;
- schema mode;
- schema seed;
- tier count;
- state-cell counts by tier;
- action-cell counts by tier;
- whether the surface is complete, bounded, sampled, or discovered;
- whether masks are exact over the generated surface or over a larger surface;
- whether any full action-space claim is blocked.

## Implementation Log Target

During execution, create and maintain:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_masked_direct_vs_live_lift_tower_no_lookahead/01_003_warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_implementation_log.md
```

The log must record:

- completed `Phase.Stage.Action` items;
- branch and dirty-state checks;
- file changes;
- test commands;
- test outcomes;
- smoke commands;
- artifact paths;
- readout generation commands;
- surprises;
- stop-condition checks;
- Project Owner clarifications.

## Workplan

### Phase 0: Execution Setup And Reality Binding

#### Phase 0.Stage 1: Verify Repository State

##### Phase 0.Stage 1.Action 1: Check branch and dirty state

Action:

- Run `git status --short --branch`.
- Record the current branch.
- Record dirty files relevant to Warehouse Gridlock, Warehouse readouts, and
  this design folder.
- Record unrelated dirty files without modifying them.

Deliverables:

- implementation log entry with branch and dirty-state summary.

Verification:

- no unexamined dirty file is in a path this workplan will modify.

Stop if:

- there are conflicting uncommitted edits in:
  - `src/big_boy_benchmarking/environments/warehouse_gridlock/`;
  - `tests/environments/warehouse_gridlock/`;
  - `docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/`;
  - this design folder.

##### Phase 0.Stage 1.Action 2: Create or switch to the implementation branch

Action:

- If not already on the correct implementation branch, create or switch to:

```text
codex/warehouse-gridlock-masked-direct-live-lift
```

Deliverables:

- implementation branch active.
- branch action recorded in the implementation log.

Verification:

- `git branch --show-current` reports the implementation branch.

Stop if:

- branch creation or switching would overwrite user work.

##### Phase 0.Stage 1.Action 3: Confirm no accidental staged artifacts

Action:

- Run `git diff --cached --name-status`.
- Record whether anything is already staged.
- If unrelated files are staged, do not unstage automatically unless the
  Project Owner has explicitly asked for cleanup.

Deliverables:

- staged-state note in implementation log.

Verification:

- staged paths are understood before implementation begins.

Stop if:

- staged files overlap this workplan and their origin is unclear.

#### Phase 0.Stage 2: Re-read Source Authority

##### Phase 0.Stage 2.Action 1: Re-read the active blueprint

Action:

- Re-read:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_masked_direct_vs_live_lift_tower_no_lookahead/01_001_warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_blueprint.md
```

Deliverables:

- log note that the blueprint was re-read.
- list of any newly discovered contradictions.

Verification:

- implementation choices still match the active arm matrix and claim boundary.

Stop if:

- the blueprint has changed in a way that contradicts this workplan.

##### Phase 0.Stage 2.Action 2: Re-read Warehouse environment authority

Action:

- Re-read:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_001_warehouse_gridlock_environment_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_003_warehouse_gridlock_environment_implementation_log.md
docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json
```

Deliverables:

- environment authority note in implementation log.

Verification:

- environment mechanics used by this evaluation match the implemented
  readiness slice:
  - invalid ensembles self-loop;
  - invalid ensembles do not advance time;
  - invalid ensembles do not partially execute;
  - valid ensembles advance time by one second;
  - reward constants match the manifest.

Stop if:

- the readiness source and implemented transition code disagree.

##### Phase 0.Stage 2.Action 3: Re-read prior tower patterns

Action:

- Re-read the current tower and liftability reference surfaces:

```text
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/training_surfaces.py
src/big_boy_benchmarking/environments/plate_support/tower_star/tower_lifts.py
docs/design/state_collapser_v072_pointwise_liftability_handoff/
```

Deliverables:

- log note describing which prior patterns will be reused and which cannot be
  reused for Warehouse.

Verification:

- the log explicitly says Counterpoint full enumeration is not valid for
  Warehouse.

Stop if:

- the available `state_collapser` APIs cannot support a scoped generated graph
  tower.

#### Phase 0.Stage 3: Establish Dependency Reality

##### Phase 0.Stage 3.Action 1: Verify `state_collapser` dependency state

Action:

- Use the repository's dependency-state helper or existing upstream tests to
  confirm the active `state_collapser` version and liftability semantics.

Deliverables:

- dependency-state note in implementation log.

Verification:

- dependency state reports v0.7.2 or a newer compatible pointwise liftability
  implementation.

Stop if:

- the dependency is older than v0.7.2;
- the dependency state cannot be inspected;
- pointwise liftability semantics cannot be verified.

##### Phase 0.Stage 3.Action 2: Verify Warehouse transition query semantics

Action:

- Inspect the Warehouse transition engine and tests.
- Confirm an action can be checked for immediate validity by calling the
  transition function without committing the resulting state to the runtime.

Deliverables:

- log note explaining the immediate-admissibility query mechanism.

Verification:

- query semantics can determine `valid` and `invalid_reasons` for a generated
  candidate at the current state.

Stop if:

- the only way to query validity mutates runtime state;
- the query would accidentally advance episode time.

##### Phase 0.Stage 3.Action 3: Lock smoke defaults

Action:

- Implement smoke defaults as configurable defaults, not as final benchmark
  claims:

```text
run_label: smoke_001
episodes_per_arm: 2
replicates_per_arm: 1
max_seconds_per_episode: 32
candidate_proposals_per_step: 64
schema_seed_count: 1
```

Deliverables:

- smoke defaults recorded in `config.py` during implementation.

Verification:

- CLI can override every smoke default.

Stop if:

- any smoke default is hard-coded in a way that prevents later diagnostic runs.

### Phase 1: Package Skeleton, IDs, And Config

#### Phase 1.Stage 1: Create Source Package

##### Phase 1.Stage 1.Action 1: Create the evaluation package

Action:

- Create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/
```

with:

```text
__init__.py
config.py
paths.py
readiness_source.py
arms.py
candidate_generation.py
admissibility.py
warehouse_tower_adapter.py
tower_surface.py
training.py
events.py
aggregation.py
manifests.py
docs_writer.py
runner.py
```

Deliverables:

- package exists with importable modules.

Verification:

- `uv run python -m compileall` or targeted import tests succeed for the new
  package.

Stop if:

- package creation collides with existing user files.

##### Phase 1.Stage 1.Action 2: Define stable evaluation constants

Action:

- In `config.py`, define constants for:
  - evaluation id;
  - artifact schema version;
  - environment family id;
  - environment instance id;
  - active arm ids;
  - candidate policy ids;
  - mask policy ids;
  - lift policy id;
  - no-lookahead policy id;
  - default smoke budget;
  - default readout surface;
  - default readiness source.

Deliverables:

- `config.py` constants.

Verification:

- tests can import constants without importing heavy runtime dependencies.

Stop if:

- constants duplicate unrelated PlateSupport or Counterpoint ids.

##### Phase 1.Stage 1.Action 3: Define path helpers

Action:

- In `paths.py`, define helpers for:
  - repo readout surface;
  - artifact root;
  - evaluation root;
  - run root;
  - result directory;
  - badge directory;
  - docs/readout paths;
  - run-specific artifact paths.

Deliverables:

- path helper functions.

Verification:

- helpers produce repo-resident paths under:

```text
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/
```

Stop if:

- any canonical path defaults to `/private/tmp`.

#### Phase 1.Stage 2: Register CLI And IDs

##### Phase 1.Stage 2.Action 1: Add CLI commands

Action:

- Add a CLI surface:

```text
warehouse-gridlock masked-direct-vs-live-lift-tower run
warehouse-gridlock masked-direct-vs-live-lift-tower summarize
```

Required `run` arguments:

```text
--repo-root
--artifact-root
--readiness-source
--run-label
--locked-by
--episodes-per-arm
--replicates-per-arm
--max-seconds-per-episode
--candidate-proposals-per-step
--schema-seeds
--smoke
```

Required `summarize` arguments:

```text
--repo-root
--artifact-root
```

Deliverables:

- CLI routes wired to `runner.py`.

Verification:

- `uv run python -m big_boy_benchmarking.cli warehouse-gridlock --help`
  includes the new command family.

Stop if:

- CLI routing would break existing Warehouse readiness commands.

##### Phase 1.Stage 2.Action 2: Register evaluation ids where needed

Action:

- If the repository has central id registries for environment/evaluation ids,
  add:

```text
warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_v001
```

Deliverables:

- central id registry update, if applicable.

Verification:

- no duplicate ids.

Stop if:

- the registry already contains a conflicting id with different semantics.

### Phase 2: Readiness Source Binding And Input Manifests

#### Phase 2.Stage 1: Load And Validate Environment Readiness

##### Phase 2.Stage 1.Action 1: Implement readiness-source loader

Action:

- In `readiness_source.py`, load:

```text
docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json
```

- Resolve repo-relative paths from the supplied repo root.

Deliverables:

- typed readiness-source object or validated dict wrapper.

Verification:

- missing file produces a clear error.
- malformed JSON produces a clear error.

Stop if:

- source binding cannot identify the Warehouse environment readiness artifact.

##### Phase 2.Stage 1.Action 2: Validate required readiness facts

Action:

- Check the readiness source for:
  - environment family id;
  - instance id;
  - source artifact root;
  - graph counts;
  - robot count;
  - box count;
  - transition rule contract;
  - collision policy;
  - reward policy;
  - hidden/admissibility policy;
  - source drawing attribution;
  - readiness status.

Deliverables:

- `evaluation_input_manifest.json` readiness section.

Verification:

- validation passes for current readiness artifacts.

Stop if:

- readiness status is not complete;
- the instance id is not `warehouse_gridlock_16x16_v001`;
- graph/action facts are missing.

##### Phase 2.Stage 1.Action 3: Bind runtime instance

Action:

- Load the Warehouse Gridlock instance from the existing environment package.
- Confirm it matches the readiness source.

Deliverables:

- runtime instance available to the runner.

Verification:

- graph node count and directed edge count match readiness source.
- robot and box counts match readiness source.

Stop if:

- runtime facts diverge from readiness-source facts.

#### Phase 2.Stage 2: Write Input And Dependency Manifests

##### Phase 2.Stage 2.Action 1: Write evaluation input manifest

Action:

- In `manifests.py`, write:

```text
evaluation_input_manifest.json
```

with:

- readiness source path;
- environment readiness status;
- instance id;
- graph facts;
- transition/reward facts;
- source design docs;
- source attribution.

Deliverables:

- `evaluation_input_manifest.json`.

Verification:

- manifest paths are repo-relative where possible.

Stop if:

- manifest would omit source attribution.

##### Phase 2.Stage 2.Action 2: Write dependency manifest

Action:

- Write:

```text
dependency_manifest.json
```

including:

- `state_collapser` dependency state;
- pointwise liftability semantics status;
- Python version;
- package version or commit if available;
- BBB source state if available.

Deliverables:

- `dependency_manifest.json`.

Verification:

- manifest includes v0.7.2-or-newer liftability statement.

Stop if:

- dependency state cannot be collected.

### Phase 3: Candidate Generation For Both Arms

#### Phase 3.Stage 1: Define Shared Candidate Types

##### Phase 3.Stage 1.Action 1: Define candidate dataclasses

Action:

- In `candidate_generation.py`, define dataclasses for:

```text
DirectActionCandidate
TowerLiftCandidate
TowerActionCandidate
TowerConcreteRealizationCandidate
CandidateGenerationReport
```

Required shared fields:

```text
candidate_id
candidate_type
state_id
policy_id
generation_scope
generation_budget
generation_seed
rank
metadata
```

Deliverables:

- candidate dataclasses.

Verification:

- dataclasses serialize cleanly to CSV/JSON rows.

Stop if:

- candidate ids are unstable across runs with the same seed.

##### Phase 3.Stage 1.Action 2: Define candidate-generation policies

Action:

- Define v001 policies:

```text
warehouse_sparse_ensemble_candidate_generator_v001
warehouse_bounded_tower_candidate_generator_v001
```

The direct generator should support:

- all-stay action;
- one-active-robot actions with all other robots stay;
- optional sparse two-active-robot proposals when budget allows;
- deterministic seeded ordering;
- bounded maximum proposals per step.

The tower generator should support:

- bounded lift candidates over the current downstairs state;
- bounded tower action/action-cell candidates from the selected live lift;
- bounded concrete realization candidates;
- deterministic seeded ordering;
- explicit reporting of whether the returned set is complete or sampled.

Deliverables:

- candidate policy definitions in code and manifests.

Verification:

- policy ids appear in run manifests and event rows.

Stop if:

- tower candidate generation is treated as automatically complete without proof.

#### Phase 3.Stage 2: Implement Direct Candidate Generation

##### Phase 3.Stage 2.Action 1: Implement all-stay candidate

Action:

- Generate the ensemble action where all robots stay.

Deliverables:

- all-stay direct candidate.

Verification:

- all-stay has stable id.
- all-stay validates against required robot ids.

Stop if:

- all-stay action cannot be represented by the existing Warehouse action class.

##### Phase 3.Stage 2.Action 2: Implement one-active-robot candidates

Action:

- For each robot and each move command, generate the action where that robot
  receives the move command and all other robots stay.

Deliverables:

- one-active-robot candidate generator.

Verification:

- candidate count is bounded by `1 + 32 * 4` before budget truncation.
- generator does not enumerate `5^32`.

Stop if:

- robot ids cannot be resolved from the instance manifest.

##### Phase 3.Stage 2.Action 3: Implement optional sparse two-active candidates

Action:

- Add a budgeted seeded sampler for two-active-robot commands.
- Keep it disabled or budget-limited by default for smoke if it makes the
  smoke too expensive.

Deliverables:

- sparse two-active candidate path.

Verification:

- candidate count respects `candidate_proposals_per_step`.
- sampler is deterministic for a seed.

Stop if:

- sampler introduces nondeterministic row ordering.

##### Phase 3.Stage 2.Action 4: Write direct candidate events

Action:

- Write one row per generated direct candidate to:

```text
direct_candidate_events.csv
```

Required fields:

```text
run_id
arm_id
episode_index
step_index
state_id
candidate_id
candidate_generation_policy_id
candidate_generation_scope
candidate_generation_budget
candidate_rank
candidate_action_id
candidate_action_summary
is_all_stay
active_robot_count
generation_complete_for_scope
```

Deliverables:

- direct candidate event writer.

Verification:

- smoke run can write rows without selected actions.

Stop if:

- candidate events omit policy id or scope.

#### Phase 3.Stage 3: Implement Tower Candidate Generation Stubs And Contracts

##### Phase 3.Stage 3.Action 1: Define tower candidate scope language

Action:

- In `candidate_generation.py` and manifests, define tower candidate scopes:

```text
generated_discovered_surface
current_live_fiber_candidate_set
current_tower_action_candidate_set
current_concrete_realization_candidate_set
```

Deliverables:

- stable scope strings.

Verification:

- scope strings are used consistently in manifests and event rows.

Stop if:

- scope language implies a full MDP surface.

##### Phase 3.Stage 3.Action 2: Implement tower candidate report shape

Action:

- Implement report objects that can record:
  - fiber candidate count;
  - live lift count;
  - dead lift count;
  - tower action candidate count before mask;
  - tower action candidate count after mask;
  - concrete realization candidate count;
  - generation complete/sampled flags.

Deliverables:

- tower candidate report object.

Verification:

- reports serialize to `tower_state_lift_events.csv` and
  `tower_action_mask_events.csv`.

Stop if:

- tower candidate counts cannot be represented before tower construction.

### Phase 4: Immediate Admissibility Masking

#### Phase 4.Stage 1: Implement Direct Immediate Mask

##### Phase 4.Stage 1.Action 1: Implement non-mutating direct validity query

Action:

- In `admissibility.py`, implement:

```text
query_direct_candidate_admissibility(instance, state, candidate, max_seconds)
```

- Use the existing Warehouse transition engine to classify the generated
  candidate at the current state.
- Do not commit the transition to runtime state.

Deliverables:

- direct admissibility query function.

Verification:

- invalid query returns `valid=false` and reasons.
- valid query returns candidate successor diagnostics.
- query does not advance the actual episode state.

Stop if:

- the transition engine cannot be used as a pure query.

##### Phase 4.Stage 1.Action 2: Implement direct mask

Action:

- Filter direct candidates to those with `valid=true`.

Deliverables:

- direct mask function.

Verification:

- selected direct action is always from the post-mask candidate set.

Stop if:

- mask selection can fall through to an invalid candidate.

##### Phase 4.Stage 1.Action 3: Write direct mask audit rows

Action:

- Write:

```text
direct_admissibility_mask_events.csv
```

Required fields:

```text
run_id
arm_id
episode_index
step_index
state_id
candidate_generation_policy_id
candidate_count_before_mask
candidate_count_after_mask
inadmissible_candidate_count
admissibility_query_count
cache_hit_count
selected_action_id
selected_action_admissible
mask_scope
mask_policy_id
successor_out_count_used_for_selection
```

Deliverables:

- direct mask audit writer.

Verification:

- every direct selected step has one mask audit row.
- `successor_out_count_used_for_selection=false` for every row.

Stop if:

- audit cannot distinguish invalid-candidate masking from successor lookahead.

#### Phase 4.Stage 2: Implement Tower Action/Realization Mask

##### Phase 4.Stage 2.Action 1: Define tower concrete realization query

Action:

- Implement a function that checks whether a tower concrete realization
  candidate is immediately valid at the current Warehouse state.

Deliverables:

- tower concrete realization admissibility query.

Verification:

- query returns the same validity result the direct mask would return for the
  same concrete ensemble action.

Stop if:

- tower action validity uses a different transition rule from direct validity.

##### Phase 4.Stage 2.Action 2: Implement tower action mask

Action:

- Filter tower action/concrete realization candidates using immediate
  current-action admissibility only.

Deliverables:

- tower action mask function.

Verification:

- selected tower action has at least one selected concrete realization
  candidate that is immediately valid.

Stop if:

- tower action mask requires successor-state `Out` after executing the action.

##### Phase 4.Stage 2.Action 3: Write tower action mask audit rows

Action:

- Write:

```text
tower_action_mask_events.csv
```

Required fields:

```text
run_id
arm_id
episode_index
step_index
tier
state_cell_id
tower_candidate_action_count_before_mask
tower_candidate_action_count_after_mask
inadmissible_tower_action_count
selected_tower_action_id
selected_concrete_action_id
selected_concrete_action_admissible
mask_scope
mask_policy_id
successor_out_count_used_for_selection
```

Deliverables:

- tower action mask audit writer.

Verification:

- every tower selected step has one tower action mask row.
- `successor_out_count_used_for_selection=false` for every row.

Stop if:

- selected concrete action id is missing.

### Phase 5: Warehouse Tower Construction

#### Phase 5.Stage 1: Implement Warehouse `state_collapser` Adapter

##### Phase 5.Stage 1.Action 1: Map Warehouse states to core states

Action:

- In `warehouse_tower_adapter.py`, implement:

```text
warehouse_state_to_core_state
core_state_to_warehouse_state
```

- Use `WarehouseGridlockState.stable_id` or an equivalent deterministic
  identity.

Deliverables:

- state conversion functions.

Verification:

- round-trip conversion preserves robot positions, box positions, and
  `time_step`.

Stop if:

- Warehouse states do not have stable identities.

##### Phase 5.Stage 1.Action 2: Map generated Warehouse actions to primitive actions

Action:

- Implement:

```text
warehouse_action_to_primitive_action
primitive_action_to_warehouse_action
```

- The action set is the generated candidate action set, not `5^32`.

Deliverables:

- primitive-action conversion functions.

Verification:

- generated candidates round-trip through `PrimitiveAction`.

Stop if:

- action identity depends on nondeterministic dict ordering.

##### Phase 5.Stage 1.Action 3: Map observed/generated Warehouse transitions to base edges

Action:

- Implement:

```text
warehouse_transition_to_base_edge
```

with labels:

```text
warehouse_transition
active_robot_count
moved_robot_count
moved_box_count
valid_transition
target_progress_delta
reward
candidate_generation_policy_id
```

Deliverables:

- base-edge conversion function.

Verification:

- valid generated transitions can become `BaseEdge` objects.

Stop if:

- invalid transitions are accidentally inserted as valid tower edges.

#### Phase 5.Stage 2: Build A Bounded Generated/Discovered Graph Surface

##### Phase 5.Stage 2.Action 1: Define generated graph surface data model

Action:

- Implement a `WarehouseGeneratedGraphSurface` or equivalent object that holds:
  - generated states;
  - generated concrete action candidates;
  - valid edges;
  - invalid candidate query records;
  - surface scope metadata;
  - seed and budget metadata.

Deliverables:

- generated surface data model.

Verification:

- object can report state count, action candidate count, valid edge count, and
  invalid candidate count.

Stop if:

- the data model implies full serious-MDP coverage.

##### Phase 5.Stage 2.Action 2: Seed the surface with the initial state

Action:

- Add the Warehouse initial state to the generated surface.

Deliverables:

- initial state present in surface.

Verification:

- initial state's outgoing generated candidates can be queried.

Stop if:

- initial state cannot be loaded from the runtime instance.

##### Phase 5.Stage 2.Action 3: Expand generated surface under candidate policy

Action:

- For each state selected for expansion:
  - generate bounded direct candidates;
  - query immediate validity;
  - add valid successor states and valid edges;
  - record invalid candidates as query records, not tower edges.

Deliverables:

- bounded generated graph surface.

Verification:

- expansion never enumerates `5^32`.
- expansion respects budget.
- expansion is deterministic for a seed.

Stop if:

- expansion cannot produce any valid edge from the initial state.

##### Phase 5.Stage 2.Action 4: Write tower surface scope artifacts

Action:

- Write:

```text
tower_surface_scope_manifest.json
results/tower_surface_scope_summary.csv
```

Required fields:

```text
run_id
schema_seed
surface_scope
surface_generation_policy_id
surface_generation_budget
state_count
generated_candidate_count
valid_edge_count
invalid_candidate_count
complete_full_action_surface
complete_generated_candidate_surface
```

Deliverables:

- tower surface scope artifacts.

Verification:

- `complete_full_action_surface=false` for Warehouse v001 unless explicitly
  proven otherwise.

Stop if:

- surface scope artifacts cannot be written before tower construction.

#### Phase 5.Stage 3: Implement Warehouse HiddenGraph Over The Generated Surface

##### Phase 5.Stage 3.Action 1: Implement generated-surface HiddenGraph

Action:

- Implement a `HiddenGraph` wrapper over `WarehouseGeneratedGraphSurface`.

Required methods:

```text
is_valid_state
is_valid_action
apply_action
is_valid_edge
out_actions
out_neighbors
out_edges
```

Deliverables:

- Warehouse generated-surface hidden graph.

Verification:

- `out_actions` returns generated valid candidates for a state.
- `out_edges` returns valid generated edges.
- invalid queried candidates are not returned as out edges.

Stop if:

- `state_collapser` requires the full primitive action set instead of a scoped
  generated action set.

##### Phase 5.Stage 3.Action 2: Add adapter tests on a micro-fixture

Action:

- Create unit tests with a small hand-authored Warehouse-like fixture.
- Do not treat the fixture as an official Warehouse instance.

Deliverables:

- adapter tests.

Verification:

- tests prove conversions, out action exposure, and edge validity.

Stop if:

- the only passing test would require an official tiny benchmark instance.

#### Phase 5.Stage 4: Define First Warehouse Tower Schema

##### Phase 5.Stage 4.Action 1: Implement source-local ratio schema for generated surface

Action:

- Implement or reuse an iterated source-local outgoing ratio schema over the
  generated surface.

Recommended v001 schema:

```text
schema_id: warehouse_source_local_ratio_iterated_v001
ratio_numerator: 9
ratio_denominator: 10
selection_mode: noisy_rate_or_stable_source_local_order
max_iterations: configurable
```

Deliverables:

- schema construction function.

Verification:

- schema assigns generated edges source-locally.
- schema does not depend on full outgoing actions outside the generated
  surface.

Stop if:

- schema assignment requires unknown full outdegree.

##### Phase 5.Stage 4.Action 2: Construct partition tower

Action:

- Build a `PartitionTower` or existing BBB runtime equivalent from the
  generated-surface hidden graph and schema.

Deliverables:

- constructed tower/runtime object.

Verification:

- tower has at least tier 0 and one nontrivial candidate tier in smoke when
  the generated surface has enough valid edges.

Stop if:

- tower construction collapses immediately for all smoke seeds;
- tower construction requires full graph enumeration;
- tower construction cannot expose tier shape.

##### Phase 5.Stage 4.Action 3: Write tower construction artifacts

Action:

- Write:

```text
tower_construction_manifest.json
results/tower_shape_summary.csv
```

Required fields:

```text
run_id
schema_seed
schema_id
schema_mode
ratio_numerator
ratio_denominator
max_iterations
tier_count
tier
state_cell_count
action_cell_count
valid_edge_count
surface_scope
complete_full_action_surface
```

Deliverables:

- tower construction artifacts.

Verification:

- readout can explain exactly how the tower was built.

Stop if:

- tower shape cannot be summarized at evaluation level.

#### Phase 5.Stage 5: Implement Live State-Lift Hygiene

##### Phase 5.Stage 5.Action 1: Define live lift over scoped surface

Action:

- Implement live lift as:

```text
LiveFiber(s) = {s' | pr(s') = s and Out_generated(s') != empty}
```

- The `Out` here is scoped to the generated/discovered tower surface. It is not
  a claim about the full serious MDP unless proven.

Deliverables:

- live lift function.

Verification:

- dead candidates with empty generated outgoing action sets are excluded.
- live candidates with nonempty generated outgoing action sets remain.

Stop if:

- lift live/dead status can only be determined by looking at successors of
  candidate actions from the selected lift.

##### Phase 5.Stage 5.Action 2: Select live lift deterministically

Action:

- Select a live lift using deterministic seeded ordering or policy value.
- Record the selection reason.

Deliverables:

- selected lift state for tower runtime.

Verification:

- same seed and same surface select same lift.

Stop if:

- selection falls back to a dead lift.

##### Phase 5.Stage 5.Action 3: Write tower state-lift audit rows

Action:

- Write:

```text
tower_state_lift_events.csv
```

Required fields:

```text
run_id
arm_id
episode_index
step_index
downstairs_state_id
tier
state_cell_id
fiber_candidate_count
live_lift_candidate_count
dead_lift_candidate_count
selected_lift_state_id
selected_lift_out_count
lift_failure
failure_reason
out_scope
```

Deliverables:

- tower live-lift audit writer.

Verification:

- every tower selected step has a lift audit row.
- rows distinguish no fiber, no live lift, and selected live lift.

Stop if:

- live-lift audit cannot be written before action selection.

### Phase 6: Arm Runtime And Learning/Search Loop

#### Phase 6.Stage 1: Define Shared Episode Runtime

##### Phase 6.Stage 1.Action 1: Define episode state and seed bundle

Action:

- In `training.py`, define runtime structs for:
  - arm id;
  - replicate index;
  - episode index;
  - seed bundle;
  - current Warehouse state;
  - cumulative reward;
  - target progress;
  - termination/truncation;
  - candidate/mask counters.

Deliverables:

- shared episode runtime structs.

Verification:

- direct and tower loops use the same episode budget and seed policy.

Stop if:

- direct and tower budgets diverge silently.

##### Phase 6.Stage 1.Action 2: Define matched seed policy

Action:

- Implement matched seeds so paired direct/tower runs use comparable:
  - replicate seed;
  - episode seed;
  - candidate-generation seed;
  - learner exploration seed.

Deliverables:

- seed bundle writer.

Verification:

- `seed_bundle.json` is written for every run.

Stop if:

- seed policy cannot reproduce candidate ordering.

##### Phase 6.Stage 1.Action 3: Define target-progress metrics

Action:

- Define score/progress metrics using existing Warehouse reward and target
  functions:
  - total reward;
  - final correct box count;
  - final correct robot count;
  - target progress delta;
  - terminal success;
  - valid selected step count.

Deliverables:

- target-progress computation function.

Verification:

- metrics can be computed from any Warehouse state.

Stop if:

- target-progress metrics require new environment mechanics.

#### Phase 6.Stage 2: Implement Direct Arm Runtime

##### Phase 6.Stage 2.Action 1: Implement direct step selection

Action:

- For each direct step:
  - generate candidates;
  - query immediate admissibility;
  - mask invalid candidates;
  - select among valid candidates using a small auditable controller;
  - execute selected action.

Recommended controller:

```text
warehouse_tabular_candidate_q_smoke_v001
```

Fallback if no Q table exists yet:

```text
seeded epsilon-greedy over candidate ids with simple reward update
```

Deliverables:

- direct runtime step function.

Verification:

- selected action is valid.
- selected action came from post-mask candidates.
- no successor `Out` is read before selection.

Stop if:

- no admissible candidate exists from the initial state in smoke.

##### Phase 6.Stage 2.Action 2: Implement direct learner update

Action:

- Implement a minimal tabular/bandit-style update keyed by candidate class or
  candidate id.

Deliverables:

- learner update rows for direct arm.

Verification:

- update rows include previous value, reward, next estimate if applicable, and
  new value.

Stop if:

- learner update requires a hidden planner.

#### Phase 6.Stage 3: Implement Tower Arm Runtime

##### Phase 6.Stage 3.Action 1: Build or update tower surface before tower step

Action:

- For the current tower run, build or update the generated/discovered surface
  using the configured surface-generation policy.
- Construct or refresh the partition tower as needed.

Deliverables:

- tower runtime snapshot for current step.

Verification:

- snapshot includes current downstairs state, tier positions, and surface
  scope.

Stop if:

- updating the tower would require full action enumeration.

##### Phase 6.Stage 3.Action 2: Implement live-lift selection

Action:

- Apply live state-lift hygiene over the current tower snapshot.

Deliverables:

- selected live lift or explicit lift failure.

Verification:

- selected lift has `Out_generated(s') != empty`.

Stop if:

- start state has no live lift under the smoke surface.

##### Phase 6.Stage 3.Action 3: Implement tower action candidate selection

Action:

- Generate bounded tower action candidates from the selected live lift.
- Apply immediate tower action/concrete realization mask.
- Select among post-mask tower candidates with the same controller family as
  direct, adapted to tower action ids.

Deliverables:

- selected tower action and selected concrete realization.

Verification:

- selected concrete realization is immediately valid.
- no successor `Out` is used before selection.

Stop if:

- tower action selection is implemented as post-hoc veto or resampling.

##### Phase 6.Stage 3.Action 4: Execute selected concrete realization

Action:

- Execute the selected concrete Warehouse ensemble action through the normal
  Warehouse transition engine.

Deliverables:

- Warehouse step result for tower arm.

Verification:

- tower and direct use the same transition function.

Stop if:

- tower execution bypasses Warehouse transition validation.

##### Phase 6.Stage 3.Action 5: Implement tower learner update

Action:

- Update tower controller values keyed by:
  - tier;
  - state cell;
  - tower action id;
  - concrete realization class if needed.

Deliverables:

- learner update rows for tower arm.

Verification:

- learner update rows distinguish tower keys from direct keys.

Stop if:

- direct and tower Q keys collide.

#### Phase 6.Stage 4: Implement No-Lookahead Diagnostics

##### Phase 6.Stage 4.Action 1: Observe successor `Out` only after selection

Action:

- After a selected action is executed, optionally compute or estimate successor
  outgoing count over the same generated/discovered scope.

Deliverables:

- successor diagnostic rows.

Verification:

- observation happens after selection and execution.

Stop if:

- successor `Out` is needed before selection.

##### Phase 6.Stage 4.Action 2: Write successor diagnostic rows

Action:

- Write:

```text
successor_diagnostic_events.csv
```

Required fields:

```text
run_id
arm_id
episode_index
step_index
selected_action_id
successor_state_id
successor_out_count_observed
successor_out_scope
successor_out_count_used_for_selection
selection_policy_id
selection_policy_description
```

Deliverables:

- successor diagnostic event writer.

Verification:

- every row has `successor_out_count_used_for_selection=false`.

Stop if:

- any runtime path sets `successor_out_count_used_for_selection=true`.

### Phase 7: Artifact Writers And Event Rows

#### Phase 7.Stage 1: Define Event Schemas

##### Phase 7.Stage 1.Action 1: Define run-level event fieldnames

Action:

- In `events.py`, define fieldnames for:

```text
episode_events.csv
step_events.csv
learner_update_events.csv
timing_segments.csv
```

Deliverables:

- centralized fieldname constants.

Verification:

- writers and tests use the same fieldnames.

Stop if:

- fieldnames drift between writer and aggregation code.

##### Phase 7.Stage 1.Action 2: Define fairness-audit event fieldnames

Action:

- In `events.py`, define fieldnames for:

```text
direct_candidate_events.csv
direct_admissibility_mask_events.csv
tower_state_lift_events.csv
tower_action_mask_events.csv
successor_diagnostic_events.csv
```

Deliverables:

- fairness-audit fieldname constants.

Verification:

- required blueprint fields are present.

Stop if:

- any required no-lookahead or candidate-scope field is missing.

#### Phase 7.Stage 2: Implement Artifact Writers

##### Phase 7.Stage 2.Action 1: Implement CSV append/write helpers

Action:

- Implement deterministic CSV writers that:
  - write headers;
  - sort or preserve stable row order;
  - avoid partial corrupt output on failure where practical.

Deliverables:

- CSV writer helpers.

Verification:

- smoke run writes parseable CSVs.

Stop if:

- event writers produce inconsistent columns.

##### Phase 7.Stage 2.Action 2: Implement JSON manifest writers

Action:

- Implement writers for:

```text
evaluation_manifest.json
evaluation_budget_lock.json
evaluation_input_manifest.json
dependency_manifest.json
arm_manifest.json
candidate_generation_manifest.json
admissibility_policy_manifest.json
live_lift_policy_manifest.json
no_lookahead_policy_manifest.json
tower_construction_manifest.json
tower_surface_scope_manifest.json
```

Deliverables:

- manifest writers.

Verification:

- JSON is stable, indented, and includes schema version.

Stop if:

- manifests omit active arm ids or mask scope.

##### Phase 7.Stage 2.Action 3: Implement run index writer

Action:

- Write:

```text
run_index.csv
```

Required fields:

```text
run_id
arm_id
replicate_index
schema_seed
episode_count
max_seconds_per_episode
candidate_proposals_per_step
run_root
status
failure_reason
```

Deliverables:

- run index.

Verification:

- every run root listed in the index exists.

Stop if:

- run index cannot distinguish direct and tower arms.

### Phase 8: Aggregation And Claim Logic

#### Phase 8.Stage 1: Aggregate Arm Results

##### Phase 8.Stage 1.Action 1: Implement arm summary aggregation

Action:

- Aggregate:

```text
results/arm_summary.csv
```

Required fields:

```text
arm_id
run_count
episode_count
mean_total_reward
median_total_reward
terminal_success_count
mean_final_correct_box_count
mean_final_correct_robot_count
mean_valid_selected_step_count
mean_invalid_selected_step_count
mean_candidate_count_before_mask
mean_candidate_count_after_mask
mean_admissibility_query_count
```

Deliverables:

- arm summary table.

Verification:

- table has one row per active arm.

Stop if:

- active arms are missing.

##### Phase 8.Stage 1.Action 2: Implement paired summary aggregation

Action:

- Aggregate direct/tower paired comparisons by matched seed where possible.

Deliverables:

```text
results/paired_summary.csv
```

Required fields:

```text
pair_id
direct_run_id
tower_run_id
reward_delta_tower_minus_direct
correct_box_delta_tower_minus_direct
correct_robot_delta_tower_minus_direct
terminal_success_delta
valid_step_delta
candidate_count_delta
query_count_delta
score_direction
```

Verification:

- paired rows exist for matched direct/tower runs.

Stop if:

- seed matching is missing or ambiguous.

##### Phase 8.Stage 1.Action 3: Implement target progress summary

Action:

- Aggregate target progress:

```text
results/target_progress_summary.csv
```

Required fields:

```text
arm_id
mean_initial_correct_boxes
mean_final_correct_boxes
mean_box_progress
mean_initial_correct_robots
mean_final_correct_robots
mean_robot_progress
terminal_success_count
```

Deliverables:

- target progress table.

Verification:

- values can be explained without reading raw step files.

Stop if:

- target progress cannot be computed from episode state rows.

#### Phase 8.Stage 2: Aggregate Fairness Audits

##### Phase 8.Stage 2.Action 1: Aggregate admissibility query summary

Action:

- Write:

```text
results/admissibility_query_summary.csv
```

Fields:

```text
arm_id
candidate_generation_policy_id
mask_scope
total_candidates_before_mask
total_candidates_after_mask
total_inadmissible_candidates
total_admissibility_queries
total_cache_hits
mean_candidates_before_mask_per_step
mean_candidates_after_mask_per_step
```

Deliverables:

- admissibility query summary.

Verification:

- both arms present.

Stop if:

- query counts are unavailable for either arm.

##### Phase 8.Stage 2.Action 2: Aggregate direct mask summary

Action:

- Write:

```text
results/direct_mask_summary.csv
```

Deliverables:

- direct mask summary table.

Verification:

- direct selected invalid count is zero.

Stop if:

- direct selected invalid count is nonzero.

##### Phase 8.Stage 2.Action 3: Aggregate tower live-lift summary

Action:

- Write:

```text
results/tower_live_lift_summary.csv
```

Fields:

```text
arm_id
tier
total_fiber_candidates
total_live_lift_candidates
total_dead_lift_candidates
live_lift_failure_count
mean_selected_lift_out_count
out_scope
```

Deliverables:

- tower live-lift summary.

Verification:

- tower arm present.
- selected live lifts have positive `selected_lift_out_count`.

Stop if:

- lift failures occur at the initial state in smoke.

##### Phase 8.Stage 2.Action 4: Aggregate no-lookahead audit

Action:

- Write:

```text
results/no_lookahead_audit_summary.csv
```

Fields:

```text
arm_id
selected_step_count
successor_out_observed_count
successor_out_used_for_selection_count
no_lookahead_pass
```

Deliverables:

- no-lookahead audit summary.

Verification:

- `successor_out_used_for_selection_count=0` for both arms.
- `no_lookahead_pass=true` for both arms.

Stop if:

- either arm used successor `Out` for selection.

#### Phase 8.Stage 3: Determine Score Direction And Status

##### Phase 8.Stage 3.Action 1: Implement score direction classifier

Action:

- Classify:

```text
tower
direct
tie
inconclusive
blocked
```

using:

- mean total reward;
- paired reward delta;
- terminal success if any;
- target progress;
- fairness audit status;
- artifact completeness.

Deliverables:

- score direction in aggregate summary.

Verification:

- classifier cannot report `tower` or `direct` if fairness audits fail.

Stop if:

- result direction ignores blocked fairness audits.

##### Phase 8.Stage 3.Action 2: Write aggregate summary JSON

Action:

- Write:

```text
evaluation_aggregate_summary.json
```

Required fields:

```text
evaluation_id
run_label
status
score_direction
active_arms
claim_boundary
fairness_audit_status
no_lookahead_status
mask_scope_summary
tower_surface_scope_summary
main_result_sentence
blocked_claims
```

Deliverables:

- aggregate summary JSON.

Verification:

- summary can drive the README top section.

Stop if:

- summary omits score direction or claim boundary.

### Phase 9: Readout Source And Human-Readable Docs

#### Phase 9.Stage 1: Generate `readout_source.json`

##### Phase 9.Stage 1.Action 1: Implement readout source writer

Action:

- Write checked-in readout source:

```text
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/readout_source.json
```

Required content:

- repo readout surface;
- source artifact root;
- source evaluation root;
- evaluation id;
- environment instance id;
- artifact run label;
- run mode;
- artifact storage mode;
- source files;
- expected files;
- goal criteria;
- badge policy;
- methodology sources;
- structural limit checks;
- claim boundary.

Deliverables:

- readout source JSON.

Verification:

- command target is exactly:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/readout_source.json
```

Stop if:

- readout source points at a README or raw artifact folder instead of the
  checked-in `readout_source.json`.

##### Phase 9.Stage 1.Action 2: Include required goal criteria

Action:

- Include goals for:
  - score/result direction;
  - equal immediate admissibility masking;
  - no one-step successor lookahead;
  - tower live-lift hygiene;
  - candidate mask scope honesty;
  - artifact completeness.

Deliverables:

- goal criteria in readout source.

Verification:

- every README top question from the blueprint can be answered from source
  files.

Stop if:

- goal criteria require the readout protocol to infer evaluation intent from
  code.

#### Phase 9.Stage 2: Implement Docs Writer

##### Phase 9.Stage 2.Action 1: Generate top-level README

Action:

- In `docs_writer.py`, generate:

```text
README.md
```

The README must start with:

- badges;
- score/result direction;
- one-paragraph meaning of the result;
- fairness audit summary;
- claim boundary.

Required explicit sentences:

```text
This evaluation does not implement Abdul-style direct* or tower* one-hop
cul-de-sac guards. Successor-state Out may be recorded for diagnosis, but it is
not used for action selection.
```

```text
Tower live lifting is a state-lift hygiene rule. It prevents selecting an
already-dead upstairs representative for a fixed downstairs state. It is not a
single-tier action-successor lookahead rule.
```

Deliverables:

- generated README.

Verification:

- README is score-first, with fairness/audit warnings immediately below.

Stop if:

- README hides the candidate-set scope below raw details.

##### Phase 9.Stage 2.Action 2: Generate method, runbook, glossary, and artifact index

Action:

- Generate:

```text
method.md
runbook.md
glossary.md
artifact_index.md
result_readout.md
```

Deliverables:

- human-readable support docs.

Verification:

- docs explain:
  - direct candidate generation;
  - tower candidate generation;
  - immediate masks;
  - live state-lift hygiene;
  - no-lookahead audit;
  - generated-surface tower scope.

Stop if:

- docs use PlateSupport-specific language.

##### Phase 9.Stage 2.Action 3: Generate results docs

Action:

- Generate:

```text
results/summary.md
results/score_readout.md
results/fairness_audit.md
results/candidate_generation_readout.md
results/tower_construction_readout.md
results/no_lookahead_audit.md
results/timing_readout.md
```

Deliverables:

- results docs.

Verification:

- score readout links to the audit docs.

Stop if:

- score readout can be read as a final benchmark claim.

##### Phase 9.Stage 2.Action 4: Generate badges

Action:

- Generate SVG badges for:

```text
environment
score_direction
admissibility_masking
one_step_lookahead
tower_live_lift
mask_scope
tower_surface_scope
claim_status
artifact_status
```

Deliverables:

- badge SVGs.

Verification:

- badges use the same visual style as existing human-readable evaluation
  reports.

Stop if:

- badges are rendered as raw text or inconsistent Markdown-style shields.

### Phase 10: Runner Implementation

#### Phase 10.Stage 1: Implement Run Orchestration

##### Phase 10.Stage 1.Action 1: Implement evaluation runner entry point

Action:

- In `runner.py`, implement:

```text
run_masked_direct_vs_live_lift_tower(...)
```

Responsibilities:

- resolve paths;
- validate readiness source;
- write manifests;
- run direct arm;
- run tower arm;
- write run index;
- aggregate results;
- write readout source;
- write human-readable docs.

Deliverables:

- runner entry point.

Verification:

- smoke run returns JSON with `status`, `run_label`, `artifact_root`, and
  `readout_source`.

Stop if:

- runner can complete while required artifacts are missing.

##### Phase 10.Stage 1.Action 2: Implement summarize entry point

Action:

- Implement:

```text
summarize_masked_direct_vs_live_lift_tower(...)
```

Responsibilities:

- read an existing artifact root;
- re-run aggregation;
- regenerate readout source;
- regenerate human-readable docs.

Deliverables:

- summarize entry point.

Verification:

- summarize does not rerun episodes.

Stop if:

- summarize mutates raw run event files.

#### Phase 10.Stage 2: Implement Status And Error Handling

##### Phase 10.Stage 2.Action 1: Define run statuses

Action:

- Define statuses:

```text
success
diagnostic_complete
blocked
failed
```

Deliverables:

- status constants.

Verification:

- blocked stop conditions produce `blocked`, not `success`.

Stop if:

- a blocked tower construction can be reported as successful evaluation.

##### Phase 10.Stage 2.Action 2: Preserve partial artifacts on blocked runs

Action:

- If a stop condition occurs after manifests are written, preserve:
  - input manifest;
  - dependency manifest;
  - blocked status summary;
  - failure reason;
  - partial audit rows if useful.

Deliverables:

- blocked run artifacts.

Verification:

- blocked run readout can explain why it stopped.

Stop if:

- blocked run deletes evidence needed for diagnosis.

### Phase 11: Tests

#### Phase 11.Stage 1: Candidate And Mask Tests

##### Phase 11.Stage 1.Action 1: Test direct generator does not enumerate full action space

Action:

- Add a test that verifies direct candidate count is bounded and far below
  `5^32`.

Deliverables:

- test in:

```text
tests/environments/warehouse_gridlock/test_masked_direct_vs_live_lift_tower.py
```

Verification:

- test passes.

Stop if:

- generator uses product enumeration over all robots.

##### Phase 11.Stage 1.Action 2: Test direct immediate mask

Action:

- Add tests where generated candidates include valid and invalid actions.

Deliverables:

- direct mask tests.

Verification:

- invalid candidates are removed.
- selected action is valid.

Stop if:

- invalid candidates can be selected.

##### Phase 11.Stage 1.Action 3: Test no direct successor lookahead

Action:

- Add an audit or mock test proving direct selection does not call successor
  `Out` before selection.

Deliverables:

- direct no-lookahead test.

Verification:

- audit rows set `successor_out_count_used_for_selection=false`.

Stop if:

- direct selection reads successor `Out`.

#### Phase 11.Stage 2: Tower Construction And Lift Tests

##### Phase 11.Stage 2.Action 1: Test Warehouse adapter conversions

Action:

- Test Warehouse state/action conversion to and from `state_collapser` core
  types.

Deliverables:

- adapter tests.

Verification:

- round trips are stable.

Stop if:

- identity is nondeterministic.

##### Phase 11.Stage 2.Action 2: Test generated-surface HiddenGraph

Action:

- Test `out_actions`, `out_edges`, and `apply_action` on a bounded generated
  surface.

Deliverables:

- HiddenGraph tests.

Verification:

- invalid candidates are excluded from out edges.

Stop if:

- HiddenGraph leaks invalid actions as valid outgoing actions.

##### Phase 11.Stage 2.Action 3: Test live-lift filter

Action:

- Create a micro-fixture with at least one dead lift and one live lift.

Deliverables:

- live-lift tests.

Verification:

- dead lift excluded.
- live lift selectable.

Stop if:

- live-lift test requires successor action lookahead.

##### Phase 11.Stage 2.Action 4: Test tower no-lookahead

Action:

- Add an audit or mock test proving tower action selection does not call
  successor `Out` for candidate action successors.

Deliverables:

- tower no-lookahead test.

Verification:

- audit rows set `successor_out_count_used_for_selection=false`.

Stop if:

- tower action selection uses successor-state deadness.

#### Phase 11.Stage 3: Artifact And CLI Tests

##### Phase 11.Stage 3.Action 1: Test smoke runner writes required artifacts

Action:

- Run the evaluation in a small smoke configuration under a temporary test
  artifact root.

Deliverables:

- smoke runner test.

Verification:

- all required manifests, run index, event files, result tables, and
  `readout_source.json` exist.

Stop if:

- runner reports success with missing required files.

##### Phase 11.Stage 3.Action 2: Test summarize does not rerun episodes

Action:

- Add a test that summarize reads existing artifacts and regenerates summaries.

Deliverables:

- summarize test.

Verification:

- raw event file mtimes or row counts do not change.

Stop if:

- summarize reruns training.

##### Phase 11.Stage 3.Action 3: Test readout source protocol readiness

Action:

- Validate `readout_source.json` contains required construction-protocol fields.

Deliverables:

- readout source test.

Verification:

- source binding includes goal criteria, methodology sources, expected files,
  badge policy, storage mode, and claim boundary.

Stop if:

- readout generation would need to infer evaluation intent.

#### Phase 11.Stage 4: Run Tests

##### Phase 11.Stage 4.Action 1: Run focused tests

Action:

- Run:

```text
uv run pytest tests/environments/warehouse_gridlock/test_masked_direct_vs_live_lift_tower.py
```

Deliverables:

- test output recorded in implementation log.

Verification:

- focused tests pass.

Stop if:

- focused tests fail.

##### Phase 11.Stage 4.Action 2: Run Warehouse regression tests

Action:

- Run:

```text
uv run pytest tests/environments/warehouse_gridlock
```

Deliverables:

- test output recorded in implementation log.

Verification:

- Warehouse tests pass.

Stop if:

- Warehouse readiness tests regress.

##### Phase 11.Stage 4.Action 3: Run upstream dependency tests

Action:

- Run the relevant `state_collapser` dependency tests:

```text
uv run pytest tests/upstream/test_state_collapser_dependency_state.py tests/upstream/test_state_collapser_pointwise_liftability.py
```

Deliverables:

- test output recorded in implementation log.

Verification:

- dependency tests pass.

Stop if:

- dependency tests fail.

### Phase 12: Smoke Run And Readout Generation

#### Phase 12.Stage 1: Run Smoke Evaluation

##### Phase 12.Stage 1.Action 1: Run smoke evaluation into repo artifact root

Action:

- Run:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock masked-direct-vs-live-lift-tower run \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/smoke_001 \
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster \
  --smoke
```

Deliverables:

- smoke artifacts under repo readout surface.

Verification:

- command returns `status=success`, `diagnostic_complete`, or a truthful
  blocked status with reason.

Stop if:

- command writes canonical artifacts outside the repo.

##### Phase 12.Stage 1.Action 2: Summarize smoke evaluation

Action:

- Run:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock masked-direct-vs-live-lift-tower summarize \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/smoke_001
```

Deliverables:

- regenerated aggregate summaries, readout source, and docs.

Verification:

- summarize output points to:

```text
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/readout_source.json
```

Stop if:

- summarize output points at the raw artifact root as the protocol target.

#### Phase 12.Stage 2: Apply Human-Readable Protocol

##### Phase 12.Stage 2.Action 1: Run artifact-table readout protocol

Action:

- Execute the protocol prompt:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/readout_source.json
```

Deliverables:

- human-readable README and support docs regenerated from the checked-in
  source binding.

Verification:

- README top section answers:
  - score/result direction;
  - whether both arms used immediate masks;
  - whether either arm used one-step successor lookahead;
  - whether tower used live state-lift hygiene;
  - whether masks are full-surface or generated-candidate-set masks;
  - whether result is complete, warning, or blocked.

Stop if:

- generated README points users to the wrong command target.

##### Phase 12.Stage 2.Action 2: Check generated docs for stale environment language

Action:

- Search generated docs for stale references to PlateSupport, Counterpoint, or
  direct-star/tower-star as active arms.

Deliverables:

- stale-language check note in implementation log.

Verification:

- no stale environment family is presented as the active Warehouse result.

Stop if:

- generated docs misidentify the environment.

### Phase 13: Final Verification And Handoff

#### Phase 13.Stage 1: Repository Hygiene

##### Phase 13.Stage 1.Action 1: Check git status

Action:

- Run:

```text
git status --short --branch
```

Deliverables:

- final dirty-state summary in implementation log.

Verification:

- all modified paths are expected.

Stop if:

- unexpected staged or modified files appear.

##### Phase 13.Stage 1.Action 2: Check for generated caches and local junk

Action:

- Inspect for:
  - `__pycache__`;
  - `.DS_Store`;
  - editor backup files;
  - tmp artifacts outside approved artifact roots.

Deliverables:

- hygiene note in implementation log.

Verification:

- local junk is not staged or included in deliverables.

Stop if:

- generated caches are staged.

##### Phase 13.Stage 1.Action 3: Check terminology

Action:

- Search the new design/evaluation work for stale planning terminology and
  stale environment names:

```text
PlateSupport
Counterpoint
direct_star
tower_star
```

Deliverables:

- terminology audit note.

Verification:

- stale planning terminology does not appear except when quoting
  prime-directive file names.
- PlateSupport/Counterpoint appear only as historical reference patterns, not
  as active Warehouse semantics.

Stop if:

- generated Warehouse docs describe the active evaluation as PlateSupport or
  Counterpoint.

#### Phase 13.Stage 2: Final Implementation Log

##### Phase 13.Stage 2.Action 1: Write completion summary

Action:

- Add a final implementation log section with:
  - completed phases;
  - final artifacts;
  - tests run;
  - smoke result;
  - known limitations;
  - stop conditions checked;
  - next recommended Project Owner conversation if any.

Deliverables:

- completed implementation log.

Verification:

- log contains enough detail for another engineer to resume.

Stop if:

- any completed action lacks evidence.

##### Phase 13.Stage 2.Action 2: Summarize public claim boundary

Action:

- Ensure final docs and log state:

```text
This is a Warehouse Gridlock diagnostic of fair immediate inadmissibility
masking versus tower live state-lift hygiene. It is not a final benchmark
claim and it does not implement Abdul-style one-hop cul-de-sac controls.
```

Deliverables:

- claim-boundary sentence in README, result readout, and implementation log.

Verification:

- no generated doc exceeds the allowed claim boundary.

Stop if:

- docs imply broad tower superiority or benchmark significance.

### Phase 14: Optional First Diagnostic Run

This phase is not required for the initial implementation unless the Project
Owner explicitly asks for a larger first diagnostic after smoke succeeds.

#### Phase 14.Stage 1: Run `masked_001`

##### Phase 14.Stage 1.Action 1: Run diagnostic budget

Action:

- Run a larger diagnostic using explicit Project Owner-approved or CLI-supplied
  budget values.

Recommended starting values from the blueprint:

```text
run_label: masked_001
episodes_per_arm: 16
replicates_per_arm: 4
max_seconds_per_episode: 128
candidate_proposals_per_step: 64
```

Deliverables:

- diagnostic artifacts under:

```text
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/masked_001/
```

Verification:

- diagnostic run uses a new artifact root and does not overwrite `smoke_001`.

Stop if:

- the Project Owner has not approved the larger diagnostic run.

##### Phase 14.Stage 1.Action 2: Regenerate readout for diagnostic budget

Action:

- Summarize and regenerate `readout_source.json` for `masked_001`.
- Execute the artifact-table readout protocol against the checked-in
  `readout_source.json`.

Deliverables:

- updated human-readable readout for the diagnostic run.

Verification:

- README clearly identifies `masked_001` as the active run label.

Stop if:

- README still describes `smoke_001` as the active result after `masked_001`.

## Final Expected Deliverables

Implementation is complete only when these exist and pass the checks above:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/
tests/environments/warehouse_gridlock/test_masked_direct_vs_live_lift_tower.py
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_masked_direct_vs_live_lift_tower_no_lookahead/01_003_warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_implementation_log.md
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/readout_source.json
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/README.md
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/result_readout.md
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/method.md
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/runbook.md
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/glossary.md
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifact_index.md
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/results/
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/badges/
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/smoke_001/
```

The final implementation must also provide command help for:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock masked-direct-vs-live-lift-tower --help
```

and the human-readable regeneration prompt:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/readout_source.json
```
