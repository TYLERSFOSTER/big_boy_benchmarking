# Counterpoint Noisy-Rate Full-Tower Training Diagnostic Implementation Workplan

Date: 2026-06-02

Status: implementation workplan, not yet executed

Repository:

```text
<repo-root>
```

Source blueprint:

```text
docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic/01_counterpoint_noisy_rate_full_tower_training_diagnostic_blueprint.md
```

## Purpose

This workplan translates the full-tower training diagnostic blueprint into
Phase.Stage.Action implementation work.

The target is a sibling evaluation for the existing counterpoint environment
family:

```text
counterpoint_symbolic_v001
```

focused on:

- selecting non-collapsed noisy-rate towers from the existing noisy-rate
  contraction diagnostic readout;
- building the full available tower for each selected candidate;
- running tower-only training on each candidate with no direct baseline
  comparison;
- preserving learner state across episodes inside a training replicate;
- recording candidate, tower, lift, concrete-step, controller, tier-occupancy,
  learner-update, and training-health evidence;
- producing repo-resident artifacts and human-readable readout support.

This is not a new environment.

This is not a direct-vs-tower comparison.

This is not approval to edit `<state-collapser-repo>`.

This is not approval to run the main full training budget unless the Project
Owner explicitly authorizes that budget.

## Execution Authority Status

This document is not approval to implement.

The Project Owner requested this workplan from the blueprint:

```text
Following `prime_directive`, turn
`docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic/01_counterpoint_noisy_rate_full_tower_training_diagnostic_blueprint.md`
into a implementation workplan in Phase.Stage.Action format
```

Therefore this document may be created now.

Source, test, CLI, artifact-schema, evaluation-readout, and benchmark-run
implementation must not begin until the Project Owner explicitly approves
execution of this exact workplan.

If the Project Owner later says to execute this workplan without overriding the
consultant defaults below, implementation should treat those defaults as the
approved execution settings for the implementation and smoke-validation
portion. The main full training budget remains a decision lock unless the
Project Owner explicitly authorizes it.

If the Project Owner overrides any default before execution, update this
workplan or record the override in the implementation log before source edits.

## Source Authority

This workplan follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/git_practices.md`
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`
- `docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md`
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`
- `docs/design/system_learning_from_evaluations/README.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/README.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/02_counterpoint_noisy_rate_contraction_diagnostics_blueprint.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/04_counterpoint_noisy_rate_contraction_diagnostics_implementation_log.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic/README.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic/design_discussion.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic/01_counterpoint_noisy_rate_full_tower_training_diagnostic_blueprint.md`
- `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/README.md`
- `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json`
- current BBB counterpoint noisy-rate, tower-control, artifact, CLI, and test
  source surfaces

## PO Attribution Preservation

This workplan preserves the source blueprint's PO Attribution Ledger. It does
not add invented Project Owner turns.

Project Owner-originated design locks carried into implementation:

1. The Project Owner asked whether the repo was ready to blueprint a full
   train for each current noisy-rate example.
2. The Project Owner confirmed the intended shape:

   ```text
   take each non-collapsed noisy-rate counterpoint tower from the current
   diagnostic, build its full available tower, then run a real tower-only
   training budget on it with no direct baseline comparison
   ```

3. The Project Owner asked to start this work in:

   ```text
   docs/design/system_learning_from_evaluations
   ```

4. The Project Owner requested a blueprint in the full-tower training
   diagnostic folder.
5. The Project Owner requested this Phase.Stage.Action implementation
   workplan.

Consultant-authored defaults and recommendations are explicitly labeled below.

## Consultant Defaults For Execution

These defaults are consultant-authored. They become execution assumptions only
if the Project Owner later approves execution of this workplan without
overriding them.

1. Use the evaluation id:

   ```text
   counterpoint_noisy_rate_full_tower_training_diagnostic_v001
   ```

2. Use the run family id:

   ```text
   counterpoint_symbolic_v001_noisy_rate_full_tower_training_diagnostic_v001
   ```

3. Use the run mode:

   ```text
   diagnostic_noisy_rate_full_tower_training
   ```

4. Use the CLI group:

   ```text
   counterpoint noisy-rate-full-train
   ```

5. Use the package:

   ```text
   src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/
   ```

6. Use the repo readout surface:

   ```text
   docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/
   ```

7. Use the parent candidate source:

   ```text
   docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json
   ```

8. Exclude `no_contraction_control` by default.

9. Treat no-contraction as an optional runtime anchor only if explicitly
   enabled by CLI flag, never as a direct baseline comparator.

10. Preserve learner state across episodes inside each training replicate.

11. Use `tensor_available_disabled`.

12. Use `tower_exploit_explore`.

13. Use the implementation smoke budget:

   ```text
   candidate cap: 2
   training replicates per candidate: 1
   episodes per replicate: 4
   ```

14. Keep the main full diagnostic training budget behind a decision lock:

   ```text
   all eligible candidates
   training replicates per candidate: 4
   episodes per replicate: 64
   ```

15. Treat reward movement as descriptive evidence, not as a pass/fail gate.

16. Treat pass/warn/fail as tower-training health, not performance.

## Fixed Design Locks

These locks are binding if this workplan is later executed.

### Environment Lock

Do not change:

```text
counterpoint_symbolic_v001
```

Do not alter:

- base state enumeration;
- action enumeration;
- transition legality;
- reward semantics;
- fixture definitions;
- legal action masks;
- upstream `state_collapser`.

### Parent Diagnostic Lock

Do not reinterpret the parent noisy-rate diagnostic as a learning comparison.

Do not mutate the parent diagnostic artifact schema except where shared helper
extraction is narrowly required and backward compatible.

Read parent candidates from:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json
```

Do not hard-code the current nine candidate examples into implementation.

### Full Available Tower Lock

For the current noisy-rate schema, "full available tower" means:

```text
tier 0: base counterpoint graph
tier 1: quotient after the single selected noisy-rate contraction block
```

Do not silently reinterpret this workplan as a deep repeated-contraction tower
implementation.

If the implementation discovers that a candidate has more than two tiers, it
may train on all available tiers, but it must record the tier sequence in the
candidate manifest and readout.

### Training Semantics Lock

A real training replicate must preserve learner state across episodes.

Do not implement this evaluation as only a larger set of independent
episode-local probes unless the Project Owner explicitly authorizes that scope
reduction.

### Comparison Lock

Do not compute:

- direct-vs-tower deltas;
- baseline advantages;
- arm rankings;
- schema superiority claims;
- sample-efficiency claims.

The result may say only whether selected towers train cleanly, train with
warnings, train weakly, or fail under the locked budget.

### Artifact Lock

Durable artifacts must be repo-resident under:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts/<run-label>/
```

The human-readable readout target must be:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
```

Do not write generated readouts into raw artifact roots.

## Stop Conditions

Stop and ask the Project Owner if:

- execution has not been explicitly approved;
- working tree or branch state would mix unrelated changes into this
  implementation;
- any action would require editing `<state-collapser-repo>`;
- any action would change `counterpoint_symbolic_v001` environment semantics;
- the parent `readout_source.json` is missing, stale, outside the repo, or
  points outside the repo;
- candidate selection yields no eligible non-collapsed candidates;
- the implementation cannot preserve learner state across episodes without a
  design change;
- learner-update evidence cannot be exposed or honestly summarized;
- "full available tower" becomes ambiguous during implementation;
- a no-contraction control starts acting like a baseline comparator;
- an action would require a weaker substitute, hidden simplification, or
  unapproved reordering;
- the implementation would omit required readout-source, expected-file,
  methodology, goal, badge, or claim-boundary evidence;
- the human-readable readout would need to reverse-engineer meaning from raw
  per-run files;
- the main full training budget would be run without explicit Project Owner
  authorization.

## Phase.Stage.Action Workplan

### Phase 0: Authority, Branch, And Reality Check

#### Phase 0. Stage 0: Execution Authority

- Phase 0. Stage 0. Action 1: Confirm the Project Owner has explicitly asked
  to execute this exact workplan.
- Phase 0. Stage 0. Action 2: If execution authority is absent, stop before
  source edits.
- Phase 0. Stage 0. Action 3: Record the exact execution instruction in the
  implementation log.

#### Phase 0. Stage 1: Working Tree And Branch Discipline

- Phase 0. Stage 1. Action 1: Run `git status --short --branch`.
- Phase 0. Stage 1. Action 2: Identify unrelated dirty files and record them
  in the implementation log.
- Phase 0. Stage 1. Action 3: Stop if unrelated dirty state would be touched
  or mixed into this implementation.
- Phase 0. Stage 1. Action 4: Create and switch to:

  ```text
  codex/noisy-rate-full-tower-training-diagnostic
  ```

- Phase 0. Stage 1. Action 5: Record branch creation and initial dirty state
  in the implementation log.

#### Phase 0. Stage 2: Source Re-Read

- Phase 0. Stage 2. Action 1: Re-read the Prime Directive source authority
  listed in this workplan.
- Phase 0. Stage 2. Action 2: Re-read the source blueprint.
- Phase 0. Stage 2. Action 3: Re-read the parent noisy-rate diagnostic
  blueprint, implementation log, and current readout.
- Phase 0. Stage 2. Action 4: Re-read current noisy-rate runner, aggregation,
  docs writer, manifest, paths, config, events, CLI, and tests.
- Phase 0. Stage 2. Action 5: Re-read serious-learning tower-control code to
  identify reusable persistent-training surfaces.
- Phase 0. Stage 2. Action 6: Record source surfaces mapped in the
  implementation log.

#### Phase 0. Stage 3: Implementation Log

- Phase 0. Stage 3. Action 1: Create:

  ```text
  docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic/03_counterpoint_noisy_rate_full_tower_training_diagnostic_implementation_log.md
  ```

- Phase 0. Stage 3. Action 2: Include branch, execution instruction, source
  workplan, initial dirty state, stop conditions, and the Phase.Stage.Action
  checklist.
- Phase 0. Stage 3. Action 3: Keep the log updated as actions are completed,
  blocked, skipped with explicit reason, or pending decision lock.

### Phase 1: Evaluation Identity, Config, And Paths

#### Phase 1. Stage 1: Evaluation Constants

- Phase 1. Stage 1. Action 1: Add evaluation id constants for
  `counterpoint_noisy_rate_full_tower_training_diagnostic_v001`.
- Phase 1. Stage 1. Action 2: Add run family id
  `counterpoint_symbolic_v001_noisy_rate_full_tower_training_diagnostic_v001`.
- Phase 1. Stage 1. Action 3: Add run mode
  `diagnostic_noisy_rate_full_tower_training`.
- Phase 1. Stage 1. Action 4: Keep existing noisy-rate contraction ids
  unchanged.
- Phase 1. Stage 1. Action 5: Add tests that the ids are exported and do not
  collide with existing counterpoint ids.

#### Phase 1. Stage 2: Package Scaffold

- Phase 1. Stage 2. Action 1: Create:

  ```text
  src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/
  ```

- Phase 1. Stage 2. Action 2: Add `__init__.py`.
- Phase 1. Stage 2. Action 3: Add `config.py`.
- Phase 1. Stage 2. Action 4: Add `paths.py`.
- Phase 1. Stage 2. Action 5: Add `events.py`.
- Phase 1. Stage 2. Action 6: Add `candidate_selection.py`.
- Phase 1. Stage 2. Action 7: Add `runner.py`.
- Phase 1. Stage 2. Action 8: Add `aggregation.py`.
- Phase 1. Stage 2. Action 9: Add `docs_writer.py`.
- Phase 1. Stage 2. Action 10: Add `manifests.py`.

#### Phase 1. Stage 3: Budget Configuration

- Phase 1. Stage 3. Action 1: Define `NoisyRateFullTrainingBudget`.
- Phase 1. Stage 3. Action 2: Include parent candidate readout source path.
- Phase 1. Stage 3. Action 3: Include include/exclude no-contraction policy.
- Phase 1. Stage 3. Action 4: Include candidate cap for implementation smoke.
- Phase 1. Stage 3. Action 5: Include training replicates per candidate.
- Phase 1. Stage 3. Action 6: Include episodes per replicate.
- Phase 1. Stage 3. Action 7: Include horizon override.
- Phase 1. Stage 3. Action 8: Include controller event ceiling override.
- Phase 1. Stage 3. Action 9: Include linearization mode validation locked to
  `tensor_available_disabled`.
- Phase 1. Stage 3. Action 10: Include base seed and locked-by fields.
- Phase 1. Stage 3. Action 11: Define smoke defaults from this workplan.
- Phase 1. Stage 3. Action 12: Define full-budget defaults but mark them as
  decision-locked in documentation and runbook.

#### Phase 1. Stage 4: Paths

- Phase 1. Stage 4. Action 1: Define default repo readout surface:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/
  ```

- Phase 1. Stage 4. Action 2: Define default artifact root under the readout
  surface.
- Phase 1. Stage 4. Action 3: Define evaluation root under:

  ```text
  <artifact-root>/evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic_v001/
  ```

- Phase 1. Stage 4. Action 4: Add repo-resident artifact-root validation.
- Phase 1. Stage 4. Action 5: Add path dataclass for manifests, run index,
  aggregate table, candidate manifest, results dir, and readout source.
- Phase 1. Stage 4. Action 6: Add tests for default paths and repo-residency
  rejection.

### Phase 2: Candidate Source And Eligibility

#### Phase 2. Stage 1: Parent Source Binding Loader

- Phase 2. Stage 1. Action 1: Implement a loader for parent
  `readout_source.json`.
- Phase 2. Stage 1. Action 2: Reject missing files.
- Phase 2. Stage 1. Action 3: Reject non-repo source bindings.
- Phase 2. Stage 1. Action 4: Resolve parent `source_evaluation_root`.
- Phase 2. Stage 1. Action 5: Resolve parent source files required by the
  blueprint.
- Phase 2. Stage 1. Action 6: Add tests for missing, outside-repo, and valid
  parent source bindings.

#### Phase 2. Stage 2: Parent Table Reader

- Phase 2. Stage 2. Action 1: Read parent `evaluation_aggregate_table.csv`.
- Phase 2. Stage 2. Action 2: Read parent `tower_shape_summary.csv`.
- Phase 2. Stage 2. Action 3: Read parent `noisy_rate_selection_summary.csv`.
- Phase 2. Stage 2. Action 4: Read parent
  `noisy_rate_source_coverage_summary.csv`.
- Phase 2. Stage 2. Action 5: Read parent
  `noisy_rate_selection_consistency_summary.csv`.
- Phase 2. Stage 2. Action 6: Read parent `endpoint_coalescence_summary.csv`.
- Phase 2. Stage 2. Action 7: Read parent `evaluation_budget_lock.json`.
- Phase 2. Stage 2. Action 8: Stop if any required parent table is missing
  without expected-file policy support.

#### Phase 2. Stage 3: Candidate Row Model

- Phase 2. Stage 3. Action 1: Define a candidate row/dataclass with fields
  from the blueprint's candidate summary row.
- Phase 2. Stage 3. Action 2: Include parent evaluation id and parent artifact
  run label.
- Phase 2. Stage 3. Action 3: Include candidate id.
- Phase 2. Stage 3. Action 4: Include tier state-cell-count sequence.
- Phase 2. Stage 3. Action 5: Include active action-cell-count sequence.
- Phase 2. Stage 3. Action 6: Include eligibility boolean and exclusion
  reason.
- Phase 2. Stage 3. Action 7: Add serialization to CSV and JSON-compatible
  dicts.

#### Phase 2. Stage 4: Candidate Eligibility

- Phase 2. Stage 4. Action 1: Group parent evidence by `(instance_id, arm_id,
  schema_seed)`.
- Phase 2. Stage 4. Action 2: Reject `no_contraction_control` by default.
- Phase 2. Stage 4. Action 3: Reject failed parent rows.
- Phase 2. Stage 4. Action 4: Reject selection-consistency mismatch.
- Phase 2. Stage 4. Action 5: Reject candidates with fewer than two tiers.
- Phase 2. Stage 4. Action 6: Reject candidates whose deepest tier has one or
  fewer state cells.
- Phase 2. Stage 4. Action 7: Reject candidates whose deepest tier has zero
  active action cells.
- Phase 2. Stage 4. Action 8: Reject full-collapse or uninterpretable parent
  aggregate classifications.
- Phase 2. Stage 4. Action 9: Sort retained candidates by instance id,
  requested rate, and schema seed.
- Phase 2. Stage 4. Action 10: Apply candidate cap only after deterministic
  sorting.
- Phase 2. Stage 4. Action 11: Stop if no eligible candidates remain.

#### Phase 2. Stage 5: Candidate Manifest

- Phase 2. Stage 5. Action 1: Write `candidate_manifest.json`.
- Phase 2. Stage 5. Action 2: Include selected candidates.
- Phase 2. Stage 5. Action 3: Include excluded candidates and exclusion
  reasons.
- Phase 2. Stage 5. Action 4: Include parent source binding path.
- Phase 2. Stage 5. Action 5: Include parent result-table paths.
- Phase 2. Stage 5. Action 6: Include candidate-selection rules.
- Phase 2. Stage 5. Action 7: Add tests for deterministic candidate manifest
  generation.

### Phase 3: Persistent Tower-Training Runtime

#### Phase 3. Stage 1: Reusable Training Adapter

- Phase 3. Stage 1. Action 1: Reuse `CounterpointTowerControlAdapter`.
- Phase 3. Stage 1. Action 2: Build the candidate tower with
  `build_counterpoint_noisy_rate_partition_tower`.
- Phase 3. Stage 1. Action 3: Pass candidate numerator, denominator, schema
  seed, and selector rule id into tower construction.
- Phase 3. Stage 1. Action 4: Verify built tower shape matches the candidate
  manifest sequence.
- Phase 3. Stage 1. Action 5: Stop if tower shape cannot be reproduced.

#### Phase 3. Stage 2: Persistent Learner Semantics

- Phase 3. Stage 2. Action 1: Implement training replicate setup with one
  `CounterpointTierLearner` per candidate training replicate.
- Phase 3. Stage 2. Action 2: Ensure the learner object persists across all
  episodes in the replicate.
- Phase 3. Stage 2. Action 3: Reset environment/runtime episode state between
  episodes without resetting learner state.
- Phase 3. Stage 2. Action 4: Preserve controller configuration across the
  replicate unless explicitly varied by budget.
- Phase 3. Stage 2. Action 5: Add a test proving learner state persists across
  episodes.
- Phase 3. Stage 2. Action 6: Stop if persistent learner semantics require
  upstream `state_collapser` changes.

#### Phase 3. Stage 3: Runtime Loop

- Phase 3. Stage 3. Action 1: Implement episode loop bounded by horizon.
- Phase 3. Stage 3. Action 2: Implement controller-event loop bounded by
  controller event ceiling.
- Phase 3. Stage 3. Action 3: Use active-tier exploit/explore runtime.
- Phase 3. Stage 3. Action 4: Use the diagnostic controller snapshot pattern
  to capture selected-tier and tier-signal evidence.
- Phase 3. Stage 3. Action 5: Record concrete steps only when a lifted action
  realizes a base transition.
- Phase 3. Stage 3. Action 6: Record terminated and truncated outcomes.
- Phase 3. Stage 3. Action 7: Preserve no-direct-baseline semantics in all run
  metadata.

#### Phase 3. Stage 4: Learner Update Evidence

- Phase 3. Stage 4. Action 1: Identify where learner summaries expose TD
  error, success, update count, or equivalent evidence.
- Phase 3. Stage 4. Action 2: Add `learner_update_events.csv` if update-level
  evidence can be captured.
- Phase 3. Stage 4. Action 3: Include candidate id, run id, episode index,
  controller event index, tier, success, td error, and update reason where
  available.
- Phase 3. Stage 4. Action 4: If update-level evidence cannot be exposed,
  stop and ask the Project Owner whether summary-level learner evidence is an
  acceptable scope reduction.

### Phase 4: Event Rows And Per-Run Artifacts

#### Phase 4. Stage 1: Event Row Types

- Phase 4. Stage 1. Action 1: Define `FullTrainingEvaluationRunIndexRow`.
- Phase 4. Stage 1. Action 2: Define `FullTrainingCandidateSummaryRow`.
- Phase 4. Stage 1. Action 3: Define `FullTrainingEpisodeRow`.
- Phase 4. Stage 1. Action 4: Define `FullTrainingStepRow`.
- Phase 4. Stage 1. Action 5: Define `FullTrainingControlEventRow`.
- Phase 4. Stage 1. Action 6: Define `FullTrainingLiftFiberEventRow`.
- Phase 4. Stage 1. Action 7: Define `FullTrainingABCSelectionEventRow`.
- Phase 4. Stage 1. Action 8: Define `FullTrainingABCTierSignalEventRow`.
- Phase 4. Stage 1. Action 9: Define `FullTrainingLearnerUpdateEventRow`.
- Phase 4. Stage 1. Action 10: Define summary row types needed by
  aggregation.

#### Phase 4. Stage 2: Per-Run Artifact Writer

- Phase 4. Stage 2. Action 1: Write `run_manifest.json`.
- Phase 4. Stage 2. Action 2: Write `seed_bundle.json`.
- Phase 4. Stage 2. Action 3: Write `mode_manifest.json`.
- Phase 4. Stage 2. Action 4: Write `linearization_manifest.json`.
- Phase 4. Stage 2. Action 5: Write `schema_manifest.json`.
- Phase 4. Stage 2. Action 6: Write `schema_construction.json`.
- Phase 4. Stage 2. Action 7: Write `quotient_summary.json`.
- Phase 4. Stage 2. Action 8: Write `episodes.csv`.
- Phase 4. Stage 2. Action 9: Write `step_events.csv`.
- Phase 4. Stage 2. Action 10: Write `control_events.csv`.
- Phase 4. Stage 2. Action 11: Write `lift_fiber_events.csv`.
- Phase 4. Stage 2. Action 12: Write `abc_selection_events.csv`.
- Phase 4. Stage 2. Action 13: Write `abc_tier_signal_events.csv`.
- Phase 4. Stage 2. Action 14: Write `learner_update_events.csv`.
- Phase 4. Stage 2. Action 15: Write `timing_segments.csv`.
- Phase 4. Stage 2. Action 16: Write `timing_summary.json`.
- Phase 4. Stage 2. Action 17: Write or touch `warnings.jsonl`.

#### Phase 4. Stage 3: Quotient Summary

- Phase 4. Stage 3. Action 1: Include candidate id and parent source context.
- Phase 4. Stage 3. Action 2: Include tier state-cell-count sequence.
- Phase 4. Stage 3. Action 3: Include tier active action-cell-count sequence.
- Phase 4. Stage 3. Action 4: Include raw historical action-cell counts.
- Phase 4. Stage 3. Action 5: Include deepest tier index and action
  availability.
- Phase 4. Stage 3. Action 6: Include parent selected edge/source coverage
  evidence.
- Phase 4. Stage 3. Action 7: Include training budget and persistent learner
  status.

#### Phase 4. Stage 4: Evaluation Manifests

- Phase 4. Stage 4. Action 1: Write `evaluation_manifest.json`.
- Phase 4. Stage 4. Action 2: Write `evaluation_budget_lock.json`.
- Phase 4. Stage 4. Action 3: Write `candidate_manifest.json`.
- Phase 4. Stage 4. Action 4: Write `evaluation_run_index.csv`.
- Phase 4. Stage 4. Action 5: Write `evaluation_aggregate_table.csv` during
  summarization.
- Phase 4. Stage 4. Action 6: Write `evaluation_aggregate_summary.json`
  during summarization.
- Phase 4. Stage 4. Action 7: Write `readout_source.json` in both the raw
  evaluation root and repo readout surface.

### Phase 5: Aggregation And Health Classification

#### Phase 5. Stage 1: Aggregation Reader

- Phase 5. Stage 1. Action 1: Read the child `evaluation_run_index.csv`.
- Phase 5. Stage 1. Action 2: For each success run, read all required per-run
  files.
- Phase 5. Stage 1. Action 3: For failed runs, emit failed aggregate rows with
  failure reasons.
- Phase 5. Stage 1. Action 4: Stop if required files are missing without an
  expected-file explanation.

#### Phase 5. Stage 2: Evaluation-Level Tables

- Phase 5. Stage 2. Action 1: Write `results/candidate_summary.csv`.
- Phase 5. Stage 2. Action 2: Write `results/tower_shape_summary.csv`.
- Phase 5. Stage 2. Action 3: Write `results/training_episode_summary.csv`.
- Phase 5. Stage 2. Action 4: Write `results/training_curve_summary.csv`.
- Phase 5. Stage 2. Action 5: Write `results/tier_occupancy_summary.csv`.
- Phase 5. Stage 2. Action 6: Write `results/tier_executability_summary.csv`.
- Phase 5. Stage 2. Action 7: Write `results/lift_success_by_tier.csv`.
- Phase 5. Stage 2. Action 8: Write `results/lift_failure_by_tier.csv`.
- Phase 5. Stage 2. Action 9: Write `results/concrete_step_summary.csv`.
- Phase 5. Stage 2. Action 10: Write
  `results/controller_action_summary.csv`.
- Phase 5. Stage 2. Action 11: Write `results/abc_selection_summary.csv`.
- Phase 5. Stage 2. Action 12: Write `results/abc_tier_signal_summary.csv`.
- Phase 5. Stage 2. Action 13: Write `results/learner_update_summary.csv`.
- Phase 5. Stage 2. Action 14: Write `results/training_health_summary.csv`.
- Phase 5. Stage 2. Action 15: Write optional timing/warning summaries if
  useful and cheap.

#### Phase 5. Stage 3: Training Curves

- Phase 5. Stage 3. Action 1: Compute per-run episode-order metrics.
- Phase 5. Stage 3. Action 2: Compute configurable episode windows.
- Phase 5. Stage 3. Action 3: Compute mean reward by window.
- Phase 5. Stage 3. Action 4: Compute mean concrete step count by window.
- Phase 5. Stage 3. Action 5: Compute lift success share by window.
- Phase 5. Stage 3. Action 6: Compute deepest-tier selected share by window.
- Phase 5. Stage 3. Action 7: Compute deepest-tier concrete step share by
  window.
- Phase 5. Stage 3. Action 8: Compute learner update count by window.

#### Phase 5. Stage 4: Health Classification

- Phase 5. Stage 4. Action 1: Implement `trainable_clean`.
- Phase 5. Stage 4. Action 2: Implement `trainable_with_warnings`.
- Phase 5. Stage 4. Action 3: Implement
  `runtime_executable_but_training_weak`.
- Phase 5. Stage 4. Action 4: Implement `untrainable_no_concrete_steps`.
- Phase 5. Stage 4. Action 5: Implement `untrainable_lift_failure`.
- Phase 5. Stage 4. Action 6: Implement `untrainable_non_executable_tier`.
- Phase 5. Stage 4. Action 7: Implement `artifact_incomplete`.
- Phase 5. Stage 4. Action 8: Implement `candidate_invalid`.
- Phase 5. Stage 4. Action 9: Lock warning thresholds in the budget or
  manifest.
- Phase 5. Stage 4. Action 10: Add unit tests for each classification.

### Phase 6: Source Binding, Goals, Badges, And Docs Writer

#### Phase 6. Stage 1: Manifest Payloads

- Phase 6. Stage 1. Action 1: Implement `evaluation_manifest_payload`.
- Phase 6. Stage 1. Action 2: Implement `budget_lock_payload`.
- Phase 6. Stage 1. Action 3: Implement `candidate_manifest_payload`.
- Phase 6. Stage 1. Action 4: Implement `aggregate_summary_payload`.
- Phase 6. Stage 1. Action 5: Implement `readout_source_payload`.
- Phase 6. Stage 1. Action 6: Implement expected-file policy.
- Phase 6. Stage 1. Action 7: Implement goal criteria.
- Phase 6. Stage 1. Action 8: Implement structural limit checks.
- Phase 6. Stage 1. Action 9: Implement claim boundary.

#### Phase 6. Stage 2: Badge Policy

- Phase 6. Stage 2. Action 1: Add artifact-status badge.
- Phase 6. Stage 2. Action 2: Add candidate-status badge.
- Phase 6. Stage 2. Action 3: Add training-health badge.
- Phase 6. Stage 2. Action 4: Add runtime-executability badge.
- Phase 6. Stage 2. Action 5: Add lift-status badge.
- Phase 6. Stage 2. Action 6: Add scope badge.
- Phase 6. Stage 2. Action 7: Add provenance badge.
- Phase 6. Stage 2. Action 8: Add tests or snapshot checks for badge
  generation inputs.

#### Phase 6. Stage 3: Docs Writer

- Phase 6. Stage 3. Action 1: Write repo-side `README.md`.
- Phase 6. Stage 3. Action 2: Write `method.md`.
- Phase 6. Stage 3. Action 3: Write `runbook.md`.
- Phase 6. Stage 3. Action 4: Write `artifact_index.md`.
- Phase 6. Stage 3. Action 5: Write `glossary.md`.
- Phase 6. Stage 3. Action 6: Write `results/summary.md`.
- Phase 6. Stage 3. Action 7: Write training-health detail docs under
  `results/`.
- Phase 6. Stage 3. Action 8: Ensure README explicitly states this is not a
  direct-vs-tower comparison.
- Phase 6. Stage 3. Action 9: Ensure README explicitly states the current full
  available tower is base tier plus one noisy-rate quotient tier.
- Phase 6. Stage 3. Action 10: Ensure README includes the correct artifact
  readout command:

  ```text
  execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-root>/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
  ```

### Phase 7: CLI

#### Phase 7. Stage 1: CLI Imports

- Phase 7. Stage 1. Action 1: Import config defaults.
- Phase 7. Stage 1. Action 2: Import path default artifact root.
- Phase 7. Stage 1. Action 3: Import runner entrypoint.
- Phase 7. Stage 1. Action 4: Import aggregation entrypoint.
- Phase 7. Stage 1. Action 5: Import docs writer.

#### Phase 7. Stage 2: Run Command

- Phase 7. Stage 2. Action 1: Add `counterpoint noisy-rate-full-train run`.
- Phase 7. Stage 2. Action 2: Add `--artifact-root`.
- Phase 7. Stage 2. Action 3: Add `--candidate-readout-source`.
- Phase 7. Stage 2. Action 4: Add `--candidate-cap`.
- Phase 7. Stage 2. Action 5: Add `--training-replicates`.
- Phase 7. Stage 2. Action 6: Add `--episodes`.
- Phase 7. Stage 2. Action 7: Add `--base-seed`.
- Phase 7. Stage 2. Action 8: Add `--locked-by`.
- Phase 7. Stage 2. Action 9: Add `--horizon`.
- Phase 7. Stage 2. Action 10: Add `--controller-event-ceiling`.
- Phase 7. Stage 2. Action 11: Add `--include-runtime-anchor` only if the
  implementation supports it without comparison semantics.
- Phase 7. Stage 2. Action 12: Add `--linearization-mode` locked to
  `tensor_available_disabled`.

#### Phase 7. Stage 3: Summarize Command

- Phase 7. Stage 3. Action 1: Add `counterpoint noisy-rate-full-train
  summarize`.
- Phase 7. Stage 3. Action 2: Add `--artifact-root`.
- Phase 7. Stage 3. Action 3: Add `--docs-root`.
- Phase 7. Stage 3. Action 4: Call aggregation.
- Phase 7. Stage 3. Action 5: Call docs writer.
- Phase 7. Stage 3. Action 6: Print JSON status and docs paths.

#### Phase 7. Stage 4: CLI Tests

- Phase 7. Stage 4. Action 1: Add parser smoke test for run command.
- Phase 7. Stage 4. Action 2: Add parser smoke test for summarize command.
- Phase 7. Stage 4. Action 3: Add validation test that unsupported
  linearization mode is rejected.
- Phase 7. Stage 4. Action 4: Add validation test that outside-repo artifact
  roots are rejected.

### Phase 8: Unit And Integration Tests

#### Phase 8. Stage 1: Candidate Tests

- Phase 8. Stage 1. Action 1: Test valid parent source binding resolution.
- Phase 8. Stage 1. Action 2: Test no-contraction default rejection.
- Phase 8. Stage 1. Action 3: Test full-collapse rejection.
- Phase 8. Stage 1. Action 4: Test zero active action-cell rejection.
- Phase 8. Stage 1. Action 5: Test deterministic sorting.
- Phase 8. Stage 1. Action 6: Test candidate cap behavior.

#### Phase 8. Stage 2: Runner Tests

- Phase 8. Stage 2. Action 1: Test single candidate smoke run writes required
  per-run artifacts.
- Phase 8. Stage 2. Action 2: Test learner state persists across episodes.
- Phase 8. Stage 2. Action 3: Test tower shape reproduction.
- Phase 8. Stage 2. Action 4: Test no direct baseline artifacts are produced
  by default.
- Phase 8. Stage 2. Action 5: Test warnings file behavior.

#### Phase 8. Stage 3: Aggregation Tests

- Phase 8. Stage 3. Action 1: Test required result tables are written.
- Phase 8. Stage 3. Action 2: Test training curve windows.
- Phase 8. Stage 3. Action 3: Test training health classes.
- Phase 8. Stage 3. Action 4: Test aggregate summary status.
- Phase 8. Stage 3. Action 5: Test readout source points to repo readout
  surface.

#### Phase 8. Stage 4: Docs Tests

- Phase 8. Stage 4. Action 1: Test docs writer creates README, method,
  runbook, artifact index, glossary, summary, and badges.
- Phase 8. Stage 4. Action 2: Test README contains the no-comparison claim
  boundary.
- Phase 8. Stage 4. Action 3: Test README contains the current full-available
  tower definition.
- Phase 8. Stage 4. Action 4: Test runbook contains the correct
  `readout_source.json` protocol invocation.

### Phase 9: Implementation Smoke Run

#### Phase 9. Stage 1: Pre-Smoke Verification

- Phase 9. Stage 1. Action 1: Run targeted compile check.
- Phase 9. Stage 1. Action 2: Run targeted unit tests for the new package.
- Phase 9. Stage 1. Action 3: Run relevant counterpoint regression tests.
- Phase 9. Stage 1. Action 4: Run relevant CLI tests.
- Phase 9. Stage 1. Action 5: Stop on any unexpected failure and diagnose
  before continuing.

#### Phase 9. Stage 2: Smoke Artifact Run

- Phase 9. Stage 2. Action 1: Run implementation smoke with repo-resident
  artifact root:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts/smoke_001/
  ```

- Phase 9. Stage 2. Action 2: Use parent candidate source:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json
  ```

- Phase 9. Stage 2. Action 3: Use candidate cap `2`.
- Phase 9. Stage 2. Action 4: Use training replicates `1`.
- Phase 9. Stage 2. Action 5: Use episodes `4`.
- Phase 9. Stage 2. Action 6: Use `locked-by codex`.
- Phase 9. Stage 2. Action 7: Verify run status is complete.

#### Phase 9. Stage 3: Smoke Summarize And Readout

- Phase 9. Stage 3. Action 1: Run summarize for the smoke artifact root.
- Phase 9. Stage 3. Action 2: Verify all required result tables exist.
- Phase 9. Stage 3. Action 3: Verify repo readout surface contains
  `readout_source.json`.
- Phase 9. Stage 3. Action 4: Execute the artifact-table readout protocol
  against the repo readout source if the generated docs writer is not already
  sufficient.
- Phase 9. Stage 3. Action 5: Review README for no-comparison language,
  candidate clarity, tower definition, health classification, and claim
  boundary.

### Phase 10: Main Budget Decision Lock

#### Phase 10. Stage 1: Stop Before Full Diagnostic Run

- Phase 10. Stage 1. Action 1: Report smoke implementation status to the
  Project Owner.
- Phase 10. Stage 1. Action 2: State that the main full training budget has
  not been run unless already explicitly authorized.
- Phase 10. Stage 1. Action 3: Ask for explicit authorization before running
  the full candidate set with `4` training replicates and `64` episodes per
  candidate.
- Phase 10. Stage 1. Action 4: Do not proceed to the main budget without that
  authorization.

#### Phase 10. Stage 2: Main Run If Authorized

- Phase 10. Stage 2. Action 1: If authorized, run the main artifact set under:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts/full_001/
  ```

- Phase 10. Stage 2. Action 2: Use all eligible candidates unless the Project
  Owner specifies a cap.
- Phase 10. Stage 2. Action 3: Use training replicates `4` unless overridden.
- Phase 10. Stage 2. Action 4: Use episodes `64` unless overridden.
- Phase 10. Stage 2. Action 5: Summarize the main artifact set.
- Phase 10. Stage 2. Action 6: Generate the human-readable readout from the
  repo readout source.
- Phase 10. Stage 2. Action 7: Record exact commands and outputs in the
  implementation log.

### Phase 11: Final Verification And Documentation

#### Phase 11. Stage 1: Final Test Pass

- Phase 11. Stage 1. Action 1: Run targeted new-package tests.
- Phase 11. Stage 1. Action 2: Run relevant counterpoint regression tests.
- Phase 11. Stage 1. Action 3: Run relevant CLI tests.
- Phase 11. Stage 1. Action 4: Run `git diff --check`.
- Phase 11. Stage 1. Action 5: Record results in the implementation log.

#### Phase 11. Stage 2: Documentation Updates

- Phase 11. Stage 2. Action 1: Update the design folder README status.
- Phase 11. Stage 2. Action 2: Update the top-level
  `system_learning_from_evaluations` index status.
- Phase 11. Stage 2. Action 3: Update root README or contributing docs only if
  the implemented evaluation changes the current workflow description.
- Phase 11. Stage 2. Action 4: Record generated readout path and runbook
  command.

#### Phase 11. Stage 3: Final Status

- Phase 11. Stage 3. Action 1: Run `git status --short --branch`.
- Phase 11. Stage 3. Action 2: Summarize files changed.
- Phase 11. Stage 3. Action 3: Summarize tests run and artifact runs
  completed.
- Phase 11. Stage 3. Action 4: Summarize any decision-locked items not run.
- Phase 11. Stage 3. Action 5: Do not claim the main full training result
  exists unless the full authorized artifact run was actually completed.

## Implementation Log Checklist Template

The implementation log should maintain this checklist and update statuses as
work proceeds.

```text
Phase 0. Stage 0. Action 1: pending
Phase 0. Stage 0. Action 2: pending
Phase 0. Stage 0. Action 3: pending
Phase 0. Stage 1. Action 1: pending
Phase 0. Stage 1. Action 2: pending
Phase 0. Stage 1. Action 3: pending
Phase 0. Stage 1. Action 4: pending
Phase 0. Stage 1. Action 5: pending
Phase 0. Stage 2. Action 1: pending
Phase 0. Stage 2. Action 2: pending
Phase 0. Stage 2. Action 3: pending
Phase 0. Stage 2. Action 4: pending
Phase 0. Stage 2. Action 5: pending
Phase 0. Stage 2. Action 6: pending
Phase 0. Stage 3. Action 1: pending
Phase 0. Stage 3. Action 2: pending
Phase 0. Stage 3. Action 3: pending
Phase 1. Stage 1 through Phase 11. Stage 3: pending, expand in the log from
this workplan before implementation begins.
```

The log may expand the remaining phases into a complete checklist, but it must
not delete or weaken any Phase.Stage.Action item from this workplan.

## Command Templates

Implementation smoke command shape:

```text
uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate-full-train run \
  --artifact-root <repo-root>/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts/smoke_001 \
  --candidate-readout-source <repo-root>/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json \
  --candidate-cap 2 \
  --training-replicates 1 \
  --episodes 4 \
  --locked-by codex \
  --linearization-mode tensor_available_disabled
```

Summarize command shape:

```text
uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate-full-train summarize \
  --artifact-root <repo-root>/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts/smoke_001
```

Human-readable protocol command:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-root>/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
```

Main budget command shape, only after explicit Project Owner authorization:

```text
uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate-full-train run \
  --artifact-root <repo-root>/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts/full_001 \
  --candidate-readout-source <repo-root>/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json \
  --training-replicates 4 \
  --episodes 64 \
  --locked-by foster \
  --linearization-mode tensor_available_disabled
```

## Completion Criteria

Implementation is complete only when:

- all non-decision-locked Phase.Stage.Action items have been completed as
  written;
- no source edits were made to `<state-collapser-repo>`;
- no counterpoint environment semantics were changed;
- candidate selection is derived from the parent readout source;
- learner state persists across episodes inside a training replicate;
- required artifacts and evaluation-level tables are generated;
- repo-side `readout_source.json` exists;
- the human-readable docs can be generated from that source binding;
- targeted tests and `git diff --check` pass;
- implementation log records completed actions, test results, smoke artifacts,
  and any decision-locked full-budget status.

## Final Reporting Requirements

When this workplan is executed, the final report must include:

- branch name;
- implementation log path;
- artifact root used for smoke;
- readout source path;
- tests run;
- whether the main full budget was run or remains decision-locked;
- any stopped or blocked Phase.Stage.Action item.

The final report must not claim:

- direct-vs-tower comparison;
- tower advantage;
- deep tower validation;
- main full-budget result if only smoke ran.

