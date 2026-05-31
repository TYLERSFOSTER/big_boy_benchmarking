# Counterpoint First Serious Learning V001 - Issue And Correction Notes

## Source

Primary generated readout:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/README.md
```

Preserved snapshot:

```text
docs/design/system_learning_from_evaluations/counterpoint_first_serious_learning_v001/01_readout_conversation_archive.md
```

## Short Result Classification

This evaluation is complete as a structural-limit diagnostic evaluation.

It shows basic system performance for:

- the BBB counterpoint fixture;
- direct masked-random and direct tabular-Q baselines;
- the empty tower shell;
- run/artifact writing;
- evaluation aggregation;
- human-readable readout generation.

It does not show much of the full tower-system capability, because the
non-empty tower conditions are dominated by full or near-full first-projection
collapse.

## Main Technical Finding

The active counterpoint fixture is:

```text
counterpoint_symbolic_n3_small_v001
```

The relevant structural facts are:

- `n = 3` voices;
- `108` reachable tier-0 state cells;
- `1140` legal graph edges;
- full tier-0 graph initialization before tower control;
- edge-generated contraction, where a contraction block merges source and
  target state cells along all edges in that block.

For structured-motion and bad/adversarial tower arms, the first contraction
block contains all `1140` edges. That means the first projection effectively
performs:

```text
H -> pi_0(H)
```

Since the reachable graph is connected, tier `1` becomes one state cell.

For random tower arms, the first block is not literally all of `H` in every
seed, but it can create a giant connected component immediately. Observed
largest tier-`1` fibers include `106/108`, `101/108`, `107/108`, and
`108/108` tier-`0` states.

## Correct Interpretation

The first generated interpretation used "mixed" too strongly as headline
language.

There is a narrow table fact that behavior is mixed across some random schema
seeds: some random schemas execute, and others fail with
`no_lift_candidate_from_current_state`.

The reader-facing classification should be stronger and more structural:

```text
Behavior: Structural Limit
Goals: Diagnostic
```

The result is not ordinary tower non-performance. It is diagnostic evidence
that broad/full-graph contraction schemas over this fixture can collapse the
first quotient projection so aggressively that ordinary learner-performance
language is blocked.

## Project Owner Correction

The Project Owner caught the key interpretive error:

- the runtime was valid for a first-pass environment/evaluation;
- the apparent weak/non-performance should not be summarized as generic
  `mixed` behavior;
- the environment/evaluation/readout stack had not recorded enough limit
  conclusions;
- the human-readable protocol did not force the right double checks before
  choosing headline language.

This correction changed the status of the result from a generic mixed
evaluation to a structural-limit diagnostic.

## Protocol Corrections Made

The correction was promoted into protocol documents so future readouts do not
depend on ad hoc carefulness.

Updated protocol obligations include:

- hidden-graph/tower environments must record known structural limit cases and
  non-claims before evaluation design;
- quotient/tower evaluations must declare structural limit checks;
- readouts must check for full or near-full first-projection collapse before
  using ordinary performance language;
- readouts must not stop at `Behavior: Mixed` when quotient collapse dominates
  interpretation;
- tower-control evaluations must promote tower shape, tier occupancy, and
  lift/action-realization summaries into evaluation-level tables when possible.

Relevant protocol files:

```text
docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/artifact_table_to_readable_document_protocol.md
docs/methods/artifact_contract.md
```

## Natural Confusion Points

This evaluation exposed several places where future users and engineers are
likely to get confused:

- `status=success` in a run index means artifact/run completion, not necessarily
  successful behavior.
- A tower-shape tuple such as `(108, 3, 1, 1, 1)` is a quotient shape, not an
  episode-by-episode time series.
- Tier `0` is the fine/base tier in this runtime convention.
- A tier existing does not mean the controller used it successfully for
  concrete action execution.
- `mixed` can be true as a table-level seed summary while still being the wrong
  headline interpretation.
- Full-graph initialization makes broad first contraction blocks much more
  powerful than an online/discovery setting would.
- Edge-generated contraction does not behave like clean per-voice coordinate
  projection.
- Structured labels such as "voice moves" or "medium span" can be dense enough
  to induce near-total connected-component collapse.

## System Correction Implications

Future counterpoint tower evaluations should separate these axes explicitly:

- full-graph/offline tower control versus incremental/discovery tower control;
- direct concrete execution versus quotient/tower execution;
- tower shape versus active-tier occupancy;
- lift/action-realization failure versus reward-learning failure;
- structural-limit diagnostic evidence versus performance evidence;
- reward/value aggregation effects versus action-realization effects.

The next serious evaluation should not treat this run as evidence against the
tower idea. It should treat this run as evidence that the next schemas and
diagnostics must control first-projection quotient collapse.

## Durable Design Lesson

Evaluation readouts are generated result surfaces. They should stay accurate,
but they should not be the only home for architectural learning.

When a readout conversation discovers a protocol error, runtime interpretation
issue, or likely user confusion, preserve that conversation in design docs and
distill the lesson into a durable note like this one.
