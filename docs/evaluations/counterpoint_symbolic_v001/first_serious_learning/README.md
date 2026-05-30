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

- [readout_source.json](readout_source.json): source binding from this repo readout surface to the raw artifact tables.
- [result_readout.md](result_readout.md): full human readout.
- [glossary.md](glossary.md): field and arm translations.
- [runbook.md](runbook.md): reconstructed commands and rerun notes.
- [artifact_index.md](artifact_index.md): evidence map with file purposes.
- [results/summary.md](results/summary.md): compact reader-facing result summary.
- [results/human_summary.md](results/human_summary.md): short result summary.
- [results/arm_readout_table.md](results/arm_readout_table.md): reader-facing arm table.
- [results/diagnostic_findings.md](results/diagnostic_findings.md): behavioral failure analysis.
- [results/timing_readout.md](results/timing_readout.md): timing summary with category boundaries.

## Claim Boundary

This readout is limited to `counterpoint_symbolic_n3_small_v001` under
`tensor_available_disabled`. Tensor execution was disabled. This is not a CUDA,
GPU, tensor-enabled, musical-quality, general superiority, or production
performance result.

## Provenance Status

The source binding for this readout is `readout_source.json`. It identifies the
source artifact root, source evaluation root, source tables, environment
instance, linearization mode, and claim boundary. It does not currently encode
the full expected-file policy for the evaluation.

Relative to the first serious learning blueprint, these evaluation-level
manifest files are expected but absent from the source evaluation root:

- `evaluation_manifest.json`
- `evaluation_arm_manifest.json`

These calibration files are also absent, but they should be read differently:
they are expected for the calibration path, not necessarily for a manually
locked serious run unless the locked run was supposed to be calibration-derived:

- `calibration_summary.json`
- `calibration_run_index.csv`
- `calibration_recommendation.md`

The aggregate, run index, budget lock, learning curves, timing summary,
controller summary, schema diagnostic summary, and per-run diagnostic files were
available and used for this readout.

## Clarifying Questions And Turns

### Project Owner / Evaluator Turn

Explain why that stuff is missing.

### Embedded Engineering Consultant / Codex Turn

Those files are missing because this artifact root appears to represent the
locked serious-run/summarize path, not the calibration path.

In the current implementation, `run_calibration` writes:

- `evaluation_manifest.json`
- `evaluation_arm_manifest.json`
- `calibration_summary.json`
- `calibration_run_index.csv`
- `calibration_recommendation.md`

The locked serious run path, `run_budget_locked_serious_learning`, writes:

- `evaluation_budget_lock.json`
- `evaluation_run_index.csv`

Then `summarize` can still aggregate and document the run from the budget lock,
run index, aggregate table, learning curves, timing summary, controller summary,
schema diagnostics, and per-run artifacts.

So this is not evidence that those files were deleted or that the run is
uninterpretable. It is a provenance/contract gap in the current serious-run
pipeline: the files are part of the intended evaluation-level artifact contract,
but this particular source artifact root was produced through a path that did
not create the calibration/setup provenance files.

Claim effect: the behavioral readout remains valid as diagnostic evidence, but
the provenance is weaker than the intended contract. A future implementation
pass should make the serious-run path write `evaluation_manifest.json` and
`evaluation_arm_manifest.json`, and should either require calibration artifacts
for a calibration-derived locked run or explicitly mark calibration files as
not applicable for a manually locked serious run.



### Project Owner / Evaluator Turn

Is there not a manifest where we pointed the human-readablility protocol that explains enough about the environment and evaluation that we wouldn't say things are "missing" when there was no epectation for them to be there? Or was there an expectation in this case?

### Embedded Engineering Consultant / Codex Turn

Yes, this was a real distinction and the report language was too blunt.

There is a source-binding manifest for the human-readability protocol:
`readout_source.json`. It tells the readout where the artifact tables live and
records the evaluation id, environment instance, artifact schema version,
linearization mode, and claim boundary. That is enough to know what source files
were used. It is not currently enough to know, by itself, which absent files
were expected versus not applicable.

The expectation comes from the serious learning blueprint and the evaluation
path contract:

- `evaluation_manifest.json` and `evaluation_arm_manifest.json` are expected
  evaluation-level artifacts for this serious evaluation. Their absence is a
  real provenance gap.
- `calibration_summary.json`, `calibration_run_index.csv`, and
  `calibration_recommendation.md` are expected for the calibration path. If this
  source artifact root was produced as a manually locked serious run without
  calibration, those files should be described as absent/not applicable, not as
  missing evidence.

I updated the section above from `Missing Evidence` to `Provenance Status` and
split those cases. The remaining design gap is that `readout_source.json`
should probably grow an explicit expected-file policy so future readouts do not
have to infer this from blueprint/code context.
