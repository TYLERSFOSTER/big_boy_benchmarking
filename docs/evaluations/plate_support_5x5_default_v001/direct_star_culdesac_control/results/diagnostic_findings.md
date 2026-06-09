# Diagnostic Findings

## Guard Filter Summary

| Arm | Guard | Mean Before | Mean After | Invalid Filtered | Self-Loop Filtered |
| --- | --- | ---: | ---: | ---: | ---: |
| `direct_raw` | `raw` | 12.0 | 12.0 | 0.0 | 0.0 |
| `direct_invalid_guard` | `invalid_guard` | 12.0 | 7.155611748687026 | 4.844388251312974 | 0.0 |
| `direct_nonself_guard` | `nonself_guard` | 12.0 | 5.483341154387611 | 4.74331299859221 | 6.516658845612389 |
| `tower_selected_candidate` | `tower_executable_action_cells` | 5.373002663115845 | 5.373002663115845 | 0.0 | 0.0 |

## Claim Effect

The guarded controls are stronger than the tower on the binary target in this run,
so the report blocks the claim that the prior tower advantage survived an
equivalent decision-surface control.
