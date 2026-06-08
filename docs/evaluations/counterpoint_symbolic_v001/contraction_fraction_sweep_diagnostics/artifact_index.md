# Artifact Index

## Public Beta Artifact Storage

Raw event-level traces and generated run trees referenced below are not tracked in git for the public beta. They are preserved in the release asset bundle:

- Mode: `github_release_asset`
- Release tag target: `v0.1.0-beta.1`
- Asset: `big_boy_calibration_smoke_v0.1.0-beta.1_artifacts.tar.zst`
- Manifest: `docs/design/beta_public_release/release_asset_manifests/ARTIFACT_BUNDLE_MANIFEST.json`
- File index: `docs/design/beta_public_release/release_asset_manifests/ARTIFACT_BUNDLE_FILE_INDEX.csv`
- Checksums: `docs/design/beta_public_release/release_asset_manifests/SHA256SUMS.txt`

Paths containing `artifacts/` are bundle-relative raw artifact paths. Human-readable reports, compact summaries, badges, methods, runbooks, and these artifact indexes remain in git.


This readout surface is generated from repo-resident artifacts, not from a temporary artifact root.

Primary binding:

- `readout_source.json`: maps this repo readout surface to the source evaluation root and expected files.

Core evidence tables:

- `results/schema_fraction_summary.csv`: scheduled edge counts and fraction widths.
- `results/tower_shape_summary.csv`: tier state-cell shape, active action-cell counts, and raw historical action-record counts.
- `results/endpoint_coalescence_summary.csv`: repeated endpoint-coalescence diagnostics for the scheduled block.
- `results/collapse_threshold_summary.csv`: first full collapse, first near collapse, last nontrivial numerator, and sweep verdict.
- `results/legacy_one_third_equivalence_summary.csv`: `6/18` equivalence against the old first one-third block.
- `results/concrete_step_summary.csv`: concrete episode-step evidence.
- `results/tier_executability_summary.csv`: live executable tier evidence.

Source evaluation root:

```text
<repo-root>/docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/artifacts/smoke_001/evaluations/counterpoint_contraction_fraction_sweep_diagnostics_v001
```
