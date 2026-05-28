# Shared Benchmark Machinery Design

## Status

Initial consolidated design document.

This is not an implementation gameplan.

This is not approval to edit source or tests.

This document exists because the first counterpoint implementation reached a prerequisite gate: the shared benchmark machinery that counterpoint needs has not been implemented yet.

## Authority

This document follows:

- `docs/design/shared_benchmark_machinery/README.md`
- `docs/design/first_infrastructure_slice/01_001_initial_benchmarking_goals_discussion.md`
- `docs/design/first_infrastructure_slice/01_002_state_collapser_read_only_reconnaissance.md`
- `docs/design/first_infrastructure_slice/01_003_benchmark_system_and_artifact_contract_blueprint.md`
- `docs/design/first_infrastructure_slice/01_004_benchmark_system_artifact_contract_implementation_gameplan.md`
- `docs/design/first_counterpoint_environment/01_003_counterpoint_hidden_graph_and_contraction_schema_implementation_gameplan.md`
- `docs/design/first_counterpoint_environment/01_004_counterpoint_hidden_graph_and_contraction_schema_implementation_log.md`
- Read-only inspection of `/Users/foster/state_collapser` docs and source surfaces

## Current Situation

The counterpoint implementation is intentionally paused at:

```text
Phase 0.7.1: Prerequisite Infrastructure Gate
```

The missing prerequisite is:

```text
shared benchmark machinery
```

Specifically:

- artifact writers;
- mode registry;
- seed bundles;
- metric and event rows;
- timing helpers;
- runner skeletons;
- upstream integration;
- CLI.

The current `big_boy_benchmarking` source package is still only a dependency probe:

```text
src/big_boy_benchmarking/__init__.py
src/big_boy_benchmarking/_version.py
src/big_boy_benchmarking/state_collapser_probe.py
```

The current repo does already contain a strong first infrastructure-slice blueprint and implementation gameplan. The purpose of this document is not to ignore those. The purpose is to consolidate them with the current understanding of `state_collapser`, so the next implementation gameplan can be less accidental and more clearly shared-machinery-first.

## Design Verdict

We should design the shared benchmark machinery as the stable measurement layer for this repo.

`big_boy_benchmarking` should own:

- run identity;
- artifact layout;
- artifact writing;
- benchmark mode contracts;
- seed bundles;
- timing records;
- event row schemas;
- run summaries;
- upstream dependency records;
- runner orchestration;
- CLI entry points;
- human-facing methods/environment/experiment/result docs.

`state_collapser` should own:

- tower runtime;
- partition tower;
- contraction schema primitives;
- training handoff objects;
- example smoke environments;
- provisional tower-aware learner surfaces;
- runtime snapshots and live runtime views;
- compatibility readouts when explicitly requested.

The boundary is important. `state_collapser` is not the benchmark manager. Its own evaluation doc explicitly says a polished benchmark harness with persistent artifacts and standardized result tables is not yet in place. This repo exists to build that missing layer.

## Owner Decisions From Reply Pass

The reply pass resolved the open choices that were previously written as questions.

### Existing Infrastructure Gameplan

Decision:

```text
Amend the existing first-infrastructure-slice gameplan.
```

Consequence:

The older infrastructure gameplan remains real project history. The next implementation plan should not pretend to supersede it wholesale. It should amend, clarify, and execute the shared machinery work with the current counterpoint prerequisite in view.

### First Smoke Environments

Decision:

```text
Use both plate_support_env and rl_counterpoint_v3 for the first shared-machinery smoke coverage.
```

Clarification:

This is not because `state_collapser` needs its own tests repeated here. Upstream already tests its own examples.

The purpose of BBB smoke is different:

- prove BBB can import the pinned upstream package;
- prove BBB can bind upstream surfaces through local adapter modules;
- prove BBB can write artifact manifests and event tables from real upstream runs;
- prove mode ids, seed bundles, timing rows, and readout flags survive a real run;
- prove the default BBB runner does not call compatibility readouts unless the mode asks for them;
- prove that the same machinery can touch both the mature upstream reference environment and the counterpoint lineage before serious local counterpoint work resumes.

So the smoke is a harness reality check, not a duplicate upstream correctness test.

### CLI Naming

Decision:

```text
Reserve the future `bbb` command name now.
```

Consequence:

The design may reserve `bbb` as the future console command. The first implementation can still expose `python -m big_boy_benchmarking.cli` as the primary stable entry if that is the cleaner implementation path, but docs and naming should not leave the eventual command identity ambiguous.

### Artifact Formats

Decision:

```text
Use JSON, JSONL, and CSV first.
```

Consequence:

Do not introduce Parquet, DuckDB, SQLite, or other heavier storage formats in the first shared-machinery implementation unless the Project Owner explicitly expands scope.

### Human-Facing Docs

Decision:

```text
Include the human-facing docs folder skeleton in the first shared-machinery implementation.
```

Consequence:

The first implementation should create the environment, experiment, result, and methods documentation directories and READMEs. It should not wait for counterpoint to create them.

## Design Evidence Scorecard

| Area | Score | Meaning |
| --- | ---: | --- |
| BBB design intent | 8.5/10 | Existing docs already describe the measurement machine clearly. |
| BBB implementation | 1/10 | Source package is still only dependency probe. |
| Existing infrastructure gameplan fit | 7.5/10 | Strong coverage, but should be refreshed against current upstream reality before execution. |
| `state_collapser` runtime contract clarity | 8/10 | Good enough for adapters, but mostly provisional. |
| `state_collapser` benchmark artifact support | 2.5/10 | Smoke benchmark exists, persistent artifact harness does not. |
| Combined readiness for shared machinery design | 8/10 | Ready for design and then gameplan. |

## Non-Goals

This shared machinery design does not implement:

- counterpoint environment logic;
- serious environment-family code;
- neural RL learners;
- old `rl_counterpoint` ports;
- statistical claims;
- medium or large benchmark result generation;
- upstream `state_collapser` changes.

This design also does not make upstream `state_collapser` APIs stable. It assumes they are provisional and must be isolated behind local adapter modules.

## Core Principle

The shared machinery must make every future result answerable.

For any run, a reader should be able to answer:

- what environment family and instance was run;
- which upstream `state_collapser` version was used;
- which benchmark mode was active;
- which schema was active;
- which learner/controller was active;
- which seed bundle was used;
- which budget was used;
- which online costs were counted;
- which diagnostics were posthoc;
- whether compatibility readouts or morphism construction were requested;
- where machine-readable artifacts live;
- whether the result is smoke, diagnostic, or claim-supporting evidence.

## System Boundary

### BBB-Owned Layer

`big_boy_benchmarking` should own durable benchmark semantics.

It should define stable local contracts even when upstream objects are provisional.

Examples:

- `BenchmarkModeContract`
- `SeedBundle`
- `RunManifest`
- `TimingSegmentRow`
- `EpisodeRow`
- `StepEventRow`
- `StructuralDiagnosticRow`
- `StateCollapserDependencyState`
- `BenchmarkRunRequest`
- `BenchmarkRunResult`

### Upstream-Owned Layer

`state_collapser` should be treated as a dependency under observation.

Its useful surfaces include:

- `TowerRuntime`
- `PartitionTower`
- `ContractionSchema`
- `NoContractionSchema`
- `DimensionwiseSchema`
- `RewardAggregator`
- `LiveRuntimeView`
- `RuntimeSnapshot`
- `ActionSelectionInput`
- `ActionDecision`
- `TrainingTransition`
- `StepCollector`
- `EpisodeCollector`
- `TabularQLearner`
- example environment runtimes
- `tower_runtime_bench`

But most of these are not stable top-level public API. The shared machinery should therefore keep upstream access concentrated in:

```text
src/big_boy_benchmarking/upstream/
```

No serious benchmark runner should scatter raw upstream imports across the codebase.

## Package Shape

Recommended first package shape:

```text
src/big_boy_benchmarking/
  __init__.py
  artifacts/
    __init__.py
    schemas.py
    paths.py
    manifests.py
    writers.py
    validators.py
  modes/
    __init__.py
    contracts.py
    registry.py
  metrics/
    __init__.py
    events.py
    timing.py
    summaries.py
    bootstrap.py
  seeds/
    __init__.py
    bundles.py
  runners/
    __init__.py
    base.py
    upstream_smoke.py
  upstream/
    __init__.py
    state_collapser.py
    smoke_envs.py
    readout_guards.py
  environments/
    __init__.py
    registry.py
  cli/
    __init__.py
    __main__.py
    main.py
```

This shape intentionally does not include counterpoint-specific modules. Counterpoint should come later under:

```text
src/big_boy_benchmarking/environments/counterpoint/
```

after the shared machinery exists.

## Artifact Contract

The artifact layer is the backbone.

Recommended root:

```text
artifacts/
```

Recommended layout:

```text
artifacts/
  README.md
  schemas/
    artifact_schema_v001.json
  runs/
    <run_family_id>/
      family_manifest.json
      matrix_manifest.json
      environment_family_manifest.json
      dependency_manifest.json
      run_index.jsonl
      summaries/
        summary.json
        summary.csv
        bootstrap_intervals.csv
      runs/
        <run_id>/
          run_manifest.json
          seed_bundle.json
          mode_manifest.json
          timing_summary.json
          episodes.csv
          step_events.csv
          control_events.csv
          timing_segments.csv
          structural_diagnostics.jsonl
          warnings.jsonl
          external_artifacts.json
```

### Artifact Writer Requirements

Artifact writers must:

- accept an explicit artifact root;
- avoid deriving meaning from current working directory;
- write UTF-8;
- produce deterministic JSON formatting where reasonable;
- produce stable CSV headers;
- append JSONL rows safely;
- handle no-data diagnostics explicitly;
- never present terminal stdout as the artifact of record.

### Artifact Schema Version

Every artifact family should include:

```text
artifact_schema_version: "bbb.v001"
```

This should live in one constant:

```text
ARTIFACT_SCHEMA_VERSION = "bbb.v001"
```

### Tracked Versus Untracked Artifacts

Track:

- artifact README files;
- schema files;
- tiny curated smoke artifacts if intentionally added;
- human-facing summaries.

Ignore:

- large step events;
- control events;
- structural diagnostics dumps;
- binary model checkpoints;
- large arrays;
- Parquet/DuckDB/SQLite outputs until explicitly curated.

## Manifest Contract

The first shared manifest types should include:

- `FamilyManifest`
- `MatrixManifest`
- `EnvironmentFamilyManifest`
- `DependencyManifest`
- `RunManifest`
- `ModeManifest`
- `ExternalArtifactsManifest`

These should be boring and explicit. They do not need clever inheritance.

### Required Manifest Themes

Every serious run must bind:

- repo state;
- upstream dependency state;
- environment family and instance;
- benchmark mode;
- schema id;
- learner id;
- controller id;
- seed bundle;
- budget;
- diagnostic profile;
- timing profile;
- artifact schema version;
- command or callable entry path;
- status.

## Mode Registry

Modes are contracts, not prose labels.

First canonical mode ids:

```text
direct_env_tabular
tower_empty_schema_tabular
tower_nonempty_schema_tabular
tower_exploit_explore
tower_fiber_conditioned_stage
tower_control_with_fiber_conditioned_substages
```

The registry must know which modes are runnable now and which are reserved.

### Mode Contract Fields

Recommended `BenchmarkModeContract` fields:

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

### Mode Validation Rules

Validation should reject:

- direct-env modes that claim tower runtime costs;
- nonempty-schema modes without a schema mode;
- modes without explicit readout policy;
- modes without explicit timing profile;
- reserved modes passed to ordinary runners.

## Seed Bundles

The benchmark should never treat a lone integer as a complete seed story.

Recommended fields:

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

The seed bundle is the unit of reproducible stochastic identity.

The replicate is the unit of uncertainty.

Random schemas must not share hidden seed state with learners.

## Metrics And Event Rows

Metrics should be split by lifecycle and cost.

### Online Hot-Path Rows

These are cheap enough for default runs.

Recommended row types:

- `RunIndexRow`
- `EpisodeRow`
- `StepEventRow`
- `TimingSegmentRow`
- `WarningRow`

### Control Rows

These are needed when a controller exists.

Recommended row type:

- `ControlEventRow`

Fields should eventually include:

- active tier before and after;
- control action;
- lift/descend/train/explore/exploit markers;
- lift success;
- fallback reason;
- controller diagnostics.

### Structural Rows

These may be periodic or posthoc.

Recommended row type:

- `StructuralDiagnosticRow`

Fields should explicitly say:

- exact or sampled;
- online or posthoc;
- readout-backed or not;
- diagnostic cadence;
- tier index;
- schema id;
- compression and fiber summaries when available.

### Summary Rows

Recommended row types:

- `BootstrapIntervalRow`
- per-seed summary dictionaries;
- run-family summary dictionaries.

## Timing Helpers

Timing must distinguish algorithm cost from benchmark bookkeeping.

Minimum timing segments:

- environment reset;
- environment step;
- tower reset;
- tower update;
- controller decision;
- lift/resolve;
- learner act;
- learner update;
- artifact logging;
- compatibility readout;
- morphism construction;
- posthoc diagnostics;
- summary generation.

Default timing profile should not include compatibility readout or morphism construction unless the mode explicitly requests them.

Use:

```text
time.perf_counter()
```

Do not mix timed online intervals with posthoc diagnostics without separate fields.

## Readout Discipline

This is a hard design constraint.

`state_collapser` now exposes compatibility readouts lazily. The shared machinery must preserve that discipline.

Every run should record:

```text
readout_requested
morphism_requested
uses_compatibility_readout
uses_morphism
```

Default smoke and benchmark modes should have:

```text
readout_requested: false
morphism_requested: false
```

Tests should monkeypatch upstream readout methods to prove they are not called in default hot-path runs.

## Upstream Integration

The upstream integration layer should answer:

- what `state_collapser` version is installed;
- where the package came from;
- whether a local path is involved;
- whether git state is available;
- which upstream smoke surfaces can be imported;
- which readout methods need guarding.

Recommended module:

```text
src/big_boy_benchmarking/upstream/state_collapser.py
```

Recommended object:

```text
StateCollapserDependencyState
```

Recommended fields:

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

All fields except `import_version` may be unavailable for pinned installed packages. Missing optional fields must not crash the tool.

## Upstream Smoke Environments

The first smoke registry should include at least:

```text
plate_support_env
```

It may later include:

```text
articulated_loop_env
dual_arm_manipulation_env
cable_parallel_env
parallelogram_singularity_env
rl_counterpoint_v3
```

Smoke envs are for:

- import checks;
- runner shape;
- artifact writing;
- readout discipline;
- timing path sanity.

Smoke envs are not serious benchmark evidence.

## Runner Skeleton

The runner layer should coordinate one mode on one environment instance under one seed bundle and one budget.

Recommended base types:

```text
BenchmarkRunRequest
BenchmarkRunResult
BenchmarkRunner
```

### Request Fields

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

### Result Fields

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

### Runner Rules

Runners must:

- accept explicit artifact roots;
- validate mode contracts before running;
- write manifests before events when possible;
- write warnings instead of silently omitting expected artifacts;
- keep smoke, diagnostic, and claim-supporting modes distinct;
- avoid business logic in CLI modules.

## CLI Shape

Use `python -m big_boy_benchmarking.cli` first.

Do not add a console script until the package stabilizes.

First commands:

```text
validate-contracts
run-upstream-smoke
summarize-smoke
```

Later commands:

```text
init-artifacts
run-matrix
summarize
inspect-run
validate-artifacts
counterpoint search-fixtures
counterpoint graph-diagnostics
counterpoint run-smoke
```

The CLI must remain thin. It should parse arguments and call package functions.

## Human-Facing Docs Layer

The shared machinery should create or support:

```text
docs/environments/
docs/experiments/
docs/results/
docs/methods/
```

The source of truth remains machine-readable artifacts.

Human docs should explain:

- what an environment family is;
- what an experiment matrix is;
- what a result summary means;
- what methods were used;
- where artifacts live;
- what claims are not being made.

## Validation Philosophy

The first implementation should be test-first in spirit.

Required tests:

- path builders are deterministic;
- artifact writers round-trip JSON/JSONL/CSV;
- mode contracts validate and reject invalid modes;
- reserved modes cannot run by default;
- seed bundles are deterministic;
- event rows serialize to flat dictionaries;
- timing recorder separates artifact logging;
- upstream dependency state handles missing git metadata;
- smoke registry imports at least one upstream env;
- readout guard counts monkeypatched calls;
- default smoke runner does not call compatibility readout;
- diagnostic smoke runner does call compatibility readout when requested;
- CLI validate command works.

## Relationship To Counterpoint

Counterpoint should not resume until the shared machinery exists.

The paused counterpoint resume gate should check for:

```text
src/big_boy_benchmarking/artifacts/
src/big_boy_benchmarking/modes/
src/big_boy_benchmarking/metrics/
src/big_boy_benchmarking/seeds/
src/big_boy_benchmarking/runners/
src/big_boy_benchmarking/upstream/
src/big_boy_benchmarking/cli/
```

And the following surfaces:

- artifact writers;
- mode registry;
- seed bundles;
- event row types;
- timing segments;
- runner skeletons.

Only then should the counterpoint gameplan continue at:

```text
Phase 0.8
```

## Relationship To Existing Infrastructure Gameplan

The existing first infrastructure-slice gameplan is still highly relevant.

The owner decision is to amend rather than erase it.

This shared-machinery design should therefore be read as an amendment layer:

- keep the old plan's core structure;
- update its scope with the current counterpoint prerequisite;
- include both `plate_support_env` and `rl_counterpoint_v3` as smoke coverage;
- reserve the `bbb` CLI name;
- keep first artifact formats to JSON, JSONL, and CSV;
- include the human-facing docs skeleton;
- preserve Prime Directive execution discipline.

The next gameplan should be written in this folder because this is now the active design area. It should explicitly identify the older infrastructure gameplan as amended source authority rather than obsolete material.

## Proposed First Implementation Slice

The first implementation slice should probably be:

```text
artifact contract
+ mode registry
+ seed bundles
+ event rows
+ timing helpers
+ upstream dependency state
+ readout guard
+ upstream smoke runner
+ python -m CLI
```

It should not include:

- counterpoint environment implementation;
- serious benchmark matrix execution;
- final statistics beyond simple smoke summaries;
- medium/large artifacts;
- neural learners.

## Design Close

The shared benchmark machinery is the measurement machine.

It should be implemented before counterpoint and before any serious environment result.

The machinery should be boring, explicit, and artifact-first:

- stable ids;
- explicit roots;
- explicit modes;
- explicit seeds;
- explicit timings;
- explicit readout flags;
- explicit upstream dependency records;
- simple writers;
- simple runners;
- thin CLI.

Once this layer exists, counterpoint can resume without carrying the benchmark system on its back.
