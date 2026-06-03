# Counterpoint Second Serious Schema Comparison

![Artifacts: Complete](badges/artifacts_complete.svg)
![Candidates: 1](badges/candidates.svg)
![Hits: 0](badges/threshold_hits.svg)
![Pairs: 0/1 unblocked](badges/pairs.svg)
![Scope: Schema Compare](badges/scope_schema_comparison.svg)
![Provenance: Repo Artifacts](badges/provenance_repo_artifacts.svg)

This repository directory is the human-readable readout surface for the second serious counterpoint schema-comparison evaluation.

## Status At A Glance

- Artifact evidence: complete; every required source file listed by `readout_source.json` is present in the repo-resident artifact root.
- Behavioral result: diagnostic; both schema arms executed real concrete steps and crossed the `13.0` reward threshold transiently.
- Goal result: blocked for speed-to-sustained-hit comparison; neither arm satisfied the `4_of_5` persistence rule.
- Claim scope: schema-comparison diagnostic only, with one candidate pair, one training replicate per arm, and an 8-episode smoke budget.
- Provenance: repo artifacts under `docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001`.

## Summary of Goals Behind this Evaluation

This evaluation exists to test whether the counterpoint benchmark can make a bounded, matched schema-comparison claim. The comparison is not between the old direct runner and a tower runner. It is between two schema conditions inside the same active-tier tower-control harness:

- `schema0_no_contraction`, the no-contraction control condition;
- `schema1_noisy_rate_one_drop`, a selected one-drop noisy-rate quotient candidate inherited from the prior noisy-rate full-tower training diagnostic.

The intended claim form is: at a locked reward threshold `R`, under the same seed bundle and training budget, one schema reaches sustained total-space adequacy faster, slower, or at the same time as the other. The measured adequacy criterion here is `episode_total_reward >= 13.0` in at least 4 of 5 consecutive episodes.

This run is still a smoke/diagnostic run. It can tell us whether the paired comparison surface and threshold logic behave coherently. It cannot prove broad abstraction superiority, musical quality, tensor-enabled behavior, or general schema dominance.

## Summary of Methodology Behind this Evaluation

The runner loaded one Schema 1 candidate from the existing noisy-rate full-tower training readout source, then created a matched Schema 0 control for the same candidate group. Both arms used the same environment instance, seed bundle, threshold policy, linearization condition, persistence rule, episode budget, and training replicate count.

The locked budget for this artifact set is:

- environment instance: `counterpoint_symbolic_n3_small_v001`;
- candidate cap: `1`;
- training replicates per arm: `1`;
- episodes per replicate: `8`;
- threshold policy: `counterpoint_total_space_sustained_reward_v001`;
- threshold value: `13.0`;
- persistence rule: `4_of_5`;
- linearization mode: `tensor_available_disabled`;
- run mode: `smoke_schema_comparison_first_sustained_hit`.

The artifact path was a run followed by summarization, then this human-readability protocol pass. The readout source binding is `readout_source.json`, and the raw evaluation tables live under `artifacts/r000_001/evaluations/counterpoint_second_serious_schema_comparison_v001`.

## One-Screen Verdict

All required artifacts are present, and both schema arms executed normally: each arm recorded 64 concrete environment steps, 64 successful lifts, and 80 learner updates. The threshold result is the important part: both arms crossed `episode_total_reward >= 13.0` at least once, but neither produced 4 qualifying episodes inside any 5-episode window. This makes the result `transient_hit_only` for both arms.

The current artifact set therefore does not support a speed-to-sustained-hit comparison. It does support a useful threshold diagnostic: under this tiny smoke budget, `12.0` was low enough to sustain in earlier probing, `15.0` was not crossed, and `13.0` is in the boundary region where both arms touch the threshold but fail persistence.

## Run Identity

- Evaluation id: `counterpoint_second_serious_schema_comparison_v001`.
- Run family: `counterpoint_symbolic_v001_second_serious_schema_comparison_v001`.
- Repo readout surface: `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison`.
- Source artifact root: `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001`.
- Source evaluation root: `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001/evaluations/counterpoint_second_serious_schema_comparison_v001`.
- Budget lock: `artifacts/r000_001/evaluations/counterpoint_second_serious_schema_comparison_v001/evaluation_budget_lock.json`.
- Artifact schema version: `bbb.v001`.

## Schema Arms

| Schema | Reader Label | Role | Runs | Behavioral Status | Threshold Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `schema0_no_contraction` | No-contraction schema control | Matched control arm in the same tower-control harness | 1 | Executed 64 concrete steps and 64 successful lifts | `transient_hit_only` | `results/first_sustained_hit_summary.csv` |
| `schema1_noisy_rate_one_drop` | One-drop noisy-rate quotient schema | Candidate schema arm selected from the prior noisy-rate diagnostic | 1 | Executed 64 concrete steps and 64 successful lifts across tiers 0 and 1 | `transient_hit_only` | `results/tower_shape_summary.csv`, `results/tier_occupancy_summary.csv` |

## First Sustained Hit Summary

| Run | Schema | Status | First Sustained Episode |
| --- | --- | --- | --- |
| counterpoint_symbolic_n3_small_v001-p001_over_144-schema0-schema0_no_contraction-trainrep0 | schema0_no_contraction | transient_hit_only |  |
| counterpoint_symbolic_n3_small_v001-p001_over_144-schema0-schema1_noisy_rate_one_drop-trainrep0 | schema1_noisy_rate_one_drop | transient_hit_only |  |

Interpretation: blank sustained-hit episodes are not missing data. They mean the runs crossed the threshold transiently but never satisfied the 4-of-5 persistence rule.

## Paired Comparison Summary

| Candidate Group | Seed | Pair Status | Delta | Blocked |
| --- | --- | --- | --- | --- |
| counterpoint_symbolic_n3_small_v001-p001_over_144-schema0 | seed-7fe8666539580bdb | blocked_or_non_sustained |  | True |

Interpretation: the pair is blocked because a speed-to-hit delta only exists when both arms have sustained hits. Here both arms are transient-only, so there is no valid episode delta.

## Threshold Window Evidence

At threshold `13.0`, Schema 0 repeatedly came close but did not reach the required persistence count:

| Schema | Best Window Hit Count | Required Count | Window Length | Sustained? |
| --- | --- | --- | --- | --- |
| `schema0_no_contraction` | 3 | 4 | 5 | no |
| `schema1_noisy_rate_one_drop` | 1 | 4 | 5 | no |

The aggregate rewards are also close to the boundary: Schema 0 has mean total reward about `12.986`, and Schema 1 has mean total reward about `12.871`. This explains why lower thresholds such as `12.0` can sustain while `13.0` becomes transient-only.

## Tower And Tier Diagnostics

The no-contraction arm only has tier `0`, with 108 state cells and 1140 active action cells. The noisy-rate candidate has tier `0` with 108 state cells and tier `1` with 100 state cells. The first contraction is therefore not a collapse-to-one structural failure in this artifact set.

Tier-occupancy evidence shows the Schema 1 controller actually used both tiers:

| Schema | Tier | Notable Events |
| --- | --- | --- |
| `schema0_no_contraction` | 0 | explore, train, exploit_execute |
| `schema1_noisy_rate_one_drop` | 0 | explore, train, lift, exploit_execute |
| `schema1_noisy_rate_one_drop` | 1 | explore, train, descend, exploit_execute |

Lift evidence is clean for this smoke run: Schema 0 has 64 successful tier-0 lift/execution records, while Schema 1 has 27 at tier 0 and 37 at tier 1, with no failure reason recorded in `lift_success_by_tier.csv`. That means the blocked claim is not a lift failure or tower-collapse story. It is a threshold-persistence story.

## Timing Readout

Timing is diagnostic only. This run is too small to support method-speed claims.

| Schema | Algorithm Online Seconds | Linearization Setup Seconds | Total Seconds |
| --- | ---: | ---: | ---: |
| `schema0_no_contraction` | 0.212 | 0.005 | 0.217 |
| `schema1_noisy_rate_one_drop` | 0.232 | 0.006 | 0.238 |

Timing evidence lives in `results/timing_summary.csv` and each run directory's `timing_summary.json`.

## Claim Boundary

This readout may support a bounded speed-to-sustained-hit comparison only when paired rows are unblocked. It may not claim broad abstraction superiority, musical quality, direct-runner advantage, tensor-enabled behavior, or general schema dominance.

## Current Claim Rows

| Claim Status | Pairs | Unblocked | Schema1 Faster | Schema1 Slower |
| --- | --- | --- | --- | --- |
| claim_blocked | 1 | 0 | 0 | 0 |

## Evidence Map

- `readout_source.json`: repo-side source binding used by this protocol execution.
- `evaluation_budget_lock.json`: locked budget, threshold, seed, run-mode, and linearization facts.
- `evaluation_run_index.csv`: the two concrete runs included in this artifact set.
- `evaluation_aggregate_table.csv`: per-run aggregate status, mean reward, step counts, lift counts, and structural classification.
- `results/first_sustained_hit_summary.csv`: the decisive hit-status table showing `transient_hit_only` for both arms.
- `results/paired_schema_comparison.csv`: the table showing that the pair is `blocked_or_non_sustained`.
- `results/threshold_window_summary.csv`: the window-level evidence explaining why threshold crossing did not become sustained success.
- `results/tower_shape_summary.csv`: tier shape evidence showing the Schema 1 contraction is not a full collapse.
- `results/tier_occupancy_summary.csv`: active-tier evidence showing both tiers were used in Schema 1.
- `results/lift_success_by_tier.csv`: lift/action-realization evidence showing no recorded lift failure reason.
- `results/timing_summary.csv`: timing evidence for diagnostic inspection only.

## Provenance Status

All required files listed in `readout_source.json` are present. No required artifact was classified as missing during this protocol pass. Files listed as not applicable in the source binding, such as old direct tabular-Q baseline artifacts, masked-random baseline artifacts, tensor-enabled conversion records, and musical quality judgments, are outside this run's claim boundary.

To regenerate the human-readable readout, run:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/readout_source.json
```

Source artifact root:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001
```

## Clarifying Questions And Turns

#### Project Owner / Evaluator Turn

> Bro, is there a comparison we can make here of a form like "with threshold of $R$, Scheme $m$ finsihes this much faster than Schema $m$. Do we hav ethe data to do this?

#### Embedded Engineering Consultant / Codex Turn

> Yes, with one important boundary. This evaluation is now shaped to support exactly that kind of paired statement:
>
> "At threshold `R`, under persistence rule `4_of_5`, Schema 1 reaches sustained adequacy `D` episodes faster/slower than Schema 0 on the matched candidate/seed pair."
>
> The data that supports that statement is in `results/paired_schema_comparison.csv` and `results/first_sustained_hit_summary.csv`. In the current smoke run, `R = -999.0`, both Schema 0 and Schema 1 have `hit_status = sustained_hit`, both have `episodes_to_sustained_hit = 5`, and the paired delta is `schema1_minus_schema0_episodes_to_hit = 0`. So the literal current result is:
>
> "At threshold `-999.0`, Schema 1 did not finish faster or slower than Schema 0 in the one unblocked matched pair; both reached sustained threshold at the same episode count."
>
> But I would not treat this as the serious scientific comparison yet. The threshold `-999.0` is intentionally permissive smoke machinery, the run has `candidate_cap = 1`, `training_replicates_per_arm = 1`, and `episodes_per_replicate = 8`. So this proves the comparison surface works; it does not yet prove a meaningful performance relationship between the schemas.
>
> The next serious version should keep this exact claim form, but run with a real locked threshold, enough candidates, and enough replicates that "Schema 1 finishes `X` episodes faster/slower than Schema 0" means something beyond smoke.

#### Project Owner / Evaluator Turn

> Can you rerun with threshold `R=0.0`

#### Embedded Engineering Consultant / Codex Turn

> Yes. The current runner exposes the threshold as `--threshold-value`, so `R = 0.0` is exactly the next natural rerun.
>
> I would not overwrite `artifacts/smoke_001`, though. That folder is useful as proof that the comparison surface works. I would create a fresh artifact root, something like:
>
> ```text
> docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001
> ```
>
> Then run the same evaluation with `--threshold-value 0.0`. If we keep the same small smoke budget, the claim will still be machinery-level: "under a less trivial threshold, does the paired comparison surface remain populated?" If we want the first genuinely interpretable comparison, we should also increase candidate count, training replicates, and episode budget.
>
> The important thing is that `R = 0.0` changes the interpretation of the paired delta. At `R = -999.0`, both arms basically clear the threshold immediately once persistence can be observed. At `R = 0.0`, the first-sustained-hit rows start to mean: "when does this schema reliably achieve nonnegative total reward?" That is much closer to the kind of bounded performance claim this evaluation was designed to make.

#### Project Owner / Evaluator Turn

> Ok fine. Start a new folder.

#### Embedded Engineering Consultant / Codex Turn

> Agreed. The new folder should be the evidence root for the `R = 0.0` rerun:
>
> ```text
> docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/r000_001
> ```
>
> That keeps `artifacts/smoke_001` as the historical smoke proof and gives the zero-threshold run its own clean provenance. After the run, the human-readable readout surface at:
>
> ```text
> docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/
> ```
>
> can be regenerated from the new run's `readout_source.json` if we want the visible README to represent `R = 0.0` instead of the original smoke run.
>
> I would label the run as "zero-threshold diagnostic" rather than "final serious comparison" unless we also raise the budget beyond the current smoke settings. The folder move is enough to keep the evidence clean; the budget choice is what determines how strong the resulting claim can be.

#### Project Owner / Evaluator Turn

> What does "`transient_hit_only`" mean?

#### Embedded Engineering Consultant / Codex Turn

> `transient_hit_only` means: the arm crossed the threshold at least once, but it did not cross it reliably enough to count as a sustained hit.
>
> In this evaluation, a single good episode is not enough. The threshold policy says:
>
> ```text
> episode_total_reward >= 13.0
> ```
>
> and the persistence rule says:
>
> ```text
> at least 4 qualifying episodes inside a 5-episode window
> ```
>
> So the possible statuses mean:
>
> - `sustained_hit`: crossed the threshold often enough to satisfy the 4-of-5 rule;
> - `transient_hit_only`: crossed the threshold sometimes, but never enough times in one 5-episode window;
> - `never_hit`: never crossed the threshold at all.
>
> For this `13.0` run, both schema arms are in the middle case. Schema 0 had windows with 3 hits out of 5, and Schema 1 had windows with at most 1 hit out of 5. So both touched the threshold, but neither made the threshold stable. That is why the pair is blocked: there is no valid "episodes to sustained hit" number to compare.

#### Project Owner / Evaluator Turn

> [...]

#### Embedded Engineering Consultant / Codex Turn

> [...]

#### Project Owner / Evaluator Turn

> [...]

#### Embedded Engineering Consultant / Codex Turn

> [...]

#### Project Owner / Evaluator Turn

> [...]

#### Embedded Engineering Consultant / Codex Turn

> [...]
