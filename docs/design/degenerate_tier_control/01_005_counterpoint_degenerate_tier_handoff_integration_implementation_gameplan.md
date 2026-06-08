# Counterpoint Degenerate-Tier Handoff Integration Implementation Workplan

Date: 2026-05-30

Status: implementation workplan, not yet executed under this workplan

Repository:

```text
<repo-root>
```

Source blueprint:

```text
docs/design/degenerate_tier_control/01_004_counterpoint_degenerate_tier_handoff_integration_blueprint.md
```

## Purpose

This workplan translates the corrected degenerate-tier handoff integration
blueprint into Phase.Stage.Action implementation work.

The work is intentionally narrow:

```text
make the completed upstream state_collapser v0.7.1 degenerate-tier runtime fix
work inside BBB's existing counterpoint serious evaluation path, verify the old
invalid_action_index failure path is gone, and return to the original
counterpoint evaluation evidence.
```

This workplan does not create a new action-realization design block.

## Execution Authority Status

This document is not approval to implement.

The Project Owner asked for this workplan:

```text
OK NOW give this a re-read, and follow prime_directive to turn it into a
Phase.Stage.Action gamplan
```

Therefore this document may be created now.

Source, test, dependency, lockfile, artifact, and evaluation-readout
implementation must not begin under this workplan until the Project Owner
explicitly approves execution of this exact file.

## Source Authority

This workplan follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/git_practices.md`
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`
- `docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md`
- `docs/design/degenerate_tier_control/error_diagnosis_conversation.md`
- `docs/design/degenerate_tier_control/01_003_big_boy_benchmarking_handoff_note.md`
- `docs/design/degenerate_tier_control/01_004_counterpoint_degenerate_tier_handoff_integration_blueprint.md`
- `docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_001_counterpoint_first_serious_learning_evaluation_blueprint.md`
- `docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_002_counterpoint_first_serious_learning_evaluation_implementation_workplan.md`
- `docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/README.md`

## Fixed Implementation Decisions

These decisions are already settled by the upstream handoff and the corrected
blueprint.

### Upstream Version

Use the public upstream release tag:

```text
state_collapser v0.7.1
```

Do not use a local editable `<state-collapser-repo>` dependency for this
work.

### Runtime Surface

Use:

```text
ExploitExploreTowerRuntime(..., tier_is_executable=...)
```

Do not redesign `state_collapser` runtime control in BBB.

### BBB Predicate

Implement the BBB-local predicate as:

```text
tier is executable if:
  tier is within the current tower depth
  and the current core state projects to a tier state-cell
  and that tier state-cell has at least one outgoing action cell
```

Do not replace this with a broader concrete lift-candidate predicate in this
workplan.

### Evaluation Scope

The target evaluation remains:

```text
counterpoint_symbolic_v001 first_serious_learning
counterpoint_symbolic_n3_small_v001
tensor_available_disabled
```

This workplan may run the smallest-valid serious-learning smoke for validation.
It must not silently change the serious evaluation budget, arms, schemas, or
claim boundary.

## Non-Goals

This workplan does not:

- add concrete candidate-selection policy;
- decide one action-cell versus multiple concrete candidate options;
- redesign structured-motion schema construction;
- add a new failure taxonomy beyond recording observed results;
- add a new learner;
- change reward shaping;
- enable tensor CPU/CUDA modes;
- edit `<state-collapser-repo>`;
- claim tower advantage.

If implementation reveals a new downstream failure after the handoff is wired,
record it as evidence and stop if addressing it would change scope.

## Global Stop Conditions

Stop and ask the Project Owner if:

- execution of this exact workplan has not been approved;
- branch or dirty-worktree state would mix unrelated source/test changes into
  this implementation;
- existing uncommitted implementation edits are present and it is unclear
  whether to adopt, move, or recommit them under this workplan;
- `state_collapser v0.7.1` cannot be installed from the public tag;
- installed `state_collapser` does not report version `0.7.1`;
- `ExploitExploreTowerRuntime` does not expose `tier_is_executable`;
- implementing the handoff would require editing `<state-collapser-repo>`;
- the BBB counterpoint adapter cannot compute current tier state cells from its
  current core state and partition tower;
- the runtime cannot accept the predicate without redesigning local controller
  or learner semantics;
- a test failure would require broader action-realization redesign to pass;
- a smoke run produces a new failure whose fix would exceed the handoff scope;
- any Phase.Stage.Action item cannot be completed as written.

## Required Branch Discipline

After Project Owner approval and before implementation edits, use a dedicated
implementation branch.

Default branch:

```text
codex/counterpoint-degenerate-tier-handoff
```

If matching uncommitted handoff-integration edits already exist on `main` when
execution begins, do not silently continue. Record the reality in the
implementation log and ask the Project Owner how to bind those edits to the
implementation branch/history.

## Required Running Implementation Log

Create and maintain:

```text
docs/design/degenerate_tier_control/01_006_counterpoint_degenerate_tier_handoff_integration_implementation_log.md
```

The log must record:

- approval to execute this exact workplan;
- initial branch and dirty state;
- how any pre-existing matching edits were handled;
- every completed Phase.Stage.Action;
- exact commands run;
- validation outcomes;
- observed smoke evidence;
- blockers and Project Owner clarifications;
- final git status.

## Phase 0: Execution Authority And Reality Binding

### Stage 0.1: Confirm Approval

#### Action 0.1.1

Confirm the Project Owner explicitly approved execution of this exact file:

```text
docs/design/degenerate_tier_control/01_005_counterpoint_degenerate_tier_handoff_integration_implementation_workplan.md
```

Acceptance criteria:

- approval is recorded in the implementation log;
- no source, test, dependency, lockfile, artifact, or evaluation-readout edits
  occur under this workplan before approval.

#### Action 0.1.2

Reread Prime Directive files:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/git_practices.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md
```

Acceptance criteria:

- implementation log records the reread;
- no contradiction is found between this workplan and the Prime Directive.

### Stage 0.2: Inspect Git State

#### Action 0.2.1

Run:

```bash
git status --short --branch
```

Acceptance criteria:

- current branch and dirty state are recorded in the implementation log;
- source/test/dependency dirty files related to this handoff are identified;
- unrelated dirty source/test/dependency files stop execution.

#### Action 0.2.2

If no conflicting dirty work prevents execution, create or switch to:

```text
codex/counterpoint-degenerate-tier-handoff
```

Acceptance criteria:

- implementation branch is active;
- branch choice is recorded in the implementation log;
- no unrelated work is staged, reverted, or rewritten.

#### Action 0.2.3

If matching uncommitted handoff-integration edits already exist before branch
creation, bind reality before proceeding.

Acceptance criteria:

- implementation log records each pre-existing matching file;
- Project Owner explicitly decides whether to adopt those edits on the new
  branch, preserve them on the current branch, or take another git action;
- no silent branch/history rewrite occurs.

### Stage 0.3: Bind Design And Code Reality

#### Action 0.3.1

Read the handoff and corrected blueprint:

```text
docs/design/degenerate_tier_control/error_diagnosis_conversation.md
docs/design/degenerate_tier_control/01_003_big_boy_benchmarking_handoff_note.md
docs/design/degenerate_tier_control/01_004_counterpoint_degenerate_tier_handoff_integration_blueprint.md
```

Acceptance criteria:

- implementation log records the source files read;
- implementation scope remains limited to handoff integration.

#### Action 0.3.2

Read current BBB surfaces:

```text
pyproject.toml
uv.lock
src/big_boy_benchmarking/upstream/state_collapser.py
tests/upstream/test_state_collapser_dependency_state.py
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
tests/environments/counterpoint/test_serious_learning_tower_control.py
README.md
CONTRIBUTING.md
```

Acceptance criteria:

- implementation log records the inspected surfaces;
- any mismatch requiring broader design stops execution.

## Phase 1: Upstream Dependency Integration

### Stage 1.1: Pin `state_collapser v0.7.1`

#### Action 1.1.1

Update the project dependency pin to:

```text
state-collapser[rl] @ git+https://github.com/TYLERSFOSTER/state_collapser.git@v0.7.1
```

Likely files:

```text
pyproject.toml
src/big_boy_benchmarking/upstream/state_collapser.py
README.md
CONTRIBUTING.md
```

Acceptance criteria:

- current setup docs and dependency-state helper name `v0.7.1`;
- historical design docs are not rewritten merely to update history.

#### Action 1.1.2

Refresh the lockfile and installed environment.

Expected commands:

```bash
UV_CACHE_DIR=<tmp-dir>/hgraphml-uv-cache uv lock
uv sync --group dev
```

Acceptance criteria:

- `uv.lock` resolves `state-collapser` from `v0.7.1`;
- installed environment contains `state-collapser==0.7.1`;
- no local editable `<state-collapser-repo>` dependency is introduced.

### Stage 1.2: Verify Upstream Runtime Surface

#### Action 1.2.1

Run a direct runtime surface probe.

Expected command:

```bash
uv run python - <<'PY'
import inspect
import state_collapser
from state_collapser.tower.runtime import ExploitExploreTowerRuntime
print(state_collapser.__version__)
print(inspect.signature(ExploitExploreTowerRuntime))
PY
```

Acceptance criteria:

- printed version is `0.7.1`;
- signature includes `tier_is_executable`.

#### Action 1.2.2

Update dependency-state tests to require:

```text
state.import_version == "0.7.1"
ExploitExploreTowerRuntime signature includes tier_is_executable
```

Likely file:

```text
tests/upstream/test_state_collapser_dependency_state.py
```

Acceptance criteria:

- test proves the installed pinned package exposes the handoff runtime surface;
- test does not import from `<state-collapser-repo>`.

## Phase 2: Counterpoint Runtime Wiring

### Stage 2.1: Add Adapter Executability Predicate

#### Action 2.1.1

Add a method equivalent to:

```python
def tier_is_executable(self, tier: int) -> bool:
    if tier < 0 or tier >= self.tower_depth:
        return False
    state_cell = self.current_tier_state(tier)
    if state_cell is None:
        return False
    return bool(self.build.tower.outgoing_action_cells(tier, state_cell))
```

Likely file:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
```

Acceptance criteria:

- predicate matches the upstream handoff using BBB's adapter-local state;
- predicate checks outgoing action cells only;
- no concrete lift-candidate filtering is introduced.

### Stage 2.2: Pass Predicate Into Runtime

#### Action 2.2.1

Pass the adapter predicate to:

```python
ExploitExploreTowerRuntime(..., tier_is_executable=adapter.tier_is_executable)
```

Likely file:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
```

Acceptance criteria:

- runtime construction includes `tier_is_executable`;
- no local runtime/controller replacement is introduced.

#### Action 2.2.2

Update the timed controller wrapper signature only as needed to forward the
upstream callback.

Likely file:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
```

Acceptance criteria:

- wrapper accepts `tier_is_executable`;
- wrapper forwards it to `ActiveTierController.decide(...)`;
- no other controller behavior changes.

## Phase 3: Focused Tests

### Stage 3.1: Adapter Executability Tests

#### Action 3.1.1

Add or update tests proving the adapter marks current executable and
non-executable tiers correctly.

Likely file:

```text
tests/environments/counterpoint/test_serious_learning_tower_control.py
```

Acceptance criteria:

- empty-schema tier `0` is executable after reset;
- at least one known non-empty-schema coarsened tier is non-executable after
  reset;
- out-of-bounds negative and too-deep tiers are non-executable.

### Stage 3.2: Runtime Surface Tests

#### Action 3.2.1

Ensure the upstream dependency-state test covers the handoff surface.

Likely file:

```text
tests/upstream/test_state_collapser_dependency_state.py
```

Acceptance criteria:

- test fails against a runtime without `tier_is_executable`;
- test passes against pinned `state_collapser v0.7.1`.

## Phase 4: Validation

### Stage 4.1: Focused Test Run

#### Action 4.1.1

Run focused tests:

```bash
uv run pytest tests/upstream/test_state_collapser_dependency_state.py tests/environments/counterpoint/test_serious_learning_tower_control.py
```

Acceptance criteria:

- focused tests pass;
- failures are logged with exact failing test names and output.

### Stage 4.2: Full Test And Lint Run

#### Action 4.2.1

Run the full test suite:

```bash
uv run pytest
```

Acceptance criteria:

- full test suite passes;
- if failures appear outside the handoff scope, stop before broadening work.

#### Action 4.2.2

Run lint and whitespace checks:

```bash
uv run ruff check .
git diff --check
```

Acceptance criteria:

- lint passes;
- whitespace check passes.

## Phase 5: Serious-Learning Smoke Evidence

### Stage 5.1: Run Smallest Valid Serious-Learning Smoke

#### Action 5.1.1

Run a smallest-valid serious-learning smoke.

Expected command:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning run \
  --artifact-root <tmp-dir>/bbb-counterpoint-degenerate-tier-handoff-smoke \
  --episodes 1 \
  --replicates 1 \
  --schema-seeds 2 \
  --locked-by codex
```

Acceptance criteria:

- command completes with `status: complete`;
- run index contains all expected serious-learning arms for the smoke budget;
- artifact root is recorded in the implementation log.

### Stage 5.2: Inspect Old Failure Symptoms

#### Action 5.2.1

Search smoke artifacts for the old failure symptoms:

```bash
rg -n "invalid_action_index|action_index_out_of_range" <tmp-dir>/bbb-counterpoint-degenerate-tier-handoff-smoke
```

Acceptance criteria:

- no old empty-vocabulary failure symptoms are found;
- if symptoms are found, stop and diagnose only within the handoff scope.

#### Action 5.2.2

Summarize tower arm episode outcomes and lift-fiber failure reasons.

Expected inspection:

```text
episodes.csv across tower runs
lift_fiber_events.csv across tower runs
```

Acceptance criteria:

- implementation log records which tower arms executed concrete steps;
- implementation log records any remaining failure reasons;
- any new failure reason is recorded as evidence, not fixed in this workplan
  unless it is directly the old degenerate-tier failure.

## Phase 6: Evaluation Readout Resume Point

### Stage 6.1: Preserve Scope Boundary

#### Action 6.1.1

Record in the implementation log whether the smoke evidence is sufficient to
resume the first serious counterpoint evaluation readout conversation.

Acceptance criteria:

- log distinguishes "handoff integration verified" from "tower learning claim
  proven";
- no tower advantage claim is made from the smoke.

### Stage 6.2: Regenerate Human-Readable Readout Only If Directed

#### Action 6.2.1

If and only if the Project Owner directs readout regeneration, run the existing
artifact-table readout protocol against the repo-side evaluation surface.

Canonical invocation:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/readout_source.json
```

Acceptance criteria:

- readout remains source-bound to the artifact tables selected by the Project
  Owner or the approved readout source;
- generated human-readable evidence distinguishes the old degenerate-tier bug
  from any remaining downstream failures.

## Phase 7: Final Reporting And Git State

### Stage 7.1: Final Validation Summary

#### Action 7.1.1

Record final validation results in the implementation log:

```text
dependency/runtime probe
focused tests
full tests
lint
diff check
serious-learning smoke
old-failure symptom search
```

Acceptance criteria:

- exact commands and outcomes are recorded;
- any unexecuted validation is explicitly named with reason.

### Stage 7.2: Final Git Status

#### Action 7.2.1

Run:

```bash
git status --short --branch
```

Acceptance criteria:

- final branch and dirty state are recorded;
- unrelated pre-existing changes are not claimed as part of this handoff;
- final report separates this workplan's changes from other repo changes.

## Completion Criteria

This workplan is complete when:

- `state_collapser v0.7.1` is pinned, locked, installed, and verified;
- BBB dependency tests require the handoff runtime surface;
- BBB counterpoint tower-control passes `tier_is_executable` into
  `ExploitExploreTowerRuntime`;
- the adapter predicate matches the upstream outgoing-action-cell handoff;
- focused tests pass;
- full tests pass;
- lint and whitespace checks pass;
- a smallest-valid serious-learning smoke completes;
- the old `invalid_action_index` / `action_index_out_of_range` empty-vocabulary
  failure path is absent from smoke artifacts;
- implementation log records any remaining failure evidence without expanding
  this workplan's scope.

## Explicitly Deferred Work

The following work is deferred unless the Project Owner opens a separate design
block:

- concrete lift-candidate executability redesign;
- action-cell candidate selection policy;
- structured-motion schema correction;
- broader failure taxonomy redesign;
- serious evaluation budget changes;
- tensor-enabled modes;
- new learners or policies.

