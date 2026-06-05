# Evaluations

Checked-in files in this folder are repo-side evaluation readout surfaces. They
describe how to interpret evaluation artifacts and which claim boundaries
apply.

This folder is stage 2 and stage 3 of the benchmark workflow:

```text
2. Construct evaluations for environments.
3. Process raw run artifacts into repo-side human-readable readouts.
```

Each evaluation readout surface should contain a `readout_source.json` file.
That file binds the repo-side readout to the raw artifact root and source
evaluation root.

For durable serious evaluations, the raw artifact root also lives inside the
repo readout surface:

```text
docs/evaluations/<environment>/<evaluation>/artifacts/<run-label>/
```

Generated evaluation READMEs should start with local SVG status badges and a
compact `Status At A Glance` section. The badges are visual summaries only; they
must agree with the source binding, expected-file policy, goal criteria,
provenance status, and detailed verdict.

The command target for human-readable readout generation is the checked-in
`readout_source.json` file inside the repo-side evaluation folder, not the
README, the raw artifact root, or the raw evaluation root:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/<environment>/<evaluation>/readout_source.json
```

Follow:

```text
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

Generated artifact-local docs may still exist for immediate inspection, but the
durable human interpretation surface lives here.

## Available Evaluation Readouts

| Evaluation | Status | Readout | Claim boundary |
| --- | --- | --- | --- |
| `counterpoint_first_serious_learning_v001` | Complete structural-limit diagnostic | [counterpoint first serious learning](counterpoint_symbolic_v001/first_serious_learning/README.md) | Fixture-only claims for `counterpoint_symbolic_n3_small_v001`, locked budget, and `tensor_available_disabled`; no general tower-performance claim. |
| `counterpoint_one_third_schema_tower_diagnostics_v001` | Complete structural-limit diagnostic | [counterpoint one-third schema tower diagnostics](counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/README.md) | Diagnostic claims for source-local one-third contraction on `small` and `medium`; no direct-vs-tower performance claim and no tensor-enabled claim. |
| `counterpoint_noisy_rate_contraction_diagnostics_v001` | Complete smoke diagnostic; full validation pending | [counterpoint noisy-rate contraction diagnostics](counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/README.md) | Smoke-scale diagnostic claims for edge-global noisy-rate contraction on `small`; no full small+medium claim, no direct-vs-tower performance claim, and no tensor-enabled claim. |
| `counterpoint_contraction_fraction_sweep_diagnostics_v001` | Complete smoke diagnostic | [counterpoint contraction fraction sweep diagnostics](counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/README.md) | Diagnostic claims for source-local `n/18` contraction collapse behavior on the checked-in smoke budget; no learning-performance claim and no tensor-enabled claim. |
| `counterpoint_noisy_rate_full_tower_training_diagnostic_v001` | Complete smoke training-health diagnostic; main full budget pending | [counterpoint noisy-rate full-tower training diagnostic](counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/README.md) | Tower-only training-health claims for selected non-collapsed noisy-rate candidates; no direct-vs-tower comparison claim and no tensor-enabled claim. |
| `counterpoint_second_serious_schema_comparison_v001` | Complete implementation smoke; calibration/serious run pending | [counterpoint second serious schema comparison](counterpoint_symbolic_v001/second_serious_schema_comparison/README.md) | Matched Schema 0 versus Schema 1 comparison machinery and readout claims only; the checked-in run is smoke, not calibrated serious evidence. |
| `counterpoint_threshold_frontier_probe_v001` | Complete implementation smoke; meaningful frontier run pending | [counterpoint threshold frontier probe](counterpoint_symbolic_v001/threshold_frontier_probe/README.md) | Threshold-sweep machinery and frontier readout claims only; the checked-in smoke uses four episodes and is behaviorally claim-blocked under the 4-of-5 sustained-hit rule. |
| `counterpoint_small_paired_replicate_probe_v001` | Complete implementation smoke; meaningful frontier-selected run pending | [counterpoint small paired replicate probe](counterpoint_symbolic_v001/small_paired_replicate_probe/README.md) | Seed-paired replicate machinery and readout claims only; the checked-in smoke is behaviorally claim-blocked and the meaningful run awaits a frontier-selected threshold or PO override. |
