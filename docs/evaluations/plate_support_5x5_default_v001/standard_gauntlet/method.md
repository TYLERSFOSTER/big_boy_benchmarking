# PlateSupport Standard Gauntlet Method

The suite runs a staged benchmark pipeline: structural diagnostics,
contraction-schema sweep, candidate discovery, tower-training health,
threshold calibration, paired comparison, and human readout synthesis.

The paired comparison uses explicit seed bundles shared by active arms.
The Stage 6 direct concrete baseline and selected tower candidate are
trained with the same episode budget and evaluated against the Stage 5
target policy.

If Stage 4 includes a trainable iterated source-local ratio candidate,
the readout emits iterated-candidate and tier-count badges from the
Stage 4 candidate-training-health table.

The readout was generated from this explicit source binding:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```
