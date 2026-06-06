# PlateSupport Threshold Frontier Calibration Implementation Workplan

## Status

Status: initial implementation workplan.

This document is generated from:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/05_threshold_frontier_calibration/01_001_plate_support_threshold_frontier_calibration_blueprint.md
```

This workplan depends on:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/00_suite_architecture/01_002_plate_support_standard_gauntlet_suite_architecture_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/01_structural_and_tower_diagnostics/01_002_plate_support_structural_and_tower_diagnostics_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/04_tower_training_health/01_002_plate_support_tower_training_health_implementation_workplan.md
```

This workplan may also read Stage 2 and Stage 3 provenance through Stage 4
manifests, but it must not select candidates.

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
- Execute only after Stage 4 emits training traces and candidate health
  classifications.
- Do not make paired-comparison claims.
- Do not use counterpoint threshold values.
- Do not choose a target without table-backed feasibility evidence.
- Stop if no feasible target can be calibrated.

## Authority And Attribution

Project Owner direction from the current request:

- create this detailed workplan after tower training health and before paired
  replicate comparison;
- follow the blueprint and Phase.Stage.Action discipline.

Consultant-authored assumptions pending Project Owner override:

- preferred first target styles are binary success and first-hit;
- return threshold is a supporting calibration view;
- sustained-hit is considered only if the episode budget makes it feasible;
- default calibration budget is 3 replicates per arm, 32 episodes per
  replicate, 50 max steps per episode;
- direct or no-contraction baseline calibration should be included if Stage 6
  will compare against a baseline.

These assumptions are not Project Owner decisions.

## Decision Locks Before Implementation

- Stage 5 consumes Stage 1 structural/reward facts and Stage 4 training traces.
- Stage 5 may run or consume calibration arms, but labels them calibration, not
  comparison.
- Stage 5 must write `recommended_comparison_target.csv`.
- If no target is feasible, Stage 6 is blocked.
- Threshold grids must be derived from observed distributions, not hard-coded
  guesses.
- Sustained windows must be feasible under the episode budget.
- Calibration target choice must be human-explainable.

## Expected Final Deliverables

Implementation should produce or update:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/threshold_frontier_calibration/
tests/environments/plate_support/test_standard_gauntlet_threshold_frontier_calibration.py
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/threshold_frontier_calibration/
docs/design/first_plate_support_environment/standard_gauntlet_suite/05_threshold_frontier_calibration/01_003_plate_support_threshold_frontier_calibration_implementation_log.md
```

Recommended package files:

```text
__init__.py
config.py
stage_sources.py
calibration_arms.py
target_policies.py
threshold_grid.py
feasibility.py
aggregation.py
manifests.py
docs_writer.py
runner.py
```

Recommended CLI surface:

```bash
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet threshold-calibration run \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \
  --training-health-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/tower_training_health/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster
```

## Workplan

### Phase 0: Execution Setup And Calibration Gate

#### Phase 0.Stage 1: Re-anchor Repository And Inputs

##### Phase 0.Stage 1.Action 1: Verify branch and dirty state

Action:

- run `git status --short --branch`;
- record branch and dirty files in the Stage 5 implementation log.

Completion criteria:

- repo state is known before edits.

Stop condition:

- stop if unrelated dirty files would be overwritten or confused with Stage 5.

##### Phase 0.Stage 1.Action 2: Verify Stage 1 and Stage 4 outputs

Action:

- confirm Stage 1 structural/reward facts are available through source
  manifests;
- confirm Stage 4 training-health readout source and result tables exist or can
  be generated.

Completion criteria:

- Stage 5 can consume required calibration inputs.

Stop condition:

- stop if Stage 4 has no usable training traces.

##### Phase 0.Stage 1.Action 3: Enforce trainable-candidate gate

Action:

- read Stage 4 candidate health classifications;
- require at least one `trainable_clean` or authorized `trainable_warning`.

Completion criteria:

- calibration candidate set is explicit.

Stop condition:

- stop if no trainable candidate exists.

#### Phase 0.Stage 2: Create Implementation Log

##### Phase 0.Stage 2.Action 1: Create Stage 5 implementation log

Action:

- create:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/05_threshold_frontier_calibration/01_003_plate_support_threshold_frontier_calibration_implementation_log.md
```

Completion criteria:

- log exists before source edits.

Stop condition:

- stop if log path conflicts with unrelated content.

##### Phase 0.Stage 2.Action 2: Add progress table and calibration source record

Action:

- add Phase.Stage.Action progress table;
- record Stage 1 and Stage 4 source paths.

Completion criteria:

- calibration inputs are auditable.

Stop condition:

- stop if Stage 4 source identity is ambiguous.

### Phase 1: Stage Package And Configuration

#### Phase 1.Stage 1: Create Calibration Package

##### Phase 1.Stage 1.Action 1: Create module directory

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/threshold_frontier_calibration/
```

Completion criteria:

- package is nested under standard gauntlet suite.

Stop condition:

- stop if suite package is missing.

##### Phase 1.Stage 1.Action 2: Add module initializer

Action:

- create `__init__.py` exporting stable config/runner symbols.

Completion criteria:

- import does not run calibration.

Stop condition:

- stop if import reads artifacts or writes files.

#### Phase 1.Stage 2: Define Calibration Config

##### Phase 1.Stage 2.Action 1: Implement calibration config

Action:

- create `config.py`;
- include:
  - artifact root;
  - run label;
  - training-health source;
  - Stage 1 source if separately required;
  - locked-by;
  - candidate cap;
  - arms to calibrate;
  - replicates per arm;
  - episodes per replicate;
  - max steps per episode;
  - paired seed policy;
  - target types to evaluate;
  - sustained window candidates;
  - threshold grid policy.

Completion criteria:

- target and budget decisions are explicit and serializable.

Stop condition:

- stop if target style or budget lacks Project Owner authorization for
  execution.

##### Phase 1.Stage 2.Action 2: Implement budget lock fields

Action:

- ensure `stage_budget_lock.json` records target types, calibration arms,
  replicate policy, episode budget, and threshold-grid construction policy.

Completion criteria:

- target calibration can be reproduced.

Stop condition:

- stop if target choices are implicit.

### Phase 2: Source Loading

#### Phase 2.Stage 1: Load Stage 4 Training Health Source

##### Phase 2.Stage 1.Action 1: Implement Stage source loader

Action:

- create `stage_sources.py`;
- load Stage 4 `readout_source.json` and resolve:
  - `training_episode_summary.csv`;
  - `training_curve_summary.csv`;
  - `concrete_step_summary.csv`;
  - `candidate_training_health_summary.csv`;
  - `downstream_comparison_input_summary.csv`.

Completion criteria:

- loader returns trainable candidates and training traces.

Stop condition:

- stop if Stage 4 source binding is outside repo.

##### Phase 2.Stage 1.Action 2: Validate Stage 4 table schemas

Action:

- validate required columns for candidate, episode, reward, success, and health
  fields.

Completion criteria:

- malformed Stage 4 inputs block calibration.

Stop condition:

- stop if success/goal fields cannot be interpreted.

#### Phase 2.Stage 2: Load Stage 1 Structural Context

##### Phase 2.Stage 2.Action 1: Resolve Stage 1 facts

Action:

- load:
  - shortest path summary;
  - random policy recon summary;
  - state-space summary;
  - transition summary.

Completion criteria:

- max steps, shortest path, random success/reward, and invalid/self-loop
  pressure are available.

Stop condition:

- stop if calibration would need reward interpretation from memory.

### Phase 3: Calibration Arms

#### Phase 3.Stage 1: Build Calibration Arm Manifest

##### Phase 3.Stage 1.Action 1: Add selected candidate calibration arms

Action:

- include trainable candidates from Stage 4 up to configured candidate cap.

Completion criteria:

- selected calibration arms trace to candidate IDs and Stage 4 health.

Stop condition:

- stop if candidate health status is missing.

##### Phase 3.Stage 1.Action 2: Add baseline calibration arm when configured

Action:

- add direct or no-contraction baseline calibration arm if Stage 6 will need a
  baseline target comparison.

Completion criteria:

- baseline calibration is labeled as calibration, not comparison.

Stop condition:

- stop if baseline runtime is unavailable or baseline semantics are unresolved.

#### Phase 3.Stage 2: Collect Calibration Episode Data

##### Phase 3.Stage 2.Action 1: Reuse existing Stage 4 traces where valid

Action:

- use Stage 4 episode traces for candidate arms when they match calibration
  budget/target requirements.

Completion criteria:

- reused traces are listed in input manifests.

Stop condition:

- stop if traces are too short or from incompatible budget/run mode.

##### Phase 3.Stage 2.Action 2: Run additional calibration arms if required

Action:

- run baseline and/or candidate calibration episodes using the configured
  calibration budget.

Completion criteria:

- calibration episode rows exist for every calibration arm.

Stop condition:

- stop if this would become a paired comparison rather than calibration.

### Phase 4: Target Policy Evaluation

#### Phase 4.Stage 1: Binary Success And First-Hit Targets

##### Phase 4.Stage 1.Action 1: Compute binary success summaries

Action:

- compute success rate by arm, candidate, replicate, and overall.

Completion criteria:

- `success_rate_summary.csv` can be written.

Stop condition:

- stop if goal/success semantics are unavailable.

##### Phase 4.Stage 1.Action 2: Compute first-hit summaries

Action:

- compute first success episode and censoring by replicate/arm.

Completion criteria:

- `first_hit_summary.csv` can be written.

Stop condition:

- stop if episode ordering is ambiguous.

#### Phase 4.Stage 2: Sustained-Hit Feasibility

##### Phase 4.Stage 2.Action 1: Evaluate window feasibility before target scoring

Action:

- reject sustained windows whose window length exceeds episode budget.

Completion criteria:

- impossible sustained-hit rules are marked infeasible.

Stop condition:

- stop if a proposed window rule repeats the counterpoint impossible-window
  failure mode.

##### Phase 4.Stage 2.Action 2: Compute sustained-hit feasibility rows

Action:

- compute sustained-hit feasibility for allowed K-of-W windows.

Completion criteria:

- `sustained_hit_feasibility_summary.csv` can be written.

Stop condition:

- stop if sustained-hit results would require more episodes than available.

#### Phase 4.Stage 3: Return Threshold Frontier

##### Phase 4.Stage 3.Action 1: Build observed reward distributions

Action:

- compute reward quantiles and distribution summaries by arm.

Completion criteria:

- `return_distribution_summary.csv` can be written.

Stop condition:

- stop if reward rows are missing or incompatible.

##### Phase 4.Stage 3.Action 2: Construct threshold grid from observed distributions

Action:

- create threshold candidates from observed quantiles and random-policy context.

Completion criteria:

- `threshold_grid_construction.csv` records source metric, source arm,
  quantile, and reason for every threshold.

Stop condition:

- stop if threshold values are hard-coded without evidence.

##### Phase 4.Stage 3.Action 3: Evaluate threshold frontier

Action:

- compute target hit feasibility for each threshold.

Completion criteria:

- `threshold_frontier_summary.csv` can be written.

Stop condition:

- stop if thresholds are all trivially above or below observed values.

### Phase 5: Recommendation Logic

#### Phase 5.Stage 1: Select Recommended Comparison Target

##### Phase 5.Stage 1.Action 1: Implement feasibility classifier

Action:

- create `feasibility.py`;
- classify each candidate target as feasible, warning, or blocked using
  blueprint rules.

Completion criteria:

- every target has a reason and claim boundary.

Stop condition:

- stop if feasibility cannot be explained in human-readable terms.

##### Phase 5.Stage 1.Action 2: Choose recommended target

Action:

- prefer binary success or first-hit when feasible;
- use return threshold as support or fallback;
- avoid composite target unless explicitly authorized.

Completion criteria:

- exactly one recommended target row is selected, or Stage 5 blocks with reason.

Stop condition:

- stop if multiple targets tie and the choice requires Project Owner judgment.

##### Phase 5.Stage 1.Action 3: Recommend Stage 6 budget

Action:

- set recommended episodes/replicates compatible with selected target.

Completion criteria:

- recommended budget is recorded in target table.

Stop condition:

- stop if feasible target requires budget beyond authorized run mode.

#### Phase 5.Stage 2: Write Downstream Pairing Input

##### Phase 5.Stage 2.Action 1: Write recommended comparison target table

Action:

- write `recommended_comparison_target.csv` with fields from the blueprint.

Completion criteria:

- Stage 6 can consume target policy without guessing.

Stop condition:

- stop if no feasible target exists.

##### Phase 5.Stage 2.Action 2: Write downstream paired comparison input summary

Action:

- write `downstream_paired_comparison_input_summary.csv`.

Completion criteria:

- Stage 6 input target and budget policy are explicit.

Stop condition:

- stop if Stage 6 would need to infer calibration intent.

### Phase 6: Artifact Writing And Readout Binding

#### Phase 6.Stage 1: Write Manifests And Tables

##### Phase 6.Stage 1.Action 1: Write Stage 5 manifests

Action:

- write:
  - `stage_manifest.json`;
  - `stage_budget_lock.json`;
  - `stage_input_manifest.json`;
  - `threshold_policy_manifest.json`;
  - `calibration_arm_manifest.json`;
  - `parent_training_health_manifest.json`.

Completion criteria:

- target choice is traceable to sources and budget.

Stop condition:

- stop if calibration arms are not provenance-bound.

##### Phase 6.Stage 1.Action 2: Write required result tables

Action:

- write:
  - `calibration_episode_summary.csv`;
  - `calibration_arm_summary.csv`;
  - `success_rate_summary.csv`;
  - `first_hit_summary.csv`;
  - `sustained_hit_feasibility_summary.csv`;
  - `return_distribution_summary.csv`;
  - `threshold_grid_construction.csv`;
  - `threshold_frontier_summary.csv`;
  - `recommended_comparison_target.csv`;
  - `downstream_paired_comparison_input_summary.csv`.

Completion criteria:

- every target recommendation is table-backed.

Stop condition:

- stop if any required table would need placeholder values.

##### Phase 6.Stage 1.Action 3: Write aggregate files

Action:

- write:
  - `stage_aggregate_summary.json`;
  - `stage_aggregate_table.csv`;
  - `stage_run_index.csv`.

Completion criteria:

- pass/warning/block and target status are explicit.

Stop condition:

- stop if no target exists but stage status is not blocked.

#### Phase 6.Stage 2: Write Readout Source And Seed Docs

##### Phase 6.Stage 2.Action 1: Create Stage 5 readout source

Action:

- write:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/threshold_frontier_calibration/readout_source.json
```

Completion criteria:

- readout source lists expected files, goal criteria, method sources,
  structural/target feasibility checks, and claim boundary.

Stop condition:

- stop if readout source would need to infer why a target was selected.

##### Phase 6.Stage 2.Action 2: Write seed human docs

Action:

- write or update:
  - `README.md`;
  - `method.md`;
  - `artifact_index.md`;
  - `runbook.md`;
  - `results/summary.md`.

Completion criteria:

- docs explain calibration and explicitly block comparison claims.

Stop condition:

- stop if docs claim candidate superiority.

### Phase 7: CLI Integration

#### Phase 7.Stage 1: Add Calibration Commands

##### Phase 7.Stage 1.Action 1: Add run command

Action:

- add `plate-support standard-gauntlet threshold-calibration run`.

Completion criteria:

- command accepts explicit artifact root and training-health source.

Stop condition:

- stop if command infers latest training health run.

##### Phase 7.Stage 1.Action 2: Add summarize/inspect command if consistent

Action:

- add an inspect/summarize command if it matches existing CLI conventions.

Completion criteria:

- command reads calibration artifacts and reports recommended target.

Stop condition:

- stop if summarize changes target selection.

### Phase 8: Tests And Verification

#### Phase 8.Stage 1: Unit Tests

##### Phase 8.Stage 1.Action 1: Test Stage 4 gate

Action:

- test missing training-health source, no trainable candidates, and authorized
  warning candidate cases.

Completion criteria:

- invalid inputs block clearly.

Stop condition:

- stop if Stage 4 health classes are incompatible.

##### Phase 8.Stage 1.Action 2: Test target feasibility rules

Action:

- test binary success, first-hit, sustained-hit impossible window, return
  threshold all-trivial cases, and no-target block.

Completion criteria:

- known feasibility cases classify correctly.

Stop condition:

- stop if target rules are underspecified.

##### Phase 8.Stage 1.Action 3: Test threshold grid provenance

Action:

- test every threshold has source metric, source arm, quantile/reason.

Completion criteria:

- unproven threshold values fail tests.

Stop condition:

- stop if grid construction cannot be made deterministic.

##### Phase 8.Stage 1.Action 4: Test downstream target table

Action:

- test `recommended_comparison_target.csv` required columns and single
  recommendation semantics.

Completion criteria:

- Stage 6 can consume target table without inference.

Stop condition:

- stop if multiple recommendations require Project Owner choice.

#### Phase 8.Stage 2: Runtime Smoke

##### Phase 8.Stage 2.Action 1: Run calibration smoke

Action:

- run Stage 5 using repo-local Stage 4 source and smoke/dev calibration budget.

Completion criteria:

- target is recommended or stage blocks with clear reason.

Stop condition:

- stop on unexpected exception, impossible sustained window bug, or path drift.

##### Phase 8.Stage 2.Action 2: Inspect recommendation reason

Action:

- inspect `recommended_comparison_target.csv` and summary tables.

Completion criteria:

- recommendation reason is human-readable and table-backed.

Stop condition:

- stop if recommendation is opaque or arbitrary.

#### Phase 8.Stage 3: Final Log Update

##### Phase 8.Stage 3.Action 1: Record validation and Stage 6 handoff

Action:

- update Stage 5 implementation log with:
  - calibration arms;
  - target types evaluated;
  - selected target or block reason;
  - recommended Stage 6 budget;
  - tests run;
  - Stage 6 input paths.

Completion criteria:

- log says whether paired comparison can proceed.

Stop condition:

- stop if Stage 6 would need hidden interpretation.

## Completion Criteria For The Component

Stage 5 is complete when:

- Stage 1 and Stage 4 sources are validated;
- calibration arms and budgets are manifest-bound;
- binary success, first-hit, sustained-hit feasibility, and return-threshold
  evidence are computed as configured;
- threshold grid is evidence-derived;
- `recommended_comparison_target.csv` exists or stage blocks explicitly;
- downstream paired comparison input summary exists;
- readout source and seed docs exist;
- CLI/run surface exists or omission is recorded;
- tests pass;
- implementation log records Phase.Stage.Action completion.

## Handoff To Next Component

Paired replicate comparison must consume:

```text
results/recommended_comparison_target.csv
results/downstream_paired_comparison_input_summary.csv
results/calibration_arm_summary.csv
results/threshold_frontier_summary.csv
stage_manifest.json
readout_source.json
```

It must use the selected target from Stage 5 rather than choosing a new
threshold inside Stage 6.
