# Counterpoint One-Third Schema Tower Diagnostics Implementation Workplan

Date: 2026-05-31

Status: implementation workplan, not yet executed

Repository:

```text
<repo-root>
```

Source blueprint:

```text
docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/01_001_counterpoint_one_third_schema_tower_diagnostics_blueprint.md
```

## Purpose

This workplan translates the one-third counterpoint tower diagnostics blueprint
into Phase.Stage.Action implementation work.

The target is a diagnostic evaluation for:

```text
counterpoint_symbolic_v001
```

focused on:

- a source-local one-third contraction schema;
- `small` and `medium` counterpoint fixtures;
- upstream `state_collapser` ABC control behavior;
- tier occupancy and lowest-executable-unclosed diagnostics;
- tower geometry and lift/executability diagnostics;
- repo-resident artifacts and human-readable readout support.

This is not a direct-vs-tower performance comparison.

This is not a new environment family.

This is not approval to edit `<state-collapser-repo>`.

## Execution Authority Status

This document is not approval to implement.

The Project Owner asked for this workplan from the blueprint:

```text
Ok can you now use docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/01_001_counterpoint_one_third_schema_tower_diagnostics_blueprint.md to geenrate implementation workplan in Phase.Stage.Action form, following prime_directive?
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
- `docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md`
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`
- `docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/design_discussion.md`
- `docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/01_001_counterpoint_one_third_schema_tower_diagnostics_blueprint.md`
- `docs/design/first_counterpoint_environment/01_002_counterpoint_hidden_graph_and_contraction_schema_benchmark_blueprint.md`
- `docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_001_counterpoint_first_serious_learning_evaluation_blueprint.md`
- `docs/environments/counterpoint_symbolic_v001.md`
- read-only current BBB counterpoint source surfaces
- read-only current `state_collapser` ABC control and partition-tower source
  surfaces

## Fixed Design Locks

These locks come from the blueprint and its recorded answers.

### Evaluation Scope

This is a diagnostic evaluation on the existing environment family:

```text
counterpoint_symbolic_v001
```

The evaluation id should be:

```text
counterpoint_one_third_schema_tower_diagnostics_v001
```

The repo readout surface should be:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/
```

### Schema Meaning

The one-third contraction parameter is:

```text
fraction of outgoing, not-yet-scheduled edges per source state = 1/3
```

The implementation must not substitute:

- global random thirds;
- deterministic lexical thirds;
- motion-label thirds;
- existing `SeededRandomRateSchema(seed, block_count=3)`;
- any schema that ignores source-local outgoing edge sets.

`SeededRandomRateSchema(seed, block_count=3)` may be referenced only as a
contrast or future sanity-check, not as the implementation of this evaluation.

### Schema Seeds

Use seeded source-local sampling for the first implementation.

Use a small fixed seed suite:

```text
schema_seeds: 3
```

Each schema seed changes only the random draw that realizes the fixed one-third
sampling rule. It does not change the contraction fraction.

### Fixtures

Use:

```text
small
medium
```

Do not add a `tiny` smoke path for this evaluation.

Current repo reality: BBB has `tiny` and `small` implemented; `medium` is only
reserved in docs. Therefore this workplan includes an explicit medium-fixture
implementation phase.

### Runtime Budget

The first locked diagnostic budget is:

```text
instances: small, medium
schema_seeds: 3
replicates_per_schema_seed: 4
episodes_per_replicate: 16
horizon: fixture default horizon
controller_event_ceiling: max(64, 8 * horizon)
```

This is an observation budget for tower/ABC diagnostics, not a performance
budget for reward-learning claims.

### Collapse Threshold

Near-full first-projection collapse threshold:

```text
largest_state_fiber_share >= 0.90
```

Human-readable docs must explain that "near full collapse" means one quotient
cell at tier `1` contains at least 90 percent of the base states, so the first
projection has preserved too little state structure for ordinary performance
language.

### Upstream ABC Boundary

BBB must not implement an alternate ABC controller.

BBB must run upstream:

```text
state_collapser.tower.control.ActiveTierController
state_collapser.tower.runtime.ExploitExploreTowerRuntime
```

BBB may instrument upstream helper functions on the same inputs passed to the
controller.

BBB must not copy controller policy and then treat the copy as source of truth.

## Global Stop Conditions

Stop and ask the Project Owner if:

- explicit approval to execute this workplan has not been received;
- branch or dirty status would mix unrelated work into this implementation;
- any action would require editing `<state-collapser-repo>`;
- installed `state_collapser` lacks the upstream ABC helper surfaces used by
  this plan;
- current BBB tower-control runtime cannot expose the inputs needed to call
  upstream ABC helper functions;
- the one-third schema cannot be implemented source-locally without relying on
  reward outcomes, terminal outcomes, learned values, or future episode data;
- medium fixture graph enumeration is too large for a diagnostic run under the
  chosen budget;
- the implementation would need to reintroduce `tiny` as an evaluation path;
- artifacts would not be repo-resident under `docs/evaluations/...`;
- a required table would be omitted without an explicit expected-file policy;
- exact implementation of any Phase.Stage.Action would require a weaker
  substitute, hidden simplification, or unapproved reordering;
- a generated workplan action would require changing the approved scope into a
  direct-vs-tower comparison.

## Required Branch Discipline

After Project Owner approval and before implementation edits, create and switch
to:

```text
codex/one-third-schema-tower-diagnostics
```

Do not implement on `main` unless the Project Owner explicitly authorizes that.

## Implementation Log Requirement

When this workplan is executed, create and maintain:

```text
docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/01_003_counterpoint_one_third_schema_tower_diagnostics_implementation_log.md
```

The log must record:

- branch name;
- each completed Phase.Stage.Action;
- files changed;
- tests and command outputs;
- runtime surprises;
- any stop condition encountered;
- any Project Owner clarifications after this workplan.

## Phase 0. Stage 0. Action 1: Confirm Execution Authority

Before edits, confirm that the Project Owner explicitly requested execution of
this exact workplan.

If not approved, stop.

## Phase 0. Stage 0. Action 2: Create Work Branch

Create and switch to:

```text
codex/one-third-schema-tower-diagnostics
```

Record the branch in the implementation log.

## Phase 0. Stage 0. Action 3: Capture Initial Repo State

Run a non-destructive repo-state inspection.

Record:

- branch;
- short git status;
- whether the new blueprint and workplan are tracked or untracked;
- whether unrelated user changes exist.

Do not revert unrelated changes.

## Phase 0. Stage 0. Action 4: Verify Upstream Dependency Surfaces

Verify that installed `state_collapser` exposes:

```text
ActiveTierController
ExploitExploreTowerRuntime
TierSignalState
TierControlConfig
productive_learning_pressure
is_unclosed
select_lowest_unclosed_tier
should_descend
should_lift
BaseGraphRegistry.source_state_id
BaseGraphRegistry.outgoing_edge_ids
```

Stop if any required surface is absent.

## Phase 0. Stage 0. Action 5: Start Implementation Log

Create the implementation log with:

- source blueprint path;
- execution approval note;
- branch name;
- initial repo status;
- dependency surface verification result.

## Phase 1. Stage 1. Action 1: Add Medium Fixture Constants

In:

```text
src/big_boy_benchmarking/environments/counterpoint/instances.py
```

add:

```text
MEDIUM_INSTANCE_ID = "counterpoint_symbolic_n3_medium_v001"
```

Do not remove or rename existing tiny or small constants.

## Phase 1. Stage 1. Action 2: Define Medium Candidate Spec

Add:

```text
medium_candidate_specs()
default_medium_spec()
```

The medium fixture must remain in the same environment family and contract ids.

Recommended starting shape:

```text
voice_count: 3
pitch_min: 58
pitch_max: 74
measure_size: 4
horizon_steps: 12
max_step_size: 2
max_outer_span: 16
```

If graph enumeration is too large or too small for diagnostic use, stop before
silently changing these parameters. Record the measured graph size and ask for
guidance.

## Phase 1. Stage 1. Action 3: Add Medium Resolver Support

Update counterpoint instance resolution surfaces so CLI and evaluation code can
resolve:

```text
medium
counterpoint_symbolic_n3_medium_v001
```

Likely target:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/runner.py
```

If a new one-third diagnostics package owns its own resolver, still share or
reuse the canonical medium spec from `instances.py`.

## Phase 1. Stage 1. Action 4: Document Medium Fixture

Update:

```text
docs/environments/counterpoint_symbolic_v001.md
```

to list `counterpoint_symbolic_n3_medium_v001` as implemented for this
diagnostic evaluation once the fixture exists.

The doc must distinguish:

- first serious learning used `small`;
- one-third schema diagnostics use `small` and `medium`;
- `tiny` remains available elsewhere but is not part of this evaluation.

## Phase 1. Stage 1. Action 5: Test Fixture Enumeration

Add or update tests proving:

- `default_medium_spec()` validates;
- `candidate_initial_states(default_medium_spec())` is nonempty;
- `initial_states(default_medium_spec())` is nonempty;
- reachable graph enumeration for medium produces nonzero states and edges.

Do not assert brittle exact graph sizes unless existing project style already
does so for fixtures.

## Phase 2. Stage 1. Action 1: Add One-Third Schema IDs

In:

```text
src/big_boy_benchmarking/environments/counterpoint/ids.py
```

add stable ids:

```text
ONE_THIRD_SCHEMA_FAMILY_ID = "counterpoint_one_third_schema_v001"
ONE_THIRD_OUTGOING_SCHEMA_ID = "counterpoint_one_third_outgoing_schema_v001"
```

Add them to `CANONICAL_IDS`.

## Phase 2. Stage 1. Action 2: Implement Source-Local One-Third Runtime Schema

In:

```text
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
```

add a BBB-owned runtime `ContractionSchema` implementation for source-local
one-third sampling.

The schema must:

- satisfy upstream `ContractionSchema`;
- expose exactly three ordered blocks;
- use `registry.source_state_id(edge_id)`;
- use `registry.outgoing_edge_ids(source_id)`;
- consider outgoing edges at the source state, not all graph edges globally;
- assign each edge to a block by sampling from outgoing, not-yet-scheduled
  edges at fraction `1/3`;
- use `schema_seed` to make the source-local random draw reproducible;
- avoid reward, terminal, learned-value, future-outcome, or evaluation-result
  inputs.

Recommended class name:

```text
CounterpointOutgoingThirdsSchema
```

## Phase 2. Stage 1. Action 3: Define Exact Sampling Rule

Implement the source-local sampling rule as:

```text
for each source state:
  seeded-shuffle that source's outgoing edge ids
  assign approximately the first third to block 0
  assign approximately the next third of remaining edges to block 1
  assign approximately the next third of remaining edges to block 2
  leave leftover edges unscheduled only if the fixed one-third recursive rule
  cannot exhaust them cleanly under integer rounding
```

Integer rounding must be deterministic and documented in the schema manifest.

Preferred rounding:

```text
block_size = max(1, ceil(remaining_count / 3))
```

applied recursively while blocks remain and remaining edges exist.

If this rounding produces a materially different meaning from the blueprint
during implementation review, stop and ask.

## Phase 2. Stage 1. Action 4: Wire Schema Into Tower Adapter

Update:

```text
contraction_schema_for_id(...)
```

so:

```text
counterpoint_one_third_outgoing_schema_v001
```

returns `CounterpointOutgoingThirdsSchema(schema_seed=...)`.

Do not replace existing schema behavior for empty, random, motion, projection,
or bad schemas.

## Phase 2. Stage 1. Action 5: Add Posthoc Schema Manifest Construction

In:

```text
src/big_boy_benchmarking/environments/counterpoint/schemas.py
```

add readout/manifest support for:

```text
counterpoint_one_third_outgoing_schema_v001
```

The manifest must record:

- `schema_family_id`;
- `schema_seed`;
- construction method;
- source-local one-third fraction;
- leakage statement;
- online eligibility;
- diagnostic role;
- expected tower depth of three contraction blocks plus base tier.

This posthoc manifest is not the runtime `ContractionSchema`; it is the
human/artifact description of the same schema policy.

## Phase 2. Stage 1. Action 6: Add Schema Unit Tests

Add tests proving:

- the schema id resolves;
- the runtime schema exposes exactly three ordered blocks;
- same seed gives stable assignment;
- different seeds can produce different assignment when outgoing branching
  permits;
- assignment is source-local rather than global;
- every scheduled edge belongs to one of the three ordered blocks;
- no reward or terminal fields are required to assign blocks.

## Phase 3. Stage 1. Action 1: Create Evaluation Package

Create a new package:

```text
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/
```

with at least:

```text
__init__.py
config.py
events.py
manifests.py
paths.py
runner.py
aggregation.py
docs_writer.py
```

This evaluation must remain separate from:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/
```

It may reuse adapter/learner/executor code where appropriate.

## Phase 3. Stage 1. Action 2: Define Evaluation Config

In `config.py`, define:

```text
EVALUATION_ID
EVALUATION_RUN_FAMILY_ID
DEFAULT_SCHEMA_ID
DEFAULT_SCHEMA_SEEDS
DEFAULT_REPLICATES_PER_SCHEMA_SEED
DEFAULT_EPISODES_PER_REPLICATE
DEFAULT_CONTROLLER_EVENT_CEILING_POLICY
DEFAULT_LINEARIZATION_MODE_ID
NEAR_FULL_COLLAPSE_THRESHOLD
```

Use:

```text
schema_seeds = (0, 1, 2)
replicates_per_schema_seed = 4
episodes_per_replicate = 16
linearization_mode_id = "tensor_available_disabled"
near_full_collapse_threshold = 0.90
```

## Phase 3. Stage 1. Action 3: Define Evaluation Paths

In `paths.py`, define paths for:

- repo readout surface;
- artifact root;
- source evaluation root;
- evaluation manifests;
- result tables;
- per-run bundles.

The default repo readout surface is:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/
```

The implementation must not default to `<tmp-dir>` for this evaluation.

## Phase 3. Stage 1. Action 4: Define Evaluation Manifests

In `manifests.py`, define payloads for:

```text
evaluation_manifest.json
evaluation_budget_lock.json
evaluation_aggregate_summary.json
readout_source.json
```

The manifest must include:

- environment family id;
- instance ids;
- schema id;
- schema seeds;
- budget;
- linearization mode;
- claim boundary;
- expected-file policy;
- structural-limit checks;
- goal criteria;
- methodology source references.

## Phase 3. Stage 1. Action 5: Define Event Rows

In `events.py`, define flat rows for:

```text
abc_selection_events.csv
abc_tier_signal_events.csv
schema_block_summary.csv
tower_shape_summary.csv
tier_executability_summary.csv
control_action_summary.csv
tier_occupancy_summary.csv
lift_failure_by_tier.csv
concrete_step_summary.csv
```

Reuse existing `FlatRow` style.

## Phase 4. Stage 1. Action 1: Add ABC Diagnostic Snapshot Type

In the one-third diagnostics package, add a dataclass representing one
controller-decision diagnostic snapshot.

It must include:

- active tier before;
- deepest known tier;
- selected lowest executable unclosed tier;
- per-tier productive-learning pressure;
- per-tier unclosed status;
- per-tier executable status;
- predicted movement direction;
- training-due flag;
- upstream controller decision after delegation.

## Phase 4. Stage 1. Action 2: Implement Diagnostic Controller Wrapper

Implement a wrapper around upstream `ActiveTierController`.

The wrapper must:

1. receive the same inputs passed to `ActiveTierController.decide(...)`;
2. call upstream helper functions on those inputs;
3. store diagnostic snapshots;
4. delegate to upstream `ActiveTierController.decide(...)`;
5. return the upstream decision unmodified.

Required upstream helper calls:

```text
productive_learning_pressure(...)
is_unclosed(...)
select_lowest_unclosed_tier(...)
should_descend(...)
should_lift(...)
```

## Phase 4. Stage 1. Action 3: Emit ABC Selection Event Rows

Convert each diagnostic snapshot into one `abc_selection_events.csv` row.

Each row must include:

- selected lowest executable unclosed tier;
- control action;
- active tier before/after;
- movement direction;
- consistency flag;
- blocked reason;
- concrete step emitted flag;
- lift attempt emitted flag.

## Phase 4. Stage 1. Action 4: Emit ABC Tier Signal Event Rows

Convert each diagnostic snapshot into per-tier `abc_tier_signal_events.csv`
rows.

Each row must include:

- tier index;
- executable status;
- visit count;
- TD-error EMA;
- success/failure counts;
- success rate;
- reward residual fields;
- productive-learning pressure;
- unclosed status;
- whether that tier was selected.

## Phase 4. Stage 1. Action 5: Preserve Existing Control Events

Continue writing ordinary `control_events.csv` rows.

Do not replace existing control events with ABC rows. ABC rows are additional
explanatory surfaces.

## Phase 5. Stage 1. Action 1: Build Diagnostic Runner Loop

Implement the run loop in:

```text
one_third_diagnostics/runner.py
```

It must run:

```text
instances: small, medium
schema_seeds: 0, 1, 2
replicates_per_schema_seed: 4
episodes_per_replicate: 16
```

using the one-third schema id and upstream `ExploitExploreTowerRuntime`.

## Phase 5. Stage 1. Action 2: Reuse Counterpoint Tower Adapter Pieces

Reuse existing counterpoint adapter pieces where possible:

```text
CounterpointTowerControlAdapter
CounterpointTierLearner
CounterpointLiftResolveExecutor
build_tier_configs
```

If reuse would require mutating first serious learning behavior in a risky way,
extract shared helper code conservatively rather than duplicating controller
policy.

## Phase 5. Stage 1. Action 3: Apply Controller Event Ceiling

Use:

```text
max_controller_events = max(64, 8 * horizon)
```

unless the runner exposes an explicit override.

Record the ceiling in budget manifests.

## Phase 5. Stage 1. Action 4: Write Per-Run Artifacts

For each run, write:

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

## Phase 5. Stage 1. Action 5: Write Evaluation Run Index

Write:

```text
evaluation_run_index.csv
```

with one row per instance/schema seed/replicate run.

Include:

- evaluation id;
- run id;
- instance id;
- schema id;
- schema seed;
- replicate index;
- status;
- artifact root;
- started/ended timestamps.

## Phase 6. Stage 1. Action 1: Aggregate Schema Block Summaries

Write:

```text
results/schema_block_summary.csv
```

from schema assignment data.

Include:

- scheduled edge count by block;
- scheduled edge share by block;
- source-local distribution metrics;
- construction rule;
- schema seed.

## Phase 6. Stage 1. Action 2: Aggregate Tower Shape Summaries

Write:

```text
results/tower_shape_summary.csv
```

with one row per instance/schema seed/run/tier.

Include:

- state-cell counts;
- action-cell counts;
- compression ratios;
- largest fiber shares;
- singleton shares;
- degeneracy class.

## Phase 6. Stage 1. Action 3: Aggregate ABC Selection Summaries

Write:

```text
results/abc_selection_summary.csv
```

Summarize:

- selected tier frequencies;
- movement-consistency rates;
- blocked reasons;
- descend/lift/train/explore/exploit/no-available-action counts.

## Phase 6. Stage 1. Action 4: Aggregate ABC Tier Signal Summaries

Write:

```text
results/abc_tier_signal_summary.csv
```

Summarize by instance/schema seed/run/tier:

- executable event share;
- unclosed event share;
- mean productive-learning pressure;
- selected event count;
- active event count.

## Phase 6. Stage 1. Action 5: Aggregate Tier Occupancy Summaries

Write:

```text
results/tier_occupancy_summary.csv
```

Summarize by instance/schema seed/run/tier/control action:

- event counts;
- event shares;
- concrete step counts;
- concrete step shares;
- mean reward on concrete steps.

## Phase 6. Stage 1. Action 6: Aggregate Lift Failure Summaries

Write:

```text
results/lift_failure_by_tier.csv
```

Summarize:

- lift attempts;
- lift successes;
- lift failures;
- candidate counts;
- failure reasons;
- fiber departure reasons.

## Phase 6. Stage 1. Action 7: Aggregate Concrete Step Summaries

Write:

```text
results/concrete_step_summary.csv
```

Summarize:

- concrete step count;
- zero-step runs;
- mean reward;
- termination/truncation counts;
- final-state summary.

## Phase 6. Stage 1. Action 8: Apply Structural Limit Classification

Write structural-limit classifications into:

```text
evaluation_aggregate_table.csv
evaluation_aggregate_summary.json
```

Classify:

- full first-projection collapse;
- near-full first-projection collapse;
- selected tier non-executability;
- no available action;
- zero concrete steps;
- missing ABC context.

Do not label a structural-limit case merely as "mixed."

## Phase 7. Stage 1. Action 1: Write Readout Source Binding

Generate:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/readout_source.json
```

Bind:

- repo readout surface;
- artifact root;
- source evaluation root;
- evaluation id;
- environment instance ids;
- schema id;
- schema seeds;
- run mode;
- source files;
- expected files;
- goal criteria;
- badge policy;
- structural-limit checks;
- claim boundary.

## Phase 7. Stage 1. Action 2: Write Human Docs Seeds

Generate or update:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/README.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/method.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/runbook.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifact_index.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/glossary.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/results/summary.md
```

The docs must clearly explain "near full collapse" in human-readable terms.

## Phase 7. Stage 1. Action 3: Write Badge Inputs

Ensure the readout source and generated README can support badges for:

```text
artifact_status
schema_geometry_status
abc_runtime_status
lift_executability_status
claim_scope
provenance_status
```

Badges must be evidence-derived, not optimistic prose.

## Phase 7. Stage 1. Action 4: Preserve Generated-Readout Conversation Discipline

If readout docs include conversation or clarification sections, they must not
invent Project Owner turns.

Use:

```text
Open Questions For Project Owner
Consultant-authored notes
```

unless quoting real Project Owner text from the conversation or checked-in
documents.

## Phase 8. Stage 1. Action 1: Add CLI Run Command

Add CLI support for:

```text
uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics run \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/<run-label> \
  --instance-ids small,medium
```

Support explicit options for:

- schema seeds;
- replicates;
- episodes;
- controller event ceiling;
- linearization mode;
- locked-by.

## Phase 8. Stage 1. Action 2: Add CLI Summarize Command

Add CLI support for:

```text
uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics summarize \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/<run-label>
```

The summarize command must generate evaluation-level aggregate tables and
readout source bindings.

## Phase 8. Stage 1. Action 3: Add CLI Validation Errors

Ensure CLI rejects:

- `tiny` for this evaluation;
- unknown instances;
- non-repo artifact roots unless explicitly allowed by a future design;
- unsupported schema ids;
- tensor-enabled modes unless a future design approves them.

## Phase 9. Stage 1. Action 1: Add Unit Tests For Medium Fixture

Add tests for:

- medium spec resolution;
- medium initial states;
- medium reachable graph enumeration;
- medium environment manifest fields.

## Phase 9. Stage 1. Action 2: Add Unit Tests For One-Third Schema

Add tests for:

- schema id resolution;
- ordered block count;
- source-local assignment;
- reproducibility by seed;
- no reward leakage;
- posthoc schema manifest fields.

## Phase 9. Stage 1. Action 3: Add Unit Tests For ABC Instrumentation

Add tests proving:

- diagnostic wrapper delegates to upstream `ActiveTierController`;
- selected lowest executable unclosed tier is recorded;
- per-tier productive-learning pressure is recorded;
- per-tier executable status is recorded;
- action consistency is classified correctly;
- wrapper does not alter upstream decisions.

## Phase 9. Stage 1. Action 4: Add Unit Tests For Aggregation

Add tests proving aggregation writes:

- schema block summary;
- tower shape summary;
- ABC selection summary;
- ABC tier signal summary;
- tier occupancy summary;
- lift failure summary;
- concrete step summary;
- aggregate summary JSON.

## Phase 9. Stage 1. Action 5: Add CLI Tests

Add tests proving:

- run command parses;
- summarize command parses;
- `tiny` is rejected;
- default artifact root convention is repo-resident;
- readout source binding is generated.

## Phase 10. Stage 1. Action 1: Run Focused Unit Tests

Run focused tests for:

```text
tests/environments/counterpoint/
tests/upstream/
```

and any new one-third diagnostics tests.

Record command output in the implementation log.

## Phase 10. Stage 1. Action 2: Run Formatting Or Static Checks

Run the repo's established formatting or static checks if present.

If no formatter/linter is configured, record that no such configured check was
found.

## Phase 10. Stage 1. Action 3: Run Small Diagnostic Command

Run the evaluation on `small` only with the locked defaults if runtime is
reasonable.

This is not a tiny smoke test. It is a small-instance artifact validation run.

Artifact root:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/small_validation_001
```

If the command is too slow, stop and report measured timing before reducing the
budget.

## Phase 10. Stage 1. Action 4: Run Medium Diagnostic Command

Run the evaluation on `medium` with the locked defaults if Phase 10. Stage 1.
Action 3 succeeds and medium graph enumeration is feasible.

Artifact root:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/medium_validation_001
```

If medium is too slow or too large, stop and report measured graph size and
timing. Do not silently replace medium with tiny.

## Phase 10. Stage 1. Action 5: Run Summarize Command

Run summarize for the validation artifact roots.

Confirm the required result tables exist and are nonempty unless expected-file
policy says otherwise.

## Phase 10. Stage 1. Action 6: Run Human-Readable Readout Protocol

Execute the repo-side readout protocol against:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/
```

Confirm the readout writes or updates:

- README;
- result readout;
- artifact index;
- method;
- runbook;
- glossary;
- badges;
- results summary.

## Phase 11. Stage 1. Action 1: Update Environment And Evaluation Indexes

Update repo-level documentation indexes only as needed:

```text
README.md
docs/README.md
docs/evaluations/README.md
docs/environments/counterpoint_symbolic_v001.md
```

These updates should be brief and link to the new readout surface.

Do not make performance claims.

## Phase 11. Stage 1. Action 2: Final Test Pass

Run the focused test suite again after docs and aggregation changes.

Also run:

```text
git diff --check
```

Record results in the implementation log.

## Phase 11. Stage 1. Action 3: Final Repo Status Review

Review:

```text
git status --short
```

Group changed files by purpose:

- medium fixture;
- one-third schema;
- diagnostics evaluation package;
- CLI;
- tests;
- docs/readout;
- implementation log.

## Phase 11. Stage 1. Action 4: Final Report

Report:

- what was implemented;
- what commands were run;
- where artifacts landed;
- where the human-readable readout lives;
- whether medium was feasible;
- any stop conditions encountered;
- remaining risks.

Do not claim the workplan was executed if any Phase.Stage.Action item was
skipped or replaced.

## Expected File Touch List

Likely source files:

```text
src/big_boy_benchmarking/environments/counterpoint/ids.py
src/big_boy_benchmarking/environments/counterpoint/instances.py
src/big_boy_benchmarking/environments/counterpoint/schemas.py
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/__init__.py
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/config.py
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/events.py
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/manifests.py
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/paths.py
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/aggregation.py
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/docs_writer.py
src/big_boy_benchmarking/cli.py
```

Likely tests:

```text
tests/environments/counterpoint/test_instances.py
tests/environments/counterpoint/test_one_third_schema.py
tests/environments/counterpoint/test_one_third_diagnostics_runner.py
tests/environments/counterpoint/test_one_third_diagnostics_aggregation.py
tests/environments/counterpoint/test_cli.py
```

Likely docs and artifact surfaces:

```text
docs/environments/counterpoint_symbolic_v001.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/
docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/01_003_counterpoint_one_third_schema_tower_diagnostics_implementation_log.md
```

Do not edit:

```text
<state-collapser-repo>
```

unless the Project Owner gives a separate explicit instruction.
