# Benchmark System And Artifact Contract Blueprint

Status: initial blueprint

Created: 2026-05-27

Repository: `/Users/foster/big_boy_benchmarking`

Related design inputs:

- `docs/design/01_001_initial_benchmarking_goals_discussion.md`
- `docs/design/01_002_state_collapser_read_only_reconnaissance.md`

## Blueprint Verdict

We are ready for a first blueprint, but not yet for an implementation gameplan.

The thing ready to blueprint is not:

```text
the first serious benchmark run
```

and not:

```text
the final environment suite
```

and not:

```text
the definitive tower-control algorithm
```

The thing ready to blueprint is:

```text
the benchmark system contract
```

That means this document defines the vocabulary, artifact layout, benchmark
modes, metric channels, timing rules, and upstream-integration discipline that
future implementation work should follow.

The core bet is simple:

> Build the measurement machine before arguing about the first big result.

If this blueprint is accepted, the next document can be an implementation
gameplan for the artifact skeleton, readout-discipline smoke test, and first
upstream smoke matrix.

## Authority Boundaries

This document binds the authority already established in the prior design docs.

### Accepted Authority

1. `big_boy_benchmarking` is the serious benchmark and evidence repo for
   `state_collapser`.
2. Upstream `state_collapser` may be read, run, imported, installed, and pinned.
3. Upstream `state_collapser` must not be edited during this work interval.
4. Existing upstream example environments are smoke and reality-binding
   surfaces, not the serious benchmark corpus.
5. New benchmark environments at multiple scales are a core responsibility of
   this repo.
6. First evidence emphasis is structural/behavioral: the tower must build
   nontrivial structure.
7. Later evidence must also cover learning performance, runtime overhead,
   multi-seed uncertainty, and baselines.
8. Direct environment training, empty-schema tower machinery, and nonempty
   schema tower machinery must be distinct benchmark modes.
9. Exploit/explore and fiber-conditioned training are one tower-control/training
   design topic, not unrelated tracks.
10. Online runtime costs count.
11. Compatibility readouts are not default hot-path metrics.
12. Output should be machine-readable first: JSON/JSONL and CSV-style tables.
13. Small artifacts can be tracked; large artifacts should live externally and
    be linked with checksums.

### This Blueprint Does Not Yet Decide

1. The first serious new environment family.
2. The exact `PVol` estimator.
3. The final tower-control regime that combines active-tier control and
   fiber-conditioned substages.
4. Whether large event tables should use CSV, Parquet, SQLite, DuckDB, or
   another storage layer.
5. Whether this repo's import package should be named
   `big_boy_benchmarking`, `bbb`, or something else.
6. Whether benchmark environments should eventually migrate upstream.

### Non-Goals

This blueprint does not implement code.

This blueprint does not design the serious environment families in full.

This blueprint does not patch upstream `state_collapser`.

This blueprint does not claim `state_collapser` speedups.

This blueprint does not force `PVol` into a fake early metric just to make a
column exist.

## Product Definition

The product of this repo is not a demo script.

The product is a reproducible benchmark evidence system with:

- declared benchmark modes;
- pinned upstream dependency state;
- stable artifact schemas;
- cheap online metrics;
- explicit expensive diagnostics;
- multi-seed statistical summaries;
- environment-family specifications;
- smoke harnesses for upstream examples;
- serious benchmark environments at multiple scales;
- reports generated from machine-readable artifacts.

The eventual output should let a skeptical reader answer:

```text
What was run?
Against which upstream state_collapser?
On which environment instance?
With which mode, schema, controller, learner, seed bundle, and budget?
What online costs were counted?
Which diagnostics were post-hoc?
Did the tower actually materialize?
Did the controller actually use the tower?
Did learning improve?
Did wall-clock cost erase the improvement?
How uncertain is the result across seeds?
Can I rerun or audit the evidence?
```

## Core Design Principles

### Principle 1: Artifacts Before Claims

No result should matter unless it survives outside terminal output.

### Principle 2: Modes Are Contracts

A benchmark mode is not a prose label. It is a declared contract saying what
machinery is active, what costs count online, and what the learner/controller
is allowed to see.

### Principle 3: Fast Path Discipline

The benchmark must preserve upstream synthetic-Blow discipline:

- partition-tower maintenance is the hot path;
- compatibility readouts are explicit;
- expensive diagnostics are flagged;
- readout-backed metrics cannot pretend to be cheap online counters.

### Principle 4: Smoke Is Not Evidence

Upstream examples are useful for smoke runs, import checks, runner shape,
artifact writing, and readout-discipline tests. They do not satisfy the big-boy
benchmark bar.

### Principle 5: Environment Geometry Comes First

A serious environment family needs a written geometric hypothesis before it
needs a giant run matrix.

### Principle 6: Neutral Results

The harness records data. It should not label runs as "positive" or "negative"
by default. The Project Owner can interpret the evidence.

### Principle 7: Small Defaults, Rich Optional Diagnostics

Default online event logging should be compact. Rich object dumps and expensive
fiber/path diagnostics should be explicit.

### Principle 8: Every Number Has A Scope

Every metric must be tied to:

- environment;
- instance;
- scale;
- mode;
- schema;
- learner;
- controller;
- seed bundle;
- budget;
- upstream commit;
- artifact schema version.

## System Vocabulary

This section standardizes the language that implementation and later docs
should use.

### Environment Family

An environment family is a class of benchmark problems sharing one hidden
constraint geometry.

Examples:

- counterpoint-like constrained symbolic sequence;
- dual-arm shared-object manipulation;
- cable or support coupling;
- loop-closure geometry;
- singularity or bottleneck geometry.

### Environment Instance

An environment instance is one concrete problem generated from a family.

Examples:

- `counterpoint_3voice_length16_v001`;
- `dual_arm_grid8_object3_v004`;
- `plate_support_smoke_v000`.

### Scale Tier

A scale tier indicates intended use.

Recommended scale tiers:

```text
tiny
small
medium
large
stress
```

Meanings:

- `tiny`: exact diagnostics and hand inspection should be possible.
- `small`: exact or mostly exact structural diagnostics should be feasible.
- `medium`: serious benchmark size, with selective diagnostics.
- `large`: scaling and wall-clock stress, with sampled diagnostics.
- `stress`: intentionally uncomfortable for runtime and artifact systems.

### Benchmark Mode

A benchmark mode is the algorithmic condition being evaluated.

It must specify:

- environment coupling;
- tower usage;
- schema usage;
- controller regime;
- training surface;
- learner;
- online metric profile;
- diagnostic profile.

### Run Family

A run family is a group of runs sharing a benchmark matrix and scientific
purpose.

Example:

```text
2026-05-plate-support-smoke-readout-discipline
```

### Run

A run is one execution of one mode on one environment instance under one seed
bundle and one budget.

### Replicate

A replicate is one independently seeded trial inside a run family.

In this repo, a replicate should be identified by a seed bundle, not a lone
integer.

### Seed Bundle

A seed bundle records all stochastic seeds used by a run.

Suggested fields:

```text
environment_seed
schema_seed
learner_seed
controller_seed
diagnostic_sampling_seed
artifact_sampling_seed
```

Some fields may be null if unused.

### Budget

A budget is the resource envelope.

Possible budget units:

- episodes;
- environment steps;
- controller events;
- learner updates;
- wall-clock seconds;
- diagnostic checkpoints;
- training batches.

The budget must say which unit is authoritative.

## Turn Question 1: Package Name

The repo name is settled: `big_boy_benchmarking`.

The import package name is still open.

Options:

1. `big_boy_benchmarking`
2. `bbb`
3. no import package at first, scripts only

Recommendation:

Use `big_boy_benchmarking` as the import package if we go package-first. It is
clear, matches the repo, and avoids another naming layer.

### PO Answer Slot

```text
Use big_boy_benchmarking as the import package.
```

### Codex Follow-Up Slot

```text
Accepted. The import package should be `big_boy_benchmarking`.

This means the first implementation gameplan can assume:

- `src/big_boy_benchmarking/` exists;
- CLI modules live under `big_boy_benchmarking.cli`;
- tests import the package by the full repo name;
- no additional abbreviation layer is introduced yet.
```

## Benchmark Mode Contract

The benchmark mode contract is the most important thing this blueprint adds.

The earlier docs established three major comparison conditions:

1. direct environment training;
2. tower machinery with empty contraction schema;
3. tower machinery with nonempty contraction schema.

The reconnaissance document added a second dimension:

1. ordinary tower-aware tabular learning;
2. exploit/explore active-tier control;
3. fiber-conditioned stages;
4. future active-tier control using fiber-conditioned substages.

Therefore, mode names should be compositional.

### Mode Dimensions

Each benchmark mode should have these dimensions:

```text
environment_coupling
schema_mode
schema_id
controller_regime
training_surface
learner_id
diagnostic_profile
timing_profile
```

#### `environment_coupling`

Allowed first values:

```text
direct_env
tower_runtime
```

Meanings:

- `direct_env`: no tower runtime in the decision path.
- `tower_runtime`: `state_collapser` runtime participates online.

#### `schema_mode`

Allowed first values:

```text
none
empty
nonempty
diagnostic
```

Meanings:

- `none`: not applicable, usually direct-env mode.
- `empty`: tower machinery runs with empty/no-contraction schema.
- `nonempty`: tower machinery runs with a contraction schema.
- `diagnostic`: schema exists only for structural probe or debug run.

#### `schema_id`

Examples:

```text
none
empty_v001
upstream_default_plate_support_v001
semantic_counterpoint_motion_v001
bad_random_grouping_v001
```

The schema id must be stable enough to join artifacts.

#### `controller_regime`

Allowed first values:

```text
none
exploit_explore
fiber_stage
future_active_tier_fiber_control
```

Meanings:

- `none`: ordinary action selection, no active-tier controller.
- `exploit_explore`: upstream active-tier controller with LIFT/DESCEND.
- `fiber_stage`: stage-local fiber-conditioned training.
- `future_active_tier_fiber_control`: reserved name for a future combined
  regime.

#### `training_surface`

Allowed first values:

```text
direct_tabular
tower_position_tabular
fiber_conditioned_stage
exploit_explore_tier_learner
future_neural
```

#### `learner_id`

Examples:

```text
upstream_tabular_q_v001
direct_tabular_q_v001
plate_support_tier_learner_v001
future_dqn_v001
```

#### `diagnostic_profile`

Allowed first values:

```text
minimal
standard
structural_periodic
readout_expensive
exact_tiny
```

#### `timing_profile`

Allowed first values:

```text
online_only
online_plus_posthoc
diagnostic_inclusive
```

Meanings:

- `online_only`: timed interval includes only required online work.
- `online_plus_posthoc`: online work and post-hoc work are separately timed.
- `diagnostic_inclusive`: expensive diagnostics are part of the run mode and
  included in reported total.

### Canonical First Mode IDs

The following mode ids should be enough for the first benchmark-system
implementation.

#### `direct_env_tabular`

Contract:

```text
environment_coupling: direct_env
schema_mode: none
controller_regime: none
training_surface: direct_tabular
learner_id: upstream_tabular_q_v001 or local_tabular_q_v001
```

Online costs:

- environment reset/step;
- learner act;
- learner update;
- action-mask handling if environment exposes masks;
- artifact logging.

Excluded costs:

- tower runtime;
- partition update;
- compatibility readout.

Purpose:

This is the ordinary flat RL baseline.

#### `tower_empty_schema_tabular`

Contract:

```text
environment_coupling: tower_runtime
schema_mode: empty
controller_regime: none
training_surface: tower_position_tabular
learner_id: upstream_tabular_q_v001
```

Online costs:

- environment reset/step;
- tower runtime reset/step;
- empty/no-contraction partition maintenance;
- learner act;
- learner update;
- masks and continuation metadata;
- artifact logging.

Excluded costs:

- nonempty schema assignment;
- compatibility readout unless explicitly requested.

Purpose:

This is the no-contraction tower-shell baseline. It is not identical to direct
environment training.

#### `tower_nonempty_schema_tabular`

Contract:

```text
environment_coupling: tower_runtime
schema_mode: nonempty
controller_regime: none
training_surface: tower_position_tabular
learner_id: upstream_tabular_q_v001
```

Online costs:

- environment reset/step;
- tower runtime reset/step;
- partition update;
- schema assignment;
- learner act;
- learner update;
- masks and continuation metadata;
- artifact logging.

Excluded costs:

- compatibility readout unless learner actually consumes it online.

Purpose:

This is the first full tower tabular comparison condition.

#### `tower_exploit_explore`

Contract:

```text
environment_coupling: tower_runtime
schema_mode: nonempty
controller_regime: exploit_explore
training_surface: exploit_explore_tier_learner
learner_id: upstream_or_env_tier_learner
```

Online costs:

- environment reset/step when controller executes environment actions;
- tower runtime reset/step;
- active-tier controller decision;
- lift/descend/train/explore/exploit events;
- tier learner observe/train;
- lift/resolve executor;
- control metrics;
- artifact logging.

Purpose:

This is the current explicit active-tier up/down control path.

Important:

This mode is not interchangeable with `tower_nonempty_schema_tabular`.

#### `tower_fiber_conditioned_stage`

Contract:

```text
environment_coupling: tower_runtime
schema_mode: nonempty
controller_regime: fiber_stage
training_surface: fiber_conditioned_stage
learner_id: upstream_tabular_q_v001 or stage_specific_learner
```

Online costs:

- environment reset/step;
- tower runtime reset/step;
- path fiber action-mask construction;
- lift-candidate resolution;
- learner act/update;
- fiber departure diagnostics;
- artifact logging.

Purpose:

This measures the stage-local fiber-conditioned substrate. It should not be
presented as the same thing as full active-tier control.

#### `tower_control_with_fiber_conditioned_substages`

Status:

Reserved for future design.

Purpose:

This would be the likely long-term "correct tower training" regime, where
active-tier control uses fiber-conditioned stages as substages or refinement
surfaces.

This should not be implemented by accident.

## Turn Question 2: Canonical Mode Names

The proposed names are:

```text
direct_env_tabular
tower_empty_schema_tabular
tower_nonempty_schema_tabular
tower_exploit_explore
tower_fiber_conditioned_stage
tower_control_with_fiber_conditioned_substages
```

Are these acceptable as first artifact-facing mode ids?

### PO Answer Slot

```text
I like these. They are acceptable.
```

### Codex Follow-Up Slot

```text
Accepted. These become the first artifact-facing mode ids.

The implementation should put them in a mode registry rather than scattering
string literals through runner code. The registry should validate that each mode
has an explicit environment coupling, schema mode, controller regime, training
surface, learner id, diagnostic profile, timing profile, and online cost policy.
```

## Artifact Root Contract

The artifact system should be stable before serious runs.

Recommended root:

```text
artifacts/
```

Recommended first layout:

```text
artifacts/
  README.md
  index.jsonl
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

This layout separates:

- run-family metadata;
- per-run metadata;
- event tables;
- summaries;
- external artifact references.

### Why Not Put Everything In One File?

Because benchmark artifacts need different access patterns.

- Manifests are nested JSON.
- Episodes are tabular.
- Step events may become large.
- Structural diagnostics may be sparse and nested.
- Summaries should be easy to scan.
- External artifact references need checksums and locations.

One giant JSON blob will become annoying immediately.

### Artifact Schema Version

Every artifact family should include:

```text
artifact_schema_version: "bbb.v001"
```

The version should change when fields are renamed, removed, or semantically
changed.

Additive nullable fields may not require a major version change, but should be
recorded in a changelog once artifacts exist.

## Turn Question 3: Artifact Root Tracking

Should `artifacts/` exist in git with a README, schema files, and tiny smoke
artifacts, while larger run outputs are ignored unless intentionally added?

Recommendation:

Yes. Track:

- `artifacts/README.md`;
- schema files;
- tiny smoke artifacts;
- curated summaries.

Ignore:

- large raw event dumps;
- model checkpoints;
- large tensors;
- large generated corpora.

### PO Answer Slot

```text
Correct.
```

### Codex Follow-Up Slot

```text
Accepted. `artifacts/` should exist in git with README/schema/tiny smoke
material, while large outputs should be ignored or externally referenced unless
intentionally curated.

The first implementation should include an `artifacts/README.md`, an artifact
schema file, and a `.gitignore` policy that prevents accidental large-output
commits.
```

## Manifest Contracts

Manifest files are the backbone of reproducibility.

### `family_manifest.json`

One per run family.

Required fields:

```text
artifact_schema_version
run_family_id
created_at
created_by
purpose
status
benchmark_repo_commit
benchmark_repo_dirty
state_collapser_commit
state_collapser_dirty
state_collapser_path
python_version
platform
matrix_manifest_path
environment_family_manifest_path
dependency_manifest_path
run_index_path
notes
```

Purpose:

Describe why this run family exists and bind it to code state.

### `matrix_manifest.json`

One per run family.

Required fields:

```text
artifact_schema_version
run_family_id
matrix_id
environment_family_ids
environment_instance_ids
scale_tiers
mode_ids
schema_ids
learner_ids
controller_ids
budget_ids
seed_bundle_ids
diagnostic_profiles
timing_profiles
matrix_notes
```

Purpose:

Define the intended Cartesian product or explicit run list.

It should also say whether the matrix is:

```text
cartesian
explicit
mixed
```

### `environment_family_manifest.json`

One per environment family or per run family if the run contains several
families.

Required fields:

```text
artifact_schema_version
environment_family_id
family_name
family_version
geometry_summary
hidden_constraint_geometry
state_space_description
action_space_description
reward_description
termination_description
truncation_description
validity_rule_summary
quotient_hypothesis
reward_locality_hypothesis
schema_leakage_risks
scale_tiers
instance_ids
source_location
notes
```

Purpose:

Prevent environment runs from becoming uninterpretable.

### `dependency_manifest.json`

Required fields:

```text
artifact_schema_version
benchmark_repo_commit
benchmark_repo_dirty
state_collapser_source_kind
state_collapser_path
state_collapser_commit
state_collapser_branch
state_collapser_dirty
state_collapser_ahead_behind
python_executable
python_version
platform
installed_packages
lockfile_hash
command_environment
```

`state_collapser_source_kind` allowed values:

```text
local_editable
local_wheel
git_commit
git_tag
pypi
unknown
```

### `run_manifest.json`

One per run.

Required fields:

```text
artifact_schema_version
run_family_id
run_id
run_index
status
started_at
ended_at
environment_family_id
environment_instance_id
scale_tier
mode_id
schema_id
learner_id
controller_id
budget_id
seed_bundle_id
diagnostic_profile
timing_profile
command
working_directory
online_cost_policy
readout_policy
morphism_policy
output_files
warnings_path
external_artifacts_path
```

### `seed_bundle.json`

Required fields:

```text
artifact_schema_version
seed_bundle_id
replicate_index
environment_seed
schema_seed
learner_seed
controller_seed
diagnostic_sampling_seed
artifact_sampling_seed
notes
```

### `mode_manifest.json`

Required fields:

```text
artifact_schema_version
mode_id
environment_coupling
schema_mode
schema_id
controller_regime
training_surface
learner_id
diagnostic_profile
timing_profile
online_costs_included
online_costs_excluded
learner_observation_contract
controller_event_contract
readout_policy
morphism_policy
notes
```

### `external_artifacts.json`

Required fields:

```text
artifact_schema_version
run_id
artifacts
```

Each artifact entry:

```text
artifact_id
kind
local_path
external_uri
size_bytes
sha256
required_for_reproduction
required_for_report
notes
```

Allowed first `kind` values:

```text
checkpoint
tensor_dump
large_event_table
plot_bundle
html_report
raw_rollout_dump
generated_environment_corpus
other
```

## Event Table Contracts

This section defines first-pass tables. These are blueprint-level contracts,
not final schemas.

### Type Conventions

Use these value conventions unless a later implementation plan changes them:

- ids are strings;
- indexes are zero-based integers;
- durations are seconds as floats;
- timestamps are ISO-8601 strings;
- booleans are lowercase JSON booleans in JSON and `true`/`false` strings in
  CSV if necessary;
- nullable fields are empty in CSV and `null` in JSON;
- object payloads should be avoided in CSV;
- large nested values should go in JSONL diagnostics, not step rows.

### `run_index.jsonl`

One row per run.

Fields:

```text
artifact_schema_version
run_family_id
run_id
run_index
status
environment_instance_id
scale_tier
mode_id
schema_id
learner_id
controller_id
budget_id
seed_bundle_id
run_manifest_path
summary_path
started_at
ended_at
```

### `episodes.csv`

One row per episode.

Fields:

```text
run_id
episode_index
seed_bundle_id
environment_seed
budget_id
mode_id
schema_id
controller_id
steps
controller_events
learner_updates
return
success
terminated
truncated
final_observation_key
max_tower_depth
final_tower_depth
max_discovered_states
max_discovered_edges
wall_clock_seconds
env_step_seconds
tower_update_seconds
learner_act_seconds
learner_update_seconds
controller_seconds
artifact_logging_seconds
posthoc_diagnostic_seconds
warnings_count
```

Important:

For direct environment mode, tower fields should be null or zero by contract,
not silently omitted.

### `step_events.csv`

One row per primitive environment step or environment-facing step.

Fields:

```text
run_id
episode_index
step_index
global_step_index
mode_id
schema_id
controller_id
seed_bundle_id
environment_action
reward
cumulative_reward
terminated
truncated
observation_key
state_key
next_state_key
legal_action_count
action_count
action_mask_density
bootstrap_allowed
bootstrap_reason
tower_depth
active_tier
control_action
discovered_state_count
discovered_edge_count
readout_requested
morphism_requested
elapsed_env_step
elapsed_tower_update
elapsed_learner_act
elapsed_learner_update
elapsed_controller
elapsed_artifact_logging
```

This table should remain compact.

Do not put full observations, full state objects, full action masks, or full
fiber members here.

### `control_events.csv`

One row per active-tier controller event.

Fields:

```text
run_id
episode_index
control_event_index
global_control_event_index
mode_id
controller_id
active_tier_before
active_tier_after
tier_state_key_before
tier_state_key_after
control_action
exploration_pressure
visit_count
td_error_ema
success_rate
reward_residual_ema
training_due
lift_resolve_success
abstract_action_duration
context_version
context_invalidated
elapsed_controller_decision
elapsed_lift_resolve
elapsed_tier_learner
```

This table is required for `tower_exploit_explore` and future active-tier
regimes.

It may be empty for ordinary tabular modes.

### `timing_segments.csv`

One row per named timing segment.

Fields:

```text
run_id
episode_index
step_index
control_event_index
segment_name
segment_kind
elapsed_seconds
included_in_online_total
included_in_diagnostic_total
notes
```

Allowed first `segment_name` values:

```text
env_reset
env_step
tower_reset
tower_update
learner_act
learner_update
controller_decide
lift_resolve
fiber_mask
fiber_lift_candidates
compatibility_readout
morphism_construction
artifact_write
posthoc_structural_diagnostics
summary_statistics
```

### `structural_diagnostics.jsonl`

One row per structural diagnostic checkpoint.

Fields:

```text
artifact_schema_version
run_id
episode_index
step_index
checkpoint_index
diagnostic_profile
cadence
exact
sampled
sample_size
uses_compatibility_readout
uses_morphism
tier_index
state_cell_count
action_cell_count
compression_ratio
scheduled_assignment_count
unscheduled_assignment_count
mean_fiber_size
max_fiber_size
fiber_size_histogram
fiber_entropy_estimate
reward_variance_estimate
pvol_estimate
policy_effective_pvol_estimate
coarse_policy_value_error
fine_refinement_residual
diagnostic_payload_path
elapsed_seconds
```

This table may be sparse. It should not be forced to have one row per step.

### `warnings.jsonl`

One row per warning, anomaly, or nonfatal issue.

Fields:

```text
artifact_schema_version
run_id
episode_index
step_index
warning_code
severity
message
source
payload
```

Allowed first `severity` values:

```text
info
warning
error
critical
```

### `summary.json`

One per run family and optionally one per run.

Required top-level fields:

```text
artifact_schema_version
run_family_id
summary_scope
generated_at
input_artifacts
grouping_keys
metrics
warnings
notes
```

`summary_scope` allowed first values:

```text
run
mode
environment_instance
run_family
```

### `bootstrap_intervals.csv`

Fields:

```text
run_family_id
environment_instance_id
mode_id
schema_id
metric_name
seed_count
mean
std
ci_low
ci_high
bootstrap_low
bootstrap_high
bootstrap_method
bootstrap_resamples
```

## Turn Question 4: Large Table Storage

For first implementation, should large step/control tables start as CSV, or
should we use a columnar/table format early?

Options:

1. CSV first, simplest and reviewable.
2. Parquet first, better for large data and pandas analysis.
3. SQLite or DuckDB first, better for queryable artifacts.

Recommendation:

CSV first for smoke and early blueprint implementation, with a clean writer
interface so Parquet or DuckDB can be added later.

### PO Answer Slot

```text
Yes. I completely agree.
```

### Codex Follow-Up Slot

```text
Accepted. CSV first, writer interface designed so Parquet/DuckDB can be added
later.

This keeps early artifacts inspectable in plain text while still avoiding a
hard dependency on CSV forever. The implementation should isolate table writing
behind artifact writer functions rather than making runners call `open(...).write`
directly.
```

## Metric Channel Contract

Metrics must be classified before implementation.

### Channel A: Online Hot-Path Counters

Collected during every run.

Rules:

- cheap;
- compact;
- no compatibility readout by default;
- stable ids only where possible;
- written incrementally or buffered safely;
- included in online timing if writing happens online.

Examples:

- step count;
- reward;
- success;
- tower depth;
- discovered states;
- discovered edges;
- active tier;
- control action;
- mask density;
- bootstrap reason;
- timing segments;
- readout requested flag;
- morphism requested flag.

### Channel B: Online Control Events

Collected for active-tier regimes.

Rules:

- no full object dumps;
- must capture tier movement;
- must capture controller mode;
- must capture enough signal state to diagnose whether control is hierarchical.

Examples:

- LIFT;
- DESCEND;
- TRAIN;
- EXPLORE;
- EXPLOIT_EXECUTE;
- exploration pressure;
- reward residual;
- lift/resolve success.

### Channel C: Periodic Structural Diagnostics

Collected periodically, sampled, or post-hoc.

Rules:

- must declare cadence;
- must declare exact versus sampled;
- must declare whether readouts were used;
- must declare elapsed diagnostic time;
- should not be silently included in online cost unless timing profile says so.

Examples:

- compression ratios;
- state/action cell counts;
- fiber size;
- fiber entropy;
- reward variance inside fibers;
- `PVol` estimates.

### Channel D: Expensive Debug Artifacts

Collected only when requested.

Rules:

- never default;
- always flagged;
- may be external;
- must have checksum if persisted;
- must say whether it was created during or after the online run.

Examples:

- full compatibility tier views;
- full fiber dumps;
- graph exports;
- dense path enumerations;
- morphism domain dumps.

### Channel E: Statistical Summaries

Computed after run completion.

Rules:

- never overwrite raw artifacts;
- include input artifact paths;
- include seed count;
- include grouping keys;
- include mean/std, confidence intervals, and bootstrap intervals when enough
  replicates exist.

## Readout Discipline Contract

This repo must not accidentally erase upstream runtime improvements.

### Default Policy

Default benchmark runs should not call:

```text
TowerRuntime.compatibility_quotient_tiers()
PartitionTower.to_quotient_tier_views()
```

unless the mode contract explicitly requires compatibility readouts online.

### Required Flags

Every run must record:

```text
readout_requested
morphism_requested
uses_compatibility_readout
uses_morphism
```

Where applicable, event rows should distinguish:

```text
readout_requested_online
readout_requested_posthoc
```

### Readout Discipline Smoke Test

The first implementation should include a smoke test that proves:

1. default mode does not call compatibility readout;
2. diagnostic mode does call compatibility readout;
3. both modes record flags correctly;
4. timing segments separate readout cost from normal tower update cost.

### Monkeypatching Rule

Monkeypatching upstream is generally forbidden.

Exception:

For diagnostic tests, it is acceptable to monkeypatch a readout method to count
calls, as long as the artifact/run is marked diagnostic and no scientific
benchmark result is claimed from that patched run.

## Turn Question 5: Readout Call-Counting

Should implementation use monkeypatch-based tests to prove default runners do
not call compatibility readouts?

Recommendation:

Yes, for tests only. Do not use monkeypatched runs for scientific artifacts.

### PO Answer Slot

```text
Yes. For tests only.
```

### Codex Follow-Up Slot

```text
Accepted. Readout call-counting monkeypatches are allowed for tests only.

The implementation should make this boundary explicit: monkeypatched tests can
prove default runner paths avoid compatibility readouts, but scientific run
artifacts should never depend on monkeypatched upstream behavior.
```

## Timing Contract

Timing must separate algorithmic cost from reporting cost.

### Clock

Use a monotonic high-resolution clock for elapsed durations.

In Python this likely means:

```text
time.perf_counter()
```

### Timing Segments

Every runner should support named timing segments:

- environment reset;
- environment step;
- tower reset;
- tower update;
- controller decision;
- lift/resolve;
- fiber mask construction;
- learner action selection;
- learner update;
- artifact logging;
- compatibility readout;
- post-hoc diagnostics;
- summary generation.

### Online Cost

Online cost includes only work required by the evaluated algorithm while it is
running.

Examples:

- if the learner needs an action mask online, mask construction counts;
- if the controller needs lift candidates online, lift-candidate resolution
  counts;
- if compatibility readout is only for a report, it does not count as online
  learner cost;
- if a benchmark mode genuinely uses compatibility readout to choose action,
  it counts.

### Artifact Logging Cost

Artifact writing can be nontrivial.

The benchmark should time:

```text
artifact_logging_seconds
```

This lets us later decide whether to report:

- algorithm-only online cost;
- algorithm-plus-artifact online cost.

Both may be useful.

### Warmup

The first implementation does not need elaborate warmup logic, but timing
artifacts should record whether warmup occurred.

Fields:

```text
warmup_enabled
warmup_steps
warmup_episodes
warmup_included_in_summary
```

## Turn Question 6: Artifact Logging In Online Total

Should primary wall-clock comparisons include artifact logging time?

Options:

1. Include artifact logging in primary wall-clock, because it is part of the
   benchmark run.
2. Exclude artifact logging from primary algorithm wall-clock, but report it
   separately.
3. Report both as first-class metrics.

Recommendation:

Report both. The algorithmic comparison should not be distorted by a verbose
logger, but artifact cost is real and should be visible.

### PO Answer Slot

```text
Report both.
```

### Codex Follow-Up Slot

```text
Accepted. Report both.

The implementation should expose at least two wall-clock fields:

- algorithm online time, excluding artifact writing;
- benchmark online time, including artifact writing.

This lets us compare the algorithm honestly while still keeping artifact cost
visible. If verbose logging becomes expensive, the artifacts will show that
rather than hiding it.
```

## Seed Bundle Contract

Seeds are reproducibility inputs, not sample counts.

### Required Seed Fields

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

### Replicate Index

The replicate index is a human-friendly ordinal.

The seed bundle is the actual reproducibility contract.

### Seed Count Tiers

First working convention:

```text
3 to 5 replicates: smoke and harness debugging
10 replicates: early exploratory evidence
30 or more replicates: public-facing claims
adaptive: allowed when variance is high
```

These are not hard statistical laws. They are evidence discipline.

## Statistics Contract

The first statistical layer should produce:

- count;
- mean;
- standard deviation;
- confidence interval;
- bootstrap interval.

### Metrics To Summarize First

Candidate first summary metrics:

- total return;
- success rate;
- steps to success;
- episodes to threshold;
- final tower depth;
- max tower depth;
- discovered state count;
- discovered edge count;
- wall-clock seconds;
- env step seconds;
- tower update seconds;
- learner seconds;
- controller seconds;
- readout seconds;
- artifact logging seconds.

### Confidence Intervals

The blueprint does not yet choose exact confidence interval methods.

Reasonable first implementation:

- normal approximation for simple mean summaries;
- Wilson interval for success rate if needed;
- bootstrap percentile intervals for non-normal distributions.

### Bootstrap Intervals

First implementation can use simple nonparametric bootstrap over seed-level
replicates.

Important:

Do not bootstrap over step rows as if they are independent seeds.

The replicate is the unit of uncertainty for multi-seed claims.

## Turn Question 7: Statistical Method Defaults

Should first implementation use simple percentile bootstrap over seed-level
replicates, with more elaborate statistics deferred?

Recommendation:

Yes.

### PO Answer Slot

```text
Agreed.
```

### Codex Follow-Up Slot

```text
Accepted. First implementation should use simple percentile bootstrap over
seed-level replicates, with fancier statistics deferred.

Important implementation guardrail: the bootstrap unit is the replicate/seed
bundle, not individual step rows. Step rows within a run are correlated; treating
them as independent samples would inflate confidence.
```

## Environment Research Contract

Serious environments are not just code. Each serious family needs a design
spec.

### Environment Family Spec Template

Each family should have a document with:

```text
environment_family_id
short_name
geometry_summary
hidden_constraint_geometry
state_definition
action_definition
validity_rule
transition_rule
reward_rule
termination_rule
truncation_rule
why_flat_search_is_wasteful
quotientable_regularities
reward_locality_hypothesis
schema_candidates
schema_leakage_risks
negative_control_variant
scale_ladder
exact_diagnostic_feasibility
expected_failure_modes
artifact_fields_needed
```

### Scale Ladder Template

Each family should define:

```text
tiny:
  purpose:
  expected_states:
  expected_edges:
  exact_metrics:

small:
  purpose:
  expected_states:
  expected_edges:
  exact_metrics:

medium:
  purpose:
  expected_states:
  expected_edges:
  sampled_metrics:

large:
  purpose:
  expected_states:
  expected_edges:
  sampled_metrics:

stress:
  purpose:
  expected_states:
  expected_edges:
  sampled_metrics:
```

### Environment Acceptance Gates

Before an environment enters the serious benchmark matrix, it should satisfy:

1. written geometry spec;
2. deterministic tiny instance;
3. direct-env smoke run;
4. tower empty-schema smoke run;
5. tower nonempty-schema smoke run;
6. structural diagnostics on tiny/small instance;
7. artifact output validation;
8. no obvious schema leakage;
9. clear reason it stresses `state_collapser`.

### Upstream Smoke Environments

Use upstream examples for:

- import smoke;
- runner shape;
- artifact schema validation;
- readout discipline;
- empty vs nonempty schema plumbing;
- exploit/explore capture on `plate_support_env`;
- fiber-conditioned stage capture where available.

Do not use upstream smoke environments as the final serious benchmark claim.

## Turn Question 8: First Serious Environment Track

Which environment research direction should receive the first serious family
blueprint?

Options:

1. counterpoint-like symbolic constrained sequence;
2. dual-arm/shared-object coordination;
3. cable/support coupling;
4. loop-closure geometry;
5. singularity/bottleneck geometry;
6. a new family not named yet.

Recommendation:

Either counterpoint-like symbolic or dual-arm/shared-object coordination,
because the public-maturity bar needs at least one symbolic and one
robotics/control-flavored environment eventually.

### PO Answer Slot

```text
The answer is really that we want both these as first two. ...But maybe counterpoint-like symbolic first, since it also has canonical projections, and then  or dual-arm/shared-object coordination second.
```

### Codex Follow-Up Slot

```text
Accepted with ordering: first serious environment-family blueprint should be
counterpoint-like symbolic constrained sequence; second should be
dual-arm/shared-object coordination.

The canonical projections point is a strong reason to start symbolic. It gives
us a better chance of defining exact tiny-instance structure, projection maps,
path/fiber diagnostics, and maybe early `PVol` estimators before facing the
messier robotics/control family. The dual-arm track should remain explicitly
second, not forgotten.
```

## Runner Architecture Blueprint

This section sketches the importable package architecture.

If the import package is `big_boy_benchmarking`, recommended layout:

```text
src/big_boy_benchmarking/
  __init__.py
  artifacts/
    __init__.py
    paths.py
    manifests.py
    writers.py
    schemas.py
  modes/
    __init__.py
    contracts.py
    registry.py
  metrics/
    __init__.py
    events.py
    timing.py
    structural.py
    summaries.py
    bootstrap.py
  seeds/
    __init__.py
    bundles.py
  runners/
    __init__.py
    base.py
    direct_env.py
    tower_tabular.py
    exploit_explore.py
    fiber_stage.py
  upstream/
    __init__.py
    state_collapser.py
    smoke_envs.py
    readout_guards.py
  environments/
    __init__.py
    specs.py
    registry.py
  cli/
    __init__.py
    main.py
```

### `artifacts`

Responsibilities:

- create run-family directories;
- write JSON manifests;
- write CSV/JSONL event tables;
- write external artifact references;
- validate required files exist;
- keep schema version attached to outputs.

### `modes`

Responsibilities:

- define `BenchmarkModeContract`;
- validate mode ids;
- encode online cost policy;
- encode readout policy;
- encode controller/training surface contract.

### `metrics`

Responsibilities:

- define event dataclasses or typed dicts;
- define timing segment helpers;
- define structural diagnostic rows;
- define summary and bootstrap computation.

### `seeds`

Responsibilities:

- define seed bundle shape;
- generate deterministic seed bundles;
- serialize seed bundles;
- prevent accidental reuse ambiguity.

### `runners`

Responsibilities:

- run one mode on one environment instance;
- emit events through artifact writers;
- enforce timing policy;
- preserve mode contracts.

### `upstream`

Responsibilities:

- locate/import `state_collapser`;
- record upstream git state;
- provide wrappers for upstream smoke envs;
- guard readout discipline in tests.

### `environments`

Responsibilities:

- hold benchmark environment specs;
- register local benchmark environments;
- distinguish smoke upstream environments from serious local families.

### `cli`

Responsibilities:

- expose simple commands;
- avoid putting business logic directly in shell scripts.

## CLI Shape

The first CLI does not need to be fancy.

Candidate commands:

```text
bbb init-artifacts
bbb run-smoke
bbb run-matrix
bbb summarize
bbb inspect-run
bbb validate-artifacts
```

If using `python -m` first:

```bash
uv run python -m big_boy_benchmarking.cli run-smoke \
  --matrix benchmarks/matrices/upstream_smoke_v001.json \
  --artifact-root artifacts/runs
```

First smoke command should probably run:

- one direct-env mode where easy;
- one tower empty-schema mode;
- one tower nonempty-schema mode;
- readout-disabled default;
- readout-enabled diagnostic variant;
- tiny seed count.

## Turn Question 9: CLI Naming

Should the executable command eventually be `bbb`, or should we stick to
`python -m big_boy_benchmarking...` until the package stabilizes?

Recommendation:

Use `python -m` first. Add `bbb` once the command surface stops changing every
hour.

### PO Answer Slot

```text
Use `python -m` first.
```

### Codex Follow-Up Slot

```text
Accepted. Use `python -m big_boy_benchmarking...` first.

The first implementation should avoid installing a console script until the CLI
surface stabilizes. A later `bbb` command can become a convenience wrapper once
the command names stop moving.
```

## Configuration Contract

Benchmark config should be explicit and machine-readable.

Recommended config locations:

```text
benchmarks/
  matrices/
  modes/
  environments/
  schemas/
  budgets/
  seed_bundles/
```

### Matrix Config

Example shape:

```json
{
  "matrix_id": "upstream_smoke_v001",
  "artifact_schema_version": "bbb.v001",
  "purpose": "Validate artifact and readout discipline on upstream smoke envs.",
  "runs": [
    {
      "environment_instance_id": "upstream_plate_support_smoke",
      "mode_id": "tower_empty_schema_tabular",
      "schema_id": "empty_v001",
      "learner_id": "upstream_tabular_q_v001",
      "budget_id": "smoke_episodes_3_steps_20",
      "seed_bundle_id": "smoke_replicate_000"
    }
  ]
}
```

### Budget Config

Example shape:

```json
{
  "budget_id": "smoke_episodes_3_steps_20",
  "episodes": 3,
  "max_environment_steps_per_episode": 20,
  "max_controller_events_per_episode": null,
  "max_learner_updates": null,
  "wall_clock_limit_seconds": null
}
```

### Diagnostic Profile Config

Example shape:

```json
{
  "diagnostic_profile": "structural_periodic",
  "structural_checkpoint_cadence_steps": 10,
  "exact_fiber_metrics": false,
  "sampled_fiber_metrics": true,
  "fiber_sample_size": 64,
  "compatibility_readout": "posthoc"
}
```

## Test Contract

The first implementation should have tests before serious runs.

### Artifact Tests

Required:

- manifest writer creates valid JSON;
- required manifest fields are present;
- run directory layout is stable;
- CSV headers match contract;
- JSONL diagnostics can be appended and read back.

### Mode Contract Tests

Required:

- known mode ids validate;
- direct env mode excludes tower costs;
- tower empty-schema mode includes tower runtime;
- nonempty schema mode requires schema id;
- diagnostic profiles mark readout behavior.

### Readout Discipline Tests

Required:

- default tower smoke runner does not request compatibility readout;
- readout diagnostic runner does request it;
- flags are recorded;
- timing segment exists for readout diagnostic.

### Seed Tests

Required:

- seed bundle serializes;
- replicate index is stable;
- generated seed bundles are deterministic;
- separate seed dimensions can be recorded.

### Summary Tests

Required:

- summary can group by mode/environment;
- mean/std computed over replicates;
- bootstrap uses seed-level replicates, not step rows.

## Turn Question 10: Test-First Discipline

Should the first implementation gameplan explicitly start with artifact/mode
contract tests before runner code?

Recommendation:

Yes. The whole point is to avoid a benchmark runner whose outputs shift under
our feet.

### PO Answer Slot

```text
Yes absolutely. ...Can you tell me a little bit more about contracts in CS/engineering?
```

### Codex Follow-Up Slot

```text
Accepted, and this is worth unpacking.

In CS/engineering, a contract is an explicit promise between pieces of a system.
It says what a component expects, what it guarantees, and what must stay true
for other components to trust it.

Common contract forms:

- preconditions: what must be true before a function or runner is called;
- postconditions: what must be true after it finishes;
- invariants: what must remain true across a whole process;
- interface contracts: what fields, methods, files, or event shapes exist;
- schema contracts: what columns and types an artifact has;
- behavioral contracts: what a mode is allowed to do online.

For this benchmark repo, examples are concrete:

- `direct_env_tabular` must not update a tower runtime;
- `tower_empty_schema_tabular` must run tower machinery but not nonempty
  contraction;
- default hot-path runs must not call compatibility readouts;
- `episodes.csv` must have the declared columns;
- a run manifest must record upstream commit and dirty status;
- bootstrap summaries must aggregate over seed-level replicates, not step rows.

Contract tests are tests that enforce those promises before we trust a runner.
They are not about making the code fancy. They prevent a future result from
being meaningless because a file changed shape, a mode silently changed
meaning, or a metric accidentally pulled an expensive readout into the hot path.

So yes: the first implementation gameplan should start with artifact/mode
contract tests before runner code.
```

## First Implementation Slice

This is not a full gameplan, but this blueprint should point toward the first
slice.

Recommended first implementation scope:

```text
Artifact skeleton + mode contracts + upstream smoke readout-discipline run.
```

Included:

1. create importable package skeleton;
2. define artifact schema version;
3. define mode contract types;
4. define seed bundle type;
5. write manifest writers;
6. write CSV/JSONL writers;
7. implement simple timing segments;
8. create upstream smoke matrix config;
9. run one tiny upstream smoke mode;
10. prove readout-disabled default does not request compatibility readout;
11. prove readout-enabled diagnostic records the readout cost;
12. write summary.json for the smoke run.

Excluded:

1. serious new environment family;
2. exact `PVol`;
3. neural learners;
4. final exploit/explore/fiber unification;
5. large-scale benchmark runs;
6. external artifact storage integration.

### Why This Slice

It exercises the measurement machine without pretending to answer the research
claim.

It creates the thing every later serious run needs:

- stable dirs;
- stable ids;
- stable mode names;
- stable manifests;
- stable timing;
- readout discipline.

## Blueprint Acceptance Criteria

This blueprint is ready to become an implementation gameplan when the Project
Owner accepts or edits these decisions:

1. import package name;
2. canonical first mode ids;
3. artifact root tracking policy;
4. large table storage first choice;
5. monkeypatch-based readout call-counting tests;
6. whether artifact logging is included in primary wall-clock or reported
   separately;
7. default statistical method;
8. first serious environment track;
9. CLI naming posture;
10. test-first implementation discipline.

Not every answer must be perfect. But the implementation gameplan should know
which way to lean.

## PO Decision Summary After First Blueprint Reply

The Project Owner filled the first blueprint turn questions. Resulting
decisions:

1. Import package name: `big_boy_benchmarking`.
2. Canonical first mode ids: accepted.
3. Artifact root tracking: accepted.
4. Large table storage: CSV first, with future-proof writer interface.
5. Readout call-counting: monkeypatch tests are allowed for tests only.
6. Artifact logging time: report both algorithm online time and benchmark
   online time.
7. Statistics: simple percentile bootstrap over seed-level replicates first.
8. First serious environment order: counterpoint-like symbolic first,
   dual-arm/shared-object coordination second.
9. CLI naming: use `python -m` first.
10. Test-first discipline: accepted, with contracts explained as engineering
    promises enforced by tests.

## Implementation Gameplan Readiness

This blueprint is now ready to become an implementation gameplan for the first
slice:

```text
artifact skeleton + mode registry + contract tests + readout-discipline upstream smoke
```

The implementation gameplan should not yet attempt the first serious
counterpoint-like environment family. That should be the next design blueprint
after the artifact/mode measurement machine exists.

## Human-Facing Documentation Layer

The blueprint above defines machine-readable artifacts. That is necessary, but
not sufficient.

This repo also needs a human-facing documentation layer where a reader can
quickly understand:

- what environments exist;
- what geometry they test;
- what experiments were run;
- what the results mean at a glance;
- where the raw artifacts live;
- what caveats matter.

Machine artifacts are for reproducibility and analysis. Human docs are for
orientation, review, and scientific communication.

### Recommended Docs Layout

Add a docs layer shaped like:

```text
docs/
  environments/
    counterpoint_symbolic_v001.md
    dual_arm_shared_object_v001.md
  experiments/
    2026_05_upstream_smoke_readout_discipline.md
    2026_06_counterpoint_tiny_structural_probe.md
  results/
    2026_05_upstream_smoke_summary.md
    2026_06_counterpoint_tiny_summary.md
  methods/
    artifact_contract.md
    benchmark_modes.md
    metric_channels.md
    seed_bundles.md
    statistics.md
```

The exact filenames can change, but the conceptual split should remain.

### `docs/environments/`

Purpose:

Human-readable descriptions of benchmark environment families and instances.

Each serious environment family should have a Markdown document describing:

- environment family id;
- human name;
- hidden constraint geometry;
- state definition;
- action definition;
- transition rule;
- reward rule;
- termination/truncation;
- why flat search is wasteful;
- quotient/projection hypothesis;
- scale ladder;
- schema candidates;
- schema leakage risks;
- negative-control variants;
- artifact fields specific to this family.

This is where a reader should go to understand why an environment belongs in
the benchmark suite.

### `docs/experiments/`

Purpose:

Human-readable descriptions of run families before or during execution.

Each experiment doc should explain:

- experiment id;
- run family id;
- purpose;
- hypothesis or question;
- environment instances;
- modes;
- schemas;
- learners/controllers;
- budgets;
- seed plan;
- diagnostic profile;
- artifact root;
- known caveats;
- what would make the run interesting.

This is where a reader should go to understand what a run family is trying to
learn.

### `docs/results/`

Purpose:

Human-readable summaries generated from or grounded in machine artifacts.

Each result doc should include:

- result id;
- run family id;
- artifact paths;
- upstream `state_collapser` commit;
- benchmark repo commit;
- short result summary;
- key tables;
- key plots if present;
- important caveats;
- what was not tested;
- links to raw artifacts;
- next questions.

The result doc should not be the source of truth. The artifacts are the source
of truth. The result doc is the readable front door.

### `docs/methods/`

Purpose:

Stable explanations of benchmark methodology.

Initial method docs should include:

- artifact contract;
- benchmark modes;
- metric channels;
- seed bundles;
- timing/readout discipline;
- statistical summaries;
- environment acceptance gates.

These docs should be written for humans who do not want to read the entire
blueprint before understanding the benchmark suite.

### Relationship To Artifacts

Human docs should link to artifacts, not replace them.

Every result doc should name:

```text
run_family_id
artifact_schema_version
artifact_root
summary.json
run_index.jsonl
raw table paths
external artifact manifest if present
```

Every experiment doc should name:

```text
matrix_manifest
environment_family_manifest
mode ids
budget ids
seed bundle ids
```

Every environment doc should name:

```text
environment_family_id
environment_instance_ids
scale tiers
source path or generator path
```

### Generated Versus Handwritten

Some docs should be handwritten:

- environment descriptions;
- methodology docs;
- experiment intent.

Some docs may be generated from artifacts:

- result summaries;
- key tables;
- run status sections.

Recommended first policy:

- handwrite `docs/environments/`, `docs/experiments/`, and `docs/methods/`;
- generate or partially generate `docs/results/` from artifacts;
- allow manual commentary in result docs, but keep raw numbers traceable to
  machine artifacts.

### First Implementation Implication

The first implementation gameplan should include creation of:

```text
docs/environments/
docs/experiments/
docs/results/
docs/methods/
```

with README files explaining each folder's purpose.

The first smoke run should produce or support a human-readable result summary
under:

```text
docs/results/
```

even if the summary is tiny.

## Risk Register

### Risk 1: Artifact Schema Churn

If the schema changes every run, old results become annoying to compare.

Mitigation:

- schema versioning;
- small first contract;
- additive fields where possible;
- validation tests.

### Risk 2: Readout Regression

Benchmark metrics may accidentally reintroduce compatibility readout cost.

Mitigation:

- readout flags;
- readout timing segment;
- call-count tests;
- diagnostic profiles.

### Risk 3: Mode Confusion

Direct env, empty-schema tower, nonempty tower, exploit/explore, and fiber-stage
runs may be collapsed into vague "flat/full" labels.

Mitigation:

- compositional mode contract;
- artifact-facing mode ids;
- mode manifests.

### Risk 4: Environment Leakage

Schemas may encode too much solution structure.

Mitigation:

- environment-family specs;
- schema leakage notes;
- bad/weak schema ablations;
- negative controls.

### Risk 5: Big Artifacts In Git

Large files may bloat the repo.

Mitigation:

- external artifact manifest;
- `.gitignore` policy;
- track only small curated outputs.

### Risk 6: Overbuilding Before First Smoke Run

The artifact system could become too elaborate before anything runs.

Mitigation:

- implement only the first slice;
- keep runners simple;
- defer Parquet/DuckDB/external storage until needed.

### Risk 7: Underbuilding The Metric Contract

A quick runner could produce output that cannot answer later questions.

Mitigation:

- mode contracts first;
- manifests first;
- event schemas first.

## Open Turn Questions Index

1. Package name.
2. Canonical mode names.
3. Artifact root tracking.
4. Large table storage.
5. Readout call-counting tests.
6. Artifact logging in online wall-clock.
7. Statistical method defaults.
8. First serious environment track.
9. CLI naming.
10. Test-first discipline.

## Closing Blueprint Statement

The first implementation should not try to prove `state_collapser` works.

It should prove that `big_boy_benchmarking` can measure honestly.

That means:

- known modes;
- known seeds;
- known upstream commit;
- known artifact schema;
- known online costs;
- known diagnostic costs;
- known readout behavior;
- known limitations.

Once that exists, the repo can begin doing the more interesting work: designing
serious environment families and running benchmark matrices that deserve to be
read by skeptical researchers.
