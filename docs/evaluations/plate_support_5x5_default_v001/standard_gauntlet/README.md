# PlateSupport Standard Gauntlet

![Suite: Limited Signal](badges/suite_status.svg)
![Artifacts: Complete](badges/artifacts_complete.svg)
![Structure: Complete](badges/structural_readiness.svg)
![Candidate: Found](badges/schema_candidates.svg)
![Training: Clean](badges/training_health.svg)
![Target: Calibrated](badges/target_calibrated.svg)
![Paired: Positive Signal](badges/paired_comparison.svg)
![Provenance: Repo Artifacts](badges/provenance_repo_artifacts.svg)
![Iterated: Candidate](badges/iterated_candidate.svg)
![Tiers: 17/18](badges/iterated_tiers.svg)

## Result

Stages 1-7 completed. Stage 6 produced bounded paired comparison status `paired_comparison_positive_signal`, and Stage 7 produced the human readout/system-learning surface.

Under this smoke Stage 6 budget, the selected tower candidate shows a limited positive target-hit signal relative to the direct baseline.

The target metric is Stage 5 binary goal success. Other metrics can explain the run, but they do not reverse the Stage 6 target claim.

## Key Numbers

- Valid states: `89`
- Shortest path length: `6`
- Random-policy success rate: `0.024`
- Stage 6 counter-signal: Tower mean reward was -27.2109375 versus direct -78.71875; tower invalid moves were 0 versus direct 2142.

## Stage Status

| Stage | Name | Status | Claim Status |
| --- | --- | --- | --- |
| 1 | structural_and_tower_diagnostics | complete | diagnostic_complete |
| 2 | contraction_schema_sweep | complete | diagnostic_complete |
| 3 | candidate_discovery | complete | candidate_found |
| 4 | tower_training_health | complete | trainable_clean |
| 5 | threshold_frontier_calibration | complete | threshold_calibrated |
| 6 | paired_replicate_comparison | complete | paired_comparison_positive_signal |
| 7 | readout_and_system_learning | complete | readout_complete |

## Artifact Provenance

- Readout source: `/Users/foster/big_boy_benchmarking/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json`
- Raw artifact root: `/Users/foster/big_boy_benchmarking/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/iterated_001`
- Suite evaluation root: `/Users/foster/big_boy_benchmarking/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/iterated_001/evaluations/plate_support_standard_gauntlet_v001`

## Claim Boundary

bounded paired smoke comparison under the Stage 5 target and budget; not a general tower-performance claim

## Clarifying Turns

### Evaluator Turn 1

_Add evaluator question or concern here._

### Codex Turn 1

_Add Codex response here._
