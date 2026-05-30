# Arm Readout Table

| Arm label | Arm id | Artifact status | Behavior status | Runs | Episodes | Mean return | Mean steps | Success rate | Delta vs direct Q | Primary evidence |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Direct masked random | `direct_masked_random` | complete | succeeded | 4 | 64 | 12.807 | 8.0 | 100% | -0.069 | `learning_curves.csv` |
| Direct tabular Q | `direct_tabular_q` | complete | succeeded | 4 | 64 | 12.876 | 8.0 | 100% | 0.000 | `learning_curves.csv` |
| Empty-schema tower | `tower_empty_exploit_explore_tabular_q` | complete | succeeded | 4 | 64 | 12.830 | 8.0 | 100% | -0.046 | `learning_curves.csv`, `lift_fiber_events.csv` |
| Random balanced tower | `tower_random_balanced_exploit_explore_tabular_q` | complete | failed | 12 | 192 | 0.000 | 0.0 | 0% | -12.876 | `learning_curves.csv`, per-run `lift_fiber_events.csv` |
| Random unbalanced tower | `tower_random_unbalanced_exploit_explore_tabular_q` | complete | failed | 12 | 192 | 0.000 | 0.0 | 0% | -12.876 | `learning_curves.csv`, per-run `lift_fiber_events.csv` |
| Structured motion tower | `tower_motion_exploit_explore_tabular_q` | complete | failed | 4 | 64 | 0.000 | 0.0 | 0% | -12.876 | `learning_curves.csv`, per-run `lift_fiber_events.csv` |
| Bad/adversarial tower | `tower_bad_exploit_explore_tabular_q` | complete | failed | 4 | 64 | 0.000 | 0.0 | 0% | -12.876 | `learning_curves.csv`, per-run `lift_fiber_events.csv` |

## Notes

- `complete` means artifact complete, not behavior successful.
- The non-empty tower zeroes are classified as behavioral failures, not
  legitimate performance zeroes.
- The direct tabular Q arm is the primary direct baseline.
- The empty-schema tower arm is the tower shell baseline.
