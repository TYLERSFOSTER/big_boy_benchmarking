# Timing Readout

Per-run timing evidence lives under each run directory as `timing_segments.csv` and `timing_summary.json`. Evaluation-level timing summary rows are in:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001/evaluations/counterpoint_second_serious_schema_comparison_v001/results/timing_summary.csv
```

| Schema | Algorithm Online Seconds | Linearization Setup Seconds | Total Seconds |
| --- | ---: | ---: | ---: |
| `schema0_no_contraction` | 0.212 | 0.005 | 0.217 |
| `schema1_noisy_rate_one_drop` | 0.232 | 0.006 | 0.238 |

These timings are included for engineering inspection only. The budget is a
two-run smoke diagnostic, so the readout must not make method-speed claims from
these wall-clock values.
