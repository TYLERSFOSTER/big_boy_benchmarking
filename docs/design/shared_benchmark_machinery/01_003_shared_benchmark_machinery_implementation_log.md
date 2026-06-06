# Shared Benchmark Machinery Implementation Log

Status: in progress

Created: 2026-05-28

Repository: `/Users/foster/big_boy_benchmarking`

Implementation branch:

```text
codex/shared-benchmark-machinery
```

Source workplan:

```text
docs/design/shared_benchmark_machinery/01_002_shared_benchmark_machinery_implementation_workplan.md
```

## Approval Statement

The Project Owner instructed:

```text
execute docs/design/shared_benchmark_machinery/01_002_shared_benchmark_machinery_implementation_workplan.md
```

This is recorded as explicit approval to execute the exact workplan named
above.

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

## Prime Directive Rebind

Phase 0.1.1 completed.

Re-read Prime Directive files:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_001.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md
docs/prime_directive/consultant_tricks.md
docs/prime_directive/git_practices.md
```

Operational obligations recorded:

- Project Owner approval required before source/test implementation;
- dedicated branch required for this implementation interval;
- global state reconstruction before edits;
- workplan-as-law execution after approval;
- re-read each Phase.Stage.Action before executing it;
- stop on ambiguity, surprise, failed baseline, missing upstream surface, or
  required simplification;
- do not edit upstream `/Users/foster/state_collapser`;
- do not use git destructively.

## Design Authority Re-read

Phase 0.2.1 completed.

Re-read design authority files:

```text
docs/design/shared_benchmark_machinery/README.md
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
docs/design/shared_benchmark_machinery/01_002_shared_benchmark_machinery_implementation_workplan.md
docs/design/first_infrastructure_slice/01_004_benchmark_system_artifact_contract_implementation_workplan.md
docs/design/first_counterpoint_environment/01_004_counterpoint_hidden_graph_and_contraction_schema_implementation_log.md
```

Recorded constraints:

- older first-infrastructure-slice workplan is amended source authority, not
  obsolete history;
- counterpoint implementation remains paused until shared machinery prerequisite
  gate passes;
- first shared smoke coverage includes `plate_support_env` and
  `rl_counterpoint_v3`;
- first artifact formats are JSON, JSONL, and CSV;
- future `bbb` command name is reserved but no console script is required in
  this slice;
- human-facing docs skeleton is included in this implementation.

## Starting Git State

Phase 0.4.1 completed.

Before shared-machinery branch creation:

```text
## codex/counterpoint-hidden-graph-schema-benchmark
```

Tracked shared machinery and counterpoint log files were confirmed by:

```text
git ls-files docs/design/shared_benchmark_machinery/01_002_shared_benchmark_machinery_implementation_workplan.md docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md docs/design/shared_benchmark_machinery/README.md docs/design/first_counterpoint_environment/01_004_counterpoint_hidden_graph_and_contraction_schema_implementation_log.md
```

Phase 0.4.2 completed.

Created and switched to:

```text
codex/shared-benchmark-machinery
```

## Global State Reconstruction

Phase 0.6.1 completed.

Working directory:

```text
/Users/foster/big_boy_benchmarking
```

Git status during reconstruction:

```text
## codex/shared-benchmark-machinery
?? docs/design/shared_benchmark_machinery/01_003_shared_benchmark_machinery_implementation_log.md
```

Current visible file inventory from `rg --files` included:

```text
src/big_boy_benchmarking/__init__.py
src/big_boy_benchmarking/state_collapser_probe.py
src/big_boy_benchmarking/_version.py
README.md
pyproject.toml
uv.lock
LICENSE
tests/test_state_collapser_dependency.py
docs/design/shared_benchmark_machinery/README.md
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
docs/design/shared_benchmark_machinery/01_002_shared_benchmark_machinery_implementation_workplan.md
docs/design/shared_benchmark_machinery/01_003_shared_benchmark_machinery_implementation_log.md
docs/design/first_infrastructure_slice/*
docs/design/first_counterpoint_environment/*
docs/prime_directive/*
assets/images/*
```

Top-level and near-top-level directory shape included:

```text
.
./tests
./docs
./docs/design
./docs/design/first_counterpoint_environment
./docs/design/shared_benchmark_machinery
./docs/design/first_infrastructure_slice
./docs/engineer_continuity
./docs/prime_directive
./assets
./assets/images
./src
./src/big_boy_benchmarking
```

Runtime/cache directories also observed:

```text
./.pytest_cache
./.ruff_cache
./.venv
./.git
```

Phase 0.6.2 completed.

Current package shape:

- `pyproject.toml` defines package `big-boy-benchmarking` version `0.1.0`.
- Python requirement is `>=3.11,<3.13`.
- Dependency is `state-collapser[rl] @ git+https://github.com/TYLERSFOSTER/state_collapser.git@v0.6.0`.
- Dev dependencies include `pytest`, `pytest-cov`, and `ruff`.
- Package exports only `__version__` and `dependency_report`.
- Existing source files are:
  - `src/big_boy_benchmarking/__init__.py`
  - `src/big_boy_benchmarking/_version.py`
  - `src/big_boy_benchmarking/state_collapser_probe.py`
- Existing test file is:
  - `tests/test_state_collapser_dependency.py`
- Existing `.gitignore` has standard Python/cache/tooling entries and no
  benchmark artifact policy yet.

Phase 0.6.3 completed.

Installed upstream state:

```text
state_collapser.__version__ = 0.6.0
importlib.metadata.version("state-collapser") = 0.6.0
```

No upstream files were edited.

## Validation Command Log

Phase 0.7.1 completed.

Baseline test command:

```bash
uv run pytest
```

Result:

```text
1 passed in 0.04s
```

Baseline lint command:

```bash
uv run ruff check .
```

Result:

```text
All checks passed!
```

Focused contract validation:

```bash
uv run pytest tests/artifacts tests/modes tests/seeds tests/metrics
```

Result:

```text
26 passed in 0.11s
```

Focused upstream/runner/CLI validation:

```bash
uv run pytest tests/upstream tests/runners tests/cli
```

Result:

```text
10 passed in 0.62s
```

Whole repo validation after lint fixes:

```bash
uv run ruff check .
uv run pytest
```

Result:

```text
All checks passed!
37 passed in 0.69s
```

CLI validation:

```bash
uv run python -m big_boy_benchmarking.cli validate-contracts
uv run python -m big_boy_benchmarking.cli run-upstream-smoke --smoke-id plate_support_env --artifact-root /private/tmp/bbb-smoke-artifacts
uv run python -m big_boy_benchmarking.cli run-upstream-smoke --smoke-id rl_counterpoint_v3 --artifact-root /private/tmp/bbb-smoke-artifacts
```

Result:

```text
{"artifact_schema_version": "bbb.v001", "mode_count": 6, "reserved_console_command": "bbb", "smoke_ids": ["plate_support_env", "rl_counterpoint_v3"], "status": "ok"}
{"run_id": "plate_support_env-tower_empty_schema_tabular-seed0", "status": "success"}
{"run_id": "rl_counterpoint_v3-tower_empty_schema_tabular-seed0", "status": "success"}
```

Phase 0.8.1 completed.

Execution method lock:

```text
Implementation will proceed by Phase.Stage.Action order.
Each action text will be re-read before implementation.
No action may be marked complete if implemented only as a weaker substitute.
Any ambiguity, surprise, missing upstream surface, failed baseline, or required
simplification triggers a stop.
```

## Phase.Stage.Action Completion Log

| Item | Status | Evidence |
| --- | --- | --- |
| 0.1.1 | completed | Prime Directive files re-read and obligations recorded. |
| 0.2.1 | completed | Shared machinery design authority and amended old infrastructure plan re-read. |
| 0.3.1 | completed | Owner execution instruction recorded as approval statement. |
| 0.4.1 | completed | Starting git status and tracked design files recorded. |
| 0.4.2 | completed | Dedicated implementation branch `codex/shared-benchmark-machinery` created and active. |
| 0.5.1 | completed | This implementation log exists before source/test implementation begins. |
| 0.6.1 | completed | Working directory, branch, file inventory, and directory shape recorded. |
| 0.6.2 | completed | Current package, README, test, and ignore policy inspected and recorded. |
| 0.6.3 | completed | Installed upstream `state_collapser` version recorded as `0.6.0`; upstream not edited. |
| 0.7.1 | completed | Baseline `uv run pytest` and `uv run ruff check .` passed. |
| 0.8.1 | completed | Execution method lock recorded before Phase 1. |
| 1.1.1 | completed | Created `artifacts/`, `artifacts/README.md`, `artifacts/schemas/`, and `artifacts/runs/`. |
| 1.1.2 | completed | Created `artifacts/schemas/artifact_schema_v001.json` with `bbb.v001`, required manifest categories, and first event table names. |
| 1.2.1 | completed | Added benchmark artifact ignore patterns; schema file is not ignored and generated step events are ignored. |
| 1.3.1 | completed | Created human-facing `docs/environments`, `docs/experiments`, `docs/results`, and `docs/methods` READMEs. |
| 1.4.1 | completed | Created method seed docs for artifact contract, modes, metric channels, seed bundles, statistics, and timing/readout discipline. |
| 2.1.1 | completed | Created package subdirectories and `__init__.py` files for artifacts, modes, metrics, seeds, runners, upstream, environments, and CLI. |
| 2.2.1 | completed | Updated package exports to preserve `__version__` and `dependency_report` while exposing `ARTIFACT_SCHEMA_VERSION`, `BenchmarkModeContract`, and `SeedBundle`. |
| 3.1.1 | completed | Created `artifacts/schemas.py` and `artifacts/paths.py` with `bbb.v001`, `ArtifactPaths`, `RunFamilyPaths`, `RunPaths`, and deterministic builders. |
| 3.2.1 | completed | Created manifest dataclasses and JSON-safe serialization helpers. |
| 3.3.1 | completed | Created JSON, JSONL, CSV, CSV-append, and artifact-directory writer utilities. |
| 3.4.1 | completed | Created lightweight artifact validators. |
| 4.1.1 | completed | Created mode contract types. |
| 4.1.2 | completed | Implemented mode contract validation. |
| 4.2.1 | completed | Created canonical mode registry with six first mode ids and reserved-mode handling. |
| 5.1.1 | completed | Created deterministic seed bundle contract and generator. |
| 6.1.1 | completed | Created flat event row types for run index, episode, step, control, timing, structural diagnostics, warnings, and bootstrap intervals. |
| 6.2.1 | completed | Created timing recorder and timing summary helpers. |
| 6.3.1 | completed | Created replicate-level mean/std, percentile bootstrap, and summary helpers. |
| 7.1.1 | completed | Created upstream dependency metadata capture with graceful missing git metadata. |
| 7.2.1 | completed | Created smoke environment registry for `plate_support_env` and `rl_counterpoint_v3`; both import from installed `state_collapser`. |
| 7.3.1 | completed | Created `ReadoutCallCounter` for monkeypatch-based readout tests. |
| 8.1.1 | completed | Created runner base request/result/protocol types. |
| 8.2.1 | completed | Created upstream smoke runner writing manifests, seed bundle, mode manifest, episode row, timing rows, warnings, and summaries. |
| 9.1.1 | completed | Created CLI module entry point and thin command parser; reserved `bbb` identity recorded without console script. |
| 9.2.1 | completed | Implemented `validate-contracts` command. |
| 10.1.1 | completed | Created human-facing docs for `plate_support_env` and `rl_counterpoint_v3` smoke environments. |
| 10.2.1 | completed | Created smoke experiment doc. |
| 10.3.1 | completed | Created pending results summary page without fabricated pass/fail status. |
| 10.4.1 | completed | Updated README with shared machinery, docs folders, CLI entry, and no-claims smoke boundary. |
| 11.1.1 | completed | Focused artifact/mode/seed/metric tests passed: 26 passed. |
| 11.2.1 | completed | Focused upstream/runner/CLI tests passed: 10 passed. |
| 11.3.1 | completed | Whole repo validation passed: `ruff check .` and `pytest` passed. |
| 11.4.1 | completed | CLI validate and both required upstream smoke commands succeeded under `/private/tmp/bbb-smoke-artifacts`. |
| 12.1.1 | completed | Phase.Stage.Action items classified in this log. |
| 12.2.1 | completed | Git status reviewed; only intended shared-machinery files and project docs/config are visible. `.DS_Store` files are ignored, not deleted. |
| 12.3.1 | completed | Counterpoint resume gate status recorded below. |
| 12.4.1 | completed | Final handoff section updated. |

## Surprises And Stop Conditions

False stop recorded and corrected.

Early upstream smoke-surface check incorrectly triggered a stop condition before
Phase 2 source/test implementation.

Read-only installed package inspection:

```bash
uv run python -c "import pkgutil, state_collapser; print(state_collapser.__file__); print([m.name for m in pkgutil.walk_packages(state_collapser.__path__, state_collapser.__name__ + '.') if 'plate' in m.name or 'counterpoint' in m.name])"
```

Observed:

```text
/Users/foster/big_boy_benchmarking/.venv/lib/python3.11/site-packages/state_collapser/__init__.py
[]
```

The failure was methodological: `pkgutil.walk_packages(state_collapser.__path__,
...)` did not descend into the examples namespace because
`state_collapser/examples` has no package-level `__init__.py`. That made the
examples appear absent even though importable subpackages exist.

The earlier statement that the full installed package had no
`state_collapser.examples.*` modules was incorrect.

Corrective evidence:

```bash
uv run python -c "from state_collapser.examples.plate_support_env import PlateSupportEnv; from state_collapser.examples.rl_counterpoint_v3 import RlCounterpointEnv; print(PlateSupportEnv.__name__); print(RlCounterpointEnv.__name__)"
```

Observed:

```text
PlateSupportEnv
RlCounterpointEnv
```

Additional metadata correction:

- `uv.lock` pins `state-collapser` to `v0.6.0` commit
  `b99d78a5073506994f82060124dca74826062c4b`.
- the installed distribution file list includes
  `state_collapser/examples/plate_support_env/*` and
  `state_collapser/examples/rl_counterpoint_v3/*`.
- the local upstream dirty state was not relevant to smoke-surface
  availability in the installed BBB environment.

Read-only local upstream inspection had observed:

```bash
rg -n "plate_support|rl_counterpoint_v3|counterpoint" /Users/foster/state_collapser
git -C /Users/foster/state_collapser status --short --branch
```

Observed:

- local upstream repo contains references and source/test surfaces for
  `state_collapser.examples.plate_support_env` and
  `state_collapser.examples.rl_counterpoint_v3`;
- local upstream repo is on `main...origin/main`;
- local upstream repo has unrelated dirty files:
  - `README.md`;
  - `assets/images/mathematical_model/main_light.xml`;
  - `docs/design/log_tropical_geometry/01_001_log_tropical_geometry_and_quotient_tower_discussion.pdf`;
  - `docs/design/log_tropical_geometry/01_001_log_tropical_geometry_and_quotient_tower_discussion.tex`;
  - `assets/images/mathematical_model/log_contractions.png`.

False stop:

```text
The workplan requires first smoke coverage for plate_support_env and
rl_counterpoint_v3. Those surfaces are absent from the installed pinned
state_collapser dependency, but present in the local upstream repo.
```

Corrected status:

```text
The installed pinned state_collapser dependency can import both required smoke
surfaces. Resume the workplan at Phase 2.
```

No upstream files were edited.

Corrective action completed:

```text
The implementation log was amended as a false stop / reality correction, and
execution resumed from Phase 2 per Project Owner instruction.
```

## Final Handoff

Completed files:

- artifact contract files under `artifacts/`;
- human-facing docs under `docs/environments/`, `docs/experiments/`,
  `docs/results/`, and `docs/methods/`;
- shared package modules under `src/big_boy_benchmarking/artifacts/`,
  `modes/`, `seeds/`, `metrics/`, `upstream/`, `runners/`, `cli/`, and
  `environments/`;
- focused tests under `tests/artifacts/`, `tests/modes/`, `tests/seeds/`,
  `tests/metrics/`, `tests/upstream/`, `tests/runners/`, and `tests/cli/`;
- README and `.gitignore` updates.

Known limitations:

- this slice is shared machinery only;
- no serious benchmark matrix has been run;
- no counterpoint-specific BBB environment has been implemented;
- `bbb` is reserved as a future command name but no console script is installed
  in this slice;
- smoke artifacts validate harness behavior and readout discipline, not
  scientific benchmark claims.

Counterpoint resume-gate status:

```text
Shared machinery prerequisite is now satisfied for the paused counterpoint
workplan's gate at the level requested by this implementation slice:
artifact writers, mode registry, seed bundles, event row types, timing helpers,
runner skeletons, upstream integration, and CLI are present and validated.
```

Recommended next owner decision:

```text
Return to docs/design/first_counterpoint_environment/01_003_counterpoint_hidden_graph_and_contraction_schema_implementation_workplan.md,
re-run its Phase 0.5, Phase 0.6, and Phase 0.7.1 gates, then continue at Phase
0.8 if the gate passes.
```
