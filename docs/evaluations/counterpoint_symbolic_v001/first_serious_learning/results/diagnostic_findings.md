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

| Schema seed | Tower shape | Mean return | Mean steps | Episode success | Main failure |
| ---: | --- | ---: | ---: | ---: | --- |
| 0 | `(108, 3, 1, 1, 1)` | 0.000 | 0.0 | 0% | `no_lift_candidate_from_current_state` |
| 1 | `(108, 8, 2, 1, 1)` | 0.000 | 0.0 | 0% | `no_lift_candidate_from_current_state` |
| 2 | `(108, 1, 1, 1, 1)` | 12.710 | 8.0 | 100% | none observed |

Across all schema seeds this becomes mean return `4.237`, mean step count
`2.7`, and 33% episode success.

## Finding 3: Random Unbalanced Is Also Schema-Seed Dependent

Random unbalanced tower behavior:

| Schema seed | Tower shape | Mean return | Mean steps | Episode success | Main failure |
| ---: | --- | ---: | ---: | ---: | --- |
| 0 | `(108, 1, 1)` | 12.710 | 8.0 | 100% | none observed |
| 1 | `(108, 2, 1)` | 0.000 | 0.0 | 0% | `no_lift_candidate_from_current_state` |
| 2 | `(108, 1, 1)` | 12.710 | 8.0 | 100% | none observed |

Across all schema seeds this becomes mean return `8.473`, mean step count
`5.3`, and 67% episode success.

## Finding 4: Structured Motion And Bad/Adversarial Execute Under Full Collapse

The structured-motion and bad/adversarial arms execute 8-step episodes, but
they do so under fully collapsed first projections. Their execution therefore
does not separate useful tower control from the collapsed schema/runtime
condition.

| Arm | Tower shape | Mean return | Delta vs empty tower |
| --- | --- | ---: | ---: |
| Empty-schema tower | `(108,)` | 12.710 | +0.000 |
| Structured motion tower | `(108, 1, 1, 1, 1)` | 12.710 | +0.000 |
| Bad/adversarial tower | `(108, 1)` | 12.710 | +0.000 |

This means the benchmark cannot claim that structured motion is a better
contraction, and it also cannot treat the bad/adversarial arm as an effective
negative control for this budget. The claim boundary is structural: the first
projection has already collapsed too much for ordinary performance comparison.

## Finding 5: Promoted Tower Tables Are Still Missing

The protocol now expects tower-control evaluations to promote:

- `results/tower_shape_summary.csv`
- `results/tier_occupancy_summary.csv`
- `results/lift_failure_by_tier.csv`

This run does not yet produce those evaluation-level tables. The readout
reconstructs the relevant facts from per-run files:

- `quotient_summary.json`
- `control_events.csv`
- `step_events.csv`
- `lift_fiber_events.csv`

That reconstruction is enough for this report, but the missing promoted tables
remain an artifact-contract gap.

## Classification

```text
artifact_status: partial
behavior_status: structural_limit
claim_status: diagnostic_evidence / no positive tower-performance claim
```
