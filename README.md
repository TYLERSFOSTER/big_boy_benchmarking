<p align="left">
  <picture>
    <source srcset="assets/images/BBB_dark.png" media="(prefers-color-scheme: dark)">
    <source srcset="assets/images/BBB_light.png" media="(prefers-color-scheme: light)">
    <img src="assets/images/BBB_light.png" alt="BBB" width="375">
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
`state_collapser` `v0.7.0` release tag:

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

## Current Scope

`big_boy_benchmarking` now has the first complete benchmarking slice:

- shared artifact, mode, seed, metric, timing, runner, upstream-smoke, and CLI
  machinery;
- a real `counterpoint_symbolic_v001` environment family with tiny and small
  fixtures;
- graph, path-volume, schema, reward-fiber, lift-fiber, and tower diagnostics;
- direct masked-random and direct tabular-Q runners;
- tower smoke runners for contraction schemas;
- first serious counterpoint learning evaluation machinery for calibration,
  budget-locked runs, aggregation, and artifact-local docs.

The serious-learning default linearization condition is
`tensor_available_disabled`: the tensorization boundary exists and is recorded,
but tensor execution is disabled. CPU/CUDA tensor-enabled modes remain reserved
until explicitly designed, implemented, and validated.

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

Human-facing summaries live under:

- `docs/environments/`
- `docs/experiments/`
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

`summarize` writes generated human-facing docs into the artifact root by
default:

```text
<artifact-root>/evaluations/counterpoint_first_serious_learning_v001/docs/
```

Pass `--docs-root` only when intentionally writing those generated docs
somewhere else.
