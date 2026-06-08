# Beta Public Release Design

This folder tracks the work needed to prepare `big_boy_benchmarking` for its
initial public beta release as the official benchmarking repository for
`state_collapser`.

The intended public framing is:

```text
Big Boy Calibration / Smoke
```

for the current environments, diagnostics, evaluation readouts, and PlateSupport
standard gauntlet, followed by a future:

```text
Benchmarking
```

component for larger, claim-bearing benchmark runs.

## Documents

- `01_001_initial_beta_public_release_readiness.md`: initial discussion and PO
  decisions/replies.
- `01_002_beta_public_release_readiness_blueprint.md`: detailed release
  readiness blueprint.
- `01_003_beta_public_release_readiness_implementation_workplan.md`:
  Phase.Stage.Action execution plan.
- `01_004_beta_public_release_readiness_implementation_log.md`: live execution
  log and resume anchor.
- `v0.1.0-beta.1_release_notes_draft.md`: draft release notes for PO review.
- `state_collapser_cross_repo_handoff.md`: suggested handoff language and
  compatibility notes for `state_collapser` engineers.

## Work Areas

- `release_inventory/`: public-entry, artifact, and hygiene inventory.
- `release_asset_manifests/`: local manifests, file index, checksums, and
  README for beta release artifact bundles.

## Release Boundary

This folder prepares the public beta. It does not by itself authorize:

- rewriting git history;
- moving or deleting the root TeX paper;
- publishing to PyPI;
- tagging a release;
- uploading GitHub release assets;
- making the GitHub repository public;
- editing `state_collapser` directly.
