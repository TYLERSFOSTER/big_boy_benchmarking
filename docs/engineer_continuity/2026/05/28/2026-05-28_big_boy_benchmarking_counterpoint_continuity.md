# Big Boy Benchmarking Continuity Report

Date: 2026-05-28

Repo: `<repo-root>`

Current branch at time of writing: `main`

Current head before this report was added: `4dd36f6 counterpoint environment built`

Purpose: preserve the engineering state, design intent, implementation lineage, and next moves for the benchmarking work around `state_collapser`, especially the first serious counterpoint environment and the shared benchmark machinery.

## 0. Executive summary

This repo has moved from an empty-or-early benchmarking shell into a runnable benchmark harness with:

- A prime-directive-driven design and implementation workflow.
- A benchmark artifact contract and shared artifact writing machinery.
- A mode registry for direct baselines, tower modes, ablations, pathologies, and diagnostics.
- Seed bundle helpers, metric/event row types, timing helpers, runner contracts, upstream smoke guards, and a CLI.
- A benchmark-owned counterpoint hidden graph environment with deterministic fixtures.
- Counterpoint graph diagnostics, schema diagnostics, direct-run smoke execution, and tower smoke integration.
- Human-readable docs folders for environments, experiments, results, and methods.
- Tests passing across the current implementation.

The repo is in a state where the current benchmark commands really run. They are still smoke and first-contract benchmarks, not serious scientific claims yet. The next design/implementation juncture is to move from "the environment and machinery run correctly" into "the first real benchmark matrix, result summarization, and comparison protocol."

## 1. Current repo state

The current known good state before adding this report:

```text
branch: main
head:   4dd36f6 counterpoint environment built
remote: main aligned with origin/main at that commit
status: clean before adding this continuity report
```

Recent commit history of interest:

```text
4dd36f6 counterpoint environment built
2e65675 Merge branch 'codex/counterpoint-hidden-graph-schema-benchmark-resume'
cbd3b17 Ignore macOS metadata files
8566d07 Implement shared benchmark machinery slice
d9d6360 artifacts design
3b3ffa4 first environment design and workplan: RL counterpoint
```

Validation state at the stopping point:

```text
uv run pytest
# 99 passed in 1.02s

uv run ruff check .
# All checks passed!
```

Focused post-merge test check:

```text
uv run pytest tests/cli tests/environments/counterpoint/test_runners.py tests/environments/counterpoint/test_tower_adapter.py
# 14 passed in 0.39s
```

Current top-level CLI surfaces:

```text
python -m big_boy_benchmarking.cli validate-contracts
python -m big_boy_benchmarking.cli run-upstream-smoke
python -m big_boy_benchmarking.cli summarize-smoke
python -m big_boy_benchmarking.cli counterpoint ...
```

Current counterpoint subcommands:

```text
python -m big_boy_benchmarking.cli counterpoint search-fixtures
python -m big_boy_benchmarking.cli counterpoint graph-diagnostics
python -m big_boy_benchmarking.cli counterpoint schema-diagnostics
python -m big_boy_benchmarking.cli counterpoint run-direct
python -m big_boy_benchmarking.cli counterpoint tower-smoke
```

## 2. Prime directive and working discipline

The user first asked Codex to read `docs/prime_directive`. Those documents are directed at the assistant and govern the work style in this repo.

The important behavioral constraints that shaped the repo work:

- Do not implement beyond approved scope.
- Use explicit design docs before implementation when the work is architecturally meaningful.
- Convert design into a Phase.Stage.Action-style workplan before execution.
- Preserve turn-by-turn owner conversation where ambiguity exists.
- Stop on real ambiguity, missing prerequisites, or dependency risk.
- Avoid silent simplification, silent reordering, and "helpful" rewriting of user intent.
- Use dedicated branches for implementation work.
- Keep implementation logs.
- Do not edit `<state-collapser-repo>` while doing this work unless explicitly told to.
- Treat `<state-collapser-repo>` as upstream/source context, not as the workspace to mutate.

There was a significant alignment correction during the shared machinery design stage. The user objected that a prior design layout was bad and put words in their mouth. The right lesson is now embedded in the repo process: when a doc is meant to hold owner answers, the assistant must not paraphrase those answers as if they were settled owner intent unless the owner actually wrote them or explicitly approved the phrasing. Questions should be visibly separated from assistant proposals and owner replies.

## 3. Relationship to `state_collapser`

This repo exists to benchmark `state_collapser`, especially in more serious settings than ad hoc toy examples. The user asked Codex to read:

- `<state-collapser-repo>/docs`
- root markdown files in `<state-collapser-repo>`

That read-only reconnaissance informed the goals here:

- We need serious benchmark artifacts, not one-off scripts.
- We need to avoid coupling benchmark semantics to hidden state in a local dirty upstream checkout.
- We need explicit contracts for environments, runs, modes, artifacts, seeds, metrics, and result docs.
- We need to preserve enough structure that results can be inspected by humans and re-run by machinery.

Important boundary:

- This repo should not modify `<state-collapser-repo>`.
- The installed dependency used during this work is `state_collapser==0.6.0`.
- The local upstream repo may contain newer or dirty files, but benchmark implementation should not silently switch to that copy.

## 4. Design lineage

### 4.1 Initial infrastructure slice

The first design arc lives under:

```text
docs/design/first_infrastructure_slice/
```

Key files:

```text
docs/design/first_infrastructure_slice/01_001_initial_benchmarking_goals_discussion.md
docs/design/first_infrastructure_slice/01_002_state_collapser_read_only_reconnaissance.md
docs/design/first_infrastructure_slice/01_003_benchmark_system_and_artifact_contract_blueprint.md
docs/design/first_infrastructure_slice/01_004_benchmark_system_artifact_contract_implementation_workplan.md
```

This arc established the need for:

- A benchmark artifact contract.
- Stable artifact directory layout.
- Environment summaries.
- Experiment summaries.
- Result summaries.
- Metric/event rows.
- Mode registry.
- Seed handling.
- Timing helpers.
- Runner skeletons.
- Upstream integration guards.
- A CLI.

It also introduced the requirement that workplans use `Phase.Stage.Action` labels. That became a hard convention.

### 4.2 Shared benchmark machinery

The shared machinery design arc lives under:

```text
docs/design/shared_benchmark_machinery/
```

Key files:

```text
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
docs/design/shared_benchmark_machinery/01_002_shared_benchmark_machinery_implementation_workplan.md
docs/design/shared_benchmark_machinery/01_003_shared_benchmark_machinery_implementation_log.md
```

This arc became the implementation foundation for:

- Artifact writers.
- Artifact validators.
- Artifact path conventions.
- Mode registry.
- Seed bundles.
- Metric/event rows.
- Timing helpers.
- Runner skeletons.
- Upstream smoke integration.
- CLI surfaces.

There was also a false stop during this arc, described later.

### 4.3 First counterpoint environment

The first real environment design arc lives under:

```text
docs/design/first_counterpoint_environment/
```

Key files:

```text
docs/design/first_counterpoint_environment/01_001_counterpoint_environment_design_discussion.md
docs/design/first_counterpoint_environment/01_002_counterpoint_hidden_graph_and_contraction_schema_benchmark_blueprint.md
docs/design/first_counterpoint_environment/01_003_counterpoint_hidden_graph_and_contraction_schema_implementation_workplan.md
docs/design/first_counterpoint_environment/01_004_counterpoint_hidden_graph_and_contraction_schema_implementation_log.md
```

This arc settled that the first environment is not the old `rl_counterpoint` example imported wholesale. It is a real benchmark-owned finite symbolic environment inspired by that thread of experimentation.

The environment is designed around:

- Hidden graph structure.
- Explicit legal transitions.
- Local reward decomposition.
- Action masks.
- Edge labels.
- Contraction schema diagnostics.
- Tower integration.
- Direct baseline execution.

## 5. Branch and merge history

The shared benchmark machinery and counterpoint work passed through several branches.

Important branch names that appeared:

```text
codex/shared-benchmark-machinery
codex/counterpoint-hidden-graph-schema-benchmark-resume
codex/counterpoint-hidden-graph-schema-benchmark
```

Important commits:

- `d9d6360 artifacts design`
- `8566d07 Implement shared benchmark machinery slice`
- `cbd3b17 Ignore macOS metadata files`
- `2e65675 Merge branch 'codex/counterpoint-hidden-graph-schema-benchmark-resume'`
- `4dd36f6 counterpoint environment built`

The user handled or directed merging such that the current `main` includes both the shared artifact machinery and the counterpoint environment implementation.

`.DS_Store` was added to `.gitignore` after macOS metadata files showed up in status. The goal was to avoid polluting benchmark commits with local Finder metadata.

## 6. False stop and reality correction

There was a confusing stop during shared machinery execution:

```text
Blocked because the installed pinned state_collapser==0.6.0 package does not expose
state_collapser.examples.plate_support_env or state_collapser.examples.rl_counterpoint_v3.
The local <state-collapser-repo> repo does have them, but it is dirty on main,
so I stopped instead of silently changing dependency semantics.
```

This was later corrected as a false stop.

What happened:

- A package discovery method made it look like the installed package did not expose example modules.
- Direct imports of the installed package examples actually worked.
- The correct interpretation is that `pkgutil.walk_packages(state_collapser.__path__)` was insufficient or misleading for this package layout.
- The installed pinned dependency can import:

```text
state_collapser.examples.plate_support_env
state_collapser.examples.rl_counterpoint_v3
```

This correction was recorded in the shared machinery implementation log.

The lasting rule:

- Do not silently switch dependency semantics to `<state-collapser-repo>`.
- But do verify with direct imports before declaring a package surface unavailable.

## 7. Shared benchmark machinery implemented

The shared machinery is now real code under:

```text
src/big_boy_benchmarking/
```

The central idea is that every benchmark run should produce structured, inspectable artifacts with enough metadata to reconstruct:

- What was run.
- Which environment fixture was used.
- Which mode was used.
- Which seed bundle was used.
- Which dependency versions and upstream surfaces were involved.
- Which metrics/events were emitted.
- Which timing information was captured.
- Whether contracts validated.

### 7.1 Artifact system

Implemented area:

```text
src/big_boy_benchmarking/artifacts/
```

The artifact system includes:

- Path conventions.
- Artifact schema constants.
- Manifest creation.
- Validation helpers.
- Writer helpers.
- JSONL metrics/events support.
- Run artifact directory handling.

The current artifact schema version reported by validation is:

```text
bbb.v001
```

The artifact machinery is intentionally boring and explicit. It exists to make benchmark outputs stable enough for future comparison, not to be a clever storage layer.

### 7.2 Mode registry

Implemented area:

```text
src/big_boy_benchmarking/modes/
```

The mode registry now reports seven modes via the contract validator:

```text
mode_count: 7
```

The design intent is that modes are first-class named benchmark choices. They are not just random command-line flags. The mode registry is where benchmark semantics become discoverable and auditable.

Mode categories include:

- Direct baselines.
- Tower modes.
- Ablations.
- Diagnostics.
- Pathologies.

For counterpoint, the mode story became more concrete through schemas such as empty, random, structured motion, projection audit, and bad/pathological schema variants.

### 7.3 Metrics and events

Implemented area:

```text
src/big_boy_benchmarking/metrics/
```

The metric/event machinery provides:

- Structured row types.
- Timing helpers.
- Summary/bootstrap utilities.
- JSONL-compatible event output.

The goal is not to invent a large analytics system yet. The current target is reliable row emission and simple summarization, with names stable enough that future scripts and docs can use them.

### 7.4 Seeds

Implemented area:

```text
src/big_boy_benchmarking/seeds/
```

Seed bundles exist so that a benchmark run can distinguish:

- User-facing run seed.
- Environment seed.
- Policy seed.
- Schema seed.
- Tie-breaker/randomness seed.

The point is reproducibility and later debugging. A single integer is not enough once environment sampling, policy choice, schema construction, and tower operations all have independent randomness.

### 7.5 Runner contracts

Implemented area:

```text
src/big_boy_benchmarking/runners/
```

The runner layer defines common contracts for:

- Runner identity.
- Run request.
- Run result.
- Smoke execution.
- Upstream smoke wiring.

The current runner layer is still intentionally skeletal. It provides enough structure to support smoke and early environment-specific runners. The next serious benchmark matrix will likely force the next refinement.

### 7.6 Upstream integration

Implemented area:

```text
src/big_boy_benchmarking/upstream/
```

The upstream layer exists to make dependency state visible rather than implicit. It checks:

- `state_collapser` version/importability.
- Known smoke surfaces.
- Readout/API compatibility boundaries.

This matters because `state_collapser` is an active project and the benchmark repo should not accidentally depend on untracked local state.

### 7.7 CLI

Implemented area:

```text
src/big_boy_benchmarking/cli/
```

The CLI now validates shared contracts and runs smoke commands. Example validation:

```text
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Known output:

```json
{
  "artifact_schema_version": "bbb.v001",
  "mode_count": 7,
  "reserved_console_command": "bbb",
  "smoke_ids": ["plate_support_env", "rl_counterpoint_v3"],
  "status": "ok"
}
```

The CLI also exposes the counterpoint subcommands described later.

## 8. Human-readable docs folders

The blueprint explicitly added docs-like human folders, because benchmark artifacts alone are not enough. A human needs quick summaries, method explanations, and result narration.

Folders now include:

```text
docs/environments/
docs/experiments/
docs/results/
docs/methods/
```

The intended split:

- `docs/environments/`: environment definitions and stable fixture descriptions.
- `docs/experiments/`: experiment plans/matrices.
- `docs/results/`: human-readable summaries of executed runs.
- `docs/methods/`: reusable method notes such as diagnostics and analysis definitions.

Current counterpoint docs include:

```text
docs/environments/counterpoint_symbolic_v001.md
docs/experiments/counterpoint_symbolic_v001_first_matrix.md
docs/results/counterpoint_symbolic_v001_first_smoke.md
docs/methods/counterpoint_schema_diagnostics.md
docs/methods/counterpoint_path_volume.md
docs/methods/counterpoint_reward_fibers.md
docs/methods/counterpoint_lift_fibers.md
```

These docs should be updated as real benchmark matrices replace smoke runs.

## 9. Counterpoint environment: high-level identity

The first benchmark environment family is:

```text
counterpoint_symbolic_v001
```

This is a benchmark-owned finite symbolic hidden graph. It is not intended to generate beautiful music. It is intended to provide a controlled structure where direct methods and abstraction/tower methods can be compared.

Core benchmark question:

```text
Can a contraction/tower method exploit structured equivalences or near-equivalences in a hidden graph while preserving enough control information to outperform or explain direct baselines?
```

The environment is counterpoint-flavored because:

- It has discrete state/action structure.
- It has local legality constraints.
- It has meaningful labels.
- It has sparse-ish legal masks over a larger raw action space.
- It has reward terms that can vary within contraction fibers.
- It naturally creates structured and pathological abstraction cases.

But it is deliberately finite and benchmark-owned, so we can enumerate graph properties and path volumes.

## 10. Counterpoint state, action, and transition model

State:

```text
CounterpointState(
    pitches: tuple[int, ...],
    beat_index: int,
)
```

Action:

```text
CounterpointAction(
    deltas: tuple[int, ...],
)
```

State semantics:

- `pitches` are symbolic MIDI-like pitch integers.
- `beat_index` is a local phase index in a fixed measure cycle.
- The number of voices is fixture-defined.

Action semantics:

- Each voice receives a bounded delta.
- Raw actions are generated lexicographically from the bounded delta range.
- Legal masks are derived from the legality contract.

Transition semantics:

- Apply action deltas to pitches.
- Advance beat index modulo measure size.
- Check legality.
- Compute local reward terms.
- Emit labels and diagnostics.
- Mark terminal state according to horizon contract in rollout contexts.

## 11. Counterpoint contract ids

The environment defines explicit contract identifiers:

```text
counterpoint_legality_local_v001
counterpoint_reward_local_v001
counterpoint_edge_labels_local_v001
counterpoint_initial_states_v001
counterpoint_terminal_horizon_v001
counterpoint_legal_action_mask_v001
```

These are important because benchmark artifacts should be interpretable even after implementation details evolve. If the semantic contract changes materially, the id should change.

## 12. Counterpoint fixtures

Two main fixtures are currently exposed:

```text
counterpoint_symbolic_n3_tiny_v001
counterpoint_symbolic_n3_small_v001
```

### 12.1 Tiny fixture

Fixture id:

```text
counterpoint_symbolic_n3_tiny_v001
```

Core parameters:

```text
voice_count: 3
pitch_min: 60
pitch_max: 67
measure_size: 4
horizon: 4
max_step: 2
max_span: 8
```

Measured graph shape:

```text
state_count: 8
edge_count: 16
reachable_start_count: 2
branch_factor_min: 2
branch_factor_mean: 2.0
branch_factor_max: 2
dead_end_count: 0
mask_density_min: 0.016
mask_density_mean: 0.016
mask_density_max: 0.016
exact_length_4_legal_paths: 32
paths_up_to_length_4: 60
```

Tiny is primarily for smoke, deterministic contract checks, and quick artifact inspection. It is too small for serious performance claims.

### 12.2 Small fixture

Fixture id:

```text
counterpoint_symbolic_n3_small_v001
```

Core parameters:

```text
voice_count: 3
pitch_min: 60
pitch_max: 72
measure_size: 4
horizon: 8
max_step: 2
max_span: 12
```

Measured graph shape:

```text
state_count: 108
edge_count: 1140
reachable_start_count: 4
branch_factor_min: 4
branch_factor_mean: 10.555555555555555
branch_factor_max: 19
dead_end_count: 0
mask_density_min: 0.032
mask_density_mean: 0.08444444444444443
mask_density_max: 0.152
exact_length_8_legal_paths: 1723548896
paths_up_to_length_8: 1873218755
```

Small is the first plausible serious benchmark fixture. It is still small enough to inspect and enumerate graph diagnostics, but large enough that path volume is nontrivial.

### 12.3 Rejected/secondary candidates

A tiny compact candidate was considered but is not used:

```text
state_count: 0
edge_count: 0
```

A wider small candidate exists as design context:

```text
state_count: 160
edge_count: 1784
exact_horizon_path_count: 7207940673
```

This wider candidate may become useful later, but it is not the current default fixture.

## 13. Initial state policy

The initial state contract is deterministic.

Current policy:

- Choose the first four legal compact beat-zero states.
- Deterministic ordering.
- Fixture may use fewer if fewer legal states exist.

This matters because initial states become a benchmark surface. They should not be accidental products of Python set ordering or local generation side effects.

## 14. Legality contract

The legality contract checks local properties only. It does not inspect long path history.

Legality constraints include:

- Pitch band constraints.
- Voice ordering constraints.
- Adjacent interval class constraints.
- Outer/root interval class constraints.
- Max span constraints.
- Beat index validity.
- Delta bound constraints.
- Stationary policy.
- Forbidden parallel interval checks.

This gives the graph enough structure to produce meaningful masks and edge labels without turning the environment into a full historical music-theory validator.

## 15. Reward contract

Reward contract id:

```text
counterpoint_reward_local_v001
```

Reward is local/action-local. Current reward terms include:

```text
valid_transition_bonus
adjacent_interval_preference
outer_interval_preference
movement_size_preference
motion_shape_preference
range_comfort_penalty
beat_phase_local_preference
terminal_completion_bonus
```

The important design point: reward diagnostics are separate from labels. Labels describe transition properties; reward terms score them. That separation lets contraction schemas be evaluated by label structure and by reward-fiber variance without confusing the two.

The reward is not intended to encode all musical quality. It is a benchmark signal with structured local variation.

## 16. Edge labels

Edge label contract id:

```text
counterpoint_edge_labels_local_v001
```

Labels include:

- Beat phase before and after transition.
- Per-voice delta.
- Per-voice movement class.
- Motion pattern.
- Adjacent interval classes.
- Outer/root interval class.
- Forbidden-parallel result.
- Span bucket.
- Terminal marker.

These labels support:

- Schema design.
- Schema diagnostics.
- Fiber variance analysis.
- Projection audit diagnostics.
- Human inspection.

## 17. Legal action masks

Legal action mask contract id:

```text
counterpoint_legal_action_mask_v001
```

Masks are derived from the legality contract over the raw action list.

Raw action ordering:

```text
lexicographic order over bounded delta tuples
```

For the tiny fixture:

```text
raw_action_count: 125
legal_action_count_per_state: 2
mask_density: 0.016
```

The sparse legal mask is one of the reasons this environment is useful as a benchmark. It lets direct masked baselines be separated from unmasked nonsense and gives tower methods a nontrivial control surface.

## 18. Counterpoint schema families

Current schema ids:

```text
counterpoint_empty_schema_v001
counterpoint_random_balanced_schema_v001
counterpoint_random_unbalanced_schema_v001
counterpoint_motion_schema_v001
counterpoint_projection_audit_schema_v001
counterpoint_bad_schema_v001
```

### 18.1 Empty schema

Purpose:

- Baseline "no meaningful contraction" or minimal schema behavior.
- Useful as a control.

### 18.2 Random balanced schema

Purpose:

- Randomized control with roughly balanced address/cell behavior.
- Helps distinguish structured schema benefit from arbitrary compression effects.

### 18.3 Random unbalanced schema

Purpose:

- Randomized control with intentionally less balanced grouping.
- Helps diagnose sensitivity to addressability and fiber shape.

### 18.4 Structured motion schema

Purpose:

- Counterpoint-aware contraction based on motion/label structure.
- This is the first positive hypothesis schema.

Current tiny tower smoke showed strong collapse:

```text
state_cell_count_by_tier: [8, 1, 1, 1, 1]
```

That is fine for smoke, but it should not be overinterpreted as benchmark evidence.

### 18.5 Projection audit schema

Purpose:

- Diagnostic-only schema family for posthoc projection/drop-one analysis.
- Not an online default.

### 18.6 Bad schema

Purpose:

- Pathology/control.
- Helps prove diagnostics can catch harmful abstraction.

## 19. Counterpoint diagnostics

Implemented diagnostics include:

- Graph diagnostics.
- Schema manifest generation.
- Quotient summary.
- Quotient cell summaries.
- Address traces.
- Balanced addressability diagnostics.
- Reward fiber variance.
- Lift fiber summary.
- Projection diagnostics.
- Path volume.

### 19.1 Graph diagnostics

Graph diagnostics produce counts and shape summaries:

- State count.
- Edge count.
- Reachable start count.
- Branch factor min/mean/max.
- Dead-end count.
- Mask density min/mean/max.
- Path counts.

Example command:

```text
uv run python -m big_boy_benchmarking.cli counterpoint graph-diagnostics \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny
```

Known output:

```json
{"artifact_count": 10, "edge_count": 16, "state_count": 8, "status": "ok"}
```

### 19.2 Schema diagnostics

Schema diagnostics create artifacts describing:

- Schema manifest.
- Quotient tier shape.
- Cell membership/summary.
- Address trace behavior.
- Reward variation inside fibers.
- Lift candidate behavior.
- Projection audit metrics where applicable.

These diagnostics are central to the benchmark. The goal is not just "which run got higher reward?" but "what did the abstraction preserve, discard, or distort?"

### 19.3 Reward fiber variance

Reward fiber variance asks:

```text
Within a contraction fiber, how much does local reward vary?
```

This is important because a schema that groups transitions with very different reward behavior may harm control even if it compresses well.

The diagnostic includes:

- Mean.
- Variance.
- Min.
- Max.
- Per-term variance summaries.

### 19.4 Lift fiber summary

Lift fiber diagnostics ask:

```text
When an abstract/tower choice points back to concrete choices, how broad and messy is that lift set?
```

The diagnostic includes:

- Candidate counts.
- Entropy-like summaries.
- Valid lift counts.
- Failed lift counts.

### 19.5 Projection diagnostics

Projection diagnostics ask:

```text
What happens if a schema drops one label/dimension at a time?
```

The current projection audit is posthoc/diagnostic-only. It should not be treated as an online schema in benchmark comparisons unless explicitly promoted later.

## 20. Tower adapter

Implemented file:

```text
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
```

The adapter maps benchmark-owned counterpoint concepts into `state_collapser` concepts.

Conversions:

```text
CounterpointState  -> state_collapser.core.State
CounterpointAction -> state_collapser.core.PrimitiveAction
Counterpoint edge  -> state_collapser.core.BaseEdge
```

It also implements:

```text
CounterpointHiddenGraph
```

And builds `PartitionTower` instances using upstream schemas such as:

```text
NoContractionSchema
DimensionwiseSchema
SeededRandomRateSchema
```

Important compatibility note:

- Tests monkeypatch `PartitionTower.to_quotient_tier_views` to ensure the default tower smoke path does not call compatibility readout behavior.
- The current tower smoke should be understood as full-graph construction and integration, not yet a full online learning/control runner.

## 21. Counterpoint direct runner

The direct runner currently supports smoke execution over the finite environment.

Known CLI:

```text
uv run python -m big_boy_benchmarking.cli counterpoint run-direct \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny \
  --policy masked-random \
  --seed 1 \
  --episodes 1
```

Known output:

```json
{
  "run_id": "counterpoint_symbolic_n3_tiny_v001-direct-masked-random-0",
  "status": "success"
}
```

This runner is useful for:

- Checking that action masks work.
- Checking reward/event emission.
- Checking deterministic run ids and artifact writing.
- Establishing a direct baseline surface.

It is not yet a serious learning benchmark.

One observed tiny run with seed `1` selected the all-zero delta action repeatedly and got a total reward of approximately:

```text
7.328571
```

Do not overinterpret that. Tiny has only 8 states and 16 edges.

## 22. Counterpoint tower smoke runner

Known CLI:

```text
uv run python -m big_boy_benchmarking.cli counterpoint tower-smoke \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny \
  --schema-id counterpoint_motion_schema_v001 \
  --seed 2
```

Known output:

```json
{
  "run_id": "counterpoint_symbolic_n3_tiny_v001-counterpoint_motion_schema_v001-0",
  "status": "success"
}
```

This confirms:

- The finite graph can be adapted into upstream hidden graph objects.
- The selected schema can be used to build a tower.
- Tower-derived artifacts can be written.
- The benchmark harness can execute the integration path.

This does not yet prove:

- Learning improvement.
- Online control improvement.
- Schema superiority.
- Generalization.

Those require the next benchmark matrix.

## 23. CLI command inventory

### 23.1 Validate contracts

```text
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Known output:

```json
{
  "artifact_schema_version": "bbb.v001",
  "mode_count": 7,
  "reserved_console_command": "bbb",
  "smoke_ids": ["plate_support_env", "rl_counterpoint_v3"],
  "status": "ok"
}
```

### 23.2 Counterpoint fixture search

```text
uv run python -m big_boy_benchmarking.cli counterpoint search-fixtures
```

Purpose:

- Discover available counterpoint fixtures.
- Support quick sanity checks.

### 23.3 Counterpoint graph diagnostics

```text
uv run python -m big_boy_benchmarking.cli counterpoint graph-diagnostics \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny
```

Known output:

```json
{"artifact_count": 10, "edge_count": 16, "state_count": 8, "status": "ok"}
```

### 23.4 Counterpoint schema diagnostics

```text
uv run python -m big_boy_benchmarking.cli counterpoint schema-diagnostics \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny \
  --schema-id counterpoint_motion_schema_v001 \
  --seed 2
```

Purpose:

- Emit schema-specific diagnostic artifacts.
- Inspect quotient behavior, addressability, reward fibers, lift fibers, and projection diagnostics.

### 23.5 Counterpoint direct run

```text
uv run python -m big_boy_benchmarking.cli counterpoint run-direct \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny \
  --policy masked-random \
  --seed 1 \
  --episodes 1
```

Known output:

```json
{
  "run_id": "counterpoint_symbolic_n3_tiny_v001-direct-masked-random-0",
  "status": "success"
}
```

### 23.6 Counterpoint tower smoke

```text
uv run python -m big_boy_benchmarking.cli counterpoint tower-smoke \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny \
  --schema-id counterpoint_motion_schema_v001 \
  --seed 2
```

Known output:

```json
{
  "run_id": "counterpoint_symbolic_n3_tiny_v001-counterpoint_motion_schema_v001-0",
  "status": "success"
}
```

## 24. Artifact roots used during smoke work

Known temporary artifact roots:

```text
<tmp-dir>/bbb-counterpoint-phase13-20260528
<tmp-dir>/bbb-counterpoint-run
<tmp-dir>/bbb-counterpoint-current-check
```

Purpose:

- `<tmp-dir>/bbb-counterpoint-phase13-20260528`: full Phase 13 smoke during implementation.
- `<tmp-dir>/bbb-counterpoint-run`: user-run examples from terminal.
- `<tmp-dir>/bbb-counterpoint-current-check`: sanity check after merge/current-state verification.

These are not committed artifacts. They are temp outputs.

Important caveat:

- The counterpoint CLI currently uses deterministic run ids and does not expose a strong `--run-id` override for all paths.
- Reusing an artifact root with the same fixture/mode/seed may overwrite or append depending on the writer path.
- For clean comparisons, use a fresh artifact root per run matrix or add a run-id/matrix-id surface.

## 25. Tests and coverage map

Current full test state:

```text
99 passed
```

Current lint state:

```text
ruff: All checks passed
```

Test coverage categories include:

- Artifact contract tests.
- Artifact writer/manifest tests.
- CLI tests.
- Mode registry tests.
- Metric/event tests.
- Seed bundle tests.
- Upstream smoke tests.
- Counterpoint fixture tests.
- Counterpoint graph tests.
- Counterpoint legality/reward/mask tests.
- Counterpoint schema diagnostics tests.
- Counterpoint direct runner tests.
- Counterpoint tower adapter tests.

Focused post-merge check:

```text
uv run pytest tests/cli tests/environments/counterpoint/test_runners.py tests/environments/counterpoint/test_tower_adapter.py
# 14 passed in 0.39s
```

## 26. Current code organization, likely files of interest

Shared machinery:

```text
src/big_boy_benchmarking/artifacts/
src/big_boy_benchmarking/modes/
src/big_boy_benchmarking/metrics/
src/big_boy_benchmarking/runners/
src/big_boy_benchmarking/seeds/
src/big_boy_benchmarking/upstream/
src/big_boy_benchmarking/cli/
```

Counterpoint environment:

```text
src/big_boy_benchmarking/environments/counterpoint/
```

Counterpoint docs:

```text
docs/design/first_counterpoint_environment/
docs/environments/counterpoint_symbolic_v001.md
docs/experiments/counterpoint_symbolic_v001_first_matrix.md
docs/results/counterpoint_symbolic_v001_first_smoke.md
docs/methods/counterpoint_schema_diagnostics.md
docs/methods/counterpoint_path_volume.md
docs/methods/counterpoint_reward_fibers.md
docs/methods/counterpoint_lift_fibers.md
```

Shared machinery docs:

```text
docs/design/shared_benchmark_machinery/
```

First infrastructure docs:

```text
docs/design/first_infrastructure_slice/
```

Prime directive:

```text
docs/prime_directive/
```

## 27. What "can run" means right now

The repo is runnable in the following sense:

- The package imports.
- The CLI works.
- Contract validation works.
- Counterpoint fixture diagnostics work.
- Direct smoke runs work.
- Tower smoke runs work.
- Artifacts are emitted.
- Tests pass.

The repo is not yet "done" in the following sense:

- No serious benchmark matrix has been run and summarized.
- No comparative result claims should be made.
- No long-run learning protocol is settled.
- No polished result aggregation CLI exists for counterpoint matrices.
- Tower smoke is not yet a full online abstraction/control benchmark.

So the right sentence is:

```text
We can run benchmark-shaped smoke and diagnostic artifacts now; we are ready to design and implement the first serious counterpoint benchmark matrix next.
```

## 28. Known caveats and risks

### 28.1 Tiny is too small for claims

Tiny has:

```text
8 states
16 edges
32 exact length-4 legal paths
```

It is excellent for smoke. It is not evidence.

### 28.2 Structured motion collapses tiny aggressively

Tiny motion schema tower smoke showed:

```text
state_cell_count_by_tier: [8, 1, 1, 1, 1]
```

That may be expected on tiny, but it means tiny schema results are mostly "does the pipeline run?" not "does this abstraction preserve useful control structure?"

### 28.3 Direct masked-random tiny behavior is trivial

Observed seed `1` selected `(0, 0, 0)` repeatedly. That is allowed and useful for smoke, but not meaningful as policy evidence.

### 28.4 CLI run-id ergonomics need improvement

The current counterpoint CLI should likely gain:

- `--run-id`
- `--matrix-id`
- or a higher-level experiment command that creates unique run directories.

Until then, use fresh artifact roots for clean runs.

### 28.5 Tower smoke is not online tower learning

Current tower smoke builds/adapts/diagnoses. It is not yet the serious online tower-vs-direct comparison.

### 28.6 Projection audit is diagnostic-only

Do not treat projection audit as a default online schema unless that is explicitly designed.

### 28.7 Medium/large/stress tiers are reserved

The current serious candidate is `small`. Larger tiers should be designed deliberately after the first small matrix is understood.

### 28.8 Do not import old `rl_counterpoint` as the benchmark environment

The benchmark-owned counterpoint environment exists to avoid making serious benchmark semantics depend on an old exploratory example.

### 28.9 Do not edit upstream casually

`<state-collapser-repo>` may be dirty and is out of scope for mutation unless explicitly requested.

## 29. What we learned from the user-run commands

The user ran:

```text
uv run python -m big_boy_benchmarking.cli counterpoint graph-diagnostics \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny
```

Output:

```json
{"artifact_count": 10, "edge_count": 16, "state_count": 8, "status": "ok"}
```

Interpretation:

- The tiny fixture graph was built.
- It has 8 states and 16 legal edges.
- Ten artifacts were written, likely including manifest, graph summary, state/edge/mask/path diagnostics, and related metadata depending on writer layout.

The user ran:

```text
uv run python -m big_boy_benchmarking.cli counterpoint run-direct \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny \
  --policy masked-random \
  --seed 1 \
  --episodes 1
```

Output:

```json
{"run_id": "counterpoint_symbolic_n3_tiny_v001-direct-masked-random-0", "status": "success"}
```

Interpretation:

- The direct runner executed one episode.
- It used only legal actions.
- It wrote a run artifact bundle under the artifact root.
- It is a smoke check, not a benchmark result.

The user ran:

```text
uv run python -m big_boy_benchmarking.cli counterpoint tower-smoke \
  --artifact-root <tmp-dir>/bbb-counterpoint-run \
  --instance-id tiny \
  --schema-id counterpoint_motion_schema_v001 \
  --seed 2
```

Output:

```json
{"run_id": "counterpoint_symbolic_n3_tiny_v001-counterpoint_motion_schema_v001-0", "status": "success"}
```

Interpretation:

- The counterpoint graph adapted into the upstream tower path.
- The motion schema built a tower successfully.
- Artifacts were written.
- This confirms integration, not performance.

## 30. Recommended next design step

The next design doc should probably be:

```text
docs/design/first_counterpoint_benchmark_matrix/01_001_counterpoint_first_real_matrix_design.md
```

or similar.

It should answer:

- Which fixture is the first serious default: likely `small`.
- Which modes are included in the first real matrix.
- Which direct baseline is fair.
- Whether tower comparison is full online control now or still graph/schema diagnostic.
- Which seeds and seed bundle policy to use.
- Which metrics define success.
- Which diagnostics are required per run.
- Which artifact and result summaries are committed or documented.
- What runtime budget is acceptable.
- What counts as a failed run.
- What is allowed to be "smoke only" versus result evidence.

## 31. Recommended next implementation work

Likely next engineering steps:

1. Add robust run id support to counterpoint CLI.
2. Add a counterpoint matrix runner command.
3. Add a counterpoint result summarizer.
4. Run small fixture graph diagnostics and schema diagnostics across selected schemas/seeds.
5. Implement or expose the first direct learning baseline beyond masked-random, if needed.
6. Decide whether tower benchmarking now uses upstream `TowerRuntime` style online stepping or remains full-graph diagnostic for one more phase.
7. Write result docs from actual artifacts under `docs/results/`.
8. Keep tiny as CI/smoke and small as the first serious benchmark surface.

## 32. Candidate first real matrix

A reasonable first matrix, subject to owner approval:

Fixture:

```text
counterpoint_symbolic_n3_small_v001
```

Direct modes:

```text
direct-masked-random
direct-tabular-q or equivalent learned direct baseline
```

Schema/tower modes:

```text
counterpoint_empty_schema_v001
counterpoint_random_balanced_schema_v001
counterpoint_random_unbalanced_schema_v001
counterpoint_motion_schema_v001
counterpoint_bad_schema_v001
```

Diagnostics:

```text
graph diagnostics
schema manifest
quotient summary
reward fiber variance
lift fiber summary
projection audit, posthoc only
path volume
per-run metrics/events
```

Seeds:

```text
small fixed seed bundle set, e.g. 5 to 10 seeds first
```

Outputs:

```text
artifact root under <tmp-dir> or user-specified path
machine-readable summaries
docs/results markdown summary
```

Open questions:

- Do we implement a learning baseline now or first run diagnostic-only matrix?
- What is the right tower online comparison protocol?
- What budget is acceptable per seed?
- Are success metrics reward-only, regret-like, legal completion, diagnostic quality, or a combination?

## 33. Do-not-do list for the next engineer

Do not:

- Claim serious benchmark results from tiny smoke.
- Reuse an artifact root for clean comparisons without understanding overwrite/append behavior.
- Silently point dependency imports at `<state-collapser-repo>`.
- Edit `<state-collapser-repo>` unless explicitly asked.
- Treat projection audit as an online schema by default.
- Remove the Phase.Stage.Action discipline from implementation plans.
- Rewrite owner answers in design docs as if they were assistant-authored conclusions.
- Use compatibility/morphism readouts in the hot path without explicitly validating the upstream API and intent.
- Import old `rl_counterpoint` code as the benchmark environment.

## 34. Resume checklist

Before starting the next work session:

```text
git status --short --branch
uv run pytest
uv run ruff check .
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Then run a tiny smoke if needed:

```text
uv run python -m big_boy_benchmarking.cli counterpoint graph-diagnostics \
  --artifact-root <tmp-dir>/bbb-counterpoint-resume-check \
  --instance-id tiny

uv run python -m big_boy_benchmarking.cli counterpoint run-direct \
  --artifact-root <tmp-dir>/bbb-counterpoint-resume-check \
  --instance-id tiny \
  --policy masked-random \
  --seed 1 \
  --episodes 1

uv run python -m big_boy_benchmarking.cli counterpoint tower-smoke \
  --artifact-root <tmp-dir>/bbb-counterpoint-resume-check \
  --instance-id tiny \
  --schema-id counterpoint_motion_schema_v001 \
  --seed 2
```

If those pass, the repo is ready to continue design for the first real benchmark matrix.

## 35. Bottom line

The repo has crossed an important threshold. It is no longer merely a design shell. It has a runnable benchmark harness, artifact discipline, docs structure, and a first finite environment with direct and tower smoke execution.

The next threshold is different: stop proving that the machinery can run, and start designing the first serious matrix where results can be compared, summarized, and argued about without hand-waving.

