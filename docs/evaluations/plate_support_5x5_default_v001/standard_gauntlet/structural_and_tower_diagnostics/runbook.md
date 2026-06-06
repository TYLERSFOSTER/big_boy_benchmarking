# PlateSupport Structural And Tower Diagnostics Runbook

Run Stage 1 with:

```text
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet structural-diagnostics run \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \
  --readiness-source docs/environments/plate_support_5x5_default_v001/readiness/dev_001/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster
```

Generate human-readable docs from:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/structural_and_tower_diagnostics/readout_source.json
```
