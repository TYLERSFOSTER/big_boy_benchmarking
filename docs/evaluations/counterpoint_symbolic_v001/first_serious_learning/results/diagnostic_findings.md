# Diagnostic Findings

## Finding 1: First Projection Collapse Controls Interpretation

The central diagnostic is structural. Non-empty tower arms either fully collapse
the first quotient projection or create a giant tier-`1` fiber that contains
most tier-`0` states. That means ordinary learner-performance language is
blocked unless a later evaluation explicitly controls for quotient collapse.

This readout should therefore classify the non-empty tower result as a
structural-limit diagnostic, not as ordinary mixed non-performance.

## Finding 2: Random Balanced Is Schema-Seed Dependent Under The Structural Limit

Random balanced tower behavior:

| Schema seed | Mean return | Mean steps | Episode success | Main failure |
| ---: | ---: | ---: | ---: | --- |
| 0 | 0.000 | 0.0 | 0% | `no_lift_candidate_from_current_state` |
| 1 | 0.000 | 0.0 | 0% | `no_lift_candidate_from_current_state` |
| 2 | 12.710 | 8.0 | 100% | none observed |

Across all schema seeds this becomes mean return `4.237`, mean step count
`2.7`, and 33% episode success.

## Finding 3: Random Unbalanced Is Also Schema-Seed Dependent

Random unbalanced tower behavior:

| Schema seed | Mean return | Mean steps | Episode success | Main failure |
| ---: | ---: | ---: | ---: | --- |
| 0 | 12.710 | 8.0 | 100% | none observed |
| 1 | 0.000 | 0.0 | 0% | `no_lift_candidate_from_current_state` |
| 2 | 12.710 | 8.0 | 100% | none observed |

Across all schema seeds this becomes mean return `8.473`, mean step count
`5.3`, and 67% episode success.

## Finding 4: Structured Motion And Bad/Adversarial Execute Under Full Collapse

The structured-motion and bad/adversarial arms execute 8-step episodes, but
they do so under fully collapsed first projections. Their execution therefore
does not separate useful tower control from the collapsed schema/runtime
condition.

| Arm | Mean return | Delta vs empty tower |
| --- | ---: | ---: |
| Empty-schema tower | 12.710 | +0.000 |
| Structured motion tower | 12.710 | +0.000 |
| Bad/adversarial tower | 12.710 | +0.000 |

This means the benchmark cannot claim that structured motion is a better
contraction, and it also cannot treat the bad/adversarial arm as an effective
negative control for this budget. The claim boundary is structural: the first
projection has already collapsed too much for ordinary performance comparison.

## Finding 5: Provenance Classification

The source evaluation root has absent provenance/calibration files. They are
not all the same kind of absence:

| File | Classification | Interpretation |
| --- | --- | --- |
| `evaluation_manifest.json` | `expected_missing_gap` | Expected evaluation-level provenance is absent. |
| `evaluation_arm_manifest.json` | `expected_missing_gap` | Expected arm-contract provenance is absent. |
| `calibration_summary.json` | `conditional_absent` | Calibration-path file; not necessarily expected for this locked serious run. |
| `calibration_run_index.csv` | `conditional_absent` | Calibration-path file; not necessarily expected for this locked serious run. |
| `calibration_recommendation.md` | `conditional_absent` | Calibration-path file; not necessarily expected for this locked serious run. |

The run can still be interpreted from the budget lock, run index, aggregate
tables, and per-run artifacts, but provenance is less complete than the current
contract expects for the two evaluation manifest files.

## Classification

```text
artifact_status: partial
behavior_status: structural_limit
claim_status: diagnostic_evidence / no positive tower-performance claim
```
