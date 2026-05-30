# Artifact Contract

The artifact contract defines where benchmark evidence lives and which files
bind run identity.

The initial schema marker is:

```text
artifacts/schemas/artifact_schema_v001.json
```

The initial schema version is:

```text
bbb.v001
```

Tensorization-aware smoke and diagnostic runs add a run-level file:

```text
linearization_manifest.json
```

That manifest records:

- the local BBB linearization mode id;
- `state_collapser.training.LinearizationConfig.to_dict()`;
- `state_collapser.training.LinearizationReport.to_dict()`;
- whether conversion/debug records were exported.

The manifest exists so future results do not blur pre-linearization control
flow with tensor-capable-disabled or tensor-enabled benchmark conditions.

Artifacts are written under an explicit artifact root. The current working
directory must not change artifact meaning.

The first serious counterpoint learning evaluation adds evaluation-level
artifacts under:

```text
evaluations/counterpoint_first_serious_learning_v001/
```

Core files include:

```text
evaluation_manifest.json
evaluation_arm_manifest.json
evaluation_run_index.csv
evaluation_budget_lock.json
calibration_summary.json
calibration_run_index.csv
calibration_recommendation.md
evaluation_aggregate_summary.json
evaluation_aggregate_table.csv
results/learning_curves.csv
results/timing_summary.csv
results/controller_summary.csv
results/schema_diagnostic_summary.csv
```

See also:

```text
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
docs/methods/counterpoint_serious_learning.md
```
