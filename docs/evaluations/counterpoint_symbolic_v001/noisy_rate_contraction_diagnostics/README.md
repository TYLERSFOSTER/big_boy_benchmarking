# Counterpoint Noisy-Rate Contraction Diagnostics

![Artifacts: Complete](badges/artifacts_complete.svg)
![Sweep: No Collapse](badges/noisy_rate_sweep.svg)
![Coverage: Min 0.54](badges/source_coverage.svg)
![Selection: Consistent](badges/selection_contract.svg)
![Runtime: Executable](badges/runtime_executable.svg)
![Scope: Diagnostic Only](badges/scope_diagnostic_only.svg)
![Provenance: Repo Artifacts](badges/provenance_repo_artifacts.svg)

This repository directory is the human-readable readout surface for the counterpoint noisy-rate contraction diagnostic.

## Status At A Glance

- Artifact evidence: complete.
- Sweep verdict: no observed full collapse.
- First full-collapse requested rate: `none observed`.
- First near-collapse requested rate: `none observed`.
- Last nontrivial requested rate: `0.05555555555555555`.
- Minimum selected-source share across non-control arms: `0.5402234636871508`.
- Maximum zero-selected-source count in an arm: `3580`.
- Metadata/runtime selected-edge consistency: `True`.
- Concrete steps emitted across this artifact run: `8`.
- Claim scope: diagnostic only; this is not a learning-performance comparison.

## One-Screen Verdict

The custom diagnostic run completed and produced the required machine-readable noisy-rate summary tables.

The key diagnostic distinction is expected edge rate versus realized source coverage. A low requested rate may select a small number of edges overall while leaving many source states with zero selected outgoing edges. That behavior is intentional here; it is the direct contrast with the earlier source-local floor rule.

On this custom diagnostic run, the observed sweep verdict is `no_collapse`.

## Source Evaluation Root

```text
<repo-root>/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/artifacts/wide_span18_p001_over018_s0_001/evaluations/counterpoint_noisy_rate_contraction_diagnostics_v001
```

## Summary of Goals Behind this Evaluation

This evaluation keeps the existing `counterpoint_symbolic_v001` environment fixed and varies only the contraction selector. It asks whether an edge-global noisy expected-rate selector avoids the immediate-collapse behavior seen in the source-local fraction diagnostic.

A smoke-scoped artifact run is implementation evidence only. A full-validation artifact run can support broader structural diagnostic claims, but still cannot support learning-performance claims without a separate comparison evaluation.

## Summary of Methodology Behind this Evaluation

For each configured arm, BBB assigns every canonical counterpoint edge a stable SHA-256 score using the selector rule id, instance id, schema seed, and edge key. An edge is scheduled when that score is below the requested rate. No source-local minimum-one floor is used, so sources can contribute zero selected outgoing edges.

This custom diagnostic run used instances `counterpoint_symbolic_n3_wide_20_108_span18_v001`, schema seeds `0`, rates `1/18`, replicates `1`, and episodes `1`.

## Selection Table

| Arm | Requested Rate | Selected Edges | Edge Share | Expected Edges | Residual |
| --- | ---: | ---: | ---: | ---: | ---: |
| no_contraction_control | 0.00000 | 0 | 0.00000 | 0.00 | 0.00 |
| p001_over_018 | 0.05556 | 2800 | 0.05694 | 2731.78 | 68.22 |

## Source Coverage Table

| Arm | Rate | Selected Sources | Zero-Selected Sources | Selected Source Share | Class |
| --- | ---: | ---: | ---: | ---: | --- |
| no_contraction_control | 0.00000 | 0 | 3580 | 0.000 | no_contraction_control |
| p001_over_018 | 0.05556 | 1934 | 1646 | 0.540 | partial_source_coverage |

## Tier Shape Table

| Arm | Rate | Tier | State Cells | Active Action Cells | Raw Historical Action Records | Largest Cell Share | Class |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| no_contraction_control | 0.00000 | 0 | 3580 | 49172 | 49172 | 0.000 | identity_or_base |
| p001_over_018 | 0.05556 | 0 | 3580 | 49172 | 49172 | 0.000 | identity_or_base |
| p001_over_018 | 0.05556 | 1 | 1035 | 24258 | 3786096 | 0.587 | compressed |

The tier table intentionally separates active action-cell count from raw historical action-cell record count. A collapsed tier can have zero live executable action cells while retaining many raw historical records from tower construction; the raw count is not the live control surface.

## Threshold Table

| Instance | Schema Seed | First Full Rate | First Near Rate | Last Nontrivial Rate | First High Coverage Rate | Verdict |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| counterpoint_symbolic_n3_wide_20_108_span18_v001 | 0 | none | none | 0.05555555555555555 | none | no_collapse |

## Endpoint-Coalescence Table

| Arm | Rate | Processed Edges | Useful Coalescences | State Cells After Block | Source Coverage | First Singleton Edge Index |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| no_contraction_control | 0.00000 | 0 | 0 | 3580 | 0.0 | none |
| p001_over_018 | 0.05556 | 2800 | 2545 | 1035 | 0.5402234636871508 | none |

## Files

- [readout_source.json](readout_source.json): source binding from this repo readout surface to raw artifact tables.
- [method.md](method.md): methodology and budget summary.
- [runbook.md](runbook.md): rerun, summarize, and human-readout commands.
- [artifact_index.md](artifact_index.md): evidence map with file purposes.
- [glossary.md](glossary.md): field and mechanism translations.
- [results/summary.md](results/summary.md): compact reader-facing result summary.
- [results/noisy_rate_thresholds.md](results/noisy_rate_thresholds.md): threshold details.
- [results/source_coverage.md](results/source_coverage.md): source-coverage details.

## Claim Boundary

This readout may claim that the custom diagnostic run completed, produced repo-resident artifacts, checked metadata/runtime selected-edge consistency, reported source coverage, and reported collapse threshold fields shown above.

This readout may not claim tower learning advantage, direct-vs-tower comparison, musical quality, tensor-enabled runtime behavior, CUDA/GPU behavior, production performance, or that the counterpoint environment is degenerate.

To regenerate the human-readable readout, run:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json
```

## Clarifying Questions And Turns

_No active public clarification turns are recorded for this readout._
