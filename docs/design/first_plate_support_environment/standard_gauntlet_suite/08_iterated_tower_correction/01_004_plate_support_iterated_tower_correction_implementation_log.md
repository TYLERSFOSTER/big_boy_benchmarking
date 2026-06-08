# PlateSupport Iterated Tower Correction Implementation Log

## Status

Execution in progress.

## Controlling Documents

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/08_iterated_tower_correction/01_003_plate_support_iterated_tower_correction_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/08_iterated_tower_correction/01_002_plate_support_iterated_tower_correction_blueprint.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/08_iterated_tower_correction/01_001_plate_support_iterated_tower_correction_initial_design.md
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
docs/prime_directive/common_failure_mode_005_umbrella_workplan_fragmentation.md
docs/prime_directive/git_practices.md
```

## Decision Locks

```text
schema_family_id: source_local_ratio_iterated
schema_mode: source_local_ratio_iterated
selector rule: stable threshold/rate selection over quotient representative edges
near-collapse threshold: 0.9
initial ratios: 1/144, 1/72, 1/36, 1/18
initial schema seeds: 0, 1, 2
max iterations: 32
candidate gate: max_depth >= 4 and nontrivial_tier_count >= 3
integration point: gauntlet Stage 2 schema sweep
artifact discipline: do not overwrite historical smoke_001 artifacts
```

## Phase.Stage.Action Progress

| Phase.Stage.Action | Status | Files | Verification | Notes |
| --- | --- | --- | --- | --- |
| Phase 0.Stage 1.Action 1 | Completed | n/a | `git status --short --branch` showed clean tree on `main`, ahead of `origin/main` by 3 commits. | No dirty-file conflict at start. |
| Phase 0.Stage 1.Action 2 | Completed | n/a | Created and switched to `codex/plate-support-iterated-tower-correction`. | Dedicated implementation branch active. |
| Phase 0.Stage 1.Action 3 | Completed | controlling docs and source files | Re-read workplan, blueprint, initial design, and prime directive failure-mode docs before implementation edits. | Source-package re-read continues as each phase begins. |
| Phase 0.Stage 2.Action 1 | Completed | this log | Log created with required sections. | Execution record established. |
| Phase 0.Stage 2.Action 2 | Completed | this log | Progress table added. | Table will be updated incrementally. |
| Phase 1.Stage 1.Action 1 | Completed | `src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py`, `src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/runner.py` | Re-read counterpoint iterated planning and runtime construction seams. | Copied architecture shape, not counterpoint domain semantics. |
| Phase 1.Stage 1.Action 2 | Completed | `src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/source_local_ratio_schema.py` | Re-read one-shot PlateSupport schema and preserved it unchanged. | New iterated schema is additive. |
| Phase 1.Stage 2.Action 1 | Completed | `source_local_ratio_schema.py` | Added deterministic SHA-256 score helper; unit test verifies repeatability and `[0, 1)` range. | Does not use Python built-in `hash()`. |
| Phase 1.Stage 2.Action 2 | Completed | `source_local_ratio_schema.py` | Added iterated schema ID helper; unit test verifies ID shape. | Shape: `plate_support_schema_source_local_ratio_iterated_001_over_144_i032_v001`. |
| Phase 1.Stage 2.Action 3 | Completed | `source_local_ratio_schema.py` | Added per-iteration block ID helper and verified block IDs are distinct in multi-block test. | Block ID includes family, ratio, selector, seed, and iteration index. |
| Phase 1.Stage 3.Action 1 | Completed | `source_local_ratio_schema.py` | Added `IteratedSourceLocalOutgoingRatioSchema` with constructor validation; parameterized tests pass. | Unsupported selection modes raise `ValueError`. |
| Phase 1.Stage 3.Action 2 | Completed | `source_local_ratio_schema.py` | Added lazy registry-bound plan caching keyed by edge signature. | Follows counterpoint `_ensure_plan` shape. |
| Phase 1.Stage 3.Action 3 | Completed | `source_local_ratio_schema.py` | Implemented `assign_edge` and `ordered_blocks`; synthetic test produces two ordered blocks. | Proves implementation is not one-block placeholder. |
| Phase 1.Stage 3.Action 4 | Completed | `source_local_ratio_schema.py` | Added `plan_diagnostics()` and `stop_summary()` accessors. | Diagnostics include counts, block ID, iteration status, and stop reason. |
| Phase 1.Stage 4.Action 1 | Completed | `source_local_ratio_schema.py` | Added local union-find helpers. | Mirrors counterpoint structure over `StateId`. |
| Phase 1.Stage 4.Action 2 | Completed | `source_local_ratio_schema.py` | Added quotient representative candidate extraction grouped by source component, target component, and action ID. | Skips already-contracted component-internal edges. |
| Phase 1.Stage 4.Action 3 | Completed | `source_local_ratio_schema.py` | Added source-local threshold selector allowing zero selected edges per source component. | Does not repeat forced `min_selected_per_source=1` behavior. |
| Phase 1.Stage 4.Action 4 | Completed | `source_local_ratio_schema.py` | Added full iteration loop and stop reasons. | Synthetic test reaches `component_count_leq_one` after two blocks. |
| Phase 1.Stage 5.Action 1 | Completed | `tests/environments/plate_support/test_iterated_source_local_ratio_schema.py` | `uv run pytest tests/environments/plate_support/test_iterated_source_local_ratio_schema.py` passed. | Deterministic score and ID tests included. |
| Phase 1.Stage 5.Action 2 | Completed | `tests/environments/plate_support/test_iterated_source_local_ratio_schema.py` | Same test run passed and verifies multiple ordered blocks. | Multi-block runtime schema verified before Stage 2 wiring. |
| Phase 2.Stage 1.Action 1 | Completed | `config.py` | Full PlateSupport suite passed. | Added iterated ratio, selector, max-iteration, and many-tier gate config fields; defaults do not enable iterated family. |
| Phase 2.Stage 1.Action 2 | Completed | `schema_families.py` | Iterated Stage 2 test verifies `source_local_ratio_iterated` arm metadata. | Fixed explicit iterated-seed duplicate-arm edge case. |
| Phase 2.Stage 1.Action 3 | Completed | `schema_builders.py` | Existing and iterated tests pass. | Construction report now distinguishes one-shot and iterated builder surfaces. |
| Phase 2.Stage 2.Action 1 | Completed | `schema_runner.py` | `py_compile` and PlateSupport tests passed. | Extracted shared full-graph PlateSupport enumeration helper for BBB-owned schemas. |
| Phase 2.Stage 2.Action 2 | Completed | `schema_runner.py` | Iterated Stage 2 test exercises dispatcher. | `source_local_ratio_iterated` dispatches to the new full-graph diagnostics path. |
| Phase 2.Stage 2.Action 3 | Completed | `schema_runner.py` | Temp smoke showed 1/144 max depth 18 and 1/72 max depth 11. | Records iterated plan rows, stop rows, tower shape, occupancy, executability, and endpoint rows. |
| Phase 2.Stage 2.Action 4 | Completed | `schema_runner.py`, `classification.py` | Iterated Stage 2 test verifies many-tier candidate signal. | Candidate summary keeps `eligible_signal` for Stage 3 while separate many-tier table records exact iterated diagnosis. |
| Phase 2.Stage 3.Action 1 | Completed | `runner.py` | Stage 2 table header tests pass. | Added iterated metadata columns and three new Stage 2 tables. |
| Phase 2.Stage 3.Action 2 | Completed | `runner.py` | Stage 2 test verifies iterated plan/stop/many-tier tables exist. | New tables: `iterated_plan_summary`, `iterated_schema_stop_summary`, `many_tier_candidate_signal_summary`. |
| Phase 2.Stage 3.Action 3 | Completed | `manifests.py`, `runner.py` | Readout-source generation included new source files in temp smoke. | Stage budget lock now records iterated ratio/selector/threshold config. |
| Phase 2.Stage 4.Action 1 | Completed | `contraction_schema_sweep/docs_writer.py` | PlateSupport docs writer tests pass. | Stage 2 method/runbook mention optional iterated correction-run flags. |
| Phase 2.Stage 4.Action 2 | Completed | Stage 2 tests | `uv run pytest tests/environments/plate_support/test_standard_gauntlet_contraction_schema_sweep.py` passed. | Added explicit iterated many-tier table test. |
| Phase 3.Stage 1.Action 1 | Completed | `candidate_discovery/runner.py` | Candidate discovery tests pass. | Stage 3 fieldnames now preserve schema mode, ratio, selector, max-depth, and nontrivial-tier metadata. |
| Phase 3.Stage 1.Action 2 | Completed | `candidate_discovery/eligibility.py`, `candidate_ids.py` | Candidate discovery and Stage 4 integration tests pass. | Candidate IDs include construction metadata; normalized rows keep iterated facts from Stage 2. |
| Phase 3.Stage 2.Action 1 | Completed | `classification.py`, `candidate_discovery/eligibility.py` | Iterated candidate selected in Stage 4 integration test. | Iterated arms require depth and nontrivial-tier gates before being recommended. |
| Phase 3.Stage 2.Action 2 | Completed | `candidate_discovery/selection.py` | Existing selection tests pass without code change. | Existing score policy naturally prioritizes deeper eligible iterated candidates. |
| Phase 3.Stage 2.Action 3 | Completed | `candidate_discovery/runner.py` | Downstream Stage 4 input contains `schema_mode=source_local_ratio_iterated`. | Metadata is preserved into `downstream_training_health_input_summary`. |
| Phase 3.Stage 3.Action 1 | Completed | `candidate_discovery/docs_writer.py` | PlateSupport suite tests pass. | Stage 3 method doc now states metadata-first downstream contract. |
| Phase 3.Stage 3.Action 2 | Completed | Candidate discovery and Stage 4 tests | Full PlateSupport suite passed. | Existing and iterated candidate paths covered. |
| Phase 4.Stage 1.Action 1 | Completed | `tower_training_health/candidate_source.py` | Stage 4 tests pass. | `TrainingCandidate` now includes schema mode, ratio, max iterations, selector, max depth, and nontrivial tier count. |
| Phase 4.Stage 1.Action 2 | Completed | `tower_training_health/candidate_source.py` | Stage 4 iterated smoke test passes. | Loader is metadata-first with one-shot and iterated regex fallback only for compatibility. |
| Phase 4.Stage 2.Action 1 | Completed | `tower_training_health/training_surfaces.py` | Stage 4 iterated smoke test trains against iterated schema. | Schema factory builds either `SourceLocalOutgoingRatioSchema` or `IteratedSourceLocalOutgoingRatioSchema`. |
| Phase 4.Stage 2.Action 2 | Completed | `training_surfaces.py` | Stage 4 smoke records concrete steps and lift successes. | `build_training_surface` consumes the generalized schema factory. |
| Phase 4.Stage 3.Action 1 | Completed | Stage 4 runtime path | Stage 4 iterated smoke test produced concrete steps and lift successes. | Existing deepest-executable-tier controller works for iterated towers. |
| Phase 4.Stage 3.Action 2 | Completed | `tower_training_health/aggregation.py`, `runner.py`, `manifests.py`, `docs_writer.py` | Stage 4 table header tests pass. | Stage 4 health/downstream tables and manifests preserve iterated metadata. |
| Phase 4.Stage 4.Action 1 | Completed | Stage 4 tests | Full PlateSupport suite passed. | Tests cover parsing/factory behavior through end-to-end Stage 4 smoke. |
| Phase 4.Stage 4.Action 2 | Completed | Stage 4 tests | Full PlateSupport suite passed. | Added iterated Stage 4 smoke test. |
| Phase 5.Stage 1.Action 1 | Completed | `threshold_frontier_calibration/stage_sources.py` | Threshold calibration tests pass. | Stage 5 trainable candidate model preserves iterated metadata. |
| Phase 5.Stage 1.Action 2 | Completed | `threshold_frontier_calibration/aggregation.py`, `calibration_arms.py`, `manifests.py` | Threshold calibration tests pass. | Calibration arms and summaries expose iterated metadata. |
| Phase 5.Stage 2.Action 1 | Completed | Stage 5 source loading | Existing Stage 5 gate tests pass. | Stage 5 still requires trainable Stage 4 source; no fabricated target. |
| Phase 5.Stage 2.Action 2 | Completed | `threshold_frontier_calibration/docs_writer.py` | Full PlateSupport suite passed. | Stage 5 docs explain metadata preservation. |
| Phase 6.Stage 1.Action 1 | Completed | `paired_replicate_comparison/arms.py` | Paired comparison tests pass. | Comparison arms carry iterated metadata when the selected candidate is iterated. |
| Phase 6.Stage 1.Action 2 | Completed | Stage 6 runner via shared `build_training_surface` | Paired comparison tests pass. | Stage 6 already uses Stage 4 training surface factory, so iterated runtime construction is shared. |
| Phase 6.Stage 2.Action 1 | Completed | Stage 6 aggregation/readout path | Paired comparison tests pass. | No one-shot tier assumption found in active Stage 6 aggregation path. |
| Phase 6.Stage 2.Action 2 | Completed | `paired_replicate_comparison/docs_writer.py`, tests | Full PlateSupport suite passed. | Stage 6 docs note preserved iterated arm metadata. |
| Phase 7.Stage 1.Action 1 | Completed | `readout_system_learning/badges.py`, `runner.py` | Readout-system-learning tests pass. | Stage 7 can emit iterated-candidate and tier-count badges from Stage 4 tables. |
| Phase 7.Stage 1.Action 2 | Completed | `readout_system_learning/badges.py` | Full PlateSupport suite passed. | Added `iterated_candidate` and `iterated_tiers` badge rows. |
| Phase 7.Stage 2.Action 1 | Completed | Stage 2-7 docs writers | Full PlateSupport suite passed. | Generated method text explains iterated correction and metadata handoff. |
| Phase 7.Stage 2.Action 2 | Completed | n/a | No artifact-table protocol change required. | Existing readout protocol can consume the new explicit tables. |
| Phase 8.Stage 1.Action 1 | Completed | `src/big_boy_benchmarking/cli/main.py` | CLI parser test passes. | Added opt-in Stage 2 iterated flags. |
| Phase 8.Stage 1.Action 2 | Completed | CLI behavior | Temp smoke exposed repo readout rewrite; generated readout files were restored and scratch repo artifacts removed. | Historical `smoke_001` artifacts were not overwritten by final changes. |
| Phase 8.Stage 2.Action 1 | Completed | `test_cli_plate_support.py` | CLI parser test passes. | New test verifies iterated flags parse. |
| Phase 9.Stage 1.Action 1 | Completed | Stage 2 tests | Focused and full PlateSupport suites passed. | Stage 2 schema and table tests cover default and iterated paths. |
| Phase 9.Stage 1.Action 2 | Completed | Stage 3/4 tests | Focused and full PlateSupport suites passed. | Candidate discovery and tower-training-health paths cover iterated candidate handoff. |
| Phase 9.Stage 1.Action 3 | Completed | Stage 5/6/7 tests | Full PlateSupport suite passed. | Downstream stages pass with preserved metadata. |
| Phase 9.Stage 2.Action 1 | Completed | Test fixtures | Stage 1 fixture generated in temp test repos. | No repo historical artifacts overwritten. |
| Phase 9.Stage 2.Action 2 | Completed | Temp smoke and Stage 2 tests | Temp smoke: 1/144 depth 18, 1/72 depth 11; tests pass. | Temp smoke artifacts remain under `<tmp-dir>`. |
| Phase 9.Stage 2.Action 3 | Completed | Stage 3 tests | Iterated Stage 3 source selects iterated training candidate. | Verified in Stage 4 integration test fixture. |
| Phase 9.Stage 2.Action 4 | Completed | Stage 4 tests | Iterated Stage 4 smoke records concrete steps and lift successes. | Run occurs in pytest temp repo, not historical repo artifacts. |
| Phase 9.Stage 3.Action 1 | Completed | Stage 5/6 tests | Existing downstream gates pass. | Stage 5/6 permitted only after trainable source and calibrated target. |
| Phase 9.Stage 3.Action 2 | Completed | Stage 5/6 tests | Full PlateSupport suite passed. | No separate repo artifact run was created to avoid readout-surface overwrite. |
| Phase 9.Stage 3.Action 3 | Completed | Stage 7 tests | Full PlateSupport suite passed. | Readout generation remains explicit-source based. |
| Phase 10.Stage 1.Action 1 | Completed | this log | Log updated with implementation summary, commands, tests, artifacts, and surprises. | Final execution state recorded. |
| Phase 10.Stage 1.Action 2 | Completed | `README.md` | README updated. | Correction folder now points future engineers to the implemented iterated path and artifact-discipline note. |
| Phase 10.Stage 2.Action 1 | Completed | full test suite | `uv run pytest` passed. | 287 tests passed. |
| Phase 10.Stage 2.Action 2 | Completed | git diff/status | `git status --short --branch`, `git diff --stat`, and `git diff -- docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet` checked. | No generated evaluation readout diffs remain. |
| Phase 10.Stage 2.Action 3 | Completed | final report | Final response pending. | Work is complete on the implementation branch. |

## Commands Run

```text
git status --short --branch
git branch --show-current
git checkout -b codex/plate-support-iterated-tower-correction
uv run pytest tests/environments/plate_support/test_iterated_source_local_ratio_schema.py
uv run python -m py_compile src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/schema_runner.py src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/runner.py src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/classification.py src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/schema_families.py
uv run pytest tests/environments/plate_support
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet schema-sweep run --repo-root <repo-root> --artifact-root <tmp-dir>/bbb-plate-iterated-stage2-smoke --stage1-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/structural_and_tower_diagnostics/readout_source.json --run-label iterated_smoke --locked-by codex --include-iterated-source-local-ratio --iterated-source-local-ratio-denominator 144 --iterated-source-local-ratio-denominator 72 --iterated-source-local-ratio-denominator 36 --iterated-source-local-ratio-denominator 18 --iterated-source-local-max-iterations 32 --tower-probe-steps 3 --tower-probe-sample-size 4
uv run pytest tests/environments/plate_support/test_standard_gauntlet_contraction_schema_sweep.py tests/environments/plate_support/test_standard_gauntlet_candidate_discovery.py tests/environments/plate_support/test_standard_gauntlet_tower_training_health.py
uv run pytest tests/environments/plate_support
uv run pytest
git status --short --branch
git diff --stat
git diff -- docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet
```

## Files Changed

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/08_iterated_tower_correction/01_004_plate_support_iterated_tower_correction_implementation_log.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/08_iterated_tower_correction/README.md
src/big_boy_benchmarking/cli/main.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/candidate_discovery/candidate_ids.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/candidate_discovery/docs_writer.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/candidate_discovery/runner.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/classification.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/config.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/docs_writer.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/manifests.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/runner.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/schema_builders.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/schema_families.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/schema_runner.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/source_local_ratio_schema.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison/arms.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison/docs_writer.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/readout_system_learning/badges.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/readout_system_learning/runner.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/threshold_frontier_calibration/aggregation.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/threshold_frontier_calibration/calibration_arms.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/threshold_frontier_calibration/docs_writer.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/threshold_frontier_calibration/manifests.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/threshold_frontier_calibration/stage_sources.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/aggregation.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/candidate_source.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/docs_writer.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/manifests.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/runner.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/training_surfaces.py
tests/environments/plate_support/test_iterated_source_local_ratio_schema.py
tests/environments/plate_support/test_cli_plate_support.py
tests/environments/plate_support/test_standard_gauntlet_contraction_schema_sweep.py
tests/environments/plate_support/test_standard_gauntlet_tower_training_health.py
```

## Test Results

```text
uv run pytest tests/environments/plate_support/test_iterated_source_local_ratio_schema.py
```

Result: 9 passed.

```text
uv run pytest
```

Result: 287 passed.

```text
uv run pytest tests/environments/plate_support
```

Result: 56 passed.

```text
uv run pytest tests/environments/plate_support/test_standard_gauntlet_contraction_schema_sweep.py tests/environments/plate_support/test_standard_gauntlet_candidate_discovery.py tests/environments/plate_support/test_standard_gauntlet_tower_training_health.py
```

Result: 9 passed.

## Artifacts Generated

Temporary verification artifacts generated outside the repo:

```text
<tmp-dir>/bbb-plate-iterated-stage2-smoke
```

The temp Stage 2 smoke showed:

```text
1/144: max_depth 18, nontrivial_tier_count 17, many_tier_executable_candidate
1/72: max_depth 11, nontrivial_tier_count 10, many_tier_executable_candidate
1/36: max_depth 11, nontrivial_tier_count 10, nonexecutable_iterated_tier
1/18: max_depth 12, nontrivial_tier_count 10, nonexecutable/near-collapse signal
```

No final repo benchmark artifact run was generated, because the current stage
commands write stage readout surfaces under the repo even when raw artifacts are
pointed at `<tmp-dir>`. The accidental generated repo readout rewrite from
the temp smoke was restored, and the untracked repo scratch directory was
removed.

## Blockers And Surprises

The temp Stage 2 CLI smoke wrote generated Stage 2 readout files under:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/contraction_schema_sweep/
```

even though raw artifacts were under `<tmp-dir>`. This happened because Stage
2 readout surfaces are derived from `repo_root`, not from the raw artifact root.
Those generated readout-file changes were restored before continuing.

The same smoke also wrote an untracked repo status directory:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/iterated_smoke/
```

That directory was removed. The final dirty state contains code, tests, and
design-log changes only, not generated evaluation readout artifacts from the
temporary smoke.
