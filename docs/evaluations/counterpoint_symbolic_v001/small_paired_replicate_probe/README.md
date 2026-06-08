# Counterpoint Small Paired Replicate Probe

![Artifacts: Complete](badges/artifacts_complete.svg)
![Pairs: 1](badges/pair_count.svg)
![Unblocked: 1/1](badges/unblocked_pairs.svg)
![S1 Margin Wins: 1](badges/schema1_margin_wins.svg)
![Hit Rate Delta: 0.0](badges/hit_rate_delta.svg)
![Liftability: Pointwise v0.7.2](badges/liftability_semantics.svg)
![Lift Failures: 0](badges/lift_failures.svg)
![Provenance: Repo Artifacts](badges/provenance_repo_artifacts.svg)

This repository directory is the human-readable readout surface for the small paired replicate probe. The probe repeats the corrected Schema 0 versus Schema 1 comparison across matched seed bundles for one selected candidate and one locked threshold.

## Status At A Glance

- Artifact evidence: `complete`.
- Run mode: `threshold_frontier_selected_small_paired_replicate_probe`.
- Instance: `counterpoint_symbolic_n3_wide_20_108_span18_v001`.
- Threshold value: `13.0`.
- Threshold source: `threshold_frontier_readout`.
- Pair rows: `1`.
- Unblocked pairs: `1`.
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
| counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0 | 1 | 1 | 1 | 0 | weak_positive_margin_pattern |

## Pair-Level Rows

| Candidate Group | Seed | Rep | Pair Status | Mean Delta | Blocked |
| --- | --- | --- | --- | --- | --- |
| counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0 | seed-7fe8666539580bdb | 0 | schema1_margin_higher | 0.18212121212121168 | False |

## Schema-Arm Distribution

| Schema | Runs | Sustained | Rate | Median Episodes | Median Mean |
| --- | --- | --- | --- | --- | --- |
| schema0_no_contraction | 1 | 1 | 1.0 | 5 | 13.368636363636364 |
| schema1_noisy_rate_one_drop | 1 | 1 | 1.0 | 5 | 13.550757575757576 |

## Sustained-Hit Rate Rows

| Schema | Run Count | Sustained | Rate | Schema1 - Schema0 |
| --- | --- | --- | --- | --- |
| schema0_no_contraction | 1 | 1 | 1.0 | 0.0 |
| schema1_noisy_rate_one_drop | 1 | 1 | 1.0 | 0.0 |

## Seed Bundle Evidence

| Candidate Group | Seed | Rep | Schema0 Run | Schema1 Run | Status |
| --- | --- | --- | --- | --- | --- |
| counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0 | seed-7fe8666539580bdb | 0 | counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0-schema0_no_contraction-trainrep0 | counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0-schema1_noisy_rate_one_drop-trainrep0 | schema1_margin_higher |

## Claim Boundary

This readout may support only a bounded single-candidate paired-seed pattern under the locked threshold. It may not claim broad abstraction superiority, statistical significance, tensor-enabled behavior, or musical quality.

To regenerate the human-readable readout, run:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-root>/docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/readout_source.json
```

Source artifact root:

```text
<repo-root>/docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts/episodes16_from_frontier_001
```

## Clarifying Questions And Turns

#### Project Owner / Evaluator Turn

> Tell me everything you can about the two orange badges here.

#### Embedded Engineering Consultant / Codex Turn

> The two orange badges are `Unblocked: 0/1` and `S1 Margin Wins: 0`.
>
> `Unblocked: 0/1` means the probe successfully produced one matched Schema 0 / Schema 1 pair, but zero of those pairs are claim-bearing under the sustained-hit rule. This is not a liftability failure and not an artifact failure. The run completed, the artifacts are present, and `Lift Failures: 0` is green. The blocking reason is behavioral/evaluation-side: the pair is marked `blocked_or_non_sustained` because at least one arm did not establish a sustained hit.
>
> The important detail is that this is a smoke run with `episodes_per_replicate = 4`, while the threshold policy is a `4_of_5` persistence rule at threshold `13.0`. With only four episodes, the run is not really capable of producing a full five-episode persistence window. Both arms are recorded as `transient_hit_only` with `threshold_crossed_but_persistence_rule_not_met`. Schema 0 has episode rewards `13.7583`, `12.9614`, `13.6356`, `13.1167`; Schema 1 has `13.1697`, `13.7636`, `13.4409`, `13.7439`. So Schema 1 actually looks superficially encouraging in this tiny sample, but the formal sustained-hit machinery refuses to count it because this artifact root is smoke-budgeted.
>
> `S1 Margin Wins: 0` is downstream from that blockage. A Schema 1 margin win requires an unblocked pair with a valid post-hit comparison window. Since there are zero unblocked pairs, the readout has no legal post-hit margin comparison to count. So `0` here should not be read as "Schema 1 failed to beat Schema 0." It means "the margin question was not adjudicated in this smoke run."
>
> My current interpretation: the orange badges are doing the right thing. They warn that this readout validates the plumbing and provenance of the small paired replicate probe, but does not yet evaluate the intended learning claim. For a meaningful version, we need a non-smoke artifact root with enough episodes to support the persistence window, and probably multiple matched seed bundles so `Unblocked` and `S1 Margin Wins` become real distributional summaries rather than single-pair smoke indicators.
