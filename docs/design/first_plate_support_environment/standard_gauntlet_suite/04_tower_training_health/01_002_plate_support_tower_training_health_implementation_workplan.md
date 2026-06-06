# PlateSupport Tower Training Health Implementation Workplan

## Status

Status: initial implementation workplan.

This document is generated from:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/04_tower_training_health/01_001_plate_support_tower_training_health_blueprint.md
```

This workplan depends on:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/00_suite_architecture/01_002_plate_support_standard_gauntlet_suite_architecture_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/01_structural_and_tower_diagnostics/01_002_plate_support_structural_and_tower_diagnostics_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/02_contraction_schema_sweep/01_002_plate_support_contraction_schema_sweep_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/03_candidate_discovery/01_002_plate_support_candidate_discovery_implementation_workplan.md
```

This workplan uses `Phase.Stage.Action` discipline.

This workplan is not execution approval. Execution requires explicit Project
Owner instruction.

## Prime Directive Compliance Notes

This workplan follows:

- `docs/prime_directive/prime_directive.md`;
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`;
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`;
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`;
- `docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md`;
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`.

Operational consequences:

- Execute only after Project Owner approval.
- Execute only after Stage 3 produces a candidate manifest.
- Do not implement a flat-versus-tower comparison in Stage 4.
- Do not calibrate thresholds in Stage 4.
- Do not fake unavailable event fields from opaque upstream summaries.
- Stop if no concrete steps, lift success, or learner updates can be observed.

## Authority And Attribution

Project Owner direction from the current request:

- create this detailed workplan after candidate discovery and before threshold
  calibration;
- follow the blueprint and Phase.Stage.Action discipline.

Consultant-authored assumptions pending Project Owner override:

- Stage 4 prefers BBB-side runner control when upstream helpers do not expose
  detailed event hooks;
- first health budget defaults to:
  - candidate cap 2;
  - 2 training replicates per candidate;
  - 16 episodes per replicate;
  - 50 max steps per episode;
- warning candidates are not trained unless explicitly authorized in the budget
  lock.

These assumptions are not Project Owner decisions.

## Decision Locks Before Implementation

- Stage 4 consumes candidates selected by Stage 3 only.
- Candidate roles allowed by default:
  - `selected_training_candidate`.
- Candidate roles requiring explicit authorization:
  - `selected_warning_candidate`.
- Stage 4 must record episode, concrete step, lift/action-realization,
  tier/controller, learner update, and timing evidence.
- Stage 4 must classify training health separately from performance.
- Stage 4 output may feed Stage 5 calibration and Stage 6 eligibility, but it
  cannot itself make comparison claims.
- Stage 4 must preserve candidate source traces from Stage 3.

## Expected Final Deliverables

Implementation should produce or update:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/
tests/environments/plate_support/test_standard_gauntlet_tower_training_health.py
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/tower_training_health/
docs/design/first_plate_support_environment/standard_gauntlet_suite/04_tower_training_health/01_003_plate_support_tower_training_health_implementation_log.md
```

Recommended package files:

```text
__init__.py
config.py
candidate_source.py
training_surfaces.py
runner.py
events.py
aggregation.py
classification.py
manifests.py
docs_writer.py
```

Recommended CLI surface:

```bash
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet tower-training-health run \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \
  --candidate-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/candidate_discovery/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster
```

## Workplan

### Phase 0: Execution Setup And Candidate Gate

#### Phase 0.Stage 1: Re-anchor Repository And Upstream Stages

##### Phase 0.Stage 1.Action 1: Verify branch and dirty state

Action:

- run `git status --short --branch`;
- record branch and dirty files in the Stage 4 implementation log.

Completion criteria:

- repo state is known before edits.

Stop condition:

- stop if unrelated dirty files would be overwritten or confused with Stage 4.

##### Phase 0.Stage 1.Action 2: Verify architecture and Stage 3 outputs

Action:

- confirm architecture helpers exist;
- confirm Stage 3 candidate manifest and downstream training-health input
  summary exist or can be generated.

Completion criteria:

- Stage 4 can consume Stage 3 artifacts.

Stop condition:

- stop if Stage 3 did not produce candidate manifest/source trace.

##### Phase 0.Stage 1.Action 3: Enforce candidate gate

Action:

- read Stage 3 selected candidates;
- require at least one `selected_training_candidate`, or authorized warning
  diagnostic.

Completion criteria:

- candidate set for Stage 4 is explicit.

Stop condition:

- stop if no trainable candidate exists and warning training is not authorized.

#### Phase 0.Stage 2: Create Implementation Log

##### Phase 0.Stage 2.Action 1: Create Stage 4 implementation log

Action:

- create:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/04_tower_training_health/01_003_plate_support_tower_training_health_implementation_log.md
```

Completion criteria:

- log exists before source edits.

Stop condition:

- stop if log path conflicts with unrelated content.

##### Phase 0.Stage 2.Action 2: Add progress table and candidate source record

Action:

- add Phase.Stage.Action progress table;
- record candidate source, selected candidate IDs, and warning authorization
  state.

Completion criteria:

- candidate training-health decision is auditable.

Stop condition:

- stop if warning authorization state is ambiguous.

### Phase 1: Stage Package And Configuration

#### Phase 1.Stage 1: Create Tower Training Health Package

##### Phase 1.Stage 1.Action 1: Create module directory

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/
```

Completion criteria:

- package is nested under the standard gauntlet suite.

Stop condition:

- stop if suite package does not exist.

##### Phase 1.Stage 1.Action 2: Add module initializer

Action:

- create `__init__.py` exporting stable config/runner symbols.

Completion criteria:

- module import does not run training.

Stop condition:

- stop if import reads artifacts or initializes runtime state.

#### Phase 1.Stage 2: Define Training Health Config

##### Phase 1.Stage 2.Action 1: Implement config dataclass

Action:

- create `config.py`;
- include:
  - artifact root;
  - run label;
  - candidate source;
  - locked-by;
  - candidate cap;
  - training replicates per candidate;
  - episodes per replicate;
  - max steps per episode;
  - base seed;
  - warning candidate authorization;
  - learner hyperparameter overrides;
  - linearization mode.

Completion criteria:

- all budget and authorization fields are explicit.

Stop condition:

- stop if defaults would train warning candidates without authorization.

##### Phase 1.Stage 2.Action 2: Implement budget-lock serialization

Action:

- ensure training budget and warning authorization are written into
  `stage_budget_lock.json`.

Completion criteria:

- every run can be interpreted against its budget and authorization state.

Stop condition:

- stop if candidate authorization cannot be represented.

### Phase 2: Candidate Source Loading

#### Phase 2.Stage 1: Parse Candidate Source

##### Phase 2.Stage 1.Action 1: Implement candidate source loader

Action:

- create `candidate_source.py`;
- load Stage 3 readout source and candidate manifest.

Completion criteria:

- loader returns selected candidates, source traces, schema construction
  metadata, and allowed downstream stages.

Stop condition:

- stop if source binding points outside repository.

##### Phase 2.Stage 1.Action 2: Validate candidate eligibility

Action:

- enforce allowed candidate roles and source trace completeness.

Completion criteria:

- ineligible candidates are blocked with reason.

Stop condition:

- stop if selected candidates lack schema construction metadata.

#### Phase 2.Stage 2: Recover Candidate Runtime Inputs

##### Phase 2.Stage 2.Action 1: Resolve schema/tower construction artifacts

Action:

- locate schema construction artifacts for each selected candidate.

Completion criteria:

- runner can reconstruct or load the tower/schema for each candidate.

Stop condition:

- stop if candidate manifest lacks enough information to reproduce runtime.

##### Phase 2.Stage 2.Action 2: Load Stage 1 graph/action/reward facts

Action:

- load relevant Stage 1 facts through Stage 3/Stage 2 provenance:
  - action table;
  - shortest path length;
  - reward/terminal semantics;
  - invalid/self-transition distinction.

Completion criteria:

- event rows can label concrete steps accurately.

Stop condition:

- stop if event labeling would require guessing PlateSupport semantics.

### Phase 3: Training Surface Selection

#### Phase 3.Stage 1: Inspect Upstream Training Surfaces

##### Phase 3.Stage 1.Action 1: Probe upstream helper observability

Action:

- inspect whether `run_tower_training` or `run_exploit_explore_training`
  exposes structured episode, step, lift, tier, and learner events.

Completion criteria:

- implementation log records which event domains are observable.

Stop condition:

- stop if only opaque summaries are available and BBB-side runner is not
  possible.

##### Phase 3.Stage 1.Action 2: Choose runner strategy

Action:

- choose one of:
  - upstream helper wrapper;
  - BBB-side runner using upstream runtime classes;
  - hybrid.

Completion criteria:

- choice is recorded in `training_surface_manifest.json`.

Stop condition:

- stop if runner choice would require an unapproved design decision.

#### Phase 3.Stage 2: Implement Training Surface Adapter

##### Phase 3.Stage 2.Action 1: Implement runtime adapter

Action:

- create `training_surfaces.py`;
- wrap upstream runtime/executor/learner surfaces behind a BBB event-emitting
  interface.

Completion criteria:

- adapter can reset, step, select/resolve tower actions, and expose learner
  update information.

Stop condition:

- stop if required event fields are inaccessible.

##### Phase 3.Stage 2.Action 2: Implement unavailable-field policy

Action:

- record unavailable fields explicitly as unavailable/not_applicable instead of
  faking values.

Completion criteria:

- readout can distinguish unavailable instrumentation from zero events.

Stop condition:

- stop if a required health classification depends on unavailable hidden data.

### Phase 4: Event-Emitting Training Runner

#### Phase 4.Stage 1: Implement Seed And Run Identity

##### Phase 4.Stage 1.Action 1: Generate seed bundles

Action:

- generate deterministic seed bundles for candidate, replicate, and episode
  contexts.

Completion criteria:

- each run writes `seed_bundle.json` or equivalent row.

Stop condition:

- stop if seeds are ambient or nondeterministic.

##### Phase 4.Stage 1.Action 2: Define run IDs

Action:

- construct stable run IDs from environment instance, stage id, candidate id,
  replicate index, and run label.

Completion criteria:

- run IDs are deterministic and path-safe.

Stop condition:

- stop if candidate IDs are too long or unsafe for paths without a documented
  shortening policy.

#### Phase 4.Stage 2: Run Training Episodes

##### Phase 4.Stage 2.Action 1: Implement per-candidate replicate loop

Action:

- for each selected candidate and replicate, run configured number of episodes.

Completion criteria:

- learner state persists across episodes within a replicate.

Stop condition:

- stop if learner state resets unexpectedly between episodes.

##### Phase 4.Stage 2.Action 2: Emit episode rows

Action:

- write episode rows with all blueprint fields available.

Completion criteria:

- `episodes.csv` exists per run.

Stop condition:

- stop if episode completion cannot be observed.

##### Phase 4.Stage 2.Action 3: Emit concrete step events

Action:

- write `concrete_step_events.csv` per run.

Completion criteria:

- concrete action, candidate state, realized next state, reward, termination,
  invalid move, self-transition, and lift status are recorded.

Stop condition:

- stop if invalid move and valid self-transition cannot be distinguished.

##### Phase 4.Stage 2.Action 4: Emit lift/action-realization events

Action:

- write `lift_fiber_events.csv` per run.

Completion criteria:

- candidate lift count, executable lift count, selected lift state/action, and
  failure reasons are recorded when observable.

Stop condition:

- stop if lift success cannot be observed and no alternate instrumentation
  exists.

##### Phase 4.Stage 2.Action 5: Emit tier/controller events

Action:

- write tier transition and controller action event tables.

Completion criteria:

- active tier before/after, control action, executable status, active action
  cells, and blocked reason are recorded.

Stop condition:

- stop if tower controller state is opaque.

##### Phase 4.Stage 2.Action 6: Emit learner update events

Action:

- write learner update events with selected state/action, reward, next state,
  TD error, old/new value, and update-applied flag where available.

Completion criteria:

- learner updates can be counted and summarized.

Stop condition:

- stop if learner updates cannot be observed or inferred safely.

### Phase 5: Aggregation And Health Classification

#### Phase 5.Stage 1: Aggregate Event Tables

##### Phase 5.Stage 1.Action 1: Aggregate episode and curve summaries

Action:

- create:
  - `training_episode_summary.csv`;
  - `training_curve_summary.csv`.

Completion criteria:

- per-candidate and per-replicate reward/success/step trends are visible.

Stop condition:

- stop if event rows are incomplete.

##### Phase 5.Stage 1.Action 2: Aggregate concrete step and lift summaries

Action:

- create:
  - `concrete_step_summary.csv`;
  - `lift_success_by_tier.csv`;
  - `lift_failure_by_tier.csv`.

Completion criteria:

- lift/action realization health is visible by tier.

Stop condition:

- stop if lift failures are hidden in raw warnings only.

##### Phase 5.Stage 1.Action 3: Aggregate tier/controller/learner summaries

Action:

- create:
  - `tier_occupancy_summary.csv`;
  - `tier_executability_summary.csv`;
  - `controller_action_summary.csv`;
  - `learner_update_summary.csv`.

Completion criteria:

- tier starvation and learner-update absence can be detected.

Stop condition:

- stop if controller/learner events are unavailable.

#### Phase 5.Stage 2: Classify Training Health

##### Phase 5.Stage 2.Action 1: Implement health classifier

Action:

- classify each candidate as:
  - `trainable_clean`;
  - `trainable_warning`;
  - `untrainable_no_concrete_steps`;
  - `untrainable_no_lift_success`;
  - `untrainable_no_learner_updates`;
  - `untrainable_runtime_failure`;
  - `artifact_incomplete`.

Completion criteria:

- classification reasons are table-backed.

Stop condition:

- stop if classifier requires unavailable event fields.

##### Phase 5.Stage 2.Action 2: Write downstream comparison input summary

Action:

- write `downstream_comparison_input_summary.csv`.

Completion criteria:

- Stage 5 and Stage 6 can identify trainable candidates and caveats.

Stop condition:

- stop if warning authorization state is lost.

### Phase 6: Artifact Writing And Readout Binding

#### Phase 6.Stage 1: Write Manifests

##### Phase 6.Stage 1.Action 1: Write Stage 4 manifests

Action:

- write:
  - `stage_manifest.json`;
  - `stage_budget_lock.json`;
  - `stage_input_manifest.json`;
  - `candidate_manifest.json`;
  - `training_config_manifest.json`;
  - `training_surface_manifest.json`;
  - `parent_candidate_manifest.json`.

Completion criteria:

- candidate provenance and runner strategy are auditable.

Stop condition:

- stop if runner strategy/event observability is undocumented.

##### Phase 6.Stage 1.Action 2: Write aggregate and run index files

Action:

- write:
  - `stage_aggregate_summary.json`;
  - `stage_aggregate_table.csv`;
  - `stage_run_index.csv`.

Completion criteria:

- stage pass/warning/block is explicit.

Stop condition:

- stop if artifact completeness cannot be assessed.

#### Phase 6.Stage 2: Write Readout Source And Seed Docs

##### Phase 6.Stage 2.Action 1: Create Stage 4 readout source

Action:

- write:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/tower_training_health/readout_source.json
```

Completion criteria:

- readout source includes required files, event domains, goal criteria, method
  sources, expected files, and claim boundary.

Stop condition:

- stop if readout source would need to infer event availability from code.

##### Phase 6.Stage 2.Action 2: Write seed human docs

Action:

- write or update:
  - `README.md`;
  - `method.md`;
  - `artifact_index.md`;
  - `runbook.md`;
  - `results/summary.md`.

Completion criteria:

- docs say Stage 4 is training health, not comparison.

Stop condition:

- stop if docs claim tower superiority or calibrated thresholds.

### Phase 7: CLI Integration

#### Phase 7.Stage 1: Add Training Health Commands

##### Phase 7.Stage 1.Action 1: Add run command

Action:

- add `plate-support standard-gauntlet tower-training-health run`.

Completion criteria:

- command accepts explicit artifact root, candidate source, run label, locked-by,
  budget, and warning authorization flag.

Stop condition:

- stop if command infers latest candidate discovery run.

##### Phase 7.Stage 1.Action 2: Add summarize/inspect command if consistent

Action:

- add an inspect/summarize command if it matches existing CLI conventions.

Completion criteria:

- command reads Stage 4 artifacts and reports health status.

Stop condition:

- stop if summarize reruns training.

### Phase 8: Tests And Verification

#### Phase 8.Stage 1: Unit Tests

##### Phase 8.Stage 1.Action 1: Test candidate gate

Action:

- test missing candidate manifest, no selected candidates, warning candidate
  without authorization, and selected training candidate pass.

Completion criteria:

- gate behavior matches blueprint.

Stop condition:

- stop if warning candidate policy is ambiguous.

##### Phase 8.Stage 1.Action 2: Test event table schemas

Action:

- test required event and aggregate columns.

Completion criteria:

- missing event domains fail tests unless explicitly unavailable by policy.

Stop condition:

- stop if event schema cannot represent current runtime.

##### Phase 8.Stage 1.Action 3: Test health classifier

Action:

- test all health classes using synthetic aggregate rows.

Completion criteria:

- classifier distinguishes no concrete steps, no lift success, no learner
  updates, runtime failure, warning, and clean cases.

Stop condition:

- stop if class boundaries require design revision.

##### Phase 8.Stage 1.Action 4: Test no fake unavailable fields

Action:

- test unavailable fields are recorded as unavailable/not_applicable, not zero.

Completion criteria:

- observability gaps do not become misleading zeros.

Stop condition:

- stop if readout protocol cannot handle unavailable fields.

#### Phase 8.Stage 2: Runtime Smoke

##### Phase 8.Stage 2.Action 1: Run Stage 4 smoke budget

Action:

- run Stage 4 on one repo-local candidate source with the configured smoke/dev
  budget.

Completion criteria:

- artifacts are written and health classification exists.

Stop condition:

- stop on unexpected runtime failure or path drift.

##### Phase 8.Stage 2.Action 2: Inspect event and aggregate consistency

Action:

- compare per-run event counts against aggregate tables.

Completion criteria:

- aggregate counts are explainable from raw events.

Stop condition:

- stop if aggregate tables cannot be traced to event rows.

#### Phase 8.Stage 3: Final Log Update

##### Phase 8.Stage 3.Action 1: Record validation and Stage 5 handoff

Action:

- update Stage 4 implementation log with:
  - runner strategy;
  - candidates trained;
  - warning authorization state;
  - health classifications;
  - tests run;
  - Stage 5 input paths.

Completion criteria:

- log says whether threshold calibration can proceed.

Stop condition:

- stop if no candidate has usable training traces.

## Completion Criteria For The Component

Stage 4 is complete when:

- candidate gate is enforced;
- runner/event capture strategy is documented;
- training runs emit required event domains or explicit unavailable-field
  records;
- aggregate tables and health classification exist;
- downstream comparison input summary exists;
- readout source and seed docs exist;
- CLI/run surface exists or omission is recorded;
- tests pass;
- implementation log records Phase.Stage.Action completion.

## Handoff To Next Component

Threshold frontier calibration must consume:

```text
results/training_episode_summary.csv
results/training_curve_summary.csv
results/candidate_training_health_summary.csv
results/downstream_comparison_input_summary.csv
results/lift_success_by_tier.csv
results/lift_failure_by_tier.csv
stage_manifest.json
readout_source.json
```

It must treat Stage 4 training traces as calibration/health evidence, not as a
flat-versus-tower comparison result.
