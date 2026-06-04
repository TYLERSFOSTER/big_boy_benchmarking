# Runbook

## Repaired Full-Iterated Run

```text
uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison run \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/full_iterated_p001_over_018_s0_r013_001 \
  --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json \
  --candidate-id counterpoint_symbolic_n3_small_v001-p001_over_018-schema0 \
  --schema1-tower-source full_iterated_noisy_rate \
  --instance-id small \
  --episodes 8 \
  --replicates 1 \
  --threshold-value 13.0 \
  --locked-by codex
```

## Summarize

```text
uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison summarize \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/full_iterated_p001_over_018_s0_r013_001
```

## Human Readout Protocol

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/readout_source.json
```
