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
apply the readable-doc protocol to this evaluation folder: <folder>
make the human readout for artifacts in <folder>
```

When the Project Owner gives one of these commands, the consultant must treat it
as an instruction to:

1. read this protocol;
2. resolve the supplied folder to an artifact root or evaluation root;
3. inspect the machine-readable artifacts under that root;
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

Bad reminder:

```text
Here is a new multi-step workflow you should follow...
```

Do not repeatedly remind the Project Owner inside the same local conversation
unless the Project Owner appears to be searching for the command again.

### Folder Resolution

The invocation must include an explicit folder. Do not infer "last run" unless
the Project Owner explicitly adds a reliable path or marker.

Resolve the supplied folder as follows:

1. If the folder contains `evaluation_aggregate_table.csv`,
   `evaluation_aggregate_summary.json`, or `evaluation_run_index.csv`, treat it
   as an evaluation root.
2. If the folder contains `evaluations/`, treat it as an artifact root and look
   for evaluation roots beneath `evaluations/`.
3. If exactly one evaluation root is found, use it.
4. If multiple evaluation roots are found and the Project Owner did not name an
   evaluation id, stop and ask which evaluation to read.
5. If no evaluation root is found, apply Case 1: No Artifacts Found.

For this repository's first serious counterpoint evaluation, the normal
evaluation root is:

```text
<artifact-root>/evaluations/counterpoint_first_serious_learning_v001/
```

### Default Output Location

Unless the Project Owner points at a different output folder, write the readable
documents under:

```text
<evaluation-root>/docs/
```

This makes the readout artifact-local. Do not promote generated readouts into
repo `docs/results/` unless the Project Owner explicitly asks for a durable
checked-in result summary.

### Execution Contract

The consultant must inspect, when present:

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

### Output Contract

The default output set is:

```text
<evaluation-root>/docs/
  README.md
  result_readout.md
  runbook.md
  artifact_index.md
  glossary.md
  results/
    human_summary.md
    arm_readout_table.md
    diagnostic_findings.md
    timing_readout.md
```

If the existing artifact-local docs already contain some of these files, update
or replace them only as needed to satisfy this protocol. Preserve useful
existing runbook or artifact-index information.

### Completion Report

After executing this surface, report:

- the input folder;
- the resolved evaluation root;
- the files written;
- any missing artifacts;
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
- artifact root;
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

## All-Cases Protocol

Use this protocol whenever translating artifact tables to readable documents.

### Case 1: No Artifacts Found

Readable statement:

```text
No result exists at this artifact root.
```

Required content:

- artifact root checked;
- expected files;
- missing files;
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
- missing files;
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
docs/
  README.md
  result_readout.md
  runbook.md
  artifact_index.md
  glossary.md
  results/
    human_summary.md
    arm_readout_table.md
    diagnostic_findings.md
    timing_readout.md
```

The exact paths may vary by artifact root, but the conceptual files should
exist somewhere.

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
