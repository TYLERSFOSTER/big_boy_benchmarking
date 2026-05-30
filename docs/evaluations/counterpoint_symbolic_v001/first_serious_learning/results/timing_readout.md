# Timing Readout

## Timing Boundary

The available timing categories are:

- `algorithm_online`
- `linearization_setup`
- `total`

This timing readout is descriptive only. It should not be used as a speed claim
because several tower arms failed behaviorally and because the result is
diagnostic rather than claim-supporting performance evidence.

## Mean Timing By Arm

| Arm | Mean total seconds | Mean algorithm-online seconds | Mean linearization setup seconds |
| --- | ---: | ---: | ---: |
| Direct masked random | 0.072260 | 0.071745 | 0.000516 |
| Direct tabular Q | 0.011114 | 0.010854 | 0.000260 |
| Empty-schema tower | 0.253078 | 0.249751 | 0.003327 |
| Random balanced tower | 0.371513 | 0.343495 | 0.028018 |
| Random unbalanced tower | 0.377663 | 0.346880 | 0.030783 |
| Structured motion tower | 0.393001 | 0.348180 | 0.044821 |
| Bad/adversarial tower | 0.387559 | 0.342590 | 0.044969 |

## Interpretation

Direct tabular Q is the fastest arm in this run. Tower arms have higher total
and algorithm-online time. The non-empty tower timing rows are still useful for
diagnostics, but because those arms failed to execute concrete environment
steps, their timings should not be read as normal successful tower rollout
costs.

## Evidence

Source table:

```text
results/timing_summary.csv
```
