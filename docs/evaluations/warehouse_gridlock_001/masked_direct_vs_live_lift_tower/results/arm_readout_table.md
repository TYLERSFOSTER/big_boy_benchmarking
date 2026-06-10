# Arm Readout Table

| Arm | Mean reward | Median reward | Episodes | Terminal successes | Mean final boxes | Mean final robots | Mean valid steps | Mean invalid steps | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Direct masked control | 379.9375 | 341.5 | 16 | 0 | 0.0 | 6.1875 | 128.0 | 0.0 | Baseline ran cleanly but did not solve the task. |
| Tower live-lift control | 379.9375 | 341.5 | 16 | 0 | 0.0 | 6.1875 | 128.0 | 0.0 | Tower ran cleanly with no live-lift failures but did not outperform direct. |

Every paired direct-vs-tower comparison had zero delta on reward, box progress, robot progress, terminal success, valid steps, candidate count, and query count.
