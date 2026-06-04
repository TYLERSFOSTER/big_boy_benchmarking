# Counterpoint Noisy-Rate Full-Tower Training Diagnostic

![Artifacts: Complete](badges/artifacts_complete.svg)
![Candidates: 1](badges/candidates.svg)
![Training: 0 clean/1 warn/0 fail](badges/training_health.svg)
![Runtime: Concrete Steps](badges/runtime_executable.svg)
![Learner: Updates](badges/lift_status.svg)
![Scope: Diagnostic Only](badges/scope_diagnostic_only.svg)
![Provenance: Repo Artifacts](badges/provenance_repo_artifacts.svg)

This repository directory is the human-readable readout surface for the counterpoint noisy-rate full-tower training health diagnostic.

## Status At A Glance

- Artifact evidence: `complete`.
- Candidate count: `1`.
- Concrete steps emitted: `1`.
- Successful learner updates: `61`.
- Claim scope: diagnostic only; this is not a direct-vs-tower comparison.

## One-Screen Verdict

This evaluation trains only on selected non-collapsed noisy-rate towers. It does not run a direct baseline and it does not support tower-advantage claims. It checks whether each selected tower can execute a real tower-only training budget with coherent lift, concrete-step, tier, controller, and learner-update traces.

For the current noisy-rate schema, the full available tower is the base tier plus one noisy-rate quotient tier.

## Source Evaluation Root

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts/wide_span18_p001_over018_s0_001
```

## Candidate Towers

| Candidate | Arm | Seed | Tier Cells | Active Cells |
| --- | --- | --- | --- | --- |
| counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0 | p001_over_018 | 0 | [3580, 1035] | [49172, 24258] |

## Training Health

| Candidate | Status | Concrete Steps | Learner Updates | Zero-Step Share |
| --- | --- | --- | --- | --- |
| counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0 | trainable_with_warnings | True | True | 0.75 |

## Claim Boundary

This readout may claim that the selected non-collapsed noisy-rate towers did or did not train cleanly under the locked budget. It may not claim direct-vs-tower advantage, schema superiority, deep tower validation, tensor-enabled behavior, or musical quality.

To regenerate the human-readable readout, run:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
```

## Clarifying Questions And Turns

#### Project Owner / Evaluator Turn

> Is the tower still only limited to $2$ tiers?

#### Embedded Engineering Consultant / Codex Turn

> Yes, in this evaluation as implemented, the current "full available tower" is still only two tiers: tier 0 is the base counterpoint graph, and tier 1 is the single noisy-rate quotient produced by the selected contraction block. That is not because tower machinery is conceptually limited to two tiers; it is because this diagnostic deliberately consumes the parent noisy-rate contraction diagnostic, whose candidates are single-step noisy-rate contractions. The runner records the tier sequence it rebuilds, so if a future schema produces more tiers the readout should show them, but this checked-in `smoke_001` result should be read as "can these non-collapsed one-step noisy-rate quotient towers train cleanly?" rather than "have we validated deep repeated quotient towers?"

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> ...

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> ...
