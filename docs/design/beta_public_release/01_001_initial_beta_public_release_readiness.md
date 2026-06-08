# Initial Beta Public Release Readiness

Date: 2026-06-08

Repository:

```text
<repo-root>
```

Status:

```text
Design assessment only. No release-prep implementation has been approved or
performed in this document.
```

#### PO Follow-Up Binding
> I think I essentially agree wiht all of this: `docs/design/beta_public_release/01_001_initial_beta_public_release_readiness.md` There are a few places where  put a PO decision or a PO reply. Please put #### Codex Turn under with your reponse. For all things I didn't reply to, I agree with you.

#### Codex Turn
Accepted. The release-readiness document should now be read with this global
binding: explicit PO decisions/replies override the original recommendation
where they differ, and sections without a local PO reply are accepted as
consultant recommendations. The next artifact after this document should be an
implementation blueprint/workplan that converts these accepted recommendations
into release-prep tasks without reopening settled scope.

## Release Intent

The intended public story is:

```text
big_boy_benchmarking is the official benchmarking repository for state_collapser.
```

The current repo should not be framed as the final benchmarking suite. It should
be framed as the first public beta component:

```text
Big Boy Calibration / Smoke
```

That component contains:

- environment-readiness surfaces;
- smoke and calibration diagnostics;
- current counterpoint evaluation readouts;
- the PlateSupport standard gauntlet correction run;
- artifact contracts, seed/mode/timing helpers, runner skeletons, and
  human-readable readout machinery;
- bounded evidence that the system can detect, diagnose, and report
  tower-control behavior.

The next public component should be:

```text
Benchmarking
```

That component should mean larger, claim-bearing benchmark runs with explicit
budgets, stronger candidate coverage, repeatability, and public artifact
discipline.

## Current Repo Snapshot

Observed current branch state:

```text
## main...origin/main
```

No local branches had unmerged commits into `main` when checked immediately
before this design pass.

Current package metadata:

```text
name = "big-boy-benchmarking"
version = "0.1.0"
description = "Serious, post-smoke benchmarking harnesses for state_collapser."
requires-python = ">=3.11,<3.13"
state_collapser dependency = git tag v0.7.2
license = MIT
```

Current remote:

```text
origin git@github.com:TYLERSFOSTER/big_boy_benchmarking
```

Current tags:

```text
none
```

Current CI:

```text
No .github workflow files found.
```

Current repo size observations:

```text
repo working tree: about 534 MB
docs/: about 397 MB
docs/evaluations/: about 394 MB
docs/design/: about 2.5 MB
src/: about 5.7 MB
tests/: about 1.6 MB
assets/: about 7.6 MB
```

Current artifact-file observations:

```text
docs/evaluations artifact files: about 4207 files under */artifacts/*
absolute local path-bearing files: about 464 files
local pyc files on disk: about 682, not tracked by git
.DS_Store files on disk: ./.DS_Store and ./assets/.DS_Store, not tracked by git
```

Important tracked asset note:

```text
assets/images/.$diagrams.xml.bkp
```

appears in tracked file listings and should be checked before public release.
It looks like an editor or filesystem sidecar, not an intended public asset.

## Proposed Public Framing

### Component 1: Big Boy Calibration / Smoke

This is what the repo currently has.

Public definition:

```text
Calibration / Smoke is the reproducible early benchmark-readiness layer for
state_collapser.
```

It answers:

- Can BBB bind `state_collapser` environments?
- Can BBB construct environment-specific artifacts?
- Can BBB diagnose quotient/tower behavior?
- Can BBB run bounded training and paired-comparison surfaces?
- Can BBB translate machine artifacts into human-readable reports?
- Can BBB expose failures without turning them into false benchmark claims?

It does not answer:

- Is a tower method generally superior?
- Which contraction schema is best?
- What is the stable performance distribution across many seeds/instances?
- What are final benchmark rankings?
- What are tensor/CUDA/GPU performance claims?

Current Calibration / Smoke public inventory:

- Counterpoint symbolic environment family.
- PlateSupport 5x5 default environment readiness.
- Counterpoint first serious learning structural-limit diagnostic.
- Counterpoint one-third tower diagnostic.
- Counterpoint contraction fraction sweep diagnostic.
- Counterpoint noisy-rate contraction diagnostic.
- Counterpoint noisy-rate tower-only training-health diagnostic.
- Counterpoint second serious schema comparison.
- Counterpoint threshold frontier probe.
- Counterpoint small paired replicate probe.
- PlateSupport standard gauntlet `iterated_001`.
- Artifact/readout protocols and badges.

The most compelling current public beta result is the PlateSupport standard
gauntlet:

```text
target hits: tower 25 / 128, direct 15 / 128
mean target-hit-rate delta: +0.078125
tower mean reward: -27.2109375
direct mean reward: -78.71875
tower invalid moves: 0
direct invalid moves: 2142
claim boundary: bounded smoke-scale positive signal
```

That should be described as a promising calibration/smoke signal, not a final
benchmark result.

### Component 2: Benchmarking

This is the next component, not the current one.

Public definition:

```text
Benchmarking is the claim-bearing evaluation layer built on top of Calibration
/ Smoke.
```

It should include:

- larger budgets;
- more seeds;
- more candidates;
- more environments or varied instances;
- frozen benchmark configs;
- CI-verifiable smoke subsets;
- separately downloadable full artifacts;
- public tables that distinguish smoke/calibration evidence from benchmark
  evidence;
- clear statistical treatment and stopping criteria.

Benchmarking should not start by renaming the current smoke runs. It should be a
new designed layer that consumes what Calibration / Smoke proved is runnable.

## P0 Release Blockers

These should be resolved before making the repo public.

### P0.1 Public Documentation Cut

The repo currently contains a lot of internal working memory:

- `docs/design/` includes design discussions, implementation logs, and raw
  troubleshooting history.
- `docs/engineer_continuity/` includes session continuity reports.
- `docs/prime_directive/` is directed to an embedded consultant, not ordinary
  public users.
- Several generated readouts include clarifying-turn conversations with
  internal tone and conversational fragments.

For public beta, decide one of three policies:

1. Keep all of this public as an open-lab notebook.
2. Move internal material to a private branch or private archive and publish a
   cleaned public docs cut.
3. Keep selected design docs public, but remove or sanitize raw conversations,
   implementation logs, and continuity reports.

Recommendation:

```text
For initial public beta, publish a cleaned docs cut.
```

Suggested public docs:

- root `README.md`;
- `CONTRIBUTING.md`, rewritten for public contributors;
- `docs/README.md`, rewritten as a public documentation map;
- `docs/environments/`;
- `docs/evaluations/` human readout surfaces, after path normalization and
  internal-turn cleanup;
- `docs/methods/`, after checking for stale/internal language;
- a new `docs/calibration_smoke/` or equivalent overview page;
- a future `docs/benchmarking/` placeholder that states the benchmark component
  is next.

Suggested private/internal docs:

- raw design conversations;
- implementation logs;
- engineer continuity reports;
- Prime Directive files;
- system-learning archives with raw conversational attribution.

If any internal docs remain public, they need a deliberate "open research
process" note and a tone/privacy pass.

#### PO Decision
> Keep all of this public as an open-lab notebook.

#### Codex Turn
Accepted. This changes the release strategy from "cleaned public docs cut" to
"open-lab notebook with guardrails." We should not hide `docs/design/`,
`docs/prime_directive/`, or `docs/engineer_continuity/` by default. Instead,
the public beta work should:

- add an explicit open-lab notebook statement near the root documentation map;
- explain that design discussions, implementation logs, and continuity reports
  are historical process records, not polished user docs;
- keep public navigation focused on README, environment pages, evaluation
  readouts, and Calibration / Smoke summaries;
- still do a tone/privacy/path pass so the open notebook is deliberate rather
  than accidentally messy;
- preserve attribution rather than rewriting history.

This also means the "suggested private/internal docs" list above is no longer
the preferred path. It remains useful only as a list of material that needs
clear labeling before public release.

### P0.2 Stale Public Docs

The root `README.md` is mostly current, but several public docs are stale:

```text
docs/README.md
docs/evaluations/README.md
```

Examples:

- `docs/README.md` still says noisy-rate full small+medium validation remains
  pending and only lists three current readouts.
- `docs/evaluations/README.md` still calls threshold-frontier and small paired
  replicate runs smoke/claim-blocked, even though current checked-in readouts
  are `episodes16_001` and `episodes16_from_frontier_001`.

Release requirement:

```text
All top-level documentation indexes must agree with root README and the current
readout surfaces before public beta.
```


#### PO Reply
> I agree

#### Codex Turn
Accepted. This becomes a straightforward P0 release task: update
`docs/README.md` and `docs/evaluations/README.md` so they agree with root
`README.md`, the current `episodes16_001` and
`episodes16_from_frontier_001` counterpoint readouts, and the PlateSupport
`iterated_001` gauntlet readout. Because these files are public navigation
surfaces, they should be fixed before any public beta tag.

### P0.3 Absolute Local Path Removal Or Normalization

The repo currently contains many absolute local paths such as:

```text
<repo-root>
<tmp-dir>/...
```

They occur in:

- source manifests and dependency manifests;
- generated readout sources;
- artifact indexes;
- generated runbooks;
- environment readiness docs;
- evaluation readouts;
- some source files and doc writers.

Source files with hard-coded local repo paths include:

```text
src/big_boy_benchmarking/runners/upstream_smoke.py
src/big_boy_benchmarking/environments/counterpoint/runners.py
src/big_boy_benchmarking/environments/counterpoint/serious_learning/direct.py
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/fraction_sweep_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_diagnostics/runner.py
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/runner.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/runner.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/*/docs_writer.py
```

Release requirement:

- source code must not serialize a hard-coded developer path;
- generated docs should use repo-relative links where possible;
- artifact manifests should either use relative paths or a symbolic root such
  as `${BBB_REPO_ROOT}`;
- readout regeneration must preserve portability.

Suggested design:

```text
Artifact manifests store both:
  repo_relative_path
  optional local_absolute_path generated at runtime and excluded from portable docs
```

#### PO Decision
> I agree.

#### Codex Turn
Accepted. This should become a dedicated portability workstream. The important
implementation distinction is:

```text
machine provenance can remember where a run happened locally,
but public readouts and portable manifests should not require that local path.
```

The likely implementation is to add path helpers that emit repo-relative paths
or `${BBB_REPO_ROOT}`-relative symbolic paths for public artifacts, then
regenerate readouts from those portable source bindings. Source files that
currently serialize `<repo-root>` should be treated as
release blockers.

### P0.4 Artifact Publication Policy

The checked-in repo currently includes a large raw artifact tree:

```text
docs/evaluations/: about 394 MB
docs/evaluations/*/*/artifacts/: about 4207 files
```

This is too heavy and too path-bound for a clean public beta unless the Project
Owner deliberately wants the raw artifact history in git.

Release choices:

1. Keep all artifacts in git.
2. Keep human-readable readouts in git, move raw artifacts to GitHub release
   assets.
3. Keep only compact summary artifacts in git, move event-level raw artifacts to
   Git LFS, DVC, or release assets.
4. Publish a `calibration_smoke_001` artifact bundle separately and make
   readout sources portable pointers to that bundle.

Recommendation:

```text
For initial public beta, keep human-readable readouts and compact summary
tables in git. Move large raw event/run artifacts out of normal git history
before making the repository public, unless preserving the current private
history is acceptable.
```

If the repo has already been pushed private with large artifacts, consider:

- public release from a cleaned branch;
- history rewrite only if acceptable;
- or public release with artifacts intact, but document the repo size honestly.

#### PO Decision
> Tell me about "Github release assets."

#### Codex Turn
GitHub release assets are files attached to a GitHub Release, separate from the
normal git-tracked repository tree.

Concrete shape:

```text
Git tag:
  v0.1.0-beta.1

GitHub Release page:
  title, notes, changelog, compatibility, claim boundary

Attached release assets:
  calibration_smoke_001_artifacts.tar.zst
  calibration_smoke_001_checksums.txt
  maybe: compact_readout_tables.zip
```

Why this helps:

- The code/docs repo can stay smaller and easier to clone.
- Large raw event/run artifacts can still be public and reproducible.
- A release asset is immutable enough for a beta evidence bundle if paired with
  checksums and a tag.
- Human-readable readouts can link to the artifact bundle instead of embedding
  thousands of raw files in the main repository.

Tradeoffs:

- Release assets are not as pleasant to diff as git files.
- They need a bundle manifest and checksums.
- If the readout source points outside the repo, the readout protocol must know
  how to say "source artifact bundle" rather than "repo-local raw artifact
  root."
- If we want every raw table browsable directly in GitHub's file UI, release
  assets are worse than tracked files.

Recommended public beta policy:

```text
Keep source code, method docs, environment pages, human-readable readouts, badge
SVGs, compact summary tables, and small manifests in git.

Move large event-level raw artifacts and nested run trees into a versioned
GitHub release asset bundle.
```

This preserves the evidence while avoiding a half-gigabyte public clone as the
default first impression.

#### PO Reply.
> Yeah I totally agree.

### P0.5 Internal Tone And Conversation Cleanup

A scan found a small number of files with raw conversational profanity or
internal emotional context. These are mostly in design/conversation archives,
but one current evaluation README also contains conversational fragments:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/README.md
```

Release requirement:

- public-facing readouts should not include raw chat fragments unless the repo
  is explicitly published as a lab notebook;
- generated clarifying-turn sections should either be omitted from public docs
  or rewritten as "Reader Notes" / "Interpretation Notes";
- Prime Directive/internal docs should not be mistaken for user documentation.

#### PO Reply
> Give me a list of *all* instances of this in the repo.

#### Codex Turn
Here is the current explicit scan result for raw profanity/internal emotional
tone. The scan terms were:

```text
[XXX]|[XXX]|[XXX]|motherf|irrate|[XXX]
```

The exact files hit by that scan are:

```text
docs/design/degenerate_tier_control/error_diagnosis_conversation.md
docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/02_readout_conversation_archive.md
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/README.md
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
docs/design/first_infrastructure_slice/01_001_initial_benchmarking_goals_discussion.md
```

Current exact instances:

1. `docs/design/degenerate_tier_control/error_diagnosis_conversation.md`

   ```text
   "this "problem" is dumb as [XXX]"
   ```

2. `docs/design/system_learning_from_evaluations/counterpoint_one_third_schema_unexpected_collapse/02_readout_conversation_archive.md`

   ```text
   "This is [XXX] nonsense."
   "true [XXX]"
   "so [XXX] ass-bakcward"
   "I don't know what the [XXX] this means"
   "I don't know what the [XXX] you're saying"
   ```

3. `docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/README.md`

   ```text
   "But that's literally what I asked you to [XXX] make."
   "really [XXX] disturbing"
   ```

4. `docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md`

   ```text
   "there's a lot of other [XXX] in docs"
   ```

5. `docs/design/first_infrastructure_slice/01_001_initial_benchmarking_goals_discussion.md`

   ```text
   "I don't want to [XXX] with anything in there"
   "[XXX] like model checkpoints"
   "This seems [XXX] made-up"
   ```

There are also public-readout conversational artifacts that are not profanity
but still read as internal chat rather than public release documentation:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/README.md
  - starts a turn with "Bro..."
  - contains many Project Owner / Codex turn sections from the debugging
    conversation;
  - contains placeholder turn pairs near the bottom: "[...]".

docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/README.md
  - contains repeated "_Open._" placeholder turns.

docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/README.md
  - contains repeated "> ..." placeholder turn pairs.
```

Because the PO decision is to keep the repo public as an open-lab notebook, I
would not erase these from design archives by default. But I would clean or
split the public-facing generated evaluation readouts so the first page a new
user sees is a reader-facing report, not raw chat. The raw turn material can
remain in an archive section or design archive with explicit open-lab labeling.

#### PO Reply
For all profanity, decide some fixed "[XXX]" or like `${XXX}`... ha ha that's kind of funny. The rest I agree with.

### P0.6 Public README Reframing

The root README currently says:

```text
Serious, post-smoke benchmarking for state_collapser
```

For initial beta, this overstates the current public claim boundary. The new
framing should be closer to:

```text
Official Calibration / Smoke and emerging benchmarking harnesses for
state_collapser.
```

Root README should have:

- "What this repo is";
- "What Calibration / Smoke means";
- "What Benchmarking will mean";
- "Current beta claim boundaries";
- "Quickstart";
- "Run the PlateSupport calibration gauntlet";
- "Read the current reports";
- "Relationship to state_collapser";
- "Version compatibility";
- "Artifact policy";
- "Contributing";
- "License".

#### PO Decision
> I agree.

#### Codex Turn
Accepted. The root README rewrite should now be treated as required P0 work.
The phrase "Serious, post-smoke benchmarking" should be replaced or qualified
so it does not overclaim the current release. The public front page should lead
with:

```text
Official Calibration / Smoke and emerging Benchmarking harnesses for
state_collapser.
```

It should then explain that the current beta release is Calibration / Smoke,
while the claim-bearing Benchmarking component is the next layer.

### P0.7 Cross-Repo Linking With state_collapser

This repo should link to `state_collapser`, and `state_collapser` should link
back.

Required here:

- root README link to public `state_collapser`;
- version compatibility table:

  ```text
  big_boy_benchmarking beta release -> state_collapser v0.7.2
  ```

- note that this repo is separate from the core library;
- note which environments are upstream examples versus BBB-owned benchmark
  surfaces.

Required in `state_collapser`:

- README section naming this repo as the official benchmarking repo;
- link to BBB public beta;
- version compatibility note;
- short explanation that `state_collapser` remains the core library and BBB is
  where calibration/smoke/benchmark artifacts live.


#### PO Reply
> I agree.

#### Codex Turn
Accepted. This needs coordinated work in both repositories. In BBB, the public
docs should say:

```text
state_collapser is the core library.
big_boy_benchmarking is the official Calibration / Smoke and future Benchmarking
repo for state_collapser.
```

In `state_collapser`, the README should link here and state the compatibility
target. This probably belongs in a small dedicated cross-repo release-prep
checklist so we do not make BBB public and then forget the backlink.

### P0.8 CI And Public Verification

There are no GitHub workflow files.

Before public beta, add at least:

```text
.github/workflows/ci.yml
```

Minimum CI:

- checkout;
- setup Python 3.11 and 3.12 if feasible;
- install `uv`;
- `uv sync --group dev`;
- `uv run pytest`;
- `uv run ruff check .`.

Because full artifact regeneration can be expensive, CI can start with:

- unit tests;
- CLI parser smoke tests;
- small artifact-writer tests;
- one tiny smoke run if runtime is acceptable.

#### PO Reply
> I agree

#### Codex Turn
Accepted. CI should be part of the beta-release preparation, not a follow-up.
Minimum useful first workflow:

```text
uv sync --group dev
uv run pytest
uv run ruff check .
git diff --check
```

I would also add a release-hygiene test or script that scans for hard-coded
local paths in source and public docs. That protects the portability work from
regressing immediately after we fix it.

### P0.9 Packaging Release Sanity

The package has no console script entry point, no classifiers, and no project
URLs in `pyproject.toml`.

Before public beta:

- add `project.urls` for repository, issues, and `state_collapser`;
- add classifiers if publishing a package;
- decide whether to add a CLI script:

  ```text
  bbb = "big_boy_benchmarking.cli.main:main"
  ```

  or keep `python -m big_boy_benchmarking.cli`;

- verify `uv build`;
- inspect wheel contents;
- decide whether PyPI is in scope.

Important dependency note:

```text
state-collapser[rl] @ git+https://github.com/TYLERSFOSTER/state_collapser.git@v0.7.2
```

is probably acceptable for a GitHub-source beta, but it may be a blocker for
PyPI publication depending on the package index policy. If PyPI is desired,
`state_collapser` should likely be released to PyPI first or BBB should avoid a
direct Git dependency in published metadata.

#### PO Reply
> I agree.

#### Codex Turn
Accepted. This means package metadata work is in scope for beta preparation.
The first decision inside that workstream is whether beta means "GitHub source
release only" or "installable package." Even for a GitHub-only beta, `project.urls`,
classifiers, and a clear CLI entry point would make the repo feel much more
public-ready.

I would not assume PyPI yet. The direct git dependency on `state_collapser`
should be treated as acceptable for a GitHub beta but a likely blocker or
policy issue for PyPI.

### P0.10 License, Citation, And Governance

MIT license exists and is public-ready.

Before public beta, consider adding:

- `CHANGELOG.md`;
- `CITATION.cff` if this is research-facing;
- `SECURITY.md`;
- issue templates;
- pull request template;
- code of conduct if public contributions are expected.

These are not all mandatory for a private-to-public beta, but `CHANGELOG.md`
and issue templates would help.

#### PO Reply
> I agree.

#### Codex Turn
Accepted. For the beta, I would prioritize:

```text
CHANGELOG.md
GitHub issue templates
GitHub PR template
SECURITY.md
```

`CITATION.cff` is worth adding if the public repo is intended to support
research citation immediately. A code of conduct is useful if outside
contributors are expected soon, but it is not as urgent as changelog, issues,
and release notes for the first beta.

## P1 Release Polish

These can happen before beta if time allows, or shortly after.

### P1.1 Public Docs Split

Consider creating:

```text
docs/calibration_smoke/
docs/benchmarking/
```

`docs/calibration_smoke/` would summarize current work.

`docs/benchmarking/` would be a placeholder for the next layer and explicitly
say:

```text
Benchmarking is not just smoke artifacts with a louder name.
```

### P1.2 Human Report Cards

Current readouts are good but long. Public beta would benefit from one compact
table per environment:

```text
Environment | Calibration status | Best current signal | Claim boundary | Report
```

For PlateSupport, the public card should say:

```text
Promising smoke-scale target signal. Tower 25/128 target hits vs direct 15/128;
zero invalid tower moves vs 2142 direct invalid moves. Not a general benchmark
claim.
```

For counterpoint, the card should say:

```text
Mature diagnostic machinery and weak bounded Schema 1 margin signal. Not a
settled learning advantage.
```

### P1.3 Reproducible Command Pages

Make a public `docs/runbooks/` or `docs/calibration_smoke/runbooks/` with:

- quick smoke command;
- PlateSupport gauntlet command;
- counterpoint threshold-frontier command;
- readout regeneration command;
- expected runtime and outputs.

The current README has commands, but public docs should make command selection
less intimidating.

### P1.4 Release Notes

Create initial beta release notes:

```text
v0.1.0-beta.1
```

Proposed release-note sections:

- "What is included";
- "Current calibration/smoke reports";
- "What this release does not claim";
- "state_collapser compatibility";
- "Known limitations";
- "Next: Benchmarking component".

### P1.5 Asset Cleanup

Audit:

```text
assets/images/
```

Questions:

- Are all images intended for public release?
- Is `assets/images/.$diagrams.xml.bkp` accidental?
- Are image names and source files clean?
- Should the logo be used in README only, or docs pages too?

## P2 Future Benchmarking Component

The future Benchmarking layer should be designed after beta release prep.

It should likely include:

- a formal benchmark registry;
- frozen benchmark ids and versioned benchmark suites;
- artifact bundle specification;
- public benchmark run manifest;
- environment family cards;
- scoring metric definitions;
- budget tiers;
- seed policy for public comparisons;
- leaderboard policy, if any;
- claim language templates;
- statistical reporting requirements;
- minimum-run gates before a result can be promoted from calibration to
  benchmark.

Suggested public transition:

```text
Calibration / Smoke proves that the machinery is working and reveals where the
system is fragile.

Benchmarking measures stable, predeclared comparisons at enough scale to support
stronger claims.
```

## Concrete Release Prep Checklist

### Documentation

- Rewrite root README around Calibration / Smoke and future Benchmarking.
- Update `docs/README.md`.
- Update `docs/evaluations/README.md`.
- Add public `docs/calibration_smoke/` overview or equivalent.
- Add public `docs/benchmarking/README.md` placeholder.
- Decide whether `docs/design/`, `docs/prime_directive/`, and
  `docs/engineer_continuity/` stay public.
- If internal docs stay public, add an explicit note explaining their purpose.
- Remove or sanitize raw conversational clarifying-turn sections from public
  readouts.
- Normalize all public links to relative paths.

### Artifacts

- Decide whether raw artifacts stay in git.
- If not, move raw artifacts to release assets, LFS, DVC, or a cleaned private
  archival branch.
- Normalize artifact manifests and readout sources to portable paths.
- Regenerate human-readable reports after path normalization.
- Keep compact summary tables in git if they are needed by public readouts.

### Source

- Replace hard-coded `<repo-root>` source strings with
  runtime repo-root or symbolic manifest values.
- Update generated runbook writers to use `$BBB_ROOT`, `<repo-root>`, or
  relative paths.
- Add or document a public CLI entry point.
- Add package metadata URLs/classifiers.
- Verify `uv build`.

### Tests And CI

- Add GitHub Actions CI.
- Run full local `uv run pytest`.
- Run `uv run ruff check .`.
- Run `git diff --check`.
- Add a release hygiene test or script that fails on hard-coded local paths in
  source/public docs.
- Add a release hygiene test or script that flags tracked cache/sidecar files.

### Cross-Repo

- Update `state_collapser` docs to link here.
- Update this repo to say it is official for `state_collapser` benchmarking.
- Add compatibility table.
- Decide whether `state_collapser` needs a new release before BBB public beta.

### GitHub Release

- Decide tag name:

  ```text
  v0.1.0-beta.1
  ```

  or

  ```text
  v0.1.0
  ```

- Create release notes.
- Attach artifact bundle if raw artifacts move out of git.
- Turn repo public only after public-doc cut and path cleanup.

## Recommended Implementation Sequence

### Phase 1: Release Boundary Decision

Decide:

- public docs cut versus open-lab notebook;
- raw artifacts in git versus external artifact bundle;
- source-only GitHub beta versus package publication;
- exact beta tag name.

No implementation should begin until these are settled, because they determine
whether we delete/move/sanitize large portions of docs.

### Phase 2: Public Framing Docs

Implement:

- root README rewrite;
- docs index rewrites;
- Calibration / Smoke overview;
- Benchmarking placeholder;
- cross-repo link text.

### Phase 3: Path And Artifact Portability

Implement:

- source hard-coded path removal;
- readout-source path normalization;
- public artifact policy;
- regenerated readouts.

### Phase 4: Source/Package/CI Hygiene

Implement:

- CI;
- package metadata;
- build verification;
- release hygiene scans.

### Phase 5: Public Beta Release

Implement:

- final tests;
- tag;
- release notes;
- artifact bundle upload if needed;
- GitHub visibility change;
- `state_collapser` README/link PR or commit.

## Open Questions For Project Owner

These are consultant-authored questions, not settled decisions.

1. Should `docs/design/`, `docs/prime_directive/`, and
   `docs/engineer_continuity/` be public in the beta, or should the public beta
   publish a cleaned documentation cut?

2. Should raw artifact directories stay in git for beta, or should they move to
   GitHub release assets / LFS / another artifact store?

3. Is the beta release source-only on GitHub, or should `big-boy-benchmarking`
   also be packaged for PyPI?

4. Is the release tag `v0.1.0-beta.1`, `v0.1.0`, or something else?

5. Should the public component name be exactly:

   ```text
   Big Boy Calibration / Smoke
   ```

   or should it be shortened in public docs to `Calibration / Smoke`?

6. Should the root TeX paper remain in the public benchmarking repo, move to a
   paper-specific repo, or remain private until it is ready?

7. Should `state_collapser` v0.7.2 remain the beta compatibility target, or do
   we want a fresh `state_collapser` release before the BBB public beta?

## Current Recommendation

The safest public beta path is:

```text
1. Keep this repo's code, environment docs, method docs, and human readouts.
2. Reframe all current executed work as Big Boy Calibration / Smoke.
3. Move or hide raw internal design/continuity/protocol chat history unless the
   Project Owner explicitly wants open-lab transparency.
4. Normalize all local paths.
5. Move large raw artifacts out of normal git or publish them as a separate
   release artifact bundle.
6. Add CI and package metadata.
7. Cross-link from state_collapser.
8. Tag v0.1.0-beta.1.
```

This gives the public a coherent repo:

```text
state_collapser = core library
big_boy_benchmarking = official Calibration / Smoke and future Benchmarking repo
```

without overclaiming the current evidence or exposing avoidable internal
working-memory noise.
