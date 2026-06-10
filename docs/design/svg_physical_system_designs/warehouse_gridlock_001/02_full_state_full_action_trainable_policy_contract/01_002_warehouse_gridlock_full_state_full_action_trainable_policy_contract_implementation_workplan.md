# Warehouse Gridlock Full-State Full-Action Trainable Policy Contract Implementation Workplan

## Status

Initial implementation workplan.

This workplan is derived from:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/02_full_state_full_action_trainable_policy_contract/01_001_warehouse_gridlock_full_state_full_action_trainable_policy_contract_blueprint.md
```

This workplan uses `Phase.Stage.Action` discipline.

This workplan is not execution approval by itself. Execution begins only when
the Project Owner explicitly asks to execute this workplan.

## Prime Directive Binding

This workplan follows:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/git_practices.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

When executed, this workplan is law. Do not silently simplify it, replace it
with a weaker learner, or call nominal update logging "training." If an action
cannot be implemented as written, stop at the exact `Phase.Stage.Action` item,
record the blocker in the implementation log, and ask the Project Owner for
guidance.

## Authority And Attribution

### Project Owner Authority

The Project Owner authored the Warehouse Gridlock physical design and locked
the core Warehouse mechanics in earlier design turns.

The Project Owner explicitly locked the model contract:

```text
Every model should get full system config and second number as input, and
should give full action vector output.
```

That sentence is the controlling design authority for this workplan.

### Abdul Malik, Project PM

Abdul Malik's fairness observation remains background authority for not
letting tower appear better merely because direct wastes budget in invalid or
dead regions. This workplan preserves the Warehouse no-lookahead fairness
boundary and does not introduce direct-star or tower-star one-hop controls.

### Codex Consultant Defaults

The blueprint contained consultant-authored open questions. The Project Owner
asked this workplan to use Codex's own recommendations for those questions.
Therefore this workplan locks the following consultant defaults for execution:

```text
first_model_family: warehouse_linear_factorized_softmax_policy_v001
projection_attempt_budget: 64
evaluation_id: warehouse_gridlock_full_state_full_action_trainable_policy_v001
cli_family: warehouse-gridlock full-state-policy-comparison
repo_readout_surface: docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/
implementation_branch: codex/warehouse-gridlock-full-state-policy-contract
```

These are consultant defaults, not Project Owner-authored words.

## Core Objective

Replace the current Warehouse candidate-id keyed "learner" surface with a real
trainable full-state/full-action policy contract.

The corrected evaluation must prove that:

```text
full system configuration + current second -> full simultaneous action vector
```

is the actual policy boundary for both direct and tower arms.

The corrected evaluation must also prove that policy updates create reusable
model state. A run with update rows but no reuse of prior learned signal is a
failed learning-health case, not a successful training run.

## Explicit Non-Goals

Do not:

- redesign Warehouse Gridlock;
- change the Project Owner-authored SVG-derived manifest;
- change blocked nodes, robot ids, box ids, targets, or reward constants;
- change the one-second timestep rule;
- change invalid ensemble semantics;
- change invalid ensemble no-time-advance semantics;
- add Abdul-style direct-star or tower-star one-hop cul-de-sac lookahead;
- inspect successor-state `Out` for action selection;
- flat-enumerate the `5^32` full primitive action surface;
- claim backprop is happening;
- introduce neural-model dependencies;
- overwrite the existing `masked_direct_vs_live_lift_tower` diagnostic;
- mutate prior Warehouse artifacts as if they were corrected learning runs;
- write canonical artifacts to `/private/tmp`;
- claim broad benchmark success or statistical significance.

## Decision Locks

### Environment

```text
environment_family_id: warehouse_gridlock_001
environment_instance_id: warehouse_gridlock_16x16_v001
```

### Corrected Evaluation

```text
evaluation_id: warehouse_gridlock_full_state_full_action_trainable_policy_v001
run_mode: trainable_policy_smoke_then_pilot
repo_readout_surface: docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/
source_package: src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/
policy_package: src/big_boy_benchmarking/environments/warehouse_gridlock/policies/
test_package: tests/environments/warehouse_gridlock/
```

### Arms

```text
warehouse_direct_full_state_policy_masked
warehouse_tower_full_state_policy_live_lift_masked
```

### Policy Contract

```text
policy_contract_id: warehouse_full_state_full_action_policy_contract_v001
model_family_id: warehouse_linear_factorized_softmax_policy_v001
projection_strategy_id: bounded_deterministic_repair_with_all_stay_fallback_v001
projection_attempt_budget: 64
```

### First Smoke Run

```text
run_label: policy_contract_smoke_001
episodes_per_arm: 4
replicates_per_arm: 1
schema_seeds: 1
max_seconds_per_episode: 128
purpose: artifact, contract, replay, and learning-health validation only
```

### Later Pilot Run Command Surface

Implementation must expose a pilot-capable CLI, but must not run the long
pilot during workplan execution unless the Project Owner separately requests
that run.

Recommended pilot defaults:

```text
episodes_per_arm: 128
replicates_per_arm: 2
schema_seeds: 1
max_seconds_per_episode: 128
```

## True Stop Conditions

Stop execution if:

- the worktree contains unrelated staged edits that would be mixed into this
  implementation;
- the implementation cannot begin on a dedicated branch;
- Warehouse transition semantics differ from the existing readiness and
  diagnostic docs;
- the current state cannot be encoded into a full system configuration;
- the policy cannot emit a command for every robot id;
- the selected concrete action vector cannot be validated by the existing
  transition engine;
- the resolver would need to inspect successor-state `Out`;
- the resolver would need a global planner or path solver;
- the first model family cannot produce reusable state changes;
- learning health cannot distinguish real reusable updates from nominal update
  rows;
- tower integration would require full `5^32` enumeration;
- tower live-lift hygiene cannot remain separate from successor-action
  lookahead;
- readout artifacts cannot explain the learning contract and its failure
  modes;
- tests reveal that invalid selected actions advance Warehouse time or
  partially execute.

## Implementation Log Requirement

Execution must create and maintain:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/02_full_state_full_action_trainable_policy_contract/01_003_warehouse_gridlock_full_state_full_action_trainable_policy_contract_implementation_log.md
```

The log must record:

- branch and dirty-state check;
- completed `Phase.Stage.Action` items;
- code and doc files touched;
- smoke run command and output;
- test commands and results;
- learning-health status;
- surprises and blockers;
- any Project Owner clarifications.

## Phase 0: Orientation, Branch Discipline, And Reality Check

### Phase 0.Stage 1.Action 1: Verify Current Git State

Run `git status --short` and record the result in the implementation log.

If unrelated staged files exist, stop and ask the Project Owner whether to
unstage them before proceeding.

### Phase 0.Stage 1.Action 2: Create Or Switch To The Implementation Branch

Create or switch to:

```text
codex/warehouse-gridlock-full-state-policy-contract
```

Record the branch in the implementation log.

### Phase 0.Stage 1.Action 3: Re-Read Authority Documents

Re-read:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/02_full_state_full_action_trainable_policy_contract/01_001_warehouse_gridlock_full_state_full_action_trainable_policy_contract_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_masked_direct_vs_live_lift_tower_no_lookahead/01_001_warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_blueprint.md
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/README.md
docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
```

Record that the active scope is the trainable policy contract only.

### Phase 0.Stage 1.Action 4: Inspect Existing Warehouse Runtime Surfaces

Inspect:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/actions.py
src/big_boy_benchmarking/environments/warehouse_gridlock/transition.py
src/big_boy_benchmarking/environments/warehouse_gridlock/runner.py
src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/runner.py
src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/docs_writer.py
src/big_boy_benchmarking/environments/warehouse_gridlock/replay.py
src/big_boy_benchmarking/cli/main.py
```

Record the reusable functions and any naming mismatches in the implementation
log.

### Phase 0.Stage 1.Action 5: Confirm Existing Tests Before Editing

Run the current Warehouse tests:

```text
uv run pytest tests/environments/warehouse_gridlock
```

Record the result. If tests fail before edits, stop and record the pre-existing
failure.

## Phase 1: Shared Full-State Full-Action Policy Contract

### Phase 1.Stage 1.Action 1: Create Policy Package

Create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/policies/
```

Minimum files:

```text
__init__.py
contracts.py
features.py
linear_policy.py
resolver.py
serialization.py
```

Do not put evaluation-runner code in this package. This package owns reusable
policy contracts and model utilities.

### Phase 1.Stage 1.Action 2: Define Full System Configuration Types

In `contracts.py`, define immutable or effectively immutable dataclasses for:

```text
WarehouseStaticSystemConfig
WarehouseDynamicSystemConfig
WarehouseFullSystemConfig
```

The full system config must include:

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
robot_positions
box_positions
current_target_counts
```

The current second must be passed explicitly to policy calls, not hidden only
inside the state object.

### Phase 1.Stage 1.Action 3: Define Full Action Vector Types

In `contracts.py`, define:

```text
WarehouseFullActionVector
WarehouseActionVectorValidation
```

`WarehouseFullActionVector` must:

- contain exactly one command for every robot id;
- reject missing robot commands;
- reject extra robot commands;
- use the existing Warehouse direction/stay command representation where
  possible;
- provide stable serialization;
- provide a stable hash for artifact rows.

### Phase 1.Stage 1.Action 4: Define Policy Decision Types

In `contracts.py`, define:

```text
WarehousePolicyDecision
WarehousePolicyTransition
WarehousePolicyUpdate
WarehouseMaskContext
WarehouseProjectionTrace
WarehousePolicyRng
```

`WarehousePolicyDecision` must record:

```text
policy_id
model_family_id
second
raw_action_vector
selected_action_vector
raw_action_vector_hash
selected_action_vector_hash
raw_valid
selected_valid
projection_trace
prior_signal_used
decision_score_summary
```

`WarehousePolicyUpdate` must record:

```text
policy_id
model_family_id
parameter_state_hash_before
parameter_state_hash_after
update_norm_or_change_count
non_noop_update
reward_signal_used
progress_signal_used
```

### Phase 1.Stage 1.Action 5: Add Config Extraction Helper

Implement a helper that converts an existing Warehouse instance and state into
`WarehouseFullSystemConfig`.

The helper must not alter the environment state.

It must be deterministic.

It must be shared by direct and tower arms at the concrete boundary.

### Phase 1.Stage 1.Action 6: Add Contract Tests

Create tests proving:

- a full config can be extracted from the Warehouse start state;
- the config includes every robot and box;
- the current second is passed as an explicit policy argument;
- a valid action vector contains every robot id exactly once;
- missing and extra robot commands fail validation;
- action vector hashes are stable.

## Phase 2: Feature Encoder And Trainable Linear Policy

### Phase 2.Stage 1.Action 1: Implement Feature Encoder

In `features.py`, implement a deterministic feature encoder for a robot-command
decision using full system config and second.

Feature groups must include at least:

```text
robot_to_robot_target_delta
robot_to_nearest_box_delta
robot_to_pushable_box_alignment
local_occupancy_around_robot
blocked_direction_indicator
edge_exists_indicator
second_fraction_remaining
correct_robot_indicator
```

Where feasible without large cost, also include:

```text
box_to_box_target_delta
box_to_target_alignment
local_occupancy_around_box
correct_box_indicator
```

If any feature group is infeasible in the first implementation, stop and
record the exact feature group and reason. Do not silently omit it.

### Phase 2.Stage 1.Action 2: Implement Model State Serialization

In `serialization.py`, implement stable JSON-serializable helpers for:

```text
feature keys
weights
policy state hash
model manifest payload
```

The policy state hash must change when reusable learned weights change.

### Phase 2.Stage 1.Action 3: Implement Linear Factorized Softmax Policy

In `linear_policy.py`, implement:

```text
WarehouseLinearFactorizedSoftmaxPolicy
```

Required behavior:

- receives `WarehouseFullSystemConfig` and `second`;
- scores each legal primitive command for each robot using reusable feature
  weights;
- samples or selects one command per robot under a reproducible exploration
  schedule;
- emits a raw full action vector before projection;
- records prior score information;
- supports an online update that changes reusable weights.

The first implementation must not key its learning state by generated
candidate id.

### Phase 2.Stage 1.Action 4: Lock First Update Rule

Implement a simple online update rule:

```text
advantage = reward + progress_delta - baseline
selected_command_feature_weights += learning_rate * advantage * features
baseline <- moving average of observed reward + progress_delta
```

Recommended defaults:

```text
learning_rate: 0.01
baseline_rate: 0.05
temperature_initial: 1.0
temperature_floor: 0.1
temperature_decay_per_episode: 0.995
progress_signal: delta_correct_robot_count + 2.0 * delta_correct_box_count
```

Record these in `policy_training_manifest.json`.

If exact numeric defaults must change for stability, record the change in the
implementation log and policy manifest.

### Phase 2.Stage 1.Action 5: Implement Direct Policy Tests

Tests must prove:

- the policy returns a full action vector;
- two policies with the same seed and state produce reproducible decisions;
- `update` changes the policy state hash in a positive-reward smoke case;
- at least one later decision can use nonzero prior learned signal;
- no candidate-id key is required for learning.

## Phase 3: Bounded Admissibility Resolver

### Phase 3.Stage 1.Action 1: Implement Shared Resolver

In `resolver.py`, implement:

```text
BoundedDeterministicWarehouseActionResolver
```

The resolver receives:

```text
instance
state
raw_full_action_vector
projection_attempt_budget
```

It returns:

```text
selected_full_action_vector
transition_result
projection_trace
```

### Phase 3.Stage 1.Action 2: Implement Projection Strategy

Use:

```text
bounded_deterministic_repair_with_all_stay_fallback_v001
```

Required algorithm:

1. Check the raw full action vector.
2. If valid, select it.
3. If invalid, rank non-stay robot commands by lowest model confidence margin
   first, with robot id as deterministic tie-breaker.
4. Try repaired vectors that set one low-confidence moving robot to `stay`.
5. Try prefix repairs that set the first `k` low-confidence moving robots to
   `stay`.
6. Stop when a valid vector is found or 64 attempts have been made.
7. If no repair succeeds, select the all-stay vector if valid.
8. If all-stay is invalid, stop as a hard environment invariant failure.

The resolver must only use immediate transition validity. It must not inspect
successor-state `Out`, future deadness, paths, target distance after candidate
execution, or global planning structure.

### Phase 3.Stage 1.Action 3: Log Projection Trace

`WarehouseProjectionTrace` must include:

```text
projection_strategy_id
projection_attempt_budget
attempt_count
raw_valid
selected_valid
fallback_used
invalid_reasons_seen
selected_reason
successor_out_count_used_for_selection
```

`successor_out_count_used_for_selection` must be false for every selected
action.

### Phase 3.Stage 1.Action 4: Add Resolver Tests

Tests must prove:

- a valid raw action passes unchanged;
- an invalid raw action can be repaired;
- all-stay fallback is used when bounded repairs fail;
- selected vectors are valid;
- invalid raw vectors do not advance Warehouse time;
- projection traces do not contain successor `Out` selection evidence;
- direct and tower callers can use the same concrete resolver.

## Phase 4: Corrected Evaluation Package

### Phase 4.Stage 1.Action 1: Create Evaluation Package

Create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/
```

Minimum files:

```text
__init__.py
config.py
paths.py
manifests.py
runner.py
aggregation.py
docs_writer.py
```

### Phase 4.Stage 1.Action 2: Define Evaluation Config

In `config.py`, define:

```text
FullStatePolicyComparisonConfig
```

Fields must include:

```text
repo_root
artifact_root
readiness_source
run_label
locked_by
episodes_per_arm
replicates_per_arm
schema_seeds
max_seconds_per_episode
learning_rate
baseline_rate
temperature_initial
temperature_floor
temperature_decay_per_episode
projection_attempt_budget
progress_every_episodes
```

Default values must match the decision locks unless the CLI overrides them.

### Phase 4.Stage 1.Action 3: Define Paths

In `paths.py`, define repo-resident paths:

```text
repo_readout_surface
source_artifact_root
source_evaluation_root
results_dir
runs_dir
docs_dir
badges_dir
```

Canonical artifacts must live under:

```text
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/artifacts/<run_label>/
```

### Phase 4.Stage 1.Action 4: Define Manifests

In `manifests.py`, write:

```text
evaluation_manifest.json
evaluation_budget_lock.json
evaluation_arm_manifest.json
environment_instance_manifest.json
policy_contract_manifest.json
policy_model_manifest.json
policy_training_manifest.json
admissibility_resolver_manifest.json
tower_policy_manifest.json
tower_construction_manifest.json
```

Each manifest must use repo-relative public paths where possible.

### Phase 4.Stage 1.Action 5: Implement Run Index Shape

The evaluation must write:

```text
run_index.csv
```

Minimum columns:

```text
run_id
arm_id
replicate_index
schema_seed
seed
policy_id
model_family_id
status
artifact_root
```

## Phase 5: Direct Arm Runner

### Phase 5.Stage 1.Action 1: Implement Direct Run Loop

In `runner.py`, implement the direct arm:

```text
warehouse_direct_full_state_policy_masked
```

For each episode and step:

1. Extract `WarehouseFullSystemConfig`.
2. Pass config and second to the direct policy.
3. Receive raw full action vector.
4. Resolve immediate admissibility with the shared resolver.
5. Apply the selected valid transition.
6. Update the direct policy with the executed transition.
7. Record decision, projection, update, step, and episode rows.

### Phase 5.Stage 1.Action 2: Preserve No-Time-Advance Semantics

The direct runner must never apply invalid selected actions.

Invalid raw proposals may be logged, but they do not count as selected
environment steps and must not advance the Warehouse timer.

### Phase 5.Stage 1.Action 3: Record Direct Events

Per direct run, write:

```text
policy_decision_events.csv
policy_update_events.csv
mask_projection_events.csv
no_lookahead_audit_events.csv
episodes.csv
step_events.csv
timing_segments.csv
warnings.jsonl
```

Rows must include the hashes and learning-health fields from the blueprint.

### Phase 5.Stage 1.Action 4: Test Direct Runner Smoke

Add tests proving:

- direct runner completes at least one episode;
- every selected action is valid;
- policy update rows exist;
- non-noop update rows exist;
- later decisions can use nonzero prior learned signal;
- run artifacts are written under the expected repo path.

## Phase 6: Tower Arm Runner

### Phase 6.Stage 1.Action 1: Reuse Existing Scoped Tower Surface

Reuse existing Warehouse scoped generated/discovered tower machinery from:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/
```

Do not flat-enumerate the full Warehouse action surface.

The tower remains a scoped runtime tower over generated/discovered action
surfaces, and artifacts must say so.

### Phase 6.Stage 1.Action 2: Implement Tower Policy Namespace

Implement:

```text
warehouse_tower_full_state_policy_live_lift_masked
```

The first implementation uses a shared tier-conditioned linear policy
namespace:

```text
policy_namespace = (arm_id, tier_id, model_family_id)
```

The tower policy must receive:

```text
full concrete system config
current second
tier id
tier state/cell metadata
live lift metadata
scoped tower surface metadata
```

It must ultimately emit or realize a full concrete action vector at the
Warehouse environment boundary.

### Phase 6.Stage 1.Action 3: Select Live State Lift

Before tower policy action selection, preserve existing live state-lift hygiene:

```text
pr(s') = s
Out(s') != empty
```

Record:

```text
live_lift_candidate_count
dead_lift_candidate_count
selected_lift_id
failure_reason
```

This step must not evaluate action-successor deadness.

### Phase 6.Stage 1.Action 4: Produce Tower Action Proposal

The tower policy may score scoped tower action candidates using reusable
features and learned tier-policy weights. It must not learn by opaque candidate
id.

For v001, tower action selection may use generated tower action candidates as a
finite proposal/projection surface, provided that:

- candidate features are reusable;
- selected concrete action is a full action vector;
- learning state is keyed by feature weights, not candidate ids;
- candidate count and mask scope are logged;
- the readout clearly says this is a scoped generated/discovered tower surface.

### Phase 6.Stage 1.Action 5: Realize Concrete Full Action Vector

The tower selected tier action must be realized into:

```text
WarehouseFullActionVector
```

Then the shared concrete resolver must validate or repair it under the same
immediate validity rules used by direct.

### Phase 6.Stage 1.Action 6: Update Tower Policy

Update the tower policy namespace using the executed transition:

```text
pre_concrete_config
pre_tier_metadata
second
selected_tier_action_or_candidate_features
selected_concrete_action_vector
reward
post_concrete_config
done flags
lift trace
projection trace
```

The update must produce reusable policy-state changes, not candidate-id
memorization.

### Phase 6.Stage 1.Action 7: Record Tower Events

Per tower run, write:

```text
policy_decision_events.csv
policy_update_events.csv
mask_projection_events.csv
tower_policy_events.csv
tower_lift_events.csv
tower_realization_events.csv
tower_shape_events.csv
no_lookahead_audit_events.csv
episodes.csv
step_events.csv
timing_segments.csv
warnings.jsonl
```

### Phase 6.Stage 1.Action 8: Test Tower Runner Smoke

Add tests proving:

- tower runner completes at least one episode;
- live-lift candidate counts are logged;
- selected concrete vectors are full 32-robot vectors;
- selected concrete vectors are valid;
- policy updates are reusable;
- no successor `Out` is used for action selection;
- tower scope is recorded as generated/discovered, not full-MDP.

## Phase 7: Aggregation And Learning-Health Tables

### Phase 7.Stage 1.Action 1: Implement Aggregation Module

In `aggregation.py`, aggregate per-run artifacts into:

```text
evaluation_aggregate_summary.json
evaluation_aggregate_table.csv
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

### Phase 7.Stage 1.Action 2: Implement Learning Health Classification

Classify each arm as one of:

```text
real_learning_signal_present
nominal_updates_only
no_updates
failed
```

Rules:

```text
no_updates:
  update_count == 0

nominal_updates_only:
  update_count > 0
  and non_noop_update_count == 0

nominal_updates_only:
  update_count > 0
  and decisions_using_nonzero_prior_signal == 0

real_learning_signal_present:
  non_noop_update_count > 0
  and decisions_using_nonzero_prior_signal > 0
  and policy_state_hash_initial != policy_state_hash_final

failed:
  run status indicates runner failure or missing required learning evidence
```

### Phase 7.Stage 1.Action 3: Implement No-Lookahead Audit

Aggregate:

```text
successor_out_count_used_for_selection_count
successor_out_count_observed_for_diagnosis_count
selected_action_count
```

The first count must be zero for both arms.

### Phase 7.Stage 1.Action 4: Implement Paired Summary

Pair direct and tower by:

```text
replicate_index
schema_seed
episode_index
```

Compute:

```text
reward_delta_tower_minus_direct
correct_box_delta
correct_robot_delta
terminal_success_delta
projection_attempt_delta
learning_health_delta
```

Do not claim statistical significance.

### Phase 7.Stage 1.Action 5: Test Aggregation

Add tests with synthetic rows proving:

- real learning is detected;
- nominal update-only failure is detected;
- no-lookahead violations are detected;
- paired rows align correctly;
- missing required tables fail loudly.

## Phase 8: Docs Writer, Readout Source, And Human-Readable Seeds

### Phase 8.Stage 1.Action 1: Implement Docs Writer

In `docs_writer.py`, generate:

```text
README.md
method.md
runbook.md
artifact_index.md
result_readout.md
results/summary.md
results/human_summary.md
results/learning_health_readout.md
results/policy_reuse_readout.md
results/fairness_audit.md
results/no_lookahead_audit.md
```

### Phase 8.Stage 1.Action 2: Implement Readout Source

Generate:

```text
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/readout_source.json
```

It must include:

```text
repo_readout_surface
source_artifact_root
source_evaluation_root
evaluation_id
environment_instance_id
artifact_run_label
artifact_schema_version
run_mode
artifact_storage
expected_files
goal_criteria
badge_policy
goal_summary_sources
methodology_summary_sources
structural_limit_checks
claim_boundary
```

The readout source must point to the repo readout surface's checked-in
`readout_source.json`, not to the README or raw artifact folder.

### Phase 8.Stage 1.Action 3: Define Badge Inputs

Badge dimensions:

```text
Artifacts
Learning Signal
Behavior
Fairness
No Lookahead
Provenance
```

The learning badge must be derived from `learning_health_summary.csv`, not from
optimistic prose.

### Phase 8.Stage 1.Action 4: Seed Human Docs

The initial README must clearly state:

- this evaluation corrects the previous nominal learner failure;
- both arms now use trainable full-state/full-action policy contracts;
- the first model is linear/factorized, not neural/backprop;
- immediate inadmissibility masking remains active for both arms;
- no one-hop successor cul-de-sac lookahead is used;
- tower live state-lift hygiene remains active;
- long-run claims require the learning-health checks to pass first.

### Phase 8.Stage 1.Action 5: Add Readout Tests

Tests must prove:

- `readout_source.json` includes expected files and goal criteria;
- the README marks nominal updates as a failure if learning health fails;
- badge inputs are human-readable labels, not raw enum leakage;
- regenerated docs preserve the correct command:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/readout_source.json
```

## Phase 9: CLI Integration

### Phase 9.Stage 1.Action 1: Add CLI Commands

Add:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-state-policy-comparison run
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-state-policy-comparison summarize
```

### Phase 9.Stage 1.Action 2: Add Required CLI Arguments

The `run` command must support:

```text
--repo-root
--artifact-root
--readiness-source
--run-label
--locked-by
--episodes-per-arm
--replicates-per-arm
--schema-seeds
--max-seconds-per-episode
--learning-rate
--projection-attempt-budget
--progress-every-episodes
```

Defaults must match this workplan's decision locks.

### Phase 9.Stage 1.Action 3: Add Progress Reporting

The run command must show a progress bar or progress output comparable to the
current Warehouse diagnostic.

It must also write:

```text
progress_events.jsonl
```

### Phase 9.Stage 1.Action 4: Add CLI Tests

Tests must prove:

- CLI help exposes the new commands;
- smoke command writes artifacts;
- summarize command writes aggregate docs and readout source;
- invalid artifact roots outside the repo are not used as canonical readout
  roots.

## Phase 10: Replay Compatibility

### Phase 10.Stage 1.Action 1: Preserve Existing Replay Command

Ensure:

```text
warehouse-gridlock render-episode
```

works against artifacts from the corrected evaluation.

### Phase 10.Stage 1.Action 2: Add Policy Overlay Metadata

If feasible, add replay metadata fields:

```text
episode_index
arm_id
policy_id
model_family_id
selected_action_vector_hash
projection_attempt_count
reward
correct_robot_count
correct_box_count
```

If visual overlay requires more work than expected, keep the replay output
compatible and log the overlay as deferred. Do not block the policy contract
implementation on decorative replay overlays.

### Phase 10.Stage 1.Action 3: Add Replay Tests

Tests must prove:

- replay can render a direct corrected run episode;
- replay can render a tower corrected run episode;
- episode index changes the selected trajectory when source traces differ;
- output path is under the artifact root unless explicitly overridden.

## Phase 11: Smoke Execution

### Phase 11.Stage 1.Action 1: Run Unit Tests

Run:

```text
uv run pytest tests/environments/warehouse_gridlock
```

Record the result.

### Phase 11.Stage 1.Action 2: Run Corrected Smoke Evaluation

Run:

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-state-policy-comparison run \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/artifacts/policy_contract_smoke_001 \
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \
  --run-label policy_contract_smoke_001 \
  --locked-by foster \
  --episodes-per-arm 4 \
  --replicates-per-arm 1 \
  --schema-seeds 1 \
  --max-seconds-per-episode 128 \
  --projection-attempt-budget 64 \
  --progress-every-episodes 1
```

If the run takes unexpectedly long, do not silently reduce the budget. Stop and
record the runtime issue.

### Phase 11.Stage 1.Action 3: Summarize Corrected Smoke Evaluation

Run:

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-state-policy-comparison summarize \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/artifacts/policy_contract_smoke_001
```

Record generated paths.

### Phase 11.Stage 1.Action 4: Verify Learning Health

Inspect:

```text
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/artifacts/policy_contract_smoke_001/results/learning_health_summary.csv
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/artifacts/policy_contract_smoke_001/results/policy_reuse_summary.csv
```

The smoke implementation is not complete unless each active arm has:

```text
non_noop_update_count > 0
decisions_using_nonzero_prior_signal > 0
learning_status == real_learning_signal_present
```

If one arm fails this gate, stop and record the precise failure. Do not call the
evaluation trainable.

### Phase 11.Stage 1.Action 5: Regenerate Human-Readable Readout

Apply the readout protocol:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/readout_source.json
```

If the readout protocol cannot generate a truthful README from the source
binding, fix the source binding or docs writer before proceeding.

## Phase 12: Final Verification

### Phase 12.Stage 1.Action 1: Run Full Relevant Tests

Run:

```text
uv run pytest tests/environments/warehouse_gridlock
```

If feasible, also run the broader test subset that covers CLI and readout
generation.

Record all results.

### Phase 12.Stage 1.Action 2: Check Worktree

Run:

```text
git status --short
```

Classify changed files into:

- intended implementation code;
- intended tests;
- intended design/workplan/log docs;
- intended evaluation artifacts/readouts;
- unrelated pre-existing files.

Do not stage unrelated files.

### Phase 12.Stage 1.Action 3: Verify No False Claims

Search generated docs for forbidden claims:

```text
backprop
neural
statistical significance
general tower superiority
full MDP
optimal
```

Any occurrence must be either:

- explicitly negated;
- marked as future work;
- or removed.

### Phase 12.Stage 1.Action 4: Verify No Machine-Local Canonical Paths

Run release-hygiene-style path checks if available.

At minimum, ensure generated public docs and source bindings do not require
machine-local absolute paths for interpretation.

### Phase 12.Stage 1.Action 5: Update Implementation Log

Mark every completed `Phase.Stage.Action`.

Record:

- final branch;
- tests;
- smoke run;
- learning-health result;
- artifact/readout paths;
- known limitations;
- exact resume point if anything remains.

## Phase 13: Completion Criteria

### Phase 13.Stage 1.Action 1: Code Completion Criteria

Implementation is code-complete only if:

- policy contract types exist;
- linear factorized policy exists;
- shared resolver exists;
- direct corrected arm uses full config plus second;
- tower corrected arm uses full config/tier context plus second;
- both arms emit or realize full concrete action vectors;
- both arms update reusable policy state;
- candidate-id learning is not the primary learner state;
- CLI run and summarize commands work.

### Phase 13.Stage 1.Action 2: Artifact Completion Criteria

Artifact completion requires:

- manifests;
- run index;
- per-run event tables;
- aggregate tables;
- learning-health tables;
- policy-reuse tables;
- no-lookahead audit tables;
- tower live-lift tables;
- readout source;
- human-readable docs.

### Phase 13.Stage 1.Action 3: Learning Completion Criteria

The smoke run must show:

```text
non_noop_update_count > 0
decisions_using_nonzero_prior_signal > 0
policy_state_hash_initial != policy_state_hash_final
```

for both active arms.

If this does not hold, the implementation may still be artifact-complete, but
it is not learning-complete. The readout must say that.

### Phase 13.Stage 1.Action 4: Claim Completion Criteria

Final summary may claim:

```text
The Warehouse corrected policy contract was implemented and smoke-validated.
Both direct and tower arms use trainable full-state/full-action policy surfaces.
The smoke run produced inspectable learning-health evidence.
```

Final summary may not claim:

```text
Warehouse is solved.
Tower is better.
Backprop happened.
The full serious MDP was enumerated.
The result is statistically significant.
```

## Expected Final Commands For The Project Owner

After successful implementation, the repo should expose:

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-state-policy-comparison run \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/artifacts/policy_contract_smoke_001 \
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \
  --run-label policy_contract_smoke_001 \
  --locked-by foster \
  --episodes-per-arm 4 \
  --replicates-per-arm 1 \
  --schema-seeds 1 \
  --max-seconds-per-episode 128 \
  --projection-attempt-budget 64 \
  --progress-every-episodes 1
```

and:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/readout_source.json
```

The long pilot command must be provided only after the smoke run passes the
learning-health gate.
