# Benchmark System Artifact Contract Implementation Workplan

Status: initial implementation workplan

Created: 2026-05-27

Repository: `<repo-root>`

Source blueprint:

- `docs/design/01_003_benchmark_system_and_artifact_contract_blueprint.md`

Supporting design context:

- `docs/design/01_001_initial_benchmarking_goals_discussion.md`
- `docs/design/01_002_state_collapser_read_only_reconnaissance.md`

## Workplan Scope

This workplan implements the first infrastructure slice authorized by the
blueprint:

```text
artifact skeleton + mode registry + contract tests + readout-discipline upstream smoke
```

It is deliberately an infrastructure workplan. It does not implement the first
serious counterpoint-like benchmark family.

## Required Execution Discipline

This workplan uses `Phase.Stage.Action` format.

If the Project Owner later approves implementation, implementation must execute
the actions as written, in order, unless the Project Owner explicitly authorizes
a change.

Silent simplification is not allowed.

Silent scope reduction is not allowed.

If an action cannot be completed exactly as written, the implementation must
stop and ask the Project Owner for guidance.

## Prime Directive Compliance Contract

This workplan must be executed under the repository's Prime Directive.

Prime Directive source files:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_001.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md
docs/prime_directive/consultant_tricks.md
docs/prime_directive/git_practices.md
```

Operational consequences for this workplan:

1. Do not implement before explicit Project Owner approval.
2. After approval, create or switch to a dedicated implementation branch before
   source/test implementation work.
3. Perform global state reconstruction before edits.
4. Treat this workplan as law during implementation.
5. Re-read each Phase.Stage.Action before executing it.
6. Maintain a running implementation log.
7. Stop on ambiguity, surprise, scope conflict, failed baseline, or need for
   simplification.
8. Do not silently rewrite, compress, reorder, or reinterpret the workplan.
9. Do not edit upstream `state_collapser`.
10. Do not use git destructively.

The implementation branch should be:

```text
codex/benchmark-system-artifact-contract
```

unless the Project Owner explicitly names a different branch.

## Current Repo Baseline

Observed current files:

```text
pyproject.toml
README.md
src/big_boy_benchmarking/__init__.py
src/big_boy_benchmarking/_version.py
src/big_boy_benchmarking/state_collapser_probe.py
tests/test_state_collapser_dependency.py
docs/design/01_001_initial_benchmarking_goals_discussion.md
docs/design/01_002_state_collapser_read_only_reconnaissance.md
docs/design/01_003_benchmark_system_and_artifact_contract_blueprint.md
docs/prime_directive/*
```

Observed current package facts:

- package name in `pyproject.toml`: `big-boy-benchmarking`
- import package already exists: `big_boy_benchmarking`
- upstream dependency pinned to `state-collapser[rl]` at `v0.6.0`
- current tests only verify importability of selected upstream surfaces

## Implementation Non-Goals

Do not implement:

- counterpoint-like serious benchmark environment;
- dual-arm/shared-object serious benchmark environment;
- exact `PVol`;
- neural learner baselines;
- external artifact storage integration;
- Parquet, DuckDB, or SQLite table backends;
- full active-tier plus fiber-conditioned unified controller;
- real benchmark claims.

Do not edit:

```text
<state-collapser-repo>
```

except for read-only inspection or approved command execution.

## Target First Slice

The first slice should leave the repo with:

- artifact directory contract;
- human-facing docs directories;
- importable package modules for artifacts, modes, metrics, seeds, runners,
  upstream integration, and CLI;
- dataclass/typed contracts for manifests, modes, seed bundles, timing segments,
  and event rows;
- JSON/JSONL/CSV writer utilities;
- a mode registry containing the accepted first mode ids;
- test-first contract coverage;
- readout call-counting tests using monkeypatch only inside tests;
- a tiny upstream smoke runner or runner skeleton sufficient to validate
  artifact writing and readout discipline;
- `python -m big_boy_benchmarking.cli` entry surface;
- no serious benchmark claim.

## Phase 0: Prime Directive Setup, Branch Discipline, And Scope Lock

### Stage 0.1: Rebind Prime Directive Authority

#### Action 0.1.1

Re-read every Prime Directive file before any source/test edit:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_001.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md
docs/prime_directive/consultant_tricks.md
docs/prime_directive/git_practices.md
```

Acceptance:

- implementation log explicitly confirms all six files were re-read.
- implementation log records the operational obligations relevant to this
  workplan:
  - explicit approval before implementation;
  - dedicated branch before source/test edits;
  - global state reconstruction;
  - workplan-as-law execution;
  - stop on ambiguity/surprise.

#### Action 0.1.2

Re-read the design authority files:

```text
docs/design/01_001_initial_benchmarking_goals_discussion.md
docs/design/01_002_state_collapser_read_only_reconnaissance.md
docs/design/01_003_benchmark_system_and_artifact_contract_blueprint.md
docs/design/01_004_benchmark_system_artifact_contract_implementation_workplan.md
```

Acceptance:

- implementation log confirms these files were re-read.
- implementation log records this workplan as the implementation authority.

### Stage 0.2: Project Owner Approval Gate

#### Action 0.2.1

Confirm Project Owner approval to implement this exact workplan before editing
source or test files.

Acceptance:

- approval is recorded in the implementation log.

Stop condition:

- if approval is absent or ambiguous, stop and ask.

### Stage 0.3: Dedicated Implementation Branch

#### Action 0.3.1

Inspect current git state:

```bash
git status --short --branch
```

Acceptance:

- current branch and dirty state are recorded in the implementation log.

Stop condition:

- if unrelated dirty files exist, record them and ask before proceeding if they
  overlap implementation paths.

#### Action 0.3.2

Create or switch to the dedicated implementation branch:

```bash
git checkout -b codex/benchmark-system-artifact-contract
```

If the branch already exists, use a non-destructive switch command instead.

Acceptance:

- implementation branch is active before source/test edits.
- branch creation/switch is recorded in the implementation log.

Stop condition:

- if branch creation/switch fails, stop and ask.

### Stage 0.4: Create Implementation Log

#### Action 0.4.1

Create:

```text
docs/design/01_005_benchmark_system_artifact_contract_implementation_log.md
```

The log must include:

- source workplan path;
- approval statement;
- starting git status;
- starting file inventory;
- validation command log;
- Phase.Stage.Action completion log.

Acceptance:

- file exists before source/test implementation begins.

### Stage 0.5: Global State Reconstruction

#### Action 0.5.1

Record global repo state:

```bash
pwd
git status --short --branch
rg --files
find . -maxdepth 2 -type d -print
```

Acceptance:

- implementation log records working directory, branch, dirty state, tracked
  file inventory, and top-level directory shape.

#### Action 0.5.2

Read current package and test files:

```text
pyproject.toml
src/big_boy_benchmarking/__init__.py
src/big_boy_benchmarking/_version.py
src/big_boy_benchmarking/state_collapser_probe.py
tests/test_state_collapser_dependency.py
README.md
```

Acceptance:

- implementation log records current package shape.

#### Action 0.5.3

Record upstream dependency state without editing upstream:

```bash
uv run python -c "import state_collapser; print(state_collapser.__version__)"
```

If a local upstream path is used later, record its git status read-only.

Acceptance:

- implementation log records installed upstream version.
- no upstream files are edited.

### Stage 0.6: Baseline Validation

#### Action 0.6.1

Run the baseline checks:

```bash
uv run pytest
uv run ruff check .
```

Acceptance:

- results are recorded in the implementation log.

Stop condition:

- if baseline checks fail for unrelated existing reasons, stop and ask before
  proceeding.

### Stage 0.7: Execution Method Lock

#### Action 0.7.1

Record in the implementation log:

```text
Implementation will proceed by Phase.Stage.Action order.
Each action text will be re-read before implementation.
No action may be marked complete if implemented only as a weaker substitute.
Any ambiguity, surprise, or required simplification triggers a stop.
```

Acceptance:

- implementation log contains the execution method lock before Phase 1 begins.

## Phase 1: Directory And Documentation Skeleton

### Stage 1.1: Artifact Root

#### Action 1.1.1

Create:

```text
artifacts/
artifacts/README.md
artifacts/schemas/
artifacts/runs/
```

Acceptance:

- directories exist.
- `artifacts/README.md` explains:
  - machine-readable artifact purpose;
  - tracked versus untracked policy;
  - large artifact external-reference policy;
  - no scientific claims from smoke artifacts.

#### Action 1.1.2

Create:

```text
artifacts/schemas/artifact_schema_v001.json
```

Acceptance:

- file exists.
- schema declares at least:
  - artifact schema version `bbb.v001`;
  - required manifest categories;
  - first event table names.

Implementation note:

- the first schema may be lightweight; it must not pretend to be a full JSON
  Schema validator unless implemented as such.

### Stage 1.2: Artifact Ignore Policy

#### Action 1.2.1

Add or update `.gitignore` for benchmark artifacts.

Acceptance:

- large raw artifact patterns are ignored.
- small intentional artifacts remain trackable.

Required ignored patterns should include at least:

```text
artifacts/runs/*/runs/*/step_events.csv
artifacts/runs/*/runs/*/control_events.csv
artifacts/runs/*/runs/*/structural_diagnostics.jsonl
artifacts/runs/*/runs/*/large/
artifacts/runs/*/runs/*/*.parquet
artifacts/runs/*/runs/*/*.duckdb
artifacts/runs/*/runs/*/*.sqlite
artifacts/runs/*/runs/*/*.pt
artifacts/runs/*/runs/*/*.npy
artifacts/runs/*/runs/*/*.npz
```

Stop condition:

- if ignore policy would hide schema/README/tiny curated smoke artifacts, stop
  and adjust with Project Owner approval.

### Stage 1.3: Human-Facing Docs Directories

#### Action 1.3.1

Create:

```text
docs/environments/
docs/experiments/
docs/results/
docs/methods/
```

Acceptance:

- each directory exists.

#### Action 1.3.2

Create README files:

```text
docs/environments/README.md
docs/experiments/README.md
docs/results/README.md
docs/methods/README.md
```

Acceptance:

- each README explains folder purpose.
- each README states relationship to machine-readable artifacts.

### Stage 1.4: Method Docs Seed

#### Action 1.4.1

Create:

```text
docs/methods/artifact_contract.md
docs/methods/benchmark_modes.md
docs/methods/metric_channels.md
docs/methods/seed_bundles.md
docs/methods/statistics.md
docs/methods/timing_and_readout_discipline.md
```

Acceptance:

- each file gives a concise human-facing summary of the corresponding blueprint
  contract.
- files link back to the full blueprint.

## Phase 2: Package Module Skeleton

### Stage 2.1: Create Package Subdirectories

#### Action 2.1.1

Create package directories:

```text
src/big_boy_benchmarking/artifacts/
src/big_boy_benchmarking/modes/
src/big_boy_benchmarking/metrics/
src/big_boy_benchmarking/seeds/
src/big_boy_benchmarking/runners/
src/big_boy_benchmarking/upstream/
src/big_boy_benchmarking/environments/
src/big_boy_benchmarking/cli/
```

Acceptance:

- each directory contains `__init__.py`.

### Stage 2.2: Public Package Exports

#### Action 2.2.1

Update:

```text
src/big_boy_benchmarking/__init__.py
```

Acceptance:

- existing `__version__` and `dependency_report` exports remain.
- new exports are minimal and stable.
- do not export every internal implementation detail.

Suggested first exports:

```text
ARTIFACT_SCHEMA_VERSION
BenchmarkModeContract
SeedBundle
```

## Phase 3: Mode Contract And Registry

### Stage 3.1: Mode Contract Types

#### Action 3.1.1

Create:

```text
src/big_boy_benchmarking/modes/contracts.py
```

Implement:

```text
BenchmarkModeContract
OnlineCostPolicy
ReadoutPolicy
TimingProfile
DiagnosticProfile
```

Acceptance:

- `BenchmarkModeContract` records:
  - `mode_id`;
  - `environment_coupling`;
  - `schema_mode`;
  - `controller_regime`;
  - `training_surface`;
  - `learner_id`;
  - `diagnostic_profile`;
  - `timing_profile`;
  - `online_costs_included`;
  - `online_costs_excluded`;
  - `readout_policy`;
  - `morphism_policy`.
- values are explicit strings or enums.
- type choices pass mypy.

#### Action 3.1.2

Add validation method or function:

```text
validate_mode_contract(...)
```

Acceptance:

- direct env mode cannot claim tower runtime online costs.
- nonempty schema mode must have nonempty schema mode fields.
- readout policy must be explicit.
- validation returns structured errors or raises `ValueError` with clear
  messages.

### Stage 3.2: Mode Registry

#### Action 3.2.1

Create:

```text
src/big_boy_benchmarking/modes/registry.py
```

Implement accepted first mode ids:

```text
direct_env_tabular
tower_empty_schema_tabular
tower_nonempty_schema_tabular
tower_exploit_explore
tower_fiber_conditioned_stage
tower_control_with_fiber_conditioned_substages
```

Acceptance:

- registry exposes lookup by mode id.
- every mode validates.
- reserved future mode is marked reserved and cannot be run by default.

#### Action 3.2.2

Create tests:

```text
tests/modes/test_mode_contracts.py
tests/modes/test_mode_registry.py
```

Acceptance:

- known modes validate.
- unknown mode raises.
- reserved mode is present but not runnable.
- direct env mode excludes tower runtime costs.
- tower modes include tower runtime costs.

## Phase 4: Seed Bundle Contract

### Stage 4.1: Seed Bundle Types

#### Action 4.1.1

Create:

```text
src/big_boy_benchmarking/seeds/bundles.py
```

Implement:

```text
SeedBundle
seed_bundle_id(...)
generate_seed_bundles(...)
```

Acceptance:

- fields include:
  - `seed_bundle_id`;
  - `replicate_index`;
  - `environment_seed`;
  - `schema_seed`;
  - `learner_seed`;
  - `controller_seed`;
  - `diagnostic_sampling_seed`;
  - `artifact_sampling_seed`.
- generation is deterministic from a base seed.
- serialization is JSON-safe.

### Stage 4.2: Seed Tests

#### Action 4.2.1

Create:

```text
tests/seeds/test_seed_bundles.py
```

Acceptance:

- seed bundle serializes to dict.
- generated bundles are deterministic.
- replicate indexes are stable.
- each seed dimension is recorded separately.

## Phase 5: Artifact Contracts And Writers

### Stage 5.1: Artifact Constants And Paths

#### Action 5.1.1

Create:

```text
src/big_boy_benchmarking/artifacts/schemas.py
src/big_boy_benchmarking/artifacts/paths.py
```

Implement:

```text
ARTIFACT_SCHEMA_VERSION = "bbb.v001"
ArtifactPaths
build_run_family_paths(...)
build_run_paths(...)
```

Acceptance:

- path builders are deterministic.
- path builders do not create directories unless explicitly told to.
- paths match blueprint layout.

### Stage 5.2: Manifest Types

#### Action 5.2.1

Create:

```text
src/big_boy_benchmarking/artifacts/manifests.py
```

Implement dataclasses or typed dicts for:

```text
FamilyManifest
MatrixManifest
EnvironmentFamilyManifest
DependencyManifest
RunManifest
ModeManifest
ExternalArtifactsManifest
```

Acceptance:

- manifests include blueprint-required fields.
- manifests serialize to JSON-safe dictionaries.
- no manifest silently drops required ids.

Implementation note:

- fields may initially be broad and simple. Do not add fake data providers.

### Stage 5.3: Event Row Types

#### Action 5.3.1

Create:

```text
src/big_boy_benchmarking/metrics/events.py
```

Implement row types for:

```text
RunIndexRow
EpisodeRow
StepEventRow
ControlEventRow
TimingSegmentRow
StructuralDiagnosticRow
WarningRow
BootstrapIntervalRow
```

Acceptance:

- each row can produce a flat dict for CSV/JSONL.
- fields follow blueprint names.
- direct-env rows can leave tower fields null.

### Stage 5.4: Writers

#### Action 5.4.1

Create:

```text
src/big_boy_benchmarking/artifacts/writers.py
```

Implement:

```text
write_json(...)
append_jsonl(...)
write_csv(...)
append_csv_row(...)
ensure_artifact_dirs(...)
```

Acceptance:

- writers use UTF-8.
- CSV headers are stable.
- append functions can create files with headers when needed.
- JSON writer pretty-prints deterministic key order where reasonable.

### Stage 5.5: Artifact Tests

#### Action 5.5.1

Create:

```text
tests/artifacts/test_paths.py
tests/artifacts/test_manifests.py
tests/artifacts/test_writers.py
tests/metrics/test_event_rows.py
```

Acceptance:

- path layout matches blueprint.
- manifest required fields serialize.
- CSV headers match event row fields.
- JSONL append/read round trip works.
- writers do not require external services.

## Phase 6: Timing And Statistics

### Stage 6.1: Timing Helpers

#### Action 6.1.1

Create:

```text
src/big_boy_benchmarking/metrics/timing.py
```

Implement:

```text
TimingRecorder
timing_segment(...)
summarize_timing_segments(...)
```

Acceptance:

- uses `time.perf_counter()`.
- records named segments.
- distinguishes algorithm online time from benchmark online time.
- records artifact logging time separately.

### Stage 6.2: Bootstrap Summary Helpers

#### Action 6.2.1

Create:

```text
src/big_boy_benchmarking/metrics/bootstrap.py
src/big_boy_benchmarking/metrics/summaries.py
```

Implement:

```text
mean_std(...)
percentile_bootstrap_interval(...)
summarize_replicates(...)
```

Acceptance:

- bootstrap operates over replicate-level values.
- random generator is seedable.
- summary records seed count.
- no dependency on pandas is required.

### Stage 6.3: Timing And Statistics Tests

#### Action 6.3.1

Create:

```text
tests/metrics/test_timing.py
tests/metrics/test_bootstrap.py
tests/metrics/test_summaries.py
```

Acceptance:

- timing recorder records segments.
- algorithm and artifact totals are separate.
- bootstrap interval is deterministic under supplied seed.
- bootstrap helper rejects empty data with clear error.

## Phase 7: Upstream Integration And Readout Discipline

### Stage 7.1: Upstream Dependency Metadata

#### Action 7.1.1

Create:

```text
src/big_boy_benchmarking/upstream/state_collapser.py
```

Implement:

```text
StateCollapserDependencyState
collect_state_collapser_dependency_state(...)
```

Acceptance:

- records import version.
- records source path where discoverable.
- records git commit/dirty/ahead-behind when given a local path.
- works with pinned installed package even when git state is unavailable.
- does not edit upstream.

### Stage 7.2: Upstream Smoke Environment Access

#### Action 7.2.1

Create:

```text
src/big_boy_benchmarking/upstream/smoke_envs.py
```

Implement smoke registry for at least:

```text
plate_support_env
```

Acceptance:

- registry can import upstream plate-support environment/runtime surfaces.
- no upstream files are modified.
- missing optional surfaces raise clear errors.

### Stage 7.3: Readout Guards

#### Action 7.3.1

Create:

```text
src/big_boy_benchmarking/upstream/readout_guards.py
```

Implement test-facing helper:

```text
ReadoutCallCounter
```

Acceptance:

- helper can be used with monkeypatch in tests.
- helper counts calls to `TowerRuntime.compatibility_quotient_tiers`.
- helper is clearly documented as test/diagnostic only.

### Stage 7.4: Upstream Integration Tests

#### Action 7.4.1

Create:

```text
tests/upstream/test_state_collapser_dependency_state.py
tests/upstream/test_smoke_envs.py
tests/upstream/test_readout_guards.py
```

Acceptance:

- dependency state collects version.
- smoke registry imports plate support.
- readout guard counts monkeypatched calls.
- tests do not write upstream files.

## Phase 8: Runner Skeleton And CLI

### Stage 8.1: Runner Base Types

#### Action 8.1.1

Create:

```text
src/big_boy_benchmarking/runners/base.py
```

Implement:

```text
BenchmarkRunRequest
BenchmarkRunResult
BenchmarkRunner
```

Acceptance:

- request contains mode, seed bundle, budget, artifact paths.
- result contains run id, status, summary paths, warning count.
- base protocol does not assume a specific environment.

### Stage 8.2: Upstream Smoke Runner

#### Action 8.2.1

Create:

```text
src/big_boy_benchmarking/runners/upstream_smoke.py
```

Implement a tiny upstream smoke runner that can:

- create a run family directory;
- write required manifests;
- run a tiny plate-support smoke operation;
- write `episodes.csv` or minimal summary rows;
- write timing segments;
- optionally request compatibility readout only under diagnostic profile.

Acceptance:

- default smoke mode does not request compatibility readout.
- diagnostic smoke mode does request compatibility readout.
- both modes record flags.
- no serious benchmark claim is emitted.

Stop condition:

- if upstream `state_collapser` `v0.6.0` lacks required smoke surfaces,
  stop and ask whether to use local upstream path, adjust dependency pin, or
  reduce smoke scope.

### Stage 8.3: CLI Entry Surface

#### Action 8.3.1

Create:

```text
src/big_boy_benchmarking/cli/__main__.py
src/big_boy_benchmarking/cli/main.py
```

Implement `python -m big_boy_benchmarking.cli` with commands:

```text
validate-contracts
run-upstream-smoke
summarize-smoke
```

Acceptance:

- commands are intentionally small.
- no console script is added yet.
- CLI uses runner/module functions, not embedded business logic.

### Stage 8.4: Runner And CLI Tests

#### Action 8.4.1

Create:

```text
tests/runners/test_upstream_smoke_runner.py
tests/cli/test_cli.py
```

Acceptance:

- smoke runner writes artifact dirs in a temporary path.
- default runner does not call readout under monkeypatch counter.
- diagnostic runner does call readout under monkeypatch counter.
- CLI help or validate command works.

## Phase 9: Human-Facing Documentation Outputs

### Stage 9.1: Environment Docs Placeholder

#### Action 9.1.1

Create:

```text
docs/environments/upstream_smoke_plate_support.md
```

Acceptance:

- clearly labeled smoke environment, not serious benchmark environment.
- links to upstream source/docs where appropriate.
- states it is used for artifact/readout discipline only.

### Stage 9.2: Experiment Docs Placeholder

#### Action 9.2.1

Create:

```text
docs/experiments/upstream_smoke_readout_discipline_v001.md
```

Acceptance:

- describes first smoke experiment purpose.
- names mode ids used.
- names artifact root.
- says no benchmark claim is made.

### Stage 9.3: Results Docs Seed

#### Action 9.3.1

Create or generate:

```text
docs/results/upstream_smoke_readout_discipline_v001.md
```

Acceptance:

- summary can be tiny.
- links to smoke artifacts if generated.
- states whether readout discipline check passed.
- states no scientific benchmark claim is made.

### Stage 9.4: README Update

#### Action 9.4.1

Update:

```text
README.md
```

Acceptance:

- README mentions artifact contract work.
- README mentions human-facing docs directories.
- README shows `python -m big_boy_benchmarking.cli validate-contracts`.
- README does not claim serious benchmark results exist.

## Phase 10: Validation Sweep

### Stage 10.1: Focused Test Runs

#### Action 10.1.1

Run:

```bash
uv run pytest tests/artifacts tests/modes tests/seeds tests/metrics
```

Acceptance:

- pass result recorded in implementation log.

#### Action 10.1.2

Run:

```bash
uv run pytest tests/upstream tests/runners tests/cli
```

Acceptance:

- pass result recorded in implementation log.

### Stage 10.2: Whole Repo Validation

#### Action 10.2.1

Run:

```bash
uv run ruff check .
```

Acceptance:

- pass result recorded in implementation log.

#### Action 10.2.2

Run:

```bash
uv run pytest
```

Acceptance:

- pass result recorded in implementation log.

### Stage 10.3: CLI Smoke Validation

#### Action 10.3.1

Run:

```bash
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Acceptance:

- command exits successfully.
- result recorded in implementation log.

#### Action 10.3.2

Run:

```bash
uv run python -m big_boy_benchmarking.cli run-upstream-smoke --artifact-root <tmp-dir>/bbb-smoke-artifacts
```

Acceptance:

- command exits successfully.
- artifacts are written under `<tmp-dir>/bbb-smoke-artifacts`.
- no repo artifact pollution occurs from this validation command.
- result recorded in implementation log.

Stop condition:

- if command needs network or writes outside allowed roots unexpectedly, stop
  and ask.

## Phase 11: Final Consistency And Handoff

### Stage 11.1: Workplan Completion Audit

#### Action 11.1.1

Review this workplan and mark each Phase.Stage.Action item in the implementation
log as:

```text
completed
blocked
deferred by explicit PO authorization
```

Acceptance:

- no action is left unclassified.

### Stage 11.2: Artifact Hygiene Check

#### Action 11.2.1

Run:

```bash
git status --short
```

Acceptance:

- only intended files are modified/created.
- no large generated artifacts are accidentally tracked.

### Stage 11.3: Final Handoff Note

#### Action 11.3.1

Update implementation log with:

- completed files;
- validation results;
- known limitations;
- next recommended design doc:
  `counterpoint-like symbolic environment family blueprint`.

Acceptance:

- implementation log is complete enough for another engineer to resume.

## Expected File Additions

This implementation is expected to add files under:

```text
artifacts/
docs/environments/
docs/experiments/
docs/results/
docs/methods/
src/big_boy_benchmarking/artifacts/
src/big_boy_benchmarking/modes/
src/big_boy_benchmarking/metrics/
src/big_boy_benchmarking/seeds/
src/big_boy_benchmarking/runners/
src/big_boy_benchmarking/upstream/
src/big_boy_benchmarking/environments/
src/big_boy_benchmarking/cli/
tests/artifacts/
tests/modes/
tests/seeds/
tests/metrics/
tests/upstream/
tests/runners/
tests/cli/
```

This implementation is expected to modify:

```text
.gitignore
README.md
src/big_boy_benchmarking/__init__.py
docs/design/01_005_benchmark_system_artifact_contract_implementation_log.md
```

## Explicit Approval Boundary

This workplan is not itself approval to implement.

Implementation requires a separate Project Owner instruction approving execution
of this workplan.

Once approved, this workplan is law unless the Project Owner explicitly changes
it.
