# PlateSupport Direct-Star Cul-de-sac Control Implementation Log

## Status

Implemented and verified.

The implemented diagnostic answers Abdul Malik's PM concern that the earlier
PlateSupport tower-positive signal might be explained by the tower controller's
one-step/executable-action filtering rather than by a hierarchy advantage that
survives a guarded direct control.

Final guarded diagnostic interpretation:

```text
validity_filtering_explains_signal
```

This means the selected tower still beats raw direct, but it does not beat the
one-step guarded direct controls in the completed `guarded_001` run.

## Controlling Documents

- `docs/design/first_plate_support_environment/standard_gauntlet_suite/09_direct_star_culdesac_control/design_discussion.md`
- `docs/design/first_plate_support_environment/standard_gauntlet_suite/09_direct_star_culdesac_control/01_001_plate_support_direct_star_culdesac_control_blueprint.md`
- `docs/design/first_plate_support_environment/standard_gauntlet_suite/09_direct_star_culdesac_control/01_002_plate_support_direct_star_culdesac_control_implementation_workplan.md`
- `state_collapser_invalid_action_self_loop_filtering_issue.md`
- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`
- `docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md`
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`
- `docs/prime_directive/git_practices.md`

## Attribution Record

- Abdul Malik, project PM, raised the self-loop / cul-de-sac concern.
- The Project Owner accepted Abdul's concern and directed BBB-side diagnostic
  design and implementation.
- Codex recommended and implemented the concrete guarded-direct control:
  `direct_raw`, `direct_invalid_guard`, `direct_nonself_guard`, and
  `tower_selected_candidate`.

No Project Owner turns were invented in generated docs.

## Decision Locks

```text
evaluation_id: plate_support_direct_star_culdesac_control_v001
cli_family: plate-support direct-star-culdesac-control
implementation_branch: codex/plate-support-direct-star-culdesac-control
source_package: src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/
test_file: tests/environments/plate_support/test_direct_star_culdesac_control.py
repo_readout_surface: docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/
parent_gauntlet_source: docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
artifact_run_labels: smoke_001, guarded_001
guarded_direct_policy: pre-mask before action selection
guarded_block_policy: diagnostic blocked termination; no silent raw fallback
claim_boundary: diagnostic smoke/calibration evidence only
```

## Phase.Stage.Action Progress

| Phase.Stage.Action | Status | Files | Verification | Notes |
| --- | --- | --- | --- | --- |
| Phase 0.Stage 1.Action 1 | Complete | n/a | `git status --short --branch` | Started from a dirty design-doc state expected for this work. |
| Phase 0.Stage 1.Action 2 | Complete | n/a | `git checkout -b codex/plate-support-direct-star-culdesac-control` | Created dedicated implementation branch. |
| Phase 0.Stage 1.Action 3 | Complete | controlling docs and source files | Re-read workplan, blueprint, discussion, prime directives, and existing PlateSupport gauntlet code | No newer contradictory design artifact found. |
| Phase 0.Stage 2.Action 1 | Complete | this log | Log existed before main source edits | Log later rewritten with full audit detail. |
| Phase 0.Stage 2.Action 2 | Complete | this log | Progress table present | This table maps implementation to workplan actions. |
| Phase 1.Stage 1.Action 1 | Complete | existing paired comparison runner/events/arms/target policy | Source inspection | Reused direct Q-learning shape, paired seeds, target-hit policy, and event conventions without changing historical Stage 6 behavior. |
| Phase 1.Stage 1.Action 2 | Complete | existing tower training surfaces | Source inspection | Reused `build_training_surface`, `available_tower_action_choices`, `next_state_best_value`, `state_payload_text`, and `cell_text`. |
| Phase 1.Stage 1.Action 3 | Complete | existing readout/source helpers | Source inspection | Matched repo-resident readout-source discipline and badge/readout protocol. |
| Phase 1.Stage 2.Action 1 | Complete | parent gauntlet readout source | Parent source loader and smoke run | Parent source binding was present, but raw `iterated_001` parent artifacts were externalized. |
| Phase 1.Stage 2.Action 2 | Complete | `parent_source.py` | Guarded run resolved candidate | Selected candidate: `plate_support_candidate:source_local_ratio_iterated:0:c8b8935b4c`. |
| Phase 1.Stage 2.Action 3 | Complete | `parent_source.py` | Guarded run resolved target | Target: `plate_support_binary_goal_success_v001`, 32 episodes per replicate, 4 replicates per arm. |
| Phase 1.Stage 2.Action 4 | Complete | dependency manifests | Dependency state checked | `state_collapser` import version was `0.7.2`; dependency manifests redact local `source_path` for public hygiene. |
| Phase 2.Stage 1.Action 1 | Complete | `src/.../direct_star_culdesac_control/` | Package exists | Kept separate from `standard_gauntlet/paired_replicate_comparison`. |
| Phase 2.Stage 1.Action 2 | Complete | `__init__.py` | Import tests | Package exports stable symbols without evaluation side effects. |
| Phase 2.Stage 2.Action 1 | Complete | `config.py` | Unit tests and CLI run | Explicit config covers repo root, artifact root, parent source, budgets, Q parameters, and smoke mode. |
| Phase 2.Stage 2.Action 2 | Complete | `paths.py` | Run artifacts landed under repo readout surface | Artifact roots are run-label scoped under `docs/evaluations/.../direct_star_culdesac_control/artifacts/`. |
| Phase 2.Stage 2.Action 3 | Complete | `parent_source.py` | Smoke and guarded runs | Loader resolves parent selected candidate and calibrated target, and fails clearly if parent release-asset evidence is absent. |
| Phase 2.Stage 3.Action 1 | Complete | `src/big_boy_benchmarking/cli/main.py` | CLI help command | Added `plate-support direct-star-culdesac-control run`. |
| Phase 2.Stage 3.Action 2 | Complete | `src/big_boy_benchmarking/cli/main.py` | Summarize command run | Added `plate-support direct-star-culdesac-control summarize`. |
| Phase 3.Stage 1.Action 1 | Complete | `guards.py` | Unit tests | Guard ids: `raw`, `invalid_guard`, `nonself_guard`. |
| Phase 3.Stage 1.Action 2 | Complete | `guards.py` | Unit tests on real PlateSupport start state | Classifier separates invalid moves, self loops, valid clipped self loops, and nonself transitions. |
| Phase 3.Stage 2.Action 1 | Complete | `guards.py` | Unit tests | Raw direct sees all 12 primitive actions. |
| Phase 3.Stage 2.Action 2 | Complete | `guards.py` | Unit tests | Invalid guard removes invalid actions only. |
| Phase 3.Stage 2.Action 3 | Complete | `guards.py` | Unit tests | Nonself guard removes self-loop actions. |
| Phase 3.Stage 2.Action 4 | Complete | `guards.py` | Unit tests and result tables | Guard summaries include before/after/filter/block counts. |
| Phase 3.Stage 3.Action 1 | Complete | `runner.py` | Runner logic and event rows | Zero available guarded actions produce diagnostic blocked termination; no raw fallback. |
| Phase 3.Stage 3.Action 2 | Complete | `runner.py`, `docs_writer.py`, manifests | Readout source and budget lock | Information mode and parity warning are machine-readable and rendered in README. |
| Phase 4.Stage 1.Action 1 | Complete | `manifests.py` | Unit tests | Four arms are separate; guarded direct does not replace raw direct. |
| Phase 4.Stage 1.Action 2 | Complete | `runner.py` | `evaluation_budget_lock.json` | Budget lock records parent source, candidate, schema, budget, seeds, Q parameters, and guard mode. |
| Phase 4.Stage 2.Action 1 | Complete | `runner.py` | Unit tests and direct raw rows | Raw direct selection uses the ambient primitive action alphabet. |
| Phase 4.Stage 2.Action 2 | Complete | `runner.py`, `guards.py` | Unit tests and guard events | Guards are applied before epsilon/greedy selection. |
| Phase 4.Stage 2.Action 3 | Complete | `runner.py` | Source inspection and run output | Direct Q bootstrap uses the same guard-specific next-state action surface. |
| Phase 4.Stage 2.Action 4 | Complete | `runner.py` | Event schema supports blocked episodes | No blocked guard states occurred in `guarded_001`, but the behavior is implemented. |
| Phase 4.Stage 3.Action 1 | Complete | `parent_source.py`, `runner.py` | Guarded run resolved selected tower | Reconstructed selected iterated tower candidate from parent tables; no hard-coded candidate id. |
| Phase 4.Stage 3.Action 2 | Complete | `runner.py` | Smoke and guarded runs | Tower arm runs through existing tower training surface. |
| Phase 4.Stage 4.Action 1 | Complete | `events.py`, `runner.py` | Result tables and tests | `guard_events.csv` has required columns and records direct and tower action surfaces. |
| Phase 4.Stage 4.Action 2 | Complete | `events.py`, `runner.py` | `episode_summary.csv`, `step_summary.csv` | Episode/step rows include invalid/self-loop/blocked evidence. |
| Phase 4.Stage 4.Action 3 | Complete | `runner.py` | Per-run artifact trees | Run manifests, seeds, timing, guard, step, learner, lift, and tier event files are written. |
| Phase 5.Stage 1.Action 1 | Complete | `aggregation.py` | Unit tests and smoke/guarded runs | Aggregation builds table set from raw rows. |
| Phase 5.Stage 1.Action 2 | Complete | `aggregation.py` | `arm_summary.csv` | Arm summary separates target hit, mean reward, invalid rate, self-transition rate, and blocked counts. |
| Phase 5.Stage 1.Action 3 | Complete | `aggregation.py` | `guard_filter_summary.csv` | Direct raw, invalid guard, nonself guard, and tower action surfaces are distinguishable. |
| Phase 5.Stage 1.Action 4 | Complete | `aggregation.py` | `self_loop_summary.csv`, `invalid_vs_self_loop_summary.csv` | Tables isolate invalid self loops from valid clipped self transitions. |
| Phase 5.Stage 1.Action 5 | Complete | `aggregation.py` | `paired_guard_comparison.csv` | Paired comparisons preserve matched seed bundles. |
| Phase 5.Stage 1.Action 6 | Complete | `aggregation.py` | `action_surface_summary.csv` | Action-surface table supports the parity warning. |
| Phase 5.Stage 2.Action 1 | Complete | `aggregation.py` | `interpretation_summary.csv` | Implemented interpretation grid; final guarded result is `validity_filtering_explains_signal`. |
| Phase 5.Stage 2.Action 2 | Complete | `aggregation.py`, `docs_writer.py` | Badge SVG inspection | Badges use local two-segment shield style. |
| Phase 5.Stage 2.Action 3 | Complete | `docs_writer.py`, `readout_source.json` | README and source binding | Information parity warning appears near the top of README and in source binding. |
| Phase 6.Stage 1.Action 1 | Complete | `docs_writer.py`, readout surface | Summarize command | Wrote README, method, runbook, artifact index, result readout, result docs, badges, and source binding. |
| Phase 6.Stage 1.Action 2 | Complete | `readout_source.json` | Source binding inspection | Required source files are explicit and repo-resident. |
| Phase 6.Stage 1.Action 3 | Complete | `readout_source.json`, README | Source binding inspection | Goal criteria, methodology sources, structural limit checks, badge policy, and claim boundary are populated. |
| Phase 6.Stage 2.Action 1 | Complete | README and result docs | Manual application of artifact-table protocol | Generated readout from explicit `readout_source.json`, not folder inference. |
| Phase 6.Stage 2.Action 2 | Complete | badges and README | Badge SVG inspection | Badges are local two-segment shields and use reader-facing `Label: Value` text. |
| Phase 7.Stage 1.Action 1 | Complete | `tests/environments/plate_support/test_direct_star_culdesac_control.py` | Focused tests | Guard tests cover raw, invalid, nonself, and core-state payload handling. |
| Phase 7.Stage 1.Action 2 | Complete | same test file | Focused tests | Tests cover arm manifest, aggregation with tower guard rows, and readout/badge generation. |
| Phase 7.Stage 1.Action 3 | Complete | same test file, CLI parser | Focused tests and CLI help | Parser accepts run and summarize subcommands. |
| Phase 7.Stage 2.Action 1 | Complete | tests | `uv run pytest tests/environments/plate_support/test_direct_star_culdesac_control.py` | 6 passed. |
| Phase 7.Stage 2.Action 2 | Complete | tests | `uv run pytest tests/environments/plate_support/test_standard_gauntlet_paired_replicate_comparison.py tests/environments/plate_support/test_cli_plate_support.py` | 6 passed. |
| Phase 7.Stage 2.Action 3 | Complete | tests | `uv run pytest tests/environments/plate_support` | 63 passed. |
| Phase 7.Stage 3.Action 1 | Complete | `artifacts/smoke_001` | Smoke run command | Smoke run completed, 46 artifacts. |
| Phase 7.Stage 3.Action 2 | Complete | `artifacts/smoke_001` | Smoke summarize earlier completed | Smoke artifacts were generated and summarized during implementation. |
| Phase 7.Stage 3.Action 3 | Complete | direct-star readout surface | README generation | Final readout was regenerated from `guarded_001`; smoke served as verification only. |
| Phase 8.Stage 1.Action 1 | Complete | `artifacts/guarded_001` | Guarded run command | Guarded run completed, 46 artifacts, interpretation `validity_filtering_explains_signal`. |
| Phase 8.Stage 1.Action 2 | Complete | `artifacts/guarded_001` | Guarded summarize command | Summarize completed, 18 docs/readout files reported. |
| Phase 8.Stage 2.Action 1 | Complete | README and result docs | Artifact-table readout protocol applied | README classifies result and includes Abdul/PO/Codex attribution and parity warning. |
| Phase 8.Stage 2.Action 2 | Not Needed | n/a | No new architecture issue beyond the intended Abdul diagnostic was discovered | Result is important, but it is the expected diagnostic outcome rather than a new separate system-learning issue. |
| Phase 9.Stage 1.Action 1 | Complete | n/a | `git status --short` | Dirty files are within work scope; restored parent input artifacts are ignored narrowly. |
| Phase 9.Stage 1.Action 2 | Complete | readout/docs | local-path check and README inspection | Direct-star readout has no machine-local path leaks. |
| Phase 9.Stage 1.Action 3 | Complete | repo | `uv run python scripts/release_hygiene.py --repo-root .` | Release hygiene passed. |
| Phase 9.Stage 2.Action 1 | Complete | this log | This file | Full implementation log completed. |
| Phase 9.Stage 2.Action 2 | Pending Final Response | n/a | Final handoff pending | To be reported to Project Owner in final response. |

## Files Changed

Implementation:

- `.gitignore`
- `src/big_boy_benchmarking/cli/main.py`
- `src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/__init__.py`
- `src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/aggregation.py`
- `src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/config.py`
- `src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/docs_writer.py`
- `src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/events.py`
- `src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/guards.py`
- `src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/manifests.py`
- `src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/parent_source.py`
- `src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/paths.py`
- `src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/runner.py`

Tests:

- `tests/environments/plate_support/test_direct_star_culdesac_control.py`

Design and logs:

- `docs/design/first_plate_support_environment/standard_gauntlet_suite/09_direct_star_culdesac_control/01_003_plate_support_direct_star_culdesac_control_implementation_log.md`

Evaluation readout/artifacts:

- `docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/`

## Artifacts Generated

Smoke verification:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/smoke_001/
```

Final guarded diagnostic:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/guarded_001/
```

Human-readable readout:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/README.md
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/result_readout.md
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/results/summary.md
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/results/human_summary.md
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/results/arm_readout_table.md
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/results/diagnostic_findings.md
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/results/timing_readout.md
```

## Commands Run

Key commands:

```text
git status --short --branch
git checkout -b codex/plate-support-direct-star-culdesac-control
uv run pytest tests/environments/plate_support/test_direct_star_culdesac_control.py
uv run pytest tests/environments/plate_support/test_standard_gauntlet_paired_replicate_comparison.py tests/environments/plate_support/test_cli_plate_support.py
uv run pytest tests/environments/plate_support
uv run python -m big_boy_benchmarking.cli plate-support direct-star-culdesac-control --help
uv run python -m big_boy_benchmarking.cli plate-support direct-star-culdesac-control run --repo-root . --artifact-root docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/smoke_001 --parent-gauntlet-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json --run-label smoke_001 --locked-by foster --smoke
uv run python -m big_boy_benchmarking.cli plate-support direct-star-culdesac-control run --repo-root . --artifact-root docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/guarded_001 --parent-gauntlet-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json --run-label guarded_001 --locked-by foster
uv run python -m big_boy_benchmarking.cli plate-support direct-star-culdesac-control summarize --repo-root . --artifact-root docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/guarded_001
uv run python scripts/release_hygiene.py --repo-root .
```

Parent artifact restoration commands:

```text
zstd -d dist/release-assets/v0.1.0-beta.1/big_boy_calibration_smoke_v0.1.0-beta.1_artifacts.tar.zst -o <tmp>/bbb-calibration-smoke-v010-beta1-artifacts.tar
tar --exclude='*/._*' -xf <tmp>/bbb-calibration-smoke-v010-beta1-artifacts.tar docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/iterated_001
```

## Test Results

```text
uv run pytest tests/environments/plate_support/test_direct_star_culdesac_control.py
6 passed

uv run pytest tests/environments/plate_support/test_standard_gauntlet_paired_replicate_comparison.py tests/environments/plate_support/test_cli_plate_support.py
6 passed

uv run pytest tests/environments/plate_support
63 passed

uv run python scripts/release_hygiene.py --repo-root .
release hygiene passed
```

## Guarded Diagnostic Result

Final `guarded_001` arm summary:

| Arm | Target Hit Rate | Mean Reward | Invalid Rate | Self-Transition Rate |
| --- | ---: | ---: | ---: | ---: |
| `direct_raw` | 0.1171875 | -78.71875 | 0.3559913578195114 | 0.4631876350340701 |
| `direct_invalid_guard` | 0.359375 | -17.1640625 | 0.0 | 0.16553199766582377 |
| `direct_nonself_guard` | 0.515625 | 18.78125 | 0.0 | 0.0 |
| `tower_selected_candidate` | 0.1953125 | -27.2109375 | 0.0 | 0.0 |

Interpretation:

```text
tower_vs_raw_delta: 0.078125
tower_vs_invalid_guard_delta: -0.1640625
tower_vs_nonself_guard_delta: -0.3203125
```

Allowed claim:

```text
ordinary one-step validity filtering explains most of the original tower signal
```

Blocked claim:

```text
tower hierarchy beat direct learning on an equivalent decision surface
```

## Blockers And Surprises

- The parent standard gauntlet `iterated_001` artifacts were not present in the
  checkout because they were externalized in the beta release artifact bundle.
  I restored them locally from the bundle to execute the diagnostic.
- The restored parent input tree is not an output of this work. A narrow
  `.gitignore` entry now prevents accidentally staging:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/iterated_001/
```

- An initial path-hygiene pass found absolute local paths in generated artifact
  indexes, parent manifests, dependency manifests, and run-index artifact-root
  fields. I fixed the generators and reran smoke/guarded artifacts so the
  direct-star output no longer leaks machine-local paths.
- No additional system-learning archive was created because the result is the
  intended diagnostic outcome of this design block, not a newly discovered
  separate architecture issue.

## Handoff Notes

- The executable surface is:

```text
uv run python -m big_boy_benchmarking.cli plate-support direct-star-culdesac-control run ...
uv run python -m big_boy_benchmarking.cli plate-support direct-star-culdesac-control summarize ...
```

- The human-readable protocol target is:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json
```

- The current readout already reflects the guarded run:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/README.md
```

- If a future engineer reruns this from a clean checkout, they must either have
  the parent `standard_gauntlet/artifacts/iterated_001` tree restored from the
  beta release asset bundle or rerun the parent standard gauntlet first.
