# Counterpoint Serious Evaluation Pause For Tensorization

Date: 2026-05-29

Repo: `<repo-root>`

Primary design folder:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/
```

Related upstream note:

```text
<state-collapser-repo>/docs/design/model_train_surfaces/01_005_big_boy_benchmarking_tensorization_alignment_note.md
```

## Executive Summary

The first serious counterpoint evaluation design block is intentionally paused.

This pause was a Project Owner decision.

The Project Owner caught the key methodological issue:

```text
Benchmarking state_collapser before tensorization exists is not the same as
benchmarking a tensor-capable state_collapser with tensorization present but
disabled.
```

That distinction makes tensorization a blocker for the intended serious
counterpoint evaluation.

The current counterpoint environment and smoke/diagnostic harness remain useful.
They are not being discarded. But they should not be promoted into the first
serious evaluation until `state_collapser` has tensorization present as an
explicit architectural option, with disabled/enabled modes that can be recorded
in benchmark artifacts.

## PO Attribution

This point must be attributed to the Project Owner.

The Project Owner caught the issue after Codex initially framed tensorization as
not blocking the first serious counterpoint benchmark, provided the benchmark
was scoped to structural/schema diagnostics and modest CPU tabular/control-flow
evaluation.

The Project Owner corrected that framing:

```text
"benchmarking state_collapser but not using the tensor stuff" is different than
"benchmarking state_collapser without any tensor stuff in the first place."
```

The Project Owner further emphasized that tensorization being present can affect
behavior even when it is not turned on.

This is the methodological reason for the pause.

Do not rewrite this later as "Codex discovered tensorization was a blocker."
Codex investigated and agreed after the PO correction. The decisive catch came
from the PO.

## What Changed

Before the PO correction, the working design path was:

```text
Proceed with a first serious counterpoint evaluation as a current-control-flow,
pre-linearization benchmark, while naming tensorization as a future axis.
```

After the PO correction, the design path is:

```text
Pause the first serious counterpoint evaluation until state_collapser has a
tensor-capable architecture where tensorized paths can be explicitly disabled or
enabled as benchmark modes.
```

The current work can still be described as:

```text
smoke/integration and pre-linearization reconnaissance
```

It should not be described as:

```text
the no-tensor arm of a tensorized benchmark
```

## Three Benchmark Categories

The discussion settled three distinct categories:

```text
1. pre-linearization / current control-flow state_collapser
2. tensor-capable state_collapser with tensor path present but disabled
3. tensor-capable state_collapser with tensor path enabled
```

The current `state_collapser` package is category 1.

The intended clean benchmark ablation is category 2 versus category 3.

This distinction matters because adding tensorization can change architecture
even when the tensor path is disabled:

- canonical numeric encodings may become required;
- shape, dtype, and device contracts may be introduced;
- action masks may receive a new representation;
- batching boundaries may reshape runtime APIs;
- validation and error behavior may change;
- state/action identity normalization may change;
- dependency and import surfaces may change;
- memory layout assumptions may change;
- conversion boundaries may add timing overhead;
- runner APIs and artifact metadata may change.

Therefore, category 1 is not an acceptable substitute for category 2.

## Current State Of Big Boy Benchmarking

At the time of this pause, `big_boy_benchmarking` has:

- shared benchmark machinery;
- artifact writers;
- mode registry;
- seed bundles;
- metric/event rows;
- timing helpers;
- runner skeletons;
- upstream smoke integration;
- CLI surfaces;
- benchmark-owned counterpoint environment family `counterpoint_symbolic_v001`;
- tiny and small fixtures;
- graph diagnostics;
- schema diagnostics;
- reward-fiber diagnostics;
- lift-fiber diagnostics;
- direct masked-random smoke;
- direct tabular-Q smoke;
- tower construction smoke.

These pieces are real and useful.

They support claims like:

```text
The counterpoint environment and smoke/diagnostic harness are runnable.
```

They do not support claims like:

```text
state_collapser has serious counterpoint benchmark evidence.
state_collapser has tensor-off versus tensor-on evidence.
state_collapser has GPU/vectorized rollout performance evidence.
```

## Files Added Or Updated In Big Boy Benchmarking

Discussion document:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
```

This records:

- the current smoke/non-smoke boundary;
- the initial Codex investigation of `state_collapser`;
- the PO correction about pre-tensor versus tensor-capable-disabled conditions;
- the final PO decision that tensorization is a blocker;
- the pause and resume gate.

Pause note:

```text
CONTRIBUTING.md
```

This records:

- the paused status;
- the reason for the pause;
- current repo state;
- required upstream alignment;
- resume gate;
- artifact fields needed later;
- non-claims while paused.

Placement correction:

```text
CONTRIBUTING.md
```

Codex initially misread the PO correction about root placement and incorrectly
treated the root-level `CONTRIBUTING.md` as something to undo. That was wrong.
The PO had moved the note to root and expected that placement to be respected.

The corrected placement is:

```text
CONTRIBUTING.md
```

Do not move this pause note back into the nested design folder unless the PO
explicitly requests it.

## File Added In State Collapser

Upstream alignment note:

```text
<state-collapser-repo>/docs/design/model_train_surfaces/01_005_big_boy_benchmarking_tensorization_alignment_note.md
```

This note was created because the PO requested that the conclusions from this
benchmarking discussion be visible in `state_collapser`, where tensorization
work will happen.

The note explains:

- why `big_boy_benchmarking` is paused;
- why category 1, category 2, and category 3 above must not be blurred;
- what minimum tensorization alignment would let the benchmark resume;
- what claims should be avoided until tensorization exists;
- what resume signal `big_boy_benchmarking` needs from `state_collapser`.

Important upstream status note:

`<state-collapser-repo>` already had unrelated dirty files when this note
was created. Those unrelated files were not modified for this work.

## Resume Gate

Do not resume serious counterpoint evaluation design until this question has a
clear yes answer:

```text
Has state_collapser reached a tensor-capable architecture where tensor paths can
be explicitly disabled or enabled under documented benchmark modes?
```

When that is true, resume by reading:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
CONTRIBUTING.md
docs/design/first_counterpoint_environment/01_002_counterpoint_hidden_graph_and_contraction_schema_benchmark_blueprint.md
docs/design/first_counterpoint_environment/01_004_counterpoint_hidden_graph_and_contraction_schema_implementation_log.md
docs/engineer_continuity/2026/2026-05-28_big_boy_benchmarking_counterpoint_continuity.md
<state-collapser-repo>/docs/design/model_train_surfaces/01_005_big_boy_benchmarking_tensorization_alignment_note.md
```

Then decide:

- whether the first serious evaluation compares tensor-disabled versus
  tensor-enabled modes directly;
- whether structural/schema diagnostics come first;
- whether learning/control behavior is included immediately;
- which fixture is in scope;
- which schemas and baselines are required;
- how artifact manifests record numeric backend state.

## Future Artifact Requirement

Future benchmark artifacts should explicitly record the numeric/backend state.

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

The exact names can change. The distinction must not disappear.

## Non-Claims Until Resume

While this design block is paused, do not claim:

- serious counterpoint benchmark evidence;
- tensor-off versus tensor-on evidence;
- mature `state_collapser` throughput evidence;
- GPU/CUDA/vectorized rollout evidence;
- final benchmark readiness.

Allowed claim:

```text
big_boy_benchmarking has a runnable counterpoint environment and smoke/
diagnostic harness, but the first serious counterpoint evaluation is paused
because the PO identified tensorization as a blocker for the intended benchmark
comparison.
```

## Current Git State Notes

At the time this report was created:

`big_boy_benchmarking` had the serious-evaluation design folder untracked:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/
```

`state_collapser` had pre-existing unrelated dirty files plus the new alignment
note:

```text
docs/design/model_train_surfaces/01_005_big_boy_benchmarking_tensorization_alignment_note.md
```

No code or tests were run for this pause report. This was docs-only continuity
work.
