# Big Boy Calibration / Smoke Artifact Bundle

Release tag target: `v0.1.0-beta.1`

Asset name: `big_boy_calibration_smoke_v0.1.0-beta.1_artifacts.tar.zst`

This local release-asset bundle contains raw generated evaluation artifact
trees that were removed from the public git tree for beta release readiness.
The public repository keeps human-readable reports, compact summaries, badges,
methods, runbooks, and readout sources in git.

Compatibility target: `state_collapser 0.7.2` or newer compatible
pointwise liftability semantics.

## Contents

- Artifact roots: 9
- Files: 4207
- Raw bytes before compression: 400304242
- Bundle SHA256: `b0fd6be1d30abaad25d5a02a308a44d6f52e3ac409c99f735150d408b94d4090`

The bundle preserves each artifact tree at its original repo-relative path, for
example `docs/evaluations/.../artifacts/...`.

## Verification

From the repository root after downloading the release asset:

```bash
shasum -a 256 big_boy_calibration_smoke_v0.1.0-beta.1_artifacts.tar.zst
```

Compare the result with `SHA256SUMS.txt` and
`docs/design/beta_public_release/release_asset_manifests/ARTIFACT_BUNDLE_MANIFEST.json`.

## Relationship To Public Readouts

Public readouts use `artifact_storage.mode = github_release_asset` to indicate
that raw event-level traces and run trees are external release assets, not
tracked git files. Compact human-readable results remain in
`docs/evaluations/`.

No tag, upload, or public repository visibility change is performed by this
bundle build step.

GitHub release-asset constraints were checked against the official GitHub Docs
on 2026-06-08. The bundle is approximately 12.5 MiB, comfortably below the
documented per-file release asset limit.
