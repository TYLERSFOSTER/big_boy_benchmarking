# Arm Readout Table

| Arm label | Arm id | Artifact status | Behavior status | Runs | Episodes | Mean return | Mean steps | Success rate | Delta vs direct Q | Primary evidence |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Direct masked random | `direct_masked_random` | complete | succeeded | 4 | 64 | 12.790 | 8.0 | 100% | +0.094 | `learning_curves.csv` |
| Direct tabular Q | `direct_tabular_q` | complete | succeeded | 4 | 64 | 12.696 | 8.0 | 100% | +0.000 | `learning_curves.csv` |
| Empty-schema tower | `tower_empty_exploit_explore_tabular_q` | complete | succeeded | 4 | 64 | 12.710 | 8.0 | 100% | +0.013 | `learning_curves.csv`, `lift_fiber_events.csv` |
| Random balanced tower | `tower_random_balanced_exploit_explore_tabular_q` | complete | structural_limit | 12 | 192 | 4.237 | 2.7 | 33% | -8.460 | `learning_curves.csv`, per-run `lift_fiber_events.csv` |
| Random unbalanced tower | `tower_random_unbalanced_exploit_explore_tabular_q` | complete | structural_limit | 12 | 192 | 8.473 | 5.3 | 67% | -4.223 | `learning_curves.csv`, per-run `lift_fiber_events.csv` |
| Structured motion tower | `tower_motion_exploit_explore_tabular_q` | complete | structural_limit | 4 | 64 | 12.710 | 8.0 | 100% | +0.013 | `learning_curves.csv`, `lift_fiber_events.csv` |
| Bad/adversarial tower | `tower_bad_exploit_explore_tabular_q` | complete | structural_limit | 4 | 64 | 12.710 | 8.0 | 100% | +0.013 | `learning_curves.csv`, `lift_fiber_events.csv` |

## Notes

- `complete` means artifact complete, not automatically behavior successful.
- Non-empty tower behavior is classified as `structural_limit` because full or
  near-full first-projection collapse dominates interpretation.
- Random balanced and random unbalanced still show schema-seed-dependent
  concrete execution inside that structural-limit condition.
- `no_lift_candidate_from_current_state` is the remaining random-schema failure
  reason in this artifact set.
- The direct tabular Q arm is the primary direct baseline.
- The empty-schema tower arm is the tower shell baseline.
