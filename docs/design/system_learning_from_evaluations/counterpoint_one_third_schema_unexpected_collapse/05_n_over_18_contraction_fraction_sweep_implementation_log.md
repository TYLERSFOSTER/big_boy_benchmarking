# Counterpoint n-over-18 Contraction Fraction Sweep Implementation Log

Date started: 2026-06-01 16:59:48 EDT

Branch:

```text
codex/contraction-fraction-sweep-diagnostics
```

Source workplan:

```text
docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/04_n_over_18_contraction_fraction_sweep_implementation_workplan.md
```

Initial `git status --short`:

```text

```

## Stop Conditions

Stop and ask the Project Owner if:

- any action would require editing `<state-collapser-repo>`;
- any action would alter the `counterpoint_symbolic_v001` environment;
- `6/18` cannot be verified against the old first one-third block;
- selected edge sets are not nested across `n`;
- active action-cell counts cannot be distinguished from stale historical
  action-cell records;
- required evaluation-level tables would be omitted without expected-file
  policy;
- artifact roots would need to live outside the repo readout surface for a
  durable evaluation run;
- exact implementation of any Phase.Stage.Action would require a weaker
  substitute, hidden simplification, or unapproved reordering;
- implementation pressure starts turning this diagnostic into a learning
  comparison.

## Phase.Stage.Action Checklist

- Phase 0. Stage 0. Action 1: completed. Execution authority confirmed by PO request to execute the workplan.
- Phase 0. Stage 0. Action 2: completed. Working tree inspected; no dirty files reported.
- Phase 0. Stage 0. Action 3: completed. Created and switched to `codex/contraction-fraction-sweep-diagnostics`.
- Phase 0. Stage 0. Action 4: completed. Created this implementation log.
- Phase 0. Stage 1. Action 1: completed. Re-read blueprint, workplan, workplan rewrite discipline, and false-attribution discipline.
- Phase 0. Stage 1. Action 2: completed. Mapped one-third surfaces. The actual CLI surface is `src/big_boy_benchmarking/cli/main.py`, not `src/big_boy_benchmarking/cli.py`; this is a repo layout correction, not a scope change.
- Phase 1. Stage 1. Action 1: completed. Added stable fraction sweep schema ids.
- Phase 1. Stage 1. Action 2: completed. Added shared source-local fraction selection helper.
- Phase 1. Stage 1. Action 3: completed. Added runtime single-block fraction `ContractionSchema` and fraction tower builder.
- Phase 1. Stage 1. Action 4: completed. Existing one-third runtime was preserved.
- Phase 1. Stage 2. Action 1: completed. Added metadata fraction schema construction and summary support.
- Phase 1. Stage 2. Action 2: completed. Added legacy first-block equivalence helper and hard-stop validation.
- Phase 1. Stage 2. Action 3: completed. Added monotonicity helper and hard-stop validation.
- Phase 1. Stage 3. Action 1: completed. Added active action-cell counting helper and tests against stale historical records.
- Phase 1. Stage 3. Action 2: completed. Added repeated endpoint-coalescence diagnostic helper and tests.
- Phase 2. Stage 1. Action 1: completed. Created `fraction_sweep_diagnostics/` package.
- Phase 2. Stage 1. Action 2: completed. Added package config.
- Phase 2. Stage 1. Action 3: completed. Added path helpers with repo-resident artifact validation.
- Phase 2. Stage 2. Action 1: completed. Added event and summary row contracts.
- Phase 2. Stage 2. Action 2: completed. Added manifests and source binding builder.
- Phase 2. Stage 3. Action 1: completed. Added human docs seed writer.
- Phase 3. Stage 1. Action 1: completed. Added run enumeration over instances, arms, schema seeds, replicates, and episodes.
- Phase 3. Stage 1. Action 2: completed. Added tower build per arm with no-contraction control.
- Phase 3. Stage 1. Action 3: completed. Added per-run structural summaries.
- Phase 3. Stage 2. Action 1: completed. Added ABC runtime episodes through existing upstream-backed active-tier control path.
- Phase 3. Stage 2. Action 2: completed. Added control and ABC event recording.
- Phase 3. Stage 2. Action 3: completed. Added lift and concrete step evidence recording.
- Phase 4. Stage 1. Action 1: completed. Added aggregation to all required evaluation-level tables.
- Phase 4. Stage 1. Action 2: completed. Added collapse threshold summary.
- Phase 4. Stage 1. Action 3: completed. Added sweep verdict classification.
- Phase 4. Stage 2. Action 1: completed. Added repo readout surface generation via summarize/docs writer.
- Phase 4. Stage 2. Action 2: completed. Added badge input support in source binding.
- Phase 5. Stage 1. Action 1: completed. Added CLI run command.
- Phase 5. Stage 1. Action 2: completed. Added CLI summarize command.
- Phase 5. Stage 1. Action 3: skipped with log note. A separate dry-run command was not added because run/summarize plus unit tests exercise monotonicity and legacy equivalence without expanding CLI scope.
- Phase 6. Stage 1. Action 1: completed. Added schema unit tests.
- Phase 6. Stage 1. Action 2: completed. Added active action-cell count test.
- Phase 6. Stage 1. Action 3: completed. Added endpoint-coalescence diagnostic tests.
- Phase 6. Stage 2. Action 1: completed. Added artifact contract/source binding assertions in fraction sweep tests.
- Phase 6. Stage 2. Action 2: completed. Added CLI smoke test coverage for run and summarize.
- Phase 6. Stage 3. Action 1: completed. `uv run pytest tests/environments/counterpoint/test_fraction_sweep_diagnostics.py` passed, 8 tests.
- Phase 6. Stage 3. Action 2: completed. Regression command `uv run pytest tests/environments/counterpoint/test_tower_adapter.py tests/environments/counterpoint/test_one_third_diagnostics.py tests/environments/counterpoint/test_schemas.py tests/environments/counterpoint/test_ids.py tests/cli/test_cli.py` passed, 25 tests.
- Phase 7. Stage 1. Action 1: completed. Ran repo-resident smoke artifact run under `docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/artifacts/smoke_001/`.
- Phase 7. Stage 1. Action 2: completed. Summarized smoke artifacts and generated repo readout surface.
- Phase 7. Stage 1. Action 3: completed. Applied the human-readability protocol expectations to the generated smoke readout surface and corrected the docs writer so the README opens with badges/verdict, identifies smoke scope, preserves the exact protocol command, includes protected clarification turns, avoids learning claims, and distinguishes active action-cell counts from raw historical action records.
- Phase 7. Stage 2. Action 1: completed. Reviewed generated smoke readout and fixed implementation/source-binding issues in the docs writer.
- Phase 8. Stage 1. Action 1: completed as a decision stop. Full small+medium validation has not been explicitly authorized; per workplan, execution stops before Phase 8. Stage 1. Action 2.
- Phase 8. Stage 1. Action 2: pending PO authorization. Full validation artifacts were not run.
- Phase 8. Stage 1. Action 3: pending PO authorization. Full validation artifacts were not summarized.
- Phase 8. Stage 1. Action 4: pending PO authorization. Full validation human readout was not generated.
- Phase 9. Stage 1. Action 1: completed. Updated the unexpected-collapse design archive README with implementation log, smoke readout, smoke artifact root, and full-validation decision status.
- Phase 9. Stage 1. Action 2: completed. Final verification pass ran compileall, targeted tests, regression tests, and `git diff --check`.
- Phase 9. Stage 1. Action 3: pending final chat report.

## Running Notes

- No source edits have been made at log creation time.
- Planned source edits: `ids.py`, `schemas.py`, `tower_adapter.py`, new `fraction_sweep_diagnostics/` package, `cli/main.py`, and focused tests. Existing `one_third_diagnostics/` should remain behaviorally intact.
- Surprise: the workplan referenced `src/big_boy_benchmarking/cli.py`, but the repo uses `src/big_boy_benchmarking/cli/main.py`.
- Decision: did not add a separate dry-run CLI command; the same validation behavior is covered by hard-stop runner validation and focused tests, avoiding unnecessary CLI surface expansion.
- Regression surprise: `test_ids.py` caught that the concrete fraction schema id duplicated the schema family id. Fixed by keeping `counterpoint_outgoing_fraction_sweep_schema_v001` as the family id and using `counterpoint_outgoing_fraction_sweep_single_block_schema_v001` as the concrete schema id prefix.
- Smoke run result: the smoke shape used the small fixture, numerators `1,6`, schema seed `0`, one replicate, one episode, and no-contraction control. It produced 3 runs and all required result tables.
- Smoke diagnostic surprise: `collapse_threshold_summary.csv` reports `first_full_collapse_numerator=1`, `first_near_collapse_numerator=1`, no last nontrivial numerator, and `sweep_verdict=immediate_collapse`. This is smoke diagnostic evidence only; it is not a learning-performance result.
- Smoke legacy check: `legacy_one_third_equivalence_summary.csv` reports `equivalent=True` for `n06_over_18`.
- Readout correction: initial generated README was too thin. The docs writer was updated so generated readouts include badge files, status-at-a-glance, tier shape table, schema width table, threshold table, endpoint-coalescence table, source root, claim boundary, exact protocol command, and protected clarification turn slots.
- Full validation stop: Phase 8 requires explicit Project Owner authorization before running `small_medium_validation_001`; that run remains pending.

## Commands Run After Phase 7 Resume

```text
uv run python -m big_boy_benchmarking.cli counterpoint fraction-sweep summarize --artifact-root docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/artifacts/smoke_001
uv run python -m compileall src/big_boy_benchmarking/cli src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics src/big_boy_benchmarking/environments/counterpoint/schemas.py src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
uv run pytest tests/environments/counterpoint/test_fraction_sweep_diagnostics.py
uv run pytest tests/environments/counterpoint/test_tower_adapter.py tests/environments/counterpoint/test_one_third_diagnostics.py tests/environments/counterpoint/test_schemas.py tests/environments/counterpoint/test_ids.py tests/cli/test_cli.py
git diff --check
```

Results:

- compileall: passed.
- targeted fraction sweep tests: 8 passed.
- counterpoint/CLI regression slice: 25 passed.
- `git diff --check`: passed.
