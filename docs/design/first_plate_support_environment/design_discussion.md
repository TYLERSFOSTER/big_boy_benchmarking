# PlateSupport BBB Environment Build Design Discussion

## Purpose

This discussion is for the BBB-side environment build for PlateSupport.

The environment itself already exists upstream in `state_collapser` as
`state_collapser.examples.plate_support_env`. The design question here is how to
make PlateSupport usable in BBB as a serious constrained-robotics benchmark
candidate, without yet designing or running PlateSupport evaluations.

The motivation is not to recreate the counterpoint environment pattern. The
motivation is to move toward constrained robot-style RL problems where training
need is visible at a human scale. The recent counterpoint threshold work
produced a real but tiny signal: `12.0` versus `13.0` was too small and too
fragile to serve as the next persuasive benchmark display. PlateSupport is
interesting because it is already a discrete robotics-flavored support/control
problem with hidden feasible geometry, invalid moves, stability constraints,
and an upstream tower/runtime integration.

The first BBB build should therefore answer:

- Can BBB bind PlateSupport as a first-class environment family rather than only
  as an upstream smoke surface?
- Can BBB expose enough structural and artifact detail to decide whether this
  problem is a better serious benchmark target than counterpoint?
- Can the environment build preserve the robotics/constrained-control meaning
  of the task, rather than forcing it into counterpoint-shaped categories?

#### PO Correction
No *not* "comparable in structure
to `src/big_boy_benchmarking/environments/counterpoint`." The whole point is *more* that we now want "'constrained robot' RL problems that are known to need some training before solving. Basically the 12.0 versus 13.0 thing [an issue that makes the first serious counterpoint environment still a bit of a toy] is too tiny to really measure and I'm trying to find an example that will display better." Please go through everything below and make sure the design discussion starts out aligned with this goal.

#### Codex Reply
Accepted. My earlier wording imported too much of the counterpoint project into
this folder. The corrected framing is:

- PlateSupport is being considered because it is a constrained robotics-style
  problem with a better chance of showing a measurable training-before-solving
  story.
- The BBB environment build should prepare PlateSupport for serious evaluation,
  not copy counterpoint's package shape or evaluation assumptions.
- Counterpoint remains relevant only as evidence that BBB's artifact/readout
  machinery works and as a cautionary example that tiny threshold-margin effects
  are not enough.
- The first design output should be an environment-build blueprint that focuses
  on PlateSupport's own geometry: plate pose, support reachability, engaged
  arms, stability, invalid/self transitions, start-goal distance, and tower
  readiness.

## Starting Alignment

Project Owner direction:

- Move on from counterpoint for now.
- Use a more robotics-based constrained example.
- Prefer the existing plate examples as the natural next candidate.
- Find an environment where training need is large enough to measure clearly,
  unlike the tiny `12.0`/`13.0` counterpoint threshold effect.
- Start an environment-build design area now.
- Do not create the evaluation folder yet; evaluation design comes later.

Codex current read:

- We do not need to design/build the upstream PlateSupport environment from
  scratch.
- We do need to build the BBB-side environment family surface for it.
- BBB currently has only upstream smoke support for `plate_support_env`.
- The build should let us inspect whether PlateSupport is a good larger-signal
  constrained-robotics benchmark candidate before committing to a serious
  evaluation.
- A serious environment-family build probably needs:
  - a `src/big_boy_benchmarking/environments/plate_support` package;
  - stable environment/family ids;
  - instance metadata for the current upstream PlateSupport problem;
  - graph/diagnostic capture centered on PlateSupport's own support geometry,
    invalid moves, liftability/executability, and tower readiness;
  - artifact/manifests/readout-source support;
  - CLI entry points for environment-level diagnostics and smoke validation;
  - docs under `docs/environments`;
  - tests proving BBB can bind the upstream environment and write meaningful
    artifacts.

Verified upstream facts from the current installed `state_collapser` surface:

- ambient candidate states: `2700`;
- valid constrained states: `89`;
- reachable valid states from the configured start: `89`;
- primitive actions: `12`;
- shortest valid path from configured start to configured goal: `6`;
- configured goal is not one primitive action from start;
- valid outgoing transition count ranges from `1` to `10`, with mean about
  `4.36`;
- invalid action count averages about `5.57` per valid state;
- self-looping transition count averages about `7.64` per valid state.

These facts support the basic motivation: PlateSupport is small enough to
inspect exhaustively, but it has a real constrained feasible subset and enough
invalid/self-loop structure that naive action choice should visibly struggle.

## Scope Boundary

In scope for this folder:

- BBB-side environment family design.
- Environment-level diagnostics/smoke artifacts.
- Mapping upstream PlateSupport concepts into BBB artifact language.
- Deciding which upstream surfaces BBB should call directly.
- Deciding what must be local to BBB versus left upstream.
- Capturing enough structural difficulty evidence to decide whether PlateSupport
  deserves a later serious evaluation folder.

Out of scope for this folder:

- Serious learning evaluation design.
- Flat-versus-tower comparison design.
- New PlateSupport environment variants.
- Any claim that PlateSupport already demonstrates tower benefit inside BBB.
- Changes to upstream `state_collapser`, unless design reveals a missing
  upstream contract that must be handed off separately.

## Open Design Questions

### 1. Environment Family Shape

Should the BBB environment package be named:

```text
src/big_boy_benchmarking/environments/plate_support
```

or should it use a more explicit family name such as:

```text
src/big_boy_benchmarking/environments/upstream_plate_support
```

Codex leaning: use `plate_support`, because this is becoming a first-class BBB
environment family, not merely a smoke adapter.

### 2. First Instance Identity

What should the canonical first instance id be?

Possible candidates:

```text
plate_support_v001
plate_support_default_v001
plate_support_5x5_default_v001
```

Codex leaning: use a descriptive id that names the fixed upstream geometry, for
example `plate_support_5x5_default_v001`, because the current upstream env has a
fixed 5x5 workspace, 3 support sockets, 3 arms, 4 orientations, and 12 primitive
actions.

### 3. What Counts As Environment-Level Validation?

Before any learning evaluation, what should BBB prove?

Possible environment-build validation surfaces:

- import pinned upstream `PlateSupportEnv` and runtime;
- enumerate candidate and valid state counts;
- enumerate valid outgoing transitions;
- summarize invalid self-transition structure;
- identify start and goal;
- verify goal differs from start and is not one primitive action from start;
- compute shortest valid path length from start to goal;
- record reachable-state coverage from the configured start;
- report support-pattern, reachability, and stability summaries;
- build the upstream default tower/runtime;
- report quotient/tower shape at reset and after a short controlled rollout;
- write artifact manifests and human-readable environment docs.

### 4. Direct Upstream Training Path

Should this environment build expose upstream `run_tower_training` /
`run_exploit_explore_training` yet, or should those wait for evaluation design?

Codex leaning: wait on serious training loops. The environment build should bind
and inspect runtime surfaces, including enough metadata to prove that the
training entry points are available, but serious training budgets and
flat/tower comparisons belong in a later evaluation folder.

### 5. Counterpoint Reuse Boundary

Which counterpoint machinery should be generalized or reused, and which should
stay counterpoint-local?

Codex leaning: reuse only the shared artifact/mode/seed/timing/readout
machinery. Do not copy counterpoint-specific schema-comparison logic,
threshold-frontier logic, or counterpoint's environment package shape as a
template. PlateSupport should get its own environment-level diagnostic
vocabulary around constrained support geometry and robotics-style feasibility.

## Turn Conversation

### Project Owner Turn 1

> No *not* "comparable in structure to
> `src/big_boy_benchmarking/environments/counterpoint`." The whole point is
> *more* that we now want "'constrained robot' RL problems that are known to
> need some training before solving. Basically the 12.0 versus 13.0 thing [an
> issue that makes the first serious counterpoint environment still a bit of a
> toy] is too tiny to really measure and I'm trying to find an example that will
> display better." Please go through everything below and make sure the design
> discussion starts out aligned with this goal.

### Codex Turn 1

Agreed. The design target is now corrected.

This folder should not ask, "How do we make a PlateSupport version of
counterpoint?" It should ask, "How do we make BBB capable of treating upstream
PlateSupport as a serious constrained robotics benchmark candidate, and what
structural evidence do we need before creating evaluation folders?"

The environment build should stay modest but purposeful. It should not run the
learning comparison yet, but it should produce enough environment-level artifact
surfaces that later evaluation design is not guessing. In particular, the build
should expose:

- the hidden feasible-state reduction from ambient candidate space to valid
  state space;
- the start and goal configuration;
- shortest valid path length and reachability from start;
- invalid-action and self-loop pressure;
- valid outgoing action distribution;
- support-pattern/reachability/stability summaries;
- upstream runtime/tower availability;
- a clean human-facing environment page explaining why this is a constrained
  robot-style problem rather than a counterpoint analogue.

My correction to the future blueprint is: make the first blueprint an
environment-readiness build, not a serious evaluation blueprint. The evaluation
folder should come only after this folder has pinned what PlateSupport is inside
BBB and what evidence suggests it can give a larger, more legible learning
signal.

## Codex Reconnaissance Pass 1

### Question Being Answered

Are we already ready to blueprint the BBB-side PlateSupport environment build?

Codex answer after reading upstream `state_collapser` PlateSupport code,
PlateSupport tests, the tower-depth probe, and BBB's existing upstream smoke
runner:

Yes, we are close enough to write an environment-build blueprint. The blueprint
should be an environment-readiness / artifact-surface blueprint, not a learning
evaluation blueprint. There is enough upstream structure to avoid guessing, but
there are also several decisions that the blueprint must preserve explicitly.

### Upstream Surfaces Already Present

The upstream `state_collapser.examples.plate_support_env` package exports:

- `PlateSupportEnv`;
- `PlateSupportState`;
- `PlateSupportEnvRuntime`;
- `PlateSupportExploitExploreRuntime`;
- `PlateSupportLiftResolveExecutor`;
- `PlateSupportTierLearner`;
- `TowerTrainingConfig`;
- `ExploitExploreTrainingConfig`;
- `run_tower_training`;
- `run_exploit_explore_training`;
- `default_plate_support_schema`;
- state/action mapping helpers;
- geometry/validity/transition/reward helper functions.

That means BBB does not need to invent the robot-like constrained environment,
its Gymnasium wrapper, its default schema, or its upstream tower runtime.

### Upstream Tests Encode Important Contracts

Upstream PlateSupport tests cover:

- frozen/hashable state records and stable observation encoding;
- support socket rotation and socket ordering;
- validity subpredicates:
  - plate center in bounds;
  - all sockets in bounds;
  - engaged-arm reachability;
  - minimum engaged supports;
  - stable support pattern;
- start and goal validity;
- goal differing from start;
- goal changing both plate pose and support configuration;
- goal not being one primitive step from start;
- valid movement/rotation/extension actions;
- invalid moves that self-loop;
- valid clipped self-transitions;
- transition metadata distinguishing candidate state from realized next state;
- reward semantics:
  - `100.0` for goal;
  - `-1.0` for valid non-goal moves;
  - `-3.0` for self-looping moves;
- Gymnasium five-tuple behavior and info keys;
- hidden graph nontriviality and start-goal reachability;
- runtime reset/step consistency between direct env and tower runtime;
- default schema creating a nontrivial tower;
- explicit `NoContractionSchema` staying flat;
- tower training returning structured results and changing a Q-table;
- exploit/explore runtime exposing active-tier state;
- exploit/explore runtime using pointwise `tier_is_executable_from_state`;
- exploit/explore runtime lifting out of non-executable tiers before action;
- a fiber-conditioned PlateSupport smoke stage using `FrozenQuotientBehavior`,
  `PathFiber`, `FiberConditionedStage`, and `TabularQLearner`.

These contracts are not all evaluation targets, but they are build-design
constraints. BBB should not collapse these into one generic "robot env works"
flag.

### Upstream Evaluation Guidance That Matters Here

The upstream `state_collapser` evaluation guidance says a serious environment
workflow should proceed in this order:

1. confirm structural appropriateness;
2. run a tower-depth probe;
3. run tower-aware training;
4. run exploit/explore control where supported;
5. compare against flat and top-tier-only baselines where those surfaces exist;
6. repeat across seeds before empirical claims.

For this folder, only steps 1 and 2 belong in the environment build. Steps 3-6
belong in later evaluation design folders.

Upstream also warns that tower depth is useful but not sufficient:

- depth can show nontrivial recursive contraction;
- depth does not show learning improvement;
- depth must be interpreted with reward trajectories, success rates,
  active-tier traces, and qualitative geometry.

The BBB blueprint should therefore include tower-depth artifacts, but it should
not make tower-benefit claims from them.

### Verified Structural Facts

Using the current installed upstream surface:

- ambient candidate states: `2700`;
- valid states: `89`;
- all `89` valid states are reachable from the configured start through valid
  non-self transitions;
- primitive actions: `12`;
- shortest valid start-to-goal path length: `6`;
- one shortest action sequence is:
  - `1`: move plate left;
  - `6`: extend arm 1;
  - `8`: extend arm 2;
  - `10`: extend arm 3;
  - `3`: move plate down;
  - `4`: rotate plate;
- valid outgoing non-self transition count ranges from `1` to `10`;
- valid outgoing non-self transition count mean is about `4.36`;
- invalid action count averages about `5.57` per valid state;
- valid clipped self-transition count ranges from `0` to `3`;
- support/reachability patterns among valid states:
  - `(1, 1, 1)`: `56` states;
  - `(1, 0, 1)`: `33` states;
- orientation distribution among valid states:
  - `theta=0`: `72`;
  - `theta=1`: `7`;
  - `theta=2`: `3`;
  - `theta=3`: `7`.

This supports the "needs training before solving" motivation better than the
tiny counterpoint threshold-margin story: a uniform random policy over 1000
episodes reached the goal only `21` times, a `0.021` success rate, with mean
reward about `-105.67`.

That random-policy number is not a benchmark result. It is only reconnaissance
evidence that PlateSupport is not trivially solved by unguided action choice.

### Tower-Depth Reconnaissance

A quick upstream `continuous_probe` on `plate_support_env` with `steps=20`,
`seed=0`, and `sample_size=1` showed:

- `schema_mode=default`:
  - max depth `2`;
  - scheduled assignments `84`;
  - unscheduled assignments `0`;
- `schema_mode=none`:
  - max depth `1`;
  - scheduled assignments `0`;
  - unscheduled assignments `84`.

This is useful for BBB because it gives a clean structural contrast between the
default PlateSupport schema and an explicit flat schema. It does not by itself
prove learning benefit.

### Training-Surface Reconnaissance

Tiny upstream training smoke runs did not make PlateSupport look trivial:

- `run_tower_training` for `20` episodes across five seeds produced mostly zero
  successes, with one seed reaching two successes;
- `run_exploit_explore_training` for `20` episodes across five seeds produced
  zero or one successes in the tiny probe;
- the exploit/explore smoke traces observed active tier `0` only in that tiny
  run.

These are not benchmark results. They do suggest that the later serious
evaluation should be designed carefully, with enough budget and with explicit
active-tier/tower-use diagnostics. They also suggest that the environment build
should expose training-surface availability without claiming training success.

### BBB Current Surface

BBB currently has `plate_support_env` only as an upstream smoke adapter.

The existing BBB upstream smoke runner:

- imports the upstream surface;
- creates the upstream runtime;
- resets once;
- steps once;
- optionally requests compatibility readout based on mode policy;
- records artifact/timing/linearization manifests.

That smoke runner is useful as artifact-discipline precedent. It should not be
treated as the serious PlateSupport environment family.

The new BBB environment build should therefore add a PlateSupport-specific
environment package and diagnostics rather than stretching
`run-upstream-smoke` into a benchmark.

### Decisions The Blueprint Should Preserve

Codex recommends the blueprint include these decisions unless the PO changes
them:

- Name the BBB environment package `plate_support`.
- Treat the first instance as the upstream fixed 5x5 PlateSupport problem.
- Use a descriptive instance id, likely `plate_support_5x5_default_v001`.
- Build environment-level diagnostics before any learning evaluation.
- Keep evaluation outputs out of this folder; later evaluations get their own
  design/evaluation folders.
- Reuse BBB shared artifact, timing, seed, dependency, mode, and linearization
  machinery.
- Do not copy counterpoint-specific threshold/schema-comparison machinery.
- Preserve PlateSupport-specific vocabulary:
  - plate pose;
  - support sockets;
  - engaged arms;
  - support pattern;
  - reachability pattern;
  - stability;
  - invalid moves;
  - valid clipped self-transitions;
  - direct-vs-runtime state consistency;
  - default schema vs flat schema depth.
- Include both machine-readable artifacts and human-readable environment docs.
- Record upstream dependency state and tensorization/linearization report
  metadata even for structural diagnostics.
- Expose training-surface availability, but defer training budgets and claims.
- Explicitly distinguish:
  - structural readiness;
  - tower-depth behavior;
  - training success;
  - tower benefit.

### Blueprint Readiness

Codex thinks we are ready to generate a detailed environment-build blueprint if
the PO agrees with the above scope.

The blueprint should not yet design:

- flat vs tower learning comparison;
- exploit/explore benchmark budgets;
- fiber-conditioned evaluation;
- human-readable evaluation readouts;
- a larger PlateSupport successor environment.

Those should come after BBB has a first-class PlateSupport environment surface
and environment-readiness artifacts.
