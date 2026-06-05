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
`state_collapser` `v0.7.2` release tag:

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

`big_boy_benchmarking` has eight repo-side counterpoint evaluation readouts and
several supporting smoke/diagnostic surfaces.

Implemented infrastructure:

- shared artifact, mode, seed, metric, timing, runner, upstream-smoke, and CLI
  machinery;
- `counterpoint_symbolic_v001`, a benchmark-owned symbolic hidden-graph
  environment family with `tiny` smoke, `small` serious, and `medium`
  diagnostic fixtures;
- graph, path-volume, schema, reward-fiber, lift-fiber, and tower diagnostics;
- direct masked-random and direct tabular-Q runners;
- tower smoke and serious-learning runners for contraction-schema arms;
- one-third, fraction-sweep, noisy-rate contraction diagnostics, and
  noisy-rate full-tower training-health diagnostics;
- second serious schema-comparison machinery for matched Schema 0 versus
  Schema 1 first-sustained-hit evaluation;
- threshold-frontier probe machinery for sweeping reward thresholds over the
  corrected Schema 0 versus Schema 1 comparison surface;
- small paired replicate probe machinery for seed-paired Schema 0 versus
  Schema 1 next-measure evaluation;
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
| Counterpoint noisy-rate contraction diagnostics v001, artifact run `smoke_001` | Complete smoke diagnostic; full validation pending | [README](docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/README.md), [summary](docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/results/summary.md), [source coverage](docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/results/source_coverage.md) | The new edge-global noisy-rate selector, metadata/runtime selected-edge consistency checks, source-coverage tables, threshold summaries, badges, and readout path work on the `small` smoke budget. In the smoke run, `1/144`, `1/36`, and `1/18` do not fully collapse the first projection; this is implementation and diagnostic evidence, not full small+medium validation. |
| Counterpoint contraction fraction sweep diagnostics v001, artifact run `smoke_001` | Complete smoke diagnostic | [README](docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/README.md), [summary](docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/results/summary.md), [sweep verdict](docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/results/sweep_verdict.md) | The n-over-18 source-local fraction sweep completed and showed immediate first-projection collapse at `1/18` on the checked-in small smoke budget; `6/18` matches the legacy one-third endpoint. This is structural diagnostic evidence, not learning-performance evidence. |
| Counterpoint noisy-rate full-tower training diagnostic v001, artifact run `smoke_001` | Complete smoke training-health diagnostic; main full budget pending | [README](docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/README.md), [full readout](docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/result_readout.md), [findings](docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/results/diagnostic_findings.md) | The repo can select non-collapsed noisy-rate candidates from the parent readout, rebuild their full available towers, preserve learner state across episodes, and emit tower-only training-health evidence. The checked-in smoke run selected two `1/144` candidates, emitted 64 concrete steps and 80 successful learner updates, and classified both as `trainable_clean`; this is not a direct-vs-tower comparison and not the main full diagnostic budget. |
| Counterpoint second serious schema comparison v001, artifact run `smoke_001` | Complete implementation smoke; calibration and serious medium run pending | [README](docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/README.md), [full readout](docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/result_readout.md), [paired comparison](docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/results/paired_comparison_readout.md) | The repo can run the matched active-tier comparison harness for Schema 0 no-contraction versus a selected Schema 1 one-drop noisy-rate candidate, emit explicit threshold/persistence windows, and produce paired schema-comparison tables. The checked-in run uses a smoke threshold and one small candidate only; it is not a calibrated or serious medium result. |
| Counterpoint threshold frontier probe v001, artifact run `smoke_001` | Complete implementation smoke; meaningful frontier run pending | [README](docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/README.md), [full readout](docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/result_readout.md), [frontier readout](docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/results/frontier_readout.md) | The repo can sweep reward thresholds over the corrected Schema 0 versus Schema 1 comparison surface and promote per-threshold arm, pair, tower, lift, timing, and frontier tables. The checked-in smoke used thresholds `12.0,13.0` and four episodes, so sustained-hit is impossible under the 4-of-5 rule; it validates machinery but is behaviorally claim-blocked. |
| Counterpoint small paired replicate probe v001, artifact run `smoke_001` | Complete implementation smoke; meaningful threshold-frontier-selected run pending | [README](docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/README.md), [full readout](docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/result_readout.md), [paired replicate readout](docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/results/paired_replicate_readout.md) | The repo can run the new seed-paired replicate probe surface for one corrected wide candidate, preserve shared seed-bundle identity, and emit pair-distribution, margin, hit-rate, lift, tower, timing, and readout tables. The checked-in smoke used `R=13.0`, one pair, and four episodes per arm; both arms were transient only, so the behavioral claim is blocked while the machinery is verified. |

Supporting smoke/diagnostic result notes:

- [Counterpoint symbolic v001 first smoke](docs/results/counterpoint_symbolic_v001_first_smoke.md):
  historical smoke record and reproducible smoke commands, not serious
  performance evidence.
- [Upstream smoke readout discipline v001](docs/results/upstream_smoke_readout_discipline_v001.md):
  upstream integration/readout discipline evidence, not a benchmark result.

## Current Conclusions

The completed counterpoint readouts support these claims:

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
- the edge-global noisy-rate diagnostic can select small edge shares without a
  source-local minimum-one floor, can report zero-selected-source counts, and
  can verify that metadata-selected and runtime-contracted edges match;
- the current noisy-rate smoke run on `small` does not show full first-projection
  collapse for `1/144`, `1/36`, or `1/18`, but full small+medium validation has
  not yet been authorized or run;
- the contraction-fraction sweep smoke shows that the current source-local
  `n/18` rule can collapse immediately at `1/18`, so it is a diagnostic lesson
  about local quota semantics rather than a negative learning result;
- selected non-collapsed noisy-rate towers from the checked-in smoke parent
  readout can be run through a tower-only training-health smoke budget with
  persistent learner state, concrete steps, lift evidence, tier/controller
  traces, and learner-update rows;
- the second serious schema-comparison harness can pair Schema 0 no-contraction
  against a selected Schema 1 noisy-rate one-drop candidate under the same
  active-tier tower-control runtime, seed bundle, threshold policy, and
  artifact/readout workflow;
- the threshold-frontier probe can rerun that matched comparison over a
  threshold grid, preserve per-threshold subrun artifacts, and promote
  frontier-level arm, pair, margin, first-failure, lift, tower, timing, and
  recommendation tables; the checked-in two-threshold smoke validates the
  machinery but is behaviorally claim-blocked because four episodes cannot
  satisfy a 4-of-5 sustained-hit rule;
- the small paired replicate probe can repeat that matched comparison surface
  across seed bundles and write pair-level margin, hit-rate, lift, tower, and
  timing tables; the checked-in smoke verifies the machinery but is
  behaviorally claim-blocked because both arms were transient only under the
  four-episode smoke budget;
- random tower schemas expose schema-seed-dependent
  `no_lift_candidate_from_current_state` lift/action-realization failures.

The current readouts do **not yet** support:

- general tower superiority or inferiority;
- tensor-enabled, CUDA, or GPU performance claims;
- musical-quality claims;
- production performance claims;
- claims beyond the recorded `small` and `medium` counterpoint budgets and the
  `tensor_available_disabled` condition;
- noisy-rate conclusions beyond the checked-in `smoke_001` run until a full
  validation budget is explicitly run and read out;
- direct-vs-tower learning comparison claims from the noisy-rate full-tower
  training diagnostic; that readout is tower-only training health.
- calibrated second-serious schema comparison claims; the checked-in second
  serious comparison artifact is implementation smoke only and uses a smoke
  threshold.
- meaningful threshold-frontier claims; the checked-in threshold-frontier
  artifact is implementation smoke only, and the intended meaningful run is the
  six-threshold, eight-episode `v072_pointwise_frontier_001` budget.
- meaningful small paired replicate claims; the checked-in paired-replicate
  artifact is implementation smoke only, and the intended meaningful run should
  use a threshold selected by a meaningful threshold-frontier run or explicit
  Project Owner override.

Known documentation/artifact notes:

- the first serious learning readout predates promoted tower summary tables and
  reconstructs some facts from per-run artifacts;
- the one-third diagnostics readout includes promoted tower-shape, tier
  occupancy, lift, concrete-step, and ABC summary tables;
- the noisy-rate diagnostics readout includes promoted selection, source
  coverage, metadata/runtime consistency, monotonicity, threshold, tower-shape,
  endpoint-coalescence, tier occupancy, lift, concrete-step, and ABC summary
  tables;
- the contraction-fraction sweep readout includes promoted schema-fraction,
  tower-shape, endpoint-coalescence, collapse-threshold, legacy-equivalence,
  tier, lift, concrete-step, controller, and ABC summary tables;
- the noisy-rate full-tower training readout includes selected-candidate,
  tower-shape, training-episode, training-curve, tier-occupancy,
  executability, lift, concrete-step, controller-action, ABC, learner-update,
  and training-health summary tables;
- the second serious schema-comparison readout includes candidate, schema-arm,
  threshold-window, first-sustained-hit, paired-comparison, claim-summary,
  tower-shape, tier, lift, concrete-step, controller, ABC, learner-update, and
  timing tables;
- the threshold-frontier probe readout includes threshold-arm,
  threshold-pair, post-hit-margin, first-failure-frontier, frontier-summary,
  tower-shape, lift, timing, badge, and artifact provenance tables;
- the small paired replicate probe readout includes pair-distribution,
  pair-level margin, schema-arm distribution, sustained-hit-rate, seed-bundle,
  lift, tower-shape, timing, and artifact provenance tables;
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
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/<environment>/<evaluation>/readout_source.json
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
protocol at the checked-in source binding:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/readout_source.json
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
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/readout_source.json
```

Noisy-rate contraction diagnostics:

```bash
export BBB_NOISY_RATE_ROOT="$PWD/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/artifacts/<run-label>"

uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate run \
  --artifact-root "$BBB_NOISY_RATE_ROOT" \
  --instances small \
  --rates 1/144,1/36,1/18 \
  --schema-seeds 0,1,2 \
  --replicates 1 \
  --episodes 1 \
  --locked-by <operator-or-run-id>

uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate summarize \
  --artifact-root "$BBB_NOISY_RATE_ROOT"
```

Durable repo-side readout target:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json
```

The checked-in `smoke_001` noisy-rate run is implementation/diagnostic
evidence. Full validation remains a separate Project Owner decision.

Noisy-rate full-tower training-health diagnostic:

```bash
export BBB_NOISY_RATE_FULL_TRAIN_ROOT="$PWD/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts/<run-label>"

uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate-full-train run \
  --artifact-root "$BBB_NOISY_RATE_FULL_TRAIN_ROOT" \
  --candidate-readout-source "$PWD/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json" \
  --candidate-cap 2 \
  --training-replicates 1 \
  --episodes 4 \
  --locked-by <operator-or-run-id> \
  --linearization-mode tensor_available_disabled

uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate-full-train summarize \
  --artifact-root "$BBB_NOISY_RATE_FULL_TRAIN_ROOT"
```

Durable repo-side readout target:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
```

The checked-in `smoke_001` full-tower training run is training-health smoke
evidence. The main full diagnostic budget remains a separate Project Owner
decision.

Second serious schema-comparison evaluation:

```bash
export BBB_SECOND_SERIOUS_ROOT="$PWD/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/<run-label>"

uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison run \
  --artifact-root "$BBB_SECOND_SERIOUS_ROOT" \
  --candidate-readout-source "$PWD/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json" \
  --candidate-cap 1 \
  --instance-id small \
  --episodes 8 \
  --replicates 1 \
  --threshold-policy-id counterpoint_total_space_sustained_reward_smoke_v001 \
  --threshold-value <locked-smoke-threshold> \
  --window-length 5 \
  --required-count 4 \
  --locked-by <operator-or-run-id> \
  --linearization-mode tensor_available_disabled

uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison summarize \
  --artifact-root "$BBB_SECOND_SERIOUS_ROOT"
```

Durable repo-side readout target:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/readout_source.json
```

The checked-in `smoke_001` second-serious run proves the matched comparison
machinery and readout path. Calibration must run before choosing the serious
threshold, and the serious `medium` run remains decision-locked until four
eligible medium Schema 1 candidates are available and explicitly authorized.

Small paired replicate probe:

```bash
export BBB_PAIRED_REPLICATE_ROOT="$PWD/docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts/<run-label>"

uv run python -m big_boy_benchmarking.cli counterpoint paired-replicate-probe run \
  --artifact-root "$BBB_PAIRED_REPLICATE_ROOT" \
  --candidate-readout-source "$PWD/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json" \
  --threshold-value <locked-smoke-threshold-or-po-override> \
  --candidate-cap 1 \
  --episodes <episode-count> \
  --replicates <matched-pair-count> \
  --locked-by <operator-or-run-id> \
  --linearization-mode tensor_available_disabled

uv run python -m big_boy_benchmarking.cli counterpoint paired-replicate-probe summarize \
  --artifact-root "$BBB_PAIRED_REPLICATE_ROOT"
```

Durable repo-side readout target:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/readout_source.json
```

The checked-in `smoke_001` paired-replicate run verifies the seed-paired
machinery and readout path. The intended meaningful run should use a threshold
selected by the threshold-frontier probe, or an explicit Project Owner
threshold override, before scaling to the agreed `8` matched pairs and `16`
episodes per arm.
