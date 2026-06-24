# Warehouse Gridlock GPU PPO Training Surface Map

## Purpose

This document copies out the prior Codex design-discussion response from
`design_discussion.md`, per Project Owner request, so the surface map can be
used as a standalone reference during later blueprint and workplan drafting.

This document is not itself a blueprint, workplan, or implementation authority.

## Copied Codex Turn

I re-investigated the current `state_collapser` repo before answering. The
important alignment point is that `state_collapser` already has a semantic
training spine, but it explicitly should not become the owner of PPO as a big
algorithm suite.

Relevant upstream surfaces I checked:

```text
state_collapser.training.ActionSelectionInput
state_collapser.training.TrainingTransition
state_collapser.training.ActionDecision
state_collapser.training.StepCollector
state_collapser.training.EpisodeCollector
state_collapser.training.LinearizationConfig
state_collapser.training.EncodingRegistry
state_collapser.training.LinearizationReport
state_collapser.training.torch.TorchDecisionBatch
state_collapser.training.torch.TorchTransitionBatch
state_collapser.training.fibers.PathFiber
state_collapser.training.fibers.FiberStageContext
state_collapser.tower.partition.PartitionTower
state_collapser.tower.partition.action_surface.TowerActionSurfaceReport
```

The upstream design language is also clear:

```text
The engineer / downstream benchmark owns the loop.
state_collapser owns semantic handoff objects and deterministic conversion
from tower/fiber/runtime objects to numeric records.
```

So for BBB Warehouse PPO, I think the right design is:

```text
BBB owns the PPO trainer.
Warehouse owns the environment/runtime semantics.
state_collapser semantics are used or mirrored where tower/fiber/linearization
meaning matters.
```

The main pieces we need are these.

## 1. Warehouse Rollout Runtime Surface

This is the thing PPO steps through. It needs to expose a clean reset/step
contract:

```text
reset(seed, options) -> observation, info, runtime/episode state
step(action) -> next_observation, reward, terminated, truncated, info
```

For Warehouse, this has to preserve:

- one-second time semantics;
- synchronous full-robot action vectors;
- exact terminal success;
- time-limit truncation separately from terminal success;
- invalid ensemble semantics;
- discovery/admissibility accounting;
- selected-trace hooks for later movies.

In `state_collapser` language, this is analogous to the runtime consumed by
`StepCollector` and `EpisodeCollector`, but Warehouse's action is not a simple
integer unless we decide to encode it that way. We need a BBB-local runtime
surface that can still emit the same conceptual data: source input, chosen
action, reward, target input, terminated/truncated, bootstrap semantics, and
diagnostics.

## 2. Observation / State Encoding Surface

PPO needs tensors. Warehouse has rich structured state:

- robot identities and positions;
- box identities and positions;
- target positions;
- blocked columns;
- current second / max seconds / remaining time;
- possibly previous actions or short history;
- later, tower context.

The current transformer smoke already has pieces of this. For the serious PPO
loop we need to make it a first-class encoding contract, not an incidental
model helper.

State-collapser alignment:

```text
ActionSelectionInput.observation
ActionSelectionInput.runtime_snapshot
ActionSelectionInput.tower_position_key
ActionSelectionInput.action_mask
LinearizationConfig
EncodingRegistry
LinearizationReport
```

For direct Warehouse PPO, we may not literally use every `state_collapser`
object, but the artifact and code structure should rhyme with them: semantic
object first, deterministic numeric encoding second, Torch tensor third.

### PO Reply
> This isn't accetable. The whole point is evaluating `state_collapser`. We don;t copy [XXX] in `state_colapser`. We address why we can't use it, and potentially fix it.

### Codex Reply

Correct. My wording there was wrong, and the correction matters.

BBB should not copy `state_collapser` training or tensorization semantics into
BBB as a parallel local version. The point of BBB is to evaluate
`state_collapser`; if the `state_collapser` surface exists and is adequate, BBB
should use it. If it exists but is awkward, BBB should document the friction and
either adapt through a thin benchmark-side adapter or open a `state_collapser`
design/fix issue. If the surface does not exist, BBB should name the missing
surface instead of quietly inventing a duplicate.

So the corrected boundary is:

```text
state_collapser owns tower/fiber/runtime handoff semantics and tensorization
boundary objects.
BBB owns Warehouse-specific environment wrapping, PPO optimization,
evaluation orchestration, artifacts, readouts, and comparison claims.
```

BBB may still need Warehouse-specific encoders because Warehouse state includes
robots, boxes, targets, blocked columns, time, and action candidates. But those
encoders should be built as consumers of `state_collapser` handoff surfaces
where possible, not as copied replacements for them.

In blueprint language, this should become a hard rule:

```text
Before adding a BBB-local representation that overlaps state_collapser, check
whether state_collapser already exposes it. If it does, use it. If it does not,
record the gap and decide whether the fix belongs upstream.
```

### PO Reply
> Correct.

## 3. Action Distribution Surface

This is the most important piece.

PPO requires:

```text
sampled_action
old_log_prob(sampled_action)
new_log_prob(sampled_action)
entropy
```

So we need a probability distribution whose sampled object is exactly the
object sent to the environment, or we need a mathematically honest account of
how projection/repair changes the probability law.

Candidate action-distribution designs:

### Direct Factorized Full-Vector Distribution

The model outputs one categorical distribution per robot:

```text
robot_i -> categorical({stay, north, south, east, west})
```

The joint log probability is:

```text
sum_i log p_i(action_i)
```

This is clean and GPU-friendly. The downside is that the sampled ensemble may
be invalid unless we only mask per-robot impossibilities and let ensemble
invalidity be an environment transition.

### Generated Valid Joint-Action Distribution

The system generates a candidate set of joint actions, filters valid ones, and
the policy samples among those generated valid actions.

This makes the executed action equal the sampled action. It also creates a
clear mask. But it changes the action random variable from "all full vectors"
to "current generated candidate set", so artifacts must record candidate-set
policy, validity queries, and whether candidate generation gives unfair help.

### Projected / Repaired Distribution

The model samples a raw full action vector, then a resolver repairs it.

This is dangerous for PPO unless we either:

- train on the log probability of the raw proposal and treat repair as part of
  the environment, while recording the mismatch; or
- compute the effective probability of the repaired action, which is usually
  hard.

My current recommendation remains: do not start serious PPO with silent repair.

### PO Reply
> I agree with your recommendation.

## 4. Mask And Admissibility Surface

Warehouse is about hidden admissibility. PPO must not accidentally give one arm
a hidden oracle.

We need to decide and artifact:

- what masks are available before sampling;
- whether masks are per-robot local masks or joint-action masks;
- how many validity queries are made;
- whether query results are cached;
- whether cache persists across episodes;
- whether invalid sampled ensembles are legal training samples;
- whether invalid attempts advance rollout step count even though Warehouse
  time does not advance.

State-collapser alignment:

```text
ActionSelectionInput.action_mask
PathFiber.action_mask(...)
TorchDecisionBatch.action_mask
TowerActionSurfaceReport
```

This is where direct/tower fairness lives.

### PO Reply
> Explain.

### Codex Reply

The masking issue is about what information a policy gets *before* it samples
an action.

For PPO, the policy samples from a probability distribution. A mask modifies
that distribution by assigning probability zero to some actions before
sampling. So the mask is not an after-the-fact diagnostic; it is part of the
policy's information surface.

In Warehouse there are at least three different things people might call an
"action mask":

```text
primitive per-robot mask
joint concrete ensemble mask
tower abstract action-cell / liftability mask
```

A primitive per-robot mask says things like "this robot cannot move north from
here because north is blocked." That does not necessarily prove the whole
ensemble is valid, because two robots or boxes might collide after individually
legal moves.

A joint concrete ensemble mask says "this entire simultaneous action vector is
valid." That is stronger. It may require generating or checking candidate
joint actions.

A tower mask says "this abstract action cell is executable or admissible from
the current concrete state/tower context." In `state_collapser` terms, this
can involve:

```text
PartitionTower.executable_action_cells(...)
PartitionTower.executable_lift_candidates(...)
PathFiber.action_mask(...)
```

The fairness problem is that these masks are not the same kind of information.
If direct PPO only sees weak primitive masks, but tower PPO sees a strong
live-lift mask, then tower may avoid dead abstract choices that direct is not
equipped to avoid. That may be legitimate if the experiment is "does the tower
technology help?" But it must be stated as part of the experimental condition,
not hidden inside implementation.

So the design should force every arm to declare:

```text
mask_kind
mask_source
mask_query_budget
whether mask is local, joint, abstract, or liftability-based
whether failed mask/lift events are possible after sampling
```

For a serious PPO run, I would prefer avoiding silent invalid repair. Either
sample from the declared valid/action-cell mask, or let invalid samples be real
training events with explicit transition semantics. Do not sample one thing,
repair it, and train PPO as if the repaired thing had the sampled log
probability.

### PO Reply
> One thing that's confusing me here is that taking `32` vectors of shape `[4]` and taking a vector of shape `[32,4]` or `[32*4]` are very similar. The latter is faster on a GPU. So the distinction is confusing me.

### Codex Reply

Yes, as tensor storage those are extremely similar, and on GPU we probably
*should* batch them into a single dense tensor. The distinction I mean is not
"will this be one tensor or many tensors?" The distinction is "what random
variable does the tensor parameterize?"

For example, suppose there are 32 robots and each has 4 possible primitive
moves. A tensor shaped:

```text
[32, 4]
```

can mean:

```text
32 independent categorical distributions, one per robot.
```

Then a sampled joint action is:

```text
(a_1, a_2, ..., a_32)
```

and the log probability is:

```text
sum_i log p_i(a_i)
```

The same data flattened to:

```text
[32 * 4]
```

can still mean exactly the same thing if we reshape it back to `[32,4]` before
constructing the distribution. That is just a layout/performance choice.

But a vector of shape `[32 * 4]` could also mean:

```text
one categorical distribution over 128 choices
```

That is a completely different probability law. It samples one item out of
128, not one action for each of 32 robots.

So the key distinction is:

```text
tensor layout != action distribution semantics
```

On GPU, we absolutely want batched dense tensors. For direct Warehouse PPO,
the actor might emit logits with physical layout:

```text
[batch, robot_count, primitive_action_count]
```

or a flattened equivalent:

```text
[batch, robot_count * primitive_action_count]
```

But semantically we still need to know whether that tensor represents:

```text
factorized per-robot categorical policy
joint candidate-set categorical policy
tower tier-local action-cell categorical policy reached by hardcoded traversal
hierarchical control-kind plus action-cell policy
```

That is why the design language matters. GPU speed tells us how to store and
compute the logits. PPO correctness depends on what probability distribution
those logits define.

### PO Reply
> The point is to coordinate robot behavior, so I don't understand. One distribution. How would a model learn this otherwise?

### Codex Reply

Yes, this is the right objection. For the actual Warehouse problem, the thing
we want conceptually is one distribution over *coordinated ensemble behavior*.
The policy is not supposed to be 32 unrelated little policies that merely
happen to run at the same time.

The reason I was separating the cases is that there are several ways to
parameterize a joint distribution.

The weak version is:

```text
pi(a_1, ..., a_32 | s) = product_i pi_i(a_i | s)
```

This still conditions every robot on the full state `s`, so the model can learn
some coordination by making each robot's logits depend on all robots, boxes,
targets, and tower context. But the sampling is conditionally independent once
the state is fixed. That means it cannot naturally represent cases like:

```text
either all robots coordinate plan A, or all robots coordinate plan B,
but do not mix half of A with half of B
```

unless the logits become nearly deterministic.

For serious Warehouse Gridlock, I agree that this is probably not the right
main policy law.

The mathematically better target is one joint policy:

```text
pi(a_ensemble | s)
```

where `a_ensemble` is the whole simultaneous robot/box-relevant decision. The
problem is that the naive joint action space is enormous:

```text
4^32
```

or larger depending on the primitive action set. We cannot just emit one dense
logit for every possible ensemble action.

So the design problem becomes:

```text
How do we parameterize one joint distribution without enumerating the full
joint action space?
```

The likely options are:

1. **Autoregressive joint policy**

   ```text
   pi(a_1, ..., a_32 | s)
   =
   pi(a_1 | s)
   pi(a_2 | s, a_1)
   ...
   pi(a_32 | s, a_1, ..., a_31)
   ```

   This is one joint distribution. PPO log probability is:

   ```text
   sum_i log pi(a_i | s, previous sampled actions)
   ```

   This lets later robot choices condition on earlier robot choices, so the
   model can represent coordinated ensembles without enumerating all possible
   ensembles.

2. **Candidate-set joint policy**

   Generate a finite set of candidate ensemble actions, then sample one:

   ```text
   pi(candidate_ensemble_j | s)
   ```

   This is also one joint distribution. The hard part is candidate generation:
   it must not smuggle in too much search or unfair admissibility knowledge
   unless that is explicitly part of the evaluated method.

3. **Latent-plan policy**

   Sample a shared latent plan, then condition robot actions on it:

   ```text
   z ~ pi(z | s)
   a_i ~ pi_i(a_i | s, z)
   ```

   This can coordinate robots through the shared plan. It is more complex, and
   I would not start here unless we decide the autoregressive/candidate-set
   approaches are wrong.

4. **Tower-control joint policy**

   For the tower arm, the joint object may not be a raw robot action vector at
   all. It may be:

   ```text
   tower_control_candidate
   ```

   where one candidate already represents a coordinated abstract move, a tower
   traversal decision, or an abstract action cell plus lift/resolve semantics.

So I agree with your conceptual point:

```text
the policy should learn coordinated ensemble behavior as one distribution.
```

The correction is:

```text
[32,4] is fine as a tensor layout, but a conditionally independent
per-robot categorical policy is probably only a debug/baseline model.
```

For serious PPO, the blueprint should prefer either:

```text
autoregressive joint ensemble policy
```

for direct Warehouse control, or:

```text
tower tier-local executable action-cell policy at hardcoded traversal
execution surfaces
```

for full-tower control.

That answers "how would the model learn this otherwise": it learns coordinated
behavior because the log probability belongs to a whole structured joint
decision, and PPO increases or decreases probability mass for that coordinated
decision according to its advantage. If we factor the policy too aggressively,
we weaken exactly the coordination mechanism the environment is meant to test.

### PO Reply
Ok. I am starting to get really frustrated with this part of the discussion. Ehat the [XXX] is this "```text
finite tower-control candidate policy
```"!? Where did that come from? Move this thread over to `docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/tower_traversing_logic_discussion.md`

### Codex Reply

Moved this sub-thread to:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/tower_traversing_logic_discussion.md
```

I am treating "finite tower-control candidate policy" as bad shorthand from
this broader PPO surface map, not as settled project vocabulary. The detailed
correction belongs in the tower-traversing document: PPO does not control
tier traversal.

## 5. Actor-Critic Model Surface

PPO needs an actor and a critic. Minimal modern shape:

```text
encoded observation -> shared trunk -> actor head(s), value head
```

For Warehouse direct PPO:

- actor emits action distribution parameters;
- critic emits scalar `V(s)`;
- the sampled action and value estimate are stored in the rollout.

For GPU training:

- model lives on `cuda` if requested and available;
- rollout tensors move to device in minibatches;
- no accidental CPU/GPU ping-pong during update;
- inference during rollout may be on GPU, but environment stepping remains
  Python/CPU unless separately vectorized later.

Non-bloated means: one transformer actor-critic model family first, not a model
zoo.

### PO Reply
> What is the minimal architecutre for actor/critic?

### Codex Reply

The minimal actor/critic should be just enough structure to represent the
Warehouse state and score the available action surface. It should not be a
model zoo, and it should not be a flat MLP that destroys the identities of
robots, boxes, targets, and action candidates.

The minimal serious shape is:

```text
structured Warehouse/tower input
-> token/feature encoder
-> small shared transformer or attention trunk
-> actor head
-> critic head
```

For direct PPO, the actor head can be simple:

```text
one categorical head per robot over {stay, north, south, east, west}
joint_log_prob = sum per-robot log_probs
```

For tower PPO, the actor head should probably be candidate-scoring:

```text
context vector = encode(current Warehouse state + tower context)
candidate vectors = encode available action cells
logit_i = score(context vector, candidate_action_cell_i)
mask non-executable candidates
sample categorical over remaining action cells
```

The critic should emit:

```text
V(observation, tower_context)
```

as one scalar for the current decision state. It can share the trunk with the
actor, then use a small value MLP on the pooled/context token.

Minimal does not mean underpowered. I would use:

```text
entity/token embeddings:
  robots
  boxes
  targets
  blocked cells
  time/remaining horizon
  active tier / tower position
  action-cell candidates when tower mode is active

small transformer trunk:
  2-4 layers to start
  modest hidden dimension
  no recurrence initially

actor:
  direct: per-robot categorical logits
  tower: variable-candidate action-cell scorer

critic:
  pooled context -> scalar value
```

That is the smallest architecture I would trust as a real Warehouse PPO
baseline/tower trainer. It gives PPO real logits, real log probabilities, real
entropy, and a real value function without introducing extra algorithmic
machinery.

### PO Reply
> I support this.

## 6. Rollout Buffer Surface

PPO is on-policy. We need a rollout buffer that stores exactly the old-policy
data used for the update:

```text
observations
actions
old_log_probs
rewards
terminated
truncated
values
bootstrap_values
advantages
returns
diagnostics / sidecars
```

This is where the `state_collapser.training.TrainingTransition` idea matters.
The package transition object already names:

```text
source_input
chosen_action
reward
target_input
terminated
truncated
bootstrap_allowed
bootstrap_reason
runtime_snapshot_summary
tower_position_key
active_tier
stage_context
fiber_departure
```

Our Warehouse PPO rollout buffer should preserve the same distinctions even if
it uses a BBB-local tensor layout. In particular, `terminated` and `truncated`
must not be collapsed.

### PO Reply
> I agree.

## 7. GAE / Return Computation Surface

This is the post-rollout reverse-time pass:

```text
delta_t = r_t + gamma * V(s_{t+1}) * nonterminal - V(s_t)
adv_t = delta_t + gamma * lambda * nonterminal * adv_{t+1}
return_t = adv_t + V(s_t)
```

Required design choices:

- true terminal success has no bootstrap;
- time-limit truncation should usually bootstrap from final value;
- invalid/no-time-advance transitions must have explicit treatment;
- advantage normalization happens per PPO update batch;
- raw and normalized advantage stats are artifacted.

### PO Reply
> Explain.

### Codex Reply

GAE is the bridge between raw rewards and the advantage numbers used by PPO.
The policy update wants to know whether the sampled action should get more or
less probability mass. GAE estimates that by comparing observed reward-plus-
future-value against the critic's previous value estimate.

At each rollout step:

```text
delta_t = reward_t + gamma * V(next_state) * nonterminal - V(state_t)
```

This `delta_t` says whether the transition was better or worse than the critic
expected. GAE then lets those surprises flow backward through time:

```text
adv_t = delta_t + gamma * lambda * nonterminal * adv_{t+1}
```

So if a move at second 12 only pays off at second 40, the later evidence can
still affect the earlier action's advantage. That matters a lot for Warehouse,
because opening space, moving boxes into useful corridors, or avoiding gridlock
may not immediately look good.

The critic target is then:

```text
return_t = adv_t + V(state_t)
```

PPO uses:

```text
adv_t
```

in the actor loss and:

```text
return_t
```

in the critic/value loss.

The design-sensitive part is terminal handling:

```text
true success terminal -> no bootstrap
time-limit truncation -> usually bootstrap from V(final_state)
diagnostic failure / mask-empty / failed lift -> must be explicitly classified
```

We should not collapse all of those into one `done=True`. If we do, the critic
learns the wrong continuation structure and GAE propagates the wrong signal.

For this project, the important artifact fields are:

```text
gamma
gae_lambda
raw_advantage_mean/std/min/max
normalized_advantage_mean/std/min/max
bootstrap_reason
terminated_count
truncated_count
diagnostic_failure_count
```

That lets the readout confirm that PPO is not just doing optimizer steps, but
actually computing advantages with the right Warehouse/tower semantics.

### PO Reply
> I support this.

## 8. PPO Update Engine

The actual trainer loop is small:

```text
collect rollout with frozen old policy
compute GAE and returns
for ppo_epoch in epochs:
    shuffle rollout indices
    for minibatch:
        recompute log_prob, entropy, value
        ratio = exp(new_log_prob - old_log_prob)
        actor_loss = -mean(min(ratio * adv, clipped_ratio * adv))
        value_loss = ...
        entropy_loss = ...
        backprop
        clip gradients
        optimizer step
        record approximate KL and clip fraction
```

Best-practice diagnostics:

- approximate KL;
- clip fraction;
- entropy;
- value loss;
- policy loss;
- explained variance for value function;
- gradient norm;
- learning rate;
- steps per second;
- GPU device and memory summary if available.

This belongs in BBB, not `state_collapser`.



### PO Reply
> Agree.

## 9. Device / Backend / Tensorization Surface

We should align with upstream `LinearizationConfig` vocabulary:

```text
none_control_flow
tensor_available_disabled
tensor_enabled_cpu
tensor_enabled_cuda
```

For this design block, the important modes are probably:

- `tensor_enabled_cpu` for correctness smoke;
- `tensor_enabled_cuda` for serious GPU training.

Artifacts should record:

- requested device;
- actual device;
- Torch version;
- CUDA availability;
- dtype;
- whether mixed precision is used;
- conversion/tensorization timing;
- model parameter count;
- training throughput.

### PO Reply
> I agree, but this seems to contradict your suggestion to copy [XXX] in `state_collapser` instead of use it.

### Codex Reply

Yes. That contradiction is real, and the correction is the same as above:
we should use `state_collapser` where it owns the concept, not copy it.

The right division is:

```text
state_collapser:
  LinearizationConfig
  EncodingRegistry
  LinearizationReport
  tower/fiber/runtime handoff semantics
  Torch conversion surfaces where available

BBB:
  PPO rollout collection
  PPO loss/update loop
  Warehouse-specific model architecture
  evaluation artifacts/readouts
  benchmark comparison claims
```

If BBB needs a tensor that `state_collapser` can already produce, BBB should
ask `state_collapser` for it and record the resulting `LinearizationReport`.
If BBB needs a Warehouse-specific tensor that is outside `state_collapser`'s
scope, BBB can build it, but the design must say why that tensor is
environment/model-specific rather than a replacement for upstream semantics.

The phrase "rhyme with" was too loose. The correct blueprint rule is:

```text
Use upstream state_collapser semantic and tensorization surfaces directly
whenever they apply. Add BBB-local tensors only for PPO/model/evaluation
needs that state_collapser intentionally does not own. If a missing upstream
surface blocks clean use, stop and design the upstream fix rather than cloning
the concept downstream.
```

That is especially important because this repo is supposed to evaluate
`state_collapser`, not gradually fork it.

### PO Reply
> I agree.

## 10. Checkpoint / Resume Surface

Serious GPU training needs real checkpoints:

```text
model state_dict
optimizer state_dict
scheduler state if any
normalization stats if any
encoding registry / vocabulary
run config
RNG states
global update index
episode index
rollout step index if resumable mid-rollout
best metric snapshot
```

For first implementation, I would not require perfect mid-rollout resume. I
would require clean resume at update boundaries.

### PO Reply
> I agree.

## 11. Trace / Movie Retention Surface

This must be explicit from the beginning.

We should not write every step of every episode by default. We need:

- selected episode trace policy;
- periodic trace retention;
- final episode retention;
- best-so-far episode retention;
- failure/interesting-episode retention;
- movie rendering from retained traces;
- clear error if a requested episode was not retained.

This follows the lesson from the previous Warehouse CSV explosion.

### PO Reply
> I agree.

## 12. Artifact And Readout Surface

PPO runs must produce human-readable and machine-readable evidence that the
training loop was real.

Minimum artifacts:

- `evaluation_manifest.json`;
- `training_config.json`;
- `model_manifest.json`;
- `optimizer_manifest.json`;
- `device_manifest.json`;
- `rollout_buffer_manifest.json`;
- `ppo_update_summary.csv`;
- `training_curve.csv`;
- `episode_summary.csv`;
- `advantage_summary.csv`;
- `value_summary.csv`;
- `action_distribution_summary.csv`;
- `mask_admissibility_summary.csv`;
- `checkpoint_manifest.json`;
- `trace_episode_index.csv`;
- `readout_source.json`.

The readout should answer:

- Did PPO actually run?
- Did optimizer steps happen?
- Did old/new log-probability ratios exist?
- Was clipping active?
- Was KL controlled?
- Did value learning improve?
- Did reward/success improve?
- Was GPU actually used?
- Were invalid/action-mask semantics fair and explicit?

### PO Reply
> I agree.

## 13. Tower-Specific Surfaces, Deferred But Named

For direct PPO, the surfaces above are enough. For tower PPO, we additionally
need:

- active tier;
- state cell;
- action cell vocabulary;
- executable action-cell mask;
- lift candidate set;
- selected abstract action cell;
- selected concrete lift;
- log probability of whatever was sampled;
- value function domain;
- fiber/stage context;
- fiber departure diagnostics.

State-collapser already has the vocabulary:

```text
PartitionTower.outgoing_action_cells(...)
PartitionTower.executable_action_cells(...)
PartitionTower.executable_lift_candidates(...)
PathFiber.action_mask(...)
PathFiber.lift_candidates(...)
FiberStageContext
FiberDeparture
EncodingRegistry
```

But we still need the PPO random-variable story. Is the tower policy sampling
an action cell? A lift candidate? A concrete action vector conditioned by tower
context? A tier and then an action? Until that is fixed, tower PPO should stay
as a named follow-up, not the first implementation target.

### PO Reply
> Explain in detail.

### Codex Reply

The tower-specific surfaces are the pieces that make the policy a tower policy
instead of a direct policy with extra metadata.

Here is what each surface means.

### Active Tier

The active tier is the level of the tower where the controller is currently
making a decision. A full-tower controller cannot just act at tier 0 forever,
and it cannot just act at one fixed tier forever if the point is to test full
tower movement. The active tier has to be part of the policy input and the
transition record.

### State Cell

At a given tier, the current concrete Warehouse state projects to a state cell.
The state cell is the abstract location of the current state at that tier.

PPO needs this because the available abstract actions depend on:

```text
current concrete state
current active tier
current state cell at that tier
```

### Action Cell Vocabulary

At a state cell, the tower has outgoing abstract action cells. This is the
tower-level action vocabulary.

In `state_collapser` terms:

```text
PartitionTower.outgoing_action_cells(active_tier, state_cell)
```

This vocabulary may vary by state and tier, so the actor head should probably
score a variable candidate set rather than use one fixed dense output head.

### Executable Action-Cell Mask

Not every outgoing action cell necessarily has a concrete lift from the current
concrete state. The executable mask filters the abstract vocabulary down to
actions that can actually be realized now.

In `state_collapser` terms:

```text
PartitionTower.executable_action_cells(...)
PartitionTower.executable_lift_candidates(...)
PathFiber.action_mask(...)
```

This mask is central to the technology. It is also central to fairness/readout
because it is stronger and different from a naive direct primitive mask.

### Lift Candidate Set

Once the policy chooses an action cell, the system still has to produce a
concrete Warehouse move. The lift candidate set is the set of concrete edges or
actions that realize the selected abstract action from the current concrete
state.

This is where PPO can become mathematically wrong if we are careless. If the
policy samples the action cell but the system chooses a lift deterministically,
the PPO log probability belongs to the action cell. If the policy samples both
the action cell and the lift, the PPO log probability must include both.

### Selected Abstract Action Cell

This is likely one tower PPO sampled action surface:

```text
sampled_action = action_cell_id
```

But after the PO correction below, this cannot be the whole full-tower action
surface by itself. It is one kind of `act_here` decision inside a broader
full-tower controller that can move up and down the tower.

### Selected Concrete Lift

This is the concrete Warehouse move that actually happens after the abstract
action cell is selected.

The selected concrete lift must be recorded even if it is deterministic,
because it explains the real environment transition and makes movie/replay
possible.

### Log Probability Of Whatever Was Sampled

PPO only works if the log probability belongs to the actual sampled random
variable.

Clean cases:

```text
sample action_cell -> log_prob(action_cell)
sample (action_cell, lift) -> log_prob(action_cell) + log_prob(lift | action_cell)
sample tower_control_action -> log_prob(tower_control_action)
```

Bad case:

```text
sample raw thing -> silently repair to different thing -> train as if repaired
thing had sampled log_prob
```

That bad case is what we must avoid.

### Value Function Domain

The critic has to estimate the value of the current decision state. For tower
PPO, that probably means:

```text
V(concrete Warehouse state, tower position, active tier, maybe state cell)
```

The critic should see enough tower context to value a tower decision, not just
a flat grid.

### Fiber / Stage Context

If we train inside a path fiber or under frozen lower/coarse behavior, the
stage context identifies what behavior is fixed and what level is currently
being trained.

This is not optional metadata if fiber training is active; it changes the
meaning of the action mask and transition.

### Fiber Departure Diagnostics

If the controller leaves the intended fiber, cannot lift, sees stale tower
context, or chooses an action outside the expected surface, the system should
record a structured departure reason.

For PPO, this matters because those events should not silently become ordinary
low-reward transitions unless we explicitly decide that they do. They may be
diagnostic failures, truncations, or special rollout events.

The short version:

```text
tower PPO = policy over tower control/action surfaces + exact lift semantics
          + exact log probability of sampled tower random variable
          + transition records that preserve tier/fiber/lift context.
```

Without those pieces, the run may still train a neural network, but it is not a
clean test of tower-structured PPO.

### PO Reply
> Start a new document in this document's parent folder for a discussion of just the "tower traversing logic` for the evaluation/PPO training we're designing right now.

### Codex Reply
Started:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/tower_traversing_logic_discussion.md
```

I seeded it as a discussion document, not a blueprint or workplan. It starts
from the Project Owner correction that this is full-tower training, not
fixed-tier smoke, and it uses the existing `state_collapser` control vocabulary
(`ControlAction`, `ActiveTierState`, `LiveRuntimeView`, and
`ExploitExploreTowerRuntime`) as the alignment point.

## My Current Slice Recommendation

For the first serious design blueprint, I would propose this order:

1. Direct Warehouse PPO with a clean action probability law.
2. GPU/device/checkpoint/trace/artifact discipline.
3. PPO readout proving real clipped PPO, GAE, KL, entropy, and value updates.
4. Only after that, tower PPO design using state_collapser tower/fiber
   semantics.

This gives us a non-[XXX] PPO trainer first. Then we can ask the hardertower question with a real reference implementation beside it.

### PO turn
> I think the real think to work out is how exactly PPO interacts with the tower architecture. I just want to walk through this. How much is already obvious from architecture?

### Codex turn

Short answer: a lot is already obvious from the architecture, but not the
entire PPO design. The architecture already tells us the *handoff shape* and
the *tower semantic objects*. It does not yet tell us the exact PPO random
variable, and that is the piece we cannot fake.

What is already obvious:

1. `state_collapser` does not own PPO. BBB owns the PPO loop.

   The upstream boundary is clear: `state_collapser` gives us tower/fiber
   semantics, typed training handoff objects, masks, lift candidates, and
   tensorization surfaces. BBB decides how to run PPO, how to checkpoint it,
   how to artifact it, and how to compare arms.

2. Every PPO decision needs to pass through an `ActionSelectionInput`-like
   object.

   That object already has the right conceptual slots:

   ```text
   observation
   current_base_state
   runtime_snapshot
   tower_position_key
   action_mask
   active_tier_state
   stage_context
   fiber_departure
   diagnostics
   ```

   So the tower PPO input is not just "the grid." It is the grid plus tower
   position, active tier, action mask, and possibly fiber/stage context.

3. Every PPO transition needs to preserve the `TrainingTransition` distinction.

   That means:

   ```text
   source_input
   chosen_action
   reward
   target_input
   terminated
   truncated
   bootstrap_allowed
   bootstrap_reason
   active_tier
   stage_context
   projected_coarse_step
   fiber_departure
   ```

   This is very important for PPO because GAE and value bootstrapping depend
   on not collapsing true terminal success, time-limit truncation, failed lift,
   fiber departure, and ordinary continuation into one sloppy "done" flag.

4. A tower policy should not be sampling arbitrary concrete full-action vectors
   at every point if it is actually using the tower.

   The tower architecture gives finite abstract surfaces:

   ```text
   current state cell
   outgoing action cells
   executable action cells
   executable lift candidates
   path-fiber admissible action cells
   path-fiber lift candidates
   ```

   So a tower PPO policy naturally wants to score a finite vocabulary of tower
   actions at the current active tier or fiber stage.

5. Live-lift masking is architecturally real.

   `PartitionTower.executable_action_cells(...)` and
   `PartitionTower.executable_lift_candidates(...)` exist specifically to avoid
   pretending that an abstract action cell is executable from a concrete state
   when it has no current concrete lift. Likewise, `PathFiber.action_mask(...)`
   says which fine-stage action cells are admissible under a frozen coarse
   behavior.

   That is not "PPO magic." It is the tower semantics. PPO has to consume that
   mask honestly.

6. Tensorization is an explicit boundary, not the source of semantics.

   The order should be:

   ```text
   semantic tower/runtime object
   deterministic encoding/linearization report
   Torch tensor batch
   PPO update
   ```

   This matches the upstream `LinearizationConfig`, `EncodingRegistry`,
   `LinearizationReport`, `TorchDecisionBatch`, and `TorchTransitionBatch`
   story.

What is *not* already obvious:

1. What exactly is the sampled PPO action?

   This is the central unresolved design question.

   Possibilities include:

   ```text
   active tier
   abstract action cell
   concrete lift candidate
   concrete full robot action vector
   pair: (abstract action cell, concrete lift candidate)
   tuple: (tier, action cell, lift candidate)
   ```

   PPO needs the log probability of the sampled object. So we have to name the
   object precisely.

2. Whether lift choice is policy-sampled or deterministic.

   If the policy samples only an abstract action cell and then the system uses
   a deterministic lift rule, then the PPO log probability is just:

   ```text
   log pi(action_cell | tower_context)
   ```

   That is clean, but it means the lift rule is controller architecture rather
   than learned policy.

   If the policy also samples the lift candidate, then the log probability is
   something like:

   ```text
   log pi(action_cell | tower_context)
   + log pi(lift_candidate | tower_context, action_cell)
   ```

   That is also mathematically clean, but more complex.

   What we should *not* do is sample one thing, execute a repaired or silently
   substituted thing, and pretend the old log probability still belongs to the
   executed action.

3. Whether the tower decision is one-level or hierarchical.

   A tower PPO decision could be:

   ```text
   choose active tier -> choose action cell -> choose lift
   ```

   or:

   ```text
   current controller has already fixed active tier -> choose action cell -> lift
   ```

   or:

   ```text
   upper tier chooses a coarse behavior; lower tier is trained inside the path
   fiber with that behavior frozen
   ```

   The architecture supports the last shape through `PathFiber` and
   `FiberStageContext`, but PPO still needs us to decide which controller is
   being trained in the present run.

4. What the critic values.

   Possible critic domains:

   ```text
   V(concrete_state)
   V(concrete_state, active_tier)
   V(tower_context)
   V(fiber_stage_context, concrete_state)
   V(state_cell)
   multi-head V_t by tier
   ```

   PPO can use any of these, but the semantics differ. For the first tower PPO,
   I would strongly prefer `V(observation, tower_context, active_tier)` over a
   critic that sees only the concrete grid or only the abstract cell.

5. Whether one tower action equals one environment second.

   If the tower policy chooses an action cell and immediately lifts it to one
   concrete Warehouse ensemble move, then the PPO step is still one second.
   That is simplest.

   If the tower policy chooses a coarse action that expands into a lower-level
   path or option, then we are closer to semi-MDP / options PPO. Then log
   probabilities, rewards, and GAE need a different treatment. I do not think
   we should start there unless the PO explicitly wants that design.

6. How direct/tower fairness is phrased.

   The tower is allowed to use its own live-lift mask because that is part of
   tower semantics. But we have to artifact exactly what information that mask
   uses. Direct PPO cannot be given an obviously weaker invalid-action surface
   by accident.

   This does not mean direct must get tower liftability. It means we must be
   explicit about which masks each arm gets:

   ```text
   direct: direct admissible action surface
   tower: tower action-cell/lift admissibility surface
   ```

   and record why the difference is the experiment, not a hidden bug.

My current concrete mental model:

```text
Tower PPO should first be a masked categorical policy over executable abstract
action cells at a fixed active tier, with a deterministic live-lift rule to
select a concrete executable lift candidate.
```

That gives us:

```text
sampled_action = action_cell_id
old_log_prob = log pi_old(action_cell_id | encoded tower context)
executed_action = deterministic_live_lift(action_cell_id, current_concrete_state)
transition = one concrete Warehouse second
critic_input = encoded concrete state + tower context + active tier
mask = executable action-cell mask
```

This is not the final possible tower PPO, but it is the first one that seems
architecturally honest and not bloated.

The next harder version would be:

```text
sampled_action = (action_cell_id, lift_candidate_id)
old_log_prob = log pi_old(action_cell_id | context)
             + log pi_old(lift_candidate_id | context, action_cell_id)
```

That is more expressive, but I would not start there until the abstract-cell
version is working and artifacted.

So: the architecture already makes the tower PPO input/transition/mask/lift
surfaces mostly obvious. It does not make the PPO sampling law obvious. The
design work should focus there first.

### PO turn
> Explain exactly what we need to still design/decide?

### Codex turn

Here is the clean decision inventory. I am separating "must decide before a
blueprint" from "can defer until later," because otherwise this will balloon
into fake uncertainty.

## Decisions Needed Before Blueprint

### 1. First Tower PPO Training Target

We need to decide what the first tower PPO implementation is actually training.

My recommendation:

```text
Train one fixed active-tier tower controller.
The controller samples an executable abstract action cell.
The system deterministically live-lifts that action cell to one concrete
Warehouse move.
One PPO timestep equals one Warehouse second.
```

This avoids options/semi-MDP complexity and gives us the smallest honest
tower-PPO object.

We should not begin with:

```text
policy chooses tier
policy chooses long abstract path
policy emits whole lower-tier behavior
policy samples concrete full action vector and calls it "tower"
```

Those can be later designs.

### 2. Which Active Tier

We need to choose how the active tier is selected for the first run.

Options:

```text
fixed tier chosen by config
highest executable nontrivial tier
best candidate tier from a prior diagnostic
small set of hand-selected tiers
```

My recommendation:

```text
Use fixed tier by explicit config, with a default selected from a prior tower
diagnostic.
```

The PPO run should not silently search across tiers during training at first.
Tier selection is a separate experimental condition.

### 3. Sampled Action Random Variable

This is the most important decision.

For first tower PPO, I recommend:

```text
sampled_action = action_cell_id
```

The policy distribution is:

```text
pi_theta(action_cell_id | encoded concrete state, tower context, active tier)
```

The mask is over executable abstract action cells at the active tier.

This makes PPO clean:

```text
old_log_prob = log pi_old(sampled_action | input)
new_log_prob = log pi_new(sampled_action | input)
ratio = exp(new_log_prob - old_log_prob)
```

### 4. Lift Rule

If the sampled action is an abstract action cell, we still need to execute a
concrete Warehouse move.

We need to decide the deterministic lift rule.

Candidate rule:

```text
Given current concrete state and sampled action cell:
1. ask the tower for executable lift candidates;
2. require at least one executable candidate;
3. choose a deterministic candidate by stable ordering;
4. execute that concrete edge/action.
```

The stable ordering must be artifacted. For example:

```text
sort by concrete edge/action id under the environment's canonical registry
```

This is not learned lift selection. It is deterministic controller machinery.
That is acceptable for the first PPO because the sampled random variable stays
clean.

### 5. What Happens When Mask Is Empty

We need explicit semantics for states where the active tier has no executable
action cell.

Options:

```text
terminate episode with diagnostic failure
fall back to lower tier
emit stay/self-loop
resample tier
mark tower controller inactive for that state
```

My recommendation for first serious PPO:

```text
Do not silently fall back.
If the configured active tier has empty executable action mask, record
mask_empty, truncate or fail the episode according to a documented rule, and
count it as a tower-controller health failure.
```

Reason: fallback would make the policy objective ambiguous. If we later want
fallback, it should be a named hierarchical controller design.

### 6. Critic Input And Critic Domain

We need to decide what the value function sees.

My recommendation:

```text
V_theta(encoded concrete Warehouse state, active tier, tower position/context)
```

The critic should not see less than the actor. It can share the transformer
trunk with the actor and emit one scalar value estimate for the current
decision surface.

We should artifact:

```text
critic_input_schema
actor_input_schema
whether actor and critic share trunk
value_bootstrap_semantics
```

### 7. Observation Encoding

We need to define the tensor input exactly.

Minimum:

```text
robot positions and identities
box positions and identities
targets
blocked columns
current second / max seconds / remaining fraction
active tier
current state cell id or embedding id
available action-cell ids / embeddings
action-cell mask
```

Open subdecision:

```text
Do action cells get represented by learned action embeddings, structural
features, or both?
```

My recommendation for first PPO:

```text
Use stable action-cell ids with learned embeddings, plus simple structural
features where already cheap to compute.
```

Do not overbuild graph neural machinery yet.

### 8. Policy Head Shape

The actor has to score a variable number of action cells.

We need to decide the scoring pattern.

Recommended pattern:

```text
encode state/context -> context vector
encode each available action cell -> action vector
score(context, action_cell) -> logit
mask non-executable cells
categorical over executable cells
```

This is better than a fixed giant output head if action vocabularies vary by
tier/state.

### 9. Direct Baseline For This Design Block

We need to decide whether this blueprint includes a direct PPO baseline or only
tower PPO.

My recommendation:

```text
Blueprint the tower PPO trainer as the main object, but include a direct PPO
baseline only insofar as it shares PPO infrastructure and later comparison
readout.
```

Reason: the current design question is tower-PPO semantics. Direct PPO is
easier, but if we let direct consume the whole design, we will postpone the
real tower question again.

### 10. Fairness Boundary

We need to write the fairness claim precisely.

A possible first statement:

```text
Direct PPO samples from its direct admissible action surface.
Tower PPO samples from its tower action-cell surface with live-lift executable
masking.
The comparison is not "same information surface"; it is "direct concrete
policy versus tower-structured policy under each controller's declared
admissibility semantics."
```

This is honest. The tower's live-lift mask is part of the tower technology. It
should not be hidden, and it should not be described as the same as direct
masking.

### 11. Invalid / Empty / Failed-Lift Transition Semantics

Even with masks, failures can happen because of bugs, stale context, or race
between action-cell selection and concrete state.

We need explicit event categories:

```text
mask_empty
selected_action_not_executable
no_lift_candidate
stale_tower_context
fiber_departure
environment_invalid_after_lift
```

For PPO, these should not be silently converted into ordinary low reward. They
should be diagnostics and probably stop/truncate the episode for first-scope
tower PPO.

### 12. Rollout Step Semantics

We need to decide whether each sampled tower action always creates one PPO
sample.

My recommendation:

```text
Yes. One sampled action cell, one deterministic lift, one environment step,
one TrainingTransition, one PPO sample.
```

No multi-step options in the first design.

### 13. PPO Hyperparameter Defaults

We need initial defaults, but these are less conceptually dangerous.

Likely first defaults:

```text
gamma = 0.99
gae_lambda = 0.95
clip_epsilon = 0.2
entropy_coef = small nonzero, maybe 0.01
value_coef = 0.5
max_grad_norm = 0.5
target_kl = configured warning/stop threshold
ppo_epochs = 4
minibatch_size = config-dependent
rollout_steps = config-dependent
```

The important part is artifacting them, not pretending they are final.

### 14. Checkpoint And Trace Policy

We need to decide retention before implementation.

Minimum:

```text
checkpoint every N PPO updates
checkpoint best-so-far by configured metric
retain trace episodes by configured interval
retain first success
retain best reward
retain final episode
do not dump all step events by default
```

This is needed because Warehouse runs can explode artifacts.

### 15. Readout Claims

We need to decide what the first readout is allowed to claim.

Recommended boundary:

```text
This run demonstrates whether tower-structured PPO training executes correctly,
learns under its declared tower action surface, and improves selected training
metrics under a bounded budget.
It does not yet prove general tower superiority.
```

## Decisions That Can Wait

These should be named but not block the first blueprint:

- learned lift-candidate policy;
- tier-selection policy;
- options/semi-MDP PPO;
- multi-tier hierarchical PPO;
- separate actor per tier versus shared actor with tier embeddings;
- recurrent memory;
- vectorized environment workers;
- graph neural action encoders;
- large hyperparameter sweeps;
- public benchmark-level statistical comparison.

## My Proposed Locked First-Scope Design

If the PO agrees, the first blueprint should lock this:

```text
First serious Warehouse tower PPO trains a fixed-active-tier masked categorical
policy over executable abstract action cells. The sampled action is the action
cell id. A deterministic, artifacted live-lift rule maps that action cell to
one concrete Warehouse move. One PPO timestep equals one Warehouse second. The
critic sees the concrete state plus tower context. Empty masks and failed lifts
are diagnostic health failures, not hidden fallbacks. BBB owns PPO;
state_collapser supplies the tower/fiber/linearization semantics.
```

That is the smallest design that is genuinely tower PPO rather than a direct
policy wearing tower-themed metadata.

### PO turn
> No this is no good. Training needs to move up and down tower. WE ARE NO LONGER DOING SINGLE TIER SMOKE. WE ARE TESTING FULL TOWER.

### Codex turn

Correct. The fixed-tier diagnostic frame is no longer the target. The corrected
target is not:

```text
train one fixed-tier policy
```

The corrected target is full-tower PPO, but that does **not** mean PPO learns
tier traversal. The full tower target is:

```text
run the full hardcoded state_collapser tower traversal/runtime during rollout,
and train PPO only at the tier-local action-selection surfaces that traversal
reaches.
```

That changes the PPO observation and rollout context, but it does not move the
PPO random variable onto `LIFT`, `DESCEND`, or `TRAIN`. The PPO random variable
is still:

```text
sampled_action = tier-local executable action cell at the active execution
surface reached by hardcoded traversal
```

The hardcoded runtime may still do these things:

```text
lift
descend
train / maintenance event
route to an executable tier
route to a tier-local action-selection surface
```

But those are controller/runtime events, not PPO-sampled actions. Conceptually,
the policy learns:

```text
what tier-local action to choose when state_collapser's hardcoded traversal
asks for action selection at the current tower position
```

This also changes the critic. The critic cannot only value:

```text
V(concrete_state, fixed_active_tier)
```

It needs to value:

```text
V(concrete_state, full_tower_position, active_control_tier,
  tier-local action mask, traversal diagnostics)
```

because the same concrete state can have different future value depending on
the tower position and action surface reached by hardcoded traversal.

The corrected full-tower PPO sample record should look more like:

```text
source tower runtime snapshot
active control tier
available tier-local action-cell vocabulary
tier-local action mask
sampled tier-local action cell
old log probability of that sampled decision
resolved concrete Warehouse action through lift/resolve semantics
resulting Warehouse transition
target tower runtime snapshot
reward
terminated / truncated / diagnostic failure
bootstrap semantics
controller/traversal events since the previous PPO sample
```

The time rule should therefore separate controller events from environment
seconds:

```text
Only concrete Warehouse moves consume Warehouse time/reward.
Hardcoded tower traversal events are recorded as context and diagnostics.
They are not PPO action samples.
```

The updated first-scope target should therefore be:

```text
Full-tower PPO over tier-local action-selection surfaces reached by
state_collapser's hardcoded traversal. The policy observes concrete Warehouse
state, full tower position, active control tier, and the current tier-local
action mask. It samples a tier-local action cell whose log probability is
recorded exactly. The runtime resolves that action through state_collapser lift
semantics to a concrete Warehouse transition. PPO trains on that transition
stream with GAE and artifacted bootstrap semantics. Traversal events are
artifacted as runtime context, not learned actions.
```

That is the current full-tower PPO design spot.
