# Human Summary

## Verdict

The evaluation is artifact-complete for required result tables but
behavior-mixed.

All `44` runs have run-index status `success`. Direct masked random, direct
tabular Q, empty-schema tower, structured-motion tower, and bad/adversarial
tower all execute 8-step episodes with 100% episode success. Random balanced
and random unbalanced are schema-seed dependent and include zero-step failures.

## Main Numbers

| Group | Mean return | Mean steps | Episode success |
| --- | ---: | ---: | ---: |
| Direct masked random | 12.790 | 8.0 | 100% |
| Direct tabular Q | 12.696 | 8.0 | 100% |
| Empty-schema tower | 12.710 | 8.0 | 100% |
| Random balanced tower | 4.237 | 2.7 | 33% |
| Random unbalanced tower | 8.473 | 5.3 | 67% |
| Structured motion tower | 12.710 | 8.0 | 100% |
| Bad/adversarial tower | 12.710 | 8.0 | 100% |

## Explanation

The only behavioral failures in the aggregate are concentrated in random schema
seeds. Random balanced fails on schema seeds `0` and `1`; random unbalanced
fails on schema seed `1`. The recorded reason is
`no_lift_candidate_from_current_state`.

## Claim

This artifact set is useful diagnostic evidence. It does not support a positive
tower-performance claim, because structured motion does not beat the empty
tower, random schemas remain seed-sensitive, and the bad/adversarial control
does not degrade under this budget.
