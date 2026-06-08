# Read-Only `state_collapser` Reconnaissance For `big_boy_benchmarking`

Status: initial reconnaissance document

Created: 2026-05-27

Repository under work: `<repo-root>`

Upstream repository inspected read-only: `<state-collapser-repo>`

Upstream branch state observed:

```text
main...origin/main [ahead 4]
```

No upstream files were edited. This pass used source/doc inspection only. I did
not run upstream tests or probes during this pass.

## Purpose

This document answers the Project Owner request embedded in
`docs/design/01_001_initial_benchmarking_goals_discussion.md`:

> Go to `state_collapser` repo and read everything related to `synthetic_blow`
> review. Speed is critical in this repo, so the changes made there need to
> stand. This means, I think, that we need to have a conversation about more
> serious metric collection... I mean runtimes have error messaging, no...
> Why is it so difficult to get metrics fast following the `synthetic_blow`
> revisions?

It also answers the later correction:

> Training with a tower requires some kind of control flow mechanism that
> pushes agent up/down tiers when appropriate. Is there anything beyond exp/exp
> that does this in `state_collapser`?

The short answer is:

1. The synthetic-Blow revisions deliberately removed expensive rich readouts
   from the hot tower path. Serious metrics can accidentally put those costs
   right back.
2. Runtime error messages and runtime metrics are different objects. Errors can
   be local and event-triggered. Metrics must be repeatable, comparable,
   statistically meaningful, and collected without changing the algorithm being
   measured.
3. The explicit active-tier up/down controller currently lives in the
   exploit/explore stack. Fiber-conditioned training is closely related, and is
   probably central to the correct training story, but it is stage-local and
   does not by itself implement the same autonomous tier-control loop.
4. Ordinary tower-aware tabular training is useful for smoke and early
   harnesses, but it should not be mistaken for the full tower-control story.

## Source Set Inspected

Primary synthetic-Blow review and revision docs:

- `<state-collapser-repo>/docs/code_review/02_001_synthetic_blow_full_repo_review.md`
- `<state-collapser-repo>/docs/code_review/synthetic_blow_review_kit/README.md`
- `<state-collapser-repo>/docs/code_review/synthetic_blow_review_kit/source_notes.md`
- `<state-collapser-repo>/docs/code_review/synthetic_blow_review_kit/synthetic_blow.md`
- `<state-collapser-repo>/docs/design/synthetic_blow_revisions_01/01_001_synthetic_blow_review_revision_blueprint.md`
- `<state-collapser-repo>/docs/design/synthetic_blow_revisions_01/01_002_synthetic_blow_review_revision_implementation_workplan.md`
- `<state-collapser-repo>/docs/design/synthetic_blow_revisions_01/01_003_synthetic_blow_review_revision_implementation_log.md`

Evaluation and public-readiness docs:

- `<state-collapser-repo>/EVALUATION.md`
- `<state-collapser-repo>/README.md`
- `<state-collapser-repo>/CONTRIBUTING.md`
- `<state-collapser-repo>/docs/engineer_continuity/2026/05/25/01_012_state_collapser_rl_spine_public_release_hgraphml_and_history_rewrite.md`

Training, runtime, and benchmark source:

- `<state-collapser-repo>/src/state_collapser/benchmarks/tower_runtime_bench.py`
- `<state-collapser-repo>/src/state_collapser/examples/tower_depth_probe.py`
- `<state-collapser-repo>/src/state_collapser/tower/runtime.py`
- `<state-collapser-repo>/src/state_collapser/tower/snapshot.py`
- `<state-collapser-repo>/src/state_collapser/training/collectors.py`
- `<state-collapser-repo>/src/state_collapser/training/learners.py`
- `<state-collapser-repo>/src/state_collapser/training/metrics.py`
- `<state-collapser-repo>/src/state_collapser/training/stages.py`
- `<state-collapser-repo>/src/state_collapser/training/fibers.py`
- `<state-collapser-repo>/src/state_collapser/training/frozen.py`
- `<state-collapser-repo>/src/state_collapser/tower/control/*`
- `<state-collapser-repo>/src/state_collapser/examples/plate_support_env/runtime.py`
- `<state-collapser-repo>/src/state_collapser/examples/plate_support_env/training.py`

Relevant tests:

- `<state-collapser-repo>/tests/benchmarks/test_tower_runtime_bench.py`
- `<state-collapser-repo>/tests/tower/control/*`
- `<state-collapser-repo>/tests/training/*`
- `<state-collapser-repo>/tests/examples/test_plate_support_env_fiber_conditioned_stage.py`
- `<state-collapser-repo>/tests/examples/test_plate_support_env_exploit_explore_training.py`

## Executive Findings

### Finding 1: The Synthetic-Blow Revisions Are Hot-Path Discipline

The synthetic-Blow review found several serious problems, but for this benchmark
repo the critical runtime finding was:

```text
The partition runtime still pays global readout costs on every update.
```

The implemented response was:

- keep `PartitionTower` as the authoritative runtime object;
- stop rebuilding compatibility `QuotientTierView` readouts on every default
  partition update;
- add lazy `TowerRuntime.compatibility_quotient_tiers()` for old/debug callers;
- split `LiveRuntimeView` from serializable `RuntimeSnapshot`;
- make morphism construction optional;
- add a tiny runtime benchmark that distinguishes readout-disabled and
  readout-enabled mode.

That means speed is not an accidental preference. It is now a core upstream
contract. Any benchmark code that asks upstream to materialize rich quotient
views or full fibers during every step may invalidate the very performance
story it is trying to measure.

### Finding 2: Upstream Has Smoke Metrics, Not Serious Metrics

Upstream now has several metric-like surfaces:

- `state_collapser.training.metrics.EpisodeMetrics`
  - episode index
  - total reward
  - steps
  - success
  - max tower depth
  - freeform diagnostics
- `state_collapser.tower.control.metrics.TierControlMetrics`
  - active-tier occupancy counts
  - controller-mode counts
- `state_collapser.benchmarks.tower_runtime_bench.TowerRuntimeBenchResult`
  - elapsed seconds
  - operations per second
  - discovered state/edge counts
  - tower depth
  - readout/morphism flags
- `tower_depth_probe`
  - schema mode
  - depth curve
  - max depth
  - scheduled/unscheduled assignments
  - reset events

These are real and useful. They are not enough for `big_boy_benchmarking`.

They do not yet give the full measurement suite implied by the paper/design
goals:

- flat and policy-effective `PVol`
- quotient compression ratios
- lift-fiber size and entropy
- reward variance inside quotient fibers
- lift success rate
- coarse-policy value error
- fine-refinement residual
- wall-clock and sample-efficiency comparison against non-tower baselines
- active-tier dwell time and transition traces across serious environments
- artifact bundles with multi-seed uncertainty summaries

Upstream `CONTRIBUTING.md` also names
`src/state_collapser/instrumentation/pathspace_metrics` and
`src/state_collapser/instrumentation/tower_metrics` as homes for future work,
but those directories currently contain no files. So the instrumentation
direction exists conceptually; the serious metric implementation does not yet
exist upstream.

### Finding 3: Fast Metrics Are Hard Because Rich Metrics Can Recreate Readout Cost

The synthetic-Blow revision made the default runtime fast by separating:

- local partition maintenance;
- rich compatibility/debug readouts.

Many serious metrics want information that lives closer to the second category:

- full quotient-tier cell inventories;
- all members of every fiber;
- all edge preimages under contraction;
- action-cell memberships;
- reward distributions inside quotient fibers;
- lift candidate enumeration;
- path-space coverage;
- comparisons of base graph and quotient graph sizes across time.

Some of these can be queried locally if the partition tower exposes the right
indices. Some can be tracked incrementally if we design counters ahead of time.
Some should be sampled. Some should be computed post-hoc. Some are simply
expensive and must be labeled as such.

The mistake would be to say:

```text
The runtime has diagnostics, so the benchmark can just log everything.
```

That is exactly how a benchmark could quietly rebuild the expensive global
objects synthetic-Blow removed from the hot path.

### Finding 4: Runtime Error Messages Are Not Metric Collection

Runtime error messages answer questions like:

- Did the hidden graph return no successor?
- Was the action outside the action space?
- Did the learner receive no legal actions?
- Did a fiber-conditioned stage leave the admissible fiber?
- Was `reset(...)` forgotten before `step(...)`?

These are guardrails. They are valuable because they are local and exceptional.

Metric collection answers different questions:

- How often did this happen?
- Under which schema, seed, budget, and environment?
- Did it happen more in flat, empty-schema tower, or nonempty-schema tower mode?
- Was it correlated with reward, tower depth, fiber size, or control mode?
- What is the confidence interval over seeds?
- Did collecting the metric itself slow the benchmark?

So metric collection needs:

- stable event schemas;
- stable ids;
- counters or append-only event logs;
- explicit online versus offline cost classification;
- seed/budget/run manifests;
- summaries that survive outside terminal output;
- tests that prevent hidden readout materialization in hot-path collection.

Error messages can live in runtime code. Serious benchmark metrics need an
artifact and instrumentation system.

## The Three Benchmark Training Modes Must Stay Distinct

The Project Owner correction is important:

1. Direct environment training, Gymnasium-style
2. Training with tower machinery while the contraction schema is empty
3. Training with tower machinery under one or more nonempty contraction schemas

These are not synonyms.

### Mode 1: Direct Environment Training

This is the ordinary RL baseline. The agent trains on the environment directly.
There is no tower runtime in the decision path.

For this mode, online cost should include:

- environment reset/step;
- learner action selection;
- learner update;
- direct logging needed by the baseline.

It should not include tower construction or partition updates because the tower
is not part of the algorithm.

### Mode 2: Tower Machinery With Empty Schema

This is not the same as direct environment training.

The agent still runs through `state_collapser` tower machinery, but the
contraction schema is empty or no-contraction. The tower remains at `G_t^0`.
This mode measures the cost and behavioral effect of the package shell without
nontrivial quotient contraction.

For this mode, online cost should include:

- environment reset/step;
- tower runtime stepping;
- base partition maintenance;
- learner action selection/update;
- masks/continuation metadata;
- artifact logging needed online.

This is the right no-contraction tower baseline.

### Mode 3: Tower Machinery With Nonempty Schemas

This is the actual quotient/tower condition. It may include multiple schema
variants:

- default upstream schema;
- hand-specified research schema;
- random/seeded schema;
- weak schema;
- intentionally bad schema;
- future learned/discovered schema.

For this mode, online cost should include all costs required by the actual
algorithm:

- environment reset/step;
- tower runtime stepping;
- partition update;
- schema assignment;
- masks/continuation;
- fiber or lift resolution if used online;
- active-tier control if used online;
- learner action selection/update;
- any compatibility readout if the learner truly consumes it online.

If compatibility readouts are only for reporting, they must be measured
separately and kept out of online mode timing.

## Current Upstream Training And Control Surfaces

This section answers the "what training is there?" and "what does up/down
control?" questions.

### Surface 1: Ordinary Tower-Aware Tabular Training

The ordinary training surfaces live under `state_collapser.training`:

- `ActionSelectionInput`
- `ActionDecision`
- `TrainingTransition`
- `StepCollector`
- `EpisodeCollector`
- `TabularQLearner`
- `run_reference_online_loop(...)`
- `run_reference_episode_loop(...)`

The important current behavior:

- `ActionSelectionInput` carries a `runtime_snapshot` and a
  `tower_position_key`.
- `StepCollector` builds training transitions from runtime reset/step results.
- `TabularQLearner` keys Q rows using tower-position keys by default.
- action masks are now first-class in action selection and bootstrap targets.
- continuation/bootstrap semantics are now explicit fields on
  `TrainingTransition`.

This is tower-aware, but not fully tower-control in the strong sense. The
learner can use tower-derived state keys and metadata, but the ordinary loop
does not decide to descend, lift, train, explore, or exploit as active control
events.

### Surface 2: Fiber-Conditioned Training

The implemented chain is:

```text
PartitionTower
    -> FrozenQuotientBehavior
        -> PathFiber
            -> FiberConditionedStage
                -> ActionSelectionInput / TrainingTransition
```

This is more structurally faithful than ordinary tower-position Q-learning.
The idea is:

1. choose behavior at a coarser tier;
2. freeze that coarse behavior;
3. construct the path fiber over it at an adjacent finer tier;
4. train only on fine actions that lift that frozen coarse behavior.

This is probably central to the long-term correct training story because it
uses the quotient/fiber structure directly rather than merely adding tower keys
to a flat learner.

However, `FiberConditionedStage` is stage-local. It does not by itself decide:

- when to descend to a more collapsed tier;
- when to lift/refine upward;
- when to re-intensify exploration;
- when to train versus execute;
- which active tier controls action-time behavior globally.

It provides the stage/fiber substrate that a control regime can use.

### Surface 3: Exploit/Explore Active-Tier Control

The explicit up/down control machinery is in `state_collapser.tower.control`
and `ExploitExploreTowerRuntime`.

Key objects:

- `ActiveTierState`
- `ActiveTierController`
- `ControlAction`
- `TierSignalState`
- `TierControlConfig`
- `FrozenLowerContext`
- `LiftResolveExecutor`
- `TierLearner`
- `TierControlMetrics`
- `ActiveTierTransition`

The controller actions are:

```text
EXPLORE
TRAIN
DESCEND
LIFT
EXPLOIT_EXECUTE
```

The runtime loop in `TowerRuntime` has a separate `ExploitExploreTowerRuntime`
class. It:

- keeps a single active control tier;
- computes pressure from visit counts, TD error, success/failure, and reward
  residual;
- selects the lowest unclosed/productive tier;
- lifts upward if a finer tier requires attention;
- descends downward if the deeper/more-collapsed tier is the productive locus;
- trains when the learner is due;
- otherwise explores or exploits through a `LiftResolveExecutor`;
- records active-tier counts and mode counts.

The tests confirm all core control branches:

- lift when signal demands it;
- descend when the deeper tier is lowest unclosed;
- train when due;
- explore under high pressure;
- exploit under low pressure;
- record mode metrics.

`PlateSupportExploitExploreRuntime` is the mature example binding. It wraps the
ordinary plate-support runtime, builds active-tier state from live tower
positions, supplies `move_down` and `move_up`, and annotates live runtime views
with `active_control_tier` and `last_control_action`.

### Preliminary Answer: Is There Anything Beyond Exploit/Explore That Pushes Up/Down?

I do not see a second equally explicit active-tier controller beyond the
exploit/explore stack.

There are related pieces:

- ordinary tower runtime updates the tower as primitive environment steps are
  observed;
- ordinary tower-aware training can key learners by tower position;
- fiber-conditioned stages train fine behavior inside a frozen quotient fiber;
- tower projection/query APIs can move information between tiers.

But the explicit "controller chooses LIFT/DESCEND/TRAIN/EXPLORE/EXPLOIT" logic
appears to be exploit/explore.

This means Questions 20 and 21 in the discussion doc are indeed about the same
issue. The real issue is the tower-control/training spine:

```text
How do we combine active tier control, frozen lower context, lift/fiber
resolution, and learner updates into benchmark modes that are faithful to the
state_collapser idea?
```

That cannot be answered by casually choosing "ordinary tower-aware training
first" versus "fiber-conditioned training later". The benchmark needs named
controller/training regimes.

## Why Serious Metrics Are Especially Hard After Synthetic-Blow

### 1. Metrics Can Change The Hot Path

If the benchmark asks for a metric at every environment step, and that metric
requires a full quotient readout, then the benchmark is no longer measuring the
fast path. It is measuring the fast path plus the old compatibility tax.

This is not a small bookkeeping issue. The synthetic-Blow revision specifically
made compatibility readouts lazy because repeatedly materializing them was the
performance bug.

### 2. Some Metrics Are Local, Some Are Global

Examples of relatively local or cheap online metrics:

- environment steps;
- learner updates;
- elapsed wall-clock segments;
- active tier;
- control action mode;
- current tower depth;
- discovered state/edge counts;
- whether readout was requested;
- whether morphism construction was requested;
- selected action;
- mask density for the current decision;
- transition reward;
- bootstrap reason;
- termination/truncation flags.

Examples of expensive or potentially global metrics:

- entropy of every lift fiber;
- reward variance inside every quotient fiber;
- all quotient compression ratios across all tiers;
- exact policy-effective path volume;
- full compatibility quotient views;
- full morphism domains;
- all lift candidates for every action cell;
- all preimage internal-loop aggregations across the tower.

The first group can usually be logged online. The second group needs sampling,
incremental summaries, post-hoc computation, or explicit "expensive diagnostic"
mode.

### 3. "Current Snapshot" Is Not A Full Artifact

Upstream now splits:

- `LiveRuntimeView`: live object references for runtime handoff;
- `RuntimeSnapshot`: compact value snapshot produced by `to_snapshot()`.

The compact value snapshot is useful, but it is not a full benchmark artifact.
It stores current position, reward totals/counts, tier count, active control
tier, last control action, and a small diagnostics field. It does not store
full rollout traces, full partition tables, full fibers, full schema state, or
statistical summaries.

So `big_boy_benchmarking` should not expect upstream snapshots to solve
artifact design. They are inputs to our artifact design.

### 4. Stable IDs Matter

Fast metrics should prefer stable IDs and counters:

- run id;
- environment id;
- episode id;
- step id;
- tier id;
- state cell id;
- action cell id;
- schema id;
- seed id;
- controller mode;
- timing segment name.

Rich Python objects are bad artifact keys. They may be unhashable, repr-based,
or unstable across runs. Upstream `RuntimeSnapshot.to_dict()` uses repr fields
for objects it cannot make JSON-safe, which is appropriate for controlled
snapshot serialization but not enough for scientific metrics.

### 5. Fiber Metrics Are Not Free

The desired diagnostics include lift-fiber size and entropy. A fiber is a
preimage-like object: many fine states/actions/paths may map to one coarse
state/action/path. Counting or summarizing those members can require looking at
many registered states and edges.

For tiny smoke graphs, exact fiber metrics are fine. For big-boy graphs, exact
fiber metrics at every step can dominate the algorithm. The benchmark must
decide:

- exact online?
- exact post-hoc?
- sampled online?
- periodic checkpoint?
- approximate sketch?
- disabled unless diagnostic flag is set?

### 6. Reward-Variance Metrics Need Retained Contributors

"Reward variance inside quotient fibers" is a strong diagnostic because it asks
whether quotient reward aggregation is honest. But variance requires retaining
or reconstructing the reward contributors inside the fiber.

If the runtime only stores an aggregate reward, variance is gone unless the
contributors were separately retained. If the benchmark retains every
contributor online, it may create memory cost. If it reconstructs contributors
from compatibility readouts, it may create readout cost.

This should be designed explicitly.

### 7. Path-Space Metrics Need A Definition Before Code

The paper/design goals refer to path-space compression and policy-effective
volume. The upstream repo has placeholders for path-space metric work, but no
implemented path-space metric suite.

`big_boy_benchmarking` should not fake this with a casual count. It needs a
clear definition per environment and per benchmark mode:

- What is a path?
- Is it a primitive environment path?
- A tier path?
- A successful path?
- A policy-supported path?
- A path in the discovered graph only?
- Does path volume count multiplicity, support size, probability mass, or
  entropy?

Until those definitions are fixed, path-space metrics should be marked as
research diagnostics, not mature benchmark columns.

## Proposed Metric Architecture For This Repo

The clean architecture is a multi-channel metric system.

### Channel A: Online Hot-Path Counters And Timings

These are collected during every benchmark run. They must be cheap and should
avoid compatibility readouts.

Candidate fields:

- run id
- environment id
- mode id
- schema id
- learner id
- controller id
- seed id
- budget id
- episode id
- step id
- environment step elapsed time
- tower update elapsed time
- learner act elapsed time
- learner update elapsed time
- artifact logging elapsed time
- current tower depth
- discovered state count
- discovered edge count
- active control tier
- control action mode
- selected action
- reward
- cumulative reward
- terminated
- truncated
- action mask legal count
- action mask total count
- bootstrap allowed
- bootstrap reason
- readout requested
- morphism requested

These should be represented as compact event rows or tables.

### Channel B: Online Control And Training Events

These are needed for exploit/explore and future tower-control modes.

Candidate fields:

- active tier before decision
- active tier after decision
- control action
- exploration pressure
- visit count
- TD error EMA
- success rate
- reward residual EMA
- lift event count
- descend event count
- train event count
- explore event count
- exploit event count
- abstract action duration
- lift/resolve success
- context version
- context invalidation
- replay item count by tier/context

The upstream exploit/explore metrics currently only count active tiers and
modes. This repo needs richer control events if it wants to diagnose tower use.

### Channel C: Periodic Structural Diagnostics

These are not necessarily collected every step. They may be periodic, sampled,
or post-hoc.

Candidate fields:

- quotient compression ratio per tier
- state-cell count per tier
- action-cell count per tier
- average fiber size
- max fiber size
- fiber-size histogram
- sampled lift-fiber entropy
- scheduled/unscheduled assignment counts
- internal-loop aggregation summaries
- reward variance inside sampled fibers
- coarse reward residual
- fine-refinement residual
- exact or estimated `PVol`
- exact or estimated policy-effective `PVol`

These should be flagged with:

- collection cadence;
- exact versus sampled;
- online versus post-hoc;
- whether compatibility readouts were used.

### Channel D: Expensive Debug Readouts

These are explicit diagnostic artifacts, not default run metrics.

Examples:

- compatibility `QuotientTierView` dumps;
- full quotient graph exports;
- full fiber member dumps;
- full morphism domain dumps;
- HGraphML-style graph readouts;
- dense path enumeration.

If a benchmark run uses these online, the run mode must say so. Otherwise they
should be computed after the timed training interval.

### Channel E: Run Manifests And Statistical Summaries

Each run family needs a manifest:

- `state_collapser` path;
- `state_collapser` git commit;
- `state_collapser` dirty/ahead status;
- benchmark repo commit;
- Python version;
- dependency lock or environment summary;
- machine/CPU summary if timing matters;
- benchmark mode;
- environment spec;
- schema spec;
- learner config;
- controller config;
- seed bundle;
- budget config;
- command line;
- artifact schema version.

Then each analysis pass should produce:

- per-seed summaries;
- mean/std;
- confidence intervals;
- bootstrap intervals;
- optional plots or downstream reports;
- explicit missing-artifact notes for large external files.

## Proposed Artifact Tables

This is not an implementation plan yet, but these are the tables I expect this
repo to need.

### `runs.jsonl`

One row per run:

```text
run_id
run_family_id
environment_id
mode_id
schema_id
learner_id
controller_id
seed_bundle_id
budget_id
state_collapser_commit
state_collapser_dirty
started_at
ended_at
status
```

### `episodes.csv`

One row per episode:

```text
run_id
episode_index
episode_seed
steps
return
success
terminated
truncated
max_tower_depth
wall_clock_seconds
env_step_seconds
tower_update_seconds
learner_seconds
artifact_seconds
```

### `steps.csv` Or `step_events.parquet`

One row per environment/control step:

```text
run_id
episode_index
step_index
mode_id
active_tier
control_action
env_action
reward
cumulative_reward
terminated
truncated
tower_depth
discovered_states
discovered_edges
legal_action_count
action_count
bootstrap_allowed
bootstrap_reason
readout_requested
morphism_requested
elapsed_env
elapsed_tower
elapsed_learner_act
elapsed_learner_update
```

### `structural_diagnostics.jsonl`

One row per diagnostic checkpoint:

```text
run_id
episode_index
step_index
cadence
exact
uses_compatibility_readout
tier_index
state_cell_count
action_cell_count
compression_ratio
mean_fiber_size
max_fiber_size
fiber_entropy_estimate
reward_variance_estimate
pvol_estimate
policy_effective_pvol_estimate
```

### `control_events.csv`

One row per controller decision:

```text
run_id
episode_index
control_event_index
active_tier_before
active_tier_after
control_action
exploration_pressure
visit_count
td_error_ema
success_rate
reward_residual_ema
lift_resolve_success
abstract_action_duration
context_version
```

## Proposed Environment Research Program

The existing upstream environments are smoke surfaces. The real work here is
environment research.

### Step 1: Define The Target Geometry

For each candidate family, write an environment spec answering:

- What is the hidden constraint geometry?
- What is the primitive state?
- What is the primitive action?
- What makes flat search wasteful?
- What quotientable regularity should exist?
- What reward locality assumption is being tested?
- What would count as schema leakage or hand-authored solution leakage?

### Step 2: Build Scale Ladders

Each serious family should have levels:

- tiny deterministic sanity instance;
- small exact-diagnostic instance;
- medium benchmark instance;
- large stress instance;
- optionally generated random instance families.

The tiny instance is for exact structural metrics. The medium/large instances
are for runtime and sample-efficiency curves.

### Step 3: Specify Baselines Before Running

At minimum:

- direct environment training;
- tower machinery with empty contraction schema;
- tower machinery with nonempty schema;
- later alternative schema families;
- later coarse-only if we define it separately;
- later stronger learners.

The comparison mode must be visible in artifact names and manifests.

### Step 4: Design Metrics With The Environment

Some metrics are generic. Some are environment-specific.

For example, in a symbolic counterpoint-like family, policy-effective volume
might have a musically constrained path-space interpretation. In a robotics
coordination family, it might be feasible coordination path volume or support
of valid joint trajectories.

Do not force one fake metric definition across all environments before the
environment semantics are clear.

### Step 5: Smoke Against Upstream

Use upstream examples to verify:

- imports;
- runner shape;
- artifact writing;
- seed handling;
- empty-schema mode;
- nonempty-schema mode;
- readout-disabled timing;
- readout-enabled diagnostic timing;
- exploit/explore event capture on `PlateSupportEnv`.

This is not the serious benchmark corpus. It is the harness shakedown.

### Step 6: Run Serious Families

Only after the harness and environment spec are stable:

- run multiple seeds;
- run multiple budgets;
- run multiple schema modes;
- write artifacts;
- summarize uncertainty;
- keep raw outcomes neutral for PO interpretation.

## Immediate Recommendations

### Recommendation 1: Keep Package-First Internals

This repo should have importable internals for:

- run manifests;
- artifact writing;
- online timers;
- metric event schemas;
- seed bundles;
- benchmark modes;
- statistical summaries.

Scripts should be thin wrappers. Otherwise the metric system will become
unreviewable.

### Recommendation 2: Start With A Readout Discipline Test

Before serious environment benchmarking, build a tiny harness smoke test that
proves:

- default run mode does not call compatibility readouts;
- diagnostic mode can call compatibility readouts explicitly;
- both modes record the flag;
- timings distinguish online from diagnostic cost.

This protects the synthetic-Blow speed contract.

### Recommendation 3: Treat Exploit/Explore And Fiber-Conditioned Training As One Design Topic

Questions 20 and 21 in the discussion file should be merged conceptually.

The benchmark should define named regimes such as:

- `direct_env_tabular`
- `tower_empty_schema_tabular`
- `tower_nonempty_schema_tabular`
- `tower_exploit_explore`
- `tower_fiber_conditioned_stage`
- future `tower_control_with_fiber_conditioned_substages`

The exact names can change, but each regime must say:

- who chooses actions;
- whether there is an active tier;
- whether LIFT/DESCEND events exist;
- whether coarse behavior is frozen;
- whether fibers constrain action masks;
- which online costs count.

### Recommendation 4: Do Not Make Compatibility Readout A Default Metric Dependency

Any metric requiring compatibility `QuotientTierView` must be:

- marked as readout-backed;
- optionally computed post-hoc;
- included in online timing only if the benchmark mode actually requires it.

### Recommendation 5: Use Exact Metrics On Tiny Instances, Sampling On Large Instances

For metrics like fiber entropy, reward variance inside fibers, and path volume:

- exact on tiny instances;
- exact periodic checkpoints on small instances;
- sampled or approximate on medium/large instances;
- post-hoc when possible.

### Recommendation 6: Record Seed Bundles, Not Just One Integer

The PO asked whether seed means "minimal validating evaluation sample". It does
not. A seed is a reproducibility input for stochastic processes. A serious run
may need several seeds:

- environment reset seed;
- schema/probe seed;
- learner exploration seed;
- controller seed;
- benchmark sampling seed.

One "replicate" should record a seed bundle. Many replicates are needed to
estimate variance.

## Questions For The Project Owner

### Question A: Should Benchmark Modes Be Named Around Controller Regime?

I think yes. The flat/empty/nonempty split names schema/tower structure, but it
does not fully name the controller/training regime.

Possible dimensions:

```text
environment coupling: direct | tower
schema: none | nonempty schema id
controller: none | exploit_explore | future control regime
training surface: tabular | fiber_conditioned | future learner
```

### Question B: Should We Treat Exact Path-Space Metrics As A Research Deliverable?

I think yes. They should not be faked in the first runner. The first runner can
reserve fields and support simple counts, but serious `PVol` definitions should
be designed with the environment families.

### Question C: How Aggressive Should Online Event Logging Be?

There is a tradeoff:

- more step-level logs make debugging and metrics easier;
- fewer logs reduce overhead and artifact size.

My recommendation is to log compact step rows by default, and only dump rich
objects under diagnostic flags.

### Question D: Should Big Environments Live Entirely Here?

Current authority says yes, many serious environments should live here. We
should still decide whether they are:

- benchmark-only packages under this repo;
- generated specs with adapters;
- candidates for later upstream migration after stabilization.

### Question E: Should We Build A First "Metric Contract" Before A Runner?

I think yes. A runner without an artifact contract will produce terminal
output, not benchmark evidence.

## Final Working Model

The present repo is not a script pile for rerunning upstream examples.

It is the serious benchmark and environment-research lab for `state_collapser`.
Its first job is to preserve the upstream synthetic-Blow speed discipline while
adding the measurement system upstream does not yet have.

The benchmark stack should therefore be built around:

1. explicit benchmark modes;
2. readout-safe online metrics;
3. expensive diagnostics kept explicit;
4. artifact manifests;
5. multi-seed uncertainty summaries;
6. new environment families at multiple scales;
7. a unified view of exploit/explore and fiber-conditioned training as the
   tower-control/training problem.

The most important correction from this reconnaissance is that "tower training"
is not one thing. Direct env training, empty-schema tower training, nonempty
schema tower training, active-tier exploit/explore control, and
fiber-conditioned stages each measure different claims. The benchmark repo must
name them carefully or the results will become impossible to interpret.
