# PlateSupport Threshold Frontier Calibration Method

Stage 5 reuses the validated Stage 4 tower-training-health traces,
summarizes binary goal success, first-hit timing, sustained-window
feasibility, and observed return distributions, then builds return
threshold candidates from observed quantiles, the success/miss boundary,
Stage 1 random-policy reward context, and the Stage 1 shortest-path
reward anchor.

Calibration arms preserve selected-candidate schema metadata,
including whether the Stage 4 trace came from the iterated
source-local ratio correction path. Calibration does not rebuild the
schema, but it must keep this identity visible for Stage 6 and human
readouts.

The recommended target is selected for Stage 6 only. This stage is
calibration evidence, not comparison evidence.
