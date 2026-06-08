# Counterpoint Small Paired Replicate Probe Blueprint

Date: 2026-06-05

Status: draft blueprint with Project Owner answer slots

Repository:

```text
<repo-root>
```

Design folder:

```text
docs/design/first_counterpoint_environment/small_paired_replicate_probe/
```

Source orientation:

```text
docs/design/first_counterpoint_environment/small_paired_replicate_probe/README.md
```

## Status And Authority

This is a design blueprint.

This is not an implementation workplan.

This is not approval to edit source code.

This is not approval to run benchmark artifacts.

This is not approval to modify TeX documents at repo root.

This is not approval to change the `counterpoint_symbolic_v001` environment.

This is not approval to edit `<state-collapser-repo>`.

A later Phase.Stage.Action implementation workplan must translate this
blueprint into executable work before source edits or benchmark runs begin.

## Source Authority

This blueprint follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`
- `docs/design/first_counterpoint_environment/small_paired_replicate_probe/README.md`
- `docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/readout_source.json`
- `docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/README.md`
- `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json`

## PO Attribution Ledger

This section records only Project Owner-originated requests visible in the
current conversation. Consultant recommendations and questions appear later
under explicit consultant labels.

1. The Project Owner asked for next-measure directions, not a full-blown final
   evaluation:

   ```text
   Give me two directions we can push this evaluation, I mean make new ones,
   that would test the bigger claims. Not full-blown, but like next measure.
   ```

2. The Project Owner asked for folders for each direction:

   ```text
   Make new folders for designing each of those, and put a readme in each
   describing what's been done and what we will desing in said folder
   ```

3. The Project Owner asked for blueprints in the respective folders:

   ```text
   Generate each blueprint in respective folder. I will answer necessary
   questions
   ```

4. The Project Owner clarified the answering process:

   ```text
   I will answer in doc
   ```

## Consultant Interpretation Summary

The current corrected comparison gives a tiny positive signal for Schema 1
reward robustness at `R = 13.0`, but it is based on one candidate and one
matched seed pair.

The replicate probe asks whether that signal survives across a small number of
paired seed bundles.

This is the natural next step after either:

1. accepting `R = 13.0` as the first replicate threshold; or
2. running the threshold-frontier probe first and choosing a sharper threshold
   from its frontier result.

## Executive Design

The small paired replicate probe repeats the corrected schema comparison across
multiple matched seed bundles.

The evaluation asks:

```text
Across a small number of matched seeds, does Schema 1 show a stable paired
advantage, disadvantage, or no-difference pattern relative to Schema 0?
```

The intended bounded claim shape is:

```text
For this corrected widened candidate and locked threshold, Schema 1 shows a
paired pattern across N matched seed bundles under a modest budget.
```

The evaluation must not claim:

- broad abstraction superiority;
- final serious statistical significance;
- multi-instance generality;
- tensor-enabled behavior;
- musical quality;
- improvement across all noisy-rate candidates.

## Evaluation Identity

Consultant recommendation:

```text
evaluation_id = counterpoint_small_paired_replicate_probe_v001
evaluation_run_family_id = counterpoint_symbolic_v001_small_paired_replicate_probe_v001
```

Repo readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/
```

Default artifact root shape:

```text
docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts/<run_label>/
```

Consultant-recommended first run label if using `R = 13.0`:

```text
v072_pointwise_r013_reps8_001
```

Consultant-recommended first run label if using a threshold discovered by the
frontier probe:

```text
v072_pointwise_r<THRESHOLD>_reps8_001
```

Project Owner answer:

```text
Pending.
```

## Fixed Inputs

These should be treated as locked unless the Project Owner answers otherwise.

Environment family:

```text
counterpoint_symbolic_v001
```

Environment instance:

```text
counterpoint_symbolic_n3_wide_20_108_span18_v001
```

Candidate source:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
```

Candidate id:

```text
counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0
```

Schema arms:

| Arm | Schema class | Meaning |
| --- | --- | --- |
| Schema 0 | `schema0_no_contraction` | matched no-contraction / total-space schema condition |
| Schema 1 | `schema1_noisy_rate_one_drop` | full-iterated noisy-rate tower sourced from corrected candidate |

Liftability semantics:

```text
state_collapser_v072_pointwise
```

Linearization mode:

```text
tensor_available_disabled
```

## Threshold Policy

Consultant recommendation if this probe is run before threshold frontier:

```text
threshold_value = 13.0
```

Reasoning:

`R = 13.0` is the first threshold where the corrected smoke run showed a
visible but tiny Schema 1 margin:

```text
Schema 0: post_hit_window_success_count = 4/5
Schema 1: post_hit_window_success_count = 5/5
```

Consultant recommendation if threshold frontier runs first:

```text
Use the lowest threshold where Schema 0 begins to wobble or fail while Schema
1 remains near the sustained-hit frontier.
```

Project Owner answer:

```text
Pending.
```

## Budget

Consultant recommendation for first paired probe:

```text
candidate_cap = 1
replicates_per_arm = 8
episodes_per_arm = 16
window_length = 5
required_count = 4
base_seed = 0
```

Reasoning:

This is larger than the current smoke run but still not full-blown. It should
be enough to detect whether the tiny margin vanishes, flips, or appears
repeatedly across seeds.

Alternative cheaper version:

```text
replicates_per_arm = 8
episodes_per_arm = 8
```

Alternative stronger version:

```text
replicates_per_arm = 16
episodes_per_arm = 32
```

Project Owner answer:

```text
Pending.
```

## Seed Bundle Policy

The evaluation must preserve matched seed bundles.

For each replicate index `k`, Schema 0 and Schema 1 must use the same
seed-bundle identity so that paired differences are interpretable.

Required source evidence:

```text
seed_bundle_id
schema0_run_id
schema1_run_id
training_replicate_index
```

Consultant recommendation:

Use the existing second-serious comparison seed-bundle construction unless it
is discovered to vary any schema-independent randomness between arms.

Project Owner answer:

```text
Pending.
```

## Runner Architecture

Consultant recommendation:

Implement this as a new evaluation module that reuses the existing
second-serious schema-comparison runner with higher `replicates_per_arm` and
possibly higher `episodes_per_arm`, then writes replicate-focused aggregate
tables and readouts.

The new CLI surface should be:

```text
uv run python -m big_boy_benchmarking.cli counterpoint paired-replicate-probe run \
  --artifact-root <repo-readout-surface>/artifacts/<run-label> \
  --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json \
  --threshold-value 13.0 \
  --candidate-cap 1 \
  --episodes 16 \
  --replicates 8 \
  --locked-by foster \
  --linearization-mode tensor_available_disabled

uv run python -m big_boy_benchmarking.cli counterpoint paired-replicate-probe summarize \
  --artifact-root <repo-readout-surface>/artifacts/<run-label>
```

Implementation note:

This should not be a pile of manual `second-serious-comparison` reruns. The
artifact identity and readout should be replicate-probe-specific so the
human-readable report can summarize seed-paired distributions directly.

Project Owner answer:

```text
Pending.
```

## Required Artifact Tables

The evaluation must satisfy
`docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`.

At minimum, it should write:

```text
evaluation_manifest.json
evaluation_budget_lock.json
evaluation_run_index.csv
evaluation_aggregate_table.csv
evaluation_aggregate_summary.json
candidate_manifest.json
parent_source_manifest.json
replicate_probe_policy_manifest.json
readout_source.json
```

Required result tables:

```text
results/replicate_pair_summary.csv
results/paired_delta_distribution.csv
results/schema_arm_distribution.csv
results/post_hit_margin_distribution.csv
results/sustained_hit_rate_summary.csv
results/seed_bundle_summary.csv
results/lift_success_by_tier.csv
results/lift_failure_by_tier.csv
results/tower_shape_summary.csv
results/timing_summary.csv
```

Recommended table meanings:

| Table | One row per | Purpose |
| --- | --- | --- |
| `replicate_pair_summary.csv` | candidate group, seed bundle | paired status, speed delta, margin delta |
| `paired_delta_distribution.csv` | candidate group | aggregate paired win/loss/same counts |
| `schema_arm_distribution.csv` | schema arm | hit rates, median episode to hit, reward statistics |
| `post_hit_margin_distribution.csv` | schema arm and pair | threshold-margin evidence |
| `sustained_hit_rate_summary.csv` | schema arm | sustained/transient/never-hit rates |
| `seed_bundle_summary.csv` | replicate | seed identity and run mapping |
| `lift_success_by_tier.csv` | schema arm, active tier | action-realization success evidence |
| `lift_failure_by_tier.csv` | schema arm, active tier, reason | action-realization blocker evidence |
| `tower_shape_summary.csv` | schema arm, tier | quotient/tower shape evidence |

Project Owner answer:

```text
Pending.
```

## Readout Requirements

The repo readout surface must include:

```text
README.md
result_readout.md
artifact_index.md
glossary.md
method.md
runbook.md
results/summary.md
results/human_summary.md
results/paired_replicate_readout.md
results/margin_distribution_readout.md
results/timing_readout.md
badges/
readout_source.json
```

The README should start with badge signals such as:

- artifacts complete/incomplete;
- pair count;
- unblocked pair count;
- Schema 1 faster/slower/same counts;
- Schema 1 post-hit margin wins;
- sustained-hit rate difference;
- liftability semantics;
- lift failures;
- provenance repo artifacts.

The canonical readout regeneration command should be:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-root>/docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/readout_source.json
```

Project Owner answer:

```text
Pending.
```

## Goal Criteria

Goal 1:

```text
Detect whether Schema 1's tiny reward-margin signal survives across matched
seed bundles.
```

Success signal:

```text
Schema 1 has a positive paired post-hit margin in a meaningful majority of
unblocked pairs, with no liftability blocker.
```

Partial signal:

```text
Speed-to-hit remains equal or noisy, but Schema 1 has a weak positive margin
distribution.
```

Failure signal:

```text
The margin signal disappears, flips negative, or is blocked by lift failures
or artifact incompleteness.
```

Goal 2:

```text
Estimate whether the evaluation is worth scaling to a larger serious
comparison.
```

Success signal:

```text
The readout shows stable, interpretable paired distributions with enough
unblocked pairs to motivate a larger run.
```

## Claim Boundary

Allowed claims:

- this candidate/source chain remains executable under v0.7.2 pointwise
  semantics across the replicate probe;
- Schema 1 shows a positive, negative, equal, or inconclusive paired pattern
  under the locked threshold and modest budget;
- a larger serious comparison is or is not motivated by the observed paired
  distribution.

Forbidden claims:

- Schema 1 is generally better;
- Schema 1 wins statistically without a planned statistical test and adequate
  sample size;
- the result generalizes to other candidates or instances;
- tensorized behavior has been tested;
- reward margin implies musical quality;
- small paired evidence settles the main scientific claim.

## Stop Conditions

The implementation should stop and report if:

- the corrected candidate source no longer exposes an eligible candidate;
- `state_collapser` is not version `0.7.2` or newer with pointwise semantics
  available;
- paired seed-bundle identity cannot be preserved between schema arms;
- lift failures appear in a way that blocks behavioral interpretation;
- artifact/readout tables cannot represent pair-level evidence;
- generated readouts would need to be written outside the repo readout surface.

## Open Questions For Project Owner

### Question 1: Threshold Choice

Consultant recommendation if running this before threshold frontier:

```text
Use R = 13.0.
```

Consultant recommendation if threshold frontier runs first:

```text
Use the first threshold near the frontier where Schema 1 plausibly separates
from Schema 0 without both arms simply failing.
```

Project Owner answer:

```text
I agree.
```

### Question 2: Replicate Count

Consultant recommendation:

```text
Use 8 matched seed pairs for the first small replicate probe.
```

Project Owner answer:

```text
I agree.
```

### Question 3: Episode Budget

Consultant recommendation:

```text
Use 16 episodes per arm.
```

Project Owner answer:

```text
I agree.
```

### Question 4: Ordering Relative To Threshold Frontier

Consultant recommendation:

```text
Run threshold frontier first, then use its sharper threshold here.
```

Project Owner answer:

```text
I agree.
```

### Question 5: Summary Badge

Consultant recommendation:

```text
Badge pair count, unblocked pairs, Schema 1 margin wins, and sustained-hit rate
difference.
```

Project Owner answer:

```text
I agree.
```

## Blueprint Readiness

This blueprint is implementation-workplan ready if the Project Owner accepts
`R = 13.0`, `8` matched pairs, and `16` episodes per arm.

If the Project Owner wants the threshold-frontier probe to run first, this
blueprint should be revisited after the frontier readout identifies the most
informative threshold.
