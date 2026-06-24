# Warehouse Gridlock Hardcoded Tower Traversal And PPO Action Selection Discussion

## Purpose

This document replaces the earlier tower-traversing discussion. The earlier
version was built around a faulty assumption: that PPO would learn a policy
for tier traversal itself.

That is not the current design.

The current design point is:

```text
Tower traversal is governed by hardcoded state_collapser control/runtime logic.
PPO trains the action-selection policy exposed at the tier-local execution
surface reached by that hardcoded traversal.
```

This is a discussion document only. It is not a blueprint, not an
implementation workplan, and not implementation authority.

## Authority And Attribution

### Project Owner

The Project Owner corrected the central premise of this document:

```text
There is not a trainable policy that controls tier traversal.
Tier traversal is governed by hardcoded logic.
```

The Project Owner's current target remains a serious full-tower Warehouse
Gridlock PPO training design, not a fixed-tier smoke. The correction is that
"full tower" means the hardcoded tower runtime moves through the tower during
rollout, while the trainable PPO policy supplies decisions at the appropriate
action-selection surfaces.

### Codex

Codex's role is to align BBB's Warehouse PPO design with the actual
`state_collapser` architecture, not invent a parallel tower-control policy.

## Corrected Core Split

The design has two different control layers.

### Hardcoded Tower Traversal Layer

This layer decides where control lives in the tower and when to move between
tiers.

It is governed by `state_collapser` runtime/controller logic, especially:

```text
ActiveTierController.decide(...)
ExploitExploreTowerRuntime.step(...)
ActiveTierState.lift(...)
ActiveTierState.descend(...)
```

The relevant existing controller actions are:

```text
ControlAction.LIFT
ControlAction.DESCEND
ControlAction.TRAIN
ControlAction.EXPLORE
ControlAction.EXPLOIT_EXECUTE
ControlAction.NO_AVAILABLE_ACTION
```

For this design, PPO does **not** learn whether to choose `LIFT` or `DESCEND`.
Those tier-traversal choices are part of the hardcoded tower controller being
evaluated.

### Trainable Tier-Local Action Selection Layer

This layer is where PPO enters.

When the hardcoded traversal/controller reaches an executable tier-local
surface, the trainable policy supplies an action for that surface. In
`state_collapser` runtime terms, this corresponds to the place where the
runtime calls something like:

```text
learner.behavior_action(active_tier_state.tier_state, mode=mode)
```

and then sends the chosen action to the lift/resolve executor.

For Warehouse PPO, that `behavior_action` role should become a PPO actor
sampling from the tier-local action surface. The PPO sampled action is not
`LIFT` or `DESCEND`. It is the action selected at the active tier after the
hardcoded traversal has decided that action selection should happen.

## What Full-Tower Training Means Here

Full-tower training does **not** mean:

```text
PPO learns a policy over tier traversal.
```

Full-tower training means:

```text
The rollout runs through the full state_collapser tower runtime.
The hardcoded traversal logic may lift, descend, skip non-executable tiers,
train/update internal signals, and route execution to different tiers.
The PPO actor is invoked at the tier-local action-selection points produced by
that traversal.
The PPO rollout records enough tower context to train and interpret those
actions across the full tower.
```

So the tower is still fully involved. The trainable object is just not the
tier-traversal policy.

## Actual State-Collapser Control Semantics

The relevant `state_collapser` runtime shape is:

1. The runtime maintains an `ActiveTierState`.
2. It checks whether the active tier is executable.
3. If the tier is not executable, it lifts toward an executable tier using
   hardcoded runtime logic.
4. It asks `ActiveTierController.decide(...)` what controller action applies.
5. If the decision is `LIFT`, the runtime moves up one tier.
6. If the decision is `DESCEND`, the runtime moves down one tier.
7. If the decision is `TRAIN`, the runtime performs a learner update in the
   old reference loop.
8. If the decision is `EXPLORE` or `EXPLOIT_EXECUTE`, the runtime asks the
   learner/policy for a tier-local behavior action, then executes it through a
   lift/resolve executor.
9. The runtime records metrics and advances its active-tier state.

The PPO design should use this architecture as source of truth.

## Correct PPO Random Variable

The PPO random variable should be located at the tier-local execution surface.

The wrong random variable is:

```text
sampled_action = LIFT | DESCEND | TRAIN | ...
```

The corrected random variable is closer to:

```text
sampled_action = tier-local action chosen when hardcoded traversal reaches an
execution surface
```

Depending on the final tower action surface, this may be:

```text
action_cell_id
```

or:

```text
action_cell_index over the active tier's executable action vocabulary
```

or, if lift selection becomes learned later:

```text
(action_cell_id, lift_candidate_id)
```

That possible future extension would still not be a learned tier-traversal
controller. It would only mean learning a tie-break or choice inside an
already reached tier-local execution surface.

For first serious design, the likely clean target is:

```text
PPO samples an executable tier-local action cell.
The lift/resolve executor deterministically maps that action cell to a concrete
Warehouse move using state_collapser lift semantics.
```

That keeps PPO's log probability attached to the thing PPO actually sampled.

## What PPO Sees

Even though PPO does not choose traversal, it must see tower context.

The action-selection input should include:

```text
concrete Warehouse state
current_position_at_every_tier
active_control_tier
active tier state
action_mask for the tier-local executable action surface
runtime_snapshot
tower_position_key
diagnostics from traversal since the previous PPO sample
```

This is how PPO can learn actions that are useful in different tower contexts
without learning the traversal controller itself.

## PPO Rollout Semantics

The rollout stream needs two layers of records.

### Controller / Traversal Events

These are hardcoded runtime events:

```text
LIFT
DESCEND
TRAIN
NO_AVAILABLE_ACTION
EXPLORE
EXPLOIT_EXECUTE
automatic lift-to-executable-tier steps
```

They should be artifacted for interpretation, debugging, and evaluation of the
tower runtime. They are not automatically PPO action samples.

### PPO Action Samples

These occur when the hardcoded runtime reaches a tier-local action-selection
surface and asks the PPO actor for an action.

Each PPO sample should record:

```text
source ActionSelectionInput
active_control_tier
tower_position_key
tier-local action vocabulary
action_mask
sampled tier-local action
old_log_prob(sampled action)
value estimate
resolved lift/concrete action
reward from resulting Warehouse transition
target ActionSelectionInput
terminated
truncated
bootstrap_allowed
bootstrap_reason
controller events since previous PPO sample
```

This is the stream that PPO/GAE should train on.

## Time And Reward Semantics

The previous document blurred controller events, PPO samples, and Warehouse
seconds. The corrected design must keep them separate.

The important counters are:

```text
controller_event_index
ppo_sample_index
environment_second
```

These may differ.

The likely first rule is:

```text
LIFT/DESCEND/TRAIN traversal events do not directly consume Warehouse time.
Concrete Warehouse moves consume Warehouse time.
PPO rewards come from concrete Warehouse transitions produced by tier-local
action execution.
Traversal events between PPO samples are recorded as context/diagnostics.
```

If a future design wants traversal events to have shaped cost, that should be
a separate explicit design decision.

## What Happens To `TRAIN`

`ControlAction.TRAIN` exists in the current `state_collapser` reference
runtime, but PPO training is normally an outer optimization process over a
rollout buffer.

So this design must decide how to bridge the old reference runtime's `TRAIN`
event with PPO.

Current recommendation:

```text
Do not make TRAIN a PPO-sampled action.
Do not treat PPO optimizer updates as environment actions.
During PPO rollout, either configure the runtime so TRAIN does not occur, or
make TRAIN a hardcoded maintenance event that is recorded but not a PPO sample.
Run PPO updates outside the tower traversal loop after collecting rollout
samples.
```

If `TRAIN` has unavoidable state-collapser semantics that affect traversal,
the design should document that explicitly and preserve the event as a
runtime diagnostic.

## What Should Use State-Collapser Directly

BBB should not copy these concepts:

```text
ActiveTierController
ActiveTierState
ControlAction
ExploitExploreTowerRuntime traversal semantics
LiveRuntimeView
ActionSelectionInput
TrainingTransition
PartitionTower executable action/lift queries
PathFiber masks, if used
LinearizationConfig / EncodingRegistry / LinearizationReport
```

BBB may need Warehouse-specific adapters, but those adapters should be thin
consumers of upstream semantics. If an upstream surface cannot support this
PPO use case cleanly, the design should record the gap and decide whether the
fix belongs in `state_collapser`.

## Existing BBB Precedent

BBB's counterpoint tower-control runner already demonstrates the rough wiring:

```text
ExploitExploreTowerRuntime
ActiveTierController
move_down / move_up
tier_is_executable
LiftResolveExecutor
controller event rows
lift/fiber event rows
runtime snapshots
```

Warehouse PPO should reuse this architectural shape where it matches, but
replace the old tabular/tower learner action-selection role with PPO rollout
collection and PPO actor decisions.

The key difference is:

```text
counterpoint old runner: learner.behavior_action supplies tabular actions
Warehouse PPO runner: PPO actor supplies tier-local sampled actions and
records log probabilities/value estimates
```

The hardcoded traversal remains.

## Remaining Design Decisions

### 1. Exact Tier-Local Action Surface

What does the PPO actor sample at a tier-local execution point?

Likely first answer:

```text
an executable action-cell index/id at the active tier
```

Open follow-up:

```text
Should lift candidate choice remain deterministic, or should it eventually be
part of the sampled action?
```

### 2. Shared Policy Across Tiers Or Tier-Specific Heads

Options:

```text
one shared PPO actor with active-tier/tower-context embeddings
one shared trunk with tier-specific action heads
separate actor per tier
```

Given the full-tower goal, a shared actor with explicit tier/tower context is
probably the cleanest first design, but the blueprint must choose.

### 3. Rollout Collection Boundary

Does one PPO sample correspond exactly to one concrete Warehouse move, or can
one PPO sample include an abstract action that resolves through multiple
controller events?

Current recommendation:

```text
one PPO sample = one tier-local action selection that resolves to one concrete
Warehouse transition
```

Hardcoded traversal events before that sample are context, not samples.

### 4. Handling No Executable Tier-Local Surface

If hardcoded traversal cannot find an executable tier/action surface, the
rollout should record:

```text
NO_AVAILABLE_ACTION
mask_empty
tier_not_executable
diagnostic truncation or failure reason
```

It should not invent a fallback policy.

### 5. Direct Baseline Alignment

Direct PPO should still be a joint coordinated policy over concrete Warehouse
ensemble behavior. That is separate from tower traversal.

The tower PPO comparison asks:

```text
Given hardcoded state_collapser tower traversal and live-lift/action-cell
surfaces, does PPO over the reached tier-local action surfaces learn better
than direct PPO over concrete ensemble actions?
```

The comparison does not ask:

```text
Can PPO learn a better tier traversal controller than state_collapser?
```

## Corrected Design Statement

The corrected current design spot is:

```text
Warehouse full-tower PPO uses state_collapser's hardcoded tower traversal
logic. PPO does not choose LIFT, DESCEND, or tier traversal. The PPO actor is
called when the traversal reaches a tier-local execution/action-selection
surface. It samples an executable tier-local action under the current tower
context, records the log probability and value estimate, and trains from the
resulting concrete Warehouse transition. Traversal events are artifacted as
runtime context and diagnostics, not treated as learned PPO actions.
```

## Turn Space

### PO Turn

So one ciritical first issue is that there needs to be a policy model for each tier. The training framwork needs to have the ability to create quotient graphs, and then introduce a policy for each. This requires some agnosticism, and it requires looking carefully in `state_collapser` for what already exists.

### Codex Turn

Yes. This is the right correction, and it is different from the bad "train a
tier traversal controller" idea.

The design should now separate three things:

```text
1. state_collapser creates and maintains the quotient tower.
2. hardcoded state_collapser traversal decides which tier is active.
3. BBB/PPO owns a policy bank with an action-selection policy for each tier
   that can become active.
```

So when you say "there needs to be a policy model for each tier," I read that
as:

```text
For every quotient tier produced by the current tower construction, BBB must be
able to attach a trainable action-selection model whose action vocabulary and
mask are the tier-local executable action surface at that tier.
```

That does **not** mean:

```text
PPO chooses LIFT/DESCEND or decides tower traversal.
```

It means:

```text
When hardcoded traversal lands at tier k and asks for a behavior action, the
training framework dispatches to policy[k].
```

The policy bank needs to be agnostic in several ways:

```text
tower depth is not fixed before construction;
tier ids are discovered from the built PartitionTower/TowerRuntime;
action-cell vocabularies differ by tier and by current tier-local state;
masks are tier-local and state-dependent;
some tiers may be non-executable or degenerate;
some tiers may share a model architecture while still having separate
parameters, optimizer state, metrics, and checkpoints.
```

From the quick `state_collapser` pass, the important existing surfaces are:

```text
TowerRuntime / PartitionTower:
  own quotient-tower construction, updating, current positions, quotient tier
  views, action cells, executable action cells, and lift candidates.

LiveRuntimeView:
  carries the current base state, current position at every tier, active
  control tier, last control action, and partition tower view.

ActionSelectionInput:
  is already the package-facing input object for action selection. It includes
  observation, runtime snapshot, tower_position_key, action_mask,
  active_tier_state, stage/fiber context, and diagnostics.

TrainingTransition:
  is already the package-facing transition handoff object. It records source
  input, chosen action, reward, target input, bootstrap flags/reasons, active
  tier, tower_position_key, and diagnostics.

LinearizationConfig / EncodingRegistry / TorchDecisionBatch /
TorchTransitionBatch:
  already define a semantic-to-numeric-to-Torch boundary.

TierLearner:
  is the current active-tier learner protocol used by the hardcoded traversal
  runtime, but its old `behavior_action(state, mode)` surface is probably too
  narrow for serious PPO unless wrapped carefully or extended upstream.
```

That last point is the main design pressure. The current `TierLearner`
contract is useful because it is exactly where hardcoded traversal asks for
behavior at the active tier. But PPO needs more than the old tabular learner
needed:

```text
active tier id
ActionSelectionInput
tier-local action vocabulary
action mask
sampled action
old log probability
value estimate
entropy/logits/probabilities if artifacted
optimizer/checkpoint identity for policy[k]
```

So the likely architecture is:

```text
WarehouseTierPolicyBank
  owns policy[k] for each realized quotient tier k
  creates policy[k] lazily or after tower construction
  exposes action selection for the active tier
  records log_prob/value/entropy in PPO rollout records
  keeps separate optimizer/checkpoint/metric state per tier, unless an explicit
  shared-trunk design is chosen

StateCollapserTowerAdapter
  uses TowerRuntime / PartitionTower / LiveRuntimeView
  builds ActionSelectionInput for the active tier
  gets tier-local action vocabulary and mask from state_collapser surfaces
  calls WarehouseTierPolicyBank.select(input)
  resolves the selected action through state_collapser lift/resolve semantics
```

This gives the framework the agnosticism you are pointing at. It should not be
hardcoded to "Warehouse has N tiers" or "tier 3 has this head shape." It should
consume the tower that `state_collapser` actually builds, then provision and
train policies against the tier surfaces that actually exist.

There are two possible parameter-sharing choices, and the blueprint should
name one:

```text
separate model per tier:
  cleanest interpretation of "policy model for each tier";
  easiest attribution, metrics, checkpointing, and ablation;
  possibly more parameters.

shared trunk with tier-specific heads:
  still a policy per tier at the action-surface level;
  shares representation across tiers;
  more complex bookkeeping and interpretation.
```

My recommendation for the first serious design is:

```text
Start with separate policy modules per tier, using a common architecture class
and common tensorization contract. Allow a later shared-trunk option, but do
not make the first blueprint depend on it.
```

The next concrete design task should be a short inventory table:

```text
Need: construct quotient tower
Use: state_collapser TowerRuntime / PartitionTower
BBB adds: Warehouse configuration and artifact hooks

Need: discover tier count and tier ids
Use: LiveRuntimeView.current_position_at_every_tier and PartitionTower views
BBB adds: policy-bank provisioning keyed by tier

Need: tier-local action vocabulary and masks
Use: PartitionTower / training stage / action surface helpers where applicable
BBB adds: Warehouse adapter if the exact active-tier PPO surface is missing

Need: semantic PPO input and transition
Use: ActionSelectionInput and TrainingTransition
BBB adds: PPO log_prob/value/advantage fields around these records

Need: Torch tensors
Use: LinearizationConfig, EncodingRegistry, TorchDecisionBatch,
TorchTransitionBatch where they fit
BBB adds: model-specific tensor fields only when upstream does not own them
```

This also changes the wording in the eventual blueprint. The core design
object is not:

```text
one tower PPO policy
```

It is:

```text
a PPO-managed tier-policy bank attached to a state_collapser-built quotient
tower, with hardcoded traversal dispatching action-selection calls to the
active tier's policy.
```

That formulation preserves the hardcoded traversal correction while also
honoring your new point: a real full-tower training framework cannot have only
one flat Warehouse policy pretending the tower exists. It needs one policy
surface per quotient tier, created from the actual tower, and trained through
the semantic surfaces `state_collapser` already provides.

### PO Turn

I just think you take off too fast. Think about the `state_collapser` underlying math? I think I need to think through the Young-diagram quotienting-representing logic a bit... it should actually apply to the poligy model itself... like... aggregation of all sorts is *really* easy for tensor-based models, so we could easily make *extremely* light-weight coupling to model that just like sums or maxes or whatever asa representation of coset behavior... need to think more carefully about this it actually involves the mathmatics, not just code... Actually, you are kind of bad at coupling mathematical models to realized code.

### Codex Turn

Yes. This is a real correction. My last turn still moved too quickly from
"there are quotient tiers" to "there is a policy bank," and that skips the
actual mathematical modeling question.

The more careful thought is:

```text
The Young-diagram quotient structure should not only decide which policy
surface exists. It should help define the representation that the policy sees.
```

In `state_collapser`, the partition tower is not just a list of quotient
graphs. It stores a tower of partitions with explicit parent/child information:

```text
state cells at tier t
parent state cell at tier t+1
previous/child cells that merged into a coarser cell
outgoing action collections attached to state cells
action cells inside those outgoing collections
member base edges and lower action cells inside action cells
internal edges produced by contraction
```

That is already almost a tensor aggregation scaffold. The model should not
treat a quotient state cell as an opaque id if the tower knows which lower
cells, base states, and outgoing action structures it represents.

A better mathematical first pass is:

```text
tier-0 state/entity embeddings
  -> aggregate along quotient parent maps
  -> tier-k state-cell embeddings

tier-0 edge/action embeddings
  -> aggregate along action-cell membership maps
  -> tier-k action-cell embeddings

current tier state-cell embedding + candidate action-cell embedding
  -> logit for that tier-local action
```

In a schematic form:

```text
h_0(s) = base/entity representation of concrete state member s
e_0(edge) = base/action representation of concrete edge/action

h_{t+1}(C) = Agg_state({h_t(c) : parent_t(c) = C}, features(C))
e_{t+1}(A) = Agg_action({e_t(a) or e_0(edge) : member of A}, features(A))

logit_t(a | c, context) =
  score_t(h_t(c), e_t(a), tower_context, warehouse_context)
```

Then the policy at tier `t` is:

```text
pi_t(a | c, context) = masked_softmax_a(logit_t(a | c, context))
```

where the mask is still the tier-local executable action surface from
`state_collapser`.

This is much better than saying "create a separate policy per tier" as if each
tier policy were unrelated. A better phrase is:

```text
one policy surface per tier, with representations coupled through the quotient
tower's aggregation maps
```

That coupling can be extremely lightweight at first. The obvious aggregation
operators are:

```text
sum:
  preserves multiplicity and coset size signal;
  useful when the number of lower states/actions matters.

mean:
  gives an average coset behavior signal;
  useful when we want size normalization.

max:
  gives existence/salience signal;
  useful when any strong lower feature should make the coarser cell visible.

sum + mean + max concatenated:
  cheap and expressive;
  probably a good first non-clever choice.

small learned attention/pooling:
  more flexible;
  should come later unless fixed aggregators are insufficient.
```

This matters mathematically because the quotient map is doing exactly the kind
of identification that a representation map should respect. If a coarser cell
is a coset of lower cells, then the model's coarser representation should be
some explicit, artifacted function of the lower representations and coset
membership, not just a freshly learned id embedding with no memory of the
quotient.

So the right design object is not merely:

```text
policy[k]
```

It is closer to:

```text
QuotientRepresentationStack:
  build tensor representations for every tier using state_collapser's
  state-cell and action-cell membership maps

TierPolicySurface[k]:
  score outgoing executable action cells at tier k using those representations

PPOTrainingLoop:
  when hardcoded traversal reaches tier k, sample from TierPolicySurface[k]
```

This preserves the earlier correction:

```text
PPO still does not learn tier traversal.
```

But it improves the model story:

```text
The trainable policy is tower-aware because the tensor representation itself is
constructed by aggregating through the Young-diagram quotient structure.
```

There is also a possible vertical-consistency question that we should not rush
past. If tier `t+1` action cells aggregate tier `t` action cells, then we might
eventually want consistency losses or diagnostics such as:

```text
coarse value roughly agrees with aggregated lower-tier values;
coarse action logits roughly agree with projected lower-tier action logits;
advantages by tier do not contradict obvious quotient projections;
high-tier policy behavior can be explained as an aggregation of lower-tier
behavior.
```

I am not saying to implement those now. I am saying they are the mathematical
questions that should be visible before we write the blueprint, because they
are exactly where the Young-diagram quotienting logic touches the policy model.

The immediate design note I would carry forward is:

```text
Before blueprinting the PPO model, define the quotient-to-policy
representation map. The model should consume state_collapser's state-cell,
action-cell, parent/child, member-edge, and action-mask tables as structured
aggregation data. Tensor aggregation should be the first-class bridge from the
mathematics to the policy model.
```

That is the slower, more correct frame. The implementation can still be simple,
but the simplicity should come from using the quotient math directly, not from
flattening it away.

### PO Turn

I'm going to sketch out a mathematical model. We have some real time updating state action graph $G^{0}_{t}$. Some contraction scehma $\Sigma^{\bullet}_{t}$, then we get a tower $G^{\bullet}_{t}$. Think of states in $G^{\bullet}_{t}$ as being *like* `JSON`s with all kinds of $\text{Out}(s)$ etc. We `__init__` a transformer model for each non-degenerate tier of $G^{\bullet}_{t}$. THen we just use some universal embedding of these "state `JSON`'s" to get our tokens. Then one thing the transformer model is doing is learning embeddings of these tokens. THen the question is more about just representing legal actions for liek the whole ensemble... the maybe makes it look like... the model needs a way to distribute over $\text{Out}(s)$ given $s$.

### Codex Turn

Yes. This model is much closer to the right object.

I would restate your sketch like this:

```text
G^0_t:
  the currently discovered concrete state-action graph at real time t

Sigma^bullet_t:
  the current contraction schema/tower-building data

G^bullet_t:
  the current quotient tower produced from G^0_t and Sigma^bullet_t

For each non-degenerate tier k of G^bullet_t:
  initialize or maintain a tier policy model M_k

For each current tier state s in tier k:
  build a structured record R_k(s), roughly "state JSON"
  build structured records R_k(a) for each a in Out_k(s)
  use M_k to define a distribution over Out_k(s)
```

The important shift is that the model is not really "output a fixed-size action
vector." It is:

```text
given a structured state record and a variable set of legal outgoing action
records, score each outgoing action record and softmax over Out(s)
```

So the action law is:

```text
pi_k(a | s) =
  softmax_{a' in Out_k(s)} score_k(EmbedState_k(s), EmbedAction_k(a'), context)
```

or more explicitly:

```text
state_tokens  = UniversalEncode(R_k(s))
action_tokens = [UniversalEncode(R_k(a)) for a in Out_k(s)]

context = Transformer_k(state_tokens, optional tower/context tokens)
logit_a = Score_k(context, action_tokens[a])

pi_k(. | s) = masked_softmax(logits over Out_k(s))
```

That fits the "state JSON" intuition well, with one caution: in implementation
we probably should not embed arbitrary raw JSON strings. The right first
surface is a canonical structured record that can serialize to JSON for
artifacts but has typed fields for the model:

```text
state cell id / tier id
member counts
current concrete representative or active concrete state, if relevant
parent / child cell references
reward summaries
outgoing action count
internal-edge summaries
liftability / executability summaries
warehouse entity features projected into this cell
```

For actions:

```text
action cell id / tier id
source state cell
target state cell
member edge count
lower action-cell membership summaries
base concrete action summaries
lift candidate summaries
invalid / executable / masked status
reward or transition summaries where available
```

This is the bridge between the mathematical object and code. The state/action
records are "JSON-like" because they are structured semantic records, but the
model sees a deterministic tensorization of those records.

This also resolves a lot of the full-action ensemble confusion. At tier 0,
`Out_0(s)` may contain concrete legal ensemble actions. At higher tiers,
`Out_k(s)` contains quotient action cells. In both cases the policy form is the
same:

```text
distribute over the legal outgoing actions of the current tier state
```

The only difference is what an outgoing action record means at that tier.

This gives a clean answer to:

```text
How does the model represent legal actions for the whole ensemble?
```

It does not need a permanent output neuron for every possible ensemble action.
Instead, legal ensemble actions or action cells are presented as a candidate
set:

```text
Out(s) = {a_1, ..., a_m}
```

and the model scores the candidates:

```text
logits = [score(s, a_1), ..., score(s, a_m)]
pi = softmax(logits)
```

For PPO this is very clean:

```text
sampled_action = one element of Out(s)
old_log_prob = log pi_old(sampled_action | s, Out(s))
new_log_prob = log pi_new(sampled_action | s, Out(s))
ratio = exp(new_log_prob - old_log_prob)
```

That means the variable-size `Out(s)` is not a problem. It is exactly a
candidate-scoring policy. Padding/masks are just batching mechanics.

The dynamic-time issue also becomes clearer. Since `G^0_t`, `Sigma^bullet_t`,
and `G^bullet_t` can change as exploration discovers more graph, the policy
model should not require a fixed state/action vocabulary known at program
start. It should require a fixed **record schema** and fixed **encoder
architecture**:

```text
new state/action record appears
  -> encode by the same universal record encoder
  -> score by the tier model
  -> include in Out(s) when legal
```

So "init a transformer per non-degenerate tier" means:

```text
initialize model parameters for tier k when tier k becomes a live
non-degenerate policy surface;
continue using those parameters as new state/action records appear in that tier;
do not reinitialize simply because the discovered graph grows.
```

There is still a subtle design point about whether tier models are completely
independent. Your aggregation thought suggests they should not be conceptually
independent even if they are separate modules. A good first mathematical
contract might be:

```text
Each non-degenerate tier has its own policy head or model M_k.
The input representations for M_k are produced by a shared quotient
representation procedure that aggregates lower-tier/base information through
the Young-diagram tower.
```

So the tier-specific part is the policy distribution:

```text
pi_k(. | s)
```

but the representation pipeline is tower-coupled:

```text
R_0 -> aggregate -> R_1 -> aggregate -> ... -> R_k
```

That seems like the right compromise between:

```text
policy model for each tier
```

and:

```text
do not ignore the quotient mathematics by treating every tier as an unrelated
flat graph.
```

The immediate next mathematical question may be:

```text
What exactly is in R_k(s) and R_k(a)?
```

I would not jump to architecture until we have at least a first draft of those
record schemas. Once those records are clear, the transformer shape becomes
much less mysterious: it is a candidate-scoring transformer over structured
state/action records, with one distribution over `Out(s)`.

## Tyler Foster Model Proposal: One-Tier Transformer Over Structured State/Action Records

### Attribution

This model family was proposed by Tyler Foster. The architectural idea, the
state/action-history framing, the use of richly encoded state/action records,
the transformer-over-history shape, and the distribution-over-\(\mathrm{Out}(s_t)\)
problem statement should be attributed to Tyler Foster.

The following section is consultant-authored explanatory prose about Tyler
Foster's proposal. It is not a Project Owner transcript.

### Core Proposal

For one tier \(G^k_t\), the model treats discovered states and edges as richly
encoded semantic records. These records are JSON-like in the engineering sense:
they are structured, serializable objects with stable fields, not opaque ids.
For example, a state in \(G^k_t\) might contain:

```text
{
  state_coset: [<state ids>],
  out_hom: [<edge ids>],
  1_hop: [<...>],
  ...
}
```

plus time-step information and any additional local/tower facts needed by the
model. Edge/action records would be similarly structured, carrying fields such
as source state id, target state id, edge/action label, tier id, edge identity,
liftability or executability facts, and other `state_collapser` metadata.

The proposal then uses a universal embedding / UAE-style encoder to turn those
structured records into time-step-independent tokens:

```text
state record -> state token
edge/action record -> edge/action token
```

For the current tier, the rollout supplies a state history and action history:

```text
state_hist = (s_0, s_1, s_2, ..., s_t)
act_hist   = (a_0, a_1, ..., a_{t-1})
```

The proposal acknowledges an on-policy/off-policy issue around how those
histories were generated, but brackets that issue for the purpose of describing
the model architecture.

The proposed tier model is transformer-shaped. It uses `state_hist` and
`act_hist` as the main sequential objects. The transformer internals are
ordinary transformer machinery, but the action-history positional encoding is
not just a sinusoidal or learned time-step encoding. Each action token should
also receive information derived from the action's source state and target
state. In other words, an action token is represented as something closer to:

```text
action semantic token
+ time-step positional encoding
+ source-state encoding
+ target-state encoding
```

This is important because actions in the state-action graph are morphisms or
edges between states, not free-floating labels. The model should be able to
learn from the fact that an action occurred at a time and connected a specific
source representation to a specific target representation.

The remaining design problem in Tyler's proposal is the distribution over
outgoing actions. The classifier at the end should give a distribution over:

```text
Out(s_t)
```

The edge/action encodings can carry stable ids and indices inside their
structured records, so the selected action can always be tied back to the
underlying `state_collapser` edge/action object. The open issue is how to size
and mask the output so that the model learns a probability distribution over
the legal outgoing actions of the current tier state.

### Consultant Interpretation

The important feature of Tyler's proposal is that it is not a generic
transformer applied near a graph. It is a transformer over semantically encoded
state and edge/action records from the current quotient tier.

The preserved architecture is:

```text
state JSON-like record -> universal state token
edge/action JSON-like record -> universal edge/action token

state_hist = (s_0, ..., s_t)
act_hist   = (a_0, ..., a_{t-1})

tier model M_k consumes the state/action history streams
candidate head produces pi_k(. | s_t) over Out_k(s_t)
```

The cleanest resolution of the output-vector/masking issue is probably not a
fixed global output vector over every edge ever discovered in tier `k`. Instead,
the model should use a candidate-scoring head over the current outgoing set:

```text
Out_k(s_t) = (a_1, ..., a_m)
```

where the tuple order is canonical and artifacted. Then:

```text
c_t       = contextual representation of the current decision state
u_i       = encoded/action-contextualized token for candidate a_i
logit_i   = score_k(c_t, u_i)
mask_i    = legal/executable flag for a_i
pi_k(a_i | s_t) = masked_softmax_i(logit_i)
```

This is still a distribution over \(\mathrm{Out}(s_t)\). The difference is
that the output vector is local to the current candidate set instead of global
to the whole discovered tier graph. In implementation, batches can pad these
local candidate lists to a maximum width and use a boolean mask.
Mathematically, the distribution remains:

```text
pi_k(. | s_t) on Out_k(s_t)
```

This keeps PPO clean:

```text
old_log_prob = log pi_old(selected a_i | s_t, Out_k(s_t))
new_log_prob = log pi_new(selected a_i | s_t, Out_k(s_t))
```

The edge/action record can still carry stable ids and indices. I would treat
those as:

```text
stable action identity:
  used for artifacts, replay, and tying an action token back to
  state_collapser objects

local candidate index:
  used for the current masked softmax over Out(s_t)
```

So the selected action record should store both:

```text
selected_action_id
selected_local_out_index
out_action_ids_in_order
out_mask
old_log_prob
```

That makes movie/replay/artifact work possible while keeping the neural head
simple.

The source/target positional encoding idea for action tokens is an important
part of the proposal. An action token should probably contain at least:

```text
edge/action semantic token
time-step positional encoding
source-state token or source-state positional/projection encoding
target-state token or target-state positional/projection encoding
tier id / quotient-level encoding
```

That gives the model a chance to learn that actions live between states, not
just in an action vocabulary.

There are several equivalent implementation shapes that can preserve Tyler's
model family:

```text
single interleaved sequence:
  [s_0, a_0, s_1, a_1, ..., s_t, candidates Out(s_t)]

two-stream encoder:
  state-history stream and action-history stream with cross-attention

encoder/candidate-scorer:
  encode state_hist and act_hist into c_t, then score candidate action tokens
```

The clean first mathematical description is the third one:

```text
history_encoder_k(state_hist, act_hist) -> c_t
candidate_encoder_k(edge_json, src_state, tgt_state, tier, time) -> u_i
score_k(c_t, u_i) -> logit_i
masked softmax over i with a_i in Out_k(s_t)
```

That leaves implementation freedom while preserving Tyler's architecture.

The on-policy/off-policy issue can remain outside the model-family section for
now. The eventual PPO record still has to remember that `act_hist` was
generated under a behavior/old policy. The model can consume history; PPO only
needs the log probability of the currently sampled action under the old policy
and then under the updated policy. The rollout record therefore needs enough
information to reconstruct:

```text
state_hist ids/tokens or reconstructible references
act_hist ids/tokens or reconstructible references
Out(s_t) ids in canonical order
selected local index
old_log_prob
value estimate
mask
```

The key unresolved design point remains:

```text
How do we size and mask the output over Out(s_t)?
```

The current consultant recommendation is:

```text
Do not size the model output by the whole graph.
Size it by the current candidate list Out(s_t).
Use canonical local ordering.
Pad only for batching.
Mask before softmax.
Store the action ids so the local index is never ambiguous.
```

This preserves the mathematical intent and avoids turning dynamic discovery
into a giant unstable output head.

## Closing Design Point: Per-Tier PPO Snapshot Pair

### Attribution

This closing PPO model-state design point is Project Owner-originated. Tyler
Foster identified the intended old/new policy structure as:

```text
policy_k        = current trainable model
rollout_policy_k = frozen snapshot used to collect the rollout
```

The consultant role here is to state the PPO consequence cleanly and connect it
to the tier-local candidate-scoring model above.

### Design Statement

For each non-degenerate quotient tier `k`, the training system should maintain
two model states:

```text
policy_k:
  current trainable tier-k policy model

rollout_policy_k:
  frozen snapshot of policy_k used to collect the current rollout batch
```

This is the standard PPO old-policy/new-policy split, specialized to the
full-tower, per-tier model family.

During rollout collection, when hardcoded `state_collapser` traversal reaches
tier `k` and requests a tier-local behavior action:

```text
input_t = (
  tier k,
  state_hist,
  act_hist,
  Out_k(s_t) in canonical order,
  mask_t
)

a_t ~ rollout_policy_k(. | input_t)
old_log_prob_t = log rollout_policy_k(a_t | input_t)
value_estimate_t = V_rollout_policy_k(input_t)
```

The rollout record must preserve the frozen decision surface:

```text
tier k
state_hist ids/tokens or reconstructible record references
act_hist ids/tokens or reconstructible record references
Out_k(s_t) ids in canonical order
mask_t
selected local index
selected action id
old_log_prob_t
value_estimate_t
reward_t
termination/truncation/bootstrap fields
```

During the PPO update, `policy_k` is updated while
`rollout_policy_k` remains frozen. The update recomputes the probability of
the same selected action on the same stored decision surface:

```text
new_log_prob_t = log policy_k(a_t | input_t)
ratio_t = exp(new_log_prob_t - old_log_prob_t)
```

The PPO clipped objective uses `ratio_t`, the advantage estimate, and the value
loss computed from the stored transition data. After the update interval is
complete, the rollout snapshot is refreshed:

```text
rollout_policy_k <- copy(policy_k)
```

### Consequences

This resolves the on-policy/off-policy concern for the current model design:

```text
The histories may be conditioning context.
The current sampled tier-local action is the PPO random variable.
The old log probability belongs to the frozen rollout policy that actually
sampled that action.
```

It is not enough to keep only two model copies. The rollout must also preserve
the old decision surface, because `G^0_t`, `Sigma^bullet_t`, and
`G^bullet_t` can change as graph discovery proceeds. If the candidate set
`Out_k(s_t)` is reconstructed later from the live graph without preserving the
old canonical order and mask, PPO may compute a ratio against the wrong action
surface.

Therefore, the design lock is:

```text
For each non-degenerate tier k, maintain policy_k and rollout_policy_k.
Collect rollouts with rollout_policy_k.
Train policy_k from stored rollout decision surfaces.
Refresh rollout_policy_k from policy_k only after the PPO update interval.
Never recompute Out_k(s_t), masks, or local action indices from a later live
graph when evaluating old rollout transitions.
```

This closes the present discussion's core model shape:

```text
hardcoded tower traversal
+ per-tier Tyler Foster transformer/candidate-scoring model
+ frozen rollout policy snapshots for PPO
+ stored tier-local decision surfaces for correct log-probability ratios
```
