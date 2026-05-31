# Method

This evaluation runs upstream `state_collapser` active-tier ABC control through
BBB's counterpoint tower adapter. The only schema under test is
`counterpoint_one_third_outgoing_schema_v001`.

The schema samples outgoing edges source-locally. For each source state,
outgoing edges are deterministically shuffled by schema seed, then assigned
through three recursive one-third contraction blocks using `ceil(remaining / 3)`
block sizes. Leftovers are reported explicitly as `one_third_unscheduled`.

BBB records ordinary control events and additional ABC diagnostic rows. The ABC
rows are computed from upstream helper functions on the exact inputs passed to
upstream `ActiveTierController.decide(...)`; BBB does not substitute a new
controller policy.

Budget summary:

| Field | Value |
| --- | --- |
| Instances | `counterpoint_symbolic_n3_small_v001`, `counterpoint_symbolic_n3_medium_v001` |
| Schema seeds | `0,1,2` |
| Replicates per schema seed | `4` |
| Episodes per replicate | `16` |
| Base seed | `0` |
| Small horizon | `8` |
| Medium horizon | `12` |
| Controller event ceiling policy | `max(64, 8 * horizon)` |
| Linearization mode | `tensor_available_disabled` |

The method supports diagnostic claims about:

- source-local one-third schema block geometry;
- quotient tower shape by tier;
- upstream ABC selected-tier and blocked-reason behavior;
- lift/executability at the active tier;
- concrete step emission under the recorded runtime path.

The method does not support direct-vs-tower comparison, tensor-enabled
performance, musical-quality claims, GPU/CUDA claims, or general tower-learning
claims.
