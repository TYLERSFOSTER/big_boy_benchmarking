# Initial Benchmarking Goals Discussion

## Status

Initial discussion document for `big_boy_benchmarking`.

This document is not an implementation blueprint.

This document is not an implementation gameplan.

This document is not approval to edit benchmark code.

Its purpose is to externalize the current working model of what this repository
is probably for, given the upstream `state_collapser` documentation corpus, and
to create a structured place for Project Owner clarification before any serious
benchmark harness is designed or implemented.

## Authority

The immediate Project Owner instruction was:

> The present project is going to be the more serious benchmarking needed for `state_collapser`. Please read `state_collapser/docs` from that project, and all the `md` docs at root in `state_collapser`. This should give you an idea of what our main goals in the present repo [`big_boy_benchmarking`] are.

> Ok let's jump out of `state_collapser` because I don't want to fuck with anything in there during this work. Go back to `big_boy_benchmarking`, and in `big_boy_benchmarking/docs/design`, put a MASSIVE initial discussion doc regarding your precevied goals for this repo. Put lots of questions to PO with spots for turn-by-turn conversation afterward.


This document therefore lives in:

```text
docs/design/01_001_initial_benchmarking_goals_discussion.md
```

inside:

```text
big_boy_benchmarking
```

The upstream `state_collapser` repository is treated as read-only context for
this work unless the Project Owner explicitly says otherwise.

## Grounding Inputs Read Before This Document

The current working model is grounded in:

- `big_boy_benchmarking/docs/prime_directive/*`
- root markdown docs from the upstream `state_collapser` repository
- upstream `state_collapser/docs/usage/*`
- upstream `state_collapser/docs/api_notes/*`
- upstream `state_collapser/EVALUATION.md`
- upstream test-design docs for the evaluation family
- upstream post-Young-diagram audit and repair docs
- upstream continuity reports for 2026-05-24 and 2026-05-25
- upstream public-release/security audit docs
- upstream synthetic review and accepted revision docs

The important caveat is that those upstream docs are evidence of project intent,
not permission to edit upstream code from this repo.

## Executive Read

My current read is that `big_boy_benchmarking` should become the serious
benchmarking and evidence repository for `state_collapser`.

The upstream package has reached a point where it contains real runtime
machinery:

- partition-backed quotient towers
- schema-driven contraction
- multiple discrete constrained evaluation environments
- tower-depth probing
- tower-aware tabular training smoke paths
- action masks
- lift-aware continuation/bootstrap semantics
- live runtime views separated from value snapshots
- lazy compatibility readouts
- benchmark smoke tooling
- fiber-conditioned training surfaces
- downstream `HGraphML` compatibility pressure

But upstream docs repeatedly state that the project does not yet have serious
benchmark evidence.

The most important open maturity gap is not another ordinary smoke test. It is:

> Can we produce honest, reproducible, multi-seed evidence that quotient/tower structure helps on the kind of coordination-constrained problems `state_collapser` claims to address?

This repo appears to be the place where that evidence should be designed,
run, recorded, and made legible.

## Core Non-Goal

The first rule for this repository should probably be:

> Do not turn benchmark work into upstream package hacking.

This repo should be allowed to depend on `state_collapser`, import it, install
it, pin it, run it, and observe it. It should not casually modify it.

If benchmark work reveals upstream defects, the output should be:

- a minimal reproduction
- a benchmark artifact
- an issue-style diagnosis
- a proposed upstream change

not a stealth edit inside `state_collapser`.

## Why This Repository Exists

The upstream public posture is currently:

> state_collapser is a pre-alpha research package for constructing quotient-tower structure over discovered transition systems and exposing tower-aware training surfaces.

The upstream public posture explicitly avoids:

> state_collapser speeds up RL training.

because that claim is not yet backed by serious benchmark artifacts.

So the likely job of this repository is to close the gap between those two
sentences.

Not by manufacturing a flattering graph.

Not by cherry-picking a single seed.

Not by comparing against weak baselines.

Not by treating tower depth as proof of learning benefit.

But by creating a benchmark program that can survive skeptical inspection.

## The Benchmarking Claim Under Test

The broad motivating claim from `state_collapser` is:

> For some RL problems with hidden constraint geometry and no obvious human-authored hierarchy, quotient/tower structure can reduce effective search or training burden relative to flat learning.

That is a subtle claim. It contains many pieces:

1. The environment must actually have hidden constraint geometry.
2. The hierarchy must not be handed to the learner as an obvious task
   decomposition.
3. The tower must actually build nontrivial quotient structure.
4. The learner or controller must actually use the hierarchy.
5. The performance improvement must survive comparison to honest baselines.
6. The improvement must survive multiple seeds and budgets.
7. The runtime overhead must not erase the benefit.
8. Negative or bad-fit environments must not be ignored.

This repo should probably treat that whole chain as the object of evaluation.

## What Counts As Evidence

The upstream docs split evaluation into three layers:

1. Structural evaluation
2. Behavioral evaluation
3. Performance evaluation

That split should probably become the backbone of this repo.

### Structural Evidence

Structural evidence answers:

- Is this environment even a legitimate `state_collapser` testbed?
- What hidden constraint geometry does it encode?
- What makes the naive flat parameterization misleading?
- What quotientable regularity might exist?
- Does the environment preserve reward locality assumptions?
- Is the state/action graph inspectable enough?

This evidence should not be optional. A benchmark that skips structural
evaluation can accidentally reward environments that are easy, rigged, or
irrelevant.

### Behavioral Evidence

Behavioral evidence answers:

- Does the tower actually become nontrivial?
- Which schemas produce scheduled assignments?
- Does default schema behavior differ from explicit flat schema behavior?
- Do tiers materialize differently across time?
- Does active-tier control actually move through the tower?
- Does the runtime look hierarchical or just tower-shaped?

The upstream post-Young audit proves why this layer matters: all example tests
can pass while most environments are semantically tower-flat.

This repo should therefore make behavioral diagnostics first-class.

### Performance Evidence

Performance evidence answers:

- Does full-tower training improve success rate?
- Does it improve sample efficiency?
- Does it improve cumulative reward?
- Does it reduce variance?
- Does it help under comparable budgets?
- Does the runtime overhead remain acceptable?
- Does it still help when compared to the empty-schema/no-contraction baseline?
- If a future `coarse-only` ablation exists, does full tower still add value
  beyond that single-abstraction condition?

This is the layer most people will look at first, but it is the layer that can
most easily lie if structural and behavioral evidence are missing.

## Canonical Comparison Structure

The upstream docs initially suggested a three-mode comparison:

1. `Flat`
2. `Top-tier-only`
3. `Full tower`

The Project Owner reply pass changed how this repository should interpret that
middle term. In this repo, the owner-defined empty-schema comparison means the
tower stays at `G_t^0`; no contractions are scheduled. If a future benchmark
needs "coarsest abstraction only," it should be given a different name, such as
`coarse-only`, rather than overloading `Top-tier-only`.

### Flat

The `Flat` condition asks:

```text
What happens if we train directly on the underlying environment without useful
quotient/tower hierarchy?
```

Potential implementation interpretations:

- direct Gymnasium-style training
- `state_collapser` runtime with `NoContractionSchema`
- a learner keyed only on the total/fine state
- no tower-aware staged behavior

These are not all identical, and the repo needs to be precise about which
meaning is used in each benchmark.

### Top-Tier-Only / Empty-Schema

For this repo, the `Top-tier-only` / empty-schema condition asks:

```text
What happens when the tower never leaves G_t^0 because the contraction schema is empty?
```

Operationally, this is the no-contraction baseline. It controls for the
benchmark harness, runtime shell, learner, and environment interaction while
removing quotient-tower construction.

Earlier language about a single coarse abstraction should be treated as a
separate possible future ablation, not as the owner-defined meaning of
`Top-tier-only` here.

### Full Tower

The `Full tower` condition asks:

```text
Does the whole quotient/tower apparatus help enough to justify itself?
```

This should include both:

- the structural benefit of quotient tiers
- the operational cost of maintaining and using them

If full tower only wins when runtime overhead is ignored, the benchmark should
say that.

If full tower only wins against weak flat baselines, the benchmark should say
that.

If full tower wins structurally but not in learning performance, the benchmark
should say that.

## Candidate Benchmark Environments

The upstream authoritative evaluation family currently appears to include:

- `plate_support_env`
- `articulated_loop_env`
- `dual_arm_manipulation_env`
- `cable_parallel_env`
- `parallelogram_singularity_env`
- `rl_counterpoint_v3`

These are not interchangeable. A serious benchmark repo should probably treat
them as different environment families with different hypotheses.

### `plate_support_env`

Likely role:

- flagship support/placement constraint environment
- most mature existing reference
- exploit/explore path most developed here

Hidden geometry:

- rigid plate on grid
- support arms
- feasible state subset cut down by reach and stability constraints

Benchmark value:

- good first sanity target
- useful for comparing default schema vs no schema
- possibly not enough by itself to carry broad claims

Risk:

- current default schema may be more smoke-schema than scientific schema
- may be too broad if all visible transitions share one contraction label

### `articulated_loop_env`

Likely role:

- loop-closure hidden geometry
- simple ambient joint directions with closure mismatch/slack

Hidden geometry:

- feasible loop-closed states are a constrained subset of joint direction
  product space

Benchmark value:

- clean geometry
- easy to inspect
- useful for validating constraint-induced quotient behavior

Risk:

- closure slack can make the graph either frozen or too unconstrained

### `dual_arm_manipulation_env`

Likely role:

- conceptually central coordination-constrained environment
- closest to the shared-object manipulation story

Hidden geometry:

- object pose plus two arm states
- valid motion depends on coordinated support/manipulation feasibility

Benchmark value:

- likely one of the most important environments for the package's motivating
  claim

Risk:

- can become simulator-like if expanded too far
- current small version may or may not be rich enough for strong performance
  separation

### `cable_parallel_env`

Likely role:

- support/coupling comparison family near `plate_support_env`

Hidden geometry:

- platform pose plus cable tensions
- validity depends on coupled support/tension feasibility

Benchmark value:

- helps show that the support story is not only one rigid-arm example

Risk:

- can collapse into `plate_support_env` with renamed variables if not
  evaluated structurally

### `parallelogram_singularity_env`

Likely role:

- bottleneck/singularity local geometry test

Hidden geometry:

- local feasible transition structure changes sharply near singular regimes

Benchmark value:

- tests whether tower structure responds to bottlenecks, not only support
  constraints

Risk:

- singularity can become decorative if it does not alter transition structure
  enough

### `rl_counterpoint_v3`

Likely role:

- symbolic constrained RL domain
- historically important source of the project owner's HRL thinking

Hidden geometry:

- ordered three-voice pitch tuples
- bounded simultaneous pitch deltas
- legal node/edge subset cut down by voice ordering, intervals, spacing, motion
  constraints, and reward context

Benchmark value:

- broadens the suite beyond robotics-flavored constraints
- tests whether the tower story works on symbolic constrained structure

Risk:

- must not reimport the old hand-authored `rl_counterpoint` rank tower
- if schema choices encode too much musical hierarchy, the benchmark can become
  circular

## Negative Controls

A serious benchmark suite should probably include bad-fit or low-fit cases.

Possible negative-control roles:

- an unconstrained or nearly unconstrained lattice
- an environment with obvious built-in hierarchy
- a small task where flat learning is already trivial
- a random/schema-null condition
- an intentionally bad contraction schema

The goal is not to make `state_collapser` look bad.

The goal is to prove that the methodology can distinguish:

```text
hierarchy helps here
```

from:

```text
the benchmark always makes hierarchy look good
```

Without negative controls, the benchmark program risks becoming self-confirming.

## Schema Questions

The post-Young repair established default schemas and explicit flat baselines.

That is necessary, but not the end of benchmark design.

There are probably at least four schema categories:

1. `none`
2. smoke/default schema
3. semantic schema
4. adversarial or intentionally bad schema

### No Schema

`NoContractionSchema` should mean explicit flat partition-tower baseline.

This is useful because it controls for overhead of the runtime shell and
discovery path while disabling quotient coarsening.

### Smoke Or Default Schema

A smoke/default schema proves:

- labels are present
- assignments schedule
- tower depth becomes nontrivial
- default environment runtime is not silently tower-flat

But a smoke schema is not necessarily a scientifically meaningful schema.

### Semantic Schema

A semantic schema represents an actual quotient hypothesis:

- support motion family
- cable tension family
- loop closure family
- singularity crossing family
- voice-motion family
- coordination family

These are likely the schemas that matter for real benchmark claims.

### Bad Or Ablation Schema

A bad schema might intentionally group edges in a way that should not help.

This can test whether results depend on meaningful quotient structure rather
than merely on any compression.

## Benchmark Harness Responsibilities

This repository should probably own a benchmark harness that can:

- install or locate a specific `state_collapser` version
- run a declared benchmark matrix
- preserve all run configuration
- execute multiple seeds
- collect structural diagnostics
- collect behavioral traces
- collect performance metrics
- write persistent artifacts
- summarize results in tables
- generate plots or lightweight reports
- compare runs against prior artifacts
- avoid mutating upstream package state

## Artifact Expectations

The upstream docs repeatedly mention missing benchmark artifacts.

This repo should probably create a stable artifact layout early.

Potential artifact tree:

```text
artifacts/
  runs/
    <run_id>/
      manifest.json
      environment_manifest.json
      dependency_manifest.json
      benchmark_matrix.json
      raw_events.jsonl
      episode_results.csv
      structural_diagnostics.csv
      tower_depth.csv
      active_tier_trace.csv
      timing.csv
      summary.json
      summary.md
      plots/
        success_rate.png
        reward_curve.png
        sample_efficiency.png
        tower_depth.png
        runtime_cost.png
```

Potential docs output tree:

```text
docs/results/
  <run_id>_summary.md
```

Potential machine-readable registry:

```text
benchmarks/
  matrices/
  configs/
  schemas/
  runners/
  reports/
```

These names are only proposals. The important thing is that artifacts must be
stable enough to support later comparison.

## Reproducibility Minimum Standard

Each run should probably record:

- benchmark repo commit
- upstream `state_collapser` version, commit, tag, or editable path
- Python version
- operating system
- dependency lockfile hash if available
- environment name
- schema mode
- training mode
- learner type
- hyperparameters
- seed
- budget
- command
- start/end time
- artifact schema version

Without this, benchmark artifacts will become anecdotal.

## Metrics Inventory

The repo should probably separate metrics by type.

### Structural Metrics

Possible structural metrics:

- flat path-volume estimate, `PVol`
- policy-effective path-volume estimate under the current learner or policy
- valid state count
- ambient state count
- valid/ambient ratio
- valid edge count
- average branching factor
- action-mask density
- connected component count
- shortest path length to goal where computable
- graph diameter where computable
- bottleneck or cut-like diagnostics where computable

### Tower Metrics

Possible tower metrics:

- max depth
- depth curve over time
- scheduled assignment count
- unscheduled assignment count
- state cell counts by tier
- action cell counts by tier
- compression ratio by tier
- quotient path-address compression ratios, conceptually `|Omega_i| / |Omega_{i-1}|`
- lift-fiber size
- lift-fiber entropy
- reward variance inside quotient fibers
- internal edge count by tier
- loop/preimage aggregation summaries
- compatibility readout cost when requested

### Behavioral Metrics

Possible behavioral metrics:

- active tier over time
- tier transitions
- fiber departures
- action-mask violations
- chosen action legality
- coarse behavior selected
- fine lift success/failure
- lift success rate
- fine-refinement residual
- control fallback reasons

### Performance Metrics

Possible performance metrics:

- episode return
- success rate
- time-to-first-success
- episodes-to-threshold
- steps-to-threshold
- area under reward curve
- sample efficiency at fixed budget
- final policy evaluation score
- variance across seeds
- coarse-policy value error
- wall-clock and sample-efficiency comparison against a non-tower baseline

### Runtime Metrics

Possible runtime metrics:

- wall-clock time
- steps per second
- partition update time
- readout time
- learner update time
- memory usage
- discovered state/edge growth
- cost with compatibility readouts disabled vs enabled
- cost with morphism construction disabled vs enabled

## Training Modes

The upstream package currently has simple research-mode training surfaces.

This repo should not pretend those are mature neural RL baselines.

Possible first training modes:

1. Flat tabular baseline
2. No-schema tower shell baseline
3. Default-schema tower-aware tabular training
4. Semantic-schema tower-aware tabular training
5. Top-tier-only tabular training
6. Exploit/explore on environments where it exists
7. Fiber-conditioned stage experiments where appropriate

Later training modes might include:

- DQN-like neural learner
- SB3 baseline wrapper
- simple policy gradient
- vectorized rollout harness
- replay-buffer experiments

But those later modes should probably wait until the artifact and semantic
surfaces are honest.

## Baseline Discipline

A benchmark result is only as good as its baselines.

Potential baseline hierarchy:

### Baseline 1: Direct Flat Learner

Train directly on the environment's observable state/action surface.

This tests whether tower machinery is useful at all.

### Baseline 2: Runtime Shell With No Schema

Use `state_collapser` runtime machinery but pass `NoContractionSchema`.

This controls for runtime/discovery overhead and training loop differences.

### Baseline 3: Empty-Schema / No-Contraction

Use the same runtime shell with an empty contraction schema, so the tower remains
at `G_t^0`.

This controls for runtime/discovery overhead without quotient-tower structure.

If a later benchmark needs to test whether a single coarse abstraction captures
all benefit, name that condition `coarse-only` or similar.

### Baseline 4: Random Or Weak Policy

Useful as a sanity floor.

This should not be the primary baseline.

### Baseline 5: Oracle Or Graph-Search Reference

For small environments, compute shortest paths or exact reachability.

This can establish task difficulty and whether learners are failing for obvious
reasons.

## What This Repo Should Not Claim Too Early

This repo should probably avoid these claims until artifacts support them:

```text
state_collapser speeds up RL in general.
```

```text
state_collapser beats RLlib or Stable-Baselines3.
```

```text
quotient towers solve sparse reward.
```

```text
the default schemas are scientifically final.
```

```text
the current tabular loops prove neural learner performance.
```

Safer early claims:

```text
This benchmark run shows nontrivial tower materialization under schema X.
```

```text
On this environment and budget, full tower outperformed flat tabular training
across N seeds.
```

```text
On this environment, the empty-schema/no-contraction baseline captured most of
the observed benefit.
```

```text
On this environment, tower overhead erased the learning benefit.
```

```text
This environment does not appear to be a strong state_collapser testbed.
```

Negative results are valuable here.

## Relationship To Upstream `state_collapser`

This repo should probably consume upstream `state_collapser` in one of three
ways:

1. local editable path for active private development
2. pinned git tag for public/release benchmark reproduction
3. later PyPI package once upstream is published

The benchmark artifact should record which one was used.

Given the Project Owner's current instruction, this repo should not modify the
upstream checkout during benchmark design.

If an upstream code defect is found, the benchmark repo can produce:

- a failing benchmark
- a reduced reproduction
- a diagnosis document
- a proposed upstream issue

The Project Owner can then decide whether to switch context and patch
`state_collapser`.

## Potential Repository Layout

This is a discussion proposal, not a gameplan.

Possible layout:

```text
big_boy_benchmarking/
  docs/
    design/
    results/
    benchmark_contracts/
  benchmarks/
    configs/
    matrices/
    runners/
    metrics/
    reports/
  scripts/
  tests/
  artifacts/
```

Potential package shape if this repo becomes importable:

```text
src/big_boy_benchmarking/
  configs/
  runners/
  metrics/
  artifacts/
  state_collapser_adapter/
```

The name of the import package, if any, should be decided deliberately.

This repo might also remain script-first rather than package-first. That is a
Project Owner decision.

## Possible First Milestone

A conservative first milestone might be:

```text
Create a benchmark harness that runs plate_support_env in Flat,
NoContractionSchema, and default-schema Full tower modes across several seeds,
emits stable artifacts, and produces a summary report that includes structural,
behavioral, performance, and runtime metrics.
```

Why this first:

- `plate_support_env` is the most mature upstream environment.
- It has exploit/explore support.
- It has existing default schema behavior.
- It can establish artifact conventions before broadening.

Risk:

- If the first milestone only uses `plate_support_env`, it might overfit the
  repository's benchmark structure to one environment.

Alternative first milestone:

```text
Create a structural/behavioral-only benchmark pass across all six environments
before doing any training comparison.
```

Why this first:

- It protects against tower-flat semantic drift.
- It is cheaper than multi-seed training.
- It clarifies which environments deserve performance runs.

Risk:

- It delays actual learning evidence.

## Possible Benchmark Phases

These are not approved phases. They are a discussion scaffold.

### Possible Phase A: Benchmark Corpus Binding

Goal:

- bind which upstream version is being benchmarked
- list environments
- list comparison modes
- define artifact contract

### Possible Phase B: Structural And Behavioral Probe Harness

Goal:

- run tower-depth and schema diagnostics across environments
- record structural environment metadata
- produce first result artifacts

### Possible Phase C: Single-Environment Training Harness

Goal:

- run a first flat vs tower training comparison on one mature environment
- validate artifact writing and seed handling

### Possible Phase D: Evaluation-Family Training Matrix

Goal:

- run the benchmark matrix across all approved environments
- compare environment families

### Possible Phase E: Empty-Schema And Ablations

Goal:

- answer whether full tower matters beyond the no-contraction baseline
- test schema ablations
- optionally define a separate `coarse-only` ablation later

### Possible Phase F: Runtime Scaling Benchmarks

Goal:

- measure partition update vs compatibility readout costs
- measure schema/no-schema and morphism/no-morphism cost shape

### Possible Phase G: Report And Release Bundle

Goal:

- produce a benchmark report suitable for upstream README/release/public claims
- preserve raw artifacts for reproducibility

___
___

## `logHRL.tex` Training-Time Diagnostics Coverage

After checking the end of upstream:

```text
/Users/foster/state_collapser/docs/design/logHRL.tex
```

the paper explicitly says the package should report not only return curves, but
also tower diagnostics. The list there is the measurable content of the
path-volume theorem's hypotheses.

This local benchmarking discussion must therefore include the following as
first-class benchmark targets:

1. Flat and policy-effective `PVol` estimates.
2. Quotient compression ratios, conceptually `|Omega_i| / |Omega_{i-1}|`.
3. Lift-fiber size and entropy.
4. Reward variance inside quotient fibers.
5. Lift success rate.
6. Coarse-policy value error and fine-refinement residual.
7. Wall-clock and sample-efficiency comparisons against a non-tower baseline.

Coverage status in this document after this update:

- `PVol` estimates are now named explicitly under structural metrics.
- Quotient compression ratios are now named explicitly under tower metrics.
- Lift-fiber size and entropy are now named explicitly under tower metrics.
- Reward variance inside quotient fibers is now named explicitly under tower
  metrics.
- Lift success rate is now named explicitly under behavioral metrics.
- Coarse-policy value error and fine-refinement residual are now named
  explicitly under performance/behavioral metrics.
- Wall-clock and sample-efficiency comparisons against a non-tower baseline are
  now named explicitly under performance/runtime metrics.

Open design issue:

```text
The paper names these diagnostics mathematically, but this benchmark repo still
needs operational estimators for each one. In particular, policy-effective
PVol, quotient path-address compression, lift-fiber entropy, reward variance
inside quotient fibers, coarse-policy value error, and fine-refinement residual
need concrete measurement definitions before they can become benchmark columns.
```

## Questions For The Project Owner

This section is intentionally large. The goal is to make the ambiguity map
explicit before any benchmark harness design hardens into code.

Each question has answer slots for turn-by-turn conversation.

## PO Question 1: What Is The Primary Audience?

Who is the first serious benchmark audience?

Possible audiences:

- you, for internal confidence
- future contributors
- skeptical RL researchers
- robotics/control researchers
- package users
- PyPI release reviewers
- HGraphML/downstream users
- public GitHub readers

Why it matters:

- internal benchmarks can be rougher
- public benchmarks need cleaner artifacts and language
- research benchmarks need stronger negative controls and baselines

### PO Answer 1.1

```text
Focus first on skeptical RL researchers = robotics/control researchers = package users, meaning the cases where these coincide.
```

### Follow-Up 1.1

```text
Codex response:

This narrows the audience usefully. The first serious benchmark should be
written for the intersection of skeptical RL researchers, robotics/control
researchers, and package users: people who care about scientific honesty, but
also need to know whether the package is practically worth trying. That means
the benchmark should privilege reproducible artifacts, explicit environment
geometry, clear baselines, and sober language over polished marketing.
```

### PO Answer 1.2

```text

```

### Follow-Up 1.2

```text

```

## PO Question 2: What Claim Should The First Benchmark Try To Support?

Should the first benchmark target be:

- "the tower builds nontrivial structure"
- "the tower improves tabular learning on small constrained examples"
- "full tower beats flat across the environment family"
- "full tower beats the empty-schema/no-contraction baseline"
- "runtime overhead is acceptable"
- "we can produce reproducible benchmark artifacts"

These are different goals.

### PO Answer 2.1

```text
"the tower builds nontrivial structure"
```

### Follow-Up 2.1

```text
Codex response:

This makes the first benchmark claim structural/behavioral rather than
performance-first. The first serious benchmark milestone should prove that the
tower actually builds nontrivial structure under declared schemas on benchmark
problems that matter. Return curves can still be recorded, but they should not
be the primary success claim for the first milestone.
```

### PO Answer 2.2

```text

```

### Follow-Up 2.2

```text

```

## PO Question 3: What Is The Minimum Public-Release Benchmark Bar?

Upstream docs say PyPI should wait for serious benchmarking.

What is the minimum benchmark evidence needed before PyPI becomes acceptable?

Possibilities:

- one strong environment
- multiple environments
- all six current environments
- at least one symbolic and one robotics-flavored environment
- explicit negative controls
- empty-schema/no-contraction comparisons
- later `coarse-only` comparisons if that ablation is defined
- runtime scaling curves
- neural learner baselines

### PO Answer 3.1

```text
ultiple environments, at least one symbolic and one robotics-flavored environment
```

### Follow-Up 3.1

```text
Codex response:

Binding this as: before PyPI, the evidence should include multiple serious
environments, with at least one symbolic family and one robotics/control-flavored
family. The existing upstream smoke environments may help exercise harness
machinery, but they do not by themselves satisfy this bar if the "big boy"
environment families are still missing.
```

### PO Answer 3.2

```text

```

### Follow-Up 3.2

```text

```

## PO Question 4: Should This Repo Be Script-First Or Package-First?

Should `big_boy_benchmarking` become an installable Python package, or should it
remain a scripts/artifacts/docs repository?

Package-first advantages:

- testable internal modules
- reusable metrics/reporting code
- cleaner dependency management

Script-first advantages:

- faster early iteration
- less packaging overhead
- clearer separation from upstream package

### PO Answer 4.1

```text
Explain.
```

### Follow-Up 4.1

```text
Codex response:

Script-first means the repo is mostly command files and ad hoc runners. That is
fast early, but it gets brittle once metrics, artifact schemas, statistical
summaries, and environment adapters need tests.

Package-first means creating a small importable benchmark library inside this
repo, likely under `src/big_boy_benchmarking/`, with scripts as thin CLI
wrappers. That is a little more upfront structure, but it gives us testable
metrics, stable artifact writers, and reusable environment/run abstractions.

My recommendation is package-first internals with script-first ergonomics:
implement real reusable code as a local package, but expose simple commands for
running benchmark matrices. This keeps the work scientifically maintainable
without making the user experience fussy.
```

### PO Answer 4.2

```text

```

### Follow-Up 4.2

```text

```

## PO Question 5: How Should We Pin `state_collapser`?

For benchmark reproducibility, should this repo use:

- local editable path
- local wheel
- public git tag
- exact commit hash
- future PyPI version

Current Project Owner instruction suggests not modifying upstream, but it does
not yet define dependency binding.

### PO Answer 5.1

```text
Tell me pros/cons and your recommendation. One thing is that the "freeing" of `state_collapser` is really just for our own scientific measure. We can go back and improve, but we want our experiments to be meaningful.
```

### Follow-Up 5.1

```text
Codex response:

Pros/cons:

- local editable path is best for reconnaissance because it is fast and can
  observe current upstream reality, but it is dangerous for official benchmark
  claims unless the upstream commit and dirty state are recorded exactly.
- local wheel is more frozen than editable path and is good for repeatable local
  runs, but it adds build friction.
- public git tag is best for public reproducibility when the benchmark targets a
  released upstream state.
- exact commit hash is best for scientific precision, especially between tags.
- future PyPI version will eventually be best for outside users, but upstream
  explicitly defers PyPI until benchmarking improves.

Recommendation:

Use local editable path only for read-only reconnaissance and harness
development. For any result we might cite, bind `state_collapser` by exact
commit hash or public tag, record the commit in the artifact manifest, and
record whether the upstream checkout was dirty. If upstream is improved because
of benchmark findings, that should start a new benchmark run family rather than
silently continuing the old one.
```

### PO Answer 5.2

```text

```

### Follow-Up 5.2

```text

```

## PO Question 6: What Environments Are In Scope First?

Should the first benchmark target:

- only `plate_support_env`
- all six current environments
- only the robotics-flavored five
- only `plate_support_env` and `rl_counterpoint_v3`
- structural probes across all, training on one
- some new larger environment not currently upstream

### PO Answer 6.1

```text
Oh there is maybe a basic confusino here. For BIG BOY benchmarking, the old environments are not sufficient at all. Part of this benchmarking is going to be some serious research into several levels or scales of new environment that actually push the package.
```

### Follow-Up 6.1

```text
Codex response:

This is a major correction to the initial document. The current upstream
environments should be treated as smoke/reality-check surfaces, not as the real
benchmark corpus. Big-boy benchmarking includes environment research: designing
new families at several levels of scale that actually stress the package. The
benchmark repo therefore needs an environment-design track, not merely a runner
for existing examples.
```

### PO Answer 6.2

```text

```

### Follow-Up 6.2

```text

```

## PO Question 7: Should We Trust Current Upstream Example Environments?

Do we treat the current six upstream environments as benchmark candidates, or
should this repo first audit whether they are serious enough?

Possible stance:

- trust them as initial benchmark surfaces
- structurally audit first
- use them only as harness smoke tests
- design new larger benchmark environments here

### PO Answer 7.1

```text
We should investigate this. They may have become defunct in some of the `synthetic_blow` code revisions. We should *not* trust them as suitable for current benchmarks, but we do want to trust them as smoke-benchmarks.
```

### Follow-Up 7.1

```text
Codex response:

Agreed. The current upstream examples become smoke-benchmarks and regression
sentinels: useful for checking that the harness can import, run, record schema
behavior, and detect tower-flat drift. They should not be trusted as the serious
benchmark suite without renewed audit. This also means a first benchmark phase
can use them for tooling without pretending they settle the package's claims.
```

### PO Answer 7.2

```text

```

### Follow-Up 7.2

```text

```

## PO Question 8: What Does `Top-Tier-Only` Mean Operationally?

The upstream docs require `Top-tier-only` comparison where possible.

But we need an operational definition.

Possible meanings:

- learner sees only top-tier state/action cells
- train over top quotient graph only, then evaluate lifted behavior
- freeze top-tier policy and use a simple lift resolver
- use only the coarsest available tier as a state abstraction
- ignore fine-tier correction

These are materially different.

### PO Answer 8.1

```text
It means the tower stays at $G^{i}_{t}$, $i=0$ the whole time, i.e., that the contracting schema is empty.
```

### Follow-Up 8.1

```text
Codex response:

This rebases the vocabulary. In this document, the comparison previously called
`Top-tier-only` should not be treated as "coarsest abstraction only." The PO
definition here is: the tower remains at `G_t^0`; the contraction schema is
empty; no quotient tiers are built. Operationally, this is the no-contraction or
flat tower-shell baseline.

If we later want to test "coarsest abstraction only," it should get a different
name, perhaps `coarse-only`, so it does not conflict with this owner-defined
meaning.
```

### PO Answer 8.2

```text

```

### Follow-Up 8.2

```text

```

## PO Question 9: Which Learner Should Be Used First?

Should first serious benchmarks use:

- current upstream tabular Q learner
- custom tabular learner in this repo
- direct environment-specific tabular baseline
- DQN-like neural learner
- Stable-Baselines3 baseline
- all of the above eventually, but tabular first

### PO Answer 9.1

```text
Current upstream tabular Q learner, but it will be important to have other learners eventually in the present benchmarking.
```

### Follow-Up 9.1

```text
Codex response:

The current upstream tabular Q learner is the right first learner because it
keeps early results inspectable and tied to upstream reality. It should not be
treated as the final learning story. The benchmark repo should design the
learner interface so later learners can be swapped in: stronger tabular
variants, simple neural learners, and eventually external baselines if useful.
```

### PO Answer 9.2

```text

```

### Follow-Up 9.2

```text

```

## PO Question 10: What Budget Regime Matters?

Should benchmarks emphasize:

- very low sample budgets
- medium budgets
- convergence behavior
- fixed wall-clock budget
- fixed environment-step budget
- fixed learner-update budget
- scaling curves across budgets

The claimed benefit is probably about effective search/training burden, so
budget choice is central.

### PO Answer 10.1

```text
We should use different budget choices.
```

### Follow-Up 10.1

```text
Codex response:

Then budget should become an axis in the benchmark matrix rather than a single
constant. At minimum, we likely want small, medium, and larger budgets measured
in environment steps or episodes, plus wall-clock timing. The point is to see
whether tower structure helps early, helps only after enough exploration, or
never repays its overhead.
```

### PO Answer 10.2

```text

```

### Follow-Up 10.2

```text

```

## PO Question 11: What Seed Count Is Serious Enough?

For early benchmark artifacts, how many seeds should count as real evidence?

Possibilities:

- 5 seeds for smoke
- 10 seeds for early evidence
- 30 seeds for public claims
- adaptive seed count based on variance

### PO Answer 11.1

```text
Explain.
```

### Follow-Up 11.1

```text
Codex response:

Seed count controls how much trust we can put in a result. A tiny seed count can
catch broken code, but it cannot support a scientific claim. A larger seed count
estimates variance and protects against cherry-picking.

Recommended tiers:

- 3 to 5 seeds for smoke and harness debugging.
- 10 seeds for early exploratory evidence.
- 30 or more seeds, or an adaptive variance-based rule, before public-facing
  benchmark claims.

For structural claims like "the tower builds nontrivial structure," the relevant
seed may include environment reset seed, exploration seed, schema/probe seed,
and learner seed. The artifact manifest should distinguish them.
```

### PO Answer 11.2

```text

```

### Follow-Up 11.2

```text

```

## PO Question 12: What Runtime Costs Must Be Counted?

Should performance comparisons include:

- environment step time
- tower update time
- learner update time
- compatibility readout time
- artifact writing time
- plotting/report generation time

My instinct is that training comparisons should include all online runtime costs
needed by the mode being evaluated, while reporting diagnostic costs separately.

### PO Answer 12.1

```text
All online runtime costs.
```

### Follow-Up 12.1

```text
Codex response:

Binding this as: online benchmark comparisons count all costs required during
the actual run mode. That includes environment stepping, tower updates, learner
action selection/update, masks, lift/fiber operations, and any compatibility
readout if the learner actually needs it online. Offline reporting, plotting,
and post-hoc diagnostics can be recorded separately so they do not contaminate
training-time cost.
```

### PO Answer 12.2

```text

```

### Follow-Up 12.2

```text

```

## PO Question 13: Are Compatibility Readouts Part Of The Benchmark Hot Path?

Upstream docs emphasize lazy compatibility readouts.

For benchmark modes, should compatibility `QuotientTierView` readouts be:

- disabled by default
- benchmarked separately
- enabled only for diagnostics
- included when the learner needs them

### PO Answer 13.1

```text
Discuss in more detail.
```

### Follow-Up 13.1

```text
Codex response:

Compatibility readouts are old-style rich quotient views used for inspection and
legacy consumers. The partition tower is supposed to be the hot runtime source
of truth. If a benchmark mode does not need compatibility readouts to choose
actions or update the learner, they should be disabled in the hot path and
measured separately.

If a learner genuinely consumes compatibility readouts online, then their cost
must be included in that mode. But the default benchmark discipline should be:
partition/runtime metrics in the hot path, compatibility readout as an explicit
diagnostic or ablation. This directly tests whether the Young-tableaux refactor
actually avoided repeated global reconstruction costs.
```

### PO Answer 13.2

```text

```

### Follow-Up 13.2

```text

```

## PO Question 14: What Should Count As A Negative Result?

Should this repo explicitly classify failures like:

- environment is bad testbed
- tower does not materialize
- tower materializes but learner does not use it
- empty-schema/no-contraction captures all benefit
- overhead erases benefit
- flat baseline wins
- schema choice is too blunt

### PO Answer 14.1

```text
Let's ignore negative/positive initially. I can read results myself and evaulate as I see fit.
```

### Follow-Up 14.1

```text
Codex response:

Understood. The benchmark harness should record neutral outcome data and avoid
pre-labeling runs as positive or negative. We can still preserve the raw signals
that would allow later interpretation: tower depth, lift success, reward,
sample efficiency, wall-clock, schema behavior, and variance. The Project Owner
can then evaluate meaning from the results.
```

### PO Answer 14.2

```text

```

### Follow-Up 14.2

```text

```

## PO Question 15: Do We Need New Environments In This Repo?

Should `big_boy_benchmarking` eventually define benchmark environments outside
upstream `state_collapser`, or should all environments live upstream?

Arguments for upstream:

- examples stay close to package APIs
- package tests protect them
- docs already describe them

Arguments for benchmark repo:

- benchmark environments can be bigger
- avoids bloating upstream
- separates public package from heavy benchmark corpus

### PO Answer 15.1

```text
Yes, many.
```

### Follow-Up 15.1

```text
Codex response:

Binding this as: new benchmark environments are central to this repo, not a
side possibility. The design problem is to create many serious environment
families at different scales, while still using upstream smoke environments as
small compatibility probes. This repo should therefore develop environment
specs, generation rules, scale tiers, and artifact contracts for environments
that are too large or too benchmark-specific to belong inside upstream
`state_collapser`.
```

### PO Answer 15.2

```text

```

### Follow-Up 15.2

```text

```

## PO Question 16: Should Benchmark Artifacts Be Tracked?

Should generated benchmark artifacts be:

- tracked in git
- ignored locally
- stored under Git LFS
- published as release assets
- summarized in docs but raw data external

This matters before the first artifact-writing harness lands.

### PO Answer 16.1

```text
I think the right policy is that benchmark objects that are small enough should be tracked, but then shit like model checkpoints or large input/output tensors should be stored somwhere else and linked to.
```

### Follow-Up 16.1

```text
Codex response:

That suggests a split artifact policy:

- track small benchmark configs, manifests, summaries, compact CSV/JSON tables,
  and lightweight plots when they are useful review artifacts;
- do not track large model checkpoints, huge tensors, raw rollout dumps, or
  bulky generated corpora in normal git;
- store large artifacts externally or in a dedicated artifact mechanism, and
  link them from tracked manifests.

The benchmark manifest should make missing large artifacts obvious by recording
their external location, checksum, size, and generation command.
```

### PO Answer 16.2

```text

```

### Follow-Up 16.2

```text

```

## PO Question 17: What Report Format Matters?

What should the benchmark output primarily produce?

Options:

- machine-readable JSON only
- CSV tables
- Markdown report
- plots
- notebook
- static HTML
- LaTeX/PDF research appendix

### PO Answer 17.1

```text
I think machine-readable JSON and/or CSV tables (maybe even pandas?) makes sense for direct benchmark output, and then a downstream LLM can turn into `md` or `pdf` if we desire.
```

### Follow-Up 17.1

```text
Codex response:

Agreed. The primary output should be machine-readable. I would standardize on:

- JSON for run manifests, nested configs, metadata, and summary objects.
- CSV or Parquet-style tables for episode-level and step-level measurements.
- Pandas can be an internal analysis tool, but the artifact format should not
  require importing a pickle or opaque dataframe object.

Markdown/PDF can be generated downstream from those artifacts. That keeps the
benchmark source of truth analyzable by Python, shell tools, and later LLM
report writers.
```

### PO Answer 17.2

```text

```

### Follow-Up 17.2

```text

```

## PO Question 18: How Much Statistical Formalism Do We Want First?

Should early reports include:

- mean/std only
- confidence intervals
- bootstrapped intervals
- hypothesis tests
- Bayesian estimates
- effect sizes

### PO Answer 18.1

```text
I think early tests should include mean/std, confidence intervals, bootstrapped intervals. We can get more elaborate if we want.
```

### Follow-Up 18.1

```text
Codex response:

Good first statistical layer:

- mean and standard deviation for quick scanning;
- confidence intervals for public readability;
- bootstrap intervals because returns and time-to-success may be non-normal and
  seed counts may start modest.

I would avoid hypothesis-test theater early. Effect sizes can come later once
the benchmark matrix stabilizes. The first priority is to show distributions
and uncertainty honestly.
```

### PO Answer 18.2

```text

```

### Follow-Up 18.2

```text

```

## PO Question 19: How Should We Treat `rl_counterpoint_v3`?

This environment is symbolically important and historically loaded.

Should it be:

- an early flagship benchmark
- a later benchmark after simpler environments are stable
- structural-only at first
- held back until schema choices are more principled

### PO Answer 19.1

```text
Some of the benchmarks we work on will be more intense versions of that smoke benchmark.
```

### Follow-Up 19.1

```text
Codex response:

So `rl_counterpoint_v3` should be treated as a smoke-scale ancestor, not the
serious endpoint. Big-boy benchmark families can inherit its core idea:
symbolic constrained multi-voice action spaces with hidden legality and
reward-local structure, but scale it into harder variants. Important guardrail:
do not smuggle the old hand-authored counterpoint tower into the benchmark as
the solution.
```

### PO Answer 19.2

```text

```

### Follow-Up 19.2

```text

```

## PO Question 20: How Should We Treat Exploit/Explore?

Upstream exploit/explore is most mature on `PlateSupportEnv`.

Should this repo benchmark:

- ordinary tower-aware training first
- exploit/explore first
- both
- exploit/explore only after flat/full/no-contraction comparisons are stable

### PO Answer 20.1

```text
Give me more detailed discussion here.
```

### Follow-Up 20.1

```text
Codex response:

Exploit/explore is different from ordinary tower-aware training. Ordinary
tower-aware training asks whether a learner benefits from tower-position or
fiber-aware decision inputs. Exploit/explore asks whether the controller can use
the tower actively: close or exploit known coarse structure, detect unclosed
regions, descend/refine, and move between tiers.

Benchmarking exploit/explore early has value because it is closer to the
package's distinctive control story. The risk is that it adds another moving
part before the basic benchmark harness is stable. My recommendation is:

1. Use ordinary upstream tabular tower-aware training for the first harness and
   artifact contract.
2. Add exploit/explore as a separate track once the harness can already record
   tower depth, active-tier traces, lift/fiber diagnostics, and wall-clock cost.
3. Do not mix exploit/explore results with ordinary full-tower results without
   naming the controller mode explicitly.
```

### PO Answer 20.2

```text

```

### Follow-Up 20.2

```text

```

## PO Question 21: How Should We Treat Fiber-Conditioned Training?

Fiber-conditioned training is the newer package-native training spine.

Should benchmarks include it early, or is it still too new?

Possible stances:

- defer until ordinary modes are benchmarked
- include as a separate experimental track
- make it central because it reflects the real long-term training story

### PO Answer 21.1

```text
I think early. What other "correct" training is there. Please do a deeper investigation of the `state_collapser` repo to make sure you understand what the pieces are, whne they were introduced, what they do...
```

### Follow-Up 21.1

```text
Codex response:

This is important enough to become its own read-only investigation before a
training benchmark blueprint hardens. My current understanding is:

- older example training used local tabular tower-aware loops;
- `state_collapser.training` introduced reusable inputs, transitions,
  collectors, learners, masks, and reference loops;
- the synthetic review revisions made masks and continuation/bootstrap
  semantics more honest;
- the later fiber-conditioned spine introduced
  `FrozenQuotientBehavior -> PathFiber -> FiberConditionedStage`, which is the
  package-native expression of "freeze coarse behavior, train inside the lift
  fiber."

If the question is "what is the correct `state_collapser` training story?", the
fiber-conditioned path is probably closer to the real answer than the older
ordinary tower-aware tabular loops. But I should verify the exact current code,
tests, and docs in upstream before encoding this into a benchmark plan.
```

### PO Answer 21.2

```text

```

### Follow-Up 21.2

```text

```

## PO Question 22: What Upstream Changes Are Off-Limits?

The current instruction says not to mess with `state_collapser` during this
work.

Should the benchmark repo still be allowed to:

- open upstream files read-only
- install upstream editable
- run upstream tests
- create issue docs referencing upstream paths
- vendor small adapters locally
- monkeypatch during benchmarks

My instinct is:

- read and run upstream is okay
- edit upstream is not okay
- monkeypatching should be avoided except in explicit diagnostic experiments

### PO Answer 22.1

```text
Correct: "read and run upstream is okay
edit upstream is not okay
monkeypatching should be avoided except in explicit diagnostic experiments"
```

### Follow-Up 22.1

```text
Codex response:

Binding this as an operating rule for this repo:

- read upstream docs/source: allowed;
- run upstream commands/tests/probes: allowed when needed;
- install upstream for benchmarking: allowed;
- edit upstream files: not allowed in this work interval;
- monkeypatching: avoid, except in explicitly marked diagnostic experiments.

If the benchmark reveals an upstream defect, the benchmark repo should produce a
reproduction and diagnosis rather than silently patching upstream.
```

### PO Answer 22.2

```text

```

### Follow-Up 22.2

```text

```

## PO Question 23: What Counts As Benchmark Harness Completion?

What is the first "done" definition?

Possible completion criteria:

- one run command works
- one artifact bundle is emitted
- one markdown report is generated
- one environment has flat/full comparison
- all six environments have structural probes
- all six environments have multi-seed performance comparisons

### PO Answer 23.1

```text
Explain.
```

### Follow-Up 23.1

```text
Codex response:

There are several possible "done" levels:

- Harness smoke done: one command runs and emits a valid artifact bundle.
- Structural benchmark done: smoke environments can be probed and structural
  diagnostics are recorded.
- First serious benchmark done: at least one new big-boy environment family has
  multi-budget, multi-seed artifacts comparing contracted vs empty-schema
  behavior.
- Release-grade benchmark done: multiple new environments, including symbolic
  and robotics/control-flavored families, have reproducible artifacts with
  uncertainty summaries and runtime costs.

My recommendation for first completion is artifact-harness done plus structural
smoke done. That gives us a trustworthy measurement machine before we ask it to
settle larger claims.
```

### PO Answer 23.2

```text

```

### Follow-Up 23.2

```text

```

## PO Question 24: Should We Start With A Blueprint Or A Reconnaissance Run?

Two possible next moves:

1. write a full benchmark-system blueprint first
2. do a read-only local reconnaissance run against upstream `state_collapser`
   to see what commands, imports, and outputs actually look like

The prime-directive bias suggests we should clarify authority before
implementation. But a read-only reconnaissance run may be useful reality
binding before writing a blueprint.

### PO Answer 24.1

```text
Explain.
```

### Follow-Up 24.1

```text
Codex response:

A blueprint first gives conceptual order, but it risks designing against a stale
or imagined upstream interface. A read-only reconnaissance run first binds
reality: imports, commands, current outputs, runtime costs, and where the
training/fiber pieces actually live.

Recommendation:

Do a read-only reconnaissance pass first, explicitly not implementation. Its
output should be a local design note recording current upstream callable
surfaces, commands, result objects, and gaps. Then write the benchmark-system
blueprint from that evidence.
```

### PO Answer 24.2

```text

```

### Follow-Up 24.2

```text

```

## PO Question 25: What Should This Repo Be Called Publicly?

`big_boy_benchmarking` is a working repo name.

Should public-facing docs use:

- `big_boy_benchmarking`
- `state_collapser_benchmarks`
- `state_collapser_serious_benchmarks`
- another name

This matters if artifacts or reports become public.

### PO Answer 25.1

```text
`big_boy_benchmarking` is the name. I have no patience for this frightened, millenial, hyper-rule-following mentality that thinks humor in the work place is dangerous. It's `big_boy_benchmarking`. If you think there's some serious technical confusion this will create, let me know, but I think healthy humans understand humor.
```

### Follow-Up 25.1

```text
Codex response:

No serious technical confusion from the name. `big_boy_benchmarking` is clear
enough as a repo name, memorable, and locally meaningful. If public-facing
papers or package metadata ever need a more formal phrase, they can describe it
as "the serious benchmark suite for `state_collapser`" while keeping the repo
name unchanged.
```

### PO Answer 25.2

```text

```

### Follow-Up 25.2

```text

```

## Conversation Synthesis After PO Reply Pass 1

The Project Owner replies materially changed the working model of this repo.

The initial document over-weighted the existing upstream example environments
as possible benchmark candidates. That is now corrected.

Current authority after PO replies:

1. The primary audience is the intersection of skeptical RL researchers,
   robotics/control researchers, and serious package users.
2. The first benchmark claim is structural/behavioral:
   `the tower builds nontrivial structure`.
3. The PyPI/public-maturity bar requires multiple serious environments, with at
   least one symbolic and one robotics/control-flavored environment.
4. The existing upstream environments are smoke-benchmarks and regression
   sentinels, not sufficient big-boy benchmarks.
5. This repo must include serious research into new benchmark environments at
   several scales.
6. The owner-defined empty-schema comparison means the tower stays at `G_t^0`;
   this should be treated as the no-contraction baseline.
7. The first learner should be the current upstream tabular Q learner, while
   leaving room for additional learners later.
8. Benchmark budgets should vary rather than use a single fixed budget.
9. Online runtime costs all count.
10. Benchmark output should be primarily machine-readable JSON and/or CSV-style
    tables, with reports generated downstream.
11. Early statistics should include mean/std, confidence intervals, and
    bootstrap intervals.
12. Large artifacts such as checkpoints and tensors should live outside normal
    git and be linked from tracked manifests.
13. `rl_counterpoint_v3` should inspire more intense symbolic benchmark
    variants rather than serving as the endpoint.
14. Exploit/explore and fiber-conditioned training need deeper treatment, not
    casual inclusion.
15. Upstream `state_collapser` may be read, run, and installed, but not edited
    during this work interval.
16. The repo name is `big_boy_benchmarking`.

Immediate design consequences:

- The next design work should not simply blueprint a runner for the six upstream
  examples.
- A read-only reconnaissance pass against upstream `state_collapser` is likely
  needed before a benchmark-system blueprint, especially to understand the
  current training and fiber-conditioned surfaces.
- The benchmark program needs an environment-design track, an artifact-contract
  track, and a measurement/estimator track for the diagnostics named by
  `logHRL.tex`.
- Existing upstream examples can still be valuable as the first harness smoke
  matrix, but the document should not imply they satisfy the serious benchmark
  bar.

## Provisional Principles

These are my current provisional principles for the repo. They are not approved
until the Project Owner accepts or edits them.

### Principle 1: Evidence Before Claims

The repo should produce artifacts before public claims.

### Principle 2: Three-Layer Evaluation

Every serious benchmark should separate structural, behavioral, and performance
evidence.

### Principle 3: Baselines Are Part Of The Product

Weak baselines are benchmark bugs.

### Principle 4: Explicit Flat Means Explicit Flat

Flat baseline should be explicitly encoded, probably through
`NoContractionSchema` where the benchmark runs through `state_collapser`.

### Principle 5: Tower Depth Is Not A Score

Tower depth is evidence of nontrivial tower materialization, not proof of
learning value.

### Principle 6: Record The Cost

Runtime overhead must be measured, not waved away.

### Principle 7: Preserve Neutral Results

The harness should preserve raw results without initially forcing them into
positive/negative labels. The Project Owner can interpret the result meaning.

### Principle 8: Do Not Patch Upstream By Accident

This repository should not casually mutate `state_collapser`.

### Principle 9: Artifacts Must Outlive The Session

Benchmark results should not live only in terminal output.

### Principle 10: Claims Must Name Their Scope

Every result should say which environment, schema, learner, seed set, and
budget it applies to.

## Suspected First Hard Design Problems

### Problem 1: Naming Empty-Schema Versus Coarse-Only Ablations

The Project Owner has defined the empty-schema comparison as staying at `G_t^0`.

If a future benchmark needs a single-coarse-abstraction-only condition, it needs
a separate name and operational contract so it does not conflict with the
empty-schema baseline.

### Problem 2: Avoiding Schema Circularity

If schemas encode too much hand-authored solution structure, the benchmark no
longer tests induced hierarchy cleanly.

But if schemas are too generic, they may not be meaningful enough for strong
claims.

### Problem 3: Separating Training Benefit From Runtime Cost

Full tower may reduce sample count but increase wall-clock time.

The benchmark needs to report both.

### Problem 4: Choosing The First Learner

Tabular learners are inspectable but limited.

Neural learners are more realistic but add many confounds.

### Problem 5: Artifact Schema Stability

If artifact shape changes every run, comparison will become painful.

### Problem 6: Upstream API Instability

`state_collapser` is pre-alpha. This repo needs either tight pins or compatibility
shims.

### Problem 7: Public Language

The benchmark report must not overstate what the evidence proves.

## Proposed Immediate Next Conversation

The next Project Owner conversation probably needs to settle:

1. whether to authorize a read-only upstream reconnaissance pass
2. the scope of that reconnaissance, especially training and fiber-conditioned pieces
3. the first environment-research direction for new big-boy benchmarks
4. dependency pinning policy for official versus reconnaissance runs
5. the first artifact contract for machine-readable benchmark output
6. whether the next design artifact should be reconnaissance report or benchmark-system blueprint

Until those are answered, implementation would risk encoding unauthorized
benchmark policy.

## Running Conversation Log

This section is for future turn-by-turn continuation.

### Turn 1

Project Owner:

```text
Filled in first-pass answers to the PO questions. Major corrections:
existing upstream environments are not sufficient for big-boy benchmarking;
they should be smoke-benchmarks only. The real benchmark program needs new,
serious environments at several scales. First claim should be that the tower
builds nontrivial structure. Public/PyPI bar requires multiple environments,
including symbolic and robotics/control-flavored families. Read/run upstream is
allowed; editing upstream is not.
```

Codex:

```text
Added Codex follow-up responses under the populated PO answer blocks and added
Conversation Synthesis After PO Reply Pass 1. Rebound the working model away
from "runner for current upstream examples" and toward "serious benchmark repo
with environment research, artifact contracts, structural diagnostics, and
read-only upstream reconnaissance before benchmark blueprinting."
```

Resulting authority change:

```text
The current upstream examples are demoted to smoke/reality-check surfaces. The
benchmark repo must design or host new serious environments, use machine-readable
artifacts, count online runtime costs, and treat fiber-conditioned training and
exploit/explore as important tracks requiring deeper investigation.
```

### Turn 2

Project Owner:

```text

```

Codex:

```text

```

Resulting authority change:

```text

```

### Turn 3

Project Owner:

```text

```

Codex:

```text

```

Resulting authority change:

```text

```

### Turn 4

Project Owner:

```text

```

Codex:

```text

```

Resulting authority change:

```text

```

### Turn 5

Project Owner:

```text

```

Codex:

```text

```

Resulting authority change:

```text

```

## Closing Current Model

My current perceived goal for `big_boy_benchmarking` is:

```text
Build the serious, reproducible, artifact-producing benchmark program that
state_collapser needs before it can honestly claim training/search speed-up or
graduate toward PyPI/public benchmark maturity.
```

The benchmark program should be skeptical by design.

It should test whether the quotient/tower apparatus helps, when it helps, why
it helps, what it costs, and where it fails.

That is the difference between a demo and evidence.
