# PlateSupport Paired Replicate Comparison Runbook

Run Stage 6 with:

```text
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet paired-comparison run \
  --repo-root <repo-root> \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \
  --candidate-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/candidate_discovery/readout_source.json \
  --training-health-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/tower_training_health/readout_source.json \
  --threshold-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/threshold_frontier_calibration/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster
```
