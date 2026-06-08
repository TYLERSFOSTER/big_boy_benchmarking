# PlateSupport Candidate Discovery Runbook

Run Stage 3 with:

```text
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet candidate-discovery run \
  --repo-root <repo-root> \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \
  --schema-sweep-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/contraction_schema_sweep/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster
```
