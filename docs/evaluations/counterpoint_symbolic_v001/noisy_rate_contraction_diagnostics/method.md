# Method

Evaluation id: `counterpoint_noisy_rate_contraction_diagnostics_v001`.

The diagnostic runs the existing counterpoint hidden graph with one scheduled noisy-rate contraction block per rate arm.
The selector is edge-global and threshold-based. It does not guarantee at least one selected outgoing edge per source.

Current scope: `smoke`.
Instances: `counterpoint_symbolic_n3_small_v001`.
Rates: `1/144`, `1/36`, `1/18`.
Schema seeds: `0`, `1`, `2`.
Selector rule id: `counterpoint_sha256_edge_threshold_v001`.
Replicates per schema seed: `1`.
Episodes per replicate: `1`.
Linearization mode: `tensor_available_disabled`.

Current artifact run label:

```text
smoke_001
```
