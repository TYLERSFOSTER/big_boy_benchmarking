# Counterpoint Second Serious Schema Comparison Implementation Gameplan

Date: 2026-06-03

Status: implementation gameplan, not executed

Repository:

```text
/Users/foster/big_boy_benchmarking
```

Source blueprint:

```text
docs/design/first_counterpoint_environment/second_counterpoint_serious_evaluation/01_001_counterpoint_second_serious_schema_comparison_blueprint.md
```

## Purpose

This gameplan translates the second serious counterpoint schema-comparison
blueprint into Phase.Stage.Action implementation work.

The target evaluation is:

```text
counterpoint_second_serious_schema_comparison_v001
```

The evaluation compares training under two schema conditions:

```text
Schema 0: no contraction / total-space only
Schema 1: one-drop noisy-rate quotient, tiers 0 and 1
```

The primary measurement is:

```text
first sustained total-space hit
```

using:

```text
metric: episode_total_reward
persistence rule: 4 of 5 rolling episodes at or above a locked threshold
```

The serious run is intended to use:

```text
environment: counterpoint_symbolic_v001
serious fixture: medium
Schema 1 candidate count: 4
episodes per replicate: 256 to start
linearization mode: tensor_available_disabled
```

This gameplan creates the path to implement the evaluation. It does not
authorize source edits, benchmark artifact runs, or the serious locked budget
until the Project Owner explicitly requests execution of this exact gameplan.

## Execution Authority Status

The Project Owner requested this gameplan:

```text
Follow `prime_directive` to write Phase.Stage.Action implemetation gameplan for
this:
`docs/design/first_counterpoint_environment/second_counterpoint_serious_evaluation/01_001_counterpoint_second_serious_schema_comparison_blueprint.md`
```

Therefore this document may be written now.

This instruction is not implementation approval.

If the Project Owner later says to execute this gameplan, implementation should
follow this document as written. If any Phase.Stage.Action item cannot be
implemented as written, stop and ask for Project Owner guidance before
substituting, simplifying, or reordering.

## Source Authority

This gameplan follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/git_practices.md`
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`
- `docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md`
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`
- `docs/design/first_counterpoint_environment/second_counterpoint_serious_evaluation/design_discussion.md`
- `docs/design/first_counterpoint_environment/second_counterpoint_serious_evaluation/01_001_counterpoint_second_serious_schema_comparison_blueprint.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/02_counterpoint_noisy_rate_contraction_diagnostics_blueprint.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic/01_counterpoint_noisy_rate_full_tower_training_diagnostic_blueprint.md`
- `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json`
- `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json`
- current BBB counterpoint source, noisy-rate source, full-tower training
  source, artifact writer source, CLI source, docs-writer source, and tests as
  read-only implementation context.

## PO Attribution Preservation

This gameplan preserves the blueprint's Project Owner-originated design locks.
It does not invent Project Owner turns.

Project Owner-originated locks carried into implementation:

1. This is a serious new evaluation in the existing counterpoint environment.
2. The comparison is training under two contraction schemata with all other
   hyperparameters/knobs as equivalent as possible.
3. Schema 0 is no contraction; the agent stays in total space.
4. Schema 1 comes from the noisy-rate diagnostic / noisy-rate full-tower
   training diagnostic lineage.
5. Schema 1 may do only one drop, yielding tiers 0 and 1.
6. The evaluation needs a reward-cutoff / tier-jump knob and an upperbound
   interpretation.
7. The primary comparison should measure staying above a certain level
   consistently.
8. Both schema conditions need the same threshold for comparison.
9. Use a few carried-over Schema 1 candidates; the Project Owner later answered
   `4`.
10. Omit a separate old direct-tabular-Q sanity anchor from the primary
    comparison; keep the comparison clean.
11. Use `256` episodes to start for the serious run.
12. The fixture answer was `medium`.

Consultant-authored implementation defaults carried from the blueprint:

- primitive adequacy metric: `episode_total_reward`;
- threshold policy: calibration-derived absolute reward threshold, locked
  before the serious run;
- persistence rule: `4` of `5` rolling episodes at or above threshold;
- Schema 0 should be represented in the matched comparison harness rather than
  by reusing an old direct-runner path;
- candidate selection should prefer the full-tower training diagnostic source
  and preserve provenance to the noisy-rate contraction diagnostic source.

## Important Candidate/Fixure Decision Gate

The Project Owner selected `medium` for the serious comparison.

The currently checked-in noisy-rate full-tower training diagnostic readout is a
`smoke_001` result with two `small` `p001_over_144` candidates.

Therefore, implementation must not pretend four `medium` Schema 1 candidates
already exist in that source.

This gameplan allows implementation of the evaluation machinery, calibration,
source validation, and smoke runs. Before any serious `medium` locked run, the
implementation must verify that the candidate source provides four eligible
`medium` one-drop Schema 1 candidates, or stop and ask the Project Owner which
candidate source expansion is authorized.

## Fixed Design Locks

### Environment Lock

Do not change:

```text
counterpoint_symbolic_v001
```

Do not alter:

- state enumeration;
- action enumeration;
- legality contract;
- reward semantics;
- terminal policy;
- initial-state policy;
- action-mask policy;
- noisy-rate parent diagnostics;
- `/Users/foster/state_collapser`.

### Comparison Lock

The evaluation compares schema conditions.

Do not convert the comparison into:

- old direct tabular Q versus tower runtime;
- masked random versus tower runtime;
- direct-vs-tower generic benchmark;
- structural collapse diagnostic;
- noisy-rate candidate-selection diagnostic;
- final reward leaderboard;
- broad abstraction superiority claim.

### Matched Harness Lock

Implementation must hold fixed wherever possible:

- learner family;
- training seed bundles;
- exploration policy;
- horizon;
- episode budget;
- threshold policy;
- persistence policy;
- artifact schema;
- aggregation logic;
- readout protocol;
- linearization mode.

Schema 0 and Schema 1 may differ only where the schema itself forces a
difference: quotient/tier structure, schema-dependent controller events,
Schema 1 lift/fiber evidence, and tier-transition evidence.

### Threshold Lock

Both schema classes must use the same threshold policy:

```text
metric_id: episode_total_reward
persistence_rule: 4_of_5
comparison: greater_than_or_equal
scope: total_space
```

The numeric threshold is calibration-derived and must be locked before the
serious run. Do not choose or tune it after inspecting serious-run outcomes.

### Artifact Lock

Durable artifacts must be repo-resident under:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/<run-label>/
```

The repo-side readout source must be:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/readout_source.json
```

Do not write durable human-readable readouts into scratch directories or raw
evaluation roots.

### TeX Lock

Do not modify:

```text
tropicalization_and_binary_coset_towers.tex
tropicalization_and_binary_coset_towers.pdf
logHRL.bib
```

or TeX-generated sidecars during this evaluation implementation unless the
Project Owner explicitly authorizes TeX work.

## Stop Conditions

Stop and ask the Project Owner if:

- execution of this gameplan has not been explicitly approved;
- working tree state would mix unrelated TeX/root document changes into this
  implementation;
- a source edit would touch `/Users/foster/state_collapser`;
- a source edit would change `counterpoint_symbolic_v001`;
- Schema 0 cannot be represented in the matched comparison harness;
- Schema 0 would require silently reusing the old direct runner as the primary
  comparison arm;
- Schema 1 candidate source cannot provide eligible candidates;
- the serious `medium` run lacks four eligible `medium` Schema 1 candidates;
- threshold calibration would require looking at serious-run outcomes;
- the 4-of-5 persistence rule cannot be computed from emitted episode rows;
- learner state cannot persist across episodes;
- artifact files required by the blueprint cannot be written;
- expected-file policy cannot honestly classify Schema 0 not-applicable tower
  files;
- readout source binding cannot be generated;
- result docs would need to infer intent from code rather than source binding;
- implementation would omit goal criteria, methodology sources, claim boundary,
  badge policy, or structural limit checks;
- a serious or medium budget run is about to be executed without explicit
  Project Owner authorization.

## Phase.Stage.Action Workplan

### Phase 0: Authority, Branch, And Reality Check

#### Phase 0. Stage 0: Execution Authority

- Phase 0. Stage 0. Action 1: Confirm the Project Owner has explicitly asked
  to execute this exact gameplan.
- Phase 0. Stage 0. Action 2: If execution authority is absent, stop before
  source edits.
- Phase 0. Stage 0. Action 3: Record the exact execution instruction in the
  implementation log.
- Phase 0. Stage 0. Action 4: Record that this gameplan itself was requested
  on 2026-06-03 but was not implementation approval.

#### Phase 0. Stage 1: Working Tree And Branch Discipline

- Phase 0. Stage 1. Action 1: Run `git status --short --branch`.
- Phase 0. Stage 1. Action 2: Identify all unrelated dirty files, especially
  root TeX files, generated TeX sidecars, bibliography files, and evaluation
  README conversation changes.
- Phase 0. Stage 1. Action 3: Stop if unrelated dirty state would be touched,
  staged, reverted, or mixed into this implementation.
- Phase 0. Stage 1. Action 4: Create and switch to:

  ```text
  codex/second-serious-schema-comparison
  ```

- Phase 0. Stage 1. Action 5: Record branch creation and initial dirty state
  in the implementation log.

#### Phase 0. Stage 2: Source Re-Read

- Phase 0. Stage 2. Action 1: Re-read Prime Directive source authority listed
  in this gameplan.
- Phase 0. Stage 2. Action 2: Re-read the source blueprint.
- Phase 0. Stage 2. Action 3: Re-read the design discussion.
- Phase 0. Stage 2. Action 4: Re-read noisy-rate contraction diagnostic source
  binding and readout docs.
- Phase 0. Stage 2. Action 5: Re-read noisy-rate full-tower training source
  binding and readout docs.
- Phase 0. Stage 2. Action 6: Re-read current `noisy_rate_full_training`
  package for reusable candidate selection, runner, aggregation, docs, and
  tests.
- Phase 0. Stage 2. Action 7: Re-read current serious-learning package for
  prior calibration/run/summarize shape.
- Phase 0. Stage 2. Action 8: Re-read CLI command registration and relevant
  counterpoint tests.
- Phase 0. Stage 2. Action 9: Record source surface mapping in the
  implementation log.

#### Phase 0. Stage 3: Implementation Log

- Phase 0. Stage 3. Action 1: Create:

  ```text
  docs/design/first_counterpoint_environment/second_counterpoint_serious_evaluation/01_003_counterpoint_second_serious_schema_comparison_implementation_log.md
  ```

- Phase 0. Stage 3. Action 2: Include branch, execution instruction, source
  gameplan, initial dirty state, stop conditions, and running
  Phase.Stage.Action checklist.
- Phase 0. Stage 3. Action 3: Keep the log updated throughout implementation.

### Phase 1: Evaluation Identity, Package, Config, And Paths

#### Phase 1. Stage 1: Evaluation Constants

- Phase 1. Stage 1. Action 1: Add evaluation id:

  ```text
  counterpoint_second_serious_schema_comparison_v001
  ```

- Phase 1. Stage 1. Action 2: Add run family id:

  ```text
  counterpoint_symbolic_v001_second_serious_schema_comparison_v001
  ```

- Phase 1. Stage 1. Action 3: Add run mode ids:

  ```text
  calibration
  serious_schema_comparison_first_sustained_hit
  smoke_schema_comparison_first_sustained_hit
  ```

- Phase 1. Stage 1. Action 4: Add schema class ids:

  ```text
  schema0_no_contraction
  schema1_noisy_rate_one_drop
  ```

- Phase 1. Stage 1. Action 5: Keep all existing counterpoint ids unchanged.
- Phase 1. Stage 1. Action 6: Add tests proving new ids are exported and do
  not collide with existing ids.

#### Phase 1. Stage 2: Package Scaffold

- Phase 1. Stage 2. Action 1: Create package:

  ```text
  src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/
  ```

- Phase 1. Stage 2. Action 2: Add `__init__.py`.
- Phase 1. Stage 2. Action 3: Add `config.py`.
- Phase 1. Stage 2. Action 4: Add `paths.py`.
- Phase 1. Stage 2. Action 5: Add `thresholds.py`.
- Phase 1. Stage 2. Action 6: Add `candidates.py`.
- Phase 1. Stage 2. Action 7: Add `arms.py`.
- Phase 1. Stage 2. Action 8: Add `events.py`.
- Phase 1. Stage 2. Action 9: Add `manifests.py`.
- Phase 1. Stage 2. Action 10: Add `runner.py`.
- Phase 1. Stage 2. Action 11: Add `aggregation.py`.
- Phase 1. Stage 2. Action 12: Add `docs_writer.py`.

#### Phase 1. Stage 3: Budget Configuration

- Phase 1. Stage 3. Action 1: Define `SecondSeriousComparisonBudget`.
- Phase 1. Stage 3. Action 2: Include `environment_instance_id`.
- Phase 1. Stage 3. Action 3: Include `candidate_readout_source`.
- Phase 1. Stage 3. Action 4: Include `candidate_cap`.
- Phase 1. Stage 3. Action 5: Include `episodes_per_replicate`.
- Phase 1. Stage 3. Action 6: Include `training_replicates_per_arm`.
- Phase 1. Stage 3. Action 7: Include matched training seed policy.
- Phase 1. Stage 3. Action 8: Include `threshold_policy`.
- Phase 1. Stage 3. Action 9: Include `tier_jump_policy`.
- Phase 1. Stage 3. Action 10: Include `linearization_mode_id`.
- Phase 1. Stage 3. Action 11: Include `locked_by`.
- Phase 1. Stage 3. Action 12: Define smoke defaults:

  ```text
  instance: small or tiny, depending on available candidate source
  candidate cap: 1
  replicates: 1
  episodes: 4-8
  threshold policy: explicit smoke threshold or calibration-derived test value
  ```

- Phase 1. Stage 3. Action 13: Define calibration defaults:

  ```text
  candidate cap: 2 unless overridden
  replicates: 2-4
  episodes: 32-64
  ```

- Phase 1. Stage 3. Action 14: Define serious defaults:

  ```text
  instance: medium
  candidate cap: 4
  episodes: 256
  threshold: locked from calibration
  ```

- Phase 1. Stage 3. Action 15: Mark the serious run as decision-locked until
  explicit Project Owner authorization.

#### Phase 1. Stage 4: Path Contracts

- Phase 1. Stage 4. Action 1: Define repo readout surface:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/
  ```

- Phase 1. Stage 4. Action 2: Define default artifact root under:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/<run-label>/
  ```

- Phase 1. Stage 4. Action 3: Define evaluation root under:

  ```text
  <artifact-root>/evaluations/counterpoint_second_serious_schema_comparison_v001/
  ```

- Phase 1. Stage 4. Action 4: Add repo-resident path validation.
- Phase 1. Stage 4. Action 5: Add source binding path validation.
- Phase 1. Stage 4. Action 6: Add tests for default paths and outside-repo
  rejection.

### Phase 2: Threshold, Persistence, And Calibration Model

#### Phase 2. Stage 1: Threshold Policy Model

- Phase 2. Stage 1. Action 1: Define `ThresholdPolicy`.
- Phase 2. Stage 1. Action 2: Include `threshold_policy_id`.
- Phase 2. Stage 1. Action 3: Include `metric_id`, locked to
  `episode_total_reward`.
- Phase 2. Stage 1. Action 4: Include numeric `threshold_value`.
- Phase 2. Stage 1. Action 5: Include `window_length`, default `5`.
- Phase 2. Stage 1. Action 6: Include `required_count`, default `4`.
- Phase 2. Stage 1. Action 7: Include comparison `greater_than_or_equal`.
- Phase 2. Stage 1. Action 8: Include scope `total_space`.
- Phase 2. Stage 1. Action 9: Include applicable schema classes.
- Phase 2. Stage 1. Action 10: Write `threshold_policy_manifest.json` in
  every run and evaluation root.

#### Phase 2. Stage 2: First-Hit Computation

- Phase 2. Stage 2. Action 1: Implement first transient hit detection.
- Phase 2. Stage 2. Action 2: Implement rolling 4-of-5 sustained-hit
  detection.
- Phase 2. Stage 2. Action 3: Define hit status `sustained_hit`.
- Phase 2. Stage 2. Action 4: Define hit status `transient_hit_only`.
- Phase 2. Stage 2. Action 5: Define hit status `never_hit`.
- Phase 2. Stage 2. Action 6: Define hit status `artifact_incomplete`.
- Phase 2. Stage 2. Action 7: Define hit status `runtime_failed`.
- Phase 2. Stage 2. Action 8: Define hit status `structural_blocked`.
- Phase 2. Stage 2. Action 9: Emit `threshold_window_events.csv`.
- Phase 2. Stage 2. Action 10: Emit `first_hit_summary.json`.
- Phase 2. Stage 2. Action 11: Add unit tests for sustained, transient-only,
  never-hit, and empty-artifact cases.

#### Phase 2. Stage 3: Calibration Recommendation

- Phase 2. Stage 3. Action 1: Implement calibration run mode.
- Phase 2. Stage 3. Action 2: Aggregate calibration episode reward
  distributions.
- Phase 2. Stage 3. Action 3: Compute candidate threshold recommendations
  without looking at serious-run outcomes.
- Phase 2. Stage 3. Action 4: Write `calibration_summary.json`.
- Phase 2. Stage 3. Action 5: Write `calibration_run_index.csv`.
- Phase 2. Stage 3. Action 6: Write `calibration_recommendation.md`.
- Phase 2. Stage 3. Action 7: Require the serious `run` command to receive an
  explicit locked threshold value.
- Phase 2. Stage 3. Action 8: Stop if serious run is attempted without locked
  threshold policy.

### Phase 3: Candidate Source And Schema Arm Construction

#### Phase 3. Stage 1: Candidate Source Loader

- Phase 3. Stage 1. Action 1: Load full-tower training diagnostic
  `readout_source.json`.
- Phase 3. Stage 1. Action 2: Validate it is repo-resident.
- Phase 3. Stage 1. Action 3: Resolve its source evaluation root.
- Phase 3. Stage 1. Action 4: Read its candidate summary.
- Phase 3. Stage 1. Action 5: Read its training-health summary.
- Phase 3. Stage 1. Action 6: Read its tower-shape summary.
- Phase 3. Stage 1. Action 7: Resolve parent noisy-rate contraction
  provenance from that source binding.
- Phase 3. Stage 1. Action 8: Stop if required source files are missing.

#### Phase 3. Stage 2: Medium Candidate Gate

- Phase 3. Stage 2. Action 1: Check whether the source contains eligible
  candidates for `counterpoint_symbolic_n3_medium_v001`.
- Phase 3. Stage 2. Action 2: Check whether at least four eligible medium
  Schema 1 candidates are available.
- Phase 3. Stage 2. Action 3: If four medium candidates are unavailable, allow
  implementation smoke on available candidates but block serious medium run.
- Phase 3. Stage 2. Action 4: Record the candidate-source insufficiency in the
  implementation log.
- Phase 3. Stage 2. Action 5: Ask the Project Owner whether to authorize a
  medium candidate-health expansion, a smaller candidate count, or a small
  fixture comparison.

#### Phase 3. Stage 3: Candidate Row Model

- Phase 3. Stage 3. Action 1: Define `SchemaCandidate`.
- Phase 3. Stage 3. Action 2: Include candidate id.
- Phase 3. Stage 3. Action 3: Include instance id.
- Phase 3. Stage 3. Action 4: Include arm id.
- Phase 3. Stage 3. Action 5: Include numerator and denominator.
- Phase 3. Stage 3. Action 6: Include requested rate.
- Phase 3. Stage 3. Action 7: Include schema seed.
- Phase 3. Stage 3. Action 8: Include tier state-cell-count sequence.
- Phase 3. Stage 3. Action 9: Include tier active-action-cell-count sequence.
- Phase 3. Stage 3. Action 10: Include parent training-health class.
- Phase 3. Stage 3. Action 11: Include concrete-step evidence.
- Phase 3. Stage 3. Action 12: Include learner-update evidence.
- Phase 3. Stage 3. Action 13: Add CSV/JSON serialization.

#### Phase 3. Stage 4: Schema 1 Candidate Selection

- Phase 3. Stage 4. Action 1: Exclude no-contraction controls.
- Phase 3. Stage 4. Action 2: Exclude failed parent rows.
- Phase 3. Stage 4. Action 3: Exclude candidates without non-base tier.
- Phase 3. Stage 4. Action 4: Exclude collapsed tier 1 candidates.
- Phase 3. Stage 4. Action 5: Exclude non-executable tier 1 candidates.
- Phase 3. Stage 4. Action 6: Exclude candidates lacking training-health
  evidence unless Project Owner authorizes an expansion pass.
- Phase 3. Stage 4. Action 7: Sort deterministically by instance id, rate,
  schema seed, candidate id.
- Phase 3. Stage 4. Action 8: Apply candidate cap after sorting.
- Phase 3. Stage 4. Action 9: Write selected and excluded candidates to
  `candidate_manifest.json`.

#### Phase 3. Stage 5: Schema 0 Arm Definition

- Phase 3. Stage 5. Action 1: Define Schema 0 as `schema0_no_contraction`.
- Phase 3. Stage 5. Action 2: Represent Schema 0 in the same comparison
  harness wherever feasible.
- Phase 3. Stage 5. Action 3: Ensure Schema 0 uses the same learner,
  threshold policy, seed bundle, budget, and artifact writer as Schema 1.
- Phase 3. Stage 5. Action 4: Mark tier-jump, lift, and Schema 1-specific
  tower files as not applicable or structurally absent for Schema 0 when
  appropriate.
- Phase 3. Stage 5. Action 5: Add a harness-mismatch check that blocks
  comparison claims if Schema 0 is implemented through an incompatible direct
  path.

### Phase 4: Matched Training Runtime

#### Phase 4. Stage 1: Shared Run Context

- Phase 4. Stage 1. Action 1: Define a shared run context for both schema
  classes.
- Phase 4. Stage 1. Action 2: Include environment instance id.
- Phase 4. Stage 1. Action 3: Include horizon.
- Phase 4. Stage 1. Action 4: Include learner configuration.
- Phase 4. Stage 1. Action 5: Include exploration policy.
- Phase 4. Stage 1. Action 6: Include threshold policy.
- Phase 4. Stage 1. Action 7: Include tier-jump policy.
- Phase 4. Stage 1. Action 8: Include seed bundle.
- Phase 4. Stage 1. Action 9: Include linearization mode.

#### Phase 4. Stage 2: Persistent Learner Semantics

- Phase 4. Stage 2. Action 1: Create one learner object per training
  replicate.
- Phase 4. Stage 2. Action 2: Preserve learner state across all episodes in a
  replicate.
- Phase 4. Stage 2. Action 3: Reset environment/runtime episode state between
  episodes.
- Phase 4. Stage 2. Action 4: Preserve threshold and tier-jump policy across
  the replicate.
- Phase 4. Stage 2. Action 5: Record learner-update events for both schema
  classes where available.
- Phase 4. Stage 2. Action 6: Add tests proving learner state persists across
  episodes.

#### Phase 4. Stage 3: Schema 1 Tower Runtime

- Phase 4. Stage 3. Action 1: Reuse the one-drop noisy-rate tower construction
  path from full-tower training diagnostics.
- Phase 4. Stage 3. Action 2: Rebuild each candidate tower from manifest
  fields.
- Phase 4. Stage 3. Action 3: Verify rebuilt tier shape matches the candidate
  manifest.
- Phase 4. Stage 3. Action 4: Use the active-tier control runtime already
  validated by full-tower training diagnostics.
- Phase 4. Stage 3. Action 5: Emit tier, lift, ABC, concrete-step, learner,
  and threshold events.
- Phase 4. Stage 3. Action 6: Stop if tower shape cannot be reproduced.

#### Phase 4. Stage 4: Schema 0 Runtime

- Phase 4. Stage 4. Action 1: Implement no-contraction schema arm in the
  matched comparison harness.
- Phase 4. Stage 4. Action 2: Ensure Schema 0 acts in total space for the
  entire run.
- Phase 4. Stage 4. Action 3: Ensure Schema 0 records the same episode reward,
  learner, threshold, timing, seed, and run-manifest fields as Schema 1.
- Phase 4. Stage 4. Action 4: Emit Schema 0 structural not-applicable markers
  for tier/lift files if those files are absent.
- Phase 4. Stage 4. Action 5: Stop if the only feasible Schema 0 path is an
  incompatible direct-runner implementation.

#### Phase 4. Stage 5: Tier-Jump Policy

- Phase 4. Stage 5. Action 1: Define `TierJumpPolicy`.
- Phase 4. Stage 5. Action 2: Include reward cutoff.
- Phase 4. Stage 5. Action 3: Include metric id.
- Phase 4. Stage 5. Action 4: Include window length or disabled reason.
- Phase 4. Stage 5. Action 5: Record applicability to Schema 0 and Schema 1.
- Phase 4. Stage 5. Action 6: Write `tier_jump_policy_manifest.json`.
- Phase 4. Stage 5. Action 7: Emit tier-transition events for Schema 1.
- Phase 4. Stage 5. Action 8: Record Schema 0 tier-jump non-applicability.

### Phase 5: Event Rows And Artifact Writers

#### Phase 5. Stage 1: Event Row Types

- Phase 5. Stage 1. Action 1: Define run index row.
- Phase 5. Stage 1. Action 2: Define arm summary row.
- Phase 5. Stage 1. Action 3: Define candidate summary row.
- Phase 5. Stage 1. Action 4: Define episode row.
- Phase 5. Stage 1. Action 5: Define step event row.
- Phase 5. Stage 1. Action 6: Define threshold window event row.
- Phase 5. Stage 1. Action 7: Define first sustained hit summary row.
- Phase 5. Stage 1. Action 8: Define paired schema comparison row.
- Phase 5. Stage 1. Action 9: Define comparison claim summary row.
- Phase 5. Stage 1. Action 10: Define tower/tier/lift/ABC rows by reusing or
  adapting existing counterpoint row models.
- Phase 5. Stage 1. Action 11: Add fieldname tests for required tables.

#### Phase 5. Stage 2: Evaluation-Level Manifests

- Phase 5. Stage 2. Action 1: Write `evaluation_manifest.json`.
- Phase 5. Stage 2. Action 2: Write `evaluation_arm_manifest.json`.
- Phase 5. Stage 2. Action 3: Write `evaluation_budget_lock.json`.
- Phase 5. Stage 2. Action 4: Write `threshold_policy_manifest.json`.
- Phase 5. Stage 2. Action 5: Write `candidate_manifest.json`.
- Phase 5. Stage 2. Action 6: Write `parent_source_manifest.json`.
- Phase 5. Stage 2. Action 7: Write `evaluation_run_index.csv`.
- Phase 5. Stage 2. Action 8: Write `evaluation_aggregate_table.csv` during
  summarization.
- Phase 5. Stage 2. Action 9: Write `evaluation_aggregate_summary.json` during
  summarization.
- Phase 5. Stage 2. Action 10: Write `readout_source.json` in both source
  evaluation root and repo readout surface.

#### Phase 5. Stage 3: Per-Run Artifact Writer

- Phase 5. Stage 3. Action 1: Write `run_manifest.json`.
- Phase 5. Stage 3. Action 2: Write `seed_bundle.json`.
- Phase 5. Stage 3. Action 3: Write `mode_manifest.json`.
- Phase 5. Stage 3. Action 4: Write `linearization_manifest.json`.
- Phase 5. Stage 3. Action 5: Write `schema_manifest.json`.
- Phase 5. Stage 3. Action 6: Write `threshold_policy_manifest.json`.
- Phase 5. Stage 3. Action 7: Write `tier_jump_policy_manifest.json`.
- Phase 5. Stage 3. Action 8: Write `episodes.csv`.
- Phase 5. Stage 3. Action 9: Write `step_events.csv`.
- Phase 5. Stage 3. Action 10: Write `control_events.csv` when applicable.
- Phase 5. Stage 3. Action 11: Write `tier_transition_events.csv` when
  applicable.
- Phase 5. Stage 3. Action 12: Write `lift_fiber_events.csv` when applicable.
- Phase 5. Stage 3. Action 13: Write `abc_selection_events.csv` when
  applicable.
- Phase 5. Stage 3. Action 14: Write `abc_tier_signal_events.csv` when
  applicable.
- Phase 5. Stage 3. Action 15: Write `learner_update_events.csv`.
- Phase 5. Stage 3. Action 16: Write `threshold_window_events.csv`.
- Phase 5. Stage 3. Action 17: Write `first_hit_summary.json`.
- Phase 5. Stage 3. Action 18: Write `timing_segments.csv`.
- Phase 5. Stage 3. Action 19: Write `timing_summary.json`.
- Phase 5. Stage 3. Action 20: Write or touch `warnings.jsonl`.

### Phase 6: Aggregation And Comparison

#### Phase 6. Stage 1: Aggregation Reader

- Phase 6. Stage 1. Action 1: Read `evaluation_run_index.csv`.
- Phase 6. Stage 1. Action 2: For successful runs, read all required per-run
  files.
- Phase 6. Stage 1. Action 3: For failed runs, emit failed aggregate rows.
- Phase 6. Stage 1. Action 4: Apply expected-file policy to Schema 0
  not-applicable tower files.
- Phase 6. Stage 1. Action 5: Stop if required files are missing without
  expected-file classification.

#### Phase 6. Stage 2: Result Tables

- Phase 6. Stage 2. Action 1: Write `results/arm_summary.csv`.
- Phase 6. Stage 2. Action 2: Write `results/candidate_summary.csv`.
- Phase 6. Stage 2. Action 3: Write `results/schema_summary.csv`.
- Phase 6. Stage 2. Action 4: Write `results/training_episode_summary.csv`.
- Phase 6. Stage 2. Action 5: Write `results/training_curve_summary.csv`.
- Phase 6. Stage 2. Action 6: Write `results/threshold_window_summary.csv`.
- Phase 6. Stage 2. Action 7: Write
  `results/first_sustained_hit_summary.csv`.
- Phase 6. Stage 2. Action 8: Write `results/paired_schema_comparison.csv`.
- Phase 6. Stage 2. Action 9: Write
  `results/schema0_total_space_summary.csv`.
- Phase 6. Stage 2. Action 10: Write
  `results/schema1_candidate_summary.csv`.
- Phase 6. Stage 2. Action 11: Write `results/tower_shape_summary.csv`.
- Phase 6. Stage 2. Action 12: Write `results/tier_occupancy_summary.csv`.
- Phase 6. Stage 2. Action 13: Write
  `results/tier_executability_summary.csv`.
- Phase 6. Stage 2. Action 14: Write `results/lift_success_by_tier.csv`.
- Phase 6. Stage 2. Action 15: Write `results/lift_failure_by_tier.csv`.
- Phase 6. Stage 2. Action 16: Write `results/concrete_step_summary.csv`.
- Phase 6. Stage 2. Action 17: Write
  `results/controller_action_summary.csv`.
- Phase 6. Stage 2. Action 18: Write `results/abc_selection_summary.csv`.
- Phase 6. Stage 2. Action 19: Write `results/abc_tier_signal_summary.csv`.
- Phase 6. Stage 2. Action 20: Write `results/learner_update_summary.csv`.
- Phase 6. Stage 2. Action 21: Write `results/timing_summary.csv`.
- Phase 6. Stage 2. Action 22: Write `results/training_health_summary.csv`.
- Phase 6. Stage 2. Action 23: Write
  `results/comparison_claim_summary.csv`.

#### Phase 6. Stage 3: Pairing

- Phase 6. Stage 3. Action 1: Pair Schema 0 and Schema 1 rows by environment
  instance id, training seed bundle id, learner config id, threshold policy id,
  budget id, and candidate group id.
- Phase 6. Stage 3. Action 2: Compute paired hit-status comparison.
- Phase 6. Stage 3. Action 3: Compute paired episodes-to-hit delta.
- Phase 6. Stage 3. Action 4: Compute paired training-step-to-hit delta.
- Phase 6. Stage 3. Action 5: Mark pairs as claim-blocked when either run is
  artifact incomplete, structurally blocked, or harness mismatched.
- Phase 6. Stage 3. Action 6: Write pair-level interpretation text fields.

#### Phase 6. Stage 4: Claim Summary

- Phase 6. Stage 4. Action 1: Count sustained-hit runs by schema class.
- Phase 6. Stage 4. Action 2: Compute sustained-hit rate by schema class.
- Phase 6. Stage 4. Action 3: Compute median episodes to hit by schema class.
- Phase 6. Stage 4. Action 4: Compute median paired delta by candidate.
- Phase 6. Stage 4. Action 5: Compute overall candidate-set median paired
  delta.
- Phase 6. Stage 4. Action 6: Count Schema 1 faster pairs.
- Phase 6. Stage 4. Action 7: Count Schema 1 slower pairs.
- Phase 6. Stage 4. Action 8: Count same-status pairs.
- Phase 6. Stage 4. Action 9: Count mixed or blocked pairs.
- Phase 6. Stage 4. Action 10: Emit bounded claim text only when claim gates
  are met.

#### Phase 6. Stage 5: Structural Limit Checks

- Phase 6. Stage 5. Action 1: Implement `schema1_collapsed_tier`.
- Phase 6. Stage 5. Action 2: Implement `schema1_non_executable_tier`.
- Phase 6. Stage 5. Action 3: Implement `schema1_no_tier1_use`.
- Phase 6. Stage 5. Action 4: Implement `schema1_lift_failure_dominant`.
- Phase 6. Stage 5. Action 5: Implement `schema0_harness_mismatch`.
- Phase 6. Stage 5. Action 6: Implement `threshold_unreached_all`.
- Phase 6. Stage 5. Action 7: Implement `threshold_saturated_immediately`.
- Phase 6. Stage 5. Action 8: Implement `artifact_incomplete`.
- Phase 6. Stage 5. Action 9: Add tests for each structural limit
  classification.

### Phase 7: Source Binding, Docs, And Readout

#### Phase 7. Stage 1: Source Binding Payload

- Phase 7. Stage 1. Action 1: Implement `readout_source.json` payload.
- Phase 7. Stage 1. Action 2: Include repo readout surface.
- Phase 7. Stage 1. Action 3: Include source artifact root.
- Phase 7. Stage 1. Action 4: Include source evaluation root.
- Phase 7. Stage 1. Action 5: Include evaluation id.
- Phase 7. Stage 1. Action 6: Include run mode.
- Phase 7. Stage 1. Action 7: Include source files.
- Phase 7. Stage 1. Action 8: Include expected-file policy.
- Phase 7. Stage 1. Action 9: Include goal criteria.
- Phase 7. Stage 1. Action 10: Include badge policy.
- Phase 7. Stage 1. Action 11: Include goal summary sources.
- Phase 7. Stage 1. Action 12: Include methodology summary sources.
- Phase 7. Stage 1. Action 13: Include structural limit checks.
- Phase 7. Stage 1. Action 14: Include claim boundary.

#### Phase 7. Stage 2: Docs Writer

- Phase 7. Stage 2. Action 1: Write repo-side `README.md`.
- Phase 7. Stage 2. Action 2: Write `method.md`.
- Phase 7. Stage 2. Action 3: Write `runbook.md`.
- Phase 7. Stage 2. Action 4: Write `artifact_index.md`.
- Phase 7. Stage 2. Action 5: Write `glossary.md`.
- Phase 7. Stage 2. Action 6: Write `result_readout.md`.
- Phase 7. Stage 2. Action 7: Write `results/summary.md`.
- Phase 7. Stage 2. Action 8: Write `results/human_summary.md`.
- Phase 7. Stage 2. Action 9: Write `results/arm_readout_table.md`.
- Phase 7. Stage 2. Action 10: Write `results/diagnostic_findings.md`.
- Phase 7. Stage 2. Action 11: Write
  `results/paired_comparison_readout.md`.
- Phase 7. Stage 2. Action 12: Write
  `results/threshold_policy_readout.md`.
- Phase 7. Stage 2. Action 13: Write `results/timing_readout.md`.
- Phase 7. Stage 2. Action 14: Write local SVG badges.
- Phase 7. Stage 2. Action 15: Preserve README clarification turns on
  regeneration.

#### Phase 7. Stage 3: README Content Gates

- Phase 7. Stage 3. Action 1: README must include local badge strip.
- Phase 7. Stage 3. Action 2: README must include `Status At A Glance`.
- Phase 7. Stage 3. Action 3: README must include `Summary of Goals Behind
  this Evaluation`.
- Phase 7. Stage 3. Action 4: README must include `Summary of Methodology
  Behind this Evaluation`.
- Phase 7. Stage 3. Action 5: README must include schema-arm table.
- Phase 7. Stage 3. Action 6: README must include first sustained hit summary.
- Phase 7. Stage 3. Action 7: README must include paired comparison summary.
- Phase 7. Stage 3. Action 8: README must include claim boundary.
- Phase 7. Stage 3. Action 9: README must include canonical readout command.
- Phase 7. Stage 3. Action 10: README must include clarification turn section.

### Phase 8: CLI

#### Phase 8. Stage 1: CLI Registration

- Phase 8. Stage 1. Action 1: Import second-serious config defaults.
- Phase 8. Stage 1. Action 2: Import path helpers.
- Phase 8. Stage 1. Action 3: Import calibration runner.
- Phase 8. Stage 1. Action 4: Import serious runner.
- Phase 8. Stage 1. Action 5: Import aggregation.
- Phase 8. Stage 1. Action 6: Import docs writer.
- Phase 8. Stage 1. Action 7: Register CLI group:

  ```text
  counterpoint second-serious-comparison
  ```

#### Phase 8. Stage 2: Calibrate Command

- Phase 8. Stage 2. Action 1: Add `calibrate` subcommand.
- Phase 8. Stage 2. Action 2: Add `--artifact-root`.
- Phase 8. Stage 2. Action 3: Add `--candidate-readout-source`.
- Phase 8. Stage 2. Action 4: Add `--candidate-cap`.
- Phase 8. Stage 2. Action 5: Add `--instance-id`.
- Phase 8. Stage 2. Action 6: Add `--episodes`.
- Phase 8. Stage 2. Action 7: Add `--replicates`.
- Phase 8. Stage 2. Action 8: Add `--base-seed`.
- Phase 8. Stage 2. Action 9: Add `--locked-by`.
- Phase 8. Stage 2. Action 10: Add `--linearization-mode`, accepting only
  `tensor_available_disabled`.
- Phase 8. Stage 2. Action 11: Print JSON status and calibration files.

#### Phase 8. Stage 3: Run Command

- Phase 8. Stage 3. Action 1: Add `run` subcommand.
- Phase 8. Stage 3. Action 2: Add `--artifact-root`.
- Phase 8. Stage 3. Action 3: Add `--candidate-readout-source`.
- Phase 8. Stage 3. Action 4: Add `--candidate-cap`.
- Phase 8. Stage 3. Action 5: Add `--instance-id`.
- Phase 8. Stage 3. Action 6: Add `--episodes`.
- Phase 8. Stage 3. Action 7: Add `--replicates`.
- Phase 8. Stage 3. Action 8: Add `--threshold-policy-id`.
- Phase 8. Stage 3. Action 9: Add `--threshold-value`.
- Phase 8. Stage 3. Action 10: Add `--window-length`.
- Phase 8. Stage 3. Action 11: Add `--required-count`.
- Phase 8. Stage 3. Action 12: Add `--base-seed`.
- Phase 8. Stage 3. Action 13: Add `--locked-by`.
- Phase 8. Stage 3. Action 14: Add `--linearization-mode`, accepting only
  `tensor_available_disabled`.
- Phase 8. Stage 3. Action 15: Reject serious `medium` execution if four
  eligible medium candidates are unavailable.

#### Phase 8. Stage 4: Summarize Command

- Phase 8. Stage 4. Action 1: Add `summarize` subcommand.
- Phase 8. Stage 4. Action 2: Add `--artifact-root`.
- Phase 8. Stage 4. Action 3: Add optional `--docs-root`.
- Phase 8. Stage 4. Action 4: Call aggregation.
- Phase 8. Stage 4. Action 5: Call docs writer.
- Phase 8. Stage 4. Action 6: Print JSON status and docs paths.

### Phase 9: Tests

#### Phase 9. Stage 1: Unit Tests

- Phase 9. Stage 1. Action 1: Add tests for config ids.
- Phase 9. Stage 1. Action 2: Add tests for paths.
- Phase 9. Stage 1. Action 3: Add tests for threshold policy serialization.
- Phase 9. Stage 1. Action 4: Add tests for first sustained hit computation.
- Phase 9. Stage 1. Action 5: Add tests for transient-only and never-hit
  statuses.
- Phase 9. Stage 1. Action 6: Add tests for candidate source binding.
- Phase 9. Stage 1. Action 7: Add tests for medium candidate gate.
- Phase 9. Stage 1. Action 8: Add tests for Schema 0 arm construction.
- Phase 9. Stage 1. Action 9: Add tests for Schema 1 arm construction.
- Phase 9. Stage 1. Action 10: Add tests for expected-file policy.

#### Phase 9. Stage 2: Integration Tests

- Phase 9. Stage 2. Action 1: Add smoke runner test with one candidate and one
  replicate.
- Phase 9. Stage 2. Action 2: Add aggregation test for required result tables.
- Phase 9. Stage 2. Action 3: Add paired comparison test.
- Phase 9. Stage 2. Action 4: Add docs writer test.
- Phase 9. Stage 2. Action 5: Add readout source test.
- Phase 9. Stage 2. Action 6: Add CLI calibrate parser test.
- Phase 9. Stage 2. Action 7: Add CLI run parser test.
- Phase 9. Stage 2. Action 8: Add CLI summarize parser test.
- Phase 9. Stage 2. Action 9: Add unsupported linearization rejection test.
- Phase 9. Stage 2. Action 10: Add no-TeX-side-effects test by verifying the
  package does not write root TeX paths.

#### Phase 9. Stage 3: Regression Tests

- Phase 9. Stage 3. Action 1: Run targeted second-serious tests.
- Phase 9. Stage 3. Action 2: Run noisy-rate full-training tests.
- Phase 9. Stage 3. Action 3: Run noisy-rate contraction tests.
- Phase 9. Stage 3. Action 4: Run serious-learning CLI/runner regression
  tests.
- Phase 9. Stage 3. Action 5: Run generic CLI tests.
- Phase 9. Stage 3. Action 6: Run `git diff --check`.
- Phase 9. Stage 3. Action 7: Record results in implementation log.

### Phase 10: Implementation Smoke And Calibration

#### Phase 10. Stage 1: Compile And Pre-Smoke

- Phase 10. Stage 1. Action 1: Run compile check for new package and CLI.
- Phase 10. Stage 1. Action 2: Run targeted unit tests.
- Phase 10. Stage 1. Action 3: Run relevant counterpoint regression tests.
- Phase 10. Stage 1. Action 4: Stop on any unexpected failure.

#### Phase 10. Stage 2: Implementation Smoke Run

- Phase 10. Stage 2. Action 1: Run only a small implementation smoke unless
  Project Owner explicitly authorizes a larger run.
- Phase 10. Stage 2. Action 2: Use repo-resident artifact root:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/smoke_001/
  ```

- Phase 10. Stage 2. Action 3: Use available candidate source:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
  ```

- Phase 10. Stage 2. Action 4: Use candidate cap `1`.
- Phase 10. Stage 2. Action 5: Use replicates `1`.
- Phase 10. Stage 2. Action 6: Use episodes `4-8`.
- Phase 10. Stage 2. Action 7: Use a manifest-labeled smoke threshold value.
- Phase 10. Stage 2. Action 8: Verify status is complete.
- Phase 10. Stage 2. Action 9: Summarize smoke artifacts.
- Phase 10. Stage 2. Action 10: Verify repo readout source exists.

#### Phase 10. Stage 3: Calibration Run Decision

- Phase 10. Stage 3. Action 1: Do not run calibration unless execution
  instruction explicitly authorizes calibration.
- Phase 10. Stage 3. Action 2: If calibration is authorized, use a separate
  artifact root:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/calibration_001/
  ```

- Phase 10. Stage 3. Action 3: Write calibration summary and recommendation.
- Phase 10. Stage 3. Action 4: Report recommended threshold but do not run
  serious evidence budget.

#### Phase 10. Stage 4: Serious Run Decision Lock

- Phase 10. Stage 4. Action 1: Do not run the serious locked budget during
  implementation unless explicitly authorized.
- Phase 10. Stage 4. Action 2: Before serious run, require:

  ```text
  instance: medium
  candidate count: 4 eligible medium Schema 1 candidates
  episodes: 256
  threshold: locked from calibration
  persistence: 4 of 5
  linearization: tensor_available_disabled
  ```

- Phase 10. Stage 4. Action 3: Stop if any serious-run prerequisite is absent.

### Phase 11: Documentation And Final Verification

#### Phase 11. Stage 1: Design Documentation Updates

- Phase 11. Stage 1. Action 1: Update the design folder README if one exists,
  or create one if needed.
- Phase 11. Stage 1. Action 2: Link the blueprint, gameplan, and
  implementation log.
- Phase 11. Stage 1. Action 3: Record implementation smoke status.
- Phase 11. Stage 1. Action 4: Record serious-run decision lock.
- Phase 11. Stage 1. Action 5: Do not update root README unless the
  implementation changes available commands or checked-in readouts.

#### Phase 11. Stage 2: Final Test Pass

- Phase 11. Stage 2. Action 1: Run targeted second-serious tests.
- Phase 11. Stage 2. Action 2: Run relevant counterpoint regression tests.
- Phase 11. Stage 2. Action 3: Run generic CLI tests.
- Phase 11. Stage 2. Action 4: Run `git diff --check`.
- Phase 11. Stage 2. Action 5: Record results in implementation log.

#### Phase 11. Stage 3: Final Status Report

- Phase 11. Stage 3. Action 1: Run `git status --short --branch`.
- Phase 11. Stage 3. Action 2: Summarize files changed.
- Phase 11. Stage 3. Action 3: Summarize commands run.
- Phase 11. Stage 3. Action 4: Summarize tests passed.
- Phase 11. Stage 3. Action 5: Summarize smoke artifacts written.
- Phase 11. Stage 3. Action 6: Summarize decision-locked serious work not run.
- Phase 11. Stage 3. Action 7: Explicitly state whether any TeX files were
  touched.

## Command Templates

### Implementation Smoke

```bash
uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison run \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/smoke_001 \
  --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json \
  --candidate-cap 1 \
  --instance-id small \
  --episodes 4 \
  --replicates 1 \
  --threshold-policy-id counterpoint_total_space_sustained_reward_smoke_v001 \
  --threshold-value <smoke-threshold> \
  --window-length 5 \
  --required-count 4 \
  --locked-by codex \
  --linearization-mode tensor_available_disabled
```

### Summarize Smoke

```bash
uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison summarize \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/smoke_001
```

### Calibration, Only If Authorized

```bash
uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison calibrate \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/calibration_001 \
  --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json \
  --candidate-cap 2 \
  --instance-id medium \
  --episodes 64 \
  --replicates 4 \
  --locked-by foster \
  --linearization-mode tensor_available_disabled
```

### Serious Locked Run, Only If Authorized After Calibration

```bash
uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison run \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/serious_001 \
  --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json \
  --candidate-cap 4 \
  --instance-id medium \
  --episodes 256 \
  --replicates <locked-replicates> \
  --threshold-policy-id counterpoint_total_space_sustained_reward_v001 \
  --threshold-value <calibration-locked-threshold> \
  --window-length 5 \
  --required-count 4 \
  --locked-by foster \
  --linearization-mode tensor_available_disabled
```

### Human-Readable Readout

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/readout_source.json
```

## Completion Criteria

Implementation is complete only when:

- all non-decision-locked Phase.Stage.Action items are completed as written;
- no `/Users/foster/state_collapser` edits occurred;
- no `counterpoint_symbolic_v001` semantics changed;
- no root TeX files or TeX sidecars were modified by implementation;
- Schema 0 and Schema 1 run under the matched comparison harness;
- threshold policy is explicit and shared;
- 4-of-5 persistence is implemented and tested;
- source bindings and expected-file policy exist;
- required manifests and result tables are written;
- repo readout surface and readout source exist;
- docs writer creates the required human-readable docs;
- targeted tests and `git diff --check` pass;
- implementation log records commands, tests, artifacts, and decision locks;
- serious `medium` budget remains unrun unless explicitly authorized.

## Final Reporting Requirements

When this gameplan is executed, final reporting must include:

- branch name;
- implementation log path;
- artifact root used for implementation smoke;
- readout source path;
- source candidate binding used;
- whether four eligible medium candidates were available;
- tests run;
- whether calibration was run;
- whether the serious locked run was run or remains decision-locked;
- whether any TeX files were touched;
- any stopped or blocked Phase.Stage.Action item.

The final report must not claim:

- general tower advantage;
- general noisy-rate advantage;
- direct-vs-tower broad superiority;
- medium serious result if only smoke or calibration ran;
- serious threshold validity if calibration was not run;
- tensor-enabled or GPU behavior.
