# PlateSupport Threshold Frontier Calibration Runbook

Run Stage 5 with:

```text
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet threshold-calibration run \
  --repo-root <repo-root> \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \
  --training-health-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/tower_training_health/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster
```
