# PlateSupport Structural And Tower Diagnostics Blueprint

## Status

Status: initial child-stage blueprint.

This is a design blueprint for Stage 1 of the PlateSupport standard gauntlet
suite. It is not an implementation workplan and not execution approval.

Parent architecture:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/00_suite_architecture/01_001_plate_support_standard_gauntlet_suite_architecture_blueprint.md
```

## Stage Identity

```text
SUITE_ID = "plate_support_standard_gauntlet_v001"
STAGE_ID = "plate_support_gauntlet_structural_tower_diagnostics_v001"
ENVIRONMENT_FAMILY_ID = "plate_support"
ENVIRONMENT_INSTANCE_ID = "plate_support_5x5_default_v001"
LINEARIZATION_MODE_ID = "tensor_available_disabled"
```

Recommended readout surface:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/structural_and_tower_diagnostics/
```

Recommended artifact root pattern:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/<run-label>/stages/structural_and_tower_diagnostics/
```

## Purpose

This stage converts the completed PlateSupport environment-readiness surface
into evaluation-stage diagnostic evidence.

The environment-readiness command already proves that BBB can bind the upstream
environment and write structural artifacts. This stage should promote those
facts into the gauntlet's formal evaluation pipeline so later stages can depend
on stable, stage-owned machine tables instead of reaching directly into
environment readiness.

## Dependency On Previous Work

This blueprint depends on:

- the suite architecture blueprint;
- `docs/environments/plate_support_5x5_default_v001.md`;
- `docs/environments/plate_support_5x5_default_v001/readiness/dev_001/readout_source.json`;
- the PlateSupport package added under
  `src/big_boy_benchmarking/environments/plate_support/`;
- the readiness runner output under:
  `docs/environments/plate_support_5x5_default_v001/readiness/dev_001/`.

The stage should reuse the readiness runner's graph/state/action/tower helper
logic where appropriate, but it should write evaluation-stage artifacts under
`docs/evaluations/.../standard_gauntlet/...`.

## Why This Stage Exists

Without this stage, later gauntlet components would have two bad choices:

1. reread environment-readiness artifacts directly and blur environment
   construction with evaluation evidence;
2. rerun structural diagnostics ad hoc inside each later stage.

This stage creates a clean boundary:

```text
environment readiness -> Stage 1 evaluation diagnostics -> downstream stages
```

It also lets the suite detect stale or incompatible readiness artifacts before
expensive schema/training stages run.

## Required Inputs

Stage 1 should require:

```text
readiness_readout_source
readiness_artifact_root
environment_doc
environment_instance_id
state_collapser_dependency_state
linearization_mode_id
run_label
locked_by
```

Recommended default readiness source:

```text
docs/environments/plate_support_5x5_default_v001/readiness/dev_001/readout_source.json
```

The stage must verify:

- source type is `environment_readiness`;
- environment family is `plate_support`;
- environment instance is `plate_support_5x5_default_v001`;
- referenced readiness artifact root exists;
- referenced environment doc exists;
- readiness summary exists;
- readiness artifacts were produced under `docs/environments`, not
  `docs/evaluations`.

## Required Diagnostic Domains

### Identity And Provenance

Record:

- suite id;
- stage id;
- run label;
- environment family id;
- environment instance id;
- upstream smoke id;
- upstream module;
- upstream dependency state;
- readiness source paths;
- BBB git state if available.

### State Space

Record:

- ambient candidate state count;
- valid state count;
- reachable valid state count;
- start state id;
- goal state id;
- start valid;
- goal valid;
- reachable-from-start status;
- state summary rows.

Known current values:

```text
candidate_state_count = 2700
valid_state_count = 89
reachable_state_count = 89
```

### Action And Transition Space

Record:

- primitive action count;
- action table;
- valid non-self edge count;
- invalid move count;
- valid clipped self-transition count;
- total self-loop transition count;
- transition rows with candidate state and realized next state separated;
- outgoing non-self count distribution;
- invalid action count distribution;
- self-transition distribution.

Known current values:

```text
action_count = 12
valid_nonself_edge_count = 388
invalid_move_count = 496
valid_self_transition_count = 184
```

### Shortest Path And Reward Anchor

Record:

- shortest path length;
- shortest path action labels;
- shortest path reward sequence;
- total shortest path reward;
- whether goal is one step from start;
- terminal/truncation behavior.

Known current values:

```text
shortest_path_length = 6
goal_one_step_from_start = False
```

The shortest path should be kept visible because it gives humans a concrete
task anchor.

### Validity And Geometry

Record:

- validity predicate summary;
- support pattern summary;
- reachability pattern summary;
- orientation summary;
- position summary;
- socket position distribution if useful;
- engaged-arm reachability distribution.

The key PlateSupport-specific point is that legality is not just a mask field.
It is a constrained geometry/stability predicate over plate pose and support
configuration.

### Random Policy Reconnaissance

Record:

- policy id;
- seed;
- episode count;
- max steps;
- success count;
- success rate;
- mean reward;
- mean step count;
- invalid move count;
- invalid move rate.

Known current readiness values:

```text
episode_count = 1000
success_count = 24
success_rate = 0.024
mean_reward = -105.748
invalid_move_rate ~= 0.452
```

Claim boundary: this is structural difficulty evidence only. It is not a
learning baseline unless a later evaluation explicitly promotes it into a
baseline arm.

### Tower Shape

Record:

- default schema id;
- no-contraction schema id;
- upstream schema mode;
- max depth;
- scheduled assignment count;
- unscheduled assignment count;
- depth curve;
- reset events.

Known current readiness values:

```text
default_schema_max_depth = 2
default_schema_scheduled_assignment_count = 96
no_contraction_schema_max_depth = 1
no_contraction_schema_scheduled_assignment_count = 0
```

Claim boundary: non-flat tower shape is not tower benefit.

### Training Surface Availability

Record availability of:

- `PlateSupportEnvRuntime`;
- `PlateSupportExploitExploreRuntime`;
- `PlateSupportLiftResolveExecutor`;
- `PlateSupportTierLearner`;
- `TowerTrainingConfig`;
- `ExploitExploreTrainingConfig`;
- `run_tower_training`;
- `run_exploit_explore_training`.

Claim boundary: availability is not successful training.

## Required Outputs

### Stage Manifests

```text
stage_manifest.json
stage_budget_lock.json
stage_input_manifest.json
stage_output_manifest.json
readiness_source_manifest.json
```

### Core Tables

```text
results/identity_summary.csv
results/state_space_summary.csv
results/action_table.csv
results/transition_summary.csv
results/shortest_path_summary.csv
results/validity_predicate_summary.csv
results/geometry_summary.csv
results/random_policy_recon_summary.csv
results/tower_shape_summary.csv
results/training_surface_availability.csv
results/downstream_readiness_summary.csv
```

### Summary Files

```text
stage_aggregate_summary.json
stage_aggregate_table.csv
stage_run_index.csv
readout_source.json
artifact_index.md
```

## Downstream Readiness Table

The most important output for later stages is:

```text
results/downstream_readiness_summary.csv
```

Recommended fields:

```text
suite_id
stage_id
environment_instance_id
ready_for_schema_sweep
ready_for_candidate_discovery
ready_for_training_health
ready_for_threshold_calibration
ready_for_paired_comparison
blocking_reason
candidate_state_count
valid_state_count
reachable_state_count
valid_nonself_edge_count
invalid_move_count
valid_self_transition_count
shortest_path_length
default_schema_max_depth
flat_schema_max_depth
training_surfaces_available
claim_boundary
```

For Stage 1, `ready_for_schema_sweep` is the primary downstream gate.

## Pass / Warning / Block Criteria

### Pass

Stage 1 passes if:

- readiness source is valid and repo-resident;
- exact graph diagnostics are complete;
- valid states are reachable from start;
- start and goal are valid;
- shortest path length is finite and greater than one;
- action table covers all primitive actions;
- invalid and self-transition distinctions are preserved;
- default and no-contraction tower probes both exist;
- default schema is non-flat or explicitly documented if flat;
- training surface availability is recorded;
- all required artifacts are written.

### Warning

Stage 1 warns if:

- random policy solves too easily;
- default tower shape is shallow or nearly flat;
- invalid/self-loop pressure is extreme enough to affect later thresholds;
- readiness dependency state differs from current installed dependency;
- default schema shape differs from readiness doc.

Warning does not necessarily block Stage 2, but it must be visible.

### Block

Stage 1 blocks if:

- readiness source is missing;
- readiness source points outside repo;
- environment ids mismatch;
- valid state graph is not fully reachable from start;
- shortest path is missing;
- action/transition contract cannot distinguish invalid self-loop from valid
  self-transition;
- tower probe cannot run;
- required upstream training surfaces are absent;
- artifacts would be written under the wrong stage or evaluation surface.

## Stage Claim Boundary

Allowed claims:

- PlateSupport structural diagnostics are complete for this fixture;
- PlateSupport tower-shape diagnostics are available;
- the suite may proceed to schema sweep if pass criteria hold.

Blocked claims:

- tower methods improve learning;
- any candidate is good;
- any threshold is calibrated;
- any flat-versus-tower comparison has succeeded;
- random policy is an official learning baseline.

## Relationship To Counterpoint

Counterpoint analogue:

- first serious learning structural diagnostics;
- one-third tower diagnostics;
- contraction/noisy-rate structural readouts.

What is inherited:

- separate structural sanity from learning claims;
- expose tower shape and lift/action availability before comparison;
- preserve human-readable claim boundaries.

What is not inherited:

- counterpoint schema mechanics;
- counterpoint reward thresholds;
- counterpoint path-volume concepts;
- counterpoint musical labels.

## Open Questions For Project Owner

These are consultant-authored open questions, not Project Owner statements.

### Question 1: Readiness Source

Consultant recommendation: default to:

```text
docs/environments/plate_support_5x5_default_v001/readiness/dev_001/readout_source.json
```

Resolution status:

```text
Pending Project Owner answer.
```

### Question 2: Should Stage 1 Rerun Diagnostics Or Promote Readiness Artifacts?

Consultant recommendation: do both lightly. Reuse readiness artifact tables as
source provenance, but rerun exact structural diagnostics inside Stage 1 so
stage artifacts are self-contained and stale-readiness mismatch can be detected.

Resolution status:

```text
Pending Project Owner answer.
```

### Question 3: Random Policy Recon Budget

Consultant recommendation: retain `1000` episodes for Stage 1 smoke/dev because
it is cheap and gives stable reconnaissance.

Resolution status:

```text
Pending Project Owner answer.
```

## Expected Next Blueprint

The next component blueprint should be:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/02_contraction_schema_sweep/01_001_plate_support_contraction_schema_sweep_blueprint.md
```

It should consume Stage 1 outputs, especially `tower_shape_summary.csv`,
`transition_summary.csv`, and `downstream_readiness_summary.csv`.
