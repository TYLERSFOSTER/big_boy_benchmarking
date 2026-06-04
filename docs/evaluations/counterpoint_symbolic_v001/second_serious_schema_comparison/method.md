# Method

This run repairs the previous wrong-scope one-drop artifact by making Schema 1
use a full iterated noisy-rate tower source.

Schema 0 remains the no-drop total-graph control. Schema 1 starts from the
promoted candidate:

```text
counterpoint_symbolic_n3_small_v001-p001_over_018-schema0
```

The runner is invoked with:

```text
--schema1-tower-source full_iterated_noisy_rate
```

Tier 1 matches the one-drop source prefix `[108,54]`. Later tiers are built by
resampling representative quotient edges at the same `1/18` rate until the
process reaches a terminal tier. The observed runtime tower is:

```text
[108, 54, 27, 19, 14]
```

Budget:

| Field | Value |
| --- | --- |
| Instance | `counterpoint_symbolic_n3_small_v001` |
| Candidate | `counterpoint_symbolic_n3_small_v001-p001_over_018-schema0` |
| Schema 1 tower source | `full_iterated_noisy_rate` |
| Episodes per arm | `8` |
| Replicates per arm | `1` |
| Threshold | `episode_total_reward >= 13.0` |
| Persistence | `4_of_5` |
| Linearization | `tensor_available_disabled` |
