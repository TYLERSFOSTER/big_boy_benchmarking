# Shared Benchmark Machinery Implementation Workplan

Status: initial implementation workplan

Created: 2026-05-28

Repository: `/Users/foster/big_boy_benchmarking`

This is a workplan only.

This is not approval to implement.

This file exists to turn the shared benchmark machinery design into an
executable `Phase.Stage.Action` plan.

## Source Authority

Primary design source:

```text
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
```

Folder boundary source:

```text
docs/design/shared_benchmark_machinery/README.md
```

Amended infrastructure source:

```text
docs/design/first_infrastructure_slice/01_004_benchmark_system_artifact_contract_implementation_workplan.md
```

Counterpoint prerequisite gate source:

```text
docs/design/first_counterpoint_environment/01_003_counterpoint_hidden_graph_and_contraction_schema_implementation_workplan.md
docs/design/first_counterpoint_environment/01_004_counterpoint_hidden_graph_and_contraction_schema_implementation_log.md
```

Prime Directive source:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_001.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md
docs/prime_directive/consultant_tricks.md
docs/prime_directive/git_practices.md
```

## Realignment Contract

This workplan is deliberately narrow.

It does not implement source code.

It does not edit upstream `state_collapser`.

It does not resume counterpoint implementation.

It does not claim that any benchmark result exists.

It converts the shared machinery design into an implementation plan that can
later be approved, executed, logged, tested, and audited.

## Owner Decisions Already Bound In The Design

The following decisions are already recorded in the design source and are used
as constraints here:

- amend the existing first-infrastructure-slice workplan rather than erasing it;
- include both `plate_support_env` and `rl_counterpoint_v3` in first smoke
  coverage;
- reserve the future `bbb` command name now;
- use JSON, JSONL, and CSV as the first artifact formats;
- include the human-facing docs skeleton in the first shared-machinery
  implementation.

This workplan does not invent additional owner decisions.

When an action reaches an unresolved design choice, the action contains a stop
condition rather than a guessed answer.

## Execution Discipline

If the Project Owner later approves execution of this exact workplan, the
implementation must proceed in `Phase.Stage.Action` order unless the Project
Owner explicitly authorizes a different order.

During execution:

- re-read each action before implementing it;
- implement the exact action, not a lighter substitute;
- record every completed, blocked, or explicitly deferred action in the
  implementation log;
- stop on ambiguity, missing upstream surface, failed baseline, unexpected
  runtime error, or required simplification;
- do not use source implementation as a way to settle design questions.

## Implementation Branch Expectation

Default implementation branch:

```text
codex/shared-benchmark-machinery
```

If that branch already exists, switch to it non-destructively.

If the current worktree contains unrelated dirty files, record them before
branch work begins. If those dirty files overlap the paths in this workplan,
stop and ask for owner guidance before touching source or test files.

## Implementation Non-Goals

Do not implement:

- counterpoint hidden-graph environment logic;
- counterpoint contraction schema experiments;
- real benchmark matrices;
- neural learners;
- old `rl_counterpoint` ports;
- Parquet, DuckDB, SQLite, or external storage backends;
- scientific/statistical claims beyond smoke-status reporting;
- large generated artifact commits;
- upstream `state_collapser` changes.

## Target End State

After successful execution, the repo should have:

- explicit artifact contract and path builders;
- JSON, JSONL, and CSV writer utilities;
- mode contracts and registry;
- seed bundle contracts;
- event row and timing row contracts;
- timing helper utilities;
- upstream dependency metadata capture;
- upstream smoke environment adapter registry for `plate_support_env` and
  `rl_counterpoint_v3`;
- readout guard/counter utilities used by tests;
- runner base types;
- upstream smoke runner;
- `python -m big_boy_benchmarking.cli` entry surface;
- reserved `bbb` command identity recorded in code/docs without requiring a
  console script in this first slice;
- human-facing docs folders and seed pages;
- tests covering the shared machinery contract;
- a running implementation log that can tell another engineer exactly what
  happened.

## Phase 0: Rebind Authority, Approval, And Worktree Reality

### Stage 0.1: Re-read Prime Directive

#### Action 0.1.1

High-level purpose:

Rebind execution behavior before any source/test implementation begins.

Ground-truth files:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_001.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md
docs/prime_directive/consultant_tricks.md
docs/prime_directive/git_practices.md
```

Machine action:

```bash
cat docs/prime_directive/prime_directive.md docs/prime_directive/common_failure_mode_001.md docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md docs/prime_directive/consultant_tricks.md docs/prime_directive/git_practices.md
```

Acceptance:

- implementation log records that all six files were re-read;
- implementation log records the active obligations:
  - Project Owner approval required before source/test implementation;
  - workplan is law after approval;
  - dedicated branch required for this implementation interval;
  - global state reconstruction before edits;
  - stop on surprise, ambiguity, failed baseline, or required simplification.

Tests:

- no automated tests for this action.

Failure hypotheses:

1. A prime-directive file may have changed since this workplan was written.
2. The file list may be stale or incomplete.
3. A newer directive may supersede an assumption in this workplan.

Stop condition:

- if any listed file is missing, stop and ask.

### Stage 0.2: Re-read Design Authority

#### Action 0.2.1

High-level purpose:

Bind implementation to the shared machinery design and amended old
infrastructure plan.

Ground-truth files:

```text
docs/design/shared_benchmark_machinery/README.md
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
docs/design/first_infrastructure_slice/01_004_benchmark_system_artifact_contract_implementation_workplan.md
docs/design/first_counterpoint_environment/01_004_counterpoint_hidden_graph_and_contraction_schema_implementation_log.md
```

Machine action:

```bash
cat docs/design/shared_benchmark_machinery/README.md docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md docs/design/first_infrastructure_slice/01_004_benchmark_system_artifact_contract_implementation_workplan.md docs/design/first_counterpoint_environment/01_004_counterpoint_hidden_graph_and_contraction_schema_implementation_log.md
```

Acceptance:

- implementation log records these files as the active design authority;
- implementation log records that the older infrastructure workplan is amended
  source authority, not obsolete history;
- implementation log records that counterpoint remains paused until the shared
  machinery prerequisite gate passes.

Tests:

- no automated tests for this action.

Failure hypotheses:

1. The design file may have been edited after this workplan was created.
2. The counterpoint pause log may name a different resume gate.
3. The old infrastructure plan may conflict with the shared machinery design.

Stop condition:

- if the source documents conflict in a way that changes implementation scope,
  stop and ask.

### Stage 0.3: Project Owner Approval Gate

#### Action 0.3.1

High-level purpose:

Prevent implementation without explicit approval.

Ground-truth files:

```text
docs/design/shared_benchmark_machinery/01_002_shared_benchmark_machinery_implementation_workplan.md
```

Machine action:

```text
Record the Project Owner's explicit execution instruction in the implementation log.
```

Acceptance:

- implementation log quotes or precisely summarizes the approval instruction;
- approval names this workplan path or otherwise clearly binds this exact plan.

Tests:

- no automated tests for this action.

Failure hypotheses:

1. The owner may approve design refinement, not implementation.
2. The owner may approve only selected phases.
3. The owner may request changes before execution.

Stop condition:

- if approval is absent or ambiguous, stop.

### Stage 0.4: Inspect Git And Branch State

#### Action 0.4.1

High-level purpose:

Record the actual repo state before implementation.

Ground-truth files:

```text
.git/
```

Machine action:

```bash
git status --short --branch
```

Acceptance:

- implementation log records current branch;
- implementation log records dirty tracked and untracked paths.

Tests:

- no automated tests for this action.

Failure hypotheses:

1. The current branch may still be the paused counterpoint branch.
2. Dirty docs may belong to earlier approved design work.
3. Dirty source/test files may overlap planned implementation paths.

Stop condition:

- if dirty source/test files overlap planned paths and are not part of the
  approved shared machinery execution, stop and ask.

#### Action 0.4.2

High-level purpose:

Create or switch to the dedicated shared-machinery implementation branch.

Ground-truth files:

```text
.git/
```

Machine action:

```bash
git checkout -b codex/shared-benchmark-machinery
```

If the branch already exists, use:

```bash
git switch codex/shared-benchmark-machinery
```

Acceptance:

- active branch is `codex/shared-benchmark-machinery`;
- branch operation is recorded in the implementation log;
- no destructive git command is used.

Tests:

- no automated tests for this action.

Failure hypotheses:

1. The branch may already exist.
2. Dirty files may prevent switching.
3. Current branch base may need owner confirmation if counterpoint docs are
   still unmerged.

Stop condition:

- if switching would require stashing, committing, resetting, or discarding
  unrelated work, stop and ask.

### Stage 0.5: Create Implementation Log

#### Action 0.5.1

High-level purpose:

Create the durable execution trace before source/test edits.

Ground-truth files:

```text
docs/design/shared_benchmark_machinery/
```

Machine action:

```text
Create docs/design/shared_benchmark_machinery/01_003_shared_benchmark_machinery_implementation_log.md
```

Required initial sections:

```text
# Shared Benchmark Machinery Implementation Log

Status
Approval Statement
Source Authority
Prime Directive Rebind
Starting Git State
Global State Reconstruction
Validation Command Log
Phase.Stage.Action Completion Log
Surprises And Stop Conditions
Final Handoff
```

Acceptance:

- log file exists before implementation source/test edits;
- log identifies this workplan as the source workplan;
- log has a section where each action can be marked `completed`, `blocked`, or
  `deferred by explicit owner authorization`.

Tests:

- no automated tests for this action.

Failure hypotheses:

1. A log with the target path may already exist.
2. Existing log content may contain owner clarifications that must be preserved.
3. Another implementation interval may already be active.

Stop condition:

- if the log already exists with non-empty implementation content, stop and ask.

### Stage 0.6: Global State Reconstruction

#### Action 0.6.1

High-level purpose:

Record actual repository topology before edits.

Ground-truth files:

```text
/Users/foster/big_boy_benchmarking
```

Machine action:

```bash
pwd
git status --short --branch
rg --files
find . -maxdepth 3 -type d -print
```

Acceptance:

- implementation log records working directory;
- implementation log records branch and dirty state;
- implementation log records current visible file inventory;
- implementation log records top-level and near-top-level directory shape.

Tests:

- no automated tests for this action.

Failure hypotheses:

1. The repo may contain new files not reflected in this workplan.
2. Generated artifacts may already exist.
3. Existing package directories may make some create actions into update actions.

Stop condition:

- if existing files conflict with planned new files, stop and inspect before
  editing.

#### Action 0.6.2

High-level purpose:

Bind implementation to current package and dependency configuration.

Ground-truth files:

```text
pyproject.toml
README.md
src/big_boy_benchmarking/__init__.py
src/big_boy_benchmarking/_version.py
src/big_boy_benchmarking/state_collapser_probe.py
tests/test_state_collapser_dependency.py
.gitignore
```

Machine action:

```bash
sed -n '1,240p' pyproject.toml
sed -n '1,220p' README.md
sed -n '1,220p' src/big_boy_benchmarking/__init__.py
sed -n '1,220p' src/big_boy_benchmarking/_version.py
sed -n '1,260p' src/big_boy_benchmarking/state_collapser_probe.py
sed -n '1,260p' tests/test_state_collapser_dependency.py
sed -n '1,240p' .gitignore
```

Acceptance:

- implementation log records package name, Python version range, dependency
  pin/source, current exports, existing tests, and ignore policy.

Tests:

- no automated tests for this action.

Failure hypotheses:

1. `pyproject.toml` may already define console scripts.
2. Existing exports may have changed.
3. `.gitignore` may already contain artifact patterns.

Stop condition:

- if existing package structure is materially different from this workplan,
  stop and update the plan only with owner approval.

#### Action 0.6.3

High-level purpose:

Bind upstream dependency reality without editing upstream.

Ground-truth files:

```text
pyproject.toml
uv.lock
/Users/foster/state_collapser
```

Machine action:

```bash
uv run python -c "import importlib.metadata as m; import state_collapser; print(state_collapser.__version__); print(m.version('state-collapser'))"
```

Optional read-only local upstream check if needed:

```bash
git -C /Users/foster/state_collapser status --short --branch
```

Acceptance:

- implementation log records installed import version;
- implementation log records whether a local upstream path was inspected;
- no upstream file is edited.

Tests:

- no automated tests for this action.

Failure hypotheses:

1. Installed package version may differ from the intended pin.
2. Import metadata may use a different distribution name.
3. Local upstream repo may not match installed dependency.

Stop condition:

- if the installed upstream dependency cannot be imported, stop and ask.

### Stage 0.7: Baseline Validation

#### Action 0.7.1

High-level purpose:

Establish pre-implementation test reality.

Ground-truth files:

```text
tests/
pyproject.toml
```

Machine action:

```bash
uv run pytest
uv run ruff check .
```

Acceptance:

- implementation log records command results;
- failures are attributed as baseline failures, not implementation failures.

Tests:

- `uv run pytest`
- `uv run ruff check .`

Failure hypotheses:

1. Existing tests may fail due to dependency drift.
2. Ruff may fail due to pre-existing files.
3. Environment may require dependency sync before validation.

Stop condition:

- if either baseline command fails, stop and ask before implementation.

### Stage 0.8: Execution Method Lock

#### Action 0.8.1

High-level purpose:

Record that implementation will follow this plan exactly.

Ground-truth files:

```text
docs/design/shared_benchmark_machinery/01_002_shared_benchmark_machinery_implementation_workplan.md
docs/design/shared_benchmark_machinery/01_003_shared_benchmark_machinery_implementation_log.md
```

Machine action:

```text
Append the execution method lock to the implementation log.
```

Required log text:

```text
Implementation will proceed by Phase.Stage.Action order.
Each action text will be re-read before implementation.
No action may be marked complete if implemented only as a weaker substitute.
Any ambiguity, surprise, missing upstream surface, failed baseline, or required
simplification triggers a stop.
```

Acceptance:

- implementation log contains the method lock before Phase 1 begins.

Tests:

- no automated tests for this action.

Failure hypotheses:

1. The owner may authorize only part of this workplan.
2. A source document may require plan amendment before execution.
3. Existing worktree state may require a different branch strategy.

Stop condition:

- if the owner changes execution scope, amend the workplan before implementing.

## Phase 1: Artifact And Human Documentation Skeleton

### Stage 1.1: Artifact Root Contract

#### Action 1.1.1

High-level purpose:

Create the machine-readable artifact root skeleton.

Ground-truth files:

```text
artifacts/
.gitignore
```

Machine action:

```text
Create artifacts/
Create artifacts/README.md
Create artifacts/schemas/
Create artifacts/runs/
```

Acceptance:

- directories exist;
- `artifacts/README.md` states that artifacts are machine-readable evidence;
- README states smoke artifacts are not benchmark claims;
- README states large raw artifacts are normally untracked;
- README states every run must bind an explicit artifact root.

Tests:

- no automated tests required for directory creation.

Failure hypotheses:

1. `artifacts/` may already exist with content.
2. Existing artifacts may be generated and should not be overwritten.
3. Ignore policy may hide files that should be tracked.

Stop condition:

- if `artifacts/` already contains nontrivial run output, stop and inspect.

#### Action 1.1.2

High-level purpose:

Create the first artifact schema marker.

Ground-truth files:

```text
artifacts/schemas/
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
```

Machine action:

```text
Create artifacts/schemas/artifact_schema_v001.json
```

Acceptance:

- file declares artifact schema version `bbb.v001`;
- file lists required manifest categories;
- file lists first event table names:
  - `run_index.jsonl`;
  - `episodes.csv`;
  - `step_events.csv`;
  - `control_events.csv`;
  - `timing_segments.csv`;
  - `structural_diagnostics.jsonl`;
  - `warnings.jsonl`;
- file does not pretend to be complete JSON Schema unless complete validator
  semantics are actually implemented.

Tests:

- later artifact schema tests load this JSON.

Failure hypotheses:

1. Schema format may be mistaken for full JSON Schema.
2. Required table list may drift from writer code.
3. Future schema versions may need migration rules.

Stop condition:

- if a richer schema format is desired, stop and get owner approval before
  expanding scope.

### Stage 1.2: Artifact Ignore Policy

#### Action 1.2.1

High-level purpose:

Prevent accidental tracking of large benchmark artifacts while preserving small
contract files.

Ground-truth files:

```text
.gitignore
artifacts/
```

Machine action:

```text
Update .gitignore with benchmark artifact patterns.
```

Required ignored patterns:

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

Required non-ignored contract files:

```text
artifacts/README.md
artifacts/schemas/artifact_schema_v001.json
```

Acceptance:

- large raw artifact patterns are ignored;
- tracked contract files remain visible to git;
- no broad `artifacts/**` ignore hides curated docs/schema files.

Tests:

```bash
git check-ignore artifacts/schemas/artifact_schema_v001.json
git check-ignore artifacts/runs/example/runs/example/step_events.csv
```

Expected:

- schema file is not ignored;
- large step event file is ignored.

Failure hypotheses:

1. Existing ignore rules may already hide all of `artifacts/`.
2. Git ignore negation rules may be ordered incorrectly.
3. Future curated smoke artifacts may need explicit unignore patterns.

Stop condition:

- if preserving small curated artifacts requires complex ignore semantics, stop
  and ask.

### Stage 1.3: Human-Facing Docs Skeleton

#### Action 1.3.1

High-level purpose:

Create the docs-like layer requested by the owner for quick summaries and
details.

Ground-truth files:

```text
docs/
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
```

Machine action:

```text
Create docs/environments/
Create docs/experiments/
Create docs/results/
Create docs/methods/
Create docs/environments/README.md
Create docs/experiments/README.md
Create docs/results/README.md
Create docs/methods/README.md
```

Acceptance:

- each README explains the folder purpose;
- each README states that machine-readable artifacts remain the source of truth;
- each README states whether its contents describe environments, experiment
  matrices, result summaries, or methodology.

Tests:

- no automated tests required for docs skeleton.

Failure hypotheses:

1. Existing docs folders may already contain content.
2. README language may imply benchmark claims too early.
3. Human docs may drift from artifact contracts.

Stop condition:

- if existing docs conflict with this skeleton, stop and inspect.

### Stage 1.4: Method Docs Seed Files

#### Action 1.4.1

High-level purpose:

Seed the human-facing methods layer for the shared machinery.

Ground-truth files:

```text
docs/methods/
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
```

Machine action:

```text
Create docs/methods/artifact_contract.md
Create docs/methods/benchmark_modes.md
Create docs/methods/metric_channels.md
Create docs/methods/seed_bundles.md
Create docs/methods/statistics.md
Create docs/methods/timing_and_readout_discipline.md
```

Acceptance:

- each file is concise and human-readable;
- each file points back to the shared machinery design and artifact contracts;
- timing/readout doc states compatibility readouts and morphism construction are
  not default hot-path costs.

Tests:

- no automated tests required for method docs.

Failure hypotheses:

1. Docs may accidentally overclaim results.
2. Method docs may duplicate too much of the design file.
3. Timing/readout language may blur online and posthoc costs.

Stop condition:

- if the doc needs to settle a new statistical policy, stop and ask.

## Phase 2: Package Skeleton And Public Surface

### Stage 2.1: Create Package Subdirectories

#### Action 2.1.1

High-level purpose:

Create the shared machinery module structure without counterpoint-specific code.

Ground-truth files:

```text
src/big_boy_benchmarking/
```

Machine action:

```text
Create src/big_boy_benchmarking/artifacts/__init__.py
Create src/big_boy_benchmarking/modes/__init__.py
Create src/big_boy_benchmarking/metrics/__init__.py
Create src/big_boy_benchmarking/seeds/__init__.py
Create src/big_boy_benchmarking/runners/__init__.py
Create src/big_boy_benchmarking/upstream/__init__.py
Create src/big_boy_benchmarking/environments/__init__.py
Create src/big_boy_benchmarking/cli/__init__.py
```

Acceptance:

- package directories exist;
- no counterpoint package is created in this phase;
- package imports remain lightweight.

Tests:

```bash
uv run python -c "import big_boy_benchmarking"
```

Failure hypotheses:

1. Some directories may already exist.
2. Empty imports may mask import-time side effects elsewhere.
3. Existing package exports may require updates after new modules are added.

Stop condition:

- if an existing package directory contains conflicting implementation, stop and
  inspect.

### Stage 2.2: Public Exports

#### Action 2.2.1

High-level purpose:

Expose only stable shared contracts at package top level.

Ground-truth files:

```text
src/big_boy_benchmarking/__init__.py
```

Machine action:

```text
Update src/big_boy_benchmarking/__init__.py
```

Required preservation:

```text
__version__
dependency_report
```

Candidate first new exports:

```text
ARTIFACT_SCHEMA_VERSION
BenchmarkModeContract
SeedBundle
```

Acceptance:

- existing public exports continue to work;
- new exports are stable contract types/constants only;
- internal runner/adapters are not all exported at top level.

Tests:

```bash
uv run python -c "from big_boy_benchmarking import __version__, dependency_report"
uv run python -c "from big_boy_benchmarking import ARTIFACT_SCHEMA_VERSION, BenchmarkModeContract, SeedBundle"
```

Failure hypotheses:

1. Exporting too early may freeze unstable internals.
2. Import order may create circular imports.
3. Existing tests may assume a smaller export surface.

Stop condition:

- if top-level exports cause circular imports, stop and refactor module layout
  before proceeding.

## Phase 3: Artifact Contracts And Writers

### Stage 3.1: Artifact Constants And Paths

#### Action 3.1.1

High-level purpose:

Define schema version and deterministic path layout.

Ground-truth files:

```text
src/big_boy_benchmarking/artifacts/
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
```

Machine action:

```text
Create src/big_boy_benchmarking/artifacts/schemas.py
Create src/big_boy_benchmarking/artifacts/paths.py
```

Required implementation:

```text
ARTIFACT_SCHEMA_VERSION = "bbb.v001"
ArtifactPaths
RunFamilyPaths
RunPaths
build_run_family_paths(...)
build_run_paths(...)
```

Acceptance:

- path builders accept explicit artifact root;
- path builders do not derive meaning from current working directory;
- path builders do not create directories unless explicitly asked;
- generated paths match the design layout.

Tests:

```text
tests/artifacts/test_paths.py
```

Required test claims:

- same inputs produce same paths;
- different CWD does not change outputs when artifact root is explicit;
- run family and run paths match expected relative layout.

Failure hypotheses:

1. Path builders may accidentally resolve against CWD.
2. Dataclass path fields may omit required artifacts.
3. `Path` serialization may be inconsistent across tests.

Stop condition:

- if a path depends on ambient CWD, refactor before continuing.

### Stage 3.2: Manifest Types

#### Action 3.2.1

High-level purpose:

Define explicit manifest contracts for run families and runs.

Ground-truth files:

```text
src/big_boy_benchmarking/artifacts/
```

Machine action:

```text
Create src/big_boy_benchmarking/artifacts/manifests.py
```

Required types:

```text
FamilyManifest
MatrixManifest
EnvironmentFamilyManifest
DependencyManifest
RunManifest
ModeManifest
ExternalArtifactsManifest
```

Required helper:

```text
to_json_dict(...)
```

Acceptance:

- manifests include `artifact_schema_version`;
- manifests include ids needed to bind environment, mode, schema, learner,
  controller, seed bundle, budget, diagnostic profile, timing profile, command
  or callable entry path, status, and upstream dependency state;
- missing optional upstream metadata is represented explicitly rather than
  crashing;
- no fake data providers are added.

Tests:

```text
tests/artifacts/test_manifests.py
```

Required test claims:

- every manifest serializes to JSON-safe dictionaries;
- required identifiers are not silently dropped;
- missing optional dependency fields serialize cleanly.

Failure hypotheses:

1. Manifest classes may become too clever or inheritance-heavy.
2. Optional fields may hide genuinely required identity.
3. JSON serialization may fail on `Path`, datetime, or enum values.

Stop condition:

- if manifest requirements expose unresolved identity fields, stop and ask.

### Stage 3.3: Artifact Writers

#### Action 3.3.1

High-level purpose:

Create boring, explicit file writers for first artifact formats.

Ground-truth files:

```text
src/big_boy_benchmarking/artifacts/
```

Machine action:

```text
Create src/big_boy_benchmarking/artifacts/writers.py
```

Required functions:

```text
write_json(...)
append_jsonl(...)
write_csv(...)
append_csv_row(...)
ensure_artifact_dirs(...)
```

Acceptance:

- writers require explicit target paths or explicit `ArtifactPaths`;
- JSON writes UTF-8 with deterministic key ordering where reasonable;
- JSONL append creates parent directories only when explicitly requested by the
  caller;
- CSV headers are stable;
- append CSV row creates header when file does not exist;
- stdout is not treated as artifact of record.

Tests:

```text
tests/artifacts/test_writers.py
```

Required test claims:

- JSON round trip works;
- JSONL append/read round trip works;
- CSV headers are stable;
- appending second CSV row does not duplicate header;
- writer behavior is independent of CWD when target path is explicit.

Failure hypotheses:

1. Header order may drift if dictionaries are used carelessly.
2. Parent directory creation policy may become implicit.
3. JSON serialization may hide non-serializable objects.

Stop condition:

- if writer behavior needs implicit project roots, stop and redesign the call
  contract.

### Stage 3.4: Artifact Validators

#### Action 3.4.1

High-level purpose:

Add lightweight contract validation without overbuilding a schema engine.

Ground-truth files:

```text
src/big_boy_benchmarking/artifacts/
artifacts/schemas/artifact_schema_v001.json
```

Machine action:

```text
Create src/big_boy_benchmarking/artifacts/validators.py
```

Required functions:

```text
validate_artifact_schema_version(...)
validate_required_run_files(...)
validate_json_safe(...)
```

Acceptance:

- validators return structured validation results or raise clear `ValueError`;
- validators do not require external services;
- validators do not pretend to validate fields they do not inspect.

Tests:

```text
tests/artifacts/test_validators.py
```

Failure hypotheses:

1. Validator names may imply stronger guarantees than implemented.
2. Required file checks may accidentally require large ignored artifacts.
3. JSON safety checks may reject legitimate `None` placeholders.

Stop condition:

- if full JSON Schema validation is desired, stop and ask before adding a
  dependency or expanding scope.

## Phase 4: Mode Contracts And Registry

### Stage 4.1: Mode Contract Types

#### Action 4.1.1

High-level purpose:

Define modes as contracts, not prose labels.

Ground-truth files:

```text
src/big_boy_benchmarking/modes/
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
```

Machine action:

```text
Create src/big_boy_benchmarking/modes/contracts.py
```

Required types:

```text
BenchmarkModeContract
OnlineCostPolicy
ReadoutPolicy
MorphismPolicy
TimingProfile
DiagnosticProfile
```

Required fields on `BenchmarkModeContract`:

```text
mode_id
environment_coupling
schema_mode
controller_regime
training_surface
learner_id
diagnostic_profile
timing_profile
online_costs_included
online_costs_excluded
readout_policy
morphism_policy
runnable
reserved_reason
```

Acceptance:

- all cost, readout, morphism, timing, and diagnostic policies are explicit;
- reserved modes are representable;
- types serialize to plain dictionaries for manifests.

Tests:

```text
tests/modes/test_mode_contracts.py
```

Failure hypotheses:

1. Enums may make JSON serialization awkward.
2. String literals may be too loose without validation.
3. Mode fields may not yet cover controller modes cleanly.

Stop condition:

- if a required mode field has no clear meaning, stop and ask.

#### Action 4.1.2

High-level purpose:

Enforce the first mode contract invariants.

Ground-truth files:

```text
src/big_boy_benchmarking/modes/contracts.py
```

Machine action:

```text
Implement validate_mode_contract(...) in src/big_boy_benchmarking/modes/contracts.py
```

Required validation:

- direct-env modes cannot claim tower runtime online costs;
- nonempty-schema modes require explicit nonempty schema mode;
- every mode must have explicit readout policy;
- every mode must have explicit morphism policy;
- every mode must have explicit timing profile;
- reserved modes cannot be run unless explicitly allowed by caller.

Acceptance:

- validation errors are clear;
- validation output is deterministic;
- tests cover valid and invalid examples.

Tests:

```text
tests/modes/test_mode_contracts.py
```

Failure hypotheses:

1. Reserved/runnable semantics may be confused with test availability.
2. Direct-env mode may accidentally inherit tower timing costs.
3. Error messages may be too vague for CLI use.

Stop condition:

- if mode validation needs a new owner decision about mode taxonomy, stop and
  ask.

### Stage 4.2: Mode Registry

#### Action 4.2.1

High-level purpose:

Create the canonical first mode registry.

Ground-truth files:

```text
src/big_boy_benchmarking/modes/
```

Machine action:

```text
Create src/big_boy_benchmarking/modes/registry.py
```

Required mode ids:

```text
direct_env_tabular
tower_empty_schema_tabular
tower_nonempty_schema_tabular
tower_exploit_explore
tower_fiber_conditioned_stage
tower_control_with_fiber_conditioned_substages
```

Required functions:

```text
iter_mode_contracts(...)
get_mode_contract(...)
require_runnable_mode(...)
```

Acceptance:

- every registered mode validates;
- reserved future modes are present but not runnable by default;
- unknown mode id raises a clear error;
- registry has no dependency on upstream runtime imports.

Tests:

```text
tests/modes/test_mode_registry.py
```

Required test claims:

- known modes validate;
- unknown mode raises;
- reserved mode present but not runnable;
- direct-env mode excludes tower runtime costs;
- tower modes include tower-relevant costs when appropriate.

Failure hypotheses:

1. Some mode ids may be reserved without first implementation support.
2. Registry may accidentally import heavy upstream modules.
3. Runnable mode set may be too broad for first smoke runner.

Stop condition:

- if implementation support for a mode is unclear, mark it reserved rather than
  silently implementing a weak substitute.

## Phase 5: Seed Bundles

### Stage 5.1: Seed Bundle Contract

#### Action 5.1.1

High-level purpose:

Replace lone integer seeds with explicit seed bundles.

Ground-truth files:

```text
src/big_boy_benchmarking/seeds/
```

Machine action:

```text
Create src/big_boy_benchmarking/seeds/bundles.py
```

Required implementation:

```text
SeedBundle
seed_bundle_id(...)
generate_seed_bundles(...)
```

Required fields:

```text
seed_bundle_id
replicate_index
environment_seed
schema_seed
learner_seed
controller_seed
diagnostic_sampling_seed
artifact_sampling_seed
```

Acceptance:

- generation is deterministic from explicit base seed and replicate count;
- seed dimensions do not share hidden state;
- bundle serializes to JSON-safe dictionary;
- seed bundle id is stable for identical seed contents.

Tests:

```text
tests/seeds/test_seed_bundles.py
```

Required test claims:

- generated bundles are deterministic;
- replicate indexes are stable;
- each seed dimension is recorded separately;
- bundle id changes when seed contents change.

Failure hypotheses:

1. Python hash randomization may affect ids if hashing is careless.
2. Seed generation may accidentally use global RNG.
3. Bundle id may omit a field.

Stop condition:

- if a seed dimension needs a new semantic category, stop and update the design.

## Phase 6: Metrics, Event Rows, Timing, And Summaries

### Stage 6.1: Event Row Types

#### Action 6.1.1

High-level purpose:

Define flat row contracts for online, control, timing, structural, warning, and
summary channels.

Ground-truth files:

```text
src/big_boy_benchmarking/metrics/
```

Machine action:

```text
Create src/big_boy_benchmarking/metrics/events.py
```

Required row types:

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

- each row serializes to a flat dict;
- field order is stable for CSV headers;
- optional tower fields may be `None` for direct-env rows;
- structural rows record whether diagnostics are exact/sampled and
  online/posthoc;
- readout-backed fields are explicit.

Tests:

```text
tests/metrics/test_event_rows.py
```

Failure hypotheses:

1. Nested fields may break CSV writing.
2. Timing fields may mix online and posthoc costs.
3. Structural diagnostic rows may imply unavailable readouts.

Stop condition:

- if a row needs nested payloads, stop and decide whether that channel should be
  JSONL-only.

### Stage 6.2: Timing Helpers

#### Action 6.2.1

High-level purpose:

Measure online algorithm cost separately from benchmark bookkeeping and posthoc
diagnostics.

Ground-truth files:

```text
src/big_boy_benchmarking/metrics/
```

Machine action:

```text
Create src/big_boy_benchmarking/metrics/timing.py
```

Required implementation:

```text
TimingRecorder
timing_segment(...)
summarize_timing_segments(...)
```

Minimum segment names:

```text
environment_reset
environment_step
tower_reset
tower_update
controller_decision
lift_resolve
learner_act
learner_update
artifact_logging
compatibility_readout
morphism_construction
posthoc_diagnostics
summary_generation
```

Acceptance:

- uses `time.perf_counter()`;
- records named timing segments;
- separates algorithm online time, benchmark online time, artifact logging time,
  readout time, morphism time, posthoc diagnostic time, and summary time;
- can summarize segment totals by category.

Tests:

```text
tests/metrics/test_timing.py
```

Failure hypotheses:

1. Timing context manager may swallow exceptions.
2. Artifact logging may be counted as algorithm time.
3. Compatibility readout may appear in default timing profile accidentally.

Stop condition:

- if timing categories require a new cost taxonomy, stop and ask.

### Stage 6.3: Summary And Bootstrap Helpers

#### Action 6.3.1

High-level purpose:

Provide minimal replicate-level summaries without making statistical claims too
early.

Ground-truth files:

```text
src/big_boy_benchmarking/metrics/
```

Machine action:

```text
Create src/big_boy_benchmarking/metrics/bootstrap.py
Create src/big_boy_benchmarking/metrics/summaries.py
```

Required implementation:

```text
mean_std(...)
percentile_bootstrap_interval(...)
summarize_replicates(...)
```

Acceptance:

- bootstrap operates over replicate-level values;
- random generator is explicitly seeded;
- empty data raises clear error;
- summaries record seed count and replicate count;
- no pandas dependency is required.

Tests:

```text
tests/metrics/test_bootstrap.py
tests/metrics/test_summaries.py
```

Failure hypotheses:

1. Bootstrap helper may treat steps as independent replicates.
2. Empty data may produce misleading NaN summaries.
3. Randomness may use global RNG.

Stop condition:

- if serious statistical reporting is requested, write a separate statistics
  design before expanding this helper.

## Phase 7: Upstream Integration, Smoke Adapters, And Readout Guards

### Stage 7.1: Dependency Metadata

#### Action 7.1.1

High-level purpose:

Record upstream dependency state without treating upstream as benchmark manager.

Ground-truth files:

```text
src/big_boy_benchmarking/upstream/
pyproject.toml
uv.lock
```

Machine action:

```text
Create src/big_boy_benchmarking/upstream/state_collapser.py
```

Required implementation:

```text
StateCollapserDependencyState
collect_state_collapser_dependency_state(...)
```

Required fields:

```text
import_version
source_path
git_commit
git_branch
git_dirty
git_ahead_behind
dependency_spec
inspection_status
```

Acceptance:

- import version is recorded when import succeeds;
- missing git metadata is represented gracefully;
- installed pinned packages work even when no repo metadata is available;
- local path inspection is optional and read-only;
- no upstream files are edited.

Tests:

```text
tests/upstream/test_state_collapser_dependency_state.py
```

Failure hypotheses:

1. Installed package may not expose `__version__`.
2. Distribution metadata name may differ from import package name.
3. Source path may be unavailable for installed package.

Stop condition:

- if dependency import fails, stop and ask before changing dependency pins.

### Stage 7.2: Smoke Environment Registry

#### Action 7.2.1

High-level purpose:

Expose upstream smoke surfaces through local adapters rather than scattered raw
imports.

Ground-truth files:

```text
src/big_boy_benchmarking/upstream/
/Users/foster/state_collapser
```

Machine action:

```text
Create src/big_boy_benchmarking/upstream/smoke_envs.py
```

Required smoke ids:

```text
plate_support_env
rl_counterpoint_v3
```

Required functions:

```text
iter_smoke_environment_specs(...)
get_smoke_environment_spec(...)
import_smoke_environment(...)
```

Acceptance:

- registry includes both required smoke ids;
- each smoke id has an explicit import adapter;
- adapter errors name the missing upstream surface clearly;
- no upstream files are edited;
- smoke registry is for harness validation only, not benchmark claims.

Tests:

```text
tests/upstream/test_smoke_envs.py
```

Required test claims:

- `plate_support_env` adapter imports or reports a clear missing-surface error;
- `rl_counterpoint_v3` adapter imports or reports a clear missing-surface error;
- registry contains both ids;
- no adapter writes upstream files.

Failure hypotheses:

1. Pinned `state_collapser` may not expose `rl_counterpoint_v3`.
2. The local upstream repo may contain surfaces not present in the installed pin.
3. Smoke constructors may require arguments not yet modeled.

Stop condition:

- if either required smoke surface is unavailable in the installed dependency,
  stop and ask whether to adjust the dependency pin, use a local upstream path,
  or split adapter registration from runnable smoke coverage.

### Stage 7.3: Readout Guards

#### Action 7.3.1

High-level purpose:

Make readout discipline testable without making readouts hot-path defaults.

Ground-truth files:

```text
src/big_boy_benchmarking/upstream/
```

Machine action:

```text
Create src/big_boy_benchmarking/upstream/readout_guards.py
```

Required implementation:

```text
ReadoutCallCounter
```

Acceptance:

- helper supports monkeypatch-based tests;
- helper counts compatibility readout calls;
- helper can count morphism construction calls if exposed by adapter;
- helper is documented as test/diagnostic support, not production runtime logic.

Tests:

```text
tests/upstream/test_readout_guards.py
```

Failure hypotheses:

1. Upstream readout method names may differ from design assumptions.
2. Monkeypatch wrapper may alter method binding semantics.
3. Guard code may be mistaken for runtime policy enforcement.

Stop condition:

- if upstream method names differ, stop and bind actual names from code before
  writing tests.

## Phase 8: Runner Base And Upstream Smoke Runner

### Stage 8.1: Runner Base Types

#### Action 8.1.1

High-level purpose:

Define runner requests/results without assuming a specific environment family.

Ground-truth files:

```text
src/big_boy_benchmarking/runners/
src/big_boy_benchmarking/seeds/bundles.py
src/big_boy_benchmarking/modes/contracts.py
```

Machine action:

```text
Create src/big_boy_benchmarking/runners/base.py
```

Required types:

```text
BenchmarkRunRequest
BenchmarkRunResult
BenchmarkRunner
```

Required request fields:

```text
run_id
run_family_id
environment_id
mode_id
schema_id
learner_id
controller_id
seed_bundle
budget
artifact_root
diagnostic_profile
timing_profile
dependency_state
```

Required result fields:

```text
run_id
status
artifact_paths
summary_path
warning_count
started_at
ended_at
failure_reason
```

Acceptance:

- request requires explicit artifact root;
- result records artifact paths and status;
- base protocol has no direct upstream environment import;
- status values distinguish success, failure, blocked, and skipped.

Tests:

```text
tests/runners/test_base.py
```

Failure hypotheses:

1. Request may duplicate fields already in manifests.
2. Result status taxonomy may be too narrow.
3. Runner protocol may force sync-only semantics too early.

Stop condition:

- if runner status semantics require owner choice, stop and ask.

### Stage 8.2: Upstream Smoke Runner

#### Action 8.2.1

High-level purpose:

Prove the shared machinery can run a tiny upstream smoke and write artifacts.

Ground-truth files:

```text
src/big_boy_benchmarking/runners/
src/big_boy_benchmarking/upstream/smoke_envs.py
src/big_boy_benchmarking/upstream/readout_guards.py
```

Machine action:

```text
Create src/big_boy_benchmarking/runners/upstream_smoke.py
```

Required implementation:

```text
run_upstream_smoke(...)
summarize_upstream_smoke(...)
```

Required behavior:

- validate mode before run;
- collect dependency state;
- create run-family and run directories under explicit artifact root;
- write required manifests;
- write seed bundle;
- write mode manifest;
- run tiny smoke operation for selected smoke id;
- write `episodes.csv` or minimal episode summary rows;
- write `timing_segments.csv`;
- write `warnings.jsonl` for non-fatal missing optional data;
- record readout flags:
  - `readout_requested`;
  - `morphism_requested`;
  - `uses_compatibility_readout`;
  - `uses_morphism`;
- default smoke mode does not request compatibility readout;
- diagnostic smoke mode requests compatibility readout only when explicitly
  configured.

Acceptance:

- runner supports `plate_support_env`;
- runner supports `rl_counterpoint_v3` if upstream surface is available;
- if a required smoke surface is unavailable, runner reports clear blocked
  status rather than fake success;
- default runner does not call compatibility readout under monkeypatch counter;
- diagnostic runner calls compatibility readout only when requested;
- no serious benchmark claim is emitted.

Tests:

```text
tests/runners/test_upstream_smoke_runner.py
```

Required test claims:

- artifacts are written under a temporary explicit artifact root;
- default profile does not call readout;
- diagnostic profile calls readout when requested;
- missing optional data produces warning row, not crash;
- no repository artifact pollution occurs.

Failure hypotheses:

1. Upstream smoke env APIs may not share a common tiny-step interface.
2. `rl_counterpoint_v3` may be unavailable in pinned upstream.
3. Readout calls may occur indirectly through an upstream helper.

Stop condition:

- if supporting both smoke ids requires hand-rolling environment semantics or
  changing upstream, stop and ask.

## Phase 9: CLI And Reserved Command Identity

### Stage 9.1: CLI Module

#### Action 9.1.1

High-level purpose:

Expose a thin Python module CLI for contract validation and smoke runs.

Ground-truth files:

```text
src/big_boy_benchmarking/cli/
pyproject.toml
```

Machine action:

```text
Create src/big_boy_benchmarking/cli/__main__.py
Create src/big_boy_benchmarking/cli/main.py
```

Required commands:

```text
validate-contracts
run-upstream-smoke
summarize-smoke
```

Acceptance:

- CLI runs with `python -m big_boy_benchmarking.cli`;
- CLI parses explicit artifact root;
- CLI calls package functions rather than embedding business logic;
- CLI output is human-readable but not the artifact of record;
- CLI records/respects reserved future command name `bbb` in code/docs;
- no console script is added to `pyproject.toml` in this action unless owner
  explicitly approves that expansion.

Tests:

```text
tests/cli/test_cli.py
```

Required test claims:

- `python -m big_boy_benchmarking.cli --help` works;
- `validate-contracts` exits successfully;
- unknown command exits nonzero;
- run command requires explicit artifact root or uses an explicitly documented
  default test temp path only inside tests.

Failure hypotheses:

1. CLI may accidentally become the home for runner logic.
2. Console script exposure may be confused with reserving `bbb`.
3. Artifact root defaults may reintroduce ambient CWD semantics.

Stop condition:

- if owner wants a real installed `bbb` console script in this slice, stop and
  amend `pyproject.toml` action explicitly before implementation.

### Stage 9.2: CLI Validation Command

#### Action 9.2.1

High-level purpose:

Make contract validation runnable before smoke execution.

Ground-truth files:

```text
src/big_boy_benchmarking/cli/main.py
src/big_boy_benchmarking/modes/registry.py
src/big_boy_benchmarking/artifacts/validators.py
```

Machine action:

```text
Implement validate-contracts command in src/big_boy_benchmarking/cli/main.py
```

Acceptance:

- command validates registered modes;
- command validates artifact schema marker;
- command exits zero on success;
- command exits nonzero with clear message on validation failure.

Tests:

```text
tests/cli/test_cli.py
```

Failure hypotheses:

1. Contract validation may import upstream unnecessarily.
2. Error formatting may hide which contract failed.
3. Validation may mutate artifacts.

Stop condition:

- if validation needs upstream runtime imports, split pure contract validation
  from upstream validation before proceeding.

## Phase 10: Human-Facing Smoke Documentation

### Stage 10.1: Environment Docs

#### Action 10.1.1

High-level purpose:

Document smoke environment identities for humans.

Ground-truth files:

```text
docs/environments/
src/big_boy_benchmarking/upstream/smoke_envs.py
```

Machine action:

```text
Create docs/environments/upstream_smoke_plate_support.md
Create docs/environments/upstream_smoke_rl_counterpoint_v3.md
```

Acceptance:

- each file is clearly labeled as smoke/harness environment documentation;
- each file states it is not serious benchmark evidence;
- each file names the corresponding smoke id;
- each file links to or names upstream source surface where known.

Tests:

- no automated tests required.

Failure hypotheses:

1. Upstream source path may be unknown for installed dependency.
2. Human docs may overstate what smoke validates.
3. `rl_counterpoint_v3` may need unavailable-surface status.

Stop condition:

- if a smoke id cannot be mapped to an upstream surface, document blocked status
  only after owner approval.

### Stage 10.2: Experiment Docs

#### Action 10.2.1

High-level purpose:

Document the first smoke experiment as harness validation.

Ground-truth files:

```text
docs/experiments/
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
```

Machine action:

```text
Create docs/experiments/upstream_smoke_readout_discipline_v001.md
```

Acceptance:

- doc states purpose is artifact/readout/timing discipline validation;
- doc names smoke ids;
- doc names modes used;
- doc names expected artifact root shape;
- doc states no benchmark claim is made.

Tests:

- no automated tests required.

Failure hypotheses:

1. Experiment doc may read like a result.
2. Mode ids may drift from registry.
3. Artifact root may be described as implicit rather than explicit.

Stop condition:

- if experiment design expands beyond smoke validation, stop and create a
  separate experiment blueprint.

### Stage 10.3: Results Docs Seed

#### Action 10.3.1

High-level purpose:

Create the result summary page location without inventing results.

Ground-truth files:

```text
docs/results/
```

Machine action:

```text
Create docs/results/upstream_smoke_readout_discipline_v001.md
```

Acceptance:

- doc is clearly marked as pending until smoke run exists, or records actual
  smoke result only after the run is executed;
- doc links to artifacts if generated;
- doc states readout discipline pass/fail only from actual test/run output;
- doc states no scientific benchmark claim is made.

Tests:

- no automated tests required.

Failure hypotheses:

1. Result doc may accidentally fabricate a pass.
2. Artifact links may point to temporary validation output.
3. Human summary may diverge from machine artifacts.

Stop condition:

- if no smoke run has been executed, do not claim pass/fail.

### Stage 10.4: README Update

#### Action 10.4.1

High-level purpose:

Expose the shared machinery entry points without overclaiming benchmark status.

Ground-truth files:

```text
README.md
docs/environments/README.md
docs/experiments/README.md
docs/results/README.md
docs/methods/README.md
```

Machine action:

```text
Update README.md
```

Acceptance:

- README mentions shared benchmark machinery;
- README mentions artifact contract and human docs folders;
- README shows:

```bash
python -m big_boy_benchmarking.cli validate-contracts
```

- README says `bbb` is the reserved future command name if included;
- README does not claim serious benchmark results exist.

Tests:

- no automated tests required.

Failure hypotheses:

1. README may imply the CLI is more complete than it is.
2. Reserved `bbb` wording may imply an installed console script.
3. Result wording may overclaim smoke status.

Stop condition:

- if README needs marketing/product framing, stop and ask; this slice is
  infrastructure documentation.

## Phase 11: Validation Sweep

### Stage 11.1: Focused Contract Tests

#### Action 11.1.1

High-level purpose:

Validate the shared contract layers before upstream smoke.

Ground-truth files:

```text
tests/artifacts/
tests/modes/
tests/seeds/
tests/metrics/
```

Machine action:

```bash
uv run pytest tests/artifacts tests/modes tests/seeds tests/metrics
```

Acceptance:

- tests pass;
- implementation log records result.

Tests:

- same as machine action.

Failure hypotheses:

1. Contract tests may reveal path ambient-state bugs.
2. Serialization tests may reveal non-JSON-safe fields.
3. Timing tests may reveal mixed cost categories.

Stop condition:

- if failures require changing contract semantics, stop and ask before
  rewriting the plan.

### Stage 11.2: Upstream, Runner, And CLI Tests

#### Action 11.2.1

High-level purpose:

Validate upstream adapters, readout discipline, smoke runner, and CLI.

Ground-truth files:

```text
tests/upstream/
tests/runners/
tests/cli/
```

Machine action:

```bash
uv run pytest tests/upstream tests/runners tests/cli
```

Acceptance:

- tests pass;
- default smoke does not call readout;
- diagnostic smoke calls readout only when requested;
- implementation log records result.

Tests:

- same as machine action.

Failure hypotheses:

1. Upstream smoke surfaces may be unavailable.
2. Readout may be called indirectly.
3. CLI may rely on ambient artifact roots.

Stop condition:

- if `rl_counterpoint_v3` or `plate_support_env` availability conflicts with
  the design, stop and ask.

### Stage 11.3: Whole Repo Validation

#### Action 11.3.1

High-level purpose:

Run the full lint and test sweep.

Ground-truth files:

```text
src/
tests/
pyproject.toml
```

Machine action:

```bash
uv run ruff check .
uv run pytest
```

Acceptance:

- both commands pass;
- implementation log records results.

Tests:

- same as machine action.

Failure hypotheses:

1. New modules may violate lint style.
2. Existing tests may fail due to changed exports.
3. Upstream dependency may be unstable under full test execution.

Stop condition:

- if failures expose unrelated pre-existing issues, stop and classify before
  changing unrelated files.

### Stage 11.4: CLI Smoke Validation

#### Action 11.4.1

High-level purpose:

Validate command-line surfaces against real execution.

Ground-truth files:

```text
src/big_boy_benchmarking/cli/
```

Machine action:

```bash
uv run python -m big_boy_benchmarking.cli validate-contracts
uv run python -m big_boy_benchmarking.cli run-upstream-smoke --smoke-id plate_support_env --artifact-root /private/tmp/bbb-smoke-artifacts
uv run python -m big_boy_benchmarking.cli run-upstream-smoke --smoke-id rl_counterpoint_v3 --artifact-root /private/tmp/bbb-smoke-artifacts
```

Acceptance:

- `validate-contracts` exits successfully;
- smoke commands write under `/private/tmp/bbb-smoke-artifacts`;
- repo artifact pollution does not occur;
- if a smoke id is unavailable, CLI reports blocked/missing surface clearly and
  exits according to the implemented blocked-status policy;
- implementation log records results.

Tests:

- same as machine action.

Failure hypotheses:

1. `/private/tmp` may already contain stale smoke artifacts.
2. `rl_counterpoint_v3` may not exist in installed upstream.
3. CLI blocked-status semantics may need owner decision.

Stop condition:

- if the smoke command needs network access or dependency changes, stop and ask.

## Phase 12: Completion Audit And Counterpoint Resume Gate

### Stage 12.1: Phase.Stage.Action Audit

#### Action 12.1.1

High-level purpose:

Make execution history auditable.

Ground-truth files:

```text
docs/design/shared_benchmark_machinery/01_002_shared_benchmark_machinery_implementation_workplan.md
docs/design/shared_benchmark_machinery/01_003_shared_benchmark_machinery_implementation_log.md
```

Machine action:

```text
Update implementation log so every action is marked completed, blocked, or deferred by explicit owner authorization.
```

Acceptance:

- no action is unclassified;
- blocked actions name the exact blocker;
- owner-authorized deferrals quote or precisely identify the authorization.

Tests:

- no automated tests required.

Failure hypotheses:

1. An action may have been partially completed.
2. A stop condition may have required owner guidance.
3. A validation action may have failed after implementation appeared complete.

Stop condition:

- if any action was implemented as a weaker substitute, mark the workplan
  blocked rather than complete.

### Stage 12.2: Artifact Hygiene Check

#### Action 12.2.1

High-level purpose:

Ensure generated artifacts and unrelated files are not accidentally included.

Ground-truth files:

```text
.gitignore
artifacts/
/private/tmp/bbb-smoke-artifacts
```

Machine action:

```bash
git status --short
```

Acceptance:

- only intended source, test, docs, and contract files are modified/created;
- large generated smoke artifacts are not tracked;
- temporary smoke output lives under `/private/tmp/bbb-smoke-artifacts` unless
  owner explicitly approves a curated artifact.

Tests:

- no automated tests required.

Failure hypotheses:

1. Smoke runner may have written into repo artifact root.
2. Ignore rules may hide files that need review.
3. Temporary artifacts may need cleanup outside git.

Stop condition:

- if unintended large artifacts appear in git status, stop and ask before
  deleting anything.

### Stage 12.3: Counterpoint Resume Gate

#### Action 12.3.1

High-level purpose:

Record whether the paused counterpoint implementation may resume.

Ground-truth files:

```text
docs/design/first_counterpoint_environment/01_003_counterpoint_hidden_graph_and_contraction_schema_implementation_workplan.md
docs/design/first_counterpoint_environment/01_004_counterpoint_hidden_graph_and_contraction_schema_implementation_log.md
src/big_boy_benchmarking/artifacts/
src/big_boy_benchmarking/modes/
src/big_boy_benchmarking/metrics/
src/big_boy_benchmarking/seeds/
src/big_boy_benchmarking/runners/
src/big_boy_benchmarking/upstream/
src/big_boy_benchmarking/cli/
```

Machine action:

```text
Update docs/design/shared_benchmark_machinery/01_003_shared_benchmark_machinery_implementation_log.md with the counterpoint resume-gate status.
```

Acceptance:

- log states whether shared machinery prerequisite is satisfied;
- log names missing surfaces if not satisfied;
- log does not resume counterpoint automatically.

Tests:

- no automated tests required.

Failure hypotheses:

1. Shared machinery may be complete enough for counterpoint but missing one
   optional smoke path.
2. Counterpoint workplan may require a stricter gate than this plan.
3. Owner may want a new counterpoint resume workplan before implementation.

Stop condition:

- do not edit counterpoint source or tests in this action.

### Stage 12.4: Final Handoff

#### Action 12.4.1

High-level purpose:

Close the implementation interval with a compact factual handoff.

Ground-truth files:

```text
docs/design/shared_benchmark_machinery/01_003_shared_benchmark_machinery_implementation_log.md
git status --short
```

Machine action:

```text
Update implementation log with final file list, validation results, known limitations, and recommended next owner decision.
```

Acceptance:

- final log identifies completed files;
- final log records validation commands and results;
- final log records known limitations;
- final log says whether counterpoint can resume or what blocks it.

Tests:

- no automated tests required.

Failure hypotheses:

1. Final status may be mixed complete/blocked.
2. Validation may be partial due to upstream availability.
3. The next step may require owner choice rather than implementation.

Stop condition:

- if any test could not be run, report that directly rather than implying a
  clean validation sweep.

## Expected File Additions

Expected additions under docs/artifacts:

```text
artifacts/README.md
artifacts/schemas/artifact_schema_v001.json
docs/environments/README.md
docs/environments/upstream_smoke_plate_support.md
docs/environments/upstream_smoke_rl_counterpoint_v3.md
docs/experiments/README.md
docs/experiments/upstream_smoke_readout_discipline_v001.md
docs/results/README.md
docs/results/upstream_smoke_readout_discipline_v001.md
docs/methods/README.md
docs/methods/artifact_contract.md
docs/methods/benchmark_modes.md
docs/methods/metric_channels.md
docs/methods/seed_bundles.md
docs/methods/statistics.md
docs/methods/timing_and_readout_discipline.md
docs/design/shared_benchmark_machinery/01_003_shared_benchmark_machinery_implementation_log.md
```

Expected additions under package:

```text
src/big_boy_benchmarking/artifacts/__init__.py
src/big_boy_benchmarking/artifacts/schemas.py
src/big_boy_benchmarking/artifacts/paths.py
src/big_boy_benchmarking/artifacts/manifests.py
src/big_boy_benchmarking/artifacts/writers.py
src/big_boy_benchmarking/artifacts/validators.py
src/big_boy_benchmarking/modes/__init__.py
src/big_boy_benchmarking/modes/contracts.py
src/big_boy_benchmarking/modes/registry.py
src/big_boy_benchmarking/metrics/__init__.py
src/big_boy_benchmarking/metrics/events.py
src/big_boy_benchmarking/metrics/timing.py
src/big_boy_benchmarking/metrics/bootstrap.py
src/big_boy_benchmarking/metrics/summaries.py
src/big_boy_benchmarking/seeds/__init__.py
src/big_boy_benchmarking/seeds/bundles.py
src/big_boy_benchmarking/runners/__init__.py
src/big_boy_benchmarking/runners/base.py
src/big_boy_benchmarking/runners/upstream_smoke.py
src/big_boy_benchmarking/upstream/__init__.py
src/big_boy_benchmarking/upstream/state_collapser.py
src/big_boy_benchmarking/upstream/smoke_envs.py
src/big_boy_benchmarking/upstream/readout_guards.py
src/big_boy_benchmarking/environments/__init__.py
src/big_boy_benchmarking/cli/__init__.py
src/big_boy_benchmarking/cli/__main__.py
src/big_boy_benchmarking/cli/main.py
```

Expected additions under tests:

```text
tests/artifacts/test_paths.py
tests/artifacts/test_manifests.py
tests/artifacts/test_writers.py
tests/artifacts/test_validators.py
tests/modes/test_mode_contracts.py
tests/modes/test_mode_registry.py
tests/seeds/test_seed_bundles.py
tests/metrics/test_event_rows.py
tests/metrics/test_timing.py
tests/metrics/test_bootstrap.py
tests/metrics/test_summaries.py
tests/upstream/test_state_collapser_dependency_state.py
tests/upstream/test_smoke_envs.py
tests/upstream/test_readout_guards.py
tests/runners/test_base.py
tests/runners/test_upstream_smoke_runner.py
tests/cli/test_cli.py
```

Expected modifications:

```text
.gitignore
README.md
src/big_boy_benchmarking/__init__.py
```

## Explicit Approval Boundary

This workplan is not approval to implement.

Implementation requires a separate Project Owner instruction approving
execution of:

```text
docs/design/shared_benchmark_machinery/01_002_shared_benchmark_machinery_implementation_workplan.md
```

Once approved, this workplan is law unless the Project Owner explicitly amends
it.
