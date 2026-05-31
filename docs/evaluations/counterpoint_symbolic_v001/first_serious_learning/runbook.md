# Runbook

## Source Artifact Root

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/v071_002_clean
```

## Source Evaluation Root

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/v071_002_clean/evaluations/counterpoint_first_serious_learning_v001
```

## Reconstructed Serious Run Command

The run manifests record command family
`python -m big_boy_benchmarking.cli counterpoint serious-learning run`, and the
budget lock records the budget. The command shape for this artifact set is:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning run \
  --artifact-root /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/v071_002_clean \
  --instance-id small \
  --episodes 16 \
  --replicates 4 \
  --schema-seeds 3 \
  --locked-by foster \
  --linearization-mode tensor_available_disabled
```

## Regenerate Aggregate Tables

```bash
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning summarize \
  --artifact-root /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/v071_002_clean
```

## Regenerate Human Readout

Use the protocol surface:

```text
execute artifact-table readout pointed at folder /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning
```

## First Files To Inspect

For the main result:

```text
evaluation_aggregate_table.csv
results/learning_curves.csv
results/controller_summary.csv
```

For random-schema failure details:

```text
runs/counterpoint_symbolic_v001_first_serious_learning_tower_v001/runs/<run-id>/lift_fiber_events.csv
runs/counterpoint_symbolic_v001_first_serious_learning_tower_v001/runs/<run-id>/control_events.csv
```

The most important random-schema failure rows are:

```text
tower_random_balanced_exploit_explore_tabular_q schema seeds 0 and 1
tower_random_unbalanced_exploit_explore_tabular_q schema seed 1
```

Those rows record `no_lift_candidate_from_current_state`, while successful
tower arms record concrete realized actions.

For linearization/backend discipline:

```text
runs/<family-id>/runs/<run-id>/linearization_manifest.json
```
