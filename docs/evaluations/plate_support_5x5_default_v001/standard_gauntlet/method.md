# PlateSupport Standard Gauntlet Method

## Status

Status: scaffolded, not yet run.

## Method Summary

The standard gauntlet is an umbrella evaluation family for the first-class BBB
PlateSupport environment. It is meant to reuse the role sequence discovered
through counterpoint work while preserving PlateSupport-specific mechanics.

The suite starts from existing environment readiness, then moves through
gated diagnostic, candidate, training-health, calibration, comparison, and
readout stages.

## Claim Boundary

Until run artifacts exist, this folder supports architecture and source-binding
claims only.

It does not support:

- a tower-performance claim;
- a flat-versus-tower comparison claim;
- a threshold calibration claim;
- a candidate eligibility claim.

## Artifact Policy

Durable run artifacts for this suite should live under:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/<run-label>/
```

The source binding must remain at:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```
