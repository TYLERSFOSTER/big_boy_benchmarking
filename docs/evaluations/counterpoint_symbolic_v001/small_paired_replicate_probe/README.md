# Counterpoint Small Paired Replicate Probe

![Artifacts: Complete](badges/artifacts_complete.svg)
![Pairs: 1](badges/pair_count.svg)
![Unblocked: 0/1](badges/unblocked_pairs.svg)
![S1 Margin Wins: 0](badges/schema1_margin_wins.svg)
![Hit Rate Delta: 0.0](badges/hit_rate_delta.svg)
![Liftability: Pointwise v0.7.2](badges/liftability_semantics.svg)
![Lift Failures: 0](badges/lift_failures.svg)
![Provenance: Repo Artifacts](badges/provenance_repo_artifacts.svg)

This repository directory is the human-readable readout surface for the small paired replicate probe. The probe repeats the corrected Schema 0 versus Schema 1 comparison across matched seed bundles for one selected candidate and one locked threshold.

## Status At A Glance

- Artifact evidence: `complete`.
- Run mode: `smoke_small_paired_replicate_probe`.
- Instance: `counterpoint_symbolic_n3_wide_20_108_span18_v001`.
- Threshold value: `13.0`.
- Threshold source: `explicit_cli_threshold`.
- Pair rows: `1`.
- Unblocked pairs: `0`.
- Lift failure rows: `0`.

## Liftability And Invariant Semantics

- Liftability semantics: `state_collapser_v072_pointwise`.
- Runtime action availability is pointwise: an abstract action must have a concrete lift executable from the current base state.

## Summary of Goals Behind this Evaluation

The goal is to see whether Schema 1's small post-hit reward-margin signal survives across matched seed bundles. This is a next-measure probe, not a final serious comparison or statistical significance test.

## Summary of Methodology Behind this Evaluation

For each selected corrected Schema 1 candidate, the runner creates matched Schema 0 and Schema 1 arm runs for each seed bundle. Pair-level tables join the two arm runs by `candidate_group_id`, `seed_bundle_id`, and `training_replicate_index`.

## Pair Distribution

| Candidate Group | Pairs | Unblocked | Margin Wins | Margin Losses | Claim |
| --- | --- | --- | --- | --- | --- |
| counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0 | 1 | 0 | 0 | 0 | claim_blocked |

## Pair-Level Rows

| Candidate Group | Seed | Rep | Pair Status | Mean Delta | Blocked |
| --- | --- | --- | --- | --- | --- |
| counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0 | seed-7fe8666539580bdb | 0 | blocked_or_non_sustained |  | True |

## Schema-Arm Distribution

| Schema | Runs | Sustained | Rate | Median Episodes | Median Mean |
| --- | --- | --- | --- | --- | --- |
| schema0_no_contraction | 1 | 0 | 0.0 |  |  |
| schema1_noisy_rate_one_drop | 1 | 0 | 0.0 |  |  |

## Sustained-Hit Rate Rows

| Schema | Run Count | Sustained | Rate | Schema1 - Schema0 |
| --- | --- | --- | --- | --- |
| schema0_no_contraction | 1 | 0 | 0.0 | 0.0 |
| schema1_noisy_rate_one_drop | 1 | 0 | 0.0 | 0.0 |

## Seed Bundle Evidence

| Candidate Group | Seed | Rep | Schema0 Run | Schema1 Run | Status |
| --- | --- | --- | --- | --- | --- |
| counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0 | seed-7fe8666539580bdb | 0 | counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0-schema0_no_contraction-trainrep0 | counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0-schema1_noisy_rate_one_drop-trainrep0 | blocked_or_non_sustained |

## Claim Boundary

This readout may support only a bounded single-candidate paired-seed pattern under the locked threshold. It may not claim broad abstraction superiority, statistical significance, tensor-enabled behavior, or musical quality.

To regenerate the human-readable readout, run:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/readout_source.json
```

Source artifact root:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts/smoke_001
```

## Clarifying Questions And Turns

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> ...

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> ...

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> ...
