# Result Readout

This diagnostic is a tower-only training-health check for selected non-collapsed noisy-rate counterpoint towers. It is not a direct baseline comparison and does not rank contraction schemas.

## What Happened

- Selected candidates: `1`.
- Concrete base steps emitted: `32`.
- Successful learner updates: `40`.
- Health classes: `{'trainable_clean': 1}`.

## How We Know

The evidence comes from the evaluation aggregate table plus candidate, tower-shape, concrete-step, lift, controller, tier, and learner-update summary tables listed in `readout_source.json`.

## What This Means

A clean health result means the selected tower executed, lifted actions to concrete transitions, and emitted learner-update evidence under the locked smoke budget.

## What This Does Not Mean

This run does not establish tower advantage, direct baseline performance, schema superiority, deep repeated-contraction behavior, tensor-enabled runtime behavior, or musical quality.
