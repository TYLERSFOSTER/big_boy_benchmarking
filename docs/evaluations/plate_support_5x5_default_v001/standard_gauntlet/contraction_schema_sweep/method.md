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
