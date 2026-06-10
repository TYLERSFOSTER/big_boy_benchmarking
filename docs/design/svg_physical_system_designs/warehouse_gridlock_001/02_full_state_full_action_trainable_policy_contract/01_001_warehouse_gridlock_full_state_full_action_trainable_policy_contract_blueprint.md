# Warehouse Gridlock Full-State Full-Action Trainable Policy Contract Blueprint

## Status

Initial full blueprint.

This is a design blueprint, not an implementation workplan. It exists to
define the narrow missing model contract for Warehouse Gridlock learning after
the first masked direct vs. live-lift tower diagnostic showed that the
evaluation machinery works but the current "learner" surface does not represent
real reusable policy learning.

The core point is:

```text
Do not redesign Warehouse Gridlock.
Do not redesign the fairness boundary.
Do not redesign the artifact/readout system.
Replace the current generated-candidate-id update surface with a real
trainable policy model that sees the full system configuration plus the current
second and emits a full simultaneous robot action vector.
```

## Source Documents

Read this blueprint beside:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_001_warehouse_gridlock_environment_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_002_warehouse_gridlock_environment_implementation_workplan.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_003_warehouse_gridlock_environment_implementation_log.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_masked_direct_vs_live_lift_tower_no_lookahead/01_001_warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_masked_direct_vs_live_lift_tower_no_lookahead/01_002_warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_implementation_workplan.md
docs/evaluations/warehouse_gridlock_001/environment_readiness/README.md
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/README.md
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/runbook.md
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

Relevant code surfaces at the time this blueprint was written:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/
src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/
tests/environments/warehouse_gridlock/
```

## Attribution

### Project Owner

The Project Owner authored the Warehouse Gridlock physical design and locked
the core environment mechanics through prior design turns:

- the physical environment is derived from the Project Owner's SVG drawings;
- one environment timestep is one second;
- every robot receives one command each timestep;
- every robot may move one graph step or stay;
- all robot commands form one synchronous ensemble move;
- invalid ensemble moves do not partially execute;
- invalid ensemble moves do not advance the timer;
- terminal success requires exact robot and box target placement;
- the serious MDP is hidden or effectively hidden;
- discovery and admissibility fairness are central to comparing arms.

The Project Owner also locked the policy-contract anchor for this blueprint:

```text
Every model should get full system config and second number as input, and
should give full action vector output.
```

This blueprint treats that sentence as the design authority for the new model
surface.

### Abdul Malik, Project PM

Abdul Malik's earlier PlateSupport observation remains relevant background:
tower-positive evidence can be confounded if a tower arm avoids invalid or dead
regions that the direct arm is allowed to waste budget on. That observation
motivated separate direct-star and tower-star controls in PlateSupport.

For the current Warehouse contract, the relevance is narrower:

```text
The new full-state/full-action training surface must preserve the existing
Warehouse no-lookahead fairness boundary. It must not smuggle in Abdul-style
one-hop cul-de-sac avoidance for only one arm.
```

### Codex

Codex authored the engineering interpretation, decomposition, and
recommendations in this blueprint. Unless a statement is quoted above or
already recorded in the cited source documents, it is consultant analysis, not
Project Owner or PM speech.

No invented Project Owner turns are present in this blueprint.

## Executive Summary

The existing Warehouse Gridlock masked direct vs. live-lift tower evaluation is
valuable, but it is not a real learning comparison.

It validates:

- the Warehouse environment implementation;
- the synchronous transition rules;
- immediate inadmissibility masking;
- no-lookahead audit rows;
- live state-lift hygiene for the tower arm;
- generated/discovered tower surface artifacts;
- progress logging;
- human-readable readout generation;
- replay generation for recorded episodes.

It does not validate:

- that direct has a trainable policy;
- that tower has a trainable policy;
- that either arm improves over long training;
- that more episodes under the current learner surface mean better learning;
- that the tied 8-episode run would become meaningful just by increasing the
  episode count.

The failure is specific and fixable.

The current Warehouse runner uses a tiny candidate-id keyed update surface:

```text
q_values: dict[candidate_id, value]
```

At each step it generates candidate actions, masks inadmissible candidates, and
selects from the remaining candidate ids by current stored value and candidate
rank. The value update is tied to the selected generated candidate id. In
practice, candidate ids are too specific to the local generated proposal and
state. Most updates do not create reusable policy knowledge. Therefore long
runs under that system are mostly longer traces, not real training.

This blueprint replaces that with a real trainable policy contract:

```text
policy.act(full_system_config, second) -> full_action_vector
policy.update(transition_record) -> policy_state_delta
```

The final selected action at the environment boundary is always a full concrete
Warehouse action vector:

```text
R01 -> north | south | east | west | stay
R02 -> north | south | east | west | stay
...
R32 -> north | south | east | west | stay
```

Both direct and tower arms must use this full-vector model boundary. The tower
arm may use tier structure internally, but it must still emit or realize a full
concrete action vector at the Warehouse environment boundary.

## What Is Already Designed And Must Not Be Reopened

This section exists to prevent a future engineer or model from treating this
blueprint as a blank-page Warehouse design.

### Environment Identity Is Already Designed

The environment is:

```text
environment_family_id: warehouse_gridlock_001
environment_instance_id: warehouse_gridlock_16x16_v001
```

The source physical design is the Project Owner's Warehouse Gridlock SVG
drawing set. This blueprint does not change that drawing, manifest, instance,
or environment family identity.

### Environment Mechanics Are Already Designed

The following mechanics are locked for this work:

```text
timestep_duration: 1 second
robot_command_set: north | south | east | west | stay
action_form: synchronous command vector for all robots
partial_execution: forbidden
invalid_action_time_advance: false
invalid_action_reward_penalty: 0.0
```

The reward constants remain:

```text
success_reward: 1000.0
elapsed_time_penalty_per_second: -1.0
correct_box_reward: 1.0
correct_robot_reward: 1.0
invalid_penalty: 0.0
```

### Manifest Authority Is Already Designed

The Warehouse manifest is manually derived from the Project Owner drawing. The
column/obstacle authority is the PO drawing, with optional helper inspection.
This blueprint does not change blocked nodes, targets, robot ids, box ids, or
coordinate authority.

### Fairness Boundary Is Already Designed

The active Warehouse comparison boundary remains:

```text
Both arms: immediate inadmissibility is masked.
Neither arm: Abdul-style one-hop successor cul-de-sac lookahead.
Tower arm: live state-lift hygiene remains active.
```

In particular:

- direct does not waste selected environment steps on immediately impossible
  actions;
- tower does not waste state lifts on upstairs states with empty outgoing
  action sets;
- neither direct nor tower rejects an otherwise admissible action because its
  successor state is locally dead;
- successor facts may be logged for diagnosis, but not used for selection.

### Artifact And Readout Discipline Is Already Designed

The new trainable-policy evaluation should reuse the existing repo-resident
artifact pattern:

```text
docs/evaluations/warehouse_gridlock_001/<evaluation_name>/
docs/evaluations/warehouse_gridlock_001/<evaluation_name>/artifacts/<run_label>/
docs/evaluations/warehouse_gridlock_001/<evaluation_name>/readout_source.json
```

The human-readable readout command remains:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-readout-surface>/readout_source.json
```

### Replay Is Already Designed

Recorded runs can be replayed from `step_events.csv`. The trainable-policy
evaluation should preserve and extend that surface rather than invent a new
visualization path.

## Problem Being Corrected

### Current Runner Shape

The current Warehouse evaluation loop creates a fresh in-run value table:

```text
q_values: dict[str, float] = {}
```

Then at each selected step it updates the selected generated candidate id:

```text
previous_value = q_values.get(selected.candidate_id, 0.0)
new_value = previous_value + 0.1 * (result.reward - previous_value)
q_values[selected.candidate_id] = new_value
```

Direct selection uses:

```text
q_values.get(candidate.candidate_id, 0.0)
```

Tower selection uses:

```text
q_values.get(candidate.concrete_candidate.candidate_id, 0.0)
```

This is adequate for proving that update rows can be written. It is not
adequate for real training.

### Why It Fails As Learning

The generated candidate id is too narrow a learning key.

It binds together too many local details:

- current exact state;
- generated proposal rank;
- selected robot subset;
- concrete full action vector;
- candidate generator seed path;
- tower or direct proposal context.

A later state that is behaviorally similar will not reuse the update unless it
happens to regenerate the same id. A later proposal with the same useful
coordination pattern may also fail to reuse the update if the id differs.

This creates a misleading artifact surface:

```text
learner_update_events.csv exists,
but the policy does not meaningfully improve.
```

### Why More Episodes Alone Does Not Fix It

Increasing from 8 episodes to 128, 512, or more under the same candidate-id
surface mostly increases the number of generated local keys. It does not, by
itself, create a model that learns reusable state-action structure.

Therefore:

```text
Long Warehouse runs must wait for this policy-contract correction.
```

## Claim Boundary For The Corrected Evaluation

The corrected evaluation may claim:

- both arms used real trainable policy models;
- both arms received full system configuration and current second as model
  input;
- both arms emitted full simultaneous action vectors at the environment
  boundary;
- immediate inadmissibility was masked for both arms under the same declared
  policy;
- neither arm used one-hop successor cul-de-sac lookahead;
- tower live state-lift hygiene remained active;
- policy updates produced measurable reusable policy-state changes;
- learning curves can be inspected episode by episode.

The corrected evaluation may not claim:

- broad Warehouse benchmark success;
- statistical significance unless the run budget supports it;
- general tower superiority;
- global optimality;
- full action-space enumeration;
- full serious-MDP discovery;
- privileged planning;
- that the tower arm and direct arm have identical internal representations.

## Core Contract

### Contract Name

Recommended contract id:

```text
warehouse_full_state_full_action_policy_contract_v001
```

Recommended evaluation id:

```text
warehouse_gridlock_full_state_full_action_trainable_policy_v001
```

Recommended CLI family:

```text
warehouse-gridlock full-state-policy-comparison
```

Recommended repo readout surface:

```text
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/
```

Recommended source package:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/
```

### Policy Act Signature

Conceptual interface:

```python
class WarehousePolicyModel:
    policy_id: str
    model_family_id: str

    def act(
        self,
        *,
        full_system_config: WarehouseFullSystemConfig,
        second: int,
        rng: PolicyRng,
        mask_context: WarehouseMaskContext,
    ) -> WarehousePolicyDecision:
        ...
```

The non-negotiable PO contract is:

```text
full_system_config + second -> full_action_vector
```

The additional `rng` and `mask_context` arguments above are implementation
support surfaces. They do not change the conceptual model input/output
contract. They exist so that stochastic training and admissibility masking can
be reproducible and auditable.

### Policy Update Signature

Conceptual interface:

```python
class WarehousePolicyModel:
    def update(
        self,
        *,
        transition: WarehousePolicyTransition,
        rng: PolicyRng,
    ) -> WarehousePolicyUpdate:
        ...
```

The transition must include:

```text
pre_config
pre_second
selected_full_action_vector
mask_or_projection_trace
reward
post_config
post_second
terminated
truncated
episode_index
step_index
```

The update must return enough information to prove whether learning state
actually changed.

### Required Output

The final action at the Warehouse environment boundary is:

```text
WarehouseFullActionVector:
  robot_commands:
    R01: north | south | east | west | stay
    R02: north | south | east | west | stay
    ...
    R32: north | south | east | west | stay
```

The model must not be fundamentally a selector over opaque generated candidate
ids.

Candidate generation may still exist as a helper for:

- admissibility projection;
- exploration proposal support;
- debugging;
- comparison to the old diagnostic;
- finite mask approximation.

But the learner's primary state must live in a reusable policy model, not in
per-candidate generated ids.

## Full System Configuration

### Static Configuration

The full system configuration includes static environment facts:

```text
environment_instance_id
grid_dimensions
traversable_nodes
blocked_nodes
traversable_edges
robot_ids
box_ids
robot_target_map
box_target_map
reward_constants
max_seconds_per_episode
```

The static configuration may be passed by reference or stable id to avoid
copying large immutable structures at every step. The artifact surface must
still record which static configuration was visible to the model.

### Dynamic Configuration

The full system configuration also includes the dynamic state:

```text
robot_positions
box_positions
current_terminal_status
current_target_counts
```

The `second` is passed explicitly even though it may also be derivable from
state. This follows the Project Owner's wording and keeps time pressure visible
to every model.

### Optional Model-Internal State

A trainable model may keep internal state such as:

- learned parameters;
- optimizer state;
- episode memory;
- exploration schedule;
- policy temperature;
- value estimates;
- tier-local policy tables.

That internal state is not a substitute for the required input contract. It
must be logged as model state, not silently treated as extra environment
observation.

## Full Action Vector

### Concrete Action Vector

At the environment boundary, every selected action is concrete:

```text
ConcreteActionVector:
  commands: dict[RobotId, DirectionOrStay]
```

It must be executable by the existing Warehouse transition engine.

### Abstract Or Tier Action Vector

The tower arm may internally select abstract or tier-local action vectors.

For example:

```text
TierActionVector:
  abstract_commands: dict[TierRobotCellId, TierDirectionOrStay]
```

However, a tower action is not complete until it is realized as:

```text
ConcreteActionVector
```

The recorded action trace must show:

```text
tier_policy_decision
selected_tier_action_vector
state_lift_trace
action_realization_trace
concrete_full_action_vector
warehouse_transition_result
```

## Admissibility Masking With Full Vectors

### Existing Rule To Preserve

Both arms must retain immediate inadmissibility masking:

```text
No selected environment step should be an immediately invalid ensemble action.
```

Invalid raw model proposals may be useful for training diagnostics, but they
must not be confused with selected environment actions.

### Why This Needs A Clear Model Boundary

With generated candidates, masking was simple:

```text
generate finite candidates
query each candidate
select from admissible candidates only
```

With a full-vector model, the action space is still enormous:

```text
5^32
```

The corrected implementation must not flat-enumerate that space.

Therefore the policy contract needs two layers:

```text
raw model preference/proposal surface
admissibility-resolved selected full action vector
```

The PO-locked output is the selected full action vector. The implementation may
also log raw model preferences, but the environment boundary receives the
admissibility-resolved vector.

### Recommended First Resolution Strategy

For the first corrected evaluation, use a deterministic, logged admissibility
resolver with bounded local search around the model's raw preferences.

Recommended shape:

```text
1. model scores or proposes one command per robot from full config + second
2. resolver checks the proposed full vector
3. if valid, execute it
4. if invalid, resolver makes a bounded, deterministic sequence of repairs
   using the same immediate transition validity oracle
5. if no repaired vector is found within budget, execute all-stay if valid
6. log every repair/projection event
```

The resolver must be identical in status for both arms at the concrete
environment boundary:

```text
direct: raw concrete vector -> concrete resolver -> selected concrete vector
tower: realized concrete vector -> concrete resolver if needed -> selected
       concrete vector
```

If the tower resolves invalidity at an abstract tier before concrete
realization, that tier-local masking must be logged separately and cannot
replace the final concrete action audit.

### Forbidden Resolver Behavior

The resolver must not:

- inspect successor-state `Out` to reject an admissible action;
- perform planning search over future steps;
- optimize distance-to-target by simulating alternatives;
- use a global solver;
- privilege tower with a richer concrete action validity oracle than direct;
- charge direct for invalidity but silently repair tower invalidity without
  comparable logs.

## Direct Arm Contract

### Direct Observation

The direct model receives:

```text
full concrete Warehouse system config
current second
direct policy internal state
```

It does not receive:

- tower tier ids;
- abstract quotient maps;
- live lift fiber counts;
- future successor `Out`;
- a global precomputed MDP graph;
- shortest-path answers.

### Direct Action

The direct model emits a full concrete action vector or the preferences needed
to produce one under the shared resolver.

The final selected direct action must be:

```text
ConcreteActionVector over R01..R32
```

### Direct Update

The direct update receives the full executed transition:

```text
pre_config
second
selected_concrete_action_vector
reward
post_config
done flags
mask/projection trace
```

The update must change reusable model state or explicitly record that no
change occurred.

### Direct Evidence Requirements

The direct arm must write:

```text
direct_policy_decision_events.csv
direct_policy_update_events.csv
direct_mask_projection_events.csv
direct_learning_reuse_summary.csv
```

Minimum columns include:

```text
run_id
episode_index
step_index
second
policy_id
model_family_id
raw_action_vector_hash
selected_action_vector_hash
raw_valid
selected_valid
projection_attempt_count
projection_strategy_id
reward
terminated
truncated
parameter_state_hash_before
parameter_state_hash_after
update_norm_or_change_count
nonzero_prior_signal_used
```

## Tower Arm Contract

### Tower Observation

The tower model may use tower structure internally, but every trainable tower
decision surface must follow the same basic PO contract at its own level:

```text
full tier/system configuration + current second -> full tier action vector
```

The tower arm may receive:

- scoped generated/discovered tower surface;
- current tier id;
- tier state cell;
- quotient/tower maps;
- live state-lift candidates;
- tier-local admissible action cells;
- concrete realization trace.

The tower arm must not receive:

- one-step successor-state cul-de-sac answers for action selection;
- a privileged full Warehouse MDP;
- unlogged concrete validity repairs;
- a different episode clock.

### Tower Policy Shape

The first corrected tower implementation should support either:

```text
shared tier-conditioned model:
  model.act(tier_id, tier_full_config, tier_state, second) -> tier_action_vector
```

or:

```text
one model namespace per tier:
  model_by_tier[tier_id].act(tier_full_config, tier_state, second)
```

Both shapes are acceptable under this blueprint if artifacts clearly record the
chosen policy namespace. The workplan should choose the simpler implementation
that matches existing tower code.

### Tower Action Realization

The tower action path must record:

```text
1. selected downstairs/current state
2. live state-lift candidate set
3. selected live upstairs representative
4. tier policy input
5. tier policy raw output
6. tier action masking or projection
7. concrete realization candidates
8. selected concrete full action vector
9. concrete immediate admissibility check
10. Warehouse transition result
```

### Live-Lift Hygiene

The existing live state-lift rule remains:

```text
Once a downstairs state is fixed, do not lift it to an upstairs state with
empty Out.
```

This is a state-lift hygiene rule. It is not an action-successor lookahead
rule.

### Tower Update

The tower update receives:

```text
pre_concrete_config
pre_tier_config
second
selected_tier_action_vector
selected_concrete_action_vector
reward
post_concrete_config
post_tier_config_or_projection
done flags
lift/realization trace
mask/projection trace
```

The update must write enough evidence to distinguish:

- tier policy parameter changes;
- concrete resolver changes;
- lift selection diagnostics;
- no-op update cases.

### Tower Evidence Requirements

The tower arm must write:

```text
tower_policy_decision_events.csv
tower_policy_update_events.csv
tower_tier_action_projection_events.csv
tower_concrete_realization_events.csv
tower_learning_reuse_summary.csv
tower_live_lift_summary.csv
tower_shape_summary.csv
```

Minimum columns include:

```text
run_id
episode_index
step_index
second
tier
policy_id
model_family_id
tier_state_id
raw_tier_action_vector_hash
selected_tier_action_vector_hash
selected_concrete_action_vector_hash
live_lift_candidate_count
dead_lift_candidate_count
action_realization_candidate_count
concrete_selected_valid
projection_attempt_count
reward
parameter_state_hash_before
parameter_state_hash_after
update_norm_or_change_count
nonzero_prior_signal_used
```

## Model Family Layer

### Contract Versus Model Family

This blueprint locks the policy contract. It does not require a neural model.

The important distinction:

```text
contract:
  what information the model receives and what action form it emits

model family:
  how the model computes, explores, and updates
```

A first implementation can satisfy the contract with a simple trainable model
before introducing backprop.

### Recommended First Model Family

Recommended initial model family:

```text
warehouse_linear_factorized_softmax_policy_v001
```

Purpose:

```text
provide real reusable learning while keeping implementation inspectable
```

Suggested behavior:

- compute per-robot command scores from full-system features;
- sample or choose one command per robot;
- form a full action vector;
- pass the vector through the shared admissibility resolver;
- update reusable feature weights from observed reward/progress signals.

This is not a claim that factorized per-robot scoring is the final model. It is
a pragmatic first trainable model that replaces candidate-id memorization with
reusable parameters.

### Why Not Start With A Deep Model By Default

A neural/backprop policy may be desirable later, but it adds:

- dependency choices;
- tensor shape choices;
- batching choices;
- optimizer configuration;
- serialization rules;
- reproducibility questions;
- longer debugging loops.

The first correction should prove the policy contract and learning evidence
surface before adding deep-model complexity.

### Backprop Compatibility

The contract should be compatible with a future neural policy:

```python
encoded = encoder(full_system_config, second)
logits = network(encoded)
action_vector = decoder_or_projector(logits, mask_context)
loss = training_objective(transition_batch)
optimizer.step()
```

If a neural model is later implemented, it must add:

```text
optimizer_manifest.json
model_checkpoint_manifest.json
gradient_update_events.csv
batch_training_events.csv
```

Until those exist, readouts must not claim backprop is happening.

## Feature Requirements For The First Trainable Model

The first model should use features that are simple, full-state, and reusable.

Recommended feature groups:

```text
robot_to_robot_target_delta
box_to_box_target_delta
robot_to_nearest_box_delta
robot_to_pushable_box_alignment
box_to_target_alignment
local_occupancy_around_robot
local_occupancy_around_box
blocked_direction_indicator
edge_exists_indicator
second_fraction_remaining
correct_robot_indicator
correct_box_indicator
```

The model should not need to know the complete admissible-state graph. It may
query the existing immediate transition engine for current action validity.

## Training Objective

### Minimal Online Objective

The first implementation may use an online reinforcement-style update:

```text
score selected commands
observe reward/progress
increase weights for selected features when outcome is good
decrease or neutralize weights when outcome is bad
```

The exact update rule belongs in the implementation workplan, but the artifact
must record:

```text
learning_rate
discount_or_bootstrap_policy
reward_signal_used
progress_signal_used
exploration_schedule
parameter_norm_before
parameter_norm_after
```

### Progress Signals

Because Warehouse terminal success may be rare at first, the training signal
should support shaped reward already present in the environment:

```text
correct_robot_count
correct_box_count
elapsed_time_penalty
success_reward
```

This does not change environment reward. It makes explicit which existing
reward components the policy update uses.

### Episode Boundary

Policy state persists across episodes within a run unless the run manifest
declares a reset policy.

Recommended default:

```text
policy_parameters persist across all episodes for one arm/run/replicate
policy_parameters reset between independent replicates
direct and tower maintain separate policy namespaces
```

## Evidence That Learning Is Real

The corrected evaluation must include explicit anti-self-deception checks.

### Required Learning Health Summary

Write:

```text
results/learning_health_summary.csv
```

Minimum rows by arm:

```text
arm_id
run_count
episode_count
decision_count
update_count
non_noop_update_count
mean_update_norm
parameter_state_changes
nonzero_prior_signal_decision_count
reused_feature_signal_decision_count
policy_state_hash_initial
policy_state_hash_final
learning_status
```

Allowed `learning_status` values:

```text
real_learning_signal_present
nominal_updates_only
no_updates
failed
```

### Required Learning Curve Summary

Write:

```text
results/learning_curve_summary.csv
```

Minimum columns:

```text
arm_id
replicate_index
schema_seed
episode_index
episode_total_reward
terminal_success
final_correct_boxes
final_correct_robots
selected_valid_steps
raw_invalid_proposal_count
projection_attempt_count
policy_update_count
non_noop_update_count
parameter_delta_norm
```

### Required Reuse Evidence

Write:

```text
results/policy_reuse_summary.csv
```

Minimum columns:

```text
arm_id
model_family_id
feature_namespace
decision_count
decisions_using_nonzero_prior_signal
decisions_with_prior_policy_state_hash_seen_before
unique_feature_keys_or_parameter_groups_touched
mean_prior_score_abs
median_prior_score_abs
reuse_status
```

The readout must flag a run as not a real learning comparison if:

```text
update_count > 0
and decisions_using_nonzero_prior_signal == 0
```

This is exactly the class of failure that motivated this blueprint.

## Evaluation Shape

### New Evaluation, Not A Silent Mutation

Do not overwrite the current diagnostic:

```text
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/
```

Create a new evaluation surface:

```text
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/
```

The old diagnostic remains useful provenance.

### Active Arms

Recommended first arms:

```text
warehouse_direct_full_state_policy_masked
warehouse_tower_full_state_policy_live_lift_masked
```

These names intentionally preserve the Warehouse fairness contract:

```text
direct: full-state trainable direct policy plus immediate mask
tower: full-state/tier trainable tower policy plus live lift and immediate mask
```

### Budget

The first implementation should include a smoke budget and a serious pilot
budget.

Smoke budget:

```text
episodes_per_arm: 2 to 4
replicates_per_arm: 1
max_seconds_per_episode: 128
purpose: artifact and update validation only
```

Pilot budget:

```text
episodes_per_arm: 128 or more
replicates_per_arm: 2 or more
max_seconds_per_episode: 128 or PO-selected serious horizon
purpose: visible learning-curve check
```

The workplan should not ask the Project Owner to run a long pilot until the
smoke run proves:

- non-noop updates exist;
- later decisions use nonzero prior learned signal;
- replay output still works;
- readout explains learning health correctly.

## Comparison Fairness

### Shared Inputs

Both arms receive:

```text
same Warehouse static configuration
same Warehouse dynamic state information at the concrete boundary
same current second
same reward function
same max seconds
same random seed policy, with matched arm pairs where applicable
same immediate concrete transition validity oracle
same concrete selected-action audit
```

### Legitimate Tower Difference

The tower arm may receive and use:

```text
quotient/tier representation
live state-lift candidates
tier action cells
concrete realization maps
```

Those are the tower technology being tested. They must be logged, not hidden.

### Forbidden Advantage

The tower arm may not receive:

```text
one-hop successor-state cul-de-sac lookahead
global future planning
unchecked concrete repairs
unlogged precomputed optimal routes
more concrete validity budget unless recorded as such
```

The direct arm may not be made artificially weak by:

```text
executing invalid full vectors
counting invalid raw proposals as environment steps
removing immediate admissibility masking
forcing candidate-id memorization
denying it full system state
```

## Artifact Contract

### Required Manifests

The corrected evaluation must write:

```text
evaluation_manifest.json
evaluation_budget_lock.json
environment_instance_manifest.json
policy_contract_manifest.json
policy_model_manifest.json
policy_training_manifest.json
admissibility_resolver_manifest.json
tower_policy_manifest.json
tower_construction_manifest.json
readout_source.json
```

### Required Result Tables

The corrected evaluation must write:

```text
results/arm_summary.csv
results/paired_summary.csv
results/learning_health_summary.csv
results/learning_curve_summary.csv
results/policy_reuse_summary.csv
results/policy_decision_summary.csv
results/policy_update_summary.csv
results/mask_projection_summary.csv
results/no_lookahead_audit_summary.csv
results/tower_live_lift_summary.csv
results/tower_shape_summary.csv
results/timing_summary.csv
```

### Required Per-Run Event Tables

Each run must write:

```text
episodes.csv
step_events.csv
policy_decision_events.csv
policy_update_events.csv
mask_projection_events.csv
no_lookahead_audit_events.csv
tower_policy_events.csv
tower_lift_events.csv
tower_realization_events.csv
timing_segments.csv
warnings.jsonl
```

Direct-only runs may write empty tower files only if the expected-file policy
declares them conditionally absent. Prefer conditional expectation over empty
fake files.

## Human-Readable Readout Requirements

The generated README must explain:

- this evaluation exists because the prior Warehouse diagnostic was not real
  learning;
- both arms now use full-state/full-action trainable policy contracts;
- what model family was used;
- whether learning was actually observed;
- whether later decisions used prior learned signal;
- whether direct and tower remained fair under immediate masking;
- whether tower live-lift hygiene remained active;
- whether one-hop successor lookahead remained absent;
- what the learning curves show;
- what the replay examples show.

Required top badges:

```text
Artifacts
Learning Signal
Behavior
Fairness
No Lookahead
Provenance
```

The README must not call the run a serious learning comparison if
`learning_health_summary.csv` says `nominal_updates_only`.

## Replay Requirements

The existing replay command should continue to work:

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock render-episode \
  --artifact-root <artifact-root> \
  --arm-id <arm-id> \
  --replicate-index 0 \
  --schema-seed 0 \
  --episode-index 0
```

The corrected evaluation should add optional replay annotations:

```text
policy score summary
projection attempt count
learning episode index
selected full action vector hash
```

Replay must remain an explanation surface, not an action-selection dependency.

## Testing Requirements

### Contract Tests

Tests must prove:

- direct policy act returns a full 32-robot action vector;
- tower policy ultimately realizes a full 32-robot concrete action vector;
- every selected action is valid under immediate Warehouse transition;
- invalid raw proposals do not advance Warehouse time;
- invalid raw proposals are logged separately from selected steps;
- policy update changes reusable model state in at least one smoke case;
- learning health detects nominal-update-only failure cases;
- readout source points at repo-resident artifacts.

### Fairness Tests

Tests must prove:

- direct and tower both receive current second;
- direct and tower both receive full visible concrete config at the boundary;
- neither arm uses successor `Out` for action selection;
- tower live-lift filtering is state-lift filtering, not successor-action
  lookahead;
- direct is not charged selected steps for invalid raw vectors;
- tower concrete realization is audited under the same concrete validity
  standard as direct.

### Regression Tests From Current Diagnostic

Tests should preserve:

- current Warehouse transition semantics;
- current environment readiness invariants;
- current replay episode selection behavior;
- current artifact readout command shape.

## Implementation Migration Strategy

### Step 1: Preserve Existing Diagnostic

Do not remove or rewrite the current masked direct/live-lift diagnostic. It is
still useful as:

- baseline controller diagnostic;
- artifact/readout example;
- replay source;
- historical evidence of the learning-surface problem.

### Step 2: Add Shared Policy Contract Module

Recommended source:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/policies/
```

Suggested files:

```text
contracts.py
features.py
linear_policy.py
resolver.py
serialization.py
```

### Step 3: Add Corrected Evaluation Package

Recommended source:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/
```

Suggested files:

```text
config.py
runner.py
aggregation.py
docs_writer.py
manifests.py
paths.py
```

### Step 4: Reuse Existing Warehouse Utilities

Reuse:

- manifest loading;
- transition engine;
- target counting;
- readiness manifests;
- replay renderer;
- progress reporter pattern;
- readout source writing pattern.

Do not duplicate Warehouse transition logic inside the policy model.

### Step 5: Add CLI

Recommended CLI:

```text
warehouse-gridlock full-state-policy-comparison run
warehouse-gridlock full-state-policy-comparison summarize
```

Optional later:

```text
warehouse-gridlock full-state-policy-comparison inspect-policy
```

## Remaining Design Choices

Most high-level design is already settled. The remaining choices are model
implementation choices, not environment or comparison philosophy choices.

### Recommended Default 1: First Model Family

Use:

```text
warehouse_linear_factorized_softmax_policy_v001
```

Reason:

```text
It is real trainable policy state, but still inspectable and fast enough for
Warehouse smoke runs.
```

### Recommended Default 2: Admissibility Resolver

Use:

```text
bounded deterministic full-vector projection with all-stay fallback
```

Reason:

```text
It preserves the existing immediate-mask fairness boundary without flat
enumerating 5^32 actions.
```

### Recommended Default 3: Learning Evidence Gate

A smoke run is not complete unless:

```text
non_noop_update_count > 0
and decisions_using_nonzero_prior_signal > 0
```

Reason:

```text
This prevents repeating the exact candidate-id nominal-learning failure.
```

## Consultant-Authored Open Questions

These questions are Codex-authored. They are not Project Owner statements.

### Question 1: First Model Family

Recommendation:

```text
Start with warehouse_linear_factorized_softmax_policy_v001.
```

Question:

```text
Should the first implementation use that simple trainable linear/factorized
model, or should it jump directly to a neural/backprop model?
```

### Question 2: Projection Budget

Recommendation:

```text
Use a bounded deterministic repair/projection budget and log projection
attempts. If no valid repair is found, select all-stay.
```

Question:

```text
What first projection budget should be used for the smoke run?
```

Suggested default:

```text
projection_attempt_budget: 64
```

### Question 3: First Corrected Evaluation Name

Recommendation:

```text
warehouse_gridlock_full_state_full_action_trainable_policy_v001
```

Question:

```text
Is that name acceptable, or should the evaluation name explicitly say
"direct-vs-tower"?
```

Suggested alternative:

```text
warehouse_gridlock_full_state_direct_vs_tower_policy_v001
```

## Blueprint Readiness

This blueprint is ready to become a Phase.Stage.Action implementation workplan
after the Project Owner either accepts the recommended defaults above or
changes them.

The workplan should not revisit:

- Warehouse geometry;
- Warehouse transition rules;
- reward constants;
- one-second timestep;
- immediate inadmissibility masking;
- no one-hop lookahead;
- tower live state-lift hygiene;
- repo-resident artifacts;
- human-readable readout protocol.

The workplan should focus on:

- shared full-state/full-action policy contracts;
- first trainable policy family;
- admissibility resolver/projection logging;
- direct and tower policy integration;
- real learning health evidence;
- corrected evaluation artifacts;
- corrected readout generation.
