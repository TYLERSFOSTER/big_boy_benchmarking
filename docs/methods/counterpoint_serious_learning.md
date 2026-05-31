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

## Result Readouts

Raw serious-learning artifacts live under the explicit artifact root. For
durable serious counterpoint evaluations, that root is repo-resident:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/<run-label>/evaluations/counterpoint_first_serious_learning_v001/
```

The summarizer may write generated docs under that artifact tree for immediate
inspection, but the durable human readout surface remains:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/
```

That repo folder must include `readout_source.json`, which binds the readout
surface to the raw aggregate tables, run index, result tables, goal sources,
methodology sources, expected-file policy, and claim boundary.

Regenerate the repo-side human readout with:

```text
execute artifact-table readout pointed at folder docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/
```

Generated readouts summarize artifacts and claim boundaries. They must not
claim a serious result exists until the corresponding machine-readable artifact
set exists and the source binding points to it.
