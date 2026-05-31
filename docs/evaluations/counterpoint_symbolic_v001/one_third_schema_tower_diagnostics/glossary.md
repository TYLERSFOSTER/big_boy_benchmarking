# Glossary

- `ABC`: upstream active-tier controller behavior from `state_collapser`. BBB
  records the helper inputs and outputs so the selected tier and blocked
  reasons are visible.
- `active tier`: the tier where the runtime is currently attempting control or
  execution. In this run, concrete execution occurs at tier `0`.
- `base tier`: tier `0`, the fine/concrete counterpoint hidden graph.
- `coarser tier`: a higher tier index. Tier `1` is the first quotient above the
  base graph.
- `concrete step`: a successful transition in the base counterpoint
  environment after an abstract action is resolved/lifted.
- `executable tier`: a tier/context where the runtime has concrete-realizable
  outgoing action options.
- `full first-projection collapse`: tier `1` has one state cell, so all base
  states map into a single tier-`1` fiber.
- `largest_state_fiber_share`: fraction of base states contained in the largest
  quotient state cell for a tier.
- `lift`: the process of resolving an abstract/tower action into a concrete
  base-environment transition.
- `near full collapse`: a quotient tier has a largest fiber share of at least
  `0.90`.
- `one_third_block_0`, `one_third_block_1`, `one_third_block_2`: recursive
  source-local edge blocks assigned by the one-third schema.
- `one_third_unscheduled`: leftover outgoing edges not assigned to the three
  scheduled one-third blocks.
- `selected tier`: the tier selected by the upstream ABC helper logic for the
  current control context. Empty selected-tier fields in the summary correspond
  to `no_executable_unclosed` contexts.
- `source-local one-third`: a contraction schema that shuffles and partitions
  outgoing edges separately for each source state rather than globally.
- `structural limit`: a result where the constructed quotient geometry blocks
  ordinary performance interpretation even if the runtime and artifact writing
  succeeded.
- `tensor_available_disabled`: linearization/tensor support is present enough
  for reporting, but conversion is disabled and no tensor-enabled claim is
  allowed.
