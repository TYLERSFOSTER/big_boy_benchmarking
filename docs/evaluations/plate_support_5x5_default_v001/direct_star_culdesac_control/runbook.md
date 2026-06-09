# PlateSupport Direct-Star Cul-de-sac Control Runbook

Run the diagnostic with:

```text
uv run python -m big_boy_benchmarking.cli plate-support direct-star-culdesac-control run \
  --repo-root . \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/guarded_001 \
  --parent-gauntlet-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json \
  --run-label guarded_001 \
  --locked-by foster
```

Regenerate the human-readable readout with:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json
```
