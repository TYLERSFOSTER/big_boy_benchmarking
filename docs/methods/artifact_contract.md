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
directory must not change artifact meaning. For serious evaluation runs that
will receive durable readouts, the artifact root should be inside the repo-side
evaluation surface under `docs/evaluations/.../artifacts/`.

The first serious counterpoint learning evaluation adds evaluation-level
artifacts under:

```text
evaluations/counterpoint_first_serious_learning_v001/
```

Required serious-run evaluation files include:

```text
evaluation_manifest.json
evaluation_arm_manifest.json
evaluation_run_index.csv
evaluation_budget_lock.json
evaluation_aggregate_summary.json
evaluation_aggregate_table.csv
results/learning_curves.csv
results/timing_summary.csv
results/controller_summary.csv
results/schema_diagnostic_summary.csv
```

Tower-control and quotient-schema serious runs should additionally promote
raw tower evidence into evaluation-level tables:

```text
results/tower_shape_summary.csv
results/tier_occupancy_summary.csv
results/lift_failure_by_tier.csv
```

The raw per-run tower files remain source evidence:

```text
quotient_summary.json
control_events.csv
step_events.csv
lift_fiber_events.csv
```

But raw files alone are not sufficient for a serious human-readable tower
readout. The evaluation-level tower tables make quotient shape, active-tier
occupancy, concrete-step tier usage, and lift failures inspectable without
requiring a reader to reconstruct them from every run directory.

Calibration-path files are conditional on calibration runs:

```text
calibration_summary.json
calibration_run_index.csv
calibration_recommendation.md
```

Human-readable evaluation readouts live in repo-side readout surfaces under:

```text
docs/evaluations/
```

Each readout surface should include `readout_source.json` so generated prose
can point back to the repo-resident artifact root, source evaluation root,
aggregate tables, run index, expected-file policy, goal criteria, badge policy,
structural limit checks, and claim boundary.

For quotient-schema, tower-control, hidden-graph contraction, and
lift/action-realization evaluations, the source binding should include
structural limit checks. Those checks tell the human readout when apparent
mixed behavior is actually a structural-limit result, such as a first
projection that collapses `H` to `pi_0(H)` or nearly collapses all tier-`0`
states into one tier-`1` cell.

See also:

```text
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/artifact_table_to_readable_document_protocol.md
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
docs/methods/counterpoint_serious_learning.md
```
