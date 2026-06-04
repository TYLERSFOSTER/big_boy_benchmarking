# Threshold Policy Readout

Policy:

```text
episode_total_reward >= 13.0
4 hits in a rolling 5-episode window
```

Observed:

| Schema arm | First hit | Best window hit count | Required | Hit status |
| --- | --- | --- | --- | --- |
| `schema0_no_contraction` | episode `0` | `3` | `4` | `transient_hit_only` |
| `schema1_noisy_rate_one_drop` | none | `0` | `4` | `never_hit` |

The result blocks the paired speed comparison.
