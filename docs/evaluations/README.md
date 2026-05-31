# Evaluations

Checked-in files in this folder are repo-side evaluation readout surfaces. They
describe how to interpret evaluation artifacts and which claim boundaries
apply.

This folder is stage 2 and stage 3 of the benchmark workflow:

```text
2. Construct evaluations for environments.
3. Process raw run artifacts into repo-side human-readable readouts.
```

Each evaluation readout surface should contain a `readout_source.json` file.
That file binds the repo-side readout to the raw artifact root and source
evaluation root.

For durable serious evaluations, the raw artifact root also lives inside the
repo readout surface:

```text
docs/evaluations/<environment>/<evaluation>/artifacts/<run-label>/
```

Generated evaluation READMEs should start with local SVG status badges and a
compact `Status At A Glance` section. The badges are visual summaries only; they
must agree with the source binding, expected-file policy, goal criteria,
provenance status, and detailed verdict.

The command target for human-readable readout generation is the repo-side
evaluation folder, not the raw artifact root:

```text
execute artifact-table readout pointed at folder docs/evaluations/<environment>/<evaluation>/
```

Follow:

```text
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

Generated artifact-local docs may still exist for immediate inspection, but the
durable human interpretation surface lives here.

## Available Evaluation Readouts

| Evaluation | Status | Readout | Claim boundary |
| --- | --- | --- | --- |
| `counterpoint_first_serious_learning_v001` | Complete structural-limit diagnostic | [counterpoint first serious learning](counterpoint_symbolic_v001/first_serious_learning/README.md) | Fixture-only claims for `counterpoint_symbolic_n3_small_v001`, locked budget, and `tensor_available_disabled`; no general tower-performance claim. |
| `counterpoint_one_third_schema_tower_diagnostics_v001` | Complete structural-limit diagnostic | [counterpoint one-third schema tower diagnostics](counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/README.md) | Diagnostic claims for source-local one-third contraction on `small` and `medium`; no direct-vs-tower performance claim and no tensor-enabled claim. |
