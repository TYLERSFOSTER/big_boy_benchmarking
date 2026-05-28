# Counterpoint Schema Diagnostics

Source blueprint:

- `docs/design/first_counterpoint_environment/01_002_counterpoint_hidden_graph_and_contraction_schema_benchmark_blueprint.md`

Schema diagnostics compare contraction schemata on the same hidden graph.

Implemented diagnostics include:

- schema manifest;
- quotient summary;
- quotient cells;
- address traces;
- balanced addressability;
- reward-fiber variance;
- lift-fiber summary.

Exact diagnostics are used on the tiny fixture. Larger fixtures may use sampled
diagnostics, and sampled artifacts must say so explicitly.

Projection-audit outputs are posthoc under v001. They are not online training
defaults.
