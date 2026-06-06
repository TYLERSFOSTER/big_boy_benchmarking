# Counterpoint Symbolic Environment Design Discussion

## Status

Initial design discussion for the first serious benchmark environment family in
`big_boy_benchmarking`.

This document is not an implementation blueprint.

This document is not an implementation workplan.

This document is not approval to edit benchmark code.

Its job is to externalize the current working model for the first real
environment family, grounded in:

- the existing `big_boy_benchmarking` design docs;
- read-only inspection of `/Users/foster/rl_counterpoint`;
- read-only inspection of relevant `state_collapser` counterpoint example
  docs and source;
- the Project Owner correction that the first environment should be the
  real-deal version of the `rl_counterpoint` example we keep playing with.

## Authority

The immediate Project Owner direction was:

```text
I like this idea, but we already know a lot about what we want. it is the
rl_counterpart example we keep playintg with. No we want to make the real-deal
version of it
```

followed by:

```text
That's just what we work on now
```

I interpret this as:

- the next active design target is the first serious counterpoint-derived
  environment family;
- the target is not a toy first env;
- the target is not merely the existing upstream smoke example;
- the target should preserve the real motivating structure from
  `rl_counterpoint`;
- the target should still serve `big_boy_benchmarking`'s purpose: serious,
  artifact-backed benchmarking for `state_collapser`.

## Source Set Inspected

### `big_boy_benchmarking`

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/common_failure_mode_001.md`
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`
- `docs/prime_directive/common_failure_mode_003_workplan_rewrite_during_implementation.md`
- `docs/prime_directive/consultant_tricks.md`
- `docs/prime_directive/git_practices.md`
- `docs/design/first_infrastructure_slice/01_001_initial_benchmarking_goals_discussion.md`
- `docs/design/first_infrastructure_slice/01_002_state_collapser_read_only_reconnaissance.md`
- `docs/design/first_infrastructure_slice/01_003_benchmark_system_and_artifact_contract_blueprint.md`
- `docs/design/first_infrastructure_slice/01_004_benchmark_system_artifact_contract_implementation_workplan.md`

### `/Users/foster/rl_counterpoint`

- `README.md`
- `docs/design/graph_spec_001.md`
- `docs/design/count_gn_sparsity.md`
- `docs/design/rl_attractors_and_escape_mechanisms.md`
- `docs/design/tower/README.md`
- `docs/design/tower/system_design.md`
- `docs/design/tower/mathematical_model.md`
- `docs/design/tower/training_protocol.md`
- `docs/design/tower/rollout_semantics.md`
- `docs/design/tower/artifact_checkpoint_dependencies.md`
- `rl_counterpoint/envs/counterpoint_env.py`
- `tower/state_action.py`
- `tower/graph/spec.py`
- `tower/graph/actions.py`
- `tower/graph/projection.py`
- `tower/graph/legality.py`
- `tower/graph/induced.py`
- `tower/reward/factory.py`
- `tower/train/config.py`
- `tower/train/runner.py`

### `/Users/foster/state_collapser`

- `EVALUATION.md`
- `docs/design/test_design/rl_counterpoint_v3/01_001_rl_counterpoint_v3_transformation_report.md`
- `docs/design/test_design/rl_counterpoint_v3/01_002_rl_counterpoint_v3_blueprint.md`
- `docs/engineer_continuity/2026/05/20/01_009_evaluation_family_counterpoint_and_training_surface_consolidation.md`
- `src/state_collapser/examples/rl_counterpoint_v3/env.py`
- `src/state_collapser/examples/rl_counterpoint_v3/runtime.py`
- `src/state_collapser/examples/rl_counterpoint_v3/training.py`
- `src/state_collapser/examples/rl_counterpoint_v3/__init__.py`

No files outside `big_boy_benchmarking` were edited.

## Executive Read

The first serious environment family should be:

```text
counterpoint_symbolic_v001
```

or a nearby name.

It should be the serious benchmark descendant of the `rl_counterpoint` lineage:

- ordered pitch-tuple states;
- bounded simultaneous per-voice pitch-delta actions;
- graph legality from contrapuntal constraints;
- finite-horizon episodic passage generation;
- musically meaningful terminal success;
- structured reward diagnostics;
- artifact-backed comparison across direct, empty-schema tower, and nonempty
  tower modes.

But it should not be a direct transplant of the `rl_counterpoint/tower` training
stack.

That distinction matters.

The old `rl_counterpoint` active system is already a hand-authored HRL system:

- rank 1 learns a pedal/root line;
- rank 2 learns an outer voice over the rank-1 scaffold;
- rank 3 learns an interior voice over the frozen lower scaffold;
- states project downward;
- actions assemble upward;
- lift-fiber masks restrict child search over parent actions;
- reward is rank-local;
- artifacts are lineage/checkpoint/MIDI centered.

That is exactly the intellectual source we care about. It is also exactly the
thing we must be careful not to smuggle into a `state_collapser` comparison as
if `state_collapser` discovered it unaided.

The benchmark family should therefore distinguish:

1. the **counterpoint problem**;
2. the **canonical musical projection geometry** used for diagnostics and
   optional semantic schema design;
3. the **old explicit `rl_counterpoint` tower** as a historical/reference
   baseline, if included at all;
4. the **`state_collapser` quotient/tower machinery** being evaluated.

The first environment should make that boundary explicit from the beginning.

#### PO Remark
It is important here that the `state_collapser` architecture let's us switch between the structured contractions and the random contractions very easily, jsut by switching contraction schemata. This is why I demanded it be designed that way.

#### Codex Reply:
This is the correction I needed.

I was treating "semantic schema strength" too much like a design danger to be
managed by caution. The better framing is that `state_collapser` was explicitly
designed so contraction schema is an experimental control surface. That means
the serious benchmark should not ask "is it suspicious to use structured
contractions?" in the abstract. It should define a schema family and compare:

- empty/no-contraction schema;
- random or approximately balanced schemas;
- structured counterpoint-motion schemas;
- projection-audit schemas;
- adversarial/bad schemas.

The environment's job is therefore to expose a rich enough labelled hidden
state/action graph that these schema choices can be swapped cleanly while the
underlying RL problem stays fixed. The benchmark's job is to measure whether
each schema produces the theorem-relevant properties: coverage, reward
compatibility, liftability, balanced addressability, lower path-volume, and
better learning/wall-clock outcomes.

So the old `rl_counterpoint` tower should not be treated primarily as a separate
baseline. Its conceptual content should inform the structured schema family and
projection diagnostics. Random-vs-structured-vs-bad contraction schema
comparisons are the more `state_collapser`-native version of that question.

## Core Claim Under Test

The serious benchmark claim is not:

```text
Can we generate nice counterpoint?
```

That is a valid long-term musical goal, but it is not the central benchmark
claim for this repo.

The benchmark claim is:

```text
Does quotient/tower structure help on a constrained symbolic sequence problem
whose hidden geometry is real, inspectable, and historically known to support a
hierarchical search interpretation?
```

For counterpoint, that means the benchmark should test whether tower machinery
helps when:

- the ambient state/action representation is simple and flat;
- legal trajectories occupy a sharply constrained subset;
- local move choices are coupled across voices;
- terminal success is not purely local;
- the useful hierarchy is plausible but not granted as a full hand-authored
  training program in the primary mode.

#### PO Remark
One thing that's critical here is that we design the system so that it is very easy to add reward terms as we were doing in the original `rl_counterpoint`.

#### Codex Reply:
[...]

## What We Already Know

### From `rl_counterpoint`

The real problem content is:

- states are ordered tuples of MIDI pitches;
- actions are signed per-voice movement vectors;
- graph nodes are legal chords;
- graph edges are legal voiceleadings;
- reward depends on current transition plus recent passage context;
- finite-horizon generation matters;
- metrical position matters;
- cadence-like terminal success matters;
- musical constraints provide a dense source of hidden geometry.

The real HRL insight is:

- one-voice voiceleading is part of two-voice voiceleading;
- two-voice voiceleading is part of three-voice voiceleading;
- higher-rank validity should project to lower-rank validity;
- parent action choice constrains child lift-fiber search;
- effective search burden should drop when the hierarchy is used well.

The real engineering artifacts are:

- rank-local training;
- frozen parent policies;
- lift-fiber masks;
- reward diagnostics;
- checkpoint lineages;
- MIDI examples.

### From `state_collapser`

The current upstream `rl_counterpoint_v3` example already rebuilt a simplified
counterpoint problem in package-appropriate form:

- `RlCounterpointState`
  - `bass_pitch`
  - `inner_pitch`
  - `upper_pitch`
  - `beat_index`
- `RlCounterpointGraphSpec`
  - pitch bounds
  - measure size
  - max steps
  - max step size
  - interval-class rules
  - forbidden parallel interval classes
  - max outer span
- flat three-voice state/action surface;
- `TowerRuntime` integration;
- default and semantic contraction schemas;
- minimal tabular tower-aware training.

That example is valuable, but by itself it is still a package example / smoke
surface. It is not the serious benchmark environment family this repo should
ultimately own.

#### PO Remark
It is important to realize that this little smoker version is probably closer to the actual design we want, as opposed to the original `rl_counterpart`. It's the scale/seriousness aht we want to take all the way.

#### Codex Reply:
[...]

### From `big_boy_benchmarking`

The benchmark system blueprint already decided:

- `big_boy_benchmarking` is the serious evidence repo;
- upstream `state_collapser` should be read/run/imported/pinned, not edited;
- direct environment training, empty-schema tower machinery, and nonempty-schema
  tower machinery must remain distinct;
- structural, behavioral, and performance evidence must all be recorded;
- compatibility readouts must not become default hot-path metrics;
- the first serious environment track should be counterpoint-like symbolic;
- human-facing environment/experiment/result/method docs should exist alongside
  machine-readable artifacts.

## Design Center

The design center should be:

```text
A parameterized flat counterpoint environment family whose primary serious
instances are three-voice and possibly four-voice constrained symbolic
voiceleading tasks, with canonical projection geometry available for audit,
schemas, and reference comparisons, but not silently injected into every
learner condition.
```

This gives us the actual thing the Project Owner cares about while preserving
benchmark validity.

## What "Real-Deal Version" Should Mean

The phrase "real-deal version" should not mean:

- port every old `rl_counterpoint` module;
- import the transformer training stack;
- rebuild the entire explicit rank tower as the primary benchmark;
- chase complete TC21M reward formalization before the environment can run.

It should mean:

- serious enough graph geometry that structural metrics matter;
- serious enough reward/terminal behavior that learning is not fake;
- serious enough scale ladder that tiny success is not the whole story;
- serious enough artifact contract that results survive inspection;
- serious enough baselines that any positive result is not a gift;
- serious enough musical examples that a human can listen/inspect, even if
  musical quality is not the main quantitative claim yet.

## Proposed Environment Family

### Family Id

Recommended:

```text
counterpoint_symbolic_v001
```

Alternative names:

```text
counterpoint_voiceleading_v001
rl_counterpoint_real_v001
counterpoint_tower_geometry_v001
```

My preference is `counterpoint_symbolic_v001` because it says what the domain is
without overclaiming the mechanism.

### Family Role

This is the first serious symbolic constrained sequence benchmark family.

It should be the counterpart to future physical/geometric families such as:

- dual-arm/shared-object coordination;
- loop closure;
- cable/support coupling;
- singularity/bottleneck geometry.

### Primary Hypothesis

Counterpoint has hidden constraint geometry that should be friendly to
quotient/tower structure because:

- the legal state set is a sparse subset of a simple pitch product;
- the legal edge set is a sparse subset of a simple action lattice;
- constraints factor partly by voice, interval, direction, and metrical role;
- local edge families create repeated structural motifs;
- canonical coordinate projections reveal real lower-rank compatibility;
- terminal success requires coordinated voices rather than independent per-voice
  optimization.

### Main Benchmark Risk

The benchmark can become circular if semantic schemas or controller modes encode
too much of the old hand-authored musical hierarchy.

The environment should have hidden structure. The benchmark mode should be
honest about whether that structure is discovered, supplied as labels, used only
for diagnostics, or used directly for control.

## Relationship To Existing `state_collapser` `rl_counterpoint_v3`

The existing upstream example is a good seed and reality-binding reference.

It should probably be treated as:

```text
upstream_counterpoint_smoke_v3
```

not as:

```text
the final serious benchmark environment
```

The serious `big_boy_benchmarking` version should decide whether to:

1. import and wrap upstream `rl_counterpoint_v3` for smoke only;
2. define a local benchmark-owned environment family that is conceptually
   descended from it;
3. support both, with names that prevent confusion.

My current recommendation is:

- keep upstream `rl_counterpoint_v3` as smoke/reference;
- design `counterpoint_symbolic_v001` in this repo as the serious family;
- implement it later only after the environment blueprint and workplan are
  approved.

Reason:

- this repo needs artifact schemas, scale ladders, result docs, and benchmark
  controls that are not the job of upstream examples;
- we do not want to mutate upstream while doing serious benchmark design;
- benchmark-owned naming prevents confusing a small example with a serious
  claim.

#### PO Remark
"define a local benchmark-owned environment family that is conceptually
   descended from it"

#### Codex Reply:
[...]

## State Design

### First Serious State Shape

The first serious state should stay flat:

```text
(p_0, p_1, p_2, beat_index)
```

where:

- `p_0` is bass/lower voice;
- `p_1` is inner voice;
- `p_2` is upper voice;
- `beat_index` is the within-measure position.

For a future four-voice scale:

```text
(p_0, p_1, p_2, p_3, beat_index)
```

The state should not include:

- explicit rank labels;
- parent scaffold ids;
- old `rl_counterpoint/tower` policy state;
- checkpoint lineage information;
- derived observation tensors.

### Episode Context

Episode context may include:

- step index;
- max steps;
- history window;
- measure size;
- cadence deadline;
- terminal target family;
- optional phrase form id;
- reset/start-state provenance.

Question:

- should history be part of the Markov state, or should the environment expose a
  small non-Markov reward context and treat the hidden graph as pitch+beat only?

This matters because `state_collapser` is graph-oriented. If reward depends on
history that is not represented in state, then the transition graph is still
well-defined but the reward process is partially history-dependent. That may be
acceptable, but it must be explicit.

#### PO Response:
Initially only local, no dependence on history.

#### Codex Reply:
[...]

### Candidate State Invariants

First serious invariants:

- all pitches lie in configured MIDI band;
- voices are strictly ordered;
- adjacent intervals lie in allowed sets;
- outer interval lies in allowed set;
- outer span is below a scale-tier cap;
- bass/root pitch class lies in allowed pitch-class family;
- beat index is valid.

Possible later invariants:

- register-specific voice ranges;
- melodic tendency constraints encoded as state annotations;
- phrase-position class beyond beat index;
- cadence-stage marker.

#### PO Response:
I support this.

#### Codex Reply:
[...]

## Action Design

### Primitive Action Shape

For three voices:

```text
(delta_0, delta_1, delta_2)
```

For `n` voices:

```text
(delta_0, ..., delta_{n-1})
```

Each coordinate lies in:

```text
[-max_step_size, max_step_size]
```

and the all-zero action is excluded.

### Why This Is Correct

This is one of the strongest ideas preserved from `rl_counterpoint`:

- the action lattice is simple;
- the legality surface is hidden;
- the hard part is finding valid and rewarding coupled transitions.

### Action Decoding

The action applies coordinatewise:

```text
p'_i = p_i + delta_i
```

and advances beat:

```text
beat_index' = (beat_index + 1) mod measure_size
```

The edge predicate decides whether the candidate transition is legal.

### Invalid Action Semantics

Potential policies:

1. reject invalid actions by action mask;
2. allow invalid actions but self-loop with penalty;
3. terminate on invalid action;
4. separate modes for masked and unmasked baselines.

My current recommendation:

- benchmark modes should record whether masks are available to the learner;
- primary fair modes should use the same mask access policy across direct and
  tower conditions;
- at least one diagnostic mode should measure invalid-action pressure without
  hiding it.

## Graph Legality

### Node Legality

Node legality should include:

- pitch range;
- strict voice order;
- adjacent interval classes;
- outer interval class;
- max outer span;
- root pitch-class family;
- beat-index validity.

### Edge Legality

Edge legality should include:

- source is node-valid;
- target is node-valid;
- action is not all zero;
- per-voice motion is bounded;
- no voice crossing by transition;
- no forbidden parallel perfect intervals;
- optional stationary-voice policy;
- optional inner-voice leap guard;
- optional contrary/oblique/parallel motion labels.

### Legality Versions

The serious environment should version its legality contract:

```text
counterpoint_symbolic.legality.v001
```

This is important because a small change to allowed intervals or forbidden
motion rules can completely change graph density and benchmark difficulty.

#### PO Response:
Correct.

#### Codex Reply:
[...]

## Reward Design

### Reward Goal

The reward should be musically meaningful enough that learning is real, but
small enough that the benchmark does not become "debug all of counterpoint."

### First Reward Families

Recommended first reward terms:

- per-step cost;
- terminal cadence reward;
- adjacent consonance bonus;
- outer consonance bonus;
- downbeat stability bonus;
- melodic smoothness penalty;
- repeated-state or narrow-cycle penalty;
- optional diversity/novelty diagnostic, probably not in primary reward yet.

### Reward Diagnostics

Each transition reward should produce structured diagnostics:

```text
step_cost
terminal_bonus
adjacent_consonance_bonus
outer_consonance_bonus
downbeat_bonus
smoothness_penalty
cycle_penalty
hard_violation
terminal_success
```

For real benchmark artifacts, reward breakdowns are not decoration. They are how
we tell whether a learner is exploiting a malformed reward.

### TC21M Boundary

The `rl_counterpoint` repo treats TC21M as a strong source for reward
vocabulary. The serious benchmark should use that heritage, but it should not
block first environment design on complete TC21M formalization.

Recommended policy:

- `v001` uses a narrow TC21M-inspired reward slice;
- every reward term is named and logged;
- future reward bundles get explicit ids rather than silently replacing the
  meaning of `v001`.

## Terminal Success

Terminal success should be a direct three-voice condition in the primary
environment.

Candidate condition:

- terminal beat or final phrase slot;
- bass/root resolves to tonic pitch class;
- outer interval is a configured terminal consonance;
- inner voice lies in a configured terminal interval from bass;
- final state is node-valid;
- optional recent-window cadence approach condition.

Important:

Terminal success should not be defined as:

```text
rank1 success AND rank2 success AND rank3 success
```

inside the primary flat environment. That would reimport the old explicit
rank-tower decomposition.

But the benchmark may compute projection-based success diagnostics offline.

## Scale Ladder

### Tiny

Purpose:

- exact enumeration;
- hand inspection;
- structural diagnostic validation;
- artifact schema debugging.

Candidate:

```text
voices: 3
pitch band: narrow, maybe 48..60 or 48..64
max_step_size: 1
measure_size: 4
max_steps: 8
reward: narrow v001
```

### Small

Purpose:

- first real learning smoke;
- exact or near-exact structural metrics;
- multi-seed sanity.

Candidate:

```text
voices: 3
pitch band: 48..72
max_step_size: 2
measure_size: 4
max_steps: 16
```

### Medium

Purpose:

- first serious benchmark matrix;
- structural diagnostics sampled or periodic;
- enough branching for tower overhead/training tradeoff to matter.

Candidate:

```text
voices: 3
pitch band: 45..84
max_step_size: 2 or 3
measure_size: 4
max_steps: 24 or 32
```

### Large

Purpose:

- scaling pressure;
- wall-clock and artifact pressure;
- possible four-voice transition.

Candidate:

```text
voices: 4
pitch band: wider
max_step_size: 2
measure_size: 4
max_steps: 32
```

### Stress

Purpose:

- not for claims at first;
- push runtime, logging, and diagnostics;
- expose readout-cost regressions.

Candidate:

```text
voices: 4 or 5
broader pitch band
sampled diagnostics only
```

## Benchmark Modes

The environment family should be evaluated in the accepted mode vocabulary:

### `direct_env_tabular`

Direct baseline:

- no tower runtime in decision path;
- same environment;
- same mask policy if masks are allowed;
- tabular or simple baseline learner.

### `tower_empty_schema_tabular`

Tower shell baseline:

- `state_collapser` runtime active;
- empty/no-contraction schema;
- measures overhead and training surface differences without useful quotienting.

### `tower_nonempty_schema_tabular`

First full tower condition:

- nonempty schema;
- no expensive readout on hot path;
- structural/behavioral diagnostics recorded under explicit profiles.

### `tower_exploit_explore`

Possible later condition:

- active-tier control;
- likely not first serious counterpoint mode unless controller semantics are
  clearly adapted.

### `tower_fiber_conditioned_stage`

Possible later condition:

- path-fiber/lift-candidate stage surface;
- conceptually close to counterpoint lift-fiber search;
- should be designed carefully before use as a primary result mode.

### Optional Historical Reference: `rl_counterpoint_explicit_tower`

This would not be a `state_collapser` mode.

It would be a historical/reference comparison against the old hand-authored HRL
tower from `/Users/foster/rl_counterpoint`.

Potential value:

- shows what a human-authored hierarchy can do;
- anchors the Project Owner's original intuition;
- gives qualitative MIDI artifacts and lineage examples.

Risk:

- different training stack;
- hard to compare fairly;
- could confuse the central `state_collapser` claim.

My recommendation:

- reserve this as a reference/appendix mode, not a primary benchmark condition.

## Schema Design

### Empty Schema

Required baseline:

```text
schema_id: empty_v001
```

Purpose:

- tower machinery with no contraction;
- controls for runtime shell overhead.

### Smoke Schema

Possible:

```text
schema_id: counterpoint_smoke_motion_v001
```

Labels:

- any voice motion;
- beat advance;
- transition family.

Purpose:

- prove assignments schedule;
- prove tower depth can become nontrivial;
- not a scientific schema.

### Semantic Schema

Possible:

```text
schema_id: counterpoint_voice_motion_semantic_v001
```

Potential labels:

- bass motion;
- inner motion;
- upper motion;
- stepwise motion;
- leap motion;
- contrary direction;
- oblique motion;
- parallel direction;
- terminal-cadence approach;
- stable downbeat sonority.

Risk:

- if labels encode too much of the solution, the comparison becomes too easy.

### Projection-Audit Schema

Possible diagnostic-only schema:

```text
schema_id: counterpoint_projection_audit_v001
```

Purpose:

- compare induced tower behavior to canonical musical projections;
- not used as primary online learner input unless explicitly named.

### Bad / Negative Schema

Possible:

```text
schema_id: counterpoint_bad_random_motion_v001
```

Purpose:

- show that arbitrary compression does not always help;
- protect against self-confirming benchmark design.

## Canonical Projection Geometry

The old `rl_counterpoint` tower gives us canonical projections:

- three voices to two voices by removing an interior coordinate;
- two voices to one voice by removing the upper coordinate;
- actions project analogously;
- higher-rank valid edges should project to lower-rank valid edges.

This geometry is real and important.

For `big_boy_benchmarking`, it should initially be used in four ways:

1. environment-family explanation;
2. structural diagnostics;
3. optional semantic schema design;
4. reference comparison against hand-authored tower behavior.

It should not be silently treated as the primary mode's built-in control policy.

## Metrics

### Structural Metrics

Required early metrics:

- ambient state count;
- valid state count;
- valid/ambient ratio;
- ambient action count;
- mean legal action count;
- action-mask density;
- valid edge count where exact enumeration is possible;
- connected component count where feasible;
- goal-state count;
- reachable goal-state count;
- shortest path to goal where feasible;
- projection compatibility rate;
- lift-fiber size distribution;
- quotient compression ratios;
- tower depth curve;
- schema assignment counts.

### Behavioral Metrics

Required once tower modes run:

- active tower depth over time;
- tier occupancy if active-tier control is used;
- schema block occupancy;
- lift success/failure rates;
- empty-fiber events;
- invalid action attempts;
- terminal approach patterns;
- reward-term breakdown over time;
- readout call counts under readout discipline tests.

### Performance Metrics

Required for first serious learning claims:

- success rate over seeds;
- episode return;
- steps to success;
- sample efficiency to threshold;
- variance across seeds;
- wall-clock time;
- online time segments;
- artifact logging time;
- memory/artifact size;
- invalid action rate;
- terminal failure modes.

### Musical / Qualitative Metrics

Useful but secondary:

- generated MIDI examples;
- interval histograms;
- motion-family histograms;
- cadence examples;
- repeated-cycle reports;
- simple diversity scores.

These should not replace success/structural/performance evidence.

## Artifact Expectations

The first serious counterpoint benchmark should emit:

```text
manifest.json
environment_manifest.json
dependency_manifest.json
benchmark_matrix.json
seed_bundle.json
mode_contract.json
episode_results.csv
step_events.jsonl or csv
reward_breakdown.csv
structural_diagnostics.jsonl
tower_depth.csv
schema_assignments.csv
timing.csv
summary.json
summary.md
examples/
  example_episode_*.mid
  example_episode_*.json
```

The MIDI files are not proof of benchmark success. They are qualitative
inspection artifacts.

## Human-Facing Docs

When the infrastructure layer exists, the counterpoint family should have:

```text
docs/environments/counterpoint_symbolic_v001.md
docs/experiments/<run_family>_counterpoint_*.md
docs/results/<run_family>_summary.md
docs/methods/counterpoint_metrics.md
```

Until that layer exists, design should stay under:

```text
docs/design/first_counterpoint_environment/
```

## Design Risks

### Risk 1: Circular Hierarchy

If the benchmark gives the tower condition the old `rl_counterpoint` rank
decomposition as a built-in mechanism, the result may no longer test
`state_collapser`.

Mitigation:

- primary modes stay flat at the environment surface;
- projection geometry is logged and optionally used by explicitly named schema
  variants;
- old explicit tower is a reference condition only.

### Risk 2: Toy Reward

If reward is too weak, the benchmark becomes graph traversal with music-flavored
names.

Mitigation:

- use a narrow but real terminal/cadence/consonance reward;
- log reward breakdowns;
- include qualitative examples.

### Risk 3: Musical Completeness Trap

If reward/legality tries to encode all of counterpoint before any benchmark can
run, the project stalls.

Mitigation:

- version legality and reward contracts;
- start with v001;
- make future musical refinements explicit new contracts.

### Risk 4: Scale Confusion

Tiny exact enumeration can look successful while medium learning fails.

Mitigation:

- define scale tiers before claims;
- never use tiny alone for performance claims.

### Risk 5: Readout Cost Regression

Counterpoint structural diagnostics are tempting and potentially expensive.

Mitigation:

- classify diagnostics as online counters, periodic diagnostics, or post-hoc
  expensive readouts;
- preserve synthetic-Blow hot-path discipline.

### Risk 6: Upstream Mutation

This repo exists partly to stop benchmark work from turning into casual upstream
package hacking.

Mitigation:

- read/run/import/pin upstream;
- do not edit `/Users/foster/state_collapser` or `/Users/foster/rl_counterpoint`
  during this design work;
- if upstream defects are found, emit repros and issue-style notes.

## Turn Question 1: Environment Ownership

Should the serious environment implementation eventually live primarily in
`big_boy_benchmarking`, with upstream `state_collapser` examples treated as
smoke/reference inputs?

Recommendation:

Yes. The serious benchmark family should be benchmark-owned, while still
pinning and importing upstream `state_collapser`.

### PO Answer Slot

```text
My thinking is we do all work in `big_boy_benchmarking`. When all this work is completely done, and we're ready to do alpha release of `state_collapser`, we'll bring `big_boy_benchmarking` into `state_collapser` as a submodule. However, this will happen at the very end, so all our work should not depend on it.
```

### Codex Follow-Up Slot

```text
Accepted. All substantive work stays in `big_boy_benchmarking` until the
benchmark program is complete enough to support `state_collapser` alpha release.
The future submodule plan is a release-integration destination, not a current
design dependency.

Immediate implication: environment docs, benchmark artifacts, result summaries,
and implementation should be benchmark-repo-owned. Every run should record the
pinned `state_collapser` dependency version/commit/path, but no design should
assume `big_boy_benchmarking` already lives inside `state_collapser`.
```

## Turn Question 2: First Scope

Should `counterpoint_symbolic_v001` begin as three-voice flat only, or should
the first serious family include both three-voice and four-voice instances?

Recommendation:

Start with three-voice as the primary first scope, but design the spec so that
four-voice can become the first large/stress tier without changing the family
identity.

### PO Answer Slot

```text
It should be designed so that this is a stupid question.
```

### Codex Follow-Up Slot

```text
Correct. My question was badly shaped.

The serious family should be parameterized so "three voice or four voice" is an
instance/scale choice, not a family-design fork. The family contract should make
voice count, pitch band, horizon, measure size, max step size, legality version,
reward version, and schema family explicit instance parameters.

We may still instantiate a first tiny/small smoke case with `voice_count = 3`,
because implementation and validation need a first concrete fixture. But the
blueprint should not encode "three-voice flat only" as the conceptual boundary.
It should define the `n`-voice counterpoint state/action graph family, with
three voice and four voice examples as scale tiers inside the same family.
```

## Turn Question 3: History In State

Should recent passage history be part of the explicit environment state, or only
part of reward/diagnostic context?

Recommendation:

For `v001`, keep explicit graph state as pitch tuple plus beat index. Keep
history in episode context and document that any history-sensitive reward is not
purely Markov with respect to the exposed graph state. If this becomes a problem
for `state_collapser`, create a `v002` state contract with compact history
included.

### PO Answer Slot

```text
Did I answer this in comments way above?
```

### Codex Follow-Up Slot

```text
Partially, yes. Your schema remark above corrects the larger frame, and
`logHRL.tex` adds the precise rule I should have centered: rewards must be
action-local after any necessary state augmentation, while histories are paths
in the hidden state/action graph.

So the right question is not "history in state or not?" as a taste choice. The
right benchmark-design obligation is:

- define the base hidden state/action graph;
- define the finite path set or horizon being measured;
- if the reward needs recent context, either augment state enough to make the
  reward action-local, or explicitly treat the object as a reward-labelled path
  problem and record that in the environment contract.

For the first blueprint, I should replace this question with an action-locality
contract: identify the smallest finite context needed for reward descent and
path-volume diagnostics. Beat index clearly belongs in state. Recent cadence
window/history may belong either in state augmentation or in the path-labelled
reward contract, but it cannot remain an informal side channel.
```

## Turn Question 4: Mask Policy

Should primary learner modes receive legal action masks?

Recommendation:

Yes, if every primary mode receives the same mask access. Also include at least
one diagnostic unmasked or invalid-action-pressure condition so the benchmark
does not hide how sparse the legal action space is.

### PO Answer Slot

```text
Yes.
```

### Codex Follow-Up Slot

```text
Accepted. Primary comparable modes should receive masks under the same access
rules.

Benchmark implication: action-mask availability becomes part of the mode
contract, and action-mask density becomes a structural metric. We can still keep
an invalid-action-pressure diagnostic mode if useful, but the main comparison
should not make one mode learn the legality surface while another mode receives
it for free.
```

## Turn Question 5: Old Explicit Tower Reference

Should the old `/Users/foster/rl_counterpoint/tower` hand-authored HRL training
stack be included as an optional historical/reference baseline?

Recommendation:

Yes eventually, but not in the primary first claim. It should be labeled
explicitly as a hand-authored hierarchy reference, not as a `state_collapser`
condition.

### PO Answer Slot

```text
I think my comment about different contraction schema answers this.
```

### Codex Follow-Up Slot

```text
Yes. Your contraction-schema comment answers it and changes my framing.

The old explicit `rl_counterpoint/tower` stack should not be a primary
benchmark baseline by default. The `state_collapser`-native move is to express
the relevant structured hierarchy pressure through contraction schemata and
projection diagnostics, then compare those schemata against empty, random,
balanced, and bad/adversarial schemata on the same environment.

If the old tower training stack appears later, it should be an explicitly
labelled historical/reference artifact, not one of the central
`state_collapser` comparison modes.
```

## Turn Question 6: Semantic Schema Strength

How much musical structure may the first nonempty schema encode?

Options:

1. weak motion labels only;
2. voice-role and motion-family labels;
3. cadence/terminal-approach labels;
4. explicit projection-derived labels.

Recommendation:

Use voice-role and motion-family labels for the first semantic schema. Keep
cadence labels and explicit projection-derived labels as diagnostic or later
schema variants, because they may encode too much of the intended solution.

### PO Answer Slot

```text
idk
```

### Codex Follow-Up Slot

```text
Fair. This should not have been posed as a one-shot PO intuition question.

The benchmark should make schema strength an experimental axis:

- `empty_v001`: no contractions;
- `random_balanced_v001`: random or approximately balanced contractions;
- `counterpoint_motion_v001`: structured motion/voice-role labels;
- `counterpoint_projection_audit_v001`: projection-informed diagnostic schema;
- `counterpoint_bad_v001`: intentionally poor or misleading contractions.

Then the evidence decides which schema family satisfies the logHRL hypotheses.
The important thing is not guessing the perfect "semantic strength" now. The
important thing is that every schema has a stable id, a written contract, and
metrics for compression, lift fibers, reward variance inside fibers, lift
success, and learning impact.
```

## Turn Question 7: Reward Completeness

How musically ambitious should reward v001 be?

Recommendation:

V001 should be narrow but real: terminal cadence, consonance/stability,
smoothness, and cycle avoidance. TC21M-derived richness should be versioned into
later reward bundles.

### PO Answer Slot

```text
I want to stop answering these I think your questions sort of show you don't totally get the point. Please look over `state_collapser` environments again, and the `logHRL.tex` paper. I just think you're losing the big picture a bit.
```

### Codex Follow-Up Slot

```text
Agreed. I was losing the big picture here.

This question over-focused on musical reward completeness. The benchmark point
from `logHRL.tex` is not "how complete is the counterpoint reward?" The point is
whether the environment gives us a finite hidden state/action graph and
reward-labelled path set where tower contraction can be evaluated against the
theorem's measurable hypotheses.

After re-reading the `state_collapser` environment strategy, post-Young audit,
and `logHRL.tex`, the design center should be corrected as follows:

- the counterpoint environment is a parameterized hidden state/action graph
  family with path-volume explosion;
- contraction schema is the core experimental knob;
- structured, random, empty, and bad schemata must be swappable on the same
  underlying problem;
- reward design matters mainly because reward descent/direct-image aggregation
  and reward variance inside quotient fibers are theorem-relevant diagnostics;
- the first blueprint should center path-volume, quotient addresses, lift
  fibers, reward compatibility, balanced addressability, and wall-clock/sample
  efficiency.

So I should retire this reward-completeness question and replace it with a
reward-locality/direct-image-reward contract in the blueprint.
```

## Turn Question 8: Qualitative Artifacts

Should MIDI examples be required artifacts for serious counterpoint runs?

Recommendation:

Yes, for any run family that makes a serious counterpoint claim. MIDI examples
should be qualitative inspection artifacts, not primary metrics.

### PO Answer Slot

```text
I think all design docs clarify this somewhere, even parent design docs or parent folder design docs
```

### Codex Follow-Up Slot

```text

```

## Turn Question 9: First Blueprint Boundary

Should the next document be a full environment-family blueprint for
`counterpoint_symbolic_v001`, or another discussion pass focused only on the
old-tower/reference-baseline boundary?

Recommendation:

Proceed to a full environment-family blueprint after this discussion pass, but
make the old explicit tower boundary one of the blueprint's central sections.

### PO Answer Slot

```text
full environment-family blueprint after this discussion pass
```

### Codex Follow-Up Slot

```text

```

## Correction After PO Reply Pass

The PO reply pass exposed a real misalignment in this document.

The earlier framing made the counterpoint environment sound too much like a
domain-design problem:

```text
Which voice count?
How much reward completeness?
How strong a semantic schema?
Do we include the old tower?
```

Those questions are not the right center of gravity.

The correct center of gravity, after re-reading the `state_collapser`
environment strategy, the post-Young evaluation audit, and `logHRL.tex`, is:

```text
Design a parameterized hidden state/action graph family whose finite-horizon
path space is large, whose legal paths are structured, and whose contraction
schemata can be swapped cleanly so that the logHRL theorem's measurable
hypotheses can be tested.
```

That means the first blueprint should be organized around:

- the `n`-voice counterpoint state/action graph family;
- finite-horizon path-volume and policy-effective path-volume;
- contraction schema families as first-class experimental arms;
- structured/random/empty/bad schema comparison on the same underlying problem;
- reward action-locality after necessary state augmentation;
- direct-image reward aggregation on action cells;
- lift-fiber size, entropy, and lift success;
- reward variance inside quotient fibers;
- quotient compression ratios;
- wall-clock and sample-efficiency comparisons against non-tower baselines.

The old `rl_counterpoint` tower remains important because it explains why
counterpoint is the right domain and suggests structured contractions/projection
diagnostics. But the primary benchmark object is the `state_collapser`
schema-driven quotient tower, not a hand-authored rank curriculum.

So the next blueprint should not merely be:

```text
counterpoint environment spec
```

It should be:

```text
counterpoint hidden-graph and contraction-schema benchmark blueprint
```

## Current Working Conclusion

We are now at the environment-design juncture.

The right first environment is not a generic toy and not just upstream
`rl_counterpoint_v3` smoke.

The right first environment is a serious benchmark-owned, parameterized
counterpoint hidden state/action graph family, descended from the old
`rl_counterpoint` problem and informed by its explicit tower insight.

The benchmark object is the family plus its contraction-schema arms.

The central design discipline is:

```text
Keep the underlying RL problem fixed. Vary contraction schemata and tower modes
explicitly. Measure the logHRL hypotheses rather than relying on domain-specific
intuition that hierarchy ought to help.
```
