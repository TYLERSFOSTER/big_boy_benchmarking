# BBB v0.7.2 Pointwise Liftability Integration Implementation Log

Date started: 2026-06-05

Repository:

```text
<repo-root>
```

Source blueprint:

```text
docs/design/state_collapser_v072_pointwise_liftability_handoff/01_001_bbb_v072_pointwise_liftability_integration_blueprint.md
```

Source workplan:

```text
docs/design/state_collapser_v072_pointwise_liftability_handoff/01_002_bbb_v072_pointwise_liftability_integration_implementation_workplan.md
```

## Starting State

- Project Owner explicitly requested execution of the source workplan.
- Required authority documents were re-read before source edits.
- Starting branch before implementation branch creation:

  ```text
  ## main...origin/main [ahead 4]
  ```

- Dedicated implementation branch created:

  ```text
  codex/bbb-v072-pointwise-liftability
  ```

- Initial working tree after branch creation had no reported dirty paths before
  this implementation log was created.

## Phase.Stage.Action Completion Log

- Phase 0. Stage 0. Action 1: completed as written. Re-read the required
  Prime Directive failure-mode docs, git practices doc, source blueprint, and
  source workplan before source edits.
- Phase 0. Stage 0. Action 2: completed as written. Inspected git status and
  recorded starting state.
- Phase 0. Stage 0. Action 3: completed as written. Created and switched to
  `codex/bbb-v072-pointwise-liftability`.
- Phase 0. Stage 0. Action 4: completed as written. Created this
  implementation log with the required sections.
- Phase 0. Stage 1. Action 1: completed as written. Verified
  `state_collapser` version and required upstream API signatures.
- Phase 0. Stage 1. Action 2: completed as written. Inspected current
  counterpoint integration points and recorded weak uses below.
- Phase 1. Stage 0. Action 1: completed as written. Added dependency-state
  checks for required `PartitionTower` pointwise/invariant methods.
- Phase 1. Stage 0. Action 2: completed as written. Added dependency probe
  assertions for the required `PartitionTower` method surface.
- Phase 1. Stage 1. Action 1: completed as written. Added an upstream
  pointwise liftability fixture proving that quotient outgoing action support
  can be nonempty while strict executable lift candidates are empty from a
  particular concrete state.
- Phase 2. Stage 0. Action 1: completed as written. Added one canonical
  counterpoint liftability semantics ID:
  `state_collapser_v072_pointwise`.
- Phase 2. Stage 0. Action 2: completed as written. Added local JSON-safe
  serialization helpers for upstream `PartitionInvariantReport` and issue
  objects.
- Phase 2. Stage 0. Action 3: completed as written. Added counterpoint tower
  invariant collection and assertion helpers that delegate to the upstream
  `PartitionTower` invariant APIs.
- Phase 2. Stage 0. Action 4: completed as written. Added tower adapter tests
  for clean structured/noisy towers and required invariant issue fields.
- Phase 3. Stage 0. Action 1: completed as written. Added quotient,
  representative, and pointwise vocabulary/candidate helpers on the counterpoint
  tower-control adapter.
- Phase 3. Stage 0. Action 2: completed as written. Replaced tier
  executability with upstream current-base-state pointwise executability.
- Phase 3. Stage 0. Action 3: completed as written. Updated learner
  vocabulary and masks to use pointwise executable action cells, with quotient
  diagnostics preserved.
- Phase 3. Stage 0. Action 4: completed as written. Kept quotient action counts
  as stable tabular learner upper bounds while enforcing pointwise runtime
  masks.
- Phase 3. Stage 1. Action 1: completed as written. Extended
  `LiftResolveTrace` with representative/pointwise candidate counts, selected
  lift details, and liftability semantics ID.
- Phase 3. Stage 1. Action 2: completed as written. Replaced execution lift
  query with strict `executable_lift_candidates`; removed representative
  fallback from execution.
- Phase 3. Stage 1. Action 3: completed as written. Representative candidate
  counts are diagnostic-only and no longer affect execution.
- Phase 3. Stage 2. Action 1: completed as written. Added tower-control tests
  for pointwise executable tier delegation, pointwise masks, strict executor
  behavior, and no representative fallback.
- Phase 4. Stage 0. Action 1: completed as written. Extended serious learning
  lift event rows with pointwise/representative liftability fields.
- Phase 4. Stage 0. Action 2: completed as written. Extended affected
  diagnostic lift/tier/shape rows additively, keeping static tower-shape counts
  explicitly labeled as non-pointwise storage evidence.
- Phase 4. Stage 0. Action 3: completed as written. Updated affected event-row
  writers so new lift rows preserve `candidate_count == pointwise_candidate_count`.
- Phase 4. Stage 1. Action 1: completed as written. Added
  `tower_invariant_report.json` artifacts to affected tower-control run roots.
- Phase 4. Stage 1. Action 2: completed as written. Counterpoint tower builds
  now call upstream `assert_consistent()` immediately after initialization, so a
  dirty/inconsistent tower fails before a long runner can emit misleading
  success rows; successful runs write `tower_invariant_report.json`.
- Phase 5. Stage 0. Action 1: completed as written. One-third diagnostics now
  use corrected adapter semantics and emit pointwise liftability fields.
- Phase 5. Stage 0. Action 2: completed as written. Fraction sweep diagnostics
  now use corrected runtime semantics and distinguish static quotient/storage
  counts from pointwise liftability.
- Phase 5. Stage 0. Action 3: completed as written. Noisy-rate diagnostics now
  use corrected runtime semantics and emit pointwise liftability fields.
- Phase 5. Stage 0. Action 4: completed as written. Noisy-rate full training now
  uses corrected masks/lift resolution and records compatibility notes when
  parent candidate data lacks current-base-state pointwise fields.
- Phase 5. Stage 0. Action 5: completed as written. Second serious comparison
  propagates pointwise fields through its wrapper rows, manifests/readout source,
  and generated docs.
- Phase 6. Stage 0. Action 1: completed as written for the first corrected
  durable target. Second-serious readout source records the pointwise semantics
  ID, `state_collapser` version, expected invariant run files, and pointwise
  lift fields.
- Phase 6. Stage 0. Action 2: completed as written for the first corrected
  durable target. Second-serious generated README/method text explains quotient
  availability versus pointwise executable liftability.
- Phase 6. Stage 0. Action 3: completed as written for the first corrected
  durable target. Second-serious docs writer generates local badges for
  liftability semantics, invariant preflight, and lift failures.
- Phase 6. Stage 0. Action 4: completed as written. Second-serious docs writer
  preserves the protected turn section across regeneration.
- Phase 7. Stage 0. Action 1: completed as written. Focused test paths from
  the workplan passed.
- Phase 7. Stage 0. Action 2: completed as written. Full pytest suite passed.
- Phase 7. Stage 0. Action 3: completed as written. Ruff passed on touched
  Python files.
- Phase 8. Stage 0. Action 1: completed as written with one repo-guard
  correction. Graph diagnostics smoke passed in `<tmp-dir>`; second-serious
  `<tmp-dir>` smoke was correctly rejected because that runner requires
  repo-resident artifact roots; fallback serious-learning tower-control smoke
  passed in `<tmp-dir>`.
- Phase 8. Stage 1. Action 1: blocked with Project Owner guidance needed.
  The configured parent candidate readout source contains one eligible
  `wide_span18` candidate and zero eligible `medium` candidates, so the
  workplan's required medium four-candidate calibration cannot start without
  changing candidate source or approved target instance.

## API Reconnaissance

Observed by running a local `uv run python` probe:

```text
version 0.7.2
invariant_report (self, *, allow_dirty: 'bool' = False) -> 'PartitionInvariantReport'
assert_consistent (self, *, allow_dirty: 'bool' = False) -> 'None'
executable_lift_candidates (self, tier: 'int', action_cell_id: 'ActionCellId', current_base_state: 'State') -> 'tuple[BaseEdge, ...]'
tier_is_executable_from_state (self, tier: 'int', current_base_state: 'State') -> 'bool'
lift_candidates (self, tier: 'int', action_cell_id: 'ActionCellId', current_base_state: 'State') -> 'tuple[BaseEdge, ...]'
outgoing_action_cells (self, tier: 'int', state_cell_id: 'StateCellId') -> 'tuple[ActionCellId, ...]'
```

Weak integration locations found before source edits:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
- CounterpointTowerControlAdapter.tier_is_executable uses outgoing_action_cells.
- CounterpointTierLearner._tier_action_count uses outgoing_action_cells.
- CounterpointTierLearner._action_vocabulary uses outgoing_action_cells.
- CounterpointLiftResolveExecutor._execute uses outgoing_action_cells, lift_candidates, and action_cell_members fallback.
- LiftResolveTrace records only candidate_count.

src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/runner.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/runner.py
- Reuse CounterpointTowerControlAdapter.tier_is_executable and LiftResolveTrace candidate_count.
- Static tower-shape helpers still count quotient outgoing_action_cells.
```

## Invariant Reports

Clean helper coverage:

```text
build_counterpoint_partition_tower(default_tiny_spec, structured motion) -> ok
build_counterpoint_noisy_rate_partition_tower(default_small_spec, 1/18) -> ok
synthetic issue serialization includes tier, code, message, state_cell_id,
action_collection_id, action_cell_id, edge_id
```

## Artifact And Readout Decisions

Pending.

## Test Results

```text
uv run pytest tests/upstream/test_state_collapser_dependency_state.py
5 passed in 0.08s
```

```text
uv run pytest tests/upstream/test_state_collapser_pointwise_liftability.py
1 passed in 0.03s
```

```text
uv run pytest tests/environments/counterpoint/test_tower_adapter.py
10 passed in 0.95s
```

```text
uv run pytest tests/environments/counterpoint/test_serious_learning_tower_control.py tests/environments/counterpoint/test_serious_learning_events.py
15 passed in 0.20s
```

```text
uv run pytest tests/environments/counterpoint/test_one_third_diagnostics.py tests/environments/counterpoint/test_fraction_sweep_diagnostics.py tests/environments/counterpoint/test_noisy_rate_diagnostics.py tests/environments/counterpoint/test_noisy_rate_full_training.py tests/environments/counterpoint/test_second_serious_comparison.py
37 passed in 16.59s
```

```text
uv run pytest tests/environments/counterpoint/test_noisy_rate_full_training.py tests/environments/counterpoint/test_second_serious_comparison.py
13 passed in 8.16s
```

```text
uv run pytest tests/upstream/test_state_collapser_dependency_state.py tests/upstream/test_state_collapser_pointwise_liftability.py tests/environments/counterpoint/test_tower_adapter.py tests/environments/counterpoint/test_serious_learning_tower_control.py tests/environments/counterpoint/test_one_third_diagnostics.py tests/environments/counterpoint/test_fraction_sweep_diagnostics.py tests/environments/counterpoint/test_noisy_rate_diagnostics.py tests/environments/counterpoint/test_noisy_rate_full_training.py tests/environments/counterpoint/test_second_serious_comparison.py
64 passed in 17.73s
```

```text
uv run pytest
224 passed in 30.83s
```

```text
uv run ruff check <touched Python files>
initial run found import ordering, unused imports, and two line-length issues;
after fixes, all checks passed.
```

```text
uv run pytest
224 passed in 31.62s
```

```text
uv run python -c 'import state_collapser; print(state_collapser.__version__)'
0.7.2
```

## Rerun Results

Smoke:

```text
uv run python -m big_boy_benchmarking.cli counterpoint graph-diagnostics --artifact-root <tmp-dir>/bbb-v072-pointwise-smoke --instance-id tiny
{"artifact_count": 10, "edge_count": 16, "state_count": 8, "status": "ok"}
```

Second-serious smoke attempts:

```text
uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison run --artifact-root <tmp-dir>/bbb-v072-pointwise-second-smoke ...
ValueError: path must be repo-resident under <repo-root>; got <tmp-dir>/bbb-v072-pointwise-second-smoke
```

```text
uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison run --artifact-root docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/v072_pointwise_smoke_001 --instance-id small ...
ValueError: candidate source yielded no eligible Schema 1 candidates for counterpoint_symbolic_n3_small_v001
```

```text
uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison run --artifact-root docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/v072_pointwise_smoke_001 --instance-id medium ...
ValueError: candidate source yielded no eligible Schema 1 candidates for counterpoint_symbolic_n3_medium_v001
```

Parent candidate source inspection:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
candidate_summary rows: 1
eligible candidate instance: counterpoint_symbolic_n3_wide_20_108_span18_v001
eligible medium candidates: 0
```

Fallback serious-learning smoke:

```text
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning run --artifact-root <tmp-dir>/bbb-v072-pointwise-serious-smoke --instance-id small --episodes 1 --replicates 1 --schema-seeds 2 --locked-by foster --horizon 4 --linearization-mode tensor_available_disabled
{"evaluation_budget_lock": "<tmp-dir>/bbb-v072-pointwise-serious-smoke/evaluations/counterpoint_first_serious_learning_v001/evaluation_budget_lock.json", "evaluation_run_index": "<tmp-dir>/bbb-v072-pointwise-serious-smoke/evaluations/counterpoint_first_serious_learning_v001/evaluation_run_index.csv", "run_count": 9, "status": "complete"}
```

## Surprises And Stop Conditions

- Phase 8. Stage 1. Action 1 is blocked by candidate-source mismatch. The
  workplan requires medium corrected calibration using four eligible candidates,
  but the configured parent source currently has one eligible `wide_span18`
  candidate and no eligible `medium` candidates.
- The second-serious CLI correctly rejected `<tmp-dir>` artifact roots
  because its path guard requires repo-resident artifacts.

## Final Audit

Pending.
