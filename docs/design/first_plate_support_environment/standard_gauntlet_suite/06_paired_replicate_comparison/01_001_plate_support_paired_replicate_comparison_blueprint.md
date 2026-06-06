# Plate Support Paired Replicate Comparison Blueprint

## Document Status

This is the initial blueprint for the paired replicate comparison component of the
PlateSupport standard gauntlet suite.

This document follows the ordering established in:

- `docs/design/first_plate_support_environment/standard_gauntlet_suite/00_suite_architecture/01_001_plate_support_standard_gauntlet_suite_architecture_blueprint.md`
- `docs/design/first_plate_support_environment/standard_gauntlet_suite/01_structural_and_tower_diagnostics/01_001_plate_support_structural_and_tower_diagnostics_blueprint.md`
- `docs/design/first_plate_support_environment/standard_gauntlet_suite/02_contraction_schema_sweep/01_001_plate_support_contraction_schema_sweep_blueprint.md`
- `docs/design/first_plate_support_environment/standard_gauntlet_suite/03_candidate_discovery/01_001_plate_support_candidate_discovery_blueprint.md`
- `docs/design/first_plate_support_environment/standard_gauntlet_suite/04_tower_training_health/01_001_plate_support_tower_training_health_blueprint.md`
- `docs/design/first_plate_support_environment/standard_gauntlet_suite/05_threshold_frontier_calibration/01_001_plate_support_threshold_frontier_calibration_blueprint.md`

It is intentionally written after the threshold-frontier calibration blueprint
because this stage must not invent its own success threshold. The comparison
stage consumes the target selected by Stage 5.

## Stage Identity

Recommended stage id:

`plate_support_gauntlet_paired_replicate_comparison_v001`

Recommended suite id:

`plate_support_standard_gauntlet_v001`

Recommended environment family id:

`plate_support`

Recommended environment instance id:

`plate_support_5x5_default_v001`

Recommended readout location:

`docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/`

Recommended raw artifact location:

`docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/<run-label>/`

Recommended stage artifact location inside a run label:

`docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/<run-label>/evaluations/plate_support_gauntlet_paired_replicate_comparison_v001/`

## Purpose

This stage is the first claim-bearing comparison stage in the PlateSupport
standard gauntlet.

The purpose is to compare one or more selected tower/schema candidates against a
baseline under paired seeds, fixed budget, fixed environment instance, and the
target policy selected by threshold calibration.

The intended question is narrow:

Does a selected PlateSupport tower/schema arm show a measurable advantage over
the selected baseline on the calibrated target, under the current small
gauntlet budget?

This stage is not intended to answer whether tower learning is generally better
than direct learning, whether a schema family is globally best, or whether
PlateSupport has been solved.

## Why This Stage Comes After Stage 5

The counterpoint sequence showed that comparison claims become confusing when
the target threshold is guessed after the fact or adjusted interactively without
clear provenance.

For PlateSupport, the stage ordering is:

1. Stage 1 establishes the environment and tower surfaces are structurally
   usable.
2. Stage 2 discovers which schema families produce meaningful non-collapsed
   towers.
3. Stage 3 selects candidate schemas without making performance claims.
4. Stage 4 verifies that selected candidates can actually train.
5. Stage 5 calibrates a target threshold/frontier from observed behavior.
6. Stage 6 compares baseline and tower arms against that calibrated target.

Stage 6 therefore must treat the Stage 5 recommended target as an input, not as
a free parameter.

## Prior Work This Blueprint Uses

This blueprint reuses the following counterpoint lessons without copying
counterpoint answers directly:

- The second serious schema comparison taught us to use paired seed bundles
  and to keep schema comparisons narrow.
- The small paired replicate probe taught us that very tiny margins can still
  be meaningful as early evidence, but the readout must say when the evidence is
  small.
- The threshold frontier probe taught us that threshold choice is part of the
  experimental design, not a thing to bury in prose.
- The noisy-rate full tower training diagnostic taught us that comparison should
  only be run after tower training health is known.
- The pointwise liftability handoff taught us that lift failures and executable
  action surfaces must remain visible in comparison readouts, because apparent
  learning failures can be runtime/liftability failures.

PlateSupport adds its own facts from the environment readiness work:

- candidate state count: 2700
- valid state count: 89
- all 89 valid states are reachable
- primitive action count: 12
- valid non-self edge count: 388
- invalid primitive move count: 496
- valid clipped self-transition count: 184
- shortest start-goal path length: 6
- random-policy success rate: about 0.024 in the recorded readiness smoke
- random-policy mean reward: about -105.748 in the recorded readiness smoke
- random-policy invalid move rate: about 0.452 in the recorded readiness smoke

Those facts imply that PlateSupport has a much stronger baseline difficulty
profile than the tiny counterpoint threshold margin that motivated this new
environment direction.

## Required Inputs

### Architecture Inputs

The stage must consume the suite architecture contract:

- suite id
- stage id
- environment family id
- environment instance id
- artifact root
- run label
- dependency manifest policy
- readout-source policy
- stage status vocabulary
- claim status vocabulary

### Stage 1 Inputs

From structural and tower diagnostics:

- environment identity summary
- state-space summary
- action table
- transition summary
- shortest path summary
- validity predicate summary
- geometry summary
- random-policy reconnaissance summary
- tower-shape summary for no-contraction/default control surfaces
- training-surface availability summary
- downstream readiness status

The comparison stage must include enough Stage 1 metadata to let a reader
understand the task difficulty without opening the readiness document.

### Stage 3 Inputs

From candidate discovery:

- `candidate_manifest.json`
- `selected_candidate_summary.csv`
- `candidate_eligibility_summary.csv`
- `blocked_candidate_summary.csv`
- `control_anchor_summary.csv`
- `candidate_source_trace.csv`
- `downstream_training_health_input_summary.csv`

Stage 6 must not select candidates directly from Stage 2 tables if Stage 3
exists. If the candidate manifest is missing, Stage 6 blocks.

### Stage 4 Inputs

From tower training health:

- `candidate_training_health_summary.csv`
- `training_health_summary.csv`
- `training_curve_summary.csv`
- `lift_success_by_tier.csv`
- `lift_failure_by_tier.csv`
- `tier_occupancy_summary.csv`
- `tier_executability_summary.csv`
- `downstream_comparison_input_summary.csv`

Stage 6 may only compare candidates that Stage 4 classified as:

- `trainable_clean`
- `trainable_warning`, if the warning was explicitly authorized for comparison

Candidates classified as untrainable must be carried into the readout as blocked
candidate context, not silently omitted.

### Stage 5 Inputs

From threshold frontier calibration:

- `recommended_comparison_target.csv`
- `threshold_frontier_summary.csv`
- `threshold_grid_construction.csv`
- `success_rate_summary.csv`
- `first_hit_summary.csv`
- `return_distribution_summary.csv`
- `downstream_paired_comparison_input_summary.csv`

Stage 6 must use the recommended comparison target unless the Project Owner
explicitly overrides it in the design/workplan.

If Stage 5 reports no feasible target, Stage 6 must block.

## Comparison Arms

### Required Arm Categories

Stage 6 should distinguish three possible arm categories:

1. Direct or flat baseline arm.
2. No-contraction tower-control arm.
3. Selected tower/schema candidate arm.

The exact baseline definition is a design-sensitive issue because PlateSupport
can plausibly compare against either direct concrete training or a no-contraction
tower wrapper. The stage must make this explicit.

### Arm A: Direct Concrete Baseline

Recommended arm id:

`plate_support_direct_concrete_baseline`

Meaning:

Train directly on the concrete PlateSupport environment without a contracted
tower controller.

This is the cleanest human-facing baseline if the claim is "does the tower help
training on this task?"

Required metadata:

- environment instance id
- no schema id
- learner configuration
- seed bundle
- max steps
- episode budget
- reward/target policy
- dependency manifest

### Arm B: No-Contraction Tower Control

Recommended arm id:

`plate_support_no_contraction_tower_control`

Meaning:

Train through the same tower/controller machinery, but with a no-contraction
schema that should behave like the concrete space in tower form.

This is the cleanest engineering baseline if the claim is "does contraction,
not merely the tower runner, explain the difference?"

Required metadata:

- no-contraction schema id
- tower depth
- scheduled assignment count
- effective action surface
- learner configuration
- seed bundle
- max steps
- episode budget
- reward/target policy
- dependency manifest

### Arm C: Selected Tower Candidate

Recommended arm id pattern:

`plate_support_selected_tower_candidate:<candidate_id>`

Meaning:

Train through the selected contracted tower/schema candidate from Stage 3,
provided Stage 4 marked it trainable and Stage 5 supplied a calibrated target.

Required metadata:

- candidate id
- schema id
- schema family id
- schema seed
- source sweep row id
- training-health status
- tower shape
- executable tier summary
- learner configuration
- seed bundle
- max steps
- episode budget
- reward/target policy
- dependency manifest

## Recommended Initial Arm Policy

For the first PlateSupport gauntlet implementation, the safest default is:

- include Arm A if the direct training surface is available
- include Arm B if the no-contraction tower-control surface is available
- include one selected tower candidate by default
- allow two selected tower candidates only if Stage 3 produced two clean,
  distinct candidates and Stage 4 training health is clean for both

The readout should present Arm A and Arm B separately. If they behave similarly,
that strengthens interpretation. If they diverge, the suite has learned
something important about runner/controller overhead before making a contraction
claim.

## Pairing Discipline

### Paired Seed Bundles

Every comparison unit must use a paired seed bundle. For each replicate index,
all arms should share:

- environment seed
- learner seed
- exploration seed
- schema/tower selection seed, when applicable
- initial-state seed, if initial states ever become stochastic
- tie-break seed

PlateSupport currently appears to use a fixed start state, but the seed bundle
should still record the initial-state seed as a forward-compatible field.

### Pair Unit

A pair unit should be:

`(replicate_id, seed_bundle_id, candidate_group_id, target_policy_id)`

For each pair unit, all active arms should run the same number of episodes and
the same maximum steps per episode.

### Missing Pair Policy

If one arm fails for a pair unit, that pair unit must be marked incomplete and
excluded from paired-delta calculations, while still appearing in artifact and
failure tables.

The readout must report:

- total requested pair units
- complete pair units
- incomplete pair units
- incomplete reason counts

## Budget Recommendation

The Stage 5 recommended comparison target should carry a recommended budget.

If Stage 5 does not yet provide one, a conservative development default is:

- selected tower candidates: 1
- baselines: direct concrete plus no-contraction tower if both are available
- replicates per arm: 5
- episodes per replicate: 32
- max steps per episode: 50
- paired seeds: true

For a smoke workplan, a smaller run is acceptable:

- selected tower candidates: 1
- baselines: direct concrete or no-contraction tower, whichever is implemented
  first
- replicates per arm: 2
- episodes per replicate: 8
- max steps per episode: 50
- paired seeds: true

The smoke run must be labeled as smoke and must not be presented as a serious
comparison result.

## Target Policy

Stage 6 must load the target policy selected by Stage 5.

Allowed target types:

- binary success target
- first-hit target
- sustained-hit target
- return-threshold target
- step-efficiency target

Recommended first target:

Use the Stage 5 recommendation. If no Stage 5 recommendation exists yet, block.

Target policy manifest should include:

- target policy id
- target type
- threshold value, if any
- sustained window length, if any
- required count, if any
- first-hit semantics, if any
- whether lower or higher is better
- source Stage 5 artifact path
- PO override field, if any

## Learner and Runtime Policy

### Learner Consistency

The same learner class and core hyperparameters should be used across arms
unless the comparison explicitly says otherwise.

Required learner fields:

- learner id
- learning rate
- discount factor
- exploration policy
- exploration schedule
- initialization policy
- update rule
- max steps
- episode budget

### Tower Controller Consistency

For tower arms, the same tower-controller policy should be used across selected
candidate and no-contraction tower-control arms unless the comparison explicitly
says otherwise.

Required controller fields:

- controller id
- tier selection policy
- lift policy
- pointwise liftability semantics version
- fallback policy for failed lift
- action masking policy
- tie-break policy

### State Collapser Version

The stage must record the `state_collapser` version and the BBB dependency
manifest.

The default for new reruns should be `state_collapser` v0.7.2 or newer, because
the pointwise liftability correction is part of the required semantics for
credible tower comparison.

If an older version is used, the stage must mark the comparison as blocked or
legacy-only.

## Required Artifacts

### Root Stage Artifacts

The stage artifact directory should include:

- `evaluation_manifest.json`
- `evaluation_stage_manifest.json`
- `evaluation_budget_lock.json`
- `environment_source_manifest.json`
- `candidate_source_manifest.json`
- `training_health_source_manifest.json`
- `threshold_policy_manifest.json`
- `comparison_arm_manifest.json`
- `paired_seed_bundle_manifest.json`
- `evaluation_run_index.csv`
- `readout_source.json`

### Per-Run Artifacts

Each arm run should include:

- `run_manifest.json`
- `environment_instance_manifest.json`
- `dependency_manifest.json`
- `mode_manifest.json`
- `schema_manifest.json`, for tower/schema arms
- `schema_construction.json`, for tower/schema arms
- `quotient_summary.json`, for tower/schema arms
- `tower_shape_summary.csv`, for tower/schema arms
- `tower_invariant_report.json`, for tower/schema arms
- `seed_bundle.json`
- `episodes.csv`
- `step_events.csv`
- `control_events.csv`, if a controller is active
- `tier_transition_events.csv`, if a tower is active
- `lift_fiber_events.csv`, if a tower is active
- `learner_update_events.csv`
- `threshold_window_events.csv`, if the target uses a window
- `first_hit_summary.json`
- `first_sustained_hit_summary.csv`, if relevant
- `timing_segments.csv`
- `timing_summary.json`
- `warnings.jsonl`

## Required Result Tables

### Run and Pair Index Tables

`results/comparison_run_index.csv`

One row per concrete run.

Required columns:

- suite_id
- stage_id
- run_label
- pair_unit_id
- replicate_id
- arm_id
- arm_kind
- candidate_id
- schema_id
- schema_family_id
- target_policy_id
- seed_bundle_id
- episodes_requested
- episodes_completed
- max_steps_per_episode
- status
- artifact_path

`results/paired_unit_summary.csv`

One row per pair unit.

Required columns:

- pair_unit_id
- replicate_id
- target_policy_id
- candidate_group_id
- arms_requested
- arms_completed
- complete_pair
- incomplete_reason
- baseline_arm_id
- tower_arm_id

### Arm Summary Tables

`results/arm_summary.csv`

One row per arm.

Required columns:

- arm_id
- arm_kind
- candidate_id
- schema_id
- run_count
- complete_run_count
- episode_count
- success_rate
- mean_return
- median_return
- mean_steps_to_success
- mean_invalid_move_rate
- mean_target_hit_rate
- first_hit_episode_mean
- first_hit_episode_median
- status

`results/baseline_summary.csv`

One row per baseline arm.

Required columns:

- baseline_arm_id
- baseline_kind
- available
- selected_as_primary_baseline
- reason
- success_rate
- mean_return
- target_hit_rate
- first_hit_episode_median

`results/candidate_comparison_arm_summary.csv`

One row per selected candidate arm.

Required columns:

- candidate_id
- schema_id
- schema_family_id
- training_health_status
- comparison_arm_id
- success_rate
- mean_return
- target_hit_rate
- first_hit_episode_median
- lift_failure_rate
- tier_occupancy_status
- status

### Primary Comparison Tables

`results/paired_schema_comparison.csv`

One row per paired baseline/candidate comparison.

Required columns:

- pair_unit_id
- baseline_arm_id
- candidate_arm_id
- target_policy_id
- baseline_target_hit
- candidate_target_hit
- target_hit_delta
- baseline_success_rate
- candidate_success_rate
- success_rate_delta
- baseline_mean_return
- candidate_mean_return
- return_delta
- baseline_first_hit_episode
- candidate_first_hit_episode
- first_hit_delta
- complete_pair
- excluded_from_primary_delta
- exclusion_reason

`results/comparison_claim_summary.csv`

One row per comparison claim candidate.

Required columns:

- claim_id
- baseline_arm_id
- candidate_arm_id
- target_policy_id
- primary_metric
- primary_delta
- primary_direction
- complete_pair_count
- total_pair_count
- evidence_class
- claim_status
- claim_sentence
- caveat_sentence

Evidence classes:

- `positive_signal`
- `negative_signal`
- `mixed_signal`
- `inconclusive`
- `blocked`

Claim statuses:

- `claim_ready`
- `claim_limited`
- `claim_inconclusive`
- `claim_blocked`

### Target and Learning Tables

`results/target_hit_summary.csv`

Required columns:

- arm_id
- target_policy_id
- target_type
- threshold_value
- episode_count
- target_hit_count
- target_hit_rate
- first_target_hit_episode
- sustained_target_hit
- status

`results/success_rate_summary.csv`

Required columns:

- arm_id
- success_count
- episode_count
- success_rate
- baseline_delta
- candidate_delta
- status

`results/first_hit_summary.csv`

Required columns:

- arm_id
- first_success_episode
- first_target_hit_episode
- first_sustained_hit_episode
- median_first_hit_episode
- censored_replicate_count
- status

`results/reward_distribution_summary.csv`

Required columns:

- arm_id
- episode_count
- mean_return
- median_return
- min_return
- max_return
- p25_return
- p75_return
- status

`results/step_efficiency_summary.csv`

Required columns:

- arm_id
- success_episode_count
- mean_steps_to_success
- median_steps_to_success
- shortest_path_length
- excess_steps_over_shortest_path_mean
- status

`results/invalid_move_summary.csv`

Required columns:

- arm_id
- total_steps
- invalid_move_count
- invalid_move_rate
- clipped_self_transition_count
- clipped_self_transition_rate
- status

### Tower Runtime Tables

`results/lift_success_by_tier.csv`

Required columns:

- arm_id
- candidate_id
- tier
- lift_attempt_count
- lift_success_count
- lift_success_rate
- executable_action_cell_count
- status

`results/lift_failure_by_tier.csv`

Required columns:

- arm_id
- candidate_id
- tier
- lift_failure_count
- failure_reason
- source_state_count
- executable_source_state_count
- status

`results/tier_occupancy_summary.csv`

Required columns:

- arm_id
- candidate_id
- tier
- visit_count
- action_selection_count
- learner_update_count
- status

`results/training_health_carryforward.csv`

Required columns:

- candidate_id
- stage4_training_health_status
- stage4_artifact_path
- comparison_runtime_status
- mismatch_detected
- mismatch_reason

### Timing and Artifact Tables

`results/timing_summary.csv`

Required columns:

- arm_id
- run_count
- total_wall_time_seconds
- mean_run_wall_time_seconds
- mean_episode_wall_time_seconds
- tower_construction_wall_time_seconds
- training_wall_time_seconds
- summarization_wall_time_seconds

`results/artifact_completeness_summary.csv`

Required columns:

- artifact_group
- expected_count
- observed_count
- missing_count
- complete
- status

## Claim Logic

### Primary Metric

The primary metric must come from Stage 5.

Examples:

- target hit rate
- success rate
- first hit episode
- sustained hit rate
- mean return over calibrated threshold

The comparison stage may compute supporting metrics, but the readout must name
which metric is primary.

### Directionality

Directionality must be explicit:

- for success, target hit, and return: higher is better
- for first hit episode and steps to success: lower is better
- for invalid move rate and lift failure rate: lower is better

### Evidence Classification

`positive_signal`

The selected tower candidate improves the primary metric over the primary
baseline on complete paired units and does not show a severe runtime health
regression.

`negative_signal`

The selected tower candidate performs worse than the baseline on the primary
metric, or the tower runtime introduces enough failures that comparison cannot
support a positive claim.

`mixed_signal`

The selected tower candidate improves one meaningful metric while worsening
another, or direct baseline and no-contraction tower baseline disagree.

`inconclusive`

The result is directionally weak, too small, too incomplete, or too budget-limited
to call.

`blocked`

The stage did not produce enough complete paired units, lacked an eligible
candidate, lacked a calibrated target, or had artifact/runtime failures.

### Claim Sentence Policy

The generated readout should include a short claim sentence with one of these
forms:

- "This run gives a limited positive signal for `<candidate>` over `<baseline>`
  on `<target>`."
- "This run does not give a positive signal for `<candidate>` over `<baseline>`
  on `<target>`."
- "This run is inconclusive because `<reason>`."
- "This comparison is blocked because `<reason>`."

The readout must not use stronger language than the evidence class supports.

## Stop Gates

### Hard Blocks

Stage 6 must block if:

- Stage 3 candidate manifest is missing.
- Stage 4 marks all selected candidates untrainable.
- Stage 5 does not provide a feasible recommended target.
- No baseline arm is available.
- `state_collapser` version is older than the required pointwise-liftability
  semantics unless explicitly marked legacy-only.
- Paired seed generation fails.
- Artifact root is outside the repository evaluation tree.

### Warning Conditions

Stage 6 may continue with warnings if:

- only one baseline arm is available
- a candidate is `trainable_warning` but explicitly authorized
- complete pair count is lower than requested but still enough for smoke
  readout
- direct baseline and no-contraction tower baseline disagree substantially
- lift failures occur but do not dominate training

### Pass Conditions

Stage 6 is complete if:

- all required manifests exist
- all requested arms either ran or have explicit blocked reasons
- paired unit table exists
- primary comparison table exists
- claim summary table exists
- artifact completeness summary exists
- readout source exists
- claim status is one of the allowed statuses

## Readout Requirements

The human-readable readout for this stage must include:

1. What was compared.
2. Which target was used and where it came from.
3. Which baseline is primary.
4. Which candidate was tested.
5. Whether pair units completed.
6. What the primary metric says.
7. What supporting metrics say.
8. Whether runtime/liftability issues affected interpretation.
9. What claim, if any, is allowed.
10. What should happen next.

The readout should be clear enough that a reader does not need to inspect raw
CSV tables to understand the comparison result.

## Badge Requirements

Recommended badges:

- `artifacts_complete`
- `paired_units_complete`
- `target_policy_available`
- `baseline_available`
- `candidate_trainable`
- `primary_claim_status`
- `liftability_semantics`
- `provenance_repo_artifacts`

Badge colors should follow the protocol vocabulary already used for counterpoint
readouts:

- green for pass/positive/complete
- yellow or orange for warning/inconclusive/limited
- red for blocked/failure/negative when appropriate
- gray for not applicable

## Provenance Requirements

Every Stage 6 readout must be able to trace:

- environment readiness source
- Stage 1 structural source
- Stage 2 sweep source
- Stage 3 candidate source
- Stage 4 training-health source
- Stage 5 target source
- dependency versions
- artifact root
- run label
- branch or commit, when available
- PO overrides, if any

## Implementation Notes

### Reuse Existing Counterpoint Machinery Carefully

The counterpoint `second_serious_schema_comparison` implementation is the closest
existing implementation pattern.

Reusable ideas:

- paired seed bundles
- arm manifests
- candidate manifests
- aggregate comparison tables
- threshold policy manifests
- human-readable readout source
- lift success/failure summaries
- claim summary table

Things not to copy blindly:

- counterpoint-specific schema ids
- counterpoint target thresholds
- counterpoint reward interpretation
- counterpoint instance ids
- counterpoint assumption that tiny threshold margins are acceptable as the main
  result

### PlateSupport-Specific Concerns

PlateSupport has invalid moves, clipped transitions, and geometric validity
constraints. The comparison readout must therefore include invalid move and
step-efficiency context.

A tower arm that improves reward only by reducing invalid moves is still
interesting, but the readout should say that this is the apparent mechanism.

A tower arm that reaches the goal faster but has many lift failures needs a
runtime caveat.

## Open Questions For Project Owner

These are consultant-authored open questions, not Project Owner statements.

### Question 1: Primary Baseline

Should the first claim-bearing comparison use direct concrete training as the
primary baseline, no-contraction tower control as the primary baseline, or report
both with one designated primary?

Consultant recommendation:

My recommendation is to report both if implementation cost is reasonable, but
designate direct concrete training as the primary human-facing baseline. The
no-contraction tower control should be an engineering control that tells us
whether any difference is due to contraction rather than the runner/controller
machinery.

### Question 2: First Serious Budget

For the first serious PlateSupport paired comparison, should we use the
development default of 5 replicates per arm and 32 episodes per replicate, or
choose a different budget after Stage 5 calibration?

Consultant recommendation:

My recommendation is to let Stage 5 supply the final budget. If we need a fixed
first implementation default, I would use 5 replicates per arm and 32 episodes
per replicate because PlateSupport random success is low enough that tiny
episode counts are likely to be misleading.

### Question 3: Evidence Threshold

What minimum directional advantage should count as a positive signal in the
first PlateSupport paired comparison?

Consultant recommendation:

My recommendation is not to require statistical strength yet. For the first
gauntlet comparison, use `positive_signal` for a clean directional improvement
on the calibrated primary metric with no severe runtime caveat, and use the
readout language "limited positive signal." Save stronger statistical claims for
later larger-budget evaluations.

## Expected Next Blueprint

The next blueprint should be:

`docs/design/first_plate_support_environment/standard_gauntlet_suite/07_readout_and_system_learning/01_001_plate_support_readout_and_system_learning_blueprint.md`

That blueprint should define how the whole gauntlet becomes readable to humans,
how badges summarize status, how generated readouts preserve turn-taking space,
and how lessons learned from PlateSupport evaluations are archived in durable
design memory.
