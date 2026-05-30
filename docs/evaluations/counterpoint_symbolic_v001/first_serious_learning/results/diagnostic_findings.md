# Diagnostic Findings

## Finding 1: Non-Empty Tower Arms Are Artifact-Complete But Behavior-Failed

Affected arms:

- `tower_random_balanced_exploit_explore_tabular_q`
- `tower_random_unbalanced_exploit_explore_tabular_q`
- `tower_motion_exploit_explore_tabular_q`
- `tower_bad_exploit_explore_tabular_q`

Evidence:

- `evaluation_aggregate_table.csv` records `mean_return=0.0`.
- `results/learning_curves.csv` records `step_count=0` and `success=False`.
- Per-run `lift_fiber_events.csv` files record repeated
  `invalid_action_index` failures.

This blocks a positive tower-performance claim for these non-empty schemas.

## Finding 2: Empty-Schema Tower Behaves Successfully

The empty-schema tower arm:

- has `64` episodes;
- has mean return `12.830`;
- has mean step count `8.0`;
- has `100%` episode success;
- records `512` successful lift-fiber events;
- records `exploit_execute`, `explore`, and `train` controller actions.

This suggests the tower shell can execute concrete environment actions when the
schema is empty/non-contractive.

## Finding 3: Non-Empty Towers Descend And Explore But Do Not Execute

Controller totals:

| Arm | Descend | Explore | Exploit execute | Train |
| --- | ---: | ---: | ---: | ---: |
| Empty-schema tower | 0 | 380 | 132 | 128 |
| Random balanced tower | 768 | 11,520 | 0 | 0 |
| Random unbalanced tower | 384 | 11,904 | 0 | 0 |
| Structured motion tower | 256 | 3,840 | 0 | 0 |
| Bad/adversarial tower | 64 | 4,032 | 0 | 0 |

The non-empty towers reach exploration at active tiers but do not record
successful exploit execution or training.

## Finding 4: Lift Failure Counts Match Controller Exploration Counts

| Arm | Lift failure reason | Count |
| --- | --- | ---: |
| Random balanced tower | `invalid_action_index` | 11,520 |
| Random unbalanced tower | `invalid_action_index` | 11,904 |
| Structured motion tower | `invalid_action_index` | 3,840 |
| Bad/adversarial tower | `invalid_action_index` | 4,032 |

The failure counts align with the controller `explore` counts for the non-empty
tower arms. This is the main mechanism behind zero-step episodes.

## Finding 5: Provenance Classification

The source evaluation root has absent provenance/calibration files. They are
not all the same kind of absence:

| File | Classification | Interpretation |
| --- | --- | --- |
| `evaluation_manifest.json` | `expected_missing_gap` | Expected evaluation-level provenance is absent. |
| `evaluation_arm_manifest.json` | `expected_missing_gap` | Expected arm-contract provenance is absent. |
| `calibration_summary.json` | `conditional_absent` | Calibration-path file; not necessarily expected for this locked serious run. |
| `calibration_run_index.csv` | `conditional_absent` | Calibration-path file; not necessarily expected for this locked serious run. |
| `calibration_recommendation.md` | `conditional_absent` | Calibration-path file; not necessarily expected for this locked serious run. |

The run can still be interpreted from the budget lock, run index, aggregate
tables, and per-run artifacts, but provenance is less complete than the current
contract expects for the two evaluation manifest files.

## Classification

This run is a mixed result:

```text
artifact_status: complete
behavior_status: mixed
claim_status: diagnostic_evidence / blocks positive non-empty tower claim
```
