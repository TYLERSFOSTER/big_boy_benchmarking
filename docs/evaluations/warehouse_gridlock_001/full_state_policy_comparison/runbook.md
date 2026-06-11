# Runbook

## Run Smoke

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-state-policy-comparison run \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/artifacts/tower_curriculum_train_2024_001 \
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \
  --run-label tower_curriculum_train_2024_001 \
  --locked-by foster \
  --episodes-per-arm 4 \
  --replicates-per-arm 1 \
  --schema-seeds 1 \
  --max-seconds-per-episode 128 \
  --projection-attempt-budget 64 \
  --progress-every-episodes 1
```

## Summarize

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-state-policy-comparison summarize \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/artifacts/tower_curriculum_train_2024_001
```

## Regenerate Human-Readable Readout

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/readout_source.json
```
