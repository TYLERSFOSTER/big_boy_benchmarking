# Counterpoint Threshold Frontier Probe Implementation Gameplan

Date: 2026-06-05

Status: implementation gameplan, not executed

Repository:

```text
/Users/foster/big_boy_benchmarking
```

Source blueprint:

```text
docs/design/first_counterpoint_environment/threshold_frontier_probe/01_001_counterpoint_threshold_frontier_probe_blueprint.md
```

## Purpose

This gameplan translates the threshold-frontier probe blueprint into
Phase.Stage.Action implementation work.

The target evaluation is:

```text
counterpoint_threshold_frontier_probe_v001
```

The evaluation sweeps reward threshold `R` while holding the corrected
candidate chain, schema arms, seed policy, and small smoke-budget shape fixed.

It tests:

```text
Where is the sustained-hit frontier for Schema 0 versus Schema 1?
```

The schema arms are:

```text
Schema 0: schema0_no_contraction
Schema 1: schema1_noisy_rate_one_drop, using the corrected full-iterated
          noisy-rate candidate source
```

The locked threshold grid is:

```text
R = 12.0, 13.0, 13.25, 13.5, 13.75, 14.0
```

The first intended budget is:

```text
candidate_cap = 1
replicates_per_arm = 1
episodes_per_arm = 8
window_length = 5
required_count = 4
base_seed = 0
linearization_mode = tensor_available_disabled
liftability_semantics = state_collapser_v072_pointwise
```

This is a next-measure threshold-frontier probe. It is not a final serious
comparison and must not be presented as statistically stable evidence.

## Execution Authority Status

The Project Owner requested this gameplan:

```text
Following `prime_directive`, generate and extremely detailed implementation
gameplan from
`docs/design/first_counterpoint_environment/threshold_frontier_probe/01_001_counterpoint_threshold_frontier_probe_blueprint.md`
in Phase.Stage.Action format
```

Therefore this document may be written now.

This instruction is not implementation approval.

If the Project Owner later says to execute this exact gameplan, implementation
must follow this document as written. If any Phase.Stage.Action item cannot be
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
- `docs/design/first_counterpoint_environment/threshold_frontier_probe/README.md`
- `docs/design/first_counterpoint_environment/threshold_frontier_probe/01_001_counterpoint_threshold_frontier_probe_blueprint.md`
- `docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/readout_source.json`
- `docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/README.md`
- `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json`
- current `src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/` source as reusable per-threshold execution context
- current `src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/` source as reusable candidate-source context
- current `src/big_boy_benchmarking/cli/main.py` command registration
- current `tests/environments/counterpoint/test_second_serious_comparison.py`
  and adjacent counterpoint evaluation tests

## PO Attribution Preservation

This gameplan preserves the source blueprint's PO Attribution Ledger. It does
not add invented Project Owner turns.

Project Owner-originated requests carried into implementation:

1. The Project Owner asked for next-measure evaluation directions, not a
   full-blown final claim.
2. The Project Owner asked for design folders for the next-measure directions.
3. The Project Owner asked for blueprints in the respective folders.
4. The Project Owner stated that answers would be written in the documents.
5. The Project Owner requested this Phase.Stage.Action implementation
   gameplan.

Project Owner answers present in the blueprint:

1. The Project Owner agreed to the recommended evaluation identity, repo
   readout surface, artifact-root shape, and first run label.
2. The Project Owner selected the recommended threshold grid:

   ```text
   12.0, 13.0, 13.25, 13.5, 13.75, 14.0
   ```

3. The Project Owner agreed to the recommended first next-measure budget:

   ```text
   candidate_cap = 1
   replicates_per_arm = 1
   episodes_per_arm = 8
   window_length = 5
   required_count = 4
   base_seed = 0
   ```

4. The Project Owner agreed to the runner architecture recommendation.
5. The Project Owner agreed to the required artifact-table set.
6. The Project Owner agreed to the readout requirements.
7. The Project Owner identified the final repeated open questions as already
   decided or delegated:

   ```text
   Didn't we decide this above? What's going on?
   ```

   and:

   ```text
   I'm not answerign these last ones. You decide.
   ```

Consultant decisions under that delegation:

- Use the new evaluation id and repo readout surface already recommended in
  the blueprint.
- Badge highest shared passing threshold and whether a Schema 1-only passing
  threshold exists, plus artifacts, thresholds tested, liftability semantics,
  lift failures, and provenance.

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
- full-tower candidate diagnostics;
- small paired replicate probe design;
- `/Users/foster/state_collapser`.

### Candidate Source Lock

Default candidate source:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
```

Expected candidate id:

```text
counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0
```

Expected instance:

```text
counterpoint_symbolic_n3_wide_20_108_span18_v001
```

The candidate source must be validated at execution time. Do not assume the
checked-in readout still exposes the expected candidate without reading it.

### Threshold Grid Lock

Use exactly:

```text
12.0
13.0
13.25
13.5
13.75
14.0
```

Do not tune the threshold grid after inspecting frontier outcomes.

### Schema Comparison Lock

The evaluation compares schema arms under matched candidate/seed/budget
conditions:

```text
Schema 0: schema0_no_contraction
Schema 1: schema1_noisy_rate_one_drop
```

Do not convert this evaluation into:

- small paired replicate probe;
- old direct-runner comparison;
- direct-vs-tower generic benchmark;
- noisy-rate candidate selection;
- full-tower training-health diagnostic;
- structural collapse diagnostic;
- broad abstraction superiority claim.

### Per-Threshold Composition Lock

The frontier probe may reuse the existing second-serious comparison machinery,
but the top-level evaluation identity must be frontier-specific.

Per-threshold work should live under threshold-scoped sub-artifact roots inside
the frontier artifact root, for example:

```text
<frontier-artifact-root>/threshold_runs/r012000/
<frontier-artifact-root>/threshold_runs/r013000/
<frontier-artifact-root>/threshold_runs/r013250/
<frontier-artifact-root>/threshold_runs/r013500/
<frontier-artifact-root>/threshold_runs/r013750/
<frontier-artifact-root>/threshold_runs/r014000/
```

The top-level frontier evaluation root must be:

```text
<frontier-artifact-root>/evaluations/counterpoint_threshold_frontier_probe_v001/
```

This avoids presenting the result as a pile of unrelated manual reruns.

### Threshold Policy Lock

Threshold policy shape:

```text
metric_id = episode_total_reward
comparison = greater_than_or_equal
window_length = 5
required_count = 4
scope = total_space
```

The only varied field is numeric `threshold_value`.

### Artifact Lock

Durable artifacts must be repo-resident under:

```text
docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts/<run-label>/
```

The repo-side readout source must be:

```text
docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/readout_source.json
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
- the corrected candidate source no longer exposes an eligible candidate;
- `state_collapser` is not version `0.7.2` or newer with pointwise semantics
  available;
- per-threshold execution cannot reuse second-serious behavior without losing
  frontier-specific provenance;
- any threshold run has lift failures that make the frontier claim invalid;
- any threshold run emits incomplete artifacts for one arm while the other arm
  succeeds, unless the result can be honestly classified as blocked;
- `readout_source.json` cannot represent threshold-indexed source files;
- implementation would silently collapse the frontier-specific tables into
  only existing second-serious tables;
- generated readouts would need to be written outside the repo readout surface;
- implementation would tune thresholds after inspecting outcomes;
- implementation would present the result as statistically stable or
  full-blown serious evidence.

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
  on 2026-06-05 but was not implementation approval.

#### Phase 0. Stage 1: Working Tree And Branch Discipline

- Phase 0. Stage 1. Action 1: Run `git status --short --branch`.
- Phase 0. Stage 1. Action 2: Identify unrelated dirty files, especially root
  TeX files, generated TeX sidecars, evaluation readout conversations, and
  artifact roots from prior runs.
- Phase 0. Stage 1. Action 3: Stop if unrelated dirty state would be touched,
  staged, reverted, or mixed into this implementation.
- Phase 0. Stage 1. Action 4: Create and switch to:

  ```text
  codex/threshold-frontier-probe
  ```

- Phase 0. Stage 1. Action 5: Record branch creation and initial dirty state
  in the implementation log.

#### Phase 0. Stage 2: Source Re-Read

- Phase 0. Stage 2. Action 1: Re-read Prime Directive source authority listed
  in this gameplan.
- Phase 0. Stage 2. Action 2: Re-read the source blueprint.
- Phase 0. Stage 2. Action 3: Re-read the threshold-frontier README.
- Phase 0. Stage 2. Action 4: Re-read the current second-serious comparison
  readout source and README.
- Phase 0. Stage 2. Action 5: Re-read the current noisy-rate full-tower
  training readout source and candidate summary.
- Phase 0. Stage 2. Action 6: Re-read the full
  `second_serious_comparison` package.
- Phase 0. Stage 2. Action 7: Re-read the full
  `noisy_rate_full_training` package portions that load candidate summaries.
- Phase 0. Stage 2. Action 8: Re-read `src/big_boy_benchmarking/cli/main.py`
  counterpoint registration and dispatch code.
- Phase 0. Stage 2. Action 9: Re-read current counterpoint tests for
  second-serious comparison, full-tower training, docs writers, and CLI.
- Phase 0. Stage 2. Action 10: Record source surface mapping in the
  implementation log.

#### Phase 0. Stage 3: Implementation Log

- Phase 0. Stage 3. Action 1: Create:

  ```text
  docs/design/first_counterpoint_environment/threshold_frontier_probe/01_003_counterpoint_threshold_frontier_probe_implementation_log.md
  ```

- Phase 0. Stage 3. Action 2: Include branch, execution instruction, source
  gameplan, initial dirty state, stop conditions, and running
  Phase.Stage.Action checklist.
- Phase 0. Stage 3. Action 3: Keep the log updated throughout implementation.

### Phase 1: Evaluation Identity, Package, Config, And Paths

#### Phase 1. Stage 1: Evaluation Constants

- Phase 1. Stage 1. Action 1: Add evaluation id:

  ```text
  counterpoint_threshold_frontier_probe_v001
  ```

- Phase 1. Stage 1. Action 2: Add run family id:

  ```text
  counterpoint_symbolic_v001_threshold_frontier_probe_v001
  ```

- Phase 1. Stage 1. Action 3: Add run mode id:

  ```text
  threshold_frontier_probe_v001
  ```

- Phase 1. Stage 1. Action 4: Reuse schema class ids:

  ```text
  schema0_no_contraction
  schema1_noisy_rate_one_drop
  ```

- Phase 1. Stage 1. Action 5: Add stable claim and badge ids for thresholds
  tested, frontier status, highest shared passing threshold, Schema 1-only
  passing threshold, liftability semantics, lift failures, and provenance.
- Phase 1. Stage 1. Action 6: Keep all existing counterpoint ids unchanged.
- Phase 1. Stage 1. Action 7: Add tests proving new ids are exported,
  stable, and non-colliding.

#### Phase 1. Stage 2: Package Scaffold

- Phase 1. Stage 2. Action 1: Create package:

  ```text
  src/big_boy_benchmarking/environments/counterpoint/threshold_frontier_probe/
  ```

- Phase 1. Stage 2. Action 2: Add `__init__.py`.
- Phase 1. Stage 2. Action 3: Add `config.py`.
- Phase 1. Stage 2. Action 4: Add `paths.py`.
- Phase 1. Stage 2. Action 5: Add `thresholds.py`.
- Phase 1. Stage 2. Action 6: Add `candidate_source.py`.
- Phase 1. Stage 2. Action 7: Add `runner.py`.
- Phase 1. Stage 2. Action 8: Add `aggregation.py`.
- Phase 1. Stage 2. Action 9: Add `manifests.py`.
- Phase 1. Stage 2. Action 10: Add `docs_writer.py`.
- Phase 1. Stage 2. Action 11: Add `badges.py` only if the existing docs
  writer pattern keeps badge policy outside `docs_writer.py`; otherwise keep
  badge generation in the local docs writer.
- Phase 1. Stage 2. Action 12: Do not copy-paste old modules blindly; reuse
  second-serious functions by import where exact semantics match.

#### Phase 1. Stage 3: Budget Configuration

- Phase 1. Stage 3. Action 1: Define `ThresholdFrontierProbeBudget`.
- Phase 1. Stage 3. Action 2: Include `environment_instance_id`, default:

  ```text
  counterpoint_symbolic_n3_wide_20_108_span18_v001
  ```

- Phase 1. Stage 3. Action 3: Include `candidate_readout_source`, default:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
  ```

- Phase 1. Stage 3. Action 4: Include `candidate_id` as optional explicit
  targeting.
- Phase 1. Stage 3. Action 5: Include `candidate_cap`, default `1`.
- Phase 1. Stage 3. Action 6: Include `threshold_values`, default exactly:

  ```text
  12.0,13.0,13.25,13.5,13.75,14.0
  ```

- Phase 1. Stage 3. Action 7: Include `training_replicates_per_arm`, default
  `1`.
- Phase 1. Stage 3. Action 8: Include `episodes_per_replicate`, default `16`.
- Phase 1. Stage 3. Action 9: Include `window_length`, default `5`.
- Phase 1. Stage 3. Action 10: Include `required_count`, default `4`.
- Phase 1. Stage 3. Action 11: Include `base_seed`, default `0`.
- Phase 1. Stage 3. Action 12: Include `linearization_mode_id`, default:

  ```text
  tensor_available_disabled
  ```

- Phase 1. Stage 3. Action 13: Include `locked_by`.
- Phase 1. Stage 3. Action 14: Include `run_mode`.
- Phase 1. Stage 3. Action 15: Validate that the threshold grid is
  non-empty, numeric, unique, and sorted.
- Phase 1. Stage 3. Action 16: Validate that the default threshold grid
  matches the blueprint lock.
- Phase 1. Stage 3. Action 17: Validate that the first meaningful default
  budget is exactly `candidate_cap=1`, `replicates=1`, and `episodes=8`.

#### Phase 1. Stage 4: Path Contracts

- Phase 1. Stage 4. Action 1: Define repo readout surface:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/
  ```

- Phase 1. Stage 4. Action 2: Define default artifact root under:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts/<run-label>/
  ```

- Phase 1. Stage 4. Action 3: Define evaluation root under:

  ```text
  <artifact-root>/evaluations/counterpoint_threshold_frontier_probe_v001/
  ```

- Phase 1. Stage 4. Action 4: Define run family root under:

  ```text
  <artifact-root>/runs/counterpoint_symbolic_v001_threshold_frontier_probe_v001/
  ```

- Phase 1. Stage 4. Action 5: Define threshold-run root under:

  ```text
  <artifact-root>/threshold_runs/<threshold-label>/
  ```

- Phase 1. Stage 4. Action 6: Define threshold label formatting:

  ```text
  r012000
  r013000
  r013250
  r013500
  r013750
  r014000
  ```

- Phase 1. Stage 4. Action 7: Add repo-resident path validation.
- Phase 1. Stage 4. Action 8: Add readout-source path validation.
- Phase 1. Stage 4. Action 9: Add artifact-root collision protection unless
  an explicit overwrite/update flag already exists in local pattern.
- Phase 1. Stage 4. Action 10: Add tests for default paths, threshold labels,
  absolute path resolution, outside-repo rejection for repo readout surfaces,
  and artifact-root label extraction.

### Phase 2: Candidate Source And Threshold Schedule

#### Phase 2. Stage 1: Candidate Source Resolution

- Phase 2. Stage 1. Action 1: Reuse the candidate loading logic from
  `second_serious_comparison.candidates` or
  `noisy_rate_full_training.candidate_selection` where semantics match.
- Phase 2. Stage 1. Action 2: Validate that the candidate readout source
  exists and is a repo-side `readout_source.json`.
- Phase 2. Stage 1. Action 3: Validate that the source artifact root is
  repo-resident.
- Phase 2. Stage 1. Action 4: Validate that at least one candidate is eligible.
- Phase 2. Stage 1. Action 5: Validate the expected environment instance:

  ```text
  counterpoint_symbolic_n3_wide_20_108_span18_v001
  ```

- Phase 2. Stage 1. Action 6: Validate candidate id targeting if supplied.
- Phase 2. Stage 1. Action 7: Apply `candidate_cap = 1`.
- Phase 2. Stage 1. Action 8: Write `candidate_manifest.json`.
- Phase 2. Stage 1. Action 9: Write `parent_source_manifest.json`.
- Phase 2. Stage 1. Action 10: Add tests for missing source, ineligible
  candidate, wrong instance, candidate-cap handling, and candidate-id targeting.

#### Phase 2. Stage 2: Threshold Schedule

- Phase 2. Stage 2. Action 1: Parse threshold values from CLI as comma-separated
  floats.
- Phase 2. Stage 2. Action 2: Preserve the numeric values exactly enough for
  path labels, table values, and budget locks to agree.
- Phase 2. Stage 2. Action 3: Sort thresholds ascending only if the input order
  is explicitly documented as order-insensitive; otherwise reject unsorted
  values.
- Phase 2. Stage 2. Action 4: Write `threshold_frontier_policy_manifest.json`.
- Phase 2. Stage 2. Action 5: Include threshold labels, threshold values,
  metric id, comparison, window length, required count, source of threshold
  grid, and claim boundary.
- Phase 2. Stage 2. Action 6: Add tests for default grid, explicit grid,
  duplicate values, malformed values, unsorted values, and label formatting.

#### Phase 2. Stage 3: Per-Threshold Budget Construction

- Phase 2. Stage 3. Action 1: For each threshold value, construct a
  second-serious comparison budget with the same candidate, seed, and budget
  settings.
- Phase 2. Stage 3. Action 2: Set `schema1_tower_source` to:

  ```text
  full_iterated_noisy_rate
  ```

- Phase 2. Stage 3. Action 3: Set `run_mode` to the existing smoke
  second-serious mode for per-threshold subruns:

  ```text
  smoke_schema_comparison_first_sustained_hit
  ```

- Phase 2. Stage 3. Action 4: Set `threshold_value` to the current threshold.
- Phase 2. Stage 3. Action 5: Use the same `base_seed` for all thresholds so
  threshold differences are not confounded by seed changes.
- Phase 2. Stage 3. Action 6: Add tests that all per-threshold budgets differ
  only in threshold value and threshold label.

### Phase 3: Runner Implementation

#### Phase 3. Stage 1: Runner Composition

- Phase 3. Stage 1. Action 1: Implement `run_threshold_frontier_probe`.
- Phase 3. Stage 1. Action 2: Compose existing second-serious comparison
  machinery for each threshold value where exact behavior matches the
  blueprint.
- Phase 3. Stage 1. Action 3: Use a threshold-scoped sub-artifact root for
  each composed second-serious run.
- Phase 3. Stage 1. Action 4: Preserve second-serious threshold/persistence
  semantics.
- Phase 3. Stage 1. Action 5: Preserve second-serious Schema 0 construction.
- Phase 3. Stage 1. Action 6: Preserve second-serious full-iterated noisy-rate
  Schema 1 construction.
- Phase 3. Stage 1. Action 7: Preserve v0.7.2 pointwise liftability semantics.
- Phase 3. Stage 1. Action 8: Ensure the top-level evaluation id/run family id
  is the threshold-frontier id, not the second-serious comparison id.
- Phase 3. Stage 1. Action 9: Ensure all top-level frontier manifests and
  aggregate tables live under the frontier evaluation root.
- Phase 3. Stage 1. Action 10: If second-serious runner reuse would overwrite
  the canonical second-serious repo readout source, call only the lower-level
  runner or aggregation pieces needed for threshold subruns, or stop and ask.

#### Phase 3. Stage 2: Threshold Run Loop

- Phase 3. Stage 2. Action 1: For each selected candidate, create a frontier
  candidate group.
- Phase 3. Stage 2. Action 2: For each threshold value in the locked grid,
  create a threshold label.
- Phase 3. Stage 2. Action 3: Create a threshold-scoped sub-artifact root.
- Phase 3. Stage 2. Action 4: Run the matched Schema 0/Schema 1 comparison for
  that threshold.
- Phase 3. Stage 2. Action 5: Aggregate that threshold's second-serious raw
  run artifacts into threshold-local result tables.
- Phase 3. Stage 2. Action 6: Record the threshold run in
  `threshold_run_manifest.json`.
- Phase 3. Stage 2. Action 7: Record every per-threshold Schema 0 and Schema 1
  arm run in the top-level frontier run index.
- Phase 3. Stage 2. Action 8: If a threshold subrun fails, preserve all written
  evidence and classify that threshold as blocked rather than discarding it.
- Phase 3. Stage 2. Action 9: Do not tune or skip later thresholds after seeing
  earlier threshold outcomes.

#### Phase 3. Stage 3: Per-Threshold Evidence Preservation

- Phase 3. Stage 3. Action 1: Preserve the per-threshold `evaluation_run_index.csv`.
- Phase 3. Stage 3. Action 2: Preserve the per-threshold
  `evaluation_aggregate_table.csv`.
- Phase 3. Stage 3. Action 3: Preserve the per-threshold
  `evaluation_aggregate_summary.json`.
- Phase 3. Stage 3. Action 4: Preserve the per-threshold
  `results/arm_summary.csv`.
- Phase 3. Stage 3. Action 5: Preserve the per-threshold
  `results/first_sustained_hit_summary.csv`.
- Phase 3. Stage 3. Action 6: Preserve the per-threshold
  `results/paired_schema_comparison.csv`.
- Phase 3. Stage 3. Action 7: Preserve per-threshold lift success/failure
  tables.
- Phase 3. Stage 3. Action 8: Preserve per-threshold tower shape tables.
- Phase 3. Stage 3. Action 9: Preserve per-threshold timing evidence.
- Phase 3. Stage 3. Action 10: Preserve per-threshold manifests that prove the
  threshold value and candidate source.

#### Phase 3. Stage 4: Top-Level Evaluation Manifests

- Phase 3. Stage 4. Action 1: Write `evaluation_manifest.json`.
- Phase 3. Stage 4. Action 2: Write `evaluation_budget_lock.json`.
- Phase 3. Stage 4. Action 3: Write `evaluation_arm_manifest.json`.
- Phase 3. Stage 4. Action 4: Write `threshold_frontier_policy_manifest.json`.
- Phase 3. Stage 4. Action 5: Write `threshold_run_manifest.json`.
- Phase 3. Stage 4. Action 6: Write `parent_source_manifest.json`.
- Phase 3. Stage 4. Action 7: Write `candidate_manifest.json`.
- Phase 3. Stage 4. Action 8: Write top-level `evaluation_run_index.csv`.
- Phase 3. Stage 4. Action 9: Write run-family `summary.json`.
- Phase 3. Stage 4. Action 10: Add tests proving every manifest contains
  evaluation id, run family id, artifact schema version, budget, source
  binding, threshold grid, and claim-boundary context.

### Phase 4: Aggregation And Result Tables

#### Phase 4. Stage 1: Threshold Arm Summary

- Phase 4. Stage 1. Action 1: Read every per-threshold arm summary and
  first-sustained-hit row.
- Phase 4. Stage 1. Action 2: Write `results/threshold_arm_summary.csv`.
- Phase 4. Stage 1. Action 3: Include per threshold and schema arm:

  ```text
  threshold_value
  threshold_label
  schema_class_id
  run_count
  sustained_hit_count
  transient_hit_count
  never_hit_count
  artifact_incomplete_count
  sustained_hit_rate
  median_episodes_to_sustained_hit
  mean_episodes_to_sustained_hit
  post_hit_window_mean
  post_hit_window_min
  post_hit_window_success_count
  ```

- Phase 4. Stage 1. Action 4: Add tests for sustained, transient, never-hit,
  and artifact-incomplete aggregation by threshold.

#### Phase 4. Stage 2: Threshold Pair Summary

- Phase 4. Stage 2. Action 1: Read every per-threshold paired comparison row.
- Phase 4. Stage 2. Action 2: Write `results/threshold_pair_summary.csv`.
- Phase 4. Stage 2. Action 3: Include:

  ```text
  threshold_value
  threshold_label
  candidate_group_id
  seed_bundle_id
  training_replicate_index
  schema0_run_id
  schema1_run_id
  schema0_hit_status
  schema1_hit_status
  schema0_episodes_to_hit
  schema1_episodes_to_hit
  schema1_minus_schema0_episodes_to_hit
  schema0_post_hit_window_mean
  schema1_post_hit_window_mean
  schema1_minus_schema0_post_hit_window_mean
  schema0_post_hit_window_min
  schema1_post_hit_window_min
  schema1_minus_schema0_post_hit_window_min
  schema0_post_hit_success_count
  schema1_post_hit_success_count
  schema1_minus_schema0_post_hit_success_count
  pair_status
  claim_blocked
  interpretation
  ```

- Phase 4. Stage 2. Action 4: Preserve speed-to-hit delta from the
  per-threshold paired comparison.
- Phase 4. Stage 2. Action 5: Add post-hit margin deltas even if speed-to-hit
  delta is zero.
- Phase 4. Stage 2. Action 6: Add tests for same-hit, Schema 1 faster,
  Schema 1 slower, Schema 1 margin higher, Schema 1 margin lower, and blocked
  threshold rows.

#### Phase 4. Stage 3: Post-Hit Margin Summary

- Phase 4. Stage 3. Action 1: Write `results/post_hit_margin_summary.csv`.
- Phase 4. Stage 3. Action 2: Include per threshold and schema arm:

  ```text
  threshold_value
  schema_class_id
  post_hit_window_mean
  post_hit_window_min
  post_hit_window_success_count
  threshold_margin_mean
  threshold_margin_min
  threshold_success_fraction
  ```

- Phase 4. Stage 3. Action 3: Include pairwise margin deltas when both arms
  are comparable.
- Phase 4. Stage 3. Action 4: Add tests for threshold margin computation and
  missing post-hit windows.

#### Phase 4. Stage 4: First Failure Frontier Summary

- Phase 4. Stage 4. Action 1: Write
  `results/first_failure_frontier_summary.csv`.
- Phase 4. Stage 4. Action 2: For each schema arm, compute the first threshold
  where sustained-hit fails.
- Phase 4. Stage 4. Action 3: For each schema arm, compute the highest
  threshold where sustained-hit passes.
- Phase 4. Stage 4. Action 4: Classify arms that pass all thresholds as
  `no_failure_observed`.
- Phase 4. Stage 4. Action 5: Classify arms that fail all thresholds as
  `no_passing_threshold_observed`.
- Phase 4. Stage 4. Action 6: Add tests for all-pass, all-fail, and mixed
  frontier cases.

#### Phase 4. Stage 5: Frontier Summary

- Phase 4. Stage 5. Action 1: Write `results/frontier_summary.csv`.
- Phase 4. Stage 5. Action 2: Include:

  ```text
  candidate_group_id
  threshold_count
  highest_shared_passing_threshold
  highest_schema0_passing_threshold
  highest_schema1_passing_threshold
  schema1_only_passing_thresholds
  schema0_only_passing_thresholds
  schema1_frontier_minus_schema0_frontier
  schema1_margin_win_count
  schema1_margin_loss_count
  schema1_margin_same_count
  blocked_threshold_count
  lift_failure_threshold_count
  recommended_replicate_probe_threshold
  claim_status
  bounded_claim_text
  ```

- Phase 4. Stage 5. Action 3: Define `recommended_replicate_probe_threshold`.
- Phase 4. Stage 5. Action 4: Recommended threshold selection rule:

  ```text
  choose the lowest threshold near the frontier where Schema 0 begins to wobble
  or fail while Schema 1 remains sustained; if no such threshold exists, choose
  the highest tested threshold with both arms unblocked and Schema 1 positive
  margin, else choose 13.0 as fallback with an inconclusive note.
  ```

- Phase 4. Stage 5. Action 5: Define bounded claim statuses:

  ```text
  schema1_frontier_advantage_observed
  schema1_margin_advantage_only
  no_frontier_separation_observed
  schema1_frontier_disadvantage_observed
  frontier_blocked_by_artifacts
  frontier_blocked_by_liftability
  frontier_inconclusive
  ```

- Phase 4. Stage 5. Action 6: Add tests for every claim status.

#### Phase 4. Stage 6: Lift, Tower, And Timing Tables

- Phase 4. Stage 6. Action 1: Promote all per-threshold tower shape rows into
  `results/tower_shape_summary.csv`.
- Phase 4. Stage 6. Action 2: Add threshold value and threshold label to every
  promoted tower row.
- Phase 4. Stage 6. Action 3: Promote lift successes into
  `results/lift_success_by_tier.csv`.
- Phase 4. Stage 6. Action 4: Promote lift failures into
  `results/lift_failure_by_tier.csv`.
- Phase 4. Stage 6. Action 5: Add threshold value and threshold label to every
  promoted lift row.
- Phase 4. Stage 6. Action 6: Promote timing evidence into
  `results/timing_summary.csv`.
- Phase 4. Stage 6. Action 7: Preserve `liftability_semantics_id` and
  `tower_invariant_report` summary fields in evaluation-level tables.
- Phase 4. Stage 6. Action 8: Add tests that zero lift failures produce a real
  empty table with headers or an explicitly documented empty-file convention,
  matching existing readout protocol expectations.

#### Phase 4. Stage 7: Aggregate Table And Summary

- Phase 4. Stage 7. Action 1: Write `evaluation_aggregate_table.csv`.
- Phase 4. Stage 7. Action 2: Write `evaluation_aggregate_summary.json`.
- Phase 4. Stage 7. Action 3: Include artifact status, threshold counts,
  per-threshold run counts, pair counts, unblocked threshold counts, frontier
  values, margin win counts, lift-failure counts, recommended replicate
  threshold, and claim status.
- Phase 4. Stage 7. Action 4: Include expected-file classifications.
- Phase 4. Stage 7. Action 5: Add tests that aggregate table and summary can
  drive the artifact-table readout protocol without inferring intent from code.

### Phase 5: Readout Source And Human-Readable Docs

#### Phase 5. Stage 1: Readout Source Binding

- Phase 5. Stage 1. Action 1: Generate repo-side `readout_source.json` in:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/
  ```

- Phase 5. Stage 1. Action 2: Include `repo_readout_surface`.
- Phase 5. Stage 1. Action 3: Include `source_artifact_root`.
- Phase 5. Stage 1. Action 4: Include `source_evaluation_root`.
- Phase 5. Stage 1. Action 5: Include `evaluation_id`.
- Phase 5. Stage 1. Action 6: Include `environment_instance_id`.
- Phase 5. Stage 1. Action 7: Include `artifact_run_label`.
- Phase 5. Stage 1. Action 8: Include `run_mode`.
- Phase 5. Stage 1. Action 9: Include `budget`.
- Phase 5. Stage 1. Action 10: Include `threshold_grid`.
- Phase 5. Stage 1. Action 11: Include `threshold_frontier_policy`.
- Phase 5. Stage 1. Action 12: Include `candidate_source`.
- Phase 5. Stage 1. Action 13: Include `threshold_run_manifest`.
- Phase 5. Stage 1. Action 14: Include complete `source_files`.
- Phase 5. Stage 1. Action 15: Include `expected_files`.
- Phase 5. Stage 1. Action 16: Include `goal_criteria`.
- Phase 5. Stage 1. Action 17: Include `badge_policy`.
- Phase 5. Stage 1. Action 18: Include `claim_boundary`.
- Phase 5. Stage 1. Action 19: Include
  `recommended_replicate_probe_threshold` when available.
- Phase 5. Stage 1. Action 20: Add tests for required readout-source keys.

#### Phase 5. Stage 2: Docs Writer

- Phase 5. Stage 2. Action 1: Implement `docs_writer.py` for the repo readout
  surface.
- Phase 5. Stage 2. Action 2: Write `README.md`.
- Phase 5. Stage 2. Action 3: Write `result_readout.md`.
- Phase 5. Stage 2. Action 4: Write `artifact_index.md`.
- Phase 5. Stage 2. Action 5: Write `glossary.md`.
- Phase 5. Stage 2. Action 6: Write `method.md`.
- Phase 5. Stage 2. Action 7: Write `runbook.md`.
- Phase 5. Stage 2. Action 8: Write `results/summary.md`.
- Phase 5. Stage 2. Action 9: Write `results/human_summary.md`.
- Phase 5. Stage 2. Action 10: Write `results/frontier_readout.md`.
- Phase 5. Stage 2. Action 11: Write `results/threshold_table.md`.
- Phase 5. Stage 2. Action 12: Write `results/paired_threshold_table.md`.
- Phase 5. Stage 2. Action 13: Write `results/timing_readout.md`.
- Phase 5. Stage 2. Action 14: Preserve `## Clarifying Questions And Turns`
  according to `artifact_table_to_readable_document_protocol.md`.
- Phase 5. Stage 2. Action 15: Add tests that docs writer does not erase
  existing user-authored clarifying turns.

#### Phase 5. Stage 3: Badges

- Phase 5. Stage 3. Action 1: Generate artifact status badge.
- Phase 5. Stage 3. Action 2: Generate thresholds-tested badge.
- Phase 5. Stage 3. Action 3: Generate frontier-status badge.
- Phase 5. Stage 3. Action 4: Generate highest-shared-passing-threshold badge.
- Phase 5. Stage 3. Action 5: Generate Schema 1-only passing-threshold badge
  when applicable.
- Phase 5. Stage 3. Action 6: Generate recommended-replicate-threshold badge
  when applicable.
- Phase 5. Stage 3. Action 7: Generate liftability-semantics badge.
- Phase 5. Stage 3. Action 8: Generate lift-failures badge.
- Phase 5. Stage 3. Action 9: Generate provenance badge.
- Phase 5. Stage 3. Action 10: Add tests for badge labels and color classes.

#### Phase 5. Stage 4: Readout Protocol Compatibility

- Phase 5. Stage 4. Action 1: Verify the generated readout can be regenerated
  using:

  ```text
  execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/readout_source.json
  ```

- Phase 5. Stage 4. Action 2: Ensure the README explicitly reminds the reader
  of that command.
- Phase 5. Stage 4. Action 3: Ensure the readout states that this is a
  threshold-frontier next-measure probe.
- Phase 5. Stage 4. Action 4: Ensure the readout does not require inspecting
  raw per-threshold second-serious files to understand the main frontier result.
- Phase 5. Stage 4. Action 5: Add tests for readout-source path invariants.

### Phase 6: CLI

#### Phase 6. Stage 1: Parser Registration

- Phase 6. Stage 1. Action 1: Add counterpoint command:

  ```text
  threshold-frontier
  ```

- Phase 6. Stage 1. Action 2: Add `run` subcommand.
- Phase 6. Stage 1. Action 3: Add `summarize` subcommand.
- Phase 6. Stage 1. Action 4: Add arguments:

  ```text
  --artifact-root
  --candidate-readout-source
  --candidate-id
  --candidate-cap
  --threshold-values
  --episodes
  --replicates
  --base-seed
  --locked-by
  --horizon
  --controller-event-ceiling
  --linearization-mode
  ```

- Phase 6. Stage 1. Action 5: Add argument validation that enforces the locked
  default threshold grid unless explicitly overridden by the command.
- Phase 6. Stage 1. Action 6: Add help text that makes this a threshold
  frontier probe, not a final serious comparison.

#### Phase 6. Stage 2: Run Dispatch

- Phase 6. Stage 2. Action 1: Wire CLI run args into
  `ThresholdFrontierProbeBudget`.
- Phase 6. Stage 2. Action 2: Enforce `tensor_available_disabled` with the
  same warning/error pattern as existing counterpoint evaluations.
- Phase 6. Stage 2. Action 3: Call the threshold frontier runner.
- Phase 6. Stage 2. Action 4: Print JSON with:

  ```text
  status
  evaluation_budget_lock
  evaluation_run_index
  candidate_manifest
  threshold_run_manifest
  threshold_count
  run_count
  pair_count
  ```

- Phase 6. Stage 2. Action 5: Add CLI tests for successful argument parsing,
  default threshold grid, explicit threshold grid, and malformed threshold
  rejection.

#### Phase 6. Stage 3: Summarize Dispatch

- Phase 6. Stage 3. Action 1: Wire CLI summarize args into aggregation and
  docs writer.
- Phase 6. Stage 3. Action 2: Require `--artifact-root`.
- Phase 6. Stage 3. Action 3: Accept optional `--docs-root`.
- Phase 6. Stage 3. Action 4: Print JSON with generated docs paths and
  recommended replicate threshold.
- Phase 6. Stage 3. Action 5: Add CLI tests for summarize output and readout
  source generation.

### Phase 7: Tests

#### Phase 7. Stage 1: Unit Tests

- Phase 7. Stage 1. Action 1: Create:

  ```text
  tests/environments/counterpoint/test_threshold_frontier_probe.py
  ```

- Phase 7. Stage 1. Action 2: Test config defaults.
- Phase 7. Stage 1. Action 3: Test path contracts.
- Phase 7. Stage 1. Action 4: Test threshold-grid parsing.
- Phase 7. Stage 1. Action 5: Test threshold-label formatting.
- Phase 7. Stage 1. Action 6: Test candidate source resolution.
- Phase 7. Stage 1. Action 7: Test per-threshold budget construction.
- Phase 7. Stage 1. Action 8: Test threshold arm summary aggregation.
- Phase 7. Stage 1. Action 9: Test threshold pair summary aggregation.
- Phase 7. Stage 1. Action 10: Test first-failure frontier summary.
- Phase 7. Stage 1. Action 11: Test frontier summary claim statuses.
- Phase 7. Stage 1. Action 12: Test recommended replicate threshold
  selection.
- Phase 7. Stage 1. Action 13: Test readout source required fields.
- Phase 7. Stage 1. Action 14: Test docs writer preserves clarifying turns.

#### Phase 7. Stage 2: Integration Tests

- Phase 7. Stage 2. Action 1: Add a tiny or synthetic fixture test that runs
  the evaluation with a reduced threshold grid and smallest locally valid
  budget.
- Phase 7. Stage 2. Action 2: Verify the run writes all required manifests.
- Phase 7. Stage 2. Action 3: Verify every threshold subrun writes or records
  evidence.
- Phase 7. Stage 2. Action 4: Verify the run writes all required result
  tables.
- Phase 7. Stage 2. Action 5: Verify summarize writes readout docs.
- Phase 7. Stage 2. Action 6: Verify no generated docs are written into the
  raw artifact tree as the canonical repo readout surface.
- Phase 7. Stage 2. Action 7: Verify zero lift failures are represented
  according to the chosen empty-table convention.

#### Phase 7. Stage 3: Regression Tests Against Existing Evaluations

- Phase 7. Stage 3. Action 1: Run existing second-serious comparison tests.
- Phase 7. Stage 3. Action 2: Run existing noisy-rate full-tower training
  tests.
- Phase 7. Stage 3. Action 3: Run existing serious-learning tests that cover
  threshold and sustained-hit machinery.
- Phase 7. Stage 3. Action 4: Run CLI tests that cover all counterpoint
  subcommands touched by parser edits.

### Phase 8: Validation Runs

#### Phase 8. Stage 1: Pre-Run Validation

- Phase 8. Stage 1. Action 1: Verify `state_collapser` version is `0.7.2` or
  newer.
- Phase 8. Stage 1. Action 2: Verify candidate source exposes at least one
  eligible corrected candidate.
- Phase 8. Stage 1. Action 3: Verify threshold grid is exactly:

  ```text
  12.0,13.0,13.25,13.5,13.75,14.0
  ```

- Phase 8. Stage 1. Action 4: Verify artifact root is new and clean.
- Phase 8. Stage 1. Action 5: Verify every per-threshold sub-artifact root is
  absent or explicitly authorized for overwrite.

#### Phase 8. Stage 2: Minimal Smoke Run

- Phase 8. Stage 2. Action 1: Run a minimal implementation smoke only after
  the Project Owner has approved execution.
- Phase 8. Stage 2. Action 2: Use a fresh repo artifact root such as:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts/smoke_001
  ```

- Phase 8. Stage 2. Action 3: Use minimal settings that complete quickly:

  ```text
  threshold_values = 12.0,13.0
  candidate_cap = 1
  replicates_per_arm = 1
  episodes_per_arm = 2 or 4
  ```

- Phase 8. Stage 2. Action 4: Label the run mode as smoke or implementation
  smoke rather than the first meaningful frontier run.
- Phase 8. Stage 2. Action 5: Summarize the smoke run.
- Phase 8. Stage 2. Action 6: Verify all required tables and readout docs
  exist.

#### Phase 8. Stage 3: First Meaningful Frontier Run

- Phase 8. Stage 3. Action 1: Run the first meaningful threshold-frontier
  probe only after smoke validation succeeds and Project Owner authorization
  exists for the artifact run.
- Phase 8. Stage 3. Action 2: Use a fresh repo artifact root:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts/v072_pointwise_frontier_001
  ```

- Phase 8. Stage 3. Action 3: Use:

  ```text
  threshold_values = 12.0,13.0,13.25,13.5,13.75,14.0
  candidate_cap = 1
  replicates_per_arm = 1
  episodes_per_arm = 8
  window_length = 5
  required_count = 4
  linearization_mode = tensor_available_disabled
  ```

- Phase 8. Stage 3. Action 4: Summarize the meaningful run.
- Phase 8. Stage 3. Action 5: Regenerate/read the human-facing surface using:

  ```text
  execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/readout_source.json
  ```

- Phase 8. Stage 3. Action 6: Verify the readout names a recommended threshold
  for the downstream small paired replicate probe.
- Phase 8. Stage 3. Action 7: Record run command, run result, summarize
  result, and readout generation result in the implementation log.

### Phase 9: Documentation And Repo Status

#### Phase 9. Stage 1: Root And Evaluation Documentation

- Phase 9. Stage 1. Action 1: Update root `README.md` only if current root
  documentation describes evaluation inventory or runnable evaluation workflow
  and would become misleading without this new probe.
- Phase 9. Stage 1. Action 2: Do not modify root TeX files.
- Phase 9. Stage 1. Action 3: Update any evaluation index docs that list
  counterpoint readouts, if such an index exists.
- Phase 9. Stage 1. Action 4: Ensure documentation states this is a
  next-measure threshold-frontier probe, not a full-blown final comparison.
- Phase 9. Stage 1. Action 5: Ensure documentation states that this probe is
  intended to feed the small paired replicate probe threshold choice.

#### Phase 9. Stage 2: Final Verification

- Phase 9. Stage 2. Action 1: Run focused tests for the new package.
- Phase 9. Stage 2. Action 2: Run existing impacted counterpoint tests.
- Phase 9. Stage 2. Action 3: Run formatting/lint checks used by this repo if
  available and already in use.
- Phase 9. Stage 2. Action 4: Run `git status --short`.
- Phase 9. Stage 2. Action 5: Verify no TeX/root generated sidecars were
  modified by this work.
- Phase 9. Stage 2. Action 6: Verify no files under `/Users/foster/state_collapser`
  were modified.
- Phase 9. Stage 2. Action 7: Verify all new artifact outputs are
  repo-resident under the threshold-frontier readout surface.
- Phase 9. Stage 2. Action 8: Verify no second-serious comparison readout was
  accidentally overwritten by per-threshold subruns unless explicitly intended
  and documented.

#### Phase 9. Stage 3: Implementation Log Completion

- Phase 9. Stage 3. Action 1: Update the implementation log with every
  completed Phase.Stage.Action item.
- Phase 9. Stage 3. Action 2: Record tests run and exact outcomes.
- Phase 9. Stage 3. Action 3: Record benchmark commands run and exact JSON
  completion results.
- Phase 9. Stage 3. Action 4: Record any stopped or deferred actions.
- Phase 9. Stage 3. Action 5: Record final repo status.

## Suggested Execution Commands After Implementation

These commands are not execution authorization. They are the intended command
shape once the gameplan has been implemented and the Project Owner has
approved the relevant run.

Minimal smoke:

```text
uv run python -m big_boy_benchmarking.cli counterpoint threshold-frontier run \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts/smoke_001 \
  --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json \
  --threshold-values 12.0,13.0 \
  --candidate-cap 1 \
  --episodes 4 \
  --replicates 1 \
  --locked-by foster \
  --linearization-mode tensor_available_disabled

uv run python -m big_boy_benchmarking.cli counterpoint threshold-frontier summarize \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts/smoke_001
```

First meaningful frontier:

```text
uv run python -m big_boy_benchmarking.cli counterpoint threshold-frontier run \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts/v072_pointwise_frontier_001 \
  --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json \
  --threshold-values 12.0,13.0,13.25,13.5,13.75,14.0 \
  --candidate-cap 1 \
  --episodes 16 \
  --replicates 1 \
  --locked-by foster \
  --linearization-mode tensor_available_disabled

uv run python -m big_boy_benchmarking.cli counterpoint threshold-frontier summarize \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts/v072_pointwise_frontier_001
```

Human-readable readout protocol:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/readout_source.json
```

## Acceptance Criteria

Implementation is complete only when:

- the new evaluation package exists and is tested;
- the CLI run/summarize commands exist and are tested;
- the evaluation runs the locked threshold grid without tuning;
- the evaluation preserves matched candidate/seed/budget conditions across
  thresholds;
- the evaluation writes all required manifests and tables;
- the evaluation writes repo-side readout source and human-readable docs;
- the evaluation can run a minimal smoke;
- the first meaningful frontier run is completed or explicitly deferred;
- the frontier readout names a recommended threshold for the small paired
  replicate probe, or clearly explains why no threshold can be recommended;
- generated readouts satisfy the artifact-table readout protocol;
- focused tests and impacted existing tests pass;
- the implementation log records all completed Phase.Stage.Action work.

## Non-Goals

This gameplan does not implement:

- the small paired replicate probe;
- multi-candidate generalization;
- tensor-enabled behavior;
- new environment construction;
- new `state_collapser` behavior;
- musical-quality scoring;
- statistical significance testing;
- final serious comparison scale.
