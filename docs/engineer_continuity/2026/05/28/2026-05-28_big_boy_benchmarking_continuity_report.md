# Big Boy Benchmarking Continuity Report

Created: 2026-05-28

Repository:

```text
<repo-root>
```

Current observed state before this report was added:

```text
branch: main
HEAD: 4dd36f6 counterpoint environment built
origin/main: 4dd36f6 counterpoint environment built
worktree: clean
```

This document is a handoff report for the serious benchmarking repo around
`state_collapser`. It summarizes design lineage, implementation work, current
runnable surfaces, known claim boundaries, and good next moves.

## One-Screen Summary

This repo is now a runnable benchmarking harness for the first serious
`state_collapser` benchmark family.

The implemented benchmark family is:

```text
counterpoint_symbolic_v001
```

The central object is not a music generator. It is a benchmark-owned finite
hidden state/action graph with:

- versioned state, action, legality, reward, label, mask, terminal, and schema
  contracts;
- exact tiny graph/path diagnostics;
- a small fixture with large legal path volume;
- direct masked-random and direct tabular-Q runners;
- `state_collapser` `PartitionTower` adapter/smoke integration;
- schema diagnostics for empty, random balanced, random unbalanced, structured
  motion, projection audit, and bad schema controls;
- machine-readable artifacts and human-facing docs.

The repo can run smoke benchmark commands today. It is not yet making serious
performance claims.

The most important current structural fact:

```text
tiny fixture:
  states: 8
  edges: 16
  exact length-4 legal paths: 32

small fixture:
  states: 108
  edges: 1140
  exact length-8 legal paths: 1,723,548,896
```

That small fixture is already the first "this is why flat search is wasteful"
example: the state graph is not huge, but the legal path set is enormous.

## Prime Directive And Process Context

The repo contains a Prime Directive workflow in:

```text
docs/prime_directive/
```

The important process rules that shaped this work:

- do not implement before explicit Project Owner approval;
- treat approved workplans as law during implementation;
- execute Phase.Stage.Action items in order;
- stop on ambiguity, missing prerequisite infrastructure, surprise, or required
  simplification;
- do not edit upstream `<state-collapser-repo>`;
- do not rewrite workplans while implementing them unless the PO explicitly
  approves an amendment;
- avoid fake completion, especially around tower integration and artifact
  surfaces.

This mattered. The counterpoint workplan initially stopped at its prerequisite
infrastructure gate because shared benchmark machinery was missing. Work then
shifted to designing and implementing shared machinery first. After that merged
back into the counterpoint branch/main, the counterpoint workplan resumed from
the recorded pause point.

## Design Lineage

The design docs that matter most are:

```text
docs/design/first_infrastructure_slice/
docs/design/shared_benchmark_machinery/
docs/design/first_counterpoint_environment/
```

### First Infrastructure Slice

The first design arc established the repo as a serious post-smoke benchmarking
workspace for `state_collapser`, not a library-feature branch.

Key docs:

```text
docs/design/first_infrastructure_slice/01_001_initial_benchmarking_goals_discussion.md
docs/design/first_infrastructure_slice/01_002_state_collapser_read_only_reconnaissance.md
docs/design/first_infrastructure_slice/01_003_benchmark_system_and_artifact_contract_blueprint.md
docs/design/first_infrastructure_slice/01_004_benchmark_system_artifact_contract_implementation_workplan.md
```

Key decisions:

- benchmark artifacts are primary;
- human docs are secondary summaries;
- seed bundles matter more than lone seed integers;
- modes need explicit contracts;
- online timing must be separated from posthoc/readout timing;
- compatibility and morphism readouts must not quietly contaminate hot-path
  timing;
- exact diagnostics are preferred on tiny instances;
- sampled diagnostics must be labelled as sampled.

### Shared Benchmark Machinery

The shared benchmark machinery work created the infrastructure the environment
workplan needed.

Key docs:

```text
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
docs/design/shared_benchmark_machinery/01_002_shared_benchmark_machinery_implementation_workplan.md
docs/design/shared_benchmark_machinery/01_003_shared_benchmark_machinery_implementation_log.md
```

Implemented package areas:

```text
src/big_boy_benchmarking/artifacts/
src/big_boy_benchmarking/modes/
src/big_boy_benchmarking/metrics/
src/big_boy_benchmarking/seeds/
src/big_boy_benchmarking/runners/
src/big_boy_benchmarking/upstream/
src/big_boy_benchmarking/cli/
```

Implemented capabilities:

- artifact schemas and version id `bbb.v001`;
- JSON, JSONL, and CSV writers;
- deterministic artifact path builders;
- family, matrix, dependency, run, mode, and external artifact manifests;
- mode contracts and mode registry;
- event row contracts;
- timing recorder and timing summaries;
- deterministic seed bundles;
- upstream smoke env import/runner support;
- dependency-state capture for `state_collapser`;
- thin CLI entry through `python -m big_boy_benchmarking.cli`.

Current shared CLI top-level commands:

```text
validate-contracts
run-upstream-smoke
summarize-smoke
counterpoint
```

### Counterpoint Environment Design

The counterpoint design arc corrected an early framing error: this is not
primarily "how musically complete should the reward be?" The benchmark center
is a finite hidden graph and reward-labelled path set where contraction
schemata can be evaluated against the `state_collapser`/logHRL hypotheses.

Key docs:

```text
docs/design/first_counterpoint_environment/01_001_counterpoint_environment_design_discussion.md
docs/design/first_counterpoint_environment/01_002_counterpoint_hidden_graph_and_contraction_schema_benchmark_blueprint.md
docs/design/first_counterpoint_environment/01_003_counterpoint_hidden_graph_and_contraction_schema_implementation_workplan.md
docs/design/first_counterpoint_environment/01_004_counterpoint_hidden_graph_and_contraction_schema_implementation_log.md
```

Final central spine:

```text
fixed counterpoint-like hidden graph family
+ swappable contraction schemas
+ exact tiny graph/path diagnostics
+ tower-ready adapter surfaces
+ artifact-first outputs
```

Important decisions:

- all substantive work stays in `big_boy_benchmarking`;
- `big_boy_benchmarking` may later become a submodule of `state_collapser`, but
  not now;
- the family is n-voice by design, even though first fixtures are 3 voice;
- old `rl_counterpoint` is conceptual memory, not an implementation dependency;
- first reward is local/action-local;
- legal masks are shared across comparable modes;
- contraction schemas are the main experimental knob;
- projection audit is posthoc/diagnostic-only until evidence justifies an
  online projection convention.

## Git And Branch History

Important recent commits:

```text
4dd36f6 counterpoint environment built
2e65675 Merge branch 'codex/counterpoint-hidden-graph-schema-benchmark-resume'
cbd3b17 Ignore macOS metadata files
8566d07 Implement shared benchmark machinery slice
d9d6360 artifacts design
3b3ffa4 first environment design and workplan: RL counterpoint
4a6e7a2 first infrastructure slice workplan
7fcc560 benchmarking first blueprint
65e5a80 benchmarking design conversation in-progress
```

Branch path:

- `main` started with basic project skeleton and design docs.
- `codex/shared-benchmark-machinery` carried design work.
- `codex/counterpoint-hidden-graph-schema-benchmark-resume` implemented shared
  benchmark machinery and was merged.
- `codex/counterpoint-hidden-graph-schema-benchmark` resumed the counterpoint
  implementation.
- The counterpoint work is now merged to `main`.

Current `main` is aligned with `origin/main` at `4dd36f6` before this continuity
report was added.

## Current Package Architecture

The source tree now has these primary areas:

```text
src/big_boy_benchmarking/
  artifacts/
  cli/
  environments/
  metrics/
  modes/
  runners/
  seeds/
  upstream/
```

### Artifact Machinery

Location:

```text
src/big_boy_benchmarking/artifacts/
```

Important files:

- `schemas.py`: artifact schema version id;
- `paths.py`: deterministic run-family and run path builders;
- `manifests.py`: dataclass manifest contracts;
- `writers.py`: JSON, JSONL, CSV writers;
- `validators.py`: artifact schema validation.

Artifacts are explicitly rooted. The code should not infer artifact roots from
ambient current working directory.

### Mode Registry

Location:

```text
src/big_boy_benchmarking/modes/
```

The registry currently contains 7 modes. The practical ones today include:

```text
direct_env_masked_random
direct_env_tabular
tower_empty_schema_tabular
tower_nonempty_schema_tabular
```

Reserved modes exist for future exploit/explore and fiber-conditioned work.

Mode contracts record:

- environment coupling;
- schema mode;
- controller regime;
- training surface;
- learner id;
- diagnostic profile;
- timing profile;
- online costs included/excluded;
- readout policy;
- morphism policy;
- runnable/reserved status.

### Metric And Timing Machinery

Location:

```text
src/big_boy_benchmarking/metrics/
```

Implemented event rows:

- `RunIndexRow`;
- `EpisodeRow`;
- `StepEventRow`;
- `ControlEventRow`;
- `TimingSegmentRow`;
- `StructuralDiagnosticRow`;
- `WarningRow`;
- `BootstrapIntervalRow`.

Timing distinguishes:

- algorithm online;
- benchmark online;
- readout;
- morphism;
- posthoc;
- summary.

### Seed Bundles

Location:

```text
src/big_boy_benchmarking/seeds/bundles.py
```

Seed bundles include separate seed channels:

- environment;
- schema;
- learner;
- controller;
- diagnostic sampling;
- artifact sampling.

This is important. Serious matrices should vary seed bundles, not quietly reuse
one global seed.

### Upstream Integration

Location:

```text
src/big_boy_benchmarking/upstream/
```

Implemented:

- import probes for upstream smoke envs;
- readout guards;
- `state_collapser` dependency-state capture.

Important corrected reality:

Earlier there was a false blocker involving `pkgutil.walk_packages` not seeing
some `state_collapser.examples.*` modules. Direct imports worked. The installed
pinned package is `state_collapser==0.6.0`; the local `<state-collapser-repo>`
repo should remain read-only for this work unless explicitly approved.

## Counterpoint Environment Implementation

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/
```

Files:

```text
__init__.py
actions.py
artifacts.py
diagnostics.py
fixture_search.py
graph.py
ids.py
instances.py
labels.py
legality.py
masks.py
path_volume.py
projection.py
rewards.py
runners.py
schemas.py
specs.py
state.py
tower_adapter.py
transition.py
```

### Identity And Locked IDs

Canonical IDs live in:

```text
src/big_boy_benchmarking/environments/counterpoint/ids.py
```

Important ids:

```text
environment_family_id: counterpoint_symbolic_v001
legality_contract_id: counterpoint_legality_local_v001
reward_bundle_id: counterpoint_reward_local_v001
edge_label_contract_id: counterpoint_edge_labels_local_v001
initial_state_policy_id: counterpoint_initial_states_v001
terminal_policy_id: counterpoint_terminal_horizon_v001
action_mask_policy_id: counterpoint_legal_action_mask_v001
empty_schema_id: counterpoint_empty_schema_v001
random_balanced_schema_family_id: counterpoint_random_balanced_schema_v001
random_unbalanced_schema_family_id: counterpoint_random_unbalanced_schema_v001
structured_motion_schema_id: counterpoint_motion_schema_v001
projection_audit_schema_id: counterpoint_projection_audit_schema_v001
bad_schema_id: counterpoint_bad_schema_v001
```

### State Contract

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/state.py
```

State:

```text
pitches: tuple[int, ...]
beat_index: int
```

States are hashable and serializable. Validation checks:

- voice count;
- pitch band;
- strict voice order;
- adjacent interval classes;
- outer interval class;
- max outer span;
- root interval class;
- beat index range.

### Action Contract

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/actions.py
```

Action:

```text
deltas: tuple[int, ...]
```

Actions are hashable and serializable. Raw action enumeration is deterministic
lexicographic over the delta lattice. Stationary voice policy is instance
controlled.

For the first tiny/small fixtures:

```text
voice_count: 3
max_step_size: 2
raw action count: 5^3 = 125
```

### Instance Spec

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/specs.py
```

The instance spec records:

- family id;
- instance id;
- family version;
- voice count;
- pitch band;
- tonic pitch class;
- measure size;
- horizon;
- max step size;
- stationary policy;
- strict voice order policy;
- allowed interval classes;
- forbidden parallel interval classes;
- max span;
- versioned legality/reward/label/mask/terminal ids.

This is the main finite graph contract.

### Fixtures

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/instances.py
```

Implemented default fixtures:

```text
counterpoint_symbolic_n3_tiny_v001
counterpoint_symbolic_n3_small_v001
```

Tiny:

```text
voice_count: 3
pitch_min: 60
pitch_max: 67
measure_size: 4
horizon_steps: 4
max_step_size: 2
max_outer_span: 8
```

Small:

```text
voice_count: 3
pitch_min: 60
pitch_max: 72
measure_size: 4
horizon_steps: 8
max_step_size: 2
max_outer_span: 12
```

Initial-state policy:

```text
first four legal compact beat-zero states
```

Observed initial tiny search chose two reachable legal start states.

### Legality

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/legality.py
```

Node checks:

- pitch band;
- strict voice order;
- adjacent interval class;
- outer interval class;
- max outer span;
- root interval class;
- beat index.

Edge checks:

- action voice count;
- action delta bounds;
- stationary voice policy;
- candidate node legality;
- forbidden parallel interval classes.

Legality returns structured failure reasons, not a bare bool.

### Transition

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/transition.py
```

Transition:

- applies one delta per voice;
- advances beat modulo measure size;
- checks legality;
- computes reward if legal;
- emits edge labels;
- marks terminal by horizon.

### Reward

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/rewards.py
```

Reward bundle:

```text
counterpoint_reward_local_v001
```

Terms:

- valid transition bonus;
- adjacent interval preference;
- outer interval preference;
- movement-size preference;
- motion-shape preference;
- range comfort penalty;
- beat-phase local preference;
- terminal completion bonus.

Important: v001 reward is action-local. It does not read path history.

The reward is not meant to be musically complete. It is a local reward-labelled
transition contract that lets us measure direct-image reward coherence,
reward-fiber variance, and whether schema cells mix incompatible reward
outcomes.

### Labels

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/labels.py
```

Edge labels include:

- beat phase before/after;
- per-voice delta;
- per-voice movement class;
- global motion direction pattern;
- adjacent interval classes before/after;
- outer interval class before/after;
- root interval class before/after;
- interval change classes;
- forbidden parallel check result;
- span bucket;
- terminal marker.

Labels are structural labels, not reward outcomes.

### Masks

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/masks.py
```

Masks enumerate raw actions in deterministic order and mark legal actions under
the active legality contract.

Mask density is a core structural diagnostic.

Tiny observed:

```text
raw actions: 125
legal actions per reachable state: 2
mask density: 0.016
```

Small observed:

```text
raw actions: 125
legal actions per reachable state: 4 to 19
mean mask density: 0.08444444444444443
```

### Graph Enumeration

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/graph.py
```

Exact reachable graph enumeration:

- starts from the active initial-state policy;
- follows legal masked actions only;
- records `GraphEdge` records with source, action, target, reward, and labels;
- deterministic ordering;
- summary includes state count, edge count, start count, dead ends, branch
  factors, mask density, horizon, and contract ids.

Observed exact counts:

```text
tiny:
  states: 8
  edges: 16
  branch_factor_min: 2
  branch_factor_mean: 2.0
  branch_factor_max: 2
  dead_end_count: 0

small:
  states: 108
  edges: 1140
  branch_factor_min: 4
  branch_factor_mean: 10.555555555555555
  branch_factor_max: 19
  dead_end_count: 0
```

### Path Volume

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/path_volume.py
```

Implemented:

- exact path count for paths of exactly length K;
- exact path count for paths up to length K;
- deterministic sampled path-volume estimates;
- random legal policy-effective path-volume hook.

Observed:

```text
tiny:
  length: 4
  exact length-K paths: 32
  exact up-to-K paths: 60

small:
  length: 8
  exact length-K paths: 1,723,548,896
  exact up-to-K paths: 1,873,218,755
```

This is probably the most motivating current data point.

### Fixture Search

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/fixture_search.py
```

Fixture search evaluates candidate specs and records:

- state count;
- edge count;
- branch factor summary;
- dead-end count;
- exact path-volume feasibility;
- exact horizon path count;
- selected flag.

Current tiny candidates:

```text
counterpoint_symbolic_n3_tiny_v001:
  selected: true
  states: 8
  edges: 16
  exact_horizon_path_count: 32

counterpoint_symbolic_n3_tiny_compact_v001:
  selected: false
  states: 0
  edges: 0
```

Current small candidates:

```text
counterpoint_symbolic_n3_small_v001:
  selected: true
  states: 108
  edges: 1140
  exact_horizon_path_count: 1,723,548,896

counterpoint_symbolic_n3_small_wide_v001:
  selected: false
  states: 160
  edges: 1784
  exact_horizon_path_count: 7,207,940,673
```

### Schema Families

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/schemas.py
```

Implemented:

```text
counterpoint_empty_schema_v001
counterpoint_random_balanced_schema_v001
counterpoint_random_unbalanced_schema_v001
counterpoint_motion_schema_v001
counterpoint_projection_audit_schema_v001
counterpoint_bad_schema_v001
```

Schema metadata records:

- schema id;
- schema family;
- version;
- family id;
- instance id;
- schema seed;
- construction method;
- source label families;
- state/action partition descriptions;
- expected tower depth;
- compression target;
- leakage-risk statement;
- intended role;
- online eligibility;
- diagnostic-only flag.

Leakage discipline:

- online-eligible schemas must not read reward outcomes, terminal outcomes,
  learned values, or future episode results;
- projection audit is diagnostic-only for now.

Schema roles:

- empty: identity/no contraction baseline;
- random balanced: seeded balanced control;
- random unbalanced: seeded giant-cell/singleton pathology;
- structured motion: edge-label motion/interval/beat/span grouping;
- projection audit: all-drop-one projection diagnostics, not online;
- bad: intentional overcompression into giant cells.

### Projection Diagnostics

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/projection.py
```

Implemented:

- projected state key;
- projected transition key;
- all-drop-one state/transition keys;
- fine states per projected state;
- fine transitions per projected transition;
- projection cell-size distribution.

This follows the Phase 1 decision:

```text
all-drop-one posthoc diagnostics;
no online projection default yet
```

### Reward/Lift/Address Diagnostics

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/diagnostics.py
```

Implemented diagnostics:

- reward-fiber variance;
- term-level variance;
- lift-fiber candidate count;
- lift-fiber entropy;
- valid/failed lift counts;
- balanced addressability;
- address frequency distribution;
- largest-cell share;
- singleton-cell share;
- effective number of cells;
- entropy.

These are the diagnostics that start to connect environment behavior to
`state_collapser` hypotheses.

### Artifact Builders

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/artifacts.py
```

Implemented environment artifacts:

- `environment_family_manifest.json`;
- `environment_instance_manifest.json`;
- `legality_manifest.json`;
- `reward_bundle_manifest.json`;
- `edge_label_manifest.json`;
- `initial_state_manifest.json`;
- `action_mask_manifest.json`;
- `graph_summary.json`;
- `mask_density.csv`;
- `path_volume_summary.json`;
- `path_volume_samples.jsonl`.

Implemented schema artifacts:

- `schema_manifest.json`;
- `schema_diagnostics.jsonl`;
- `quotient_summary.json`;
- `quotient_cells.csv`;
- `address_traces.jsonl`;
- `reward_fiber_variance.csv`;
- `lift_fiber_summary.csv`;
- `reward_term_diagnostics.jsonl`;
- `lift_attempts.jsonl`;
- `balanced_addressability.json`.

## Tower Integration

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
```

Verified upstream surfaces from installed `state_collapser==0.6.0`:

```text
state_collapser.core.state.State
state_collapser.core.action.PrimitiveAction
state_collapser.core.edges.BaseEdge
state_collapser.graph.hidden_graph.HiddenGraph
state_collapser.tower.partition.PartitionTower
state_collapser.tower.partition.RewardAggregator
state_collapser.tower.partition.schema.NoContractionSchema
state_collapser.tower.partition.schema.DimensionwiseSchema
state_collapser.tower.partition.schema.SeededRandomRateSchema
state_collapser.training.ActionDecision
state_collapser.training.ActionSelectionInput
```

Implemented adapter:

- converts `CounterpointState` to `state_collapser.core.state.State`;
- converts `CounterpointAction` to `PrimitiveAction`;
- converts graph edges to `BaseEdge`;
- implements `HiddenGraph` over the benchmark-owned environment;
- builds a `PartitionTower` over the exact reachable graph.

Hot-path readout discipline:

- default tower smoke does not call `PartitionTower.to_quotient_tier_views()`;
- tests monkeypatch that method to raise if it is accidentally used.

Current tower smoke supports:

- empty schema;
- structured motion schema;
- random balanced schema.

## Runners

Location:

```text
src/big_boy_benchmarking/environments/counterpoint/runners.py
```

Implemented direct runners:

```text
run_direct_masked_random
run_direct_tabular_q
```

Implemented tower runner:

```text
run_tower_schema_smoke
```

Direct masked-random:

- uses legal action masks;
- uses environment and learner seed channels from seed bundles;
- writes run manifests, seed bundle, mode manifest, timing segments, episodes,
  step events, and environment manifests.

Direct tabular-Q:

- uses legal action masks;
- separates learner seed from environment seed;
- records learner-act and learner-update timing;
- writes the same artifact family as masked random.

Tower schema smoke:

- builds exact graph;
- builds `PartitionTower`;
- writes schema manifest;
- writes quotient summary;
- writes reward-fiber variance;
- writes lift-fiber summary;
- writes timing and mode manifest;
- marks compatibility readout usage as false.

## CLI

Location:

```text
src/big_boy_benchmarking/cli/main.py
```

Top-level help:

```bash
uv run python -m big_boy_benchmarking.cli --help
```

Counterpoint help:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint --help
```

Counterpoint commands:

```text
search-fixtures
graph-diagnostics
schema-diagnostics
run-direct
tower-smoke
```

### Useful Current Commands

Validate shared contracts:

```bash
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Fixture search:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint search-fixtures \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --scale tiny
```

Tiny graph diagnostics:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint graph-diagnostics \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny
```

Small graph diagnostics:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint graph-diagnostics \
  --artifact-root <tmp-dir>/bbb-counterpoint-run-small \
  --instance-id small
```

Direct masked-random:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint run-direct \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny \
  --policy masked-random \
  --seed 1 \
  --episodes 1
```

Direct tabular-Q:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint run-direct \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny \
  --policy tabular-q \
  --seed 2 \
  --episodes 4
```

Schema diagnostics:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint schema-diagnostics \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny \
  --schema-id counterpoint_motion_schema_v001
```

Tower smoke:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint tower-smoke \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny \
  --schema-id counterpoint_motion_schema_v001 \
  --seed 2
```

Use a fresh artifact root per matrix if comparing results. Reusing the same root
can overwrite family summaries and append some row files.

## Current Smoke Run Observations

Recent user-run artifact root:

```text
<tmp-dir>/bbb-counterpoint-run
```

Commands run:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint graph-diagnostics \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny

uv run python -m big_boy_benchmarking.cli counterpoint run-direct \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny \
  --policy masked-random \
  --seed 1 \
  --episodes 1

uv run python -m big_boy_benchmarking.cli counterpoint tower-smoke \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny \
  --schema-id counterpoint_motion_schema_v001 \
  --seed 2
```

Observed outputs:

```text
graph-diagnostics:
  {"artifact_count": 10, "edge_count": 16, "state_count": 8, "status": "ok"}

run-direct:
  {"run_id": "counterpoint_symbolic_n3_tiny_v001-direct-masked-random-0", "status": "success"}

tower-smoke:
  {"run_id": "counterpoint_symbolic_n3_tiny_v001-counterpoint_motion_schema_v001-0", "status": "success"}
```

Graph summary:

```text
state_count: 8
edge_count: 16
reachable_start_count: 2
dead_end_count: 0
branch_factor_min: 2
branch_factor_mean: 2.0
branch_factor_max: 2
mask_density_min: 0.016
mask_density_mean: 0.016
mask_density_max: 0.016
horizon_steps: 4
```

Path volume:

```text
exact length-4 paths: 32
exact up-to-length-4 paths: 60
```

Direct masked-random single episode:

```text
total_reward: 7.328571428571429
step_count: 4
terminated: true
truncated: false
```

That particular seed chose action `(0, 0, 0)` at each step. This is legal
because stationary voices are currently enabled. Do not treat that as policy
quality evidence.

Tower motion smoke:

```text
schema_id: counterpoint_motion_schema_v001
mode_id: tower_nonempty_schema_tabular
partition_tier_count: 5
state_cell_count_by_tier: [8, 1, 1, 1, 1]
uses_compatibility_readout: false
```

In tiny, the structured motion schema collapses to a point quickly. That is
not automatically good or bad; it is an inspectable smoke fact. The small
fixture is probably the first place where schema distinctions become more
interesting.

## Test Coverage

Current full test suite:

```text
99 tests
```

Last observed validation:

```text
uv run pytest
-> 99 passed in 1.02s

uv run ruff check .
-> All checks passed!
```

Coverage areas:

- artifact manifests, paths, validators, writers;
- CLI commands;
- counterpoint IDs, specs, states, actions;
- legality;
- rewards;
- labels;
- masks;
- transition;
- fixture search;
- graph enumeration;
- path volume;
- projection diagnostics;
- schema families;
- reward/lift/address diagnostics;
- environment-specific artifacts;
- direct runners;
- tower adapter;
- mode registry/contracts;
- metrics/timing;
- seed bundles;
- upstream smoke integration and readout guards.

Important test files:

```text
tests/environments/counterpoint/test_tower_adapter.py
tests/environments/counterpoint/test_runners.py
tests/environments/counterpoint/test_graph.py
tests/environments/counterpoint/test_path_volume.py
tests/environments/counterpoint/test_schemas.py
tests/environments/counterpoint/test_diagnostics.py
tests/cli/test_cli.py
```

## Human-Facing Docs

Environment doc:

```text
docs/environments/counterpoint_symbolic_v001.md
```

Experiment matrix:

```text
docs/experiments/counterpoint_symbolic_v001_first_matrix.md
```

Method docs:

```text
docs/methods/counterpoint_schema_diagnostics.md
docs/methods/counterpoint_path_volume.md
docs/methods/counterpoint_reward_fibers.md
docs/methods/counterpoint_lift_fibers.md
```

Results stub:

```text
docs/results/counterpoint_symbolic_v001_first_smoke.md
```

The results stub intentionally preserves the claim boundary: current artifacts
are smoke/contract artifacts, not serious benchmark evidence.

## What We Can Honestly Benchmark Right Now

We can run these now:

1. Structural graph diagnostics:
   - state count;
   - edge count;
   - branch factors;
   - mask density;
   - dead ends;
   - exact/sampled path volume.

2. Schema diagnostics:
   - quotient cell counts;
   - address traces;
   - reward-fiber variance;
   - term-level variance;
   - lift-fiber size/entropy;
   - balanced addressability;
   - largest-cell share;
   - singleton-cell share;
   - effective number of cells.

3. Direct learner smoke:
   - masked random;
   - tabular Q;
   - episode return;
   - step count;
   - termination/truncation;
   - timing segments.

4. Tower integration smoke:
   - empty schema;
   - structured motion schema;
   - random balanced schema;
   - partition tier count;
   - state-cell count by tier;
   - readout-discipline flags;
   - schema diagnostics.

What we cannot honestly claim yet:

- no serious performance claim;
- no stable matrix over many seed bundles;
- no meaningful statistical comparison between schemas;
- no medium/large/stress results;
- no exploit/explore controller result;
- no fiber-conditioned substage result;
- no deep RL baseline;
- no claim that structured motion is actually better than random balanced;
- no claim that tower learning improves sample efficiency yet.

## The First Real Benchmark Matrix To Design Next

The next sensible design artifact should be a concrete run matrix workplan.

Suggested first serious matrix:

```text
environment_instance_id:
  counterpoint_symbolic_n3_small_v001

seed bundles:
  start with 10 or 30 replicates, not 1

arms:
  direct_env_masked_random
  direct_env_tabular
  tower_empty_schema_tabular
  tower_random_balanced_schema_tabular
  tower_motion_schema_tabular
  tower_random_unbalanced_schema_diagnostic
  tower_bad_schema_diagnostic

diagnostics:
  graph summary
  path volume
  mask density
  reward-fiber variance
  lift-fiber summary
  balanced addressability
  timing segments
  episode returns
```

Important: the current tower smoke builds a `PartitionTower`, but it is not yet
a full tower learner comparison. A serious matrix needs a sharper definition of
what tower action selection/training means for the comparison.

## Likely Next Engineering Tasks

### 1. Create A First Serious Matrix Design Doc

Path suggestion:

```text
docs/design/first_counterpoint_environment/01_005_counterpoint_first_serious_matrix_design.md
```

Questions to resolve:

- tiny or small as first serious target;
- number of seed bundles;
- episode budget;
- whether tabular Q is enough for first claim;
- whether tower arms need a true tower policy or only partition-diagnostic
  comparison first;
- what exact metric table should be generated;
- whether results should be written under `<tmp-dir>`, repo `artifacts/`, or
  both;
- whether artifact roots should include timestamp/run-family ids by default.

### 2. Make Matrix Runner

Current CLI runs one thing at a time. A next useful surface:

```bash
python -m big_boy_benchmarking.cli counterpoint run-matrix ...
```

It should:

- create a fresh run-family root;
- generate seed bundles;
- run each arm;
- write matrix manifest;
- write run index;
- write aggregate summary;
- avoid overwriting previous family summaries;
- record status for every arm/seed pair.

### 3. Add Results Summarization

Useful command:

```bash
python -m big_boy_benchmarking.cli counterpoint summarize-matrix ...
```

It should summarize:

- returns by arm;
- timing by arm;
- completion/truncation;
- schema diagnostics;
- readout/morphism policy flags;
- seed counts;
- bootstrap intervals eventually.

### 4. Tighten Tower Learning Semantics

The current tower smoke is real `PartitionTower` integration, but not a full
tower learning comparison. Before serious claims, decide:

- what is the tower action space exposed to the learner;
- how lifts are selected;
- whether tabular Q learns on coarse action cells;
- how failed lifts are counted;
- how online timing is separated from posthoc diagnostics;
- whether compatibility readouts remain excluded by default.

### 5. Improve Tiny Fixture Or Add A Better Toy

The current tiny fixture is perhaps too degenerate:

- only 8 states;
- only 16 edges;
- all states have exactly 2 legal actions;
- structured motion collapses to a point by tier 1.

It is still useful for unit tests and artifact smoke. It is probably not
interesting enough for schema-quality intuition.

The current small fixture is more interesting:

- 108 states;
- 1140 edges;
- branch factor 4 to 19;
- exact length-8 paths around 1.7B.

Use small for first serious diagnostics unless runtime surprises appear.

### 6. Add Stronger Artifact Hygiene

Current warning:

```text
Reusing the same artifact root can overwrite family summaries and append some
row files.
```

Next machinery should probably generate a unique run-family id with timestamp or
explicit `--run-family-id`, and should fail or require `--overwrite` if a root
already exists.

### 7. Add Stable Dataframe-Friendly Result Tables

Current artifacts are mostly per-run/per-diagnostic. We need result tables like:

```text
matrix_summary.csv
arm_summary.csv
schema_summary.csv
timing_summary_by_arm.csv
seed_bundle_outcomes.csv
```

This will make actual benchmark interpretation easier.

## Known Caveats And Traps

### Artifact Root Reuse

Do not casually reuse the same artifact root for serious matrix runs. Some
summary files are overwritten by run family, and some row files append. For
exploration this is fine; for real results it is not.

### Tiny Is Mostly A Contract Fixture

Tiny is great for:

- unit tests;
- exact enumeration;
- artifact shape checks;
- CLI smoke;
- tower adapter smoke.

Tiny is weak for:

- schema quality;
- learning comparison;
- meaningful reward-fiber conclusions.

### Direct Masked Random Can Look Too Good On Tiny

In a one-episode tiny run, masked random chose `(0, 0, 0)` each step and
terminated with positive reward. That is not a performance result.

### Structured Motion Collapse On Tiny

The tiny tower motion smoke produced:

```text
state_cell_count_by_tier: [8, 1, 1, 1, 1]
```

That is an interesting smoke fact, but not a proof. On tiny, the schema may be
too strong or the graph may be too small.

### Reward Is Narrow On Purpose

The reward is action-local and theorem-diagnostic-oriented. It should not be
treated as a full counterpoint aesthetic reward.

### Projection Audit Is Not Online

The projection audit schema is explicitly diagnostic-only in v001.

### Upstream Is Pinned

Dependency is pinned in `pyproject.toml` to:

```text
state-collapser[rl] @ git+https://github.com/TYLERSFOSTER/state_collapser.git@v0.6.0
```

Do not silently switch to the dirty local `<state-collapser-repo>` repo.

### Readout Discipline Matters

Do not accidentally include compatibility/morphism readout costs in default
online timing. Tests currently guard the tower adapter hot path.

### Commit State Changed After This Report

This report itself dirties the repo until committed.

## Validation Commands

Run these before any serious next step:

```bash
uv run pytest
uv run ruff check .
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Focused counterpoint checks:

```bash
uv run pytest tests/environments/counterpoint tests/cli
```

Current expected result:

```text
99 passed
All checks passed
```

## Suggested Immediate Next Session

Start with a design doc, not code.

Suggested prompt:

```text
Create a Phase.Stage.Action design/workplan for the first serious
counterpoint_symbolic_v001 small-fixture benchmark matrix, using the current
shared machinery and preserving the claim boundary.
```

Suggested design target:

```text
docs/design/first_counterpoint_environment/01_005_counterpoint_first_serious_matrix_design.md
```

The thing to decide is whether the next slice should be:

1. structural/schema diagnostics only on `small`;
2. direct learner matrix on `small`;
3. tower partition diagnostics on `small`;
4. a true tower learner comparison, which likely needs more design.

My recommendation:

```text
Do a structural/schema diagnostics matrix on small first.
Then do direct learner runs.
Then design true tower learner semantics after seeing the schema diagnostics.
```

Reason:

The current system already has strong graph/schema diagnostics. The riskiest
unresolved part is not graph construction; it is tower learning semantics. We
should get the small-fixture structural evidence before inventing more tower
controller machinery.

## Bottom Line

The repo has crossed from design-only into runnable benchmark machinery.

It can now:

- validate benchmark contracts;
- import pinned `state_collapser`;
- run upstream smoke checks;
- enumerate counterpoint graphs;
- compute exact and sampled path volume;
- construct and diagnose schema families;
- run direct masked-random and tabular-Q smoke;
- build `state_collapser` `PartitionTower`s for the benchmark-owned graph;
- write machine-readable artifacts;
- maintain human-facing environment/method/experiment/result docs.

The next meaningful step is not "can it run?" It can. The next meaningful step
is: define the first serious matrix carefully enough that the resulting
artifacts can support a real claim.
