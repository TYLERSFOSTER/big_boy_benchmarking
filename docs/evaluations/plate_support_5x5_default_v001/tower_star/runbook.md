# PlateSupport Tower-Star Guarded Lift Comparison Runbook

```bash
uv run python -m big_boy_benchmarking.cli plate-support tower-star run \
  --repo-root "$BBB_ROOT" \
  --artifact-root "$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/tower_star/artifacts/tower_star_001" \
  --parent-gauntlet-source "$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json" \
  --direct-star-source "$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json" \
  --run-label tower_star_001 \
  --locked-by foster

uv run python -m big_boy_benchmarking.cli plate-support tower-star summarize \
  --repo-root "$BBB_ROOT" \
  --artifact-root "$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/tower_star/artifacts/tower_star_001"
```
