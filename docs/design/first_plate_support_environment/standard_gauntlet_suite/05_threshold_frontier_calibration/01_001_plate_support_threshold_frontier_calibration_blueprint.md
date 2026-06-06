# PlateSupport Threshold Frontier Calibration Blueprint

## Status

Status: initial child-stage blueprint.

This is a design blueprint for Stage 5 of the PlateSupport standard gauntlet
suite. It is not an implementation workplan and not execution approval.

Depends on:

```text
../00_suite_architecture/01_001_plate_support_standard_gauntlet_suite_architecture_blueprint.md
../01_structural_and_tower_diagnostics/01_001_plate_support_structural_and_tower_diagnostics_blueprint.md
../04_tower_training_health/01_001_plate_support_tower_training_health_blueprint.md
```

Stage 5 may also consume Stage 3 candidate metadata and Stage 2 schema metadata
for provenance, but it should not select candidates. Candidate selection belongs
to Stage 3.

## Stage Identity

```text
SUITE_ID = "plate_support_standard_gauntlet_v001"
STAGE_ID = "plate_support_gauntlet_threshold_frontier_calibration_v001"
ENVIRONMENT_FAMILY_ID = "plate_support"
ENVIRONMENT_INSTANCE_ID = "plate_support_5x5_default_v001"
LINEARIZATION_MODE_ID = "tensor_available_disabled"
```

Recommended readout surface:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/threshold_frontier_calibration/
```

Recommended artifact root pattern:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/<run-label>/stages/threshold_frontier_calibration/
```

## Purpose

This stage calibrates the success or reward target that Stage 6 paired
comparison will use.

Counterpoint taught that the threshold stage is easy to get wrong: a threshold
can be too easy, too hard, too close to noise, or impossible under the selected
episode/window budget. PlateSupport has its own reward scale, terminal behavior,
max-step horizon, and random policy baseline. Therefore it needs a
PlateSupport-specific calibration stage.

## PlateSupport Reward Context

Known from readiness:

- max steps per episode: `50`;
- shortest valid start-goal path length: `6`;
- random policy success rate: about `0.024`;
- random policy mean reward: about `-105.748`;
- invalid move rate: about `0.452`;
- invalid/self-loop pressure is significant.

Known upstream reward contract from environment docs:

- goal-reaching behavior terminates;
- invalid self-loops and valid clipped self-transitions must be distinguished;
- reward is a benchmark control signal, not a robotics-quality proof.

The calibration stage must inspect actual episode traces before choosing a
threshold. It must not assume the counterpoint `12.0` / `13.0` style threshold
logic applies.

## Candidate Target Types

Stage 5 should evaluate several target styles before recommending one.

### Target Type A: Binary Success

Definition:

```text
goal_reached == true
```

Pros:

- human-readable;
- directly tied to task completion;
- avoids reward-scale ambiguity.

Cons:

- may be too sparse under small budgets;
- may not show partial learning progress;
- may require more episodes than a smoke/dev budget.

### Target Type B: First Hit Episode

Definition:

```text
first episode index where goal_reached == true
```

Pros:

- natural robotics/control metric;
- maps to "learns to solve eventually";
- useful if success events are sparse but present.

Cons:

- censored if no hit occurs;
- requires enough episodes to interpret.

### Target Type C: Sustained Hit Window

Definition:

```text
goal_reached in at least K of the last W episodes
```

Pros:

- closer to reliability than one lucky hit;
- can support comparison claims if budget is long enough.

Cons:

- counterpoint showed this can be impossible if episodes per replicate < W;
- likely requires a larger budget for PlateSupport.

### Target Type D: Return Threshold

Definition:

```text
episode_total_reward >= R
```

Pros:

- can detect partial improvement before terminal success;
- useful when success is sparse.

Cons:

- reward scale must be understood;
- invalid/self-loop penalties may dominate;
- threshold can be arbitrary if not calibrated.

### Target Type E: Step-Efficiency Conditional On Success

Definition:

```text
goal_reached == true and step_count <= S
```

Pros:

- connected to "speed-up" in a concrete sense;
- shortest path is known to be length `6`.

Cons:

- too strict early;
- depends on enough successes.

### Target Type F: Composite Progress Score

Definition:

```text
weighted combination of reward, invalid-move reduction, distance-to-goal proxy,
and success
```

Pros:

- can show progress in sparse-success regimes.

Cons:

- risks becoming opaque;
- requires careful human explanation;
- should not be used for first comparison unless simpler targets fail.

Consultant recommendation:

- prefer binary success / first-hit metrics first;
- use sustained-hit only when the episode budget makes it feasible;
- use return threshold as a secondary calibration view;
- avoid composite score for first serious comparison unless PO explicitly wants
  a progress proxy.

## Calibration Inputs

Required Stage 1 inputs:

```text
shortest_path_summary.csv
random_policy_recon_summary.csv
state_space_summary.csv
transition_summary.csv
```

Required Stage 4 inputs:

```text
training_episode_summary.csv
training_curve_summary.csv
concrete_step_summary.csv
candidate_training_health_summary.csv
```

Optional direct/flat baseline calibration input:

- A no-contraction or direct-environment calibration run may be needed if Stage
  6 baseline behavior is not represented in Stage 4.

Important: Stage 5 may need a small direct/no-contraction calibration arm even
though Stage 4 is tower-only. If so, it must be labeled calibration, not
comparison.

## Calibration Design

Recommended first calibration matrix:

```text
arms:
  - direct_or_no_contraction_baseline_calibration
  - selected_trainable_candidate_calibration

candidate_cap: 1 or 2
replicates_per_arm: 3
episodes_per_replicate: 32
max_steps_per_episode: 50
base_seed: 0
paired_seed_policy: true
```

Why `32` episodes:

- long enough to observe first-hit or sustained-window candidates;
- still far smaller than a final serious budget;
- avoids the counterpoint four-episode impossibility problem.

This budget is a consultant recommendation, not a PO decision.

## Threshold Frontier Sweep

If using return thresholds, Stage 5 should sweep a small grid derived from
observed distributions, not from hard-coded guesses.

Example construction:

1. run calibration traces;
2. collect episode total reward distributions by arm;
3. compute candidate threshold grid from quantiles:
   - baseline median;
   - baseline 75th percentile;
   - candidate median;
   - candidate 75th percentile;
   - known random-policy mean plus offsets;
4. write the exact grid to the budget lock;
5. evaluate first-hit or sustained-hit feasibility per threshold.

Required table:

```text
results/threshold_grid_construction.csv
```

Fields:

```text
threshold_id
threshold_value
source_metric
source_arm
source_quantile
construction_reason
```

## Required Outputs

### Manifests

```text
stage_manifest.json
stage_budget_lock.json
stage_input_manifest.json
threshold_policy_manifest.json
calibration_arm_manifest.json
parent_training_health_manifest.json
```

### Tables

```text
results/calibration_episode_summary.csv
results/calibration_arm_summary.csv
results/success_rate_summary.csv
results/first_hit_summary.csv
results/sustained_hit_feasibility_summary.csv
results/return_distribution_summary.csv
results/threshold_grid_construction.csv
results/threshold_frontier_summary.csv
results/recommended_comparison_target.csv
results/downstream_paired_comparison_input_summary.csv
```

### Summary

```text
stage_aggregate_summary.json
stage_aggregate_table.csv
stage_run_index.csv
readout_source.json
artifact_index.md
```

## Recommended Comparison Target Table

The decisive output is:

```text
results/recommended_comparison_target.csv
```

Recommended fields:

```text
target_policy_id
target_type
threshold_value
window_length
required_count
episodes_required_minimum
recommended_episodes_per_replicate
recommended_replicates_per_arm
baseline_feasibility
candidate_feasibility
calibration_status
claim_boundary
reason
```

If no target is calibrated, Stage 6 must not proceed.

## Feasibility Rules

### Binary Success

Feasible if:

- at least one arm has nonzero success in calibration;
- episode count is enough to observe variation;
- success events are not all single lucky outliers unless the target is first
  hit.

### Sustained Hit

Feasible only if:

```text
episodes_per_replicate >= window_length
```

and preferably:

```text
episodes_per_replicate >= 2 * window_length
```

Counterpoint failure mode to avoid:

- a 4-of-5 rule with only 4 episodes.

### Return Threshold

Feasible if:

- reward distributions differ enough to place a threshold with interpretive
  meaning;
- threshold is not simply "above all observed values" or "below all observed
  values";
- invalid/self-loop effects are documented.

## Pass / Warning / Block Criteria

### Pass

Stage 5 passes if:

- calibration traces complete;
- at least one target policy is feasible;
- recommended comparison target is written;
- recommended budget is compatible with the target;
- Stage 6 input summary is complete.

### Warning

Stage 5 warns if:

- success is too sparse and only return-threshold targets are feasible;
- target is feasible only at a larger-than-smoke budget;
- calibration distinguishes arms weakly;
- candidate behavior is trainable but reward signal remains noisy.

### Block

Stage 5 blocks if:

- Stage 4 training-health source is missing;
- no trainable candidate exists;
- no feasible target can be calibrated;
- proposed sustained-window rule is impossible under budget;
- target construction cannot be explained in human-readable terms.

## Stage Claim Boundary

Allowed claims:

- a PlateSupport comparison target is calibrated or unresolved;
- a recommended Stage 6 budget exists or is blocked;
- specific threshold/target choices are justified by calibration artifacts.

Blocked claims:

- tower beats no-contraction;
- candidate is superior;
- calibrated threshold is a final benchmark standard for all PlateSupport
  variants;
- reward threshold alone proves robotics quality.

## Relationship To Counterpoint

Inherited lessons:

- threshold/frontier calibration is necessary before paired comparison;
- sustained windows must be budget-feasible;
- readouts must explain why a threshold is chosen;
- smoke thresholds do not support serious claims.

Not inherited:

- counterpoint threshold values;
- counterpoint reward scale;
- counterpoint 4-of-5 rule as a default;
- counterpoint `wide_span18` candidate assumptions.

## Open Questions For Project Owner

These are consultant-authored open questions, not Project Owner statements.

### Question 1: Preferred Target Style

Consultant recommendation: prioritize `binary_success` and `first_hit`, then
use return thresholds as support. Use sustained-hit only if the budget is long
enough.

Resolution status:

```text
Pending Project Owner answer.
```

### Question 2: Calibration Budget

Consultant recommendation:

```text
replicates_per_arm = 3
episodes_per_replicate = 32
max_steps_per_episode = 50
```

Resolution status:

```text
Pending Project Owner answer.
```

### Question 3: Include Direct Baseline Calibration?

Consultant recommendation: yes. Stage 5 needs baseline calibration evidence if
Stage 6 will compare against a baseline.

Resolution status:

```text
Pending Project Owner answer.
```

## Expected Next Blueprint

The next component blueprint should be:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/06_paired_replicate_comparison/01_001_plate_support_paired_replicate_comparison_blueprint.md
```

It should consume `recommended_comparison_target.csv`,
`downstream_paired_comparison_input_summary.csv`, and Stage 3/4 candidate
artifacts.
