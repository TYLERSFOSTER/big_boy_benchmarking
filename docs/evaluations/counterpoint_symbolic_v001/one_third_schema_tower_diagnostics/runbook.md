# Runbook

## Regenerate The Artifact Run

Use a repo-resident artifact root under this evaluation readout surface:

```bash
export BBB_COUNTERPOINT_EVAL_ROOT="$PWD/docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/small_medium_validation_001"
```

Run the diagnostic budget:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics run \
  --artifact-root "$BBB_COUNTERPOINT_EVAL_ROOT" \
  --instance-ids small,medium \
  --schema-seeds 0,1,2 \
  --replicates 4 \
  --episodes 16 \
  --base-seed 0 \
  --locked-by cli \
  --linearization-mode tensor_available_disabled
```

Aggregate the machine-readable evaluation tables:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics summarize \
  --artifact-root "$BBB_COUNTERPOINT_EVAL_ROOT" \
  --docs-root "$PWD/docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics"
```

The `summarize` command refreshes evaluation-owned aggregate tables and
lightweight generated docs. It is not a substitute for the full human-readable
readout protocol.

## Regenerate The Human Readout

Execute the readout protocol against the checked-in source binding:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/readout_source.json
```

The command target is the source binding, not the README, artifact root, or raw
evaluation root.

## Current Source Artifact Set

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/small_medium_validation_001
```

Current source evaluation root:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001
```
