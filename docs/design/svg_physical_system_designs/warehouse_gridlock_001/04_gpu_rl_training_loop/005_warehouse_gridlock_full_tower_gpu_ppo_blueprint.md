# Warehouse Gridlock Full-Tower GPU PPO Blueprint

## Purpose

This blueprint defines the intended design for a serious Warehouse Gridlock
GPU PPO training loop, its associated per-tier policy models, its use of
`state_collapser` hardcoded tower traversal, and the first evaluation family
that should exercise it.

This is a blueprint. It is not an implementation workplan and not
implementation authority. The next artifact should be a Phase.Stage.Action
implementation workplan if the Project Owner approves this blueprint.

## Source Documents And Precedence

This blueprint is based on the design folder:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop
```

The source documents are:

```text
001_design_discussion.md
002_ppo_training_surface_map.md
003_tower_traversing_logic_discussion.md
004_blueprint_decision_gates_for_full_tower_gpu_ppo.md
```

Precedence for conflicts:

1. `004_blueprint_decision_gates_for_full_tower_gpu_ppo.md` controls the
   resolved decision gates.
2. `003_tower_traversing_logic_discussion.md` controls tower traversal and
   model-family semantics.
3. The corrected tail of `002_ppo_training_surface_map.md` controls general
   PPO surfaces where it does not conflict with `003` or `004`.
4. `001_design_discussion.md` supplies early PPO/GAE/background framing and
   is superseded wherever later documents correct it.

The following earlier ideas are explicitly superseded and must not be revived
in implementation:

```text
direct-only PPO as the first target;
fixed-active-tier tower PPO;
PPO learning tier traversal;
direct as a separate direct-control policy family;
shared learned parameters across tier policies;
representative fallback for executable lift resolution;
mutable episode/time/PPO facts inside state/action geometry JSONs.
```

## Authority And Attribution

### Project Owner-Originated Design

The following architectural ideas are Project Owner-originated and should be
attributed to Tyler Foster:

```text
1. The Warehouse Gridlock environment is a PO-authored SVG physical-system
   design and hidden/discovered state-action graph benchmark target.

2. The serious training loop should be a real PPO-style RL training loop using
   the mathematical framing from docs/mathematical_notes_on_RL_training.md.

3. Full-tower training means the hardcoded state_collapser tower runtime moves
   through the tower during rollout; PPO does not learn tier traversal.

4. The policy model for a tier uses richly encoded state/action records,
   state history, action history, and a transformer-shaped architecture.

5. The policy should define a distribution over Out_k(s_t), not over a fixed
   global output vector.

6. The clean action-scoring form is:

   history_encoder_k(state_hist, act_hist) -> c_t
   candidate_encoder_k(edge_json, src_state, tgt_state, tier, time) -> u_i
   score_k(c_t, u_i) -> logit_i
   masked softmax over i with a_i in Out_k(s_t)

7. For PPO, each tier has:

   policy_k         = current trainable model
   rollout_policy_k = frozen snapshot used to collect the rollout

8. There is a separate policy model for each tier. The tier policies are not
   explicitly parameter-coupled. They share an architecture family, and model
   capacity should decay in a controlled way as tier index increases down the
   tower.

9. Direct is the no-contraction schema arm, not a separate direct-control
   policy family.
```

### Codex Role

Codex's role is to organize the design into an implementable architecture,
identify contracts and artifacts, and make conservative engineering
recommendations where the Project Owner has not locked an exact parameter.
Codex should not claim authorship of the Project Owner-originated model
family, mathematical framing, or SVG environment design.

## Scope

This blueprint covers:

```text
full-tower PPO rollout semantics;
per-tier policy model family;
old/new PPO model snapshot handling;
geometry records, decision context, and rollout sample records;
state_collapser integration boundaries;
pointwise executable action surfaces;
PPO update loop, GAE, checkpoints, and GPU/device handling;
artifact and readout contracts;
first evaluation family and claim boundaries;
test and verification plan.
```

This blueprint does not cover:

```text
implementation steps;
final hyperparameter tuning;
large statistical benchmark claims;
learning tier traversal;
learned lift-candidate selection;
semi-MDP/options PPO;
distributed rollout;
vectorized Warehouse simulation;
public benchmark leaderboard design.
```

Those may be later design blocks.

## Terminology And Direction Convention

### Tower Direction

Use this convention everywhere:

```text
tier index 0 is uppermost;
passing from i to i + 1 moves down the tower.
```

Avoid casual "up" and "down" language unless it follows this convention.

### Graph And Tower Notation

Use:

```text
G^0_t:
  the currently discovered concrete state-action graph at time/discovery
  stage t.

Sigma^bullet_t:
  the contraction schema/tower-building data at time/discovery stage t.

G^bullet_t:
  the quotient tower derived from G^0_t and Sigma^bullet_t.

G^k_t:
  tier k of the current quotient tower.
```

### Three Kinds Of Records

The design must keep these distinct:

```text
Geometry record:
  immutable-within-snapshot description of state/action space geometry as
  currently understood.

Decision context:
  episode/time/runtime-local information at a decision point.

Rollout sample:
  PPO-specific sample data collected under rollout_policy_k.
```

This distinction is mandatory. Episode-specific or time-step-specific facts
must not be placed inside state/action geometry records.

## High-Level Design Statement

Warehouse Gridlock full-tower GPU PPO uses `state_collapser` hardcoded tower
traversal. The PPO actor does not choose `LIFT`, `DESCEND`, `TRAIN`, or tier
traversal. The PPO actor is invoked only when hardcoded traversal reaches a
tier-local, pointwise executable action-selection surface.

For each non-degenerate tier `k`, the training system maintains:

```text
policy_k:
  current trainable tier-k model.

rollout_policy_k:
  frozen snapshot of policy_k used to collect the current rollout batch.
```

The model samples an action from the current tier-local outgoing set:

```text
a_t in Out_k(s_t)
```

using a candidate-scoring masked softmax. The rollout record stores the exact
decision surface, selected local index, selected action id, old log
probability, and value estimate. PPO updates recompute the probability of the
same selected action against the same stored decision surface under
`policy_k`.

Direct comparison is represented as a no-contraction schema arm. Nontrivial
tower arms are represented by nontrivial contraction schemas. The same
training/evaluation machinery should handle both by schema selection.

## Existing BBB Context To Reuse

The current Warehouse implementation already has:

```text
environment readiness;
masked direct vs live-lift tower diagnostic;
full-state/full-action trainable policy contract;
transformer policy smoke path;
trace retention and GIF rendering machinery;
CLI surfaces under warehouse-gridlock;
artifact/readout patterns used across Warehouse, Counterpoint, and PlateSupport.
```

This blueprint should reuse those lessons, but it must replace the previous
nominal/smoke training with a real PPO rollout/update loop.

Existing patterns to preserve:

```text
repo-resident artifact roots under docs/evaluations;
readout_source.json as the input surface for human-readable report generation;
explicit dependency/state_collapser manifests;
selected trace retention for movies;
separate run/summarize/render CLI commands;
structured CSV/JSON summaries, not ad hoc logs.
```

## State-Collapser Integration Boundary

BBB is the benchmarking/evaluation repo. It should not fork or clone
`state_collapser` semantics.

`state_collapser` owns:

```text
tower/fiber/runtime handoff semantics;
ActiveTierController;
ActiveTierState;
ControlAction;
ExploitExploreTowerRuntime traversal semantics;
PartitionTower queries;
pointwise executable action/lift semantics;
LinearizationConfig;
EncodingRegistry;
LinearizationReport;
Torch conversion surfaces where upstream exposes them.
```

Minimum dependency expectation:

```text
state_collapser v0.7.2 or newer compatible pointwise liftability semantics.
```

BBB owns:

```text
Warehouse environment wrapping;
PPO rollout collection;
PPO update/loss/optimizer loop;
Warehouse-specific policy model code;
evaluation orchestration;
artifact and human-readable readout generation;
benchmark claim boundaries.
```

Required implementation rule:

```text
Before adding a BBB-local representation that overlaps state_collapser, check
whether state_collapser already exposes it. If it does, use it. If it does not,
record the gap and decide whether the fix belongs upstream instead of silently
cloning the concept downstream.
```

If an upstream surface is missing and blocks clean implementation, the workplan
must stop at that boundary and produce a design note for either BBB adapter
work or upstream `state_collapser` work.

## Tower Runtime Semantics

### Hardcoded Traversal

Full-tower training means:

```text
run the full hardcoded state_collapser tower traversal/runtime during rollout;
train PPO only at tier-local action-selection surfaces reached by traversal.
```

The runtime may emit controller/traversal events:

```text
LIFT
DESCEND
TRAIN
EXPLORE
EXPLOIT_EXECUTE
NO_AVAILABLE_ACTION
automatic lift-to-executable-tier steps
```

These events are diagnostics and context. They are not PPO-sampled actions.

### PPO Action Samples

A PPO sample occurs only when the hardcoded runtime reaches a pointwise
executable tier-local action-selection surface and asks the actor for a
behavior action.

At that boundary:

```text
active tier = k
current tier state = s_t
candidate set = Out_k(s_t) in canonical order
mask = executable candidate mask
sampled action = a_t in Out_k(s_t)
```

The PPO random variable is:

```text
sampled_action = tier-local action chosen at the reached execution surface
```

It is not:

```text
LIFT | DESCEND | TRAIN | tier traversal control.
```

### TRAIN Events

`ControlAction.TRAIN` is part of the current `state_collapser` reference
runtime vocabulary. PPO optimizer updates, however, are outer-loop updates
over rollout buffers.

Blueprint rule:

```text
Do not make TRAIN a PPO-sampled action.
Do not treat PPO optimizer updates as environment actions.
During rollout, either configure the runtime so TRAIN does not trigger
learner updates, or record TRAIN as hardcoded maintenance/context.
Run PPO updates outside the tower traversal loop after rollout collection.
```

If `TRAIN` must preserve upstream runtime invariants, artifact it as a
controller event, not as a policy sample.

## Pointwise Executability And Lift Semantics

This design reuses the settled v0.7.2 pointwise-liftability semantics from
prior BBB work.

Required rule:

```text
The PPO actor is called only at a nonempty pointwise executable action surface.
```

Before PPO sampling, hardcoded traversal must use current-state executability:

```text
tier_is_executable = tier_is_executable_from_state(tier, current_base_state)
```

Action cells available for policy sampling must be pointwise executable from
the current concrete state:

```text
pointwise_executable_action_cells(tier, state_cell)
  = quotient action cells with nonempty
    executable_lift_candidates(tier, action_cell, current_base_state)
```

Execution must use strict executable lift candidates:

```text
fetch pointwise executable vocabulary;
map selected local index to action cell;
call executable_lift_candidates(tier, action_cell, current_base_state);
choose the first strict executable lift candidate by default;
execute that concrete action;
record representative candidate counts only as diagnostics;
do not fallback to action_cell_members(...) for execution.
```

If no executable tier/action exists:

```text
record NO_AVAILABLE_ACTION as a runtime/control diagnostic;
do not create a PPO sample;
do not invent a synthetic action;
do not use representative fallback.
```

If a PPO actor boundary receives an empty surface, treat it as an invariant
violation or stale-surface race. Record a diagnostic failure and do not train
from a fake sample.

## Time And Reward Semantics

The training loop must track separate counters:

```text
controller_event_index
ppo_sample_index
environment_second
episode_index
global_update_index
```

Rules:

```text
Hardcoded traversal events do not directly consume Warehouse time.
Concrete Warehouse moves consume Warehouse time.
PPO rewards come from concrete Warehouse transitions.
Traversal events since the previous PPO sample are recorded as context.
```

The rollout sample should attach the reward from the concrete transition
resolved from the selected tier-local action.

Termination and truncation must remain distinct:

```text
terminated:
  true environment success/failure terminal condition.

truncated:
  time limit, diagnostic limit, configured training cutoff, or similar
  nonterminal cutoff.
```

GAE/bootstrap semantics must use this distinction.

## Direct And Tower Arms

### Direct Arm

Direct is the no-contraction schema arm:

```text
schema0_no_contraction
```

It is not a separate direct-control policy family. It uses the same general
structured record/history/candidate-scoring PPO machinery applied to the
no-contraction tower. Its active action surface is the `G^0_t` outgoing action
surface under the no-contraction schema.

### Tower Arm

A tower arm is a nontrivial contraction schema:

```text
schema1_or_later
```

The first serious evaluation should support one configured nontrivial schema
as the main tower arm, with the option to add more schema arms later.

### Comparison Boundary

The first comparison asks:

```text
Under the same Warehouse environment and PPO machinery, does the nontrivial
contraction-schema tower arm learn differently from the no-contraction schema
arm?
```

It does not claim:

```text
general tower superiority;
final robotics performance;
statistical benchmark-level proof;
learned traversal superiority.
```

## Geometry Records

Geometry records describe the state/action space as currently understood.
They are stable within a graph/tower snapshot. They must not contain mutable
episode/time/PPO facts.

Forbidden in geometry records:

```text
current_second
remaining_seconds
old_log_prob
new_log_prob
value_estimate
advantage
return
reward
terminated
truncated
episode_index
rollout_update_index
selected_action
runtime event counters
```

Those belong in decision-context or rollout-sample records.

### State Geometry Record

Required state geometry fields:

```text
schema_version
graph_snapshot_id
tower_snapshot_id
tier_index
tier_direction_convention = "0_uppermost_i_to_i_plus_1_down"
state_cell_id
state_coset_member_ids
state_coset_size
parent_state_cell_id
child_state_cell_ids
outgoing_action_cell_ids
outgoing_action_count
quotient_adjacency_summary
known_one_hop_geometry
geometry_source_manifest_ref
```

Recommended state geometry fields:

```text
state_cell_label
representative_state_id_for_readout_only
base_state_member_count
internal_edge_count
boundary_edge_count
target_relation_summary
blocked_region_relation_summary
robot_position_set_summary_if_static_to_state
box_position_set_summary_if_static_to_state
```

The record may serialize to JSON for artifacts, but the tensor path should
consume typed fields or deterministic tokenization of these fields.

### Action Geometry Record

Required action geometry fields:

```text
schema_version
graph_snapshot_id
tower_snapshot_id
tier_index
action_cell_id
source_state_cell_id
target_state_cell_id
member_edge_ids
member_edge_count
lower_or_child_action_cell_ids
representative_edge_ids_for_readout_only
out_hom_or_action_hom_summary
geometry_source_manifest_ref
```

Recommended action geometry fields:

```text
action_cell_label
base_concrete_action_summary
source_coset_size
target_coset_size
lift_candidate_geometry_count
representative_candidate_count_for_diagnostics
known_internal_or_boundary_class
```

The geometry action record may include representative evidence for explanation,
but execution must not use representative fallback.

### Record Tokenization Manifest

Every run must artifact a record-tokenization manifest:

```text
record_schema_version
geometry_record_kind = state | action
field_list
field_sources
variable_length_field_encoding_ops
token_dim
hashing_or_id_embedding_policy
unknown_field_policy
snapshot_id
```

Variable-length field encoding is a tokenization detail, not a separate
mathematical coupling layer. The coset/Young-diagram data itself is the record
content.

## Decision Context Records

Decision context records capture runtime-local facts at an action-selection
point.

Required fields:

```text
decision_context_id
episode_id
ppo_sample_index
controller_event_start_index
controller_event_end_index
environment_second
active_tier
active_tier_state_id
current_concrete_state_id_or_digest
current_position_at_every_tier
tower_position_key
runtime_snapshot_id_or_digest
schema_arm_id
graph_snapshot_id
tower_snapshot_id
state_geometry_record_id
candidate_action_geometry_record_ids_in_order
candidate_local_indices
candidate_mask
mask_kind = pointwise_executable
mask_source = state_collapser
mask_semantics_id
controller_events_since_previous_sample
```

The decision context is what the policy sees, together with geometry tokens
and history. It may include time/episode facts because it is not a geometry
record.

## Rollout Sample Records

Rollout samples are PPO training records collected under `rollout_policy_k`.

Required fields:

```text
rollout_sample_id
decision_context_id
tier_index
policy_snapshot_id
rollout_policy_snapshot_id
state_hist_refs_or_serialized_tokens
act_hist_refs_or_serialized_tokens
candidate_action_ids_in_order
candidate_mask
selected_local_index
selected_action_id
old_log_prob
value_estimate
entropy_at_sample
resolved_concrete_action_id_or_digest
lift_candidate_id_or_digest
lift_resolution_semantics_id
reward
next_decision_context_ref_if_available
terminated
truncated
bootstrap_allowed
bootstrap_reason
diagnostic_failure_kind
```

PPO updates must not reconstruct `Out_k(s_t)`, masks, or selected local
indices from a later live graph. The rollout sample preserves the old decision
surface.

## Histories

For tier `k`, the model consumes:

```text
state_hist = (s_0, s_1, ..., s_t)
act_hist   = (a_0, a_1, ..., a_{t-1})
```

Here `s_i` and `a_i` refer to tier-local state/action geometry records plus
decision-context facts as appropriate.

History policy:

```text
History belongs to the model input.
The current sampled action is the PPO random variable.
The old log probability belongs only to the current sampled action under
rollout_policy_k.
```

First implementation should define:

```text
max_history_length
history_truncation_policy
history_padding_policy
whether histories are per-tier or stitched across tier dispatches
```

Recommended first default:

```text
per-tier histories, capped by max_history_length, with oldest-prefix truncation.
```

The blueprint permits a later cross-tier history design, but first-scope PPO
should keep history reconstruction simple and artifactable.

## Per-Tier Model Family

### Policy Bank

The training system maintains a policy bank:

```text
policy_bank = {
  tier_index k:
    policy_k
    rollout_policy_k
    optimizer_k
    rollout_buffer_k
    capacity_config_k
}
```

Policy bank rules:

```text
one separate policy model per non-degenerate tier;
one separate frozen rollout policy snapshot per active tier;
no explicit learned parameter sharing between tier policies;
same architecture family across tiers;
controlled capacity decay as tier index increases down the tower.
```

### Capacity Schedule

First default:

```text
capacity_k = max(min_capacity, round(capacity_0 * gamma_capacity**k))
```

where:

```text
k = tier index;
k = 0 is uppermost;
k -> k + 1 moves down the tower;
0 < gamma_capacity <= 1.
```

The capacity schedule must be artifacted:

```text
capacity_schedule_id
capacity_0
gamma_capacity
min_capacity
per_tier_hidden_dim
per_tier_layer_count
per_tier_attention_heads
per_tier_parameter_count
```

The exact defaults are future-tunable. The blueprint should require a
configurable schedule and visible manifests.

### Tier Model Shape

For each non-degenerate tier `k`:

```text
history_encoder_k(state_hist, act_hist) -> c_t
candidate_encoder_k(edge_json, src_state, tgt_state, tier, time) -> u_i
score_k(c_t, u_i) -> logit_i
masked softmax over i with a_i in Out_k(s_t)
value_head_k(c_t, decision_context) -> V_k
```

The model should be transformer-shaped:

```text
structured state/action records -> tokens;
state/action history -> contextual representation;
current candidate action records -> candidate tokens;
context/candidate scorer -> logits over current Out_k(s_t);
critic head -> scalar value estimate.
```

### Candidate Scoring

Do not use a fixed global output vector over all possible discovered actions.
Use a local candidate set:

```text
Out_k(s_t) = (a_1, ..., a_m)
```

with canonical order. Then:

```text
logit_i = score_k(c_t, u_i)
pi_k(a_i | s_t) = masked_softmax_i(logit_i)
```

For batching:

```text
pad candidate sets to max width in minibatch;
use boolean masks;
store original candidate order and ids in rollout samples.
```

### Action Token Encoding

Action tokens must encode edge/morphism structure:

```text
action geometry token
time-step or history-position encoding
source-state encoding
target-state encoding
tier-index encoding
```

This is required because actions are edges between states, not free-floating
labels.

### Value Function

The critic should see at least what the actor sees. It should estimate:

```text
V_k(decision context, state/action history, tower context)
```

The critic input must include enough context to distinguish:

```text
same concrete Warehouse state;
different tower position;
different active tier;
different candidate surface;
different traversal diagnostics.
```

The value estimate stored in the rollout sample is produced by
`rollout_policy_k`.

## PPO Snapshot Semantics

For each tier `k`:

```text
policy_k:
  trainable current model.

rollout_policy_k:
  frozen snapshot used for rollout collection.
```

During rollout:

```text
a_t ~ rollout_policy_k(. | input_t)
old_log_prob_t = log rollout_policy_k(a_t | input_t)
value_estimate_t = V_rollout_policy_k(input_t)
```

During PPO update:

```text
new_log_prob_t = log policy_k(a_t | stored_input_t)
ratio_t = exp(new_log_prob_t - old_log_prob_t)
```

After the update interval:

```text
rollout_policy_k <- copy(policy_k)
```

The policy snapshot manifest must include:

```text
tier_index
policy_snapshot_id
rollout_policy_snapshot_id
model_architecture_id
capacity_config_id
parameter_count
optimizer_state_ref
created_at_update_index
source_snapshot_id_if_copied
```

## Dynamic Graph Growth

Discovery-driven geometry changes are expected. They are not a conceptual
blocker.

The model may see unstable early geometry:

```text
early exploration can radically shift downstairs tiers;
learned embeddings and attention heads may be temporarily misaligned;
as exploration stabilizes, embeddings should become largely right and
adjustable.
```

This is a training dynamics issue, not a reason to freeze discovery entirely.

However, PPO bookkeeping must remain exact:

```text
Every PPO sample stores the exact decision surface used at sampling time.
PPO updates use stored candidate ids, order, masks, selected index, and old
log probability.
PPO updates do not recompute candidate order or masks from a later live graph.
```

When new non-degenerate tiers appear:

```text
initialize policy_k and rollout_policy_k at a named synchronization point;
record initialization reason;
record capacity schedule values;
do not silently insert a new policy mid-update without a manifest entry.
```

## PPO Rollout Collection

### Outer Loop

First-scope outer loop:

```text
initialize environment and schema arm;
initialize graph/tower state;
initialize per-tier policy bank;
copy policy_k to rollout_policy_k for active tiers;
collect rollout samples until update budget is reached;
compute GAE/returns by tier or configured rollout stream;
update policy_k models from stored samples;
refresh rollout_policy_k snapshots;
checkpoint and summarize;
repeat.
```

### Sample Grouping

Because policies are separate per tier, samples should be grouped by tier for
model update:

```text
rollout_buffer_k contains samples collected when traversal invoked tier k.
policy_k updates from rollout_buffer_k.
```

If a tier has too few samples for a full minibatch, supported options are:

```text
skip update for that tier and carry samples forward;
run a small-batch update if above a configured minimum;
emit low_sample_count diagnostics.
```

Recommended first default:

```text
carry samples forward until min_samples_per_tier_update is reached,
unless the run ends, in which case perform a final small-batch update with a
diagnostic flag.
```

### Environment Episode Handling

Each episode records:

```text
episode_index
schema_arm_id
seed
initial_environment_state
initial_graph_snapshot_id
initial_tower_snapshot_id
terminal_status
total_environment_seconds
total_controller_events
total_ppo_samples
total_reward
success
diagnostic_failure_kind
```

Warehouse time advances only on concrete Warehouse moves.

## GAE And Returns

Use GAE by default:

```text
delta_t = reward_t + gamma * V(next_state) * nonterminal - V(state_t)
adv_t = delta_t + gamma * gae_lambda * nonterminal * adv_{t+1}
return_t = adv_t + V(state_t)
```

Bootstrap semantics:

```text
true terminal success:
  no bootstrap.

time-limit truncation:
  bootstrap if final value is defined and bootstrap_allowed = true.

diagnostic failure:
  use explicit bootstrap_reason. Default to no bootstrap unless the failure is
  a benign run cutoff.

NO_AVAILABLE_ACTION:
  runtime/control diagnostic, not a PPO sample. Episode-level handling should
  mark the diagnostic and avoid fake action samples.
```

Advantages should be normalized per update batch, ideally per tier:

```text
advantage_normalization_scope = per_tier_update_batch
```

Artifact required:

```text
raw_advantage_mean/std/min/max
normalized_advantage_mean/std/min/max
return_mean/std/min/max
bootstrap_reason_counts
terminated_count
truncated_count
diagnostic_failure_count
```

## PPO Update Engine

The update loop:

```text
for each tier k with enough rollout samples:
  for ppo_epoch in 1..ppo_epochs:
    shuffle tier rollout samples
    for minibatch:
      reconstruct stored decision surfaces
      recompute log_prob, entropy, and value under policy_k
      ratio = exp(new_log_prob - old_log_prob)
      actor_loss = -mean(min(ratio * advantage,
                             clipped_ratio * advantage))
      value_loss = configured value objective
      entropy_loss = -entropy_coef * entropy
      total_loss = actor_loss + value_coef * value_loss + entropy_loss
      backprop
      clip gradients
      optimizer step
      record diagnostics
  refresh rollout_policy_k after update interval
```

Required diagnostics:

```text
policy_loss
value_loss
entropy
approx_kl
clip_fraction
explained_variance
gradient_norm
learning_rate
samples_used
minibatch_count
ppo_epoch_count
update_wall_time_seconds
device_actual
```

Approximate KL warnings:

```text
if approx_kl > target_kl:
  mark update warning;
  optionally early-stop PPO epochs for that tier according to profile.
```

## Device And Tensorization

Supported device modes:

```text
tensor_enabled_cpu
tensor_enabled_cuda
```

Device policy:

```text
request cuda when profile requires GPU;
fall back to CPU only if profile permits fallback;
record requested device and actual device;
fail loudly if serious_gpu requires CUDA and CUDA is unavailable.
```

First default:

```text
mixed_precision = false
dtype = float32
```

Mixed precision can be added later.

Artifact required:

```text
device_requested
device_actual
torch_version
cuda_available
cuda_device_name
dtype
mixed_precision
model_parameter_count_by_tier
tensorization_timing_summary
update_throughput_samples_per_second
rollout_throughput_env_seconds_per_second
```

## Named Training Profiles

The first implementation should expose named profiles:

```text
smoke_cpu
debug_gpu
serious_gpu
```

### smoke_cpu

Purpose:

```text
CI/local correctness.
```

Expected traits:

```text
small episode count;
small rollout batch;
short max seconds;
CPU allowed;
detailed traces for a few episodes;
strict invariants.
```

### debug_gpu

Purpose:

```text
short GPU run for validating real CUDA PPO mechanics.
```

Expected traits:

```text
GPU requested;
moderate rollout samples;
frequent checkpointing;
more detailed diagnostics;
selected traces retained.
```

### serious_gpu

Purpose:

```text
long local/VM training run.
```

Expected traits:

```text
GPU required unless overridden;
selected trace retention only;
checkpoint at update intervals;
summary rows for all episodes and updates;
no exhaustive step/candidate dump by default.
```

Every run must expand and artifact:

```text
profile_id
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
checkpoint_interval_updates
trace_retention_policy
capacity_schedule
```

Hyperparameter values are future-tunable and should not be treated as final
benchmark commitments.

## Artifact Retention

Use retention profiles, with `serious_train` as the default for long PPO runs.

Always retain:

```text
evaluation_manifest.json
training_config.json
schema_arm_manifest.json
state_collapser_dependency_manifest.json
geometry_record_schema_manifest.json
record_tokenization_manifest.json
policy_bank_manifest.json
model_manifest.json
optimizer_manifest.json
device_manifest.json
checkpoint_manifest.json
rollout_buffer_manifest.json
ppo_update_summary.csv
episode_summary.csv
training_curve.csv
per_tier_training_summary.csv
advantage_summary.csv
value_summary.csv
action_distribution_summary.csv
mask_admissibility_summary.csv
controller_event_summary.csv
timing_summary.csv
readout_source.json
```

Retain selected detailed traces:

```text
first episode;
final episode;
first success;
best reward so far;
every Nth episode by config;
diagnostic failure episodes up to a configured cap.
```

Do not retain by default:

```text
every candidate surface for every step;
every raw tensor;
every movie frame;
every full step event row for every episode;
every controller event row for every episode in long runs unless configured.
```

Movie generation should work only from retained traces. If a requested episode
was not retained, the renderer must give a clear error that identifies the
trace-retention policy and available episodes.

## Checkpoints And Resume

Checkpoint at update boundaries.

Checkpoint contents:

```text
run_config
schema_arm_config
policy_bank state_dicts by tier
rollout_policy snapshots by tier, if needed for exact resume
optimizer states by tier
capacity schedule
record tokenizer state
encoding registries
RNG states
global update index
episode index
rollout sample counts
best metric snapshot
checkpoint_manifest entry
```

First-scope resume requirement:

```text
clean resume at PPO update boundary.
```

Mid-rollout resume is optional and should not block first implementation.

## Evaluation Family

### Evaluation Id

Recommended evaluation id:

```text
warehouse_gridlock_full_tower_gpu_ppo_v001
```

Recommended readout surface:

```text
docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/
```

Recommended artifact root for a run:

```text
docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/artifacts/<run_label>/
```

### Evaluation Goal

The evaluation should determine whether the full-tower GPU PPO training
system:

```text
executes real PPO;
uses state_collapser hardcoded tower traversal correctly;
trains separate per-tier policies;
collects old-policy rollout samples correctly;
preserves candidate surfaces for PPO ratio computation;
uses pointwise executable action/lift semantics;
produces interpretable learning curves and artifacts;
can compare no-contraction and nontrivial contraction schema arms under the
same PPO machinery.
```

### Evaluation Arms

Minimum arms:

```text
schema0_no_contraction:
  direct/no-contraction arm.

schema1_nontrivial_tower:
  first configured nontrivial contraction-schema tower arm.
```

Optional later arms:

```text
additional nontrivial contraction schemas;
ablation schemas;
capacity schedules;
profile variants.
```

The first blueprint should keep the comparison small enough to debug. It
should prioritize correctness of PPO/tower mechanics over large statistical
claims.

### Budgets

The evaluation should support:

```text
smoke_cpu budget;
debug_gpu budget;
serious_gpu budget.
```

Budget lock should record:

```text
episodes_per_arm
max_environment_seconds_per_episode
rollout_samples_per_update
max_updates
max_wall_time_seconds_if_configured
replicates_per_arm
schema_seeds
base_seed
locked_by
run_label
```

### Success Criteria

System success criteria:

```text
PPO update rows exist with nonzero optimizer steps;
old_log_prob and new_log_prob ratio diagnostics exist;
clip fraction and approximate KL are recorded;
GAE/return summaries exist;
per-tier policy snapshots and checkpoint manifests exist;
controller/traversal events are recorded separately from PPO samples;
NO_AVAILABLE_ACTION events, if any, are classified;
pointwise executable masks are used;
representative fallback is not used for execution;
selected traces can render movies.
```

Learning signal criteria:

```text
episode reward and success metrics are plotted/summarized by arm;
per-tier sample counts show which tiers were actually trained;
value loss and explained variance are recorded;
entropy and action distribution summaries show whether the policy collapsed;
mask/action-surface summaries show whether the policy saw real choices.
```

Comparison claim criteria:

```text
schema0_no_contraction and schema1_nontrivial_tower run under matched budget;
both use the same PPO engine and artifact contract;
differences in action surfaces are explicitly described as schema differences;
readout avoids claiming final benchmark superiority from smoke/debug budgets.
```

### Failure Classification

Stable failure categories:

```text
state_collapser_surface_missing
geometry_record_schema_error
empty_pointwise_action_surface_at_actor_boundary
no_available_action
representative_fallback_attempted
invalid_lift_resolution
ppo_ratio_surface_mismatch
old_log_prob_missing
gae_bootstrap_inconsistent
cuda_required_unavailable
checkpoint_write_failed
trace_not_retained
```

These should appear in manifests and readouts.

## CLI Surface

Recommended CLI family:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-tower-gpu-ppo inspect

uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-tower-gpu-ppo run

uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-tower-gpu-ppo summarize

uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-tower-gpu-ppo render-episode
```

### inspect

Purpose:

```text
Validate dependencies, environment readiness, state_collapser version,
schema configs, GPU availability, and output paths before a long run.
```

Required inputs:

```text
--repo-root
--readiness-source
--profile
--schema-config
--run-label
```

### run

Purpose:

```text
Execute PPO training/evaluation.
```

Required inputs:

```text
--repo-root
--artifact-root
--readiness-source
--run-label
--locked-by
--profile
--schema-arm
```

Useful optional inputs:

```text
--episodes-per-arm
--max-seconds-per-episode
--rollout-samples-per-update
--max-updates
--replicates-per-arm
--schema-seed
--base-seed
--device
--trace-episode-index
--trace-every-episodes
--checkpoint-every-updates
--capacity-0
--gamma-capacity
--min-capacity
--progress
```

### summarize

Purpose:

```text
Aggregate artifacts and write readout_source.json plus machine-readable and
human-readable summary inputs.
```

Required inputs:

```text
--repo-root
--artifact-root
```

### render-episode

Purpose:

```text
Render a retained Warehouse trace to GIF/movie.
```

It must support both:

```text
artifact-root + selectors
direct trace path
```

and must fail clearly if the requested episode was not retained.

## Readout Contract

The generated human-readable report should answer:

```text
Did real PPO run?
Was GPU actually used when requested?
Which arms ran?
Which schema was no-contraction direct?
Which schema was nontrivial tower?
Which tiers received policy samples?
Did PPO update each active tier?
Were old/new policy ratios valid?
Were candidate surfaces preserved?
Were pointwise executable masks used?
Were representative fallbacks avoided?
Did reward/success improve over time?
Did either arm show a bounded signal?
What are the main failure modes or caveats?
Which traces can be rendered?
```

Badges should include:

```text
ppo_status
gpu_status
state_collapser_semantics
pointwise_liftability
representative_fallback
artifact_completeness
training_signal
comparison_boundary
trace_retention
```

The readout must distinguish:

```text
system readiness evidence;
training mechanics evidence;
bounded learning signal;
comparison signal;
claims not yet supported.
```

## Artifact Tables

### Manifests

Required manifests:

```text
evaluation_manifest.json
evaluation_budget_lock.json
schema_arm_manifest.json
environment_manifest.json
dependency_manifest.json
state_collapser_manifest.json
graph_snapshot_manifest.json
tower_snapshot_manifest.json
geometry_record_schema_manifest.json
record_tokenization_manifest.json
policy_bank_manifest.json
capacity_schedule_manifest.json
model_manifest.json
optimizer_manifest.json
device_manifest.json
checkpoint_manifest.json
trace_retention_manifest.json
readout_source.json
```

### Summary Tables

Required CSV/JSON summaries:

```text
episode_summary.csv
training_curve.csv
ppo_update_summary.csv
per_tier_training_summary.csv
per_tier_policy_capacity_summary.csv
controller_event_summary.csv
ppo_sample_summary.csv
advantage_summary.csv
value_summary.csv
action_distribution_summary.csv
mask_admissibility_summary.csv
lift_resolution_summary.csv
no_available_action_summary.csv
checkpoint_summary.csv
timing_summary.csv
device_summary.csv
trace_episode_index.csv
```

### Optional Debug Tables

Only under debug retention profiles:

```text
detailed_controller_events.csv
detailed_ppo_samples.csv
detailed_candidate_surfaces.jsonl
detailed_lift_resolution_events.csv
detailed_tensorization_events.csv
```

## Invariants

The implementation must enforce:

```text
1. Geometry records do not contain episode/time/PPO mutable fields.

2. Every PPO sample has a rollout_policy_snapshot_id.

3. Every PPO sample has old_log_prob.

4. Every PPO update recomputes new_log_prob on the stored decision surface.

5. Candidate action ids and local order are stored.

6. Candidate masks are stored.

7. PPO actor is not called on an empty pointwise executable surface.

8. Representative fallback is not used for execution.

9. Direct arm is the no-contraction schema arm.

10. Tier 0 is uppermost, and i -> i + 1 is moving down the tower.

11. Separate per-tier policy models exist for non-degenerate tiers.

12. Capacity schedule is artifacted.

13. Controller events and PPO samples are distinct.

14. Concrete Warehouse moves are the events that consume Warehouse time.

15. TRAIN is not a PPO-sampled action.
```

## Test Plan

### Unit Tests

Add tests for:

```text
geometry records reject mutable rollout/time fields;
state/action record serialization is deterministic;
record tokenization preserves stable ids;
tier direction convention is artifacted;
capacity schedule decreases or holds according to gamma_capacity;
policy bank creates separate policy objects per tier;
rollout_policy_k snapshot is frozen during rollout;
masked softmax only assigns probability to unmasked candidates;
candidate ordering is preserved in rollout samples;
old/new log-prob ratio uses stored candidate surface;
direct arm uses no-contraction schema id;
pointwise executable action surface is nonempty before actor call;
representative fallback is not used for execution;
NO_AVAILABLE_ACTION is diagnostic, not PPO sample;
GAE terminal/truncation bootstrap cases are distinct;
trace renderer errors clearly for non-retained episodes.
```

### Integration Tests

Add tests for:

```text
smoke_cpu inspect command;
smoke_cpu run command with one direct/no-contraction arm;
smoke_cpu run command with one nontrivial tower arm;
summarize command produces readout_source.json;
selected trace can render;
PPO update summary has optimizer steps;
per-tier policy summary has at least one active tier;
device manifest records CPU in smoke mode;
NO_AVAILABLE_ACTION path, if forced, does not create fake PPO samples.
```

### Regression Tests

Carry forward prior regression concerns:

```text
no representative fallback;
pointwise liftability semantics id present;
artifact roots are repo-resident by default;
human-readable readout protocol can consume readout_source.json;
old unnumbered/renamed design files do not matter to runtime.
```

## Implementation Package Shape

Recommended new package:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/full_tower_gpu_ppo/
```

Recommended modules:

```text
__init__.py
ids.py
config.py
profiles.py
paths.py
records.py
geometry_records.py
decision_context.py
rollout_samples.py
tokenization.py
policy_bank.py
models.py
ppo.py
gae.py
state_collapser_runtime.py
schema_arms.py
retention.py
events.py
aggregation.py
docs_writer.py
runner.py
replay.py
manifests.py
```

This is a blueprint module shape, not a required final file list. The workplan
may merge modules if that is simpler, but it should preserve the conceptual
boundaries.

## Human-Readable Documentation

The evaluation readout should be generated under:

```text
docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/
```

Expected generated files:

```text
README.md
result_readout.md
artifact_index.md
method.md
glossary.md
runbook.md
results/summary.md
results/training_curve.md
results/per_tier_policy.md
results/ppo_health.md
results/comparison.md
badges/*.svg
```

The README should have a conversation section with Project Owner / Codex
turns, consistent with the human-readable report protocol.

## System Learning Hooks

This evaluation is likely to teach us about:

```text
state_collapser runtime integration gaps;
geometry record schema adequacy;
whether per-tier policy separation is enough;
whether capacity decay is too aggressive;
whether no-contraction direct and nontrivial tower arms produce comparable
training traces;
whether early graph geometry shifts destabilize the model;
whether trace retention is sufficient for debugging.
```

If the run reveals design consequences, archive conversation and distilled
notes under:

```text
docs/design/system_learning_from_evaluations/
```

## Blueprint Defaults

Initial recommended defaults, all future-tunable:

```text
profile_id:
  smoke_cpu for tests, serious_gpu for real run.

capacity_schedule:
  capacity_k = max(min_capacity, round(capacity_0 * gamma_capacity**k))

capacity_0:
  implementation workplan should choose based on model size target.

gamma_capacity:
  configurable; first value should be conservative.

min_capacity:
  configurable; prevents degenerate lower-tier models.

mixed_precision:
  false.

advantage_normalization:
  per tier update batch.

trace_retention:
  summaries always; selected detailed traces only.

direct arm:
  schema0_no_contraction.

tower arm:
  first configured nontrivial contraction schema.
```

## Remaining Non-Blocking Tunables

The following do not block blueprint-to-workplan conversion:

```text
exact PPO hyperparameter defaults;
exact capacity_0/gamma_capacity/min_capacity values;
exact first serious_gpu episode/update budget;
exact first nontrivial Warehouse contraction schema id;
exact trace interval;
whether to accumulate low-sample tiers or small-batch update at run end;
whether to support CUDA fallback in debug_gpu.
```

The implementation workplan may choose conservative defaults and require all
of them to be artifacted.

## Workplan Readiness

This blueprint is ready to become a Phase.Stage.Action implementation
workplan if the Project Owner accepts the following locked commitments:

```text
1. PPO does not learn tower traversal.
2. Direct is no-contraction schema.
3. Separate policy model per tier.
4. Geometry records do not contain mutable episode/time/PPO facts.
5. Candidate-scoring masked softmax over current Out_k(s_t).
6. Pointwise executable action surfaces only.
7. No representative fallback for execution.
8. Stored decision surfaces for PPO ratios.
9. Repo-resident artifacts and readout_source.json.
10. Selected-trace retention, not exhaustive long-run dumps.
```

If any of those commitments change, update this blueprint before producing the
implementation workplan.
