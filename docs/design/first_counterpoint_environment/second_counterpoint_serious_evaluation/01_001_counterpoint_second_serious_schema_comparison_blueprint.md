# Counterpoint Second Serious Schema Comparison Blueprint

Date: 2026-06-03

Status: draft blueprint

Repository:

```text
/Users/foster/big_boy_benchmarking
```

Design folder:

```text
docs/design/first_counterpoint_environment/second_counterpoint_serious_evaluation/
```

Source discussion:

```text
docs/design/first_counterpoint_environment/second_counterpoint_serious_evaluation/design_discussion.md
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
blueprint into executable work before source changes begin.

## Source Authority

This blueprint follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`
- `docs/design/first_counterpoint_environment/second_counterpoint_serious_evaluation/design_discussion.md`
- `docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_001_counterpoint_first_serious_learning_evaluation_blueprint.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/02_counterpoint_noisy_rate_contraction_diagnostics_blueprint.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic/01_counterpoint_noisy_rate_full_tower_training_diagnostic_blueprint.md`
- `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json`
- `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json`
- current BBB counterpoint environment, noisy-rate, tower-control, artifact,
  aggregation, docs-writer, and CLI source surfaces as read-only context.

## PO Attribution Ledger

This section records only Project Owner-originated scope, observations, and
requests visible in the design discussion or direct conversation. Consultant
interpretation appears in later sections under explicit consultant labels.

1. The Project Owner started a new serious evaluation design and specified that
   it remains in the same counterpoint environment:

   ```text
   Ok. I want to start a really serious new evaluation. It will be in the same
   counterpoint environment we've been using
   ```

2. The Project Owner asked for a folder to hold the discussion:

   ```text
   Make a folder for it, and then we'll have duscssion ther
   ```

3. The Project Owner described the central comparison:

   ```text
   what I want to compare here is training under two contraction schemata, with
   all other hyperparameters/knobs as equivalent as possible
   ```

4. The Project Owner identified Schema 0 as no contraction:

   ```text
   Schema 0 is "not contraction," so the agent stays in the total space the
   whole time
   ```

5. The Project Owner identified Schema 1 as sourced from either:

   ```text
   docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics
   ```

   or:

   ```text
   docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic
   ```

6. The Project Owner explicitly allowed Schema 1 to perform only one drop:

   ```text
   Even let it do only one drop, so that Schema 1 creates only tiers 0 and 1.
   ```

7. The Project Owner identified the need for a reward-cutoff knob for tier
   movement and suggested first-hit style measurement:

   ```text
   The reason we need a knob here is because we need to include reward cut-off
   for jumping up tier... it introduces an upperbound, so maybe what we
   actually measure is first to hit upperbound on total space.
   ```

8. The Project Owner clarified the upperbound hit as sustained performance:

   ```text
   I think maybe stayign above a certain level consistently.
   ```

9. The Project Owner corrected a consultant ambiguity: the two schemas are the
   comparison and need the same threshold:

   ```text
   the two Schema are what we're comparing ... it needs the same threshold for
   comparison
   ```

10. The Project Owner approved using a few carried-over Schema 1 examples:

   ```text
   Ah yeah a few carried over is better.
   ```

11. The Project Owner requested this blueprint:

   ```text
   I think this is ready to be turned into an extremely detailed blueprint
   ```

## Consultant Interpretation Summary

The design is ready for a full blueprint.

The main evaluation is a learning comparison, not a structural diagnostic.

The comparison object is:

```text
training under matched schema conditions
```

The variable of interest is contraction schema:

```text
Schema 0: no contraction / identity / total-space only
Schema 1: one-drop noisy-rate quotient with tiers 0 and 1
```

The primary outcome should be first passage to sustained total-space adequacy,
not merely final reward, not a one-episode reward spike, and not a structural
collapse classification.

The design should reuse the same comparison harness for both schemas as much
as possible. That is a fairness requirement. If Schema 0 is implemented through
an older direct learner while Schema 1 is implemented through tower-control
runtime, then the result mixes schema differences with runtime implementation
differences. This blueprint therefore treats Schema 0 as a no-contraction
schema arm inside the comparison harness, not as an unrelated direct baseline.

## Executive Design

This evaluation asks:

```text
Under matched training conditions, does a one-drop noisy-rate contraction
schema change time-to-sustained-total-space-adequacy relative to no
contraction?
```

The evaluation should run inside:

```text
counterpoint_symbolic_v001
```

The likely serious fixture remains:

```text
counterpoint_symbolic_n3_small_v001
```

The comparison uses two schema classes:

| Schema class | Informal name | Tower shape | Intended role |
| --- | --- | --- | --- |
| Schema 0 | no contraction / identity | total space only, or identity tower shell | matched no-contraction schema condition |
| Schema 1 | one-drop noisy-rate quotient | tier 0 base graph, tier 1 noisy-rate quotient | selected non-collapsed contraction schema condition |

The Schema 1 candidates should be selected from the full-tower training
diagnostic readout by default:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
```

That source is preferable because it has already filtered parent noisy-rate
examples for non-collapse and tower-training-health smoke evidence. The new
evaluation should still preserve provenance back to:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json
```

because that is where the structural noisy-rate candidates originated.

## Evaluation Class

Recommended evaluation class:

```text
schema_comparison_first_sustained_hit
```

This is a serious learning comparison.

It is not:

- a tower construction smoke;
- a structural collapse diagnostic;
- a noisy-rate candidate-selection diagnostic;
- a full-tower training-health diagnostic only;
- a direct-vs-tower comparison in the broad sense;
- a claim that abstraction is generally better;
- a musical-quality benchmark.

## Primary Evaluation Question

Primary question:

```text
When all ordinary knobs are held equivalent, does one-drop noisy-rate
contraction alter the training budget needed to reach sustained total-space
performance adequacy compared with no contraction?
```

The important phrase is:

```text
sustained total-space performance adequacy
```

This should mean that the learned policy stays above a locked threshold for a
locked persistence rule. The exact threshold and persistence rule remain open
for Project Owner selection, but the shape is settled:

- same threshold for Schema 0 and Schema 1;
- total-space criterion, not quotient-only criterion;
- sustained window, not isolated spike;
- first-hit / first-passage metric, not only final reward.

## Secondary Evaluation Questions

1. Do both schema conditions produce comparable artifact-complete training
   traces?
2. Does Schema 1 retain the tower-training-health properties observed in the
   prior smoke diagnostic under a serious comparison budget?
3. Does Schema 1 use tier 1 in a meaningful way, or does it mostly behave as a
   base-tier policy with tower metadata attached?
4. Does the no-contraction schema condition remain a fair total-space control
   under the same harness?
5. Are first-sustained-hit results consistent across training seeds?
6. Are results sensitive to which carried-over noisy-rate candidate is chosen?
7. Are non-hit runs distinguishable from artifact failures, lift failures,
   tier-control failures, or ordinary slow learning?
8. Does the generated human readout explain the comparison without requiring a
   reader to reconstruct raw event tables?

## Non-Goals

This evaluation must not claim:

- general tower superiority;
- general tower inferiority;
- general noisy-rate schema superiority;
- direct-vs-tower advantage outside this locked schema comparison;
- musical quality;
- tensor-enabled behavior;
- CUDA/GPU behavior;
- production performance;
- deep repeated quotient tower behavior;
- claims beyond the selected fixture, budget, learner family, seed policy, and
  linearization mode.

This evaluation must not change:

- `counterpoint_symbolic_v001` state enumeration;
- action enumeration;
- legality contract;
- reward semantics;
- terminal policy;
- action mask policy;
- noisy-rate parent diagnostic artifacts;
- `/Users/foster/state_collapser`.

## Recommended Evaluation Identity

Recommended evaluation id:

```text
counterpoint_second_serious_schema_comparison_v001
```

Recommended run family id:

```text
counterpoint_symbolic_v001_second_serious_schema_comparison_v001
```

Recommended run mode:

```text
serious_schema_comparison_first_sustained_hit
```

Recommended package:

```text
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/
```

Recommended CLI group:

```text
counterpoint second-serious-comparison
```

Recommended commands:

```text
counterpoint second-serious-comparison calibrate
counterpoint second-serious-comparison run
counterpoint second-serious-comparison summarize
```

Recommended repo readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/
```

Recommended artifact root shape:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/<run-label>/
```

Recommended design source reference:

```text
docs/design/first_counterpoint_environment/second_counterpoint_serious_evaluation/01_001_counterpoint_second_serious_schema_comparison_blueprint.md
```

Consultant note: the folder name `second_counterpoint_serious_evaluation` can
remain the design discussion folder, while the evaluation/readout id should be
more specific: `second_serious_schema_comparison`.

## Comparison Arms

### Arm Overview

The minimal serious comparison matrix is:

| Arm id | Schema class | Contraction | Runtime shape | Primary role |
| --- | --- | --- | --- | --- |
| `schema0_no_contraction` | Schema 0 | none / identity | matched comparison harness | total-space no-contraction condition |
| `schema1_noisy_rate_one_drop_<candidate>` | Schema 1 | selected noisy-rate block | matched comparison harness with tiers 0 and 1 | one-drop quotient condition |

The exact number of Schema 1 candidates remains open, but the Project Owner has
indicated that a few carried-over candidates is better than one.

### Schema 0: No-Contraction Condition

Schema 0 means:

```text
the agent stays in the total space for the whole run
```

Implementation should represent this as a no-contraction schema condition in
the same comparison harness wherever feasible.

Schema 0 should not silently mean:

- existing direct learner path with a different runner architecture;
- masked-random baseline;
- old first-serious direct-tabular-Q run reused as a comparator;
- an empty-schema tower result with different threshold semantics;
- a smoke-only control.

The reason is fairness: the evaluation compares schema conditions, not old
runner code against new runner code.

### Schema 1: One-Drop Noisy-Rate Condition

Schema 1 means:

```text
tier 0: total counterpoint space
tier 1: one noisy-rate quotient produced from a selected noisy-rate candidate
```

Schema 1 should use selected candidates from:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
```

Candidate provenance must preserve:

- parent noisy-rate contraction diagnostic source;
- full-tower training-health diagnostic source;
- candidate id;
- instance id;
- arm id;
- requested rate;
- numerator;
- denominator;
- schema seed;
- selected-edge count/share;
- selected-source share;
- zero-selected-source count;
- tier state-cell-count sequence;
- tier active-action-cell-count sequence;
- parent training-health status;
- parent concrete-step evidence;
- parent learner-update evidence.

## Candidate Selection Policy

### Default Candidate Source

Default source binding:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
```

This source should be used because it selects examples that are:

- non-collapsed in the noisy-rate contraction diagnostic;
- rebuilt as one-drop towers;
- smoke-validated for tower-only training health.

### Parent Provenance Source

The new evaluation should also preserve the parent structural source:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json
```

That source remains important because it explains:

- how noisy-rate edges were selected;
- why source-local minimum-one behavior was avoided;
- which rates and schema seeds were tested;
- whether metadata and runtime selected edges matched;
- source coverage and zero-selected-source behavior;
- tower shape before training-health filtering.

### Candidate Count

Project Owner-originated direction:

```text
a few carried over is better
```

Consultant recommendation:

```text
Use 2-4 Schema 1 candidates for the first serious comparison.
```

Rationale:

- one candidate is too brittle;
- all candidates may be too expensive for the first serious comparison;
- a few candidates allow candidate sensitivity to be visible without turning
  the evaluation into another noisy-rate sweep.

### Candidate Mix

Consultant recommendation:

Use the already smoke-clean `p001_over_144` candidates first, because the
current full-tower training-health smoke readout contains:

```text
counterpoint_symbolic_n3_small_v001-p001_over_144-schema0
counterpoint_symbolic_n3_small_v001-p001_over_144-schema1
```

If the Project Owner wants broader coverage, add one candidate from a denser
rate such as `p001_over_036` or `p001_over_018` only after verifying that those
candidates have equivalent full-tower training-health evidence or running a
larger candidate-health pass first.

### Candidate Manifest

Implementation must write:

```text
candidate_manifest.json
```

It must include:

- selected Schema 1 candidates;
- excluded candidates;
- exclusion reasons;
- parent readout source path;
- full-tower training readout source path;
- parent contraction diagnostic readout source path;
- candidate selection rules;
- candidate cap;
- deterministic sort order;
- exact candidate rows copied from source tables.

## Matched Harness Requirement

This evaluation must minimize differences between Schema 0 and Schema 1 that
are not the contraction schema itself.

Hold fixed wherever possible:

- environment family;
- environment instance;
- initial-state policy;
- horizon;
- reward function;
- action mask semantics;
- learner family;
- learning-rate schedule;
- exploration policy;
- discount factor;
- episode budget;
- training seed bundle;
- threshold criterion;
- threshold persistence window;
- artifact schema;
- run-index schema;
- aggregation logic;
- timing categories;
- linearization mode.

Allow to differ:

- contraction schema;
- quotient/tier structure implied by the schema;
- controller behavior that is necessarily schema-dependent;
- tier-transition events that cannot exist in Schema 0;
- lift/fiber evidence that is meaningful only for Schema 1.

## Success Criterion: First Sustained Total-Space Hit

### Concept

The core outcome should be:

```text
first sustained total-space hit
```

Meaning:

```text
the earliest episode index or training-step index at which the run enters a
locked persistence window in which total-space performance remains above the
locked threshold.
```

This should be computed for each run.

### Why Sustained Hit Instead Of Final Reward

The Project Owner noted that the reward cutoff / tier-jump knob introduces an
upper bound.

If both arms can saturate, then final reward may hide the training-speed
difference. First sustained hit preserves the question:

```text
which schema condition reaches adequate total-space behavior sooner under the
same threshold?
```

### Required Fields

Every per-run summary should record:

- `hit_threshold_value`;
- `hit_metric_id`;
- `hit_persistence_rule_id`;
- `hit_persistence_window_length`;
- `hit_persistence_required_count`;
- `first_hit_episode_index`;
- `first_sustained_hit_episode_index`;
- `first_sustained_hit_training_step`;
- `hit_status`;
- `episodes_to_sustained_hit`;
- `training_steps_to_sustained_hit`;
- `post_hit_window_mean`;
- `post_hit_window_min`;
- `post_hit_window_success_count`;
- `hit_failure_reason`, when no hit occurs.

### Suggested Hit Status Values

Use explicit statuses:

| Status | Meaning |
| --- | --- |
| `sustained_hit` | Run reached the threshold under the persistence rule. |
| `transient_hit_only` | Run crossed threshold at least once but did not sustain it. |
| `never_hit` | Run never crossed the threshold. |
| `artifact_incomplete` | Required evidence is missing. |
| `runtime_failed` | Runtime failed before metric interpretation. |
| `structural_blocked` | Schema structure blocked meaningful comparison. |

## Threshold And Persistence Policy

The exact threshold remains an open Project Owner decision.

This blueprint recommends designing the implementation so the threshold policy
is a named manifest object rather than a hidden constant.

Recommended manifest shape:

```json
{
  "threshold_policy_id": "counterpoint_total_space_sustained_reward_v001",
  "metric_id": "episode_total_reward",
  "threshold_value": "<locked value>",
  "window_length": "<locked integer>",
  "required_count": "<locked integer>",
  "comparison": "greater_than_or_equal",
  "scope": "total_space",
  "applies_to_schema_classes": ["schema0_no_contraction", "schema1_noisy_rate_one_drop"]
}
```

Possible threshold strategies:

1. Use an absolute reward cutoff derived from environment reward semantics.
2. Use a percentile or target derived from a calibration run.
3. Use a fixed success predicate derived from terminal or near-terminal state
   quality if such a predicate is already available.
4. Use a run-budget-normalized criterion if episode reward is too noisy.

Consultant recommendation:

Use calibration to propose the threshold, then lock it before the serious run.
Do not set the threshold after looking at serious-run outcomes.

## Tier-Jump / Reward-Cutoff Knob

The design discussion identifies a reward cutoff for jumping up tier.

This must be explicit in the evaluation contract.

Recommended fields:

- `tier_jump_policy_id`;
- `tier_jump_reward_cutoff`;
- `tier_jump_metric_id`;
- `tier_jump_window_length`, if movement uses smoothing;
- `tier_jump_min_observations`;
- `tier_jump_applies_to_schema0`;
- `tier_jump_applies_to_schema1`;
- `tier_jump_disabled_reason`, when not applicable.

Important distinction:

```text
The tier-jump cutoff may control movement between tiers, but the comparison
threshold measures total-space sustained adequacy.
```

Do not conflate:

- tier-jump eligibility;
- first sustained total-space hit;
- final reward;
- tower training health.

For Schema 0, tier-jump events may be not applicable because there is no
non-base tier. The implementation should still record the same threshold policy
and explain why tier-jump events are absent.

## Calibration Mode

This serious evaluation should have a calibration mode before a locked serious
run.

Calibration should answer:

- What threshold value is sane?
- What persistence window is neither too spiky nor too impossible?
- What episode budget is adequate to distinguish never-hit from slow-hit?
- Does Schema 0 in the matched harness execute cleanly?
- Do selected Schema 1 candidates still execute cleanly under the proposed
  threshold/tier-jump mechanics?

Calibration must not become the final result.

Calibration artifacts should be clearly separated:

```text
run_mode: calibration
```

Serious artifacts should use:

```text
run_mode: serious_schema_comparison_first_sustained_hit
```

## Recommended Budget Shape

Exact budget is not yet settled.

Consultant recommendation for blueprint-level shape:

| Run mode | Candidate count | Schema 0 reps | Schema 1 reps per candidate | Episodes | Purpose |
| --- | ---: | ---: | ---: | ---: | --- |
| smoke | 1 | 1 | 1 | 4-8 | command/artifact sanity only |
| calibration | 2 | 2-4 | 2-4 | 32-64 | choose threshold/window/budget |
| serious locked run | 2-4 | 8-16 | 8-16 | 128-512 | first serious comparison evidence |

Budget should be locked before serious execution in:

```text
evaluation_budget_lock.json
```

The implementation gameplan should not run the serious locked budget without
explicit Project Owner authorization if the gameplan only authorizes
implementation smoke.

## Seed Policy

The evaluation needs separate seed concepts:

- environment seed;
- learner initialization seed;
- exploration seed;
- schema seed for Schema 1 candidate selection;
- run replicate seed;
- candidate selection seed, if selection is stochastic;
- calibration seed bundle;
- serious run seed bundle.

Recommended policy:

- candidate selection is deterministic from source readout tables;
- Schema 0 and Schema 1 receive matched training seed bundles;
- Schema 1 candidate seed is part of candidate identity, not sampled during
  the serious run;
- every run writes `seed_bundle.json`;
- aggregate tables can pair Schema 0 and Schema 1 rows by matched training seed
  where possible.

## Pairing And Comparison Design

The comparison should avoid treating all rows as unrelated if matched seeds
are available.

Recommended pairing keys:

```text
environment_instance_id
training_seed_bundle_id
learner_config_id
threshold_policy_id
budget_id
schema1_candidate_group_id
```

For each Schema 1 candidate, compare:

```text
Schema 1 candidate under seed bundle k
against
Schema 0 no-contraction under seed bundle k
```

This allows:

- paired hit-time delta;
- paired hit-status comparison;
- paired artifact status comparison;
- candidate-specific comparison;
- aggregate candidate-set summary.

Do not report a schema advantage from unpaired means alone if paired seeds were
available but ignored.

## Environment And Fixture Scope

Environment family:

```text
counterpoint_symbolic_v001
```

Recommended serious instance:

```text
counterpoint_symbolic_n3_small_v001
```

Smoke instance:

```text
counterpoint_symbolic_n3_tiny_v001
```

The `tiny` instance is only for command, artifact, and contract smoke.

Serious claims should not use `tiny`.

The current blueprint does not include `medium` by default. `medium` can become
a later validation extension if the small-fixture comparison is interpretable.

## Learner And Runtime Scope

The learner should remain in the current repo/upstream learner family unless
the Project Owner explicitly authorizes a new learner design.

Likely learner class:

```text
CounterpointTierLearner
```

or the local wrapper already used for noisy-rate full-tower training.

Implementation should preserve persistent learner state across episodes inside
a training replicate.

Do not implement this as independent episode-local probes.

## Linearization Mode

Default linearization mode:

```text
tensor_available_disabled
```

This is a tensor-capable package with tensor execution disabled.

This evaluation must not claim:

- tensor-enabled CPU behavior;
- tensor-enabled CUDA behavior;
- GPU performance.

Reserved future modes:

```text
tensor_enabled_cpu
tensor_enabled_cuda
```

## Artifact Contract

The evaluation must satisfy the evaluation construction protocol.

Every durable run should write machine-readable artifacts under:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/<run-label>/
```

Expected evaluation root:

```text
<artifact-root>/evaluations/counterpoint_second_serious_schema_comparison_v001/
```

Expected repo readout source:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/readout_source.json
```

## Required Evaluation-Level Manifests

Required manifests:

- `evaluation_manifest.json`;
- `evaluation_arm_manifest.json`;
- `evaluation_budget_lock.json`;
- `threshold_policy_manifest.json`;
- `candidate_manifest.json`;
- `parent_source_manifest.json`;
- `evaluation_run_index.csv`;
- `evaluation_aggregate_table.csv`;
- `evaluation_aggregate_summary.json`;
- `readout_source.json`.

## Required Per-Run Artifacts

Each run should write:

- `run_manifest.json`;
- `seed_bundle.json`;
- `mode_manifest.json`;
- `linearization_manifest.json`;
- `schema_manifest.json`;
- `threshold_policy_manifest.json`;
- `tier_jump_policy_manifest.json`;
- `episodes.csv`;
- `step_events.csv`;
- `control_events.csv`, when using tower/control harness;
- `tier_transition_events.csv`, when applicable;
- `lift_fiber_events.csv`, when applicable;
- `abc_selection_events.csv`, when applicable;
- `abc_tier_signal_events.csv`, when applicable;
- `learner_update_events.csv`;
- `threshold_window_events.csv`;
- `first_hit_summary.json`;
- `timing_segments.csv`;
- `timing_summary.json`;
- `warnings.jsonl`.

For Schema 0, tower-only files may be structurally not applicable if the
matched harness has no non-base tier. Absence must be recorded in
`expected_files`, not left implicit.

## Required Evaluation-Level Result Tables

The summarizer should write:

- `results/arm_summary.csv`;
- `results/candidate_summary.csv`;
- `results/schema_summary.csv`;
- `results/training_episode_summary.csv`;
- `results/training_curve_summary.csv`;
- `results/threshold_window_summary.csv`;
- `results/first_sustained_hit_summary.csv`;
- `results/paired_schema_comparison.csv`;
- `results/schema0_total_space_summary.csv`;
- `results/schema1_candidate_summary.csv`;
- `results/tower_shape_summary.csv`;
- `results/tier_occupancy_summary.csv`;
- `results/tier_executability_summary.csv`;
- `results/lift_success_by_tier.csv`;
- `results/lift_failure_by_tier.csv`;
- `results/concrete_step_summary.csv`;
- `results/controller_action_summary.csv`;
- `results/abc_selection_summary.csv`;
- `results/abc_tier_signal_summary.csv`;
- `results/learner_update_summary.csv`;
- `results/timing_summary.csv`;
- `results/training_health_summary.csv`;
- `results/comparison_claim_summary.csv`.

## Result Table Semantics

### `first_sustained_hit_summary.csv`

One row per run.

Required fields:

- `evaluation_id`;
- `run_id`;
- `schema_class`;
- `schema_arm_id`;
- `candidate_id`;
- `training_replicate_index`;
- `training_seed_bundle_id`;
- `threshold_policy_id`;
- `threshold_value`;
- `window_length`;
- `required_count`;
- `hit_status`;
- `first_hit_episode_index`;
- `first_sustained_hit_episode_index`;
- `first_sustained_hit_training_step`;
- `episodes_to_sustained_hit`;
- `training_steps_to_sustained_hit`;
- `post_hit_window_mean`;
- `post_hit_window_min`;
- `hit_failure_reason`.

### `paired_schema_comparison.csv`

One row per matched Schema 0 / Schema 1 pair.

Required fields:

- `evaluation_id`;
- `pair_id`;
- `schema1_candidate_id`;
- `training_seed_bundle_id`;
- `schema0_run_id`;
- `schema1_run_id`;
- `schema0_hit_status`;
- `schema1_hit_status`;
- `schema0_episodes_to_sustained_hit`;
- `schema1_episodes_to_sustained_hit`;
- `delta_schema1_minus_schema0_episodes_to_hit`;
- `schema0_artifact_status`;
- `schema1_artifact_status`;
- `comparison_interpretation`;
- `claim_allowed`;
- `claim_blocked_reason`.

### `comparison_claim_summary.csv`

One row per evaluation/candidate group.

Required fields:

- `evaluation_id`;
- `artifact_run_label`;
- `schema1_candidate_group_id`;
- `schema0_run_count`;
- `schema1_run_count`;
- `paired_count`;
- `schema0_sustained_hit_count`;
- `schema1_sustained_hit_count`;
- `schema0_median_episodes_to_hit`;
- `schema1_median_episodes_to_hit`;
- `median_paired_delta_episodes_to_hit`;
- `schema1_faster_pair_count`;
- `schema1_slower_pair_count`;
- `same_status_pair_count`;
- `mixed_or_blocked_pair_count`;
- `claim_scope`;
- `claim_text_if_supported`;
- `claim_text_if_blocked`;

## Aggregation And Statistics

This first serious comparison should use simple, auditable statistics.

Recommended summaries:

- hit counts by schema class;
- sustained-hit rate by schema class;
- median episodes to sustained hit by schema class;
- paired deltas by candidate and training seed;
- candidate-level median paired delta;
- overall candidate-set median paired delta;
- number of pairs where Schema 1 is faster;
- number of pairs where Schema 1 is slower;
- number of pairs where statuses differ but no numeric delta is meaningful;
- artifact/runtime failure classification.

Avoid overclaiming from small samples.

If sample size is small, the readout should say:

```text
directional serious diagnostic evidence
```

not:

```text
statistically established superiority
```

unless a later design explicitly adds statistical testing and sufficient
replication.

## Claim Boundary

Allowed claims if evidence supports them:

- the evaluation ran with repo-resident artifacts;
- both schema conditions used the locked threshold policy;
- Schema 0 and Schema 1 were compared under matched training conditions;
- selected Schema 1 one-drop candidates reached, failed to reach, or reached
  faster/slower than Schema 0 under the locked sustained-hit criterion;
- candidate-specific sensitivity was observed or not observed;
- structural/runtime blockers did or did not occur.

Blocked claims:

- general abstraction advantage;
- general noisy-rate advantage;
- general tower advantage;
- performance beyond selected candidate set;
- performance beyond `counterpoint_symbolic_v001`;
- performance beyond the locked fixture;
- tensor-enabled performance;
- GPU/CUDA performance;
- musical quality;
- deep tower behavior;
- claims based on final reward alone if the primary sustained-hit criterion is
  not met or not interpretable.

## Structural Limit Checks

Declare these checks before implementation:

| Check id | Trigger | Interpretation | Claim effect |
| --- | --- | --- | --- |
| `schema1_collapsed_tier` | Schema 1 tier 1 has one or fewer state cells | one-drop quotient lost meaningful abstraction | block comparison claim for that candidate |
| `schema1_non_executable_tier` | Schema 1 deepest tier has zero active action cells | quotient tier cannot support action selection | block comparison claim for that candidate |
| `schema1_no_tier1_use` | tier 1 selected/use share below locked minimum | Schema 1 behaved mostly as base-tier training | downgrade or qualify claim |
| `schema1_lift_failure_dominant` | lift failures exceed locked threshold | comparison confounded by lift/action-realization failure | block or classify as runtime failure |
| `schema0_harness_mismatch` | Schema 0 did not use matched harness/threshold policy | no fair schema comparison | block comparison claim |
| `threshold_unreached_all` | neither schema reaches threshold | no speed comparison; only failure/non-hit evidence | block speed claim |
| `threshold_saturated_immediately` | both schemas satisfy threshold from initial episodes | threshold too weak | block serious comparison claim |
| `artifact_incomplete` | required files missing | evidence incomplete | block all substantive claims |

## Expected-File Policy

The implementation must generate `readout_source.json` with:

```json
{
  "expected_files": {
    "required": [
      "evaluation_manifest.json",
      "evaluation_arm_manifest.json",
      "evaluation_budget_lock.json",
      "threshold_policy_manifest.json",
      "candidate_manifest.json",
      "evaluation_run_index.csv",
      "evaluation_aggregate_table.csv",
      "evaluation_aggregate_summary.json",
      "results/first_sustained_hit_summary.csv",
      "results/paired_schema_comparison.csv",
      "results/comparison_claim_summary.csv",
      "results/training_episode_summary.csv",
      "results/training_curve_summary.csv",
      "results/learner_update_summary.csv"
    ],
    "expected_absent_is_gap": [],
    "conditional": {
      "schema1_tower_control": [
        "results/tower_shape_summary.csv",
        "results/tier_occupancy_summary.csv",
        "results/lift_success_by_tier.csv",
        "results/lift_failure_by_tier.csv",
        "results/abc_selection_summary.csv",
        "results/abc_tier_signal_summary.csv"
      ],
      "calibration": [
        "calibration_summary.json",
        "calibration_run_index.csv",
        "calibration_recommendation.md"
      ]
    },
    "not_applicable": [
      "direct-vs-tower generic baseline result",
      "deep repeated tower artifacts",
      "tensor-enabled conversion records",
      "CUDA/GPU timing records",
      "musical-quality judgments"
    ],
    "expectation_sources": [
      "docs/design/first_counterpoint_environment/second_counterpoint_serious_evaluation/01_001_counterpoint_second_serious_schema_comparison_blueprint.md"
    ]
  }
}
```

## Goal Criteria For Readout

The source binding should include goal criteria.

Recommended goal ids:

### `matched_schema_comparison`

Question:

```text
Did both schema conditions run under the same threshold, budget, learner, seed,
and harness policy?
```

Success signal:

```text
evaluation_arm_manifest and evaluation_budget_lock show matched policies;
paired_schema_comparison.csv has nonzero paired_count.
```

Failure signal:

```text
Schema 0 and Schema 1 use incompatible runner/threshold policies or cannot be
paired.
```

Allowed claim if met:

```text
This run supports a bounded schema comparison under the locked conditions.
```

### `first_sustained_hit_measurement`

Question:

```text
Was first sustained total-space hit measured for each run?
```

Success signal:

```text
first_sustained_hit_summary.csv records hit statuses and hit indices for all
successful runs.
```

Failure signal:

```text
hit policy is missing or hit summaries are absent.
```

Allowed claim if met:

```text
The readout may discuss time-to-sustained-adequacy.
```

### `schema1_runtime_integrity`

Question:

```text
Did one-drop Schema 1 candidates remain executable and produce meaningful
tower traces?
```

Success signal:

```text
tower_shape, tier_occupancy, lift, concrete-step, and learner-update summaries
are present and healthy.
```

Failure signal:

```text
Schema 1 collapses, cannot execute, or does not use tier 1.
```

Allowed claim if met:

```text
Schema 1 comparison results are not blocked by tower-runtime health failures.
```

### `claim_boundary_enforced`

Question:

```text
Does the readout avoid unsupported broad claims?
```

Success signal:

```text
comparison_claim_summary.csv and README claim boundary agree.
```

Failure signal:

```text
README or result docs imply broad tower/noisy-rate superiority from a narrow
run.
```

Allowed claim if met:

```text
The result is interpretable within its bounded scope.
```

## Human-Readable Readout Requirements

The repo readout surface should include:

- `README.md`;
- `method.md`;
- `runbook.md`;
- `artifact_index.md`;
- `glossary.md`;
- `result_readout.md`;
- `results/summary.md`;
- `results/human_summary.md`;
- `results/arm_readout_table.md`;
- `results/diagnostic_findings.md`;
- `results/paired_comparison_readout.md`;
- `results/threshold_policy_readout.md`;
- `results/timing_readout.md`;
- `badges/`.

README must include:

- local badge strip;
- `Status At A Glance`;
- `Summary of Goals Behind this Evaluation`;
- `Summary of Methodology Behind this Evaluation`;
- one-screen verdict;
- schema-arm table;
- first sustained hit summary;
- paired comparison summary;
- claim boundary;
- source binding command;
- clarifying-turn section.

Canonical readout command:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/readout_source.json
```

## Badges

Recommended badge dimensions:

- `Artifacts`;
- `Comparison`;
- `Hit Metric`;
- `Schema 1 Runtime`;
- `Claim Scope`;
- `Provenance`.

Possible labels:

| Badge | Green | Yellow | Red/Orange |
| --- | --- | --- | --- |
| `Artifacts` | complete | partial | missing |
| `Comparison` | paired | mixed | unpaired/blocked |
| `Hit Metric` | sustained hits measured | partial | threshold invalid |
| `Schema 1 Runtime` | executable | warnings | blocked |
| `Claim Scope` | serious bounded | diagnostic only | unsupported |
| `Provenance` | repo artifacts | partial | outside repo |

## CLI Design

Recommended command shape:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison calibrate \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/<calibration-label> \
  --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json \
  --candidate-cap <n> \
  --episodes <episodes> \
  --replicates <replicates> \
  --locked-by <operator-or-run-id> \
  --linearization-mode tensor_available_disabled
```

```bash
uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison run \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/<run-label> \
  --candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json \
  --candidate-cap <n> \
  --episodes <episodes> \
  --replicates <replicates> \
  --threshold-policy-id <policy-id> \
  --threshold-value <value> \
  --window-length <n> \
  --required-count <n> \
  --locked-by <operator-or-run-id> \
  --linearization-mode tensor_available_disabled
```

```bash
uv run python -m big_boy_benchmarking.cli counterpoint second-serious-comparison summarize \
  --artifact-root docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts/<run-label>
```

## Tests Required By Implementation

Implementation should add tests for:

- id constants exported and noncolliding;
- repo-resident artifact-root validation;
- candidate source binding resolution;
- parent provenance preservation;
- deterministic candidate selection;
- no-contraction Schema 0 arm construction;
- one-drop Schema 1 arm construction;
- matched threshold policy applied to both schemas;
- persistent learner state across episodes;
- first-hit and first-sustained-hit computation;
- transient-hit-only classification;
- never-hit classification;
- paired comparison aggregation;
- readout source generation;
- expected-file policy;
- docs writer output;
- README turn-section preservation;
- CLI calibrate/run/summarize parser behavior;
- unsupported linearization mode rejection;
- no TeX/root document side effects.

## Stop Conditions Before Implementation

Stop and ask the Project Owner before implementation if:

- the threshold metric cannot be defined;
- the threshold value must be chosen by looking at serious-run outcomes;
- the persistence window cannot be chosen;
- Schema 0 cannot be represented in the matched comparison harness;
- Schema 1 cannot reuse carried-over full-tower diagnostic candidates;
- candidate selection yields no eligible candidates;
- the implementation would need to edit `/Users/foster/state_collapser`;
- the implementation would change `counterpoint_symbolic_v001`;
- the implementation would omit source binding, expected-file policy, goal
  criteria, methodology sources, or claim boundary;
- the evaluation would become another structural diagnostic rather than a
  schema learning comparison;
- full serious budget execution is being considered without explicit Project
  Owner authorization.

## Open Questions For Project Owner

These are consultant-authored questions. They are not Project Owner turns.

1. What metric should define total-space adequacy: episode total reward,
   rolling mean reward, terminal success predicate, or another existing
   counterpoint quality metric?
   - *PO:* Explain.
   - *Codex:* Use `episode_total_reward` as the primitive total-space adequacy
     metric. The reason is that both Schema 0 and Schema 1 ultimately receive
     reward from the same concrete counterpoint environment, so episode total
     reward is the cleanest shared signal that does not depend on quotient-tier
     internals. Do not use a quotient-only metric, and do not introduce a new
     terminal success predicate unless the reward contract is versioned to
     define one. Keep rolling/window logic out of the primitive metric itself;
     the "staying above a certain level consistently" part belongs in the
     persistence rule below. The readout should still record secondary
     diagnostics such as concrete step count, termination/truncation, final
     state, tier occupancy, and learner updates, but those should explain the
     hit result rather than define it.
2. Should the threshold be chosen by calibration, by an absolute value from the
   reward contract, or by a Project Owner-specified target?
   - *PO:* Pick the most reasonable, and then we cna calibrate after first evaluation assessment.
   - *Codex:* Choose a calibration-derived absolute reward threshold, then lock
     it before the serious comparison run. The first assessment should be a
     calibration/readiness pass, not the final evidence run. From that
     calibration pass, choose a single numeric `episode_total_reward` threshold
     that is high enough to represent meaningful total-space adequacy but not
     so high that neither schema can plausibly sustain it. Once chosen, the
     threshold becomes an absolute manifest value shared by Schema 0 and all
     Schema 1 candidates. Do not tune the threshold after looking at the
     serious-run outcomes.
3. What persistence rule should count as "staying above a certain level
   consistently": consecutive episodes, `k` of `n` rolling episodes, or a
   rolling mean/min threshold?
   - *PO:* You decide and report back. We might change with finetune.
   - *Codex:* Use a `k` of `n` rolling-window rule over per-episode total
     reward. Recommended starting default: `4` of `5` consecutive episodes
     must have `episode_total_reward >= threshold_value`. This is stricter than
     a one-episode spike but less brittle than requiring every episode in a
     window to clear the threshold. The first sustained hit is the first
     episode index at which such a completed window exists. Record both the
     first transient hit and the first sustained hit, because a schema that
     spikes early but cannot sustain performance is substantively different
     from a schema that never reaches the threshold at all.
4. How many carried-over Schema 1 candidates should be included in the first
   serious locked run?
   - *PO:* 4
5. Should the first locked run use only `p001_over_144` candidates from the
   full-tower training smoke, or should it include denser candidates after an
   expanded candidate-health pass?
   - *PO:* Same.
6. Should a separate old direct-tabular-Q run appear only as a sanity anchor,
   or should the readout omit it entirely to keep the schema comparison clean?
   - *PO:* Keep comparison clean. Omit entirely.
7. What budget size is acceptable for the serious run after calibration:
   roughly 128, 256, or 512 episodes per replicate?
   - *PO:* `256` to start.
8. Should the first serious comparison stay on `small`, or should a `medium`
   validation extension be planned but decision-locked?
   - *PO:* `medium`

## Consultant Recommendations Pending Project Owner Confirmation

These are recommendations, not Project Owner decisions.

1. Use `episode_total_reward` as the first threshold metric if it is already
   consistently emitted and interpretable.
2. Choose the threshold through calibration, then lock it before serious
   execution.
3. Use a `k` of `n` rolling-window persistence rule rather than strict
   consecutive episodes, because strict consecutive success may be too brittle.
4. Use two Schema 1 candidates for the first serious locked run if no expanded
   candidate-health run is authorized.
5. Use the two currently smoke-clean `p001_over_144` candidates first.
6. Keep any old direct-tabular-Q result out of the primary comparison table.
7. Treat Schema 0 as no-contraction inside the matched harness.
8. Make the initial implementation smoke small and run the serious locked
   budget only after explicit Project Owner authorization.

## Blueprint Completion Criteria

This blueprint is complete enough to produce a Phase.Stage.Action implementation
gameplan once the Project Owner either answers the open questions or accepts
consultant defaults for them.

It is not complete enough to run the serious evaluation directly.

The next artifact should be:

```text
docs/design/first_counterpoint_environment/second_counterpoint_serious_evaluation/01_002_counterpoint_second_serious_schema_comparison_implementation_gameplan.md
```

That gameplan must follow Phase.Stage.Action discipline and preserve all stop
conditions above.
