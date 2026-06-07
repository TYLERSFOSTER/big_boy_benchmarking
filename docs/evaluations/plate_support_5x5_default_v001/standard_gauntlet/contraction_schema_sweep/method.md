# PlateSupport Contraction Schema Sweep Method

The sweep consumes Stage 1 structural diagnostics, runs the mandatory
no-contraction and upstream-default schema modes, runs BBB-owned
source-local outgoing-edge ratio schemas on the exact PlateSupport
graph, and emits explicit unsupported rows for custom schema families
that the current upstream PlateSupport probe cannot represent honestly.

Source-local ratio schemas use catch semantics: every source with
at least one valid non-self outgoing edge contributes
`max(1, ceil(out_degree * numerator / denominator))` selected
edges to the contraction block.

Iterated source-local ratio schemas are optional correction-run
arms. They repeatedly select stable quotient-representative
source-local edges, one block per iteration, and record plan, stop,
and many-tier candidate-signal tables. They do not use the one-shot
catch rule and they allow zero selected edges in a source component.
