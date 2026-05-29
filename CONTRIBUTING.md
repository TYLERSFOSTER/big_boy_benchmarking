# First Counterpoint Serious Evaluation Pause Note

## Status

Paused.

Do not create the serious-evaluation blueprint or implementation gameplan yet.

The Project Owner decided that tensorization in `state_collapser` is a blocker
for the first serious counterpoint evaluation.

This root `CONTRIBUTING.md` exists as the repo-level resume guard for this pause.

## Why This Is Paused

The counterpoint environment in `big_boy_benchmarking` is real enough for:

- smoke and integration checks;
- graph diagnostics;
- schema diagnostics;
- direct masked-random smoke;
- direct tabular-Q smoke;
- tower construction smoke;
- artifact-contract validation.

It is not yet the right basis for the first serious evaluation, because the
intended serious comparison needs `state_collapser` to have tensorization
present as an architectural option.

The important distinction is:

```text
pre-linearization/current-control-flow state_collapser
```

is not the same benchmark condition as:

```text
tensor-capable state_collapser with tensor path present but disabled
```

The second condition is the meaningful "tensor-off" ablation. The first
condition is only a pre-linearization baseline.

## Current State In This Repo

At the pause point:

- shared benchmark machinery exists;
- counterpoint environment family `counterpoint_symbolic_v001` exists;
- tiny and small fixtures exist;
- environment artifacts can be written;
- graph diagnostics can be written;
- schema diagnostics can be written;
- direct baseline smoke can run;
- tower smoke can build partition towers;
- current smoke should not be described as serious benchmark evidence.

Relevant local discussion file:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
```

## Required Upstream Alignment

An alignment note should exist in `/Users/foster/state_collapser` describing the
benchmark-driven tensorization needs. At the time this pause note was created,
the intended path was:

```text
/Users/foster/state_collapser/docs/design/model_train_surfaces/01_005_big_boy_benchmarking_tensorization_alignment_note.md
```

That note is meant to align upstream tensorization work with the benchmark needs
here.

## Resume Gate

Do not resume serious counterpoint evaluation design until `state_collapser` has
an answer to this question:

```text
Has state_collapser reached a tensor-capable architecture where tensor paths can
be explicitly disabled or enabled under documented benchmark modes?
```

When the answer is yes, resume by rereading:

```text
CONTRIBUTING.md
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
docs/design/first_counterpoint_environment/01_002_counterpoint_hidden_graph_and_contraction_schema_benchmark_blueprint.md
docs/design/first_counterpoint_environment/01_004_counterpoint_hidden_graph_and_contraction_schema_implementation_log.md
docs/engineer_continuity/2026/2026-05-28_big_boy_benchmarking_counterpoint_continuity.md
docs/engineer_continuity/2026/2026-05-29_counterpoint_serious_evaluation_pause_for_tensorization.md
```

Then decide whether the first serious evaluation should compare:

- tensor-capable disabled path versus tensor-enabled path;
- structural/schema diagnostics only;
- learning/control behavior;
- both structural and learning layers.

## Required Artifact Fields Later

The eventual benchmark artifacts should record the numeric/backend state so
future docs cannot blur categories.

Candidate field:

```text
numeric_backend:
  none_control_flow
  tensor_available_disabled
  tensor_enabled_cpu
  tensor_enabled_cuda
```

or:

```text
linearization_state:
  absent
  present_disabled
  present_enabled
```

## Non-Claims While Paused

Do not claim:

- serious counterpoint benchmark evidence;
- tensor-off versus tensor-on evidence;
- GPU or vectorized rollout performance;
- mature `state_collapser` evaluation.

Allowed claim:

```text
big_boy_benchmarking has a runnable counterpoint environment and smoke/
diagnostic harness, but the first serious evaluation is intentionally paused
until upstream tensorization is ready.
```

