# Big Boy Benchmarking Beta Public Release Readiness Implementation Workplan

Status: initial implementation workplan.

This workplan is derived from:

```text
docs/design/beta_public_release/01_002_beta_public_release_readiness_blueprint.md
```

This workplan uses `Phase.Stage.Action` discipline.

This workplan is not execution approval. Execution requires an explicit Project
Owner instruction to execute this file.

## 0. Governing Rules

This workplan follows:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
docs/prime_directive/common_failure_mode_005_umbrella_workplan_fragmentation.md
docs/prime_directive/git_practices.md
```

It also follows the Prime Directive failure-mode rule requiring approved
Phase.Stage.Action workplans to be implemented as written, not silently
compressed or reinterpreted.

The workplan is law once approved for execution. During execution, do not
compress, reorder, simplify, or substitute a lighter release-prep path unless a
true stop condition occurs and the Project Owner approves a revision.

## 1. Execution Spine

This is one parent release-readiness workplan. It is not a set of independent
child jobs.

If the Project Owner asks to execute this workplan, execute the phases in order
until the release-readiness branch is complete or a true stop condition occurs.

Completion of one phase is a checkpoint, not an automatic stop.

True stop conditions:

- the Project Owner explicitly says to stop, pause, or switch topics;
- execution would require rewriting git history;
- execution would require changing, moving, or deleting the root TeX paper or
  built PDF without a fresh Project Owner decision;
- execution would delete raw artifacts before a verified artifact bundle and
  manifest exist;
- execution would edit `state_collapser` directly;
- execution would publish to PyPI;
- execution would make the GitHub repository public;
- execution would tag a release;
- execution would upload release assets;
- execution would materially change scientific claims beyond the approved
  bounded calibration/smoke framing;
- an unexpected repo state contradicts this workplan;
- a required source file is missing or has been replaced by incompatible
  content;
- a release-hygiene check reveals a public-release blocker that cannot be
  corrected under this workplan.

## 2. Decision Locks Before Implementation

The following decisions are locked by the blueprint.

### 2.1 Public Framing

Current beta component:

```text
Big Boy Calibration / Smoke
```

Future component:

```text
Benchmarking
```

The release must not claim that the current repo already contains final,
claim-bearing benchmarks.

### 2.2 Repo Role

`big_boy_benchmarking` remains separate from `state_collapser` and is framed as
the official benchmarking/calibration repository for `state_collapser`.

### 2.3 Open-Lab Posture

The docs remain public as an open-lab notebook, with guardrails.

Open-lab material should not be erased merely because it records live design
process. It should be labeled, sanitized where required, and made navigable.

### 2.4 Profanity Redaction Token

The public tracked tree uses:

```text
[XXX]
```

for profanity redaction.

Do not invent Project Owner text while redacting. Preserve attribution and
meaning.

### 2.5 Source-Only Beta

The beta is source-first on GitHub. PyPI publication is deferred unless the
Project Owner separately approves it.

### 2.6 Release Version

Release tag target:

```text
v0.1.0-beta.1
```

Package version, if changed, should align with existing Python packaging
conventions and may use:

```text
0.1.0b1
```

only if that does not conflict with existing project metadata.

### 2.7 state_collapser Compatibility

Current public reports assume:

```text
state_collapser v0.7.2
```

or newer compatible pointwise liftability semantics.

### 2.8 Artifact Strategy

Keep in git:

- human-readable readouts;
- compact summary tables;
- badges;
- methods and runbooks;
- artifact indexes;
- release manifests;
- protocols.

Move to release assets:

- raw run trees;
- large event-level traces;
- large nested artifact directories;
- per-step traces;
- large threshold-run trees.

## 3. Open Decisions Handling

These are unresolved in the blueprint. The implementation must handle them
without silently deciding them.

### 3.1 Git History Redaction Boundary

Default execution behavior:

- redact the current tracked tree;
- do not rewrite git history;
- do not claim that prior history is sanitized;
- stop if the Project Owner requires full-history sanitization.

### 3.2 Root TeX Paper Disposition

Default execution behavior:

- inspect and report root TeX-related files;
- keep existing `.tex`, `.bib`, and `.pdf` files untouched;
- remove only generated build byproducts that are clearly ignored/untracked or
  explicitly approved;
- stop before moving, deleting, editing, or reframing the TeX paper itself.

### 3.3 Artifact Bundle Format

Default execution behavior:

- prepare a local release-asset bundle using a compressed tar format if
  supported locally;
- fall back to zip if needed;
- verify current GitHub release asset constraints before final release
  packaging;
- stop before upload.

### 3.4 Citation File

Default execution behavior:

- defer `CITATION.cff`;
- mention citation guidance as a future public-release improvement unless the
  Project Owner separately approves adding a citation file now.

## 4. Expected Implementation Log

Create and maintain:

```text
docs/design/beta_public_release/01_004_beta_public_release_readiness_implementation_log.md
```

The log must record:

- branch name;
- starting git status;
- each completed `Phase.Stage.Action`;
- files changed;
- commands run;
- tests run;
- artifact bundle paths and checksums if created;
- stop conditions encountered;
- unresolved release decisions left for the Project Owner;
- final readiness status.

Do not present incomplete release readiness as complete.

## 5. Phase.Stage.Action Progress

### Phase 0 - Authority, Branch, And Baseline

#### Phase 0.Stage 1 - Verify Workplan Authority

Phase 0.Stage 1.Action 1:
Re-read this workplan, the blueprint, and the governing prime directive files.

Expected evidence:

- the implementation log names all controlling documents;
- no implementation starts from memory alone.

Stop condition:

- stop if a newer design document contradicts this workplan.

Phase 0.Stage 1.Action 2:
Confirm that execution was explicitly requested by the Project Owner.

Expected evidence:

- implementation log records the execution instruction context.

Stop condition:

- stop if there is no explicit execution instruction.

Phase 0.Stage 1.Action 3:
Record all locked decisions and all unresolved decisions from Sections 2 and 3
in the implementation log.

Expected evidence:

- log distinguishes decision locks from open decisions.

Stop condition:

- stop if any unresolved decision blocks the very first implementation step.

#### Phase 0.Stage 2 - Establish Git Safety

Phase 0.Stage 2.Action 1:
Run a git status check.

Expected evidence:

- implementation log includes current branch and dirty state.

Stop condition:

- stop if unrelated dirty files would be overwritten or confused with release
  readiness work.

Phase 0.Stage 2.Action 2:
Create or switch to:

```text
codex/beta-public-release-readiness
```

Expected evidence:

- branch is active before implementation edits begin.

Stop condition:

- stop if branch creation or switching would hide, overwrite, or strand
  uncommitted user work.

Phase 0.Stage 2.Action 3:
Record the base commit and branch relationship to `main`.

Expected evidence:

- implementation log records base commit hash.

Stop condition:

- stop if the branch is not based on the expected current `main` without
  explicit Project Owner direction.

#### Phase 0.Stage 3 - Create Release Work Areas

Phase 0.Stage 3.Action 1:
Create release staging directories only inside the repository.

Suggested paths:

```text
docs/design/beta_public_release/release_inventory/
docs/design/beta_public_release/release_asset_manifests/
dist/release-assets/v0.1.0-beta.1/
```

Expected evidence:

- directories exist;
- implementation log explains their purpose.

Stop condition:

- stop if existing directories contain unrelated material.

Phase 0.Stage 3.Action 2:
Create the implementation log file.

Expected evidence:

- implementation log exists before further edits.

Stop condition:

- stop if log path conflicts with existing unrelated content.

### Phase 1 - Repository Inventory And Public-Release Baseline

#### Phase 1.Stage 1 - Inventory Public Entry Points

Phase 1.Stage 1.Action 1:
Inspect these public entry points:

```text
README.md
CONTRIBUTING.md
CHANGELOG.md
LICENSE
SECURITY.md
docs/README.md
docs/evaluations/README.md
docs/environments/README.md
docs/design/README.md
docs/design/beta_public_release/README.md
pyproject.toml
.gitignore
```

Expected evidence:

- inventory notes which files exist, which are stale, and which are missing.

Stop condition:

- stop if a public entry point contains conflicting release framing that needs
  a PO decision.

Phase 1.Stage 1.Action 2:
Inspect current top-level evaluation reports.

Required roots:

```text
docs/evaluations/counterpoint_symbolic_v001/
docs/evaluations/plate_support_5x5_default_v001/
```

Expected evidence:

- inventory lists current report READMEs and their statuses.

Stop condition:

- stop if a report is missing its `readout_source.json` and the public README
  would need to claim it as current.

Phase 1.Stage 1.Action 3:
Inspect current environment docs.

Required roots:

```text
docs/environments/
```

Expected evidence:

- inventory identifies Counterpoint and PlateSupport public environment docs.

Stop condition:

- stop if environment docs are absent and cannot be recreated from repo
  sources without inventing claims.

#### Phase 1.Stage 2 - Inventory Artifact Weight

Phase 1.Stage 2.Action 1:
Measure size and file counts for evaluation artifact trees.

Expected evidence:

- inventory records byte counts and file counts for `docs/evaluations/**`.
- artifact-heavy directories are ranked.

Stop condition:

- stop if artifact roots are missing but public reports point at them as
  present-in-git artifacts.

Phase 1.Stage 2.Action 2:
Classify artifact content into:

- keep in git;
- move to release asset;
- generated locally only;
- investigate before deciding.

Expected evidence:

- classification file exists under release inventory.

Stop condition:

- stop if classification would remove a file required to render current public
  reports and no replacement link/manifest exists.

Phase 1.Stage 2.Action 3:
Identify all raw run trees, event-level CSVs, threshold-run trees, and large
per-step traces.

Expected evidence:

- inventory lists candidate paths for release-asset bundling.

Stop condition:

- stop if a candidate path contains hand-authored documentation mixed with raw
  generated artifacts.

#### Phase 1.Stage 3 - Inventory Public Hygiene Risks

Phase 1.Stage 3.Action 1:
Scan public Markdown and source docs for machine-local absolute paths.

Expected evidence:

- inventory records file, line, and role of each occurrence.

Stop condition:

- stop if machine-local paths appear in fields that cannot be normalized
  without changing readout semantics.

Phase 1.Stage 3.Action 2:
Scan public tracked text for raw profanity and common typo variants without
printing the raw matched terms into new public docs.

Expected evidence:

- inventory records file and line locations needing `[XXX]` redaction.

Stop condition:

- stop if redaction would make a PO-authored correction impossible to
  understand without a new explanatory note.

Phase 1.Stage 3.Action 3:
Scan for generated placeholders and stale conversation slots.

Targets include:

- empty or dangling "Next turn" sections;
- placeholder-only `> ...` blocks;
- unexplained `_Open._` fields;
- stale "last run" references;
- ambiguous artifact-table commands.

Expected evidence:

- inventory lists files requiring cleanup.

Stop condition:

- stop if a placeholder appears to be an intentional active PO conversation
  surface.

Phase 1.Stage 3.Action 4:
Scan for build byproducts and local noise.

Targets include:

- OS metadata;
- Python caches;
- TeX build byproducts;
- backup files;
- large generated files that are not intentional public artifacts.

Expected evidence:

- inventory lists tracked and untracked byproducts separately.

Stop condition:

- stop before removing tracked TeX-related material unless it is clearly a
  build byproduct and not the `.tex`, `.bib`, or `.pdf` public artifact.

### Phase 2 - Release Hygiene Tooling

#### Phase 2.Stage 1 - Add A Release Hygiene Script

Phase 2.Stage 1.Action 1:
Create a repo-local release hygiene script.

Suggested path:

```text
scripts/release_hygiene.py
```

Required checks:

- raw profanity in public tracked docs, using obfuscated denylist construction
  so the script itself does not add raw terms to the public tree;
- machine-local absolute paths in public Markdown;
- OS metadata;
- Python caches;
- TeX byproducts except intentional `.tex`, `.bib`, and `.pdf`;
- huge artifact trees still tracked after externalization;
- missing badges referenced by public README files;
- missing `readout_source.json` for public evaluation reports.

Expected evidence:

- script exists;
- script has clear command-line output;
- script exits nonzero on release blockers.

Stop condition:

- stop if implementing the script requires writing raw profane terms into
  tracked source.

Phase 2.Stage 1.Action 2:
Add tests for the hygiene script where practical.

Suggested path:

```text
tests/test_release_hygiene.py
```

Expected evidence:

- tests cover at least path detection, placeholder detection, and byproduct
  detection.

Stop condition:

- stop if test fixtures would require adding prohibited raw text to the public
  tree.

Phase 2.Stage 1.Action 3:
Run the hygiene script against the current tree and record results.

Expected evidence:

- implementation log records baseline failures before cleanup.

Stop condition:

- stop if failures reveal a release blocker not covered by this workplan.

#### Phase 2.Stage 2 - Update Ignore Rules

Phase 2.Stage 2.Action 1:
Update `.gitignore` to cover local and build byproducts.

Expected coverage:

- OS metadata;
- Python caches;
- virtualenv/build caches;
- TeX byproducts;
- release local staging artifacts that should not be committed unless they are
  manifests.

Expected evidence:

- `.gitignore` covers known byproduct patterns;
- intentional public artifacts remain trackable.

Stop condition:

- stop if ignoring a pattern would hide required public reports or release
  manifests.

### Phase 3 - Public Documentation Reframe

#### Phase 3.Stage 1 - Root README

Phase 3.Stage 1.Action 1:
Rewrite or update `README.md` as the public beta front door.

Required content:

- project identity;
- relationship to `state_collapser`;
- beta status;
- `Big Boy Calibration / Smoke` framing;
- future `Benchmarking` framing;
- source install quickstart;
- environment summary;
- evaluation summary;
- bounded conclusions;
- what not to conclude yet;
- links to human-readable reports;
- artifact storage note;
- `state_collapser v0.7.2` compatibility note.

Expected evidence:

- README can be understood by a new public reader.
- README does not overclaim.

Stop condition:

- stop if the README would need a TeX-paper public-disposition decision to be
  truthful.

Phase 3.Stage 1.Action 2:
Verify all README report links.

Expected evidence:

- all linked paths exist.

Stop condition:

- stop if a key linked report is stale or missing and cannot be corrected under
  this workplan.

Phase 3.Stage 1.Action 3:
Ensure README examples use source-first commands only.

Expected command style:

```bash
git clone <repo-url>
cd big_boy_benchmarking
uv sync
uv run pytest
uv run python -m big_boy_benchmarking.cli --help
```

Expected evidence:

- commands do not depend on machine-local paths.

Stop condition:

- stop if install commands require unpublished private dependencies.

#### Phase 3.Stage 2 - Top-Level Docs Indexes

Phase 3.Stage 2.Action 1:
Update `docs/README.md`.

Required content:

- docs tree map;
- open-lab posture;
- three-step workflow:
  - environment design/readiness;
  - evaluation or gauntlet design;
  - artifact-table readout to human-readable reports;
- release asset note.

Expected evidence:

- public reader can navigate the docs tree.

Stop condition:

- stop if docs tree has major missing areas that require new design decisions.

Phase 3.Stage 2.Action 2:
Update `docs/evaluations/README.md`.

Required content:

- Counterpoint report index;
- PlateSupport report index;
- status column or equivalent;
- bounded conclusions;
- raw artifact storage location;
- readout regeneration command form.

Expected evidence:

- all linked evaluation READMEs exist.

Stop condition:

- stop if a report cannot be classified as current, archived, or superseded.

Phase 3.Stage 2.Action 3:
Update `docs/environments/README.md`.

Required content:

- Counterpoint Symbolic v001 summary;
- PlateSupport 5x5 Default v001 summary;
- maturity/status;
- linked evaluation families;
- `state_collapser` compatibility.

Expected evidence:

- environment docs do not imply nonexistent evaluations.

Stop condition:

- stop if environment status conflicts with root README claims.

Phase 3.Stage 2.Action 4:
Add or update `docs/design/README.md`.

Required content:

- open-lab design note;
- explanation of design discussions, blueprints, workplans, implementation
  logs, and system-learning archives;
- false-attribution caution;
- pointer to beta public release design folder.

Expected evidence:

- design docs are framed as public engineering memory, not polished product
  docs.

Stop condition:

- stop if adding this index would require rewriting historical design docs.

Phase 3.Stage 2.Action 5:
Update `docs/design/beta_public_release/README.md`.

Required content:

- readiness discussion;
- blueprint;
- workplan;
- implementation log;
- release inventory folder;
- release asset manifests folder.

Expected evidence:

- beta release design folder is self-navigable.

Stop condition:

- stop if generated paths differ from actual created paths.

#### Phase 3.Stage 3 - Open-Lab Labels And Public Context

Phase 3.Stage 3.Action 1:
Add concise open-lab context to public-facing design indexes.

Expected evidence:

- public readers are warned that design docs preserve live process and
  attribution.

Stop condition:

- stop if adding labels would require editing a PO-authored historical turn.

Phase 3.Stage 3.Action 2:
Update `docs/design/system_learning_from_evaluations/README.md` if stale.

Required content:

- system-learning purpose;
- relationship to evaluation readouts;
- link to liftability and gauntlet lessons;
- public open-lab warning.

Expected evidence:

- system-learning archive is understandable without reading chat history.

Stop condition:

- stop if system-learning folders contain unresolved active conversations that
  should not be summarized.

### Phase 4 - Public Readout And Protocol Cleanup

#### Phase 4.Stage 1 - Protocol Updates

Phase 4.Stage 1.Action 1:
Update:

```text
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

Required additions:

- explicit public-release hygiene mode;
- exact command form:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <readout_source.json>
```

- repo-relative path requirement;
- release asset bundle field handling;
- `[XXX]` redaction requirement;
- no invented PO turns;
- badge consistency requirements;
- no ambiguous "last run" semantics.

Expected evidence:

- protocol prevents the previous folder/surface ambiguity.

Stop condition:

- stop if the existing protocol structure requires a separate blueprint to
  modify safely.

Phase 4.Stage 1.Action 2:
Update:

```text
docs/prime_directive/evaluation_build_and_readout_material_protocol.md
```

Required additions:

- evaluation builders must provide human-readability source material;
- public-readout fields must include artifact storage mode;
- generated docs must avoid machine-local paths;
- generated docs must support release-asset artifact storage.

Expected evidence:

- future evaluations have enough material for public readouts.

Stop condition:

- stop if this protocol is absent or superseded by another controlling file.

Phase 4.Stage 1.Action 3:
Add a short prime-directive release-readiness note if no existing protocol owns
public release hygiene.

Suggested path:

```text
docs/prime_directive/public_release_readiness_protocol.md
```

Expected evidence:

- protocol points to release hygiene script and redaction/path rules.

Stop condition:

- stop if adding a new prime-directive file would duplicate existing protocol
  authority.

#### Phase 4.Stage 2 - Generated Readout Surface Cleanup

Phase 4.Stage 2.Action 1:
Inspect current public readout READMEs for stale placeholders, machine-local
paths, raw profanity, inconsistent badges, and ambiguous artifact locations.

Required roots:

```text
docs/evaluations/counterpoint_symbolic_v001/
docs/evaluations/plate_support_5x5_default_v001/
```

Expected evidence:

- cleanup list is recorded in release inventory.

Stop condition:

- stop if a readout is generated from missing source data and cannot be safely
  repaired manually.

Phase 4.Stage 2.Action 2:
Regenerate or manually update public readouts only from their
`readout_source.json` and approved protocols.

Expected evidence:

- no human-authored clarification section is lost or reattributed.

Stop condition:

- stop if regeneration would overwrite preserved PO/Codex conversation content.

Phase 4.Stage 2.Action 3:
Normalize badges across public readouts.

Expected evidence:

- badges use consistent visual style and all referenced files exist.

Stop condition:

- stop if a report's badge semantics are unclear and require a claim-boundary
  decision.

### Phase 5 - Path Portability And Source Changes

#### Phase 5.Stage 1 - Find Source-Level Absolute Path Writers

Phase 5.Stage 1.Action 1:
Search source and tests for machine-local path emission.

Targets:

```text
src/
tests/
docs/prime_directive/
```

Expected evidence:

- implementation log records likely path writer modules.

Stop condition:

- stop if path normalization would change artifact contract semantics.

Phase 5.Stage 1.Action 2:
Update doc writers and manifest writers to prefer repo-relative public paths.

Expected behavior:

- public Markdown uses repo-relative paths;
- manifests may retain explicitly local provenance fields;
- commands use environment variables or `<repo-root>`.

Expected evidence:

- tests or snapshots cover normalized output.

Stop condition:

- stop if a writer cannot determine repo root reliably.

Phase 5.Stage 1.Action 3:
Update tests for path normalization.

Expected evidence:

- tests fail on accidental machine-local public Markdown paths.

Stop condition:

- stop if existing tests depend on exact absolute path strings and need
  broader redesign.

#### Phase 5.Stage 2 - Regenerate Affected Public Readouts

Phase 5.Stage 2.Action 1:
Identify readouts affected by path writer changes.

Expected evidence:

- list of readouts to regenerate exists.

Stop condition:

- stop if source artifacts required for regeneration are missing.

Phase 5.Stage 2.Action 2:
Regenerate affected readouts using explicit readout-source protocol commands.

Expected evidence:

- regenerated readouts no longer contain machine-local public paths.

Stop condition:

- stop if regeneration changes scientific result interpretation.

### Phase 6 - Artifact Bundle Preparation

#### Phase 6.Stage 1 - Build Release Asset Staging

Phase 6.Stage 1.Action 1:
Create an artifact bundle staging manifest from the Phase 1 artifact
classification.

Required manifest fields:

- release tag;
- repository commit;
- `state_collapser` version;
- source evaluation family;
- artifact role;
- original repo-relative path;
- bundle-relative path;
- byte count;
- file count;
- checksum.

Expected evidence:

- manifest exists under:

```text
docs/design/beta_public_release/release_asset_manifests/
```

Stop condition:

- stop if any artifact cannot be classified.

Phase 6.Stage 1.Action 2:
Copy or archive raw artifacts into local release asset staging.

Expected staging root:

```text
dist/release-assets/v0.1.0-beta.1/
```

Expected evidence:

- staged tree mirrors manifest mappings.

Stop condition:

- stop if copy/archive operation would omit a raw artifact referenced by a
  public report.

Phase 6.Stage 1.Action 3:
Generate checksums for all staged files and bundle outputs.

Required file:

```text
SHA256SUMS.txt
```

Expected evidence:

- checksums verify locally.

Stop condition:

- stop if checksums fail or staged files change during verification.

Phase 6.Stage 1.Action 4:
Create bundle README.

Required file:

```text
ARTIFACT_BUNDLE_README.md
```

Required content:

- what is in the bundle;
- which repo release it belongs to;
- how to verify checksums;
- how paths map back to public readouts;
- compatibility note for `state_collapser`.

Expected evidence:

- bundle README is included in staging and linked from public docs.

Stop condition:

- stop if bundle README requires claims not supported by reports.

#### Phase 6.Stage 2 - Update Readout Sources For External Artifacts

Phase 6.Stage 2.Action 1:
Add artifact storage metadata to public `readout_source.json` files.

Required fields or equivalent:

```json
{
  "artifact_storage": {
    "mode": "github_release_asset",
    "release_tag": "v0.1.0-beta.1",
    "asset_name": "big_boy_calibration_smoke_v0.1.0-beta.1_artifacts.tar.zst",
    "bundle_manifest_path": "ARTIFACT_BUNDLE_MANIFEST.json"
  }
}
```

Expected evidence:

- readout sources point to release asset storage without requiring upload yet.

Stop condition:

- stop if existing readout schema rejects the field and requires code changes
  outside this workplan.

Phase 6.Stage 2.Action 2:
Update public artifact indexes to distinguish:

- in git;
- in release asset bundle;
- generated locally only;
- intentionally omitted.

Expected evidence:

- public artifact indexes no longer imply large raw artifacts remain in git.

Stop condition:

- stop if an artifact index cannot be updated without rerunning an evaluation.

#### Phase 6.Stage 3 - Remove Heavy Raw Artifacts From Git After Verification

Phase 6.Stage 3.Action 1:
Verify the release asset bundle and manifest cover every artifact selected for
externalization.

Expected evidence:

- implementation log records verification result.

Stop condition:

- stop if any selected artifact is missing from the manifest or bundle.

Phase 6.Stage 3.Action 2:
Remove verified heavy raw artifacts from the tracked public tree.

Expected behavior:

- keep human-readable reports and compact summaries;
- remove only artifacts covered by the verified release bundle;
- preserve local staged bundle.

Expected evidence:

- git status shows intended removals only.

Stop condition:

- stop if removal would delete hand-authored docs, compact public summaries, or
  unrecoverable raw data.

Phase 6.Stage 3.Action 3:
Run public readout link checks after artifact removal.

Expected evidence:

- reports still link to compact in-git material and external bundle metadata.

Stop condition:

- stop if public docs contain broken links after artifact removal.

### Phase 7 - Package Metadata, Governance, And CI

#### Phase 7.Stage 1 - Package Metadata

Phase 7.Stage 1.Action 1:
Inspect `pyproject.toml`.

Expected evidence:

- implementation log records current project metadata, dependency constraints,
  and CLI exposure.

Stop condition:

- stop if package metadata already follows a different release scheme that
  conflicts with `0.1.0b1`.

Phase 7.Stage 1.Action 2:
Update package metadata as needed for source beta.

Required or preferred metadata:

- project URLs;
- classifiers;
- dependency on `state_collapser` compatible with v0.7.2 semantics;
- dev dependencies if already using that pattern;
- CLI entry point only if already appropriate.

Expected evidence:

- package metadata supports public source install.

Stop condition:

- stop before inventing a new console script if the project has intentionally
  used `python -m big_boy_benchmarking.cli`.

Phase 7.Stage 1.Action 3:
Run package/import sanity checks.

Expected commands:

```bash
uv sync
uv run python -m big_boy_benchmarking.cli --help
uv run pytest
```

Expected evidence:

- command results are recorded.

Stop condition:

- stop on unexpected test failure and diagnose before further edits.

#### Phase 7.Stage 2 - Governance Files

Phase 7.Stage 2.Action 1:
Verify or add `LICENSE`.

Expected evidence:

- public license is present.

Stop condition:

- stop if license choice is absent and cannot be inferred safely.

Phase 7.Stage 2.Action 2:
Create or update `CHANGELOG.md`.

Required sections:

- `Unreleased`;
- `v0.1.0-beta.1`;
- beta scope;
- current environment families;
- current public evaluation families;
- artifact storage note;
- known limitations.

Expected evidence:

- changelog aligns with README claims.

Stop condition:

- stop if changelog would need a release date or tag that has not been
  approved.

Phase 7.Stage 2.Action 3:
Create or update `SECURITY.md`.

Required content:

- supported versions;
- reporting channel placeholder if final channel is unknown;
- sensitive data and artifact provenance warning.

Expected evidence:

- public security file exists without overpromising response policy.

Stop condition:

- stop if a real security contact must be supplied by the PO.

Phase 7.Stage 2.Action 4:
Create issue templates.

Suggested templates:

```text
.github/ISSUE_TEMPLATE/bug_report.md
.github/ISSUE_TEMPLATE/evaluation_readout_problem.md
.github/ISSUE_TEMPLATE/environment_proposal.md
.github/ISSUE_TEMPLATE/artifact_reproducibility_problem.md
```

Expected evidence:

- templates route public feedback to useful categories.

Stop condition:

- stop if GitHub issue policy should be disabled or externalized.

Phase 7.Stage 2.Action 5:
Create PR template.

Suggested path:

```text
.github/pull_request_template.md
```

Required prompts:

- affected environment/evaluation/protocol;
- readout regeneration;
- artifact storage mode;
- public path hygiene;
- PO attribution preservation;
- tests run.

Expected evidence:

- PR template reinforces release discipline.

Stop condition:

- stop if repo already has a conflicting PR template convention.

#### Phase 7.Stage 3 - Continuous Integration

Phase 7.Stage 3.Action 1:
Create GitHub Actions CI workflow.

Suggested path:

```text
.github/workflows/ci.yml
```

Required jobs:

- checkout;
- install `uv`;
- `uv sync`;
- CLI help smoke;
- `uv run pytest`;
- release hygiene script.

Expected evidence:

- workflow is syntactically valid.

Stop condition:

- stop if CI requires secrets or private package credentials.

Phase 7.Stage 3.Action 2:
Run local equivalents of CI commands.

Expected evidence:

- implementation log records command results.

Stop condition:

- stop on unexpected failure and diagnose before continuing.

### Phase 8 - Release Notes And Cross-Repo Handoff

#### Phase 8.Stage 1 - Release Notes Draft

Phase 8.Stage 1.Action 1:
Create release notes draft for:

```text
v0.1.0-beta.1
```

Suggested path:

```text
docs/design/beta_public_release/v0.1.0-beta.1_release_notes_draft.md
```

Required sections:

- what this release is;
- relationship to `state_collapser`;
- current component: `Big Boy Calibration / Smoke`;
- future component: `Benchmarking`;
- included environments;
- included evaluation/readout families;
- key bounded PlateSupport smoke result;
- known limitations;
- source install;
- report links;
- artifact bundle instructions;
- checksums;
- compatibility.

Expected evidence:

- release notes are ready for PO review but not published.

Stop condition:

- stop if release notes would require upload URLs that do not exist yet.

Phase 8.Stage 1.Action 2:
Ensure release notes do not claim the repo is already public, tagged, or
published.

Expected evidence:

- release notes use draft language where appropriate.

Stop condition:

- stop if release status needs a PO decision.

#### Phase 8.Stage 2 - Cross-Repo Handoff

Phase 8.Stage 2.Action 1:
Create a `state_collapser` handoff note inside this repo.

Suggested path:

```text
docs/design/beta_public_release/state_collapser_cross_repo_handoff.md
```

Required content:

- link target for BBB once public;
- current BBB role;
- `state_collapser v0.7.2` compatibility note;
- suggested README wording for `state_collapser`;
- no direct edits to `state_collapser`.

Expected evidence:

- handoff is ready for upstream engineers.

Stop condition:

- stop before editing the `state_collapser` repo.

Phase 8.Stage 2.Action 2:
Update this repo's public docs to describe the cross-repo relationship.

Expected evidence:

- root README and docs README link conceptually to `state_collapser`.

Stop condition:

- stop if the public URL for `state_collapser` is unknown and must be exact.

### Phase 9 - Verification And Release-Readiness Report

#### Phase 9.Stage 1 - Run Full Verification

Phase 9.Stage 1.Action 1:
Run tests.

Expected command:

```bash
uv run pytest
```

Expected evidence:

- test result recorded in implementation log.

Stop condition:

- stop on failure unless failure is already known and explicitly documented as
  non-blocking.

Phase 9.Stage 1.Action 2:
Run CLI smoke.

Expected command:

```bash
uv run python -m big_boy_benchmarking.cli --help
```

Expected evidence:

- command result recorded.

Stop condition:

- stop on import or CLI failure.

Phase 9.Stage 1.Action 3:
Run release hygiene script.

Expected evidence:

- hygiene script passes or records only approved non-blockers.

Stop condition:

- stop on raw profanity, machine-local public paths, missing public links, or
  tracked heavy artifact leftovers not covered by bundle decision.

Phase 9.Stage 1.Action 4:
Run artifact bundle verification.

Expected evidence:

- checksums verify;
- manifest matches staged bundle.

Stop condition:

- stop if bundle verification fails.

#### Phase 9.Stage 2 - Manual Public Surface Review

Phase 9.Stage 2.Action 1:
Review root README as a new public reader.

Checklist:

- public framing clear;
- current environments clear;
- calibration/smoke boundary clear;
- no overclaiming;
- report links work;
- artifact storage clear.

Expected evidence:

- implementation log records result.

Stop condition:

- stop if README still feels stale or misleading.

Phase 9.Stage 2.Action 2:
Review evaluation index and main report READMEs.

Checklist:

- Counterpoint reports are bounded;
- PlateSupport gauntlet report reflects current strongest smoke result;
- badges render consistently;
- external artifact storage is clear;
- generated/readout surfaces do not preserve confusing empty placeholders.

Expected evidence:

- implementation log records reviewed files.

Stop condition:

- stop if report conclusions contradict root README.

Phase 9.Stage 2.Action 3:
Review open-lab docs index and system-learning docs.

Checklist:

- open-lab posture clear;
- PO attribution preserved;
- no invented turns;
- redactions use `[XXX]`;
- unresolved decisions are visible.

Expected evidence:

- implementation log records reviewed files.

Stop condition:

- stop if any false attribution is detected.

#### Phase 9.Stage 3 - Final Release-Readiness Summary

Phase 9.Stage 3.Action 1:
Write final release-readiness summary in the implementation log.

Required content:

- completed phases;
- files changed;
- tests run;
- hygiene status;
- artifact bundle status;
- unresolved decisions;
- release actions not yet performed.

Expected evidence:

- implementation log can orient a future engineer without chat context.

Stop condition:

- stop if any completed phase cannot be truthfully documented.

Phase 9.Stage 3.Action 2:
Create a concise PO-facing release readiness checklist.

Suggested path:

```text
docs/design/beta_public_release/v0.1.0-beta.1_release_readiness_checklist.md
```

Required sections:

- ready;
- needs PO decision;
- not yet performed by design;
- commands run;
- recommended final release sequence.

Expected evidence:

- checklist makes clear that tag/upload/public visibility are still manual
  release actions unless separately approved.

Stop condition:

- stop if checklist would imply release has already happened.

Phase 9.Stage 3.Action 3:
Run final git status.

Expected evidence:

- implementation log records final status.

Stop condition:

- stop if unexpected files are modified, deleted, or untracked.

## 6. Final Acceptance Criteria

This workplan is complete when all of the following are true:

- release readiness work happened on a dedicated branch;
- implementation log exists and is complete;
- root README accurately frames the public beta;
- docs indexes are non-stale and navigable;
- current environments and evaluations are indexed;
- public claims are bounded to calibration/smoke;
- human-readable reports are linked;
- public reports explain raw artifact storage;
- large raw artifacts are either externalized into a verified local release
  bundle or explicitly left in git with recorded justification;
- public docs avoid machine-local absolute paths;
- public tracked docs use `[XXX]` for profanity redaction;
- PO attribution is preserved;
- no invented PO turns were introduced;
- release hygiene script exists and passes or records approved non-blockers;
- CI workflow exists;
- package/import/test sanity has been checked;
- governance files exist or missing ones are explicitly blocked by PO decision;
- release notes draft exists;
- cross-repo handoff note exists;
- final release readiness checklist exists;
- unresolved decisions are visible;
- no tag, upload, public visibility change, PyPI publish, history rewrite, or
  direct `state_collapser` edit has occurred without explicit separate PO
  approval.

## 7. Expected Resume Points

If interrupted, resume by reading:

```text
docs/design/beta_public_release/01_004_beta_public_release_readiness_implementation_log.md
```

Then identify the first incomplete `Phase.Stage.Action`.

Do not resume from memory.

Do not skip completed verification just because the file tree looks plausible.

Do not stop at a phase boundary unless a true stop condition exists.
