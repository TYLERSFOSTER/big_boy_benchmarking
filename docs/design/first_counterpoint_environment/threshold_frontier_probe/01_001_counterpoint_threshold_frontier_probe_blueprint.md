# Counterpoint Threshold Frontier Probe Blueprint

Date: 2026-06-05

Status: draft blueprint with Project Owner answer slots

Repository:

```text
/Users/foster/big_boy_benchmarking
```

Design folder:

```text
docs/design/first_counterpoint_environment/threshold_frontier_probe/
```

Source orientation:

```text
docs/design/first_counterpoint_environment/threshold_frontier_probe/README.md
```

## Status And Authority

This is a design blueprint.

This is not an implementation gameplan.

This is not approval to edit source code.

This is not approval to run benchmark artifacts.

This is not approval to modify TeX documents at repo root.

This is not approval to change the `counterpoint_symbolic_v001` environment.

This is not approval to edit `/Users/foster/state_collapser`.

A later Phase.Stage.Action implementation gameplan must translate this
blueprint into executable work before source edits or benchmark runs begin.

## Source Authority

This blueprint follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`
- `docs/design/first_counterpoint_environment/threshold_frontier_probe/README.md`
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

The current `second_serious_schema_comparison` readout gives a first faint
positive signal for Schema 1, but not yet a speed-to-hit win and not yet a
general performance claim.

The corrected `R = 13.0` smoke-budget run has:

```text
Schema 0:
  hit_status = sustained_hit
  episodes_to_sustained_hit = 5
  post_hit_window_success_count = 4/5
  post_hit_window_min = 12.961363636363636

Schema 1:
  hit_status = sustained_hit
  episodes_to_sustained_hit = 5
  post_hit_window_success_count = 5/5
  post_hit_window_min = 13.169696969696968
  lift_failure rows = 0
```

That means the first next-measure question should be:

```text
Does Schema 1 continue to satisfy sustained-hit at stricter reward thresholds
than Schema 0 under matched candidate/seed/budget conditions?
```

This is a threshold-frontier question. It is not primarily a learning-speed
question.

## Executive Design

The threshold-frontier probe sweeps reward threshold `R` upward while holding
the corrected candidate chain, schema arms, seed policy, and small budget
mostly fixed.

The evaluation asks:

```text
Where is the sustained-hit frontier for Schema 0 versus Schema 1?
```

The intended bounded claim shape is:

```text
Under matched smoke-budget conditions for this corrected widened candidate,
Schema 1 either does or does not preserve sustained-hit at stricter thresholds
than Schema 0.
```

The evaluation must not claim:

- broad abstraction superiority;
- general musical quality;
- final serious statistical significance;
- tensor-enabled behavior;
- multi-candidate generality;
- speed-to-hit improvement unless the paired rows actually show it.

## Evaluation Identity

Consultant recommendation:

```text
evaluation_id = counterpoint_threshold_frontier_probe_v001
evaluation_run_family_id = counterpoint_symbolic_v001_threshold_frontier_probe_v001
```

Repo readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/
```

Default artifact root shape:

```text
docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts/<run_label>/
```

Consultant-recommended first run label:

```text
v072_pointwise_frontier_001
```

Project Owner answer:

```text
Agreed.
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

## Threshold Grid

Consultant recommendation:

```text
R = 12.0, 13.0, 13.25, 13.5, 13.75, 14.0
```

Reasoning:

- `12.0` preserves a reference row from the corrected successful run.
- `13.0` preserves the first faint-positive smoke signal.
- quarter-step increments probe the frontier without jumping directly past the
  likely interesting boundary.
- `14.0` is high enough to make failure plausible under the current tiny
  budget.

Alternative:

```text
R = 13.0, 13.5, 14.0
```

This is cheaper and simpler, but less informative about where the frontier
actually sits.

Project Owner answer:

```text
Go with recommendation.
```

## Budget

Consultant recommendation for first next-measure probe:

```text
candidate_cap = 1
replicates_per_arm = 1
episodes_per_arm = 8
window_length = 5
required_count = 4
base_seed = 0
```

Reasoning:

This intentionally keeps the first frontier probe close to the existing
`R = 12.0` and `R = 13.0` smoke runs. The point is not yet statistical
confidence. The point is to discover whether there is an immediate threshold
edge worth spending more compute on.

Alternative:

```text
episodes_per_arm = 16
```

This may give stricter thresholds more room to separate without becoming a
larger serious run.

Project Owner answer:

```text
Agreed.
```

## Runner Architecture

Consultant recommendation:

Implement this as a new evaluation module that composes the existing
second-serious schema-comparison runner once per threshold value, then
aggregates the threshold-indexed outputs into frontier-level tables.

The new CLI surface should be:

```text
uv run python -m big_boy_benchmarking.cli counterpoint threshold-frontier run \
  --artifact-root <repo-readout-surface>/artifacts/<run-label> \
  --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json \
  --threshold-values 12.0,13.0,13.25,13.5,13.75,14.0 \
  --candidate-cap 1 \
  --episodes 8 \
  --replicates 1 \
  --locked-by foster \
  --linearization-mode tensor_available_disabled

uv run python -m big_boy_benchmarking.cli counterpoint threshold-frontier summarize \
  --artifact-root <repo-readout-surface>/artifacts/<run-label>
```

Implementation note:

The underlying per-threshold run may reuse the existing
`second-serious-comparison` machinery, but the artifact identity should be
frontier-specific so the readout does not look like a pile of unrelated manual
reruns.

Project Owner answer:

```text
Agreed.
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
threshold_frontier_policy_manifest.json
readout_source.json
```

Required result tables:

```text
results/frontier_summary.csv
results/threshold_arm_summary.csv
results/threshold_pair_summary.csv
results/first_failure_frontier_summary.csv
results/post_hit_margin_summary.csv
results/lift_success_by_tier.csv
results/lift_failure_by_tier.csv
results/tower_shape_summary.csv
results/timing_summary.csv
```

Recommended table meanings:

| Table | One row per | Purpose |
| --- | --- | --- |
| `frontier_summary.csv` | candidate group | top-level frontier outcome and claim status |
| `threshold_arm_summary.csv` | threshold, schema arm | sustained-hit counts, median episodes, post-hit stats |
| `threshold_pair_summary.csv` | threshold, candidate group, seed pair | paired speed and margin deltas |
| `first_failure_frontier_summary.csv` | schema arm | first threshold where sustained-hit fails |
| `post_hit_margin_summary.csv` | threshold, schema arm | mean/min/success-count margins around threshold |
| `lift_success_by_tier.csv` | schema arm, active tier | action-realization success evidence |
| `lift_failure_by_tier.csv` | schema arm, active tier, reason | action-realization blocker evidence |
| `tower_shape_summary.csv` | schema arm, tier | quotient/tower shape evidence |

Project Owner answer:

```text
Agreed.
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
results/frontier_readout.md
results/threshold_table.md
results/paired_threshold_table.md
results/timing_readout.md
badges/
readout_source.json
```

The README should start with badge signals such as:

- artifacts complete/incomplete;
- thresholds tested;
- frontier status;
- highest shared passing threshold;
- highest Schema 1-only passing threshold, if any;
- liftability semantics;
- lift failures;
- provenance repo artifacts.

The canonical readout regeneration command should be:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/readout_source.json
```

Project Owner answer:

```text
Agreed.
```

## Goal Criteria

Goal 1:

```text
Detect whether Schema 1 has a stricter sustained-hit threshold frontier than
Schema 0 under matched smoke-budget conditions.
```

Success signal:

```text
There exists at least one threshold R where Schema 1 is sustained-hit and
Schema 0 is not, with no liftability or artifact blocker.
```

Partial signal:

```text
Both schemas pass/fail together, but Schema 1 has consistently stronger
post-hit margins near the frontier.
```

Failure signal:

```text
Schema 1 loses sustained-hit earlier than Schema 0, or the comparison is
blocked by lift failures/artifact incompleteness.
```

Goal 2:

```text
Identify a sharper threshold for a future paired-replicate probe.
```

Success signal:

```text
The frontier readout recommends a threshold where arm differences are plausible
but not trivially saturated.
```

## Claim Boundary

Allowed claims:

- this candidate/source chain is executable under v0.7.2 pointwise semantics;
- under the locked small budget, both arms pass/fail at listed thresholds;
- Schema 1 has, lacks, or may have a threshold-frontier advantage for this
  candidate and seed policy;
- the next replicate probe should use a named threshold from the frontier.

Forbidden claims:

- Schema 1 is generally better;
- Schema 1 learns faster unless paired `episodes_to_hit` deltas show that;
- the result is statistically stable across seeds;
- the result generalizes to other counterpoint instances;
- tensorized behavior has been tested;
- the result says anything about musical quality.

## Stop Conditions

The implementation should stop and report if:

- the corrected candidate source no longer exposes an eligible candidate;
- `state_collapser` is not version `0.7.2` or newer with pointwise semantics
  available;
- any threshold run has lift failures that invalidate the frontier claim;
- the existing second-serious runner cannot be composed without losing
  provenance;
- `readout_source.json` cannot represent threshold-indexed source files;
- generated readouts would need to be written outside the repo readout surface.

## Open Questions For Project Owner

### Question 1: Threshold Grid

Consultant recommendation:

```text
Use 12.0, 13.0, 13.25, 13.5, 13.75, 14.0.
```

Project Owner answer:

```text
Didn't we decide this above? What's going on?
```

### Question 2: Budget

Consultant recommendation:

```text
Keep the first frontier at candidate_cap=1, replicates=1, episodes=8.
```

Project Owner answer:

```text
I'm not answerign these last ones. You decide.
```

### Question 3: Evaluation Surface

Consultant recommendation:

```text
Create a new evaluation id and repo readout surface:
docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/
```

Project Owner answer:

```text
Pending.
```

### Question 4: Summary Badge

Consultant recommendation:

```text
Badge the highest shared passing threshold and whether any Schema 1-only
passing threshold exists.
```

Project Owner answer:

```text
Pending.
```

## Blueprint Readiness

This blueprint is close to implementation-gameplan ready after the Project
Owner answers the threshold grid and budget questions.

If the Project Owner accepts the consultant recommendations, no additional
design discussion is required before writing a Phase.Stage.Action gameplan.
