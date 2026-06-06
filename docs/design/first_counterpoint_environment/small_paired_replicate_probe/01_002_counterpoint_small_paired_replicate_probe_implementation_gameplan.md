# Counterpoint Small Paired Replicate Probe Implementation Workplan

Date: 2026-06-05

Status: implementation workplan, not executed

Repository:

```text
/Users/foster/big_boy_benchmarking
```

Source blueprint:

```text
docs/design/first_counterpoint_environment/small_paired_replicate_probe/01_001_counterpoint_small_paired_replicate_probe_blueprint.md
```

## Purpose

This workplan translates the small paired replicate probe blueprint into
Phase.Stage.Action implementation work.

The target evaluation is:

```text
counterpoint_small_paired_replicate_probe_v001
```

The evaluation repeats the corrected second-serious schema comparison across a
small number of matched seed bundles.

It tests:

```text
Across a small number of matched seeds, does Schema 1 show a stable paired
advantage, disadvantage, or no-difference pattern relative to Schema 0?
```

The schema arms are:

```text
Schema 0: schema0_no_contraction
Schema 1: schema1_noisy_rate_one_drop, using the corrected full-iterated
          noisy-rate candidate source
```

The first intended modest budget is:

```text
candidate_cap = 1
replicates_per_arm = 8
episodes_per_arm = 16
window_length = 5
required_count = 4
linearization_mode = tensor_available_disabled
liftability_semantics = state_collapser_v072_pointwise
```

The Project Owner agreed that the threshold frontier probe should run first and
that this replicate probe should use the sharper threshold discovered by that
frontier, unless the Project Owner later overrides that ordering.

## Execution Authority Status

The Project Owner requested this workplan:

```text
Following `prime_directive`, generate and extremely detailed implementation
workplan from
`docs/design/first_counterpoint_environment/small_paired_replicate_probe/01_001_counterpoint_small_paired_replicate_probe_blueprint.md`
in Phase.Stage.Action format
```

Therefore this document may be written now.

This instruction is not implementation approval.

If the Project Owner later says to execute this exact workplan, implementation
must follow this document as written. If any Phase.Stage.Action item cannot be
implemented as written, stop and ask for Project Owner guidance before
substituting, simplifying, or reordering.

## Source Authority

This workplan follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/git_practices.md`
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`
- `docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md`
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`
- `docs/design/first_counterpoint_environment/small_paired_replicate_probe/README.md`
- `docs/design/first_counterpoint_environment/small_paired_replicate_probe/01_001_counterpoint_small_paired_replicate_probe_blueprint.md`
- `docs/design/first_counterpoint_environment/threshold_frontier_probe/README.md`
- `docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/readout_source.json`
- `docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/README.md`
- `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json`
- current `src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/` source as reusable implementation context
- current `src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/` source as reusable candidate-source context
- current `src/big_boy_benchmarking/cli/main.py` command registration
- current `tests/environments/counterpoint/test_second_serious_comparison.py`
  and adjacent counterpoint evaluation tests

## PO Attribution Preservation

This workplan preserves the source blueprint's PO Attribution Ledger. It does
not add invented Project Owner turns.

Project Owner-originated requests carried into implementation:

1. The Project Owner asked for next-measure evaluation directions, not a
   full-blown final claim.
2. The Project Owner asked for design folders for the next-measure directions.
3. The Project Owner asked for blueprints in the respective folders.
4. The Project Owner stated that answers would be written in the documents.
5. The Project Owner requested this Phase.Stage.Action implementation
   workplan.

Project Owner answers present in the blueprint:

1. The Project Owner agreed to use the first threshold near the frontier if the
   threshold frontier probe runs first.
2. The Project Owner agreed to `8` matched seed pairs.
3. The Project Owner agreed to `16` episodes per arm.
4. The Project Owner agreed to run threshold frontier first, then use its
   sharper threshold here.
5. The Project Owner agreed to badge pair count, unblocked pairs, Schema 1
   margin wins, and sustained-hit rate difference.

Consultant-authored recommendations that become execution assumptions only
under later execution approval:

- evaluation id:

  ```text
  counterpoint_small_paired_replicate_probe_v001
  ```

- run family id:

  ```text
  counterpoint_symbolic_v001_small_paired_replicate_probe_v001
  ```

- repo readout surface:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/
  ```

- CLI group:

  ```text
  counterpoint paired-replicate-probe
  ```

- package:

  ```text
  src/big_boy_benchmarking/environments/counterpoint/small_paired_replicate_probe/
  ```

## Dependency On Threshold Frontier

This workplan is implementation-ready, but the main evaluation run has a
threshold dependency.

The Project Owner agreed:

```text
Run threshold frontier first, then use its sharper threshold here.
```

Therefore, implementation must distinguish:

1. machinery implementation, tests, smoke fixtures, and readout scaffolding;
2. the first meaningful paired-replicate artifact run.

The first meaningful paired-replicate run must not select its own threshold by
looking at replicate-probe outcomes.

Accepted threshold sources:

- a completed `threshold_frontier_probe` readout that names the selected
  threshold;
- an explicit Project Owner override before execution.

If neither exists when an execution reaches the benchmark-run stage, stop.

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
- threshold-frontier diagnostics;
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

### Schema Comparison Lock

The evaluation compares schema arms under matched seed bundles:

```text
Schema 0: schema0_no_contraction
Schema 1: schema1_noisy_rate_one_drop
```

Do not convert this evaluation into:

- threshold frontier;
- old direct-runner comparison;
- direct-vs-tower generic benchmark;
- noisy-rate candidate selection;
- full-tower training-health diagnostic;
- structural collapse diagnostic;
- broad abstraction superiority claim.

### Threshold Lock

Threshold policy shape:

```text
metric_id = episode_total_reward
comparison = greater_than_or_equal
window_length = 5
required_count = 4
scope = total_space
```

The numeric threshold value must come from the threshold frontier readout or
from explicit Project Owner override.

### Seed Pairing Lock

Each replicate index must produce a paired Schema 0 and Schema 1 run with a
shared seed-bundle identity.

Required evidence per pair:

```text
seed_bundle_id
training_replicate_index
schema0_run_id
schema1_run_id
schema0_seed_bundle_path
schema1_seed_bundle_path
```

If paired seed identity cannot be proven from artifacts, stop.

### Artifact Lock

Durable artifacts must be repo-resident under:

```text
docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts/<run-label>/
```

The repo-side readout source must be:

```text
docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/readout_source.json
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

- execution of this workplan has not been explicitly approved;
- working tree state would mix unrelated TeX/root document changes into this
  implementation;
- a source edit would touch `/Users/foster/state_collapser`;
- a source edit would change `counterpoint_symbolic_v001`;
- threshold-frontier output is absent when the first meaningful replicate run
  needs a numeric threshold;
- the threshold source recommends no threshold or an ambiguous threshold;
- candidate source no longer exposes an eligible corrected candidate;
- `state_collapser` is not version `0.7.2` or newer with pointwise semantics
  available;
- paired seed-bundle identity cannot be preserved and proven;
- the existing second-serious runner cannot be reused without losing
  provenance or pair identity;
- artifact tables required by the blueprint cannot be written honestly;
- readout source binding cannot represent pair-level evidence;
- generated readouts would need to be written outside the repo readout
  surface;
- implementation would silently simplify the required pair-distribution
  tables into only the old second-serious aggregate tables;
- implementation would treat the result as statistically conclusive.

## Phase.Stage.Action Workplan

### Phase 0: Authority, Branch, And Reality Check

#### Phase 0. Stage 0: Execution Authority

- Phase 0. Stage 0. Action 1: Confirm the Project Owner has explicitly asked
  to execute this exact workplan.
- Phase 0. Stage 0. Action 2: If execution authority is absent, stop before
  source edits.
- Phase 0. Stage 0. Action 3: Record the exact execution instruction in the
  implementation log.
- Phase 0. Stage 0. Action 4: Record that this workplan itself was requested
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
  codex/small-paired-replicate-probe
  ```

- Phase 0. Stage 1. Action 5: Record branch creation and initial dirty state
  in the implementation log.

#### Phase 0. Stage 2: Source Re-Read

- Phase 0. Stage 2. Action 1: Re-read Prime Directive source authority listed
  in this workplan.
- Phase 0. Stage 2. Action 2: Re-read the source blueprint.
- Phase 0. Stage 2. Action 3: Re-read the threshold-frontier README and any
  threshold-frontier blueprint/workplan/readout that exists at execution time.
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
  docs/design/first_counterpoint_environment/small_paired_replicate_probe/01_003_counterpoint_small_paired_replicate_probe_implementation_log.md
  ```

- Phase 0. Stage 3. Action 2: Include branch, execution instruction, source
  workplan, initial dirty state, stop conditions, and running
  Phase.Stage.Action checklist.
- Phase 0. Stage 3. Action 3: Keep the log updated throughout implementation.

### Phase 1: Evaluation Identity, Package, Config, And Paths

#### Phase 1. Stage 1: Evaluation Constants

- Phase 1. Stage 1. Action 1: Add evaluation id:

  ```text
  counterpoint_small_paired_replicate_probe_v001
  ```

- Phase 1. Stage 1. Action 2: Add run family id:

  ```text
  counterpoint_symbolic_v001_small_paired_replicate_probe_v001
  ```

- Phase 1. Stage 1. Action 3: Add run mode ids:

  ```text
  smoke_small_paired_replicate_probe
  threshold_frontier_selected_small_paired_replicate_probe
  ```

- Phase 1. Stage 1. Action 4: Reuse schema class ids:

  ```text
  schema0_no_contraction
  schema1_noisy_rate_one_drop
  ```

- Phase 1. Stage 1. Action 5: Add stable claim and badge ids for pair count,
  unblocked pair count, Schema 1 margin wins, sustained-hit rate difference,
  liftability semantics, and lift failures.
- Phase 1. Stage 1. Action 6: Keep all existing counterpoint ids unchanged.
- Phase 1. Stage 1. Action 7: Add tests proving new ids are exported,
  stable, and non-colliding.

#### Phase 1. Stage 2: Package Scaffold

- Phase 1. Stage 2. Action 1: Create package:

  ```text
  src/big_boy_benchmarking/environments/counterpoint/small_paired_replicate_probe/
  ```

- Phase 1. Stage 2. Action 2: Add `__init__.py`.
- Phase 1. Stage 2. Action 3: Add `config.py`.
- Phase 1. Stage 2. Action 4: Add `paths.py`.
- Phase 1. Stage 2. Action 5: Add `threshold_source.py`.
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

- Phase 1. Stage 3. Action 1: Define `SmallPairedReplicateProbeBudget`.
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
- Phase 1. Stage 3. Action 6: Include `training_replicates_per_arm`, default
  `8`.
- Phase 1. Stage 3. Action 7: Include `episodes_per_replicate`, default `16`.
- Phase 1. Stage 3. Action 8: Include `threshold_value`, nullable until
  resolved by threshold source.
- Phase 1. Stage 3. Action 9: Include optional `threshold_frontier_readout_source`.
- Phase 1. Stage 3. Action 10: Include `window_length`, default `5`.
- Phase 1. Stage 3. Action 11: Include `required_count`, default `4`.
- Phase 1. Stage 3. Action 12: Include `base_seed`, default `0`.
- Phase 1. Stage 3. Action 13: Include `linearization_mode_id`, default:

  ```text
  tensor_available_disabled
  ```

- Phase 1. Stage 3. Action 14: Include `locked_by`.
- Phase 1. Stage 3. Action 15: Include `run_mode`.
- Phase 1. Stage 3. Action 16: Validate that either `threshold_value` or a
  usable `threshold_frontier_readout_source` is present for a non-smoke
  execution.
- Phase 1. Stage 3. Action 17: Validate that the first meaningful default
  budget is exactly `8` matched seed pairs and `16` episodes per arm.

#### Phase 1. Stage 4: Path Contracts

- Phase 1. Stage 4. Action 1: Define repo readout surface:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/
  ```

- Phase 1. Stage 4. Action 2: Define default artifact root under:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts/<run-label>/
  ```

- Phase 1. Stage 4. Action 3: Define evaluation root under:

  ```text
  <artifact-root>/evaluations/counterpoint_small_paired_replicate_probe_v001/
  ```

- Phase 1. Stage 4. Action 4: Define run family root under:

  ```text
  <artifact-root>/runs/counterpoint_symbolic_v001_small_paired_replicate_probe_v001/
  ```

- Phase 1. Stage 4. Action 5: Add repo-resident path validation.
- Phase 1. Stage 4. Action 6: Add readout-source path validation.
- Phase 1. Stage 4. Action 7: Add artifact-root collision protection unless
  an explicit overwrite/update flag already exists in local pattern.
- Phase 1. Stage 4. Action 8: Add tests for default paths, absolute path
  resolution, outside-repo rejection for repo readout surfaces, and artifact
  root label extraction.

### Phase 2: Threshold Source, Candidate Source, And Pairing Contracts

#### Phase 2. Stage 1: Threshold Source Resolution

- Phase 2. Stage 1. Action 1: Implement threshold resolution from explicit
  `--threshold-value`.
- Phase 2. Stage 1. Action 2: Implement threshold resolution from a
  threshold-frontier readout source if available.
- Phase 2. Stage 1. Action 3: Define the expected field or table path for a
  frontier-selected threshold.
- Phase 2. Stage 1. Action 4: If the threshold-frontier implementation uses a
  different field name than this plan predicts, stop and update this workplan
  or record explicit Project Owner authorization before adapting.
- Phase 2. Stage 1. Action 5: Write `threshold_policy_manifest.json` with:

  ```text
  threshold_policy_id
  threshold_value
  threshold_source_type
  threshold_source_readout
  metric_id
  window_length
  required_count
  comparison
  scope
  ```

- Phase 2. Stage 1. Action 6: Add tests for explicit threshold, frontier
  threshold, missing threshold, malformed frontier source, and ambiguous
  frontier source.

#### Phase 2. Stage 2: Candidate Source Resolution

- Phase 2. Stage 2. Action 1: Reuse the candidate loading logic from
  `second_serious_comparison.candidates` or
  `noisy_rate_full_training.candidate_selection` where semantics match.
- Phase 2. Stage 2. Action 2: Validate that the candidate readout source
  exists and is a repo-side `readout_source.json`.
- Phase 2. Stage 2. Action 3: Validate that the source artifact root is
  repo-resident.
- Phase 2. Stage 2. Action 4: Validate that at least one candidate is eligible.
- Phase 2. Stage 2. Action 5: Validate the expected environment instance:

  ```text
  counterpoint_symbolic_n3_wide_20_108_span18_v001
  ```

- Phase 2. Stage 2. Action 6: Validate candidate id targeting if supplied.
- Phase 2. Stage 2. Action 7: Apply `candidate_cap = 1`.
- Phase 2. Stage 2. Action 8: Write `candidate_manifest.json`.
- Phase 2. Stage 2. Action 9: Write `parent_source_manifest.json`.
- Phase 2. Stage 2. Action 10: Add tests for missing source, ineligible
  candidate, wrong instance, candidate-cap handling, and candidate-id targeting.

#### Phase 2. Stage 3: Seed Bundle Pairing

- Phase 2. Stage 3. Action 1: Reuse the seed-bundle construction from
  `second_serious_comparison` if it preserves arm-paired identity.
- Phase 2. Stage 3. Action 2: For each replicate index, generate one
  `seed_bundle_id`.
- Phase 2. Stage 3. Action 3: Pass the same seed bundle to Schema 0 and Schema
  1 runs for that replicate.
- Phase 2. Stage 3. Action 4: Persist seed bundle evidence for both arms.
- Phase 2. Stage 3. Action 5: Write `results/seed_bundle_summary.csv`.
- Phase 2. Stage 3. Action 6: Add invariant checks that every pair has exactly
  one Schema 0 run and one Schema 1 run sharing the same `seed_bundle_id`.
- Phase 2. Stage 3. Action 7: Add tests that pair identity fails closed if
  one arm is missing, duplicated, or mismatched.

### Phase 3: Runner Implementation

#### Phase 3. Stage 1: Runner Composition

- Phase 3. Stage 1. Action 1: Implement a runner that delegates individual
  arm execution to existing second-serious comparison machinery where exact
  behavior matches the blueprint.
- Phase 3. Stage 1. Action 2: Preserve second-serious threshold/persistence
  semantics.
- Phase 3. Stage 1. Action 3: Preserve second-serious Schema 0 construction.
- Phase 3. Stage 1. Action 4: Preserve second-serious full-iterated noisy-rate
  Schema 1 construction.
- Phase 3. Stage 1. Action 5: Preserve v0.7.2 pointwise liftability semantics.
- Phase 3. Stage 1. Action 6: Ensure the local evaluation id/run family id is
  the small paired replicate probe id, not the second-serious comparison id.
- Phase 3. Stage 1. Action 7: Ensure run ids encode candidate, schema class,
  and training replicate index.
- Phase 3. Stage 1. Action 8: Ensure per-arm raw artifacts remain under the
  small paired replicate probe artifact root.

#### Phase 3. Stage 2: Run Loop

- Phase 3. Stage 2. Action 1: For each selected candidate, create a candidate
  group.
- Phase 3. Stage 2. Action 2: For each `training_replicate_index` in
  `0..replicates_per_arm-1`, create a matched seed bundle.
- Phase 3. Stage 2. Action 3: Run Schema 0 for that candidate/replicate.
- Phase 3. Stage 2. Action 4: Run Schema 1 for that candidate/replicate.
- Phase 3. Stage 2. Action 5: Record each run in the run index as it
  completes.
- Phase 3. Stage 2. Action 6: If one arm fails, preserve the other arm's
  artifact and mark the pair blocked rather than discarding the pair.
- Phase 3. Stage 2. Action 7: If both arms fail due to the same upstream
  artifact or candidate-source error, stop the evaluation and classify the
  run as artifact blocked.
- Phase 3. Stage 2. Action 8: Do not tune threshold, budget, candidate source,
  or seed policy during the run.

#### Phase 3. Stage 3: Per-Run Evidence Preservation

- Phase 3. Stage 3. Action 1: Preserve `episodes.csv` for every arm run.
- Phase 3. Stage 3. Action 2: Preserve `threshold_window_events.csv` for every
  arm run.
- Phase 3. Stage 3. Action 3: Preserve `first_hit_summary.json` and
  `first_sustained_hit_summary.csv` for every arm run.
- Phase 3. Stage 3. Action 4: Preserve `control_events.csv` and
  `tier_transition_events.csv`.
- Phase 3. Stage 3. Action 5: Preserve `lift_fiber_events.csv`.
- Phase 3. Stage 3. Action 6: Preserve `learner_update_events.csv`.
- Phase 3. Stage 3. Action 7: Preserve `tower_shape_summary.csv`.
- Phase 3. Stage 3. Action 8: Preserve `tower_invariant_report.json`.
- Phase 3. Stage 3. Action 9: Preserve `timing_segments.csv` and
  `timing_summary.json`.
- Phase 3. Stage 3. Action 10: Preserve `warnings.jsonl`.

#### Phase 3. Stage 4: Evaluation-Level Manifests

- Phase 3. Stage 4. Action 1: Write `evaluation_manifest.json`.
- Phase 3. Stage 4. Action 2: Write `evaluation_budget_lock.json`.
- Phase 3. Stage 4. Action 3: Write `evaluation_arm_manifest.json`.
- Phase 3. Stage 4. Action 4: Write `replicate_probe_policy_manifest.json`.
- Phase 3. Stage 4. Action 5: Write `threshold_policy_manifest.json`.
- Phase 3. Stage 4. Action 6: Write `parent_source_manifest.json`.
- Phase 3. Stage 4. Action 7: Write `candidate_manifest.json`.
- Phase 3. Stage 4. Action 8: Write `evaluation_run_index.csv`.
- Phase 3. Stage 4. Action 9: Write run-family `summary.json`.
- Phase 3. Stage 4. Action 10: Add tests proving every manifest contains
  evaluation id, run family id, artifact schema version, budget, source
  binding, and claim-boundary context.

### Phase 4: Aggregation And Result Tables

#### Phase 4. Stage 1: Per-Arm Distribution Tables

- Phase 4. Stage 1. Action 1: Aggregate every per-run first-sustained-hit row.
- Phase 4. Stage 1. Action 2: Write `results/schema_arm_distribution.csv`.
- Phase 4. Stage 1. Action 3: Include per schema arm:

  ```text
  run_count
  sustained_hit_count
  transient_hit_count
  never_hit_count
  artifact_incomplete_count
  sustained_hit_rate
  median_episodes_to_sustained_hit
  mean_episodes_to_sustained_hit
  median_post_hit_window_mean
  median_post_hit_window_min
  mean_post_hit_window_success_count
  ```

- Phase 4. Stage 1. Action 4: Add tests for sustained, transient, never-hit,
  and artifact-incomplete aggregation.

#### Phase 4. Stage 2: Pair Summary Table

- Phase 4. Stage 2. Action 1: Join Schema 0 and Schema 1 rows by candidate
  group id and seed bundle id.
- Phase 4. Stage 2. Action 2: Write `results/replicate_pair_summary.csv`.
- Phase 4. Stage 2. Action 3: Include:

  ```text
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

- Phase 4. Stage 2. Action 4: Define pair statuses:

  ```text
  schema1_faster
  schema1_slower
  same_episode_to_hit
  schema1_margin_higher
  schema1_margin_lower
  same_margin
  blocked_or_non_sustained
  artifact_incomplete
  runtime_failed
  ```

- Phase 4. Stage 2. Action 5: Add tests for every pair status.

#### Phase 4. Stage 3: Paired Delta Distribution

- Phase 4. Stage 3. Action 1: Write `results/paired_delta_distribution.csv`.
- Phase 4. Stage 3. Action 2: Include:

  ```text
  candidate_group_id
  pair_count
  unblocked_pair_count
  schema1_faster_pair_count
  schema1_slower_pair_count
  same_episode_pair_count
  schema1_margin_win_count
  schema1_margin_loss_count
  schema1_margin_same_count
  blocked_pair_count
  median_schema1_minus_schema0_episodes_to_hit
  median_schema1_minus_schema0_post_hit_window_mean
  median_schema1_minus_schema0_post_hit_window_min
  mean_schema1_minus_schema0_post_hit_success_count
  ```

- Phase 4. Stage 3. Action 3: Define a bounded `claim_status`.
- Phase 4. Stage 3. Action 4: Define `bounded_claim_text`.
- Phase 4. Stage 3. Action 5: Add tests for positive margin pattern,
  negative margin pattern, equal pattern, mixed/inconclusive pattern, and
  blocked pattern.

#### Phase 4. Stage 4: Post-Hit Margin Distribution

- Phase 4. Stage 4. Action 1: Write
  `results/post_hit_margin_distribution.csv`.
- Phase 4. Stage 4. Action 2: Include per pair and schema arm:

  ```text
  post_hit_window_mean
  post_hit_window_min
  post_hit_window_success_count
  threshold_margin_mean
  threshold_margin_min
  threshold_success_fraction
  ```

- Phase 4. Stage 4. Action 3: Include pairwise deltas when both arms have
  comparable post-hit windows.
- Phase 4. Stage 4. Action 4: Add tests for missing post-hit windows and
  non-sustained arms.

#### Phase 4. Stage 5: Sustained-Hit Rate Summary

- Phase 4. Stage 5. Action 1: Write `results/sustained_hit_rate_summary.csv`.
- Phase 4. Stage 5. Action 2: Include schema-arm hit rates.
- Phase 4. Stage 5. Action 3: Include Schema 1 minus Schema 0 sustained-hit
  rate difference.
- Phase 4. Stage 5. Action 4: Include blocked pair counts.
- Phase 4. Stage 5. Action 5: Add tests for hit-rate difference computation.

#### Phase 4. Stage 6: Tower, Lift, And Timing Tables

- Phase 4. Stage 6. Action 1: Promote all per-run tower shape rows into
  `results/tower_shape_summary.csv`.
- Phase 4. Stage 6. Action 2: Promote lift successes into
  `results/lift_success_by_tier.csv`.
- Phase 4. Stage 6. Action 3: Promote lift failures into
  `results/lift_failure_by_tier.csv`.
- Phase 4. Stage 6. Action 4: Promote timing evidence into
  `results/timing_summary.csv`.
- Phase 4. Stage 6. Action 5: Preserve `liftability_semantics_id` and
  `tower_invariant_report` summary fields in evaluation-level tables.
- Phase 4. Stage 6. Action 6: Add tests that zero lift failures produce a real
  empty table with headers or an explicitly documented empty-file convention,
  matching existing readout protocol expectations.

#### Phase 4. Stage 7: Aggregate Table And Summary

- Phase 4. Stage 7. Action 1: Write `evaluation_aggregate_table.csv`.
- Phase 4. Stage 7. Action 2: Write `evaluation_aggregate_summary.json`.
- Phase 4. Stage 7. Action 3: Include artifact status, run counts, pair
  counts, unblocked pair counts, margin win counts, sustained-hit rate
  differences, lift-failure counts, and claim status.
- Phase 4. Stage 7. Action 4: Include expected-file classifications.
- Phase 4. Stage 7. Action 5: Add tests that aggregate table and summary can
  drive the artifact-table readout protocol without inferring intent from code.

### Phase 5: Readout Source And Human-Readable Docs

#### Phase 5. Stage 1: Readout Source Binding

- Phase 5. Stage 1. Action 1: Generate repo-side `readout_source.json` in:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/
  ```

- Phase 5. Stage 1. Action 2: Include `repo_readout_surface`.
- Phase 5. Stage 1. Action 3: Include `source_artifact_root`.
- Phase 5. Stage 1. Action 4: Include `source_evaluation_root`.
- Phase 5. Stage 1. Action 5: Include `evaluation_id`.
- Phase 5. Stage 1. Action 6: Include `environment_instance_id`.
- Phase 5. Stage 1. Action 7: Include `artifact_run_label`.
- Phase 5. Stage 1. Action 8: Include `run_mode`.
- Phase 5. Stage 1. Action 9: Include `budget`.
- Phase 5. Stage 1. Action 10: Include `threshold_policy`.
- Phase 5. Stage 1. Action 11: Include `threshold_source`.
- Phase 5. Stage 1. Action 12: Include `candidate_source`.
- Phase 5. Stage 1. Action 13: Include complete `source_files`.
- Phase 5. Stage 1. Action 14: Include `expected_files`.
- Phase 5. Stage 1. Action 15: Include `goal_criteria`.
- Phase 5. Stage 1. Action 16: Include `badge_policy`.
- Phase 5. Stage 1. Action 17: Include `claim_boundary`.
- Phase 5. Stage 1. Action 18: Add tests for required readout-source keys.

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
- Phase 5. Stage 2. Action 10: Write `results/paired_replicate_readout.md`.
- Phase 5. Stage 2. Action 11: Write `results/margin_distribution_readout.md`.
- Phase 5. Stage 2. Action 12: Write `results/timing_readout.md`.
- Phase 5. Stage 2. Action 13: Preserve `## Clarifying Questions And Turns`
  according to `artifact_table_to_readable_document_protocol.md`.
- Phase 5. Stage 2. Action 14: Add tests that docs writer does not erase
  existing user-authored clarifying turns.

#### Phase 5. Stage 3: Badges

- Phase 5. Stage 3. Action 1: Generate artifact status badge.
- Phase 5. Stage 3. Action 2: Generate pair-count badge.
- Phase 5. Stage 3. Action 3: Generate unblocked-pairs badge.
- Phase 5. Stage 3. Action 4: Generate Schema 1 margin-wins badge.
- Phase 5. Stage 3. Action 5: Generate sustained-hit-rate-difference badge.
- Phase 5. Stage 3. Action 6: Generate liftability-semantics badge.
- Phase 5. Stage 3. Action 7: Generate lift-failures badge.
- Phase 5. Stage 3. Action 8: Generate provenance badge.
- Phase 5. Stage 3. Action 9: Add tests for badge labels and color classes.

#### Phase 5. Stage 4: Readout Protocol Compatibility

- Phase 5. Stage 4. Action 1: Verify the generated readout can be regenerated
  using:

  ```text
  execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/readout_source.json
  ```

- Phase 5. Stage 4. Action 2: Ensure the README explicitly reminds the reader
  of that command.
- Phase 5. Stage 4. Action 3: Ensure the readout does not require inspecting
  raw per-run files to understand the main paired result.
- Phase 5. Stage 4. Action 4: Add tests for readout-source path invariants.

### Phase 6: CLI

#### Phase 6. Stage 1: Parser Registration

- Phase 6. Stage 1. Action 1: Add counterpoint command:

  ```text
  paired-replicate-probe
  ```

- Phase 6. Stage 1. Action 2: Add `run` subcommand.
- Phase 6. Stage 1. Action 3: Add `summarize` subcommand.
- Phase 6. Stage 1. Action 4: Add arguments:

  ```text
  --artifact-root
  --candidate-readout-source
  --candidate-id
  --candidate-cap
  --threshold-value
  --threshold-frontier-readout-source
  --episodes
  --replicates
  --base-seed
  --locked-by
  --linearization-mode
  ```

- Phase 6. Stage 1. Action 5: Add argument validation that enforces
  threshold-source requirements.
- Phase 6. Stage 1. Action 6: Add help text that makes this a small paired
  replicate probe, not the final serious comparison.

#### Phase 6. Stage 2: Run Dispatch

- Phase 6. Stage 2. Action 1: Wire CLI run args into
  `SmallPairedReplicateProbeBudget`.
- Phase 6. Stage 2. Action 2: Enforce `tensor_available_disabled` with the
  same warning/error pattern as existing counterpoint evaluations.
- Phase 6. Stage 2. Action 3: Call the paired replicate runner.
- Phase 6. Stage 2. Action 4: Print JSON with:

  ```text
  status
  evaluation_budget_lock
  evaluation_run_index
  candidate_manifest
  run_count
  pair_count
  ```

- Phase 6. Stage 2. Action 5: Add CLI tests for successful argument parsing
  and missing threshold rejection.

#### Phase 6. Stage 3: Summarize Dispatch

- Phase 6. Stage 3. Action 1: Wire CLI summarize args into aggregation and
  docs writer.
- Phase 6. Stage 3. Action 2: Require `--artifact-root`.
- Phase 6. Stage 3. Action 3: Accept optional `--docs-root`.
- Phase 6. Stage 3. Action 4: Print JSON with generated docs paths.
- Phase 6. Stage 3. Action 5: Add CLI tests for summarize output and readout
  source generation.

### Phase 7: Tests

#### Phase 7. Stage 1: Unit Tests

- Phase 7. Stage 1. Action 1: Create:

  ```text
  tests/environments/counterpoint/test_small_paired_replicate_probe.py
  ```

- Phase 7. Stage 1. Action 2: Test config defaults.
- Phase 7. Stage 1. Action 3: Test path contracts.
- Phase 7. Stage 1. Action 4: Test threshold source resolution.
- Phase 7. Stage 1. Action 5: Test candidate source resolution.
- Phase 7. Stage 1. Action 6: Test seed-bundle pairing invariants.
- Phase 7. Stage 1. Action 7: Test pair summary status classification.
- Phase 7. Stage 1. Action 8: Test paired delta distribution aggregation.
- Phase 7. Stage 1. Action 9: Test post-hit margin distribution aggregation.
- Phase 7. Stage 1. Action 10: Test sustained-hit rate difference.
- Phase 7. Stage 1. Action 11: Test readout source required fields.
- Phase 7. Stage 1. Action 12: Test docs writer preserves clarifying turns.

#### Phase 7. Stage 2: Integration Tests

- Phase 7. Stage 2. Action 1: Add a tiny or synthetic fixture test that runs
  the evaluation with `candidate_cap = 1`, `replicates = 1`, and
  `episodes = 2` or the smallest locally valid budget.
- Phase 7. Stage 2. Action 2: Verify the run writes all required manifests.
- Phase 7. Stage 2. Action 3: Verify the run writes all required result
  tables.
- Phase 7. Stage 2. Action 4: Verify summarize writes readout docs.
- Phase 7. Stage 2. Action 5: Verify no generated docs are written into the
  raw artifact tree as the canonical repo readout surface.
- Phase 7. Stage 2. Action 6: Verify zero lift failures are represented
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
- Phase 8. Stage 1. Action 3: Verify threshold source is available.
- Phase 8. Stage 1. Action 4: If threshold frontier has not been run and no
  Project Owner override exists, stop before the meaningful replicate run.
- Phase 8. Stage 1. Action 5: Verify artifact root is new and clean.

#### Phase 8. Stage 2: Minimal Smoke Run

- Phase 8. Stage 2. Action 1: Run a minimal implementation smoke only after
  the Project Owner has approved execution.
- Phase 8. Stage 2. Action 2: Use a fresh repo artifact root such as:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts/smoke_001
  ```

- Phase 8. Stage 2. Action 3: Use minimal settings that complete quickly:

  ```text
  candidate_cap = 1
  replicates_per_arm = 1
  episodes_per_arm = 2 or 4
  ```

- Phase 8. Stage 2. Action 4: Use explicit `--threshold-value 13.0` only for
  implementation smoke if threshold frontier output is unavailable, and label
  the run mode as smoke rather than threshold-frontier-selected.
- Phase 8. Stage 2. Action 5: Summarize the smoke run.
- Phase 8. Stage 2. Action 6: Verify all required tables and readout docs
  exist.

#### Phase 8. Stage 3: First Meaningful Probe Run

- Phase 8. Stage 3. Action 1: Run the first meaningful small paired replicate
  probe only after threshold frontier output exists or the Project Owner gives
  explicit override.
- Phase 8. Stage 3. Action 2: Use a fresh repo artifact root such as:

  ```text
  docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts/v072_pointwise_r<THRESHOLD>_reps8_001
  ```

- Phase 8. Stage 3. Action 3: Use:

  ```text
  candidate_cap = 1
  replicates_per_arm = 8
  episodes_per_arm = 16
  window_length = 5
  required_count = 4
  linearization_mode = tensor_available_disabled
  ```

- Phase 8. Stage 3. Action 4: Summarize the meaningful run.
- Phase 8. Stage 3. Action 5: Regenerate/read the human-facing surface using:

  ```text
  execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/readout_source.json
  ```

- Phase 8. Stage 3. Action 6: Record run command, run result, summarize
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
  next-measure paired replicate probe, not a full-blown final comparison.

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
  repo-resident under the paired replicate readout surface.

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
shape once the workplan has been implemented and the Project Owner has
approved the relevant run.

Minimal smoke:

```text
uv run python -m big_boy_benchmarking.cli counterpoint paired-replicate-probe run \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts/smoke_001 \
  --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json \
  --threshold-value 13.0 \
  --candidate-cap 1 \
  --episodes 4 \
  --replicates 1 \
  --locked-by foster \
  --linearization-mode tensor_available_disabled

uv run python -m big_boy_benchmarking.cli counterpoint paired-replicate-probe summarize \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts/smoke_001
```

First meaningful probe after threshold frontier:

```text
uv run python -m big_boy_benchmarking.cli counterpoint paired-replicate-probe run \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts/v072_pointwise_r<THRESHOLD>_reps8_001 \
  --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json \
  --threshold-frontier-readout-source docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/readout_source.json \
  --candidate-cap 1 \
  --episodes 16 \
  --replicates 8 \
  --locked-by foster \
  --linearization-mode tensor_available_disabled

uv run python -m big_boy_benchmarking.cli counterpoint paired-replicate-probe summarize \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts/v072_pointwise_r<THRESHOLD>_reps8_001
```

Human-readable readout protocol:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/readout_source.json
```

## Acceptance Criteria

Implementation is complete only when:

- the new evaluation package exists and is tested;
- the CLI run/summarize commands exist and are tested;
- the evaluation preserves matched seed-bundle identity;
- the evaluation writes all required manifests and tables;
- the evaluation writes repo-side readout source and human-readable docs;
- the evaluation can run a minimal smoke;
- the first meaningful run is either completed from threshold-frontier output
  or explicitly deferred because threshold frontier has not yet run;
- generated readouts satisfy the artifact-table readout protocol;
- focused tests and impacted existing tests pass;
- the implementation log records all completed Phase.Stage.Action work.

## Non-Goals

This workplan does not implement:

- the threshold frontier probe itself;
- multi-candidate generalization;
- tensor-enabled behavior;
- new environment construction;
- new `state_collapser` behavior;
- musical-quality scoring;
- statistical significance testing;
- final serious comparison scale.
