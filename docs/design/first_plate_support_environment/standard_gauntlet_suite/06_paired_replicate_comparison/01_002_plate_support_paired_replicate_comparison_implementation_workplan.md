# PlateSupport Paired Replicate Comparison Implementation Workplan

## Status

Status: initial implementation workplan.

This document is generated from:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/06_paired_replicate_comparison/01_001_plate_support_paired_replicate_comparison_blueprint.md
```

This workplan depends on:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/00_suite_architecture/01_002_plate_support_standard_gauntlet_suite_architecture_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/01_structural_and_tower_diagnostics/01_002_plate_support_structural_and_tower_diagnostics_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/03_candidate_discovery/01_002_plate_support_candidate_discovery_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/04_tower_training_health/01_002_plate_support_tower_training_health_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/05_threshold_frontier_calibration/01_002_plate_support_threshold_frontier_calibration_implementation_workplan.md
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
- Execute only after Stages 3, 4, and 5 provide required inputs.
- Do not invent a target threshold inside Stage 6.
- Do not silently select candidates directly from Stage 2.
- Do not claim broad tower superiority.
- Do not use `state_collapser` versions older than the required pointwise
  liftability semantics unless explicitly marked legacy-only.
- Incomplete pairs must remain visible and be excluded from paired deltas.

## Authority And Attribution

Project Owner direction from the current request:

- create this detailed workplan after target calibration and before readout;
- follow the blueprint and Phase.Stage.Action discipline.

Consultant-authored assumptions pending Project Owner override:

- direct concrete baseline is the primary human-facing baseline when available;
- no-contraction tower control is also included when available as an engineering
  control;
- Stage 5 supplies the first comparison budget and target;
- if Stage 5 does not supply a budget, a development default of 5 replicates per
  arm and 32 episodes per replicate is used only after execution approval;
- first claim wording is limited to "limited positive signal" for clean
  directional improvement.

These assumptions are not Project Owner decisions.

## Decision Locks Before Implementation

- Stage 6 is the first claim-bearing stage, but only for the narrow fixed
  fixture, budget, target, baseline, and candidate set.
- Stage 6 must consume Stage 5 `recommended_comparison_target.csv`.
- Stage 6 must carry forward untrainable/blocked candidates as readout context.
- Stage 6 must include baseline availability and primary-baseline choice in
  manifests.
- Stage 6 must use paired seed bundles.
- Stage 6 must distinguish direct baseline, no-contraction tower control, and
  selected tower candidate arms.
- Stage 6 must record liftability/runtime caveats for tower arms.
- Stage 6 must write comparison claim summary using bounded language.

## Expected Final Deliverables

Implementation should produce or update:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison/
tests/environments/plate_support/test_standard_gauntlet_paired_replicate_comparison.py
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/paired_replicate_comparison/
docs/design/first_plate_support_environment/standard_gauntlet_suite/06_paired_replicate_comparison/01_003_plate_support_paired_replicate_comparison_implementation_log.md
```

Recommended package files:

```text
__init__.py
config.py
stage_sources.py
arms.py
seed_bundles.py
target_policy.py
runner.py
events.py
aggregation.py
claim_logic.py
manifests.py
docs_writer.py
```

Recommended CLI surface:

```bash
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet paired-comparison run \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \
  --candidate-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/candidate_discovery/readout_source.json \
  --training-health-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/tower_training_health/readout_source.json \
  --threshold-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/threshold_frontier_calibration/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster
```

## Workplan

### Phase 0: Execution Setup And Hard Gates

#### Phase 0.Stage 1: Re-anchor Repository And Inputs

##### Phase 0.Stage 1.Action 1: Verify branch and dirty state

Action:

- run `git status --short --branch`;
- record branch and dirty files in the Stage 6 implementation log.

Completion criteria:

- repo state is known before edits.

Stop condition:

- stop if unrelated dirty files would be overwritten or confused with Stage 6.

##### Phase 0.Stage 1.Action 2: Verify required upstream stage sources

Action:

- verify source bindings for:
  - Stage 1 structural diagnostics;
  - Stage 3 candidate discovery;
  - Stage 4 tower training health;
  - Stage 5 threshold calibration.

Completion criteria:

- source paths are repo-resident and readable.

Stop condition:

- stop if any required source binding is missing or outside repo.

##### Phase 0.Stage 1.Action 3: Enforce Stage 5 target gate

Action:

- load `recommended_comparison_target.csv`;
- require a feasible target and recommended budget or explicit development
  default authorization.

Completion criteria:

- target policy is fixed before arms run.

Stop condition:

- stop if Stage 5 has no feasible target.

##### Phase 0.Stage 1.Action 4: Enforce trainable candidate gate

Action:

- load Stage 4 health classifications;
- require at least one `trainable_clean`, or explicitly authorized
  `trainable_warning`.

Completion criteria:

- compared candidate set is fixed.

Stop condition:

- stop if all selected candidates are untrainable.

##### Phase 0.Stage 1.Action 5: Enforce dependency semantics gate

Action:

- verify `state_collapser` dependency version/semantics are v0.7.2 or newer
  pointwise-liftability semantics, or mark legacy-only if explicitly allowed.

Completion criteria:

- liftability semantics are manifest-bound.

Stop condition:

- stop if dependency is older and not explicitly legacy-only.

#### Phase 0.Stage 2: Create Implementation Log

##### Phase 0.Stage 2.Action 1: Create Stage 6 implementation log

Action:

- create:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/06_paired_replicate_comparison/01_003_plate_support_paired_replicate_comparison_implementation_log.md
```

Completion criteria:

- log exists before source edits.

Stop condition:

- stop if log path conflicts with unrelated content.

##### Phase 0.Stage 2.Action 2: Add progress table and source record

Action:

- add Phase.Stage.Action progress table;
- record Stage 1/3/4/5 source paths, target id, candidate ids, and baseline
  availability state.

Completion criteria:

- comparison provenance is auditable.

Stop condition:

- stop if baseline or target identity is ambiguous.

### Phase 1: Stage Package And Configuration

#### Phase 1.Stage 1: Create Paired Comparison Package

##### Phase 1.Stage 1.Action 1: Create module directory

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison/
```

Completion criteria:

- package is nested under standard gauntlet suite.

Stop condition:

- stop if suite package is missing.

##### Phase 1.Stage 1.Action 2: Add module initializer

Action:

- create `__init__.py` exporting stable config/runner symbols.

Completion criteria:

- import does not run comparisons.

Stop condition:

- stop if import reads artifacts or writes files.

#### Phase 1.Stage 2: Define Comparison Config

##### Phase 1.Stage 2.Action 1: Implement config dataclass

Action:

- create `config.py`;
- include:
  - artifact root;
  - run label;
  - candidate source;
  - training-health source;
  - threshold source;
  - structural source;
  - locked-by;
  - selected baseline policy;
  - candidate cap;
  - replicates per arm;
  - episodes per replicate;
  - max steps;
  - paired seed policy;
  - allow warning candidate flag;
  - legacy dependency allowance flag.

Completion criteria:

- all comparison conditions are explicit and budget-lockable.

Stop condition:

- stop if primary baseline choice is unresolved for execution.

##### Phase 1.Stage 2.Action 2: Implement comparison budget lock

Action:

- write config values into `evaluation_budget_lock.json`.

Completion criteria:

- target, budget, arms, seeds, and dependency semantics are reproducible.

Stop condition:

- stop if any comparison parameter is implicit.

### Phase 2: Source Loading And Arm Construction

#### Phase 2.Stage 1: Load Upstream Stage Sources

##### Phase 2.Stage 1.Action 1: Implement source loader

Action:

- create `stage_sources.py`;
- load Stage 1, 3, 4, and 5 readout sources and resolve required tables.

Completion criteria:

- loader returns structural facts, candidates, health classifications, and
  target policy.

Stop condition:

- stop if source bindings point outside the repository.

##### Phase 2.Stage 1.Action 2: Validate required source tables

Action:

- validate Stage 3 candidate manifest, Stage 4 health tables, and Stage 5
  target tables.

Completion criteria:

- missing or malformed source files block before running arms.

Stop condition:

- stop if Stage 6 would need to select candidates or targets itself.

#### Phase 2.Stage 2: Build Comparison Arms

##### Phase 2.Stage 2.Action 1: Build direct concrete baseline arm

Action:

- define `plate_support_direct_concrete_baseline` if direct runtime/training
  surface is available.

Completion criteria:

- direct baseline metadata is complete or unavailable reason is recorded.

Stop condition:

- stop if no baseline arm is available.

##### Phase 2.Stage 2.Action 2: Build no-contraction tower-control arm

Action:

- define `plate_support_no_contraction_tower_control` if no-contraction tower
  runtime is available.

Completion criteria:

- no-contraction arm metadata includes schema id, tower depth, effective action
  surface, and controller policy.

Stop condition:

- stop if including no-contraction would require unapproved schema behavior.

##### Phase 2.Stage 2.Action 3: Build selected tower candidate arms

Action:

- build tower candidate arms from Stage 3/4 candidates that pass health gate.

Completion criteria:

- each candidate arm has schema id, family id, seed, health status, tower shape,
  learner config, controller config, and target policy.

Stop condition:

- stop if candidate runtime cannot be reconstructed.

##### Phase 2.Stage 2.Action 4: Write comparison arm manifest

Action:

- write `comparison_arm_manifest.json`.

Completion criteria:

- arm manifest marks primary baseline and arm roles.

Stop condition:

- stop if primary baseline choice cannot be represented.

### Phase 3: Pairing And Seed Bundles

#### Phase 3.Stage 1: Generate Pair Units

##### Phase 3.Stage 1.Action 1: Implement paired seed bundle generator

Action:

- create `seed_bundles.py`;
- generate paired bundles with environment, learner, exploration, schema/tower,
  initial-state, and tie-break seeds.

Completion criteria:

- all arms in a pair unit share the required seed fields.

Stop condition:

- stop if seed generation is nondeterministic.

##### Phase 3.Stage 1.Action 2: Build pair unit manifest

Action:

- create pair units keyed by replicate id, seed bundle id, candidate group id,
  and target policy id.

Completion criteria:

- `paired_seed_bundle_manifest.json` records every pair unit.

Stop condition:

- stop if pair unit definition cannot cover all arms.

#### Phase 3.Stage 2: Missing Pair Policy

##### Phase 3.Stage 2.Action 1: Implement incomplete pair tracking

Action:

- ensure any failed/missing arm marks its pair unit incomplete and records
  reason.

Completion criteria:

- incomplete pairs remain in `paired_unit_summary.csv`.

Stop condition:

- stop if failed runs would be silently excluded.

### Phase 4: Run Comparison Arms

#### Phase 4.Stage 1: Execute Baseline Arms

##### Phase 4.Stage 1.Action 1: Run direct baseline pairs

Action:

- run direct baseline episodes for each pair unit if available.

Completion criteria:

- direct baseline per-run artifacts and episode rows exist.

Stop condition:

- stop if direct baseline runtime behavior is not comparable to tower runtime
  under target policy.

##### Phase 4.Stage 1.Action 2: Run no-contraction tower-control pairs

Action:

- run no-contraction tower-control episodes for each pair unit if available.

Completion criteria:

- no-contraction per-run artifacts include tower-specific files.

Stop condition:

- stop if no-contraction tower control cannot use the same learner/controller
  policy as candidate tower arms.

#### Phase 4.Stage 2: Execute Candidate Arms

##### Phase 4.Stage 2.Action 1: Run selected tower candidate pairs

Action:

- run selected candidate tower arms under the same paired seeds, episode budget,
  max steps, learner policy, and target policy.

Completion criteria:

- candidate per-run artifacts exist for every requested pair or explicit
  failure reason is recorded.

Stop condition:

- stop on unexpected runtime failure that invalidates the comparison model.

##### Phase 4.Stage 2.Action 2: Emit per-run artifacts

Action:

- for every run, write required per-run artifacts:
  - manifests;
  - seed bundle;
  - episodes;
  - step events;
  - learner updates;
  - tower artifacts where applicable;
  - threshold window events where applicable;
  - first-hit summaries;
  - timing files;
  - warnings.

Completion criteria:

- artifact completeness can be checked per run.

Stop condition:

- stop if required event domains are missing without explicit policy.

### Phase 5: Aggregation

#### Phase 5.Stage 1: Run And Pair Tables

##### Phase 5.Stage 1.Action 1: Write comparison run index

Action:

- write `comparison_run_index.csv`.

Completion criteria:

- every run has run label, pair id, arm id, candidate id, target id, seed id,
  episode counts, status, and artifact path.

Stop condition:

- stop if run identity is not stable.

##### Phase 5.Stage 1.Action 2: Write paired unit summary

Action:

- write `paired_unit_summary.csv`.

Completion criteria:

- complete and incomplete pair counts are explicit.

Stop condition:

- stop if incomplete pair reasons are unavailable.

#### Phase 5.Stage 2: Arm And Target Summaries

##### Phase 5.Stage 2.Action 1: Write arm summary tables

Action:

- write:
  - `arm_summary.csv`;
  - `baseline_summary.csv`;
  - `candidate_comparison_arm_summary.csv`.

Completion criteria:

- every arm has reward, success, target-hit, first-hit, invalid-move, and status
  fields.

Stop condition:

- stop if baseline/candidate summaries use different metric semantics.

##### Phase 5.Stage 2.Action 2: Write target and learning tables

Action:

- write:
  - `target_hit_summary.csv`;
  - `success_rate_summary.csv`;
  - `first_hit_summary.csv`;
  - `reward_distribution_summary.csv`;
  - `step_efficiency_summary.csv`;
  - `invalid_move_summary.csv`.

Completion criteria:

- target policy results and supporting metrics are table-backed.

Stop condition:

- stop if primary metric directionality is ambiguous.

#### Phase 5.Stage 3: Tower Runtime And Timing Summaries

##### Phase 5.Stage 3.Action 1: Write tower runtime summaries

Action:

- write:
  - `lift_success_by_tier.csv`;
  - `lift_failure_by_tier.csv`;
  - `tier_occupancy_summary.csv`;
  - `training_health_carryforward.csv`.

Completion criteria:

- liftability/runtime caveats are visible in comparison readout.

Stop condition:

- stop if tower runtime failures are only present in raw logs.

##### Phase 5.Stage 3.Action 2: Write timing and artifact completeness summaries

Action:

- write:
  - `timing_summary.csv`;
  - `artifact_completeness_summary.csv`.

Completion criteria:

- artifact completeness and runtime cost are inspectable.

Stop condition:

- stop if missing artifacts cannot be classified.

### Phase 6: Paired Deltas And Claim Logic

#### Phase 6.Stage 1: Compute Paired Comparisons

##### Phase 6.Stage 1.Action 1: Compute paired schema comparison table

Action:

- write `paired_schema_comparison.csv` using complete pair units only for
  paired deltas while retaining incomplete-pair rows with exclusion reason.

Completion criteria:

- paired deltas are not computed from incomplete pairs.

Stop condition:

- stop if paired seeds or pair IDs are inconsistent.

##### Phase 6.Stage 1.Action 2: Validate primary metric from Stage 5

Action:

- confirm the primary metric and directionality come from Stage 5 target policy.

Completion criteria:

- Stage 6 does not choose a new primary metric.

Stop condition:

- stop if target policy lacks directionality.

#### Phase 6.Stage 2: Classify Evidence And Claim Status

##### Phase 6.Stage 2.Action 1: Implement claim classifier

Action:

- create `claim_logic.py`;
- classify comparison as:
  - `positive_signal`;
  - `negative_signal`;
  - `mixed_signal`;
  - `inconclusive`;
  - `blocked`.

Completion criteria:

- classification uses primary metric, supporting metrics, pair completeness,
  and runtime caveats.

Stop condition:

- stop if evidence threshold requires Project Owner decision not encoded in
  config.

##### Phase 6.Stage 2.Action 2: Write comparison claim summary

Action:

- write `comparison_claim_summary.csv` with claim id, baseline, candidate,
  target, primary metric, delta, direction, complete pair count, evidence class,
  claim status, claim sentence, and caveat sentence.

Completion criteria:

- claim language is bounded and does not overstate result.

Stop condition:

- stop if generated claim sentence exceeds allowed scope.

### Phase 7: Manifests And Readout Binding

#### Phase 7.Stage 1: Write Root Stage Artifacts

##### Phase 7.Stage 1.Action 1: Write evaluation manifests

Action:

- write:
  - `evaluation_manifest.json`;
  - `evaluation_stage_manifest.json`;
  - `evaluation_budget_lock.json`;
  - `environment_source_manifest.json`;
  - `candidate_source_manifest.json`;
  - `training_health_source_manifest.json`;
  - `threshold_policy_manifest.json`;
  - `comparison_arm_manifest.json`;
  - `paired_seed_bundle_manifest.json`;
  - `evaluation_run_index.csv`.

Completion criteria:

- all source, arm, target, budget, and seed provenance is manifest-bound.

Stop condition:

- stop if any source path is outside repository.

##### Phase 7.Stage 1.Action 2: Write Stage 6 readout source

Action:

- write:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/paired_replicate_comparison/readout_source.json
```

Completion criteria:

- source binding lists expected files, goal criteria, methodology sources,
  badges, structural/runtime caveats, and claim boundary.

Stop condition:

- stop if readout would need to infer target or candidate source from memory.

#### Phase 7.Stage 2: Write Seed Human Docs

##### Phase 7.Stage 2.Action 1: Write stage docs

Action:

- write or update:
  - `README.md`;
  - `method.md`;
  - `artifact_index.md`;
  - `runbook.md`;
  - `results/summary.md`.

Completion criteria:

- docs explain what was compared, target source, primary baseline, candidate,
  pair completion, primary metric, supporting metrics, runtime caveats, and
  allowed claim.

Stop condition:

- stop if docs claim broad tower superiority.

### Phase 8: CLI Integration

#### Phase 8.Stage 1: Add Paired Comparison Commands

##### Phase 8.Stage 1.Action 1: Add run command

Action:

- add `plate-support standard-gauntlet paired-comparison run`.

Completion criteria:

- command accepts explicit Stage 3, Stage 4, and Stage 5 sources and explicit
  artifact root.

Stop condition:

- stop if command infers latest sources.

##### Phase 8.Stage 1.Action 2: Add summarize/inspect command if consistent

Action:

- add an inspect/summarize command if it matches existing CLI conventions.

Completion criteria:

- command reads comparison artifacts and reports claim status.

Stop condition:

- stop if summarize recomputes claims with different policy.

### Phase 9: Tests And Verification

#### Phase 9.Stage 1: Unit Tests

##### Phase 9.Stage 1.Action 1: Test hard gates

Action:

- test missing candidate manifest, all-untrainable candidates, missing target,
  missing baseline, old dependency semantics, and outside-repo artifact root.

Completion criteria:

- each hard block produces explicit blocked status.

Stop condition:

- stop if dependency/liftability semantics cannot be verified.

##### Phase 9.Stage 1.Action 2: Test paired seed discipline

Action:

- test all arms in a pair unit share required seeds.

Completion criteria:

- seed mismatch fails tests.

Stop condition:

- stop if run IDs cannot map back to seed bundle ids.

##### Phase 9.Stage 1.Action 3: Test incomplete pair exclusion

Action:

- test failed/missing arm rows remain visible and are excluded from paired
  deltas.

Completion criteria:

- incomplete pairs are not silently dropped.

Stop condition:

- stop if aggregation cannot represent incomplete pair reasons.

##### Phase 9.Stage 1.Action 4: Test claim classifier

Action:

- test positive, negative, mixed, inconclusive, and blocked cases.

Completion criteria:

- claim status and sentence remain bounded.

Stop condition:

- stop if evidence thresholds are underspecified.

##### Phase 9.Stage 1.Action 5: Test required tables and readout source

Action:

- test every required table and required readout source field exists after a
  smoke run.

Completion criteria:

- missing artifacts fail tests.

Stop condition:

- stop if expected-file policy is incomplete.

#### Phase 9.Stage 2: Runtime Smoke

##### Phase 9.Stage 2.Action 1: Run Stage 6 smoke comparison

Action:

- run paired comparison against repo-local Stage 3/4/5 sources with a smoke or
  dev budget.

Completion criteria:

- comparison completes, warns, or blocks with explicit reason.

Stop condition:

- stop on unexpected runtime failure or artifact path drift.

##### Phase 9.Stage 2.Action 2: Inspect claim and pair tables

Action:

- inspect `paired_unit_summary.csv`, `paired_schema_comparison.csv`, and
  `comparison_claim_summary.csv`.

Completion criteria:

- claim is supported by pair table and target policy.

Stop condition:

- stop if claim summary cannot be traced to paired data.

#### Phase 9.Stage 3: Final Log Update

##### Phase 9.Stage 3.Action 1: Record validation and Stage 7 handoff

Action:

- update Stage 6 implementation log with:
  - arms compared;
  - target policy;
  - pair completion;
  - primary metric;
  - claim status;
  - runtime caveats;
  - tests run;
  - Stage 7 readout source paths.

Completion criteria:

- log states whether readout/system-learning stage can proceed.

Stop condition:

- stop if claim status is ambiguous.

## Completion Criteria For The Component

Stage 6 is complete when:

- Stage 3, Stage 4, and Stage 5 hard gates are enforced;
- comparison arms are manifest-bound;
- paired seed bundles exist;
- per-run artifacts exist or explicit blocked reasons are written;
- pair, arm, target, learning, runtime, timing, artifact, and claim tables
  exist;
- incomplete pairs remain visible and excluded from paired deltas;
- claim summary uses bounded language;
- readout source and seed docs exist;
- CLI/run surface exists or omission is recorded;
- tests pass;
- implementation log records Phase.Stage.Action completion.

## Handoff To Next Component

Readout and system learning must consume:

```text
results/comparison_claim_summary.csv
results/paired_schema_comparison.csv
results/paired_unit_summary.csv
results/arm_summary.csv
results/target_hit_summary.csv
results/artifact_completeness_summary.csv
readout_source.json
```

It must render Stage 6 as a bounded fixed-run comparison, not as general tower
superiority.
