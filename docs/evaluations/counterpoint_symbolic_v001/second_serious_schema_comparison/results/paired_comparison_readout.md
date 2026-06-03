# Paired Comparison Readout

| Candidate Group | Seed | Pair Status | Delta | Blocked |
| --- | --- | --- | --- | --- |
| counterpoint_symbolic_n3_small_v001-p001_over_144-schema0 | seed-7fe8666539580bdb | blocked_or_non_sustained |  | True |

## Interpretation

This pair is blocked because both arms are `transient_hit_only`. The empty
delta cell is therefore not a tie. It means the speed-to-sustained-hit
quantity is undefined for this artifact set.

For this comparison to become unblocked, both arms must have
`hit_status = sustained_hit` in `results/first_sustained_hit_summary.csv`.
Only then can `schema1_minus_schema0_episodes_to_hit` be interpreted as faster,
slower, or same-time.
