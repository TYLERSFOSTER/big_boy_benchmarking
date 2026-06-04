# Results Summary

The repaired artifact uses `schema1_tower_source=full_iterated_noisy_rate`.

Schema 1 runtime tower shape:

```text
[108, 54, 27, 19, 14]
```

This fixes the earlier wrong-scope two-tier run. The comparison remains
claim-blocked because Schema 0 is `transient_hit_only` and Schema 1 is
`never_hit` at `R = 13.0`.
