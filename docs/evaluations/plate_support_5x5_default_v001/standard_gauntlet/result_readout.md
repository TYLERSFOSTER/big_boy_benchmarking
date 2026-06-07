# PlateSupport Standard Gauntlet Result Readout

Stages 1-7 completed. Stage 6 produced bounded paired comparison status `paired_comparison_positive_signal`, and Stage 7 produced the human readout/system-learning surface.

The target claim is bounded by the Stage 5 binary-success target and the
Stage 6 smoke budget. The result should not be read as a general claim about
all tower policies or all PlateSupport thresholds.

## Stage Narrative

### Stage 1: structural_and_tower_diagnostics

- Status: `complete`
- Claim status: `diagnostic_complete`
- Boundary: diagnostic-only; schema-sweep readiness if pass criteria hold

### Stage 2: contraction_schema_sweep

- Status: `complete`
- Claim status: `diagnostic_complete`
- Boundary: schema structural diagnostics and candidate signals only

### Stage 3: candidate_discovery

- Status: `complete`
- Claim status: `candidate_found`
- Boundary: candidate classification only; no training or comparison claim

### Stage 4: tower_training_health

- Status: `complete`
- Claim status: `trainable_clean`
- Boundary: tower-only training health evidence; no flat comparison claim

### Stage 5: threshold_frontier_calibration

- Status: `complete`
- Claim status: `threshold_calibrated`
- Boundary: threshold calibration evidence only; no tower-vs-flat comparison claim

### Stage 6: paired_replicate_comparison

- Status: `complete`
- Claim status: `paired_comparison_positive_signal`
- Boundary: bounded paired smoke comparison under the Stage 5 target and budget; not a general tower-performance claim

### Stage 7: readout_and_system_learning

- Status: `complete`
- Claim status: `readout_complete`
- Boundary: human readout and system-learning synthesis only

## Comparison Interpretation

Under this smoke Stage 6 budget, the selected tower candidate shows a limited positive target-hit signal relative to the direct baseline.

Tower mean reward was -27.2109375 versus direct -78.71875; tower invalid moves were 0 versus direct 2142.
