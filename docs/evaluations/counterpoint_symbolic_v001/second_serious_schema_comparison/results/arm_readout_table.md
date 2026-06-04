# Arm Readout Table

| Schema arm | Human label | Tower shape | Hit status | Mean reward | Main interpretation |
| --- | --- | --- | --- | --- | --- |
| `schema0_no_contraction` | Total graph / no-drop control | `[108]` | `transient_hit_only` | `12.9865` | Runs correctly but does not meet the sustained threshold rule. |
| `schema1_noisy_rate_one_drop` | Full iterated `1/18` noisy-rate tower | `[108,54,27,19,14]` | `never_hit` | `3.0736` | The repaired multi-tier tower runs, but never crosses `R = 13.0` in this budget. |
