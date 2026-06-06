# PlateSupport Candidate Discovery Blueprint

## Status

Status: initial child-stage blueprint.

This is a design blueprint for Stage 3 of the PlateSupport standard gauntlet
suite. It is not an implementation workplan and not execution approval.

Depends on:

```text
../00_suite_architecture/01_001_plate_support_standard_gauntlet_suite_architecture_blueprint.md
../01_structural_and_tower_diagnostics/01_001_plate_support_structural_and_tower_diagnostics_blueprint.md
../02_contraction_schema_sweep/01_001_plate_support_contraction_schema_sweep_blueprint.md
```

## Stage Identity

```text
SUITE_ID = "plate_support_standard_gauntlet_v001"
STAGE_ID = "plate_support_gauntlet_candidate_discovery_v001"
ENVIRONMENT_FAMILY_ID = "plate_support"
ENVIRONMENT_INSTANCE_ID = "plate_support_5x5_default_v001"
LINEARIZATION_MODE_ID = "tensor_available_disabled"
```

Recommended readout surface:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/candidate_discovery/
```

Recommended artifact root pattern:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/<run-label>/stages/candidate_discovery/
```

## Purpose

This stage turns Stage 2 schema-sweep signals into an explicit downstream
candidate manifest.

It answers:

- which PlateSupport schema/tower arms are eligible for training-health checks;
- which are useful controls or degeneracy anchors;
- which are blocked and why;
- what exact source artifacts justify each selection.

Candidate discovery must be its own stage because counterpoint showed that
downstream evaluations become confusing when they silently pick towers out of
diagnostic outputs.

## Dependency On Previous Stages

Stage 3 may run only if Stage 2 emits:

```text
results/schema_candidate_signal_summary.csv
results/schema_arm_summary.csv
results/tower_shape_summary.csv
results/tier_executability_summary.csv
results/collapse_diagnostic_summary.csv
stage_aggregate_summary.json
```

Stage 3 should also retain Stage 1 source facts:

```text
valid_state_count = 89
valid_nonself_edge_count = 388
shortest_path_length = 6
default_schema_max_depth = 2
flat_schema_max_depth = 1
```

These facts help interpret whether a candidate is meaningfully structured in
the context of a small constrained graph.

## Candidate Classes

Stage 3 should classify every Stage 2 candidate signal into one of:

```text
selected_training_candidate
selected_warning_candidate
selected_control_anchor
selected_degeneracy_anchor
eligible_not_selected
blocked_flat
blocked_collapse
blocked_unexecutable
blocked_construction_failure
blocked_missing_source
```

### Selected Training Candidate

Meaning:

- intended for Stage 4 tower-only training-health;
- may later be considered for Stage 6 paired comparison if Stage 4 passes.

Minimum criteria:

- non-control schema;
- structural class `nonflat_structured`;
- max depth greater than `1`;
- not full first-projection collapse;
- active/executable action surface nonzero in Stage 2 diagnostics;
- construction metadata complete;
- source paths valid.

### Selected Warning Candidate

Meaning:

- may be run in Stage 4 only if PO or implementation workplan explicitly
  allows warning candidates;
- useful when all clean candidates are too sparse but diagnostic value remains.

Possible warning reasons:

- near-full but not full collapse;
- sparse active action surface;
- shallow but non-flat tower;
- optional schema-family implementation uncertainty.

### Selected Control Anchor

Meaning:

- no-contraction or known-flat schema used to anchor diagnostics;
- not treated as the tower condition in a comparison.

Examples:

```text
plate_support_schema_no_contraction_v001
```

### Selected Degeneracy Anchor

Meaning:

- intentionally pathological or collapse-heavy schema retained for readout
  interpretation;
- not eligible for Stage 4 unless a diagnostic workplan explicitly asks for
  degenerate training behavior.

### Blocked Candidates

Blocked candidates must remain in the output table. Do not drop them.

Why:

- the absence of candidates is evidence;
- future schema design needs to know which ideas failed;
- human readouts must explain why no comparison can proceed if that happens.

## Selection Policy

Recommended first policy:

```text
plate_support_candidate_selection_policy_v001
```

Policy priorities:

1. include the no-contraction control anchor;
2. include upstream default if eligible or warning-eligible;
3. include up to `N` clean nonflat structured candidates from distinct schema
   families;
4. include at most one warning candidate if no clean candidates exist or if the
   warning candidate is uniquely informative;
5. include at most one degeneracy anchor for interpretability;
6. never select a candidate with missing construction metadata;
7. never select a candidate with zero executable action surface unless the
   explicit role is degeneracy anchor.

Recommended smoke/dev candidate cap:

```text
clean_candidate_cap = 2
warning_candidate_cap = 1
degeneracy_anchor_cap = 1
```

The cap should be recorded in the budget lock.

## Required Inputs

```text
schema_candidate_signal_summary.csv
schema_arm_summary.csv
schema_construction_summary.csv
tower_shape_summary.csv
tier_executability_summary.csv
collapse_diagnostic_summary.csv
stage_aggregate_summary.json
```

Every input row must be traceable back to:

- Stage 2 artifact root;
- schema id;
- schema family id;
- schema seed;
- environment instance id;
- linearization mode.

## Required Outputs

### Manifests

```text
stage_manifest.json
stage_budget_lock.json
stage_input_manifest.json
candidate_selection_policy_manifest.json
candidate_manifest.json
parent_schema_sweep_manifest.json
```

### Tables

```text
results/candidate_eligibility_summary.csv
results/selected_candidate_summary.csv
results/blocked_candidate_summary.csv
results/control_anchor_summary.csv
results/degeneracy_anchor_summary.csv
results/candidate_source_trace.csv
results/downstream_training_health_input_summary.csv
```

### Summary

```text
stage_aggregate_summary.json
stage_aggregate_table.csv
stage_run_index.csv
readout_source.json
artifact_index.md
```

## Candidate Manifest Fields

Recommended fields:

```text
candidate_id
candidate_role
selection_status
schema_id
schema_family_id
schema_seed
schema_construction_id
source_stage_id
source_artifact_root
source_row_id
environment_instance_id
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
eligibility_score
eligibility_reason
blocking_reason
allowed_downstream_stages
```

`candidate_id` should be stable and deterministic. Recommended format:

```text
plate_support_candidate:<schema_family_id>:<schema_seed>:<short_hash>
```

## Eligibility Score

The score is not a statistical result. It is a deterministic ranking helper.

Recommended ingredients:

- non-flat depth;
- not near-full collapse;
- active action surface;
- successful liftability/executability probe;
- family diversity;
- construction metadata completeness.

Example score components:

```text
+3 nonflat structured
+2 executable action surface present
+2 largest cell share below near-collapse threshold
+1 schema family diversity
+1 upstream default continuity
-3 near-full collapse
-5 full collapse
-5 zero executable actions
-5 missing construction metadata
```

Scores should be written only as selection-policy metadata. Do not treat them as
performance.

## Downstream Gate

Stage 4 may run only if:

```text
selected_training_candidate_count >= 1
```

or if the Project Owner explicitly authorizes a warning-candidate diagnostic.

Stage 6 may not consume Stage 3 directly. It must wait for Stage 4
training-health and Stage 5 threshold calibration.

## Pass / Warning / Block Criteria

### Pass

Stage 3 passes if:

- Stage 2 source artifacts are valid;
- candidate policy manifest is written;
- every Stage 2 signal row is classified;
- at least one selected training candidate exists;
- selected candidates have complete source traces.

### Warning

Stage 3 warns if:

- only upstream default is eligible;
- candidates exist but are shallow or sparse;
- selected candidates are warning-class only;
- degeneracy anchors dominate the sweep.

### Block

Stage 3 blocks if:

- Stage 2 source artifacts are missing;
- no selected training candidate exists and warning candidates are not
  authorized;
- source trace is incomplete;
- candidate IDs cannot be stable;
- selection would silently discard blocked candidates.

## Stage Claim Boundary

Allowed claims:

- the suite selected candidate towers/schemas for downstream training-health;
- specific candidates are eligible, warning, blocked, controls, or degeneracy
  anchors;
- Stage 4 may proceed if selected training candidates exist.

Blocked claims:

- selected candidates train successfully;
- selected candidates beat no-contraction;
- threshold is calibrated;
- candidate score is performance evidence;
- blocked candidates prove PlateSupport is unsuitable.

## Relationship To Counterpoint

Inherited lessons:

- downstream stages need explicit candidate manifests;
- candidate source paths must be repo-resident;
- blocked candidates must remain visible;
- candidate selection must not confuse diagnostic eligibility with performance.

Not inherited:

- counterpoint noisy-rate candidate IDs;
- counterpoint `wide_span18` fixture assumptions;
- counterpoint threshold-specific eligibility criteria.

## Open Questions For Project Owner

These are consultant-authored open questions, not Project Owner statements.

### Question 1: Candidate Cap

Consultant recommendation for first implementation:

```text
clean_candidate_cap = 2
warning_candidate_cap = 1
degeneracy_anchor_cap = 1
```

Resolution status:

```text
Pending Project Owner answer.
```

### Question 2: Upstream Default Candidate Treatment

Consultant recommendation: include upstream default as a candidate if it meets
eligibility, because it is the known upstream schema. If it is the only eligible
candidate, mark the suite warning rather than blocked.

Resolution status:

```text
Pending Project Owner answer.
```

### Question 3: Warning Candidate Authorization

Consultant recommendation: Stage 3 may select warning candidates, but Stage 4
should require explicit budget-lock acknowledgement before training them.

Resolution status:

```text
Pending Project Owner answer.
```

## Expected Next Blueprint

The next component blueprint should be:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/04_tower_training_health/01_001_plate_support_tower_training_health_blueprint.md
```

It should consume `candidate_manifest.json`,
`selected_candidate_summary.csv`, and `downstream_training_health_input_summary.csv`.
