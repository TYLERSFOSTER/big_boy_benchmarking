# Counterpoint Second Serious Schema Comparison

![Artifacts: Complete](badges/artifacts_complete.svg)
![Candidates: 1](badges/candidates.svg)
![Hits: 2](badges/threshold_hits.svg)
![Pairs: 1/1 unblocked](badges/pairs.svg)
![Scope: Schema Compare](badges/scope_schema_comparison.svg)
![Provenance: Repo Artifacts](badges/provenance_repo_artifacts.svg)

This repository directory is the human-readable readout surface for the second serious counterpoint schema-comparison evaluation.

## Status At A Glance

- Artifact evidence: `complete`.
- Run mode: `smoke_schema_comparison_first_sustained_hit`.
- Instance: `counterpoint_symbolic_n3_small_v001`.
- Threshold value: `-999.0`.
- Paired rows: `1`.
- Sustained-hit rows: `2`.

## Summary of Goals Behind this Evaluation

The goal is to compare schema conditions, not old runner paths: `schema0_no_contraction` versus selected `schema1_noisy_rate_one_drop` candidates under a matched active-tier tower-control harness. The main measurement is first sustained total-space adequacy under a locked `episode_total_reward` threshold and a 4-of-5 persistence rule.

## Summary of Methodology Behind this Evaluation

Schema 1 candidates are loaded from the noisy-rate full-tower training readout source, preserving provenance back to the noisy-rate contraction diagnostic. For each selected Schema 1 candidate, the runner creates a paired Schema 0 no-contraction condition with the same seed bundle, episode budget, learner family, threshold policy, and linearization mode.

## Schema Arms

| Schema | Runs | Sustained | Transient | Never | Median Episodes |
| --- | --- | --- | --- | --- | --- |
| schema0_no_contraction | 1 | 1 | 0 | 0 | 5 |
| schema1_noisy_rate_one_drop | 1 | 1 | 0 | 0 | 5 |

## First Sustained Hit Summary

| Run | Schema | Status | First Sustained Episode |
| --- | --- | --- | --- |
| counterpoint_symbolic_n3_small_v001-p001_over_144-schema0-schema0_no_contraction-trainrep0 | schema0_no_contraction | sustained_hit | 4 |
| counterpoint_symbolic_n3_small_v001-p001_over_144-schema0-schema1_noisy_rate_one_drop-trainrep0 | schema1_noisy_rate_one_drop | sustained_hit | 4 |

## Paired Comparison Summary

| Candidate Group | Seed | Pair Status | Delta | Blocked |
| --- | --- | --- | --- | --- |
| counterpoint_symbolic_n3_small_v001-p001_over_144-schema0 | seed-7fe8666539580bdb | same_episode_to_hit | 0 | False |

## Claim Boundary

This readout may support a bounded speed-to-sustained-hit comparison only when paired rows are unblocked. It may not claim broad abstraction superiority, musical quality, direct-runner advantage, tensor-enabled behavior, or general schema dominance.

## Current Claim Rows

| Claim Status | Pairs | Unblocked | Schema1 Faster | Schema1 Slower |
| --- | --- | --- | --- | --- |
| bounded_comparison_available | 1 | 1 | 0 | 0 |

To regenerate the human-readable readout, run:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/readout_source.json
```

Source artifact root:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/smoke_001
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
