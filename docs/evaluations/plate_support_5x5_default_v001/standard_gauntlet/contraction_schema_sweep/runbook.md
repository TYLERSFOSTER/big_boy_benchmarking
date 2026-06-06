# PlateSupport Contraction Schema Sweep Runbook

Run Stage 2 with:

```text
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet schema-sweep run \
  --repo-root /Users/foster/big_boy_benchmarking \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \
  --stage1-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/structural_and_tower_diagnostics/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster
```
