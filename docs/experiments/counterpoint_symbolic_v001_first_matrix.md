# Counterpoint Symbolic V001 First Matrix

Environment family:

```text
counterpoint_symbolic_v001
```

Implemented smoke/diagnostic arms:

- direct masked-random smoke;
- direct tabular-Q smoke;
- tower empty-schema smoke;
- tower random-balanced-schema smoke;
- tower random-unbalanced-schema smoke;
- tower structured-motion-schema smoke.

Implemented diagnostic schema families:

- empty;
- random balanced;
- random unbalanced;
- structured motion;
- projection audit;
- bad/adversarial.

Implemented first serious-learning arms:

- `direct_masked_random`;
- `direct_tabular_q`;
- `tower_empty_exploit_explore_tabular_q`;
- `tower_random_balanced_exploit_explore_tabular_q`;
- `tower_random_unbalanced_exploit_explore_tabular_q`;
- `tower_motion_exploit_explore_tabular_q`;
- `tower_bad_exploit_explore_tabular_q`.

Reserved or non-claim surfaces:

- projection audit as online schema;
- medium, large, and stress tiers;
- deep RL learners;
- fiber-conditioned substages.

Claim boundary:

The smoke/diagnostic rows are implementation and artifact-contract evidence
only.

The serious-learning rows are runnable for the first serious fixture
`counterpoint_symbolic_n3_small_v001` under `tensor_available_disabled`.
They do not claim tensor-enabled performance, GPU performance, musical quality,
or general method superiority.
