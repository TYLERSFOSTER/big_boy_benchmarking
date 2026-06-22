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

## My Current Slice Recommendation

For the first serious design blueprint, I would propose this order:

1. Direct Warehouse PPO with a clean action probability law.
2. GPU/device/checkpoint/trace/artifact discipline.
3. PPO readout proving real clipped PPO, GAE, KL, entropy, and value updates.
4. Only after that, tower PPO design using state_collapser tower/fiber
   semantics.

This gives us a non-bullshit PPO trainer first. Then we can ask the harder
tower question with a real reference implementation beside it.
