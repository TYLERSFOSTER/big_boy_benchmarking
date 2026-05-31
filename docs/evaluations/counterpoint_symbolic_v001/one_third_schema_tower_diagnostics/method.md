# Method

This evaluation runs upstream `state_collapser` active-tier ABC control through BBB's counterpoint tower adapter. The only schema under test is `counterpoint_one_third_outgoing_schema_v001`.

The schema samples outgoing edges source-locally. For each source state, outgoing edges are deterministically shuffled by schema seed, then assigned through three recursive one-third contraction blocks using `ceil(remaining / 3)` block sizes. Leftovers are reported explicitly.

BBB records ordinary control events and additional ABC diagnostic rows. The additional rows are computed from upstream helper functions on the exact inputs passed to upstream `ActiveTierController.decide(...)`; BBB does not substitute a new controller policy.

Budget summary:

- controller event ceiling policy: `max(64, 8 * horizon)`
- horizon by instance id: `{'counterpoint_symbolic_n3_medium_v001': 12, 'counterpoint_symbolic_n3_small_v001': 8}`
