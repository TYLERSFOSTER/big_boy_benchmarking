#!/usr/bin/env bash
set -euo pipefail

BBB_ROOT="${BBB_ROOT:-$(git rev-parse --show-toplevel)}"
RUN_LABEL="${RUN_LABEL:-tower_curriculum_train_001}"
EPISODES_PER_ARM="${EPISODES_PER_ARM:-1024}"
REPLICATES_PER_ARM="${REPLICATES_PER_ARM:-1}"
SCHEMA_SEEDS="${SCHEMA_SEEDS:-1}"
SEED="${SEED:-0}"
LOCKED_BY="${LOCKED_BY:-foster}"
PROJECTION_ATTEMPT_BUDGET="${PROJECTION_ATTEMPT_BUDGET:-64}"
PROGRESS_EVERY_EPISODES="${PROGRESS_EVERY_EPISODES:-1}"

ARTIFACT_ROOT="${ARTIFACT_ROOT:-$BBB_ROOT/docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/artifacts/$RUN_LABEL}"
READINESS_SOURCE="${READINESS_SOURCE:-$BBB_ROOT/docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json}"

cd "$BBB_ROOT"

uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-state-policy-comparison run \
  --repo-root "$BBB_ROOT" \
  --artifact-root "$ARTIFACT_ROOT" \
  --readiness-source "$READINESS_SOURCE" \
  --run-label "$RUN_LABEL" \
  --locked-by "$LOCKED_BY" \
  --episodes-per-arm "$EPISODES_PER_ARM" \
  --replicates-per-arm "$REPLICATES_PER_ARM" \
  --schema-seeds "$SCHEMA_SEEDS" \
  --max-seconds-per-episode 64 \
  --max-seconds-curriculum-start 2 \
  --max-seconds-curriculum-end 64 \
  --max-seconds-curriculum-span-episodes 1024 \
  --active-arm-id warehouse_tower_full_state_policy_live_lift_masked \
  --projection-attempt-budget "$PROJECTION_ATTEMPT_BUDGET" \
  --progress-every-episodes "$PROGRESS_EVERY_EPISODES" \
  --seed "$SEED"

uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-state-policy-comparison summarize \
  --repo-root "$BBB_ROOT" \
  --artifact-root "$ARTIFACT_ROOT"
