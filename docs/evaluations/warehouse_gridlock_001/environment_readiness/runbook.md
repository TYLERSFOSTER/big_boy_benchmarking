# Runbook

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock graph-diagnostics \
  --artifact-root docs/evaluations/warehouse_gridlock_001/environment_readiness/artifacts/smoke_001 \
  --instance-id warehouse_gridlock_16x16_v001 \
  --run-label smoke_001

uv run python -m big_boy_benchmarking.cli warehouse-gridlock state-diagnostics \
  --artifact-root docs/evaluations/warehouse_gridlock_001/environment_readiness/artifacts/smoke_001 \
  --instance-id warehouse_gridlock_16x16_v001 \
  --run-label smoke_001

uv run python -m big_boy_benchmarking.cli warehouse-gridlock transition-smoke \
  --artifact-root docs/evaluations/warehouse_gridlock_001/environment_readiness/artifacts/smoke_001 \
  --instance-id warehouse_gridlock_16x16_v001 \
  --run-label smoke_001

uv run python -m big_boy_benchmarking.cli warehouse-gridlock readiness-docs \
  --artifact-root docs/evaluations/warehouse_gridlock_001/environment_readiness/artifacts/smoke_001 \
  --instance-id warehouse_gridlock_16x16_v001 \
  --run-label smoke_001
```
