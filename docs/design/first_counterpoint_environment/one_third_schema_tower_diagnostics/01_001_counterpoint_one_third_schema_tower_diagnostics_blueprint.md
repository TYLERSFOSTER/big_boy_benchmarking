# Counterpoint One-Third Schema Tower Diagnostics Blueprint

Date: 2026-05-31

Status: draft blueprint

Repository:

```text
/Users/foster/big_boy_benchmarking
```

Design folder:

```text
docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/
```

## Status And Authority

This is a design blueprint.

This is not an implementation gameplan.

This is not approval to edit source code.

This is not approval to run benchmark artifacts.

This blueprint converts the design discussion in:

```text
docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/design_discussion.md
```

into a detailed benchmark-evaluation design for a one-third contraction schema
diagnostic on the existing counterpoint environment family.

A later Phase.Stage.Action implementation gameplan must translate this
blueprint into executable work before code changes begin.

## Source Authority

This blueprint follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md`
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`
- `docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/design_discussion.md`
- `docs/design/first_counterpoint_environment/01_002_counterpoint_hidden_graph_and_contraction_schema_benchmark_blueprint.md`
- `docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_001_counterpoint_first_serious_learning_evaluation_blueprint.md`
- `docs/environments/counterpoint_symbolic_v001.md`
- `docs/design/system_learning_from_evaluations/README.md`
- read-only inspection of current BBB counterpoint source surfaces
- read-only inspection of current `state_collapser` ABC and partition-tower
  source surfaces

Important current BBB source surfaces:

```text
src/big_boy_benchmarking/environments/counterpoint/ids.py
src/big_boy_benchmarking/environments/counterpoint/schemas.py
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
src/big_boy_benchmarking/environments/counterpoint/diagnostics.py
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
src/big_boy_benchmarking/environments/counterpoint/serious_learning/events.py
```

Important current `state_collapser` source surfaces:

```text
/Users/foster/state_collapser/src/state_collapser/tower/control/controller.py
/Users/foster/state_collapser/src/state_collapser/tower/control/signals.py
/Users/foster/state_collapser/src/state_collapser/tower/runtime.py
/Users/foster/state_collapser/src/state_collapser/tower/partition/schema.py
/Users/foster/state_collapser/src/state_collapser/tower/partition/base_registry.py
```

Important current `state_collapser` design surfaces:

```text
/Users/foster/state_collapser/docs/design/HRL_exploit-explore/01_015_abc_find_unclosed_correction.md
/Users/foster/state_collapser/docs/design/HRL_exploit-explore/01_016_find_lowest_unclosed_system_change_blueprint.md
/Users/foster/state_collapser/docs/engineer_continuity/2026/05/18/01_008_control_corrections_tower_ownership_and_release_readiness.md
```

## Prime Directive Alignment

The Project Owner has corrected the design direction for this block.

This blueprint must preserve those corrections:

- this is an evaluation on the existing `counterpoint_symbolic_v001`
  environment family;
- this is not a new environment;
- this is not a direct-vs-tower performance comparison;
- this is not approval to alter `state_collapser`;
- this is not a request to rewrite ABC control logic in BBB;
- the existing upstream `state_collapser` ABC runtime is the thing under
  observation;
- BBB's job is to build the one-third contraction schema, run the upstream
  control surface against it, and produce interpretable artifacts;
- any remaining ambiguity should be recorded as explicit PO turn questions,
  not silently resolved by implementation drift.

This blueprint therefore uses the following control hierarchy:

```text
Project Owner design intent
-> current BBB environment and artifact protocols
-> upstream state_collapser control semantics
-> local instrumentation and readout surfaces
```

## Executive Design

This evaluation asks:

```text
For counterpoint_symbolic_v001, what tower geometry is produced by a
one-third contraction schema, and how does the existing upstream
state_collapser ABC controller occupy and move through that tower during
training/control events?
```

The evaluation has two linked evidence layers:

1. **Tower geometry diagnostics**

   These answer what quotient tower the one-third contraction schema creates:
   tier count, state-cell counts, action-cell counts, fiber sizes, contraction
   block balance, first-projection collapse, lift/action availability, and
   degenerate-tier structure.

2. **ABC occupancy diagnostics**

   These answer what the upstream `state_collapser` active-tier controller does
   when run against that tower: active tier before/after each control event,
   selected lowest executable unclosed tier, per-tier productive-learning
   pressure, per-tier executability, controller action, lift/action realization,
   and whether observed tier movement matches upstream ABC semantics.

The evaluation does not ask whether this schema improves reward learning.

The evaluation does not compare against direct environment training.

The evaluation may decide that the one-third schema is structurally promising,
structurally pathological, runtime-blocked, or not yet interpretable. It may
not make a "tower beats direct" claim.

## Evaluation Identity

Recommended evaluation id:

```text
counterpoint_one_third_schema_tower_diagnostics_v001
```

Environment family id:

```text
counterpoint_symbolic_v001
```

Recommended schema family id:

```text
counterpoint_one_third_schema_v001
```

Recommended primary schema id, if the PO accepts the per-source outgoing-edge
thirds interpretation:

```text
counterpoint_one_third_outgoing_schema_v001
```

Recommended repo-side readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/
```

Recommended artifact root shape:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/<run-label>/
```

Recommended source evaluation root shape:

```text
<artifact-root>/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001/
```

Recommended run label examples:

```text
one_third_schema_diagnostics_001
one_third_schema_diagnostics_small_001
one_third_schema_diagnostics_smoke_001
```

The implementation gameplan should choose final names once the PO answers the
schema-rule and run-scope questions at the bottom of this document.

## Settled Decisions

### Decision 1: Existing Environment Only

The environment is:

```text
counterpoint_symbolic_v001
```

The evaluation must not create a new environment family.

It may add a new schema and a new evaluation surface inside the existing
counterpoint family.

### Decision 2: Diagnostic Evaluation, Not Comparison Benchmark

This evaluation is not the next version of:

```text
first_serious_learning
```

It is a narrower diagnostic block focused on one schema and one runtime-control
question.

The first serious learning evaluation already exists as the first direct/tower
learning comparison surface. This evaluation sits beside it and asks a more
local question:

```text
Does this one-third schema produce an inspectable tower, and does upstream ABC
control occupy it in an interpretable way?
```

### Decision 3: Use Upstream ABC Control

BBB must not reimplement ABC logic.

The control surfaces under observation are upstream:

```text
state_collapser.tower.control.ActiveTierController
state_collapser.tower.control.select_lowest_unclosed_tier
state_collapser.tower.control.productive_learning_pressure
state_collapser.tower.control.is_unclosed
state_collapser.tower.control.should_descend
state_collapser.tower.control.should_lift
state_collapser.tower.runtime.ExploitExploreTowerRuntime
```

BBB may instrument these surfaces by calling upstream helper functions on the
same inputs that are passed to the upstream controller.

BBB may not fork, copy, rewrite, or semantically replace these surfaces inside
this evaluation.

### Decision 4: BBB Owns Schema And Artifact Instrumentation

BBB is allowed to own:

- counterpoint schema ids;
- counterpoint-specific contraction-schema construction;
- the counterpoint `tier_is_executable` predicate;
- diagnostic wrappers around upstream controller calls;
- event rows and aggregate tables;
- repo-side human-readable evaluation readouts.

This is not a violation of "do not rewrite ABC." The schema and instrumentation
are benchmark-local surfaces. The controller policy remains upstream.

### Decision 5: Human-Readable Readout Is Part Of Construction

This evaluation is not construction-complete unless it satisfies:

```text
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
```

In particular, it must produce enough machine-readable evidence for:

```text
execute artifact-table readout pointed at folder <repo-readout-surface>
```

to generate a truthful human-readable readout without reverse-engineering the
evaluation from raw per-run files.

## Non-Goals

This blueprint does not authorize:

- editing `/Users/foster/state_collapser`;
- rewriting upstream ABC control;
- implementing a new controller in BBB;
- making a direct-vs-tower performance comparison;
- comparing one-third against motion, random, bad, or empty schemas as result
  arms;
- claiming reward improvement;
- claiming musical quality;
- claiming general `state_collapser` quality;
- claiming tensor-enabled, CUDA, or GPU performance;
- treating `tiny` as serious result evidence;
- using reward outcomes, terminal outcomes, learned values, or future episode
  information to construct the online-eligible schema;
- hiding structural collapse behind generic "mixed" language;
- writing human-readable reports only into raw artifact folders.

## Current Reality Check

### Upstream ABC Reality

Current `state_collapser` implements ABC-style control with:

```text
select_lowest_unclosed_tier(...)
should_descend(...)
should_lift(...)
ActiveTierController.decide(...)
ExploitExploreTowerRuntime.step(...)
```

The key semantics are:

- scan for the lowest, highest-indexed, currently unclosed tier;
- skip non-executable tiers when a `tier_is_executable` predicate is supplied;
- descend when the selected lowest unclosed tier is deeper than the active tier;
- lift when the selected lowest unclosed tier is above the active tier;
- train, explore, or exploit at the selected active locus when no tier movement
  is indicated;
- lift out of a non-executable active tier before action choice;
- return `NO_AVAILABLE_ACTION` if no executable tier exists.

This logic is tested upstream in `state_collapser` tests.

### BBB Counterpoint Runtime Reality

Current BBB already uses upstream runtime/control for counterpoint tower arms in:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
```

The current binding constructs:

```text
ExploitExploreTowerRuntime(
    controller=TimedActiveTierController(...),
    tier_is_executable=adapter.tier_is_executable,
    ...
)
```

and `TimedActiveTierController` delegates to upstream:

```text
ActiveTierController()
```

This is the correct architectural direction.

### BBB Current Instrumentation Gap

Current BBB already records:

- `control_events.csv`;
- active tier before and after;
- control action;
- learner update success and TD-error fields where available;
- `lift_fiber_events.csv`;
- per-run `quotient_summary.json`;
- timing surfaces;
- linearization manifests;
- run manifests.

For this evaluation, that is not enough.

The evaluation must record the controller's ABC context, not just its action.
Without that context, a human reader can see that the controller descended or
lifted, but cannot tell why that movement was correct or blocked under upstream
ABC semantics.

## Claim Boundary

### Claims This Evaluation May Support

If the artifacts are complete, this evaluation may support claims like:

- the one-third schema produced a tower with a specific tier shape on a named
  counterpoint fixture;
- the first projection did or did not collapse most reachable concrete states;
- lift/action availability was or was not present at specific tiers;
- the upstream ABC controller selected and occupied tiers in a way consistent
  with its own lowest-executable-unclosed semantics;
- observed tier movement was blocked by executability, lift/action failure, or
  structural collapse;
- the schema is or is not worth promoting into a later comparative learning
  evaluation.

### Claims This Evaluation Must Not Support

This evaluation must not support claims like:

- one-third schema improves reward learning over direct training;
- one-third schema beats structured motion, random, empty, or bad schemas;
- `state_collapser` generally solves counterpoint;
- the result proves musical quality;
- the result proves general HRL superiority;
- the result proves tensorization or GPU performance;
- zero or low reward means controller failure without checking tower shape,
  executability, and lift/action realization.

## Core Evaluation Questions

### Question 1: What Tower Does One-Third Contraction Produce?

The evaluation must report:

- tier count;
- state-cell count by tier;
- action-cell count by tier;
- edge/action-cell count by tier if available;
- state compression ratio by tier;
- action compression ratio by tier;
- largest state-cell fiber count and share by tier;
- largest action-cell fiber count and share by tier;
- singleton-cell share by tier;
- effective number of cells by tier;
- entropy of cell distributions where useful;
- scheduled edge count by contraction block;
- contraction block balance;
- whether tier `1` is a full or near-full first-projection collapse;
- whether any deeper tiers are degenerate;
- whether each tier has outgoing action cells from representative current
  states.

### Question 2: Does Runtime Occupy The Tower Under Upstream ABC Semantics?

The evaluation must report:

- active tier before and after each controller event;
- selected lowest executable unclosed tier at each controller event;
- per-tier productive-learning pressure at each controller event;
- per-tier unclosed/closed status at each controller event;
- per-tier executable/non-executable status at each controller event;
- controller action;
- training-due status;
- whether movement was toward the selected tier;
- whether non-movement was expected because the active tier already matched the
  selected tier;
- whether lift occurred because selected lowest-unclosed tier moved upward;
- whether descent was blocked by non-executability;
- whether action execution produced a concrete environment step.

### Question 3: Are Lift And Executability Blocking The Runtime?

The evaluation must report:

- `NO_AVAILABLE_ACTION` counts;
- tier-level executable status;
- lift candidate counts;
- lift success counts;
- lift failure counts;
- lift failure reasons;
- abstract action cells that repeatedly fail to realize concrete actions;
- whether the base tier remains executable even if coarser tiers are not;
- whether controller movement is explainable by executability rather than
  reward-learning behavior.

### Question 4: Is The Result Human-Readable?

The evaluation must produce repo-side human docs and source bindings that let a
future Embedded Engineering Consultant generate readable reports through:

```text
execute artifact-table readout pointed at folder docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics
```

The readout must explain:

- what the schema is;
- what the tower looked like;
- what ABC control did;
- why active-tier occupancy matters;
- where the raw evidence lives;
- what was expected but absent;
- what claims are allowed;
- what claims are blocked.

## One-Third Schema Design

### Conceptual Requirement

The schema must assign eligible base edges to three ordered contraction blocks:

```text
block 0 -> creates tier 1
block 1 -> creates tier 2
block 2 -> creates tier 3
```

This matches the upstream `ContractionSchema` contract:

```text
assign_edge(edge_id, registry) -> SchemaBlockId | None
ordered_blocks() -> tuple[SchemaBlockId, ...]
```

Edges assigned to earlier blocks create coarser tiers earlier. Returning
`None` leaves an edge unscheduled for contraction.

### Current Upstream Option: Seeded Random Rate

Current upstream `state_collapser` already exposes:

```text
SeededRandomRateSchema(seed=<seed>, block_count=3)
```

This assigns each edge to one of three deterministic pseudo-random blocks using
the edge id and seed.

Advantages:

- no new schema class required upstream;
- already satisfies the upstream `ContractionSchema` protocol;
- already tested upstream;
- simple to add as a BBB schema id;
- clearly avoids rewriting ABC.

Limitations:

- it is edge-global rather than source-local;
- it does not guarantee each source state contributes roughly one third of its
  outgoing edges to each block;
- a source with few outgoing edges can be unevenly represented across blocks;
- it may be less faithful to the PO's local-action-surface intuition.

### Recommended BBB Option: Per-Source Outgoing Thirds

The current best design recommendation, subject to PO approval, is a BBB-owned
counterpoint schema that still satisfies the upstream `ContractionSchema`
protocol:

```text
CounterpointOutgoingThirdsSchema
```

This schema would:

- use the upstream `BaseGraphRegistry`;
- inspect the source state id for each edge through `registry.source_state_id`;
- inspect outgoing edge ids for that source through `registry.outgoing_edge_ids`;
- sort or seeded-shuffle each source's outgoing edge ids under a stable rule;
- assign each edge to one of three block ids based on its index within its own
  source-local outgoing list;
- return ordered blocks:

```text
SchemaBlockId(("counterpoint_one_third", 0))
SchemaBlockId(("counterpoint_one_third", 1))
SchemaBlockId(("counterpoint_one_third", 2))
```

The point is:

```text
Each local action surface contributes approximately one third of its currently
known outgoing edges to each contraction block.
```

This is a schema policy, not ABC control logic.

### Deterministic Versus Seeded Per-Source Thirds

The per-source rule still has one real ambiguity.

Option A: deterministic ordered thirds

```text
For each source, sort outgoing edges by stable key and assign edge index mod 3.
```

Advantages:

- maximally reproducible without schema seeds;
- easiest to reason about;
- simplest artifact story.

Risks:

- stable key ordering may encode arbitrary lexical structure;
- repeated deterministic ordering could accidentally privilege some action
  classes.

Option B: seeded per-source thirds

```text
For each source, seeded-shuffle outgoing edges using schema_seed and source id,
then assign edge index mod 3.
```

Advantages:

- reduces lexical-order artifact risk;
- allows several schema seeds as a diagnostic suite;
- still preserves source-local balance.

Risks:

- requires schema seeds and seed artifacts;
- a single seed should not be overread;
- human readout must explain seed variability.

Option C: upstream seeded random thirds

```text
Use SeededRandomRateSchema(seed=schema_seed, block_count=3).
```

Advantages:

- minimal local code;
- uses an upstream schema implementation.

Risks:

- tests a global random-thirds schema, not necessarily the PO's intended
  source-local one-third runtime intuition.

### Blueprint Recommendation

Unless the PO corrects this, the later gameplan should implement:

```text
seeded per-source outgoing thirds
```

as a BBB-owned counterpoint schema, while optionally retaining upstream
`SeededRandomRateSchema(block_count=3)` as an internal sanity-check or future
comparison candidate.

The result arm for this evaluation should remain one schema family:

```text
counterpoint_one_third_schema_v001
```

No comparison against random, motion, empty, or bad schemas belongs in this
evaluation unless the PO explicitly changes scope.

## Fixture Scope

### Smoke Fixture

Smoke fixture:

```text
counterpoint_symbolic_n3_tiny_v001
```

Allowed uses:

- fast command validation;
- artifact-contract validation;
- readout generation sanity checks;
- verifying that diagnostic tables are nonempty and joinable.

Disallowed uses:

- serious schema-quality claims;
- meaningful occupancy interpretation;
- promotion of one-third schema.

### Main Diagnostic Fixture

Recommended main fixture:

```text
counterpoint_symbolic_n3_small_v001
```

Allowed uses:

- primary tower-geometry diagnostics;
- primary ABC occupancy diagnostics;
- structural-limit classification;
- deciding whether the schema deserves later comparative learning evaluation.

Disallowed uses:

- general performance claims;
- direct-vs-tower claims;
- musical-quality claims.

## Runtime Design

### Runtime Class

The evaluation should run upstream:

```text
state_collapser.tower.runtime.ExploitExploreTowerRuntime
```

via the existing BBB counterpoint binding pattern.

The runtime must use upstream:

```text
state_collapser.tower.control.ActiveTierController
```

### Instrumentation Wrapper

BBB may extend or replace the current `TimedActiveTierController` wrapper with
a diagnostic wrapper that:

1. receives the same inputs that will be passed to upstream
   `ActiveTierController.decide(...)`;
2. computes a diagnostic snapshot by calling upstream helper functions;
3. delegates to upstream `ActiveTierController.decide(...)`;
4. records the upstream decision and diagnostic snapshot;
5. does not alter the decision.

The wrapper must not select the action itself.

The wrapper must not fork the controller.

The wrapper must not use copied controller logic as the source of truth.

### Required Upstream Helper Calls

The diagnostic wrapper should call, where available:

```text
productive_learning_pressure(signal, config)
is_unclosed(signal, config)
select_lowest_unclosed_tier(
    deepest_known_tier,
    signals_by_tier,
    tier_configs,
    tier_is_executable=tier_is_executable,
)
should_descend(active_tier, selected_lowest_unclosed_tier)
should_lift(active_tier, selected_lowest_unclosed_tier)
```

The wrapper should compute per-tier signal rows by iterating over known tier
indices and using the same `signals_by_tier`, `tier_configs`, and
`tier_is_executable` inputs that the controller sees.

### Training Surface

This evaluation may reuse the current counterpoint tower-control learner
binding from the first serious learning surface:

```text
CounterpointTierLearner
CounterpointLiftResolveExecutor
CounterpointTowerControlAdapter
```

The evaluation should not redesign the learner.

The learner is not the experimental object here. It exists to drive control
events and produce tier-signal state so ABC occupancy can be observed.

### Budget Interpretation

Budget in this evaluation is a diagnostic observation budget, not a performance
budget.

The run should be long enough to produce:

- multiple controller decisions;
- some train/explore/exploit events;
- enough signal changes for closure/unclosed status to vary if the schema
  permits it;
- enough lift/action realization attempts to reveal blocked tiers.

The run should not be described as sufficient to evaluate learning superiority.

## Artifact Contract

This evaluation must satisfy the evaluation construction protocol.

### Repo-Side Readout Surface

Recommended:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/
```

This is the target folder for the human-readout protocol.

It is not the raw artifact root.

### Source Binding

The repo-side readout surface must contain:

```text
readout_source.json
```

It must bind:

- repo readout surface;
- source artifact root;
- source evaluation root;
- evaluation id;
- environment instance id;
- artifact run label;
- run mode;
- artifact schema version;
- aggregate table paths;
- run index paths;
- expected-file policy;
- goal criteria;
- badge policy;
- methodology sources;
- claim boundary.

### Evaluation-Level Manifests

Required evaluation-level files:

```text
evaluation_manifest.json
evaluation_run_index.csv
evaluation_budget_lock.json
evaluation_aggregate_summary.json
evaluation_aggregate_table.csv
readout_source.json
```

If this evaluation has a calibration/smoke mode, calibration-only files should
be classified as conditional or not applicable rather than silently missing.

### Required Result Tables

The source evaluation root must include:

```text
results/schema_block_summary.csv
results/schema_diagnostic_summary.csv
results/tower_shape_summary.csv
results/tower_fiber_summary.csv
results/action_cell_summary.csv
results/tier_executability_summary.csv
results/abc_selection_summary.csv
results/abc_tier_signal_summary.csv
results/control_action_summary.csv
results/tier_occupancy_summary.csv
results/lift_failure_by_tier.csv
results/concrete_step_summary.csv
```

The exact table count may be consolidated during implementation if the same
information remains directly queryable. The implementation must not bury these
concepts only in per-run raw files.

### Required Per-Run Files

Each run bundle should include:

```text
run_manifest.json
seed_bundle.json
mode_manifest.json
linearization_manifest.json
environment_instance_manifest.json
schema_manifest.json
quotient_summary.json
timing_summary.json
timing_segments.csv
control_events.csv
abc_selection_events.csv
abc_tier_signal_events.csv
step_events.csv
lift_fiber_events.csv
warnings.jsonl
```

If a file is not applicable to a run mode, `readout_source.json` must say so.

### Human Docs Seed Files

The repo readout surface should contain or generate:

```text
README.md
method.md
runbook.md
artifact_index.md
glossary.md
results/summary.md
badges/
```

These are generated/readout surfaces. Durable design lessons discovered during
evaluation should be archived under:

```text
docs/design/system_learning_from_evaluations/
```

not left only in generated README conversation turns.

## Table Schemas

### `schema_block_summary.csv`

One row per schema seed and contraction block.

Required columns:

```text
evaluation_id
run_label
environment_instance_id
schema_id
schema_family_id
schema_seed
block_index
block_id
scheduled_edge_count
scheduled_edge_share
source_state_count
source_with_edges_count
min_edges_per_source_in_block
mean_edges_per_source_in_block
max_edges_per_source_in_block
zero_edge_source_count
construction_rule
```

Purpose:

```text
Show whether "one third" actually distributed contraction work across blocks
and source-local action surfaces.
```

### `tower_shape_summary.csv`

One row per run/schema seed/tier.

Required columns:

```text
evaluation_id
run_id
environment_instance_id
schema_id
schema_seed
tier_index
state_cell_count
action_cell_count
base_state_count
base_edge_count
state_compression_ratio
action_compression_ratio
largest_state_fiber_count
largest_state_fiber_share
largest_action_fiber_count
largest_action_fiber_share
singleton_state_cell_share
singleton_action_cell_share
effective_state_cell_count
effective_action_cell_count
degeneracy_class
```

Purpose:

```text
Make quotient collapse or gradual tower shape visible without opening per-run
JSON files.
```

### `abc_selection_events.csv`

One row per controller event.

Required columns:

```text
evaluation_id
run_id
episode_index
controller_event_index
environment_step_index
active_tier_before
active_tier_after
deepest_known_tier
selected_lowest_unclosed_tier
selected_tier_executable
control_action
training_due
decision_pressure
abc_direction_before
abc_action_consistent
abc_blocked_reason
concrete_step_emitted
lift_attempt_emitted
```

`abc_direction_before` should use a small stable vocabulary:

```text
descend_to_selected
lift_to_selected
at_selected
no_executable_unclosed
unknown
```

`abc_blocked_reason` should use a small stable vocabulary:

```text
none
selected_tier_not_executable
no_executable_tier
no_available_action
lift_failure
missing_signal
unknown
```

Purpose:

```text
Show what upstream ABC selected and whether the observed controller action
matched that selection.
```

### `abc_tier_signal_events.csv`

One row per controller event per tier.

Required columns:

```text
evaluation_id
run_id
episode_index
controller_event_index
tier_index
active_tier_before
is_active_tier
is_executable
visit_count
td_error_ema
success_count
failure_count
success_rate
reward_residual_ema
has_reward_residual
productive_learning_pressure
is_unclosed
selected_lowest_unclosed_tier
```

Purpose:

```text
Expose the signal substrate behind upstream lowest-unclosed selection.
```

### `tier_occupancy_summary.csv`

One row per run/schema seed/tier/action group.

Required columns:

```text
evaluation_id
run_id
environment_instance_id
schema_id
schema_seed
tier_index
control_action
event_count
event_share
concrete_step_count
concrete_step_share
successful_lift_count
failed_lift_count
mean_reward_on_concrete_steps
first_event_index
last_event_index
```

Purpose:

```text
Give the human reader a compact tier-occupancy view.
```

### `lift_failure_by_tier.csv`

One row per run/schema seed/tier/failure reason.

Required columns:

```text
evaluation_id
run_id
environment_instance_id
schema_id
schema_seed
tier_index
failure_reason
fiber_departure_reason
attempt_count
success_count
failure_count
mean_candidate_count
max_candidate_count
```

Purpose:

```text
Separate controller tier choice from concrete action-realization failures.
```

### `tier_executability_summary.csv`

One row per run/schema seed/tier.

Required columns:

```text
evaluation_id
run_id
environment_instance_id
schema_id
schema_seed
tier_index
event_count
executable_event_count
non_executable_event_count
executable_share
selected_while_executable_count
selected_while_non_executable_count
```

Purpose:

```text
Show whether coarser tiers were available for action at runtime.
```

## Badge Policy

The generated README should include a compact status badge strip at the top.

Recommended badge dimensions:

```text
artifact_status
schema_geometry_status
abc_runtime_status
lift_executability_status
claim_scope
provenance_status
```

### `artifact_status`

Green if:

- all required machine-readable files exist;
- `readout_source.json` is parseable;
- expected-file policy is complete;
- aggregate tables are nonempty.

Yellow if:

- core artifacts exist but optional/conditional files are missing or partially
  empty with recorded explanation.

Red if:

- required files are missing or source paths are ambiguous.

### `schema_geometry_status`

Green if:

- one-third block summaries exist;
- tower shape tables exist;
- tier `1` is not a full or near-full collapse under configured thresholds;
- deeper tiers are nontrivial enough to inspect.

Yellow if:

- tower shape exists but contains partial collapse, heavy imbalance, or one
  interpretable degenerate tier.

Red if:

- first projection collapses to one state cell;
- largest tier-`1` fiber exceeds the configured structural-limit threshold;
- tower shape is absent.

### `abc_runtime_status`

Green if:

- ABC selection event rows exist;
- selected lowest-unclosed tier is recorded;
- observed actions are mostly consistent with upstream selection semantics;
- tier occupancy is not pinned without explanation.

Yellow if:

- ABC event rows exist but behavior is mixed, short, or dominated by
  explainable structural limits.

Red if:

- ABC context is not recorded;
- runtime is pinned or oscillating without explanatory signal/executability
  rows;
- controller events are absent.

### `lift_executability_status`

Green if:

- executable tier rows exist;
- lift/action realization succeeds often enough to inspect concrete behavior;
- failures are sparse or clearly classified.

Yellow if:

- lift failures occur frequently but are classified and interpretable.

Red if:

- no executable tier is available;
- no concrete steps are emitted;
- lift failures dominate without sufficient classification.

### `claim_scope`

This badge should generally read diagnostic-only for this evaluation.

It should not turn green as "performance proven."

### `provenance_status`

Green if:

- artifacts are repo-resident under the readout surface;
- dependency state records `state_collapser` version and source;
- run ids, seeds, schema seeds, and linearization modes are recorded.

Yellow if:

- provenance is local but partial.

Red if:

- artifacts are outside the repo without source binding or dependency state.

## Structural Limit Checks

The evaluation must declare and apply these checks.

### Check 1: Full First-Projection Collapse

Trigger:

```text
tier_index == 1 and state_cell_count == 1
```

Interpretation:

```text
The first contraction block behaves like H -> pi_0(H) or near that limit.
Runtime behavior should be read as structural-limit evidence, not performance
evidence.
```

Claim effect:

```text
Blocks schema-promotion and performance claims.
Supports a structural pathology claim.
```

### Check 2: Near-Full First-Projection Collapse

Default trigger:

```text
tier_index == 1 and largest_state_fiber_share >= 0.90
```

Interpretation:

```text
The first tier retains too little state structure for ordinary occupancy or
reward-learning language to be trusted without qualification.
```

Claim effect:

```text
Blocks strong schema-promotion claims.
May support a cautionary diagnostic claim.
```

### Check 3: Non-Executable Selected Tier

Trigger:

```text
selected_lowest_unclosed_tier is not null
and selected_tier_executable == false
```

Interpretation:

```text
The active-tier controller's meaningful movement may be constrained by concrete
action availability rather than by ABC policy failure.
```

Claim effect:

```text
Blocks simple "controller failed" language.
Requires lift/executability explanation.
```

### Check 4: No Available Action

Trigger:

```text
control_action == "no_available_action"
```

Interpretation:

```text
The runtime could not find an executable action at any available tier for that
event.
```

Claim effect:

```text
Supports a runtime-blocked or structural-blocked classification.
Blocks learning-behavior claims for affected runs.
```

### Check 5: Zero Concrete Steps

Trigger:

```text
concrete_step_count == 0
```

Interpretation:

```text
The control loop may have emitted controller events, but the environment did
not receive concrete transitions.
```

Claim effect:

```text
Blocks behavioral claims.
Requires lift/action-realization diagnosis.
```

### Check 6: ABC Context Missing

Trigger:

```text
abc_selection_events.csv missing
or selected_lowest_unclosed_tier absent from event rows
or abc_tier_signal_events.csv missing
```

Interpretation:

```text
The evaluation cannot answer its central runtime question.
```

Claim effect:

```text
Artifacts may be complete in a narrow run sense, but the evaluation is
construction-incomplete for this blueprint.
```

## Expected-File Policy

The evaluation must classify files explicitly.

### Required

```text
readout_source.json
evaluation_manifest.json
evaluation_run_index.csv
evaluation_budget_lock.json
evaluation_aggregate_summary.json
evaluation_aggregate_table.csv
results/schema_block_summary.csv
results/schema_diagnostic_summary.csv
results/tower_shape_summary.csv
results/tier_occupancy_summary.csv
results/abc_selection_summary.csv
results/abc_tier_signal_summary.csv
results/lift_failure_by_tier.csv
results/tier_executability_summary.csv
```

### Expected Absent Is Gap

These files are expected for runtime modes and should be gaps if absent:

```text
per-run control_events.csv
per-run abc_selection_events.csv
per-run abc_tier_signal_events.csv
per-run lift_fiber_events.csv
per-run quotient_summary.json
per-run schema_manifest.json
```

### Conditional

Calibration-only files:

```text
calibration_summary.json
calibration_run_index.csv
calibration_recommendation.md
```

Smoke-only files:

```text
smoke_summary.json
```

### Not Applicable

Unless the PO changes scope, this evaluation does not require:

```text
direct arm aggregate comparison tables
direct-vs-tower statistical comparison tables
GPU timing tables
tensor-enabled comparison tables
musical-quality review tables
```

## Human-Readable Readout Requirements

The generated README must include:

- badge strip;
- one-paragraph result summary;
- "What this evaluation tested";
- "What this evaluation did not test";
- tower geometry summary;
- ABC runtime occupancy summary;
- lift/executability summary;
- structural-limit classification;
- allowed claims;
- blocked claims;
- links to method, runbook, artifact index, and result detail;
- turn conversation section for Evaluator and Codex clarification.

The generated `method.md` must explain:

- environment family and fixture;
- schema rule;
- state_collapser ABC surfaces used;
- what BBB instruments;
- what BBB does not implement;
- run budget and seed policy;
- artifact and expected-file policy;
- structural limit checks.

The generated `runbook.md` must explain:

- how to run smoke diagnostics;
- how to run the main diagnostic;
- how to summarize artifacts;
- how to invoke human-readable readout generation;
- where artifacts must live in the repo.

The generated `artifact_index.md` must link:

- source artifact root;
- source evaluation root;
- aggregate tables;
- per-run examples;
- schemas;
- manifests;
- timing.

The generated `glossary.md` must define:

- one-third contraction schema;
- contraction block;
- tier;
- active tier;
- lowest unclosed tier;
- productive-learning pressure;
- executable tier;
- lift;
- fiber;
- first-projection collapse;
- structural limit;
- diagnostic-only claim scope.

## Implementation Surface Expectations

This is not a gameplan, but the later gameplan will likely touch these areas.

### Counterpoint Ids

Add schema and evaluation ids in BBB-owned counterpoint surfaces.

Likely target:

```text
src/big_boy_benchmarking/environments/counterpoint/ids.py
```

### Schema Construction

Add one-third schema construction in:

```text
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
```

and, if needed for posthoc schema manifests:

```text
src/big_boy_benchmarking/environments/counterpoint/schemas.py
```

The implementation must distinguish:

- runtime `ContractionSchema` for `PartitionTower`;
- posthoc/readout schema manifest data for human and artifact docs.

### Runtime Instrumentation

Extend or specialize:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
```

or create a new diagnostic evaluation package that reuses its adapter pieces.

The instrumentation must call upstream helper functions, not copy controller
policy.

### Event Rows

Add event row dataclasses for:

```text
abc_selection_events.csv
abc_tier_signal_events.csv
```

Likely target:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/events.py
```

or a new evaluation-specific events module.

### Aggregation

Add evaluation-level aggregation for:

- schema block summaries;
- tower shape summaries;
- ABC selection summaries;
- tier signal summaries;
- tier occupancy summaries;
- lift/executability summaries.

### CLI

Add a CLI surface that keeps this evaluation separate from first serious
learning.

Possible shape:

```text
uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics run \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/<run-label> \
  --instance-id small \
  --schema-seeds 3
```

and:

```text
uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics summarize \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/<run-label>
```

The final CLI naming should be settled in the implementation gameplan.

## Validation Requirements

### Unit Tests

Tests should verify:

- the one-third schema id resolves;
- the schema returns exactly three ordered blocks;
- deterministic mode is stable if chosen;
- seeded mode is stable for the same seed and different for different seeds
  where expected;
- per-source block assignment is approximately balanced for sources with
  enough outgoing edges;
- the schema does not inspect reward outcomes, terminal outcomes, learned
  values, or future episode results;
- tower construction succeeds on `tiny`;
- tower construction succeeds on `small`;
- ABC diagnostic wrapper delegates to upstream `ActiveTierController`;
- ABC diagnostic wrapper records selected lowest-unclosed tier;
- per-tier signal rows can be generated;
- readout source binding is parseable.

### Smoke Runs

The gameplan should include a tiny smoke run that proves:

- the CLI works;
- artifacts land under the repo readout surface;
- required tables are nonempty;
- human-readout protocol can target the repo readout surface.

### Main Diagnostic Run

The gameplan should include a small diagnostic run that proves:

- tower geometry is inspectable;
- control events are emitted;
- ABC event rows are emitted;
- lift/executability rows are emitted;
- readout can summarize the result without raw artifact spelunking.

## Stop Conditions

Stop before implementation if:

- the PO has not settled the operational meaning of "one third";
- the PO has not settled whether schema seeds are part of the first pass;
- the planned implementation would require editing `/Users/foster/state_collapser`;
- BBB cannot call upstream ABC helper functions without copying policy;
- artifacts would not be repo-resident under `docs/evaluations/...`;
- the readout source binding cannot distinguish repo readout surface from raw
  artifact root;
- the evaluation would need to infer expected files after the fact;
- the runtime emits controller actions but no way to explain selected
  lowest-unclosed tier;
- the schema behaves like immediate `H -> pi_0(H)` collapse and the readout has
  no structural-limit language.

## Open Questions For Project Owner

These are consultant-authored open questions, not Project Owner statements.

They are the real remaining ambiguities that should be answered before the
implementation gameplan.

### Question 1: Operational Meaning Of "One Third"

What exact operational meaning of "one third" should this first evaluation use?

Current options:

- seeded per-source outgoing thirds, recommended by this blueprint;
- deterministic per-source outgoing thirds;
- upstream `SeededRandomRateSchema(seed, block_count=3)`;
- another rule specified by the Project Owner.

#### PO Answer:
> I think it literally means that $\delta_{H}$ from `logHRL_w_comments.tex` in `state_collapser` is $=1/3$.

### Question 2: Schema Seed Policy

Should the first main diagnostic use schema seeds?

Current options:

- yes, use a small fixed suite such as 3 seeds;
- no, use one deterministic no-seed schema;
- start with one seed only, treating it explicitly as a pilot.

#### PO Answer:
> Explain what this would mean here.

#### Codex Reply:
> I read this as fixing the contraction fraction, not as introducing a new
> comparison variable.
>
> One careful notation point: in `logHRL_w_comments.tex`, `\delta_H` appears as
> a connectivity threshold in the point-cloud example, while the later
> contraction-schema discussion says to sample `1/3` of the outgoing,
> not-yet-sampled edges at each node. For this BBB evaluation, I would treat
> your answer as binding the operational contraction parameter to:
>
> ```text
> fraction of outgoing, not-yet-scheduled edges per source state = 1/3
> ```
>
> Schema seeds would therefore not change the value `1/3`. They would only
> choose the random draw that realizes that fixed `1/3` sampling rule.
>
> Concretely:
>
> - if the one-third rule is deterministic, there is no schema-seed question;
>   the schema has one reproducible tower;
> - if the one-third rule is sampled, a schema seed records which outgoing
>   edges were selected into the first third, then which remaining outgoing
>   edges were selected into the next third, and so on;
> - each seed still means the same mathematical policy: sample one third of
>   outgoing, not-yet-sampled edges per source state;
> - multiple seeds are useful only to tell whether one random draw produced a
>   misleadingly good or misleadingly bad tower shape.
>
> My recommendation is: use seeded sampling for the first serious diagnostic,
> with a small fixed seed suite, because the source-local random draw is part
> of the intended point-cloud-like construction. The readout should present
> each seed separately and then summarize cross-seed stability. It should not
> present seed variation as a different contraction rate.

### Question 3: Fixture Scope

Which fixture scope should the first non-smoke run use?

Current options:

- `tiny` smoke plus `small` main diagnostic, recommended by this blueprint;
- `small` only;
- `tiny` only for a first implementation pass, with no meaningful claim.

#### PO Answer:
> I think think small and medium. Fuck "tiny" for this one.

### Question 4: Controller Runtime Budget

How much controller runtime should the first diagnostic use?

The run needs enough events to inspect ABC occupancy, but it is not a
performance comparison. The implementation gameplan can propose a concrete
budget after this design choice is clear.

#### PO Reply:
> What do you recommend?

#### Codex Answer:
> I recommend treating this as an observation-budget question, not a
> performance-budget question.
>
> Since you answered "small and medium" and explicitly rejected `tiny`, the
> implementation gameplan should not use `tiny` for this evaluation. There is a
> current repo reality issue, though: BBB currently implements `tiny` and
> `small`, while `medium` is only a reserved scale tier in the docs. So the
> gameplan needs an explicit prerequisite action to add and document
> `counterpoint_symbolic_n3_medium_v001`, or it must stop if that fixture cannot
> be responsibly defined.
>
> My recommended first locked diagnostic budget is:
>
> ```text
> instances: small, medium
> schema_seeds: 3
> replicates_per_schema_seed: 4
> episodes_per_replicate: 16
> horizon: fixture default horizon
> controller_event_ceiling: max(64, 8 * horizon)
> ```
>
> Rationale:
>
> - `3` schema seeds is enough to detect whether one random one-third draw is
>   anomalous without turning this into a big schema-stability study;
> - `4` replicates per seed is enough to distinguish deterministic tower-shape
>   effects from start/learner/controller-seed noise;
> - `16` episodes matches the scale of the recent corrected counterpoint run
>   and should produce enough controller events for occupancy and ABC
>   diagnostics;
> - `max(64, 8 * horizon)` stays close to current BBB runtime discipline while
>   giving short-horizon fixtures enough controller decisions to inspect.
>
> If this produces too few `TRAIN`, `DESCEND`, `LIFT`, or concrete-step events,
> I would increase the controller-event ceiling first, not convert the
> evaluation into a larger reward-learning run. The goal here is enough traces
> to explain tower geometry and ABC occupancy, not enough budget to claim
> learning superiority.

### Question 5: Near-Full Collapse Threshold

Should the readout treat near-full first projection collapse as:

```text
largest_state_fiber_share >= 0.90
```

or should it use a different threshold?

#### PO Answer:
> I think that's good. Just explain clearly what "near full collapse" means in human readable docs.

## Blueprint Completion Checklist

This blueprint is complete enough for a Phase.Stage.Action gameplan when:

- the PO accepts or corrects the recommended one-third schema rule;
- schema seed policy is settled;
- fixture scope is settled;
- main diagnostic budget policy is settled or delegated to calibration;
- structural-limit threshold policy is settled;
- the later gameplan preserves the upstream-ABC boundary.

Until then, the implementation gameplan may be drafted with explicit decision
locks, but it must not quietly implement a different schema or controller
interpretation.
