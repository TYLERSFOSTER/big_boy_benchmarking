# Repository Operating Notes

## Current Status

This repository is active. It is no longer paused on the first serious
counterpoint evaluation.

As of 2026-06-07, the implemented repo state is:

- shared benchmark machinery exists;
- `state_collapser` is pinned through the `v0.7.2` pointwise-liftability
  integration;
- `counterpoint_symbolic_v001` has tiny, small, medium, and widened `span18`
  fixtures;
- graph, schema, direct, tower-smoke, and serious-learning commands are
  runnable;
- first serious learning evaluation machinery exists for calibration,
  budget-locked execution, aggregation, source-bound repo readouts, and
  human-readable interpretation;
- one-third schema tower diagnostics machinery exists for small/medium
  diagnostic runs, aggregation, source-bound repo readouts, and
  human-readable interpretation;
- noisy-rate contraction diagnostics machinery exists for custom structural
  diagnostic runs,
  aggregation, source-bound repo readouts, and human-readable interpretation;
- noisy-rate full-tower training-health diagnostic machinery exists for
  tower-only training-health runs, aggregation, source-bound repo
  readouts, and human-readable interpretation;
- second serious schema-comparison machinery exists for matched Schema 0
  versus Schema 1 first-sustained-hit bounded comparisons, aggregation,
  source-bound repo readouts, and human-readable interpretation;
- threshold-frontier probe machinery exists for reward-threshold sweeps over
  the corrected Schema 0 versus Schema 1 comparison surface, aggregation,
  source-bound repo readouts, and human-readable interpretation;
- small paired replicate probe machinery exists for seed-paired Schema 0
  versus Schema 1 next-measure comparisons, aggregation, source-bound
  repo readouts, and human-readable interpretation;
- eight repo-side counterpoint evaluation readouts exist:
  `first_serious_learning`, `one_third_schema_tower_diagnostics`,
  `noisy_rate_contraction_diagnostics`,
  `contraction_fraction_sweep_diagnostics`,
  `noisy_rate_full_tower_training_diagnostic`,
  `second_serious_schema_comparison`, `threshold_frontier_probe`, and
  `small_paired_replicate_probe`.
- `plate_support_5x5_default_v001` has a completed standard-gauntlet correction
  readout under
  `docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/`,
  covering structural diagnostics, iterated source-local-ratio schema sweep,
  candidate discovery, tower-training health, target calibration, paired
  comparison, and generated readout/system-learning synthesis. The current
  checked-in correction artifact root is `iterated_001`, and the Stage 6
  paired comparison records a bounded positive target-hit signal for the
  selected iterated tower candidate.

The current serious-learning default linearization condition is:

```text
tensor_available_disabled
```

This records that the tensorization boundary is present while tensor execution
is disabled. It is not a tensor-enabled CPU, tensor-enabled CUDA, GPU, or
general performance claim.

## Current Next Work

The immediate next fork is a Project Owner decision, not automatic execution.
Do not assume the next step from old counterpoint notes.

The main positive PlateSupport result remains the standard-gauntlet correction
run:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/iterated_001/
```

That run completed Stages 1-7 and produced:

```text
claim_status: paired_comparison_positive_signal
target hits: selected tower 25 / 128, direct baseline 15 / 128
mean target-hit-rate delta: +0.078125
mean total reward: selected tower -27.2109375, direct baseline -78.71875
invalid moves: selected tower 0, direct baseline 2142
```

Treat this as bounded smoke-scale positive evidence for a promising
PlateSupport tower-control mechanism. It is not a general PlateSupport tower
superiority claim.

After Abdul Malik raised the cul-de-sac / validity-filtering concern, the repo
added two follow-up diagnostic controls:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/
docs/evaluations/plate_support_5x5_default_v001/tower_star/
```

`direct_star_culdesac_control` tests whether one-step direct guards explain the
original tower signal. `tower_star` then applies analogous one-step filtering
inside tower lift-candidate pools before tower action-cell selection. The first
`tower_star_001` smoke run is inconclusive/tied on the primary target, so it
should be treated as a diagnostic control result, not a new positive tower
claim.

The next PlateSupport design block, if the Project Owner chooses it, should
start from those control diagnostics and decide whether to increase budgets,
adjust targets, test more candidates, or broaden PlateSupport instances. Do
not jump directly from the standard-gauntlet correction run to a general
success claim.

A separate counterpoint next-measure path has also progressed beyond the old
smoke-blocked state:

```text
threshold_frontier_probe episodes16_001 -> small_paired_replicate_probe episodes16_from_frontier_001 -> larger comparison design
```

The counterpoint threshold-frontier probe has been implemented and rerun with
enough episodes for the 4-of-5 persistence rule:

```text
docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/
docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts/episodes16_001/
```

The checked-in `episodes16_001` artifact tests thresholds `12.0` and `13.0`.
Both schemas pass both thresholds, and Schema 1 has the higher post-hit margin
at both thresholds. Treat this as a bounded next-measure margin signal, not as
broad schema dominance or statistical evidence.

The small paired replicate probe has also been rerun from the threshold-frontier
selected threshold:

```text
docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/
docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts/episodes16_from_frontier_001/
```

The checked-in `episodes16_from_frontier_001` artifact uses `R = 13.0`, has one
unblocked matched pair, both schemas sustain the target, and Schema 1 records
the higher post-hit reward margin. Treat this as a weak positive one-pair
pattern, not as a settled comparison.

The relevant design/workplan surfaces are:

```text
docs/design/first_counterpoint_environment/threshold_frontier_probe/
docs/design/first_counterpoint_environment/small_paired_replicate_probe/
```

The noisy-rate contraction and full-tower training-health diagnostics remain
supporting structural/training-health evidence:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/
```

Do not inflate those diagnostics into direct-vs-tower comparison claims or the
main serious comparison.

The previous one-third diagnostic remains a diagnosing issue, not a negative
learning result. Do not summarize it as "one-third failed" or "tower learning
failed." The recorded result is:

```text
source-local one-third contraction fully collapses the first projection on the
current small/medium fixtures, while base-tier concrete execution and lift
remain healthy.
```

Because the paired-replicate margin signal survived one threshold-frontier
selected pair, a likely future counterpoint design block is:

```text
counterpoint learning comparisons
```

That comparison should be designed only after the structural diagnostic path is
understood. It should compare learning behavior on counterpoint under explicit
baselines, schema choices, budgets, seeds, linearization condition, artifact
contracts, and human-readable readout requirements. Do not jump straight from
diagnostics into a learning-comparison implementation without a
blueprint/workplan and explicit Project Owner approval.

The current PlateSupport standard gauntlet is complete as a correction suite.
It supports a bounded statement only: the selected iterated tower candidate is
trainable, the suite can calibrate a binary-success target, and the Stage 6
paired comparison is positive on that target while also recording better tower
mean reward and zero invalid moves. The later direct-star and tower-star
controls are diagnostic follow-ups to that signal. Do not summarize any of
this as general PlateSupport tower success.

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

Before executing an approved blueprint or implementation workplan, reread:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/git_practices.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md
docs/prime_directive/common_failure_mode_005_umbrella_workplan_fragmentation.md
```

When a workplan uses `Phase.Stage.Action`, execute those items as written.
Do not silently simplify, reorder, replace, or partially satisfy the approved
plan.

## Git Discipline

Use a task branch for approved implementation work, especially when the work is
attached to a blueprint and workplan.

Default branch shape:

```text
codex/<task-name>
```

Do not rewrite or revert unrelated user changes.

## Documentation Map

Use the docs folders this way:

- `docs/design/`: design discussions, blueprints, implementation workplans,
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

PlateSupport environment-readiness command:

```bash
uv run python -m big_boy_benchmarking.cli plate-support readiness \
  --artifact-root docs/environments/plate_support_5x5_default_v001/readiness/dev_001
```

This command writes environment-readiness artifacts under `docs/environments/`,
not `docs/evaluations/`. It is an environment construction check, not a
learning evaluation.

PlateSupport standard-gauntlet correction commands:

```text
Use the full command sequence in README.md under "Run the PlateSupport standard
gauntlet correction path". The checked-in correction run is `iterated_001`.
For a new run, choose a fresh run label and keep the artifact root under:

docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/<run-label>
```

The schema-sweep stage must include:

```text
--include-iterated-source-local-ratio
```

The durable suite readout is rebuilt with:

```bash
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet readout build \
  --readout-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json \
  --create-system-learning-archive
```

PlateSupport direct-star and tower-star control readouts use explicit
repo-side source bindings:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/plate_support_5x5_default_v001/tower_star/readout_source.json
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

Counterpoint noisy-rate structural diagnostic:

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

Counterpoint noisy-rate full-tower training-health diagnostic:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate-full-train run \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts/<run-label> \
  --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json \
  --candidate-cap 2 \
  --training-replicates 1 \
  --episodes 4 \
  --locked-by <operator-or-run-id> \
  --linearization-mode tensor_available_disabled

uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate-full-train summarize \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts/<run-label>
```

Durable readout command:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
```
