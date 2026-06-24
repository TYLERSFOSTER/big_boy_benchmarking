# Warehouse Gridlock Full-Tower GPU PPO Implementation Workplan

## Status

Detailed implementation workplan.

This document is the execution contract for implementing the accepted
Warehouse Gridlock full-tower GPU PPO blueprint:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/005_warehouse_gridlock_full_tower_gpu_ppo_blueprint.md
```

Do not execute this workplan until the Project Owner explicitly asks to execute
it.

When execution is requested, follow the `Phase.Stage.Action` order below. Each
action is an obligation unless a stop condition is reached.

## Prime Directive Commitments

This workplan follows:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
docs/prime_directive/common_failure_mode_005_umbrella_workplan_fragmentation.md
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

Execution rules:

```text
1. Read each Phase.Stage.Action item immediately before implementing it.
2. Implement the action as written.
3. Do not silently simplify, reorder, or substitute nearby behavior.
4. If exact implementation is not possible, stop and record the blocker.
5. Do not invent Project Owner turns.
6. Do not put Codex-authored text under Project Owner headings.
7. Keep a running implementation log.
8. Keep artifacts repo-resident by default.
9. Keep generated human-readable readouts bound to readout_source.json.
```

## Source Authority

### Environment Authority

Primary Warehouse Gridlock environment authority:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_001_warehouse_gridlock_environment_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_002_warehouse_gridlock_environment_implementation_workplan.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_003_warehouse_gridlock_environment_implementation_log.md
```

Important correction:

The initial environment blueprint and early workplan contain older open or
provisional language about whether invalid ensemble attempts consume one
second. That older language is superseded by the later PO decision recorded in
the implementation log:

```text
invalid ensemble attempts do not consume one second.
invalid ensembles self-loop without advancing time_step.
no partial execution.
if any part of the ensemble is invalid, no robot or box moves.
```

This workplan must implement against that later locked decision.

### GPU PPO Authority

Primary full-tower GPU PPO authority:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/001_design_discussion.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/002_ppo_training_surface_map.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/003_tower_traversing_logic_discussion.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/004_blueprint_decision_gates_for_full_tower_gpu_ppo.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/005_warehouse_gridlock_full_tower_gpu_ppo_blueprint.md
```

Precedence inside the GPU PPO design folder:

```text
1. 004_blueprint_decision_gates_for_full_tower_gpu_ppo.md
2. 003_tower_traversing_logic_discussion.md
3. corrected tail of 002_ppo_training_surface_map.md
4. 001_design_discussion.md
```

The accepted blueprint controls implementation if it conflicts with earlier
discussion text.

## Attribution Guard

The following are Project Owner-originated and must be attributed to Tyler
Foster when described in implementation docs or readouts:

```text
1. The Warehouse Gridlock SVG physical-system design.
2. The hidden/discovered state-action graph benchmark framing.
3. The requirement that full-tower PPO uses hardcoded state_collapser tower
   traversal rather than a trainable traversal policy.
4. The per-tier model family based on rich state/action records, history
   encoding, candidate action encoding, and masked scoring over Out_k(s_t).
5. The PPO old/current model pair per tier:
   policy_k and rollout_policy_k.
6. The direct arm as the no-contraction schema arm.
7. The requirement that no arm receives a weird or unfair admissibility surface
   relative to the other arm.
```

Codex may be credited only for implementation organization, conservative
engineering recommendations, code, tests, and artifact/readout translation.

## Superseded Ideas That Must Not Return

Do not implement or imply any of the following:

```text
direct-only PPO as the first serious target;
fixed-active-tier tower PPO;
PPO learning tier traversal;
direct as a separate direct-control policy family;
shared learned parameters across tier policies;
representative fallback for executable lift resolution;
mutable episode/time/PPO facts inside state/action geometry JSONs;
official tiny Warehouse Gridlock benchmark instances;
long-run exhaustive per-step CSV dumping by default.
```

## Implementation Target

New evaluation family:

```text
warehouse_gridlock_full_tower_gpu_ppo_v001
```

New source package:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/full_tower_gpu_ppo/
```

New readout surface:

```text
docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/
```

Repo-resident artifact root for runs:

```text
docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/artifacts/<run_label>/
```

Implementation log:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/007_warehouse_gridlock_full_tower_gpu_ppo_implementation_log.md
```

## Required Branch

Use a new branch when executing:

```text
codex/warehouse-gridlock-full-tower-gpu-ppo
```

Do not implement this work on `main` unless the Project Owner explicitly
instructs otherwise.

## Global Stop Conditions

Stop and ask the Project Owner before proceeding if any of these occur:

```text
1. state_collapser does not expose the runtime or pointwise liftability surface
   needed for exact implementation.
2. The implementation would need representative fallback for execution.
3. PPO actor invocation would occur on an empty pointwise executable surface.
4. The direct arm cannot be represented as the no-contraction schema arm.
5. The only available implementation path would make PPO learn tier traversal.
6. Stored decision surfaces cannot be used to recompute PPO ratios.
7. A required artifact/readout contract would need to be weakened.
8. A long serious GPU run is required before smoke correctness is verified.
9. Existing user changes conflict with this work in a way that cannot be
   resolved by preserving them.
10. Any implementation step would require changing state_collapser itself.
```

If a state_collapser change is needed, write a BBB handoff note instead of
modifying state_collapser from this workplan.

## Phase 0: Repository State, Authority, And Execution Log

### Phase 0.Stage 1: Branch And Dirty-State Control

#### Phase 0.Stage 1.Action 1: Verify current branch

Run:

```bash
git branch --show-current
```

If the current branch is `main`, create and switch to:

```bash
git checkout -b codex/warehouse-gridlock-full-tower-gpu-ppo
```

If the branch already exists, switch to it only after checking that the working
tree state can be preserved safely.

#### Phase 0.Stage 1.Action 2: Inspect dirty state

Run:

```bash
git status --short
```

Classify every dirty file as:

```text
user/preexisting
expected generated artifact
current implementation target
unknown
```

Do not overwrite unknown or user/preexisting changes.

#### Phase 0.Stage 1.Action 3: Record branch and dirty state

Create:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/007_warehouse_gridlock_full_tower_gpu_ppo_implementation_log.md
```

Record:

```text
branch name
timestamp
git status summary
source authority list
known superseded environment time-semantics note
```

### Phase 0.Stage 2: Source Authority Re-Read

#### Phase 0.Stage 2.Action 1: Re-read Prime Directive files

Read the Prime Directive files listed in this workplan before implementing
code. In the log, record that this was done.

#### Phase 0.Stage 2.Action 2: Re-read Warehouse Gridlock environment sources

Re-read:

```text
warehouse_001.md
01_001_warehouse_gridlock_environment_blueprint.md
01_003_warehouse_gridlock_environment_implementation_log.md
```

Record the locked mechanics:

```text
16 x 16 PO drawing instance
32 robots
32 boxes
one second per valid environment transition
invalid ensemble self-loop without time advance
no partial execution
push-only box interaction
manual PO drawing manifest authority
hidden/effectively hidden admissible-state graph
```

#### Phase 0.Stage 2.Action 3: Re-read GPU PPO design sources

Re-read the entire `04_gpu_rl_training_loop` folder in order.

Record the locked PPO commitments:

```text
PPO does not learn tower traversal
direct is no-contraction schema
separate policy model per tier
geometry records exclude mutable episode/time/PPO facts
candidate-scoring masked softmax over current Out_k(s_t)
pointwise executable action surfaces only
no representative fallback for execution
stored decision surfaces for PPO ratios
repo-resident artifacts and readout_source.json
selected-trace retention rather than exhaustive long-run dumps
```

### Phase 0.Stage 3: Existing Code Inventory

#### Phase 0.Stage 3.Action 1: Inventory Warehouse Gridlock environment code

Inspect:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/
tests/environments/warehouse_gridlock/
docs/evaluations/warehouse_gridlock_001/
```

Record which existing modules can be reused for:

```text
environment state/action dataclasses
transition validation
reward computation
readiness manifests
episode replay/rendering
existing full-state policy comparison code
existing transformer policy code
CLI command registration
```

#### Phase 0.Stage 3.Action 2: Inventory relevant Counterpoint and PlateSupport patterns

Inspect existing serious evaluation packages for:

```text
artifact writer conventions
readout_source.json conventions
schema arm manifests
state_collapser runtime integration
threshold/frontier and paired comparison summaries
test organization
CLI parser layout
```

Reuse established patterns where they do not conflict with the accepted GPU
PPO blueprint.

#### Phase 0.Stage 3.Action 3: Verify dependency state

Run the project dependency/version check used elsewhere in the repo, or inspect
the lock file if no command exists.

Confirm:

```text
state_collapser >= 0.7.2 or newer compatible pointwise liftability semantics
torch import availability
tqdm availability if progress bars are used
```

If `state_collapser` lacks a required surface, stop and write the blocker in
the implementation log.

## Phase 1: Package Skeleton, Ids, Config, Profiles, And Paths

### Phase 1.Stage 1: Package Skeleton

#### Phase 1.Stage 1.Action 1: Create full_tower_gpu_ppo package

Create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/full_tower_gpu_ppo/
```

Add:

```text
__init__.py
ids.py
config.py
profiles.py
paths.py
```

Keep the package isolated from older smoke/full-state policy code so older
experiments remain reproducible.

#### Phase 1.Stage 1.Action 2: Define evaluation and policy ids

In `ids.py`, define stable ids for:

```text
WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_EVALUATION_ID
WAREHOUSE_GRIDLOCK_DIRECT_NO_CONTRACTION_ARM_ID
WAREHOUSE_GRIDLOCK_TOWER_FIRST_NONTRIVIAL_ARM_ID
WAREHOUSE_GRIDLOCK_POINTWISE_LIFTABILITY_SEMANTICS_ID
WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_ARTIFACT_CONTRACT_ID
WAREHOUSE_GRIDLOCK_PPO_RECORD_SCHEMA_VERSION
WAREHOUSE_GRIDLOCK_GEOMETRY_RECORD_SCHEMA_VERSION
WAREHOUSE_GRIDLOCK_DECISION_CONTEXT_SCHEMA_VERSION
WAREHOUSE_GRIDLOCK_ROLLOUT_SAMPLE_SCHEMA_VERSION
```

Add tests asserting that ids are stable strings and do not collide with older
Warehouse evaluation ids.

#### Phase 1.Stage 1.Action 3: Define source-authority constants

Expose constants listing the source docs and their precedence so manifests can
artifact the authority chain.

### Phase 1.Stage 2: Config Objects

#### Phase 1.Stage 2.Action 1: Implement run config dataclasses

In `config.py`, define dataclasses for:

```text
WarehouseFullTowerPPOConfig
WarehouseFullTowerPPOArmConfig
WarehousePPOHyperparameters
WarehousePolicyCapacityConfig
WarehouseRetentionConfig
WarehouseCheckpointConfig
WarehouseDeviceConfig
WarehouseTraceSelectionConfig
WarehouseDiscoveryAccountingConfig
```

Required top-level fields:

```text
run_label
repo_root
artifact_root
readiness_source
instance_id
arms
episodes_per_arm
replicates_per_arm
schema_seeds
max_seconds_per_episode
ppo_update_interval_samples
ppo_epochs
minibatch_size
gamma
gae_lambda
clip_epsilon
entropy_coef
value_coef
target_kl
learning_rate
max_grad_norm
device_profile_id
retention_profile_id
locked_by
random_seed
```

#### Phase 1.Stage 2.Action 2: Validate config invariants

Implement validation that rejects:

```text
episodes_per_arm <= 0
replicates_per_arm <= 0
schema_seeds <= 0
max_seconds_per_episode <= 0
missing readiness_source
artifact_root outside repo unless explicitly allowed
unknown arm ids
direct arm with non-no-contraction schema
tower arm without a nontrivial schema source
mixed_precision true in the initial implementation unless explicitly enabled
```

#### Phase 1.Stage 2.Action 3: Define conservative default hyperparameters

Choose conservative first defaults and artifact them.

These are implementation defaults, not Project Owner-originated decisions:

```text
gamma = 0.99
gae_lambda = 0.95
clip_epsilon = 0.2
entropy_coef = 0.01
value_coef = 0.5
target_kl = 0.03
max_grad_norm = 0.5
mixed_precision = false
advantage_normalization = per_tier_update_batch
```

If choosing exact `capacity_0`, `gamma_capacity`, or `min_capacity`, mark them
as consultant implementation defaults in manifests.

### Phase 1.Stage 3: Profiles

#### Phase 1.Stage 3.Action 1: Implement named profiles

In `profiles.py`, implement:

```text
smoke_cpu
debug_gpu
serious_gpu
```

Profile responsibilities:

```text
smoke_cpu:
  correctness and CI-friendly mechanics; CPU allowed; tiny budgets.

debug_gpu:
  short GPU run validating CUDA device path and PPO updates.

serious_gpu:
  long-run profile intended for Project Owner-initiated training only.
```

#### Phase 1.Stage 3.Action 2: Add long-run safety gating

Require explicit CLI flags for serious run sizes.

Do not allow default commands to accidentally start a long GPU job.

#### Phase 1.Stage 3.Action 3: Artifact profile manifests

Every run must write a profile manifest containing:

```text
profile_id
device request
device actually used
episodes/budget
PPO hyperparameters
capacity schedule
retention profile
long-run safety status
```

### Phase 1.Stage 4: Paths

#### Phase 1.Stage 4.Action 1: Implement path helpers

In `paths.py`, define paths for:

```text
evaluation_root
source_artifact_root
runs_root
summaries_root
checkpoints_root
docs_root
badges_root
readout_source_path
```

#### Phase 1.Stage 4.Action 2: Enforce repo-resident readout surface

Make the docs/readout surface resolve to:

```text
docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/
```

Do not write primary readouts only inside artifact-local folders.

## Phase 2: Schema Arms And state_collapser Runtime Boundary

### Phase 2.Stage 1: Schema Arm Contract

#### Phase 2.Stage 1.Action 1: Implement schema arm definitions

Create:

```text
schema_arms.py
```

Define two minimum arms:

```text
direct_no_contraction:
  no-contraction schema over the current discovered graph.

tower_first_nontrivial:
  first configured nontrivial Warehouse contraction schema.
```

#### Phase 2.Stage 1.Action 2: Reuse existing Warehouse schema where available

Inspect existing Warehouse contraction/tower code from prior experiments.

If a nontrivial Warehouse schema already exists and is valid under the accepted
design, reuse it.

If no valid nontrivial schema exists, stop and write a blocker. Do not invent a
new contraction schema inside this PPO workplan unless the accepted blueprint
already authorizes it.

#### Phase 2.Stage 1.Action 3: Write schema arm manifest

Each run must write:

```text
schema_arm_manifest.json
```

It must identify:

```text
arm_id
schema_id
schema_kind
direct/no-contraction status
nontrivial status
schema source
schema parameters
state_collapser dependency version
```

### Phase 2.Stage 2: Runtime Adapter

#### Phase 2.Stage 2.Action 1: Create state_collapser_runtime.py

Implement an adapter module that calls upstream `state_collapser` for:

```text
tower construction
active tier controller state
hardcoded traversal
pointwise executable action surfaces
executable lift candidates
strict lift resolution
linearization/tensorization surfaces where upstream provides them
```

Do not clone or reimplement state_collapser internals unless no upstream
surface exists and the Project Owner approves a separate design change.

#### Phase 2.Stage 2.Action 2: Enforce tower traversal boundary

The adapter must make this invariant mechanically clear:

```text
PPO does not choose LIFT, DESCEND, TRAIN, active tier, or traversal.
```

PPO may only choose from a tier-local, pointwise executable outgoing action
surface presented by the hardcoded runtime.

#### Phase 2.Stage 2.Action 3: Implement pointwise executable action query

Implement a query with the semantics:

```text
tier_is_executable_from_state(tier, current_base_state)
pointwise_executable_action_cells(tier, current_base_state)
executable_lift_candidates(tier, action_cell, current_base_state)
```

The returned candidate action list must be:

```text
nonempty before actor call
canonically ordered
stored in the decision context
accompanied by a mask
traceable to state_collapser semantics id
```

#### Phase 2.Stage 2.Action 4: Reject representative fallback

Add a runtime assertion that execution cannot use representative fallback.

If strict executable lift candidates are absent, emit a diagnostic event and do
not create a fake PPO sample.

#### Phase 2.Stage 2.Action 5: Classify NO_AVAILABLE_ACTION

Represent `NO_AVAILABLE_ACTION` as a runtime/control diagnostic.

It is not:

```text
a sampled PPO action
a negative action chosen by the actor
a placeholder candidate
a terminal success
```

### Phase 2.Stage 3: Time And Event Semantics

#### Phase 2.Stage 3.Action 1: Separate controller events and PPO samples

Define separate counters:

```text
controller_event_index
ppo_sample_index
environment_second
episode_index
global_update_index
```

#### Phase 2.Stage 3.Action 2: Enforce Warehouse time semantics

Only concrete valid Warehouse moves consume Warehouse time.

Hardcoded traversal events do not consume Warehouse time.

Invalid ensemble self-loops do not advance time under the later locked PO
decision.

#### Phase 2.Stage 3.Action 3: Write runtime event manifests

Each run must artifact the time and event convention so readouts can explain
why controller event count differs from PPO sample count and concrete
environment seconds.

## Phase 3: Record Contracts

### Phase 3.Stage 1: Geometry Records

#### Phase 3.Stage 1.Action 1: Create geometry_records.py

Define immutable geometry record dataclasses for:

```text
TierStateGeometryRecord
TierActionGeometryRecord
TowerSnapshotGeometryManifest
GeometryRecordValidationError
```

#### Phase 3.Stage 1.Action 2: Implement state geometry fields

State geometry records must include:

```text
schema_version
graph_snapshot_id
tower_snapshot_id
tier_index
tier_direction_convention
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

#### Phase 3.Stage 1.Action 3: Implement action geometry fields

Action geometry records must include:

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
out_hom_summary
action_hom_summary
geometry_source_manifest_ref
```

#### Phase 3.Stage 1.Action 4: Reject mutable geometry fields

Geometry records must reject:

```text
episode_index
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
selected_action
rollout_update_index
controller_event_index
ppo_sample_index
```

Add tests proving these fields cannot silently enter geometry JSON.

### Phase 3.Stage 2: Decision Context Records

#### Phase 3.Stage 2.Action 1: Create decision_context.py

Define:

```text
DecisionContextRecord
PointwiseActionSurfaceRecord
DecisionContextValidationError
```

#### Phase 3.Stage 2.Action 2: Implement required decision fields

Decision context records must include:

```text
decision_context_id
episode_id
replicate_index
schema_seed
arm_id
tier_index
ppo_sample_index
controller_event_index_start
controller_event_index_end
environment_second
active_tier
current_concrete_state_digest
current_position_at_every_tier
tower_position_key
runtime_snapshot_id
schema_arm_id
graph_snapshot_id
tower_snapshot_id
state_geometry_record_id
candidate_action_ids_ordered
candidate_local_indices
candidate_mask
mask_kind
mask_semantics_id
state_collapser_source_ref
controller_event_refs
```

#### Phase 3.Stage 2.Action 3: Validate pointwise action surface

Reject decision contexts where:

```text
candidate_action_ids_ordered is empty for an actor call
mask length differs from candidate count
all candidates are masked
mask_kind is not pointwise_executable
candidate order is missing
state_collapser source ref is missing
```

### Phase 3.Stage 3: Rollout Sample Records

#### Phase 3.Stage 3.Action 1: Create rollout_samples.py

Define:

```text
RolloutSampleRecord
RolloutBufferShard
RolloutSampleValidationError
```

#### Phase 3.Stage 3.Action 2: Implement required PPO sample fields

Rollout samples must include:

```text
rollout_sample_id
decision_context_id
tier_index
policy_snapshot_id
rollout_policy_snapshot_id
state_history_ref
action_history_ref
candidate_action_ids_ordered
candidate_mask
selected_local_index
selected_action_cell_id
old_log_prob
value_estimate
entropy
resolved_concrete_action_digest
lift_candidate_id
lift_candidate_digest
lift_semantics_id
reward
next_decision_context_id
terminated
truncated
bootstrap_value
diagnostic_failure_code
```

#### Phase 3.Stage 3.Action 3: Validate PPO sample invariants

Reject samples where:

```text
old_log_prob is missing
rollout_policy_snapshot_id is missing
selected index is outside stored candidate surface
selected candidate is masked
candidate order differs from decision context
reward is missing
termination/truncation flags are inconsistent
diagnostic failure is being treated as a selected action
```

### Phase 3.Stage 4: Stable Serialization

#### Phase 3.Stage 4.Action 1: Implement deterministic JSON/CSV writers

Create serialization helpers that write:

```text
stable key ordering
repo-relative paths where possible
schema versions
source authority refs
content digests for large objects
```

#### Phase 3.Stage 4.Action 2: Add round-trip tests

Add tests for deterministic serialization and round-trip loading of:

```text
geometry records
decision context records
rollout sample records
run config
profile manifests
```

## Phase 4: Tokenization And Per-Tier Policy Models

### Phase 4.Stage 1: Tokenization Contract

#### Phase 4.Stage 1.Action 1: Create tokenization.py

Implement encoders for:

```text
state geometry records
action geometry records
decision context scalar features
time/environment second features
tier index features
history position features
```

#### Phase 4.Stage 1.Action 2: Preserve stable ids

Tokenization must preserve stable ids through side channels or manifests so
readouts can map model inputs back to state/action records.

#### Phase 4.Stage 1.Action 3: Emit tokenization manifest

Every run must write:

```text
record_tokenization_manifest.json
```

It must include:

```text
record schema versions
token dimensions
hashing/embedding strategy
unknown-token policy
history truncation policy
candidate ordering policy
padding policy
mask semantics
```

### Phase 4.Stage 2: Model Architecture

#### Phase 4.Stage 2.Action 1: Create models.py

Implement the Project Owner-originated per-tier architecture in implementation
form:

```text
history_encoder_k(state_hist, act_hist) -> c_t
candidate_encoder_k(edge_json, src_state, tgt_state, tier, time) -> u_i
score_k(c_t, u_i) -> logit_i
masked softmax over i with a_i in Out_k(s_t)
value_head_k(c_t, decision_context) -> V_k
```

#### Phase 4.Stage 2.Action 2: Implement history encoder

The history encoder must accept:

```text
state history token sequence
action history token sequence
history masks
position/time encodings
```

It must produce a context vector usable by both actor scoring and critic.

#### Phase 4.Stage 2.Action 3: Implement candidate encoder

The candidate encoder must accept candidate action geometry plus source/target
state geometry and context features.

It must support variable candidate counts per decision surface.

#### Phase 4.Stage 2.Action 4: Implement masked candidate scorer

The scorer must:

```text
score each stored candidate in local order
apply the stored pointwise executable mask
return logits, log_probs, entropy, selected index, selected id
assign zero probability to masked candidates
fail clearly if all candidates are masked
```

#### Phase 4.Stage 2.Action 5: Implement value head

The value head must estimate the value of the current decision context for the
active tier.

It must not depend on hidden future information or full-run outcomes.

### Phase 4.Stage 3: Policy Bank

#### Phase 4.Stage 3.Action 1: Create policy_bank.py

Implement:

```text
TierPolicyBank
TierPolicyEntry
PolicySnapshot
PolicyCapacitySchedule
```

#### Phase 4.Stage 3.Action 2: Create separate policy per nondegenerate tier

For every active nondegenerate tier:

```text
policy_k is a separate trainable model
rollout_policy_k is a frozen snapshot
optimizer_k is separate unless explicitly configured otherwise
rollout_buffer_k is separate
```

No learned parameters are shared across tiers in this implementation.

#### Phase 4.Stage 3.Action 3: Implement capacity schedule

Implement:

```text
capacity_k = max(min_capacity, round(capacity_0 * gamma_capacity**k))
```

Artifact:

```text
capacity_schedule_manifest.json
```

#### Phase 4.Stage 3.Action 4: Implement rollout snapshot refresh

At PPO update boundaries:

```text
rollout_policy_k.load_state_dict(policy_k.state_dict())
rollout_policy_k.eval()
rollout_policy_k.requires_grad_(False)
```

Store snapshot ids and write a snapshot manifest.

### Phase 4.Stage 4: History Management

#### Phase 4.Stage 4.Action 1: Implement per-tier histories

Maintain tier-local:

```text
state_hist_k
act_hist_k
```

Histories must follow the hardcoded traversal runtime and record only tier-k
decision/action events relevant to policy_k.

#### Phase 4.Stage 4.Action 2: Implement history truncation

Use a configured max history length.

Truncation policy:

```text
oldest prefix truncation
truncation recorded in decision context or history manifest
```

#### Phase 4.Stage 4.Action 3: Add history tests

Test that histories:

```text
advance only when tier-local PPO samples occur
do not confuse controller events with action history
respect max length
serialize deterministically
```

## Phase 5: Rollout Collection And Hardcoded Tower Traversal

### Phase 5.Stage 1: Runner Skeleton

#### Phase 5.Stage 1.Action 1: Create runner.py

Implement a runner with explicit phases:

```text
load config
load readiness source
construct environment
construct schema arms
construct state_collapser tower runtime
construct policy bank
collect rollouts
run PPO updates
write artifacts
summarize
```

#### Phase 5.Stage 1.Action 2: Keep run loop arm-agnostic

Both direct/no-contraction and tower/nontrivial arms must use the same runner,
same PPO machinery, same record contracts, and same artifact surfaces.

#### Phase 5.Stage 1.Action 3: Add progress display

Use a progress bar for user-facing long runs when available.

Progress postfix should prioritize:

```text
reward
success
updates
arm
tier
episode
```

Reward should appear early because the user explicitly asked for reward to be
visible first in progress output.

### Phase 5.Stage 2: Episode Loop

#### Phase 5.Stage 2.Action 1: Implement episode initialization

For every episode:

```text
reset Warehouse Gridlock environment
reset hardcoded runtime position
reset episode-local counters
initialize per-tier histories
record episode manifest row
```

#### Phase 5.Stage 2.Action 2: Run until terminal or horizon

Loop until:

```text
full success
max_seconds_per_episode reached
runtime no-available-action terminal condition
configured safety limit reached
```

#### Phase 5.Stage 2.Action 3: Respect Warehouse invalid-time semantics

If a concrete invalid ensemble is attempted, the environment self-loops without
advancing `environment_second`.

Record the invalid event.

Do not let invalid self-loop create an unbounded infinite loop. Add a separate
runtime safety counter and artifact it.

### Phase 5.Stage 3: Controller Events

#### Phase 5.Stage 3.Action 1: Record traversal/controller events

Record events for:

```text
tower position changes
hardcoded descent/lift/control decisions
TRAIN events if exposed by runtime
NO_AVAILABLE_ACTION diagnostics
strict lift candidate resolution
concrete action execution
```

#### Phase 5.Stage 3.Action 2: Separate controller events from PPO samples

Controller events must go to controller event tables.

PPO samples must go to rollout sample tables.

The same event may be cross-referenced, but not conflated.

#### Phase 5.Stage 3.Action 3: Add invariant tests

Test that:

```text
TRAIN is not stored as a PPO selected action
LIFT/DESCEND are not stored as PPO selected actions
NO_AVAILABLE_ACTION is not stored as a PPO selected action
controller event count may exceed PPO sample count
```

### Phase 5.Stage 4: Actor Invocation

#### Phase 5.Stage 4.Action 1: Build decision context before actor call

For each actor call:

```text
query pointwise executable action surface
build geometry records if needed
build decision context
validate candidate order and mask
write or buffer decision context
```

#### Phase 5.Stage 4.Action 2: Call rollout_policy_k only

During rollout, sample from:

```text
rollout_policy_k
```

Do not sample from mutable `policy_k` during a rollout batch.

#### Phase 5.Stage 4.Action 3: Store exact selected surface

After sampling, store:

```text
candidate ids
candidate order
candidate mask
selected local index
selected action id
old_log_prob
value estimate
entropy
rollout policy snapshot id
```

#### Phase 5.Stage 4.Action 4: Resolve concrete execution

Use strict executable lift candidates only.

Store:

```text
lift candidate id
lift candidate digest
resolved concrete action digest
lift semantics id
```

If strict resolution fails, emit a diagnostic and do not fake a sample.

### Phase 5.Stage 5: Rewards And Next Context

#### Phase 5.Stage 5.Action 1: Assign PPO reward from concrete transition

Reward comes from the Warehouse environment transition and configured reward
mode.

Do not reward traversal events directly in the initial implementation.

#### Phase 5.Stage 5.Action 2: Link next decision context

Each rollout sample must point to the next decision context or terminal/truncate
state needed for GAE.

#### Phase 5.Stage 5.Action 3: Record episode summaries

For each episode, write summary rows for:

```text
total_reward
success
seconds_elapsed
valid_concrete_moves
invalid_concrete_moves
controller_event_count
ppo_sample_count
per-tier sample counts
NO_AVAILABLE_ACTION count
```

## Phase 6: GAE, Returns, And PPO Update Engine

### Phase 6.Stage 1: GAE

#### Phase 6.Stage 1.Action 1: Create gae.py

Implement Generalized Advantage Estimation:

```text
delta_t = reward_t + gamma * V(next_state) * nonterminal - V(state_t)
advantage_t = delta_t + gamma * lambda * nonterminal * advantage_{t+1}
return_t = advantage_t + V(state_t)
```

#### Phase 6.Stage 1.Action 2: Distinguish terminal and truncation

Handle:

```text
terminal success:
  no bootstrap beyond terminal.

time-limit truncation:
  bootstrap from value estimate if configured and valid.

NO_AVAILABLE_ACTION diagnostic terminal:
  classify separately and apply configured handling.
```

#### Phase 6.Stage 1.Action 3: Normalize advantages per tier

Normalize advantages within each tier update batch.

Do not normalize across tiers.

### Phase 6.Stage 2: PPO Loss

#### Phase 6.Stage 2.Action 1: Create ppo.py

Implement PPO clipped objective:

```text
ratio = exp(new_log_prob - old_log_prob)
policy_loss = -mean(min(ratio * advantage, clipped_ratio * advantage))
value_loss = configured value objective
entropy_bonus = entropy coefficient * entropy
total_loss = policy_loss + value_coef * value_loss - entropy_coef * entropy
```

#### Phase 6.Stage 2.Action 2: Recompute new log prob on stored surface

For every update, reconstruct model input from stored:

```text
state/action histories
candidate ids
candidate order
candidate mask
selected local index
```

Do not recompute candidate order or mask from the live graph.

#### Phase 6.Stage 2.Action 3: Enforce old/new ratio invariants

Add assertions:

```text
old_log_prob exists
new_log_prob finite
ratio finite
selected index valid
stored candidate order matches batch tensor order
```

### Phase 6.Stage 3: Per-Tier Updates

#### Phase 6.Stage 3.Action 1: Group rollout samples by tier

Each tier updates only from its own rollout buffer.

#### Phase 6.Stage 3.Action 2: Handle low-sample tiers

Implement a configured policy:

```text
carry_forward_until_min_samples
or
final_small_update_with_flag
```

The selected policy must be artifacted.

#### Phase 6.Stage 3.Action 3: Run PPO epochs and minibatches

For each tier with enough samples:

```text
shuffle samples deterministically from seed
run configured PPO epochs
apply gradient clipping
track optimizer steps
track approximate KL
optionally early-stop on target KL
```

#### Phase 6.Stage 3.Action 4: Refresh rollout snapshots

After a successful update boundary, refresh `rollout_policy_k` from
`policy_k`.

Record snapshot ids.

### Phase 6.Stage 4: PPO Diagnostics

#### Phase 6.Stage 4.Action 1: Write update summary rows

For every tier update, write:

```text
global_update_index
tier_index
arm_id
sample_count
optimizer_steps
policy_loss
value_loss
entropy
approx_kl
clip_fraction
explained_variance
grad_norm
learning_rate
ppo_epochs
minibatch_size
device
update_wall_time_seconds
snapshot_before
snapshot_after
```

#### Phase 6.Stage 4.Action 2: Write skipped-update rows

If a tier does not update because sample count is low, write an explicit row.

Do not make missing rows carry semantic meaning.

#### Phase 6.Stage 4.Action 3: Add PPO health tests

Tests must prove:

```text
at least one optimizer step occurs in smoke runs with samples
old/new ratio changes after an update when gradients are nonzero
KL and clip fraction are finite
skipped updates are explicitly recorded
```

## Phase 7: Device Handling, Checkpoints, And Resume

### Phase 7.Stage 1: Device Handling

#### Phase 7.Stage 1.Action 1: Create device selection utility

Implement device selection for:

```text
cpu
cuda
auto
```

Record requested and actual device.

#### Phase 7.Stage 1.Action 2: Implement CUDA fallback policy

For `smoke_cpu`, use CPU.

For `debug_gpu` and `serious_gpu`, if CUDA is unavailable:

```text
fail clearly unless profile explicitly allows fallback.
```

Do not silently run a claimed GPU run on CPU.

#### Phase 7.Stage 1.Action 3: Write device manifest

Write:

```text
device_manifest.json
```

Include:

```text
torch version
cuda availability
requested device
actual device
dtype
mixed precision flag
determinism settings
```

### Phase 7.Stage 2: Checkpoints

#### Phase 7.Stage 2.Action 1: Implement checkpoint format

Checkpoint at PPO update boundaries.

Include:

```text
config
run manifest
policy bank state
optimizer states
rollout snapshot states
random generator states if practical
global counters
completed episode/update indices
artifact schema versions
```

#### Phase 7.Stage 2.Action 2: Implement resume loading

Resume only from clean PPO update boundaries in the initial implementation.

If mid-rollout resume is requested, stop unless a later workplan authorizes it.

#### Phase 7.Stage 2.Action 3: Add checkpoint tests

Test:

```text
save checkpoint
load checkpoint
continue one update
manifest marks resumed run
corrupt checkpoint fails clearly
```

### Phase 7.Stage 3: Long-Run Safety

#### Phase 7.Stage 3.Action 1: Add wall-time and episode limits

Support:

```text
max_wall_time_seconds
max_episodes
max_updates
```

#### Phase 7.Stage 3.Action 2: Gracefully stop at update boundaries

If a stop limit triggers, finish current safe boundary and write:

```text
run_status = stopped_at_boundary
resume_checkpoint = <path>
```

#### Phase 7.Stage 3.Action 3: Avoid massive default CSV dumps

Use selected-trace retention by default.

Do not dump every step/candidate/tensor/frame for long serious runs unless a
debug retention profile explicitly requests it.

## Phase 8: Artifact Contract, Retention, And Aggregation

### Phase 8.Stage 1: Events And Retention

#### Phase 8.Stage 1.Action 1: Create events.py

Define row schemas for:

```text
controller_events
ppo_rollout_samples
episode_summary
ppo_update_summary
tier_policy_summary
pointwise_action_surface_summary
lift_resolution_summary
no_available_action_summary
discovery_accounting_summary
trace_selection_summary
timing_summary
```

#### Phase 8.Stage 1.Action 2: Create retention.py

Implement retention profiles:

```text
smoke_debug:
  retain enough detailed traces to debug tests.

serious_train:
  retain summaries always and selected traces only.

full_debug:
  explicit opt-in for large dumps.
```

#### Phase 8.Stage 1.Action 3: Select detailed traces

Default selected traces should include:

```text
first episode
last episode
first success if any
best reward so far
worst diagnostic failure
one representative episode after each update interval if configured
```

### Phase 8.Stage 2: Manifests

#### Phase 8.Stage 2.Action 1: Create manifests.py

Write manifests for:

```text
evaluation_manifest.json
run_manifest.json
profile_manifest.json
schema_arm_manifest.json
device_manifest.json
dependency_manifest.json
state_collapser_runtime_manifest.json
capacity_schedule_manifest.json
record_schema_manifest.json
tokenization_manifest.json
checkpoint_manifest.json
retention_manifest.json
source_authority_manifest.json
```

#### Phase 8.Stage 2.Action 2: Include claim boundary

Manifests must state that initial runs are system/evaluation readiness evidence,
not final broad benchmark claims.

#### Phase 8.Stage 2.Action 3: Include dependency provenance

Record:

```text
state_collapser version
torch version
python version
BBB git commit if available
dirty state summary if available
```

### Phase 8.Stage 3: Aggregation

#### Phase 8.Stage 3.Action 1: Create aggregation.py

Aggregate summaries for:

```text
training curves
reward over episodes
success over episodes
per-tier sample counts
per-tier optimizer steps
PPO health
action-surface health
NO_AVAILABLE_ACTION diagnostics
lift success/failure
controller vs PPO event counts
direct vs tower comparison
device/timing
```

#### Phase 8.Stage 3.Action 2: Keep claims bounded

Summary tables must distinguish:

```text
system mechanics passed
PPO actually updated
training reward improved
tower arm outperformed direct in this run
statistical benchmark claim
```

Only the first three may be claimed from smoke runs.

#### Phase 8.Stage 3.Action 3: Write expected files list

The aggregation step must produce an `expected_files` section in
`readout_source.json` sufficient for the artifact-table readout protocol.

## Phase 9: Human-Readable Docs And Readout Source

### Phase 9.Stage 1: docs_writer.py

#### Phase 9.Stage 1.Action 1: Create docs_writer.py

Write repo-side docs under:

```text
docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/
```

Expected files:

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

#### Phase 9.Stage 1.Action 2: Generate readout_source.json

Create:

```text
docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/readout_source.json
```

It must point to repo-resident artifacts and summary tables.

#### Phase 9.Stage 1.Action 3: Include methodology fields for readout protocol

`readout_source.json` must include enough information for:

```text
badge strip
plain-English evaluation question
claim boundary
methodology
artifact provenance
result interpretation
known limitations
conversation section
system learning hooks
```

### Phase 9.Stage 2: Badges

#### Phase 9.Stage 2.Action 1: Generate badge SVGs

Generate badges for:

```text
artifacts_complete
ppo_updates
pointwise_liftability
representative_fallback
device
direct_arm
tower_arm
readout_source
claim_boundary
```

#### Phase 9.Stage 2.Action 2: Match existing badge style

Use the style established in successful Counterpoint and PlateSupport readouts.

Do not regress to plain text pseudo-badges or inconsistent badge styling.

### Phase 9.Stage 3: Readout Protocol Compatibility

#### Phase 9.Stage 3.Action 1: Verify protocol invocation

After a run and summarize, the human-readable command must be:

```bash
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/readout_source.json
```

#### Phase 9.Stage 3.Action 2: Preserve conversation section behavior

Generated README must include a conversation section that can preserve
Project Owner / Evaluator and Embedded Engineering Consultant / Codex turn
pairs without inventing turns.

#### Phase 9.Stage 3.Action 3: Add readout compatibility test

Add a test that checks the readout source contains required protocol fields and
all referenced files exist after summarize.

## Phase 10: CLI Surface

### Phase 10.Stage 1: CLI Registration

#### Phase 10.Stage 1.Action 1: Extend CLI parser

Add:

```text
warehouse-gridlock full-tower-gpu-ppo inspect
warehouse-gridlock full-tower-gpu-ppo run
warehouse-gridlock full-tower-gpu-ppo summarize
warehouse-gridlock full-tower-gpu-ppo render-episode
```

Keep existing Warehouse Gridlock commands working.

#### Phase 10.Stage 1.Action 2: Add command help

Each command must expose useful `--help` text and name the repo-side readout
surface.

### Phase 10.Stage 2: inspect

#### Phase 10.Stage 2.Action 1: Implement inspect command

`inspect` must check:

```text
readiness source exists
environment manifest can load
state_collapser version/surfaces exist
schema arms can be built
torch/device availability
artifact root writability
profile validity
```

#### Phase 10.Stage 2.Action 2: Return JSON status

Return JSON with:

```text
status
failure_reason
environment_family_id
evaluation_id
state_collapser_version
torch_version
device_status
schema_arm_status
```

### Phase 10.Stage 3: run

#### Phase 10.Stage 3.Action 1: Implement run command

Required arguments:

```text
--repo-root
--artifact-root
--readiness-source
--run-label
--locked-by
--profile
```

Optional overrides:

```text
--episodes-per-arm
--replicates-per-arm
--schema-seeds
--max-seconds-per-episode
--device
--ppo-update-interval-samples
--retention-profile
--progress-every-episodes
--resume-from-checkpoint
```

#### Phase 10.Stage 3.Action 2: Require explicit serious run confirmation

If the command selects `serious_gpu` or large budgets, require an explicit flag
such as:

```text
--confirm-long-run
```

The exact flag name may follow local CLI style.

#### Phase 10.Stage 3.Action 3: Emit machine-readable completion JSON

Return:

```text
status
run_label
artifact_root
readout_source
checkpoint_path
artifact_count
failure_reason
```

### Phase 10.Stage 4: summarize

#### Phase 10.Stage 4.Action 1: Implement summarize command

`summarize` must read the run artifacts and generate:

```text
aggregate tables
readout_source.json
repo-side docs
badges
```

#### Phase 10.Stage 4.Action 2: Make summarize idempotent

Running summarize twice on the same artifact root should not duplicate rows or
corrupt the readout surface.

### Phase 10.Stage 5: render-episode

#### Phase 10.Stage 5.Action 1: Implement selected-trace replay

`render-episode` must render only episodes retained by the retention policy.

If a requested episode was not retained, error with a clear message listing
available retained traces.

#### Phase 10.Stage 5.Action 2: Preserve exact episode indexing

Do not reproduce the prior bug where different episode indices render the same
movie.

Tests must prove different retained episode indices resolve to different trace
sources.

#### Phase 10.Stage 5.Action 3: Output GIF path clearly

Return JSON with:

```text
status
output
episode_index
arm_id
replicate_index
schema_seed
trace_source
```

## Phase 11: Tests

### Phase 11.Stage 1: Unit Tests

#### Phase 11.Stage 1.Action 1: Add record contract tests

Create tests for:

```text
geometry record mutable field rejection
decision context nonempty pointwise surface validation
rollout sample old_log_prob requirement
candidate order preservation
serialization determinism
```

#### Phase 11.Stage 1.Action 2: Add model tests

Test:

```text
masked softmax gives zero probability to masked candidates
all-masked surface fails clearly
variable candidate count batches work
policy bank creates distinct model objects per tier
capacity schedule artifacts expected capacities
rollout snapshot is frozen
```

#### Phase 11.Stage 1.Action 3: Add PPO tests

Test:

```text
GAE terminal/truncation distinction
old/new log prob ratio uses stored surface
PPO update changes policy parameters
skipped low-sample tier update is explicitly recorded
approx KL and clip fraction finite
```

### Phase 11.Stage 2: Integration Tests

#### Phase 11.Stage 2.Action 1: Add inspect integration test

Run inspect in `smoke_cpu` mode against the existing Warehouse readiness
source.

#### Phase 11.Stage 2.Action 2: Add direct smoke run test

Run a tiny direct/no-contraction smoke config.

Assert:

```text
PPO samples exist
PPO updates exist
direct schema id is no-contraction
readout_source.json exists after summarize
```

#### Phase 11.Stage 2.Action 3: Add tower smoke run test

Run a tiny nontrivial tower smoke config.

Assert:

```text
at least one nondegenerate tier policy exists
pointwise liftability semantics id exists
no representative fallback occurred
controller events and PPO samples are distinct
```

#### Phase 11.Stage 2.Action 4: Add selected trace render test

Run render on a retained smoke episode and assert the GIF exists.

### Phase 11.Stage 3: Regression Tests

#### Phase 11.Stage 3.Action 1: Add artifact path regression

Assert primary docs and `readout_source.json` are repo-side, not only
artifact-local.

#### Phase 11.Stage 3.Action 2: Add old movie-index regression

Assert different retained episode indices map to different step traces or
different trace identifiers.

#### Phase 11.Stage 3.Action 3: Add no-fake-learning regression

Assert update summaries contain real optimizer steps and model parameter
changes. This guards against returning to scripted/random policies while
printing training-like progress.

### Phase 11.Stage 4: Test Command

#### Phase 11.Stage 4.Action 1: Run focused tests

Run:

```bash
uv run pytest tests/environments/warehouse_gridlock -q
```

Record results in the implementation log.

#### Phase 11.Stage 4.Action 2: Run broader affected tests

Run the repo's relevant affected test set. If full test runtime is large, run
the Warehouse and shared artifact tests first, then record what was not run.

## Phase 12: Smoke Execution And Readout Verification

### Phase 12.Stage 1: Inspect Smoke

#### Phase 12.Stage 1.Action 1: Run inspect in smoke_cpu profile

Example shape:

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-tower-gpu-ppo inspect \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/artifacts/smoke_cpu_001 \
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \
  --profile smoke_cpu
```

Adjust exact flags to match implemented CLI.

#### Phase 12.Stage 1.Action 2: Record inspect output

Record status, failure reason, and dependency/device state in the log.

### Phase 12.Stage 2: Run Smoke

#### Phase 12.Stage 2.Action 1: Run a small smoke training job

Run both minimum arms under a small CPU profile.

The run must be large enough to produce at least one real PPO update but small
enough for development verification.

#### Phase 12.Stage 2.Action 2: Confirm real learning machinery

Verify:

```text
rollout samples exist
old_log_prob exists
new_log_prob was recomputed
optimizer steps > 0 for at least one tier/arm
policy parameter change is recorded
PPO update rows exist
reward/episode summaries exist
```

#### Phase 12.Stage 2.Action 3: Confirm no false tower mechanics

Verify:

```text
PPO did not sample traversal actions
TRAIN is not a sampled PPO action
representative fallback count is zero
empty pointwise actor calls are zero
direct is no-contraction
tower arm is nontrivial
```

### Phase 12.Stage 3: Summarize Smoke

#### Phase 12.Stage 3.Action 1: Run summarize

Run:

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-tower-gpu-ppo summarize \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/artifacts/smoke_cpu_001
```

Adjust exact flags to match implemented CLI.

#### Phase 12.Stage 3.Action 2: Verify readout source

Confirm:

```text
docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/readout_source.json exists
readout_source.json points to existing tables
badge files exist
README exists
artifact_index exists
method/runbook/glossary exist
```

### Phase 12.Stage 4: Render Smoke Trace

#### Phase 12.Stage 4.Action 1: Render a retained episode

Run render for one retained direct episode and one retained tower episode if
available.

#### Phase 12.Stage 4.Action 2: Verify output

Verify:

```text
GIF exists
trace source exists
episode index is correct
rendered episode is not silently substituted
```

### Phase 12.Stage 5: Generate Human-Readable Readout

#### Phase 12.Stage 5.Action 1: Apply readout protocol

Use:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/readout_source.json
```

#### Phase 12.Stage 5.Action 2: Inspect generated README

Check:

```text
badge styling matches existing reports
claim boundary is bounded
PPO mechanics are explained plainly
Project Owner-originated model attribution is correct
conversation section has safe turn placeholders
no Project Owner words are invented
```

## Phase 13: Documentation Updates

### Phase 13.Stage 1: Environment And Evaluation Indexes

#### Phase 13.Stage 1.Action 1: Update evaluation index

Update:

```text
docs/evaluations/README.md
```

Add the Warehouse full-tower GPU PPO evaluation with its bounded status.

#### Phase 13.Stage 1.Action 2: Update Warehouse evaluation family index

If present, update:

```text
docs/evaluations/warehouse_gridlock_001/README.md
```

If absent and local patterns support it, create a concise index.

#### Phase 13.Stage 1.Action 3: Update root README only if warranted

Update root `README.md` only after smoke run/readout exists and only with a
bounded statement such as:

```text
Full-tower GPU PPO training machinery exists for Warehouse Gridlock and has
passed smoke/readiness checks.
```

Do not claim serious benchmark success from smoke runs.

### Phase 13.Stage 2: System Learning Hooks

#### Phase 13.Stage 2.Action 1: Create system learning folder if needed

If implementation exposes architectural lessons, create:

```text
docs/design/system_learning_from_evaluations/warehouse_gridlock_full_tower_gpu_ppo/
```

#### Phase 13.Stage 2.Action 2: Archive major lessons

Archive only substantive lessons, such as:

```text
state_collapser runtime surface gaps
pointwise liftability problems
PPO record contract confusion
GPU/device reproducibility issues
trace retention failures
human-readability confusion
```

Do not archive routine implementation chatter.

## Phase 14: Final Verification And Commit Preparation

### Phase 14.Stage 1: Static Review

#### Phase 14.Stage 1.Action 1: Search for forbidden terminology and stale claims

Run searches for:

```text
representative fallback
learned traversal
direct-control policy family
fixed active tier
invalid consumes one second
gameplan
Project Owner Turn
```

Confirm any hits are either historical source documents or explicitly marked
as superseded.

#### Phase 14.Stage 1.Action 2: Search for machine-local paths

Search generated docs/manifests for machine-local paths that should be
repo-relative, except explicit local provenance fields where allowed.

#### Phase 14.Stage 1.Action 3: Run release hygiene if relevant

If root/public docs are touched, run the release hygiene script and fix any
public-release blockers.

### Phase 14.Stage 2: Test Verification

#### Phase 14.Stage 2.Action 1: Run focused tests

Run Warehouse-focused tests again.

#### Phase 14.Stage 2.Action 2: Run broader tests as practical

Run broader tests if runtime is reasonable. If not, record exact tests skipped
and why.

#### Phase 14.Stage 2.Action 3: Record all results

Record command, status, and important output summary in the implementation log.

### Phase 14.Stage 3: Git Review

#### Phase 14.Stage 3.Action 1: Inspect git status

Run:

```bash
git status --short
```

Review every tracked and untracked path.

#### Phase 14.Stage 3.Action 2: Ensure generated large artifacts are intentional

Do not accidentally stage massive step/event dumps, movies, checkpoints, or
debug traces unless they are explicitly part of the intended repo-resident
smoke artifact contract.

#### Phase 14.Stage 3.Action 3: Prepare final change summary

Prepare a summary grouped by:

```text
source package
CLI
tests
docs/readouts
artifacts
known limitations
tests run
```

## Completion Criteria

The workplan is complete only when all of the following are true:

```text
1. Full-tower GPU PPO package exists.
2. Direct/no-contraction and tower/nontrivial arms use the same PPO machinery.
3. PPO does not learn tower traversal.
4. Per-tier policy_k and rollout_policy_k exist and are artifacted.
5. PPO samples store old_log_prob and exact decision surfaces.
6. PPO updates recompute new_log_prob on stored surfaces.
7. Geometry records reject mutable episode/time/PPO fields.
8. Pointwise executable action surfaces are nonempty before actor calls.
9. Representative fallback is impossible for execution.
10. Controller events and PPO samples are distinct.
11. Concrete Warehouse time semantics match the locked PO decision.
12. Smoke run produces real optimizer updates.
13. Summarize produces repo-side readout_source.json and docs.
14. Selected trace rendering works and respects episode index.
15. Focused tests pass or every failure is recorded with a blocker.
16. Implementation log records every completed Phase.Stage.Action item.
```

## Non-Blocking Future Work

Do not implement these inside this workplan unless the Project Owner explicitly
authorizes an expansion:

```text
semi-MDP/options PPO
learned lift-candidate selection
learned tower traversal
shared cross-tier parameterization
distributed rollout workers
vectorized Warehouse simulation
cross-tier discovery pressure mechanisms
large serious benchmark claim runs
public leaderboard surfaces
```
