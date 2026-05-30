# Counterpoint First Serious Learning Evaluation Readout

This repository directory is the human-readable readout surface for the
counterpoint first serious learning evaluation.

Source evaluation root:

```text
/private/tmp/bbb-counterpoint-serious-learning-serious-001/evaluations/counterpoint_first_serious_learning_v001
```

Source binding:

```text
readout_source.json
```

To regenerate this repo-side readout, point the protocol at this directory, not
at the raw artifact root:

```text
execute artifact-table readout pointed at folder /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning
```

Protocol applied:

```text
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

## One-Screen Verdict

All seven required arms produced machine-readable artifacts, and every run row
is marked `success`. That is artifact success, not behavioral success.

The direct environment arms and the empty-schema tower arm executed real
8-step episodes and received nonzero return. The non-empty tower arms completed
artifact runs but failed behaviorally: their episodes have mean return `0.0`,
mean step count `0.0`, and success rate `0%`. The per-run lift-fiber artifacts
show repeated `invalid_action_index` failures for those non-empty tower arms.

This run is useful diagnostic evidence about the current tower-control/action
realization surface. It does not support a positive tower-performance claim.

## Files

- [result_readout.md](result_readout.md): full human readout.
- [glossary.md](glossary.md): field and arm translations.
- [runbook.md](runbook.md): reconstructed commands and rerun notes.
- [artifact_index.md](artifact_index.md): evidence map with file purposes.
- [results/human_summary.md](results/human_summary.md): short result summary.
- [results/arm_readout_table.md](results/arm_readout_table.md): reader-facing arm table.
- [results/diagnostic_findings.md](results/diagnostic_findings.md): behavioral failure analysis.
- [results/timing_readout.md](results/timing_readout.md): timing summary with category boundaries.

## Claim Boundary

This readout is limited to `counterpoint_symbolic_n3_small_v001` under
`tensor_available_disabled`. Tensor execution was disabled. This is not a CUDA,
GPU, tensor-enabled, musical-quality, general superiority, or production
performance result.

## Missing Evidence

The evaluation root is missing these optional/provenance files:

- `evaluation_manifest.json`
- `evaluation_arm_manifest.json`
- `calibration_summary.json`
- `calibration_run_index.csv`
- `calibration_recommendation.md`

The aggregate, run index, budget lock, learning curves, timing summary,
controller summary, schema diagnostic summary, and per-run diagnostic files were
available and used for this readout.
