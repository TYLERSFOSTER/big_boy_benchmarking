# PlateSupport Standard Gauntlet Runbook

The canonical human-readout invocation is:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```

Do not point the protocol at the artifact root or infer the latest run.

The optional CLI equivalent is:

```text
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet readout build --readout-source /Users/foster/big_boy_benchmarking/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```
