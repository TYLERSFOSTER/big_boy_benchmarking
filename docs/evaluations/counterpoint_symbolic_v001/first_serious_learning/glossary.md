# Glossary

## Status Terms

`artifact status`
: Whether the benchmark harness ran and wrote expected machine-readable files.

`behavior status`
: Whether the measured environment/control behavior executed meaningful
episodes.

`claim status`
: Whether this artifact set supports a benchmark claim.

In this run, all arms are artifact-complete. Direct and empty-schema arms
execute meaningful episodes. Non-empty tower arms are classified as
structural-limit diagnostics because full or near-full first-projection
collapse dominates interpretation; random balanced and random unbalanced also
show schema-seed-dependent lift/action-realization failures.

## Fields

`arm_id`
: Machine id for an evaluation arm.

`mode_id`
: Benchmark execution mode. Direct arms use direct environment modes; tower
arms use `tower_exploit_explore`.

`schema_id`
: Contraction schema used by a tower arm.

`schema_seed`
: Seed used to generate a random schema.

`mean_return`
: Average total reward per episode.

`delta_vs_direct_tabular_q`
: Difference between an arm's mean return and the direct tabular Q baseline.

`delta_vs_empty_tower`
: Difference between an arm's mean return and the empty-schema tower arm.

`step_count`
: Number of concrete environment steps executed in an episode.

`success`
: Episode-level success flag. In this artifact set, zero-step episodes are
marked unsuccessful, while 8-step episodes are marked successful.

`state_cell_count_by_tier`
: Tower shape tuple. Tier `0` is the fine/base tier. Later indices are more
coarsened quotient tiers.

`structural_limit`
: Behavior classification used when quotient shape dominates interpretation,
especially when the first projection fully or nearly fully collapses tier-`0`
states.

`no_lift_candidate_from_current_state`
: Lift/action-realization failure where the active tier has an abstract action
but no lift candidate from the current concrete state. In this run, it appears
on specific random schema seeds.

`linearization_mode_id`
: Numeric/backend discipline label. This run records
`tensor_available_disabled`.
