# Counterpoint Threshold Frontier Probe Implementation Log

Date: 2026-06-05

Branch:

```text
codex/threshold-frontier-probe
```

Source gameplan:

```text
docs/design/first_counterpoint_environment/threshold_frontier_probe/01_002_counterpoint_threshold_frontier_probe_implementation_gameplan.md
```

Execution instruction:

```text
execute `docs/design/first_counterpoint_environment/threshold_frontier_probe/01_002_counterpoint_threshold_frontier_probe_implementation_gameplan.md`
```

Initial repo state:

```text
## main...origin/main [ahead 1]
```

Branch action:

```text
git checkout -b codex/threshold-frontier-probe
```

## Phase.Stage.Action Checklist

### Phase 0: Authority, Branch, And Reality Check

- Phase 0. Stage 0. Action 1: Completed. The Project Owner explicitly asked
  to execute this exact gameplan.
- Phase 0. Stage 0. Action 2: Completed. Execution authority was present.
- Phase 0. Stage 0. Action 3: Completed. Exact execution instruction recorded
  above.
- Phase 0. Stage 0. Action 4: Completed. The gameplan-generation request is
  distinguished from this execution request.
- Phase 0. Stage 1. Action 1: Completed. Initial `git status --short --branch`
  showed clean `main` ahead of `origin/main` by one commit.
- Phase 0. Stage 1. Action 2: Completed. No unrelated dirty files, TeX files,
  generated TeX sidecars, readout conversations, or artifact roots were
  present before branch creation.
- Phase 0. Stage 1. Action 3: Completed. No unrelated dirty state needed to be
  touched, staged, reverted, or mixed.
- Phase 0. Stage 1. Action 4: Completed. Created and switched to
  `codex/threshold-frontier-probe`.
- Phase 0. Stage 1. Action 5: Completed. Branch creation and initial dirty
  state recorded here.
- Phase 0. Stage 2. Actions 1-9: Completed. Re-read Prime Directive authority,
  threshold-frontier blueprint/README, current candidate/readout sources,
  second-serious comparison source, small-paired probe source, CLI surfaces,
  and adjacent tests.
- Phase 0. Stage 2. Action 10: Completed. Source mapping: the
  threshold-frontier probe will compose existing second-serious per-threshold
  run and aggregation behavior, then write frontier-specific top-level
  manifests, tables, `readout_source.json`, and docs. This avoids overwriting
  the canonical second-serious repo readout.
- Phase 0. Stage 3. Action 1: Completed. This log was created.
- Phase 0. Stage 3. Action 2: Completed. Branch, execution instruction, source
  gameplan, initial state, stop conditions, and checklist are recorded.
- Phase 0. Stage 3. Action 3: Completed. This log was updated after
  implementation and verification.

### Phase 1: Evaluation Identity, Package, Config, And Paths

- Phase 1. Stage 1: Completed. Added the threshold-frontier evaluation id,
  run-family id, and run-mode id in
  `src/big_boy_benchmarking/environments/counterpoint/ids.py`, preserving
  existing ids.
- Phase 1. Stage 2: Completed. Added the new package:

```text
src/big_boy_benchmarking/environments/counterpoint/threshold_frontier_probe/
```

  with `config.py`, `paths.py`, `thresholds.py`, `candidate_source.py`,
  `runner.py`, `aggregation.py`, `manifests.py`, and `docs_writer.py`.
- Phase 1. Stage 3: Completed. Implemented
  `ThresholdFrontierProbeBudget` with locked defaults: wide span-18 instance,
  parent noisy-rate full-tower candidate source, `candidate_cap = 1`,
  threshold grid `12.0,13.0,13.25,13.5,13.75,14.0`,
  `training_replicates_per_arm = 1`, `episodes_per_replicate = 8`,
  `window_length = 5`, `required_count = 4`, `base_seed = 0`, and
  `tensor_available_disabled`.
  Post-smoke correction: after the Project Owner identified that the 4-of-5
  sustained-hit rule is central and should be preserved, the threshold-frontier
  default was raised to `episodes_per_replicate = 16` so future non-smoke runs
  have enough episode runway to adjudicate the persistence window without
  weakening the 4/5 ratio.
- Phase 1. Stage 4: Completed. Implemented repo-resident path contracts under:

```text
docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/
```

  including threshold-run roots such as `threshold_runs/r012000/`.

### Phase 2: Candidate Source And Threshold Schedule

- Phase 2. Stage 1: Completed. Candidate loading reuses the existing
  second-serious schema-candidate source contract and validates the repo-side
  noisy-rate full-tower readout source.
- Phase 2. Stage 2: Completed. Threshold parsing enforces numeric,
  non-empty, unique, sorted grids and stable labels such as `r012000` and
  `r013250`.
- Phase 2. Stage 3: Completed. Each threshold constructs a matched
  second-serious comparison subrun with the same candidate, seed, budget, and
  full-iterated noisy-rate Schema 1 source, differing only by threshold value
  and threshold label.

### Phase 3: Runner Implementation

- Phase 3. Stage 1: Completed. Implemented
  `run_threshold_frontier_probe`.
- Phase 3. Stage 2: Completed. The runner writes frontier-level manifests,
  then runs each threshold into a threshold-scoped sub-artifact root using
  existing second-serious run and aggregation machinery.
- Phase 3. Stage 3: Completed. Per-threshold second-serious evidence is
  preserved under `threshold_runs/<threshold-label>/`, including run indices,
  aggregate tables, first-sustained-hit rows, paired comparison rows, lift
  tables, tower-shape tables, and timing evidence.
- Phase 3. Stage 4: Completed. Top-level frontier manifests include
  `evaluation_manifest.json`, `evaluation_budget_lock.json`,
  `evaluation_arm_manifest.json`, `threshold_frontier_policy_manifest.json`,
  `threshold_run_manifest.json`, `parent_source_manifest.json`,
  `candidate_manifest.json`, a frontier run index, and a run-family summary.

### Phase 4: Aggregation And Result Tables

- Phase 4. Stage 1: Completed. Wrote `results/threshold_arm_summary.csv`.
- Phase 4. Stage 2: Completed. Wrote `results/threshold_pair_summary.csv`,
  including speed-to-hit and post-hit margin deltas.
- Phase 4. Stage 3: Completed. Wrote `results/post_hit_margin_summary.csv`.
- Phase 4. Stage 4: Completed. Wrote
  `results/first_failure_frontier_summary.csv`.
- Phase 4. Stage 5: Completed. Wrote `results/frontier_summary.csv`,
  including highest shared passing threshold, Schema 1-only thresholds,
  recommended paired-replicate threshold, bounded claim status, and bounded
  claim text.
- Phase 4. Stage 6: Completed. Promoted tower-shape, lift success, lift
  failure, and timing evidence into frontier-level tables with threshold
  values and labels.
- Phase 4. Stage 7: Completed. Wrote `evaluation_aggregate_table.csv` and
  `evaluation_aggregate_summary.json`.

### Phase 5: Readout Source And Human-Readable Docs

- Phase 5. Stage 1: Completed. Generated repo-side `readout_source.json` with
  source artifact root, source evaluation root, budget, threshold grid,
  threshold-frontier policy, threshold-run manifest, source files, expected
  files, goal criteria, badge policy, and claim boundary.
- Phase 5. Stage 2: Completed. Implemented the docs writer and generated
  `README.md`, `result_readout.md`, `artifact_index.md`, `glossary.md`,
  `method.md`, `runbook.md`, and result readouts under `results/`.
- Phase 5. Stage 3: Completed. Generated badges for artifacts, thresholds
  tested, frontier status, highest shared threshold, Schema 1-only thresholds,
  recommended threshold, liftability semantics, lift failures, and provenance.
- Phase 5. Stage 4: Completed. The generated README includes the explicit
  protocol command:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/readout_source.json
```

  The docs writer preserves `## Clarifying Questions And Turns` on
  regeneration.

### Phase 6: CLI

- Phase 6. Stage 1: Completed. Added:

```text
uv run python -m big_boy_benchmarking.cli counterpoint threshold-frontier run
uv run python -m big_boy_benchmarking.cli counterpoint threshold-frontier summarize
```

- Phase 6. Stage 2: Completed. The run command prints JSON with status,
  threshold count, run count, pair count, budget lock, run index, candidate
  manifest, and threshold-run manifest.
- Phase 6. Stage 3: Completed. The summarize command aggregates artifacts,
  writes repo-side docs, and prints generated docs paths plus the recommended
  paired-replicate threshold.

### Phase 7: Tests

- Phase 7. Stage 1: Completed. Added:

```text
tests/environments/counterpoint/test_threshold_frontier_probe.py
```

  covering ids, threshold labels, threshold parsing, path guards, end-to-end
  artifact generation, aggregation, docs generation, and CLI dispatch.
- Phase 7. Stage 2: Completed. The integration test builds self-contained
  parent/full-training candidate fixtures and runs a reduced two-threshold
  frontier probe.
- Phase 7. Stage 3: Completed by risk. Reran existing second-serious and small
  paired replicate tests because this slice reuses and feeds those surfaces.

### Phase 8: Validation Runs

- Phase 8. Stage 1: Completed. The installed dependency satisfies the
  `state_collapser>=0.7.2` pointwise-liftability requirement used by the
  runner. The candidate source exposed the expected corrected wide candidate.
- Phase 8. Stage 2: Completed. Ran repo-resident implementation smoke:

```text
uv run python -m big_boy_benchmarking.cli counterpoint threshold-frontier run --artifact-root docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts/smoke_001 --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json --threshold-values 12.0,13.0 --candidate-cap 1 --episodes 4 --replicates 1 --locked-by foster --linearization-mode tensor_available_disabled
```

  Result:

```json
{"pair_count": 2, "run_count": 4, "status": "complete", "threshold_count": 2}
```

  Then summarized:

```text
uv run python -m big_boy_benchmarking.cli counterpoint threshold-frontier summarize --artifact-root docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts/smoke_001
```

  Result: status `complete`, generated repo-side docs, and recommended
  paired-replicate threshold `13.0`.

  Smoke interpretation: behavior is claim-blocked. The smoke used four
  episodes while the persistence rule is 4-of-5, so sustained-hit cannot be
  achieved. This validates machinery and readout generation, not frontier
  behavior.
- Phase 8. Stage 3: Deferred. The first meaningful frontier run should use the
  full six-threshold, eight-episode `v072_pointwise_frontier_001` budget from
  the gameplan. It was not run in this implementation pass because the wide
  two-threshold smoke took several minutes and the meaningful run is
  substantially larger; it should be launched as the next explicit PO-directed
  artifact run.

### Phase 9: Documentation And Repo Status

- Phase 9. Stage 1: Completed. Updated root `README.md`,
  `docs/evaluations/README.md`, and `CONTRIBUTING.md` to list the
  threshold-frontier probe, link the human-readable report, and distinguish
  implementation smoke from meaningful frontier evidence.
- Phase 9. Stage 2: Completed with bounded caveat. Verification commands:

```text
uv run ruff check src/big_boy_benchmarking/cli/main.py src/big_boy_benchmarking/environments/counterpoint/ids.py src/big_boy_benchmarking/environments/counterpoint/threshold_frontier_probe tests/environments/counterpoint/test_threshold_frontier_probe.py
```

  Result: `All checks passed!`

```text
uv run pytest tests/environments/counterpoint/test_threshold_frontier_probe.py tests/environments/counterpoint/test_second_serious_comparison.py tests/environments/counterpoint/test_small_paired_replicate_probe.py
```

  Result: `15 passed in 14.35s`.

```text
uv run python -m big_boy_benchmarking.cli validate-contracts
```

  Result:

```json
{"artifact_schema_version": "bbb.v001", "linearization_mode_count": 4, "mode_count": 7, "reserved_console_command": "bbb", "serious_learning_arm_count": 7, "smoke_ids": ["plate_support_env", "rl_counterpoint_v3"], "status": "ok", "tower_exploit_explore_available": true}
```

```text
uv run ruff check .
```

  Result: failed with 140 existing line-length errors in older counterpoint
  diagnostic modules and tests, especially fraction-sweep and noisy-rate
  full-training files. The touched threshold-frontier slice passed targeted
  lint.
- Phase 9. Stage 3: Completed. Current uncommitted branch state includes the
  expected docs updates, CLI/ids changes, new threshold-frontier package, new
  threshold-frontier tests, implementation log, and repo-resident smoke
  readout/artifacts.

## Stop Conditions Tracked

- No edits to `/Users/foster/state_collapser`.
- No edits to `counterpoint_symbolic_v001` environment semantics.
- No root TeX edits or generated TeX sidecar churn.
- Do not tune thresholds after inspecting outcomes.
- Do not overwrite the canonical second-serious comparison readout.
- Durable artifacts and human-readable readouts must stay repo-resident under
  `docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/`.
