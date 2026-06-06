# PlateSupport Readout And System Learning Implementation Workplan

## Status

Status: initial implementation workplan.

This document is generated from:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/07_readout_and_system_learning/01_001_plate_support_readout_and_system_learning_blueprint.md
```

This workplan depends on all previous standard gauntlet component workplans:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/00_suite_architecture/01_002_plate_support_standard_gauntlet_suite_architecture_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/01_structural_and_tower_diagnostics/01_002_plate_support_structural_and_tower_diagnostics_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/02_contraction_schema_sweep/01_002_plate_support_contraction_schema_sweep_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/03_candidate_discovery/01_002_plate_support_candidate_discovery_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/04_tower_training_health/01_002_plate_support_tower_training_health_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/05_threshold_frontier_calibration/01_002_plate_support_threshold_frontier_calibration_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/06_paired_replicate_comparison/01_002_plate_support_paired_replicate_comparison_implementation_workplan.md
```

This workplan uses `Phase.Stage.Action` discipline.

This workplan is not execution approval. Execution requires explicit Project
Owner instruction.

## Prime Directive Compliance Notes

This workplan follows:

- `docs/prime_directive/prime_directive.md`;
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`;
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`;
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`;
- `docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md`;
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`.

Operational consequences:

- Execute only after Project Owner approval.
- Do not generate human readouts from memory.
- Do not infer "last run."
- Do not overwrite populated clarification conversation turns.
- Do not fabricate Project Owner, evaluator, consultant, engineer, or Codex
  turns.
- Do not overwrite system-learning archives during readout regeneration.
- Do not claim broad tower superiority from a first gauntlet run.

## Authority And Attribution

Project Owner direction from the current request:

- create this staged workplan after the paired replicate comparison workplan;
- follow the blueprint and Phase.Stage.Action discipline;
- reference prior work and dependencies.

Consultant-authored assumptions pending Project Owner override:

- first implementation generates one top-level suite README with linked
  per-stage result files;
- per-stage READMEs can remain separate but are not required as duplicate
  suite-level surfaces;
- system-learning archive is created only when a durable lesson exists;
- top-level badge strip uses at most ten badges;
- generated clarification sections use role labels and preserve actual
  authored content.

These assumptions are not Project Owner decisions.

## Decision Locks Before Implementation

- The canonical readout invocation is:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```

- The invocation target is the suite-level `readout_source.json`, not the
  artifact root and not a raw evaluation subdirectory.
- Generated readouts live under:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/
```

- Raw artifacts live under:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/<run-label>/
```

- Durable system learning lives under:

```text
docs/design/system_learning_from_evaluations/plate_support_standard_gauntlet_v001/
```

- Generated readouts are allowed to be regenerated; system-learning archives are
  not generated-result scratch space.
- Every status, badge, and claim must be grounded in artifact tables or
  manifests.

## Expected Final Deliverables

Implementation should produce or update:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/readout_system_learning/
tests/environments/plate_support/test_standard_gauntlet_readout_system_learning.py
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/
docs/design/system_learning_from_evaluations/plate_support_standard_gauntlet_v001/
docs/design/first_plate_support_environment/standard_gauntlet_suite/07_readout_and_system_learning/01_003_plate_support_readout_and_system_learning_implementation_log.md
```

Recommended package files:

```text
__init__.py
config.py
stage_sources.py
suite_status.py
claim_summary.py
badges.py
markdown_writer.py
artifact_index.py
glossary.py
runbook.py
system_learning.py
runner.py
```

Recommended CLI surface:

```bash
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet readout build \
  --readout-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```

The CLI may be useful, but the human/LLM protocol surface remains the canonical
instruction:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```

## Workplan

### Phase 0: Execution Setup And Protocol Binding

#### Phase 0.Stage 1: Re-anchor Repository And Sources

##### Phase 0.Stage 1.Action 1: Verify branch and dirty state

Action:

- run `git status --short --branch`;
- record branch and dirty files in the Stage 7 implementation log.

Completion criteria:

- repo state is known before edits.

Stop condition:

- stop if unrelated dirty files would be overwritten or confused with Stage 7.

##### Phase 0.Stage 1.Action 2: Verify suite-level readout source

Action:

- inspect:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```

- confirm it exists or can be generated by the architecture component.

Completion criteria:

- suite readout source is the explicit source binding.

Stop condition:

- stop if no explicit readout source exists and implementation would infer last
  run.

##### Phase 0.Stage 1.Action 3: Verify stage readout/source availability

Action:

- inspect available stage source bindings for Stages 1 through 6;
- record which stages ran, blocked, or are not run.

Completion criteria:

- Stage 7 knows which stage inputs exist.

Stop condition:

- stop if a source binding points outside repo or to raw artifact root instead
  of readout source.

##### Phase 0.Stage 1.Action 4: Re-read readout protocol

Action:

- re-read `docs/prime_directive/artifact_table_to_readable_document_protocol.md`
  before implementing readout generation behavior.

Completion criteria:

- implementation log records protocol version/source.

Stop condition:

- stop if protocol contradicts this blueprint or workplan.

#### Phase 0.Stage 2: Create Implementation Log

##### Phase 0.Stage 2.Action 1: Create Stage 7 implementation log

Action:

- create:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/07_readout_and_system_learning/01_003_plate_support_readout_and_system_learning_implementation_log.md
```

Completion criteria:

- log exists before source edits.

Stop condition:

- stop if log path conflicts with unrelated content.

##### Phase 0.Stage 2.Action 2: Add progress table and source map

Action:

- add Phase.Stage.Action progress table;
- add source map for suite and stage readout sources.

Completion criteria:

- readout generation provenance is auditable.

Stop condition:

- stop if source map cannot distinguish generated readout from raw artifact
  roots.

### Phase 1: Readout Package And Configuration

#### Phase 1.Stage 1: Create Readout/System-Learning Package

##### Phase 1.Stage 1.Action 1: Create module directory

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/readout_system_learning/
```

Completion criteria:

- package is nested under standard gauntlet suite.

Stop condition:

- stop if suite package is missing.

##### Phase 1.Stage 1.Action 2: Add module initializer

Action:

- create `__init__.py` exporting stable config/runner symbols.

Completion criteria:

- import does not generate docs or mutate files.

Stop condition:

- stop if import reads artifacts or writes generated readouts.

#### Phase 1.Stage 2: Define Readout Config

##### Phase 1.Stage 2.Action 1: Implement config dataclass

Action:

- create `config.py`;
- include:
  - suite readout source;
  - repo readout surface;
  - artifact root;
  - run label;
  - stage source paths;
  - generated output paths;
  - system-learning archive root;
  - preserve clarification turns flag;
  - create system-learning archive flag.

Completion criteria:

- all paths come from explicit source binding or explicit args.

Stop condition:

- stop if config depends on "last run" or current working directory.

##### Phase 1.Stage 2.Action 2: Validate readout source contract

Action:

- validate required fields:
  - protocol version;
  - suite id;
  - environment ids;
  - run label;
  - artifact root;
  - target directory;
  - stage readout source paths;
  - badge source paths;
  - method/runbook/glossary sources.

Completion criteria:

- missing fields produce controlled protocol block.

Stop condition:

- stop if readout source cannot identify source artifact root.

### Phase 2: Stage Source Collection

#### Phase 2.Stage 1: Load Stage Sources

##### Phase 2.Stage 1.Action 1: Implement stage source loader

Action:

- create `stage_sources.py`;
- load available Stage 1 through Stage 6 readout sources and stage summary
  tables.

Completion criteria:

- loader returns a normalized per-stage source record.

Stop condition:

- stop if stage source path is ambiguous or outside repo.

##### Phase 2.Stage 1.Action 2: Classify stage availability

Action:

- classify each stage as:
  - `complete`;
  - `complete_with_warning`;
  - `blocked`;
  - `not_run`;
  - `legacy_only`.

Completion criteria:

- unavailable stages are represented as not run/blocked rather than omitted.

Stop condition:

- stop if missing stage files cannot be classified by expected-file policy.

#### Phase 2.Stage 2: Collect Key Stage Facts

##### Phase 2.Stage 2.Action 1: Extract structural facts

Action:

- collect Stage 1 key numbers:
  - valid states;
  - valid non-self edges;
  - shortest path;
  - random policy recon;
  - downstream readiness.

Completion criteria:

- README can state task context without raw CSV inspection.

Stop condition:

- stop if structural facts are unavailable but Stage 1 is marked complete.

##### Phase 2.Stage 2.Action 2: Extract schema/candidate/health/calibration/comparison facts

Action:

- collect:
  - Stage 2 schema signal counts;
  - Stage 3 selected/blocked candidate counts;
  - Stage 4 training-health statuses;
  - Stage 5 recommended target or block reason;
  - Stage 6 claim status or non-run reason.

Completion criteria:

- suite-level result paragraph can be generated from evidence.

Stop condition:

- stop if any fact would need to be inferred from prose.

### Phase 3: Suite Status, Claim Summary, And Badges

#### Phase 3.Stage 1: Produce Status Tables

##### Phase 3.Stage 1.Action 1: Write stage status summary

Action:

- write `results/stage_status_summary.csv` with columns from the blueprint.

Completion criteria:

- every stage has a row.

Stop condition:

- stop if any stage status is unknown without reason.

##### Phase 3.Stage 1.Action 2: Write suite status summary

Action:

- write `results/suite_status_summary.csv`.

Completion criteria:

- suite status maps to allowed status vocabulary:
  - `complete_claim_ready`;
  - `complete_limited_signal`;
  - `complete_inconclusive`;
  - `complete_no_comparison`;
  - `blocked_before_training`;
  - `blocked_before_comparison`;
  - `artifact_incomplete`;
  - `legacy_only`.

Stop condition:

- stop if status would imply a claim unsupported by stage outputs.

##### Phase 3.Stage 1.Action 3: Write suite claim summary

Action:

- write `results/suite_claim_summary.csv`;
- if Stage 6 did not run, write blocked/not-applicable row rather than
  omitting the table.

Completion criteria:

- suite-level claim is present, bounded, and traceable.

Stop condition:

- stop if Stage 6 claim language is too strong or unavailable.

#### Phase 3.Stage 2: Generate Badges

##### Phase 3.Stage 2.Action 1: Implement badge policy

Action:

- create `badges.py`;
- derive badge values from status/claim/artifact tables.

Completion criteria:

- badges are data-derived, not hand-authored optimism.

Stop condition:

- stop if badge status cannot be traced to a table/source column.

##### Phase 3.Stage 2.Action 2: Write badge SVGs

Action:

- write badges for:
  - suite status;
  - artifacts complete;
  - structural readiness;
  - schema candidates;
  - training health;
  - target calibrated;
  - paired comparison status;
  - claim status;
  - liftability semantics;
  - provenance repo artifacts.

Completion criteria:

- badge SVGs exist under `badges/`.

Stop condition:

- stop if badge count or meaning becomes noisy/ambiguous.

### Phase 4: Generated Human Documents

#### Phase 4.Stage 1: Generate Top-Level README

##### Phase 4.Stage 1.Action 1: Preserve existing clarification section

Action:

- before rewriting README, parse and preserve populated clarification
  conversation content.

Completion criteria:

- existing human-authored clarification turns are not overwritten.

Stop condition:

- stop if clarification attribution cannot be parsed safely.

##### Phase 4.Stage 1.Action 2: Write README

Action:

- write `README.md` with:
  - title;
  - badge block;
  - one-paragraph result;
  - what the suite tested;
  - current conclusion;
  - stage status table;
  - key numbers;
  - claim boundary;
  - links to details;
  - artifact provenance;
  - clarification conversation section.

Completion criteria:

- README is human-readable and bounded.

Stop condition:

- stop if README would need to invent absent stage results.

#### Phase 4.Stage 2: Generate Supporting Docs

##### Phase 4.Stage 2.Action 1: Write result readout

Action:

- write `result_readout.md` with stage-by-stage narrative, key numeric results,
  claim status, caveats, and recommended next work.

Completion criteria:

- narrative is grounded in stage status and summary tables.

Stop condition:

- stop if narrative overstates a blocked/inconclusive result.

##### Phase 4.Stage 2.Action 2: Write method doc

Action:

- write `method.md` covering environment, baseline policy, schema sweep,
  candidate selection, training health, calibration, paired comparison, seeds,
  dependencies, and artifact provenance.

Completion criteria:

- method source does not require reading code to know what was tested.

Stop condition:

- stop if methodology differs by run mode and cannot be described.

##### Phase 4.Stage 2.Action 3: Write artifact index

Action:

- write `artifact_index.md` with top-level artifact root, stage artifact roots,
  raw run dirs, summary table paths, manifest paths, generated readout paths,
  and dependency manifests.

Completion criteria:

- a human can find every key artifact.

Stop condition:

- stop if artifact paths are non-repo-resident for durable readout.

##### Phase 4.Stage 2.Action 4: Write glossary

Action:

- write `glossary.md` with required terms from the blueprint.

Completion criteria:

- specialized terms are explained in human-readable language.

Stop condition:

- stop if definitions would require new design decisions.

##### Phase 4.Stage 2.Action 5: Write runbook

Action:

- write `runbook.md` with environment assumptions, dependency check, artifact
  root policy, run/summarize command patterns, readout-generation command,
  cleanup policy, and provenance notes.

Completion criteria:

- runbook repeats the explicit readout invocation:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```

Stop condition:

- stop if runbook suggests folder-based or last-run-based readout generation.

#### Phase 4.Stage 3: Generate Results Detail Files

##### Phase 4.Stage 3.Action 1: Write stage detail readouts

Action:

- write:
  - `results/summary.md`;
  - `results/stage_status.md`;
  - `results/structural_readout.md`;
  - `results/schema_sweep_readout.md`;
  - `results/candidate_readout.md`;
  - `results/training_health_readout.md`;
  - `results/threshold_frontier_readout.md`;
  - `results/paired_comparison_readout.md`.

Completion criteria:

- each file explains stage results, status, caveats, and source artifacts.

Stop condition:

- stop if a stage did not run and detail file would pretend it did.

##### Phase 4.Stage 3.Action 2: Write system learning prompt

Action:

- write `results/system_learning_prompt.md`.

Completion criteria:

- prompt explains when and where to preserve durable learning.

Stop condition:

- stop if prompt implies generated README conversations are permanent design
  memory.

### Phase 5: System-Learning Archive

#### Phase 5.Stage 1: Prepare Archive Area

##### Phase 5.Stage 1.Action 1: Create archive root when triggered

Action:

- create:

```text
docs/design/system_learning_from_evaluations/plate_support_standard_gauntlet_v001/
```

only when an archive trigger condition is met or Project Owner asks for it.

Completion criteria:

- archive root exists only for durable learning, not every run by default.

Stop condition:

- stop if archive creation trigger is ambiguous.

##### Phase 5.Stage 1.Action 2: Write archive README

Action:

- write archive `README.md` explaining purpose, links, attribution policy, and
  relationship to generated readouts.

Completion criteria:

- future LLMs can detect the archive and understand its role.

Stop condition:

- stop if archive would duplicate generated readout without durable lesson.

#### Phase 5.Stage 2: Preserve Durable Learning

##### Phase 5.Stage 2.Action 1: Archive readout conversation when needed

Action:

- create or update `01_readout_conversation_archive.md` with actual relevant
  conversation, preserving attribution.

Completion criteria:

- Project Owner-authored content is only labeled Project Owner when actually
  authored by the Project Owner.

Stop condition:

- stop if attribution cannot be verified.

##### Phase 5.Stage 2.Action 2: Write issue and correction notes

Action:

- create or update `02_issue_and_correction_notes.md` with:
  - issue;
  - how it appeared;
  - why it mattered;
  - artifacts involved;
  - correction made or proposed;
  - whether it affects implementation, protocol, docs, or future design.

Completion criteria:

- notes are compact and useful without replacing the transcript.

Stop condition:

- stop if notes would invent causality not supported by evidence.

##### Phase 5.Stage 2.Action 3: Write follow-up design questions

Action:

- create or update `03_follow_up_design_questions.md`.

Completion criteria:

- unresolved questions and known non-goals are preserved.

Stop condition:

- stop if questions are presented as Project Owner decisions.

### Phase 6: Root Documentation Integration

#### Phase 6.Stage 1: Update Root Docs If Appropriate

##### Phase 6.Stage 1.Action 1: Inspect root README and CONTRIBUTING

Action:

- inspect root docs for evaluation listings and workflow language.

Completion criteria:

- current root documentation state is known.

Stop condition:

- stop if root docs have unrelated user edits that need preservation.

##### Phase 6.Stage 1.Action 2: Add links to PlateSupport gauntlet readout

Action:

- update root README and/or CONTRIBUTING only if implementation has created a
  real readout worth linking.

Completion criteria:

- root docs give digest and links, not raw table detail.

Stop condition:

- stop if gauntlet readout has not run or is only a placeholder.

### Phase 7: CLI Or Protocol Helper

#### Phase 7.Stage 1: Add Optional CLI Readout Builder

##### Phase 7.Stage 1.Action 1: Add readout build command if useful

Action:

- add optional command:

```text
plate-support standard-gauntlet readout build
```

accepting an explicit `--readout-source`.

Completion criteria:

- command reads explicit source binding and writes generated docs.

Stop condition:

- stop if command weakens or replaces the prime-directive protocol invocation.

##### Phase 7.Stage 1.Action 2: Add readout inspect command if useful

Action:

- add optional inspect command that validates source binding and reports stage
  availability without writing docs.

Completion criteria:

- inspect command helps diagnose source-binding problems.

Stop condition:

- stop if inspect command infers last run.

### Phase 8: Tests And Verification

#### Phase 8.Stage 1: Unit Tests

##### Phase 8.Stage 1.Action 1: Test readout source validation

Action:

- test missing source, wrong filename, outside-repo source, artifact-root target,
  raw evaluation-root target, and valid source binding.

Completion criteria:

- invalid invocation surfaces block according to protocol.

Stop condition:

- stop if protocol behavior differs from implementation.

##### Phase 8.Stage 1.Action 2: Test stage status synthesis

Action:

- test complete, warning, blocked, not-run, and legacy-only stage cases.

Completion criteria:

- stage status table is complete and deterministic.

Stop condition:

- stop if missing stage files are classified ambiguously.

##### Phase 8.Stage 1.Action 3: Test badge generation

Action:

- test badges derive from source tables and include label, value, status class,
  color, source table, source column, and reason.

Completion criteria:

- badge without evidence fails tests.

Stop condition:

- stop if badge policy needs design revision.

##### Phase 8.Stage 1.Action 4: Test clarification preservation

Action:

- test regeneration preserves populated clarification content and adds an empty
  pair only when none exists.

Completion criteria:

- human-authored clarification text is not overwritten.

Stop condition:

- stop if attribution parsing is unsafe.

##### Phase 8.Stage 1.Action 5: Test false-attribution scan

Action:

- test generated docs do not contain forbidden false-attribution headings or
  phrases.

Completion criteria:

- false attribution fails tests.

Stop condition:

- stop if generated clarification labels are ambiguous.

##### Phase 8.Stage 1.Action 6: Test no last-run semantics

Action:

- test readout generation requires explicit source binding.

Completion criteria:

- there is no API path that silently uses the latest run.

Stop condition:

- stop if convenience helpers bypass source-binding validation.

#### Phase 8.Stage 2: Generated Readout Smoke

##### Phase 8.Stage 2.Action 1: Generate readout from fixture source

Action:

- run readout generation against a controlled fixture or real repo-local suite
  source.

Completion criteria:

- generated docs and badges are written under the repo readout surface.

Stop condition:

- stop if generated docs are written into raw artifact tree.

##### Phase 8.Stage 2.Action 2: Inspect generated README

Action:

- verify README includes badge block, result paragraph, stage status table,
  claim boundary, artifact provenance, and clarification section.

Completion criteria:

- README is readable and bounded.

Stop condition:

- stop if README overclaims or omits blocked stage reasons.

##### Phase 8.Stage 2.Action 3: Inspect system-learning behavior

Action:

- verify system-learning archive is not created unless triggered, and is never
  overwritten during readout regeneration.

Completion criteria:

- generated readout and durable archive are separate surfaces.

Stop condition:

- stop if archive behavior could erase design memory.

#### Phase 8.Stage 3: Final Log Update

##### Phase 8.Stage 3.Action 1: Record validation and final suite handoff

Action:

- update Stage 7 implementation log with:
  - source binding used;
  - generated files;
  - badge count/status;
  - suite status;
  - claim status;
  - system-learning archive action;
  - tests run.

Completion criteria:

- log records whether the standard gauntlet suite is readable and auditable.

Stop condition:

- stop if generated docs cannot be traced to source artifacts.

## Completion Criteria For The Component

Stage 7 is complete when:

- suite readout source validation exists;
- stage source loading handles complete/warning/blocked/not-run stages;
- suite status, stage status, and suite claim summaries are generated;
- badges are evidence-derived;
- README, result readout, method, artifact index, glossary, runbook, and
  results detail files are generated;
- clarification turns are preserved without false attribution;
- optional system-learning archive behavior is implemented safely;
- root docs are updated only when a real readout exists;
- explicit protocol invocation is documented;
- tests pass;
- implementation log records Phase.Stage.Action completion.

## Final Handoff For The Standard Gauntlet Suite

After this component, the PlateSupport standard gauntlet implementation should
have a complete staged design-to-implementation path:

1. architecture and contracts;
2. structural/tower diagnostics;
3. contraction schema sweep;
4. candidate discovery;
5. tower training health;
6. threshold calibration;
7. paired comparison;
8. human readout and system learning.

The suite should be executable only through explicit artifact roots and explicit
readout source bindings, and the human-readable output should explain exactly
what happened, what it means, what it does not mean, and where the machine
evidence lives.
