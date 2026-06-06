# Counterpoint n-over-18 Contraction Fraction Sweep Implementation Workplan

Date: 2026-06-01

Status: implementation workplan, not yet executed

Repository:

```text
/Users/foster/big_boy_benchmarking
```

Source blueprint:

```text
docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/03_n_over_18_contraction_fraction_sweep_blueprint.md
```

## Purpose

This workplan translates the n-over-18 contraction fraction sweep blueprint
into Phase.Stage.Action implementation work.

The target is a diagnostic evaluation for the existing counterpoint
environment family:

```text
counterpoint_symbolic_v001
```

focused on:

- a single scheduled first-tier contraction block per fraction arm;
- fractions `n/18` for `n = 1, 2, 3, 4, 5, 6`;
- preserving the existing counterpoint environment unchanged;
- verifying whether lower contraction fractions preserve meaningful tower
  structure before the old one-third endpoint collapses;
- checking whether `6/18` matches the old one-third first scheduled block;
- separating constructed quotient shape from active executable control
  surface;
- producing repo-resident artifacts and human-readable readout support.

This is not a direct-vs-tower performance comparison.

This is not a new environment family.

This is not approval to edit `/Users/foster/state_collapser`.

## Execution Authority Status

This document is not approval to implement.

The Project Owner requested this workplan from the blueprint:

```text
Ok turn this into a Phase.Stage.Action style implmentation workplan. Follwo prime_directive in doing so `docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/03_n_over_18_contraction_fraction_sweep_blueprint.md`
```

Therefore this document may be created now.

Source, test, CLI, fixture, artifact-schema, and evaluation-readout
implementation must not begin until the Project Owner explicitly approves
execution of this exact workplan.

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
- `docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/README.md`
- `docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/01_issue_and_next_tests.md`
- `docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/02_readout_conversation_archive.md`
- `docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/03_n_over_18_contraction_fraction_sweep_blueprint.md`
- `docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/README.md`
- current BBB counterpoint source surfaces

## PO Attribution Preservation

This workplan preserves the source blueprint's PO Attribution Ledger. It does
not add invented Project Owner turns.

Project Owner-originated design locks carried into implementation:

1. Redesign the evaluation itself, not the counterpoint environment.
2. Replace fixed `1/3` contraction with `n/18` contraction for
   `n = 1, 2, 3, 4, 5, 6`.
3. Record each fraction arm.
4. Use the sweep to check whether behavior looks reasonable at low contraction
   strengths and then collapses.
5. Keep this redesign under the unexpected one-third collapse archive.
6. Preserve the correction that the one-third collapse is suspicious diagnostic
   evidence, not a negative learning result about counterpoint.
7. Avoid loose `pi_0` or connected-components claims unless they are exactly
   justified.

Consultant implementation assumptions are explicitly labeled below.

## Fixed Design Locks For Execution

These locks are binding if the Project Owner later says to execute this
workplan.

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
- upstream `state_collapser`.

### Evaluation Identity Lock

Use:

```text
counterpoint_contraction_fraction_sweep_diagnostics_v001
```

Recommended CLI group:

```text
counterpoint fraction-sweep
```

Recommended repo readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/
```

### Fraction Arm Lock

Implement exactly these required arms:

```text
n01_over_18
n02_over_18
n03_over_18
n04_over_18
n05_over_18
n06_over_18
```

Each required arm corresponds to numerator `1` through `6` with denominator
`18`.

### Single-Block Semantics Lock

Each `n/18` arm must schedule exactly one first-tier contraction block.

Remaining edges are unscheduled for that arm.

The new sweep must not implement an 18-tier recursive schedule.

The new sweep must not repeatedly sample from remaining edges until collapse.

### Legacy One-Third Clarification Lock

The existing one-third schema is recursive only in the sense that it schedules
three blocks over the remaining per-source outgoing list:

```text
block 0: ceil(total / 3)
block 1: ceil(remaining / 3)
block 2: ceil(remaining / 3)
```

The old observed singleton collapse happened at tier `1`, so this workplan
compares `6/18` to the old first scheduled block only.

The implementation must verify that `6/18` selects the same source-local edge
set as old one-third block `0` for the same instance and schema seed.

If it cannot verify this equivalence, stop.

### Monotonicity Lock

For a fixed instance and schema seed:

```text
selected_edges(1/18)
subset selected_edges(2/18)
subset selected_edges(3/18)
subset selected_edges(4/18)
subset selected_edges(5/18)
subset selected_edges(6/18)
```

If selected edge sets are not nested, stop.

### Language Lock

Use:

- repeated endpoint coalescence;
- scheduled contraction block;
- first-tier state-cell count;
- active action-cell count;
- coset-size or state-cell member-count histogram.

Avoid:

- claiming a separate `pi_0` operation;
- claiming a separate connected-components pass;
- claiming the counterpoint environment is degenerate;
- claiming a learning result.

## Consultant Defaults For Open Blueprint Questions

These defaults are consultant-authored and become execution assumptions only if
the Project Owner approves execution without overriding them.

1. Use single-block semantics for each `n/18` arm.
2. Include a no-contraction structural control arm in the artifact set.
3. Implement support for both smoke and full validation runs.
4. Use `largest first-tier state cell share >= 0.90` as the initial
   near-collapse threshold.
5. Compare `6/18` primarily to the old first scheduled one-third block, not to
   the whole old recursive three-block tower.

## Required Branch Discipline

After Project Owner approval and before implementation edits, create and switch
to:

```text
codex/contraction-fraction-sweep-diagnostics
```

Do not implement on `main` unless the Project Owner explicitly authorizes that.

## Implementation Log Requirement

When this workplan is executed, create and maintain:

```text
docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/05_n_over_18_contraction_fraction_sweep_implementation_log.md
```

The log must record:

- branch name;
- each completed Phase.Stage.Action;
- files changed;
- commands run;
- test results;
- artifact runs;
- surprises and failures;
- stop conditions encountered;
- Project Owner clarifications after this workplan.

## Global Stop Conditions

Stop and ask the Project Owner if:

- explicit approval to execute this workplan has not been received;
- branch or dirty status would mix unrelated work into this implementation;
- any action would require editing `/Users/foster/state_collapser`;
- any action would alter the `counterpoint_symbolic_v001` environment;
- `6/18` cannot be verified against the old first one-third block;
- selected edge sets are not nested across `n`;
- active action-cell counts cannot be distinguished from stale historical
  action-cell records;
- a required evaluation-level table would be omitted without an explicit
  expected-file policy;
- artifact roots would need to live outside the repo readout surface for a
  durable evaluation run;
- exact implementation of any Phase.Stage.Action would require a weaker
  substitute, hidden simplification, or unapproved reordering;
- implementation pressure starts turning this diagnostic into a learning
  comparison.

## Phase 0. Stage 0. Action 1: Confirm Execution Authority

Before edits, confirm that the Project Owner explicitly requested execution of
this exact workplan.

If not approved, stop.

## Phase 0. Stage 0. Action 2: Inspect Working Tree

Run non-destructive git status inspection.

Identify unrelated dirty or untracked files.

Do not modify unrelated files.

If unrelated dirty state would be mixed into this work, stop and ask.

## Phase 0. Stage 0. Action 3: Create Work Branch

Create and switch to:

```text
codex/contraction-fraction-sweep-diagnostics
```

Record the branch in the implementation log.

## Phase 0. Stage 0. Action 4: Create Implementation Log

Create:

```text
docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/05_n_over_18_contraction_fraction_sweep_implementation_log.md
```

Initialize it with:

- source workplan path;
- branch name;
- execution start timestamp;
- current `git status --short`;
- declared stop conditions;
- a Phase.Stage.Action checklist.

## Phase 0. Stage 1. Action 1: Re-Read Source Authority

Immediately before code edits, re-read:

```text
docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/03_n_over_18_contraction_fraction_sweep_blueprint.md
docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/04_n_over_18_contraction_fraction_sweep_implementation_workplan.md
docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
```

Record completion in the implementation log.

## Phase 0. Stage 1. Action 2: Map Existing One-Third Surfaces

Inspect existing one-third diagnostic code and record reusable surfaces:

```text
src/big_boy_benchmarking/environments/counterpoint/ids.py
src/big_boy_benchmarking/environments/counterpoint/schemas.py
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/
src/big_boy_benchmarking/cli.py
tests/
```

Record which files will be edited and which will be left untouched.

## Phase 1. Stage 1. Action 1: Add Stable Evaluation And Schema IDs

Add stable ids for:

```text
counterpoint_contraction_fraction_sweep_diagnostics_v001
counterpoint_outgoing_fraction_sweep_schema_v001
```

Add arm id helpers for:

```text
n01_over_18
n02_over_18
n03_over_18
n04_over_18
n05_over_18
n06_over_18
no_contraction_control
```

Do not remove or rename existing one-third ids.

## Phase 1. Stage 1. Action 2: Implement Shared Source-Local Selection Helper

Implement a helper that, for a graph or registry source:

1. sorts outgoing edge identities stably;
2. shuffles with deterministic seed derived from `schema_seed` and
   source-state identity;
3. selects the first `max(1, ceil(out_degree * numerator / denominator))`
   edges for sources with at least one outgoing edge;
4. returns selected edges in a stable order suitable for summary tables and
   equivalence tests.

The helper must be usable by both metadata/schema summaries and runtime
`ContractionSchema` assignment.

## Phase 1. Stage 1. Action 3: Implement Runtime Fraction Schema

Implement a new `state_collapser` `ContractionSchema` adapter for the fraction
sweep.

Required behavior:

- constructor accepts `numerator`, `denominator`, and `schema_seed`;
- denominator must be positive;
- numerator must be between `1` and denominator;
- for this evaluation, valid numerators are `1..6` with denominator `18`;
- `ordered_blocks()` returns exactly one scheduled block for fraction arms;
- `assign_edge()` returns that scheduled block only for selected edges;
- unselected edges return `None`.

Do not implement recursive remaining-block scheduling for this new schema.

## Phase 1. Stage 1. Action 4: Preserve Existing One-Third Runtime

Keep `CounterpointOutgoingThirdsSchema` and existing one-third CLI behavior
working.

Do not mutate old one-third behavior unless a tiny extraction is required and
covered by regression tests.

## Phase 1. Stage 2. Action 1: Implement Metadata Fraction Schema Construction

Implement a metadata/schema construction function for the fraction sweep.

It must emit enough information to summarize:

- numerator;
- denominator;
- requested fraction;
- selected edge count;
- selected edge share;
- source count with scheduled edges;
- per-source selected edge counts;
- quota rule id;
- unscheduled edge count.

It must not use rewards, terminal outcomes, learned values, or future episode
results.

## Phase 1. Stage 2. Action 2: Implement Legacy First-Block Equivalence Helper

Implement a helper that compares, for each instance and schema seed:

```text
fraction arm n06_over_18 selected edge set
old one-third block 0 selected edge set
```

The helper must report:

- selected edge set equality;
- selected edge count for both sides;
- missing-from-fraction count;
- extra-in-fraction count;
- mismatch examples when present;
- pass/fail status.

If equality fails in tests, stop and return to design.

## Phase 1. Stage 2. Action 3: Implement Monotonicity Helper

Implement a helper that checks selected-edge nesting across `n = 1..6` for each
instance and schema seed.

The helper must report:

- current arm;
- next arm;
- subset pass/fail;
- missing nested edge count;
- example offending edges when present.

If monotonicity fails in tests, stop and return to design.

## Phase 1. Stage 3. Action 1: Implement Active Action-Cell Counting Helper

Implement or reuse a helper that counts action cells reachable from active
state cells and active outgoing collections.

This helper must not count only:

```text
len(action_layer.edge_ids_by_action_cell)
```

because that can include stale historical records.

If retaining the raw historical count, label it explicitly as raw historical
action-cell record count.

## Phase 1. Stage 3. Action 2: Implement Endpoint-Coalescence Diagnostic Helper

Implement a diagnostic helper that replays or observes the scheduled block
under the same repeated endpoint-coalescence semantics used by the tower.

It must report:

- state cells after the scheduled block;
- largest coalesced cell size;
- useful coalescence count;
- redundant or internal edge count;
- processed-edge index at first singleton state cell, if singleton collapse
  occurs;
- whether singleton collapse required most of the block or only a few early
  edges.

Do not describe this helper as a separate `pi_0` or connected-components pass
in code comments or docs.

If the exact processing order used by the tower cannot be matched or observed,
stop and return to design.

## Phase 2. Stage 1. Action 1: Create Fraction Sweep Diagnostics Package

Create a new package:

```text
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/
```

Do not replace:

```text
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/
```

## Phase 2. Stage 1. Action 2: Add Package Config

Add config definitions for:

- evaluation id;
- default schema family id;
- default numerators `1,2,3,4,5,6`;
- denominator `18`;
- default instances `small,medium`;
- schema seeds `0,1,2`;
- replicates `4`;
- episodes `16`;
- linearization mode `tensor_available_disabled`;
- near-collapse threshold `0.90`;
- run mode `diagnostic_contraction_fraction_sweep_tower_abc`.

Allow CLI overrides for smoke runs without changing the locked defaults.

## Phase 2. Stage 1. Action 3: Add Path Helpers

Add path helpers for:

```text
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/
```

and source evaluation roots under:

```text
<artifact-root>/evaluations/counterpoint_contraction_fraction_sweep_diagnostics_v001/
```

Enforce repo-resident artifact roots for durable evaluation runs.

## Phase 2. Stage 2. Action 1: Define Event And Summary Rows

Define typed row models or equivalent structured serializers for:

```text
schema_fraction_summary.csv
tower_shape_summary.csv
endpoint_coalescence_summary.csv
tier_executability_summary.csv
tier_occupancy_summary.csv
control_action_summary.csv
abc_selection_summary.csv
abc_tier_signal_summary.csv
lift_failure_by_tier.csv
concrete_step_summary.csv
collapse_threshold_summary.csv
legacy_one_third_equivalence_summary.csv
```

Every row that belongs to an arm must include:

- evaluation id;
- instance id;
- arm id;
- numerator;
- denominator;
- schema seed;
- replicate index where applicable;
- run id where applicable.

## Phase 2. Stage 2. Action 2: Add Manifests And Source Binding Builder

Implement manifest and `readout_source.json` builders.

The source binding must include:

- repo readout surface;
- source artifact root;
- source evaluation root;
- evaluation id;
- run mode;
- source files;
- expected files;
- goal criteria;
- structural limit checks;
- badge policy;
- goal summary sources;
- methodology summary sources;
- claim boundary;
- link to the blueprint;
- link to the unexpected one-third collapse archive.

## Phase 2. Stage 3. Action 1: Add Human Docs Seed Writer

Add docs seed generation for:

```text
README.md
method.md
runbook.md
artifact_index.md
glossary.md
results/summary.md
results/human_summary.md
results/sweep_verdict.md
results/threshold_table.md
```

The seed docs must include the correct human-readability command:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/readout_source.json
```

## Phase 3. Stage 1. Action 1: Implement Run Enumeration

Implement run enumeration over:

- instances;
- fraction arms;
- schema seeds;
- replicates;
- episodes.

Include the no-contraction structural control arm if the execution assumptions
are not overridden.

Ensure run ids encode instance, arm id, schema seed, and replicate index.

## Phase 3. Stage 1. Action 2: Implement Tower Build Per Arm

For each fraction arm, build a `PartitionTower` using the new single-block
fraction schema.

For the no-contraction control arm, use the existing no-contraction schema.

Record tower construction metadata before any controller episodes run.

## Phase 3. Stage 1. Action 3: Implement Per-Run Structural Summaries

For each run, emit per-run structural files that support the evaluation-level
tables.

Required evidence includes:

- quotient/tower shape;
- active action-cell count;
- raw historical action-cell count if retained;
- state-cell member-size histogram;
- scheduled block selected edges;
- endpoint-coalescence diagnostics;
- legacy equivalence result for `n06_over_18`;
- monotonicity result for the arm family.

## Phase 3. Stage 2. Action 1: Implement ABC Runtime Episodes

Run the existing upstream-backed active-tier counterpoint control path for each
configured run.

Do not implement a new controller policy.

Do not copy upstream ABC logic and treat the copy as source of truth.

## Phase 3. Stage 2. Action 2: Record Control And ABC Events

Record:

- active tier before and after control events;
- selected tier;
- controller action;
- upstream ABC helper inputs and outputs when available;
- tier signal rows;
- exploit/explore/train counts;
- episode termination reasons.

Maintain compatibility with existing counterpoint control event conventions
where practical.

## Phase 3. Stage 2. Action 3: Record Lift And Concrete Step Evidence

Record:

- lift attempts;
- lift successes;
- lift failures;
- failure reason;
- tier;
- selected abstract action cell;
- realized concrete action when present;
- concrete counterpoint step rows.

The readout must be able to tell whether a tier was constructed but not live
executable.

## Phase 4. Stage 1. Action 1: Implement Aggregation

Implement summarization from per-run artifacts to evaluation-level tables.

All required tables listed in Phase 2. Stage 2. Action 1 must be written by the
summarize command.

If a table is genuinely not applicable for a run mode, it must be recorded in
expected-file policy rather than silently omitted.

## Phase 4. Stage 1. Action 2: Implement Collapse Threshold Summary

Aggregate the arm sweep into:

```text
results/collapse_threshold_summary.csv
```

For each instance and schema seed family, report:

- first `n` with full first-tier singleton collapse;
- first `n` with near-collapse;
- last `n` with nontrivial state structure;
- mixed-by-seed status;
- mixed-by-instance status;
- whether `n06_over_18` matches old one-third first-block behavior.

## Phase 4. Stage 1. Action 3: Implement Sweep Verdict Classification

Classify each instance and overall run as one of:

```text
threshold_found
immediate_collapse
no_collapse
mixed
invalid_or_uninterpretable
```

Back each classification with table fields, not prose-only inference.

## Phase 4. Stage 2. Action 1: Generate Repo Readout Surface

Ensure the summarize command writes or updates:

```text
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/readout_source.json
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/README.md
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/method.md
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/runbook.md
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/artifact_index.md
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/glossary.md
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/results/
```

Do not point the readout protocol at a raw artifact root.

## Phase 4. Stage 2. Action 2: Implement Badge Input Support

Populate source binding and/or summary fields needed for badges:

- artifact status;
- sweep status;
- `6/18` legacy check status;
- runtime executability status;
- diagnostic-only scope;
- repo artifact provenance.

Do not hard-code optimistic status if artifacts do not support it.

## Phase 5. Stage 1. Action 1: Add CLI Run Command

Add:

```text
uv run python -m big_boy_benchmarking.cli counterpoint fraction-sweep run
```

Required options:

- `--artifact-root`;
- `--instances`;
- `--numerators`;
- `--denominator`;
- `--schema-seeds`;
- `--replicates`;
- `--episodes`;
- `--linearization-mode`;
- `--locked-by`, if current evaluation conventions require it.

Provide defaults matching the config, while allowing smoke overrides.

## Phase 5. Stage 1. Action 2: Add CLI Summarize Command

Add:

```text
uv run python -m big_boy_benchmarking.cli counterpoint fraction-sweep summarize
```

Required option:

```text
--artifact-root
```

The summarize command must produce evaluation-level tables, docs seeds, and
`readout_source.json`.

## Phase 5. Stage 1. Action 3: Add CLI Diagnostics Or Dry-Run Command If Useful

If local patterns support it, add a lightweight command or option that builds
schema selections and reports monotonicity/legacy equivalence without running
episodes.

If adding this would cause scope drift, skip it and record the decision in the
implementation log.

## Phase 6. Stage 1. Action 1: Add Schema Unit Tests

Add tests proving:

- quota rule behavior for representative source out-degrees;
- selected edge count equals `max(1, ceil(out_degree * n / 18))`;
- selected edge sets are nested for `n = 1..6`;
- `n06_over_18` selected edge set equals old one-third block `0`;
- unselected edges remain unscheduled;
- invalid numerator/denominator inputs fail clearly.

## Phase 6. Stage 1. Action 2: Add Active Action-Cell Count Tests

Add tests proving the active action-cell helper does not count stale historical
action-cell records as live executable action cells.

If constructing the exact stale-record case is too expensive, add a focused
unit fixture or regression using the known one-third collapse artifact shape.

Do not mark this action complete with only a placeholder test.

## Phase 6. Stage 1. Action 3: Add Endpoint-Coalescence Diagnostic Tests

Add tests for the endpoint-coalescence diagnostic helper.

Required cases:

- a tiny graph where one scheduled edge coalesces exactly two states;
- a tiny chain where repeated endpoint coalescence accumulates through shared
  endpoints;
- a redundant/internal edge case;
- first singleton-collapse index when a block fully collapses a small graph.

Use language in test names and assertions that avoids implying a separate
`pi_0` operation.

## Phase 6. Stage 2. Action 1: Add Artifact Contract Tests

Add tests proving:

- `readout_source.json` is generated and parses;
- required result tables are listed;
- expected-file policy exists;
- goal summary sources include the blueprint;
- methodology summary sources include the blueprint and docs seeds;
- artifact root validation enforces repo-resident durable evaluation paths;
- source binding targets the repo readout surface, not raw artifacts.

## Phase 6. Stage 2. Action 2: Add CLI Smoke Tests

Add tests or scripted test coverage for:

```text
counterpoint fraction-sweep run
counterpoint fraction-sweep summarize
```

Use a small budget appropriate for test runtime.

The smoke test must include at least two numerators so monotonicity and table
shape are exercised.

## Phase 6. Stage 3. Action 1: Run Targeted Tests

Run the targeted fraction sweep tests.

Record exact commands and results in the implementation log.

If tests fail, fix the implementation or stop if the failure indicates a
design conflict.

## Phase 6. Stage 3. Action 2: Run Counterpoint Regression Tests

Run existing counterpoint tests covering:

- environment enumeration;
- tower adapter;
- one-third diagnostics;
- first serious learning evaluation surfaces, if present and feasible.

Record exact commands and results in the implementation log.

## Phase 7. Stage 1. Action 1: Run Repo-Resident Smoke Artifact Run

Run a bounded smoke artifact run under:

```text
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/artifacts/smoke_001/
```

Recommended smoke shape:

- instance: `small`;
- numerators: `1,6`;
- denominator: `18`;
- schema seeds: `0`;
- replicates: `1`;
- episodes: `1`;
- linearization mode: `tensor_available_disabled`.

This smoke run is for implementation verification, not for final human claims.

## Phase 7. Stage 1. Action 2: Summarize Smoke Artifacts

Run the summarize command against the smoke artifact root.

Verify:

- all required smoke result tables exist;
- `readout_source.json` exists;
- docs seed files exist;
- `6/18` legacy check table exists;
- monotonicity check passes;
- active action-cell counts are present.

## Phase 7. Stage 1. Action 3: Run Human-Readability Protocol On Smoke

Execute the readout protocol against:

```text
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/readout_source.json
```

Verify that generated docs:

- open with a sweep verdict;
- identify the run as smoke if the source binding says smoke;
- do not claim learning performance;
- include the exact protocol command;
- include protected clarification turn slots;
- distinguish active action-cell counts from raw historical records.

## Phase 7. Stage 2. Action 1: Review Generated Smoke Readout

Read the generated README and supporting docs.

Fix any implementation or source-binding issue that causes:

- artifact-root confusion;
- missing claim boundary;
- false learning claim;
- missing sweep threshold interpretation;
- misleading action-cell language;
- loose `pi_0` or connected-components language.

## Phase 8. Stage 1. Action 1: Full Validation Run Decision Lock

Before running the full small+medium validation budget, confirm that the
Project Owner has explicitly authorized the full artifact run.

If the Project Owner has not explicitly authorized the full run, stop after the
smoke-verified implementation and report that full validation remains pending.

## Phase 8. Stage 1. Action 2: Run Full Validation Artifacts If Authorized

If authorized, run the full validation artifact set under:

```text
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/artifacts/small_medium_validation_001/
```

Default full shape:

- instances: `small,medium`;
- numerators: `1,2,3,4,5,6`;
- denominator: `18`;
- schema seeds: `0,1,2`;
- replicates: `4`;
- episodes: `16`;
- linearization mode: `tensor_available_disabled`.

## Phase 8. Stage 1. Action 3: Summarize Full Validation Artifacts If Run

If full validation artifacts were generated, run the summarize command.

Verify all required evaluation-level tables exist and parse.

## Phase 8. Stage 1. Action 4: Generate Full Human Readout If Full Run Was Summarized

If full validation artifacts were summarized, execute:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/readout_source.json
```

Review generated docs for the same claim-boundary and language checks used for
smoke.

## Phase 9. Stage 1. Action 1: Update Design Archive Status

Update the unexpected-collapse archive README only if implementation status has
changed.

Record links to:

- implementation log;
- evaluation readout surface;
- smoke artifact run;
- full validation run, if produced.

Do not overwrite the archived one-third conversation.

## Phase 9. Stage 1. Action 2: Final Verification Pass

Run:

- formatting checks used by the repo;
- targeted tests;
- relevant counterpoint regression tests;
- `git diff --check`.

Record all commands and results in the implementation log.

## Phase 9. Stage 1. Action 3: Final Implementation Report

Report:

- branch name;
- completed Phase.Stage.Action items;
- files changed;
- tests run;
- artifact runs produced;
- readouts generated;
- stop conditions encountered;
- full validation status;
- remaining PO decisions.

Do not claim completion of any action that was skipped by a decision lock.

## Expected File Change Map

Likely source additions:

```text
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/
```

Likely source edits:

```text
src/big_boy_benchmarking/environments/counterpoint/ids.py
src/big_boy_benchmarking/environments/counterpoint/schemas.py
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
src/big_boy_benchmarking/cli.py
```

Likely docs/evaluation additions:

```text
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/
```

Likely design-log addition:

```text
docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/05_n_over_18_contraction_fraction_sweep_implementation_log.md
```

Likely tests:

```text
tests/
```

The exact file list must be discovered during implementation. This section is
a map, not permission to make unrelated edits.
