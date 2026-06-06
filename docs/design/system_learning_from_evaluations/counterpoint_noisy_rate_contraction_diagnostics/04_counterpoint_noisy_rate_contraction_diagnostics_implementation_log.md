# Counterpoint Noisy-Rate Contraction Diagnostics Implementation Log

Date started: 2026-06-01 19:02:13 EDT

Branch:

```text
codex/noisy-rate-contraction-diagnostics
```

Source workplan:

```text
docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/03_counterpoint_noisy_rate_contraction_diagnostics_implementation_workplan.md
```

Initial `git status --short --branch` after branch creation:

```text
## codex/noisy-rate-contraction-diagnostics
 M docs/design/system_learning_from_evaluations/README.md
 M docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/README.md
?? docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/
```

Initial dirty-state note:

The dirty files above were created during the immediately preceding noisy-rate
design and readout-conversation work. They are related to this implementation
thread and were carried onto the implementation branch. No unrelated dirty
files were observed before branch creation.

## Stop Conditions

Stop and ask the Project Owner if:

- explicit approval to execute this exact workplan has not been received;
- branch or dirty status would mix unrelated work into this implementation;
- any action would require editing `/Users/foster/state_collapser`;
- any action would alter `counterpoint_symbolic_v001` environment semantics;
- the noisy selector cannot be implemented without a source-local minimum-one
  floor;
- metadata-selected and runtime-selected edge sets cannot be reconciled;
- coupled-rate monotonicity fails;
- source coverage cannot be summarized;
- active action-cell counts cannot be distinguished from stale historical
  action-cell records;
- a required evaluation-level table would be omitted without expected-file
  policy;
- artifact roots would need to live outside the repo readout surface for a
  durable evaluation run;
- exact implementation of any Phase.Stage.Action would require a weaker
  substitute, hidden simplification, or unapproved reordering;
- implementation pressure starts turning this diagnostic into a learning
  comparison.

## Initial Phase.Stage.Action Checklist

- Phase 0. Stage 0. Action 1: completed. Execution authority confirmed by PO request to execute this workplan.
- Phase 0. Stage 0. Action 2: completed. Working tree inspected; dirty files are related noisy-rate design/readout docs from the preceding design interval.
- Phase 0. Stage 0. Action 3: completed. Created and switched to `codex/noisy-rate-contraction-diagnostics`.
- Phase 0. Stage 0. Action 4: completed. Created this implementation log.
- Phase 0. Stage 1. Action 1: in progress.
- Phase 0. Stage 1. Action 2: pending.
- Phase 1. Stage 1. Action 1: pending.
- Phase 1. Stage 1. Action 2: pending.
- Phase 1. Stage 1. Action 3: pending.
- Phase 1. Stage 1. Action 4: pending.
- Phase 1. Stage 1. Action 5: pending.
- Phase 1. Stage 1. Action 6: pending.
- Phase 1. Stage 1. Action 7: pending.
- Phase 1. Stage 2. Action 1: pending.
- Phase 1. Stage 2. Action 2: pending.
- Phase 1. Stage 2. Action 3: pending.
- Phase 1. Stage 3. Action 1: pending.
- Phase 1. Stage 3. Action 2: pending.
- Phase 2. Stage 1. Action 1: pending.
- Phase 2. Stage 1. Action 2: pending.
- Phase 2. Stage 1. Action 3: pending.
- Phase 2. Stage 2. Action 1: pending.
- Phase 2. Stage 2. Action 2: pending.
- Phase 2. Stage 2. Action 3: pending.
- Phase 2. Stage 3. Action 1: pending.
- Phase 2. Stage 3. Action 2: pending.
- Phase 3. Stage 1. Action 1: pending.
- Phase 3. Stage 1. Action 2: pending.
- Phase 3. Stage 1. Action 3: pending.
- Phase 3. Stage 2. Action 1: pending.
- Phase 3. Stage 2. Action 2: pending.
- Phase 3. Stage 2. Action 3: pending.
- Phase 4. Stage 1. Action 1: pending.
- Phase 4. Stage 1. Action 2: pending.
- Phase 4. Stage 1. Action 3: pending.
- Phase 4. Stage 1. Action 4: pending.
- Phase 4. Stage 1. Action 5: pending.
- Phase 4. Stage 1. Action 6: pending.
- Phase 4. Stage 1. Action 7: pending.
- Phase 4. Stage 2. Action 1: pending.
- Phase 4. Stage 2. Action 2: pending.
- Phase 5. Stage 1. Action 1: pending.
- Phase 5. Stage 1. Action 2: pending.
- Phase 5. Stage 1. Action 3: pending.
- Phase 6. Stage 1. Action 1: pending.
- Phase 6. Stage 1. Action 2: pending.
- Phase 6. Stage 1. Action 3: pending.
- Phase 6. Stage 1. Action 4: pending.
- Phase 6. Stage 2. Action 1: pending.
- Phase 6. Stage 2. Action 2: pending.
- Phase 6. Stage 3. Action 1: pending.
- Phase 6. Stage 3. Action 2: pending.
- Phase 7. Stage 1. Action 1: pending.
- Phase 7. Stage 1. Action 2: pending.
- Phase 7. Stage 1. Action 3: pending.
- Phase 7. Stage 2. Action 1: pending.
- Phase 8. Stage 1. Action 1: pending.
- Phase 8. Stage 1. Action 2: pending decision lock.
- Phase 8. Stage 1. Action 3: pending decision lock.
- Phase 8. Stage 1. Action 4: pending decision lock.
- Phase 9. Stage 1. Action 1: pending.
- Phase 9. Stage 1. Action 2: pending.
- Phase 9. Stage 1. Action 3: pending.

## Running Notes

- No implementation source edits have been made at log creation time.
- Planned implementation source edits are expected in `ids.py`, `schemas.py`,
  `tower_adapter.py`, a new `noisy_rate_diagnostics/` package, `cli/main.py`,
  and focused tests.

## Completion Update

Date updated: 2026-06-01

The implementation proceeded on branch:

```text
codex/noisy-rate-contraction-diagnostics
```

No `/Users/foster/state_collapser` files were edited.

No `counterpoint_symbolic_v001` environment semantics were changed. The new
work is a sibling evaluation and selector/schema family.

### Completed Phase.Stage.Action Items

- Phase 0. Stage 1. Action 1: completed. Re-read source authority and prime-directive failure-mode documents before source edits.
- Phase 0. Stage 1. Action 2: completed. Mapped reusable surfaces in ids, schemas, tower adapter, fraction sweep diagnostics, one-third diagnostics, CLI, and tests.
- Phase 1. Stage 1. Action 1: completed. Added noisy-rate evaluation/schema ids in `src/big_boy_benchmarking/environments/counterpoint/ids.py`.
- Phase 1. Stage 1. Action 2: completed. Added explicit rate parsing and `pNNN_over_DDD` arm helpers in the noisy-rate package config.
- Phase 1. Stage 1. Action 3: completed. Added SHA-256 stable edge score helper in `schemas.py`.
- Phase 1. Stage 1. Action 4: completed. Added metadata noisy-rate selected-edge helpers in `schemas.py`.
- Phase 1. Stage 1. Action 5: completed. Added source-coverage report helper in `schemas.py`.
- Phase 1. Stage 1. Action 6: completed. Added coupled-rate monotonicity report helper in `schemas.py`.
- Phase 1. Stage 1. Action 7: completed. Added metadata/runtime selection consistency helper and hard consistency check in the runner.
- Phase 1. Stage 2. Action 1: completed. Added `CounterpointNoisyRateSchema` in `tower_adapter.py`.
- Phase 1. Stage 2. Action 2: completed. Added `build_counterpoint_noisy_rate_partition_tower`.
- Phase 1. Stage 2. Action 3: completed. Existing schema regression tests passed.
- Phase 1. Stage 3. Action 1: completed. Reused endpoint-coalescence logic in noisy-rate runner with noisy-rate fields.
- Phase 1. Stage 3. Action 2: completed. Reused active action-cell counting and kept it separate from raw historical action records.
- Phase 2. Stage 1. Action 1: completed. Added `src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/`.
- Phase 2. Stage 1. Action 2: completed. Added noisy-rate config, defaults, smoke rates, selector rule id, and budget lock.
- Phase 2. Stage 1. Action 3: completed. Added path helpers for `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/`.
- Phase 2. Stage 2. Action 1: completed. Added typed row models for noisy-rate selection, source coverage, consistency, monotonicity, threshold, tower/runtime summaries, aggregate table, and run index.
- Phase 2. Stage 2. Action 2: completed. Added manifests and `readout_source.json` source binding builder.
- Phase 2. Stage 2. Action 3: completed. Added expected-file policy for noisy-rate-specific result tables.
- Phase 2. Stage 3. Action 1: completed. Added docs seed writer for README, method, runbook, artifact index, glossary, summary, thresholds, source coverage, and badges.
- Phase 2. Stage 3. Action 2: completed. Added badge inputs and generated badges in the repo readout surface.
- Phase 3. Stage 1. Action 1: completed. Implemented run enumeration over instances, rates, schema seeds, replicates, and episodes with no-contraction control.
- Phase 3. Stage 1. Action 2: completed. Implemented tower build per noisy-rate arm and no-contraction control.
- Phase 3. Stage 1. Action 3: completed. Emitted per-run structural summaries for selection, coverage, consistency, monotonicity, tower shape, active/raw action counts, and endpoint coalescence.
- Phase 3. Stage 2. Action 1: completed. Reused the existing active-tier counterpoint control path.
- Phase 3. Stage 2. Action 2: completed. Recorded control and ABC selection/tier-signal rows.
- Phase 3. Stage 2. Action 3: completed. Recorded lift and concrete step evidence.
- Phase 4. Stage 1. Action 1: completed. Implemented aggregation to evaluation-level tables.
- Phase 4. Stage 1. Action 2: completed. Wrote `results/noisy_rate_selection_summary.csv`.
- Phase 4. Stage 1. Action 3: completed. Wrote `results/noisy_rate_source_coverage_summary.csv`.
- Phase 4. Stage 1. Action 4: completed. Wrote `results/noisy_rate_selection_consistency_summary.csv`.
- Phase 4. Stage 1. Action 5: completed. Wrote `results/noisy_rate_monotonicity_summary.csv`.
- Phase 4. Stage 1. Action 6: completed. Wrote `results/noisy_rate_threshold_summary.csv`.
- Phase 4. Stage 1. Action 7: completed. Implemented sweep verdict classification.
- Phase 4. Stage 2. Action 1: completed. Generated repo readout surface.
- Phase 4. Stage 2. Action 2: completed. Generated readout interpretation text for expected rate, source coverage, zero-selected sources, active action-cell counts, and claim boundaries.
- Phase 5. Stage 1. Action 1: completed. Added `counterpoint noisy-rate run`.
- Phase 5. Stage 1. Action 2: completed. Added `counterpoint noisy-rate summarize`.
- Phase 5. Stage 1. Action 3: skipped deliberately. A separate lightweight diagnostic command was not added; the run/summarize path and unit tests cover the selector surfaces without adding CLI scope.
- Phase 6. Stage 1. Action 1: completed. Added selector tests.
- Phase 6. Stage 1. Action 2: completed. Added metadata/runtime consistency test.
- Phase 6. Stage 1. Action 3: completed. Added source coverage tests.
- Phase 6. Stage 1. Action 4: completed. Added endpoint-coalescence regression test.
- Phase 6. Stage 2. Action 1: completed. Added artifact contract tests.
- Phase 6. Stage 2. Action 2: completed. Added CLI smoke tests.
- Phase 6. Stage 3. Action 1: completed. Targeted noisy-rate tests passed.
- Phase 6. Stage 3. Action 2: completed. Counterpoint regression tests passed.
- Phase 7. Stage 1. Action 1: completed. Smoke artifact run produced 12 successful runs under the repo readout surface.
- Phase 7. Stage 1. Action 2: completed. Smoke artifacts summarized successfully.
- Phase 7. Stage 1. Action 3: completed. Human-readable readout surface generated from the repo-side `readout_source.json`.
- Phase 7. Stage 2. Action 1: completed. Generated smoke README and supporting docs were reviewed for artifact-root confusion, source coverage, zero-selected-source language, active action-cell language, and claim boundaries.
- Phase 8. Stage 1. Action 1: completed as a decision lock. Full validation was not run because Project Owner authorization for the full small+medium validation budget has not been given in this execution turn.
- Phase 8. Stage 1. Action 2: pending PO authorization.
- Phase 8. Stage 1. Action 3: pending PO authorization.
- Phase 8. Stage 1. Action 4: pending PO authorization.
- Phase 9. Stage 1. Action 1: completed. Updated design archive status and top-level system-learning index.
- Phase 9. Stage 1. Action 2: completed. Final compile, targeted noisy-rate tests, and `git diff --check` passed.

### Files Changed Or Added

- `src/big_boy_benchmarking/environments/counterpoint/ids.py`
- `src/big_boy_benchmarking/environments/counterpoint/schemas.py`
- `src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py`
- `src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/`
- `src/big_boy_benchmarking/cli/main.py`
- `tests/environments/counterpoint/test_noisy_rate_diagnostics.py`
- `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/README.md`
- `docs/design/system_learning_from_evaluations/README.md`

### Commands Run

```text
uv run python -m compileall src/big_boy_benchmarking/environments/counterpoint src/big_boy_benchmarking/cli/main.py
uv run pytest tests/environments/counterpoint/test_noisy_rate_diagnostics.py
uv run pytest tests/environments/counterpoint/test_schemas.py tests/environments/counterpoint/test_tower_adapter.py tests/environments/counterpoint/test_one_third_diagnostics.py tests/environments/counterpoint/test_fraction_sweep_diagnostics.py tests/environments/counterpoint/test_noisy_rate_diagnostics.py
uv run pytest tests/cli/test_cli.py
uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate run --artifact-root /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/artifacts/smoke_001 --instances small --rates 1/144,1/36,1/18 --schema-seeds 0,1,2 --replicates 1 --episodes 1 --controller-event-ceiling 8 --locked-by codex
uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate summarize --artifact-root /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/artifacts/smoke_001
```

### Test Results

- `uv run python -m compileall ...`: passed after one typo fix in the endpoint-coalescence helper.
- `uv run pytest tests/environments/counterpoint/test_noisy_rate_diagnostics.py`: passed, 10 tests.
- Counterpoint regression set: passed, 35 tests.
- `uv run pytest tests/cli/test_cli.py`: passed, 7 tests.
- Final verification after smoke regeneration: `uv run python -m compileall ...` passed, `uv run pytest tests/environments/counterpoint/test_noisy_rate_diagnostics.py` passed with 10 tests, and `git diff --check` passed.

### Smoke Artifact Result

Smoke artifact root:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/artifacts/smoke_001/
```

Run shape:

- instance: `small`
- rates: `1/144,1/36,1/18`
- schema seeds: `0,1,2`
- replicates: `1`
- episodes: `1`
- no-contraction control: included
- linearization mode: `tensor_available_disabled`

Run result:

```text
run_count: 12
status: complete
```

Summarize result:

```text
status: complete
```

Generated readout source:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json
```

### Surprises And Fixes

- The copied runner initially still carried source-local fraction concepts. The final implementation replaced them with explicit noisy-rate arms and noisy-rate result tables.
- The first compile pass found a typo in the endpoint-coalescence helper; it was fixed before tests.
- The first targeted test pass found a docs-writer comprehension bug; it was fixed.
- The first CLI smoke test found a `RateSpec`/tuple mismatch in monotonicity context construction; it was fixed.
- A later review noticed that monotonicity rows should reflect the configured run rates rather than the full default grid during smoke runs. The budget rates were threaded into per-run monotonicity summaries, a wiring mistake was corrected, targeted tests were rerun, and the repo smoke artifacts/readout were regenerated successfully.
- No metadata/runtime selected-edge mismatch occurred after the runtime canonical edge mapping was implemented.

### Remaining Decision

Full small+medium validation remains intentionally unrun until the Project Owner
explicitly authorizes the Phase 8 full artifact budget.
