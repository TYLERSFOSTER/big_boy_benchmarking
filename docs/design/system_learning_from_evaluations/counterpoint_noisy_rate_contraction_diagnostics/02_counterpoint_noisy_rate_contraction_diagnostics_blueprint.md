# Counterpoint Noisy-Rate Contraction Diagnostics Blueprint

Date: 2026-06-01

Status: draft blueprint

Repository:

```text
/Users/foster/big_boy_benchmarking
```

Design folder:

```text
docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/
```

## Status And Authority

This is a design blueprint.

This is not an implementation workplan.

This is not approval to edit source code.

This is not approval to run benchmark artifacts.

This is not approval to change the `counterpoint_symbolic_v001`
environment.

This is not approval to edit `/Users/foster/state_collapser`.

This blueprint turns the noisy-rate contraction discussion into a concrete
diagnostic evaluation design. A later Phase.Stage.Action implementation
workplan must translate this blueprint into executable work before source
changes begin.

## Source Authority

This blueprint follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`
- `docs/design/system_learning_from_evaluations/README.md`
- `docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/README.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/README.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/01_fraction_sweep_readout_conversation_archive.md`
- `docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/README.md`
- current BBB counterpoint schema/tower/evaluation source surfaces as read-only
  context

## PO Attribution Ledger

This section records only Project Owner-originated scope, observations, and
requests. Consultant interpretation appears later under explicit consultant
labels.

1. The Project Owner asked for an explanation of the `1/18` collapse observed
   in the contraction fraction sweep readout.

2. The Project Owner asked how difficult it would be to modify the evaluation
   so that contraction selection is noisier than a ceiling function.

3. The Project Owner proposed the motivating example of a `1/36` mean rate
   that often samples no arrows.

4. The Project Owner stated an expectation that contraction schemata had been
   set up so this should be relatively simple, while asking how different it
   would be from the details of the `1/18` evaluation.

5. The Project Owner requested creation of a folder for the new evaluation and
   asked that the motivating conversation be copied there.

6. The Project Owner asked whether the folder contains enough information to
   build a full blueprint.

7. The Project Owner requested this full blueprint in the noisy-rate design
   folder.

## Consultant Sufficiency Judgement

There is enough information to write a full blueprint.

There is not enough Project Owner authority to implement it yet.

The open choices are normal blueprint-level choices rather than blockers:

- sampling model;
- exact rate grid;
- smoke and full validation budgets;
- whether to include the deterministic source-local floor rule as a structural
  reference arm;
- naming preferences.

Those ambiguities are recorded in the turn-question section near the end.

## Executive Design

The current source-local fraction sweep produced a surprising smoke result:

```text
n01_over_18, small fixture:
base tier: 108 state cells, 1140 active action cells
tier 1:      1 state cell,     0 active action cells
```

The relevant selector rule was:

```text
max(1, ceil(out_degree * n / denominator))
```

At `n=1`, `denominator=18`, this selected `112` edges out of `1140`, about
`9.8%` of base edges. That is not globally huge, but it selected at least one
edge from every source state with outgoing edges. The scheduled block therefore
had complete source coverage.

The endpoint-coalescence table showed:

```text
processed edges:            112
useful coalescences:        107
redundant/internal edges:     5
state cells after block:      1
```

Since the base has `108` states, `107` useful coalescences are exactly enough
to merge every base state into a singleton quotient cell.

This blueprint designs a sibling diagnostic that removes the source-local
minimum-one floor. Instead of scheduling at least one edge per source, it
selects edges according to a noisy expected rate. This allows many sources to
contribute zero scheduled edges, especially at low rates such as `1/36`,
`1/72`, or `1/144`.

The core diagnostic question becomes:

```text
At what expected edge rate, and at what realized source coverage, does repeated
endpoint coalescence begin to collapse the counterpoint tower?
```

## Evaluation Purpose

The purpose is to determine whether the `1/18` collapse was primarily caused
by source-covering deterministic quota semantics.

The evaluation should separate:

- expected selected edge rate;
- realized selected edge rate;
- realized selected edge count;
- realized source coverage;
- zero-selected-source count;
- useful endpoint coalescence count;
- first singleton-collapse edge index;
- tower quotient shape;
- live executable tier surface;
- concrete runtime behavior under the existing active-tier controller.

This is a structural/runtime diagnostic.

This is not a learning-performance comparison.

## Primary Evaluation Question

Primary question:

```text
If contraction edges are selected by a noisy expected-rate selector that allows
sources to contribute zero scheduled edges, does the counterpoint tower still
collapse at very low realized rates?
```

Secondary questions:

1. Does collapse correlate more strongly with selected edge share or realized
   source coverage?
2. Does collapse occur only after source coverage approaches a high threshold?
3. Are there low-rate random selections that preserve nontrivial first-tier
   structure?
4. Do some low-rate selections still collapse because they hit high-bridge
   edges?
5. Does the medium fixture behave like the small fixture?
6. Does the active executable tier surface fail only after quotient collapse,
   or earlier?
7. Does the runtime continue to generate concrete steps at base tier even when
   tier 1 collapses?

## Non-Goals

This evaluation must not claim:

- tower learning advantage;
- direct-vs-tower comparison;
- final counterpoint learning quality;
- musical quality;
- tensor-enabled behavior;
- CUDA/GPU behavior;
- production performance;
- upstream `state_collapser` semantics changes;
- that the counterpoint environment is degenerate;
- that the prior source-local fraction sweep was invalid;
- that a noisy-rate selector is the intended final counterpoint schema.

This evaluation must not change:

- the `counterpoint_symbolic_v001` environment definition;
- state enumeration;
- action enumeration;
- transition legality;
- reward semantics;
- legal-action masks;
- upstream `state_collapser`.

## Recommended Evaluation Identity

Recommended evaluation id:

```text
counterpoint_noisy_rate_contraction_diagnostics_v001
```

Recommended schema family id:

```text
counterpoint_noisy_rate_contraction_schema_v001
```

Recommended concrete schema id prefix:

```text
counterpoint_noisy_rate_contraction_single_block_schema_v001
```

Recommended run mode:

```text
diagnostic_noisy_rate_contraction_tower_abc
```

Recommended CLI group:

```text
counterpoint noisy-rate
```

Recommended repo readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/
```

Recommended artifact root shape:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/artifacts/<run-label>/
```

Recommended source evaluation root shape:

```text
<artifact-root>/evaluations/counterpoint_noisy_rate_contraction_diagnostics_v001/
```

Recommended initial smoke run label:

```text
smoke_001
```

Recommended first full validation run label:

```text
small_medium_validation_001
```

## Relationship To Existing Fraction Sweep

This noisy-rate diagnostic must be a sibling evaluation, not a mutation of the
existing fraction sweep.

The existing fraction sweep means:

```text
source-local deterministic quota with minimum one selected edge per nonempty source
```

The proposed noisy-rate diagnostic means:

```text
seeded random expected-rate selection with no minimum-one source floor
```

Existing artifacts under:

```text
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/
```

must remain interpretable as source-local floor quota artifacts.

The new artifacts should live under:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/
```

This preserves the distinction between:

- deterministic source-covering quota behavior;
- noisy expected-rate behavior with zero-selected sources.

## Recommended Selector Semantics

### Consultant Recommendation

Use a coupled Bernoulli edge-threshold selector.

For each base edge and schema seed, compute a deterministic pseudo-random
uniform score:

```text
u(edge, schema_seed) in [0, 1)
```

For a rate:

```text
p = numerator / denominator
```

select the edge if:

```text
u(edge, schema_seed) < p
```

This has several useful properties:

1. It gives each edge marginal selection probability `p`.
2. It allows any source to contribute zero selected outgoing edges.
3. It produces nested selections when rates increase for the same schema seed:

   ```text
   selected_edges(p1) subset selected_edges(p2) when p1 <= p2
   ```

4. It makes threshold diagnosis much cleaner than independently resampling at
   every rate.
5. It is easy to summarize source coverage after selection.

This recommendation is consultant-authored. It is not yet a Project Owner
decision.

### Alternatives Considered

Edge Bernoulli with independent rate draws:

- Simple.
- Allows zero-source selection.
- Does not automatically produce nested rate sweeps unless the same per-edge
  score is reused across rates.

Source-local binomial with shuffled prefix:

- Keeps continuity with the current per-source shuffle pattern.
- Allows zero selected edges from a source.
- Can be made equivalent in distribution to edge Bernoulli if the selected
  subset is uniform conditional on count.
- Less direct than coupled edge-threshold selection for monotone rate sweeps.

Poisson count per source:

- Noisy and flexible.
- Adds a new distributional assumption.
- Not recommended as the first diagnostic unless the Project Owner explicitly
  wants Poisson semantics.

## Selector Invariants

The selected-edge helper and runtime `ContractionSchema` must satisfy these
invariants:

1. Denominator is positive.
2. Numerator is nonnegative and not greater than denominator.
3. `numerator=0` selects no edges and should be represented by the explicit
   no-contraction control rather than a normal noisy-rate arm unless the
   implementation chooses to allow a zero-rate arm.
4. For every edge, selection is deterministic for:

   ```text
   instance_id, schema_seed, edge_identity, numerator, denominator
   ```

5. For coupled rates under the same seed:

   ```text
   p1 <= p2 => selected_edges(p1) subset selected_edges(p2)
   ```

6. No source-local minimum-one floor is allowed.
7. A source with outgoing edges may select zero edges.
8. Metadata-selected edges and runtime-selected edges must match exactly.
9. The selected block is a single scheduled contraction block.
10. Unselected edges are unscheduled.

If invariant 8 cannot be verified, implementation must stop and return to
design.

## Runtime Schema Shape

The runtime schema should be a new `state_collapser` `ContractionSchema`
adapter in BBB, parallel to `CounterpointOutgoingFractionSchema`.

Conceptual constructor:

```text
CounterpointNoisyRateSchema(
    numerator: int,
    denominator: int,
    schema_seed: int,
    selector_rule_id: str = "coupled_bernoulli_edge_threshold_v001",
)
```

`ordered_blocks()` should return exactly one scheduled block:

```text
("counterpoint_noisy_rate", numerator, denominator)
```

`assign_edge(edge_id, registry)` should return that block id if the edge is
selected by the seeded noisy-rate selector and `None` otherwise.

The runtime selector must not depend on episode outcomes, rewards, learned
values, controller state, or future observations.

## Metadata And Runtime Consistency

This evaluation has a special consistency risk: metadata helpers may operate
on BBB `GraphEdge` identities, while runtime schemas operate on
`state_collapser` registry edge ids.

The implementation must either:

1. use a single shared edge identity canonicalization for both paths; or
2. extract selected runtime edge identities after tower initialization and use
   those as the source of truth for summaries; or
3. write a proof/test that BBB graph-edge keys and runtime edge ids map
   one-to-one for this selector.

The artifact set must include a consistency table:

```text
noisy_rate_selection_consistency_summary.csv
```

Required fields:

- evaluation id;
- instance id;
- rate arm id;
- numerator;
- denominator;
- schema seed;
- metadata selected edge count;
- runtime selected edge count;
- equality status;
- missing from runtime count;
- extra in runtime count;
- example mismatches.

If equality fails, the run is invalid for interpretation.

## Rate Arms

The blueprint needs rates low enough that many sources can select zero edges.

Recommended initial diagnostic rates:

```text
1/288
1/144
1/72
1/36
1/24
1/18
1/12
1/9
```

Rationale:

- `1/288`, `1/144`, and `1/72` probe far below the old `1/18` smoke result.
- `1/36` is the Project Owner's motivating example.
- `1/24` and `1/18` connect the noisy-rate sweep back to the observed collapse
  neighborhood.
- `1/12` and `1/9` give stronger rates in case all lower rates preserve
  structure.

Recommended arm ids:

```text
no_contraction_control
p001_over_288
p001_over_144
p001_over_072
p001_over_036
p001_over_024
p001_over_018
p001_over_012
p001_over_009
```

Use zero-padded denominator formatting only where local code style requires it.
The readout should always print the human-readable rate as `1/36`, not only an
arm id.

## Optional Reference Arms

The evaluation may optionally include structural reference arms from the
source-local floor sweep:

```text
floor_n01_over_18_reference
floor_n06_over_18_reference
```

These arms would not make the evaluation a learning comparison. They would
only remind the readout where the previous source-local floor semantics
collapsed.

However, this adds scope. If included, the readout must label them as
reference controls, not part of the noisy-rate sweep threshold.

Open PO question: include these reference arms or keep the first noisy-rate
diagnostic pure?

## Randomness And Seed Discipline

Noisy-rate selection makes schema-seed variance central rather than incidental.

The evaluation must distinguish:

- selector schema seed;
- controller/episode replicate seed;
- base environment instance id;
- rate arm id.

The selection score for an edge should be stable across repeated runs with the
same:

```text
instance_id, edge identity, schema_seed
```

Recommended implementation detail:

```text
score = stable_uniform_0_1(sha256(selector_rule_id, schema_seed, canonical_edge_key))
```

Do not use Python's process-randomized `hash()`.

If the repo already has a deterministic seed bundle helper for artifacts, the
implementation should use it for recording seeds, but selection itself should
remain reproducible from explicit artifact fields.

## Expected Source-Coverage Behavior

For a source with out-degree `d` and rate `p`, edge Bernoulli selection gives:

```text
P(source selects zero edges) = (1 - p)^d
```

For the motivating `1/36` example and a source out-degree near `10`:

```text
P(zero selected) ~= (35/36)^10 ~= 0.754
```

That means most sources should contribute zero scheduled edges at `1/36`.

This is the core contrast with the source-local floor rule, where every
nonempty source contributed at least one scheduled edge.

The readout must therefore place source coverage near the top of the result,
not bury it in raw tables.

## Evaluation Budget

### Smoke Budget

Recommended smoke budget:

```text
instances: small
rates: 1/144,1/36,1/18
schema_seeds: 0,1,2
replicates_per_schema_seed: 1
episodes_per_replicate: 1
linearization_mode: tensor_available_disabled
include_no_contraction_control: true
```

Purpose:

- verify CLI and artifact contract;
- verify noisy selector can select zero-source outcomes;
- verify selected edge sets are nested by rate for each schema seed;
- verify readout can explain realized source coverage;
- detect obvious immediate-collapse behavior without spending full budget.

### Full Validation Budget

Recommended full validation budget:

```text
instances: small,medium
rates: 1/288,1/144,1/72,1/36,1/24,1/18,1/12,1/9
schema_seeds: 0..31
replicates_per_schema_seed: 4
episodes_per_replicate: 16
linearization_mode: tensor_available_disabled
include_no_contraction_control: true
```

Reason for more schema seeds:

Noisy selection creates meaningful selector variance. One schema seed can be a
bad witness. A useful diagnostic should report distributions across selector
seeds, not only one sample.

If runtime is too expensive, a first full run may reduce:

```text
schema_seeds: 0..15
replicates_per_schema_seed: 2
episodes_per_replicate: 8
```

but that should be recorded as a constrained validation budget, not silently
called complete full validation.

## Required Artifact Tables

The evaluation must produce the shared benchmark machinery tables already used
by counterpoint diagnostics, plus noisy-rate-specific tables.

Core run/evaluation tables:

```text
evaluation_manifest.json
evaluation_arm_manifest.json
evaluation_budget_lock.json
evaluation_run_index.csv
evaluation_aggregate_table.csv
evaluation_aggregate_summary.json
readout_source.json
```

Noisy-rate structural tables:

```text
results/noisy_rate_selection_summary.csv
results/noisy_rate_source_coverage_summary.csv
results/noisy_rate_selection_consistency_summary.csv
results/noisy_rate_monotonicity_summary.csv
results/noisy_rate_threshold_summary.csv
```

Tower/runtime tables:

```text
results/tower_shape_summary.csv
results/endpoint_coalescence_summary.csv
results/tier_executability_summary.csv
results/tier_occupancy_summary.csv
results/control_action_summary.csv
results/abc_selection_summary.csv
results/abc_tier_signal_summary.csv
results/lift_failure_by_tier.csv
results/concrete_step_summary.csv
```

Optional reference-control table if source-local floor reference arms are
included:

```text
results/source_local_floor_reference_summary.csv
```

No required table may be silently omitted. If a table is not applicable for a
run mode, the expected-file policy must say so.

## Noisy-Rate Selection Summary

`results/noisy_rate_selection_summary.csv` should contain one row per:

```text
instance_id, rate_arm_id, schema_seed
```

Required fields:

- evaluation id;
- environment family id;
- instance id;
- rate arm id;
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
- selected edge count z-like standardized residual if useful;
- construction rule;
- single block id.

## Source Coverage Summary

`results/noisy_rate_source_coverage_summary.csv` should contain one row per:

```text
instance_id, rate_arm_id, schema_seed
```

Required fields:

- source count with outgoing edges;
- source count with selected edges;
- zero-selected-source count;
- selected-source share;
- minimum selected edges per source;
- mean selected edges per source;
- maximum selected edges per source;
- source selected-edge count histogram;
- source out-degree histogram;
- selected source out-degree histogram;
- expected zero-source share if available;
- realized zero-source share;
- source-coverage class.

Recommended source-coverage classes:

```text
zero_or_tiny_coverage
low_coverage
medium_coverage
high_coverage
full_source_coverage
```

Exact thresholds should be recorded in the artifact manifest.

## Monotonicity Summary

If using the coupled edge-threshold selector, selected edge sets must be nested
for increasing rates under the same schema seed.

`results/noisy_rate_monotonicity_summary.csv` should include:

- instance id;
- schema seed;
- from rate arm;
- to rate arm;
- subset pass;
- missing nested edge count;
- example offending edges.

If monotonicity fails for coupled selectors, the run is invalid.

## Endpoint-Coalescence Summary

The endpoint-coalescence summary should reuse the current diagnostic language:

- repeated endpoint coalescence;
- scheduled contraction block;
- state cells after the scheduled block;
- useful coalescence count;
- redundant/internal edge count;
- processed-edge index at first singleton state cell;
- whether singleton collapse required most of the block.

Avoid:

- loose `pi_0` claims;
- connected-components claims unless exactly justified;
- language implying the counterpoint environment is degenerate.

Additional noisy-rate fields should include:

- selected edge count;
- selected source count;
- zero-selected-source count;
- realized source coverage.

This lets the readout say whether collapse arrived with broad source coverage
or with surprisingly sparse source coverage.

## Threshold Summary

`results/noisy_rate_threshold_summary.csv` should aggregate per:

```text
instance_id, schema_seed
```

and also include overall grouped summaries by instance.

Per-seed fields:

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

Overall fields:

- instance id;
- rate count;
- schema seed count;
- collapse count by rate;
- median first full-collapse rate;
- minimum first full-collapse rate;
- maximum first full-collapse rate;
- rate at which at least 50 percent of seeds collapse;
- rate at which at least 90 percent of seeds collapse;
- source coverage distribution at collapse.

Recommended sweep verdicts:

```text
no_collapse
low_rate_immediate_collapse
coverage_threshold_found
edge_rate_threshold_found
mixed_by_seed
invalid_or_uninterpretable
```

## Tower Shape Summary

Reuse the existing tower-shape semantics:

- tier index;
- state cell count;
- active action-cell count;
- raw historical action-cell record count;
- base state count;
- base edge count;
- compression ratio;
- largest state-cell size;
- largest state-cell share;
- state-cell size histogram;
- full collapse flag;
- near collapse flag;
- degeneracy class.

The readout must again distinguish active action-cell count from raw historical
action records.

This distinction was essential in the `1/18` readout.

## Runtime And Controller Scope

The noisy-rate diagnostic should reuse the existing counterpoint active-tier
controller path, not invent a new policy.

Runtime evidence should answer:

- Which tiers are live executable?
- Which tiers are selected by the controller?
- How many concrete steps occur?
- Do lift attempts succeed?
- Are collapsed tiers constructed but not executable?
- Does the controller remain effectively base-tier-only?

The runtime evidence supports structural diagnosis. It must not be used as a
learning-performance comparison.

## Human-Readable Readout Requirements

The generated repo readout must live at:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/
```

It must include:

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

The README should open with badges.

Recommended badge dimensions:

- artifact status;
- noisy-rate sweep status;
- source coverage status;
- collapse threshold status;
- runtime executability status;
- diagnostic-only scope;
- repo artifact provenance.

The README must explain:

- expected rate versus realized edge count;
- selected edge share versus source coverage;
- zero-selected-source count;
- why this differs from the source-local floor rule;
- that lower rates can still collapse if the selected edges are structurally
  bridging;
- that this is not a learning-performance comparison.

The README must include the exact human-readability protocol command:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json
```

The README must include protected clarification turn slots.

## Readout Interpretation Matrix

The readout should map outcomes to interpretations.

If low rates preserve structure and high rates collapse:

```text
Interpretation: collapse is threshold-like under noisy-rate semantics.
```

If collapse appears only when source coverage is high:

```text
Interpretation: source coverage is likely a major driver of the earlier
source-local floor collapse.
```

If collapse appears at low selected edge share and low source coverage:

```text
Interpretation: particular high-bridge edges or graph endpoint geometry may be
enough to trigger collapse.
```

If no collapse appears even at rates above `1/18`:

```text
Interpretation: the source-local minimum-one floor was probably the dominant
cause of the earlier immediate collapse.
```

If results are mixed by seed:

```text
Interpretation: noisy selection exposes high variance; threshold claims must be
distributional rather than single-run.
```

If metadata and runtime selected-edge sets mismatch:

```text
Interpretation: invalid run; fix selection consistency before making claims.
```

## Expected Source Changes

This section is not implementation approval. It is a map for the later
workplan.

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

Likely test additions:

```text
tests/environments/counterpoint/test_noisy_rate_diagnostics.py
```

Likely docs/evaluation additions:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/
```

## Reuse From Existing Fraction Sweep

The implementation should reuse these existing concepts where practical:

- repo-resident artifact roots;
- evaluation manifests;
- budget locks;
- run indices;
- source bindings;
- docs writer shape;
- active action-cell count helper;
- endpoint-coalescence diagnostic helper;
- tower-shape summary;
- active-tier controller runtime;
- lift/concrete-step event rows;
- badge/readout conventions.

It should not copy/paste the entire fraction-sweep package without extracting
shared code where reuse is obvious. However, implementation should stay scoped:
avoid a broad refactor unless necessary.

## Tests Required By Blueprint

Schema/selector tests:

- rate zero behavior if supported;
- numerator/denominator validation;
- deterministic selection for fixed seed;
- different seeds can produce different selections;
- no source-local minimum-one floor;
- at least one fixture where some sources select zero edges;
- nested selected-edge sets for coupled increasing rates;
- selected edge count is plausible against expected rate;
- metadata/runtime selected-edge consistency.

Artifact contract tests:

- run command writes required manifests and tables;
- summarize command writes required evaluation-level tables;
- `readout_source.json` points to repo readout surface, not raw artifact root;
- expected-file policy lists noisy-rate-specific tables;
- docs writer produces README, method, runbook, result summaries, badges, and
  clarification turn slots.

Regression tests:

- existing fraction sweep still passes;
- existing one-third diagnostics still pass;
- existing counterpoint tower adapter tests still pass;
- CLI smoke tests still pass.

## Stop Conditions For Later Implementation

The later implementation must stop and return to the Project Owner if:

- it would require editing `/Users/foster/state_collapser`;
- it would change `counterpoint_symbolic_v001` environment semantics;
- runtime and metadata selected-edge sets cannot be reconciled;
- nested rate monotonicity fails under the coupled selector;
- source coverage cannot be summarized;
- active action-cell count cannot be distinguished from raw historical records;
- required tables would be omitted without expected-file policy;
- artifact roots would need to leave the repo for durable evaluation output;
- implementation starts turning the diagnostic into a learning comparison;
- a design choice in this blueprint cannot be implemented without weakening or
  changing it.

## Recommended Blueprint Decisions

The following are consultant recommendations, not PO decisions:

1. Use coupled Bernoulli edge-threshold selection as the first noisy-rate
   selector.
2. Keep this as a sibling evaluation with its own readout folder.
3. Include no-contraction control.
4. Do not include deterministic floor-reference arms in the first smoke run.
5. Include deterministic floor-reference arms in full validation only if the
   Project Owner wants direct structural context inside the same artifact set.
6. Use many schema seeds in full validation because selector variance is now
   part of the result.
7. Require metadata/runtime selection consistency as a hard validity check.
8. Put source coverage and zero-selected-source counts near the top of the
   human-readable README.

## Open Turn Questions For Project Owner

The Project Owner slots below remain unanswered unless the Project Owner
actually writes into them. The consultant answer slots are filled with
consultant-authored defaults so a later workplan can proceed if the Project
Owner explicitly accepts defaults or executes without overriding them.

### Question 1: Selector Model

#### Embedded Engineering Consultant / Codex Question

> Do you want the first noisy-rate diagnostic to use coupled Bernoulli
> edge-threshold selection as recommended here, or would you prefer
> source-local binomial selection to preserve more of the current
> source-local shuffled-prefix style?

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> Consultant default answer pending Project Owner confirmation:
>
> Use coupled Bernoulli edge-threshold selection for the first noisy-rate
> diagnostic.
>
> Rationale: this selector directly implements "mean rate" semantics, allows
> many sources to contribute zero scheduled edges, and preserves monotone
> nesting across increasing rates when the same per-edge stable score is reused.
> It also gives the cleanest threshold story: if `p1 <= p2`, then every edge
> selected at `p1` is also selected at `p2`.
>
> Source-local binomial remains a reasonable later variant, especially if we
> want to preserve the shuffled-prefix style more closely. But for the first
> diagnostic, the coupled edge-threshold selector is the cleanest test of
> whether source coverage, not raw selected edge share, drove the `1/18`
> collapse.

### Question 2: Rate Grid

#### Embedded Engineering Consultant / Codex Question

> Is the proposed rate grid `1/288, 1/144, 1/72, 1/36, 1/24, 1/18, 1/12,
> 1/9` the right first full sweep, or should the first version focus more
> tightly around `1/36`?

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> Consultant default answer pending Project Owner confirmation:
>
> Use the proposed full grid:
>
> ```text
> 1/288, 1/144, 1/72, 1/36, 1/24, 1/18, 1/12, 1/9
> ```
>
> Use the smoke grid:
>
> ```text
> 1/144, 1/36, 1/18
> ```
>
> Rationale: the full grid probes well below the source-local `1/18` collapse,
> includes the Project Owner's motivating `1/36` rate, reconnects to `1/18`,
> and includes stronger rates in case all low rates preserve structure. The
> smoke grid is small enough to validate the machinery while still checking
> below, at, and near the observed collapse neighborhood.

### Question 3: Reference Arms

#### Embedded Engineering Consultant / Codex Question

> Should the noisy-rate evaluation include deterministic source-local floor
> reference arms such as `floor_n01_over_18_reference`, or should it stay pure
> and only compare to the previous readout in prose?

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> Consultant default answer pending Project Owner confirmation:
>
> Keep the first noisy-rate implementation pure. Do not include deterministic
> source-local floor reference arms in the artifact set.
>
> Rationale: the first diagnostic should isolate the new selector semantics.
> The previous source-local floor readout already exists and can be linked in
> prose. Adding reference arms now would widen the artifact contract and make it
> easier for the readout to look like a comparison rather than a focused
> diagnostic.
>
> If the first noisy-rate run is hard to interpret without side-by-side floor
> references, add those as a later explicit extension.

### Question 4: Validation Ordering

#### Embedded Engineering Consultant / Codex Question

> Do you want to run the full small+medium validation for the existing
> source-local `n/18` fraction sweep before implementing this noisy-rate
> sibling, or should this noisy-rate diagnostic become the next implementation
> target?

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> Consultant default answer pending Project Owner confirmation:
>
> Make the noisy-rate diagnostic the next implementation target. Do not require
> the existing source-local `n/18` sweep to finish full small+medium validation
> first.
>
> Rationale: the current smoke result already revealed the likely problem with
> the source-local minimum-one floor. Running a full validation of that same
> selector may mostly tell us more about a failure mode we already suspect. The
> noisy-rate diagnostic tests the sharper hypothesis: whether collapse persists
> once many sources are allowed to select zero arrows.
>
> The noisy-rate workplan should still include its own full-validation decision
> lock before expensive artifact generation.

### Question 5: Naming

#### Embedded Engineering Consultant / Codex Question

> Do you prefer the word `noisy_rate`, `bernoulli_rate`, or something else in
> evaluation ids, CLI names, and readout folders?

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> Consultant default answer pending Project Owner confirmation:
>
> Use `noisy_rate` in evaluation ids, CLI names, package names, and readout
> folders.
>
> Rationale: `noisy_rate` leaves room for implementation details such as
> coupled Bernoulli edge-threshold selection while still naming the conceptual
> point of the evaluation: expected-rate stochastic contraction without a
> source-local minimum-one floor. `bernoulli_rate` is more precise for the
> recommended first selector, but too narrow if a later variant compares
> source-local binomial or another random-rate selector.

## Blueprint Readiness

This blueprint is ready for Project Owner review.

It is ready to support a Phase.Stage.Action implementation workplan using the
consultant defaults above, provided the Project Owner explicitly approves
workplan execution and does not override those defaults.
