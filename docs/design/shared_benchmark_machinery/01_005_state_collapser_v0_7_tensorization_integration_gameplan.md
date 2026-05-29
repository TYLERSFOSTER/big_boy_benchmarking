# State Collapser v0.7 Tensorization Integration Gameplan

Date: 2026-05-29

Status: implementation gameplan, not yet executed

Repository:

```text
/Users/foster/big_boy_benchmarking
```

## Purpose

This gameplan defines the local `big_boy_benchmarking` integration work needed
after upstream `state_collapser` released the first tensorization boundary in
`v0.7.0`.

The Project Owner directed:

```text
integrate state_collapser v0.7.0 into BBB shared machinery, then resume serious
counterpoint design discussion
```

This file exists because the repo's Prime Directive requires implementation
work to be controlled by a Phase.Stage.Action plan before source/test edits.

## Execution Authority Status

The Project Owner has identified the desired work:

```text
integrate state_collapser v0.7.0 into BBB shared machinery
```

However, this exact gameplan did not exist when that instruction was given.

Therefore:

- this document may be reviewed and corrected by the Project Owner;
- source/test/lockfile execution should begin only after the Project Owner
  explicitly approves execution of this gameplan;
- when approved, execution must follow this gameplan in order unless the
  Project Owner explicitly changes it.

## Source Authority

This gameplan follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/git_practices.md`
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`
- `docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md`
- `CONTRIBUTING.md`
- `docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md`
- `docs/design/shared_benchmark_machinery/01_002_shared_benchmark_machinery_implementation_gameplan.md`
- `docs/design/shared_benchmark_machinery/01_003_shared_benchmark_machinery_implementation_log.md`
- `docs/design/shared_benchmark_machinery/01_004_state_collapser_tensorization_resume_note.md`
- `docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md`
- `/Users/foster/state_collapser/docs/usage/01_010_tensorization_boundary.md`
- `/Users/foster/state_collapser/docs/design/tensorization/01_004_tensorization_implementation_log.md`
- `/Users/foster/state_collapser/docs/engineer_continuity/2026/05/29/01_013_log_tropical_tensorization_and_hgraphml_followup.md`

## Current Reality Bound By This Plan

Observed local BBB state before this gameplan:

```text
## main...origin/main [ahead 1]
```

The local `pyproject.toml` still pins:

```text
state-collapser[rl] @ git+https://github.com/TYLERSFOSTER/state_collapser.git@v0.6.0
```

The local BBB import gate currently fails:

```python
from state_collapser.training import LinearizationConfig
```

Observed result:

```text
ImportError
state_collapser.__version__ = 0.6.0
```

Upstream `/Users/foster/state_collapser` now exposes the required tensorization
surface in release `v0.7.0`.

## Fixed Decisions For This Gameplan

These decisions are encoded here so the Project Owner can approve or correct
them before execution.

### Dependency Target

Pin BBB to:

```text
state-collapser[rl] @ git+https://github.com/TYLERSFOSTER/state_collapser.git@v0.7.0
```

Do not use a local editable `/Users/foster/state_collapser` dependency for this
integration.

### Tensorization Axis

Represent tensorization as a BBB-owned companion axis rather than replacing the
existing execution-mode registry.

Existing `BenchmarkModeContract` answers:

```text
What run shape is this?
```

New linearization contract answers:

```text
What state_collapser tensorization condition was active?
```

### First Linearization Mode Ids

Use the upstream derived labels as local linearization mode ids:

```text
none_control_flow
tensor_available_disabled
tensor_enabled_cpu
tensor_enabled_cuda
```

### Initial Runnable/Reserved State

Initial runnable modes:

```text
none_control_flow
tensor_available_disabled
```

Initial reserved modes:

```text
tensor_enabled_cpu
tensor_enabled_cuda
```

Reason:

- CPU tensor construction exists upstream but BBB does not yet have a real
  tensor-consuming learner/model benchmark path.
- CUDA has not been locally validated in BBB.

### Artifact Schema Marker

Keep:

```text
bbb.v001
```

for this integration slice.

Reason:

- the current artifact schema marker is intentionally lightweight;
- current artifacts remain smoke/diagnostic, not published serious evidence;
- this slice can add linearization manifest files without claiming a finalized
  schema migration.

If the Project Owner wants the tensorization boundary to force a schema bump,
stop before Phase 4 and change this plan.

### Runner Defaults

Existing smoke commands should default to:

```text
tensor_available_disabled
```

after this integration.

Reason:

The purpose of returning from the upstream tensorization detour is to stop
generating new BBB artifacts that blur:

```text
pre-linearization package
```

with:

```text
tensor-capable package with tensor path disabled
```

Existing callers may explicitly request:

```text
none_control_flow
```

when they want a control-flow baseline.

### Registry Timing

Use a dedicated timing segment:

```text
encoding_registry_build
```

and a dedicated timing segment:

```text
linearization_report_build
```

Do not hide these under compatibility readout, learner action, tower update, or
artifact logging.

## Global Stop Conditions

Stop and ask the Project Owner if:

- `state_collapser v0.7.0` cannot be installed or locked;
- the required tensorization imports fail after the dependency update;
- the `v0.7.0` tag does not resolve;
- changing the lockfile requires network access that fails under sandboxing;
- the current branch or git status diverges from this gameplan's assumptions;
- an implementation action requires editing `/Users/foster/state_collapser`;
- a source action would require reinterpreting tensorization as the existing
  execution-mode axis;
- the existing smoke runners cannot be updated without changing their public CLI
  behavior more than this plan states;
- tests reveal that upstream `v0.7.0` changed existing `v0.6.0` behavior needed
  by counterpoint or upstream smoke runners;
- a reserved tensor mode would need to become runnable for tests to pass;
- any action needs to be simplified or approximated.

## Required Branch Discipline

After Project Owner approval and before source/test/lockfile edits, create and
switch to a dedicated implementation branch:

```text
codex/state-collapser-v0-7-bbb-integration
```

Do not implement directly on `main`.

## Required Running Implementation Log

Create and maintain:

```text
docs/design/shared_benchmark_machinery/01_006_state_collapser_v0_7_tensorization_integration_implementation_log.md
```

The log must record:

- starting branch and status;
- each completed Phase.Stage.Action;
- exact commands run;
- validation outcomes;
- blockers and PO clarifications;
- final git status;
- whether serious counterpoint design discussion was resumed.

## Validation Command Set

Expected validation commands:

```bash
uv lock
uv sync --group dev
uv run python -c "from state_collapser.training import LinearizationConfig, LinearizationReport, LinearizationState, NumericBackend, TensorDeviceKind, build_linearization_report; print('ok')"
uv run python -m big_boy_benchmarking.cli validate-contracts
uv run pytest
uv run ruff check .
```

If `uv lock` or `uv sync` fails due network/sandbox access, request escalation
instead of editing the lockfile by hand.

## Phase 0: Execution Setup And Reality Binding

### Stage 0.1: Confirm Execution Authority

#### Action 0.1.1

Confirm the Project Owner explicitly approved execution of this file:

```text
docs/design/shared_benchmark_machinery/01_005_state_collapser_v0_7_tensorization_integration_gameplan.md
```

Acceptance criteria:

- approval is recorded in the implementation log;
- no source/test/lockfile files are edited before this approval.

#### Action 0.1.2

Re-read Prime Directive files:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/git_practices.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md
```

Acceptance criteria:

- implementation log records the re-read;
- no contradictions are found between this gameplan and the Prime Directive.

### Stage 0.2: Create Implementation Branch

#### Action 0.2.1

Inspect status:

```bash
git status --short --branch
```

Acceptance criteria:

- current branch and dirty/ahead state are recorded;
- if unexpected source/test changes exist, stop.

#### Action 0.2.2

Create and switch to:

```text
codex/state-collapser-v0-7-bbb-integration
```

Acceptance criteria:

- branch exists;
- implementation log records the branch;
- no source/test edits have happened yet.

### Stage 0.3: Bind Current Code Reality

#### Action 0.3.1

Read current dependency and lockfile surfaces:

```text
pyproject.toml
uv.lock
```

Acceptance criteria:

- current `v0.6.0` pin is recorded;
- current lockfile state is recorded.

#### Action 0.3.2

Read current shared machinery surfaces:

```text
src/big_boy_benchmarking/upstream/state_collapser.py
src/big_boy_benchmarking/modes/contracts.py
src/big_boy_benchmarking/modes/registry.py
src/big_boy_benchmarking/artifacts/manifests.py
src/big_boy_benchmarking/artifacts/paths.py
src/big_boy_benchmarking/artifacts/schemas.py
src/big_boy_benchmarking/metrics/timing.py
src/big_boy_benchmarking/runners/base.py
src/big_boy_benchmarking/runners/upstream_smoke.py
src/big_boy_benchmarking/environments/counterpoint/runners.py
src/big_boy_benchmarking/cli/main.py
```

Acceptance criteria:

- implementation log records that these files were read;
- any mismatch with this gameplan stops execution.

## Phase 1: Dependency Pin And Import Gate

### Stage 1.1: Update Dependency Target

#### Action 1.1.1

Update `pyproject.toml` dependency from `v0.6.0` to:

```text
v0.7.0
```

Acceptance criteria:

- only the `state-collapser[rl]` dependency target changes in this action;
- no local editable path is introduced.

#### Action 1.1.2

Run:

```bash
uv lock
```

Acceptance criteria:

- `uv.lock` resolves `state-collapser` from `v0.7.0`;
- if sandbox/network failure occurs, request escalation.

#### Action 1.1.3

Run:

```bash
uv sync --group dev
```

Acceptance criteria:

- local BBB environment installs the updated dependency;
- `state_collapser.__version__` is `0.7.0`.

### Stage 1.2: Add Dependency Import Tests

#### Action 1.2.1

Update dependency tests to require backend-independent tensorization imports:

```python
EncodingRegistry
LinearizationConfig
LinearizationReport
LinearizationState
NumericBackend
TensorDeviceKind
build_linearization_report
```

Likely file:

```text
tests/test_state_collapser_dependency.py
```

Acceptance criteria:

- test fails under `v0.6.0`;
- test passes under `v0.7.0`;
- Torch imports are not required here.

#### Action 1.2.2

Add optional Torch import-state coverage without requiring Torch.

Likely file:

```text
tests/upstream/test_state_collapser_dependency_state.py
```

Acceptance criteria:

- missing Torch does not fail the suite;
- import status can be represented as `ok`, `missing`, or `not_requested`.

## Phase 2: Upstream Dependency State Extension

### Stage 2.1: Extend Dependency State Model

#### Action 2.1.1

Extend:

```text
src/big_boy_benchmarking/upstream/state_collapser.py
```

to record tensorization import state.

Candidate fields:

```text
linearization_import_status
linearization_symbols
torch_import_status
cuda_available
```

Acceptance criteria:

- dependency state can report the required backend-independent symbols;
- Torch state is optional;
- existing fields remain present.

#### Action 2.1.2

Update dependency-state tests.

Acceptance criteria:

- dependency-state `to_dict()` includes the new fields;
- tests do not require a local `/Users/foster/state_collapser` checkout;
- tests pass with installed `v0.7.0`.

## Phase 3: Linearization Mode Contracts

### Stage 3.1: Add Contract Types

#### Action 3.1.1

Add a local linearization contract module.

Likely file:

```text
src/big_boy_benchmarking/modes/linearization.py
```

Required dataclasses:

```text
LinearizationModeContract
```

Required validation:

```text
validate_linearization_mode_contract
```

Acceptance criteria:

- local contract records the upstream enum values as strings;
- local contract records runnable/reserved state;
- reserved modes require reserved reasons;
- contract does not import Torch.

#### Action 3.1.2

Add linearization mode registry entries:

```text
none_control_flow
tensor_available_disabled
tensor_enabled_cpu
tensor_enabled_cuda
```

Likely file:

```text
src/big_boy_benchmarking/modes/linearization.py
```

Acceptance criteria:

- first two modes are runnable;
- CPU and CUDA modes are reserved;
- expected upstream benchmark labels match mode ids.

### Stage 3.2: Export And Validate Contracts

#### Action 3.2.1

Export linearization registry helpers from:

```text
src/big_boy_benchmarking/modes/__init__.py
```

Acceptance criteria:

- imports are stable from `big_boy_benchmarking.modes`;
- existing mode exports remain unchanged.

#### Action 3.2.2

Update CLI contract validation to include linearization modes.

Likely file:

```text
src/big_boy_benchmarking/cli/main.py
```

Acceptance criteria:

- `validate-contracts` validates execution modes and linearization modes;
- JSON output includes `linearization_mode_count`.

#### Action 3.2.3

Add tests for linearization mode validation.

Likely file:

```text
tests/modes/test_linearization_modes.py
```

Acceptance criteria:

- known modes validate;
- unknown mode raises;
- reserved CPU/CUDA modes are rejected by default;
- disabled mode is runnable.

## Phase 4: Artifact And Manifest Integration

### Stage 4.1: Add Artifact Path

#### Action 4.1.1

Add `linearization_manifest` to `RunPaths`.

Likely file:

```text
src/big_boy_benchmarking/artifacts/paths.py
```

Expected path:

```text
runs/<run_family_id>/runs/<run_id>/linearization_manifest.json
```

Acceptance criteria:

- path builder tests cover the new path;
- existing paths remain unchanged.

### Stage 4.2: Add Manifest Type

#### Action 4.2.1

Add a run-level manifest dataclass:

```text
LinearizationManifest
```

Likely file:

```text
src/big_boy_benchmarking/artifacts/manifests.py
```

Required fields:

```text
run_id
linearization_mode_id
linearization_config
linearization_report
report_source
conversion_records_exported
debug_record_artifacts
artifact_schema_version
```

Acceptance criteria:

- manifest serializes with `to_json_dict`;
- upstream `LinearizationConfig.to_dict()` and `LinearizationReport.to_dict()`
  payloads are accepted as mappings;
- tests cover JSON-safe serialization.

#### Action 4.2.2

Add `linearization_manifest` to required manifest category metadata.

Likely files:

```text
src/big_boy_benchmarking/artifacts/schemas.py
artifacts/schemas/artifact_schema_v001.json
```

Acceptance criteria:

- schema marker remains `bbb.v001`;
- validators/tests include the new category.

### Stage 4.3: Extend Run And Mode Manifests

#### Action 4.3.1

Extend `RunManifest` with:

```text
linearization_mode_id
linearization_benchmark_label
linearization_enabled
```

Acceptance criteria:

- existing tests and callsites are updated;
- values come from the linearization report, not guessed strings.

#### Action 4.3.2

Extend `ModeManifest` with:

```text
linearization_mode_contract
```

Acceptance criteria:

- existing execution `mode_contract` remains present;
- linearization contract is written beside it;
- tests cover both contract payloads.

## Phase 5: Timing Integration

### Stage 5.1: Add Linearization Timing Segments

#### Action 5.1.1

Add timing segment categories for:

```text
linearization_report_build
encoding_registry_build
linearize_action_selection
linearize_training_transition
torch_decision_batch_build
torch_transition_batch_build
tensor_policy_forward
tensor_action_decode
```

Likely file:

```text
src/big_boy_benchmarking/metrics/timing.py
```

Acceptance criteria:

- report and registry timing are not hidden under learner/tower/readout timing;
- tensor conversion timings are distinct from environment and learner timings;
- timing tests cover at least two new segments.

## Phase 6: Linearization Helpers

### Stage 6.1: Add Shared Helper Module

#### Action 6.1.1

Add a helper module for building configs/reports.

Likely file:

```text
src/big_boy_benchmarking/upstream/linearization.py
```

Required behavior:

- build `LinearizationConfig` for local linearization mode id;
- build `LinearizationReport` via upstream `build_linearization_report`;
- optionally build `EncodingRegistry.from_tower(...)` when a tower is supplied;
- time report and registry construction using BBB timing segments;
- return JSON-safe config/report dictionaries for artifacts.

Acceptance criteria:

- no Torch import at module import time;
- disabled mode does not construct linearized records or Torch batches;
- `none_control_flow` builds an explicit report;
- tests prove expected benchmark labels.

### Stage 6.2: Add Helper Tests

#### Action 6.2.1

Add tests for config/report helper behavior.

Likely file:

```text
tests/upstream/test_linearization.py
```

Acceptance criteria:

- `none_control_flow` report label is correct;
- `tensor_available_disabled` report label is correct;
- disabled mode does not require Torch;
- reserved modes are rejected unless explicitly allowed.

## Phase 7: Runner Integration

### Stage 7.1: Update Runner Request Contract

#### Action 7.1.1

Extend:

```text
BenchmarkRunRequest
```

with:

```text
linearization_mode_id
```

Likely file:

```text
src/big_boy_benchmarking/runners/base.py
```

Acceptance criteria:

- request contract can carry linearization condition;
- existing callers are updated.

### Stage 7.2: Update Upstream Smoke Runner

#### Action 7.2.1

Update:

```text
src/big_boy_benchmarking/runners/upstream_smoke.py
```

to write `linearization_manifest.json`.

Acceptance criteria:

- default linearization mode is `tensor_available_disabled`;
- dependency spec names `v0.7.0`;
- run and mode manifests include linearization fields;
- default run does not construct Torch batches.

### Stage 7.3: Update Counterpoint Direct Runners

#### Action 7.3.1

Update direct counterpoint runners:

```text
run_direct_masked_random
run_direct_tabular_q
```

to accept and record `linearization_mode_id`.

Acceptance criteria:

- default is `tensor_available_disabled`;
- explicit `none_control_flow` is accepted;
- linearization manifest is written;
- run manifest records linearization label;
- disabled mode does not change policy behavior.

### Stage 7.4: Update Counterpoint Tower Smoke Runner

#### Action 7.4.1

Update:

```text
run_tower_schema_smoke
```

to accept and record `linearization_mode_id`.

Acceptance criteria:

- default is `tensor_available_disabled`;
- tower smoke builds `EncodingRegistry` for disabled mode;
- registry build timing is recorded separately;
- no compatibility readout or morphism construction is introduced by default.

## Phase 8: CLI Integration

### Stage 8.1: Add CLI Option

#### Action 8.1.1

Add a linearization-mode option to relevant commands:

```text
--linearization-mode
```

Relevant commands:

```text
run-upstream-smoke
counterpoint run-direct
counterpoint tower-smoke
```

Acceptance criteria:

- default is `tensor_available_disabled`;
- choices include all four known linearization modes;
- reserved modes are rejected by default.

### Stage 8.2: Reserved Mode Handling

#### Action 8.2.1

Add explicit reserved-mode controls only if needed for tests/smoke.

Preferred first behavior:

```text
reserved modes fail clearly
```

Acceptance criteria:

- CPU/CUDA modes fail with a clear message;
- no accidental CUDA claim is possible.

## Phase 9: Documentation Updates

### Stage 9.1: Update Methods Docs

#### Action 9.1.1

Update:

```text
docs/methods/benchmark_modes.md
docs/methods/artifact_contract.md
docs/methods/timing_and_readout_discipline.md
```

Acceptance criteria:

- docs distinguish execution mode from linearization mode;
- docs name the new linearization manifest;
- docs state CPU/CUDA modes are reserved.

### Stage 9.2: Update README

#### Action 9.2.1

Update stale README dependency language from `v0.6.0` to `v0.7.0`.

Acceptance criteria:

- setup docs name `v0.7.0`;
- no claim is made that BBB has serious tensor-on/tensor-off evidence yet.

### Stage 9.3: Update Resume Note

#### Action 9.3.1

Append a short status update to:

```text
docs/design/shared_benchmark_machinery/01_004_state_collapser_tensorization_resume_note.md
```

Acceptance criteria:

- update records that the integration was executed;
- update points to implementation log;
- update does not rewrite the earlier pause history.

## Phase 10: Serious Counterpoint Design Discussion Resume

### Stage 10.1: Reopen Paused Discussion

#### Action 10.1.1

Append a Codex turn to:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
```

The turn should state:

- upstream tensorization gate is satisfied by `state_collapser v0.7.0`;
- BBB local integration has been completed by this implementation;
- the serious counterpoint design discussion can now resume;
- no serious evaluation claim has been made yet;
- the next design decision is the first serious evaluation shape.

Acceptance criteria:

- PO attribution remains intact;
- the earlier PO correction about tensorization remains explicitly credited;
- the discussion is resumed, not converted into a blueprint.

## Phase 11: Validation

### Stage 11.1: Focused Import Gate

#### Action 11.1.1

Run:

```bash
uv run python -c "from state_collapser.training import LinearizationConfig, LinearizationReport, LinearizationState, NumericBackend, TensorDeviceKind, build_linearization_report; print('ok')"
```

Acceptance criteria:

- command prints `ok`;
- installed package is `state_collapser 0.7.0`.

### Stage 11.2: CLI Contract Gate

#### Action 11.2.1

Run:

```bash
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Acceptance criteria:

- command exits 0;
- output includes execution mode count and linearization mode count.

### Stage 11.3: Focused Smoke Runs

#### Action 11.3.1

Run counterpoint direct smoke into `/private/tmp`.

Acceptance criteria:

- run succeeds;
- `linearization_manifest.json` exists;
- manifest label is `tensor_available_disabled`.

#### Action 11.3.2

Run counterpoint tower smoke into `/private/tmp`.

Acceptance criteria:

- run succeeds;
- `linearization_manifest.json` exists;
- registry/report timing segments exist;
- no compatibility readout/morphism flags are enabled by default.

### Stage 11.4: Full Test And Lint

#### Action 11.4.1

Run:

```bash
uv run pytest
```

Acceptance criteria:

- all tests pass.

#### Action 11.4.2

Run:

```bash
uv run ruff check .
```

Acceptance criteria:

- ruff passes.

## Phase 12: Completion Audit

### Stage 12.1: Implementation Log Completion

#### Action 12.1.1

Complete the implementation log.

Acceptance criteria:

- every Phase.Stage.Action is marked complete, blocked, or explicitly skipped
  by PO instruction;
- validation commands and outcomes are recorded;
- final status states whether serious counterpoint design discussion was
  resumed.

### Stage 12.2: Git Status Review

#### Action 12.2.1

Run:

```bash
git status --short --branch
```

Acceptance criteria:

- final status is recorded;
- no unexpected files are present.

## Final Completion Criteria

This integration is complete when:

- BBB pins and installs `state_collapser v0.7.0`;
- BBB has a failing-under-v0.6/passing-under-v0.7 tensorization import gate;
- dependency state records tensorization import status;
- BBB has local linearization mode contracts;
- artifacts include `linearization_manifest.json`;
- run/mode manifests record linearization condition;
- timing includes linearization/report/registry segments;
- upstream smoke, direct counterpoint, and tower counterpoint smoke paths write
  tensorization-aware artifacts;
- CLI exposes `--linearization-mode`;
- CPU and CUDA tensor modes are reserved by default;
- tests and lint pass;
- serious counterpoint design discussion is explicitly resumed in its discussion
  doc.
