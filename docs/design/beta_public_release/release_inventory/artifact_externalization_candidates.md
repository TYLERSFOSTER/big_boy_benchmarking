# Artifact Externalization Candidates

This file records the initial release-asset classification for beta public
release preparation.

## Candidate Roots

Candidate roots for release asset bundling:

- `docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/artifacts`
- `docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts`
- `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/artifacts`
- `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts`
- `docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts`
- `docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts`
- `docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts`
- `docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts`
- `docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts`

## Public In-Git Surfaces To Preserve

Do not remove these public surfaces during artifact externalization:

- `docs/evaluations/**/README.md`
- `docs/evaluations/**/result_readout.md`
- `docs/evaluations/**/artifact_index.md`
- `docs/evaluations/**/method.md`
- `docs/evaluations/**/runbook.md`
- `docs/evaluations/**/glossary.md`
- `docs/evaluations/**/badges/*.svg`
- `docs/evaluations/**/results/*.md`
- `docs/evaluations/**/readout_source.json`

## Externalization Rule

For beta, externalize raw artifacts only after:

1. the artifact appears in the release asset manifest;
2. the bundle contains the artifact;
3. checksums verify;
4. public readouts point to release asset storage;
5. top-level public summaries remain available in git.

