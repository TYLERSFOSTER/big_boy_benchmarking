# PlateSupport Paired Replicate Comparison Implementation Log

## Status

Status: complete.

This log records execution of:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/06_paired_replicate_comparison/01_002_plate_support_paired_replicate_comparison_implementation_workplan.md
```

This execution is part of the whole-gauntlet Mode B resume recorded in:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/00_suite_architecture/01_002_plate_support_standard_gauntlet_suite_architecture_implementation_workplan.md
```

## Phase.Stage.Action Progress

| Phase.Stage.Action | Status | Notes |
| --- | --- | --- |
| Phase 0.Stage 1.Action 1 | complete | Verified repo state before gauntlet Stage 6 edits. Branch is `main`; repo is ahead of `origin/main` and contains dirty earlier gauntlet work. These files are treated as existing umbrella work, not reverted. |
| Phase 0.Stage 1.Action 2 | complete | Verified required repo-resident Stage 1, Stage 3, Stage 4, and Stage 5 readout source paths exist. |
| Phase 0.Stage 1.Action 3 | complete | Stage 5 target gate passes: `plate_support_binary_goal_success_v001`, target type `binary_success`, recommended budget `32` episodes by `4` replicates per arm. |
| Phase 0.Stage 1.Action 4 | complete | Stage 4 trainable-candidate gate passes: one `trainable_clean` source-local ratio candidate. |
| Phase 0.Stage 1.Action 5 | complete | `state_collapser` dependency reports import version `0.7.2` and inspection status `ok`. |
| Phase 0.Stage 2.Action 1 | complete | Created this gauntlet Stage 6 implementation log before Stage 6 source edits. |
| Phase 0.Stage 2.Action 2 | complete | Initial source record added below. |
| Phase 1.Stage 1.Action 1 | complete | Create paired comparison package. |
| Phase 1.Stage 1.Action 2 | complete | Add module initializer. |
| Phase 1.Stage 2.Action 1 | complete | Implement config dataclass. |
| Phase 1.Stage 2.Action 2 | complete | Implement comparison budget lock. |
| Phase 2.Stage 1.Action 1 | complete | Implement source loader. |
| Phase 2.Stage 1.Action 2 | complete | Validate required source tables. |
| Phase 2.Stage 2.Action 1 | complete | Build direct concrete baseline arm. |
| Phase 2.Stage 2.Action 2 | complete | Build no-contraction tower-control arm or record unavailable reason. |
| Phase 2.Stage 2.Action 3 | complete | Build selected tower candidate arms. |
| Phase 2.Stage 2.Action 4 | complete | Write comparison arm manifest. |
| Phase 3.Stage 1.Action 1 | complete | Generate paired seed bundles. |
| Phase 3.Stage 1.Action 2 | complete | Build pair unit manifest. |
| Phase 3.Stage 2.Action 1 | complete | Track incomplete pairs visibly. |
| Phase 4.Stage 1.Action 1 | complete | Run direct baseline pairs. |
| Phase 4.Stage 1.Action 2 | complete | Run no-contraction tower-control pairs if available. |
| Phase 4.Stage 2.Action 1 | complete | Run selected tower candidate pairs. |
| Phase 4.Stage 2.Action 2 | complete | Emit per-run artifacts. |
| Phase 5.Stage 1.Action 1 | complete | Write comparison run index. |
| Phase 5.Stage 1.Action 2 | complete | Write paired unit summary. |
| Phase 5.Stage 2.Action 1 | complete | Write arm summary tables. |
| Phase 5.Stage 2.Action 2 | complete | Write target and learning tables. |
| Phase 5.Stage 3.Action 1 | complete | Write tower runtime summaries. |
| Phase 5.Stage 3.Action 2 | complete | Write timing and artifact completeness summaries. |
| Phase 6.Stage 1.Action 1 | complete | Compute paired schema comparison table. |
| Phase 6.Stage 1.Action 2 | complete | Validate primary metric from Stage 5. |
| Phase 6.Stage 2.Action 1 | complete | Implement claim classifier. |
| Phase 6.Stage 2.Action 2 | complete | Write comparison claim summary. |
| Phase 7.Stage 1.Action 1 | complete | Write evaluation manifests. |
| Phase 7.Stage 1.Action 2 | complete | Write gauntlet Stage 6 readout source. |
| Phase 7.Stage 2.Action 1 | complete | Write seed human docs. |
| Phase 8.Stage 1.Action 1 | complete | Add CLI run command. |
| Phase 8.Stage 1.Action 2 | complete | Add summarize/inspect only if consistent. |
| Phase 9.Stage 1.Action 1 | complete | Test hard gates. |
| Phase 9.Stage 1.Action 2 | complete | Test paired seed discipline. |
| Phase 9.Stage 1.Action 3 | complete | Test incomplete pair exclusion. |
| Phase 9.Stage 1.Action 4 | complete | Test claim classifier. |
| Phase 9.Stage 1.Action 5 | complete | Test required tables and readout source. |
| Phase 9.Stage 2.Action 1 | complete | Run gauntlet Stage 6 smoke comparison. |
| Phase 9.Stage 2.Action 2 | complete | Inspect claim and pair tables. |
| Phase 9.Stage 3.Action 1 | complete | Record validation and gauntlet Stage 7 handoff. |

## Source Record

Stage 1 structural source:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/structural_and_tower_diagnostics/readout_source.json
```

Stage 3 candidate source:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/candidate_discovery/readout_source.json
```

Stage 4 tower-training-health source:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/tower_training_health/readout_source.json
```

Stage 5 threshold calibration source:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/threshold_frontier_calibration/readout_source.json
```

Target:

```text
plate_support_binary_goal_success_v001
```

Initial arms:

- primary baseline: `plate_support_direct_concrete_baseline`;
- tower candidate: `plate_support_selected_tower_candidate:<candidate-id>`;
- no-contraction tower control: record unavailable unless an approved Stage 6
  no-contraction runtime adapter exists.

## Final Result

Stage 6 was implemented and run at the repo artifact root:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001/stages/paired_replicate_comparison
```

The run completed with:

```text
claim_status = paired_comparison_negative_signal
complete_pair_count = 4
mean_target_hit_rate_delta = -0.0703125
```

The bounded target claim is negative because Stage 5 selected binary goal
success as the comparison target. The same tables record that the tower
candidate had better mean reward and zero invalid moves versus the direct
baseline; this is preserved as interpretation/counter-signal, not as a reversal
of the target claim.

Validation:

```text
uv run ruff check src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison src/big_boy_benchmarking/cli/main.py --select F401,F821,F822,F823
uv run pytest tests/environments/plate_support/test_standard_gauntlet_paired_replicate_comparison.py tests/environments/plate_support/test_standard_gauntlet_readout_system_learning.py
uv run pytest tests/environments/plate_support/test_standard_gauntlet_*.py
```

Handoff:

- Stage 6 is complete.
- The whole-gauntlet resume continued into Stage 7, as required by the parent
  umbrella workplan.
