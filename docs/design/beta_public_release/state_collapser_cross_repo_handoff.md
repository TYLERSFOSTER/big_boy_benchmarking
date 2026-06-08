# state_collapser Cross-Repo Handoff

Status: draft handoff note. This file is for `state_collapser` engineers and
does not edit the `state_collapser` repository.

## Purpose

`big_boy_benchmarking` is the official calibration and benchmarking companion
repository for `state_collapser`.

The first public beta should be linked from `state_collapser` as the place to
inspect downstream environment calibration, smoke evidence, artifact contracts,
and human-readable reports.

## Current BBB Public Framing

Current component:

```text
Big Boy Calibration / Smoke
```

Future component:

```text
Benchmarking
```

The public release should not describe BBB as already containing final
claim-bearing benchmarks. The correct message is that BBB contains serious
calibration/smoke machinery and the initial evidence base for later benchmark
claims.

## Compatibility Note

Current BBB reports assume:

```text
state_collapser v0.7.2
```

or newer compatible pointwise liftability semantics.

This matters because several Counterpoint and PlateSupport evaluations were
designed around the corrected pointwise liftability behavior that followed from
the BBB-discovered lift issue.

## Suggested state_collapser README Wording

```markdown
For downstream calibration, smoke evaluations, artifact contracts, and
human-readable benchmark reports, see the companion repository:

https://github.com/TYLERSFOSTER/big_boy_benchmarking

The initial BBB public beta is framed as Big Boy Calibration / Smoke. It
contains Counterpoint and PlateSupport environment/evaluation reports that
exercise `state_collapser` tower construction, pointwise liftability, artifact
generation, and early tower-vs-direct comparison surfaces.
```

## Release Asset Note

BBB keeps human-readable reports and compact summaries in git. Raw generated
run trees and event-level traces are externalized into the BBB release asset:

```text
big_boy_calibration_smoke_v0.1.0-beta.1_artifacts.tar.zst
```

The local manifest and checksum files live in:

```text
docs/design/beta_public_release/release_asset_manifests/
```

## Actions For state_collapser Engineers

- Link to BBB after the BBB repository is public.
- Mention the BBB beta as calibration/smoke, not final benchmark proof.
- Keep `state_collapser v0.7.2` pointwise liftability semantics as the minimum
  relevant compatibility reference for current BBB reports.
- Do not copy raw BBB artifact trees into `state_collapser`; link to BBB
  reports and release assets instead.
