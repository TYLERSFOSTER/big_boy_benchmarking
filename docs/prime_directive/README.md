# Prime Directive Protocol Map

This folder contains operating protocols directed to the Embedded Engineering
Consultant.

The benchmark workflow is:

```text
1. Construct an environment.
2. Construct evaluations for that environment.
3. Process run artifacts into repo-side human-readable readouts.
```

Use these protocol documents for that workflow:

- `environment_construction_for_benchmark_evaluations_protocol.md`
- `evaluation_construction_for_readable_artifacts_protocol.md`
- `artifact_table_to_readable_document_protocol.md`

The core collaboration and execution discipline lives in:

- `prime_directive.md`
- `git_practices.md`
- `common_failure_mode_001.md`
- `common_failure_mode_002_implementation_without_owner_approval.md`
- `common_failure_mode_003_gameplan_rewrite_during_implementation.md`

When the Project Owner asks for a human-readable run report, remind them of the
repo-side readout surface:

```text
execute artifact-table readout pointed at folder docs/evaluations/<environment>/<evaluation>/
```

The folder in that command is not the raw artifact root. It is the checked-in
evaluation readout surface that contains `readout_source.json`.
