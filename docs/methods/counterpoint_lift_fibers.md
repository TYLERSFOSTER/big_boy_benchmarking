# Counterpoint Lift Fibers

Source blueprint:

- `docs/design/first_counterpoint_environment/01_002_counterpoint_hidden_graph_and_contraction_schema_benchmark_blueprint.md`

Lift-fiber diagnostics describe how many fine candidates live below a coarse
schema address.

Implemented fields include:

- cell id;
- fine candidate count;
- entropy;
- valid lift count;
- failed lift count;
- failed lift reason counts.

Tiny diagnostics are exact. Larger diagnostics may be sampled if a later
approved workplan expands the scale.
