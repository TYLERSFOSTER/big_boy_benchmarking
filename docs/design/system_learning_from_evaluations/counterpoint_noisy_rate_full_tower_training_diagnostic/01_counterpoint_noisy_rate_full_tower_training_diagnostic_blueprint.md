# Counterpoint Noisy-Rate Full-Tower Training Diagnostic Blueprint

Date: 2026-06-02

Status: draft blueprint

Repository:

```text
/Users/foster/big_boy_benchmarking
```

Design folder:

```text
docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic/
```

## Status And Authority

This is a design blueprint.

This is not an implementation gameplan.

This is not approval to edit source code.

This is not approval to run benchmark artifacts.

This is not approval to change the `counterpoint_symbolic_v001`
environment.

This is not approval to edit `/Users/foster/state_collapser`.

This blueprint turns the Project Owner's stated next evaluation shape into a
concrete design target. A later Phase.Stage.Action implementation gameplan
must translate this blueprint into executable work before source changes
begin.

## Source Authority

This blueprint follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`
- `docs/design/system_learning_from_evaluations/README.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/README.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/02_counterpoint_noisy_rate_contraction_diagnostics_blueprint.md`
- `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic/design_discussion.md`
- `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/README.md`
- current BBB counterpoint noisy-rate/tower-control/evaluation source surfaces
  as read-only context

## PO Attribution Ledger

This section records only Project Owner-originated scope, observations, and
requests. Consultant interpretation appears later under explicit consultant
labels.

1. The Project Owner asked whether the repo is ready to quickly blueprint a
   "full train for each of the examples here," meaning build the full tower and
   train on it, still with no real comparison.

2. The Project Owner confirmed the intended meaning as:

   ```text
   take each non-collapsed noisy-rate counterpoint tower from the current
   diagnostic, build its full available tower, then run a real tower-only
   training budget on it with no direct baseline comparison
   ```

3. The Project Owner asked to start this design work in:

   ```text
   docs/design/system_learning_from_evaluations
   ```

4. The Project Owner then requested generation of the blueprint in:

   ```text
   docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic
   ```

## Consultant Sufficiency Judgement

There is enough information to write a full blueprint.

There is not yet enough Project Owner authority to implement it.

The key design is clear:

```text
Use the non-collapsed noisy-rate towers already surfaced by the noisy-rate
diagnostic as candidate examples, then run tower-only training on those towers
without adding direct baselines or comparison claims.
```

The remaining ambiguities are normal blueprint-level choices:

- exact training budget;
- whether the no-contraction control is omitted or kept as a runtime sanity
  anchor;
- whether learner state must persist across episodes;
- how many candidates to include if a later parent diagnostic produces many
  non-collapsed examples;
- exact pass/warn/fail thresholds for "trained cleanly."

This blueprint gives consultant recommendations for those points while keeping
them visibly separate from Project Owner decisions.

## Executive Design

The parent noisy-rate contraction diagnostic answered a structural/runtime
question:

```text
If noisy-rate contraction removes the source-local minimum-one floor, does the
first quotient projection still immediately collapse?
```

The current smoke readout says no for the observed small-fixture arms/seeds.
It produced non-collapsed first-projection towers such as:

```text
no_contraction_control, seed 0: [108]
p001_over_144, seed 0:       [108, 100]
p001_over_144, seed 1:       [108, 104]
p001_over_144, seed 2:       [108, 98]
p001_over_036, seed 0:       [108, 82]
p001_over_036, seed 1:       [108, 79]
p001_over_036, seed 2:       [108, 75]
p001_over_018, seed 0:       [108, 54]
p001_over_018, seed 1:       [108, 53]
p001_over_018, seed 2:       [108, 43]
```

Those sequences are tier state-cell-count sequences. They count quotient state
cells by tier. They do not count raw historical action-cell records, and they
do not list individual cell sizes.

This blueprint designs the next evaluation:

```text
For each selected non-collapsed noisy-rate tower, build the full tower that the
current noisy-rate schema produces, then run a real tower-only training budget
on that tower and report whether the tower trains cleanly.
```

For the current noisy-rate schema, "full available tower" means:

```text
tier 0: base counterpoint graph
tier 1: quotient after the selected noisy-rate contraction block
```

This is a full available tower for the current single-block noisy-rate schema.
It is not a deep binary-coset tower. A deep tower would require a separate
multi-block schema design and is out of scope for this blueprint.

## Evaluation Class

Recommended class:

```text
tower_training_health_diagnostic
```

This is a health and executability evaluation. It asks whether the non-
collapsed noisy-rate towers can be used as actual training surfaces.

This is not a direct-vs-tower comparison.

This is not a learning-advantage benchmark.

This is not an environment redesign.

## Primary Evaluation Question

Primary question:

```text
Can each selected non-collapsed noisy-rate counterpoint tower support a real
tower-only training budget with coherent lift, concrete-step, tier-occupancy,
controller, and learner traces?
```

Secondary questions:

1. Do all candidate towers emit concrete steps throughout training?
2. Does tier 1 remain executable when selected by the active-tier controller?
3. Do lift attempts from tier 1 produce successful realized base actions?
4. Does training avoid zero-step episodes and no-available-action loops?
5. Does tier occupancy show actual use of the quotient tier, rather than
   silently falling back to base-tier behavior?
6. Do learner updates occur with nonempty TD/update evidence?
7. Do the noisier/sparser towers behave differently from the denser `1/18`
   towers in health terms, without making comparison-performance claims?
8. Does the generated readout make the answer legible to a human without
   requiring inspection of raw CSVs?

## Non-Goals

This evaluation must not claim:

- tower advantage over direct training;
- direct-vs-tower comparison;
- schema-to-schema superiority;
- final counterpoint learning quality;
- musical quality;
- deep tower/binary-coset behavior;
- tensor-enabled behavior;
- CUDA/GPU behavior;
- production performance;
- upstream `state_collapser` semantics changes;
- that the prior noisy-rate contraction diagnostic proves training quality.

This evaluation must not change:

- the `counterpoint_symbolic_v001` environment definition;
- state enumeration;
- action enumeration;
- transition legality;
- reward semantics;
- legal-action masks;
- upstream `state_collapser`.

## Recommended Evaluation Identity

Recommended evaluation id:

```text
counterpoint_noisy_rate_full_tower_training_diagnostic_v001
```

Recommended run family id:

```text
counterpoint_symbolic_v001_noisy_rate_full_tower_training_diagnostic_v001
```

Recommended run mode:

```text
diagnostic_noisy_rate_full_tower_training
```

Recommended mode contract:

```text
tower_exploit_explore
```

Recommended CLI group:

```text
counterpoint noisy-rate-full-train
```

Recommended CLI commands:

```text
counterpoint noisy-rate-full-train run
counterpoint noisy-rate-full-train summarize
```

Alternative CLI shape:

```text
counterpoint noisy-rate train-candidates
counterpoint noisy-rate summarize-training
```

Consultant recommendation: use the dedicated `noisy-rate-full-train` group so
this evaluation cannot be confused with the structural noisy-rate contraction
diagnostic.

Recommended repo readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/
```

Recommended artifact root shape:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts/<run-label>/
```

Recommended design source reference:

```text
docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic/01_counterpoint_noisy_rate_full_tower_training_diagnostic_blueprint.md
```

## Parent Diagnostic Dependency

This evaluation depends on a parent noisy-rate contraction diagnostic artifact
surface.

The parent surface supplies:

- candidate noisy-rate arms;
- instance ids;
- schema seeds;
- selected-edge counts;
- selected-source coverage;
- tower state-cell-count sequences;
- active action-cell counts;
- endpoint-coalescence summaries;
- selection consistency checks;
- structural collapse classifications.

The child training diagnostic should accept a parent source binding, not a
hand-copied candidate list:

```text
--candidate-readout-source docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/readout_source.json
```

From that binding, the implementation can resolve the parent evaluation root
and read:

```text
results/tower_shape_summary.csv
results/noisy_rate_selection_summary.csv
results/noisy_rate_source_coverage_summary.csv
results/noisy_rate_selection_consistency_summary.csv
results/endpoint_coalescence_summary.csv
evaluation_aggregate_table.csv
evaluation_budget_lock.json
```

The child evaluation should write its own `candidate_manifest.json` recording
which parent candidates were selected, why they were eligible, and which parent
tables supported that choice.

## Candidate Definition

A candidate is a parent noisy-rate run/schema example that satisfies:

- parent run status is `success`;
- arm is not `no_contraction_control`;
- selection consistency is true;
- the tower has at least one non-base tier;
- the deepest available tier has more than one state cell;
- the deepest available tier has at least one active action cell;
- the parent aggregate row is not classified as full collapse or
  uninterpretable;
- the parent artifact root is repo-resident.

For the current smoke readout, this means the nine non-control examples:

| Arm | Schema Seed | Tier State-Cell-Count Sequence |
| --- | ---: | --- |
| `p001_over_144` | 0 | `[108, 100]` |
| `p001_over_144` | 1 | `[108, 104]` |
| `p001_over_144` | 2 | `[108, 98]` |
| `p001_over_036` | 0 | `[108, 82]` |
| `p001_over_036` | 1 | `[108, 79]` |
| `p001_over_036` | 2 | `[108, 75]` |
| `p001_over_018` | 0 | `[108, 54]` |
| `p001_over_018` | 1 | `[108, 53]` |
| `p001_over_018` | 2 | `[108, 43]` |

The implementation should not hard-code this table. It should regenerate the
candidate manifest from the parent source binding at run time.

## Full Available Tower Definition

For this blueprint, "full available tower" means the full partition tower
constructed by the existing noisy-rate schema for that candidate.

Current expected depth:

```text
2 tiers for non-control noisy-rate arms:
  tier 0 = base state/action graph
  tier 1 = quotient after the single selected noisy-rate contraction block
```

This is not a partial run of the current tower. It uses all tiers that the
current schema produces.

This is also not a deep repeated-contraction tower. If the Project Owner later
wants a tower like:

```text
[108, n1, n2, n3, ...]
```

that should be a separate schema/evaluation blueprint.

## Training Semantics

The phrase "real tower-only training budget" should be implemented more
strongly than "run more one-episode probes."

Important source observation:

The current noisy-rate runner constructs a `CounterpointTierLearner` inside
the episode runner. That means learner state is episode-local unless the code
is changed.

This blueprint recommends:

```text
One learner state per candidate training replicate, preserved across all
episodes in that replicate.
```

Without persistent learner state, a longer run would still be useful as an
executability stress test, but it would not cleanly satisfy the Project
Owner's "full train" framing.

Recommended semantics:

- one tower build per candidate/schema seed/replicate;
- one active-tier runtime reset per episode;
- one learner object per candidate/schema seed/replicate;
- learner state persists across episodes;
- controller/runtime traces are recorded per episode;
- aggregate training curves are computed across episodes;
- no direct baseline learner is created.

## Recommended Training Budget

This is a consultant recommendation, not a Project Owner decision.

Initial full-tower training diagnostic budget:

```text
candidate source: latest approved noisy-rate contraction diagnostic readout
instances: derived from candidate source
arms: all eligible non-control candidates
schema seeds: derived from candidate source
training replicates per candidate: 4
episodes per replicate: 64
horizon: environment default unless explicitly overridden
controller event ceiling: max(64, 8 * horizon)
linearization mode: tensor_available_disabled
mode id: tower_exploit_explore
```

Why this budget:

- it is large enough to expose training traces and zero-step failure modes;
- it remains small enough for the current small-fixture nine-candidate case;
- it keeps the result diagnostic rather than turning it into a leaderboard;
- it does not require direct baseline runs.

Smaller implementation smoke budget:

```text
training replicates per candidate: 1
episodes per replicate: 4 or 8
candidate cap: 1 or 2
```

The smoke budget is only for implementation validation. It should not be
reported as the main training-health result.

## No-Contraction Control Policy

The Project Owner explicitly requested no direct baseline comparison.

Therefore the default should be:

```text
omit no_contraction_control from the training-health candidate set
```

An implementation may include an optional `--include-runtime-anchor` flag that
runs no-contraction as a sanity anchor. If present, the readout must label it
as a runtime anchor, not as a comparator or baseline.

Consultant recommendation:

- default omit;
- add an optional sanity-anchor flag only if implementation cost is low;
- do not place the anchor in comparison tables;
- do not compute advantage, delta, or rank against the anchor.

## Runner Design

The runner should be a sibling to the current noisy-rate diagnostic runner,
not a mutation of the structural diagnostic's meaning.

Recommended package:

```text
src/big_boy_benchmarking/environments/counterpoint/noisy_rate_full_training/
```

Recommended files:

```text
__init__.py
config.py
paths.py
events.py
candidate_selection.py
runner.py
aggregation.py
docs_writer.py
manifests.py
```

Reusable existing pieces:

- noisy-rate arm ids and rate helpers from `noisy_rate_diagnostics.config`;
- schema construction from `build_noisy_rate_contraction_schema`;
- tower construction from `build_counterpoint_noisy_rate_partition_tower`;
- active-tier control adapter from `serious_learning.tower_control`;
- diagnostic active-tier controller pattern from `noisy_rate_diagnostics.runner`;
- timing, artifact, manifest, seed-bundle, and readout-source helpers;
- aggregation table patterns from noisy-rate diagnostics.

New or changed pieces:

- parent candidate-source binding;
- candidate manifest and candidate eligibility checks;
- persistent learner across episodes;
- training-curve rows;
- candidate-level health classification;
- readout writer focused on training health rather than collapse threshold.

## Candidate Selection Algorithm

Recommended selection procedure:

1. Load the parent `readout_source.json`.
2. Resolve the parent `source_evaluation_root`.
3. Read parent result tables and aggregate table.
4. Build one candidate record per `(instance_id, arm_id, schema_seed)`.
5. Join tower shape, selection, coverage, consistency, endpoint coalescence,
   and aggregate classification evidence.
6. Retain only non-control candidates with a live deepest tier.
7. Sort candidates by:

   ```text
   instance_id, requested_rate, schema_seed
   ```

8. Write a locked `candidate_manifest.json`.

Recommended candidate id shape:

```text
<instance_id>-<arm_id>-schema<schema_seed>
```

Example:

```text
counterpoint_symbolic_n3_small_v001-p001_over_018-schema2
```

## Training Run Identity

Recommended run id shape:

```text
<candidate_id>-trainrep<replicate_index>
```

Example:

```text
counterpoint_symbolic_n3_small_v001-p001_over_018-schema2-trainrep3
```

Recommended seed bundle policy:

- preserve parent schema seed;
- allocate training replicate seed from child evaluation base seed;
- keep learner/controller randomness separate from schema selection;
- record seed bundle ids in every event row.

The schema seed should not change during a training replicate. The training
replicate changes only runtime/learner seeds.

## Artifact Contract

The evaluation must produce a repo-resident readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/
```

The durable artifact root must live under that surface:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts/<run-label>/
```

The source evaluation root should be:

```text
<artifact-root>/evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic_v001/
```

Required top-level evaluation files:

```text
evaluation_manifest.json
evaluation_budget_lock.json
candidate_manifest.json
evaluation_run_index.csv
evaluation_aggregate_table.csv
evaluation_aggregate_summary.json
readout_source.json
results/
```

Required per-run files:

```text
run_manifest.json
seed_bundle.json
mode_manifest.json
linearization_manifest.json
schema_manifest.json
schema_construction.json
quotient_summary.json
episodes.csv
step_events.csv
control_events.csv
lift_fiber_events.csv
abc_selection_events.csv
abc_tier_signal_events.csv
learner_update_events.csv
timing_segments.csv
timing_summary.json
warnings.jsonl
```

If learner internals cannot currently expose `learner_update_events.csv`, the
implementation gameplan must either add that evidence or explicitly record why
the training claim is limited.

## Evaluation-Level Result Tables

The summarizer should promote the relevant per-run evidence into
evaluation-level tables. The human-readable protocol must not have to
reverse-engineer tower training from raw per-run files.

Required result tables:

```text
results/candidate_summary.csv
results/tower_shape_summary.csv
results/training_episode_summary.csv
results/training_curve_summary.csv
results/tier_occupancy_summary.csv
results/tier_executability_summary.csv
results/lift_success_by_tier.csv
results/lift_failure_by_tier.csv
results/concrete_step_summary.csv
results/controller_action_summary.csv
results/abc_selection_summary.csv
results/abc_tier_signal_summary.csv
results/learner_update_summary.csv
results/training_health_summary.csv
```

Recommended optional tables:

```text
results/final_state_summary.csv
results/reward_distribution_summary.csv
results/timing_summary.csv
results/warning_summary.csv
```

## Core Row Concepts

Candidate summary row:

```text
evaluation_id
candidate_id
parent_evaluation_id
parent_artifact_run_label
parent_run_id
instance_id
arm_id
numerator
denominator
requested_rate
selector_rule_id
schema_seed
selected_edge_count
selected_edge_share
selected_source_share
zero_selected_source_count
tier_state_cell_count_sequence
tier_active_action_cell_count_sequence
deepest_tier_index
deepest_tier_state_cell_count
deepest_tier_active_action_cell_count
largest_state_cell_share
endpoint_useful_coalescence_count
candidate_eligible
candidate_exclusion_reason
```

Training episode row:

```text
evaluation_id
run_id
candidate_id
instance_id
arm_id
schema_seed
training_replicate_index
episode_index
total_reward
concrete_step_count
controller_event_count
lift_attempt_count
lift_success_count
learner_update_count
terminated
truncated
final_state
```

Training curve summary row:

```text
evaluation_id
run_id
candidate_id
training_replicate_index
episode_window_start
episode_window_end
mean_total_reward
mean_concrete_step_count
mean_lift_success_share
mean_selected_deepest_tier_share
mean_deepest_tier_concrete_step_share
zero_step_episode_count
learner_update_count
```

Training health summary row:

```text
evaluation_id
run_id
candidate_id
status
training_health_class
artifact_complete
tower_noncollapsed
deepest_tier_executable
concrete_steps_positive
lift_successes_positive
learner_updates_positive
zero_step_episode_share
no_available_action_event_count
selected_tier_non_executability_count
claim_if_met
claim_if_not_met
```

## Health Classification

Recommended classifications:

```text
trainable_clean
trainable_with_warnings
runtime_executable_but_training_weak
untrainable_no_concrete_steps
untrainable_lift_failure
untrainable_non_executable_tier
artifact_incomplete
candidate_invalid
```

Recommended classification logic:

- `trainable_clean`: artifacts complete; tower non-collapsed; deepest tier has
  active actions; concrete steps emitted; lift successes emitted; learner
  updates emitted; zero-step episode share below warning threshold.
- `trainable_with_warnings`: training completes and concrete steps/lift
  successes exist, but warnings such as high zero-step share, frequent
  no-available-action events, or sparse deepest-tier use are present.
- `runtime_executable_but_training_weak`: concrete steps exist but learner
  updates or tier use are too sparse to call the run a clean training health
  pass.
- `untrainable_no_concrete_steps`: no concrete steps were emitted.
- `untrainable_lift_failure`: lift attempts occur but no successful lifts
  occur.
- `untrainable_non_executable_tier`: selected quotient tier repeatedly has no
  executable actions.
- `artifact_incomplete`: required tables or per-run files are missing.
- `candidate_invalid`: the parent candidate no longer satisfies eligibility.

Warning thresholds should be locked in the budget or manifest. Consultant
recommended defaults:

```text
zero_step_episode_share_warning: 0.10
selected_tier_non_executability_warning_count: 1
minimum_concrete_step_count_for_clean: 1
minimum_lift_success_count_for_clean: 1
minimum_learner_update_count_for_clean: 1
```

These thresholds should be interpreted as health checks, not performance
targets.

## Success Criteria

The evaluation succeeds as a construction/run artifact if:

- all selected candidates are recorded in `candidate_manifest.json`;
- every selected candidate has a completed training run for every requested
  training replicate;
- required per-run files exist;
- required evaluation-level result tables exist;
- `readout_source.json` exists in the repo readout surface;
- the human-readable readout protocol can render the result.

The evaluation succeeds as a training-health diagnostic if:

- every selected candidate is classified as `trainable_clean` or
  `trainable_with_warnings`; or
- mixed classifications are clearly reported with candidate-specific reasons.

The evaluation fails or is blocked if:

- no eligible non-collapsed candidates exist;
- the child run cannot reproduce the candidate tower shape;
- the deepest available tier has zero active action cells;
- all episodes emit zero concrete steps;
- lift attempts cannot realize base actions;
- learner-update evidence is missing while the run is described as training;
- source artifacts are outside the repo readout surface;
- the readout has to infer evaluation purpose from code rather than
  `readout_source.json`.

## Claim Boundary

Allowed claims:

- the evaluation trained on the selected non-collapsed noisy-rate towers;
- the evaluation used repo-resident parent candidate evidence;
- the evaluation built the full tower available under the current noisy-rate
  schema;
- the evaluation recorded tower shape, tier occupancy, lift, concrete-step,
  controller, and learner-update evidence;
- a given candidate did or did not support a clean tower-only training run
  under the locked budget;
- results are health/diagnostic results only.

Blocked claims:

- tower training is better than direct training;
- any noisy-rate arm is better than any other arm;
- quotient training improves sample efficiency;
- learned counterpoint quality is good;
- the result generalizes beyond the locked candidates and budget;
- deep tower behavior has been validated;
- tensor-enabled behavior has been validated;
- `state_collapser` architecture should be changed based only on this run.

## Readout Requirements

The generated human-readable README should start with badges:

```text
Artifacts: Complete/Incomplete
Candidates: N Trainable/Mixed/Blocked
Training: Clean/Warnings/Weak/Failed
Runtime: Concrete Steps/No Concrete Steps
Lift: Successes/Failures
Scope: Diagnostic Only
Provenance: Repo Artifacts
```

The README should contain:

- one-screen verdict;
- source parent diagnostic root;
- child artifact root;
- candidate list;
- tier state-cell-count sequence table;
- training-health table by candidate;
- training-curve overview;
- tier occupancy summary;
- lift success/failure summary;
- concrete-step and zero-step episode summary;
- methodology section;
- claim boundary;
- command to regenerate:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
```

The readout must explicitly say:

```text
This is not a direct-vs-tower comparison.
```

It must also explicitly say:

```text
For the current noisy-rate schema, the full available tower is the base tier
plus one noisy-rate quotient tier.
```

## Source Binding Requirements

The child readout surface must include:

```text
readout_source.json
```

Required fields:

```json
{
  "repo_readout_surface": "<absolute repo path>",
  "source_artifact_root": "<child artifact root>",
  "source_evaluation_root": "<child evaluation root>",
  "parent_readout_source": "<parent noisy-rate readout_source.json>",
  "parent_source_evaluation_root": "<parent evaluation root>",
  "evaluation_id": "counterpoint_noisy_rate_full_tower_training_diagnostic_v001",
  "artifact_run_label": "<run label>",
  "run_mode": "diagnostic_noisy_rate_full_tower_training",
  "source_files": {
    "aggregate_table": "<child aggregate table>",
    "run_index": "<child run index>",
    "candidate_manifest": "<candidate manifest>",
    "candidate_summary": "<candidate summary>",
    "training_health_summary": "<training health summary>"
  },
  "expected_files": {
    "required": ["<required child files>"],
    "expected_absent_is_gap": [],
    "conditional": {},
    "not_applicable": ["direct baseline artifacts"]
  },
  "goal_criteria": [],
  "badge_policy": {
    "dimensions": [
      "artifact_status",
      "candidate_status",
      "training_health_status",
      "runtime_executability_status",
      "lift_status",
      "claim_scope",
      "provenance_status"
    ]
  },
  "goal_summary_sources": [
    "docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic/01_counterpoint_noisy_rate_full_tower_training_diagnostic_blueprint.md"
  ],
  "methodology_summary_sources": [
    "docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_full_tower_training_diagnostic/01_counterpoint_noisy_rate_full_tower_training_diagnostic_blueprint.md",
    "docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md"
  ],
  "claim_boundary": []
}
```

The exact JSON can differ, but it must provide all information needed by the
readout protocol without requiring reverse engineering.

## Implementation Implications

This blueprint probably does not require a new environment.

It probably requires:

- a new evaluation package;
- new candidate-selection helper;
- small CLI additions;
- persistent-learner training runner;
- aggregation/readout support;
- focused tests;
- one implementation smoke run;
- one human-readable generated readout.

It should not require:

- changes to environment dynamics;
- changes to legal action masks;
- changes to state_collapser;
- new tensorization machinery;
- direct baseline runner work.

## Test Strategy

Recommended tests:

1. Candidate selection accepts the current non-collapsed noisy-rate examples.
2. Candidate selection rejects no-contraction control by default.
3. Candidate selection rejects full-collapse or zero-active-action tiers.
4. Candidate manifest is deterministic under a fixed parent source.
5. Runner preserves learner state across episodes.
6. Runner writes all required per-run files.
7. Aggregator writes all required evaluation-level result tables.
8. Health classification distinguishes clean, warning, weak, and failed runs.
9. CLI run/summarize smoke works with a tiny candidate cap.
10. Readout source points at the repo readout surface, not raw tmp folders.
11. Human-readable protocol target command names the repo
    `readout_source.json`.

## Stop Conditions

Stop and ask the Project Owner if:

- implementation pressure turns this into a direct-vs-tower comparison;
- the candidate source is missing, stale, or outside the repo;
- no eligible non-collapsed candidates exist;
- "full available tower" is interpreted as a deep multi-tier tower rather than
  the current noisy-rate schema's full tower;
- persistent learner state cannot be implemented without changing upstream
  semantics;
- required learner-update evidence cannot be exposed;
- the no-contraction control starts being treated as a baseline comparator;
- artifact roots would need to live outside the repo readout surface;
- any edit to `/Users/foster/state_collapser` appears necessary;
- any edit to `counterpoint_symbolic_v001` environment semantics appears
  necessary.

## Decision Locks For Project Owner

These are consultant-authored open questions, not Project Owner statements.

1. Should the initial real budget be `4` training replicates and `64` episodes
   per candidate, or should it be smaller/larger?
2. Should no-contraction be omitted entirely, or included only as a clearly
   labeled runtime sanity anchor?
3. Should this evaluation train exactly the current smoke candidates first, or
   should it require a full parent noisy-rate diagnostic run before training?
4. Should "clean training" require learner-update evidence, or is coherent
   runtime/lift/concrete-step evidence enough for the first pass?
5. Should candidates with near-collapse but non-singleton tiers be included if
   they remain executable?

## Consultant Recommendations

1. Use a sibling evaluation package and readout surface.
2. Select candidates from the parent readout source dynamically.
3. Omit no-contraction by default.
4. Preserve learner state across episodes.
5. Treat reward movement as descriptive evidence, not a success gate.
6. Make pass/warn/fail about executability, lift success, concrete steps,
   learner updates, and non-degenerate tier occupancy.
7. Keep the readout language blunt about scope:

   ```text
   This run shows whether these towers train cleanly under the locked budget.
   It does not show whether they outperform direct training.
   ```

## Blueprint Completion Condition

This blueprint is complete enough to generate a Phase.Stage.Action
implementation gameplan after Project Owner approval.

The gameplan should begin by re-reading the Prime Directive, this blueprint,
the parent noisy-rate diagnostic blueprint/log/readout, and the current noisy-
rate runner source.

