# Repository Operating Notes

## Current Status

This repository is active. It is no longer paused on the first serious
counterpoint evaluation.

As of 2026-06-01, the implemented repo state is:

- shared benchmark machinery exists;
- `state_collapser` is pinned through the `v0.7.1` active-tier integration;
- `counterpoint_symbolic_v001` has tiny, small, and medium fixtures;
- graph, schema, direct, tower-smoke, and serious-learning commands are
  runnable;
- first serious learning evaluation machinery exists for calibration,
  budget-locked execution, aggregation, source-bound repo readouts, and
  human-readable interpretation;
- one-third schema tower diagnostics machinery exists for small/medium
  diagnostic runs, aggregation, source-bound repo readouts, and
  human-readable interpretation;
- noisy-rate contraction diagnostics machinery exists for smoke-scale runs,
  aggregation, source-bound repo readouts, and human-readable interpretation;
- three repo-side counterpoint evaluation readouts exist:
  `first_serious_learning`, `one_third_schema_tower_diagnostics`, and
  `noisy_rate_contraction_diagnostics`.

The current serious-learning default linearization condition is:

```text
tensor_available_disabled
```

This records that the tensorization boundary is present while tensor execution
is disabled. It is not a tensor-enabled CPU, tensor-enabled CUDA, GPU, or
general performance claim.

## Current Next Work

The immediate next fork is a Project Owner decision, not automatic execution.

The newly implemented noisy-rate contraction diagnostic has a checked-in smoke
run:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/
```

The smoke result says the machinery works and, on the small smoke budget, the
requested rates `1/144`, `1/36`, and `1/18` do not fully collapse the first
projection. That is implementation and structural diagnostic evidence only.
Do not inflate it into a full small/medium conclusion.

The next decision is whether the Project Owner wants to authorize the full
small+medium noisy-rate validation budget from:

```text
docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/03_counterpoint_noisy_rate_contraction_diagnostics_implementation_gameplan.md
```

If full validation is authorized, run it through the same artifact/readout
discipline and then interpret the result before designing learning comparisons.

The previous one-third diagnostic remains a diagnosing issue, not a negative
learning result. Do not summarize it as "one-third failed" or "tower learning
failed." The recorded result is:

```text
source-local one-third contraction fully collapses the first projection on the
current small/medium fixtures, while base-tier concrete execution and lift
remain healthy.
```

After the noisy-rate diagnostic lesson is settled, the likely next major design
block is:

```text
counterpoint learning comparisons
```

That comparison should be designed only after the structural diagnostic path is
understood. It should compare learning behavior on counterpoint under explicit
baselines, schema choices, budgets, seeds, linearization condition, artifact
contracts, and human-readable readout requirements. Do not jump straight from
diagnostics into a learning-comparison implementation without a
blueprint/gameplan and explicit Project Owner approval.

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
- `docs/environments/`: human summaries of environment families, fixtures,
  contracts, diagnostics, and claim boundaries.
- `docs/methods/`: method, contract, mode, metric, timing, and statistics
  explanations.
- `docs/experiments/`: planned or runnable experiment matrices.
- `docs/evaluations/`: repo-side readout surfaces for evaluation families.
  These contain `readout_source.json`, status badges, goal/methodology
  summaries, artifact indexes, and generated human-readable readouts grounded
  in raw artifact tables.
- `docs/results/`: promoted durable result summaries when the repo
  intentionally records a result beyond an evaluation-local readout.
- `docs/engineer_continuity/`: continuity reports and historical handoff notes.
- `docs/prime_directive/`: operating protocol directed to the embedded
  engineering consultant.

Machine-readable artifacts are the source of truth for executed runs. For
serious evaluations that will receive a durable human-facing readout, write the
raw artifact root inside the repo-side evaluation surface under
`docs/evaluations/.../artifacts/`. Repo-side human-facing readouts must describe
claim boundaries and must not invent a result that is not backed by recorded
artifacts.

## Benchmark Workflow

The repo workflow is:

```text
1. Construct an environment.
2. Construct evaluations for that environment.
3. Process run artifacts into repo-side human-readable readouts.
```

Follow these protocols:

```text
docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

## Evaluation Readouts

Evaluation summarization writes aggregate tables under the explicit artifact
root and may write generated docs there for immediate inspection. For durable
serious evaluations, that artifact root belongs under the repo-side evaluation
surface:

```text
docs/evaluations/<environment>/<evaluation>/artifacts/<run-label>/evaluations/<evaluation-id>/docs/
```

The durable checked-in readout lives under `docs/evaluations/` and is generated
by pointing the artifact-table protocol at that readout surface's checked-in
source binding:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/<environment>/<evaluation>/readout_source.json
```

Each repo-side evaluation readout surface should include `readout_source.json`
so generated readouts can truthfully bind back to the machine-readable artifact
tables. Generated evaluation READMEs should start with local SVG badges and a
compact `Status At A Glance` section.

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
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/<run-label> \
  --instance-id tiny \
  --episodes 1 \
  --replicates 1 \
  --schema-seeds 1

uv run python -m big_boy_benchmarking.cli counterpoint serious-learning run \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/<run-label> \
  --instance-id small \
  --episodes <episode-count> \
  --replicates <replicate-count> \
  --schema-seeds <schema-seed-count> \
  --locked-by <operator-or-run-id> \
  --linearization-mode tensor_available_disabled

uv run python -m big_boy_benchmarking.cli counterpoint serious-learning summarize \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/<run-label>
```

The `tiny` serious-learning path is smoke/non-evidence. The `small` path is the
first serious fixture, subject to the budget and claim boundaries documented in
the evaluation method docs.

Counterpoint noisy-rate diagnostic smoke:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate run \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/artifacts/<run-label> \
  --instances small \
  --rates 1/144,1/36,1/18 \
  --schema-seeds 0,1,2 \
  --replicates 1 \
  --episodes 1 \
  --locked-by <operator-or-run-id>

uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate summarize \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/artifacts/<run-label>
```

Durable readout command:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json
```
