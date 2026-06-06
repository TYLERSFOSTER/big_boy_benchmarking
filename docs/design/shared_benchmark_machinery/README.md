# Shared Benchmark Machinery Design

## Status

Historical design workspace. The first shared benchmark machinery slice has
been implemented; this folder remains the design/history record for that work.

## Scope

This folder is for designing the shared benchmark machinery that counterpoint
and later environment families should build on:

- artifact writers;
- mode registry;
- seed bundles;
- metric and event rows;
- timing helpers;
- runner skeletons;
- upstream integration;
- CLI.

## Boundary

This folder is for design artifacts, implementation workplans, implementation
logs, and resume notes.

Current workflow-facing protocols live under:

```text
docs/prime_directive/
```

Use those protocols for new environment construction, evaluation construction,
and artifact-table readout generation. Do not treat old pause wording in this
folder as current repo state without checking the implementation logs and
current branch state.
