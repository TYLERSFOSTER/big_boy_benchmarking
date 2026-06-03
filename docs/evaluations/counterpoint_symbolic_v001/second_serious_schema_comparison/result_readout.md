# Result Readout

This readout translates the current `r000_001` artifact set into the bounded
claim language used by the second serious counterpoint schema-comparison
evaluation.

## Verdict

The artifact set is complete and both schema arms executed real environment
steps. The threshold result is blocked for comparison: at `episode_total_reward
>= 13.0`, both arms crossed the threshold transiently but neither arm met the
`4_of_5` persistence rule. Therefore no speed-to-sustained-hit delta is
available.

## Arm Summary

| Schema | Runs | Sustained | Transient | Never | Median Episodes |
| --- | --- | --- | --- | --- | --- |
| schema0_no_contraction | 1 | 0 | 1 | 0 |  |
| schema1_noisy_rate_one_drop | 1 | 0 | 1 | 0 |  |

Reader translation:

- `schema0_no_contraction` executed successfully, averaged about `12.986` total
  reward, and reached only transient threshold hits at `13.0`.
- `schema1_noisy_rate_one_drop` executed successfully, averaged about `12.871`
  total reward, used both tier 0 and tier 1, and also reached only transient
  threshold hits at `13.0`.

## Pair Summary

| Candidate Group | Seed | Pair Status | Delta | Blocked |
| --- | --- | --- | --- | --- |
| counterpoint_symbolic_n3_small_v001-p001_over_144-schema0 | seed-7fe8666539580bdb | blocked_or_non_sustained |  | True |

The blank delta is meaningful: it is not zero and it is not missing. It means
the delta is undefined because both arms failed the sustained-hit criterion.

## Claim Summary

| Claim Status | Pairs | Unblocked | Schema1 Faster | Schema1 Slower |
| --- | --- | --- | --- | --- |
| claim_blocked | 1 | 0 | 0 | 0 |

Allowed claim: this run is useful evidence about the `13.0` threshold boundary
under a tiny smoke budget.

Blocked claim: this run does not show that either schema learns faster to a
sustained threshold.

## Evidence Files

- `evaluation_aggregate_table.csv`: aggregate execution and reward evidence.
- `results/first_sustained_hit_summary.csv`: hit-status evidence.
- `results/paired_schema_comparison.csv`: comparison-claim gate.
- `results/threshold_window_summary.csv`: persistence-window evidence.
