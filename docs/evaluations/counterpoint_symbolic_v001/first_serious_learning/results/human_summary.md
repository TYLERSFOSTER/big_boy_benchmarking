# Human Summary

## Verdict

The evaluation is artifact-complete but behavior-mixed.

All required arms wrote artifacts and have run-index status `success`. The
direct arms and empty-schema tower arm behaved successfully. The non-empty
tower arms failed behaviorally: they produced zero return, zero concrete
environment steps, and zero successful episodes.

## Main Numbers

| Group | Mean return | Mean steps | Episode success |
| --- | ---: | ---: | ---: |
| Direct masked random | 12.807 | 8.0 | 100% |
| Direct tabular Q | 12.876 | 8.0 | 100% |
| Empty-schema tower | 12.830 | 8.0 | 100% |
| Non-empty tower arms | 0.000 | 0.0 | 0% |

## Explanation

The non-empty tower arms did not realize valid concrete environment actions.
Per-run `lift_fiber_events.csv` files record repeated `invalid_action_index`
failures. The controller summaries show descent and exploration, but no
successful exploit execution or training for those arms.

## Claim

This artifact set is diagnostic evidence. It does not support a positive tower
performance claim.
