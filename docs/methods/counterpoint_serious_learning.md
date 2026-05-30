# Counterpoint Serious Learning

This method document describes the first serious learning/control evaluation
surface for `counterpoint_symbolic_v001`.

It is not a result report.

## Evaluation Shape

The serious fixture is:

```text
counterpoint_symbolic_n3_small_v001
```

The `tiny` fixture is for smoke, CI, and command validation only.

The first serious matrix has seven arms:

- `direct_masked_random`
- `direct_tabular_q`
- `tower_empty_exploit_explore_tabular_q`
- `tower_random_balanced_exploit_explore_tabular_q`
- `tower_random_unbalanced_exploit_explore_tabular_q`
- `tower_motion_exploit_explore_tabular_q`
- `tower_bad_exploit_explore_tabular_q`

The direct tabular arm uses upstream
`state_collapser.training.TabularQLearner` with concrete counterpoint state
keys.

The tower arms use:

```text
mode_id: tower_exploit_explore
controller_regime: exploit_explore
training_surface: tower
learner_id: tabular_q
```

The empty-schema tower arm is not direct training. It is the active-tier
tower-control shell with no nontrivial contraction.

The nonempty tower arms keep the same learner, controller, seed, budget, mask,
timing, and artifact discipline while varying the contraction schema.

## Calibration And Budget Lock

Calibration runs first. It records runtime, artifact volume, completion status,
lift/resolve failures, random-schema variability when available, and a proposed
locked budget.

A serious run must execute from a budget lock. It must not silently mutate the
budget during execution.

## Linearization

The default serious linearization condition is:

```text
tensor_available_disabled
```

This means the tensorization boundary is present and recorded, but tensor
execution is disabled. `tensor_enabled_cpu` and `tensor_enabled_cuda` remain
reserved.

## Result Docs

Generated human-facing evaluation docs live under the artifact root by default:

```text
<artifact-root>/evaluations/counterpoint_first_serious_learning_v001/docs/
```

Generated docs summarize artifacts and claim boundary. They must not claim a
serious result exists until the corresponding artifact root exists.

Checked-in files under
`docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/` are stable
guides and templates. They should use `<artifact-root>` placeholders unless a
durable artifact location is intentionally promoted.
