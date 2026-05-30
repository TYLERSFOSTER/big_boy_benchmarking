# Glossary

## Status Terms

`artifact status`
: Whether the benchmark harness ran and wrote expected machine-readable files.

`behavior status`
: Whether the measured environment/control behavior succeeded.

`claim status`
: Whether this artifact set supports a benchmark claim.

In this run, all arms are artifact-complete, but non-empty tower arms are
behavior-failed.

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

`seed_bundle_id`
: Seed bundle for the environment/learner run.

`mean_return`
: Average total reward per episode.

`delta_vs_direct_tabular_q`
: Difference between an arm's mean return and the direct tabular Q baseline.

`delta_vs_empty_tower`
: Difference between an arm's mean return and the empty-schema tower arm.

`step_count`
: Number of concrete environment steps executed in an episode.

`success`
: Episode-level success flag. In this artifact set, non-empty tower arms have
`success=False` for every episode.

`control_action`
: Tower controller action such as `descend`, `explore`, `exploit_execute`, or
`train`.

`active_tier_before` / `active_tier_after`
: Tower tier before and after a controller event.

`failure_reason`
: Diagnostic reason for a failed lift/action-realization attempt.

`invalid_action_index`
: Lift/action-realization failure where the abstract or realized action index
does not map to a valid concrete environment action.

`linearization_mode_id`
: Numeric/backend discipline label. This run records
`tensor_available_disabled`.

## Arms

`direct_masked_random`
: Direct environment random policy constrained by legal action masks.

`direct_tabular_q`
: Direct environment tabular Q-learning baseline.

`tower_empty_exploit_explore_tabular_q`
: Tower controller with empty schema. This is a tower-control shell without
nontrivial contraction.

`tower_random_balanced_exploit_explore_tabular_q`
: Tower controller with seeded balanced random contraction schema.

`tower_random_unbalanced_exploit_explore_tabular_q`
: Tower controller with seeded unbalanced random contraction schema.

`tower_motion_exploit_explore_tabular_q`
: Tower controller with structured motion contraction schema.

`tower_bad_exploit_explore_tabular_q`
: Tower controller with intentionally bad/adversarial overcompression schema.
