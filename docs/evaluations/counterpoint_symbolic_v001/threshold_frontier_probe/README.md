# Counterpoint Threshold Frontier Probe

![Artifacts](badges/artifacts_complete.svg)
![Thresholds](badges/thresholds_tested.svg)
![Frontier](badges/frontier_status.svg)
![Shared](badges/highest_shared.svg)
![S1 Only](badges/schema1_only.svg)
![Recommend](badges/recommended_threshold.svg)
![Lift](badges/liftability_semantics.svg)
![Lift Fail](badges/lift_failures.svg)
![Provenance](badges/provenance_repo_artifacts.svg)

This repository directory is the human-readable readout surface for the threshold-frontier probe. The probe reruns the corrected Schema 0 versus Schema 1 comparison over a locked reward-threshold grid while holding candidate, seed policy, and small budget fixed.

## Status At A Glance

- Artifact evidence: `complete`.
- Run mode: `threshold_frontier_probe_v001`.
- Instance: `counterpoint_symbolic_n3_wide_20_108_span18_v001`.
- Threshold count: `2`.
- Pair rows: `2`.
- Claim status: `frontier_blocked_by_artifacts`.
- Recommended paired-replicate threshold: `13.0`.

## Liftability And Invariant Semantics

- Liftability semantics: `state_collapser_v072_pointwise`.
- Runtime action availability is pointwise: an abstract action must have a concrete lift executable from the current base state.

## Summary of Goals Behind this Evaluation

The goal is to locate the sustained-hit threshold frontier for Schema 0 and Schema 1 under one corrected widened candidate. This is a next-measure probe, not a final serious comparison.

## Summary of Methodology Behind this Evaluation

For each threshold value, the runner executes the existing corrected second-serious schema comparison under matched candidate, seed, budget, and persistence settings. The frontier layer then promotes each threshold's arm, pair, tower, lift, and timing evidence into top-level frontier tables.

## Frontier Summary

| highest_shared_passing_threshold | highest_schema0_passing_threshold | highest_schema1_passing_threshold | schema1_only_passing_thresholds | recommended_replicate_probe_threshold | claim_status |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  | 13.0 | frontier_blocked_by_artifacts |

## First Failure By Schema

| schema_class_id | first_failure_threshold | highest_passing_threshold | frontier_classification |
| --- | --- | --- | --- |
| schema0_no_contraction | 12.0 |  | no_passing_threshold_observed |
| schema1_noisy_rate_one_drop | 12.0 |  | no_passing_threshold_observed |

## Threshold Arm Rows

| threshold_value | schema_class_id | sustained_hit_count | run_count | sustained_hit_rate | post_hit_window_mean | threshold_margin_mean | passes_frontier_threshold |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 12.0 | schema0_no_contraction | 0 | 1 | 0.0 |  |  | False |
| 12.0 | schema1_noisy_rate_one_drop | 0 | 1 | 0.0 |  |  | False |
| 13.0 | schema0_no_contraction | 0 | 1 | 0.0 |  |  | False |
| 13.0 | schema1_noisy_rate_one_drop | 0 | 1 | 0.0 |  |  | False |

## Paired Threshold Rows

| threshold_value | schema0_hit_status | schema1_hit_status | schema1_minus_schema0_episodes_to_hit | schema1_minus_schema0_post_hit_window_mean | pair_status | claim_blocked |
| --- | --- | --- | --- | --- | --- | --- |
| 12.0 | transient_hit_only | transient_hit_only |  |  | blocked_or_non_sustained | True |
| 13.0 | transient_hit_only | transient_hit_only |  |  | blocked_or_non_sustained | True |

## Claim Boundary

This readout may support only a bounded single-candidate threshold-frontier interpretation. It may not claim broad abstraction superiority, statistical significance, tensor-enabled behavior, or musical quality.

To regenerate the human-readable readout, run:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/readout_source.json
```

Source artifact root:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts/smoke_001
```

## Clarifying Questions And Turns

### Evaluator Turn 1

_Open._

### Codex Turn 1

_Open._
