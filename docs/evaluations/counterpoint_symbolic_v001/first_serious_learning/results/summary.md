# Results Summary

Aggregate status: `complete`

Complete arms: `7` / `7`

Run count: `44`

Required result tables are present and parse. Expected evaluation-level
manifest files and promoted tower summary tables remain absent, so artifact
evidence is classified as partial rather than fully contract-complete.

## Main Result

| Arm | Mean return | Mean steps | Episode success | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Direct masked random | 12.790 | 8.0 | 100% | Direct non-learning floor. |
| Direct tabular Q | 12.696 | 8.0 | 100% | Primary direct baseline. |
| Empty-schema tower | 12.710 | 8.0 | 100% | Tower shell executes. |
| Random balanced tower | 4.237 | 2.7 | 33% | Structural-limit diagnostic; schema seeds `0` and `1` fail, seed `2` executes. |
| Random unbalanced tower | 8.473 | 5.3 | 67% | Structural-limit diagnostic; schema seed `1` fails, seeds `0` and `2` execute. |
| Structured motion tower | 12.710 | 8.0 | 100% | Executes under full first-projection collapse; not useful tower-control evidence. |
| Bad/adversarial tower | 12.710 | 8.0 | 100% | Executes under full first-projection collapse; not a valid negative-control result here. |

## Interpretation

The non-empty tower arms are dominated by full or near-full first-projection
collapse. The remaining zero-step failures are localized to random-schema seeds
and are recorded as `no_lift_candidate_from_current_state`.

The run does not support a positive tower-performance claim and should not be
summarized as ordinary mixed non-performance.
