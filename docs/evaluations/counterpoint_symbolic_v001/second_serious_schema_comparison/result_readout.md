# Result Readout

The repaired full-iterated run completed artifacts and built the requested
multi-tier Schema 1 tower:

```text
[108, 54, 27, 19, 14]
```

The paired learning comparison is still blocked at `R = 13.0`.

| Schema arm | Tower source | Hit status | Mean reward | Concrete steps | Learner updates |
| --- | --- | --- | --- | --- | --- |
| `schema0_no_contraction` | total graph / no drop | `transient_hit_only` | `12.9865` | `64` | `80` |
| `schema1_noisy_rate_one_drop` | full iterated noisy-rate tower | `never_hit` | `3.0736` | `16` | `128` |

The pair has `claim_blocked=True`. No speed-to-hit delta is computed because
neither arm produced a sustained-hit episode.
