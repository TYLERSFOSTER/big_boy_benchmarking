# Runbook

The source run for this readout used `masked_8ep_001`.

## Rerun The Same Diagnostic

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock masked-direct-vs-live-lift-tower run \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/masked_8ep_001 \
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \
  --run-label masked_8ep_001 \
  --locked-by foster \
  --episodes-per-arm 8 \
  --replicates-per-arm 2 \
  --max-seconds-per-episode 128 \
  --candidate-proposals-per-step 256 \
  --max-active-robots 8 \
  --candidate-mix-id coordination_ready_sparse_interleaved_v001 \
  --progress-every-episodes 1
```

## Summarize The Artifact Root

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock masked-direct-vs-live-lift-tower summarize \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/masked_8ep_001
```

## Regenerate Human-Readable Readout

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/readout_source.json
```

## Watch Progress During A Run

The CLI displays a `tqdm` bar on stderr. It also writes:

```text
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/masked_8ep_001/progress_events.jsonl
```

Use:

```bash
tail -f docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/masked_8ep_001/progress_events.jsonl
```

## Render A Specific Episode

Generate an animated GIF from a recorded run's `step_events.csv`:

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock render-episode \
  --artifact-root docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/masked_8ep_001 \
  --arm-id warehouse_direct_admissible_masked \
  --replicate-index 0 \
  --schema-seed 0 \
  --episode-index 0
```

If `--output` is omitted, the GIF is written under:

```text
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/masked_8ep_001/replays/
```

Use `--arm-id warehouse_tower_live_lift_masked` to render the tower arm for
the same replicate, schema seed, and episode index.

## Scaling Up

For a more serious pilot, increase `--episodes-per-arm` first. Keep the same fairness knobs unless deliberately designing a new evaluation:

```text
--candidate-proposals-per-step 256
--max-active-robots 8
--candidate-mix-id coordination_ready_sparse_interleaved_v001
```
