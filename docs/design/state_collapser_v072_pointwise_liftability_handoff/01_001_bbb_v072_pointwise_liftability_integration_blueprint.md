# BBB v0.7.2 Pointwise Liftability Integration Blueprint

Status: initial detailed blueprint

Owner: `big_boy_benchmarking`

Upstream dependency: `state_collapser` `v0.7.2`

Primary environment: `counterpoint_symbolic_v001`

Primary affected subsystem: counterpoint active-tier tower control, tower
diagnostics, and human-readable evaluation readouts

This document is a blueprint, not an implementation gameplan. The next
artifact should translate this into a `Phase.Stage.Action` implementation
gameplan before source-code execution.

## Source Material

This blueprint is based on the documents in:

```text
docs/design/state_collapser_v072_pointwise_liftability_handoff/
```

The source documents are:

```text
state_collapser_pointwise_liftability_diagnostic_report.md
state_collapser_pointwise_liftability_github_issue.md
big_boy_benchmarking_synthetic_blow_revisions_02_handoff.md
```

It also binds to the current observed BBB runtime state after the dependency
update to `state_collapser` `v0.7.2`.

Runtime API reconnaissance at blueprint time observed these upstream methods:

```text
PartitionTower.invariant_report(self, *, allow_dirty=False)
PartitionTower.assert_consistent(self, *, allow_dirty=False)
PartitionTower.executable_lift_candidates(self, tier, action_cell_id, current_base_state)
PartitionTower.tier_is_executable_from_state(self, tier, current_base_state)
PartitionTower.lift_candidates(self, tier, action_cell_id, current_base_state)
PartitionTower.outgoing_action_cells(self, tier, state_cell_id)
```

Runtime API reconnaissance also observed these exports:

```text
state_collapser.tower.partition.PartitionInvariantIssue
state_collapser.tower.partition.PartitionInvariantReport
state_collapser.tower.partition.action_layer_invariant_report
state_collapser.training.LiftSelector
state_collapser.training.deterministic_first_lift_selector
state_collapser.training.FiberConditionedStage
```

Runtime API reconnaissance did not observe this convenience method under the
name used in some earlier design notes:

```text
PartitionTower.executable_action_cells_from_base_state
```

Therefore BBB must either derive pointwise executable action-cell vocabularies
locally by filtering quotient action cells through
`PartitionTower.executable_lift_candidates(...)`, or use some other verified
upstream method if one is discovered during implementation. The implementation
must not assume the missing helper exists.

## Prime Directive Constraints

This blueprint follows the repo's prime-directive discipline:

1. Bind every proposed code change to actual files, APIs, and runtime facts.
2. Do not invent Project Owner turns.
3. Preserve Project Owner attribution where the PO supplied the conceptual
   correction.
4. Do not rewrite existing evaluation history silently.
5. Do not implement from this blueprint until a separate Phase.Stage.Action
   gameplan exists and execution is approved.
6. If implementation discovers that the observed upstream API behaves
   differently from the signatures above, stop the affected action and update
   the plan rather than silently substituting a different semantics.

## Project Owner Attribution

The Project Owner identified the core mathematical issue using a simplex-style
example:

- quotient-level action availability is not the same as pointwise executable
  liftability;
- after contracting states, a high-tier action may be outgoing from the
  abstract cell while not extending from the current concrete representative;
- the correct lift condition must look at preimage states with nonempty
  outgoing support for the selected action, not merely choose an arbitrary
  representative of the abstract state.

The Project Owner also approved the downstream provenance policy for this BBB
integration:

```text
the blueprint should make the integration default for new reruns, but require
explicit new artifact roots/readout regeneration for affected evaluations.
That gives us correctness going forward without trashing provenance.
```

This blueprint treats that as an authoritative design requirement.

## Problem Statement

BBB's counterpoint tower-control code currently has a known semantic gap:

```text
quotient outgoing action cell exists
```

is being used in places where the runtime really needs:

```text
there is at least one executable concrete lift from the current concrete state
```

The immediate symptom in previous counterpoint tower evaluations was repeated:

```text
no_lift_candidate_from_current_state
```

The failure was not merely a random bad action choice. It exposed a mismatch
between:

- the abstract tier's quotient-level action vocabulary;
- the current base state inside the fiber;
- the concrete transition that can actually be executed from that current base
  state.

`state_collapser` `v0.7.2` now exposes upstream pointwise liftability and
invariant-checking surfaces that BBB should consume. BBB must update its
counterpoint tower-control adapter, learner action masks, lift executor,
diagnostic artifacts, and readout semantics so that new reruns use pointwise
liftability by default.

## Current BBB State

At blueprint time, the relevant observed BBB files are:

```text
pyproject.toml
uv.lock
src/big_boy_benchmarking/upstream/state_collapser.py
tests/upstream/test_state_collapser_dependency_state.py
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
src/big_boy_benchmarking/environments/counterpoint/serious_learning/events.py
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/events.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/events.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/runner.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/events.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/runner.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/events.py
```

The dependency pin has already been updated to `state_collapser` `v0.7.2` in
the current repository state. The implementation gameplan should verify this
at its first step rather than assuming it remains true.

Focused current behavior in BBB:

1. `CounterpointTowerControlAdapter.tier_is_executable(...)` currently returns
   true when the current tier state has any quotient outgoing action cells.
2. `CounterpointTierLearner._action_vocabulary(...)` currently returns
   `tower.outgoing_action_cells(tier, state)`.
3. `CounterpointTierLearner._action_input(...)` builds an action mask from that
   quotient vocabulary.
4. `CounterpointLiftResolveExecutor._execute(...)` currently calls
   `tower.lift_candidates(...)`, hand-filters candidates by current source, and
   falls back to `action_cell_members(...)` if needed.
5. Diagnostic runners reuse the serious-learning tower-control adapter and
   therefore inherit the same quotient-level predicate and vocabulary.
6. Existing event rows record `candidate_count`, `failure_reason`, and
   `fiber_departure_reason`, but they do not cleanly separate representative
   candidate counts from strict pointwise executable candidate counts.
7. Existing tower shape tables record `active_action_cell_count`, but the
   helper currently counts action cells reachable from active abstract state
   cells by quotient outgoing support, not necessarily from the current base
   state.

## Design Goal

For all new affected counterpoint tower reruns, BBB should use `state_collapser`
`v0.7.2` pointwise liftability as the default semantics.

The corrected default semantics should mean:

```text
An abstract tier/action pair is executable for the current runtime step only
when the selected action cell has at least one concrete edge whose source is
the current concrete/base state.
```

In practical upstream API terms, the strict check should be anchored by:

```python
tower.executable_lift_candidates(tier, action_cell, current_core_state)
```

and:

```python
tower.tier_is_executable_from_state(tier, current_core_state)
```

where the current state is the actual current base/core state used by the
counterpoint runtime.

## Non-Goals

This integration must not:

1. edit `/Users/foster/state_collapser`;
2. redesign upstream `state_collapser`;
3. pretend old BBB evaluation artifacts were generated under the new semantics;
4. silently overwrite historical evaluation artifacts;
5. silently compare old and new runs as if only random seed changed;
6. change the counterpoint environment dynamics;
7. introduce a new counterpoint environment;
8. use temporary artifact roots for durable serious reruns;
9. require tensor-enabled execution;
10. turn diagnostic-only evaluations into learning-performance claims.

## Provenance And Existing Evaluation Guardrails

The PO-approved provenance rule is central:

```text
make the integration default for new reruns, but require explicit new artifact
roots/readout regeneration for affected evaluations
```

Therefore implementation must follow these rules.

### Historical Artifact Preservation

Existing artifact directories under:

```text
docs/evaluations/counterpoint_symbolic_v001/**/artifacts/
```

are historical evidence. They must not be deleted, rewritten, or reinterpreted
unless the Project Owner explicitly asks for that exact cleanup.

Old reports may be superseded by a new current readout, but the raw artifact
folders should remain unless explicitly cleared.

### New Rerun Artifact Roots

Corrected reruns should use new repo-resident artifact roots with names that
make the semantics visible. Recommended pattern:

```text
docs/evaluations/counterpoint_symbolic_v001/<evaluation>/artifacts/v072_pointwise_001/
```

If several iterations are needed:

```text
v072_pointwise_002
v072_pointwise_003
...
```

The exact run label may be adjusted by the Project Owner, but the label must
encode that this is a `state_collapser` `v0.7.2` pointwise-liftability rerun.

### Readout Regeneration

Repo readout surfaces may be regenerated only when the target
`readout_source.json` explicitly points to the new artifact root.

The command surface remains:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-readout-surface>/readout_source.json
```

The readout must state:

- `state_collapser_version`;
- dependency revision/source if available;
- BBB commit if available;
- `liftability_semantics_id`;
- source artifact root;
- whether the readout supersedes an older method run.

### No Silent Cross-Method Comparison

If a report mentions old results, it must label them as historical and generated
under different tower-control semantics unless they were explicitly rerun under
the new pointwise semantics.

Comparisons across old quotient-liftability runs and new pointwise-liftability
runs must be described as cross-methodology comparisons, not ordinary
same-method learning comparisons.

## Proposed Semantics Identifier

Add a method/provenance identifier:

```text
liftability_semantics_id = "state_collapser_v072_pointwise"
```

This identifier should appear in:

- run manifests;
- run metadata/budget blocks;
- `readout_source.json`;
- generated README methodology sections;
- relevant event rows or summary rows where feasible;
- implementation logs for affected evaluations.

If code needs a Python constant, use a local BBB constant with a stable name,
for example:

```python
STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID = (
    "state_collapser_v072_pointwise"
)
```

Do not bury the semantics inside a prose-only README.

## Core Integration Design

### 1. Add Pointwise Action Vocabulary Helpers

BBB should add local helper methods on `CounterpointTowerControlAdapter`.

Recommended methods:

```python
def quotient_action_cells(self, tier: int) -> tuple[object, ...]:
    ...

def pointwise_executable_action_cells(self, tier: int) -> tuple[object, ...]:
    ...

def executable_lift_candidates(self, tier: int, action_cell: object) -> tuple[BaseEdge, ...]:
    ...

def representative_lift_candidates(self, tier: int, action_cell: object) -> tuple[BaseEdge, ...]:
    ...
```

The implementation should preserve the ordering of
`tower.outgoing_action_cells(...)` and filter it by strict pointwise
executability:

```python
quotient_cells = tower.outgoing_action_cells(tier, current_tier_state)
pointwise_cells = tuple(
    action_cell
    for action_cell in quotient_cells
    if tower.executable_lift_candidates(tier, action_cell, current_core_state)
)
```

This provides a strict runtime vocabulary while retaining the quotient
vocabulary for diagnostics.

Important ordering rule:

```text
Do not sort or otherwise reorder action cells after filtering.
```

The action index selected by the tabular learner should continue to refer to
the current runtime vocabulary order. Filtering should remove non-executable
cells, not reshuffle the remaining cells.

### 2. Replace Weak Tier Executability

Current weak behavior:

```python
return bool(self.build.tower.outgoing_action_cells(tier, state_cell))
```

Corrected default behavior:

```python
return self.build.tower.tier_is_executable_from_state(
    tier,
    self.current_core_state,
)
```

If implementation discovers that the upstream method's behavior differs from
the strict pointwise expectation, stop and document the discrepancy before
proceeding.

The adapter should still be able to report the old quotient-level value for
diagnostics:

```text
quotient_tier_has_outgoing_action_cells
```

but it must not use that weak predicate as the controller executability
predicate for new reruns.

### 3. Change Learner Action Masks

Current learner mask source:

```python
vocabulary = tower.outgoing_action_cells(tier, state)
```

Corrected learner mask source:

```python
vocabulary = adapter.pointwise_executable_action_cells(tier)
```

The learner action mask should expose only action cells with at least one
strict executable lift from the current base/core state.

The `ActionSelectionInput.diagnostics` should include both vocabularies:

```text
quotient_action_vocabulary
pointwise_action_vocabulary
quotient_action_cell_count
pointwise_executable_action_cell_count
liftability_semantics_id
```

This is necessary because a future human report must be able to explain cases
where the abstract quotient tier appears nonempty while the pointwise runtime
has no legal abstract action from the current base state.

### 4. Change Lift Resolution

Current executor flow:

1. fetch quotient vocabulary;
2. map action index to an action cell;
3. call `tower.lift_candidates(...)`;
4. filter returned candidates by current source;
5. fallback to `action_cell_members(...)`;
6. fail if no current-source edge is found.

Corrected executor flow:

1. fetch pointwise executable vocabulary;
2. map action index to an action cell;
3. call `tower.executable_lift_candidates(tier, action_cell, current_core_state)`;
4. fail only if the strict upstream query unexpectedly returns no candidates;
5. select a deterministic candidate by default;
6. execute the realized concrete counterpoint action.

Default candidate selection should remain deterministic unless the Project
Owner explicitly requests a stochastic or policy-driven lift selector.

Recommended default:

```text
first strict executable lift candidate in upstream order
```

This matches the upstream `deterministic_first_lift_selector` policy in spirit,
while keeping BBB's local executor explicit.

### 5. Preserve Representative Queries For Diagnostics

The old representative/readout behavior may still be useful for explaining the
gap. BBB should not delete all representative evidence.

Where useful, record:

```text
representative_lift_candidate_count
pointwise_lift_candidate_count
quotient_action_cell_count
pointwise_executable_action_cell_count
```

But runtime execution must use:

```text
pointwise_lift_candidate_count
```

not:

```text
representative_lift_candidate_count
```

### 6. Add Invariant Preflight

`state_collapser` `v0.7.2` exposes:

```python
tower.invariant_report(allow_dirty=False)
tower.assert_consistent(allow_dirty=False)
```

BBB should call invariant checks after tower construction in affected tower
paths. The checks should run outside timed benchmark hot loops.

Recommended helper:

```python
def collect_tower_invariant_report(build: CounterpointTowerBuildResult) -> dict[str, object]:
    ...

def assert_counterpoint_tower_consistent(build: CounterpointTowerBuildResult) -> None:
    ...
```

Because `PartitionInvariantReport` exposes `issues` and `ok`, but not a
runtime-observed `.to_dict()`, BBB should serialize reports locally, for
example with dataclass field extraction.

Required serialized shape:

```json
{
  "ok": true,
  "allow_dirty": false,
  "issue_count": 0,
  "issues": []
}
```

For failures:

```json
{
  "ok": false,
  "allow_dirty": false,
  "issue_count": 2,
  "issues": [
    {
      "tier": 3,
      "code": "...",
      "message": "...",
      "state_cell_id": "...",
      "action_collection_id": "...",
      "action_cell_id": "...",
      "edge_id": "..."
    }
  ]
}
```

Exact ID formatting may use `repr(...)`, but it must be stable enough for
human-readable reports.

### 7. Failure Policy For Invariant Checks

Invariant checks should have two behaviors:

1. In tests and explicit diagnostics, invariant failure should fail fast.
2. In long-running evaluation runners, invariant failure should write a
   machine-readable failure artifact and mark the run failed/incomplete rather
   than producing a misleading success run.

Do not ignore invariant failures.

If an invariant failure mentions stale flattened base-source caches or
source-support maps, the report should explicitly say this is upstream-facing
and should be escalated to `state_collapser` engineers.

## Affected Evaluation Families

The integration affects every BBB evaluation that uses active-tier tower
control or tower lift/action realization.

### First Serious Learning

Readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/
```

Likely affected because tower arms use:

```text
CounterpointTowerControlAdapter
CounterpointTierLearner
CounterpointLiftResolveExecutor
ExploitExploreTowerRuntime
```

Expected changes after corrected rerun:

- tower arms should expose fewer action choices when quotient actions are not
  pointwise executable;
- `no_lift_candidate_from_current_state` should be eliminated or converted into
  a structural failure if it still appears;
- step counts and returns may change;
- direct baseline arms should not change except for dependency metadata if
  they do not use tower control.

### One-Third Schema Tower Diagnostics

Readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/
```

Likely affected because it exercises active-tier control and lift realization.

Expected changes after corrected rerun:

- tier executability tables should report pointwise semantics;
- bottom-stuck or non-executable-tier interpretations may change;
- the diagnostic may remain negative, but for a different and more accurate
  reason.

### Contraction Fraction Sweep Diagnostics

Readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/
```

Likely affected because it uses the same tower-control adapter and reports
tier executability/active action cells.

Expected changes after corrected rerun:

- `active_action_cell_count` should be renamed or clarified if it remains
  quotient-level;
- pointwise action counts should be added;
- collapse threshold claims should continue to focus on tower structure, but
  runtime liftability claims must use pointwise columns.

### Noisy-Rate Contraction Diagnostics

Readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/
```

Likely affected because it was explicitly used to find non-collapsed towers and
runtime lift/control issues.

Expected changes after corrected rerun:

- candidate eligibility based on active action cells should be reviewed;
- pointwise executable action counts should participate in eligibility;
- a tower that has quotient active action cells but zero pointwise executable
  cells for relevant current states should not be treated as cleanly
  trainable.

### Noisy-Rate Full Tower Training Diagnostic

Readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/
```

Likely affected because it consumes candidates from the noisy-rate diagnostic
and runs tower-only training.

Expected changes after corrected rerun:

- candidate selection should use corrected pointwise evidence;
- lift failure counts should drop if the previous failures were caused by weak
  masks;
- if failures remain, they are stronger evidence of a real structural/runtime
  issue.

### Second Serious Schema Comparison

Readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/
```

Likely affected because it compares tower schema arms and was part of the
conversation that exposed bottom-stuck/non-executable behavior.

Expected changes after corrected rerun:

- tower arms may execute different numbers of concrete steps;
- thresholds and schema selection may need to be rerun under the corrected
  semantics;
- old comparison results must not be mixed with new pointwise reruns without a
  visible methodology boundary.

## Artifact Schema Extensions

BBB should add fields carefully. Existing CSV readers should continue to work
where feasible.

Recommended new or clarified fields:

```text
liftability_semantics_id
quotient_action_cell_count
pointwise_executable_action_cell_count
representative_lift_candidate_count
pointwise_lift_candidate_count
lift_query_api
tier_executable_query_api
tower_invariant_ok
tower_invariant_issue_count
```

For lift event rows, recommended additions:

```text
representative_candidate_count
pointwise_candidate_count
selected_lift_index
selected_lift_source_matches_current
selected_lift_target_repr
liftability_semantics_id
```

If preserving backward compatibility with `candidate_count`, define it as:

```text
candidate_count = pointwise_candidate_count
```

for new reruns, and document this in the generated README.

For tier shape and tier signal rows, recommended additions:

```text
quotient_active_action_cell_count
pointwise_executable_action_cell_count
executable_semantics
```

If old fields remain:

```text
active_action_cell_count
raw_historical_action_cell_record_count
```

then the readout must explain exactly what they mean under `v0.7.2`.

## Naming Cleanup

The old field name:

```text
raw_historical_action_cell_record_count
```

is now potentially misleading under `state_collapser` `v0.7.2`, because
upstream may clean historical records rather than retaining stale action-cell
records. Future schema changes should prefer:

```text
raw_action_cell_storage_count
```

However, changing public CSV field names can break existing tests/readers. The
gameplan should decide whether to:

1. add the new field while preserving the old field for compatibility; or
2. rename the field in new evaluation families only; or
3. keep the old field but change generated prose.

Codex recommendation: add the clearer field in affected new reruns while
preserving the old field until a deliberate artifact schema migration is
planned.

## Readout Requirements

Generated readouts for affected reruns must include a short methodology block
near the top:

```text
This run used state_collapser v0.7.2 pointwise liftability semantics. Tower
action masks and tier executability were based on executable concrete lifts
from the current base state, not merely quotient-level outgoing action cells.
```

The readout must also include:

- a badge or status line for `Liftability Semantics`;
- a badge or status line for `Invariant Preflight`;
- a clear statement of whether any invariant issues were found;
- a clear statement of whether `no_lift_candidate_from_current_state` appears;
- an evidence map pointing to lift event rows and tower-shape/tier-signal
  tables;
- a claim boundary separating structural/runtime diagnostics from learning
  performance claims.

If the readout is regenerated in a folder that previously held an old-method
README, the new README must not imply that earlier artifacts were generated
under the corrected method.

## Test Blueprint

The implementation should add or update tests at several levels.

### Dependency/API Probe Tests

Existing dependency tests should continue to verify:

```text
state_collapser import_version == "0.7.2"
PartitionInvariantIssue exported
PartitionInvariantReport exported
action_layer_invariant_report exported
LiftSelector exported
deterministic_first_lift_selector exported
```

Add or verify tests for:

```text
PartitionTower.executable_lift_candidates exists
PartitionTower.tier_is_executable_from_state exists
PartitionTower.assert_consistent exists
PartitionTower.invariant_report exists
```

### Minimal Pointwise Liftability Test

Add a minimal test that reproduces the simplex-style issue from the diagnostic
report in BBB test form, using upstream `state_collapser` APIs.

The test should assert:

```text
quotient outgoing action cell exists
current-state executable lift candidates are empty for the wrong representative
current-state executable lift candidates are nonempty for the supported representative
```

This test anchors the PO's conceptual correction in executable test evidence.

### Adapter Executability Tests

Add tests for `CounterpointTowerControlAdapter`:

```text
tier_is_executable uses current_core_state
tier_is_executable returns false for pointwise-empty tiers
quotient action support can be nonempty while pointwise executable support is empty
```

If the current counterpoint fixture cannot naturally produce the mismatch in a
small deterministic case, use a small upstream synthetic tower fixture for the
adapter helper and a counterpoint smoke assertion for real environment wiring.

### Learner Mask Tests

Add tests asserting:

```text
_action_vocabulary returns only pointwise executable action cells
action_mask length remains compatible with TabularQLearner action_count
diagnostics include quotient and pointwise vocabulary counts
```

### Executor Tests

Add tests asserting:

```text
CounterpointLiftResolveExecutor calls strict executable lift semantics
no fallback to representative-only lift candidates is used for execution
candidate_count means pointwise candidate count in new semantics
no_lift_candidate_from_current_state is unexpected when learner mask was pointwise
```

### Diagnostic Runner Tests

For each affected diagnostic runner, add or update tests to ensure:

```text
readout_source.json records liftability_semantics_id
tower_shape_summary or equivalent includes pointwise counts
lift failure summary distinguishes pointwise and representative counts
invariant report artifact is written
```

### Full Suite Verification

The final implementation should run:

```text
uv run pytest
```

and a targeted Ruff check on touched files.

The repo currently has some pre-existing broad Ruff debt in generated/evaluation
writer files. The implementation should avoid adding new lint issues in touched
files, but it does not need to refactor unrelated existing line-length debt
unless the gameplan explicitly includes that cleanup.

## Implementation Surfaces

The Phase.Stage.Action gameplan should inspect and probably edit these files.

### Dependency Probe

```text
src/big_boy_benchmarking/upstream/state_collapser.py
tests/upstream/test_state_collapser_dependency_state.py
```

Expected work:

- add required symbol checks for strict pointwise methods if not already
  present;
- expose dependency-state metadata to run manifests/readouts if needed.

### Tower Adapter

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
```

Expected work:

- add quotient-vs-pointwise vocabulary helpers;
- change `tier_is_executable`;
- change learner vocabulary/mask;
- change executor lift query;
- enrich `LiftResolveTrace`;
- record semantics ID in diagnostics.

### Tower Construction

```text
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
```

Expected work:

- consider adding invariant helper functions near build results;
- optionally call invariant checks inside build functions or at runner call
  sites;
- keep invariant checks outside timed hot loops.

### Event Rows

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/events.py
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/events.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/events.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/events.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/events.py
```

Expected work:

- add pointwise/quotient fields where affected tables need them;
- avoid breaking old readers without a conscious migration;
- document field semantics in readout writers.

### Diagnostic Runners

```text
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/runner.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/runner.py
```

Expected work:

- feed the corrected adapter semantics through all active-tier runtime paths;
- update summary rows;
- write invariant report artifacts;
- record semantic mode in run metadata and source bindings.

### Docs Writers And Readout Source

```text
src/big_boy_benchmarking/environments/counterpoint/**/docs_writer.py
src/big_boy_benchmarking/environments/counterpoint/**/manifests.py
```

Expected work:

- update methodology text for pointwise liftability;
- add badge/status support for liftability semantics and invariant preflight;
- update expected-file declarations for invariant reports and new summary
  fields.

## Evaluation Rerun Policy

After implementation, affected evaluations should not be rerun in-place unless
the Project Owner explicitly asks for an in-place clean regeneration.

Recommended rerun order:

1. small smoke: graph diagnostics and one tiny tower run;
2. targeted pointwise-liftability synthetic test;
3. one small counterpoint tower-control run;
4. one affected diagnostic rerun with repo-resident artifacts;
5. regenerate one human-readable readout;
6. then decide which historical readouts need corrected reruns.

Recommended first durable artifact target:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/v072_pointwise_001/
```

or, if the Project Owner wants to isolate the liftability correction before
schema comparison:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts/v072_pointwise_001/
```

This is a recommendation, not an instruction. The Project Owner should choose
which evaluation gets the first corrected durable rerun.

## Acceptance Criteria

The implementation is complete when all of the following are true.

### Runtime Semantics

1. New counterpoint tower-control runs use pointwise executable liftability by
   default.
2. `tier_is_executable` is based on current-base-state strict liftability.
3. Learner action masks expose only pointwise executable action cells.
4. Lift resolution uses `PartitionTower.executable_lift_candidates(...)`.
5. `no_lift_candidate_from_current_state` does not occur after a pointwise mask
   selected the action, unless the run records it as an invariant/structural
   failure requiring investigation.

### Invariant Checks

1. A tower invariant report is written for affected tower builds.
2. Invariant failures are not ignored.
3. Invariant failures produce readable failure status and machine-readable
   evidence.

### Artifact Provenance

1. New reruns record `liftability_semantics_id`.
2. New reruns record `state_collapser` `0.7.2`.
3. New reruns use explicit new artifact roots.
4. Old artifacts remain available unless explicitly cleared by the Project
   Owner.
5. Generated readouts state whether they are old-method historical reports or
   new pointwise reruns.

### Human Readability

1. Readouts distinguish quotient action availability from pointwise executable
   liftability.
2. Readouts explain zero-step/zero-return tower results using concrete lift and
   tier-control evidence, not merely status fields.
3. Readouts map raw evidence files to human claims.
4. Readouts include protected Project Owner / Evaluator and Embedded
   Engineering Consultant / Codex turn sections per the artifact-table protocol.

### Tests

1. Full pytest passes.
2. Touched files pass targeted Ruff checks.
3. New tests cover pointwise liftability, adapter executable tiers, learner
   masks, executor strict lift queries, invariant report serialization, and
   artifact/readout metadata.

## Risks

### Risk 1: Dynamic Action Vocabulary Changes Learning Behavior

Filtering quotient action cells to pointwise executable action cells changes
the action mask seen by learners. This is intended, but it means corrected
reruns are methodologically different from old runs.

Mitigation:

- record `liftability_semantics_id`;
- use new artifact roots;
- do not silently compare old and new runs.

### Risk 2: Action Index Instability

The pointwise vocabulary can vary by current base state. A tabular learner's
chosen action index refers to the current masked vocabulary, not a fixed global
action identity.

Mitigation:

- preserve quotient ordering before filtering;
- record action vocabulary diagnostics;
- include the selected action cell representation in event rows.

### Risk 3: Invariant Checks Add Cost

Invariant checks may be expensive on larger towers.

Mitigation:

- run invariant preflight after tower construction;
- do not run invariant checks inside timed hot loops unless explicitly
  configured as a diagnostic mode.

### Risk 4: Field Name Compatibility

Adding clearer fields may collide with existing readers that expect current CSV
schemas.

Mitigation:

- add fields rather than rename where possible;
- update tests and docs writers together;
- reserve full schema migration for a separate explicit plan.

### Risk 5: Reports Become Too Technical

Pointwise liftability is conceptually subtle.

Mitigation:

- include a short reader-facing explanation in every affected README;
- use the simplex example or binary-search analogy where helpful;
- show a table with quotient action count versus pointwise executable count.

## Open Questions For Project Owner

These are not blockers for writing the implementation gameplan, but they should
be answered before rerunning durable evaluations.

### Question 1: First Corrected Durable Rerun

Which evaluation should be the first durable corrected rerun?

Codex recommendation:

```text
second_serious_schema_comparison
```

because it is the most directly connected to the recent bottom-stuck
conversation.

Alternative:

```text
noisy_rate_full_tower_training_diagnostic
```

because it isolates full tower training health on selected non-collapsed
towers.

### Question 2: Artifact Label

Should the first corrected artifact label be:

```text
v072_pointwise_001
```

Codex recommendation: yes, unless the Project Owner wants a more evaluation-
specific label.

### Question 3: Historical README Treatment

When regenerating a readout surface, should the old README be archived first
under `docs/design/system_learning_from_evaluations/...`, or is preserving the
old raw artifact folder enough?

Codex recommendation: archive only if the README contains substantial
conversation or interpretive discussion. Otherwise, preserving old artifacts
and writing clear supersession language is enough.

## Blueprint-To-Gameplan Translation Notes

The next document should be a Phase.Stage.Action implementation gameplan.

Recommended gameplan structure:

```text
Phase 1: Reconnaissance and API verification
Phase 2: Dependency probe and invariant serialization
Phase 3: Counterpoint adapter pointwise semantics
Phase 4: Event/artifact schema extensions
Phase 5: Diagnostic runner propagation
Phase 6: Readout/protocol-facing documentation updates
Phase 7: Tests and verification
Phase 8: Corrected rerun instructions and handoff
```

The gameplan should include an implementation log section or companion log
file, because this work touches multiple evaluations and must preserve
provenance carefully.

The gameplan should also require a new implementation branch before source-code
execution, unless the Project Owner explicitly instructs otherwise.

