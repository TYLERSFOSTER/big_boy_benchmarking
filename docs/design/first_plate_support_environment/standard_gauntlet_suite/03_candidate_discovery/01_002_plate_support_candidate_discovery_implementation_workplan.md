# PlateSupport Candidate Discovery Implementation Workplan

## Status

Status: initial implementation workplan.

This document is generated from:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/03_candidate_discovery/01_001_plate_support_candidate_discovery_blueprint.md
```

This workplan depends on:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/00_suite_architecture/01_002_plate_support_standard_gauntlet_suite_architecture_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/01_structural_and_tower_diagnostics/01_002_plate_support_structural_and_tower_diagnostics_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/02_contraction_schema_sweep/01_002_plate_support_contraction_schema_sweep_implementation_workplan.md
```

This workplan uses `Phase.Stage.Action` discipline.

This workplan is not execution approval. Execution requires explicit Project
Owner instruction.

## Prime Directive Compliance Notes

This workplan follows:

- `docs/prime_directive/prime_directive.md`;
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`;
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`;
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`;
- `docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md`;
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`.

Operational consequences:

- Execute only after Project Owner approval.
- Execute only after Stage 2 emits candidate-signal tables.
- Do not silently select candidates from raw tower files when Stage 2 summary
  tables exist.
- Do not drop blocked candidates.
- Do not treat eligibility score as performance evidence.
- Do not train candidates in this stage.
- Do not allow Stage 6 to consume Stage 3 directly.

## Authority And Attribution

Project Owner direction from the current request:

- create this detailed workplan after schema sweep and before training health;
- follow the blueprint and Phase.Stage.Action discipline.

Consultant-authored assumptions pending Project Owner override:

- candidate selection policy id is `plate_support_candidate_selection_policy_v001`;
- first implementation uses:
  - `clean_candidate_cap = 2`;
  - `warning_candidate_cap = 1`;
  - `degeneracy_anchor_cap = 1`;
- upstream default is included if eligible or warning-eligible;
- warning candidates are selected as warning candidates only and require later
  explicit authorization before training.

These assumptions are not Project Owner decisions.

## Decision Locks Before Implementation

- Stage 3 consumes Stage 2 outputs:
  - `schema_candidate_signal_summary.csv`;
  - `schema_arm_summary.csv`;
  - `schema_construction_summary.csv`;
  - `tower_shape_summary.csv`;
  - `tier_executability_summary.csv`;
  - `collapse_diagnostic_summary.csv`;
  - `stage_aggregate_summary.json`.
- Stage 3 retains important Stage 1 context but does not reach around Stage 2
  to select candidates.
- Every Stage 2 signal row must be classified.
- Candidate IDs must be deterministic.
- Candidate source traces must be repo-resident.
- Candidate selection is not training evidence.
- Stage 4 may consume Stage 3; Stage 6 must wait for Stages 4 and 5.

## Expected Final Deliverables

Implementation should produce or update:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/candidate_discovery/
tests/environments/plate_support/test_standard_gauntlet_candidate_discovery.py
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/candidate_discovery/
docs/design/first_plate_support_environment/standard_gauntlet_suite/03_candidate_discovery/01_003_plate_support_candidate_discovery_implementation_log.md
```

Recommended package files:

```text
__init__.py
config.py
stage2_source.py
policy.py
eligibility.py
candidate_ids.py
selection.py
aggregation.py
manifests.py
docs_writer.py
runner.py
```

Recommended CLI surface:

```bash
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet candidate-discovery run \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \
  --schema-sweep-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/contraction_schema_sweep/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster
```

## Workplan

### Phase 0: Execution Setup And Stage 2 Gate

#### Phase 0.Stage 1: Re-anchor Repository And Inputs

##### Phase 0.Stage 1.Action 1: Verify branch and dirty state

Action:

- run `git status --short --branch`;
- record branch and dirty files in the Stage 3 implementation log.

Completion criteria:

- repo state is known before edits.

Stop condition:

- stop if unrelated dirty files would be overwritten or confused with Stage 3.

##### Phase 0.Stage 1.Action 2: Verify architecture, Stage 1, and Stage 2 availability

Action:

- confirm 00 architecture helpers exist;
- confirm Stage 1 context paths are available through Stage 2 provenance;
- confirm Stage 2 readout/source artifacts exist or can be generated.

Completion criteria:

- Stage 3 can consume Stage 2 without direct raw inference.

Stop condition:

- stop if Stage 2 has not emitted candidate-signal outputs.

##### Phase 0.Stage 1.Action 3: Validate Stage 2 pass/warning/block state

Action:

- read Stage 2 aggregate status and candidate-signal table.

Completion criteria:

- Stage 3 knows whether it can proceed, warn, or block.

Stop condition:

- stop if Stage 2 is blocked and no candidate-signal table exists.

#### Phase 0.Stage 2: Create Implementation Log

##### Phase 0.Stage 2.Action 1: Create Stage 3 implementation log

Action:

- create:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/03_candidate_discovery/01_003_plate_support_candidate_discovery_implementation_log.md
```

Completion criteria:

- log exists before source edits.

Stop condition:

- stop if log path conflicts with unrelated content.

##### Phase 0.Stage 2.Action 2: Add progress table and source record

Action:

- add Phase.Stage.Action progress table;
- record Stage 2 source documents and artifact paths.

Completion criteria:

- selection process can be audited later.

Stop condition:

- stop if source artifact identity is ambiguous.

### Phase 1: Stage Package And Configuration

#### Phase 1.Stage 1: Create Candidate Discovery Package

##### Phase 1.Stage 1.Action 1: Create module directory

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/candidate_discovery/
```

Completion criteria:

- package is nested under the standard gauntlet suite package.

Stop condition:

- stop if suite package is missing.

##### Phase 1.Stage 1.Action 2: Add module initializer

Action:

- create `__init__.py` exporting stable runner/config symbols.

Completion criteria:

- import has no side effects and performs no selection.

Stop condition:

- stop if import reads artifacts or writes files.

#### Phase 1.Stage 2: Define Config And Selection Policy

##### Phase 1.Stage 2.Action 1: Implement candidate discovery config

Action:

- create `config.py`;
- define:
  - artifact root;
  - run label;
  - schema sweep source;
  - locked-by;
  - clean candidate cap;
  - warning candidate cap;
  - degeneracy anchor cap;
  - allow warning selection flag;
  - linearization mode.

Completion criteria:

- selection policy knobs are explicit and budget-lockable.

Stop condition:

- stop if candidate cap defaults are not approved for execution.

##### Phase 1.Stage 2.Action 2: Implement policy manifest model

Action:

- create `policy.py`;
- define `plate_support_candidate_selection_policy_v001` with policy priorities
  from the blueprint.

Completion criteria:

- policy can be serialized into `candidate_selection_policy_manifest.json`.

Stop condition:

- stop if policy requires unresolved Project Owner choices.

### Phase 2: Stage 2 Source Loading

#### Phase 2.Stage 1: Parse Schema Sweep Source

##### Phase 2.Stage 1.Action 1: Implement Stage 2 source loader

Action:

- create `stage2_source.py`;
- load Stage 2 `readout_source.json`;
- resolve required Stage 2 result tables.

Completion criteria:

- loader returns validated paths to every required table.

Stop condition:

- stop if source binding is not repo-resident.

##### Phase 2.Stage 1.Action 2: Validate required Stage 2 files and columns

Action:

- require:
  - `schema_candidate_signal_summary.csv`;
  - `schema_arm_summary.csv`;
  - `schema_construction_summary.csv`;
  - `tower_shape_summary.csv`;
  - `tier_executability_summary.csv`;
  - `collapse_diagnostic_summary.csv`;
  - `stage_aggregate_summary.json`.

Completion criteria:

- missing or malformed inputs produce controlled block rows.

Stop condition:

- stop if Stage 2 tables do not contain source row identifiers.

#### Phase 2.Stage 2: Preserve Stage 1 Context

##### Phase 2.Stage 2.Action 1: Extract Stage 1 contextual facts

Action:

- read Stage 1 context through Stage 2 provenance or explicit Stage 2 summary
  fields:
  - valid state count;
  - valid non-self edge count;
  - shortest path length;
  - default schema max depth;
  - flat schema max depth.

Completion criteria:

- context appears in candidate manifests where relevant.

Stop condition:

- stop if context cannot be traced through source manifests.

### Phase 3: Candidate Classification

#### Phase 3.Stage 1: Normalize Stage 2 Signal Rows

##### Phase 3.Stage 1.Action 1: Create normalized candidate input rows

Action:

- create `eligibility.py`;
- normalize Stage 2 rows into a common candidate-input structure keyed by
  schema id, schema family id, schema seed, and source row id.

Completion criteria:

- every Stage 2 signal row has a normalized input row.

Stop condition:

- stop if Stage 2 rows cannot be uniquely keyed.

##### Phase 3.Stage 1.Action 2: Verify source trace completeness

Action:

- check every input row has source artifact root, source stage id, environment
  instance id, linearization mode, and source row id.

Completion criteria:

- rows with missing source metadata become `blocked_missing_source`.

Stop condition:

- stop if source trace cannot be preserved at all.

#### Phase 3.Stage 2: Implement Candidate Classifier

##### Phase 3.Stage 2.Action 1: Classify selected training candidates

Action:

- classify clean candidates that satisfy:
  - non-control schema;
  - structural class `nonflat_structured`;
  - max depth > 1;
  - not full first-projection collapse;
  - nonzero executable action surface;
  - complete construction metadata;
  - valid source paths.

Completion criteria:

- eligible clean candidates are identified before cap selection.

Stop condition:

- stop if required fields are missing from Stage 2 tables.

##### Phase 3.Stage 2.Action 2: Classify warning candidates

Action:

- classify warning candidates for near-full collapse, sparse action surface,
  shallow non-flat tower, or schema-family uncertainty.

Completion criteria:

- warning reason is explicit.

Stop condition:

- stop if warning criteria are not evidence-backed.

##### Phase 3.Stage 2.Action 3: Classify controls, degeneracy anchors, and blocked candidates

Action:

- classify:
  - no-contraction or known-flat controls as `selected_control_anchor`;
  - pathological schemas as `selected_degeneracy_anchor`;
  - flat/collapsed/unexecutable/construction-failed/missing-source rows as
    blocked classes.

Completion criteria:

- no Stage 2 row is dropped.

Stop condition:

- stop if blocked candidates would be omitted from output.

### Phase 4: Eligibility Scoring And Deterministic Selection

#### Phase 4.Stage 1: Implement Eligibility Score

##### Phase 4.Stage 1.Action 1: Implement score components

Action:

- implement deterministic score components from the blueprint:
  - positive points for non-flat structure, executable surface, non-collapse,
    diversity, upstream continuity;
  - penalties for near/full collapse, zero executable actions, missing
    metadata.

Completion criteria:

- score is written as selection metadata only.

Stop condition:

- stop if scoring is interpreted as performance evidence.

##### Phase 4.Stage 1.Action 2: Add score explanation

Action:

- produce an `eligibility_reason` field explaining score components.

Completion criteria:

- human readout can explain why a candidate was selected or not.

Stop condition:

- stop if explanation would require inventing information absent from Stage 2.

#### Phase 4.Stage 2: Select Candidate Sets

##### Phase 4.Stage 2.Action 1: Select control anchor

Action:

- select no-contraction control anchor if present.

Completion criteria:

- control anchor appears in `control_anchor_summary.csv`.

Stop condition:

- stop if no-contraction arm is absent from Stage 2.

##### Phase 4.Stage 2.Action 2: Select clean training candidates

Action:

- select up to configured clean candidate cap, preferring family diversity and
  score.

Completion criteria:

- selected clean candidates have deterministic order.

Stop condition:

- stop if stable deterministic sorting cannot be defined.

##### Phase 4.Stage 2.Action 3: Select warning candidate if policy allows

Action:

- select at most one warning candidate when allowed by config or when no clean
  candidate exists and policy records the warning.

Completion criteria:

- warning candidate has role `selected_warning_candidate`.

Stop condition:

- stop if warning selection would authorize training without later budget-lock
  acknowledgement.

##### Phase 4.Stage 2.Action 4: Select degeneracy anchor

Action:

- select at most one degeneracy anchor for interpretability.

Completion criteria:

- degeneracy anchor is not marked eligible for normal Stage 4 training.

Stop condition:

- stop if degeneracy anchor would be promoted as a training candidate.

### Phase 5: Candidate IDs And Manifest

#### Phase 5.Stage 1: Stable Candidate IDs

##### Phase 5.Stage 1.Action 1: Implement candidate ID builder

Action:

- create `candidate_ids.py`;
- implement deterministic ids:

```text
plate_support_candidate:<schema_family_id>:<schema_seed>:<short_hash>
```

Completion criteria:

- same input row produces same candidate id across runs.

Stop condition:

- stop if source row data is insufficient for stable hashing.

##### Phase 5.Stage 1.Action 2: Test candidate ID stability

Action:

- add tests for deterministic ids and collision avoidance on representative
  rows.

Completion criteria:

- candidate id instability fails tests.

Stop condition:

- stop if hash inputs include nondeterministic paths or timestamps.

#### Phase 5.Stage 2: Build Candidate Manifest

##### Phase 5.Stage 2.Action 1: Populate candidate manifest rows

Action:

- create `candidate_manifest.json` with fields from the blueprint.

Completion criteria:

- each selected/blocked/control/degeneracy candidate has complete row data.

Stop condition:

- stop if required source trace fields are unavailable.

##### Phase 5.Stage 2.Action 2: Assign allowed downstream stages

Action:

- set allowed downstream stages:
  - selected training candidates -> Stage 4;
  - selected warning candidates -> Stage 4 only with warning authorization;
  - control anchors -> diagnostic/control use;
  - degeneracy anchors -> diagnostic-only unless explicitly overridden;
  - blocked candidates -> none.

Completion criteria:

- Stage 4 can enforce training gate from manifest fields.

Stop condition:

- stop if allowed downstream semantics are ambiguous.

### Phase 6: Artifact Writing And Aggregation

#### Phase 6.Stage 1: Write Manifests

##### Phase 6.Stage 1.Action 1: Write Stage 3 manifests

Action:

- write:
  - `stage_manifest.json`;
  - `stage_budget_lock.json`;
  - `stage_input_manifest.json`;
  - `candidate_selection_policy_manifest.json`;
  - `candidate_manifest.json`;
  - `parent_schema_sweep_manifest.json`.

Completion criteria:

- candidate selection is fully traceable to Stage 2.

Stop condition:

- stop if parent schema sweep manifest is missing source artifact paths.

#### Phase 6.Stage 2: Write Result Tables

##### Phase 6.Stage 2.Action 1: Write candidate summary tables

Action:

- write:
  - `candidate_eligibility_summary.csv`;
  - `selected_candidate_summary.csv`;
  - `blocked_candidate_summary.csv`;
  - `control_anchor_summary.csv`;
  - `degeneracy_anchor_summary.csv`;
  - `candidate_source_trace.csv`;
  - `downstream_training_health_input_summary.csv`.

Completion criteria:

- every Stage 2 row appears in at least one candidate output classification.

Stop condition:

- stop if blocked rows are lost.

##### Phase 6.Stage 2.Action 2: Write aggregate files

Action:

- write:
  - `stage_aggregate_summary.json`;
  - `stage_aggregate_table.csv`;
  - `stage_run_index.csv`.

Completion criteria:

- pass/warning/block criteria are encoded.

Stop condition:

- stop if candidate count is ambiguous.

### Phase 7: Readout Binding And Docs

#### Phase 7.Stage 1: Create Stage 3 Readout Source

##### Phase 7.Stage 1.Action 1: Write `readout_source.json`

Action:

- create:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/candidate_discovery/readout_source.json
```

Completion criteria:

- source binding lists candidate manifest, required tables, goal sources,
  methodology sources, expected files, and claim boundary.

Stop condition:

- stop if readout source would need to infer candidate policy from code.

##### Phase 7.Stage 1.Action 2: Write seed human docs

Action:

- write or update:
  - `README.md`;
  - `method.md`;
  - `artifact_index.md`;
  - `runbook.md`;
  - `results/summary.md`.

Completion criteria:

- docs explain selection and non-performance claim boundary.

Stop condition:

- stop if docs imply selected candidates have trained or won.

### Phase 8: CLI Integration

#### Phase 8.Stage 1: Add Candidate Discovery Commands

##### Phase 8.Stage 1.Action 1: Add run command

Action:

- add `plate-support standard-gauntlet candidate-discovery run`.

Completion criteria:

- command accepts explicit artifact root and schema-sweep source.

Stop condition:

- stop if command infers "latest schema sweep" implicitly.

##### Phase 8.Stage 1.Action 2: Add summarize/inspect command if consistent

Action:

- add an inspect/summarize command only if it matches existing CLI patterns.

Completion criteria:

- command reads candidate artifacts and prints selection status.

Stop condition:

- stop if summarize would regenerate selection under a different policy.

### Phase 9: Tests And Verification

#### Phase 9.Stage 1: Unit Tests

##### Phase 9.Stage 1.Action 1: Test source validation

Action:

- test missing Stage 2 source, malformed candidate signal table, and outside-repo
  source paths.

Completion criteria:

- invalid inputs block cleanly.

Stop condition:

- stop if validation cannot distinguish malformed from no-data.

##### Phase 9.Stage 1.Action 2: Test every row is classified

Action:

- test representative Stage 2 rows for all candidate classes.

Completion criteria:

- unclassified rows fail tests.

Stop condition:

- stop if class criteria are underspecified.

##### Phase 9.Stage 1.Action 3: Test selection caps and stable ordering

Action:

- test clean, warning, and degeneracy caps plus deterministic tie-breaking.

Completion criteria:

- repeated runs select the same candidates.

Stop condition:

- stop if tie-breaking relies on unordered input iteration.

##### Phase 9.Stage 1.Action 4: Test downstream gate

Action:

- test Stage 4 gate fields in `downstream_training_health_input_summary.csv`.

Completion criteria:

- selected training candidate count is machine-readable.

Stop condition:

- stop if warning authorization cannot be represented.

#### Phase 9.Stage 2: Runtime Smoke

##### Phase 9.Stage 2.Action 1: Run Stage 3 smoke command

Action:

- run candidate discovery against a repo-local Stage 2 smoke source.

Completion criteria:

- artifacts and candidate manifest are produced or controlled block status is
  written.

Stop condition:

- stop on unexpected exception or path drift.

##### Phase 9.Stage 2.Action 2: Inspect candidate manifest

Action:

- verify selected, blocked, control, and degeneracy rows are present as
  applicable.

Completion criteria:

- no Stage 2 candidate-signal rows are silently discarded.

Stop condition:

- stop if candidate source trace is incomplete.

#### Phase 9.Stage 3: Final Log Update

##### Phase 9.Stage 3.Action 1: Record validation and Stage 4 handoff

Action:

- update implementation log with:
  - selection policy;
  - selected candidates;
  - blocked candidates;
  - warning/degeneracy handling;
  - tests run;
  - Stage 4 input paths.

Completion criteria:

- log says whether Stage 4 may proceed.

Stop condition:

- stop if Stage 4 would need to infer candidate intent.

## Completion Criteria For The Component

Stage 3 is complete when:

- Stage 2 source validation exists;
- every Stage 2 signal row is classified;
- candidate selection policy manifest exists;
- deterministic candidate IDs exist;
- candidate manifest and all required result tables exist;
- downstream training-health input summary exists;
- readout source and seed docs exist;
- CLI/run surface exists or omission is recorded;
- tests pass;
- implementation log records Phase.Stage.Action completion.

## Handoff To Next Component

Tower training health must consume:

```text
candidate_manifest.json
results/selected_candidate_summary.csv
results/downstream_training_health_input_summary.csv
results/candidate_source_trace.csv
stage_manifest.json
readout_source.json
```

Tower training health must not train candidates absent from the Stage 3
manifest unless the Project Owner explicitly approves a diagnostic override.
