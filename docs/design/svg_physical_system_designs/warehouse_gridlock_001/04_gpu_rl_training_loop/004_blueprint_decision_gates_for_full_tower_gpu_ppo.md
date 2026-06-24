# Blueprint Decision Gates For Warehouse Full-Tower GPU PPO

## Purpose

This document collects the remaining design issues that should be resolved, or
explicitly carried as open gates, before generating the full blueprint for the
Warehouse Gridlock full-tower GPU PPO model and training loop.

It is a discussion scaffold. It is not a blueprint, not an implementation
workplan, and not implementation authority.

## Authority And Attribution

The model-family direction in this folder is Project Owner-originated. In
particular, Tyler Foster proposed the structured state/action record model,
the state/action history transformer shape, the distribution over
`Out_k(s_t)`, and the old/new PPO snapshot pattern:

```text
policy_k         = current trainable model
rollout_policy_k = frozen snapshot used to collect the rollout
```

Codex's role in this document is to organize unresolved design issues,
describe possible solutions, and make consultant recommendations. The
conversation slots below are intentionally blank so later Project Owner and
Codex turns can be added without false attribution.

## Current Design Baseline

The current design point from the previous discussion is:

```text
Warehouse full-tower PPO uses state_collapser's hardcoded tower traversal
logic. PPO does not choose LIFT, DESCEND, TRAIN, or tier traversal. The PPO
actor is invoked only when hardcoded traversal reaches a tier-local action
selection surface. The actor samples an action from the current tier-local
outgoing set, records old log probability and value estimate, and PPO trains
from the resulting concrete Warehouse transition.
```

The model family is:

```text
history_encoder_k(state_hist, act_hist) -> c_t
candidate_encoder_k(edge_json, src_state, tgt_state, tier, time) -> u_i
score_k(c_t, u_i) -> logit_i
masked softmax over i with a_i in Out_k(s_t)
```

The hard remaining work is not whether this is the right general shape. The
hard remaining work is specifying the exact schemas, freezing rules, masks,
artifact contracts, and first-scope choices tightly enough that a blueprint can
be made without smuggling in new assumptions.

## Issue 1: Exact Structured Record Schemas For States And Actions

### Why This Matters

The proposed model relies on structured state/action records:

```text
R_k(s) for a tier-k state
R_k(a) for a tier-k outgoing action/action-cell
```

These records are JSON-like for artifact and schema purposes, but the model
should see typed, deterministic tensorizable fields. If these records are too
thin, the model collapses back into opaque id embeddings and loses the
state-collapser quotient structure. If they are too broad or ad hoc, the first
GPU PPO implementation becomes brittle and hard to debug.

The blueprint must decide which fields are required, which fields are optional,
which fields are produced by `state_collapser`, and which fields are
Warehouse-specific.

### Candidate State Record Fields

A tier-k state record might include:

```text
tier_id
state_cell_id
state_coset_member_ids
state_coset_size
parent_state_cell_id
child_state_cell_ids
current_concrete_state_id_or_digest
warehouse_robot_positions_projected_or_summarized
warehouse_box_positions_projected_or_summarized
target_alignment_features
blocked_column_relation_features
current_second
remaining_seconds
outgoing_action_count
executable_outgoing_action_count
liftability_summary
one_hop_or_local_adjacency_summary
tower_position_key
runtime_snapshot_digest
```

Not all of these need to be first-scope trainable features. Some may be
artifact-only or debug-only.

### Candidate Action Record Fields

A tier-k action record might include:

```text
tier_id
action_cell_id
source_state_cell_id
target_state_cell_id
member_edge_ids
member_edge_count
lower_action_cell_ids
representative_concrete_action_id_or_digest
lift_candidate_count
is_executable_from_current_concrete_state
mask_reason_if_not_executable
warehouse_move_summary
predicted_or_known_reward_summary_if_available
source_state_record_ref
target_state_record_ref
```

Again, the first-scope model does not need every field as a neural feature,
but the record schema should say what exists, what is tensorized, and what is
only retained for replay/readout.

### Possible Solutions

1. Minimal id-plus-count schema.

   Use stable tier/state/action ids, coset sizes, outgoing counts, executable
   counts, and a few Warehouse time features. This is easiest to implement and
   debug, but it may underuse the quotient structure.

2. Structured quotient schema.

   Include parent/child membership, member counts, source/target ids,
   executable masks, lift candidate summaries, and compact Warehouse projected
   features. This is more aligned with the mathematics and still manageable.

3. Rich record schema with many semantic fields.

   Include all available tower/fiber/runtime summaries, one-hop summaries,
   reward summaries, graph-local statistics, and detailed Warehouse entity
   projections. This gives the model more signal but risks overbuilding before
   PPO mechanics are stable.

### Recommendation

Use option 2 for the blueprint:

```text
structured quotient schema
```

The blueprint should define required record fields in three tiers:

```text
required_tensor_fields
required_artifact_fields
optional_debug_fields
```

It should also require a source column for every field:

```text
state_collapser
Warehouse environment
BBB PPO runtime
derived during tensorization
```

That keeps us from cloning upstream semantics while still giving the model
real quotient-aware structure.

### Conversation Slots

#### PO Turn 1

I agree that option 2 is the correct one. We need to avoid putting *anything* mutable in these `JSON` fields. Specifically, anything thing we might attach to a state that is episode-specific or time-step-specific needs to be expunged from these `JSON`s. These `JSON`s are supposed to capture state/action space geometry as currently understood.

#### Codex Turn 1

Yes. This is the right correction, and it changes how the blueprint should
separate the model inputs.

The state/action `JSON` records should describe the currently known geometry
of the state-action space, not episode-local rollout facts. So fields such as:

```text
current_second
remaining_seconds
runtime_snapshot_digest
old_log_prob
selected_local_index
value_estimate
reward
terminated/truncated
```

do not belong inside the immutable state/action geometry records. They belong
in a separate decision-context or rollout-sample record.

The corrected split should be:

```text
Geometry records:
  stable within a graph/tower snapshot;
  describe state cells, action cells, cosets, source/target structure,
  outgoing structure, quotient membership, and known geometric facts.

Decision context:
  episode/time-specific facts at the moment of action selection, such as
  active tier, active concrete state, time step, action mask, and current
  tower runtime position.

Rollout sample:
  PPO-specific sampled data, such as selected action id, selected local index,
  old log probability, value estimate, reward, bootstrap flags, and PPO
  bookkeeping.
```

If exploration changes the discovered geometry, that should create a new
graph/tower snapshot or record version. It should not mutate the meaning of an
already stored rollout decision surface. This gives us clean record semantics:
the `JSON` captures geometry as currently understood, while rollout/context
records capture the time-local use of that geometry.

#### PO Turn 2

#### Codex Turn 2

## Issue 2: First Quotient Aggregation Rule

### Why This Matters

The Project Owner identified that the Young-diagram quotienting logic should
apply to the model representation itself. A tier-k state or action cell should
not merely become a new opaque id. It should be represented by the nested
coset/quotient data already attached to the current description of
`G^0_t` and its quotient tower.

Important direction convention:

```text
index 0 is the uppermost graph/tier;
passing from i to i + 1 is moving down the tower.
```

The blueprint must use this convention consistently. It should avoid casual
"up" and "down" language unless it means this exact tower-of-fibrations
direction.

### Possible Solutions

1. Opaque learned embeddings per tier object.

   Every state/action cell gets an embedding id. This is easy but ignores the
   quotient structure except through ids and metadata.

2. Fixed aggregation over member embeddings.

   Start with the member/coset data named by the quotient description and
   encode variable-length fields with deterministic operators such as:

   ```text
   sum
   mean
   max
   sum + mean + max concatenated
   ```

3. Learned attention/pooling over members.

   Use a small learned pooling module to encode variable-length coset/member
   fields. This is flexible but adds complexity and can obscure whether the
   quotient scaffold is doing the work.

4. Hybrid fixed aggregation plus learned residual.

   Use `sum + mean + max` as the base representation, then allow a small
   learned projection or residual block.

### Recommendation

Earlier recommendation, now demoted pending Project Owner discussion:

```text
aggregate = concat(sum(member_tokens), mean(member_tokens), max(member_tokens))
representation = learned_projection(aggregate + local_features)
```

The corrected interpretation is that this should not be treated as a separate
cross-tier coupling problem. The nested Young-diagram/coset description itself
is the state/action record content. Aggregation or pooling is only an internal
tokenization technique for variable-length fields inside those records.

The blueprint should require record-tokenization manifests:

```text
tier_id
object_kind = state_cell | action_cell
object_id
member_ids
variable_length_field_encoding_ops
input_feature_schema
output_feature_shape
```

### Conversation Slots

#### PO Turn 1
First of all, you have a critical alignment issue. The "up" "down" language refers to the tower of iberations. But index $0$ is "uppermost". Passing from $i$ to $i+1$ is "goign down". You need to correct your langauge. Second, there is no real issue here. Use coset as state name or whatever. Like all that data in the Young diagram description of the quotient tower as nested data attached to $G^{0}_{t}$, that description *is* what gets put in the fields of the state and action `JSON`s that we tokenize. Do you see? You're inventing issues where there aren't actually issues.

#### Codex Turn 1

Yes. I see the correction, and I agree that I invented an issue where the
better design is simpler.

First, I will use the tower direction convention exactly as you stated it:

```text
index 0 is uppermost;
i -> i + 1 means moving down the tower.
```

Second, the blueprint should not introduce a separate "quotient aggregation
problem" as if the Young-diagram data were absent and needed to be recreated.
The nested quotient/coset description attached to `G^0_t` is already the
structured content of the state/action records. The model tokenizes those
records.

The corrected design statement is:

```text
Use the coset/quotient data itself as the state/action record content.
Do not add a separate cross-tier coupling mechanism.
If variable-length coset fields need pooling for tensorization, treat that as
record tokenization, not as a new mathematical design layer.
```

So this section should be downgraded from "open decision" to "resolved
correction." The blueprint should say that the record schema carries the
Young-diagram quotient information directly. Any `sum/mean/max` or similar
operation is merely a practical encoding choice for variable-length fields
inside the record, not an additional policy-coupling thesis.

#### PO Turn 2

#### Codex Turn 2

## Issue 3: Per-Tier Models Versus Shared Parameters

### Why This Matters

The current design locks a PPO policy surface for each non-degenerate tier:

```text
policy_k
rollout_policy_k
```

But it does not fully decide whether the model parameters are completely
separate per tier, shared across tiers with tier embeddings, or partially
shared through a common record encoder and tier-specific heads.

This matters for learning, memory, checkpointing, and how strongly the model
uses quotient structure across tiers.

### Possible Solutions

1. Fully separate model per tier.

   Each tier has its own history encoder, candidate encoder, scorer, critic,
   optimizer state, and frozen rollout snapshot.

   Strength: conceptually simple per-tier PPO bookkeeping.

   Weakness: poor parameter sharing, likely data inefficiency, awkward when
   tiers appear/disappear dynamically.

2. Fully shared model with tier embedding.

   One model handles every tier, and tier id/context is part of the input.

   Strength: maximal parameter sharing and simpler global optimization.

   Weakness: may blur tier-local action semantics and make old/new snapshot
   management more delicate.

3. Shared record encoders plus tier-specific policy/value heads.

   A shared universal record encoder and quotient aggregation stack produce
   state/action tokens. Each live tier has a small policy/value surface,
   including its own trainable head and frozen rollout snapshot.

   Strength: respects the Project Owner's per-tier policy intuition while
   preserving quotient-coupled representations.

   Weakness: more bookkeeping than a single shared model.

4. Shared trunk plus tier-specific adapters.

   A global trunk handles history, with small per-tier adapters/heads.

   Strength: a middle ground. Weakness: more architecture choices up front.

### Recommendation

Earlier recommendation, now superseded by the Project Owner turn below:

```text
shared universal record encoder;
shared quotient aggregation stack;
per-tier policy/value surfaces;
per-tier rollout snapshots.
```

Corrected blueprint direction after discussion:

```text
Each tier has a separate policy model and a separate frozen rollout snapshot.
Tier policies are not explicitly parameter-coupled.
The shared part is architecture/schema/code shape, not learned weights.
Capacity should decay in a controlled way as tier index increases down the
tower.
```

The blueprint should define exactly what is per-tier:

```text
current policy head or adapter
frozen rollout head or adapter
optimizer parameter group or state
candidate mask/output surface
rollout buffer partition
metrics partition
```

And exactly what is shared:

```text
record schema definitions
deterministic tokenizer/schema code, if useful
model architecture family
device/tensorization utilities
artifact schema code
```

### Conversation Slots

#### PO Turn 1
There is a separate policy for each tier. They are not explicitly coupled in any way. The only important relationship between them is that they all have the same underlying architecture, and the cpaacity should drop in some controlled way as we move down tower, like geometric drop in capactity or something. Like `gamma**n*cap_0` or something.


#### Codex Turn 1

Understood. This resolves the parameter-sharing question more strongly than my
recommendation did.

The blueprint should lock:

```text
one separate policy model per tier;
one separate frozen rollout policy snapshot per tier;
no explicit learned parameter sharing between tier policies;
same architecture family across tiers;
controlled capacity decay as tier index increases down the tower.
```

So `policy_k` and `rollout_policy_k` are not just named decision surfaces over
a shared trunk. They are separate tier-specific models. The commonality is
architectural and contractual, not shared weights.

A good first capacity rule can be stated parametrically:

```text
capacity_k = max(min_capacity, round(capacity_0 * gamma_capacity**k))
```

where:

```text
k = tier index;
k = 0 is uppermost;
k -> k + 1 moves down the tower;
0 < gamma_capacity <= 1 controls geometric capacity decay.
```

The blueprint should not hard-code the exact capacity formula as
mathematically final, but it should include this as the first default schedule
and artifact:

```text
capacity_schedule_id
capacity_0
gamma_capacity
min_capacity
per_tier_hidden_dim
per_tier_layer_count
per_tier_parameter_count
```

This also means the previous "shared universal record encoder" recommendation
should be removed or demoted. We can still use the same deterministic record
schema and tokenizer code across tiers, but learned model parameters should be
separate unless you explicitly reopen that decision.

#### PO Turn 2

#### Codex Turn 2

## Issue 4: Whether The First Blueprint Includes Direct PPO

### Why This Matters

The folder started from "real GPU PPO training loop" and later became focused
on full-tower PPO. A direct PPO baseline is still important for eventual
comparison, but including it in the same blueprint may either clarify the
shared PPO infrastructure or distract from the harder tower model design.

The blueprint needs to decide whether direct PPO is:

```text
inside first scope
named shared infrastructure only
explicitly deferred
```

### Possible Solutions

1. Tower-only first blueprint.

   Blueprint only full-tower PPO. Direct PPO is deferred.

   Strength: avoids re-centering the work on direct control after the PO
   explicitly pushed toward full tower.

   Weakness: less immediate comparison structure.

2. Shared PPO infrastructure plus tower-first implementation.

   Blueprint the PPO engine, rollout buffer, checkpoints, GAE, update loop,
   artifacts, and readouts in an arm-agnostic way, but make full-tower PPO the
   first model/control arm. Direct PPO is described only as a future consumer
   of the same engine.

3. Full paired direct-vs-tower blueprint.

   Include both direct PPO and tower PPO in the first serious blueprint.

   Strength: comparison-ready. Weakness: more scope and more unresolved direct
   action-law design.

### Recommendation

Earlier recommendation, now superseded by the Project Owner turn below:

```text
shared PPO engine, tower-first model/control arm
```

Corrected blueprint direction after discussion:

```text
Direct is not a separate unresolved policy-design family.
Direct is the no-contraction schema arm.
Nontrivial tower arms are nontrivial contraction-schema arms.
The same PPO/evaluation machinery should handle both by schema selection.
```

### Conversation Slots

#### PO Turn 1
This is stupid. Direct will be contraction schema with no contrations.  Right. We already went over this multiple times for a previous evaluation.

#### Codex Turn 1

Yes. The direct arm should not be a separate direct-control theory bolted onto
this design. It is the no-contraction schema case, exactly as in the previous
schema-comparison pattern.

The corrected blueprint rule should be:

```text
Direct = contraction schema with no contractions.
Tower = contraction schema with nontrivial contractions.
Both run through the same general training/evaluation machinery.
```

So direct PPO is in scope, but not as a new factorized per-robot direct policy
design. It is the same structured record/history candidate-scoring PPO
framework applied to the no-contraction tower. In that case, the active action
surface is just the `G^0_t` outgoing action surface under the no-contraction
schema.

This is cleaner than my option list. The blueprint should describe arms by
schema:

```text
schema0_no_contraction:
  direct/no-contraction arm

schema1_or_later:
  nontrivial tower arm
```

and it should reuse the same artifact/readout language we already established
for counterpoint and PlateSupport comparisons.

#### PO Turn 2

#### Codex Turn 2

## Issue 5: No Executable Action Surface

### Why This Matters

Hardcoded tower traversal may fail to find a usable tier-local action surface,
or it may reach a surface where the candidate mask is empty. PPO cannot sample
from an empty distribution, and the training loop must not hide this by
inventing fallback actions.

The design must distinguish:

```text
no executable tier exists
active tier exists but Out_k(s_t) is empty
Out_k(s_t) exists but mask removes every candidate
lift candidates disappeared or are stale
runtime reached NO_AVAILABLE_ACTION
bug/invariant failure
```

### Possible Solutions

1. Diagnostic truncation.

   End the episode as a diagnostic truncation with a structured failure reason
   and no PPO action sample for the failed decision point.

2. Self-loop/stay action.

   Add a synthetic "stay" or no-op action when mask is empty.

   This keeps rollout length simple but changes the action surface and may
   teach the model artifacts of failure handling rather than tower control.

3. Continue hardcoded traversal to an executable tier.

   If the current tier has no executable action surface, let upstream
   `state_collapser` traversal continue according to its normal
   `tier_is_executable_from_state` semantics until it reaches an executable
   tier or returns `NO_AVAILABLE_ACTION`.

   This is not a PPO fallback after sampling. It is hardcoded traversal before
   the PPO actor is called.

4. Record failure and continue environment time.

   Treat no-action as an environment event with reward/time semantics.

   This risks blurring traversal diagnostics with Warehouse seconds unless
   carefully justified.

### Recommendation

Earlier recommendation, now superseded by the repo check and Project Owner
turn below.

Corrected blueprint direction:

```text
Reuse the settled pointwise liftability semantics from prior BBB evaluations.
Hardcoded state_collapser traversal skips non-executable tiers before PPO
sampling.
The PPO actor is called only at a nonempty pointwise executable action surface.
Execution uses strict executable lift candidates from the current concrete
state, with no representative fallback.
If no executable tier/action exists, record NO_AVAILABLE_ACTION as a runtime
diagnostic, not a PPO sample.
```

Do not invent synthetic actions in the first blueprint.

The rollout should record:

```text
diagnostic_failure_kind
controller_events_since_previous_sample
active_tier
tower_position_key
candidate_count
executable_candidate_count
mask_empty
bootstrap_allowed = false unless explicitly decided otherwise
```

### Conversation Slots

#### PO Turn 1
I think we completely solved this for previous evaluations. Please go over this repo extensively to find how we have already solved this. There may be multiple solution attempts that finally settle on one choice. But I really think you're re-inventing the wheel here.

#### Codex Turn 1

I checked the repo, and you are right. We already solved most of this in the
counterpoint and PlateSupport tower work, and this section should import that
settled rule instead of redesigning it.

The prior solution has three parts.

First, the tower runtime gets a pointwise executability predicate and skips
non-executable tiers during traversal:

```text
tier_is_executable = tier_is_executable_from_state(tier, current_base_state)
```

The counterpoint one-third tower diagnostics explicitly say the runtime should:

```text
skip non-executable tiers;
descend toward the selected executable unclosed tier;
lift out of a non-executable active tier before action choice;
return NO_AVAILABLE_ACTION if no executable tier exists.
```

Second, the action surface is pointwise executable from the current concrete
state. In the implemented counterpoint adapter, the executable action cells are
computed by filtering quotient action cells through strict executable lift
candidates:

```text
pointwise_executable_action_cells(tier, state_cell)
  = action cells whose executable_lift_candidates(...)
    are nonempty from the current concrete state
```

Third, execution must not use representative fallback. The v0.7.2
pointwise-liftability handoff settled the rule:

```text
fetch pointwise executable vocabulary;
call executable_lift_candidates(tier, action_cell, current_state);
choose the first strict executable lift candidate by default;
record representative candidates only as diagnostics;
do not fallback to action_cell_members(...) for execution.
```

There is even a regression test enforcing that representative-only candidates
are not used for execution.

So for this PPO blueprint, the correct rule is not "what should PPO do with an
empty mask?" The rule is:

```text
The PPO actor is only called after hardcoded traversal presents a nonempty
pointwise executable action surface.
```

If no executable tier/action exists, that is a runtime/control diagnostic:

```text
NO_AVAILABLE_ACTION
```

not a PPO sample. If the actor boundary receives an empty candidate surface
anyway, that is an invariant violation or stale-surface race and should be
recorded as a diagnostic failure, not handled by synthetic fallback. This
section should be rewritten in the blueprint as "reuse settled pointwise
liftability and no-representative-fallback semantics."

#### PO Turn 2

#### Codex Turn 2

## Issue 6: Dynamic Graph Growth And PPO Freezing Rules

### Why This Matters

Warehouse Gridlock has a discovered state-action graph:

```text
G^0_t
```

and a changing contraction/tower structure:

```text
Sigma_t^bullet
G_t^bullet
```

During a PPO run, discovery may add states/actions, modify outgoing sets,
change candidate masks, create new non-degenerate tiers, or alter quotient
records. PPO, however, requires the old probability of the exact sampled
action under the exact old decision surface.

If the update recomputes `Out_k(s_t)` later from the live graph, it may compute
the probability ratio against the wrong action set.

### Possible Solutions

1. Freeze the entire graph/tower for each rollout batch.

   Discovery can happen only between PPO update cycles. During rollout, the
   tower is fixed.

   Strength: clean PPO semantics. Weakness: less natural for online discovery.

2. Allow discovery during rollout, but freeze each sampled decision surface.

   Each PPO sample stores its exact candidate ids, canonical order, mask,
   state/action record references or serialized records, and old log prob.

   Strength: supports online discovery while preserving PPO ratios. Weakness:
   more artifact and memory burden.

3. Freeze only model snapshots, recompute graph surfaces later.

   This is insufficient because the decision surface itself may change.

4. Periodic rebuild windows.

   Let discovery accumulate, then rebuild `G_t^bullet` and update model/tier
   surfaces at controlled synchronization points.

### Recommendation

Use option 2 for correctness, with option 4 as an implementation discipline:

```text
Every PPO sample stores the exact decision surface used at sampling time.
Graph/tower rebuilds happen only at named synchronization points.
PPO updates never recompute candidate order, masks, or local action indices
from the later live graph.
```

The blueprint should define:

```text
rollout_policy_snapshot_id
tower_snapshot_id_or_digest
decision_surface_snapshot_id
out_action_ids_in_order
out_mask
selected_local_index
selected_action_id
state_record_refs_or_serialized_records
action_record_refs_or_serialized_records
```

When new tiers appear, the blueprint should specify:

```text
initialize policy_k and rollout_policy_k at synchronization boundary
record initialization reason
do not insert a new tier policy mid-update without a manifest entry
```

### Conversation Slots

#### PO Turn 1
I thought about this. I don;t think it's an issue. It *does* mean that at early exploration intervals, radicla shifts in the geometry of downstairs tiers will upset the meaning of attention head embeddings and classifier performance, but once the geometry stabilises with exploration, the embeddings will be largely rigth and adjustable. Let me know if you understand.

#### Codex Turn 1

Yes, I understand. The graph/tower changing during early discovery is not a
conceptual blocker; it is part of the learning problem.

The important distinction is:

```text
representation stability problem:
  early exploration can radically change downstairs geometry, which can make
  learned embeddings and attention heads temporarily bad or stale.

PPO accounting problem:
  the update still needs the old log probability for the action sampled from
  the old decision surface.
```

Your point addresses the first one: the model can tolerate early instability,
and once exploration stabilizes the geometry, the embeddings should become
largely right and then adjustable. That is a learning-dynamics issue, not a
reason to freeze the entire graph or treat discovery as impossible.

The blueprint should therefore not frame dynamic graph growth as an unsolved
architecture issue. It should say:

```text
Discovery-driven geometry shifts are expected.
Early instability in tier representations is acceptable.
The model trains through this nonstationarity.
```

But it should still preserve the PPO bookkeeping invariant:

```text
for each PPO sample, store the candidate ids, canonical order, mask, selected
local index, selected action id, old log probability, and enough record refs
or serialized records to recompute the new log probability against the same
decision surface during the update.
```

So I would downgrade this from "possible blocker" to "known training-dynamics
feature plus a rollout-recording requirement."

#### PO Turn 2

#### Codex Turn 2

## Issue 7: Artifact Retention And Trace Policy

### Why This Matters

Warehouse runs have already produced artifact explosions. Serious GPU PPO can
produce much larger traces, especially if every step, candidate set, tensor
summary, and movie frame is retained.

The design must prove PPO is real without writing everything forever.

### Possible Solutions

1. Retain all step-level data.

   Best for debugging, unacceptable for long runs.

2. Retain summaries plus selected traces.

   Write per-update and per-episode summaries for all episodes, but retain
   full step/candidate traces only for selected episodes.

3. Retain rolling windows only.

   Keep recent detailed traces and summary history. This is compact but bad
   for reproducibility unless checkpoints and selected snapshots are strong.

4. Configurable retention classes.

   Use named retention policies:

   ```text
   smoke
   debug
   serious_train
   archive
   ```

### Recommendation

Use options 2 and 4 together.

The blueprint should define a default `serious_train` retention profile:

```text
always retain:
  training_config.json
  model_manifest.json
  device_manifest.json
  checkpoint_manifest.json
  ppo_update_summary.csv
  episode_summary.csv
  training_curve.csv
  advantage_summary.csv
  value_summary.csv
  action_distribution_summary.csv
  mask_admissibility_summary.csv
  readout_source.json

retain selected detailed traces:
  first episode
  final episode
  first success
  best reward so far
  every Nth episode by config
  diagnostic failure episodes up to a cap

do not retain by default:
  every candidate surface for every step
  every raw tensor
  every movie frame
  every full step event row for every episode
```

Movie generation should work only from retained traces, and should give a
clear error if the requested episode was not retained.

### Conversation Slots

#### PO Turn 1
I'm going to go with your recommendation, modulo all discussions here. We can adjust this later if necessary, like if we have memory or disk issues on a VM.

#### Codex Turn 1

Agreed. The blueprint should keep the recommended retention structure as the
first default and mark it as adjustable after we see real VM/storage behavior.

The important locked part is not the exact episode interval. The locked part
is:

```text
summaries for all episodes/updates;
selected detailed traces only;
movie generation only from retained traces;
clear error when a requested episode was not retained;
named retention profile in artifacts.
```

The future-tuning note should say:

```text
If VM disk, memory, or upload constraints become binding, adjust the retention
profile without changing PPO semantics.
```

So this is not a model-design blocker. It is a release/ops knob that should be
artifacted.

#### PO Turn 2

#### Codex Turn 2

## Issue 8: PPO Hyperparameters, Batch Shape, And GPU Defaults

### Why This Matters

The conceptual design can be correct while the first run is unusable because
the default batch sizes, rollout lengths, device policy, or checkpoint cadence
are wrong. The blueprint does not need final tuned values, but it should define
serious defaults and make them artifacted.

### Possible Solutions

1. Minimal debug defaults.

   Tiny rollout length, CPU-compatible, few PPO epochs. Good for tests, not
   serious training.

2. Serious single-GPU defaults.

   Moderate rollout batches, GPU if available, checkpoint by update interval,
   selected traces only.

3. Fully configurable only.

   No defaults, everything must be passed by CLI/config.

4. Named profiles.

   Provide profiles such as:

   ```text
   smoke_cpu
   debug_gpu
   serious_gpu
   long_gpu
   ```

### Recommendation

Use named profiles with explicit defaults, beginning with:

```text
smoke_cpu:
  correctness and CI-oriented

debug_gpu:
  short GPU run with detailed traces

serious_gpu:
  intended local long run with selected traces and checkpoints
```

The blueprint should not pretend hyperparameters are final. It should require
all of the following in artifacts:

```text
gamma
gae_lambda
clip_epsilon
entropy_coef
value_coef
learning_rate
max_grad_norm
target_kl
rollout_samples_per_update
ppo_epochs
minibatch_size
device_requested
device_actual
torch_version
cuda_available
model_parameter_count
checkpoint_interval_updates
trace_retention_policy
```

### Conversation Slots

#### PO Turn 1
I agree. We may adjust later. Mark this as a potential future issue.

#### Codex Turn 1

Agreed. Named profiles with explicit defaults should go into the blueprint,
and the exact values should be marked as future-tunable.

The blueprint should treat these as training-run configuration, not as
mathematical commitments. It should require that every run artifacts the
profile and all expanded values:

```text
profile_id
gamma
gae_lambda
clip_epsilon
entropy_coef
value_coef
learning_rate
rollout_samples_per_update
ppo_epochs
minibatch_size
device_requested
device_actual
checkpoint_interval
trace_retention_policy
```

Future issue:

```text
Tune PPO/GPU profiles after the first serious run shows actual throughput,
memory pressure, KL behavior, reward scale, and trace volume.
```

So this should remain visible in the blueprint, but it should not block
blueprint generation.

#### PO Turn 2

#### Codex Turn 2

## Readiness Assessment

After these gates are resolved, the project should be ready to generate the
full blueprint for:

```text
Warehouse Gridlock full-tower GPU PPO
with Tyler Foster structured record/history transformer policy family
and state_collapser hardcoded tower traversal semantics
```

If these gates are not resolved first, the blueprint can still be generated,
but it must carry them explicitly as open decisions and must not quietly
choose implementation behavior without Project Owner approval.
