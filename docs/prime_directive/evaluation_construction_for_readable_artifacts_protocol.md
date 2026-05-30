# Evaluation Construction For Readable Artifacts Protocol

## Status

Proposed prime-directive adjunct.

This document is directed to future Embedded Engineering Consultants working in
this repository.

Its purpose is to define what every new benchmark evaluation must produce so
that `docs/prime_directive/artifact_table_to_readable_document_protocol.md` can
generate truthful, complete, human-readable readouts without reverse-engineering
the evaluation after the fact.

## Core Rule

> An evaluation is not construction-complete until it provides the machine
> evidence, source binding, goal context, methodology context, expected-file
> policy, and claim boundary needed by the human-readable readout protocol.

Do not treat human-readable docs as an afterthought.

Do not rely on a future consultant to infer evaluation intent from code alone.

Do not build an evaluation that can run but cannot explain what it was trying
to test, how it was tested, which files were expected, and which claims are
allowed.

## Relationship To The Other Protocols

This is the second protocol in the benchmark workflow.

The environment construction protocol is:

```text
docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md
```

The downstream readout protocol is:

```text
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

The three stages are:

```text
1. Construct an environment that can support evaluations.
2. Construct evaluations for that environment.
3. Process run artifacts into repo-side human-readable readouts.
```

The construction protocol answers:

```text
What must an evaluation write or declare before a readout exists?
```

The readout protocol answers:

```text
How does Codex turn those artifacts and declarations into readable docs?
```

If a new evaluation does not satisfy this construction protocol, the readout
protocol will either produce weak prose, ask avoidable clarifying questions, or
misclassify absent files.

## Required Construction Outputs

Every evaluation must define these outputs before implementation is considered
complete.

### Repo Readout Surface

Define the repository folder where human-readable readouts live.

Example:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/
```

This folder is the command target for:

```text
execute artifact-table readout pointed at folder <repo-readout-surface>
```

It is not the raw artifact root.

### Source Artifact Shape

Define the raw artifact root and source evaluation root shape.

At minimum, specify:

- artifact root argument or convention;
- evaluation id;
- source evaluation root path under the artifact root;
- run-family paths;
- result-table paths;
- per-run event paths.

### Source Binding

Every evaluation readout surface must include or be able to generate:

```text
readout_source.json
```

The source binding must include:

```json
{
  "repo_readout_surface": "<absolute repo path>",
  "source_artifact_root": "<raw artifact root>",
  "source_evaluation_root": "<raw evaluation root>",
  "evaluation_id": "<evaluation id>",
  "environment_instance_id": "<environment instance id>",
  "artifact_run_label": "<human run label>",
  "artifact_schema_version": "<artifact schema version>",
  "run_mode": "<run mode>",
  "source_files": {
    "aggregate_table": "<path to aggregate table>",
    "run_index": "<path to run index>"
  },
  "expected_files": {
    "required": ["<required source file>"],
    "expected_absent_is_gap": [],
    "conditional": {},
    "not_applicable": [],
    "expectation_sources": ["<path documenting expectation policy>"]
  },
  "goal_summary_sources": ["<path documenting evaluation goals>"],
  "methodology_summary_sources": ["<path documenting evaluation methodology>"],
  "claim_boundary": ["<allowed or excluded claim>"]
}
```

Do not omit `run_mode`. It is needed to distinguish calibration, smoke,
manually locked serious runs, calibration-derived serious runs, diagnostic
runs, and final result runs.

## Expected-File Policy

Every evaluation must declare expected files by expectation class.

Use this shape:

```json
{
  "expected_files": {
    "required": [],
    "expected_absent_is_gap": [],
    "conditional": {},
    "not_applicable": [],
    "expectation_sources": []
  }
}
```

Meanings:

| Field | Meaning |
| --- | --- |
| `required` | Must exist for this source artifact set to be interpretable. |
| `expected_absent_is_gap` | Expected by the evaluation contract; absence is a provenance or artifact gap. |
| `conditional` | Expected only for named run modes or conditions. |
| `not_applicable` | Explicitly not applicable for this run mode or claim boundary. |
| `expectation_sources` | Docs or source files that justify this policy. |

Do not let the readout protocol guess whether absent files are missing,
conditional, or not applicable.

## Goal Summary Material

Every evaluation must provide enough material for the README section:

```markdown
## Summary of Goals Behind this Evaluation
```

The construction artifacts must answer:

- what question the evaluation exists to answer;
- why this environment or fixture was chosen;
- what arms, baselines, controls, and comparison groups matter;
- what success or failure would mean;
- what non-goals and claim exclusions apply.

Record the source material in:

```json
{
  "goal_summary_sources": [
    "docs/design/<evaluation-blueprint>.md",
    "docs/evaluations/<evaluation>/method.md",
    "readout_source.json"
  ]
}
```

## Methodology Summary Material

Every evaluation must provide enough material for the README section:

```markdown
## Summary of Methodology Behind this Evaluation
```

The construction artifacts must answer:

- evaluation method class and comparison design;
- environment fixture and why that fixture is the serious or smoke target;
- arms, baselines, controls, and what each arm tests;
- budget, seeds, schema seeds, episode horizon, and replicates;
- calibration, run, summarize, and readout path distinction;
- artifact contract and expected-file policy;
- aggregation/statistics method;
- timing categories and what timing cannot claim;
- linearization/backend condition;
- claim boundary and non-goals.

Record the source material in:

```json
{
  "methodology_summary_sources": [
    "docs/design/<evaluation-blueprint>.md",
    "docs/evaluations/<evaluation>/method.md",
    "docs/evaluations/<evaluation>/runbook.md",
    "readout_source.json"
  ]
}
```

If methodology differs by run mode, the source binding must say so. For
example, calibration methodology and locked serious-run methodology are not the
same thing.

## Evaluation Manifests

Every serious evaluation should write evaluation-level manifests unless the
Project Owner explicitly approves a narrower run mode.

At minimum:

```text
evaluation_manifest.json
evaluation_arm_manifest.json
evaluation_run_index.csv
evaluation_budget_lock.json
evaluation_aggregate_summary.json
evaluation_aggregate_table.csv
```

Calibration paths should additionally write:

```text
calibration_summary.json
calibration_run_index.csv
calibration_recommendation.md
```

If a run mode does not write a file from the broader contract, record that in
`expected_files` as `conditional` or `not_applicable`, not as an implicit
absence left for the readout to guess.

## Human Docs Seeds

Every evaluation should have checked-in human-doc seed files under its repo
readout surface:

```text
README.md
method.md
runbook.md
artifact_index.md
results/summary.md
```

These files do not replace machine-readable artifacts. They provide stable
context for goal and methodology summaries and make readouts auditable by a
human.

## Required Tests

An evaluation implementation should include tests that fail if:

- `readout_source.json` cannot be generated or parsed;
- required source files are not listed;
- expected-file policy is absent;
- `goal_summary_sources` is empty;
- `methodology_summary_sources` is empty;
- the repo readout surface is confused with the raw artifact root;
- README generation would leave `[...]`, `TODO`, or `TBD`;
- calibration-only files are treated as required for every run mode;
- serious evaluation manifests are omitted without explicit policy.

## Stop Conditions

Stop and ask the Project Owner before implementing or declaring an evaluation
complete if:

- the evaluation goal is not clear enough to populate the README goal summary;
- the methodology is not clear enough to populate the README methodology
  summary;
- expected files cannot be classified;
- run modes are not distinguished;
- source paths are ambiguous;
- claim boundaries are not known;
- a generated readout would need to infer intent from code only.

## Operating Summary

When building evaluations:

```text
Do not only make the run executable.
Do not only make tables.
Do not leave readout intent implicit.
Do not make future readouts guess expected files.
Do not leave goal or methodology summaries as placeholders.

Build the evidence.
Bind the evidence to a repo readout surface.
Declare file expectations.
Declare goal sources.
Declare methodology sources.
Declare claim boundaries.
Then the readout protocol can translate rather than reconstruct.
```
