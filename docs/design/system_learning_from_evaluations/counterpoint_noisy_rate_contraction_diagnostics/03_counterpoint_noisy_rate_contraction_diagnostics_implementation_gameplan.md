# Counterpoint Noisy-Rate Contraction Diagnostics Implementation Workplan

Date: 2026-06-01

Status: implementation workplan, not yet executed

Repository:

```text
<repo-root>
```

Source blueprint:

```text
docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/02_counterpoint_noisy_rate_contraction_diagnostics_blueprint.md
```

## Purpose

This workplan translates the noisy-rate contraction diagnostics blueprint into
Phase.Stage.Action implementation work.

The target is a sibling diagnostic evaluation for the existing counterpoint
environment family:

```text
counterpoint_symbolic_v001
```

focused on:

- replacing source-local deterministic minimum-one quota selection with noisy
  expected-rate selection;
- allowing sources to contribute zero scheduled outgoing edges;
- measuring selected edge rate, source coverage, zero-selected-source count,
  endpoint-coalescence behavior, tower shape, and active executable tier
  surface;
- preserving the existing counterpoint environment unchanged;
- preserving the existing source-local fraction sweep unchanged;
- producing repo-resident artifacts and human-readable readout support.

This is not a direct-vs-tower learning comparison.

This is not a new counterpoint environment family.

This is not approval to edit `<state-collapser-repo>`.

## Execution Authority Status

This document is not approval to implement.

The Project Owner requested this workplan from the blueprint:

```text
Give this a re-read and then write full implementatino gamplan using Phase.Staage.Action style, and follwoing prime_directuve
```

Therefore this document may be created now.

Source, test, CLI, artifact-schema, evaluation-readout, and benchmark-run
implementation must not begin until the Project Owner explicitly approves
execution of this exact workplan.

If the Project Owner later says to execute this workplan without overriding the
consultant defaults below, implementation should treat those defaults as the
approved execution settings for this workplan. If the Project Owner overrides
any default before execution, update this workplan or record the override in
the implementation log before source edits.

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
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/README.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/01_fraction_sweep_readout_conversation_archive.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/02_counterpoint_noisy_rate_contraction_diagnostics_blueprint.md`
- `docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/README.md`
- current BBB counterpoint source surfaces

## PO Attribution Preservation

This workplan preserves the source blueprint's PO Attribution Ledger. It does
not add invented Project Owner turns.

Project Owner-originated design locks carried into implementation:

1. The Project Owner asked for a follow-up diagnostic prompted by the `1/18`
   source-local fraction collapse.
2. The Project Owner proposed a noisy expected-rate idea like `1/36`, where
   sources often sample no arrows.
3. The Project Owner framed the goal as modifying the contraction-schema
   selection behavior, not the counterpoint environment.
4. The Project Owner asked to create the new evaluation design folder and copy
   the motivating conversation there.
5. The Project Owner requested a full blueprint, and then this
   Phase.Stage.Action workplan.

Consultant-authored defaults and recommendations are explicitly labeled below.

## Consultant Defaults For Execution

These defaults are consultant-authored. They become execution assumptions only
if the Project Owner later approves execution of this workplan without
overriding them.

1. Use coupled Bernoulli edge-threshold selection:

   ```text
   select edge when stable_uniform(edge, schema_seed) < numerator / denominator
   ```

2. Use the evaluation id:

   ```text
   counterpoint_noisy_rate_contraction_diagnostics_v001
   ```

3. Use the schema family id:

   ```text
   counterpoint_noisy_rate_contraction_schema_v001
   ```

4. Use the concrete schema id prefix:

   ```text
   counterpoint_noisy_rate_contraction_single_block_schema_v001
   ```

5. Use the run mode:

   ```text
   diagnostic_noisy_rate_contraction_tower_abc
   ```

6. Use the CLI group:

   ```text
   counterpoint noisy-rate
   ```

7. Use the repo readout surface:

   ```text
   docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/
   ```

8. Use these default full rates:

   ```text
   1/288,1/144,1/72,1/36,1/24,1/18,1/12,1/9
   ```

9. Use these smoke rates:

   ```text
   1/144,1/36,1/18
   ```

10. Include `no_contraction_control`.

11. Do not implement deterministic source-local floor reference arms in the
    first implementation. The readout may compare to the previous fraction
    sweep in prose and links. If the Project Owner later wants reference arms
    inside the artifact set, that should be a separate explicit update.

12. Require metadata/runtime selected-edge consistency as a hard validity
    check.

13. Require coupled-rate monotonicity as a hard validity check.

14. Keep the evaluation diagnostic-only. Do not make learning-performance
    claims.

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
- upstream `state_collapser`.

### Sibling Evaluation Lock

Do not mutate existing artifacts or semantics for:

```text
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/
```

Do not rename or reinterpret:

```text
counterpoint_contraction_fraction_sweep_diagnostics_v001
counterpoint_outgoing_fraction_sweep_schema_v001
```

The noisy-rate diagnostic gets its own ids, package, artifact roots, readout
surface, docs writer, and tests unless a very small shared helper can be safely
extracted.

### Selector Lock

The new selector must not use:

```text
max(1, ceil(out_degree * numerator / denominator))
```

The new selector must allow a nonempty source to select zero outgoing edges.

The new selector must use stable deterministic per-edge scores, not Python's
process-randomized `hash()`.

The new selector must produce nested selected-edge sets for increasing rates
under the same instance and schema seed.

### Language Lock

Use:

- noisy expected-rate selection;
- coupled Bernoulli edge-threshold selector;
- selected edge share;
- realized source coverage;
- zero-selected-source count;
- repeated endpoint coalescence;
- scheduled contraction block;
- active action-cell count;
- raw historical action-cell record count.

Avoid:

- loose `pi_0` claims;
- connected-components claims unless exactly justified;
- claims that the counterpoint environment is degenerate;
- claims that this is a learning-performance comparison.

## Required Branch Discipline

After Project Owner approval and before implementation edits, create and switch
to:

```text
codex/noisy-rate-contraction-diagnostics
```

Do not implement on `main` unless the Project Owner explicitly authorizes that.

## Implementation Log Requirement

When this workplan is executed, create and maintain:

```text
docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/04_counterpoint_noisy_rate_contraction_diagnostics_implementation_log.md
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

- explicit approval to execute this exact workplan has not been received;
- branch or dirty status would mix unrelated work into this implementation;
- any action would require editing `<state-collapser-repo>`;
- any action would alter `counterpoint_symbolic_v001` environment semantics;
- the noisy selector cannot be implemented without a source-local minimum-one
  floor;
- metadata-selected and runtime-selected edge sets cannot be reconciled;
- coupled-rate monotonicity fails;
- source coverage cannot be summarized;
- active action-cell counts cannot be distinguished from stale historical
  action-cell records;
- a required evaluation-level table would be omitted without expected-file
  policy;
- artifact roots would need to live outside the repo readout surface for a
  durable evaluation run;
- exact implementation of any Phase.Stage.Action would require a weaker
  substitute, hidden simplification, or unapproved reordering;
- implementation pressure starts turning this diagnostic into a learning
  comparison.

## Phase 0. Stage 0. Action 1: Confirm Execution Authority

Before implementation edits, confirm that the Project Owner explicitly
requested execution of this exact workplan.

If not approved, stop.

## Phase 0. Stage 0. Action 2: Inspect Working Tree

Run non-destructive git status inspection.

Identify unrelated dirty or untracked files.

Do not modify unrelated files.

If unrelated dirty state would be mixed into this work, stop and ask.

## Phase 0. Stage 0. Action 3: Create Work Branch

Create and switch to:

```text
codex/noisy-rate-contraction-diagnostics
```

Record the branch in the implementation log.

## Phase 0. Stage 0. Action 4: Create Implementation Log

Create:

```text
docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/04_counterpoint_noisy_rate_contraction_diagnostics_implementation_log.md
```

Initialize it with:

- source workplan path;
- branch name;
- execution start timestamp;
- current `git status --short`;
- declared stop conditions;
- Phase.Stage.Action checklist.

## Phase 0. Stage 1. Action 1: Re-Read Source Authority

Immediately before code edits, re-read:

```text
docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/02_counterpoint_noisy_rate_contraction_diagnostics_blueprint.md
docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/03_counterpoint_noisy_rate_contraction_diagnostics_implementation_workplan.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

Record completion in the implementation log.

## Phase 0. Stage 1. Action 2: Map Existing Reusable Surfaces

Inspect existing counterpoint source surfaces:

```text
src/big_boy_benchmarking/environments/counterpoint/ids.py
src/big_boy_benchmarking/environments/counterpoint/schemas.py
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/
src/big_boy_benchmarking/cli/main.py
tests/environments/counterpoint/
tests/cli/
```

Record in the implementation log:

- files expected to be edited;
- files expected to remain behaviorally unchanged;
- reusable helpers;
- places where shared extraction is safe;
- places where copy-adapt is safer than refactor.

## Phase 1. Stage 1. Action 1: Add Stable IDs

Add stable ids for:

```text
counterpoint_noisy_rate_contraction_diagnostics_v001
counterpoint_noisy_rate_contraction_schema_v001
counterpoint_noisy_rate_contraction_single_block_schema_v001
```

Add them to canonical id coverage where the repo expects canonical ids.

Do not remove or rename existing one-third or fraction-sweep ids.

## Phase 1. Stage 1. Action 2: Add Rate Arm Helpers

Add helpers for rate arm ids.

Required arms for the default full sweep:

```text
p001_over_288
p001_over_144
p001_over_072
p001_over_036
p001_over_024
p001_over_018
p001_over_012
p001_over_009
```

Required control arm:

```text
no_contraction_control
```

Rate parsing must support CLI input shaped as:

```text
1/144,1/36,1/18
```

and serialize numerator/denominator fields explicitly in result rows.

## Phase 1. Stage 1. Action 3: Implement Stable Edge Score Helper

Implement a deterministic helper that maps:

```text
selector_rule_id, instance_id, schema_seed, canonical_edge_key
```

to a stable uniform score in `[0, 1)`.

Required properties:

- use a stable hash such as SHA-256;
- do not use Python's `hash()`;
- return the same value across processes and machines;
- include `selector_rule_id` in the hashed material;
- include instance id or an equivalent graph identity guard;
- expose enough detail for tests to verify determinism.

## Phase 1. Stage 1. Action 4: Implement Metadata Noisy-Rate Selection Helper

Implement a metadata helper that selects graph edges by:

```text
stable_uniform(edge, schema_seed) < numerator / denominator
```

Required outputs:

- selected edge keys;
- selected edge count;
- selected edge share;
- expected selected edge count;
- selected source count;
- zero-selected-source count;
- selected-source share;
- selected-edge count per source;
- source out-degree distribution inputs;
- selector rule id.

This helper must allow sources with outgoing edges to select zero edges.

## Phase 1. Stage 1. Action 5: Implement Source Coverage Helper

Implement source-coverage summarization for a graph and selected edge set.

Required outputs:

- source count with outgoing edges;
- source count with selected edges;
- zero-selected-source count;
- selected-source share;
- minimum selected edges per source;
- mean selected edges per source;
- maximum selected edges per source;
- selected-edge count histogram by source;
- source out-degree histogram;
- selected source out-degree histogram;
- expected zero-source share if practical.

If expected zero-source share is not implemented, record that as a deliberate
not-applicable field in expected-file or row policy rather than silently
omitting it.

## Phase 1. Stage 1. Action 6: Implement Noisy-Rate Monotonicity Helper

For a fixed instance and schema seed, verify:

```text
selected_edges(rate_a) subset selected_edges(rate_b)
```

whenever:

```text
rate_a <= rate_b
```

Required report fields:

- instance id;
- schema seed;
- from arm id;
- to arm id;
- from numerator;
- from denominator;
- to numerator;
- to denominator;
- subset pass;
- missing nested edge count;
- example offending edge keys.

If monotonicity fails in tests, stop and return to design.

## Phase 1. Stage 1. Action 7: Implement Metadata/Runtime Consistency Helper

Implement a helper that compares metadata-selected edge keys with
runtime-selected edge keys for the same instance, rate, and schema seed.

Required report fields:

- metadata selected edge count;
- runtime selected edge count;
- equality status;
- missing from runtime count;
- extra in runtime count;
- example mismatches.

If equality fails in tests, stop and return to design.

## Phase 1. Stage 2. Action 1: Implement Runtime Noisy-Rate Schema

Implement a new `state_collapser` `ContractionSchema` adapter in BBB, parallel
to `CounterpointOutgoingFractionSchema`.

Required behavior:

- constructor accepts `numerator`, `denominator`, `schema_seed`, and
  `selector_rule_id`;
- denominator must be positive;
- numerator must be between `1` and denominator for normal rate arms;
- `ordered_blocks()` returns exactly one scheduled block for noisy-rate arms;
- `assign_edge()` returns that scheduled block only for selected edges;
- unselected edges return `None`;
- no source-local minimum-one floor is used.

The runtime selection must use the same stable score semantics as metadata
selection, or the implementation must provide a verified canonical mapping.

## Phase 1. Stage 2. Action 2: Implement Noisy-Rate Tower Builder

Add a tower builder parallel to:

```text
build_counterpoint_fraction_partition_tower
```

Required conceptual API:

```text
build_counterpoint_noisy_rate_partition_tower(
    spec,
    numerator,
    denominator,
    schema_seed,
    selector_rule_id,
)
```

The builder must:

- preserve counterpoint hidden graph construction;
- use the existing reward aggregator pattern;
- initialize states and edges as existing builders do;
- return the existing `CounterpointTowerBuildResult` shape or a compatible
  extension.

## Phase 1. Stage 2. Action 3: Preserve Existing Schemas

Run or update regression coverage to prove these remain behaviorally intact:

- no-contraction schema;
- structured motion schema;
- random balanced/unbalanced schema ids;
- one-third outgoing schema;
- source-local fraction sweep schema.

No existing schema id may be repurposed for noisy-rate behavior.

## Phase 1. Stage 3. Action 1: Reuse Or Extract Endpoint-Coalescence Helper

Reuse the endpoint-coalescence diagnostic helper introduced for the fraction
sweep, or extract it to a shared local helper if needed.

The helper must report:

- processed edge count;
- useful coalescence count;
- redundant/internal edge count;
- state cells after block;
- largest coalesced cell size;
- largest coalesced cell share;
- processed edge index at first singleton;
- whether singleton collapse required most of the block.

Add noisy-rate fields at aggregation time:

- selected edge count;
- selected source count;
- zero-selected-source count;
- realized source coverage.

Do not describe this as a separate `pi_0` operation.

## Phase 1. Stage 3. Action 2: Reuse Active Action-Cell Counting

Reuse the existing active action-cell count helper.

The noisy-rate evaluation must keep separate:

- active action-cell count;
- raw historical action-cell record count.

If this helper cannot be reused safely, stop before substituting a weaker
count.

## Phase 2. Stage 1. Action 1: Create Noisy-Rate Diagnostics Package

Create a new package:

```text
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/
```

Do not replace:

```text
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/
```

## Phase 2. Stage 1. Action 2: Add Package Config

Add config definitions for:

- evaluation id;
- schema family id;
- selector rule id;
- default rates;
- smoke rates;
- default instances;
- schema seeds;
- replicates;
- episodes;
- linearization mode;
- near-collapse threshold;
- source-coverage class thresholds;
- run mode.

Recommended defaults:

```text
default_instances: small,medium
default_rates: 1/288,1/144,1/72,1/36,1/24,1/18,1/12,1/9
smoke_rates: 1/144,1/36,1/18
full_schema_seeds: 0..31
smoke_schema_seeds: 0,1,2
full_replicates: 4
smoke_replicates: 1
full_episodes: 16
smoke_episodes: 1
linearization_mode: tensor_available_disabled
```

Allow CLI overrides for smoke and constrained runs without changing locked
defaults.

## Phase 2. Stage 1. Action 3: Add Path Helpers

Add path helpers for:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/
```

and source evaluation roots under:

```text
<artifact-root>/evaluations/counterpoint_noisy_rate_contraction_diagnostics_v001/
```

Enforce repo-resident artifact roots for durable evaluation runs.

## Phase 2. Stage 2. Action 1: Define Event And Summary Rows

Define typed row models or equivalent structured serializers for:

```text
noisy_rate_selection_summary.csv
noisy_rate_source_coverage_summary.csv
noisy_rate_selection_consistency_summary.csv
noisy_rate_monotonicity_summary.csv
noisy_rate_threshold_summary.csv
tower_shape_summary.csv
endpoint_coalescence_summary.csv
tier_executability_summary.csv
tier_occupancy_summary.csv
control_action_summary.csv
abc_selection_summary.csv
abc_tier_signal_summary.csv
lift_failure_by_tier.csv
concrete_step_summary.csv
evaluation_aggregate_table.csv
evaluation_run_index.csv
```

Every row that belongs to an arm must include:

- evaluation id;
- instance id;
- arm id;
- numerator;
- denominator;
- requested rate;
- schema seed;
- selector rule id where applicable;
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
- selector rule id;
- source files;
- expected files;
- goal criteria;
- structural limit checks;
- badge policy;
- goal summary sources;
- methodology summary sources;
- claim boundary;
- link to the noisy-rate blueprint;
- link to the parent unexpected-collapse archive;
- link to the previous source-local fraction sweep readout.

## Phase 2. Stage 2. Action 3: Add Expected-File Policy

Add expected-file policy listing every required manifest and result table.

The expected-file policy must distinguish:

- required;
- conditional;
- not applicable;
- expected absent is gap.

Do not silently omit noisy-rate-specific tables.

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
results/noisy_rate_thresholds.md
results/source_coverage.md
badges/
```

The seed docs must include the correct human-readability command:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-root>/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json
```

Docs must include protected clarification turn slots if the current readout
protocol expects them.

## Phase 2. Stage 3. Action 2: Add Badge Input Support

Populate source binding and/or summary fields needed for badges:

- artifact status;
- noisy-rate sweep status;
- source coverage status;
- collapse threshold status;
- runtime executability status;
- diagnostic-only scope;
- repo artifact provenance.

Do not hard-code green success if artifacts do not support it.

## Phase 3. Stage 1. Action 1: Implement Run Enumeration

Implement run enumeration over:

- instances;
- rate arms;
- schema seeds;
- replicates;
- episodes.

Include `no_contraction_control`.

Do not include deterministic floor-reference arms in this first implementation.

Ensure run ids encode:

- instance id;
- rate arm id;
- schema seed;
- replicate index.

## Phase 3. Stage 1. Action 2: Implement Tower Build Per Arm

For each noisy-rate arm, build a `PartitionTower` using the new single-block
noisy-rate schema.

For `no_contraction_control`, use the existing no-contraction schema.

Record tower construction metadata before controller episodes run.

## Phase 3. Stage 1. Action 3: Implement Per-Run Structural Summaries

For each run, emit per-run structural files that support evaluation-level
tables.

Required evidence includes:

- noisy-rate selected edges;
- source coverage;
- zero-selected-source count;
- metadata/runtime consistency;
- monotonicity context;
- quotient/tower shape;
- active action-cell count;
- raw historical action-cell record count if retained;
- state-cell member-size histogram;
- endpoint-coalescence diagnostics.

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

All required tables listed in Phase 2. Stage 2. Action 1 must be written by
the summarize command.

If a table is genuinely not applicable for a run mode, record that in
expected-file policy rather than silently omitting it.

## Phase 4. Stage 1. Action 2: Implement Noisy-Rate Selection Summary

Aggregate:

```text
results/noisy_rate_selection_summary.csv
```

Required row fields include:

- evaluation id;
- environment family id;
- instance id;
- arm id;
- numerator;
- denominator;
- requested rate;
- schema seed;
- selector rule id;
- base state count;
- base edge count;
- selected edge count;
- realized selected edge share;
- expected selected edge count;
- selected edge count residual from expectation;
- construction rule;
- block id.

## Phase 4. Stage 1. Action 3: Implement Source Coverage Summary

Aggregate:

```text
results/noisy_rate_source_coverage_summary.csv
```

Required row fields include:

- source count with outgoing edges;
- source count with selected edges;
- zero-selected-source count;
- selected-source share;
- minimum selected edges per source;
- mean selected edges per source;
- maximum selected edges per source;
- selected-edge count histogram;
- source out-degree histogram;
- selected source out-degree histogram;
- expected zero-source share where implemented;
- realized zero-source share;
- source-coverage class.

## Phase 4. Stage 1. Action 4: Implement Selection Consistency Summary

Aggregate:

```text
results/noisy_rate_selection_consistency_summary.csv
```

Required row fields include:

- metadata selected edge count;
- runtime selected edge count;
- equality status;
- missing from runtime count;
- extra in runtime count;
- example mismatches.

Any false equality status must invalidate interpretation and be reflected in
aggregate status.

## Phase 4. Stage 1. Action 5: Implement Monotonicity Summary

Aggregate:

```text
results/noisy_rate_monotonicity_summary.csv
```

Required row fields include:

- from arm id;
- to arm id;
- from requested rate;
- to requested rate;
- subset pass;
- missing nested edge count;
- example offending edges.

Any monotonicity failure under coupled selection must invalidate
interpretation and be reflected in aggregate status.

## Phase 4. Stage 1. Action 6: Implement Threshold Summary

Aggregate:

```text
results/noisy_rate_threshold_summary.csv
```

For each instance and schema seed, report:

- first full-collapse rate;
- first near-collapse rate;
- last nontrivial rate;
- first high-source-coverage rate;
- source coverage at first full collapse;
- selected edge share at first full collapse;
- selected edge count at first full collapse;
- useful coalescence count at first full collapse;
- first singleton edge index at first full collapse;
- sweep verdict.

Also support grouped instance-level summaries in either this table or a
separate aggregate summary field:

- collapse count by rate;
- median first full-collapse rate;
- rate at which at least 50 percent of seeds collapse;
- rate at which at least 90 percent of seeds collapse;
- source coverage distribution at collapse.

## Phase 4. Stage 1. Action 7: Implement Sweep Verdict Classification

Classify each per-seed sweep as one of:

```text
no_collapse
low_rate_immediate_collapse
coverage_threshold_found
edge_rate_threshold_found
mixed_by_seed
invalid_or_uninterpretable
```

Back each classification with table fields, not prose-only inference.

## Phase 4. Stage 2. Action 1: Generate Repo Readout Surface

Ensure the summarize command writes or updates:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/README.md
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/method.md
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/runbook.md
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/artifact_index.md
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/glossary.md
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/results/
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/badges/
```

Do not point the readout protocol at a raw artifact root.

## Phase 4. Stage 2. Action 2: Implement Readout Interpretation Text

The generated README must explain:

- expected rate versus realized selected edge count;
- selected edge share versus source coverage;
- zero-selected-source count;
- how noisy-rate semantics differ from the source-local floor rule;
- whether collapse correlates with source coverage;
- whether active tiers are executable;
- claim boundaries.

It must not claim learning performance.

## Phase 5. Stage 1. Action 1: Add CLI Run Command

Add:

```text
uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate run
```

Required options:

- `--artifact-root`;
- `--instances`;
- `--rates`;
- `--schema-seeds`;
- `--replicates`;
- `--episodes`;
- `--base-seed`;
- `--linearization-mode`;
- `--locked-by`;
- `--horizon`;
- `--controller-event-ceiling`;
- `--include-no-contraction-control`;
- `--omit-no-contraction-control`.

`--rates` should accept comma-separated fractions such as:

```text
1/144,1/36,1/18
```

Defaults must match package config while allowing smoke overrides.

## Phase 5. Stage 1. Action 2: Add CLI Summarize Command

Add:

```text
uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate summarize
```

Required option:

```text
--artifact-root
```

Optional option:

```text
--docs-root
```

The summarize command must produce evaluation-level tables, docs seeds,
badges, and `readout_source.json`.

## Phase 5. Stage 1. Action 3: Add CLI Diagnostics Option If Useful

If it fits local CLI patterns without scope drift, add a lightweight
diagnostic option or command that builds noisy-rate selections and reports
source coverage, monotonicity, and selected-edge counts without running
episodes.

If adding this would cause scope drift, skip it and record the decision in the
implementation log.

## Phase 6. Stage 1. Action 1: Add Selector Unit Tests

Add tests proving:

- deterministic stable scores for fixed seed and edge;
- no use of Python process-randomized `hash()`;
- rate parsing handles `1/144,1/36,1/18`;
- selected edge sets are nested across increasing rates;
- different schema seeds can produce different selections;
- no source-local minimum-one floor exists;
- at least one test fixture has sources with zero selected edges;
- invalid numerator/denominator inputs fail clearly.

## Phase 6. Stage 1. Action 2: Add Metadata/Runtime Consistency Tests

Add tests proving metadata-selected edge sets match runtime-selected edge sets
for representative rates and seeds.

If exact runtime extraction is expensive, add a focused small fixture that
still exercises the same canonical mapping.

Do not mark this action complete with only a placeholder test.

## Phase 6. Stage 1. Action 3: Add Source Coverage Summary Tests

Add tests proving:

- selected source count is correct;
- zero-selected-source count is correct;
- selected-source share is correct;
- source selected-edge count histogram is correct;
- no-contraction control reports zero selected edges and zero selected
  sources;
- low-rate noisy selections can have zero-selected sources.

## Phase 6. Stage 1. Action 4: Add Endpoint-Coalescence Regression Tests

Add or reuse tests proving endpoint-coalescence diagnostics still report:

- useful coalescence count;
- redundant/internal edge count;
- state cells after block;
- first singleton edge index.

Ensure test names and assertions avoid loose `pi_0` language.

## Phase 6. Stage 2. Action 1: Add Artifact Contract Tests

Add tests proving:

- `readout_source.json` is generated and parses;
- required noisy-rate result tables are listed;
- expected-file policy exists;
- goal summary sources include the noisy-rate blueprint;
- methodology summary sources include the noisy-rate blueprint and protocols;
- artifact root validation enforces repo-resident durable evaluation paths;
- source binding targets the repo readout surface, not raw artifacts.

## Phase 6. Stage 2. Action 2: Add CLI Smoke Tests

Add tests or scripted test coverage for:

```text
counterpoint noisy-rate run
counterpoint noisy-rate summarize
```

Use a small budget appropriate for test runtime.

The smoke test must include at least two rates and at least two schema seeds
so nesting and source-coverage variance are exercised.

## Phase 6. Stage 3. Action 1: Run Targeted Tests

Run the targeted noisy-rate diagnostics tests.

Record exact commands and results in the implementation log.

If tests fail, fix the implementation or stop if the failure indicates a
design conflict.

## Phase 6. Stage 3. Action 2: Run Counterpoint Regression Tests

Run existing counterpoint tests covering:

- tower adapter;
- one-third diagnostics;
- source-local fraction sweep diagnostics;
- schemas;
- ids;
- CLI.

Record exact commands and results in the implementation log.

## Phase 7. Stage 1. Action 1: Run Repo-Resident Smoke Artifact Run

Run a bounded smoke artifact run under:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/artifacts/smoke_001/
```

Recommended smoke shape:

- instance: `small`;
- rates: `1/144,1/36,1/18`;
- schema seeds: `0,1,2`;
- replicates: `1`;
- episodes: `1`;
- linearization mode: `tensor_available_disabled`;
- no-contraction control: included.

This smoke run is for implementation verification and first diagnostic
evidence. It is not full validation.

## Phase 7. Stage 1. Action 2: Summarize Smoke Artifacts

Run the summarize command against the smoke artifact root.

Verify:

- all required smoke result tables exist;
- `readout_source.json` exists;
- docs seed files exist;
- badges exist;
- source coverage table exists;
- monotonicity table exists;
- selection consistency table exists;
- active action-cell counts are present.

## Phase 7. Stage 1. Action 3: Run Human-Readability Protocol On Smoke

Execute the readout protocol against:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json
```

Verify that generated docs:

- open with badge/status summary;
- identify the run as smoke if the source binding says smoke;
- explain expected rate versus realized selected edge count;
- explain selected edge share versus source coverage;
- report zero-selected-source count;
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
- missing source-coverage interpretation;
- missing zero-selected-source interpretation;
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
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/artifacts/small_medium_validation_001/
```

Default full shape:

- instances: `small,medium`;
- rates: `1/288,1/144,1/72,1/36,1/24,1/18,1/12,1/9`;
- schema seeds: `0..31`;
- replicates: `4`;
- episodes: `16`;
- linearization mode: `tensor_available_disabled`;
- no-contraction control: included.

## Phase 8. Stage 1. Action 3: Summarize Full Validation Artifacts If Run

If full validation artifacts were generated, run the summarize command.

Verify all required evaluation-level tables exist and parse.

## Phase 8. Stage 1. Action 4: Generate Full Human Readout If Full Run Was Summarized

If full validation artifacts were summarized, execute:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-root>/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json
```

Review generated docs for the same claim-boundary, source-coverage, and
action-cell language checks used for smoke.

## Phase 9. Stage 1. Action 1: Update Design Archive Status

Update:

```text
docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/README.md
docs/design/system_learning_from_evaluations/README.md
```

only if implementation status has changed.

Record links to:

- implementation log;
- evaluation readout surface;
- smoke artifact run;
- full validation run, if produced.

Do not overwrite the archived conversation.

## Phase 9. Stage 1. Action 2: Final Verification Pass

Run:

- formatting or compile checks used by this repo;
- targeted noisy-rate tests;
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
- remaining Project Owner decisions.

Do not claim completion of any action that was skipped by a decision lock.

## Expected File Change Map

Likely source additions:

```text
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/
```

Likely source edits:

```text
src/big_boy_benchmarking/environments/counterpoint/ids.py
src/big_boy_benchmarking/environments/counterpoint/schemas.py
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
src/big_boy_benchmarking/cli/main.py
```

Likely docs/evaluation additions:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/
```

Likely design-log addition:

```text
docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/04_counterpoint_noisy_rate_contraction_diagnostics_implementation_log.md
```

Likely tests:

```text
tests/environments/counterpoint/test_noisy_rate_diagnostics.py
tests/cli/test_cli.py
```

The exact file list must be discovered during implementation. This section is
a map, not permission to make unrelated edits.

## Implementation Readiness

This workplan is ready for Project Owner review.

It is not yet authorized for execution.
