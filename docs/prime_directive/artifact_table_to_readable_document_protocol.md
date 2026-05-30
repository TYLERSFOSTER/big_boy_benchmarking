# Artifact Tables To Readable Documents Protocol

## Status

Proposed prime-directive adjunct.

This document is directed to future Embedded Engineering Consultants working in
this repository.

Its purpose is to define how machine-readable benchmark artifacts, especially
tables, should be translated into human-readable documents without losing
evidence, hiding failures, or inventing claims.

## Problem

Benchmark systems naturally produce files that are readable to engineers:

- JSON manifests;
- CSV aggregate tables;
- CSV event rows;
- timing summaries;
- run indices;
- diagnostic rows;
- artifact indexes.

Those files are necessary. They are not sufficient.

A human reader who does not already know the benchmark internals should not have
to infer the story from:

- raw arm ids;
- path-heavy artifact indexes;
- nested run directories;
- status fields that mean "artifact complete" rather than "behavior successful";
- diagnostic details buried several files away from the summary;
- local abbreviations such as `lift`, `fiber`, `schema`, `tier`, or `mode`.

The core failure mode is:

```text
machine evidence exists, but the human-facing document does not translate it
into a truthful, readable explanation.
```

## Core Rule

> A result document must tell the reader what happened, how we know, what it
> means, what it does not mean, and where the machine evidence lives.

Do not treat a table copy, artifact index, or manifest list as a human result
report.

Do not summarize away the evidence.

The readable document must preserve the path back to the artifacts while
explaining the artifacts in ordinary engineering language.

## Non-Negotiable Path Invariants

The protocol has three different path roles. Do not merge them.

```text
repo_readout_surface:
  The folder named by the Project Owner in the invocation.
  The human-readable files are written here.
  This folder is inside this repository.

source_artifact_root:
  The raw benchmark artifact root.
  This may be temporary, such as /private/tmp/...
  This is evidence metadata, not the invocation target.

source_evaluation_root:
  The evaluation subfolder containing aggregate tables and result tables.
  This is evidence metadata, not the invocation target.
```

The invocation folder always means `repo_readout_surface`.

If the Project Owner accidentally points the command at `source_artifact_root`
or `source_evaluation_root`, stop and ask for the repo-side readout surface.
Do not write generated readouts into the raw artifact tree unless the Project
Owner explicitly asks for an artifact-local temporary dump.

## Consultant Invocation Surface

This protocol defines a you-readable surface: a natural-language command the
Project Owner can give to an Embedded Engineering Consultant without needing a
separate shell script.

The canonical invocation is:

```text
execute artifact-table readout pointed at folder <folder>
```

Equivalent accepted invocations:

```text
execute human-readable evaluation readout pointed at folder <folder>
apply artifact-table-to-readable-document protocol to folder <folder>
apply the readable-doc protocol to this repo readout folder: <folder>
make the human readout in <folder>
```

When the Project Owner gives one of these commands, the consultant must treat it
as an instruction to:

1. read this protocol;
2. resolve the supplied folder as a repository-side readout surface;
3. read that surface's source binding to find the machine-readable artifacts;
4. write the human-readable files required by this protocol;
5. report exactly what was written and what could not be interpreted.

The Project Owner should not need to restate the document shape, claim-boundary
rules, all-cases protocol, or evidence discipline. Those are supplied by this
protocol.

### Reminder Rule

When the conversation touches any of the following:

- evaluation artifacts;
- unreadable result tables;
- aggregate CSVs;
- result docs;
- benchmark evidence;
- "what happened in this run?";
- "how do I read this?";
- "make this human-readable";
- confusion about `complete` versus successful behavior;
- confusion about zero, null, missing, or failed metrics;

the consultant should remind the Project Owner of the invocation surface:

```text
execute artifact-table readout pointed at folder <folder>
```

The reminder should be short and optional, not a derailment.

Good reminder:

```text
For this repo, the protocol surface is:
execute artifact-table readout pointed at folder <folder>
```

Here `<folder>` means the repo-side readout surface, usually somewhere under
`docs/evaluations/`. It does not mean the raw artifact directory.

Bad reminder:

```text
Here is a new multi-step workflow you should follow...
```

Do not repeatedly remind the Project Owner inside the same local conversation
unless the Project Owner appears to be searching for the command again.

### Folder Resolution

The invocation must include an explicit repository folder. Relative folders are
resolved from the repository root. Do not infer "last run" unless the Project
Owner explicitly adds a reliable repo surface or marker.

The supplied `<folder>` is the repo-side readout surface. It is not the raw
artifact root and it is not the raw evaluation root.

For this repository's first serious counterpoint evaluation, the normal command
target is:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning
```

Resolve the supplied folder as follows:

1. If the folder is outside the repository, stop. Tell the Project Owner that
   the protocol must be pointed at a repo-side readout surface, not the raw
   artifact directory.
2. If the folder does not exist but its parent exists inside the repository,
   create it only when the Project Owner's command clearly names the intended
   repo readout surface.
3. If the folder contains `readout_source.json`, read it and use its source
   paths to find the raw artifact tables.
4. If the folder contains `artifact_index.md` with concrete source paths, use
   those paths only if no `readout_source.json` exists, and write
   `readout_source.json` as part of the readout.
5. If the folder contains only placeholder paths such as `<artifact-root>`,
   stop and ask for the source artifact root, unless the source can be
   established from explicit Project Owner context already present in the
   conversation. If that context is used, record it in `readout_source.json`.
6. If the folder itself contains raw tables such as
   `evaluation_aggregate_table.csv`, treat that as copied source evidence inside
   the repo surface, not as a reason to move the readout elsewhere. Write
   `readout_source.json` with repo-local source file paths.
7. If no source binding or copied source tables are found, apply Case 1: No
   Artifacts Found.

### Source Binding

Every repo readout surface should have a source binding file:

```text
<repo-readout-surface>/readout_source.json
```

It should record at least:

```json
{
  "repo_readout_surface": "<absolute repo path>",
  "source_artifact_root": "<raw artifact root>",
  "source_evaluation_root": "<raw evaluation root>",
  "evaluation_id": "<evaluation id>",
  "artifact_run_label": "<human run label>",
  "source_files": {
    "aggregate_table": "<path to evaluation_aggregate_table.csv>",
    "run_index": "<path to evaluation_run_index.csv>",
    "learning_curves": "<path to results/learning_curves.csv>"
  }
}
```

When possible, `readout_source.json` should also record expected-file policy so
the human readout can distinguish real missing evidence from files that are not
applicable to this run mode:

```json
{
  "expected_files": {
    "required": ["evaluation_budget_lock.json", "evaluation_run_index.csv"],
    "expected_absent_is_gap": [
      "evaluation_manifest.json",
      "evaluation_arm_manifest.json"
    ],
    "conditional": {
      "calibration": [
        "calibration_summary.json",
        "calibration_run_index.csv",
        "calibration_recommendation.md"
      ]
    },
    "not_applicable": []
  }
}
```

If the source binding lacks expected-file policy, do not flatten all absent
files into "missing evidence." Use the evaluation design docs, artifact
contract, run mode, and available manifests to classify each absent file as:

```text
present
expected_missing_gap
conditional_absent
not_applicable
unknown_expectation
```

The source artifact root may live in `/private/tmp`, another local artifact
directory, or a durable artifact store. That path is evidence metadata. It is
not the protocol invocation target.

If the source path is temporary, say so in the readable documents. Do not imply
that a `/private/tmp` source is a durable artifact archive. The repo readout is
durable documentation of the interpretation; the raw machine evidence remains
where the source binding says it remains.

### Output Location

Write the readable documents into the supplied repo readout surface.

For example:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning
```

Do not write under `docs/results/` unless the Project Owner explicitly asks to
promote a final result summary there.

Do not write under `/private/tmp`, an artifact root, or a raw evaluation root
unless the Project Owner explicitly asks for an artifact-local temporary dump.

### Execution Contract

The consultant must first resolve the source binding, then inspect, when
present:

- `evaluation_manifest.json`;
- `evaluation_arm_manifest.json`;
- `evaluation_budget_lock.json`;
- `evaluation_run_index.csv` or `calibration_run_index.csv`;
- `calibration_summary.json`;
- `evaluation_aggregate_summary.json`;
- `evaluation_aggregate_table.csv`;
- `results/learning_curves.csv`;
- `results/timing_summary.csv`;
- `results/controller_summary.csv`;
- `results/schema_diagnostic_summary.csv`;
- representative per-run `episodes.csv`;
- representative per-run `control_events.csv`;
- representative per-run `lift_fiber_events.csv`;
- representative per-run `warnings.jsonl`;
- representative per-run manifests needed to interpret claim boundaries.

If the artifact set is large, inspect representative per-run files for every
arm class and every anomalous condition before writing the final readout.

If a required source file listed in `readout_source.json` is absent, do not
silently reuse an older table. Classify it as `expected_missing_gap` and apply
the relevant all-cases rule.

If a source file is absent but not listed as required, classify expectation
before writing the report. For example, calibration files may be absent because
the source artifact root came from a manually locked serious run rather than a
calibration path. In that case, call them `conditional_absent` or
`not_applicable`; do not call them missing evidence unless the source binding,
blueprint, or run mode says they were expected for this artifact set.

### Output Contract

The default output set is:

```text
<repo-readout-surface>/
  readout_source.json
  README.md
  result_readout.md
  runbook.md
  artifact_index.md
  glossary.md
  results/
    summary.md
    human_summary.md
    arm_readout_table.md
    diagnostic_findings.md
    timing_readout.md
```

If the existing repo-local readout already contains some of these files, update
or replace them only as needed to satisfy this protocol. Preserve useful
existing runbook or artifact-index information.

If a prior version of this protocol wrote artifact-local docs under
`<evaluation-root>/docs/`, treat those files as non-authoritative temporary
readouts unless the Project Owner explicitly asks to preserve or migrate them.

### README Turn Surface

Every generated `README.md` must include a place for human/consultant turns
when clarification is needed. This is part of the readout surface, not a
separate design document.

Use these headings unless the Project Owner gives different labels:

```markdown
## Clarifying Questions And Turns

### Project Owner / Evaluator Turn

<!-- Record only explicit Project Owner or evaluator text here. Do not invent,
     smooth, or complete this side of the exchange. Leave blank if unanswered. -->

### Embedded Engineering Consultant / Codex Turn

<!-- Record Codex's clarifying question, interpretation check, or response
     here. Keep it tied to the artifact evidence and claim boundary. -->
```

Use this section for:

- unresolved source-binding questions;
- unclear claim boundaries;
- ambiguous zero/null/failure interpretation;
- missing baseline decisions;
- PO/evaluator corrections to the readout;
- Codex replies that explain how the report was changed or why a claim was
  blocked.

Do not use this section to narrate normal findings that already belong in the
verdict, result table, diagnostics, or evidence map.

Do not put words in the Project Owner's mouth. If the Project Owner has not
answered a question, leave the Project Owner / Evaluator turn blank or mark it
`Pending`.

### Completion Report

After executing this surface, report:

- the input folder, meaning the repo readout surface;
- the resolved source artifact root;
- the resolved source evaluation root;
- the files written;
- any absent artifacts, classified by expectation status;
- any stopped claim decisions;
- validation performed, if any.

Do not merely say "done" if the readout contains warnings or blocked claims.

## Translation Ladder

Every table-to-document translation must move through this ladder:

1. Artifact location
2. Artifact type
3. Field meaning
4. Observed values
5. Interpretation
6. Claim boundary
7. Inspection path

Example:

```text
evaluation_aggregate_table.csv
-> aggregate arm table
-> mean_return is average episode total reward
-> non-empty tower arms have mean_return 0.0 and step_count 0
-> these arms completed as artifact runs but failed behaviorally
-> this does not support a tower-performance claim
-> inspect lift_fiber_events.csv and control_events.csv for failure mechanism
```

Skipping steps creates misleading documents.

## Required Reader Layers

A readable benchmark report should serve three reader layers.

### 1. First-Contact Reader

This reader wants to know:

- what was run;
- whether it worked;
- what the big result was;
- whether any result is surprising or invalidating;
- whether the report is making a benchmark claim.

This reader should not need to understand file layout or internal ids.

### 2. Technical Reviewer

This reader wants:

- arm ids;
- exact budgets;
- seeds and schema seeds;
- baselines;
- confidence intervals;
- timing categories;
- diagnostic failure rates;
- artifact paths.

This reader should be able to audit the result without guessing which file
matters.

### 3. Future Engineer

This reader wants:

- what to rerun;
- which files to inspect first;
- what anomalies are already known;
- what implementation behavior may need fixing;
- which claims are allowed or blocked.

This reader should be able to resume work without rediscovering the same
interpretation from scratch.

## Required Document Shape

When generating or writing a human-facing result document from artifact tables,
use this shape unless the Project Owner asks for a different one.

### 1. Title

Name the evaluation, environment, and run class.

Bad:

```text
Results Summary
```

Better:

```text
Counterpoint First Serious Learning Evaluation - Human Readout
```

### 2. One-Screen Verdict

State the result in plain language.

The verdict must distinguish:

- artifact completion;
- behavioral success;
- benchmark claim support.

Example:

```text
All required arms produced artifacts. Direct arms and the empty tower arm
executed real environment steps and received nonzero return. The non-empty tower
arms completed artifact runs but produced zero-return, zero-step episodes due to
lift/action-realization failures. This run is therefore useful diagnostic
evidence, but it does not support a positive tower-performance claim.
```

### 3. Run Identity

Record:

- evaluation id;
- source artifact root;
- source evaluation root;
- repo readout surface;
- environment family and instance;
- run date/time if available;
- linearization mode;
- artifact schema version;
- command or runbook path;
- budget lock path if applicable.

### 4. Claim Boundary

Say exactly what the report may and may not claim.

The claim boundary must include:

- smoke, calibration, diagnostic, or serious run status;
- whether tensor execution is enabled or disabled;
- whether GPU/CUDA claims are excluded;
- whether musical-quality claims are excluded;
- whether general method superiority claims are excluded.

### 5. Arm Legend

Translate every arm id into a human label.

The legend should include:

- arm id;
- short label;
- method class;
- schema class if any;
- baseline role;
- expected interpretation.

Example labels:

```text
direct_tabular_q
Direct tabular Q baseline. Learns on concrete counterpoint states.

tower_random_balanced_exploit_explore_tabular_q
Tower controller with random balanced contraction schema. Tests whether this
schema supports action realization and learning under the tower interface.
```

### 6. Main Result Table

Do not paste the raw aggregate table as the only table.

Create a reader-facing table with:

- short arm label;
- artifact status;
- behavioral status;
- mean return;
- delta versus baseline;
- episode count;
- step count or mean step count;
- main warning;
- evidence file.

Raw statistical columns can follow in a technical appendix.

### 7. Diagnostic Findings

If any arm has surprising, zero, missing, failed, or inconsistent values, write a
diagnostic section.

This section should answer:

- what went wrong or changed;
- which artifacts show it;
- how widespread it is;
- whether it invalidates a claim;
- whether it indicates a code bug, environment fact, schema fact, or expected
  negative result.

### 8. Timing Readout

Timing tables must distinguish:

- total runtime;
- algorithm-online time;
- linearization setup;
- artifact logging;
- diagnostic/readout time;
- summary generation.

Do not compare methods on wall-clock timing unless the report says which timing
categories are included.

### 9. Evidence Map

End with an evidence map that tells the reader where to inspect:

- aggregate table;
- learning curves;
- timing summary;
- controller summary;
- schema diagnostics;
- run index;
- per-run event files;
- manifests;
- warnings.

The evidence map must say what each file is for.

### 9.1 Provenance Status

If any expected or commonly inspected files are absent, write a provenance
status section instead of a generic "missing evidence" section.

The provenance status must classify each absent file:

| Classification | Meaning |
| --- | --- |
| `expected_missing_gap` | The file is expected by the artifact contract for this run/evaluation and is absent. |
| `conditional_absent` | The file is expected only under a condition, such as calibration, and that condition is not established for this artifact set. |
| `not_applicable` | The file does not apply to this run mode or claim boundary. |
| `unknown_expectation` | The consultant cannot determine whether the file was expected. |

Do not use "missing" alone for files that may be conditional or not applicable.
Say what the expectation source is: source binding, blueprint, artifact
contract, CLI/run mode, or explicit Project Owner instruction.

For the counterpoint first serious learning readout, this means:

- `evaluation_manifest.json` and `evaluation_arm_manifest.json` are expected by
  the serious evaluation artifact contract; if absent, classify them as
  `expected_missing_gap`.
- `calibration_summary.json`, `calibration_run_index.csv`, and
  `calibration_recommendation.md` are calibration-path files; if the source
  artifact root is a manually locked serious run without calibration, classify
  them as `conditional_absent` or `not_applicable`, not as missing evidence.

### 10. Clarifying Questions And Turns

In `README.md`, include the turn surface defined above. The section may be
empty, but it must exist so the Project Owner, evaluator, and Codex have a
stable place to resolve report questions without scattering corrections across
the conversation.

If the readout has no open ambiguity, write:

```text
No open clarifying questions recorded for this readout.
```

If there is an open ambiguity, write the Codex turn as a concrete question or
interpretation check, and leave the Project Owner / Evaluator turn pending until
the human answers.

## All-Cases Protocol

Use this protocol whenever translating artifact tables to readable documents.

### Case 1: No Artifacts Found

Readable statement:

```text
No source artifacts could be resolved for this repo readout surface.
```

Required content:

- repo readout surface checked;
- source binding status;
- source artifact root checked, if known;
- source evaluation root checked, if known;
- expected files;
- absent files classified as `expected_missing_gap`, `conditional_absent`,
  `not_applicable`, or `unknown_expectation`;
- command to generate artifacts if known.

Forbidden:

- implying failure of the method;
- inventing a status;
- filling with placeholder performance text.

### Case 2: Smoke Run

Readable statement:

```text
This is a smoke run. It validates command execution and artifact writing only.
```

Required content:

- command run;
- artifact files written;
- pass/fail status;
- explicit non-claim boundary.

Forbidden:

- comparing performance as benchmark evidence;
- calling it "serious";
- using smoke results in method claims.

### Case 3: Calibration Run

Readable statement:

```text
This calibration estimates budget, runtime, artifact volume, noise, completion,
and failure modes. It is not the final result unless the Project Owner says so.
```

Required content:

- measured runtime;
- artifact volume;
- completion rate;
- curve-noise proxy if present;
- lift or controller failure indicators if present;
- proposed locked budget.

Forbidden:

- treating calibration as final evidence;
- hiding failure signals because the calibration status is complete.

### Case 4: Complete Artifact Run, Behavior Successful

Readable statement:

```text
Artifacts are complete and the behavior being measured succeeded.
```

Required content:

- completion evidence;
- behavioral success metric;
- baseline comparison;
- uncertainty or replicate count;
- claim boundary.

Forbidden:

- overclaiming beyond the benchmark condition;
- omitting the baseline.

### Case 5: Complete Artifact Run, Behavior Failed

Readable statement:

```text
Artifacts are complete, but the measured behavior failed.
```

Required content:

- which arms failed behaviorally;
- which fields show failure;
- which diagnostic rows explain failure;
- whether the failure is an implementation bug, schema limitation, controller
  limitation, or unresolved;
- whether the report is evidence against a claim or only diagnostic evidence.

This is the case that raw tables often hide.

Example signs:

- `status=complete` but `mean_return=0.0`;
- `success=False`;
- `step_count=0`;
- repeated invalid lift/action failures;
- controller events never reach execution;
- missing or empty final state.

### Case 6: Mixed Run

Readable statement:

```text
Some arms succeeded and others failed. The result must be interpreted arm by
arm.
```

Required content:

- per-arm status;
- per-arm behavioral status;
- grouped warnings;
- whether any baseline is missing;
- whether comparisons remain valid.

Forbidden:

- one global "success" label that hides failed arms;
- averaging failed and successful conditions without explanation.

### Case 7: Incomplete Run

Readable statement:

```text
The run is incomplete. Interpret available rows only as partial evidence.
```

Required content:

- completed arm count;
- missing arms;
- failed arms;
- absent files with expectation classification;
- whether rerun/resume is possible.

Forbidden:

- presenting partial tables as final;
- using missing arms as zero unless the artifact explicitly records zero.

### Case 8: Missing Baseline

Readable statement:

```text
The baseline needed for the intended comparison is missing.
```

Required content:

- intended baseline;
- missing artifact or arm;
- comparisons blocked;
- any still-readable descriptive metrics.

Forbidden:

- computing deltas against another arm without saying the baseline changed.

### Case 9: Zero Values

Zero is never self-explanatory.

For each zero in a primary metric, classify it as:

- legitimate measured zero;
- missing converted to zero;
- failed behavior converted to zero;
- impossible/unexpected zero;
- unresolved.

Required content:

- evidence for the classification;
- files inspected;
- effect on claim boundary.

### Case 10: Empty Values, Nulls, NaNs

Readable statement:

```text
Some fields were not produced or are not applicable.
```

Required content:

- whether empty means not applicable, missing, failed, or not computed;
- whether downstream statistics were skipped;
- whether the result remains interpretable.

Forbidden:

- treating null and zero as the same thing.

### Case 11: Outliers Or High Variance

Readable statement:

```text
The result varies substantially across seeds, schema seeds, or replicates.
```

Required content:

- which variance column shows it;
- whether variation is across environment seeds, schema seeds, or episodes;
- whether more runs are needed before a claim.

### Case 12: Timing Result

Readable statement:

```text
The timing result applies only to the recorded timing categories.
```

Required content:

- included categories;
- excluded categories;
- whether artifact logging is included;
- whether setup time is included;
- whether linearization setup is included.

Forbidden:

- presenting total runtime as algorithm speed without category explanation.

### Case 13: Diagnostic-Only Result

Readable statement:

```text
This result diagnoses structure or mechanism. It is not a learning-performance
claim.
```

Required content:

- diagnostic target;
- relevant counts/rates;
- what would count as healthy or unhealthy;
- whether it blocks a performance claim.

### Case 14: Claim-Supporting Result

Readable statement:

```text
This result supports only the claim named below.
```

Required content:

- exact claim;
- baseline;
- budget;
- seed policy;
- environment fixture;
- linearization/backend condition;
- uncertainty;
- known exclusions.

Forbidden:

- generalizing from one fixture to all environments;
- generalizing from tensor-disabled to tensor-enabled;
- claiming musical quality from reward tables alone.

## Field Translation Rules

Raw field names must be translated when exposed to human readers.

Use a glossary or inline labels for fields such as:

- `arm_id`;
- `mode_id`;
- `schema_id`;
- `schema_seed`;
- `seed_bundle_id`;
- `mean_return`;
- `delta_vs_direct_tabular_q`;
- `delta_vs_empty_tower`;
- `schema_seed_return_std`;
- `control_action`;
- `active_tier_before`;
- `active_tier_after`;
- `failure_reason`;
- `linearization_mode_id`.

Do not assume readers know whether a field is:

- identity metadata;
- budget metadata;
- statistical output;
- behavioral output;
- diagnostic output;
- claim-boundary metadata.

## Status Translation Rules

Never use a single status field as the whole result.

Every report must separate:

```text
artifact_status
behavior_status
claim_status
```

Suggested meanings:

```text
artifact_status:
  missing
  incomplete
  complete

behavior_status:
  not_run
  succeeded
  failed
  mixed
  diagnostic_only
  unresolved

claim_status:
  no_claim
  smoke_non_evidence
  calibration_only
  diagnostic_evidence
  supports_limited_claim
  blocks_claim
  unresolved
```

If the machine artifact has only `status=complete`, the readable document must
still infer and state whether behavior succeeded or failed.

## Evidence Discipline

Readable documents must include enough evidence for audit.

For every important interpretation, include:

- the source table or file;
- the relevant field names;
- the observed value or pattern;
- the conclusion drawn;
- the confidence or uncertainty.

Bad:

```text
The tower arms failed.
```

Better:

```text
The non-empty tower arms completed artifact runs but failed behaviorally:
their aggregate rows have mean_return 0.0, their episode rows have step_count 0
and success False, and their lift-fiber event rows repeatedly record
invalid_action_index.
```

## Claim Boundary Discipline

A readable document must say what it does not prove.

Common non-claims:

- not a tensor-enabled result;
- not a CUDA/GPU result;
- not a musical-quality result;
- not a general superiority result;
- not a production performance result;
- not a claim beyond the named fixture;
- not a claim beyond the named budget.

If a failure occurs, do not hide it behind the non-claim boundary. State both:

```text
This does not prove X.
It does show Y failed under this run condition.
```

## Required Output Files

For a serious evaluation, prefer this generated human-facing set:

```text
<repo-readout-surface>/
  readout_source.json
  README.md
  result_readout.md
  runbook.md
  artifact_index.md
  glossary.md
  results/
    summary.md
    human_summary.md
    arm_readout_table.md
    diagnostic_findings.md
    timing_readout.md
```

The exact repo folder may vary by evaluation, but the command target and output
home are the same repo-side readout surface. Raw artifact roots are evidence
sources, not output homes.

## Minimum Acceptable Human Report

If time is short, the minimum acceptable human-readable report is:

1. one-screen verdict;
2. arm legend;
3. reader-facing result table;
4. diagnostic warnings;
5. claim boundary;
6. evidence map.

Anything less is an artifact index, not a result report.

## Stop Conditions

Stop and ask the Project Owner before writing a claim if:

- a table says complete but behavior looks failed;
- a primary metric is zero and the reason is unclear;
- a baseline is missing;
- a run is partial;
- a field meaning is ambiguous;
- two artifacts disagree;
- the result would require a claim not approved in design docs;
- interpreting the result requires a domain judgment the Project Owner has not
  authorized.

## Operating Summary

When turning benchmark tables into readable docs:

```text
Do not merely list files.
Do not merely paste tables.
Do not let complete mean successful.
Do not let zero pass unexplained.
Do not hide diagnostics in appendices.
Do not make claims from artifacts alone.

Translate ids into names.
Translate statuses into artifact/behavior/claim state.
Translate metrics into meaning.
Translate anomalies into explicit warnings.
Translate every conclusion back to evidence.
```

The machine artifacts are the source of truth.

The human document is the source of understanding.
