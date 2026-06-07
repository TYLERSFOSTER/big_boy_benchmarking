# Diagnostic Findings

## Candidate Gate Resolved

The earlier PlateSupport gauntlet issue was that candidate discovery had no trainable candidate to feed Stage 4. That is now resolved for `smoke_001`.

Evidence:

```text
artifacts/smoke_001/stages/candidate_discovery/results/downstream_training_health_input_summary.csv
```

Selected candidate:

```text
plate_support_candidate:source_local_ratio:0:342448ef2e
```

## Stage 4 Health Is Clean

Evidence:

```text
artifacts/smoke_001/stages/tower_training_health/results/candidate_training_health_summary.csv
```

Observed counts:

- 32 episodes;
- 1546 concrete steps;
- 1546 lift successes;
- 1546 learner updates;
- 0 runtime failures.

## Suite Is Not Complete

Stages 5-7 remain unimplemented or not run. This blocks calibration and paired-comparison claims.

## Suite-Level Provenance Gaps

The suite-level status table exists, but several suite-level manifest files expected by the post-run contract are absent. Stage-specific artifacts still support the Stage 4 claim, but the suite-level artifact contract needs another pass.
