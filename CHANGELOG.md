# Changelog

All notable public-beta changes for Big Boy Benchmarking are tracked here.

## Unreleased

- Keep public release actions manual: no tag, upload, public visibility change,
  or PyPI publication has happened as part of release-readiness work.
- Continue using this repository as an open-lab design and calibration surface
  for `state_collapser`.

## v0.1.0-beta.1

Planned source-first public beta.

### Scope

- Introduces the current `Big Boy Calibration / Smoke` component.
- Frames claim-bearing `Benchmarking` as future work.
- Publishes two environment families:
  - Counterpoint Symbolic v001.
  - PlateSupport 5x5 Default v001.
- Publishes human-readable reports for Counterpoint diagnostic and learning
  probes.
- Publishes the PlateSupport standard gauntlet readout as the strongest current
  smoke signal.

### Artifact Storage

- Human-readable reports, compact summaries, badges, methods, runbooks, and
  readout sources remain in git.
- Raw event-level traces and generated run trees are externalized to the local
  release asset bundle described in
  `docs/design/beta_public_release/release_asset_manifests/`.

### Known Limitations

- The current release is not a final benchmark suite.
- Counterpoint evidence is useful but mostly small-signal calibration work.
- PlateSupport provides the clearest current smoke signal for tower-guided
  behavior, but it is still bounded calibration evidence.
- Release assets still need Project Owner review before upload.
- PyPI publication is deferred.
