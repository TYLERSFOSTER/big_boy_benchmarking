<p align="left">
  <picture>
    <source srcset="assets/images/BBB_dark.png" media="(prefers-color-scheme: dark)">
    <source srcset="assets/images/BBB_light.png" media="(prefers-color-scheme: light)">
    <img src="assets/images/BBB_light.png" alt="BBB" width="400">
  </picture>
</p>

# BIG BOY BENCHMARKING

Serious, post-smoke benchmarking for the `state_collapser` package.

This repository is a benchmarking workspace, not the core library. The core
runtime, quotient-tower construction, training surfaces, and environment
adapters live in [`state_collapser`](https://github.com/TYLERSFOSTER/state_collapser).

## Setup

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency management.
`state_collapser` is a first-class dependency, pinned to the public
`state_collapser` `v0.6.0` release tag:

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

The initial project skeleton verifies that `big_boy_benchmarking` can import the
specific `state_collapser` surfaces that benchmarking work will depend on:

- partition-tower runtime surfaces
- reward aggregation surfaces
- fiber-conditioned training input/decision surfaces

The next real work is to add benchmark families that measure scaling behavior
beyond `state_collapser`'s smoke-level in-repo benchmarks.
