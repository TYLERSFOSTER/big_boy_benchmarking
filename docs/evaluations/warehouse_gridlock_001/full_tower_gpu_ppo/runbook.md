# Runbook

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-tower-gpu-ppo run \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/artifacts/tower_movie_only_100000_001 \
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \
  --run-label tower_movie_only_100000_001 \
  --locked-by foster \
  --profile smoke_cpu
```
