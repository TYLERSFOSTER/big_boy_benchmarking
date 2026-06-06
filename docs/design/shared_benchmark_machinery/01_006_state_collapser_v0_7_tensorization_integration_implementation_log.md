# State Collapser v0.7 Tensorization Integration Implementation Log

Date: 2026-05-29

Status: complete

Repository:

```text
/Users/foster/big_boy_benchmarking
```

Implementation branch:

```text
codex/state-collapser-v0-7-bbb-integration
```

Source workplan:

```text
docs/design/shared_benchmark_machinery/01_005_state_collapser_v0_7_tensorization_integration_workplan.md
```

## Approval Statement

The Project Owner asked:

```text
integrate state_collapser v0.7.0 into BBB shared machinery, then resume serious
counterpoint design discussion
```

Codex created the Phase.Stage.Action workplan, then the Project Owner replied:

```text
proceed
```

This is recorded as approval to execute the exact workplan named above.

## Phase.Stage.Action Log

### Phase 0: Execution Setup And Reality Binding

#### Action 0.1.1

Status: complete.

Project Owner approval to execute this workplan was received in conversation.
No source, test, dependency, or lockfile edits occurred before approval.

#### Action 0.1.2

Status: complete.

Re-read:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/git_practices.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md
```

No contradiction was found between the workplan and the Prime Directive.

#### Action 0.2.1

Status: complete.

Starting status before implementation branch creation:

```text
## main...origin/main [ahead 1]
?? docs/design/shared_benchmark_machinery/01_005_state_collapser_v0_7_tensorization_integration_workplan.md
```

No unexpected source/test changes were present.

#### Action 0.2.2

Status: complete.

Created and switched to:

```text
codex/state-collapser-v0-7-bbb-integration
```

Status after branch creation:

```text
## codex/state-collapser-v0-7-bbb-integration
?? docs/design/shared_benchmark_machinery/01_005_state_collapser_v0_7_tensorization_integration_workplan.md
```

#### Action 0.3.1

Status: complete.

Read:

```text
pyproject.toml
uv.lock
```

Current dependency pin:

```text
state-collapser[rl] @ git+https://github.com/TYLERSFOSTER/state_collapser.git@v0.6.0
```

Current lockfile resolves `state-collapser` from:

```text
https://github.com/TYLERSFOSTER/state_collapser.git?rev=v0.6.0#b99d78a5073506994f82060124dca74826062c4b
```

#### Action 0.3.2

Status: complete.

Read:

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

Also read representative existing tests for runner/artifact behavior:

```text
tests/runners/test_upstream_smoke_runner.py
tests/environments/counterpoint/test_runners.py
tests/artifacts/test_manifests.py
tests/artifacts/test_paths.py
```

No mismatch requiring a stop was found.

### Phase 1: Dependency Pin And Import Gate

#### Action 1.1.1

Status: complete.

Updated `pyproject.toml` dependency target from:

```text
v0.6.0
```

to:

```text
v0.7.0
```

No local editable path was introduced.

#### Action 1.1.2

Status: complete.

Initial command:

```bash
uv lock
```

Initial result:

```text
failed to open file `/Users/foster/.cache/uv/sdists-v9/.git`: Operation not permitted
```

This matched the workplan's sandbox/cache stop condition, so Codex reran with
escalated permission.

Escalated command:

```bash
uv lock
```

Result:

```text
Resolved 18 packages in 833ms
Updated state-collapser v0.6.0 -> v0.7.0
```

`uv.lock` now resolves `state-collapser` from `v0.7.0`.

#### Action 1.1.3

Status: complete.

Command:

```bash
uv sync --group dev
```

Result:

```text
Installed state-collapser==0.7.0
```

Focused import check:

```bash
uv run python -c "import state_collapser; from state_collapser.training import LinearizationConfig, LinearizationReport, LinearizationState, NumericBackend, TensorDeviceKind, build_linearization_report; print(state_collapser.__version__)"
```

Result:

```text
0.7.0
```

The local BBB environment now installs the updated dependency.

### Stage 1.2: Add Dependency Import Tests

#### Action 1.2.1

Status: complete.

Updated:

```text
src/big_boy_benchmarking/state_collapser_probe.py
tests/test_state_collapser_dependency.py
```

The dependency report now requires backend-independent tensorization imports:

```text
EncodingRegistry
LinearizationConfig
LinearizationReport
LinearizationState
NumericBackend
TensorDeviceKind
build_linearization_report
```

#### Action 1.2.2

Status: complete.

Updated optional Torch import-state coverage in:

```text
tests/upstream/test_state_collapser_dependency_state.py
```

Torch is represented as optional dependency state. A missing Torch install does
not fail the BBB suite.

### Phase 2: Upstream Dependency State Extension

#### Action 2.1.1

Status: complete.

Extended:

```text
src/big_boy_benchmarking/upstream/state_collapser.py
```

with tensorization-aware dependency state:

```text
linearization_import_status
linearization_symbols
torch_import_status
cuda_available
```

Also added the canonical BBB dependency spec:

```text
state-collapser[rl] @ git+https://github.com/TYLERSFOSTER/state_collapser.git@v0.7.0
```

#### Action 2.1.2

Status: complete.

Updated dependency-state tests. The state dictionary now records the
backend-independent linearization symbols and optional Torch/CUDA status.

Focused validation:

```bash
uv run pytest tests/test_state_collapser_dependency.py tests/upstream/test_state_collapser_dependency_state.py
```

Result:

```text
4 passed
```

### Phase 3: Linearization Mode Contracts

#### Action 3.1.1

Status: complete.

Added:

```text
src/big_boy_benchmarking/modes/linearization.py
```

The module defines `LinearizationModeContract`, validation helpers, and lookup
helpers without importing Torch.

#### Action 3.1.2

Status: complete.

Added local linearization mode entries:

```text
none_control_flow
tensor_available_disabled
tensor_enabled_cpu
tensor_enabled_cuda
```

Runnable:

```text
none_control_flow
tensor_available_disabled
```

Reserved:

```text
tensor_enabled_cpu
tensor_enabled_cuda
```

#### Action 3.2.1

Status: complete.

Exported linearization registry helpers from:

```text
src/big_boy_benchmarking/modes/__init__.py
```

Existing execution-mode exports remain present.

#### Action 3.2.2

Status: complete.

Updated:

```text
src/big_boy_benchmarking/cli/main.py
```

`validate-contracts` now validates both execution modes and linearization modes
and reports `linearization_mode_count`.

#### Action 3.2.3

Status: complete.

Added:

```text
tests/modes/test_linearization_modes.py
```

Focused validation:

```bash
uv run pytest tests/modes/test_linearization_modes.py tests/cli/test_cli.py::test_validate_contracts_command_works
```

Result:

```text
6 passed
```

### Phase 4: Artifact And Manifest Integration

#### Action 4.1.1

Status: complete.

Added `RunPaths.linearization_manifest` in:

```text
src/big_boy_benchmarking/artifacts/paths.py
tests/artifacts/test_paths.py
```

Expected run path:

```text
runs/<run_family_id>/runs/<run_id>/linearization_manifest.json
```

#### Action 4.2.1

Status: complete.

Added `LinearizationManifest` in:

```text
src/big_boy_benchmarking/artifacts/manifests.py
```

The manifest accepts JSON-safe upstream `LinearizationConfig` and
`LinearizationReport` dictionaries.

#### Action 4.2.2

Status: complete.

Added `linearization_manifest` to required manifest category metadata in:

```text
src/big_boy_benchmarking/artifacts/schemas.py
artifacts/schemas/artifact_schema_v001.json
```

Schema marker remains:

```text
bbb.v001
```

#### Action 4.3.1

Status: complete.

Extended `RunManifest` with:

```text
linearization_mode_id
linearization_benchmark_label
linearization_enabled
```

Runner callsites now source these values from the upstream linearization report.

#### Action 4.3.2

Status: complete.

Extended `ModeManifest` with:

```text
linearization_mode_contract
```

Execution mode contract and linearization mode contract are written beside one
another.

### Phase 5: Timing Integration

#### Action 5.1.1

Status: complete.

Added timing segments in:

```text
src/big_boy_benchmarking/metrics/timing.py
tests/metrics/test_timing.py
```

New segment ids:

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

### Phase 6: Linearization Helpers

#### Action 6.1.1

Status: complete.

Added:

```text
src/big_boy_benchmarking/upstream/linearization.py
```

The helper builds upstream `LinearizationConfig` and `LinearizationReport`
payloads, optionally builds `EncodingRegistry.from_tower(...)`, records
`encoding_registry_build` and `linearization_report_build` timings, and avoids
Torch imports at module import time.

#### Action 6.2.1

Status: complete.

Added:

```text
tests/upstream/test_linearization.py
```

Focused validation:

```bash
uv run pytest tests/artifacts/test_paths.py tests/artifacts/test_manifests.py tests/metrics/test_timing.py tests/upstream/test_linearization.py
```

Result:

```text
14 passed
```

### Phase 7: Runner Integration

#### Action 7.1.1

Status: complete.

Extended `BenchmarkRunRequest` with:

```text
linearization_mode_id
```

Updated tests in:

```text
tests/runners/test_base.py
```

#### Action 7.2.1

Status: complete.

Updated upstream smoke runner to default to `tensor_available_disabled`, write
`linearization_manifest.json`, record the `v0.7.0` dependency spec, and include
linearization fields in run/mode manifests.

#### Action 7.3.1

Status: complete.

Updated direct counterpoint runners:

```text
run_direct_masked_random
run_direct_tabular_q
```

Both now accept and record `linearization_mode_id`, defaulting to:

```text
tensor_available_disabled
```

#### Action 7.4.1

Status: complete.

Updated counterpoint tower smoke runner to accept and record
`linearization_mode_id`. Tower smoke builds an encoding registry for disabled
mode and records registry/report timing separately.

Focused validation:

```bash
uv run pytest tests/runners/test_base.py tests/runners/test_upstream_smoke_runner.py tests/environments/counterpoint/test_runners.py tests/cli/test_cli.py::test_counterpoint_direct_and_tower_commands_run
```

Result:

```text
7 passed
```

### Phase 8: CLI Integration

#### Action 8.1.1

Status: complete.

Added:

```text
--linearization-mode
```

to:

```text
run-upstream-smoke
counterpoint run-direct
counterpoint tower-smoke
```

Default:

```text
tensor_available_disabled
```

Choices include all four local linearization modes.

#### Action 8.2.1

Status: complete.

No extra reserved-mode override was required. Reserved CPU/CUDA modes fail
clearly through the shared linearization helper.

### Phase 9: Documentation Updates

#### Action 9.1.1

Status: complete.

Updated:

```text
docs/methods/benchmark_modes.md
docs/methods/artifact_contract.md
docs/methods/timing_and_readout_discipline.md
```

The docs now distinguish execution mode from linearization mode, name
`linearization_manifest.json`, and mark CPU/CUDA modes as reserved.

#### Action 9.2.1

Status: complete.

Updated:

```text
README.md
```

Stale dependency language now names `state_collapser v0.7.0`. The README does
not claim serious tensor-on/tensor-off evidence.

#### Action 9.3.1

Status: complete.

Updated:

```text
docs/design/shared_benchmark_machinery/01_004_state_collapser_tensorization_resume_note.md
```

The update records that the integration was executed and points to this
implementation log without rewriting the earlier pause history.

### Phase 10: Serious Counterpoint Design Discussion Resume

#### Action 10.1.1

Status: complete.

Appended a Codex resume turn to:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
```

The turn preserves the PO attribution: the Project Owner caught that
benchmarking before tensorization was not equivalent to benchmarking a
tensor-capable architecture with tensor paths disabled.

### Phase 11: Validation

#### Action 11.1.1

Status: complete.

Command:

```bash
uv run python -c "from state_collapser.training import LinearizationConfig, LinearizationReport, LinearizationState, NumericBackend, TensorDeviceKind, build_linearization_report; print('ok')"
```

Result:

```text
ok
```

The import gate is satisfied by installed `state_collapser 0.7.0`.

#### Action 11.2.1

Status: complete.

Command:

```bash
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Result:

```json
{"artifact_schema_version": "bbb.v001", "linearization_mode_count": 4, "mode_count": 7, "reserved_console_command": "bbb", "smoke_ids": ["plate_support_env", "rl_counterpoint_v3"], "status": "ok"}
```

#### Action 11.3.1

Status: complete.

Command:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint run-direct --artifact-root /private/tmp/bbb-v07-direct-smoke --instance-id tiny --policy masked-random --seed 1 --episodes 1
```

Result:

```json
{"run_id": "counterpoint_symbolic_n3_tiny_v001-direct-masked-random-0", "status": "success"}
```

Verified artifact:

```text
/private/tmp/bbb-v07-direct-smoke/runs/counterpoint_symbolic_v001_direct_v001/runs/counterpoint_symbolic_n3_tiny_v001-direct-masked-random-0/linearization_manifest.json
```

Manifest label:

```text
tensor_available_disabled
```

Timing rows include:

```text
linearization_report_build
```

#### Action 11.3.2

Status: complete.

Command:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint tower-smoke --artifact-root /private/tmp/bbb-v07-tower-smoke --instance-id tiny --schema-id counterpoint_empty_schema_v001 --seed 2
```

Result:

```json
{"run_id": "counterpoint_symbolic_n3_tiny_v001-counterpoint_empty_schema_v001-0", "status": "success"}
```

Verified artifact:

```text
/private/tmp/bbb-v07-tower-smoke/runs/counterpoint_symbolic_v001_tower_smoke_v001/runs/counterpoint_symbolic_n3_tiny_v001-counterpoint_empty_schema_v001-0/linearization_manifest.json
```

Manifest label:

```text
tensor_available_disabled
```

Timing rows include:

```text
encoding_registry_build
linearization_report_build
```

No compatibility readout or morphism flags are enabled by default.

#### Action 11.4.1

Status: complete.

Command:

```bash
uv run pytest
```

Final result after documentation updates:

```text
113 passed
```

#### Action 11.4.2

Status: complete.

Command:

```bash
uv run ruff check .
```

Initial result found import ordering issues in:

```text
src/big_boy_benchmarking/modes/__init__.py
src/big_boy_benchmarking/upstream/linearization.py
```

Final result after formatting/import-order fixes and documentation updates:

```text
All checks passed!
```

### Phase 12: Completion Audit

#### Action 12.1.1

Status: complete.

This implementation log records every workplan Phase.Stage.Action as complete.
No actions were blocked or skipped by later PO instruction.

Serious counterpoint design discussion was resumed in:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
```

#### Action 12.2.1

Status: complete.

Final command:

```bash
git status --short --branch
```

Final result:

```text
## codex/state-collapser-v0-7-bbb-integration
 M README.md
 M artifacts/schemas/artifact_schema_v001.json
 M docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
 M docs/design/shared_benchmark_machinery/01_004_state_collapser_tensorization_resume_note.md
 M docs/methods/artifact_contract.md
 M docs/methods/benchmark_modes.md
 M docs/methods/timing_and_readout_discipline.md
 M pyproject.toml
 M src/big_boy_benchmarking/artifacts/manifests.py
 M src/big_boy_benchmarking/artifacts/paths.py
 M src/big_boy_benchmarking/artifacts/schemas.py
 M src/big_boy_benchmarking/cli/main.py
 M src/big_boy_benchmarking/environments/counterpoint/runners.py
 M src/big_boy_benchmarking/metrics/timing.py
 M src/big_boy_benchmarking/modes/__init__.py
 M src/big_boy_benchmarking/runners/base.py
 M src/big_boy_benchmarking/runners/upstream_smoke.py
 M src/big_boy_benchmarking/state_collapser_probe.py
 M src/big_boy_benchmarking/upstream/state_collapser.py
 M tests/artifacts/test_manifests.py
 M tests/artifacts/test_paths.py
 M tests/cli/test_cli.py
 M tests/environments/counterpoint/test_runners.py
 M tests/metrics/test_timing.py
 M tests/runners/test_base.py
 M tests/runners/test_upstream_smoke_runner.py
 M tests/test_state_collapser_dependency.py
 M tests/upstream/test_state_collapser_dependency_state.py
 M uv.lock
?? docs/design/shared_benchmark_machinery/01_005_state_collapser_v0_7_tensorization_integration_workplan.md
?? docs/design/shared_benchmark_machinery/01_006_state_collapser_v0_7_tensorization_integration_implementation_log.md
?? src/big_boy_benchmarking/modes/linearization.py
?? src/big_boy_benchmarking/upstream/linearization.py
?? tests/modes/test_linearization_modes.py
?? tests/upstream/test_linearization.py
```

All listed changes are expected for this integration slice.

Torch imports are not required by this test.

#### Action 1.2.2

Status: complete.

Updated:

```text
src/big_boy_benchmarking/upstream/state_collapser.py
tests/upstream/test_state_collapser_dependency_state.py
```

Optional Torch import state is recorded without requiring Torch to be installed.

Focused validation:

```bash
uv run pytest tests/test_state_collapser_dependency.py tests/upstream/test_state_collapser_dependency_state.py
```

Result:

```text
4 passed
```

### Phase 2: Upstream Dependency State Extension

#### Action 2.1.1

Status: complete.

Extended `StateCollapserDependencyState` with:

```text
linearization_import_status
linearization_symbols
torch_import_status
cuda_available
```

#### Action 2.1.2

Status: complete.

Dependency-state tests verify the new fields and pass against installed
`state_collapser v0.7.0`.

### Phase 3: Linearization Mode Contracts

#### Action 3.1.1

Status: complete.

Added:

```text
src/big_boy_benchmarking/modes/linearization.py
```

with:

```text
LinearizationModeContract
validate_linearization_mode_contract
```

The contract records upstream enum values as strings and does not import Torch.

#### Action 3.1.2

Status: complete.

Added linearization mode registry entries:

```text
none_control_flow
tensor_available_disabled
tensor_enabled_cpu
tensor_enabled_cuda
```

Runnable:

```text
none_control_flow
tensor_available_disabled
```

Reserved:

```text
tensor_enabled_cpu
tensor_enabled_cuda
```

#### Action 3.2.1

Status: complete.

Exported linearization mode helpers from:

```text
src/big_boy_benchmarking/modes/__init__.py
```

#### Action 3.2.2

Status: complete.

Updated CLI contract validation to validate linearization mode contracts and
emit `linearization_mode_count`.

#### Action 3.2.3

Status: complete.

Added:

```text
tests/modes/test_linearization_modes.py
```

Focused validation:

```bash
uv run pytest tests/modes/test_linearization_modes.py tests/cli/test_cli.py::test_validate_contracts_command_works
```

Result:

```text
6 passed
```

### Phase 4: Artifact And Manifest Integration

#### Action 4.1.1

Status: in progress.
