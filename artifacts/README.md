# Benchmark Artifacts

This directory holds machine-readable benchmark evidence.

Every run must bind an explicit artifact root. Tools in this repository must
not infer artifact meaning from the current working directory.

Smoke artifacts are harness checks. They are not scientific benchmark claims.

Tracked here:

- artifact contract notes;
- schema markers;
- small curated summaries when intentionally added.

Normally untracked:

- large step-event tables;
- control-event tables;
- structural diagnostic dumps;
- model checkpoints;
- large arrays;
- temporary smoke outputs.

Large external artifacts should be referenced from explicit manifest files
rather than treated as terminal output or hidden local state.

Human-readable readouts are not normally stored here. They live in repo-side
evaluation surfaces under `docs/evaluations/` and point back to raw artifacts
through `readout_source.json`.
