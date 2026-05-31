# Timing Readout

## Timing Boundary

The available timing categories are:

- `algorithm_online`
- `linearization_setup`
- `total`

This timing readout is descriptive only. It should not be used as a speed claim
because the run is fixture-local, tensor execution is disabled, and random
schema arms are structural-limit diagnostics rather than ordinary performance
comparisons.

## Mean Timing By Arm

| Arm | Mean total seconds | Mean algorithm-online seconds | Mean linearization setup seconds |
| --- | ---: | ---: | ---: |
| Direct masked random | 0.070866 | 0.070372 | 0.000494 |
| Direct tabular Q | 0.011411 | 0.011154 | 0.000256 |
| Empty-schema tower | 0.254612 | 0.251285 | 0.003327 |
| Random balanced tower | 0.402994 | 0.375936 | 0.027058 |
| Random unbalanced tower | 0.432385 | 0.398726 | 0.033659 |
| Structured motion tower | 0.458044 | 0.414122 | 0.043921 |
| Bad/adversarial tower | 0.451407 | 0.407782 | 0.043625 |

## Interpretation

Direct tabular Q is the fastest arm in this run. Tower arms have higher total
and algorithm-online time. The timing rows are useful for diagnostics, but this
readout should not compare methods as production-speed candidates.

## Evidence

Source table:

```text
results/timing_summary.csv
```
