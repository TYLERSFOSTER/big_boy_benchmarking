# Documentation Map

This repository keeps design history, method descriptions, environment docs,
evaluation readout surfaces, and result summaries separate on purpose.

The benchmark workflow is:

```text
1. Construct an environment.
2. Construct evaluations for that environment.
3. Process run artifacts into repo-side human-readable readouts.
```

The corresponding protocols are:

- `prime_directive/environment_construction_for_benchmark_evaluations_protocol.md`
- `prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `prime_directive/artifact_table_to_readable_document_protocol.md`

Use the folders this way:

- `design/`: design discussions, blueprints, implementation gameplans, and
  implementation logs.
- `environments/`: human descriptions of environment families, fixtures,
  contracts, diagnostics, and claim boundaries.
- `methods/`: benchmark contracts, modes, metric channels, timing/readout
  rules, seed policy, and statistical method notes.
- `experiments/`: planned or runnable matrices that name environments, arms,
  budgets, seeds, and claim boundaries.
- `evaluations/`: repo-side readout surfaces for evaluation families. These
  contain `readout_source.json`, status badges, goal/methodology summaries,
  artifact indexes, and generated human-readable readouts grounded in raw
  artifact tables.
- `results/`: promoted durable result summaries when the repo intentionally
  records a result beyond an evaluation-local readout.
- `engineer_continuity/`: session reports, pause notes, and handoff records.
- `prime_directive/`: operating protocol directed to the embedded engineering
  consultant.

Machine-readable artifacts remain the execution source of truth. Repo-side
readouts are the human interpretation layer. Docs may summarize artifacts, but
they must not invent status, performance claims, or scientific conclusions
without recorded artifacts.
