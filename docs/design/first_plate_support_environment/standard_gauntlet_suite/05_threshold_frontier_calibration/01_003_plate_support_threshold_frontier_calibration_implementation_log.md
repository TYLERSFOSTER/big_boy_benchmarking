# PlateSupport Threshold Frontier Calibration Implementation Log

## Status

Status: in progress.

This log records execution of:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/05_threshold_frontier_calibration/01_002_plate_support_threshold_frontier_calibration_implementation_workplan.md
```

The current resume point was supplied by the Project Owner as Stage 5 of the
PlateSupport standard gauntlet. Stages 1-4 already have repo-local artifacts;
Stage 5 must consume Stage 1 structural facts and Stage 4 tower-training-health
traces, then either write a table-backed target recommendation or block without
inventing a threshold.

## Phase.Stage.Action Progress

| Phase.Stage.Action | Status | Notes |
| --- | --- | --- |
| Phase 0.Stage 1.Action 1 | complete | Verified repo state before Stage 5 edits. Branch is `main`; repo is ahead of `origin/main` and contains dirty Stage 2-4/code/readout work. These files are treated as existing work, not reverted or overwritten. |
| Phase 0.Stage 1.Action 2 | complete | Verified Stage 1 readout source and required structural/reward tables exist. Verified Stage 4 readout source and training-health tables exist. |
| Phase 0.Stage 1.Action 3 | complete | Stage 4 has one `trainable_clean` candidate: `plate_support_candidate:source_local_ratio:0:342448ef2e`. |
| Phase 0.Stage 2.Action 1 | complete | Created this Stage 5 implementation log before source edits. |
| Phase 0.Stage 2.Action 2 | complete | Recorded Stage 1 and Stage 4 source paths below. |
| Phase 1.Stage 1.Action 1 | complete | Created Stage 5 package under `threshold_frontier_calibration/`. |
| Phase 1.Stage 1.Action 2 | complete | Added module initializer exporting config and runner. |
| Phase 1.Stage 2.Action 1 | complete | Implemented `ThresholdFrontierCalibrationConfig` with explicit source, candidate cap, target types, sustained windows, threshold quantiles, and recommended Stage 6 budget fields. |
| Phase 1.Stage 2.Action 2 | complete | `stage_budget_lock.json` records arms, target types, window policy, threshold-grid policy, and recommended budget. |
| Phase 2.Stage 1.Action 1 | complete | Implemented Stage 4 source loader with repo-bound path validation. |
| Phase 2.Stage 1.Action 2 | complete | Stage 4 loader validates required table columns before calibration. |
| Phase 2.Stage 2.Action 1 | complete | Stage 1 loader resolves shortest path, random policy, state space, and transition facts from tables. |
| Phase 3.Stage 1.Action 1 | complete | Selected trainable candidate calibration arm is built from Stage 4 health rows. |
| Phase 3.Stage 1.Action 2 | complete | Baseline arm is opt-in and explicitly blocked in this smoke path rather than silently invented. |
| Phase 3.Stage 2.Action 1 | complete | Stage 4 traces are reused as calibration traces because they have table-backed hit/miss variation. |
| Phase 3.Stage 2.Action 2 | complete | No additional calibration arms were required for the Stage 5 smoke target calibration. |
| Phase 4.Stage 1.Action 1 | complete | Wrote `success_rate_summary.csv`. |
| Phase 4.Stage 1.Action 2 | complete | Wrote `first_hit_summary.csv`. |
| Phase 4.Stage 2.Action 1 | complete | Sustained-window feasibility rejects windows exceeding available per-replicate episodes. |
| Phase 4.Stage 2.Action 2 | complete | Wrote `sustained_hit_feasibility_summary.csv`. |
| Phase 4.Stage 3.Action 1 | complete | Wrote observed return distribution rows with Stage 1 random and shortest-path context. |
| Phase 4.Stage 3.Action 2 | complete | Wrote evidence-derived `threshold_grid_construction.csv`; no hard-coded threshold values. |
| Phase 4.Stage 3.Action 3 | complete | Wrote `threshold_frontier_summary.csv` with trivial/nontrivial feasibility classifications. |
| Phase 5.Stage 1.Action 1 | complete | Feasibility classifier prefers binary success, then first-hit, then return-threshold fallback. |
| Phase 5.Stage 1.Action 2 | complete | Selected exactly one target: `plate_support_binary_goal_success_v001`. |
| Phase 5.Stage 1.Action 3 | complete | Recommended Stage 6 budget: 32 episodes per replicate, 4 replicates per arm. |
| Phase 5.Stage 2.Action 1 | complete | Wrote `recommended_comparison_target.csv`. |
| Phase 5.Stage 2.Action 2 | complete | Wrote `downstream_paired_comparison_input_summary.csv`. |
| Phase 6.Stage 1.Action 1 | complete | Wrote Stage 5 manifests. |
| Phase 6.Stage 1.Action 2 | complete | Wrote all required result tables. |
| Phase 6.Stage 1.Action 3 | complete | Wrote `stage_aggregate_summary.json`, `stage_aggregate_table.csv`, and `stage_run_index.csv`; suite status now has a Stage 5 row. |
| Phase 6.Stage 2.Action 1 | complete | Wrote Stage 5 readout source. |
| Phase 6.Stage 2.Action 2 | complete | Wrote seed Stage 5 human docs. |
| Phase 7.Stage 1.Action 1 | complete | Added `plate-support standard-gauntlet threshold-calibration run`. |
| Phase 7.Stage 1.Action 2 | complete | Did not add summarize/inspect; current run command reports selected target and docs are protocol-readable. |
| Phase 8.Stage 1.Action 1 | complete | Added tests for missing trainable candidate gate. |
| Phase 8.Stage 1.Action 2 | complete | Added tests covering binary target selection and impossible sustained window classification. |
| Phase 8.Stage 1.Action 3 | complete | Added tests that threshold grid rows carry provenance. |
| Phase 8.Stage 1.Action 4 | complete | Added tests that downstream target table permits Stage 6 after calibration. |
| Phase 8.Stage 2.Action 1 | complete | Ran Stage 5 against repo-local Stage 4 smoke artifacts; status `complete`. |
| Phase 8.Stage 2.Action 2 | complete | Inspected recommendation and downstream handoff rows. |
| Phase 8.Stage 3.Action 1 | complete | Recorded validation and Stage 6 handoff below. |

## Source Records

Stage 1 structural/reward source:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/structural_and_tower_diagnostics/readout_source.json
```

Stage 1 required tables confirmed:

```text
shortest_path_summary.csv
random_policy_recon_summary.csv
state_space_summary.csv
transition_summary.csv
```

Stage 4 training-health source:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/tower_training_health/readout_source.json
```

Stage 4 required tables confirmed:

```text
candidate_training_health_summary.csv
training_episode_summary.csv
training_curve_summary.csv
concrete_step_summary.csv
downstream_comparison_input_summary.csv
```

Stage 4 calibration facts observed before implementation:

- selected candidate: `plate_support_candidate:source_local_ratio:0:342448ef2e`;
- schema: `plate_support_schema_source_local_ratio_001_over_018_v001`;
- health: `trainable_clean`;
- episodes: `32`;
- successes: `2`;
- concrete steps: `1546`;
- lift successes: `1546`;
- learner updates: `1546`;
- runtime failures: `0`.

Initial calibration implication:

Stage 4 has enough nontrivial variation to evaluate binary success, first-hit,
sustained-window feasibility, and observed-return thresholds. It does not yet
authorize a paired comparison claim.

## Implemented Files

Stage 5 package:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/threshold_frontier_calibration/
```

Key files:

```text
__init__.py
config.py
stage_sources.py
calibration_arms.py
target_policies.py
threshold_grid.py
feasibility.py
aggregation.py
manifests.py
docs_writer.py
runner.py
```

Test file:

```text
tests/environments/plate_support/test_standard_gauntlet_threshold_frontier_calibration.py
```

CLI command:

```text
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet threshold-calibration run \
  --repo-root <repo-root> \
  --artifact-root <repo-root>/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \
  --training-health-source <repo-root>/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/tower_training_health/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster
```

## Repo Smoke Output

Stage 5 repo-local run completed with:

```text
status: complete
recommended_target_policy_id: plate_support_binary_goal_success_v001
readout_source: docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/threshold_frontier_calibration/readout_source.json
stage_root: docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001/stages/threshold_frontier_calibration
```

Recommended target row:

```text
target_type: binary_success
required_count: 1
candidate_feasibility: feasible_sparse_success_2_of_32
calibration_status: threshold_calibrated
recommended_episodes_per_replicate: 32
recommended_replicates_per_arm: 4
```

Interpretation:

The target is table-backed because Stage 4 observed both hits and misses for the
trainable tower candidate. Success is sparse, so Stage 6 should use the
recommended larger paired budget rather than treating the Stage 4 smoke budget
as a serious comparison.

Stage 5 writes return-threshold diagnostics as supporting evidence only. The
selected target is not a copied counterpoint threshold and not a return-value
guess.

## Validation

Focused checks:

```text
uv run ruff check src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/threshold_frontier_calibration tests/environments/plate_support/test_standard_gauntlet_threshold_frontier_calibration.py
```

Result:

```text
All checks passed.
```

CLI name/import sanity check:

```text
uv run ruff check src/big_boy_benchmarking/cli/main.py --select F401,F821,F822,F823
```

Result:

```text
All checks passed.
```

PlateSupport test slice:

```text
uv run pytest tests/environments/plate_support
```

Result:

```text
40 passed in 1.62s
```

## Stage 6 Handoff

Stage 6 should consume:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/threshold_frontier_calibration/readout_source.json
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001/stages/threshold_frontier_calibration/results/recommended_comparison_target.csv
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001/stages/threshold_frontier_calibration/results/downstream_paired_comparison_input_summary.csv
```

Stage 6 may use the calibrated binary success target. It must not reselect a
threshold internally.

## Parent Readout Note

The Stage 5 readout surface is current. The parent standard-gauntlet
`readout_source.json` has been updated from Stage 1-4 to Stage 1-5 and now
includes the Stage 5 child readout source path.

The parent standard-gauntlet README was generated before Stage 5 and still
describes the suite as Stage 1-4 partial. Regenerate the parent readout with:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-root>/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```

Do this after deciding whether to proceed directly to Stage 6 or pause for a
human-readable Stage 5 readout pass.

Validation:

```text
jq empty docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```

Result:

```text
valid JSON
```
