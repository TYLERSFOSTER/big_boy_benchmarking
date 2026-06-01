# Counterpoint Contraction Fraction Sweep Diagnostics

![Artifacts: Complete](badges/artifacts_complete.svg)
![Sweep: Immediate Collapse](badges/sweep_status.svg)
![n=6/18: Matches Legacy](badges/legacy_endpoint.svg)
![Runtime: Executable](badges/runtime_executable.svg)
![Scope: Diagnostic Only](badges/scope_diagnostic_only.svg)
![Provenance: Repo Artifacts](badges/provenance_repo_artifacts.svg)

This repository directory is the human-readable readout surface for the counterpoint n-over-18 contraction fraction sweep diagnostic.

## Status At A Glance

- Artifact evidence: complete.
- Sweep verdict: immediate collapse.
- First full-collapse numerator: `1`.
- First near-collapse numerator: `1`.
- Last nontrivial numerator: `none observed`.
- Legacy endpoint check for `6/18`: `True`.
- Concrete steps emitted across this artifact run: `21`.
- Claim scope: diagnostic only; this is not a learning-performance comparison.

## One-Screen Verdict

The smoke run completed and produced the required machine-readable summary tables.

On this smoke run, `1/18` is the first observed full-collapse numerator. When that value is `1/18`, the current single-block source-local fraction semantics are already severe at the weakest requested fraction.

`6/18` matches the legacy one-third first scheduled block in the generated equivalence table, so the sweep endpoint is comparable to the old one-third diagnostic for this run configuration.

## Source Evaluation Root

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/artifacts/smoke_001/evaluations/counterpoint_contraction_fraction_sweep_diagnostics_v001
```

## Summary of Goals Behind this Evaluation

This evaluation keeps the existing `counterpoint_symbolic_v001` environment fixed and varies only the scheduled contraction fraction. It asks whether small `n/18` fractions preserve meaningful first-tier structure before higher fractions collapse.

A smoke-scoped artifact run is implementation evidence only. A full-validation artifact run can support broader structural diagnostic claims, but still cannot support learning-performance claims without a separate comparison evaluation.

## Summary of Methodology Behind this Evaluation

For each configured arm, BBB selects one source-local scheduled outgoing-edge block using `max(1, ceil(out_degree * n / 18))`. Remaining edges are unscheduled for that arm. The tower is then built through the existing `state_collapser` partition tower path and exercised through the existing active-tier controller runtime.

This smoke run used instances `counterpoint_symbolic_n3_small_v001`, schema seeds `0`, numerators `1`, `6`, denominator `18`, replicates `1`, and episodes `1`.

## Tier Shape Table

| Arm | Tier | State Cells | Active Action Cells | Raw Historical Action Records | Largest Cell Share | Class |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| no_contraction_control | 0 | 108 | 1140 | 1140 | 0.009 | identity_or_base |
| n01_over_18 | 0 | 108 | 1140 | 1140 | 0.009 | identity_or_base |
| n01_over_18 | 1 | 1 | 0 | 1532 | 1.000 | full_collapse |
| n06_over_18 | 0 | 108 | 1140 | 1140 | 0.009 | identity_or_base |
| n06_over_18 | 1 | 1 | 0 | 17147 | 1.000 | full_collapse |

The tier table intentionally separates active action-cell count from raw historical action-cell record count. A collapsed tier can have zero live executable action cells while retaining many raw historical records from tower construction; the raw count is not the live control surface.

## Schema Width Table

| Arm | Scheduled Edges | Edge Share | Edges/(States-1) | Monotone |
| --- | ---: | ---: | ---: | --- |
| no_contraction_control | 0 | 0.000 | 0.0 |  |
| n01_over_18 | 112 | 0.098 | 1.0467289719626167 | True |
| n06_over_18 | 408 | 0.358 | 3.8130841121495327 | True |

## Threshold Table

| Instance | Schema Seed | First Full Collapse n | First Near Collapse n | Last Nontrivial n | n06 Matches Legacy | Verdict |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| counterpoint_symbolic_n3_small_v001 | 0 | 1 | 1 | none | True | immediate_collapse |

## Endpoint-Coalescence Table

| Arm | Processed Edges | Useful Coalescences | Redundant/Internal Edges | State Cells After Block | First Singleton Edge Index | Collapse Used Most Block |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| no_contraction_control | 0 | 0 | 0 | 108 | none |  |
| n01_over_18 | 112 | 107 | 5 | 1 | 112 | True |
| n06_over_18 | 408 | 107 | 301 | 1 | 405 | True |

## Files

- [readout_source.json](readout_source.json): source binding from this repo readout surface to raw artifact tables.
- [method.md](method.md): methodology and budget summary.
- [runbook.md](runbook.md): rerun, summarize, and human-readout commands.
- [artifact_index.md](artifact_index.md): evidence map with file purposes.
- [glossary.md](glossary.md): field and mechanism translations.
- [results/summary.md](results/summary.md): compact reader-facing result summary.
- [results/sweep_verdict.md](results/sweep_verdict.md): sweep verdict details.
- [results/threshold_table.md](results/threshold_table.md): threshold table.

## Claim Boundary

This readout may claim that the smoke run completed, produced repo-resident artifacts, checked `6/18` against the old first one-third block, and reported the collapse threshold fields shown above.

This readout may not claim tower learning advantage, direct-vs-tower comparison, musical quality, tensor-enabled runtime behavior, CUDA/GPU behavior, production performance, or that the counterpoint environment is degenerate.

To regenerate the human-readable readout, run:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/readout_source.json
```

## Clarifying Questions And Turns

#### Project Owner / Evaluator Turn

> Tell me as much as you can about this $1/18$ collapse.

#### Embedded Engineering Consultant / Codex Turn

> ...

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> ...

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> ...
