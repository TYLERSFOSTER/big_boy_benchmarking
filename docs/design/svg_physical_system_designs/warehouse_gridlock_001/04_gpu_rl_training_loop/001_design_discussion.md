# Warehouse Gridlock GPU RL Training Loop Design Discussion

## Purpose

This folder is for the next Warehouse Gridlock design block: a serious,
non-smoke RL training loop intended to train on GPU and to use the conceptual
framework developed in:

```text
docs/mathematical_notes_on_RL_training.md
```

This is a discussion surface only. It is not a blueprint, not an implementation
workplan, and not authority to change code.

## Attribution And Authority

### Project Owner

The Project Owner is directing this return to Warehouse Gridlock and has set
the immediate process constraint:

- do not jump into implementation;
- proceed through controlled design discussion first;
- use the RL training notes as a conceptual guide;
- build toward a real GPU training loop rather than another smoke-only or
  nominal "learning" surface.

The mathematical framing in `docs/mathematical_notes_on_RL_training.md` is the
Project Owner's synthesis. Codex may use it as source material for design
discussion, but should not claim authorship of that conceptual framework.

### Codex

Codex's role in this folder is to help translate the Project Owner's RL
training notes and Warehouse Gridlock goals into explicit design questions,
blueprints, workplans, and eventually implementation only after the Project
Owner authorizes each stage.

## Current Context

Warehouse Gridlock already has:

- a PO-authored SVG physical-system design;
- a BBB environment implementation and readiness readout;
- a masked direct vs live-lift tower diagnostic;
- a corrected full-state/full-action trainable policy contract;
- a first transformer actor-critic smoke implementation.

The transformer smoke path proved that BBB can run a real Torch-backed
optimizer step and retain selected traces, but it does not yet settle the
serious training architecture.

## Design Target

The intended next design target is a real RL training loop for Warehouse
Gridlock that:

- can run on GPU when available;
- has a serious rollout/training/update structure;
- uses explicit policy-gradient concepts rather than opaque candidate-id
  updates;
- preserves the Warehouse fairness boundaries around admissibility,
  no-lookahead, and live-lift semantics;
- makes artifact retention and movie generation intentional rather than
  accidentally enormous;
- gives the Project Owner enough control to inspect assumptions before code is
  written.

## Initial Discussion Slots

### Project Owner Turn

Ok I want to discuss implementing PPO. A central part of our discussion needs to be a *high level* conversation, half in the language of `docs/mathematical_notes_on_RL_training.md`, about turning PPO as described in that document into a strong, code implmentation that follows current best practices (without being bloated *at all*).

### Codex Turn

Yes. I think PPO is the right object to discuss first, but I also think the
danger is exactly what you are flagging: PPO can be implemented in a way that
looks "standard" while still being conceptually fake for this environment. For
Warehouse Gridlock, the important thing is not merely "use PPO"; it is to make
the probability law, action surface, admissibility handling, and update loop
line up with the mathematical story in `docs/mathematical_notes_on_RL_training.md`.

In the language of the notes, PPO is a controlled motion of probability mass.
The policy $\pi_\theta(a\mid s)$ induces a path measure over trajectories, and
the update uses

```math
\nabla_\theta\log\pi_\theta(a_t\mid s_t)
```

as the infinitesimal multiplicative change of probability mass assigned to the
sampled action. The advantage term says which sampled actions should receive
more or less mass. The likelihood ratio

```math
r_\theta(s,a)
=
\frac{\pi_\theta(a\mid s)}
{\pi_{\mathrm{old}}(a\mid s)}
```

is the finite multiplicative comparison between the new policy and the old
policy. PPO clipping is then a deliberately crude but effective trust-region
device: let probability mass move in the advantage-improving direction, but
do not let any one update multiply the old probability by too much. That is
the high-level bridge from your notes to code.

The best-practice implementation should therefore be minimal but real:

- collect rollouts under a frozen old policy;
- store observations, actions, old log probabilities, rewards, done flags, and
  value estimates;
- compute returns and advantages, almost certainly with GAE unless we decide
  against it explicitly;
- normalize advantages within the update batch;
- run several minibatch epochs of clipped PPO;
- include value loss, entropy bonus, gradient clipping, and approximate-KL /
  clip-fraction diagnostics;
- stop or warn if KL motion is too large;
- checkpoint model, optimizer, config, RNG state, and enough rollout metadata
  to interpret the run;
- retain selected episode traces for movies without dumping every step of every
  episode forever.

That is the non-bloated core. I would resist adding distributed rollout,
recurrent policies, curriculum schedulers, hyperparameter sweeps, fancy logging
backends, or many baseline variants until the single-GPU PPO path is clean and
legible.

For Warehouse, the most important design issue is the action distribution. PPO
needs the log probability of the action that was actually executed, under the
policy that sampled it. If our model emits a full simultaneous action vector
directly, this is clean: the probability of the vector is the product/sum of
per-robot action probabilities under a factorized policy, with masks applied
before sampling. If instead the model emits a proposal and a resolver repairs
or projects it into a valid action, then PPO can become mathematically
ambiguous: the log probability of the proposal is not necessarily the log
probability of the executed action. That exact point needs design attention.

My initial recommendation is:

```text
Start with a direct, factorized, masked simultaneous-action distribution.
Each robot has a categorical distribution over {stay, north, south, east, west}.
The sampled joint action is the product distribution over robots.
The environment applies the existing ensemble transition validity rule.
Invalid sampled ensembles should be handled by an explicit policy that we choose
and artifact, not hidden by silent repair.
```

The hard question is what that invalid-action policy should be. For a serious
PPO implementation, I do not want silent projection unless we can account for
the probability law correctly. Safer first options are:

- mask only per-robot physically impossible primitive moves, while allowing
  ensemble invalidity to be an environment outcome;
- or use a candidate-set policy where the policy samples among explicitly
  valid generated joint actions, so the sampled object and executed object are
  the same;
- or implement a mathematically honest rejection/resampling rule and record the
  effective distribution, though that may get ugly fast.

This is probably the first major discussion fork.

The second major fork is tower PPO. I do not think we should pretend this is
already solved by the existing transformer smoke. A direct PPO arm has a clear
state/action distribution. A tower PPO arm has to say what the policy actually
samples: an abstract action cell, a concrete lift candidate, a tier choice, a
concrete vector scored with tower context, or some composition of these. PPO
can train any of those if we can write down the sampled action, the old log
probability, the executed transition, and the value baseline cleanly. But if
we cannot say what random variable the policy sampled, we do not yet have PPO;
we have a heuristic controller with gradients.

So I would structure the design conversation around these questions:

1. What is the first serious PPO arm: direct only, tower only, or paired
   direct/tower?
2. What is the sampled action random variable for that arm?
3. Is the action distribution over per-robot primitives, generated valid joint
   actions, abstract tower cells, concrete lifts, or something else?
4. How do admissibility masks enter without giving one arm an unfair
   information surface?
5. What happens when an invalid ensemble is sampled?
6. What value function is being learned, and on what observation/tier surface?
7. What rollout size, minibatch size, PPO epochs, gamma, lambda, clip epsilon,
   entropy coefficient, value coefficient, and target KL are the initial
   minimal defaults?
8. What artifacts are required for us to trust that the run is real PPO rather
   than another nominal training surface?

My strongest current recommendation is to start the blueprint with a
single-GPU, direct-only PPO training loop that is mathematically clean, then
add tower PPO only once we have a precise random-variable story for the tower
action. That may feel less ambitious, but it gives us a hard reference
implementation of PPO in this environment. Then tower work has something real
to be compared against.

### Project Owner Turn

Explain *GAE*, both in present mathematical language, and in high level implmentation language.

### Codex Turn

GAE means *Generalized Advantage Estimation*. It is not a new objective and it
is not the PPO-specific clipping mechanism. It is the practical estimator we
usually use for the advantage term

```math
A^\pi(s_t,a_t)
=
Q^\pi(s_t,a_t)-V^\pi(s_t)
```

that appears inside the policy-gradient / PPO update.

In the language of your notes, the policy-gradient term wants to know how to
move probability mass multiplicatively:

```math
\widehat A_t
\nabla_\theta \log \pi_\theta(a_t\mid s_t).
```

The score term

```math
\nabla_\theta \log \pi_\theta(a_t\mid s_t)
```

says *which bit of probability mass is being infinitesimally changed*. The
advantage estimator says *whether that sampled action deserves more or less
mass than the policy's current average behavior at that state*. GAE is a way of
constructing that second scalar with a tunable bias/variance tradeoff.

The clean starting point is the one-step temporal-difference residual:

```math
\delta_t
=
r_t
+
\gamma V(s_{t+1})
-
V(s_t).
```

This is an instantaneous surprise/correction signal for the critic: after
seeing reward $r_t$ and the next value estimate, was the old estimate $V(s_t)$
too low or too high? If $\delta_t$ is positive, the transition was better than
the critic expected. If negative, worse.

Plain one-step actor-critic could use $\delta_t$ as the advantage estimate,
but that is too local. Monte Carlo return minus value,

```math
G_t - V(s_t),
```

uses the whole future trajectory, but it is high variance. GAE interpolates
between these by summing future TD residuals with geometric decay:

```math
\widehat A_t^{\mathrm{GAE}(\gamma,\lambda)}
=
\sum_{\ell=0}^{\infty}
(\gamma\lambda)^\ell
\delta_{t+\ell}.
```

In finite rollouts, this becomes a backward recursion:

```math
\widehat A_t
=
\delta_t
+
\gamma\lambda(1-d_{t+1})\widehat A_{t+1}.
```

Here $d_{t+1}$ is a terminal flag. If the episode ended, the recursion stops.

The parameter $\gamma$ is the usual reward-discount factor. The parameter
$\lambda$ controls how far advantage credit reaches into the future:

- $\lambda=0$ gives mostly one-step TD advantage, low variance but more bias;
- $\lambda=1$ approaches Monte Carlo-style return-minus-value, lower bias but
  higher variance;
- common PPO practice uses something like `gamma=0.99`, `gae_lambda=0.95`,
  then treats those as tunable defaults.

The value target used to train the critic is usually:

```math
\widehat R_t
=
\widehat A_t
+
V(s_t).
```

So GAE gives us two things:

- `advantages`: used in the policy loss;
- `returns` or `value_targets`: used in the value loss.

High-level implementation language:

1. During rollout, store for each timestep:
   - observation;
   - sampled action;
   - old log probability;
   - reward;
   - done flag;
   - value estimate from the critic;
   - optionally next value or final bootstrap value.
2. After collecting a rollout chunk, run a reverse-time pass.
3. For each step from last to first, compute:

```text
delta = reward[t] + gamma * next_value * nonterminal - value[t]
advantage[t] = delta + gamma * gae_lambda * nonterminal * next_advantage
return[t] = advantage[t] + value[t]
```

4. Normalize advantages across the training batch:

```text
advantage = (advantage - mean) / (std + eps)
```

5. Feed `observation`, `action`, `old_log_prob`, `advantage`, and `return`
   into PPO minibatch updates.

For Warehouse Gridlock, GAE matters because rewards are delayed and structured.
An action that helps open a corridor, move a box, or avoid a future jam may not
look good immediately. One-step TD is likely too myopic. Pure Monte Carlo is
likely too noisy because the action space and horizon are huge. GAE is the
standard practical compromise: it lets later evidence flow backward through the
trajectory without making every update depend equally on the entire remaining
episode.

One design caution: invalid-action semantics interact with GAE. If invalid
ensemble attempts do not advance time and yield zero invalid penalty, then a
policy can produce many "no time advanced" transitions unless we decide how
rollout steps are counted. For PPO/GAE, every sampled action in the rollout is
a training sample. If invalid/self-loop samples exist, they still affect
advantages unless they are masked out before sampling. So before implementation
we need to decide whether the PPO training loop samples only from an
admissible/generated action set, or whether invalid attempts become real
training transitions with rewards/dones/time flags. GAE will faithfully
propagate whatever semantics we choose.

My practical recommendation for the first serious PPO implementation is:

```text
Use GAE.
Default gamma = 0.99.
Default gae_lambda = 0.95.
Normalize advantages per PPO update batch.
Store raw and normalized advantage statistics in artifacts.
Record bootstrap handling at time-limit truncation separately from true terminal success.
```

That last line is important. In Warehouse, an episode can end because the task
is solved, or because the time horizon is exhausted. GAE should treat those
differently:

- true terminal success: no bootstrap from next value;
- time-limit truncation: usually bootstrap from the critic's final value,
  because the underlying process did not naturally terminate.

If we do that cleanly, GAE becomes exactly the bridge from your mathematical
advantage story to a robust PPO implementation.

### Project Owner Turn

Let's discuss actual design. Given the current warehouse gridlock environment, what are the main surfaces or "pieces" needed for the PPO training. Keep in mind existing structure in `state_collapser`. Maybe re-investigate that repo to align well. 

### Codex Turn

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

This gives us a non-[XXX] PPO trainer first. Then we can ask the harder
tower question with a real reference implementation beside it.


### Project Owner Turn
Copy that last reponse over to a new document in this same folder

### Codex Turn

Copied the prior Codex response into:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/ppo_training_surface_map.md
```

I kept the new file as a standalone design reference, not a blueprint,
workplan, or implementation authority. The point is to preserve the PPO
surface map separately so we can refer to it directly when the discussion
turns into a blueprint.
