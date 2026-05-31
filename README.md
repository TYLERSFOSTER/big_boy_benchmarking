<p align="left">
  <picture>
    <source srcset="assets/images/BBB_dark.png" media="(prefers-color-scheme: dark)">
    <source srcset="assets/images/BBB_light.png" media="(prefers-color-scheme: light)">
    <img src="assets/images/BBB_light.png" alt="BBB" width="395">
  </picture>
</p>

# BIG BOY BENCHMARKING

Serious, post-smoke benchmarking for the [`state_collapser`](https://github.com/TYLERSFOSTER/state_collapser) package.

This repository is a benchmarking workspace, not the core library. The core
runtime, quotient-tower construction, training surfaces, and environment
adapters live in [`state_collapser`](https://github.com/TYLERSFOSTER/state_collapser).

## Setup

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency management.
`state_collapser` is a first-class dependency, pinned to the public
`state_collapser` `v0.7.1` release tag:

```bash
uv sync --group dev
```

Run the test suite:

```bash
uv run pytest
```

Run lint checks:

```bash
uv run ruff check .
```

## Current Status

`big_boy_benchmarking` has two complete serious evaluation readouts and several
supporting smoke/diagnostic surfaces.

Implemented infrastructure:

- shared artifact, mode, seed, metric, timing, runner, upstream-smoke, and CLI
  machinery;
- `counterpoint_symbolic_v001`, a benchmark-owned symbolic hidden-graph
  environment family with `tiny` smoke, `small` serious, and `medium`
  diagnostic fixtures;
- graph, path-volume, schema, reward-fiber, lift-fiber, and tower diagnostics;
- direct masked-random and direct tabular-Q runners;
- tower smoke and serious-learning runners for contraction-schema arms;
- repo-side human-readable readout protocol and local status badges.

The serious-learning default linearization condition is
`tensor_available_disabled`: the tensorization boundary exists and is recorded,
but tensor execution is disabled. CPU/CUDA tensor-enabled modes remain reserved
until explicitly designed, implemented, and validated.

## Completed Evaluation Readouts

| Evaluation | Status | Human-readable report | What we can conclude |
| --- | --- | --- | --- |
| Counterpoint first serious learning v001, artifact run `pi0_h_evaluation_001` | Complete structural-limit diagnostic | [README](docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/README.md), [full readout](docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/result_readout.md), [diagnostics](docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/results/diagnostic_findings.md) | The harness, artifact pipeline, direct baselines, empty tower shell, and human readout path work on `counterpoint_symbolic_n3_small_v001`; non-empty tower arms are dominated by full or near-full first-projection collapse and lift/action-realization effects. |
| Counterpoint one-third schema tower diagnostics v001, artifact run `small_medium_validation_001` | Complete structural-limit diagnostic | [README](docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/README.md), [full readout](docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/result_readout.md), [summary](docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/results/summary.md) | The source-local one-third schema runs through upstream ABC control on `small` and `medium`; all 24 locked runs fully collapse at the first projection, but runtime execution itself does not stall: 3,840 concrete steps and 3,840 / 3,840 successful lift attempts. |

Supporting smoke/diagnostic result notes:

- [Counterpoint symbolic v001 first smoke](docs/results/counterpoint_symbolic_v001_first_smoke.md):
  historical smoke record and reproducible smoke commands, not serious
  performance evidence.
- [Upstream smoke readout discipline v001](docs/results/upstream_smoke_readout_discipline_v001.md):
  upstream integration/readout discipline evidence, not a benchmark result.

## Current Conclusions

The completed serious readouts support these claims:

- the counterpoint small fixture can be run through the shared BBB artifact and
  readout machinery;
- the counterpoint medium fixture is implemented and can run the one-third
  diagnostic budget;
- direct masked-random, direct tabular-Q, and empty-schema tower arms execute
  real 8-step episodes under the locked budget;
- the current non-empty tower schemas are a useful structural diagnostic, not a
  tower-performance comparison;
- broad/full-graph contraction schemas can collapse the first quotient
  projection so aggressively that ordinary learner-performance language is
  blocked;
- the source-local one-third contraction schema also fully collapses the first
  projection on the current `small` and `medium` fixtures, while preserving
  concrete execution and lift success in the recorded diagnostic budget;
- random tower schemas expose schema-seed-dependent
  `no_lift_candidate_from_current_state` lift/action-realization failures.

The current readouts do **not yet** support:

- general tower superiority or inferiority;
- tensor-enabled, CUDA, or GPU performance claims;
- musical-quality claims;
- production performance claims;
- claims beyond the recorded `small` and `medium` counterpoint budgets and the
  `tensor_available_disabled` condition.

Known documentation/artifact notes:

- the first serious learning readout predates promoted tower summary tables and
  reconstructs some facts from per-run artifacts;
- the one-third diagnostics readout includes promoted tower-shape, tier
  occupancy, lift, concrete-step, and ABC summary tables;
- design learning from these evaluations is preserved under
  [system learning from evaluations](docs/design/system_learning_from_evaluations/README.md).

## Benchmark Workflow

This repo now uses a three-stage benchmark workflow.

1. **Construct environments.**
   Build benchmark environment families and fixtures that have stable ids,
   legality/reward/action-mask contracts, diagnostics, artifact support, and
   human environment docs.
   Protocol:
   `docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md`

2. **Construct evaluations.**
   Construct evaluation definitions for those environments: arms, baselines,
   budgets, seeds, run modes, expected files, source bindings,
   goal/methodology sources, and claim boundaries.
   Protocol:
   `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`

3. **Process run artifacts into repo-side human-readable readouts.**
   Point Codex at the repo-side evaluation readout surface. The readout surface
   uses `readout_source.json` to find raw artifact tables and writes
   human-readable Markdown back into the repo, including local status badges
   and a compact `Status At A Glance` section.
   Protocol:
   `docs/prime_directive/artifact_table_to_readable_document_protocol.md`

Canonical readout invocation:

```text
execute artifact-table readout pointed at folder docs/evaluations/<environment>/<evaluation>/
```

Machine-readable artifacts remain the source of truth. For serious evaluations
that will receive a durable human readout, write the raw artifact root inside
the repo-side evaluation surface under `docs/evaluations/.../artifacts/`.
Repo-side readouts are the durable human interpretation layer.

## Shared Benchmark Machinery

The first benchmark infrastructure slice adds the measurement layer that future
environment families should use:

- artifact contracts and JSON/JSONL/CSV writers
- mode contracts and registry
- seed bundles
- event rows and timing helpers
- upstream smoke adapters
- runner skeletons
- a thin Python module CLI

Validate contracts with:

```bash
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Run a harness smoke into an explicit artifact root with:

```bash
uv run python -m big_boy_benchmarking.cli run-upstream-smoke \
  --smoke-id plate_support_env \
  --artifact-root <artifact-root>
```

The future installed command name `bbb` is reserved, but this slice exposes the
stable entry point through `python -m big_boy_benchmarking.cli`.

Human-facing docs live under:

- `docs/environments/`
- `docs/experiments/`
- `docs/evaluations/`
- `docs/results/`
- `docs/methods/`

Machine-readable artifacts remain the source of truth. Smoke artifacts do not
constitute serious benchmark results.

## Counterpoint Commands

Basic diagnostics and smoke:

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

First serious-learning surface:

For durable serious-learning runs, use a repo-resident artifact root:

```bash
export BBB_COUNTERPOINT_EVAL_ROOT="$PWD/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/<run-label>"
```

```bash
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning calibrate \
  --artifact-root "$BBB_COUNTERPOINT_EVAL_ROOT" \
  --instance-id tiny \
  --episodes 1 \
  --replicates 1 \
  --schema-seeds 1

uv run python -m big_boy_benchmarking.cli counterpoint serious-learning run \
  --artifact-root "$BBB_COUNTERPOINT_EVAL_ROOT" \
  --instance-id small \
  --episodes <episode-count> \
  --replicates <replicate-count> \
  --schema-seeds <schema-seed-count> \
  --locked-by <operator-or-run-id> \
  --linearization-mode tensor_available_disabled

uv run python -m big_boy_benchmarking.cli counterpoint serious-learning summarize \
  --artifact-root "$BBB_COUNTERPOINT_EVAL_ROOT"
```

`summarize` writes aggregate tables under the repo-resident artifact root and
may write generated docs there for immediate inspection:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/<run-label>/evaluations/counterpoint_first_serious_learning_v001/docs/
```

Durable repo-side readouts are generated by pointing the artifact-table readout
protocol at the checked-in evaluation surface:

```text
execute artifact-table readout pointed at folder docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/
```

One-third schema tower diagnostics:

```bash
export BBB_ONE_THIRD_ROOT="$PWD/docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/<run-label>"

uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics run \
  --artifact-root "$BBB_ONE_THIRD_ROOT" \
  --instance-ids small,medium

uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics summarize \
  --artifact-root "$BBB_ONE_THIRD_ROOT"
```

Durable repo-side readout target:

```text
execute artifact-table readout pointed at folder docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/
```
