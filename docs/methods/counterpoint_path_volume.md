# Counterpoint Path Volume

Source blueprint:

- `docs/design/first_counterpoint_environment/01_002_counterpoint_hidden_graph_and_contraction_schema_benchmark_blueprint.md`

Path-volume diagnostics measure the size of the legal hidden graph path set.

Implemented tiny diagnostics include:

- exact paths of exactly length `K`;
- exact paths up to length `K`;
- deterministic sampled estimates for larger or policy-effective probes.

The tiny fixture currently has exact graph/path enumeration. Sampled
path-volume artifacts must include `diagnostic_sampling_seed` and
`exact_or_sampled`.
