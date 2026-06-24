# Evaluations

Checked-in files in this folder are repo-side human-readable evaluation
readout surfaces. Machine-readable artifacts remain the execution source of
truth; these reports are the public interpretation layer.

Current public beta component:

```text
Big Boy Calibration / Smoke
```

## Readout Command

Use the explicit protocol-file command against a checked-in
`readout_source.json`:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/<environment>/<evaluation>/readout_source.json
```

Do not point the protocol at "last run" or at an arbitrary artifact folder.

## Artifact Policy

For the beta release, human-readable reports, badges, methods, runbooks,
artifact indexes, compact summaries, and root `readout_source.json` files stay
in git. Large raw run trees and event-level artifacts have been externalized to
the local release-asset bundle described in
`docs/design/beta_public_release/release_asset_manifests/`.

## Counterpoint Symbolic v001

| Evaluation | Status | Readout | Claim boundary |
| --- | --- | --- | --- |
| first serious learning | Complete structural-limit diagnostic | [README](counterpoint_symbolic_v001/first_serious_learning/README.md) | Harness/readout/direct-baseline evidence; no general tower-performance claim. |
| one-third schema tower diagnostics | Complete structural-limit diagnostic | [README](counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/README.md) | Source-local one-third collapse behavior; no learning-performance claim. |
| contraction fraction sweep diagnostics | Complete structural diagnostic | [README](counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/README.md) | `n/18` source-local contraction behavior; no learning-performance claim. |
| noisy-rate contraction diagnostics | Complete structural diagnostic | [README](counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/README.md) | Edge-global noisy-rate candidate discovery on the widened fixture; no direct comparison claim. |
| noisy-rate full-tower training diagnostic | Complete tower-only training-health diagnostic | [README](counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/README.md) | Selected candidates can be trained under pointwise liftability; no direct comparison claim. |
| second serious schema comparison | Complete bounded comparison surface | [README](counterpoint_symbolic_v001/second_serious_schema_comparison/README.md) | Matched Schema 0 versus Schema 1 machinery and narrow calibration-scale evidence. |
| threshold frontier probe | Complete next-measure probe | [README](counterpoint_symbolic_v001/threshold_frontier_probe/README.md) | Small Schema 1 post-hit margin pattern; no broad dominance claim. |
| small paired replicate probe | Complete next-measure probe | [README](counterpoint_symbolic_v001/small_paired_replicate_probe/README.md) | Seed-paired machinery and weak positive margin pattern; no statistical significance claim. |

## PlateSupport 5x5 Default v001

| Evaluation | Status | Readout | Claim boundary |
| --- | --- | --- | --- |
| standard gauntlet | Complete correction gauntlet with bounded positive smoke signal | [README](plate_support_5x5_default_v001/standard_gauntlet/README.md) | One selected iterated tower candidate beats direct on one calibrated binary-success target and shows a coherent invalid-move/reward counter-signal; not a general PlateSupport benchmark claim. |
| direct-star cul-de-sac control | Complete diagnostic control | [README](plate_support_5x5_default_v001/direct_star_culdesac_control/README.md) | Tests Abdul Malik's cul-de-sac concern by comparing raw direct, one-step guarded direct, and the selected tower candidate; diagnostic only. |
| tower-star guarded lift comparison | Complete diagnostic control with inconclusive small-margin smoke result | [README](plate_support_5x5_default_v001/tower_star/README.md) | Compares direct-star controls against tower lift-candidate star controls; current smoke run is tied on the primary target and does not resolve a tower advantage. |

## Warehouse Gridlock v001

| Evaluation | Status | Readout | Claim boundary |
| --- | --- | --- | --- |
| environment readiness | Complete environment readiness surface | [README](warehouse_gridlock_001/environment_readiness/README.md) | SVG-derived 16x16 multi-robot/box environment is implemented and smoke-checked; no learning claim. |
| masked direct vs live-lift tower | Complete control-surface smoke | [README](warehouse_gridlock_001/masked_direct_vs_live_lift_tower/README.md) | Both arms use admissibility masks; tower uses live-lift state filtering; not a trainable PPO comparison. |
| full-state policy comparison | Complete trainable-policy contract smoke | [README](warehouse_gridlock_001/full_state_policy_comparison/README.md) | Establishes full-state/full-action policy surface and replayability; early model is intentionally simple. |
| transformer policy | Complete transformer-policy smoke | [README](warehouse_gridlock_001/transformer_policy/README.md) | Establishes transformer-policy mechanics and selected trace retention; not full-tower PPO. |
| full-tower GPU PPO | Complete CPU smoke for full-tower PPO machinery | [README](warehouse_gridlock_001/full_tower_gpu_ppo/README.md) | Direct/no-contraction and tower/nontrivial arms share PPO machinery; smoke proves real PPO updates and replayability, not a serious GPU benchmark result. |
