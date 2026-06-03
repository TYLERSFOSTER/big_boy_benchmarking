# Arm Readout Table

This table translates the schema ids into reader-facing roles and threshold
outcomes for the current `r000_001` artifact set.

| Schema | Runs | Sustained | Transient | Never | Median Episodes |
| --- | --- | --- | --- | --- | --- |
| schema0_no_contraction | 1 | 0 | 1 | 0 |  |
| schema1_noisy_rate_one_drop | 1 | 0 | 1 | 0 |  |

| Schema | Reader Label | Role | Mean Total Reward | Concrete Steps | Lift Successes | Threshold Interpretation |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `schema0_no_contraction` | No-contraction control | Matched control arm in the active-tier harness | 12.986 | 64 | 64 | Crossed `13.0` transiently, did not sustain |
| `schema1_noisy_rate_one_drop` | One-drop noisy-rate candidate | Candidate quotient schema selected from prior noisy-rate diagnostics | 12.871 | 64 | 64 | Crossed `13.0` transiently, did not sustain |

Neither arm has a median episodes-to-sustained-hit value because neither arm
produced a sustained hit.
