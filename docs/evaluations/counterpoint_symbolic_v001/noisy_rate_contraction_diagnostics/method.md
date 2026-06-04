# Method

Evaluation id: `counterpoint_noisy_rate_contraction_diagnostics_v001`.

The diagnostic runs the existing counterpoint hidden graph with one scheduled noisy-rate contraction block per rate arm.
The selector is edge-global and threshold-based. It does not guarantee at least one selected outgoing edge per source.

Current scope: `custom diagnostic`.
Instances: `counterpoint_symbolic_n3_wide_20_108_span18_v001`.
Rates: `1/18`.
Schema seeds: `0`.
Selector rule id: `counterpoint_sha256_edge_threshold_v001`.
Replicates per schema seed: `1`.
Episodes per replicate: `1`.
Linearization mode: `tensor_available_disabled`.

Current artifact run label:

```text
wide_span18_p001_over018_s0_001
```
