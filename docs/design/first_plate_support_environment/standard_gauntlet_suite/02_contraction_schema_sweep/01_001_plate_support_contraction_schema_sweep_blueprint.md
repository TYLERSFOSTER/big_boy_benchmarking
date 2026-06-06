# PlateSupport Contraction Schema Sweep Blueprint

## Status

Status: initial child-stage blueprint.

This is a design blueprint for Stage 2 of the PlateSupport standard gauntlet
suite. It is not an implementation workplan and not execution approval.

Depends on:

```text
../00_suite_architecture/01_001_plate_support_standard_gauntlet_suite_architecture_blueprint.md
../01_structural_and_tower_diagnostics/01_001_plate_support_structural_and_tower_diagnostics_blueprint.md
```

## Stage Identity

```text
SUITE_ID = "plate_support_standard_gauntlet_v001"
STAGE_ID = "plate_support_gauntlet_contraction_schema_sweep_v001"
ENVIRONMENT_FAMILY_ID = "plate_support"
ENVIRONMENT_INSTANCE_ID = "plate_support_5x5_default_v001"
LINEARIZATION_MODE_ID = "tensor_available_disabled"
```

Recommended readout surface:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/contraction_schema_sweep/
```

Recommended artifact root pattern:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/<run-label>/stages/contraction_schema_sweep/
```

## Purpose

This stage explores PlateSupport-specific contraction/schema choices and
records how each choice affects tower shape, action availability,
executability, endpoint coalescence, and degeneracy.

It is the PlateSupport analogue of several counterpoint diagnostic roles:

- one-third schema tower diagnostics;
- contraction fraction sweep;
- noisy-rate contraction diagnostics.

But it must not copy counterpoint's mechanics blindly. PlateSupport has a small
valid graph, constrained robotics geometry, invalid/self-loop pressure, and a
default upstream schema that already produces max depth `2`.

## Dependency On Stage 1

Stage 2 may run only if Stage 1 says:

```text
ready_for_schema_sweep = true
```

Required Stage 1 source tables:

```text
results/transition_summary.csv
results/tower_shape_summary.csv
results/validity_predicate_summary.csv
results/geometry_summary.csv
results/downstream_readiness_summary.csv
stage_aggregate_summary.json
```

Stage 2 should copy or reference Stage 1 source paths in:

```text
stage_input_manifest.json
stage_source_manifest.json
```

## Central Design Problem

We need schema families that are meaningful for PlateSupport.

Counterpoint's local edge-fraction and noisy-rate strategies were useful
because counterpoint was a symbolic hidden graph with edge-label structure and
path-volume concerns. PlateSupport is instead a constrained control graph over:

```text
x_idx, y_idx, theta_idx, e1, e2, e3
```

A PlateSupport schema sweep should ask:

- What contractions respect or expose plate/support geometry?
- Which contractions collapse too much?
- Which contractions remain flat or near-flat?
- Which contractions preserve enough executable action structure for training?
- Which contractions produce candidate towers for later stages?

## Proposed Schema Families

### Family A: Upstream Default Schema

ID:

```text
plate_support_schema_upstream_default_v001
```

Role:

- reference the upstream default `default_plate_support_schema`;
- preserve current behavior:
  - max depth `2`;
  - scheduled assignments around `96`;
  - no-contraction control depth `1`.

Why include:

- establishes continuity with environment readiness;
- becomes a baseline schema candidate.

### Family B: No-Contraction Control

ID:

```text
plate_support_schema_no_contraction_v001
```

Role:

- explicit flat control;
- required for every sweep;
- not a training comparison yet.

Why include:

- proves the runner can distinguish tower effects from direct/flat behavior.

### Family C: Geometry-Coordinate Schemas

Candidate IDs:

```text
plate_support_schema_position_only_v001
plate_support_schema_orientation_only_v001
plate_support_schema_support_pattern_only_v001
plate_support_schema_reachability_pattern_only_v001
plate_support_schema_position_support_v001
```

Role:

- collapse or group edges/states according to PlateSupport-relevant geometry;
- reveal whether position, orientation, support pattern, or reachability
  structure creates useful tower layers.

Design caution:

- upstream `state_collapser` schema surfaces may be edge-label oriented. If
  state-feature schemas require upstream support that does not exist, Stage 2
  must either:
  - restrict itself to available schema surfaces; or
  - stop and request a separate upstream/BBB design discussion.

Do not silently fake state-feature contraction if the runtime only supports
edge-label schemas.

### Family D: Action-Category Schemas

Candidate IDs:

```text
plate_support_schema_plate_motion_actions_v001
plate_support_schema_arm_extension_actions_v001
plate_support_schema_motion_vs_support_actions_v001
```

Role:

- group primitive actions by control category:
  - plate translation;
  - plate rotation;
  - arm extension/retraction;
  - motion versus support.

Why include:

- PlateSupport action semantics are robotics-flavored and may expose useful
  abstraction structure by action category.

### Family E: Edge-Global Noisy-Rate Schemas

Candidate IDs should include rate labels, for example:

```text
plate_support_schema_edge_global_noisy_rate_001_over_089_v001
plate_support_schema_edge_global_noisy_rate_002_over_089_v001
plate_support_schema_edge_global_noisy_rate_004_over_089_v001
plate_support_schema_edge_global_noisy_rate_008_over_089_v001
```

Role:

- retain the counterpoint lesson that source-local minimum-one semantics can
  be too aggressive;
- test small edge-global contraction budgets without forcing every source to
  contribute an edge.

Recommended rate basis:

- use valid non-self edge count as denominator if the schema operates over
  valid transition edges;
- current valid non-self edge count is `388`, so rate labels may need to use
  denominator `388` rather than `89` after final design.

Open issue:

- decide whether denominator should be valid states, valid non-self edges, or
  candidate transition rows.

### Family F: Controlled Degeneracy Anchors

Candidate IDs:

```text
plate_support_schema_full_single_block_v001
plate_support_schema_source_local_one_drop_v001
```

Role:

- deliberately include known-risk or likely-degenerate anchors;
- help readouts explain collapse pathologies;
- not eligible for downstream training unless explicitly marked usable.

Why include:

- counterpoint showed that knowing where collapse begins is part of the
  diagnostic value.

## Sweep Axes

Recommended axes:

```text
schema_family_id
schema_id
schema_seed
selection_policy_id
selection_rate
selection_count
state_feature_basis
action_category_basis
edge_basis
```

Not every schema family uses every axis. Missing axes should be explicit
`not_applicable`, not blank.

## Required Runtime Diagnostics

For every schema arm, record:

- schema manifest;
- construction metadata;
- scheduled assignment count;
- unscheduled assignment count;
- contracted edge count;
- selected source count;
- zero-selected-source count if relevant;
- selected action categories if relevant;
- selected geometry features if relevant;
- tower max depth;
- state-cell count by tier;
- action-cell count by tier;
- active action-cell count by tier;
- largest cell share by tier;
- singleton cell share by tier;
- endpoint coalescence summary;
- tower invariant report;
- liftability/executability summary by tier;
- concrete step smoke summary if a tiny rollout is used;
- compatibility readout timing.

## Required Outputs

### Manifests

```text
stage_manifest.json
stage_budget_lock.json
stage_input_manifest.json
schema_family_manifest.json
schema_arm_manifest.json
schema_construction_manifest.json
```

### Tables

```text
results/schema_arm_summary.csv
results/schema_construction_summary.csv
results/schema_selection_summary.csv
results/tower_shape_summary.csv
results/tier_occupancy_summary.csv
results/tier_executability_summary.csv
results/endpoint_coalescence_summary.csv
results/collapse_diagnostic_summary.csv
results/schema_candidate_signal_summary.csv
results/timing_summary.csv
results/downstream_candidate_input_summary.csv
```

### Summary

```text
stage_aggregate_summary.json
stage_aggregate_table.csv
stage_run_index.csv
readout_source.json
artifact_index.md
```

## Collapse And Degeneracy Criteria

Every schema arm should receive a structural class:

```text
flat_control
nonflat_structured
near_flat
near_full_collapse
full_first_projection_collapse
runtime_unexecutable
construction_failed
```

Recommended criteria:

- `flat_control`: max depth `1` and schema is no-contraction;
- `near_flat`: max depth `1` but schema intended non-flat;
- `nonflat_structured`: max depth `> 1`, first projection does not collapse
  nearly all states, executable action surface remains nonzero;
- `near_full_collapse`: largest non-base tier state-cell share above a chosen
  high threshold, such as `0.90`;
- `full_first_projection_collapse`: all reachable states share one first
  quotient cell;
- `runtime_unexecutable`: tower exists but selected/active action surface is
  empty under the smoke rollout;
- `construction_failed`: schema cannot be built.

Threshold values must be visible and overrideable.

## Candidate Signal Summary

Stage 2 should not select final candidates. It should emit candidate signals for
Stage 3.

Recommended fields:

```text
schema_id
schema_family_id
schema_seed
structural_class
candidate_signal
candidate_signal_reason
max_depth
first_nonbase_tier_state_cell_count
largest_cell_share
active_action_cell_min
active_action_cell_mean
lift_success_probe_count
lift_failure_probe_count
selected_edge_count
zero_selected_source_count
recommended_for_candidate_discovery
blocking_reason
```

Candidate signal values:

```text
eligible_signal
warning_signal
blocked_signal
control_anchor
degeneracy_anchor
```

## Pass / Warning / Block Criteria

### Pass

Stage 2 passes if:

- no-contraction control runs and stays flat;
- upstream default schema runs;
- at least one non-control schema family runs;
- every attempted schema arm produces a structured status row;
- candidate-signal table is written;
- stage artifacts are repo-resident.

### Warning

Stage 2 warns if:

- only upstream default produces non-flat structure;
- all custom schemas collapse or stay flat;
- construction failures occur for optional schema families;
- execution smoke shows sparse or unstable action availability.

### Block

Stage 2 blocks if:

- Stage 1 source is missing or not ready for schema sweep;
- no-contraction control cannot run;
- upstream default schema cannot run;
- the runtime cannot represent any designed schema family and a redesign is
  required;
- artifacts cannot preserve schema construction metadata.

## Stage Claim Boundary

Allowed claims:

- the suite explored specific PlateSupport schema families;
- specific schema arms are flat, nonflat, degenerate, or blocked;
- Stage 3 has candidate-signal inputs if any exist.

Blocked claims:

- candidate selected for training;
- tower training works;
- tower beats flat/no-contraction baseline;
- threshold is calibrated;
- broad abstraction benefit.

## Relationship To Counterpoint

Inherited lessons:

- source-local minimum-one selection can hide severe collapse;
- edge-global noisy rates are useful to test small contraction budgets;
- full or near-full first projection collapse must be described structurally,
  not as learning failure;
- candidate source manifests are critical.

Not inherited:

- counterpoint `n/18` denominator;
- counterpoint reward threshold values;
- counterpoint path-volume semantics;
- counterpoint-specific motion schema IDs.

## Open Questions For Project Owner

These are consultant-authored open questions, not Project Owner statements.

### Question 1: Include Experimental Geometry Schemas?

Consultant recommendation: include them in the blueprint as desired schema
families, but require implementation to stop if upstream schema surfaces cannot
represent them honestly.

Resolution status:

```text
Pending Project Owner answer.
```

### Question 2: Initial Sweep Budget

Consultant recommendation: first run should be smoke/dev, with no serious
training budget. Include no-contraction, upstream default, a small action-
category set, and a small edge-global noisy-rate set.

Resolution status:

```text
Pending Project Owner answer.
```

### Question 3: Edge-Global Denominator

Consultant recommendation: use valid non-self edge count (`388`) as the primary
denominator if the schema operates over executable transition edges. Use valid
state count (`89`) only for state-based selection policies.

Resolution status:

```text
Pending Project Owner answer.
```

## Expected Next Blueprint

The next component blueprint should be:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/03_candidate_discovery/01_001_plate_support_candidate_discovery_blueprint.md
```

It should consume `schema_candidate_signal_summary.csv` and the Stage 2 schema
construction/tower-shape tables.
