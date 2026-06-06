# 01.002 Counterpoint Hidden Graph and Contraction Schema Benchmark Blueprint

## Status

Draft blueprint for the first serious benchmark environment family in `big_boy_benchmarking`.

This is not an implementation workplan.

This document specifies the intended environment family, schema families, benchmark modes, diagnostics, artifacts, and remaining PO questions. A later implementation workplan must translate this into Phase.Stage.Action execution steps before code is written.

## Intended Reader

This document is directed to Codex and the PO.

Codex should treat it as the working design contract for the first counterpoint benchmark family unless superseded by a later design or implementation workplan.

## Source Corpus

This blueprint follows:

- `docs/design/first_infrastructure_slice/01_001_initial_benchmarking_goals_discussion.md`
- `docs/design/first_infrastructure_slice/01_002_state_collapser_read_only_reconnaissance.md`
- `docs/design/first_infrastructure_slice/01_003_benchmark_system_and_artifact_contract_blueprint.md`
- `docs/design/first_infrastructure_slice/01_004_benchmark_system_artifact_contract_implementation_workplan.md`
- `docs/design/first_counterpoint_environment/01_001_counterpoint_environment_design_discussion.md`
- Read-only inspection of `/Users/foster/state_collapser/docs`
- Read-only inspection of root `*.md` docs in `/Users/foster/state_collapser`
- Read-only inspection of the existing `state_collapser` counterpoint smoker shape
- Read-only memory of the old `rl_counterpoint` tower/projection discussions, without treating that old code as the primary baseline

## Prime Directive Alignment

This document follows the present repo discipline:

- Design first.
- Blueprint before workplan.
- Workplan before implementation.
- `big_boy_benchmarking` owns substantive benchmark work.
- `state_collapser` is read-only during this work unless explicitly authorized otherwise.
- Existing upstream examples are reality-binding smoke surfaces, not serious evidence.
- Benchmark evidence must be artifact-first, reproducible, mode-scoped, and neutral.
- The benchmark must test the actual logHRL/state-collapser claim, not merely produce pleasant toy examples.

## Executive Verdict

We are ready to blueprint the first serious environment family.

The first environment should not be framed merely as "a counterpoint environment." It should be framed as:

> A benchmark-owned, parameterized hidden state/action graph family whose path space resembles symbolic counterpoint, and whose central experimental control is the contraction schema used by `state_collapser`.

The environment is the fixed RL problem.

The contraction schema is the experimental knob.

The benchmark question is not only whether an agent can produce locally plausible counterpoint-like sequences. The benchmark question is whether nontrivial quotient/tower structure reduces the effective search problem in ways predicted by the logHRL design:

- lower policy-effective path volume,
- useful quotient addresses,
- manageable lift fibers,
- stable reward direct-images,
- improved lift success,
- lower sample or wall-clock cost at matched task definition,
- and clear failure when the schema is bad.

## Core Design Correction

The PO corrected an important early drift:

The point is not to copy the old `rl_counterpoint` training stack into this repo.

The point is to build a serious benchmark-owned environment family, conceptually descended from the small `state_collapser` `rl_counterpoint_v3` smoker, scaled and instrumented until it can serve as a real benchmark.

Old `rl_counterpoint` remains useful as conceptual memory:

- it showed that additive reward terms matter,
- it showed that qualitative musical artifacts can help sanity-check behavior,
- it supplied intuitions about projections between voices,
- and it motivated the idea that counterpoint has massive combinatorial path volume.

But the benchmark should be built around the present `state_collapser` idea:

- finite hidden graph,
- state/action partitions,
- contraction schemas,
- quotient towers,
- lift fibers,
- path-volume diagnostics,
- reward compatibility,
- and controlled comparisons across schemas.

## Non-Goals

This first blueprint does not authorize:

- editing `/Users/foster/state_collapser`,
- importing the old `rl_counterpoint` implementation as the benchmark core,
- implementing a full music-theory engine,
- relying on human-listenable MIDI as primary evidence,
- claiming musical quality as the benchmark objective,
- hand-tuning a single hierarchy until it looks good,
- benchmarking only one tower mode,
- or treating upstream smoke examples as sufficient evidence.

## Accepted Decisions

### Repository Ownership

All substantive benchmark work belongs in `big_boy_benchmarking`.

At some future alpha-release point, the PO may bring `big_boy_benchmarking` into `state_collapser` as a submodule. That is out of scope for the present design. Current code and documents must not depend on that future integration.

### First Environment Family

The first serious environment family is counterpoint-like symbolic sequence construction.

It must be benchmark-owned and parameterized.

It must be capable of producing hidden state/action graphs at multiple scales.

It must be suitable for direct-env baselines, empty-schema tower modes, nonempty structured schema modes, random schema controls, and bad/adversarial schema controls.

### Voice Count

The family is `n`-voice by design.

Three voice versus four voice must be an instance parameter, not a conceptual fork. A first smoke fixture may be three voice because it is easier to enumerate and inspect, but the environment contract must not bake in three voices.

### History

The first version is local and action-local.

No path history is part of the initial reward contract.

If future reward terms require context, the benchmark must either:

- augment the explicit state with the required context, or
- introduce a clearly versioned path-labelled reward contract.

It must not silently smuggle history into reward computation while claiming a local Markov graph.

### Action Masks

Primary comparable benchmark modes use legal action masks under the same access rules.

Action-mask availability is part of the mode contract.

Mask density is a required structural metric.

Unmasked invalid-action pressure may be added later as a diagnostic stress mode, but it is not the primary first comparison.

### Reward Extensibility

The environment must make it easy to add, remove, version, and inspect reward terms.

This is a design requirement, not an implementation nicety.

The old `rl_counterpoint` work made clear that reward design evolves. The benchmark must support that evolution without turning each reward change into a bespoke environment fork.

### Schema as Experimental Control

The contraction schema is the central experiment-control surface.

The same underlying environment instance must be runnable with:

- no contraction,
- empty schema,
- random balanced schema,
- random bad or adversarial schema,
- structured counterpoint-motion schema,
- and projection-audit schema.

The benchmark should ask which schemas create useful quotient/tower structure, not simply whether "the tower" helps.

### MIDI and Qualitative Artifacts

MIDI or symbolic example outputs can be useful qualitative artifacts.

They are not primary evidence.

They must not displace machine-readable diagnostics about path volume, compression, fibers, reward compatibility, lift success, timing, and learning curves.

## Central Benchmark Question

Given a fixed symbolic counterpoint hidden graph, do schema-induced quotient towers produce useful RL structure?

"Useful" means:

- the tower reduces policy-effective search volume,
- quotient cells produce coherent coarse decisions,
- lift fibers are not pathological,
- reward variance inside quotient fibers is controlled,
- lifted coarse choices can be resolved into valid fine actions,
- controller or learner performance improves relative to direct baselines,
- overhead is measured honestly,
- and bad schemas visibly fail.

## What This Benchmark Must Prove or Disprove

The benchmark should be capable of supporting neutral conclusions such as:

- Structured counterpoint-motion schemas help on some scales but not others.
- Random balanced schemas compress but do not preserve reward.
- Empty-schema tower overhead is measurable and sometimes not worth paying.
- Bad schemas increase reward variance inside quotient fibers and hurt liftability.
- Direct tabular learning remains stronger on tiny instances.
- Tower modes become competitive only once path volume crosses a scale threshold.
- Projection-inspired schemas help only when their induced fibers are balanced enough.

Negative results are acceptable.

Vague positive claims are not.

## Relationship to logHRL Concepts

The benchmark must bind each logHRL concept to concrete artifacts.

| logHRL concept | Benchmark interpretation | Required evidence |
| --- | --- | --- |
| Finite hidden graph | Explicit reachable state/action graph for a counterpoint instance | Environment manifest, graph summary, reachability stats |
| Flat path volume | Number or estimate of valid action paths through the environment | `path_volume_summary.json`, exact tiny counts, sampled larger counts |
| Policy-effective path volume | Number or estimate of paths plausibly explored by a learner or policy family | Policy-sampled path statistics, coverage artifacts |
| Partition tower | Nested quotient of states/actions induced by schema | Schema manifest, quotient size table |
| Path address | Coarse-to-fine address of a path through quotient tower | Address diagnostics, sampled address traces |
| Lift fiber | Set of fine states/actions under a quotient address or coarse choice | Lift-fiber size and entropy summaries |
| Reward direct-image | Aggregated reward signal on quotient action/state cells | Reward bundle manifest, reward-fiber variance table |
| Reward compatibility | Whether cells group transitions with similar reward | Reward variance inside quotient fibers |
| Liftability | Whether coarse decisions resolve to valid useful fine actions | Lift success rate, failed-lift reason table |
| Balanced addressability | Whether quotient addresses are neither singleton noise nor giant useless bins | Cell size distribution, entropy, max/min ratios |
| log speed-up hypothesis | Structured hierarchy reduces search burden at sufficient scale | Matched baseline learning curves, timing, seed intervals |
| Bad-contraction warning | Arbitrary contractions need not help | Bad/adversarial schema comparison |

## Environment Family Identity

Recommended family id:

```text
counterpoint_symbolic_v001
```

Alternative ids considered:

- `counterpoint_hidden_graph_v001`
- `counterpoint_contraction_schema_v001`
- `symbolic_counterpoint_hidden_graph_v001`

The recommended id is short enough for artifact paths while still saying what the domain is.

The hidden-graph and schema emphasis should live in the blueprint title, method docs, and manifests rather than making every id too long.

### Turn Question 01: Family Id

PO:

Should the family id be `counterpoint_symbolic_v001`, or do you want the id itself to foreground hidden graphs or contraction schemas?

Codex recommendation:

Use `counterpoint_symbolic_v001` for the environment family, and use separate schema ids for the contraction experiments.

PO response:

[PO fill in]

Codex next turn:

[Codex fill in]

## Environment Family Summary

The environment is a finite-horizon symbolic sequence-construction problem.

At each step, the state contains:

- a tuple of ordered pitches, one per voice,
- a beat index or phase index,
- and later, only if explicitly versioned, any additional context needed by nonlocal reward terms.

The action contains:

- a tuple of per-voice pitch deltas,
- bounded by a maximum step size,
- filtered by local legality rules.

The transition:

- applies the deltas,
- advances the beat index,
- checks node and edge legality,
- emits stable transition labels,
- produces reward via a modular reward bundle,
- and terminates or truncates at a fixed horizon.

The hidden graph consists of all reachable legal states and legal labelled transitions for a fixed instance spec.

## Why This Is the First Serious Environment

Counterpoint-like symbolic sequence generation is a good first serious benchmark because:

- it has a compact local state description but explosive path volume,
- legality masks are meaningful and measurable,
- multiple plausible quotient structures exist,
- bad quotient structures are easy to construct,
- reward compatibility can be measured directly,
- voice projections give natural lift-fiber diagnostics,
- scale can be controlled by voice count, pitch band, horizon, and max step size,
- exact graph diagnostics are feasible at tiny scales,
- sampled diagnostics are feasible at larger scales,
- and qualitative examples can sanity-check failure modes without becoming primary evidence.

## Conceptual Descent from `state_collapser` Smoker

The existing `state_collapser` counterpoint smoker has the right rough shape:

- pitch tuple state,
- beat index,
- pitch band,
- strict voice ordering,
- max step size,
- interval constraints,
- forbidden parallels,
- max outer span,
- local reward,
- action masks,
- and a semantic schema hook.

The benchmark-owned version should preserve that conceptual shape while making it serious:

- parameterize voice count,
- version legality contracts,
- version reward bundles,
- version schema families,
- expose graph diagnostics,
- expose mask density,
- expose path-volume diagnostics,
- expose quotient and lift diagnostics,
- compare multiple schemas on the same underlying graph,
- and write full artifacts.

The benchmark must not require editing the upstream smoker.

## Relationship to Old `rl_counterpoint`

Old `rl_counterpoint` is not the implementation baseline for this repo.

Its value is conceptual:

- additive reward design,
- the importance of easy reward-term iteration,
- the intuition that counterpoint search space grows brutally with voices and horizon,
- the idea that voice projections can be musically meaningful diagnostics,
- and the need to inspect qualitative outputs when something seems suspicious.

The benchmark should not revive the old tower stack as the primary experimental object.

Instead, it should express hierarchy pressure through contraction schemas and projection diagnostics within the current `state_collapser` worldview.

## Instance Spec Contract

Each concrete environment instance must have an instance spec that can be serialized into a manifest.

Recommended shape:

```text
CounterpointInstanceSpec
  environment_family_id
  environment_instance_id
  family_version
  voice_count
  pitch_min
  pitch_max
  tonic_pitch_class
  measure_size
  horizon_steps
  max_step_size
  allow_stationary_voice
  require_strict_voice_order
  allowed_adjacent_interval_classes
  allowed_outer_interval_classes
  allowed_root_interval_classes
  forbidden_parallel_interval_classes
  max_outer_span
  legality_contract_id
  reward_bundle_id
  edge_label_contract_id
  initial_state_policy_id
  terminal_policy_id
  action_mask_policy_id
```

### Required Instance Fields

`environment_family_id`

Stable family id, initially recommended as `counterpoint_symbolic_v001`.

`environment_instance_id`

Stable id for this concrete parameter setting, for example:

```text
counterpoint_symbolic_n3_tiny_v001
counterpoint_symbolic_n3_small_v001
counterpoint_symbolic_n4_medium_v001
```

`voice_count`

Number of voices. Must be at least 2. First serious family should support at least 3 and 4.

`pitch_min`, `pitch_max`

Inclusive pitch band for all voices.

`tonic_pitch_class`

Pitch class used by root/tonic constraints and reward terms.

`measure_size`

Number of beat phases before beat index wraps.

`horizon_steps`

Finite episode horizon.

`max_step_size`

Maximum absolute pitch delta for a single voice in one action.

`allow_stationary_voice`

Whether a voice may use delta 0.

`require_strict_voice_order`

Whether pitches must be strictly increasing from low to high voice.

`allowed_adjacent_interval_classes`

Set of allowed pitch-class intervals between adjacent voices.

`allowed_outer_interval_classes`

Set of allowed pitch-class intervals between lowest and highest voices.

`allowed_root_interval_classes`

Set of allowed intervals from tonic/root if enabled.

`forbidden_parallel_interval_classes`

Set of interval classes for which parallel motion is forbidden.

`max_outer_span`

Maximum semitone span between lowest and highest voice.

`legality_contract_id`

Versioned id describing exactly how node and edge legality are computed.

`reward_bundle_id`

Versioned id describing reward terms and weights.

`edge_label_contract_id`

Versioned id describing emitted edge labels.

`initial_state_policy_id`

Versioned id describing allowed start states.

`terminal_policy_id`

Versioned id describing termination and truncation.

`action_mask_policy_id`

Versioned id describing how masks are generated and exposed.

## State Contract

Recommended state shape:

```text
CounterpointState
  pitches: tuple[int, ...]
  beat_index: int
```

Constraints:

- `len(pitches) == voice_count`
- each pitch is in `[pitch_min, pitch_max]`
- if strict order is enabled, `pitches[i] < pitches[i + 1]`
- `beat_index` is in `[0, measure_size - 1]`

The first version should not include:

- last action,
- previous interval vector,
- recent contour history,
- accumulated cadence state,
- phrase position beyond beat index,
- or hidden reward memory.

Those can be added later only as versioned state contracts.

### State Invariants

The PO accepted the following candidate state invariants:

- pitch band,
- strict voice order,
- adjacent intervals,
- outer interval,
- max outer span,
- root pitch class relationship,
- beat index.

These should be documented in the legality contract and serialized into instance manifests.

## Action Contract

Recommended action shape:

```text
CounterpointAction
  deltas: tuple[int, ...]
```

Constraints:

- `len(deltas) == voice_count`
- each delta is in `[-max_step_size, max_step_size]`
- stationary voices are permitted only when `allow_stationary_voice` is true
- action legality is determined by applying the candidate deltas and checking edge/node legality

The raw action space size is:

```text
(2 * max_step_size + 1) ** voice_count
```

or smaller if stationary movement is globally disabled.

The legal action set is the masked subset of this raw action space at a given state.

## Transition Contract

For state `s_t = (pitches_t, beat_index_t)` and action `a_t = deltas_t`:

1. Candidate pitches are `pitches_t + deltas_t`.
2. Candidate beat index is `(beat_index_t + 1) mod measure_size`.
3. Node legality is checked on candidate state.
4. Edge legality is checked on `(state, action, candidate_state)`.
5. If legal, transition to candidate state.
6. Emit reward from the active reward bundle.
7. Emit transition labels from the active edge-label contract.
8. Terminate or truncate according to the terminal policy.

Primary comparable modes should expose only legal actions through masks.

Invalid transitions should still have a well-defined diagnostic contract for unmasked stress modes, but those modes are not primary.

## Legality Contract

Legality must be explicitly versioned.

Recommended first id:

```text
counterpoint_legality_local_v001
```

The first legality version is local:

- current state,
- candidate action,
- candidate next state,
- beat index,
- and instance parameters.

It must not inspect earlier history.

### Node Legality

Node legality should include:

- all voices in pitch band,
- strict ordering when enabled,
- adjacent interval class membership,
- outer interval class membership,
- maximum outer span,
- root/tonic interval constraint when enabled,
- beat index validity.

### Edge Legality

Edge legality should include:

- action delta bounds,
- stationary voice policy,
- forbidden parallel interval-class checks,
- optional movement-shape constraints,
- optional beat-phase-specific constraints,
- and any local transition-only constraints needed by the first reward bundle.

### Versioning Rule

Changing any legality rule changes the legality contract id.

The benchmark must not compare runs across different legality ids without explicitly saying so.

## Reward Contract

The reward system must be modular.

Recommended first bundle id:

```text
counterpoint_reward_local_v001
```

The reward bundle is a weighted sum or structured aggregation of reward terms.

Each reward term must have:

```text
RewardTermSpec
  reward_term_id
  reward_term_version
  weight
  enabled
  input_scope
  locality_class
  output_range
  diagnostic_fields
```

### Required Reward Term Properties

`reward_term_id`

Stable id, for example `adjacent_interval_preference_v001`.

`reward_term_version`

Version separate from the weight.

`weight`

Numeric coefficient.

`enabled`

Boolean.

`input_scope`

Explicitly says what the term reads.

Allowed first-version scopes:

- current state,
- action,
- next state,
- beat index,
- instance parameters.

`locality_class`

Initially `action_local`.

Future possibilities:

- `state_augmented_local`,
- `path_labelled`,
- `episode_terminal`.

`output_range`

Expected numeric range for diagnostics.

`diagnostic_fields`

Term-level values that can be emitted for debugging and reward compatibility analysis.

### First Reward Family

The first reward bundle should probably include simple local terms such as:

- valid transition bonus,
- preferred adjacent interval classes,
- preferred outer interval classes,
- small movement preference,
- contrary or oblique motion preference,
- leap penalty,
- range comfort penalty,
- beat-phase cadence-like local preference,
- terminal completion bonus.

These are examples, not a finalized implementation list.

The important contract is that adding a reward term should be routine.

### Reward Direct-Image Diagnostics

Because quotient towers aggregate state/action cells, the benchmark must measure whether reward is coherent inside quotient fibers.

Required diagnostics:

- reward mean per quotient cell,
- reward variance per quotient cell,
- min/max reward per quotient cell,
- number of fine transitions contributing,
- term-level variance when feasible,
- and worst cells by reward variance.

The benchmark can record multiple reward direct-image aggregators for analysis. It should not silently choose an aggregator and present it as the only truth.

### Turn Question 02: Reward Aggregator Defaults

PO:

For quotient reward diagnostics, should the first artifacts compute multiple aggregators by default, such as mean, max, min, and softmax-like summaries, or should the first benchmark privilege a single mean direct-image and add others later?

Codex recommendation:

Record multiple diagnostics where cheap, but treat mean and variance as the first primary pair.

PO response:

[PO fill in]

Codex next turn:

[Codex fill in]

## Edge Label Contract

The environment should emit stable edge labels because schemas should contract over labelled transitions rather than ad hoc code internals.

Recommended first id:

```text
counterpoint_edge_labels_local_v001
```

### Required Label Families

Every legal transition should be able to emit labels from these families:

- beat phase before transition,
- beat phase after transition,
- per-voice delta,
- per-voice movement class,
- global motion direction pattern,
- adjacent interval classes before,
- adjacent interval classes after,
- outer interval class before,
- outer interval class after,
- interval change classes,
- root interval class before,
- root interval class after,
- forbidden-parallel check result,
- max-span bucket,
- cadence-like beat-phase marker if enabled,
- terminal candidate marker.

### Movement Classes

Movement labels should be coarse and stable.

Possible per-voice movement classes:

- `down_leap`
- `down_step`
- `stationary`
- `up_step`
- `up_leap`

The exact thresholds must be versioned.

### Direction Pattern Labels

For an `n`-voice action, global direction pattern can be a tuple over:

- `D`
- `S`
- `U`

This label is useful for schemas that group transitions by motion shape.

### Interval Labels

Adjacent and outer interval labels should include both:

- raw semitone interval where useful,
- pitch-class interval for contraction.

The benchmark must be careful not to overfit labels to a desired schema result.

## Hidden Graph Contract

For a fixed instance spec, the hidden graph is:

```text
G = (S, A, E)
```

where:

- `S` is the finite set of reachable legal states,
- `A(s)` is the legal masked action set at state `s`,
- `E` is the set of labelled legal transitions.

The graph may be generated lazily or explicitly depending on scale.

For tiny and small instances, exact graph enumeration should be feasible and preferred.

For medium and larger instances, sampled graph diagnostics are acceptable if clearly labelled as sampled.

## Initial State Contract

Recommended first id:

```text
counterpoint_initial_states_v001
```

The initial state policy should be deterministic or seed-controlled.

The first tiny fixtures should probably use a small fixed set of legal starting states to make exact diagnostics easier.

Larger instances may sample from legal start states under a deterministic seed bundle.

The initial state policy must be recorded in the instance manifest.

## Termination and Truncation Contract

Recommended first id:

```text
counterpoint_terminal_horizon_v001
```

The first version should use:

- termination on successful completion if a terminal predicate is enabled,
- truncation at `horizon_steps`,
- and no hidden failure termination except invalid action in diagnostic unmasked modes.

For masked primary modes, invalid action termination should not occur because illegal actions are unavailable.

## Action Mask Contract

Recommended first id:

```text
counterpoint_legal_action_mask_v001
```

The mask for state `s` is the set of raw actions whose transition is legal under the active legality contract.

Primary modes:

- direct env tabular uses this mask,
- tower empty schema uses this mask,
- tower nonempty schema uses this mask.

The mask itself is not a schema advantage.

It is part of the shared environment interface.

### Mask Diagnostics

Required metrics:

- raw action count,
- legal action count per state,
- mask density per state,
- mean mask density,
- min/max mask density,
- mask entropy or distribution summary,
- dead-end state count,
- states with exactly one legal action,
- and states with zero legal actions.

## Contraction Schema Role

The contraction schema tells `state_collapser` how to group or identify structure in the hidden graph.

It must be treated as an experimental variable.

The benchmark should hold the environment instance fixed and vary schema id.

The benchmark must support at least:

- empty schema,
- random balanced schema,
- structured counterpoint-motion schema,
- projection-audit schema,
- bad/adversarial schema.

## Schema Manifest Contract

Every schema run must write a schema manifest.

Recommended fields:

```text
SchemaManifest
  schema_id
  schema_family_id
  schema_version
  environment_family_id
  environment_instance_id
  schema_seed
  construction_method
  source_label_families
  state_partition_description
  action_partition_description
  expected_tower_depth
  expected_compression_target
  leakage_risk_statement
  intended_role
  online_eligible
  diagnostic_only
```

### Required Schema Properties

`schema_id`

Stable id used in mode manifests.

`schema_family_id`

Family-level grouping, for example `random_balanced`.

`schema_seed`

Required for random schemas.

`construction_method`

Human-readable and machine-readable construction summary.

`source_label_families`

Edge/state labels used by the schema.

`expected_tower_depth`

Expected or target nontrivial quotient depth.

`expected_compression_target`

Approximate target compression if applicable.

`leakage_risk_statement`

Explicit statement of what reward or future information this schema might leak.

`intended_role`

One of:

- `baseline_empty`
- `random_control`
- `structured_candidate`
- `projection_diagnostic`
- `bad_control`

`online_eligible`

Whether the schema can be used by online tower modes.

`diagnostic_only`

Whether the schema is only for posthoc diagnostics.

## Required Schema Families

### Empty Schema

Recommended id:

```text
counterpoint_empty_schema_v001
```

Purpose:

- establish tower overhead when no useful contraction is supplied,
- separate "tower machinery cost" from "schema structure benefit."

Expected behavior:

- little or no meaningful compression,
- minimal lift ambiguity,
- no strong performance advantage,
- measurable overhead.

### Random Balanced Schema

Recommended id pattern:

```text
counterpoint_random_balanced_schema_v001_seed_<seed>
```

Purpose:

- test whether compression alone helps,
- control for cell-size balance,
- expose reward variance caused by semantically arbitrary grouping.

Expected behavior:

- nontrivial compression,
- maybe balanced cell sizes,
- likely poor reward compatibility,
- likely lower lift success than structured schemas.

Construction requirement:

- deterministic given `schema_seed`,
- no reward labels,
- no terminal future information,
- no leakage from evaluation statistics.

### Random Unbalanced Schema

Recommended id pattern:

```text
counterpoint_random_unbalanced_schema_v001_seed_<seed>
```

Purpose:

- create a compression pathology control,
- demonstrate why balanced addressability matters.

Expected behavior:

- large giant cells or singleton-heavy cells,
- high lift-fiber entropy,
- poor reward compatibility,
- unstable performance.

This may be optional for the very first implementation slice, but the blueprint should reserve it.

### Structured Motion Schema

Recommended id:

```text
counterpoint_motion_schema_v001
```

Purpose:

- group transitions by musically/domain-plausible local motion features,
- test whether a simple structured schema improves quotient usefulness.

Possible source labels:

- direction pattern,
- step/leap movement class,
- adjacent interval class before and after,
- outer interval class before and after,
- beat phase,
- span bucket.

Expected behavior:

- nontrivial compression,
- better reward compatibility than random,
- better lift success than bad schemas,
- possible sample-efficiency gains at medium scale.

Leakage risk:

- must not use future rewards,
- must not use episode outcome,
- must not use learned value estimates.

### Projection-Audit Schema

Recommended id:

```text
counterpoint_projection_audit_schema_v001
```

Purpose:

- test old `rl_counterpoint` projection intuition as a diagnostic,
- measure whether dropping or coarsening a voice creates useful quotient fibers,
- bind voice-projection ideas to current state-collapser artifacts.

This schema may be diagnostic-only at first.

It should not become the default structured schema until evidence supports it.

Possible projection:

- map `n` voices to `n - 1` by removing one interior voice,
- preserve outer voices and beat index,
- or preserve lower voices and beat index.

The projection convention must be explicit.

### Bad or Adversarial Schema

Recommended id:

```text
counterpoint_bad_schema_v001
```

Purpose:

- show that arbitrary contraction can hurt,
- test reward-incompatible grouping,
- validate diagnostics by producing visible failures.

Possible construction:

- group states/actions by labels known to ignore reward-relevant structure,
- group incompatible interval classes,
- group high-reward and low-reward transitions together,
- create lift fibers with high invalid-resolution rates.

Leakage caution:

If constructed using reward diagnostics, it must be labelled as adversarial diagnostic, not a fair online schema.

## Projection Diagnostics

Projection diagnostics are important because counterpoint gives a natural way to compare fine and coarse voice sets.

However, projection diagnostics must be carefully separated from primary online training modes.

Projection can answer:

- how many fine states lift from a projected state,
- whether projected transitions have valid fine lifts,
- whether reward is coherent under projection,
- whether voice removal produces balanced or pathological fibers,
- whether projected addresses compress path space without destroying action usefulness.

### Candidate Projection Conventions

For `n >= 3`, possible projections include:

1. Drop the second-from-top voice.
2. Drop the most interior voice by index.
3. Keep only outer voices.
4. Drop each voice in turn and report separate diagnostics.

The old tower/projection conversations suggest the second-from-top voice may be a meaningful inherited convention, but this should not be smuggled in without an explicit decision.

### Turn Question 03: Projection Convention

PO:

For the first projection-audit schema, should we inherit the old second-from-top projection convention, use an all-drop-one diagnostic suite, or start with outer-voice-only projection?

Codex recommendation:

Use all-drop-one diagnostics for posthoc analysis, but pick one named online-eligible projection only after seeing tiny/small diagnostics. If a single first convention is required, use second-from-top for continuity with prior work and label it clearly.

PO response:

[PO fill in]

Codex next turn:

[Codex fill in]

## Benchmark Mode Matrix

The first benchmark family must support the canonical modes from the infrastructure blueprint.

### Required First Modes

`direct_env_tabular`

Direct learner on the environment with legal masks.

`tower_empty_schema_tabular`

Tower runtime with empty schema, same learner class where applicable, same masks.

`tower_nonempty_schema_tabular`

Tower runtime with nonempty schema, initially structured motion and random controls.

### Reserved Later Modes

`tower_exploit_explore`

Tower control mode where exploration/exploitation policy uses tower structure.

`tower_fiber_conditioned_stage`

Training stage conditioned by fiber or quotient context.

`tower_control_with_fiber_conditioned_substages`

Reserved composite regime.

### Mode Dimensions

Every run must record:

- `environment_coupling`
- `schema_mode`
- `schema_id`
- `controller_regime`
- `training_surface`
- `learner_id`
- `diagnostic_profile`
- `timing_profile`
- `action_mask_policy_id`
- `legality_contract_id`
- `reward_bundle_id`
- `edge_label_contract_id`

## First Experimental Matrix

The first full matrix should eventually include:

| Arm | Environment | Schema | Learner | Purpose |
| --- | --- | --- | --- | --- |
| A | fixed instance | none/direct | tabular | direct baseline |
| B | fixed instance | empty | tabular | tower overhead |
| C | fixed instance | random balanced | tabular | compression control |
| D | fixed instance | random unbalanced | tabular | balance failure control |
| E | fixed instance | structured motion | tabular | first structured candidate |
| F | fixed instance | projection audit | diagnostic or tabular | projection hypothesis |
| G | fixed instance | bad/adversarial | tabular or diagnostic | failure validation |

Not all arms must be implemented in the first code slice.

But the environment and artifacts should be designed so these arms are natural.

## Learner Scope

The first learner can be simple.

Recommended first learner id:

```text
local_tabular_q_v001
```

It should be enough to produce:

- comparable direct/tower runs,
- seed-level learning curves,
- episode returns,
- success or completion rates if defined,
- action coverage,
- and timing overhead.

The first benchmark is not a deep-RL benchmark.

The point is to expose hidden graph, quotient, lift, reward compatibility, and path-volume structure.

### Turn Question 04: First Learner

PO:

Should first implementation use a minimal tabular Q learner as the shared learner across direct and tower modes, or should the first slice use an even simpler random/masked policy before any learning?

Codex recommendation:

Use both, but stage them: random/masked policy for graph and artifact smoke, then tabular Q for the first learning comparison.

PO response:

[PO fill in]

Codex next turn:

[Codex fill in]

## Scale Ladder

The scale ladder must make exact diagnostics feasible early while preserving a path toward real pressure.

The exact numbers below are draft instance-shape recommendations. The implementation workplan should validate them by quick enumeration before committing final fixture ids.

### Tiny

Purpose:

- deterministic exact graph enumeration,
- exact path-volume counts,
- exact reward-fiber variance,
- schema construction tests,
- artifact contract tests.

Recommended shape:

```text
voice_count: 3
pitch_band_width: very small
measure_size: 2 or 4
horizon_steps: 4 to 8
max_step_size: 1
strict_order: true
```

Expected evidence:

- exact reachable state count,
- exact edge count,
- exact legal mask density,
- exact path count for horizon,
- exact quotient cell sizes,
- exact lift-fiber summaries.

### Small

Purpose:

- first meaningful learning smoke,
- exact or near-exact graph diagnostics,
- compare direct, empty, random, and structured schemas.

Recommended shape:

```text
voice_count: 3
pitch_band_width: small to moderate
measure_size: 4
horizon_steps: 8 to 16
max_step_size: 1 or 2
strict_order: true
```

Expected evidence:

- graph summary,
- path-volume exact or bounded,
- seed-level learning curves,
- schema diagnostics,
- timing overhead.

### Medium

Purpose:

- first serious pressure regime,
- sampled path-volume diagnostics,
- meaningful comparison of structured versus random schemas.

Recommended shape:

```text
voice_count: 3 or 4
pitch_band_width: moderate
measure_size: 4
horizon_steps: 16 to 32
max_step_size: 2
strict_order: true
```

Expected evidence:

- sampled path-volume estimates,
- policy-effective path-volume estimates,
- learning curves with multiple seeds,
- quotient compression ratios,
- lift-fiber entropy,
- reward-fiber variance,
- timing segments.

### Large

Purpose:

- test whether tower structure becomes useful when flat path volume is large,
- measure overhead at scale,
- expose online diagnostic cost.

Recommended shape:

```text
voice_count: 4
pitch_band_width: moderate to large
measure_size: 4
horizon_steps: 32 to 64
max_step_size: 2 or 3
strict_order: true
```

Expected evidence:

- sampled graph/path diagnostics,
- multi-seed learning intervals,
- strict timing breakdown,
- no expensive compatibility readouts unless explicitly requested.

### Stress

Purpose:

- probe failure modes,
- identify memory/time boundaries,
- avoid overclaiming.

Recommended shape:

```text
voice_count: 4 or 5
pitch_band_width: large
measure_size: 4 or 8
horizon_steps: 64+
max_step_size: 3+
strict_order: true
```

Expected evidence:

- sampled-only diagnostics,
- runtime/memory profile,
- clear warning labels,
- no first-paper claims unless reproducibility is strong.

### Turn Question 05: First Concrete Fixture Values

PO:

Should the first implementation workplan choose tiny/small numeric parameters by hand, or should it begin with a quick enumeration tool that searches for fixtures in target state/edge/path-count ranges?

Codex recommendation:

Use a small enumeration/search utility during implementation. Hand-picked musical-looking values are less important than hitting exact diagnostic feasibility and path-volume pressure targets.

PO response:

[PO fill in]

Codex next turn:

[Codex fill in]

## Path-Volume Diagnostics

Path volume is central.

The benchmark must not merely report episode return.

### Required Path Metrics

For tiny and small instances where feasible:

- exact number of reachable states,
- exact number of legal edges,
- exact number of valid paths of length `K`,
- exact number of valid paths up to length `K`,
- exact path count by terminal/success status if applicable.

For larger instances:

- sampled path-count estimates,
- branching-factor summaries,
- legal mask density summaries,
- policy-sampled path diversity,
- confidence intervals or bootstrap intervals where appropriate.

### Policy-Effective Path Volume

The benchmark should distinguish raw valid path count from policy-effective path volume.

Policy-effective estimates may be based on:

- random legal policy,
- learner policy checkpoints,
- epsilon-greedy policy samples,
- quotient-conditioned policy samples,
- or replay/trajectory coverage.

Artifacts must say exactly which policy generated the estimate.

## Quotient and Tower Diagnostics

For every schema/tower run, the benchmark should report:

- tower depth,
- quotient state count per tier,
- quotient action count per tier,
- compression ratio per tier,
- cell size distribution per tier,
- lift-fiber size distribution,
- lift-fiber entropy,
- failed-lift rate,
- failed-lift reason counts,
- reward variance inside quotient fibers,
- mask density by quotient context if available,
- and sampled address traces.

### Compression Alone Is Not Success

The benchmark must avoid treating high compression as good by itself.

A useful schema should compress while preserving enough reward and lift structure to improve learning or control.

## Reward Compatibility Diagnostics

Required outputs:

- reward mean by quotient cell,
- reward variance by quotient cell,
- term-level reward variance where feasible,
- worst reward-incompatible cells,
- correlation between cell size and reward variance,
- comparison against random balanced schema,
- comparison against bad schema.

The central question:

> Did the schema group together transitions that are reward-compatible enough for coarse decisions to be meaningful?

## Lift Diagnostics

Required outputs:

- number of possible fine lifts for sampled coarse choices,
- lift success rate,
- lift failure reasons,
- lift-fiber size distribution,
- lift-fiber entropy,
- reward distribution over candidate lifts,
- valid-action availability inside lift fiber,
- and whether successful lifts remain legal under the original environment.

The central question:

> Did the quotient decision leave a usable set of fine choices, or did it create an ambiguous bin with no reliable resolution?

## Balanced Addressability Diagnostics

Required outputs:

- address count,
- address frequency distribution,
- quotient cell size distribution,
- entropy of address distribution,
- largest cell share,
- singleton cell share,
- effective number of cells,
- path coverage by address.

The central question:

> Did the schema create an address system for path space, or did it merely rename the original search problem?

## Timing Discipline

The benchmark must preserve the timing discipline from the infrastructure blueprint.

Use `time.perf_counter()`.

Report at least:

- environment reset time,
- environment step time,
- action mask construction time,
- tower reset/update time,
- controller decision time,
- lift/resolve time,
- learner action time,
- learner update time,
- artifact logging time,
- compatibility readout time if requested,
- posthoc diagnostics time,
- summary generation time.

### Hot-Path Rule

Default benchmark runs must not call rich compatibility readouts unless the mode explicitly requests them.

Required flags:

- `readout_requested`
- `morphism_requested`
- `uses_compatibility_readout`
- `uses_morphism`

This matters because expensive readouts can recreate costs that recent `state_collapser` revisions intentionally removed from the hot path.

## Artifact Contract

The infrastructure blueprint already defines the global artifact layout. This environment family adds specific environment/schema artifacts.

### Required Environment Artifacts

`environment_family_manifest.json`

Describes the family, geometry, legality ids, reward bundle ids, and supported scale ladder.

`environment_instance_manifest.json`

Describes one concrete instance.

`legality_manifest.json`

Describes active legality contract and parameters.

`reward_bundle_manifest.json`

Describes reward terms, weights, scopes, and versions.

`edge_label_manifest.json`

Describes emitted label families.

`initial_state_manifest.json`

Describes start-state policy.

`action_mask_manifest.json`

Describes mask construction and exposure.

### Required Graph Artifacts

`graph_summary.json`

State count, edge count, reachability summary, dead ends, branch factors.

`mask_density.csv`

State-level or sampled mask-density rows.

`path_volume_summary.json`

Exact or sampled path-volume diagnostics.

`path_volume_samples.jsonl`

Sampled path diagnostics for non-exact scales.

### Required Schema Artifacts

`schema_manifest.json`

One per schema run.

`schema_diagnostics.jsonl`

Schema construction events and statistics.

`quotient_summary.json`

Tier counts, compression ratios, cell stats.

`quotient_cells.csv`

Cell ids and size summaries where feasible.

`address_traces.jsonl`

Sampled path addresses.

### Required Lift and Reward Artifacts

`lift_fiber_summary.csv`

Fiber size and entropy summaries.

`lift_attempts.jsonl`

Sampled lift attempts and outcomes.

`reward_fiber_variance.csv`

Reward variance by quotient cell/fiber.

`reward_term_diagnostics.jsonl`

Term-level diagnostics where enabled.

### Required Learning Artifacts

Inherited from infrastructure:

- `run_index.jsonl`
- `episodes.csv`
- `step_events.csv`
- `control_events.csv`
- `timing_segments.csv`
- `structural_diagnostics.jsonl`
- `warnings.jsonl`
- `summary.json`
- `bootstrap_intervals.csv`

### Qualitative Artifacts

Optional:

- symbolic example trajectories as JSON,
- MIDI examples,
- compact text renderings of selected sequences.

These should live under an explicit qualitative/examples directory and must be labelled non-primary.

## Human-Facing Docs Layer

The infrastructure blueprint added a docs-like layer for human summaries. This environment should populate it once implemented.

Recommended files:

```text
docs/environments/counterpoint_symbolic_v001.md
docs/experiments/counterpoint_symbolic_v001_first_matrix.md
docs/results/counterpoint_symbolic_v001_first_results.md
docs/methods/counterpoint_schema_diagnostics.md
docs/methods/counterpoint_path_volume.md
```

### Environment Human Doc Contents

The environment doc should summarize:

- family id,
- hidden geometry,
- state definition,
- action definition,
- transition rule,
- legality rule,
- reward bundle,
- termination/truncation,
- why flat search is wasteful,
- quotient/projection hypothesis,
- scale ladder,
- schema candidates,
- schema leakage risks,
- negative controls,
- artifact fields,
- and known limitations.

### Experiment Human Doc Contents

The experiment doc should summarize:

- matrix arms,
- instance ids,
- schema ids,
- learner ids,
- seed bundle policy,
- diagnostic profile,
- timing profile,
- acceptance gates,
- and planned comparisons.

### Results Human Doc Contents

The result doc should summarize:

- artifact bundle ids,
- exact dates,
- run ids,
- high-level findings,
- confidence intervals,
- failures and warnings,
- and links to machine-readable artifacts.

Artifacts remain the source of truth.

Human docs are summaries, not evidence replacement.

## Seed Bundle Contract

Every run must record the seed bundle fields from the infrastructure blueprint:

```text
seed_bundle_id
replicate_index
environment_seed
schema_seed
learner_seed
controller_seed
diagnostic_sampling_seed
artifact_sampling_seed
```

The replicate is the unit of uncertainty.

Schema randomization must be separated from learner randomization.

This is especially important for random schema controls.

## Statistical Contract

The first serious results should use seed-level replicate summaries.

Default interval:

- simple percentile bootstrap over seed-level replicates.

Required caution:

- do not overclaim from tiny/small smoke runs,
- distinguish exact graph metrics from sampled estimates,
- distinguish single-instance results from family-level results,
- distinguish schema-seed variability from learner-seed variability.

## Environment Acceptance Gates

Before this family can be called implementation-ready, it needs:

1. Written geometry spec.
2. Versioned instance spec.
3. Versioned state contract.
4. Versioned action contract.
5. Versioned transition contract.
6. Versioned legality contract.
7. Versioned reward bundle contract.
8. Versioned edge-label contract.
9. Deterministic tiny instance.
10. Direct-env smoke on tiny instance.
11. Tower empty-schema smoke on tiny instance.
12. Tower nonempty-schema smoke on tiny instance.
13. Random balanced schema construction.
14. Structured motion schema construction.
15. Bad/adversarial schema construction or reserved diagnostic.
16. Exact tiny graph diagnostics.
17. Exact tiny path-volume diagnostics.
18. Mask density diagnostics.
19. Reward-fiber variance diagnostics.
20. Lift-fiber diagnostics.
21. Artifact validation.
22. No obvious schema leakage.
23. Timing segmentation.
24. Human environment doc stub.
25. Clear explanation of why this stresses `state_collapser`.

## Test Contract

This is not an implementation plan, but later code should have tests covering at least:

- state serialization stability,
- action serialization stability,
- deterministic action enumeration,
- deterministic mask generation,
- legality contract examples,
- reward term composition,
- reward bundle versioning,
- edge label emission,
- tiny graph reachability,
- exact tiny path-volume counts,
- schema construction determinism,
- random schema seed sensitivity,
- structured schema nontriviality,
- bad schema expected pathology,
- artifact schema validation,
- no rich compatibility readout in default hot path,
- and mode manifest correctness.

## Implementation Boundaries

When implementation begins, code should likely be organized under a benchmark-owned package in this repo, not inside `state_collapser`.

Possible package shape:

```text
src/big_boy_benchmarking/
  environments/
    counterpoint/
      spec.py
      state.py
      actions.py
      legality.py
      rewards.py
      labels.py
      graph.py
      masks.py
      schemas.py
      diagnostics.py
      artifacts.py
```

This is a sketch, not an instruction to implement yet.

The implementation workplan must inspect the actual repo package layout before deciding final paths.

## Risks

### Risk: Counterpoint Becomes Music-Quality Benchmark

Mitigation:

Keep the benchmark framed around hidden graph structure, quotient quality, reward compatibility, and learning/timing evidence.

### Risk: Schema Leaks Reward or Future Information

Mitigation:

Every schema manifest must include source labels and leakage-risk statement. Structured online schemas must not use future reward, outcomes, or learned values.

### Risk: Action Masks Make the Task Too Easy

Mitigation:

Use masks consistently across comparable modes and report mask density. Add invalid-action-pressure modes later only as diagnostics.

### Risk: Tiny Instances Overfit the Design

Mitigation:

Use tiny only for exactness and tests. Do not make substantive performance claims until small/medium multi-seed runs.

### Risk: Random Schemas Are Unfairly Weak

Mitigation:

Use balanced random controls and record compression targets. Compare structured schema against controls with similar cell-size distributions when possible.

### Risk: Structured Schema Is Too Hand-Designed

Mitigation:

Document labels used, avoid reward leakage, compare against projection and random controls, and report failures.

### Risk: Diagnostics Recreate Hot-Path Cost

Mitigation:

Separate online hot-path metrics from periodic/posthoc diagnostics. Record readout flags and timing segments.

### Risk: Reward Evolves Faster Than Artifacts

Mitigation:

Make reward bundles versioned and modular from the first implementation.

## First Blueprint-Level Deliverables

The next design-to-implementation sequence should produce:

1. Final PO answers to the turn questions in this blueprint.
2. A Phase.Stage.Action implementation workplan.
3. A tiny instance spec with target exact-count feasibility.
4. A small instance spec for first learning smoke.
5. A reward bundle v001.
6. A legality contract v001.
7. An edge-label contract v001.
8. Empty, random balanced, structured motion, and bad schema specs.
9. Artifact schemas for the environment-specific files.
10. Human environment doc stub.

## Open Turn Questions Summary

### Turn Question 01: Family Id

PO:

Should the family id be `counterpoint_symbolic_v001`, or do you want the id itself to foreground hidden graphs or contraction schemas?

Codex recommendation:

Use `counterpoint_symbolic_v001` for the environment family, and use separate schema ids for the contraction experiments.

PO response:

[PO fill in]

Codex next turn:

[Codex fill in]

### Turn Question 02: Reward Aggregator Defaults

PO:

For quotient reward diagnostics, should the first artifacts compute multiple aggregators by default, such as mean, max, min, and softmax-like summaries, or should the first benchmark privilege a single mean direct-image and add others later?

Codex recommendation:

Record multiple diagnostics where cheap, but treat mean and variance as the first primary pair.

PO response:

[PO fill in]

Codex next turn:

[Codex fill in]

### Turn Question 03: Projection Convention

PO:

For the first projection-audit schema, should we inherit the old second-from-top projection convention, use an all-drop-one diagnostic suite, or start with outer-voice-only projection?

Codex recommendation:

Use all-drop-one diagnostics for posthoc analysis, but pick one named online-eligible projection only after seeing tiny/small diagnostics. If a single first convention is required, use second-from-top for continuity with prior work and label it clearly.

PO response:

[PO fill in]

Codex next turn:

[Codex fill in]

### Turn Question 04: First Learner

PO:

Should first implementation use a minimal tabular Q learner as the shared learner across direct and tower modes, or should the first slice use an even simpler random/masked policy before any learning?

Codex recommendation:

Use both, but stage them: random/masked policy for graph and artifact smoke, then tabular Q for the first learning comparison.

PO response:

[PO fill in]

Codex next turn:

[Codex fill in]

### Turn Question 05: First Concrete Fixture Values

PO:

Should the first implementation workplan choose tiny/small numeric parameters by hand, or should it begin with a quick enumeration tool that searches for fixtures in target state/edge/path-count ranges?

Codex recommendation:

Use a small enumeration/search utility during implementation. Hand-picked musical-looking values are less important than hitting exact diagnostic feasibility and path-volume pressure targets.

PO response:

[PO fill in]

Codex next turn:

[Codex fill in]

## Blueprint Close

This blueprint defines the first serious environment as a fixed counterpoint-like hidden graph family with schema variation as the main experimental axis.

The design is intentionally stricter than a toy environment:

- it demands explicit graph geometry,
- explicit legality,
- explicit reward terms,
- explicit action masks,
- explicit schema families,
- explicit artifacts,
- explicit timing,
- explicit diagnostics,
- and explicit failure controls.

If the PO accepts the remaining turn-question answers, the next artifact should be a detailed Phase.Stage.Action implementation workplan for `counterpoint_symbolic_v001`.
