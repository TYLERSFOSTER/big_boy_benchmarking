# Timing Readout

## Timing Boundary

The available timing categories are:

- `algorithm_online`
- `linearization_setup`
- `total`

This timing readout is descriptive only. It should not be used as a speed claim
because the run is fixture-local, tensor execution is disabled, and non-empty
tower arms are structural-limit diagnostics rather than ordinary performance
comparisons.

## Mean Timing By Arm

| Arm | Mean total seconds | Mean algorithm-online seconds | Mean linearization setup seconds |
| --- | ---: | ---: | ---: |
| Direct masked random | 0.078030 | 0.077439 | 0.000592 |
| Direct tabular Q | 0.012335 | 0.011891 | 0.000444 |
| Empty-schema tower | 0.267029 | 0.263408 | 0.003621 |
| Random balanced tower | 0.415845 | 0.387888 | 0.027957 |
| Random unbalanced tower | 0.458017 | 0.422194 | 0.035823 |
| Structured motion tower | 0.483324 | 0.434323 | 0.049001 |
| Bad/adversarial tower | 0.510866 | 0.458775 | 0.052091 |

## Interpretation

Direct tabular Q is the fastest arm in this run. Tower arms have higher total
and algorithm-online time. The timing rows are useful for diagnostics, but this
readout should not compare methods as production-speed candidates.

## Evidence

Source table:

```text
results/timing_summary.csv
```
