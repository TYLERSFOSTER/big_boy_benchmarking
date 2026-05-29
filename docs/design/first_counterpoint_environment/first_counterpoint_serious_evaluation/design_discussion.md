# Counterpoint Serious Evaluation Design Discussion

## Status

Initial discussion document for the first non-smoke evaluation block for
`counterpoint_symbolic_v001`.

This document is not an implementation blueprint.

This document is not an implementation gameplan.

This document is not approval to edit benchmark code.

Its job is to collect the opening alignment for the next design block:

```text
What counts as the first serious benchmark evaluation for the counterpoint
environment we just built?
```

## Immediate Context

The repo is currently past the first major construction threshold:

- shared benchmark machinery exists;
- artifact writers exist;
- mode registry exists;
- seed bundles exist;
- metric/event rows exist;
- timing helpers exist;
- runner skeletons exist;
- upstream smoke integration exists;
- CLI surfaces exist;
- the benchmark-owned counterpoint environment exists;
- tiny and small counterpoint fixtures exist;
- graph diagnostics run;
- schema diagnostics run;
- direct masked-random smoke runs;
- direct tabular-Q smoke runs;
- tower smoke builds partition towers and writes structural artifacts.

That is good and necessary. It is also not yet the same thing as serious
benchmark evidence.

The current counterpoint commands prove that the environment is coherent enough
to run, emit artifacts, and build towers. They do not yet prove that any
abstraction, schema, tower controller, or learner improves performance.

## Opening Answer To The Resume Question

The Project Owner asked whether `big_boy_benchmarking` already has more serious
evaluations set up that can simply be pointed at the new counterpoint
environment.

Current answer:

```text
Partially, but not in the serious benchmark-matrix sense.
```

What exists now:

- graph/environment diagnostics;
- schema diagnostics;
- reward fiber diagnostics;
- lift fiber diagnostics;
- balanced addressability diagnostics;
- path-volume diagnostics;
- direct masked-random runner;
- direct tabular-Q runner;
- tower construction smoke runner;
- artifact and summary writing for those surfaces.

What does not yet exist:

- a serious multi-seed counterpoint evaluation matrix runner;
- a counterpoint result aggregator;
- a first-class comparison protocol;
- a committed non-smoke result summary;
- an online tower learner/controller evaluation;
- a clear definition of what tower-vs-direct performance comparison means for
  this environment.

The repo therefore appears ready to design the serious evaluation layer, not to
run it immediately as if it already existed.

## Current Claim Boundary

Existing docs intentionally label the current counterpoint matrix as smoke:

```text
implementation and artifact-contract smoke matrix
```

That should stay true until this design block defines and the implementation
block builds a real evaluation protocol.

Current smoke can support statements like:

- the finite graph can be enumerated;
- the legal mask works;
- the reward contract emits rows;
- schema diagnostics can be written;
- direct tabular-Q can execute episodes;
- a partition tower can be built from the graph;
- artifacts are produced under the shared benchmark contract.

Current smoke should not support statements like:

- the tower method beats direct learning;
- the structured schema beats random schemas;
- the counterpoint abstraction is useful for online control;
- `state_collapser` has demonstrated serious benchmark improvement here.

## The Main Design Block

This design block should settle:

```text
What is the first non-smoke evaluation for counterpoint_symbolic_v001?
```

The likely location is this folder:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/
```

This discussion should eventually produce a blueprint and then a
Phase.Stage.Action implementation gameplan.

## Key Distinction: Two Evaluation Layers

The important split is:

```text
A. serious structural/schema evaluation
B. serious policy/learning evaluation
```

These are related but not identical.

### A. Structural/schema evaluation

This asks whether a schema produces useful abstract structure over the exact
counterpoint hidden graph.

Possible evidence:

- quotient tier sizes;
- edge/cell compression;
- reward fiber variance;
- lift fiber ambiguity;
- balanced addressability;
- path-volume reduction;
- projection audit results;
- structured-vs-random-vs-bad schema comparisons;
- timing for graph/tower construction and diagnostics.

This layer may be the first serious evaluation because it is already close to
the machinery we built.

### B. Policy/learning evaluation

This asks whether a learner/controller using tower structure actually improves
control, sample efficiency, return, completion, or wall-clock behavior.

Possible evidence:

- return curves;
- completion rates;
- legal episode success;
- sample efficiency by episode budget;
- direct tabular-Q versus tower tabular-Q;
- structured schema versus random schema under the same learner;
- bad schema as a pathology check;
- timing separated into online algorithm cost and benchmark bookkeeping.

This layer is probably the eventual target, but it needs clearer tower
semantics than we currently have.

## The Largest Ambiguity

The largest ambiguity is:

```text
What does "tower evaluation" mean in the first serious counterpoint benchmark?
```

Current implementation has `tower-smoke`, which builds a tower and writes
diagnostic artifacts. It is not yet an online tower learner/controller.

Possible interpretations:

1. Tower evaluation means structural/schema quality only for this first serious
   block.
2. Tower evaluation means an online tower tabular-Q learner.
3. Tower evaluation means a controller that chooses among tower tiers or
   contracted actions.
4. Tower evaluation means a two-stage design: first structural evidence, then
   learning evidence in a follow-up block.

This document should not silently pick one. This is a real PO decision point.

## Candidate First Serious Evaluation Shape

This is a Codex opening proposal, not a decision.

The first serious evaluation could use:

```text
fixture: counterpoint_symbolic_n3_small_v001
tiny: CI/smoke only
```

Candidate arms:

- direct masked-random;
- direct tabular-Q;
- empty schema diagnostics;
- random balanced schema diagnostics;
- random unbalanced schema diagnostics;
- structured motion schema diagnostics;
- bad/adversarial schema diagnostics;
- projection audit as diagnostic-only, not online default.

Possible first serious claim type:

```text
On the small finite counterpoint graph, structured motion schemas preserve more
reward/lift/control-relevant information than random or bad schemas under the
same artifact and diagnostic protocol.
```

Possible later claim type:

```text
On the small finite counterpoint graph, a tower-aware learner/controller using
structured schema information improves learning or control metrics relative to
direct tabular-Q and random-schema tower controls.
```

The first claim is closer to existing machinery. The second claim requires more
runner design.

## Candidate Metrics

Possible structural metrics:

- state count;
- edge count;
- branch factor;
- legal mask density;
- exact path volume;
- quotient tier count;
- state cell count by tier;
- edge cell count by tier, if available;
- reward fiber mean/variance/min/max;
- reward term variance;
- lift candidate count;
- lift entropy;
- valid lift count;
- failed lift count;
- addressability balance.

Possible learning/control metrics:

- per-episode return;
- mean return;
- return confidence intervals over seeds;
- completion rate;
- truncation rate;
- legal action failure rate, if applicable;
- episode length;
- sample efficiency to threshold;
- online timing per segment;
- artifact logging time kept separate from online timing.

Possible artifact completeness checks:

- every run has manifest files;
- every run has seed bundle;
- every run has mode manifest;
- every run has timing summary;
- every run has episode rows, where applicable;
- every schema diagnostic has quotient/reward/lift/addressability artifacts.

## PO Initial Discussion Topic

#### PO Turn

We have a TODO in `state_collapser` that I would call $\mathbb{R}$-*linearization*, but that you formulate in terms of tensors/GPU/CUDA I think. My understanding was that our `state_collapser` package is architected around control flow at present, without a lot of the GPU-based speed-up devices. ...So my questions are: 1. Do I understand this correctly? 2. Please do a thorough investigation of `state_collapser` to give me conclusion. 3. How ciritical is getting that complete to this present benchmarking?

#### Codex Turn

Yes: I think you understand the current architecture correctly.

I would phrase the TODO this way:

```text
state_collapser currently has a graph/tower/control-flow architecture, with future work needed to linearize/tensorize the relevant objects into stable numeric forms for batched rollout, neural learners, and GPU-backed execution.
```

Your phrase `$\mathbb{R}$-*linearization*` is actually a good mathematical name
for part of the missing layer. The package currently knows about states,
primitive actions, edges, quotient cells, action cells, schemas, fibers,
runtime snapshots, and learner-facing inputs as structured Python objects. What
is not yet built is a canonical system that turns those structured objects into
fixed-shape arrays/tensors with declared dtype/device/shape contracts.

The more engineering-ish formulation I have been using is:

```text
tensor/device/batch/sequence/vectorized-rollout infrastructure
```

but I think these are two views of the same gap. Your formulation names the
mathematical operation; mine names the implementation substrate.

### Investigation Summary

I inspected `/Users/foster/state_collapser` read-only for the relevant TODOs,
docs, and implementation surfaces.

The docs explicitly confirm the gap:

- `CONTRIBUTING.md` lists deep tensor-backend hardening, large-scale training
  framework maturity, full vectorized rollout semantics, tensor/device,
  batch/sequence, and checkpoint integration as critical TODOs.
- `docs/usage/01_001_what_state_collapser_is.md` says the package is not trying
  to be a general RL training framework and does not currently own neural model
  families, distributed rollout, replay buffers, checkpoints, or experiment
  manifests.
- `docs/usage/01_005_using_your_own_training_loop.md` says future
  tensor/device utilities should convert observations, tower-position keys,
  masks, stage context, and diagnostics into model inputs, and states directly
  that this tensor stack is not implemented yet.
- `docs/code_review/02_001_synthetic_blow_full_repo_review.md` records the
  current representative path as CPU-only with no tensor/device surface
  implemented yet.
- `docs/design/RL_framework_maturity/01_001_rl_framework_maturity_and_tower_training_spine_discussion.md`
  repeats the current missing pieces: no PyTorch model family, no tensor/device
  abstraction, no vectorized rollout system, no serious replay buffer, no
  checkpoint/resume surface, and no experiment manifest/artifact contract.
- `pyproject.toml` declares `torch` only in the optional `ml` extra. That is a
  posture toward future ML backends, not an implemented Torch training stack.

The code confirms the same thing:

- `State` and `PrimitiveAction` are immutable wrappers around `Hashable`
  payloads/identities, not tensor-backed records.
- `ActionSelectionInput` carries `observation: object`, runtime snapshot,
  tower-position tuple, action mask, and diagnostics as Python objects.
- `TabularQLearner` is dictionary/list based: Q rows are Python dicts, replay is
  a list of transitions, and the update path operates on one latest transition.
- `PartitionTower` builds and updates state/action partition layers with Python
  registries, schema assignment stores, merge records, and object ids.
- `ContractionSchema` is a Python protocol assigning edge ids to schema blocks;
  the built-in schemas use labels, deterministic random assignment, or discovery
  order, not tensor kernels.
- `TowerRuntime.step(...)` is explicit runtime control flow: apply primitive
  action, update explored graph/vista graph, update partition tower, compute
  reward, return a live runtime view.
- The existing `state_collapser.benchmarks.tower_runtime_bench` is a lightweight
  CPU runtime benchmark over steps/ops/sec/readout flags, not a tensor or GPU
  benchmark.

So the short conclusion is:

```text
state_collapser is currently a sparse graph/tower/control-flow package with
research-grade tabular/training surfaces. It is not yet an R-linearized,
tensorized, vectorized, GPU-backed RL framework.
```

### Criticality For This Present Benchmarking

For the immediate `big_boy_benchmarking` counterpoint work, I do **not** think
the tensor/GPU/R-linearization TODO is a blocker.

It is not critical for the first serious counterpoint evaluation if that first
evaluation is one of:

- structural/schema evaluation;
- small finite-graph diagnostics;
- quotient/tower construction diagnostics;
- reward-fiber variance;
- lift-fiber ambiguity;
- path-volume reduction;
- direct tabular-Q versus simple baselines on `small`;
- smoke or modest CPU timing under the current architecture.

In fact, benchmarking before that layer exists is useful. It gives us a clean
measurement of the current architecture: where Python object/control-flow cost
shows up, where tower updates dominate, where diagnostics are expensive, and
how far the sparse graph approach gets before tensorization becomes obviously
necessary.

It becomes critical later if the benchmark claim changes to any of these:

- large-scale throughput;
- vectorized multi-env rollout;
- neural policy/value learners;
- replay-buffer-heavy off-policy training;
- GPU utilization;
- CUDA-vs-CPU wall-clock claims;
- large fixture tiers where Python object loops dominate;
- comparison against mature RL libraries on their own performance terms.

So I would not pause the present benchmark design to finish this TODO in
`state_collapser`. I would instead make the boundary explicit:

```text
First serious counterpoint evaluation measures the current sparse
graph/tower/control-flow architecture. It does not claim tensorized or
GPU-backed performance.
```

Then we should design the benchmark artifacts so they can expose the future need
for R-linearization:

- include timing segments for graph enumeration, tower construction, schema
  diagnostics, learner action, learner update, environment step, and artifact
  writing;
- keep online timing separate from posthoc diagnostics;
- record that tensor/device/vectorized rollout is not implemented in the
  dependency state;
- avoid GPU claims;
- avoid benchmarking against GPU-based RL frameworks as if the substrate were
  equivalent;
- leave room for a later `state_collapser` tensorized-backend benchmark family.

My recommendation:

```text
Do not make R-linearization a prerequisite for the first serious counterpoint
benchmark. Make it a named future axis. The first serious benchmark should
measure structural/schema quality and modest CPU learning/control behavior under
the package architecture that actually exists today.
```

#### PO Turn
Ok I want to be really careful here though. I absolutely agree that the ``no tensors yet'' benchmarking you describe is useful. But really only if the tensorization is there, but not turned on. Like benchmarking "`state_collapser` but not using the tensor stuff" is different than benchmarking "`state_collapser` wihtout any tensor stuff in the first place." Right? Because the tensor stuff ebing present actually effects behavior, even if it isn't used.

#### Codex Turn

Yes. This is a real distinction, and I was too loose in the previous reply.

There are at least three different things:

```text
1. pre-linearization / current control-flow state_collapser
2. tensor-capable state_collapser with tensor path present but disabled
3. tensor-capable state_collapser with tensor path enabled
```

The current repo state is category 1.

What you are describing as the clean ablation is category 2 versus category 3.
That is different. It is more scientifically controlled because the tensor
system has already forced whatever architectural changes it forces:

- canonical numeric encodings;
- shape/dtype/device contracts;
- mask representation;
- batch boundaries;
- deterministic conversion rules;
- validation/error behavior;
- possible state/action identity normalization;
- dependency and import surface;
- memory layout assumptions;
- timing overhead from conversion boundaries;
- likely changes in runner APIs and artifact metadata.

Even if the tensor path is "off," the package may behave differently simply
because the architecture has been rebuilt to make the tensor path possible. So
benchmarking:

```text
state_collapser after tensorization, tensor path disabled
```

is not the same evidence as benchmarking:

```text
state_collapser before tensorization exists
```

I agree with that.

### Corrected Claim Boundary

The current counterpoint evaluation can still be useful, but it must be named
honestly:

```text
current sparse control-flow baseline
```

or:

```text
pre-R-linearization baseline
```

It should not be called:

```text
no-tensor ablation
```

unless a tensorization layer exists in the package and is deliberately disabled
under a documented mode/config.

That changes the earlier recommendation from:

```text
benchmark now and treat tensorization as future axis
```

to the sharper version:

```text
benchmark now only as a pre-linearization/current-architecture baseline, and
reserve any "tensor off vs tensor on" conclusion until the tensor-capable
architecture exists.
```

### How Critical Is Tensorization, With This Correction?

It depends on the claim we want this design block to support.

If the first serious counterpoint evaluation is allowed to claim:

```text
The current sparse graph/tower/control-flow architecture can produce useful
structural diagnostics and modest CPU tabular baselines on the counterpoint
environment.
```

then tensorization is not a blocker.

If the first serious counterpoint evaluation is meant to claim:

```text
The mature architecture of state_collapser, with tensorization available but
disabled, behaves like this; and with tensorization enabled, behaves like that.
```

then tensorization is absolutely a blocker.

If the first serious counterpoint evaluation is meant to claim:

```text
state_collapser is competitive as a high-throughput RL execution substrate.
```

then tensorization/vectorized rollout is also a blocker.

### Design Consequence

We should probably split the serious evaluation roadmap into named layers:

```text
Layer 0: smoke/integration, already done
Layer 1: pre-linearization structural/control-flow baseline
Layer 2: tensor-capable disabled-path baseline
Layer 3: tensor-enabled/vectorized benchmark
```

Layer 1 is still worth doing because:

- it validates the environment and artifact contract on the real current
  package;
- it gives us a regression baseline before architecture changes;
- it tells us which costs are due to graph/tower/control logic rather than
  tensor kernels;
- it gives tensorization work a concrete before/after target.

But Layer 1 should not be sold as the final no-tensor ablation. It is a
precondition baseline.

### Practical Artifact Requirement

The benchmark artifact contract should record a dependency/backend state field
along these lines:

```text
linearization_state:
  absent
  present_disabled
  present_enabled
```

or, more concretely:

```text
numeric_backend:
  none_control_flow
  tensor_available_disabled
  tensor_enabled_cpu
  tensor_enabled_cuda
```

That way future result docs cannot blur the categories.

### Revised Recommendation

My revised recommendation is:

```text
Proceed with the first serious counterpoint design only if we explicitly call it
a pre-R-linearization/current-control-flow baseline. Do not use it as the
no-tensor arm of a tensorized benchmark. Create a future blocked milestone for
the tensor-capable disabled/enabled comparison.
```

That keeps the current work valuable without overstating what kind of evidence
it gives us.

#### PO Turn
Tensorization is a blocker. I'm goign to pause this work and move to tensorization. We'll come back to this shortly. Please create a `CONTRIBUTING.md` document to note this pause, where we're currently at, etc., so that when we come back we understand wehre to pick up. Please also put an `md` note somewhere in the `state_collapser` repo that summarizes all the conclusions we came to here, so that work in `state_collapser` is perfectly aligned with needs here.

#### Codex Turn

Agreed. I will treat tensorization as a blocker for this serious evaluation
block.

That means this design block should pause here. We should not continue into a
blueprint or Phase.Stage.Action implementation gameplan for the first serious
counterpoint evaluation until `state_collapser` has a tensor-capable
architecture available as part of the package surface.

The important corrected state is:

```text
Current counterpoint benchmark work is real and useful, but it is only ready for
smoke/integration and pre-linearization reconnaissance. It is not yet ready for
the first serious benchmark evaluation, because the intended serious comparison
depends on tensorization being present as an architectural option.
```

The pause reason is not that the counterpoint environment is bad or incomplete.
It is that the serious evaluation target has changed from:

```text
Can we evaluate the current control-flow package?
```

to:

```text
Can we evaluate state_collapser in the architecture that includes tensorization,
with tensorized paths disabled/enabled as explicit benchmark modes?
```

That requires work in `state_collapser` first.

Acting accordingly:

- this discussion file should record the pause;
- the repo root should get a `CONTRIBUTING.md` continuity note;
- `state_collapser` should get a separate markdown alignment note describing
  what the tensorization work must preserve/expose for this benchmark;
- no serious counterpoint evaluation blueprint should be created from this
  block until the tensorization alignment note has been acted on upstream.

When we return, the first question should not be "what matrix do we run?" It
should be:

```text
Has state_collapser reached the tensor-capable architecture state needed to make
the tensor-off versus tensor-on distinction meaningful?
```

Only after that answer is yes should we reopen:

- first serious fixture scope;
- structural/schema versus learning/control layer;
- tower evaluation semantics;
- direct/tower/random/bad baselines;
- artifact fields for numeric backend state;
- result-claim boundary.

## Candidate Design Questions

These questions are for discussion. They are not decisions.

### Question 1: First serious layer

Should the first non-smoke evaluation be:

- structural/schema evaluation only;
- learning-performance evaluation only;
- both in one matrix;
- structural first, learning next?

#### PO Turn

```text

```

#### Codex Reply

```text

```

### Question 2: Fixture scope

Should the first serious fixture be `small`, with `tiny` kept only for smoke and
tests?

#### PO Turn

```text

```

#### Codex Reply

```text

```

### Question 3: Tower semantics

For this block, what should count as a tower evaluation?

#### PO Turn

```text

```

#### Codex Reply

```text

```

### Question 4: Baselines

Which baselines are required before we allow the result to count as serious?

Potential candidates:

- masked-random;
- direct tabular-Q;
- empty schema;
- random balanced schema;
- random unbalanced schema;
- structured motion schema;
- bad/adversarial schema.

#### PO Turn

```text

```

#### Codex Reply

```text

```

### Question 5: Result claim

What is the first claim this evaluation is allowed to support?

#### PO Turn

```text

```

#### Codex Reply

```text

```

### Question 6: Budget

What is the acceptable first serious budget?

Potential axes:

- number of seeds;
- number of episodes;
- number of schemas;
- tiny/small only versus larger fixtures;
- runtime tolerance;
- whether temp artifact roots are acceptable or result artifacts should be
  preserved elsewhere.

#### PO Turn

```text

```

#### Codex Reply

```text

```

### Question 7: Artifact and docs output

What human-readable result docs should be produced by the first serious run?

Potential outputs:

- experiment plan under `docs/experiments/`;
- method notes under `docs/methods/`, if new metrics are introduced;
- result summary under `docs/results/`;
- artifact root recorded with exact commands;
- comparison tables;
- explicit non-claim boundaries.

#### PO Turn

```text

```

#### Codex Reply

```text

```

## Turn Log

### Turn 001 - Codex Opening

Codex seeded this document with the resumed discussion state:

- current repo has smoke and diagnostics, not a serious evaluation matrix;
- the next design block should define the first non-smoke counterpoint
  evaluation;
- structural/schema evaluation and policy/learning evaluation should be
  separated;
- tower semantics are the main ambiguity;
- `small` is the likely first serious fixture, with `tiny` remaining smoke;
- no serious benchmark claim should be made from current smoke artifacts.

### Turn 002 - PO Response

```text
We have a TODO in `state_collapser` that I would call
R-linearization, but that you formulate in terms of tensors/GPU/CUDA I think.
My understanding was that our `state_collapser` package is architected around
control flow at present, without a lot of the GPU-based speed-up devices. The
questions were whether this is correct, what investigation of `state_collapser`
concludes, and how critical completing that TODO is to this present benchmarking.
```

### Turn 003 - Codex Reply

```text
Codex replied in the "PO Initial Discussion Topic" section: the understanding is
correct; `state_collapser` is currently sparse graph/tower/control-flow oriented,
with tensor/device/batch/vectorized rollout work explicitly listed as future
maturity work; that future R-linearization/tensorization layer is not a blocker
for the first serious counterpoint benchmark, provided the benchmark is scoped
to structural/schema diagnostics and modest CPU tabular/control-flow evaluation
without GPU or vectorized-throughput claims.
```

### Turn 004 - PO Response

```text
The PO clarified that benchmarking without tensors present is not the same as
benchmarking a tensor-capable `state_collapser` with the tensor path present but
disabled. The presence of tensorization can itself change behavior, architecture,
conversion boundaries, validation, and timing even when disabled.
```

### Turn 005 - Codex Reply

```text
Codex agreed and corrected the claim boundary: the current benchmark can only be
called a pre-R-linearization/current-control-flow baseline, not a no-tensor
ablation of the final tensor-capable architecture. Any tensor-off versus
tensor-on comparison is blocked until a tensor-capable architecture exists.
```

### Turn 006 - PO Response

```text
Tensorization is a blocker. The PO paused this serious counterpoint evaluation
work and directed work to move to tensorization. The PO requested a root
`CONTRIBUTING.md` continuity document and an alignment note inside
`/Users/foster/state_collapser` summarizing the conclusions reached here.
```

### Turn 007 - Codex Reply

```text
Codex agreed to treat tensorization as a blocker for this serious evaluation
block, pause blueprint/gameplan work, create the local continuity note, and add a
read-only-derived alignment note in `state_collapser` for the tensorization work.
The next resume gate is whether `state_collapser` has a tensor-capable
architecture where tensor paths can be explicitly disabled or enabled.
```
