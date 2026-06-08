# Beta Public Release Readiness Implementation Log

## Status

Status: in progress.

Workplan:

```text
docs/design/beta_public_release/01_003_beta_public_release_readiness_implementation_workplan.md
```

Blueprint:

```text
docs/design/beta_public_release/01_002_beta_public_release_readiness_blueprint.md
```

## Phase 0 Baseline

### Phase 0.Stage 1 - Authority

Execution instruction received from the Project Owner:

```text
execute `docs/design/beta_public_release/01_003_beta_public_release_readiness_implementation_workplan.md`
```

Controlling documents re-read or consulted:

```text
docs/design/beta_public_release/01_003_beta_public_release_readiness_implementation_workplan.md
docs/design/beta_public_release/01_002_beta_public_release_readiness_blueprint.md
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
docs/prime_directive/common_failure_mode_005_umbrella_workplan_fragmentation.md
docs/prime_directive/git_practices.md
```

Decision locks:

- Current public component: `Big Boy Calibration / Smoke`.
- Future component: `Benchmarking`.
- Repository role: separate official benchmarking/calibration repo for
  `state_collapser`.
- Public posture: open-lab notebook with release guardrails.
- Public profanity redaction token: `[XXX]`.
- Beta release mode: source-first GitHub beta; PyPI deferred.
- Release tag target: `v0.1.0-beta.1`.
- `state_collapser` compatibility target: `v0.7.2` or newer compatible
  pointwise liftability semantics.
- Artifact strategy: keep readable reports and compact summaries in git; move
  large raw artifacts to release assets.

Open decisions that remain intentionally unsettled:

- Full git-history redaction versus current-tree redaction only.
- Root TeX paper public-beta disposition.
- Exact release asset format until local packaging and current GitHub release
  constraints are verified.
- Whether to add `CITATION.cff` for beta.

### Phase 0.Stage 2 - Git Baseline

Starting branch:

```text
main
```

Base commit:

```text
063db017da4dbe2e831c469f0455264ef79d0b1e
```

Starting status before branch creation:

```text
A  docs/design/beta_public_release/01_001_initial_beta_public_release_readiness.md
A  docs/design/beta_public_release/01_002_beta_public_release_readiness_blueprint.md
A  docs/design/beta_public_release/01_003_beta_public_release_readiness_implementation_workplan.md
A  docs/design/beta_public_release/README.md
```

Implementation branch created:

```text
codex/beta-public-release-readiness
```

### Phase 0.Stage 3 - Release Work Areas

Created release work areas:

```text
docs/design/beta_public_release/release_inventory/
docs/design/beta_public_release/release_asset_manifests/
dist/release-assets/v0.1.0-beta.1/
```

This implementation log is the resume anchor for the workplan.

## Phase 1 Inventory

### Phase 1.Stage 1 - Public Entry Points

Completed initial public entry-point scan.

Present:

- `README.md`
- `CONTRIBUTING.md`
- `LICENSE`
- `.gitignore`
- `pyproject.toml`
- `docs/README.md`
- `docs/evaluations/README.md`
- `docs/environments/README.md`
- `docs/design/beta_public_release/README.md`

Missing or not found:

- `CHANGELOG.md`
- `SECURITY.md`
- `docs/design/README.md`

Inventory written:

```text
docs/design/beta_public_release/release_inventory/phase1_inventory.md
```

### Phase 1.Stage 2 - Artifact Weight

Measured:

- `docs/evaluations`: 394M.
- `docs/evaluations/counterpoint_symbolic_v001`: 300M.
- `docs/evaluations/plate_support_5x5_default_v001`: 94M.
- `docs/evaluations`: 4435 files.
- `docs/evaluations/**/artifacts/**`: 4207 files.
- Artifact trees contain 45 files over 1M.

Initial externalization candidate inventory written:

```text
docs/design/beta_public_release/release_inventory/artifact_externalization_candidates.md
```

### Phase 1.Stage 3 - Hygiene Risks

Initial scan results:

- 463 files contain machine-local absolute path strings.
- 7 files contain raw profanity or common typo variants requiring `[XXX]`
  public redaction.
- Placeholder/readout scan found generated placeholder turn pads and ambiguous
  older readout command strings.
- Tracked byproduct found: `assets/images/.$diagrams.xml.bkp`.
- Local untracked byproducts include `.DS_Store` files and Python
  `__pycache__` directories.

## Phase 2 Release Hygiene Tooling

### Phase 2.Stage 1 - Release Hygiene Script

Added:

```text
scripts/release_hygiene.py
tests/test_release_hygiene.py
```

The script checks:

- tracked local/build byproducts;
- large tracked artifacts;
- machine-local absolute paths in public text surfaces;
- public redaction requirements using `[XXX]`;
- generated readout placeholders;
- ambiguous artifact-table readout command forms.

Focused tests passed:

```text
uv run pytest tests/test_release_hygiene.py
```

Result:

```text
4 passed
```

Baseline full-tree hygiene run:

```text
uv run python scripts/release_hygiene.py --repo-root .
```

Result:

```text
release hygiene failed: 4338 issue(s)
```

This failure is expected before path normalization and artifact externalization.
The largest known categories are machine-local provenance paths inside docs and
readout sources, large tracked artifact files, and one tracked backup
byproduct.

### Phase 2.Stage 2 - Ignore Rules

Updated `.gitignore` for additional TeX sidecars and local office/editor backup
files.

## Phase 3 Public Documentation Reframe

### Phase 3.Stage 1 - Root README

Updated `README.md` as the public beta front door.

The README now states:

- `big_boy_benchmarking` is the official benchmarking/calibration repository
  for `state_collapser`;
- the current component is `Big Boy Calibration / Smoke`;
- the future component is `Benchmarking`;
- the current public beta is source-first;
- current evidence is bounded and does not claim general tower superiority;
- Counterpoint and PlateSupport are the current environment families;
- PlateSupport standard gauntlet is the clearest current bounded positive smoke
  signal;
- raw artifacts are external release-asset material, not tracked git payload.

### Phase 3.Stage 2 - Top-Level Docs Indexes

Updated:

```text
docs/README.md
docs/evaluations/README.md
docs/environments/README.md
docs/design/README.md
docs/design/beta_public_release/README.md
```

These indexes now describe the environment/evaluation/readout workflow and
public open-lab posture.

### Phase 3.Stage 3 - Open-Lab Context

Public-facing design indexes now identify design docs as open-lab engineering
memory. The release-readiness work did not invent Project Owner turns or
rewrite historical attribution.

## Phase 4 Public Readout And Protocol Cleanup

### Phase 4.Stage 1 - Protocol Updates

Updated:

```text
docs/prime_directive/artifact_table_to_readable_document_protocol.md
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/README.md
```

Added:

```text
docs/prime_directive/public_release_readiness_protocol.md
```

The workplan named
`docs/prime_directive/evaluation_build_and_readout_material_protocol.md`, but
that file does not exist in this repo. The active superseding protocol is
`docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`,
which was updated instead.

### Phase 4.Stage 2 - Generated Readout Surface Cleanup

Updated generated readout defaults in Counterpoint docs writers so new public
readouts do not emit empty `> ...` Project Owner/Codex turn pads.

Cleaned existing public evaluation READMEs to replace empty placeholder turn
slots with explicit public no-active-turn text.

Final checks:

```text
rg -n "> \.\.\.|_Open\._" docs/evaluations/counterpoint_symbolic_v001 docs/evaluations/plate_support_5x5_default_v001
```

No matches remained after cleanup.

## Phase 5 Path Portability And Source Changes

### Phase 5.Stage 1 - Source-Level Path Writers

Normalized machine-local path classes in public docs and readout surfaces:

```text
BBB checkout root -> <repo-root>
state_collapser checkout root -> <state-collapser-repo>
rl_counterpoint checkout root -> <rl-counterpoint-repo>
temporary artifact root -> <tmp-dir>
private temporary/cache root -> <private-var-dir>
user cache root -> <local-cache>
```

to public placeholders such as:

```text
<repo-root>
<state-collapser-repo>
<tmp-dir>
<private-var-dir>
<local-cache>
```

Then repaired executable source writers so runtime dependency manifests do not
emit literal `<repo-root>` as code data. Runtime manifest `repo_state` now uses:

```text
runtime_repository_root
```

with an explicit path policy stating that absolute local paths are omitted from
portable artifact manifests.

### Phase 5.Stage 2 - Loader Compatibility

Updated PlateSupport Stage 1 readiness-source loading to resolve public
`<repo-root>/...` paths against the supplied `repo_root`. This keeps public
readout sources portable while preserving runtime validation.

## Phase 6 Artifact Bundle Preparation

### Phase 6.Stage 1 - Build Release Asset Staging

Added:

```text
scripts/build_release_artifact_bundle.py
```

Built local release asset:

```text
dist/release-assets/v0.1.0-beta.1/big_boy_calibration_smoke_v0.1.0-beta.1_artifacts.tar.zst
```

Bundle result:

```json
{
  "artifact_files": 4207,
  "artifact_roots": 9,
  "bundle_sha256": "b0fd6be1d30abaad25d5a02a308a44d6f52e3ac409c99f735150d408b94d4090",
  "status": "complete"
}
```

Tracked release asset metadata:

```text
docs/design/beta_public_release/release_asset_manifests/ARTIFACT_BUNDLE_MANIFEST.json
docs/design/beta_public_release/release_asset_manifests/ARTIFACT_BUNDLE_FILE_INDEX.csv
docs/design/beta_public_release/release_asset_manifests/SHA256SUMS.txt
docs/design/beta_public_release/release_asset_manifests/ARTIFACT_BUNDLE_README.md
```

GitHub release-asset constraints were checked against official GitHub Docs on
2026-06-08. The bundle is approximately 12.5 MiB, comfortably below the
documented per-file release asset limit.

Reference:

```text
https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
```

### Phase 6.Stage 2 - Readout Source Storage Metadata

Updated 15 public `docs/evaluations/**/readout_source.json` files outside raw
artifact trees with:

```json
{
  "artifact_storage": {
    "mode": "github_release_asset",
    "release_tag": "v0.1.0-beta.1",
    "asset_name": "big_boy_calibration_smoke_v0.1.0-beta.1_artifacts.tar.zst"
  }
}
```

Updated 15 public `artifact_index.md` files with a public beta artifact storage
note explaining that paths containing `artifacts/` are bundle-relative raw
artifact paths.

### Phase 6.Stage 3 - Remove Heavy Raw Artifacts From Git

Verified coverage before removal:

```json
{
  "manifest_roots": 9,
  "tracked_artifact_files": 4207,
  "missing_from_manifest_roots": 0
}
```

Removed verified raw artifact trees from git:

```text
docs/evaluations/**/artifacts/**
```

Removed tracked byproduct:

```text
assets/images/.$diagrams.xml.bkp
```

Post-removal checks:

```text
git ls-files docs/evaluations | rg '/artifacts/' | wc -l
```

Result:

```text
0
```

Size change:

```text
docs/evaluations: 394M -> 1.1M
dist/release-assets/v0.1.0-beta.1: 12M
```

## Phase 7 Package Metadata, Governance, And CI

### Phase 7.Stage 1 - Package Metadata

Updated `pyproject.toml` and `uv.lock`:

- package version: `0.1.0b1`;
- source beta description;
- project URLs;
- classifiers;
- keywords;
- retained `state-collapser[rl]` dependency pinned to GitHub tag `v0.7.2`;
- did not add a console script because the established beta entry point is
  `python -m big_boy_benchmarking.cli`.

### Phase 7.Stage 2 - Governance Files

Verified `LICENSE` exists and is MIT.

Added:

```text
CHANGELOG.md
SECURITY.md
.github/ISSUE_TEMPLATE/bug_report.md
.github/ISSUE_TEMPLATE/evaluation_readout_problem.md
.github/ISSUE_TEMPLATE/environment_proposal.md
.github/ISSUE_TEMPLATE/artifact_reproducibility_problem.md
.github/pull_request_template.md
```

### Phase 7.Stage 3 - CI

Added:

```text
.github/workflows/ci.yml
```

CI runs:

- checkout;
- install `uv`;
- `uv sync`;
- CLI help smoke;
- `uv run pytest`;
- release hygiene.

## Phase 8 Release Notes And Cross-Repo Handoff

### Phase 8.Stage 1 - Release Notes Draft

Added:

```text
docs/design/beta_public_release/v0.1.0-beta.1_release_notes_draft.md
```

The draft release notes state that no tag, upload, public visibility change, or
PyPI publication has been performed.

### Phase 8.Stage 2 - state_collapser Handoff

Added:

```text
docs/design/beta_public_release/state_collapser_cross_repo_handoff.md
```

The handoff suggests wording for `state_collapser` engineers and explicitly
does not edit the `state_collapser` repo.

## Phase 9 Verification And Release-Readiness Report

### Phase 9.Stage 1 - Verification Commands

Ran:

```bash
uv sync --group dev
uv run python -m big_boy_benchmarking.cli --help
uv run pytest
uv run pytest tests/test_release_hygiene.py
uv run python scripts/release_hygiene.py --repo-root .
shasum -a 256 -c docs/design/beta_public_release/release_asset_manifests/SHA256SUMS.txt
zstd -t dist/release-assets/v0.1.0-beta.1/big_boy_calibration_smoke_v0.1.0-beta.1_artifacts.tar.zst
uv run ruff check scripts/release_hygiene.py scripts/build_release_artifact_bundle.py tests/test_release_hygiene.py
```

Results:

- `uv sync --group dev`: passed. It removed a stray `pillow==12.2.0` from the
  local environment.
- CLI help smoke: passed.
- Full tests: passed, `292 passed in 44.02s`.
- Release hygiene: passed.
- Bundle checksums: passed.
- Bundle archive integrity: passed.
- Scoped Ruff check for new release scripts/tests: passed.

An extra non-gating command was run:

```bash
uv run ruff check .
```

It failed on broad pre-existing import-order and line-length issues outside
this release-readiness slice. Full-repo Ruff is not part of this workplan's
acceptance gates and is no longer advertised in the root README command block.

### Phase 9.Stage 2 - Public Surface Review

Checked main public Markdown links in:

```text
README.md
docs/README.md
docs/evaluations/README.md
docs/environments/README.md
docs/design/beta_public_release/README.md
```

Result:

```text
missing: []
```

Release hygiene found no tracked machine-local public paths, no raw profanity
requiring redaction, no stale ambiguous artifact-table commands, no tracked
large artifacts, and no tracked byproducts.

### Phase 9.Stage 3 - Final Checklist

Added:

```text
docs/design/beta_public_release/v0.1.0-beta.1_release_readiness_checklist.md
```

Final readiness status:

```text
Ready for Project Owner review.
```

Release actions intentionally not performed:

- no git tag created;
- no GitHub release created;
- no release asset uploaded;
- no repository visibility change made;
- no PyPI publication performed;
- no `state_collapser` edit made;
- no root TeX paper or PDF edit made;
- no git-history rewrite performed.

Final dirty status is expected to be large because the release-readiness branch
removes 4,207 tracked raw artifact files after verified bundle creation and
updates public docs/protocols/readout sources for beta portability.
