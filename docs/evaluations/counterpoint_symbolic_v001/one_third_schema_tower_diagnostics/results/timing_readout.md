# Timing Readout

The timing readout is based on the `24` per-run `timing_summary.json` files
under the source artifact root.

| Category | Total seconds | Mean per run | Minimum | Maximum | Small mean | Medium mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `linearization_setup` | 2.311357 | 0.096307 | 0.024732 | 0.231706 | 0.038582 | 0.154031 |
| `algorithm_online` | 24.432552 | 1.018023 | 0.445027 | 1.731106 | 0.457611 | 1.578435 |
| `total` | 26.743908 | 1.114330 | 0.470270 | 1.920395 | 0.496193 | 1.732466 |

The mode manifest says `algorithm_online` includes:

- environment reset and step;
- tower reset and update;
- controller decision;
- lift resolution;
- learner action and update.

The mode manifest excludes:

- compatibility readout;
- morphism construction.

The linearization mode is `tensor_available_disabled`. The linearization report
records `conversion_count = 0`, `enabled = false`, `numeric_backend = NUMPY`,
and no exported tensor conversion records. These timings are therefore
diagnostic runtime timings, not tensor-enabled performance measurements.
