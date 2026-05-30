# Runbook

```bash
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning calibrate \
  --artifact-root <artifact-root> \
  --instance-id tiny \
  --episodes 1 \
  --replicates 1 \
  --schema-seeds 1
```

```bash
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning run \
  --artifact-root <artifact-root> \
  --episodes <episode-count> \
  --replicates <replicate-count> \
  --schema-seeds <schema-seed-count> \
  --locked-by <operator-or-run-id>
```

```bash
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning summarize \
  --artifact-root <artifact-root>
```
