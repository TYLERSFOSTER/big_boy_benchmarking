# PlateSupport Contraction Schema Sweep Runbook

Run Stage 2 with:

```text
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet schema-sweep run \
  --repo-root <repo-root> \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \
  --stage1-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/structural_and_tower_diagnostics/readout_source.json \
  --source-local-ratio-numerator 1 \
  --source-local-ratio-denominator 18 \
  --run-label smoke_001 \
  --locked-by foster
```

For an iterated correction run, add:

```text
  --include-iterated-source-local-ratio \
  --iterated-source-local-ratio-denominator 144 \
  --iterated-source-local-ratio-denominator 72 \
  --iterated-source-local-ratio-denominator 36 \
  --iterated-source-local-ratio-denominator 18 \
  --iterated-source-local-max-iterations 32
```
