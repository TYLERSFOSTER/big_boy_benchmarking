# PlateSupport Standard Gauntlet Runbook

## Status

Status: scaffolded, not yet run.

## Architecture Inspection

The architecture helper can be inspected without running an evaluation stage:

```text
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet inspect-architecture --repo-root /Users/foster/big_boy_benchmarking --run-label smoke_001
```

## Readout Generation

After run artifacts exist and `readout_source.json` points to them, use:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```

This command points at the repo-side source binding, not the artifact folder.
