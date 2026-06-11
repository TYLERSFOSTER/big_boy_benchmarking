#!/usr/bin/env bash
set -euo pipefail

BBB_ROOT="${BBB_ROOT:-$(pwd)}"
RUN_LABEL="${RUN_LABEL:-tower_transformer_curriculum_train_001}"
EPISODES="${EPISODES:-128}"
REPLICATES="${REPLICATES:-1}"
SCHEMA_SEEDS="${SCHEMA_SEEDS:-1}"
MAX_SECONDS_START="${MAX_SECONDS_START:-2}"
MAX_SECONDS_END="${MAX_SECONDS_END:-64}"
CURRICULUM_RAMP_EPISODES="${CURRICULUM_RAMP_EPISODES:-1024}"
CHECKPOINT_EVERY_EPISODES="${CHECKPOINT_EVERY_EPISODES:-100}"
TRACE_EVERY_EPISODES="${TRACE_EVERY_EPISODES:-0}"
PROGRESS_EVERY_EPISODES="${PROGRESS_EVERY_EPISODES:-1}"
DEVICE="${DEVICE:-cpu}"

ARTIFACT_ROOT="${ARTIFACT_ROOT:-$BBB_ROOT/docs/evaluations/warehouse_gridlock_001/transformer_policy/artifacts/$RUN_LABEL}"
READINESS_SOURCE="${READINESS_SOURCE:-$BBB_ROOT/docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json}"

echo "Warehouse Gridlock transformer tower curriculum"
echo "artifact_root=$ARTIFACT_ROOT"
echo "readiness_source=$READINESS_SOURCE"
echo "run_label=$RUN_LABEL"

uv run python -m big_boy_benchmarking.cli warehouse-gridlock transformer-policy run \
  --repo-root "$BBB_ROOT" \
  --artifact-root "$ARTIFACT_ROOT" \
  --readiness-source "$READINESS_SOURCE" \
  --run-label "$RUN_LABEL" \
  --locked-by "${LOCKED_BY:-foster}" \
  --episodes "$EPISODES" \
  --replicates "$REPLICATES" \
  --schema-seeds "$SCHEMA_SEEDS" \
  --max-seconds-start "$MAX_SECONDS_START" \
  --max-seconds-end "$MAX_SECONDS_END" \
  --curriculum-ramp-episodes "$CURRICULUM_RAMP_EPISODES" \
  --checkpoint-every-episodes "$CHECKPOINT_EVERY_EPISODES" \
  --trace-episode-index 0 \
  --trace-episode-index final \
  --trace-every-episodes "$TRACE_EVERY_EPISODES" \
  --progress-every-episodes "$PROGRESS_EVERY_EPISODES" \
  --device "$DEVICE"

uv run python -m big_boy_benchmarking.cli warehouse-gridlock transformer-policy summarize \
  --repo-root "$BBB_ROOT" \
  --artifact-root "$ARTIFACT_ROOT"

echo "readout_source=$BBB_ROOT/docs/evaluations/warehouse_gridlock_001/transformer_policy/readout_source.json"

