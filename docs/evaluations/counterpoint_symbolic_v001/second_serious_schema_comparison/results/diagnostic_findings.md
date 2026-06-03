# Diagnostic Findings

- Claim status `claim_blocked`: all pairs are blocked or non-sustained, so no
  speed-to-hit claim is supported.

## Primary Diagnostic

At threshold `13.0`, both arms are `transient_hit_only`.

This means the runs did cross the threshold at least once, but no 5-episode
window contained the required 4 threshold hits. The decisive evidence is in
`results/first_sustained_hit_summary.csv` and `results/threshold_window_summary.csv`.

## Persistence-Window Evidence

- `schema0_no_contraction` reached at most 3 hits in a 5-episode window, short
  of the required 4.
- `schema1_noisy_rate_one_drop` reached at most 1 hit in a 5-episode window,
  short of the required 4.

Because neither arm reached sustained adequacy, `results/paired_schema_comparison.csv`
correctly marks the pair as `blocked_or_non_sustained`.

## Structural And Tower Evidence

This is not a full-collapse or lift-failure result.

- Schema 0 has a single tier with 108 state cells and 1140 active action cells.
- Schema 1 has tier 0 with 108 state cells and tier 1 with 100 state cells.
- Schema 1's largest tier-1 state-cell share is about `0.0185`, so the first
  contraction is not a near-universal collapse.
- Schema 1 recorded controller activity on both tier 0 and tier 1.
- `lift_success_by_tier.csv` records successful lift/action-realization events
  and no failure reason for either schema.

The blocked claim is therefore best read as a threshold-persistence boundary,
not as an environment execution failure.

## What This Does Not Show

This run does not show Schema 1 losing, Schema 0 winning, or either schema
being generally superior. With only one candidate, one replicate, and eight
episodes, it is a diagnostic threshold probe. A serious comparison would need a
larger candidate set, more replicates, and a pre-locked threshold policy.
