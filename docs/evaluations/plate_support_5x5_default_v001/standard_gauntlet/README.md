# PlateSupport Standard Gauntlet

![Suite: Limited Signal](badges/suite_status.svg)
![Artifacts: Complete](badges/artifacts_complete.svg)
![Structure: Complete](badges/structural_readiness.svg)
![Candidate: Found](badges/schema_candidates.svg)
![Training: Clean](badges/training_health.svg)
![Target: Calibrated](badges/target_calibrated.svg)
![Paired: Negative Signal](badges/paired_comparison.svg)
![Provenance: Repo Artifacts](badges/provenance_repo_artifacts.svg)

## Result

Stages 1-7 completed. Stage 6 produced bounded paired comparison status `paired_comparison_negative_signal`, and Stage 7 produced the human readout/system-learning surface.

Under this smoke Stage 6 budget, the selected tower candidate is below the direct baseline on target-hit rate.

The target metric is Stage 5 binary goal success. Other metrics can explain the run, but they do not reverse the Stage 6 target claim.

## Key Numbers

- Valid states: `89`
- Shortest path length: `6`
- Random-policy success rate: `0.024`
- Stage 6 counter-signal: Tower mean reward was -44.515625 versus direct -78.71875; tower invalid moves were 0 versus direct 2142.

## Stage Status

| Stage | Name | Status | Claim Status |
| --- | --- | --- | --- |
| 1 | structural_and_tower_diagnostics | complete | diagnostic_complete |
| 2 | contraction_schema_sweep | complete | diagnostic_complete |
| 3 | candidate_discovery | complete | candidate_found |
| 4 | tower_training_health | complete | trainable_clean |
| 5 | threshold_frontier_calibration | complete | threshold_calibrated |
| 6 | paired_replicate_comparison | complete | paired_comparison_negative_signal |
| 7 | readout_and_system_learning | complete | readout_complete |

## Artifact Provenance

- Readout source: `/Users/foster/big_boy_benchmarking/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json`
- Raw artifact root: `/Users/foster/big_boy_benchmarking/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001`
- Suite evaluation root: `/Users/foster/big_boy_benchmarking/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001/evaluations/plate_support_standard_gauntlet_v001`

## Claim Boundary

bounded paired smoke comparison under the Stage 5 target and budget; not a general tower-performance claim

## Clarifying Turns

#### PO Turn

Explain "limited signal" and "negative signal" badges to me.

#### Codex Turn

The `Suite: Limited Signal` badge means the whole standard-gauntlet pipeline completed, but the result should not be read as a promoted positive performance claim. In this run, all child stages reached a valid readout state: structure, schema sweep, candidate discovery, tower-training health, threshold calibration, paired comparison, and human readout. So the suite itself is functioning. The "limited" part is about interpretation: the final claim is bounded by the smoke budget, the selected Stage 5 binary target, and the single selected candidate path. It says "we got a coherent end-to-end signal," not "tower abstraction wins generally."

The `Paired: Negative Signal` badge is narrower and more concrete. It refers specifically to the Stage 6 paired comparison target metric. Under the calibrated binary goal target, the selected tower candidate hit the target less often than the direct baseline in this smoke run. The readout records this as `paired_comparison_negative_signal`; numerically, the target hit-rate delta was negative. That is why this badge is orange.

The important subtlety is that this is not a broken-artifact badge. The artifacts are complete, the candidate was found, the training-health stage was clean, and the target was calibrated. The negative badge says the paired target metric went against the tower candidate. At the same time, the report keeps the counter-signal visible: the tower arm had better mean reward and zero invalid moves compared with the direct baseline. That counter-signal is interesting, but it does not override the locked Stage 6 binary target claim.

#### PO Turn
> I want to explore this in more detail: "The Paired: Negative Signal badge is narrower and more concrete. It refers specifically to the Stage 6 paired comparison target metric. Under the calibrated binary goal target, the selected tower candidate hit the target less often than the direct baseline in this smoke run. The readout records this as paired_comparison_negative_signal; numerically, the target hit-rate delta was negative. That is why this badge is orange." Give me as much concrete information about this as you can.

#### Codex Turn

The negative paired signal is coming from one exact Stage 6 claim table:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001/stages/paired_replicate_comparison/results/comparison_claim_summary.csv
```

That table says:

- `claim_status = paired_comparison_negative_signal`
- `direction = candidate_below_direct`
- `complete_pair_count = 4`
- `mean_target_hit_rate_delta = -0.0703125`

The target metric is not total reward. It is the calibrated Stage 5 binary goal-success target:

```text
target_policy_id = plate_support_binary_goal_success_v001
target_type = binary_success
recommended_episodes_per_replicate = 32
recommended_replicates_per_arm = 4
```

So Stage 6 ran four matched replicate pairs. Each active arm got 32 episodes per replicate, for 128 episodes per arm. The active arms were:

- direct baseline: `plate_support_direct_concrete_baseline`
- tower candidate: `plate_support_selected_tower_candidate:plate_support_candidate:source_local_ratio:0:342448ef2e`

The selected tower candidate came from:

```text
schema_id = plate_support_schema_source_local_ratio_001_over_018_v001
health_status = trainable_clean
```

Here is the target-hit arithmetic:

| Arm | Target Hits | Episodes | Target Hit Rate |
| --- | ---: | ---: | ---: |
| direct concrete baseline | 15 | 128 | 0.1171875 |
| selected tower candidate | 6 | 128 | 0.046875 |

The delta is:

```text
0.046875 - 0.1171875 = -0.0703125
```

That is the numeric source of the orange `Paired: Negative Signal` badge.

It is not just one unlucky aggregate hiding a mixed replicate pattern. The per-replicate target-hit deltas were all negative:

| Replicate | Direct Hits / 32 | Tower Hits / 32 | Delta |
| ---: | ---: | ---: | ---: |
| 0 | 3 | 1 | -0.0625 |
| 1 | 5 | 1 | -0.125 |
| 2 | 4 | 2 | -0.0625 |
| 3 | 3 | 2 | -0.03125 |

So on the locked binary target, the direct baseline beat the tower candidate in every matched replicate.

But the counter-signal is real and important. On total reward, the tower candidate looked much healthier:

| Arm | Mean Total Reward | Min | Max |
| --- | ---: | ---: | ---: |
| direct concrete baseline | -78.71875 | -128.0 | 90.0 |
| selected tower candidate | -44.515625 | -50.0 | 87.0 |

The tower also avoided invalid moves entirely:

| Arm | Concrete Steps | Invalid Moves | Invalid Move Rate |
| --- | ---: | ---: | ---: |
| direct concrete baseline | 6017 | 2142 | 0.3559913578195114 |
| selected tower candidate | 6304 | 0 | 0.0 |

My interpretation is: the direct baseline is messier but finds the binary goal more often in this small run, while the tower candidate is cleaner and higher-reward but less successful on the sparse binary goal. That is why the report must say `Paired: Negative Signal` for the target claim, while also preserving the reward/invalid-move counter-signal as a reason to keep investigating rather than dismissing the tower path.

The current result is therefore not "the tower broke" and not "the tower wins." It is: under this smoke budget, for this source-local-ratio candidate, using the Stage 5 binary success target, the direct baseline had more goal hits; however, the tower candidate had better reward hygiene and no invalid moves. The next design question is whether the target is too sparse/coarse for the thing the tower is improving, or whether the tower candidate is genuinely cleaning up behavior at the cost of goal-reaching.

#### PO Turn
> What is the shape of the tower, in terms of node count? Is the tower static here or is it discovered?


#### Codex Turn

For the selected Stage 6 tower candidate, the tower is two tiers deep:

| Tier | Meaning | State Cells | Action Cells |
| ---: | --- | ---: | ---: |
| 0 | base/concrete PlateSupport state graph | 89 | 388 |
| 1 | source-local-ratio quotient tier | 10 | 116 |

So if by "node count" we mean state-cell count in the tower, the selected candidate has:

```text
tier 0: 89 state cells
tier 1: 10 state cells
total across state tiers: 99 state cells
```

The relevant shape row comes from:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001/stages/contraction_schema_sweep/results/tower_shape_summary.csv
```

For the selected candidate schema:

```text
schema_id = plate_support_schema_source_local_ratio_001_over_018_v001
schema_family_id = source_local_ratio
schema_seed = 0
max_depth = 2
tier 0 state_cell_count = 89
tier 1 state_cell_count = 10
```

The selected candidate record also says:

```text
candidate_id = plate_support_candidate:source_local_ratio:0:342448ef2e
first_nonbase_tier_state_cell_count = 10
selected_edge_count = 89
largest_cell_share = 0.2247191011235955
structural_class = nonflat_structured
selection_status = selected_training_candidate
```

On "static versus discovered": it is both, depending on which phase we mean.

It is discovered upstream by the gauntlet, before the paired comparison. Stage 2 runs the contraction-schema sweep and constructs/scans candidate schemas. Stage 3 chooses this `source_local_ratio` candidate as the selected training candidate. Stage 4 checks that it is trainable cleanly. By the time Stage 6 runs the paired comparison, the tower is already selected.

During Stage 6 itself, the tower is static. The learner is not discovering or changing the quotient structure online. The paired comparison consumes the fixed candidate:

```text
schema_id = plate_support_schema_source_local_ratio_001_over_018_v001
schema_source = stage3_selected_candidate
```

So Stage 6 training is learning a policy/control behavior over a fixed two-tier tower, not growing a tower, changing the partition, or discovering new tiers during training.

There is one more useful behavioral detail: during the Stage 6 tower-candidate run, the controller overwhelmingly operated at the quotient tier:

| Tier | Controller Steps | Share |
| ---: | ---: | ---: |
| 0 | 152 | 0.024111675126903553 |
| 1 | 6152 | 0.9758883248730964 |

That means the actual tower arm was not merely carrying around an unused quotient. Almost all controller steps happened at tier 1, and then lifted back to concrete execution. This makes the negative target result more interesting: the fixed quotient tower was heavily used, produced cleaner action behavior, but still underperformed the direct baseline on the sparse binary goal-hit target.

#### PO Turn
> Ok then this is the wrong architecture. Do intensive repo research to find where the counterpoint with many tiers occurs. ...Actually, do we have the wrong architecture, or are we using the wrong ratio? Figure out what's going wrong, because I want many non-trivial tiers.


#### Codex Turn

I checked this against the counterpoint runs that actually produced many tiers, and the answer is not "PlateSupport is impossible" and not "just change the ratio." The current problem is architecture first, ratio second.

The counterpoint many-tier case lives in the full-iterated schema path, especially the second serious schema comparison artifacts and code:

```text
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/config.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/runner.py
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
```

The key schema source there is:

```text
SCHEMA1_TOWER_SOURCE_FULL_ITERATED = "full_iterated_noisy_rate"
```

That is different from the older one-drop/noisy-rate diagnostic. The one-drop path builds one quotient above the base tier. The full-iterated path starts with the same kind of first contraction block, then repeatedly applies fresh contraction blocks to the current quotient tower until it reaches a stopping condition or the configured iteration cap.

That difference shows up directly in the counterpoint tower-shape artifacts. For the wide counterpoint full-iterated run:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/wide_span18_full_iterated_p001_over018_s0_r012_001/evaluations/counterpoint_second_serious_schema_comparison_v001/results/tower_shape_summary.csv
```

the schema-1 tower has nontrivial tiers from tier 0 through tier 32. Its state-cell counts start:

| Tier | State Cells |
| ---: | ---: |
| 0 | 3580 |
| 1 | 1035 |
| 2 | 729 |
| 3 | 555 |
| 4 | 435 |
| 5 | 354 |
| 6 | 297 |
| 7 | 240 |
| 8 | 217 |
| 9 | 185 |
| 10 | 160 |

and continue down to tier 32 with 19 state cells. That is the many-nontrivial-tier behavior we want to recover.

By contrast, the current PlateSupport standard gauntlet is using a one-shot source-local-ratio schema. The relevant PlateSupport code is here:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/config.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/schema_runner.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/source_local_ratio_schema.py
```

The current selected schema is:

```text
plate_support_schema_source_local_ratio_001_over_018_v001
```

and its tower shape is:

| Tier | State Cells | Action Cells |
| ---: | ---: | ---: |
| 0 | 89 | 388 |
| 1 | 10 | 116 |

That is not failing to discover many tiers after trying to grow them. It is not trying to grow many tiers. It constructs one quotient layer and stops. So if the PO goal is many nontrivial tiers, the current PlateSupport gauntlet has the wrong tower-construction architecture.

The ratio still matters, but it is secondary. A `1/18` ratio is gentle in the counterpoint wide graph because the base has 3580 state cells and 49172 active action cells. In PlateSupport, the base has only 89 state cells and 388 active action cells. The same-looking ratio can be much more aggressive because the state/action surface is smaller. The current first quotient already jumps from 89 state cells to 10. If we simply repeated that exact behavior naively, it would probably collapse quickly.

So the diagnosis is:

```text
architecture blocker: PlateSupport currently has one-shot source-local-ratio, not full-iterated source-local-ratio
ratio concern: 1/18 may be too aggressive for an 89-state PlateSupport graph once iteration exists
desired next object: PlateSupport iterated source-local-ratio tower diagnostic
```

The next design should not start with another paired comparison. It should start with a tower-shape diagnostic whose only job is to produce and inspect many-tier PlateSupport towers. I would design it as an analog of counterpoint's `full_iterated_noisy_rate`, but using the PlateSupport source-local-ratio contraction family:

1. Add an iterated PlateSupport schema family, probably named something like `source_local_ratio_iterated`.
2. For each tier, select a fresh source-local-ratio contraction block on the current quotient surface.
3. Record every tier's state-cell count, action-cell count, largest-cell share, liftability/executability health, and stopping reason.
4. Sweep gentler ratios such as `1/144`, `1/72`, `1/36`, and `1/18`.
5. Treat "many nontrivial tiers" as the gate, before any training comparison.

For PlateSupport, the success target for this diagnostic should be something like: find at least one schema configuration with several nontrivial tiers, no immediate collapse, and executable action surfaces at each tier. Only after that should the gauntlet feed the candidate into tower-training health and paired replicate comparison.

So I agree with the PO's instinct that the current architecture is wrong for the many-tier goal. The correction is not to discard PlateSupport. The correction is to stop asking the one-shot schema to behave like the counterpoint full-iterated schema. We need to build the PlateSupport iterated-tower version, then tune the ratio inside that architecture.

#### PO Turn
> Create a new folder for design work, this time inside `docs/design/first_plate_support_environment/standard_gauntlet_suite`. This will be for the corrections to the guantlet, per your turn immediately above.

#### Codex Turn

Created:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/08_iterated_tower_correction/
```

I put a README in that folder explaining that this is a correction track for the PlateSupport standard gauntlet, triggered by the mismatch between:

```text
current PlateSupport behavior: one-shot source-local-ratio, two-tier tower
desired PO target: many nontrivial executable tiers
counterpoint reference: full-iterated noisy-rate tower construction
```

The folder is intentionally numbered after the existing seven standard gauntlet components because it is not yet a normal stage in the gauntlet. It is design work needed to repair the gauntlet architecture before we should treat PlateSupport as capable of the many-tier tower behavior the PO wants.

The immediate design target I recorded there is diagnostic-first:

1. Specify or build an iterated PlateSupport source-local-ratio schema family.
2. Repeatedly apply fresh contraction blocks to the current quotient surface.
3. Sweep gentle ratios such as `1/144`, `1/72`, `1/36`, and `1/18`.
4. Record tier-by-tier shape, executability, liftability health, largest-cell share, and stopping reason.
5. Only feed a candidate into training/comparison after the diagnostic finds several nontrivial executable tiers.

That preserves the distinction we need: the current gauntlet run is a valid smoke run over the one-shot schema, but the next design correction is about making the PlateSupport gauntlet capable of discovering and using genuinely many-tier towers.
