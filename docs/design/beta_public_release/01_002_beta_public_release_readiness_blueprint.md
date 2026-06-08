# Big Boy Benchmarking Beta Public Release Readiness Blueprint

## 0. Blueprint Status

This blueprint translates the release-readiness discussion in
`docs/design/beta_public_release/01_001_initial_beta_public_release_readiness.md`
into a detailed release preparation design.

This is not an implementation workplan. The next document should convert this
blueprint into Phase.Stage.Action form before execution.

This blueprint follows the prime directive attribution rule:

- Do not invent Project Owner turns.
- Do not rewrite consultant inferences as PO decisions.
- Preserve PO attribution where the PO made a decision.
- Mark unresolved questions as unresolved.
- Keep open-lab design material public where the PO explicitly chose that
  posture, while applying the public-release guardrails defined below.

## 1. Source Authority

### 1.1 Primary Source

Primary source:

```text
docs/design/beta_public_release/01_001_initial_beta_public_release_readiness.md
```

The primary source establishes:

- The current repository should be prepared for initial beta public release.
- The repository remains separate from `state_collapser`.
- This repository is the official benchmarking repository for
  `state_collapser`.
- The current public framing should be:

```text
Big Boy Calibration / Smoke
```

- The later, larger component should be:

```text
Benchmarking
```

### 1.2 Prime Directive Sources

Relevant governing documents:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
```

The false-attribution document is especially binding here because the release
readiness source includes PO turns, Codex turns, recommendations, and
unanswered questions. This blueprint must distinguish them carefully.

### 1.3 Existing Repository Sources To Recheck During Implementation

Implementation must re-read these before editing:

```text
README.md
CONTRIBUTING.md
pyproject.toml
.gitignore
docs/README.md
docs/evaluations/README.md
docs/environments/README.md
docs/prime_directive/artifact_table_to_readable_document_protocol.md
docs/prime_directive/evaluation_build_and_readout_material_protocol.md
docs/design/system_learning_from_evaluations/README.md
docs/evaluations/counterpoint_symbolic_v001/
docs/evaluations/plate_support_5x5_default_v001/
src/big_boy_benchmarking/
tests/
```

The implementation workplan should treat these as inspection targets, not as
already-correct surfaces.

## 2. Release Thesis

The beta release should present `big_boy_benchmarking` as a serious,
research-facing, public calibration and smoke-testing repository for
`state_collapser`.

The release should not claim that the repository already contains final
claim-bearing benchmarks. The stronger framing is:

- We have a working benchmark harness.
- We have two nontrivial environment families.
- We have artifact contracts, human-readable readouts, and public result
  summaries.
- We have a standard gauntlet pattern that can discover candidate towers,
  calibrate thresholds, run tower/direct paired probes, and summarize results.
- We have already used the system to find real integration and liftability
  issues, especially around pointwise liftability in `state_collapser`.
- We have early calibration/smoke evidence that tower-guided behavior can
  improve practical behavior in at least one robotics-like constrained
  environment, but the current evidence remains bounded and preliminary.

The release should make the repo legible to three audiences:

- `state_collapser` engineers who need a downstream integration and regression
  harness.
- External researchers who want to understand what was tested and what can be
  concluded.
- Future benchmark builders who need to add new environments and evaluations
  without rediscovering the existing workflow.

## 3. Decision Locks From The Discussion

These are decisions either explicitly made by the PO or accepted by the PO by
the top-level follow-up binding in the source document.

### 3.1 Public Open-Lab Posture

Decision:

```text
Keep all of this public as an open-lab notebook.
```

Implications:

- Design docs, evaluation readouts, system-learning archives, and continuity
  reports may remain public.
- The public repo should not pretend the process was cleaner or more linear
  than it was.
- Public surfaces need guardrails so they are intelligible, non-stale, and
  not misleading.
- The release should label open-lab material explicitly, so readers understand
  what is polished guidance, what is live design history, and what is archived
  evaluation conversation.

### 3.2 Current Component Name

Decision:

```text
Big Boy Calibration / Smoke
```

This is the public name for the current environments, diagnostics, gauntlets,
artifact readouts, and smoke-calibration evaluations.

### 3.3 Future Component Name

Decision:

```text
Benchmarking
```

This name is reserved for later, larger, claim-bearing evaluation work.

### 3.4 Separate Official Benchmarking Repository

Decision:

- This repo remains separate from `state_collapser`.
- This repo becomes the official benchmarking repository for
  `state_collapser`.
- The repos should cross-link.

### 3.5 Artifact Strategy

Decision:

- Keep human-readable summaries, compact result tables, badges, protocols,
  and provenance pointers in git.
- Move large raw artifact trees and heavy event-level run data to GitHub
  release assets for the beta release.

Release design implication:

- Public users should be able to inspect high-level conclusions from git.
- Public users should be able to download exact raw artifacts from a release
  asset bundle.
- Public users should be able to verify that readouts correspond to release
  artifacts by manifest and checksum.

### 3.6 Source-Only Beta, PyPI Deferred

Decision:

- The beta release should not assume immediate PyPI publication.
- The primary public artifact is the GitHub source release.
- Package/build sanity should still be checked.

### 3.7 Release Tag

Decision:

```text
v0.1.0-beta.1
```

This is the intended initial beta release tag unless the PO changes it before
release.

### 3.8 state_collapser Compatibility Target

Decision:

```text
state_collapser v0.7.2
```

This matters because the current meaningful downstream results depend on the
pointwise liftability semantics introduced in that upstream release.

### 3.9 Public Profanity Redaction Token

Decision:

The PO asked Codex to choose a fixed redaction token for profanity in public
tracked docs.

Blueprint choice:

```text
[XXX]
```

Rationale:

- It is visually obvious.
- It is plain Markdown.
- It is not shell-like.
- It does not look like a template variable.
- It is easy to scan for in release checks.

Release contract:

- Raw profane tokens in public tracked files should be replaced with `[XXX]`.
- Redaction must preserve attribution and meaning.
- Redaction must not convert a PO-authored turn into a Codex-authored
  paraphrase.
- If a sentence becomes unclear after redaction, add a neutral bracketed note
  after the quoted or archived material.
- Do not silently remove the fact that the PO was angry, concerned, or issuing
  a corrective instruction when that matters to the engineering history.

### 3.10 Stale Documentation Must Be Fixed Before Public Release

Decision:

- Root and top-level documentation must not present a false current scope.
- The root README must list current environments, current evaluations, current
  completed gauntlets, and bounded conclusions.
- Human-readable reports should be linked from public entry points.

### 3.11 Absolute Local Paths Must Be Normalized

Decision:

- Public documentation must not depend on `<local-home>/...` or other
  machine-local paths.
- Generated readout surfaces should use repo-relative paths, environment
  variables, or explicit placeholders such as `<repo-root>`.
- Raw artifact manifests may retain local path provenance only if the field is
  clearly marked as local provenance and not required for public use.

### 3.12 CI Is P0 For Beta Release

Decision:

- Add basic CI before public beta.
- CI should verify install/test health and release hygiene.

### 3.13 Governance And Release Metadata Are P0/P1

Decision:

- Add at least basic public governance and release surfaces.
- Required or strongly preferred files include:
  - `CHANGELOG.md`
  - `LICENSE` or license confirmation if already present
  - issue templates
  - PR template
  - `SECURITY.md`
  - package metadata URLs/classifiers where appropriate
  - release notes for `v0.1.0-beta.1`

## 4. Remaining Open Decisions

These are not safe to treat as settled.

### 4.1 Git History Redaction Boundary

The PO has chosen public open-lab docs and a profanity redaction token for
public tracked docs. There is still a release-management distinction:

- Redacting the current tree makes current public files cleaner.
- Making an existing private GitHub repo public also exposes prior git history.

Open decision:

```text
Should beta public release accept historical raw language in git history, or
should the public release be made from a cleaned history/export?
```

Recommended default unless the PO says otherwise:

- Do not rewrite history automatically.
- Redact the current tree.
- State in release notes that open-lab history has been cleaned in current
  docs for readability.
- If complete history sanitization is required, create a separate explicit
  workplan because history rewriting is destructive and coordination-heavy.

### 4.2 Root TeX Paper Disposition

The source discussion asks whether the root TeX paper should stay at root,
move under docs, be included as a research note, or be excluded from public
beta.

Open decision:

```text
What is the public-beta disposition of the root TeX paper and its built PDF?
```

Recommended default:

- Keep the `.tex`, `.bib` if present, and `.pdf` only if the PO wants the paper
  visible in the beta release.
- Keep build byproducts out of git.
- If included, link it as an exploratory note, not as the benchmark
  specification.

### 4.3 Artifact Bundle Format

The PO accepted moving large raw artifacts to GitHub release assets, but the
exact bundle format is not locked.

Recommended default:

```text
big_boy_calibration_smoke_v0.1.0-beta.1_artifacts.tar.zst
```

Fallback:

```text
big_boy_calibration_smoke_v0.1.0-beta.1_artifacts.zip
```

The implementation workplan must verify current GitHub release asset limits
before final release packaging.

### 4.4 Citation File

Open decision:

```text
Add CITATION.cff for beta, or defer until a paper/preprint exists?
```

Recommended default:

- Add `CITATION.cff` only if the PO wants early academic citation metadata.
- Otherwise defer and mention citation guidance in the release notes.

## 5. Current Repo-State Signals From The Readiness Discussion

The readiness source recorded the following repo-state signals. These must be
rechecked during implementation because they may already have changed.

### 5.1 Size And Artifact Pressure

Recorded state:

- Repository working tree size around 534 MB.
- `docs/evaluations` around 394 MB.
- Around 4207 files under `docs/evaluations/**/artifacts`.

Interpretation:

- The repo is currently too artifact-heavy for a clean public beta if raw
  artifacts remain in git.
- The beta release needs an artifact relocation or pruning plan.
- Readable reports should remain in git.

### 5.2 Local Path Pressure

Recorded state:

- Hundreds of occurrences of machine-local absolute paths were present.

Interpretation:

- Some are probably in generated provenance artifacts.
- Public-facing docs and commands must not require those paths.
- Public readout surfaces should present commands with `$BBB_ROOT`,
  `<repo-root>`, or repo-relative paths.

### 5.3 Generated And Local Byproduct Pressure

Recorded state:

- Python caches and `.DS_Store` files existed locally but were not necessarily
  tracked.
- Some TeX byproducts had previously appeared in git.
- A suspicious asset backup file existed:

```text
assets/images/.$diagrams.xml.bkp
```

Interpretation:

- The release work should include byproduct scans.
- `.gitignore` should cover Python, OS, and TeX build byproducts.
- Tracked byproducts should be removed from tracking if they are not intended
  public artifacts.

## 6. Public Release Architecture

The beta public release should be organized around four layers:

### 6.1 Layer A: Polished Public Entry Points

These are the files a new reader is expected to encounter first:

```text
README.md
CONTRIBUTING.md
CHANGELOG.md
LICENSE
SECURITY.md
docs/README.md
docs/evaluations/README.md
docs/environments/README.md
docs/design/beta_public_release/README.md
```

They should be concise, stable, and non-stale.

### 6.2 Layer B: Calibration / Smoke Reports

These are human-readable result surfaces:

```text
docs/evaluations/counterpoint_symbolic_v001/
docs/evaluations/plate_support_5x5_default_v001/
```

They should explain:

- What was run.
- What was observed.
- What can be concluded.
- What cannot be concluded.
- Where raw artifacts live.
- How to regenerate or inspect readouts.

### 6.3 Layer C: Open-Lab Design And System Learning

These are public engineering-history surfaces:

```text
docs/design/
docs/design/system_learning_from_evaluations/
docs/engineer_continuity/
docs/prime_directive/
```

They should remain public but be clearly labeled as open-lab material.

### 6.4 Layer D: Raw Artifact Bundles

These should move out of the git tree for public beta:

```text
docs/evaluations/**/artifacts/**/runs/**
docs/evaluations/**/artifacts/**/threshold_runs/**
docs/evaluations/**/artifacts/**/stages/**/raw/**
large event CSV trees
large generated raw manifests not needed by public docs
```

The exact paths must be determined by artifact inventory during
implementation.

## 7. Public README Blueprint

The root README should become the public front door for the beta release.

### 7.1 Required Opening

The first screen should establish:

- Project name.
- Relationship to `state_collapser`.
- Current status as beta.
- Current component name: `Big Boy Calibration / Smoke`.
- Future component name: `Benchmarking`.
- One-sentence caution that current evaluations are calibration/smoke, not
  final benchmark claims.

### 7.2 Required Current Environment Summary

The README should summarize at least:

#### Counterpoint Symbolic v001

Purpose:

- Hidden graph / contraction schema environment.
- Used to develop the core artifact, readout, liftability, and tower training
  machinery.

Current evaluation families to link:

- first serious learning evaluation
- one-third schema tower diagnostics
- contraction fraction sweep diagnostics
- noisy-rate contraction diagnostics
- noisy-rate full tower training diagnostic
- second serious schema comparison
- small paired replicate probe
- threshold frontier probe

Bounded conclusion:

- Counterpoint established that the BBB machinery can build and inspect towers,
  produce human-readable reports, run tower/direct comparisons, and expose
  important integration issues.
- Evidence in counterpoint was often subtle and diagnostic, not yet a broad
  benchmark claim.

#### PlateSupport 5x5 Default v001

Purpose:

- Robotics-like constrained plate support environment.
- Better suited than counterpoint for showing practical control differences
  because invalid moves and constrained support failures are behaviorally
  meaningful.

Current evaluation family to link:

- standard gauntlet

Bounded conclusion:

- The corrected PlateSupport standard gauntlet produced a trainable tower arm
  and a direct comparison signal.
- The tower arm had much better mean total reward than direct in the smoke
  run, with zero invalid concrete moves versus many invalid direct moves.
- This is an encouraging calibration/smoke result, not yet a final benchmark
  claim.

### 7.3 Required "What Can We Conclude?" Section

The README should include a short, careful conclusion section:

- The framework can create, run, and summarize nontrivial tower evaluations.
- The artifact/readout protocol is mature enough for public inspection.
- `state_collapser` v0.7.2 pointwise liftability is the required baseline for
  current meaningful tower runs.
- PlateSupport provides first meaningful evidence that tower guidance can
  reduce invalid action behavior and improve practical reward in a constrained
  control setting.
- Larger benchmarking is future work.

### 7.4 Required "What Not To Conclude Yet" Section

The README must explicitly avoid overclaiming:

- Do not claim general speedup across environments.
- Do not claim final statistical significance.
- Do not claim final robotics benchmark status.
- Do not claim PyPI stability unless PyPI is actually published.
- Do not claim that raw artifacts are in git if they have moved to release
  assets.

### 7.5 Required Quickstart

The quickstart should support source install:

```bash
git clone <repo-url>
cd big_boy_benchmarking
uv sync
uv run pytest
uv run python -m big_boy_benchmarking.cli --help
```

If `state_collapser` installation has a special source or version constraint,
the README should state it plainly.

### 7.6 Required Report Links

The README should link to the best human-readable reports:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/README.md
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/README.md
docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/README.md
docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/README.md
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/README.md
```

The implementation should verify which reports are still current and include
only current, non-stale links.

## 8. Documentation Map Blueprint

### 8.1 docs/README.md

Should explain the docs tree:

- `docs/prime_directive`: protocols for Codex/engineer behavior.
- `docs/design`: open-lab design history and blueprints.
- `docs/environments`: environment descriptions and readiness docs.
- `docs/evaluations`: human-readable evaluation reports and compact tables.
- `docs/engineer_continuity`: dated continuity reports.

It should also explain the three-step workflow:

1. Environment design and readiness.
2. Evaluation or gauntlet design.
3. Artifact-table readout to human-readable reports.

### 8.2 docs/evaluations/README.md

Should become a compact index of public reports:

- Environment family.
- Evaluation name.
- Current status.
- Key bounded conclusion.
- Link to README.
- Link to release artifact bundle entry if raw artifacts are externalized.

### 8.3 docs/environments/README.md

Should list environment families:

- Counterpoint Symbolic v001.
- PlateSupport 5x5 Default v001.

Each should include:

- Purpose.
- Current maturity.
- Available evaluation families.
- Required `state_collapser` compatibility.

### 8.4 docs/design/README.md

If missing or stale, add or update it to explain:

- Design docs are open-lab material.
- Blueprints are design specifications.
- Workplans are Phase.Stage.Action execution plans.
- System-learning folders preserve lessons discovered through evaluation.

### 8.5 docs/design/beta_public_release/README.md

Should remain the local index for release readiness design:

- Link to readiness discussion.
- Link to this blueprint.
- Link to the eventual workplan.
- Link to release implementation logs once they exist.

## 9. Open-Lab And Attribution Blueprint

### 9.1 Public Open-Lab Labels

Open-lab docs should carry a short label such as:

```text
Open-lab design note: this document preserves live design reasoning,
corrections, and PO/Codex attribution. It is public engineering memory, not a
polished paper.
```

This label should be used where a doc is likely to confuse a public reader.

### 9.2 PO Attribution Preservation

When sanitizing public docs:

- Preserve who said what.
- Keep `PO Decision`, `PO Reply`, `PO Follow-up`, `Codex Turn`, and similar
  labels where they are part of the document's structure.
- Do not invent missing PO replies.
- Do not convert a PO quote into a Codex conclusion without saying it is an
  inference.

### 9.3 Redaction Semantics

Use `[XXX]` to replace profane tokens.

Examples of permitted transformation:

```text
Original intent: PO expressed strong anger that a protocol drifted.
Public text: PO expressed strong anger that a protocol drifted. [Profanity
redacted as [XXX] in public tree.]
```

For archived dialogue:

- Replace only the profane word or phrase with `[XXX]`.
- Leave the rest of the sentence intact when possible.
- If the remaining sentence is unreadable because of typos plus redaction,
  add a neutral note after the turn.

### 9.4 Release Hygiene Scan

Before release, run a scan for:

- raw profane terms and common typos of those terms
- local absolute paths
- stale placeholder text
- invented turn headings
- orphaned generated docs with empty "next turn" slots
- legacy pre-workplan terminology if the repository standard is now
  "workplan"

The workplan should define the exact scan commands and stop conditions.

## 10. Artifact Externalization Blueprint

### 10.1 Goals

The artifact externalization work should:

- Reduce git weight.
- Keep public result summaries inspectable without downloading large bundles.
- Preserve exact reproducibility through release assets.
- Avoid breaking readout links.

### 10.2 Keep In Git

The following should generally stay in git:

```text
README.md
result_readout.md
artifact_index.md
method.md
runbook.md
glossary.md
badges/*.svg
results/*.md
small summary CSVs
readout_source.json
```

For summary CSVs, use a size threshold in the workplan. If a summary CSV is
small and directly supports the public report, keep it. If it is event-level
or run-level raw data, move it to the release bundle.

### 10.3 Move To Release Assets

The following should generally move to release assets:

```text
raw run directories
event-level CSVs
large nested artifacts
per-step traces
large threshold run trees
large copied upstream artifacts
```

This includes many paths under:

```text
docs/evaluations/**/artifacts/
```

The implementation must inventory first and then move only what the readout
contract can still reference externally.

### 10.4 Release Bundle Manifest

Each artifact bundle should include:

```text
ARTIFACT_BUNDLE_MANIFEST.json
SHA256SUMS.txt
README.md
```

The manifest should include:

- release tag
- repository commit
- `state_collapser` version
- artifact bundle creation time
- source evaluation families
- top-level artifact roots
- file counts
- byte counts
- checksums
- mapping from repo readout paths to bundle paths

### 10.5 Readout Source Changes

Each public `readout_source.json` affected by artifact externalization should
include:

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

Exact schema can differ if existing readout contracts require it, but the
public report must clearly say where raw artifacts are.

### 10.6 Artifact Index Changes

Public artifact indexes should distinguish:

- available in git
- available in release bundle
- generated locally only
- intentionally omitted

## 11. Path Portability Blueprint

### 11.1 Public Command Style

Public commands should use:

```bash
export BBB_ROOT="$PWD"
export BBB_ARTIFACT_ROOT="$BBB_ROOT/docs/evaluations/<...>/artifacts/<run-label>"
```

or:

```text
<repo-root>/docs/evaluations/...
```

Do not use:

```text
<local-home>/...
<tmp-dir>/...
```

except in explicitly archived historical context where the path is marked as
local provenance.

### 11.2 Generated Doc Writers

All generated doc writers should:

- Prefer repo-relative paths in public fields.
- Keep absolute local paths out of README-level summaries.
- Include enough path information for a local rerun.
- Avoid writing machine-local absolute paths into public Markdown.

### 11.3 Manifests

Manifests may contain local absolute paths only if:

- the field name makes locality explicit, such as `local_absolute_path`;
- the value is not required by public commands;
- the human-readable report explains that raw local paths are provenance from
  the original run.

### 11.4 Tests

Add tests or release checks that fail when public docs contain forbidden local
paths.

## 12. Generated Readout Protocol Blueprint

### 12.1 Existing Protocol To Update

Primary protocol:

```text
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

Possible companion protocol:

```text
docs/prime_directive/evaluation_build_and_readout_material_protocol.md
```

### 12.2 Required Public-Release Mode

The protocol should include a public-release mode or release-hygiene section
requiring:

- consistent badge style
- stable top summary
- bounded claims
- artifact storage location
- repo-relative paths
- `[XXX]` profanity redaction
- no invented PO turns
- preservation of existing human clarification sections unless the section is
  explicitly regenerated by protocol
- no empty public placeholders unless they are intentionally labeled as future
  reader questions

### 12.3 Readout Surfaces

Public evaluation readouts should include:

- Status badges.
- One-paragraph result.
- Key numbers.
- What this supports.
- What this does not support.
- Artifact provenance.
- Method.
- Links to compact tables.
- Link to raw artifact bundle.
- Optional public conversation or reader-question section, if present.

### 12.4 Protocol Command

The release docs should prefer the explicit command form:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <readout_source.json>
```

Avoid ambiguous phrasing such as:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-readout-surface>/readout_source.json
```

unless the protocol itself still documents that shorthand and its resolution
rules.

## 13. CI Blueprint

### 13.1 Required GitHub Actions Workflow

Add:

```text
.github/workflows/ci.yml
```

Minimum jobs:

- checkout
- install `uv`
- `uv sync`
- `uv run pytest`
- import CLI smoke
- release hygiene scan

### 13.2 Release Hygiene Job

The hygiene job should check:

- no raw profane tokens in public tracked docs
- no forbidden local absolute paths in public Markdown
- no `.DS_Store`
- no Python caches
- no TeX build byproducts except intentional `.tex`, `.bib`, `.pdf`
- no huge raw artifact directories in git after externalization
- generated readout sources exist for linked evaluation reports
- badges referenced by public READMEs exist

### 13.3 Optional But Useful Jobs

Optional:

- package build check
- `ruff` or formatter check if project already uses it
- type check only if project already has stable typing config
- artifact bundle manifest validation

Do not introduce heavy new tooling unless it is needed for release confidence.

## 14. Packaging And Metadata Blueprint

### 14.1 pyproject.toml

Verify or update:

- project name
- version strategy
- Python version requirement
- dependencies
- optional dev dependencies
- project URLs
- classifiers
- CLI entry point if appropriate

For source-only beta, the package version can align with:

```text
0.1.0b1
```

while the git tag remains:

```text
v0.1.0-beta.1
```

Only do this if it matches existing package conventions.

### 14.2 CLI Sanity

Public README should show:

```bash
uv run python -m big_boy_benchmarking.cli --help
```

If a console script exists, also show it. If not, do not invent one without a
workplan decision.

### 14.3 Dependency State

`state_collapser` dependency should be pinned or constrained clearly enough
that public users get the pointwise liftability behavior required by current
reports.

The beta release must not silently allow an older `state_collapser` version
that recreates known liftability failures.

## 15. Cross-Repo Linking Blueprint

### 15.1 In This Repo

Add links to `state_collapser` in:

- root README
- docs README
- environment docs
- release notes

Explain:

- `state_collapser` provides tower/collapse machinery.
- `big_boy_benchmarking` provides downstream environments, evaluations, and
  public calibration/smoke reports.

### 15.2 In state_collapser

The release program should eventually update `state_collapser` docs to link
back here.

Because `state_collapser` is outside the current writable repo, the workplan
must either:

- stop and ask before editing that repo; or
- create a separate cross-repo task list for the `state_collapser` engineers.

### 15.3 Version Boundary

Public docs should state:

```text
Current beta reports assume state_collapser v0.7.2 or newer compatible
pointwise liftability semantics.
```

If that compatibility changes before release, update all public docs.

## 16. Governance Blueprint

### 16.1 Required Files

Add or verify:

```text
LICENSE
CHANGELOG.md
SECURITY.md
.github/ISSUE_TEMPLATE/
.github/pull_request_template.md
```

### 16.2 CHANGELOG Shape

`CHANGELOG.md` should include:

- `Unreleased`
- `v0.1.0-beta.1`
- summary of public beta scope
- major environment/evaluation families
- artifact storage note
- known limitations

### 16.3 Issue Templates

Recommended templates:

- bug report
- evaluation/readout problem
- environment proposal
- artifact/reproducibility problem

### 16.4 PR Template

PR template should ask:

- What environment/evaluation/protocol is affected?
- Were readouts regenerated?
- Are artifacts stored in git or release assets?
- Were public docs checked for local paths?
- Were PO attributions preserved if docs changed?

### 16.5 SECURITY.md

Even if the project is not security-sensitive, include:

- supported versions
- how to report vulnerabilities or sensitive data leaks
- statement that benchmark artifacts may contain local provenance unless
  release-cleaned

## 17. Public Claims Boundary

### 17.1 Allowed Claims

The beta release may claim:

- BBB is the official benchmarking/calibration repository for
  `state_collapser`.
- The current public component is Big Boy Calibration / Smoke.
- The repo contains working environment/evaluation machinery.
- Counterpoint and PlateSupport have generated public human-readable reports.
- PlateSupport standard gauntlet produced encouraging smoke evidence for
  tower-guided control.
- The system has already helped identify and validate `state_collapser`
  integration semantics, especially pointwise liftability.

### 17.2 Disallowed Claims

The beta release must not claim:

- final benchmark victory
- general speedup theorem
- broad robotics superiority
- production stability
- PyPI availability unless actually published
- that raw artifacts are in git if they have been moved
- that the system is free of known open design questions

### 17.3 Phrase To Prefer

Use:

```text
calibration/smoke evidence
```

instead of:

```text
proof
```

Use:

```text
encouraging tower-guided control signal
```

instead of:

```text
benchmark win
```

Use:

```text
future Benchmarking component
```

instead of implying the current repo already contains final benchmarks.

## 18. Release Notes Blueprint

Create release notes for:

```text
v0.1.0-beta.1
```

Required sections:

- What this release is.
- Relationship to `state_collapser`.
- Current component: Big Boy Calibration / Smoke.
- Included environment families.
- Included evaluation/readout families.
- Most important observed result.
- Known limitations.
- How to install from source.
- How to run smoke tests.
- How to inspect reports.
- How to download raw artifact bundle.
- Artifact checksums.
- Compatibility with `state_collapser`.

## 19. Release Branch Blueprint

Implementation should happen on a branch such as:

```text
codex/beta-public-release-readiness
```

The branch should be used to stage:

- docs cleanup
- artifact externalization
- CI
- metadata
- governance files
- release notes
- hygiene checks

Do not mix unrelated new evaluations into the release readiness branch unless
the PO explicitly asks.

## 20. Implementation Stop Conditions

Stop and ask the PO before:

- rewriting git history
- deleting raw artifacts without a verified release bundle
- changing scientific claims materially
- changing the root TeX paper disposition if unclear
- editing `state_collapser` directly
- publishing to PyPI
- making the GitHub repo public
- tagging a release
- uploading release assets

## 21. Acceptance Criteria

The beta release readiness work is complete when:

- Root README accurately frames the beta release.
- Top-level docs are non-stale.
- Current environments and evaluations are indexed.
- Public claims are bounded.
- Human-readable reports are linked.
- Large raw artifacts are externalized or explicitly justified.
- Release asset bundle manifest exists if artifacts are externalized.
- Public docs do not require local absolute paths.
- Public docs use `[XXX]` for profanity redaction.
- PO attribution is preserved in open-lab docs.
- CI passes.
- `uv sync` and `uv run pytest` pass locally or failures are documented.
- Package/build sanity is checked.
- Governance files exist.
- Release notes exist.
- Cross-repo relationship to `state_collapser` is documented.
- Remaining unresolved decisions are listed explicitly.

## 22. Workplan Derivation Requirements

The next document should be:

```text
docs/design/beta_public_release/01_003_beta_public_release_readiness_implementation_workplan.md
```

It should:

- Use Phase.Stage.Action discipline.
- Execute in a single parent workplan rather than requiring the PO to manually
  drive sub-stages.
- Include checkpoints for artifact inventory, docs cleanup, CI, and release
  hygiene.
- Include explicit resume points.
- Include implementation logs in this folder.
- Respect the stop conditions above.
