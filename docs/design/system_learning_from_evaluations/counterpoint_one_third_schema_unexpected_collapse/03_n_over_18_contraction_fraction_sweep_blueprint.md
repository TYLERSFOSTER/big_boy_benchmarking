# Counterpoint n-over-18 Contraction Fraction Sweep Blueprint

Date: 2026-06-01

Status: draft blueprint

Repository:

```text
/Users/foster/big_boy_benchmarking
```

Design folder:

```text
docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/
```

## Status And Authority

This is a design blueprint.

This is not an implementation workplan.

This is not approval to edit source code.

This is not approval to run benchmark artifacts.

This blueprint converts the unexpected one-third collapse archive and the
Project Owner's requested evaluation redesign into a concrete diagnostic
evaluation design. A later Phase.Stage.Action implementation workplan must
translate this blueprint into executable work before code changes begin.

## Source Authority

This blueprint follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`
- `docs/design/system_learning_from_evaluations/README.md`
- `docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/README.md`
- `docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/01_issue_and_next_tests.md`
- `docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/02_readout_conversation_archive.md`
- `docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/README.md`
- read-only inspection of the existing one-third schema implementation in
  `src/big_boy_benchmarking/environments/counterpoint/schemas.py`
- read-only inspection of the existing tower adapter implementation in
  `src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py`
- Project Owner turns in the current chat on 2026-06-01

## PO Attribution Ledger

This section records only Project Owner-originated scope, corrections, and
decisions. Consultant interpretations appear in later sections under explicit
consultant labels.

1. The Project Owner requested a redesign of the evaluation itself, not a
   change to the counterpoint environment.

2. The Project Owner requested replacing the fixed `1/3` contraction diagnostic
   with a sweep over `n/18` for `n = 1, 2, 3, 4, 5, 6`, recording each case.

3. The Project Owner stated the purpose of the sweep: verify whether the system
   looks reasonable at low contraction strengths and then collapses as the
   contraction strength increases.

4. The Project Owner suggested this redesign belongs under the existing
   unexpected one-third collapse archive:

   ```text
   docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/
   ```

5. The Project Owner requested that PO attribution be included in this
   blueprint.

6. From the archived conversation, the Project Owner identified the one-third
   singleton collapse as suspicious diagnostic evidence rather than a negative
   learning result about counterpoint.

7. From the archived conversation, the Project Owner corrected the consultant
   away from loose `pi_0` or connected-components language and toward the
   intended `coset` / Young-tableaux interpretation discussed in
   `state_collapser` documentation.

8. From the archived conversation, the Project Owner emphasized that a true
   counterpoint voice projection can be more semantically severe than a generic
   one-third outgoing schema while still not collapsing to one state cell.

## Consultant Sufficiency Judgement

We have enough discussion to write this blueprint.

We do not yet have enough authority to implement it. Implementation should wait
for a Phase.Stage.Action workplan and an explicit execution request.

The remaining ambiguities are ordinary design details rather than blockers to
blueprint creation. They are recorded under "Open Questions For Project Owner"
near the end of this document.

## Executive Design

The existing one-third diagnostic showed:

```text
small:  108 -> 1 -> 1 -> 1
medium: 228 -> 1 -> 1 -> 1
```

That result is unresolved. It may be caused by the current one-third block
being too wide, by the way BBB represents a source-local outgoing schema as a
global contraction block, by a deeper mismatch with upstream contraction/coset
semantics, or by some combination of those factors.

The next evaluation should therefore stop asking only:

```text
What happens at 1/3?
```

and instead ask:

```text
As the scheduled contraction fraction increases from 1/18 through 6/18,
where does the counterpoint tower first begin to collapse?
```

The new evaluation keeps the existing `counterpoint_symbolic_v001` environment
family and changes only the diagnostic schema family and evaluation surface.

The evaluation is a structural/runtime diagnostic sweep, not a learning
comparison.

## Evaluation Question

Primary question:

```text
For the existing counterpoint hidden graph, how does first-tier quotient shape
change as the source-local scheduled outgoing-edge contraction fraction moves
from 1/18 through 6/18?
```

Secondary questions:

1. Does low contraction strength preserve a meaningful number of state cells?
2. Is there a visible collapse threshold as `n` increases?
3. Does `6/18` reproduce the old one-third first-block behavior?
4. Does tier executability fail only after state collapse, or does it fail
   earlier?
5. Do active action-cell counts, lift attempts, and concrete steps tell the
   same story as the tower-shape summaries?
6. Does the readout provide enough evidence to distinguish "schema too broad"
   from "counterpoint environment degenerate"?

## Non-Goals

This evaluation must not claim:

- direct-vs-tower learning comparison;
- tower advantage or disadvantage;
- musical quality;
- tensor-enabled behavior;
- CUDA or GPU performance;
- production timing;
- a new `state_collapser` semantics result;
- that counterpoint projection intuition is wrong;
- that the counterpoint environment is degenerate;
- that loose `pi_0` or connected-components language is the intended object.

This evaluation must not change:

- the `counterpoint_symbolic_v001` environment definition;
- the base counterpoint state/action enumeration;
- the reward model;
- legal-action masks;
- upstream `state_collapser` code.

## Recommended Evaluation Identity

Recommended evaluation id:

```text
counterpoint_contraction_fraction_sweep_diagnostics_v001
```

Recommended schema family id:

```text
counterpoint_outgoing_fraction_sweep_schema_v001
```

Recommended run mode:

```text
diagnostic_contraction_fraction_sweep_tower_abc
```

Recommended repo-side readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/
```

Recommended artifact root shape:

```text
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/artifacts/<run-label>/
```

Recommended source evaluation root shape:

```text
<artifact-root>/evaluations/counterpoint_contraction_fraction_sweep_diagnostics_v001/
```

Recommended initial run label:

```text
small_medium_validation_001
```

## Relationship To Existing One-Third Evaluation

The existing evaluation remains historical evidence:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/
```

It found the unexpected collapse.

The new sweep is the corrective diagnostic that asks whether collapse emerges
gradually as schema width increases, or whether even tiny fractions collapse
the graph.

The old one-third evaluation should not be overwritten. The new evaluation
should link back to it as motivation.

## Arm Matrix

The required arms are:

| Arm id | Numerator | Denominator | Fraction | Intended meaning |
| --- | ---: | ---: | ---: | --- |
| `n01_over_18` | 1 | 18 | 0.055555... | weakest requested scheduled contraction |
| `n02_over_18` | 2 | 18 | 0.111111... | low scheduled contraction |
| `n03_over_18` | 3 | 18 | 0.166666... | one-sixth scheduled contraction |
| `n04_over_18` | 4 | 18 | 0.222222... | moderate scheduled contraction |
| `n05_over_18` | 5 | 18 | 0.277777... | near one-third scheduled contraction |
| `n06_over_18` | 6 | 18 | 0.333333... | should match the old first one-third block if quota rules align |

Recommended internal control arm:

| Arm id | Purpose |
| --- | --- |
| `no_contraction_control` | verify the environment/tower builder preserves the base graph when no contraction is scheduled |

The control arm is not a learning comparison. It is a structural sanity check.

## Consultant Interpretation Of `n/18`

Consultant interpretation:

`n/18` should mean one scheduled source-local outgoing-edge contraction block
whose per-source quota is approximately `n/18` of that source state's outgoing
edge set.

This should be a single first-projection diagnostic, not an 18-tier recursive
schedule.

Reason:

The PO's stated purpose is to check whether low contraction strengths look
reasonable and then collapse as contraction strength increases. That is a
threshold sweep over contraction width. A single scheduled block per arm gives
the cleanest threshold surface.

Assumption pending Project Owner confirmation:

The tower for an `n/18` arm should have two conceptual tiers:

```text
tier 0: base hidden graph
tier 1: result after scheduled n/18 endpoint coalescence
```

If implementation keeps extra diagnostic tiers for adapter compatibility, the
readout must still make clear that the primary evidence is the first scheduled
projection.

## Schema Construction Rule

For each arm and schema seed:

1. Enumerate the same base graph used by the current counterpoint environment.
2. Group outgoing edges by source state.
3. For each source state, sort outgoing edge ids by stable identity.
4. Shuffle that source-local list with a deterministic seed derived from:

   ```text
   schema_seed, source_state_id
   ```

5. Compute the scheduled quota:

   ```text
   quota(source, n) = max(1, ceil(out_degree(source) * n / 18))
   ```

   for sources with at least one outgoing edge.

6. Assign the first `quota(source, n)` shuffled outgoing edges to the arm's
   scheduled contraction block.

7. Leave remaining outgoing edges unscheduled for this diagnostic arm.

8. Build the `state_collapser` `PartitionTower` using the scheduled block.

This rule is chosen so that `n = 6` gives:

```text
max(1, ceil(out_degree(source) * 6 / 18))
= max(1, ceil(out_degree(source) / 3))
```

That should match the first block of the existing recursive one-third schema,
which uses:

```text
max(1, ceil(len(remaining) / 3))
```

for the first scheduled block.

The implementation must verify this equivalence explicitly rather than assume
it.

## Monotonicity Requirement

For a fixed instance and schema seed, the selected edge set for `n/18` should
be a subset of the selected edge set for `(n+1)/18`.

This gives the readout a clean interpretation:

```text
more scheduled contraction fraction -> superset of scheduled endpoint
coalescences -> equal or coarser first-tier partition under current semantics
```

If monotonicity fails, the evaluation should be considered invalid until the
schema construction is corrected or the non-monotonic rule is explicitly
approved.

## Required Metrics

The new evaluation must promote these metrics into evaluation-level tables.
They must not exist only inside per-run raw files.

### Schema Width Metrics

Per instance, arm, schema seed, and source summary:

- numerator;
- denominator;
- requested fraction;
- base state count;
- base edge count;
- scheduled edge count;
- scheduled edge share;
- scheduled edge count divided by `base_state_count - 1`;
- source count with scheduled edges;
- min/mean/max selected edges per source;
- min/mean/max source out-degree;
- quota rule id;
- monotonicity check result.

### First-Tier Shape Metrics

Per instance, arm, schema seed, replicate:

- tier count;
- tier index;
- state-cell count;
- active action-cell count;
- raw historical action-cell record count, if retained;
- largest state-cell size;
- largest state-cell share;
- singleton state-cell count;
- singleton base-state share;
- coset-size histogram or equivalent state-cell member-count histogram;
- full-collapse flag;
- near-collapse flag;
- first singleton-collapse tier, if any.

### Endpoint-Coalescence Diagnostics

Use language discipline here.

The readout should not say that the system performs a separate `pi_0` or
connected-components operation.

Instead, report the result of applying the same repeated endpoint-coalescence
rule to the scheduled block:

- number of state cells after scheduled endpoint coalescence;
- largest coalesced cell size;
- useful coalescence count;
- redundant/internal edge count;
- processed-edge index at first singleton state cell, if singleton collapse
  occurs;
- whether collapse required most of the block or only a few early edges.

Recommended table name:

```text
results/endpoint_coalescence_summary.csv
```

### Active Runtime Metrics

Per instance, arm, schema seed, replicate, tier:

- active ABC event count;
- selected tier count;
- exploit event count;
- explore event count;
- train event count;
- lift attempt count;
- lift success count;
- lift failure count;
- concrete step count;
- episode count;
- terminal count;
- timeout count.

### Collapse Threshold Metrics

Across the arm sweep:

- first `n` with full first-tier singleton collapse;
- first `n` with near-collapse;
- last `n` with nontrivial state structure;
- whether `n = 6` matches old one-third first-block state shape;
- whether collapse behavior is stable across schema seeds;
- whether collapse behavior is stable across small and medium instances.

Recommended table name:

```text
results/collapse_threshold_summary.csv
```

## Required Readout Shape

The generated human-readable README should open with a sweep verdict, not with
one arm's result.

The first screen should answer:

```text
Did the sweep find a threshold?
At which n did collapse begin?
Did lower n values preserve nontrivial structure?
Does 6/18 reproduce the old one-third collapse?
```

Recommended top-level badges:

- `Artifacts: Complete | Incomplete`
- `Sweep: Threshold Found | Immediate Collapse | No Collapse | Mixed`
- `n=6/18: Matches Legacy | Differs From Legacy | Not Checked`
- `Runtime: Executable | Base-Tier Only | Lift Blocked | Mixed`
- `Scope: Diagnostic Only`
- `Provenance: Repo Artifacts`

The readout must include at least these human-facing tables:

1. Sweep verdict by instance.
2. Tierwise state-cell counts by `n/18`.
3. Active action-cell counts by `n/18`.
4. Scheduled block width by `n/18`.
5. Endpoint-coalescence summary by `n/18`.
6. Active tier occupancy by `n/18`.
7. Lift/executability by `n/18`.
8. Legacy `1/3` equivalence check for `6/18`.

The readout must preserve the claim boundary that this is diagnostic-only.

## Expected Artifact Contract

The evaluation should produce:

```text
evaluation_manifest.json
evaluation_arm_manifest.json
evaluation_budget_lock.json
evaluation_run_index.csv
evaluation_aggregate_table.csv
evaluation_aggregate_summary.json
readout_source.json
```

Required result tables:

```text
results/schema_fraction_summary.csv
results/tower_shape_summary.csv
results/endpoint_coalescence_summary.csv
results/tier_executability_summary.csv
results/tier_occupancy_summary.csv
results/control_action_summary.csv
results/abc_selection_summary.csv
results/abc_tier_signal_summary.csv
results/lift_failure_by_tier.csv
results/concrete_step_summary.csv
results/collapse_threshold_summary.csv
results/legacy_one_third_equivalence_summary.csv
```

Recommended docs seed files:

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

Per-run artifacts should still include raw control, ABC, lift, quotient, and
step evidence so the evaluation-level summaries remain auditable.

## Source Binding Requirements

The `readout_source.json` must point to the repo-side readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/readout_source.json
```

It must include:

- source artifact root;
- source evaluation root;
- evaluation id;
- run mode;
- expected files;
- goal criteria;
- structural limit checks;
- badge policy;
- goal summary sources;
- methodology summary sources;
- claim boundary;
- link back to this blueprint;
- link back to the unexpected one-third collapse archive.

The human-readability command must use the protocol file and the checked-in
source binding:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/readout_source.json
```

## Goal Criteria

### Goal 1: Sweep Artifacts Complete

Question:

```text
Did every requested arm produce the required evaluation-level artifacts?
```

Success signal:

- every requested `n/18` arm is represented;
- required manifests and result tables exist;
- source binding parses;
- artifact paths are repo-resident.

Claim if met:

```text
The contraction-fraction sweep completed its artifact contract.
```

### Goal 2: Threshold Visibility

Question:

```text
Does the sweep reveal whether collapse emerges gradually or immediately?
```

Success signal:

- collapse status exists for every `n`;
- first full-collapse `n`, if any, is reported;
- last nontrivial `n`, if any, is reported;
- mixed seed/instance behavior is explicitly classified.

Claim if met:

```text
The evaluation identifies the observed first-tier collapse threshold under
the current BBB/state_collapser schema semantics.
```

### Goal 3: Legacy One-Third Check

Question:

```text
Does 6/18 reproduce the old one-third first-block behavior?
```

Success signal:

- selected-edge equivalence is checked against the existing one-third first
  block for the same instance and schema seed;
- tower-shape equivalence is checked;
- any mismatch is reported as an evaluation-design issue.

Claim if met:

```text
The sweep's 6/18 endpoint is comparable to the prior one-third diagnostic.
```

### Goal 4: Active Surface Readability

Question:

```text
Can a human tell whether each tier is actually executable?
```

Success signal:

- active action-cell counts are reported separately from raw historical action
  cell records;
- active tier occupancy is reported;
- lift failures are summarized by tier and reason.

Claim if met:

```text
The evaluation distinguishes constructed quotient shape from live executable
control surface.
```

## Structural Limit Classifications

The readout should classify each arm into one of these statuses:

| Status | Meaning |
| --- | --- |
| `nontrivial` | first scheduled tier retains more than one state cell and is not near-collapse |
| `near_collapse` | first scheduled tier retains more than one state cell, but largest cell share crosses the near-collapse threshold |
| `full_collapse` | first scheduled tier has one state cell |
| `mixed_by_seed` | seeds disagree on collapse class |
| `mixed_by_instance` | instances disagree on collapse class |
| `invalid_or_uninterpretable` | required evidence is missing or schema monotonicity/equivalence checks fail |

Assumption pending Project Owner confirmation:

Near-collapse should initially mean largest first-tier state cell share is at
least `0.90`.

This is a consultant default from existing protocol language, not a PO-authored
threshold.

## Interpretation Guide

The evaluation should be read as follows:

### Case A: Low n Looks Good, High n Collapses

This is the hoped-for calibration result.

Interpretation:

```text
The old 1/3 result was likely too broad for the intended diagnostic. A smaller
fraction may provide an inspectable tower surface.
```

Next likely work:

- choose a smaller diagnostic fraction;
- design a more serious structural/control evaluation around the stable range;
- compare against actual counterpoint voice projections later.

### Case B: n = 1 Already Collapses

This is a severe diagnostic result.

Interpretation:

```text
Even a one-edge-per-source-style fraction may be enough to collapse the graph
under current endpoint-coalescence semantics.
```

Next likely work:

- run fixed-edge-count diagnostics;
- test one selected edge globally;
- test one source-star;
- test tiny synthetic graphs;
- revisit whether this schema API is the wrong surface for local outgoing
  grouping.

### Case C: Nothing Collapses Through 6/18

This is a contradiction against the old one-third result unless `6/18` is not
equivalent to the old first block.

Interpretation:

```text
Either the new sweep does not reproduce the old schema endpoint, or the old
result depended on recursive/block-order details not captured by this sweep.
```

Next likely work:

- inspect the legacy equivalence table;
- compare selected edge sets;
- compare ordered blocks;
- compare tower construction logs.

### Case D: Non-Monotonic Result

This should be treated as an evaluation-design problem until proven otherwise.

Interpretation:

```text
The schema construction probably is not producing nested contraction arms, so
the sweep is not a clean threshold experiment.
```

Next likely work:

- fix quota or shuffling;
- re-run;
- only interpret monotone sweep results.

## Required Tests

### Schema Tests

- `n = 6` selects the same source-local edge set as the first block of the
  existing one-third schema for the same instance and schema seed.
- For fixed instance and schema seed, `n` selected edge sets are nested.
- Each source with outgoing edges contributes `max(1, ceil(out_degree * n / 18))`
  selected edges.
- Remaining edges are unscheduled for the single-block sweep arm.
- Schema ids and arm ids are stable and parseable.

### Artifact Tests

- `readout_source.json` is generated under the repo-side readout surface.
- Required result tables exist after summarization.
- `goal_summary_sources` includes this blueprint.
- `methodology_summary_sources` includes this blueprint and runbook/method docs.
- Expected-file policy distinguishes required, conditional, and not-applicable
  files.
- Artifact root remains under the repo readout surface.

### Readout Tests

- Generated README includes a sweep verdict.
- Generated README includes the exact protocol command targeting
  `readout_source.json`.
- Generated README does not claim learning performance.
- Generated README distinguishes active action-cell counts from raw historical
  action-cell records.
- Generated README includes the protected clarifying-turn surface required by
  the readout protocol.

### Regression Tests

- Existing one-third diagnostics commands and tests continue to pass unless
  explicitly deprecated by a later PO decision.
- Existing first serious learning evaluation commands and tests continue to
  pass.
- Existing counterpoint environment enumeration remains unchanged.

## Implementation Strategy Recommendation

Consultant recommendation:

Do not mutate the existing one-third diagnostics module in place.

Instead:

1. Extract shared schema/tower diagnostic helpers where the one-third code is
   clearly reusable.
2. Add a new fraction-sweep diagnostics module with its own ids, config,
   paths, manifests, docs writer, aggregation, and runner.
3. Keep the old one-third evaluation import paths and CLI commands intact.
4. Add a new CLI surface for the sweep.
5. Add equivalence tests proving the `6/18` arm is comparable to the old first
   one-third block.

Suggested CLI shape:

```text
uv run python -m big_boy_benchmarking.cli counterpoint fraction-sweep run \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/artifacts/small_medium_validation_001 \
  --instances small,medium \
  --numerators 1,2,3,4,5,6 \
  --denominator 18 \
  --schema-seeds 0,1,2 \
  --replicates 4 \
  --episodes 16 \
  --linearization-mode tensor_available_disabled

uv run python -m big_boy_benchmarking.cli counterpoint fraction-sweep summarize \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/artifacts/small_medium_validation_001
```

The exact CLI names should be finalized in the implementation workplan.

## Budget Recommendation

Consultant recommendation:

Use the same initial fixture and budget shape as the one-third diagnostic:

- instances: small and medium;
- schema seeds: `0,1,2`;
- replicates: `4`;
- episodes per replicate: `16`;
- linearization mode: `tensor_available_disabled`;
- horizon: existing instance-specific horizon;
- artifact root: repo-resident under the evaluation readout surface.

Reason:

This makes the sweep comparable to the old one-third result and keeps the
diagnostic grounded in already-understood artifact conventions.

Risk:

The sweep multiplies the number of arms by six. If runtime is too heavy, the
workplan can define a smoke subset first, but the full evidence run should use
small+medium if feasible.

## Open Questions For Project Owner

These are consultant-authored open questions, not Project Owner statements.

### Question 1: Single-Block Semantics

Should each `n/18` arm be exactly one scheduled first-tier contraction block,
with all remaining outgoing edges unscheduled?

Consultant recommendation:

Yes. This best matches the threshold question.

### Question 2: No-Contraction Control

Should the sweep include a no-contraction structural control arm in the same
artifact set?

Consultant recommendation:

Yes, as a sanity check only. It should not be presented as a learning
comparison.

### Question 3: Run Budget

Should the first full run reuse the one-third diagnostic budget across small
and medium, or should it start with a smaller smoke/calibration run?

Consultant recommendation:

Write the implementation to support both, run smoke first, then run the full
small+medium validation once smoke passes.

### Question 4: Near-Collapse Threshold

Is `largest first-tier state cell share >= 0.90` acceptable as the initial
near-collapse threshold?

Consultant recommendation:

Yes for the first readout, as long as the raw cell-size distributions are also
reported.

### Question 5: Legacy One-Third Comparison

Should the readout compare `6/18` only to the old first scheduled one-third
block, or also to the entire old recursive three-block tower?

Consultant recommendation:

The primary comparison should be first-block equivalence. The full old tower
can be cited as historical context, but the collapse happened at tier `1`, so
first-block equivalence is the decisive check.

## Stop Conditions For Future Implementation

Stop and return to design if:

- `6/18` cannot be made equivalent to the old first one-third block under a
  stable quota rule;
- selected edge sets are not nested across `n`;
- the readout cannot distinguish active action cells from stale historical
  action-cell records;
- the evaluation would require changing the counterpoint environment;
- the evaluation would require changing upstream `state_collapser`;
- generated artifacts would need to live outside the repo readout surface;
- implementation pressure starts turning this diagnostic into a learning
  comparison.

## Blueprint Completion Criteria

This blueprint is complete enough to generate a Phase.Stage.Action workplan
when the Project Owner requests one.

The workplan should:

- preserve this PO attribution ledger;
- treat open questions as explicit decision locks or assumptions;
- create a branch before implementation if source edits are requested;
- implement the new evaluation without deleting the historical one-third
  diagnostic;
- verify schema equivalence, monotonicity, artifact contracts, and readout
  generation before reporting completion.

