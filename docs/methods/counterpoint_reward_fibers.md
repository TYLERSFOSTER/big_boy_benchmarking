# Counterpoint Reward Fibers

Source blueprint:

- `docs/design/first_counterpoint_environment/01_002_counterpoint_hidden_graph_and_contraction_schema_benchmark_blueprint.md`

Reward-fiber diagnostics measure reward compatibility inside schema cells.

Implemented fields include:

- schema id;
- cell id;
- fine transition count;
- reward mean;
- reward variance;
- reward min;
- reward max;
- term-level variance.

The first reward direct-image policy treats mean and variance as primary, while
also recording cheap secondary diagnostics where available.
