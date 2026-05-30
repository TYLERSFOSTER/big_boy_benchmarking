# Repository Operating Notes

## Current Status

This repository is active. It is no longer paused on the first serious
counterpoint evaluation.

As of 2026-05-30, the implemented repo state is:

- shared benchmark machinery exists;
- `state_collapser` is pinned through the `v0.7.0` tensorization integration;
- `counterpoint_symbolic_v001` has tiny and small fixtures;
- graph, schema, direct, tower-smoke, and serious-learning commands are
  runnable;
- first serious learning evaluation machinery exists for calibration,
  budget-locked execution, aggregation, and generated artifact-local docs.

The current serious-learning default linearization condition is:

```text
tensor_available_disabled
```

This records that the tensorization boundary is present while tensor execution
is disabled. It is not a tensor-enabled CPU, tensor-enabled CUDA, GPU, or
general performance claim.

## Root Contribution Rule

This file is a live repo orientation and contribution guard. It must not be
used as a one-off pause note again.

Historical pause notes belong in:

```text
docs/engineer_continuity/
docs/design/
```

If the project pauses again, record the pause in the relevant design or
continuity document and link it from here only if it remains the current repo
state.

## Prime Directive

Before executing an approved blueprint or implementation gameplan, reread:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/git_practices.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md
```

When a gameplan uses `Phase.Stage.Action`, execute those items as written.
Do not silently simplify, reorder, replace, or partially satisfy the approved
plan.

## Git Discipline

Use a task branch for approved implementation work, especially when the work is
attached to a blueprint and gameplan.

Default branch shape:

```text
codex/<task-name>
```

Do not rewrite or revert unrelated user changes.

## Documentation Map

Use the docs folders this way:

- `docs/design/`: design discussions, blueprints, implementation gameplans,
  and implementation logs.
- `docs/environments/`: human summaries of environment families and fixtures.
- `docs/methods/`: method, contract, mode, metric, timing, and statistics
  explanations.
- `docs/experiments/`: planned or runnable experiment matrices.
- `docs/results/`: durable human result summaries for artifact sets that the
  repo intentionally records.
- `docs/evaluations/`: checked-in guides for interpreting generated evaluation
  docs. Local generated readouts should live under the artifact root by default.
- `docs/engineer_continuity/`: continuity reports and historical handoff notes.
- `docs/prime_directive/`: operating protocol directed to the embedded
  engineering consultant.

Machine-readable artifacts are the source of truth for executed runs.
Human-facing docs must describe claim boundaries and must not invent a result
that is not backed by recorded artifacts.

## Generated Evaluation Docs

Evaluation summarization writes generated docs under the artifact root by
default:

```text
<artifact-root>/evaluations/<evaluation-id>/docs/
```

Do not commit generated docs that contain machine-local paths such as
`/private/tmp/...`.

Checked-in evaluation docs should use `<artifact-root>` placeholders unless a
durable, intentionally preserved artifact location is being recorded.

## Validation

Common checks:

```bash
uv run pytest
uv run ruff check .
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Counterpoint smoke commands:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint graph-diagnostics \
  --artifact-root <artifact-root> \
  --instance-id tiny

uv run python -m big_boy_benchmarking.cli counterpoint run-direct \
  --artifact-root <artifact-root> \
  --instance-id tiny \
  --policy masked-random \
  --seed 1 \
  --episodes 1

uv run python -m big_boy_benchmarking.cli counterpoint tower-smoke \
  --artifact-root <artifact-root> \
  --instance-id tiny \
  --schema-id counterpoint_motion_schema_v001 \
  --seed 2
```

Counterpoint serious-learning commands:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning calibrate \
  --artifact-root <artifact-root> \
  --instance-id tiny \
  --episodes 1 \
  --replicates 1 \
  --schema-seeds 1

uv run python -m big_boy_benchmarking.cli counterpoint serious-learning run \
  --artifact-root <artifact-root> \
  --episodes <episode-count> \
  --replicates <replicate-count> \
  --schema-seeds <schema-seed-count> \
  --locked-by <operator-or-run-id>

uv run python -m big_boy_benchmarking.cli counterpoint serious-learning summarize \
  --artifact-root <artifact-root>
```

The `tiny` serious-learning path is smoke/non-evidence. The `small` path is the
first serious fixture, subject to the budget and claim boundaries documented in
the evaluation method docs.
