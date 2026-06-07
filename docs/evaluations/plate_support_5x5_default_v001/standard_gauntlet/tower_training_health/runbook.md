# PlateSupport Tower Training Health Runbook

Run Stage 4 with:

```text
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet tower-training-health run \
  --repo-root /Users/foster/big_boy_benchmarking \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \
  --candidate-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/candidate_discovery/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster
```
