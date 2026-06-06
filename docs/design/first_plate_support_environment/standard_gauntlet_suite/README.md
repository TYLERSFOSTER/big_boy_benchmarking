# PlateSupport Standard Gauntlet Suite Design

## Purpose

This folder is the parent design area for a PlateSupport umbrella evaluation
family.

The Project Owner identified that the counterpoint sequence has become a useful
baseline pipeline or gauntlet: not because PlateSupport should copy
counterpoint literally, but because the counterpoint work discovered a sequence
of evaluation roles that a standard tower-capable benchmark environment should
be able to meet.

This folder should organize that suite as one umbrella design while keeping the
individual parts separated enough to prevent compression drift.

## Current Intent

Design one umbrella evaluation family, likely along the lines of:

```text
plate_support_standard_gauntlet_v001
```

The umbrella should define:

- the full suite architecture;
- stage ordering and stop gates;
- shared artifact contracts;
- shared readout expectations;
- how each child evaluation role contributes evidence;
- what counts as environment readiness versus evaluation evidence;
- when later stages may consume earlier-stage outputs;
- claim boundaries at each stage.

## Compression Guard

Do not implement this as a blind rename of counterpoint.

The counterpoint pipeline supplies roles, not PlateSupport answers. PlateSupport
has different state semantics, action legality, reward scale, training surfaces,
tower shapes, schema construction, thresholds, and possible failure modes.

The safe design pattern is:

```text
one umbrella blueprint
many explicitly gated child-stage designs
implementation workplans that stop at unknowns rather than inventing answers
```

## Child Design Areas

- `00_suite_architecture/`: umbrella architecture, stage ordering, shared
  contracts, suite-level claim boundaries, and cross-stage artifact flow.
- `01_structural_and_tower_diagnostics/`: PlateSupport structural diagnostics
  and tower-shape diagnostics as an evaluation-stage input.
- `02_contraction_schema_sweep/`: schema-strength or contraction-choice sweep
  adapted to PlateSupport.
- `03_candidate_discovery/`: selection of non-degenerate or otherwise useful
  tower/schema candidates for downstream training work.
- `04_tower_training_health/`: tower-only training-health diagnostic for
  selected candidates, without direct comparison claims.
- `05_threshold_frontier_calibration/`: threshold or success-frontier
  calibration for PlateSupport reward/goal behavior.
- `06_paired_replicate_comparison/`: paired comparison between a flat/no-
  contraction baseline and selected tower/schema condition.
- `07_readout_and_system_learning/`: human-readable readouts, status badges,
  system-learning archive, and cross-stage narrative.

## Current Status

Status: scaffold only.

Next expected action: begin design discussion in `00_suite_architecture/`.
