# Documentation Map

This repository keeps design history, method descriptions, runnable experiment
matrices, and result summaries separate on purpose.

Use the folders this way:

- `design/`: design discussions, blueprints, implementation gameplans, and
  implementation logs.
- `environments/`: human descriptions of environment families, fixtures, and
  smoke adapters.
- `methods/`: benchmark contracts, modes, metric channels, timing/readout
  rules, seed policy, and statistical method notes.
- `experiments/`: planned or runnable matrices that name environments, arms,
  budgets, seeds, and claim boundaries.
- `results/`: durable human summaries for artifact sets the repo intentionally
  records.
- `evaluations/`: checked-in guides for interpreting generated evaluation docs.
  Generated readouts should live under the artifact root unless deliberately
  promoted.
- `engineer_continuity/`: session reports, pause notes, and handoff records.
- `prime_directive/`: operating protocol directed to the embedded engineering
  consultant.

Machine-readable artifacts remain the execution source of truth. Docs may
summarize artifacts, but they must not invent status, performance claims, or
scientific conclusions without recorded artifacts.
