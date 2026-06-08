# BBB v0.7.2 Pointwise Liftability Integration Implementation Workplan

Date: 2026-06-04

Status: implementation workplan, not executed

Repository:

```text
<repo-root>
```

Source blueprint:

```text
docs/design/state_collapser_v072_pointwise_liftability_handoff/01_001_bbb_v072_pointwise_liftability_integration_blueprint.md
```

Required implementation log:

```text
docs/design/state_collapser_v072_pointwise_liftability_handoff/01_003_bbb_v072_pointwise_liftability_integration_implementation_log.md
```

## Purpose

This workplan translates the BBB `state_collapser` `v0.7.2` pointwise
liftability integration blueprint into exact `Phase.Stage.Action`
implementation work.

The work updates BBB so that new affected counterpoint tower-control reruns use
pointwise executable liftability by default, while preserving old evaluation
artifacts as historical evidence.

The core corrected runtime rule is:

```text
An abstract tier/action pair is executable for the current runtime step only
when the selected action cell has at least one concrete edge whose source is
the current concrete/base state.
```

The implementation must be anchored to the upstream `state_collapser` `v0.7.2`
APIs:

```text
PartitionTower.executable_lift_candidates(...)
PartitionTower.tier_is_executable_from_state(...)
PartitionTower.invariant_report(...)
PartitionTower.assert_consistent(...)
```

## Execution Authority Status

This document is not source-code implementation approval.

The Project Owner requested this workplan with:

```text
I agree with all your recommendations here:
`docs/design/state_collapser_v072_pointwise_liftability_handoff/01_001_bbb_v072_pointwise_liftability_integration_blueprint.md`
Make Pahse.Stage.Action workplan following `prime_directive`
```

Therefore this document may be created now.

Source-code, test, CLI, artifact-schema, readout, and benchmark-run execution
must not begin until the Project Owner explicitly asks to execute this exact
workplan.

If the Project Owner later says to execute this workplan, implementation must
follow this document in order. If any `Phase.Stage.Action` item cannot be
implemented as written, the implementing consultant must stop and ask for
Project Owner guidance before substituting, simplifying, or reordering.

## Source Authority

This workplan follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/git_practices.md`
- `docs/prime_directive/common_failure_mode_001.md`
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`
- `docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md`
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`
- `docs/design/state_collapser_v072_pointwise_liftability_handoff/state_collapser_pointwise_liftability_diagnostic_report.md`
- `docs/design/state_collapser_v072_pointwise_liftability_handoff/state_collapser_pointwise_liftability_github_issue.md`
- `docs/design/state_collapser_v072_pointwise_liftability_handoff/big_boy_benchmarking_synthetic_blow_revisions_02_handoff.md`
- `docs/design/state_collapser_v072_pointwise_liftability_handoff/01_001_bbb_v072_pointwise_liftability_integration_blueprint.md`

## Project Owner Attribution Preservation

This workplan does not invent Project Owner turns.

Project Owner-originated correction carried into implementation:

1. Quotient-level action availability is not pointwise executable liftability.
2. A lift must be executable from the current concrete/base state, not merely
   from some representative or some preimage state.
3. Existing evaluation artifacts must not be trashed or silently reinterpreted.
4. The new integration should become default for new reruns.
5. Affected evaluations require explicit new artifact roots/readout
   regeneration.

The Project Owner approved all consultant recommendations in the source
blueprint. This resolves the blueprint's open recommendations as follows:

1. The first corrected durable rerun target is:

   ```text
   second_serious_schema_comparison
   ```

2. The first corrected durable artifact label is:

   ```text
   v072_pointwise_001
   ```

3. Historical README archiving is required only when the old README contains
   substantial conversation or interpretive discussion that would otherwise be
   overwritten. Otherwise, preserving old raw artifact roots plus writing clear
   supersession/provenance language is enough.

## Fixed Design Locks

### Dependency Lock

Use `state_collapser` `v0.7.2`.

Do not edit:

```text
<state-collapser-repo>
```

If a needed fix appears to belong upstream, stop and document the exact BBB
evidence rather than editing the upstream repo.

### Runtime Semantics Lock

New affected counterpoint tower-control reruns must use:

```text
liftability_semantics_id = "state_collapser_v072_pointwise"
```

The strict execution query is:

```text
PartitionTower.executable_lift_candidates(tier, action_cell, current_core_state)
```

The strict tier-executable query is:

```text
PartitionTower.tier_is_executable_from_state(tier, current_core_state)
```

### Artifact Provenance Lock

Do not overwrite historical artifact roots.

Corrected reruns must use repo-resident artifact roots. The first corrected
durable rerun must target:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/v072_pointwise_001/
```

### Readout Invocation Lock

Generated readouts must use the explicit protocol command surface:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-readout-surface>/readout_source.json
```

Do not use the older folder-only wording as the canonical command.

### Compatibility Lock

Add clearer artifact fields where needed, but do not perform a broad artifact
schema migration unless this exact workplan says so.

If old fields remain, their generated prose must state their current meaning
under `state_collapser` `v0.7.2`.

## Global Stop Conditions

During execution, stop and ask the Project Owner if any of the following occur:

1. `state_collapser` is not actually importable as version `0.7.2`.
2. `PartitionTower.executable_lift_candidates(...)` is missing or behaves
   contrary to the pointwise semantics required by the blueprint.
3. `PartitionTower.tier_is_executable_from_state(...)` is missing or behaves
   contrary to the pointwise semantics required by the blueprint.
4. A `Phase.Stage.Action` item would require editing `<state-collapser-repo>`.
5. A `Phase.Stage.Action` item would require deleting or rewriting historical
   evaluation artifacts.
6. A `Phase.Stage.Action` item would require silently weakening the plan.
7. A test fixture cannot demonstrate quotient-vs-pointwise mismatch without a
   substitute that changes the semantics.
8. A serious corrected rerun lacks the needed candidate source or threshold
   value.
9. Broad readout regeneration would erase substantial conversation that has not
   been archived.
10. Any implementation action conflicts with the Prime Directive.

## Required Branch Discipline

Before source or test edits, create or switch to a dedicated implementation
branch:

```text
codex/bbb-v072-pointwise-liftability
```

If a branch with that name already exists, inspect it before use and record the
decision in the implementation log.

Do not execute this workplan directly on `main` unless the Project Owner
explicitly overrides branch discipline.

## Required Implementation Log

Create and maintain:

```text
docs/design/state_collapser_v072_pointwise_liftability_handoff/01_003_bbb_v072_pointwise_liftability_integration_implementation_log.md
```

The log must record:

- branch name;
- starting git status;
- current `state_collapser` version and API signature observations;
- each completed `Phase.Stage.Action`;
- every test command and result;
- every rerun command and artifact root;
- any invariant report failures;
- any old README/archive decision;
- final status and merge guidance.

## Phase.Stage.Action Workplan

## Phase 0. Stage 0. Action 1: Re-read Authority Documents

Before implementation, re-read:

```text
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
docs/prime_directive/git_practices.md
docs/design/state_collapser_v072_pointwise_liftability_handoff/01_001_bbb_v072_pointwise_liftability_integration_blueprint.md
```

Record in the implementation log that this re-read happened.

Verification:

- log entry exists;
- no source files are edited yet.

## Phase 0. Stage 0. Action 2: Inspect Git State

Run:

```text
git status --short --branch
```

Record the starting branch, ahead/behind state, and dirty/untracked files in
the implementation log.

If unrelated dirty files exist, preserve them and work around them. Do not
revert user changes.

Verification:

- implementation log contains starting git status;
- no unrelated files are modified.

## Phase 0. Stage 0. Action 3: Create Implementation Branch

Create or switch to:

```text
codex/bbb-v072-pointwise-liftability
```

Use non-interactive git commands.

Verification:

- `git status --short --branch` reports the implementation branch;
- implementation log records the branch transition.

## Phase 0. Stage 0. Action 4: Create Implementation Log

Create:

```text
docs/design/state_collapser_v072_pointwise_liftability_handoff/01_003_bbb_v072_pointwise_liftability_integration_implementation_log.md
```

The log must include sections:

```text
# BBB v0.7.2 Pointwise Liftability Integration Implementation Log
Starting State
Phase.Stage.Action Completion Log
API Reconnaissance
Invariant Reports
Artifact And Readout Decisions
Test Results
Rerun Results
Surprises And Stop Conditions
Final Audit
```

Verification:

- log file exists;
- log file names this workplan and source blueprint.

## Phase 0. Stage 1. Action 1: Verify Dependency Version And API Signatures

Run a local API probe using `uv run python`.

Verify:

```text
state_collapser.__version__ == "0.7.2"
PartitionTower.invariant_report exists
PartitionTower.assert_consistent exists
PartitionTower.executable_lift_candidates exists
PartitionTower.tier_is_executable_from_state exists
```

Record exact signatures in the implementation log.

Verification:

- log contains observed signatures;
- stop if any required surface is absent.

## Phase 0. Stage 1. Action 2: Inspect Current Counterpoint Integration Points

Re-read the current implementation files before editing:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/runner.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/runner.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/runner.py
```

Record the exact current weak uses of:

```text
outgoing_action_cells
lift_candidates
tier_is_executable
candidate_count
active_action_cell_count
raw_historical_action_cell_record_count
```

Verification:

- implementation log lists the exact file/function locations to be edited.

## Phase 1. Stage 0. Action 1: Strengthen Dependency Probe Constants

Update:

```text
src/big_boy_benchmarking/upstream/state_collapser.py
```

Add dependency-state checks for required `PartitionTower` methods:

```text
invariant_report
assert_consistent
executable_lift_candidates
tier_is_executable_from_state
```

The probe may represent these as a new tuple such as:

```text
REQUIRED_TOWER_PARTITION_METHODS
```

and new dataclass fields such as:

```text
tower_partition_method_status
tower_partition_methods
```

Do not remove existing symbol checks.

Verification:

- dependency-state collection reports the required methods;
- missing methods produce a clear non-`ok` status.

## Phase 1. Stage 0. Action 2: Add Dependency Probe Tests

Update:

```text
tests/upstream/test_state_collapser_dependency_state.py
```

Assert:

```text
state.import_version == "0.7.2"
state.tower_partition_import_status == "ok"
state.tower_partition_method_status == "ok"
PartitionTower method set includes executable_lift_candidates
PartitionTower method set includes tier_is_executable_from_state
PartitionTower method set includes invariant_report
PartitionTower method set includes assert_consistent
```

Verification:

```text
uv run pytest tests/upstream/test_state_collapser_dependency_state.py
```

## Phase 1. Stage 1. Action 1: Add Minimal Upstream Pointwise Liftability Test

Create or extend a BBB upstream/counterpoint test file, preferably:

```text
tests/upstream/test_state_collapser_dependency_state.py
```

or a new focused test:

```text
tests/upstream/test_state_collapser_pointwise_liftability.py
```

The test must construct a small upstream partition tower that demonstrates:

```text
quotient outgoing action cell exists
executable_lift_candidates returns empty for an unsupported current base state
executable_lift_candidates returns nonempty for a supported current base state
tier_is_executable_from_state agrees with the pointwise result
```

This test should encode the Project Owner's simplex-style correction as
executable evidence.

Verification:

```text
uv run pytest tests/upstream/test_state_collapser_pointwise_liftability.py
```

or the exact updated upstream test path.

Stop if a faithful fixture cannot be created without changing the issue's
semantics.

## Phase 2. Stage 0. Action 1: Add Liftability Semantics Constant

Add a stable local BBB constant for the corrected semantics.

Preferred location:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
```

or a shared counterpoint constants module if implementation discovers one is
more appropriate.

Required value:

```text
STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID = "state_collapser_v072_pointwise"
```

Verification:

- affected metadata, diagnostics, and readouts can import one canonical
  semantics ID;
- no duplicate string constants are introduced in separate files without
  explanation.

## Phase 2. Stage 0. Action 2: Add Invariant Report Serialization Helpers

Update:

```text
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
```

Add local serialization helpers for `PartitionInvariantReport` and issues.

Required helper behavior:

```text
input: PartitionInvariantReport
output: JSON-serializable dict
fields: ok, allow_dirty, issue_count, issues
issue fields: tier, code, message, state_cell_id, action_collection_id,
              action_cell_id, edge_id
```

Use `repr(...)` or string conversion for IDs.

Do not assume `PartitionInvariantReport.to_dict()` exists.

Verification:

- helper returns `{"ok": true, "issue_count": 0, "issues": []}` for a clean
  tower;
- helper can serialize at least one synthetic issue object if feasible.

## Phase 2. Stage 0. Action 3: Add Counterpoint Tower Consistency Helpers

Update:

```text
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
```

Add helpers:

```text
collect_counterpoint_tower_invariant_report(build, allow_dirty=False)
assert_counterpoint_tower_consistent(build, allow_dirty=False)
```

The assertion helper must call upstream `tower.assert_consistent(...)`.

The collection helper must call upstream `tower.invariant_report(...)` and
serialize it locally.

Verification:

- clean counterpoint tower build produces `ok == true`;
- failed invariant reports, if simulated, are not silently swallowed.

## Phase 2. Stage 0. Action 4: Add Invariant Helper Tests

Add tests covering:

```text
build_counterpoint_partition_tower(...).tower invariant report is ok
build_counterpoint_noisy_rate_partition_tower(...).tower invariant report is ok
serialized invariant report includes ok, issue_count, and issues
```

Suggested test file:

```text
tests/environments/counterpoint/test_tower_adapter.py
```

Verification:

```text
uv run pytest tests/environments/counterpoint/test_tower_adapter.py
```

## Phase 3. Stage 0. Action 1: Add Quotient And Pointwise Adapter Vocabulary Helpers

Update:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
```

On `CounterpointTowerControlAdapter`, add helpers equivalent to:

```text
quotient_action_cells(tier)
representative_lift_candidates(tier, action_cell)
executable_lift_candidates(tier, action_cell)
pointwise_executable_action_cells(tier)
quotient_action_cell_count(tier)
pointwise_executable_action_cell_count(tier)
```

Required semantics:

- `quotient_action_cells` calls `tower.outgoing_action_cells(...)` for the
  current tier state;
- `executable_lift_candidates` calls
  `tower.executable_lift_candidates(tier, action_cell, current_core_state)`;
- `pointwise_executable_action_cells` preserves quotient ordering and filters
  out action cells with no strict executable lift candidates;
- methods return empty tuples if current state/core state/tier state is absent.

Verification:

- helper tests prove ordering is preserved;
- helper tests prove pointwise vocabulary is a subset of quotient vocabulary.

## Phase 3. Stage 0. Action 2: Replace Adapter Tier Executability

Update:

```text
CounterpointTowerControlAdapter.tier_is_executable
```

Replace the weak quotient-level predicate with:

```text
tower.tier_is_executable_from_state(tier, current_core_state)
```

Required behavior:

- invalid tier returns `False`;
- missing current core state returns `False`;
- valid tier delegates to upstream pointwise method;
- quotient-level nonemptiness is not used for controller executability.

Verification:

- tests show `tier_is_executable` matches upstream pointwise method;
- tests preserve false for negative/out-of-range tiers.

## Phase 3. Stage 0. Action 3: Update Learner Action Vocabulary And Masks

Update:

```text
CounterpointTierLearner._action_vocabulary
CounterpointTierLearner._action_input
```

Required behavior:

- learner action vocabulary uses `adapter.pointwise_executable_action_cells(tier)`;
- `ActionSelectionInput.action_mask` exposes only pointwise executable cells;
- diagnostics include:

  ```text
  liftability_semantics_id
  quotient_action_vocabulary
  pointwise_action_vocabulary
  quotient_action_cell_count
  pointwise_executable_action_cell_count
  ```

- action count remains compatible with the learner's existing tabular action
  count approach.

Verification:

- tests assert the mask is empty when pointwise vocabulary is empty;
- tests assert quotient diagnostics can be nonempty while pointwise diagnostics
  are empty in a synthetic mismatch fixture.

## Phase 3. Stage 0. Action 4: Update Max Tier Action Count Without Weakening Masks

Review and update:

```text
CounterpointTierLearner._tier_action_count
_max_tier_action_count
```

Required rule:

```text
The maximum action count may remain a stable upper bound, but the runtime mask
must be pointwise filtered.
```

If the implementation uses quotient counts as an upper bound, document that
choice in code or tests.

If the implementation computes a stricter pointwise maximum, prove it does not
depend on only the current episode state in a misleading way.

Verification:

- learner initialization succeeds for all tiers;
- action masks prevent out-of-vocabulary execution.

## Phase 3. Stage 1. Action 1: Update LiftResolveTrace

Update:

```text
LiftResolveTrace
```

Add fields sufficient to distinguish:

```text
representative_candidate_count
pointwise_candidate_count
selected_lift_index
selected_lift_source_matches_current
selected_lift_target_repr
liftability_semantics_id
```

Keep existing fields where downstream code expects them.

For new semantics:

```text
candidate_count == pointwise_candidate_count
```

Verification:

- existing lift event row writers still work after updates;
- tests cover success and failure trace creation.

## Phase 3. Stage 1. Action 2: Replace Executor Lift Query

Update:

```text
CounterpointLiftResolveExecutor._execute
```

Required execution flow:

1. fetch pointwise executable vocabulary from the adapter;
2. reject invalid action indices against pointwise vocabulary;
3. call `adapter.executable_lift_candidates(tier, action_cell)`;
4. do not use `tower.lift_candidates(...)` for execution;
5. do not fallback to `action_cell_members(...)` for execution;
6. choose the first strict executable lift candidate by default;
7. record representative candidate count only as diagnostic evidence.

Verification:

- tests fail if representative-only candidates are used for execution;
- `no_lift_candidate_from_current_state` cannot occur after a pointwise mask
  selected the action unless the upstream strict query changes between mask and
  execution.

## Phase 3. Stage 1. Action 3: Preserve Representative Diagnostics

Add representative diagnostic counts without using them for execution.

Required evidence:

```text
representative_candidate_count
pointwise_candidate_count
quotient_action_cell_count
pointwise_executable_action_cell_count
```

Verification:

- lift event rows can explain quotient/representative availability separately
  from strict executable liftability;
- runtime execution still uses pointwise candidates.

## Phase 3. Stage 2. Action 1: Add Adapter And Executor Tests

Update or add tests in:

```text
tests/environments/counterpoint/test_serious_learning_tower_control.py
```

Required tests:

- `tier_is_executable` delegates to current-base-state pointwise semantics;
- pointwise vocabulary is subset of quotient vocabulary;
- learner mask uses pointwise vocabulary;
- executor calls strict executable lift candidates;
- executor does not use representative fallback;
- failure traces record pointwise semantics ID.

Verification:

```text
uv run pytest tests/environments/counterpoint/test_serious_learning_tower_control.py
```

## Phase 4. Stage 0. Action 1: Extend Serious Learning Event Rows

Update:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/events.py
```

Extend `LiftFiberEventRow` with add-only/default-compatible fields for:

```text
liftability_semantics_id
representative_candidate_count
pointwise_candidate_count
selected_lift_index
selected_lift_source_matches_current
selected_lift_target_repr
quotient_action_cell_count
pointwise_executable_action_cell_count
```

If dataclass default ordering prevents direct add-only changes, update writer
call sites and tests together. Do not leave placeholder fields unwritten.

Verification:

- serious learning event row fieldnames include the new fields;
- existing serious learning tests pass after writer updates.

## Phase 4. Stage 0. Action 2: Extend Diagnostic Event Rows

Update event rows for affected evaluations:

```text
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/events.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/events.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/events.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/events.py
```

For lift rows, add the same pointwise/representative fields as serious
learning.

For tier signal or tower-shape rows, add fields where the data is well-defined:

```text
liftability_semantics_id
quotient_action_cell_count
pointwise_executable_action_cell_count
executable_semantics
raw_action_cell_storage_count
```

Do not write a pointwise count into a static tower-shape table unless the row
has a clearly defined current base state or explicitly says it is an
initial-state or runtime-aggregated count.

Verification:

- event row fieldnames match updated writers;
- no row fabricates a pointwise count without a current-state interpretation.

## Phase 4. Stage 0. Action 3: Update Event Row Writers

Update all construction sites for modified rows in:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/runner.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/runner.py
```

Required behavior:

- write `liftability_semantics_id` on all affected lift/control/tier rows;
- write pointwise candidate counts from strict executable queries;
- write representative counts from representative queries only for diagnostics;
- preserve old `candidate_count` with new meaning:

  ```text
  candidate_count == pointwise_candidate_count
  ```

Verification:

- updated tests inspect generated CSV headers and at least one row value.

## Phase 4. Stage 1. Action 1: Add Invariant Report Artifacts

For affected tower-control run families, write an invariant report artifact
outside timed hot loops.

Recommended file name:

```text
tower_invariant_report.json
```

Place it somewhere discoverable per run or evaluation family. Preferred:

```text
<run-root>/artifacts/tower_invariant_report.json
```

or the nearest existing run artifact directory if the evaluation uses a
different layout.

Required content:

```text
ok
allow_dirty
issue_count
issues
state_collapser_version
liftability_semantics_id
```

Verification:

- tests assert the artifact exists for at least one affected runner;
- readout source or manifest lists the artifact where relevant.

## Phase 4. Stage 1. Action 2: Add Invariant Failure Handling

For affected long-running evaluation runners:

- if invariant report is not ok before the run, mark the run failed or
  incomplete;
- write the invariant report;
- avoid producing misleading success rows;
- record failure reason such as:

  ```text
  tower_invariant_failed
  ```

In tests and explicit low-level diagnostics, fail fast with
`assert_counterpoint_tower_consistent(...)`.

Verification:

- tests cover clean invariant pass;
- tests cover failure handling if feasible with monkeypatching.

## Phase 5. Stage 0. Action 1: Propagate Pointwise Semantics To One-Third Diagnostics

Update:

```text
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/runner.py
```

Required behavior:

- use the corrected `CounterpointTowerControlAdapter` semantics;
- record pointwise liftability fields in emitted lift/control/tier rows if the
  one-third runner has separate row classes;
- ensure tier-executability summaries use the corrected predicate;
- do not change environment or schema construction.

Verification:

```text
uv run pytest tests/environments/counterpoint/test_one_third_diagnostics.py
```

## Phase 5. Stage 0. Action 2: Propagate Pointwise Semantics To Fraction Sweep Diagnostics

Update:

```text
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/events.py
```

Required behavior:

- runtime executability and lift rows use pointwise semantics;
- tower shape or equivalent summary separates quotient action support from
  pointwise executable support;
- `raw_action_cell_storage_count` is added or old raw-field prose is corrected;
- source-local contraction fraction semantics remain unchanged.

Verification:

```text
uv run pytest tests/environments/counterpoint/test_fraction_sweep_diagnostics.py
```

## Phase 5. Stage 0. Action 3: Propagate Pointwise Semantics To Noisy-Rate Diagnostics

Update:

```text
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/events.py
```

Required behavior:

- runtime executability and lift rows use pointwise semantics;
- candidate eligibility summaries include pointwise executable action evidence;
- a tower with quotient action support but no pointwise support for runtime
  states is not described as cleanly trainable;
- noisy-rate schema selection remains unchanged.

Verification:

```text
uv run pytest tests/environments/counterpoint/test_noisy_rate_diagnostics.py
```

## Phase 5. Stage 0. Action 4: Propagate Pointwise Semantics To Noisy-Rate Full Training

Update:

```text
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/runner.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/events.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/candidate_selection.py
```

Required behavior:

- full tower training uses corrected pointwise masks and lift resolution;
- candidate selection consumes pointwise executable evidence when available;
- if parent candidate data lacks pointwise fields, record a compatibility path
  and do not overclaim candidate cleanliness;
- training health summaries treat remaining lift failures as stronger
  structural evidence.

Verification:

```text
uv run pytest tests/environments/counterpoint/test_noisy_rate_full_training.py
```

## Phase 5. Stage 0. Action 5: Propagate Pointwise Semantics To Second Serious Comparison

Update:

```text
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/runner.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/events.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/aggregation.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/manifests.py
```

Required behavior:

- Schema 1 tower-control arms use corrected pointwise masks and lift
  resolution;
- Schema 0/no-contraction arms record the same semantics metadata when they run
  through tower-control paths;
- aggregation preserves pointwise candidate and lift-failure evidence;
- manifests point to this blueprint and this workplan as method sources;
- generated `readout_source.json` records `liftability_semantics_id`.

Verification:

```text
uv run pytest tests/environments/counterpoint/test_second_serious_comparison.py
```

## Phase 6. Stage 0. Action 1: Update Readout Source Bindings And Manifest Payloads

Update affected manifest/source-binding code so generated readout sources
include:

```text
liftability_semantics_id
state_collapser_version
tower_invariant_report expected file information
pointwise lift/candidate fields in expected-file context
```

Affected likely files:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/docs_writer.py
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/docs_writer.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/docs_writer.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/docs_writer.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/docs_writer.py
src/big_boy_benchmarking/environments/counterpoint/**/manifests.py
```

Verification:

- generated `readout_source.json` for second-serious smoke includes
  `liftability_semantics_id`;
- expected files mention invariant report artifacts where generated.

## Phase 6. Stage 0. Action 2: Update Human-Facing Methodology Text

Update docs writers so affected READMEs include this content in natural,
reader-facing language:

```text
This run used state_collapser v0.7.2 pointwise liftability semantics. Tower
action masks and tier executability were based on executable concrete lifts
from the current base state, not merely quotient-level outgoing action cells.
```

Also include:

- what quotient action availability means;
- what pointwise executable liftability means;
- whether invariant preflight passed;
- whether `no_lift_candidate_from_current_state` appears;
- why old runs are historical if mentioned.

Verification:

- docs writer tests inspect generated README content for the pointwise
  methodology statement.

## Phase 6. Stage 0. Action 3: Update Badge And Status Support

For affected generated readouts, add badge/status support for:

```text
Liftability Semantics
Invariant Preflight
Lift Failures
```

Do not use remote badge services.

Use local SVG badge generation consistent with existing readout protocol.

Verification:

- docs writer tests verify local badge files exist where the readout supports
  badges;
- README badge bullets agree with detailed verdict.

## Phase 6. Stage 0. Action 4: Preserve Protected Turn Sections

When updating generated README logic, preserve the protocol requirement:

- do not rewrite existing Project Owner / Evaluator turns;
- do not rewrite existing Embedded Engineering Consultant / Codex turns;
- append blank turn pairs only according to the readout protocol.

Verification:

- if a docs-writer test fixture has a turn section, regeneration preserves it.

## Phase 7. Stage 0. Action 1: Run Focused Unit Tests

Run focused tests after implementation:

```text
uv run pytest tests/upstream/test_state_collapser_dependency_state.py
uv run pytest tests/upstream/test_state_collapser_pointwise_liftability.py
uv run pytest tests/environments/counterpoint/test_tower_adapter.py
uv run pytest tests/environments/counterpoint/test_serious_learning_tower_control.py
uv run pytest tests/environments/counterpoint/test_one_third_diagnostics.py
uv run pytest tests/environments/counterpoint/test_fraction_sweep_diagnostics.py
uv run pytest tests/environments/counterpoint/test_noisy_rate_diagnostics.py
uv run pytest tests/environments/counterpoint/test_noisy_rate_full_training.py
uv run pytest tests/environments/counterpoint/test_second_serious_comparison.py
```

If a test path does not exist because implementation placed tests elsewhere,
record the actual path in the implementation log.

Verification:

- all focused tests pass;
- failures are fixed or the exact blocking Phase.Stage.Action is recorded.

## Phase 7. Stage 0. Action 2: Run Full Pytest Suite

Run:

```text
uv run pytest
```

Verification:

- full test suite passes;
- implementation log records total pass/fail count.

## Phase 7. Stage 0. Action 3: Run Targeted Ruff Checks

Run Ruff on touched source and test files.

Do not use a broad Ruff run as the only signal if unrelated pre-existing
line-length debt appears.

Minimum command shape:

```text
uv run ruff check <touched src/test files>
```

Verification:

- touched files pass Ruff;
- any unrelated broad Ruff debt is not hidden or misreported.

## Phase 8. Stage 0. Action 1: Run Tiny Counterpoint Smoke

Run a tiny smoke after tests pass.

Minimum smoke:

```text
uv run python -m big_boy_benchmarking.cli counterpoint graph-diagnostics \
  --artifact-root <tmp-dir>/bbb-v072-pointwise-smoke \
  --instance-id tiny
```

Then run a small tower-control smoke through an affected CLI path, preferably
`second-serious-comparison run` with smoke settings and a temporary artifact
root, or the smallest available serious-learning tower-control command.

Verification:

- smoke command exits successfully;
- smoke output records `state_collapser` `0.7.2` where applicable;
- no durable repo readout is regenerated in this smoke action.

## Phase 8. Stage 1. Action 1: Calibrate Second Serious Corrected Threshold

Before the first durable corrected second-serious run, run calibration into a
repo-resident calibration artifact root using pointwise semantics.

Recommended calibration root:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/v072_pointwise_calibration_001/
```

Command shape:

```text
uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison calibrate \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/v072_pointwise_calibration_001 \
  --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json \
  --candidate-cap 4 \
  --instance-id medium \
  --episodes <calibration-episodes> \
  --replicates <calibration-replicates> \
  --locked-by foster \
  --linearization-mode tensor_available_disabled
```

Use existing CLI defaults for calibration episodes/replicates unless the
implementation log records a reason to override them.

Extract and record the threshold value needed for the run command.

Verification:

- calibration completes;
- threshold evidence is recorded in the implementation log;
- stop if four eligible medium candidates are not available.

## Phase 8. Stage 1. Action 2: Run First Durable Corrected Second Serious Evaluation

Run the first durable corrected rerun at:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/v072_pointwise_001/
```

Command shape:

```text
uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison run \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/v072_pointwise_001 \
  --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json \
  --candidate-cap 4 \
  --instance-id medium \
  --episodes 256 \
  --replicates <approved-replicates-or-existing-serious-default> \
  --threshold-value <threshold-from-calibration> \
  --run-mode serious_schema_comparison_first_sustained_hit \
  --serious-run-authorized \
  --locked-by foster \
  --linearization-mode tensor_available_disabled
```

Use the existing serious default replicate count unless implementation
reconnaissance shows the CLI requires an explicit value. Record the exact
command in the implementation log.

Verification:

- run completes or records a clear failure artifact;
- artifact root is repo-resident;
- artifact root is not an old historical root;
- run metadata records `liftability_semantics_id`.

## Phase 8. Stage 1. Action 3: Summarize The Corrected Rerun

Run:

```text
uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison summarize \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/v072_pointwise_001
```

Verification:

- summary completes;
- `docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/readout_source.json`
  points to the corrected artifact root;
- generated docs mention pointwise semantics and invariant preflight.

## Phase 8. Stage 1. Action 4: Apply Human-Readable Readout Protocol

Execute:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/readout_source.json
```

If the current README contains substantial conversation or interpretive
discussion, archive that material first under:

```text
docs/design/system_learning_from_evaluations/
```

If the README does not contain substantial conversation, preserving old
artifacts and writing clear supersession language is sufficient.

Verification:

- generated README is repo-side, not artifact-local only;
- README states pointwise liftability semantics;
- README does not imply old artifacts used the new semantics;
- protected turn section is present and preserved according to protocol.

## Phase 9. Stage 0. Action 1: Audit Artifacts And Source Bindings

Audit:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/readout_source.json
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/README.md
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/results/
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/v072_pointwise_001/
```

Required audit checks:

- source artifact root is inside the repo;
- expected files exist or are explicitly classified;
- no historical artifact root was deleted;
- liftability semantics ID appears in source binding/readout;
- invariant report evidence exists or is explicitly classified.

Verification:

- implementation log records audit result.

## Phase 9. Stage 0. Action 2: Update Root Documentation If Needed

Inspect root documentation:

```text
README.md
CONTRIBUTING.md
```

If they still describe old counterpoint evaluation status without the
`v0.7.2` pointwise-liftability correction, update them briefly.

Required content if updated:

- current `state_collapser` integration level;
- corrected pointwise liftability default for new reruns;
- link to corrected second-serious readout;
- reminder that older artifacts are historical unless rerun under
  `state_collapser_v072_pointwise`.

Verification:

- root docs remain brief and digestible;
- root docs do not overclaim learning conclusions.

## Phase 9. Stage 0. Action 3: Final Full Verification

Run final verification:

```text
uv run pytest
uv run ruff check <touched src/test files>
uv run python -c 'import state_collapser; print(state_collapser.__version__)'
```

If a full Ruff run is attempted and fails on unrelated existing debt, record
that separately from touched-file Ruff status.

Verification:

- full pytest passes;
- touched-file Ruff passes;
- imported `state_collapser` version is `0.7.2`.

## Phase 9. Stage 0. Action 4: Final Phase.Stage.Action Audit

Review this workplan against the implementation log.

For every action, record one status:

```text
completed as written
blocked with Project Owner guidance needed
explicitly superseded by Project Owner instruction
```

Do not mark a partially implemented or simplified action as complete.

Verification:

- implementation log contains a complete Phase.Stage.Action audit.

## Phase 9. Stage 0. Action 5: Prepare Merge Guidance

After all required actions are complete, provide the Project Owner:

- branch name;
- test summary;
- artifact/readout summary;
- files changed summary;
- any remaining risks;
- exact fast-forward merge command if appropriate.

Do not merge to `main` unless the Project Owner explicitly asks.

## Implementation Log Checklist Template

The implementation log should include a checklist with these action IDs:

```text
Phase 0. Stage 0. Action 1
Phase 0. Stage 0. Action 2
Phase 0. Stage 0. Action 3
Phase 0. Stage 0. Action 4
Phase 0. Stage 1. Action 1
Phase 0. Stage 1. Action 2
Phase 1. Stage 0. Action 1
Phase 1. Stage 0. Action 2
Phase 1. Stage 1. Action 1
Phase 2. Stage 0. Action 1
Phase 2. Stage 0. Action 2
Phase 2. Stage 0. Action 3
Phase 2. Stage 0. Action 4
Phase 3. Stage 0. Action 1
Phase 3. Stage 0. Action 2
Phase 3. Stage 0. Action 3
Phase 3. Stage 0. Action 4
Phase 3. Stage 1. Action 1
Phase 3. Stage 1. Action 2
Phase 3. Stage 1. Action 3
Phase 3. Stage 2. Action 1
Phase 4. Stage 0. Action 1
Phase 4. Stage 0. Action 2
Phase 4. Stage 0. Action 3
Phase 4. Stage 1. Action 1
Phase 4. Stage 1. Action 2
Phase 5. Stage 0. Action 1
Phase 5. Stage 0. Action 2
Phase 5. Stage 0. Action 3
Phase 5. Stage 0. Action 4
Phase 5. Stage 0. Action 5
Phase 6. Stage 0. Action 1
Phase 6. Stage 0. Action 2
Phase 6. Stage 0. Action 3
Phase 6. Stage 0. Action 4
Phase 7. Stage 0. Action 1
Phase 7. Stage 0. Action 2
Phase 7. Stage 0. Action 3
Phase 8. Stage 0. Action 1
Phase 8. Stage 1. Action 1
Phase 8. Stage 1. Action 2
Phase 8. Stage 1. Action 3
Phase 8. Stage 1. Action 4
Phase 9. Stage 0. Action 1
Phase 9. Stage 0. Action 2
Phase 9. Stage 0. Action 3
Phase 9. Stage 0. Action 4
Phase 9. Stage 0. Action 5
```

## Completion Definition

This workplan is complete only when:

1. all implementation actions are completed as written or explicitly resolved
   by Project Owner instruction;
2. BBB uses pointwise executable liftability by default for new affected
   counterpoint tower reruns;
3. invariant reports are generated and acted on;
4. event rows/readouts distinguish quotient availability from pointwise
   liftability;
5. first corrected second-serious durable rerun exists under
   `v072_pointwise_001`;
6. the human-readable readout is regenerated from repo-side
   `readout_source.json`;
7. old artifacts remain preserved unless the Project Owner explicitly cleared
   them;
8. final tests pass.

