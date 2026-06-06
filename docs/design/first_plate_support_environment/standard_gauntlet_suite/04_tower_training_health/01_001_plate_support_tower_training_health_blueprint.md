# PlateSupport Tower Training Health Blueprint

## Status

Status: initial child-stage blueprint.

This is a design blueprint for Stage 4 of the PlateSupport standard gauntlet
suite. It is not an implementation workplan and not execution approval.

Depends on:

```text
../00_suite_architecture/01_001_plate_support_standard_gauntlet_suite_architecture_blueprint.md
../01_structural_and_tower_diagnostics/01_001_plate_support_structural_and_tower_diagnostics_blueprint.md
../02_contraction_schema_sweep/01_001_plate_support_contraction_schema_sweep_blueprint.md
../03_candidate_discovery/01_001_plate_support_candidate_discovery_blueprint.md
```

## Stage Identity

```text
SUITE_ID = "plate_support_standard_gauntlet_v001"
STAGE_ID = "plate_support_gauntlet_tower_training_health_v001"
ENVIRONMENT_FAMILY_ID = "plate_support"
ENVIRONMENT_INSTANCE_ID = "plate_support_5x5_default_v001"
LINEARIZATION_MODE_ID = "tensor_available_disabled"
```

Recommended readout surface:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/tower_training_health/
```

Recommended artifact root pattern:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/<run-label>/stages/tower_training_health/
```

## Purpose

This stage tests whether selected PlateSupport tower/schema candidates can
support real tower-only training mechanics.

It should answer:

- can the selected tower runtime reset and step repeatedly;
- do tower-selected actions resolve into concrete PlateSupport transitions;
- does the controller/tier machinery have nonempty executable surfaces;
- do learner updates occur;
- does learner state persist across episodes;
- do artifacts capture lift/action realization, tier movement, concrete steps,
  rewards, and training-health classification.

This stage is explicitly not a flat-versus-tower comparison. It is a health
diagnostic that determines whether candidates can safely proceed toward
comparison.

## Dependency On Stage 3

Stage 4 may run only if Stage 3 emits:

```text
candidate_manifest.json
results/selected_candidate_summary.csv
results/downstream_training_health_input_summary.csv
```

Stage 4 should consume only candidates with:

```text
candidate_role in ("selected_training_candidate", "selected_warning_candidate")
```

Warning candidates require explicit budget-lock acknowledgement:

```text
warning_candidate_training_authorized = true
```

unless the Project Owner decides otherwise.

## Training Surface Choice

PlateSupport upstream exposes:

- `PlateSupportEnvRuntime`;
- `PlateSupportExploitExploreRuntime`;
- `PlateSupportLiftResolveExecutor`;
- `PlateSupportTierLearner`;
- `TowerTrainingConfig`;
- `ExploitExploreTrainingConfig`;
- `run_tower_training`;
- `run_exploit_explore_training`.

The Stage 4 design should decide whether to:

1. call upstream `run_tower_training` / `run_exploit_explore_training` and wrap
   their outputs into BBB artifacts;
2. build a BBB-side runner using upstream runtime classes directly;
3. use a hybrid approach.

Consultant recommendation:

- use BBB-side runner control if possible, because BBB needs uniform artifact
  tables and detailed event rows;
- call upstream helper training functions only if they expose enough structured
  hooks for event capture;
- stop if upstream functions return only opaque summaries.

## Candidate Training Budget

Recommended first smoke/dev budget:

```text
candidate_cap = 2
training_replicates_per_candidate = 2
episodes_per_replicate = 16
max_steps_per_episode = 50
base_seed = 0
epsilon = upstream default unless explicitly overridden
alpha = upstream default unless explicitly overridden
gamma = upstream default unless explicitly overridden
```

Why `16` episodes:

- counterpoint showed that too-short episode budgets can make downstream
  success criteria impossible to interpret;
- PlateSupport has max steps `50` and random policy success about `0.024`, so
  a tiny one-to-four episode smoke is likely too weak to reveal training health.

This is still not a serious performance budget.

## Required Inputs

```text
candidate_manifest.json
selected_candidate_summary.csv
candidate_source_trace.csv
schema_construction_manifest.json
Stage 1 graph/action/reward facts
Stage 2 tower shape/executability tables
```

Input manifests must record:

- selected candidate IDs;
- schema IDs and schema construction metadata;
- source artifact roots;
- candidate role and eligibility class;
- whether warning candidates are authorized.

## Required Runtime Event Domains

### Episode Rows

Fields:

```text
candidate_id
schema_id
seed_bundle_id
training_replicate_index
episode_index
total_reward
step_count
terminated
truncated
goal_reached
invalid_move_count
valid_self_transition_count
concrete_step_count
learner_update_count
```

### Concrete Step Events

Fields:

```text
candidate_id
run_id
episode_index
step_index
base_state_before
selected_tier
selected_action_cell
resolved_action_index
resolved_action_label
candidate_state_id
next_state_id
reward
terminated
truncated
invalid_move
valid_self_transition
lift_success
fallback_reason
```

### Lift / Action-Realization Events

Fields:

```text
candidate_id
run_id
episode_index
step_index
active_tier
abstract_action_id
base_state_id
candidate_lift_count
executable_lift_count
selected_lift_state_id
selected_concrete_action_index
lift_success
failure_reason
fiber_departure_reason
```

### Tier / Controller Events

Fields:

```text
candidate_id
run_id
episode_index
step_index
active_tier_before
active_tier_after
control_action
tier_executable_before
tier_executable_after
active_action_cell_count
blocked_reason
```

### Learner Update Events

Fields:

```text
candidate_id
run_id
episode_index
step_index
learner_id
selected_state_key
selected_action_key
reward
next_state_key
td_error
old_value
new_value
update_applied
```

If upstream learner surfaces cannot expose all fields, Stage 4 should document
which fields are unavailable and should not fake values.

## Required Outputs

### Manifests

```text
stage_manifest.json
stage_budget_lock.json
stage_input_manifest.json
candidate_manifest.json
training_config_manifest.json
training_surface_manifest.json
parent_candidate_manifest.json
```

### Event Tables

```text
runs/<run-id>/episodes.csv
runs/<run-id>/concrete_step_events.csv
runs/<run-id>/lift_fiber_events.csv
runs/<run-id>/tier_transition_events.csv
runs/<run-id>/controller_action_events.csv
runs/<run-id>/learner_update_events.csv
runs/<run-id>/timing_segments.csv
```

### Aggregate Tables

```text
results/training_episode_summary.csv
results/training_curve_summary.csv
results/concrete_step_summary.csv
results/lift_success_by_tier.csv
results/lift_failure_by_tier.csv
results/tier_occupancy_summary.csv
results/tier_executability_summary.csv
results/controller_action_summary.csv
results/learner_update_summary.csv
results/training_health_summary.csv
results/candidate_training_health_summary.csv
results/downstream_comparison_input_summary.csv
```

### Summary

```text
stage_aggregate_summary.json
stage_aggregate_table.csv
stage_run_index.csv
readout_source.json
artifact_index.md
```

## Training Health Classes

Recommended classes:

```text
trainable_clean
trainable_warning
untrainable_no_concrete_steps
untrainable_no_lift_success
untrainable_no_learner_updates
untrainable_runtime_failure
artifact_incomplete
```

### Trainable Clean

Criteria:

- all planned runs completed;
- concrete steps > 0;
- successful lift/action realization > 0;
- learner updates > 0;
- at least one nonzero reward or meaningful reward-gradient event if available;
- no dominant runtime fallback;
- artifacts complete.

### Trainable Warning

Criteria:

- runs completed;
- concrete steps and learner updates exist;
- but there are concerns such as sparse lift success, very low reward signal,
  excessive self-looping, or tier starvation.

### Untrainable

Criteria:

- no concrete steps;
- no lift success;
- no learner updates;
- runtime failure;
- artifacts incomplete.

## Downstream Gate

Stage 6 paired comparison may consider a candidate only if Stage 4 marks it:

```text
trainable_clean
```

or:

```text
trainable_warning
```

with explicit Project Owner authorization.

Stage 5 threshold calibration may use Stage 4 reward/episode traces to choose
thresholds, but Stage 5 must keep calibration separate from comparison.

## Pass / Warning / Block Criteria

### Pass

Stage 4 passes if:

- at least one selected candidate completes the budget;
- at least one candidate is `trainable_clean`;
- all required event and aggregate tables are written;
- source candidate traces are preserved.

### Warning

Stage 4 warns if:

- only warning candidates are trainable;
- learner updates occur but reward signal is extremely sparse;
- lift failures are frequent but not dominant;
- training behavior is dominated by valid self-transitions;
- candidate count is lower than planned.

### Block

Stage 4 blocks if:

- Stage 3 candidate manifest is missing;
- no eligible candidates exist;
- upstream training surfaces are unavailable;
- no concrete steps occur;
- no lift/action realization succeeds;
- no learner updates can be observed or recorded;
- event capture would require inventing unavailable upstream data.

## Stage Claim Boundary

Allowed claims:

- candidate tower training mechanics are healthy or unhealthy;
- selected candidates can or cannot proceed to comparison;
- runtime and artifact surfaces support or block training diagnostics.

Blocked claims:

- tower beats no-contraction;
- reward threshold is calibrated;
- PlateSupport is solved;
- candidate trainability equals performance improvement.

## Relationship To Counterpoint

Inherited lessons:

- tower-only training-health is distinct from comparison;
- concrete steps, lift success, tier traces, and learner updates are all needed;
- candidate provenance must remain visible;
- persistent learner state across episodes matters.

Not inherited:

- counterpoint active-tier controller assumptions unless upstream PlateSupport
  runtime supports the same semantics;
- counterpoint reward thresholds;
- counterpoint candidate source IDs.

## Open Questions For Project Owner

### Question 1: Use Upstream Training Helpers Or BBB-Controlled Runner?

Consultant recommendation: prefer BBB-controlled runner if upstream helpers do
not expose detailed event hooks.

Project Owner response:

```text
TODO
```

### Question 2: First Health Budget

Consultant recommendation:

```text
training_replicates_per_candidate = 2
episodes_per_replicate = 16
max_steps_per_episode = 50
```

Project Owner response:

```text
TODO
```

### Question 3: Warning Candidate Training

Consultant recommendation: default to no warning-candidate training unless no
clean candidates exist and the budget lock explicitly records why.

Project Owner response:

```text
TODO
```

## Expected Next Blueprint

The next component blueprint should be:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/05_threshold_frontier_calibration/01_001_plate_support_threshold_frontier_calibration_blueprint.md
```

It should consume Stage 1 reward/structural facts and Stage 4 training traces
to design a PlateSupport-specific comparison target.
