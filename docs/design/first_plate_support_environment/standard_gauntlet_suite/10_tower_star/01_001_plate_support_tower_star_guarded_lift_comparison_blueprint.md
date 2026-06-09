# PlateSupport Tower-Star Guarded Lift Comparison Blueprint

## Status

This is a blueprint, not an implementation workplan.

It defines the next PlateSupport diagnostic after the direct-star cul-de-sac
control evaluation. It should be reviewed before being converted into a
Phase.Stage.Action implementation workplan.

This blueprint does not modify the PlateSupport environment and does not
change the standard gauntlet result retroactively. It defines a new sibling
diagnostic evaluation that explicitly stars the tower side as well as the
direct side.

## Source Documents

- `docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/README.md`
- `docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json`
- `docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/README.md`
- `docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json`
- `docs/design/first_plate_support_environment/standard_gauntlet_suite/09_direct_star_culdesac_control/01_001_plate_support_direct_star_culdesac_control_blueprint.md`
- `docs/design/first_plate_support_environment/standard_gauntlet_suite/09_direct_star_culdesac_control/01_003_plate_support_direct_star_culdesac_control_implementation_log.md`
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`

## Attribution

Abdul Malik, project PM, raised the original PlateSupport concern: the prior
gauntlet signal could be inflated because raw direct learning hit invalid or
self-loop cul-de-sacs while the tower controller avoided those cul-de-sacs
through liftability and executable-action filtering.

The Project Owner accepted Abdul's concern and asked for the direct-star
diagnostic. After seeing that direct-star controls beat the current tower arm,
the Project Owner clarified the next issue in the direct-star readout
conversation: direct had been starred, but the tower had not been explicitly
starred in the same local one-step sense. The Project Owner then requested a
new `tower_star` design folder and an extremely detailed blueprint.

Codex authored the concrete engineering proposal in this blueprint. Unless
marked as a direct quotation or already recorded decision, the arm matrix,
artifact contract, implementation surface, and stop conditions below are
consultant recommendations.

## Problem Statement

The current PlateSupport evidence chain has three important steps:

1. The standard gauntlet produced a tower-positive smoke signal.
2. Abdul Malik pointed out a possible confound: raw direct repeatedly entered
   local invalid or self-loop cul-de-sacs, while tower did not.
3. The direct-star diagnostic confirmed the confound is serious: guarded direct
   controls beat the current selected tower arm under the checked-in diagnostic
   budget.

That result is useful, but it leaves a second comparison ambiguity.

The direct-star diagnostic explicitly changed the direct action surface:

- `direct_invalid_guard` removed primitive actions whose one-step transition
  was invalid.
- `direct_nonself_guard` removed primitive actions whose one-step transition
  returned to the same concrete state.

The tower arm in that diagnostic remained the current selected tower candidate.
It acted through executable quotient action cells backed by concrete lift
candidates. It produced zero invalid moves and zero self-transitions in the
run, but that does not prove that its action surface was starred in the same
sense as direct-star.

The missing question is:

```text
If direct gets a one-step local star guard, should tower also get a one-step
local star guard on its concrete lift candidates before selecting tower action
cells?
```

The answer for the next diagnostic is yes.

## Central Design Claim

The next diagnostic should compare direct-star and tower-star arms inside the
same evaluation.

The tower-star operation must be applied at the concrete lift-candidate level.
It must not be a post-hoc veto after a tower action has already been selected.

For a tower action cell to be available under a tower-star arm, the action cell
must have at least one executable concrete lift candidate that survives the
same one-step primitive transition classifier used by direct-star.

## Claim Boundary

Allowed claim:

```text
This diagnostic tests whether the PlateSupport tower candidate survives a
stricter control where both direct and tower are normalized against the same
one-step local invalid/self-loop mechanism.
```

Blocked claims:

- Do not claim final robotics benchmark significance.
- Do not claim broad tower superiority.
- Do not claim broad tower failure.
- Do not claim perfect information parity between direct-star and tower-star.
- Do not claim that one-step nonself masking is a natural deployable controller
  unless a later design explicitly defends that use.

The correct interpretation level is calibration / smoke diagnostic evidence.

## Terminology

### Star

In this design, `star` means a one-step local action-surface guard applied
before action selection.

For direct arms, the guard filters primitive actions available at concrete
state `s`.

For tower arms, the guard filters concrete lift candidates backing a quotient
action cell at the current concrete state and tower state.

### Direct-Star

`direct_star` refers to the already implemented direct diagnostic controls:

- `direct_raw`
- `direct_invalid_guard`
- `direct_nonself_guard`

Direct-star evaluates primitive actions directly against the PlateSupport
surface.

### Tower-Star

`tower_star` is the new operation defined here.

Tower-star does not merely check whether the chosen concrete lift happened to
be valid after selection. It changes the tower action surface:

```text
tower action cell is available
iff
that cell has at least one executable lift candidate surviving the star guard
```

The selected concrete lift must then be drawn from the guarded lift pool.

### Current Tower Lift Executability

The current tower arm exposes quotient action cells using liftability and
executability. It already avoids some dead action cells, but the direct-star
diagnostic did not prove that this action surface is identical to primitive
nonself filtering.

This blueprint names the current tower arm:

```text
tower_lift_executable_current
```

That name is intentionally descriptive. It should not be shortened to
`tower_raw`, because the current tower is not raw in the same sense as
`direct_raw`.

## Evaluation Identity

Recommended evaluation id:

```text
plate_support_tower_star_guarded_lift_comparison_v001
```

Recommended CLI family:

```text
plate-support tower-star
```

Recommended repo readout surface:

```text
docs/evaluations/plate_support_5x5_default_v001/tower_star/
```

Recommended first run label:

```text
tower_star_001
```

Rationale:

- This is a sibling diagnostic to `direct_star_culdesac_control`, not a
  replacement for it.
- It needs its own readout because the primary human question is different:
  the direct-star run asked whether guarded direct explains the prior signal;
  tower-star asks whether hierarchy survives after both sides receive the same
  one-step local star normalization.
- It should keep provenance links to both the standard gauntlet and the
  direct-star diagnostic.

## Required Inputs

### Parent Gauntlet Source

Required:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```

Required facts:

- selected PlateSupport candidate;
- selected iterated source-local-ratio tower schema;
- calibrated binary target policy;
- parent seed/budget conventions;
- environment instance id;
- dependency state, especially `state_collapser` pointwise liftability
  semantics compatible with v0.7.2 or newer.

### Direct-Star Source

Required:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json
```

Required facts:

- direct-star run label;
- direct-star arm matrix;
- direct-star target-hit rates;
- direct-star interpretation case;
- direct-star guard definitions;
- artifact locations for arm, guard, action-surface, and interpretation tables.

This source is required for continuity and provenance. The new evaluation
should rerun direct-star arms inside the tower-star paired run rather than
importing old direct-star numbers as final comparison values. Imported old
numbers can appear as context, but the primary comparison should come from one
paired evaluation with one seed policy.

## Recommended Arm Matrix

The first tower-star diagnostic should run six required arms.

### Arm 1: `direct_raw`

Purpose:

```text
Keep the original direct baseline visible inside the paired diagnostic.
```

Action surface:

```text
all primitive PlateSupport actions
```

Guard:

```text
none
```

Expected behavior:

- may choose invalid actions;
- may choose valid clipped self-loop actions;
- records all invalid and self-loop transitions.

### Arm 2: `direct_invalid_guard`

Purpose:

```text
Measure how much of direct's weakness comes from invalid primitive moves.
```

Action surface at state `s`:

```text
{a | primitive_transition(s, a).invalid_move is False}
```

Guard:

```text
invalid-action filtering only
```

It may still allow valid self-loop transitions.

### Arm 3: `direct_nonself_guard`

Purpose:

```text
Measure the strict one-step direct-star control.
```

Action surface at state `s`:

```text
{a | primitive_transition(s, a).next_state != s}
```

Guard:

```text
nonself transition filtering
```

This removes invalid actions if they self-loop and removes valid clipped
self-loop actions. It is the strongest direct-star local control in the current
design family.

### Arm 4: `tower_lift_executable_current`

Purpose:

```text
Retain the current selected tower behavior as the bridge to prior runs.
```

Action surface:

```text
current executable quotient action cells backed by concrete lift candidates
```

Guard:

```text
current tower liftability/executability semantics only
```

This arm must not be described as unguarded. It is the existing tower action
surface.

### Arm 5: `tower_invalid_guard`

Purpose:

```text
Test the tower action surface after removing concrete lift candidates whose
primitive one-step transition is invalid.
```

Action surface:

```text
quotient action cells with at least one executable lift candidate whose
primitive transition is not invalid
```

Guard:

```text
invalid-action filtering at the concrete lift-candidate level
```

The selected concrete lift must come from the invalid-guard-compatible lift
pool.

### Arm 6: `tower_nonself_guard`

Purpose:

```text
Test the tower action surface after removing concrete lift candidates whose
primitive one-step transition returns to the same concrete state.
```

Action surface:

```text
quotient action cells with at least one executable lift candidate whose
primitive transition is nonself
```

Guard:

```text
nonself filtering at the concrete lift-candidate level
```

The selected concrete lift must come from the nonself-compatible lift pool.

This is the main fairness-normalized tower arm for comparison to
`direct_nonself_guard`.

## Non-Goals

This blueprint does not ask for:

- a new PlateSupport environment;
- a new `state_collapser` release;
- a change to the standard gauntlet definition;
- removal of the raw direct baseline;
- removal of the current tower arm;
- reward lookahead;
- shortest-path lookahead;
- multi-step reachability checking;
- future liftability checking beyond current executable lift candidates;
- a general theorem about quotient action-cell fairness.

## Tower-Star Semantics

### Required Ordering

For each tower decision point:

1. Identify the current concrete state.
2. Identify the current tower state/tier context used by the selected tower
   candidate.
3. Enumerate current quotient action cells using the same source as the
   current tower arm.
4. For each quotient action cell, enumerate its executable concrete lift
   candidates.
5. Classify each concrete lift candidate with the same one-step primitive
   transition classifier used by direct-star.
6. Filter lift candidates according to the tower-star arm guard.
7. Remove any quotient action cell with zero surviving guarded lift candidates.
8. Run tower action selection over the remaining quotient action cells.
9. Select the concrete lift from the surviving guarded lift pool for the chosen
   action cell.
10. Apply that primitive transition.
11. Record both the pre-star and post-star action/lift surfaces.

### Forbidden Ordering

The implementation must not:

- select a tower action cell first, then reject it if the chosen representative
  lift is bad;
- select a concrete lift first, then silently resample until a good lift
  appears;
- fall back to the current tower action surface when tower-star removes all
  action cells;
- fall back to `direct_raw` behavior when guards remove all direct actions;
- use reward or goal distance to filter lift candidates;
- use later rollout outcomes to filter lift candidates;
- compare imported direct-star numbers against newly generated tower-star
  numbers as the main paired comparison.

### Guard Compatibility Classes

Every concrete lift candidate should receive these booleans:

```text
lift_executable
primitive_invalid_move
primitive_self_loop
primitive_valid_clipped_self_loop
primitive_nonself_transition
invalid_guard_compatible
nonself_guard_compatible
```

Definitions:

```text
invalid_guard_compatible = lift_executable and not primitive_invalid_move
nonself_guard_compatible = lift_executable and primitive_nonself_transition
```

The nonself guard should not need a separate invalid check if invalid moves are
represented as self-loops by the surface, but the implementation must still
record invalid status separately so future readers can see which mechanism was
responsible.

## Key Questions Answered By The Evaluation

### Question 1: Does direct-star still beat tower-star?

Primary comparison:

```text
direct_nonself_guard versus tower_nonself_guard
```

Interpretation:

- if `tower_nonself_guard` wins, the tower signal survives one-step local
  action-surface normalization;
- if `direct_nonself_guard` wins, the prior tower-positive signal remains
  explainable by local one-step action filtering under this budget.

### Question 2: Was the current tower already effectively starred?

Primary comparison:

```text
tower_lift_executable_current versus tower_nonself_guard
```

Interpretation:

- if they are nearly identical in action surface and behavior, the current
  tower arm was already star-clean in practice;
- if they differ materially, the current tower arm had lift pools or action
  cells that were not locally star-clean.

### Question 3: Are tower action cells internally mixed?

Primary table:

```text
lift_pool_mixing_summary.csv
```

Interpretation:

- mixed cells show that a quotient action cell may contain both clean and bad
  concrete lift candidates;
- cells with only bad lifts explain action-cell removal under tower-star;
- all-clean cells show places where tower-star is redundant.

### Question 4: Does invalid filtering or self-loop filtering drive the effect?

Primary comparisons:

```text
direct_invalid_guard versus direct_nonself_guard
tower_invalid_guard versus tower_nonself_guard
```

Interpretation:

- if invalid guard explains most improvement, the issue is mainly environment
  boundary invalidity;
- if nonself guard adds major improvement, valid clipped self-loops are central;
- if tower invalid/nonself guards are identical, current tower lift pools may
  already avoid both mechanisms.

### Question 5: Does tower-star create structural blockage?

Primary table:

```text
tower_action_cell_surface_summary.csv
```

Interpretation:

- if tower-star removes all action cells frequently, the selected candidate may
  not support a fair star-normalized tower comparison;
- if action cells remain plentiful, the diagnostic can proceed as behavioral
  evidence.

## Interpretation Cases

The aggregation should produce a single primary interpretation case and
supporting flags.

### Case: `tower_survives_star_control`

Criteria:

- `tower_nonself_guard` target-hit rate exceeds `direct_nonself_guard`;
- no major tower-star blockage;
- tower reward and invalid/self-loop counters are coherent with target result.

Meaning:

```text
The hierarchy survives the local one-step star normalization in this run.
```

Allowed claim:

```text
This is positive smoke evidence for tower value beyond the local cul-de-sac
filtering confound.
```

### Case: `direct_star_still_explains_signal`

Criteria:

- `direct_nonself_guard` target-hit rate exceeds `tower_nonself_guard`;
- direct guarded arms remain strong;
- tower-star does not uncover a hidden tower improvement.

Meaning:

```text
The direct-star confound remains sufficient to explain the prior PlateSupport
signal under this budget.
```

Allowed claim:

```text
The prior tower-positive signal has not yet been separated from one-step local
action filtering.
```

### Case: `tower_current_was_not_star_clean`

Criteria:

- `tower_lift_executable_current` differs materially from
  `tower_nonself_guard`;
- tower action-cell/lift-pool tables show many cells removed or many selected
  lifts that would fail the star guard.

Meaning:

```text
The current tower action surface had local lift-pool confounds that must be
reported before stronger claims.
```

### Case: `tower_current_already_star_clean`

Criteria:

- `tower_lift_executable_current` and `tower_nonself_guard` have nearly
  identical action surfaces and outcomes;
- selected lifts under current tower were already nonself and valid.

Meaning:

```text
The current tower arm was already effectively star-clean in this run.
```

If direct-star still beats it, this strengthens the negative-control reading.

### Case: `tower_star_surface_blocked`

Criteria:

- tower-star removes all action cells at too many states or at initial states;
- behavioral comparison cannot proceed honestly.

Meaning:

```text
The selected candidate is not suitable for this star-normalized comparison.
```

This should be treated as a diagnostic result, not a software crash.

### Case: `inconclusive_small_margin`

Criteria:

- primary target-hit margins are tiny;
- behavior counters conflict;
- budget too small to support even smoke-level directional interpretation.

Meaning:

```text
The evaluation ran, but the next design should adjust budget or candidate
selection before interpretation.
```

## Artifact Contract

The evaluation must be readable by the artifact-table readout protocol.

Recommended repo surface:

```text
docs/evaluations/plate_support_5x5_default_v001/tower_star/
```

Recommended source artifact root for first run:

```text
docs/evaluations/plate_support_5x5_default_v001/tower_star/artifacts/tower_star_001/
```

Required top-level files after summarization:

```text
README.md
artifact_index.md
glossary.md
method.md
readout_source.json
result_readout.md
runbook.md
badges/
results/
artifacts/
```

Required machine-readable source:

```text
docs/evaluations/plate_support_5x5_default_v001/tower_star/readout_source.json
```

The readout source must point at tables inside the repo. It must not depend on
machine-local temporary paths.

## Required Result Tables

### `arm_summary.csv`

One row per arm.

Required columns:

```text
arm_id
arm_type
guard_type
episode_count
replicate_count
target_hit_count
target_hit_rate
mean_total_reward
mean_episode_steps
invalid_move_count
invalid_move_rate
self_transition_count
self_transition_rate
blocked_episode_count
blocked_episode_rate
mean_available_action_count
mean_available_action_count_before_star
mean_available_action_count_after_star
```

### `paired_star_comparison.csv`

One row per named comparison.

Required comparisons:

```text
direct_raw_vs_tower_current
direct_invalid_vs_tower_invalid
direct_nonself_vs_tower_nonself
tower_current_vs_tower_invalid
tower_current_vs_tower_nonself
direct_invalid_vs_direct_nonself
tower_invalid_vs_tower_nonself
```

Required columns:

```text
comparison_id
left_arm_id
right_arm_id
metric
left_value
right_value
delta_right_minus_left
direction
interpretation_flag
```

### `tower_lift_guard_summary.csv`

One row per sampled or selected tower action cell at a decision point. If the
full surface is tractable, record the full surface. If the full surface is too
large, record selected cells and aggregate counts, then state the sampling rule
in `method.md`.

Required columns:

```text
run_id
episode_index
step_index
arm_id
tier_index
concrete_state_id
tower_state_id
action_cell_id
candidate_lift_count
executable_lift_count
invalid_guard_compatible_lift_count
nonself_guard_compatible_lift_count
selected_by_current_tower
selected_by_tower_star
action_cell_available_before_star
action_cell_available_after_invalid_star
action_cell_available_after_nonself_star
action_cell_removed_by_invalid_star
action_cell_removed_by_nonself_star
selected_lift_invalid_move
selected_lift_self_loop
selected_lift_nonself_transition
```

### `tower_action_cell_surface_summary.csv`

One row per arm/tier or arm/run/tier, depending on table size.

Required columns:

```text
arm_id
tier_index
decision_count
mean_action_cells_before_star
mean_action_cells_after_star
mean_action_cells_removed_by_star
max_action_cells_removed_by_star
states_with_no_cells_before_star
states_with_no_cells_after_star
blocked_decision_count
blocked_decision_rate
```

### `lift_pool_mixing_summary.csv`

One row per arm/tier or aggregate cell class.

Required columns:

```text
arm_id
tier_index
action_cell_count
all_clean_cell_count
mixed_clean_and_bad_cell_count
only_invalid_cell_count
only_self_loop_cell_count
only_bad_cell_count
mean_clean_lift_fraction
mean_nonself_lift_fraction
```

### `direct_guard_filter_summary.csv`

This may reuse the direct-star `guard_filter_summary.csv` schema, but should
be regenerated inside this evaluation.

Required purpose:

```text
Make direct-star filtering visible beside tower-star filtering.
```

### `star_surface_blockage_summary.csv`

Required columns:

```text
arm_id
blocked_episode_count
blocked_decision_count
first_blocked_step_min
first_blocked_step_median
blocked_reason
comparison_usable
```

### `interpretation_summary.csv`

Required columns:

```text
evaluation_id
run_label
primary_interpretation_case
primary_target_comparison
primary_target_delta
tower_star_surface_blocked
tower_current_star_clean_flag
direct_star_still_explains_signal_flag
tower_survives_star_control_flag
allowed_claim
blocked_claim
```

### `badge_summary.csv`

Required badge concepts:

```text
artifacts_complete
claim_boundary
direct_star_complete
tower_star_complete
primary_interpretation
tower_surface_blockage
tower_current_star_clean
direct_vs_tower_star
provenance_repo_artifacts
```

The generated badge strip should match the style used by the other successful
evaluation readouts, not plain Markdown text badges.

## Event Tables

The implementation should preserve enough event-level evidence to audit the
summary tables.

Required event families:

- episode events;
- step events;
- direct guard events;
- tower lift candidate events;
- tower action-cell surface events;
- learner update events;
- tier transition events;
- timing events.

For tower-star, the most important event table is the lift-candidate event
surface. It should record lift candidates before and after star filtering, not
only selected lifts.

## Human-Readable Readout Requirements

The generated README must include:

1. Badge strip at top.
2. Status at a glance.
3. Summary of goals.
4. Summary of methodology.
5. One-screen verdict.
6. Primary arm table.
7. Direct-star versus tower-star comparison table.
8. Tower action-cell/lift-pool findings.
9. Information parity warning.
10. Attribution section naming Abdul Malik's observation and the Project
    Owner's `tower_star` request.
11. Claim boundary.
12. Inspection map.
13. Clarifying questions and turns section, preserving any real PO turns and
    Codex replies without inventing PO content.

The README must explain the core distinction in plain language:

```text
Direct-star filters primitive actions. Tower-star filters concrete lifts inside
quotient action cells before the tower chooses among those cells.
```

## Implementation Surface Recommendation

Recommended new package:

```text
src/big_boy_benchmarking/environments/plate_support/tower_star/
```

Recommended modules:

```text
__init__.py
aggregation.py
config.py
docs_writer.py
events.py
guards.py
manifests.py
parent_source.py
paths.py
runner.py
tower_lifts.py
```

Recommended CLI:

```text
uv run python -m big_boy_benchmarking.cli plate-support tower-star run \
  --repo-root "$BBB_ROOT" \
  --artifact-root "$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/tower_star/artifacts/tower_star_001" \
  --parent-gauntlet-source "$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json" \
  --direct-star-source "$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json" \
  --run-label tower_star_001 \
  --locked-by foster
```

Recommended summarize command:

```text
uv run python -m big_boy_benchmarking.cli plate-support tower-star summarize \
  --repo-root "$BBB_ROOT" \
  --artifact-root "$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/tower_star/artifacts/tower_star_001"
```

The implementation may reuse direct-star helpers where appropriate. In
particular, the primitive one-step classification semantics should match the
existing direct-star classifier so direct and tower are using one local
transition vocabulary.

## Important Engineering Constraint

If the current tower training surface cannot expose candidate lifts before
representative selection, implementation must stop and report the gap.

The evaluation is invalid if tower-star is implemented as:

```text
run current tower, observe selected lift, discard bad selected lift after the
fact
```

The evaluation is valid only if tower-star changes action-cell availability
before tower action selection.

## Budget Recommendation

Initial recommendation:

```text
reuse the direct-star diagnostic budget
```

That means:

- same parent selected candidate;
- same target policy;
- same episodes per replicate;
- same replicate count;
- same paired seed bundle shape.

Rationale:

- The first goal is semantic correction and interpretation, not power.
- The direct-star numbers are already interpretable at this budget.
- Reusing the budget makes the new result easier to compare to the prior
  direct-star diagnostic.

Consultant-authored open question for PO:

```text
Should the first `tower_star` run reuse the direct-star budget exactly, or
should it increase episodes per replicate now that the arm matrix is larger?
```

Codex recommendation:

```text
Reuse the direct-star budget first. Increase only after the semantic tables
confirm the comparison is valid.
```

## Candidate Scope Recommendation

Initial recommendation:

```text
run only the selected PlateSupport iterated tower candidate from the corrected
standard gauntlet
```

Rationale:

- The design question is about the already reported PlateSupport signal.
- Expanding to multiple candidates would mix candidate discovery with fairness
  control.
- A broader candidate sweep can be a later evaluation if tower-star changes
  the story.

Consultant-authored open question for PO:

```text
Should `tower_star` stay on the selected candidate only, or should it include a
small candidate panel?
```

Codex recommendation:

```text
Selected candidate only for v001.
```

## Direct Arms Should Be Rerun

The direct-star source is required for provenance, but the primary direct arms
should be rerun inside `tower_star`.

Reason:

```text
The central comparison should share one paired seed bundle, one artifact root,
one target policy manifest, and one aggregation pass.
```

Imported direct-star results may appear in contextual notes, but they should
not be the primary comparison row.

## Expected Failure Modes

### Failure Mode: Cannot Reconstruct Parent Candidate

Stop condition:

```text
selected candidate cannot be loaded from parent gauntlet source
```

Required output:

- blocked result manifest;
- human-readable failure reason;
- no invented fallback candidate.

### Failure Mode: Cannot Enumerate Tower Lift Candidates

Stop condition:

```text
implementation cannot inspect executable concrete lift candidates before tower
action selection
```

Required output:

- blocked implementation log entry;
- workplan correction note;
- no post-hoc tower-star approximation.

### Failure Mode: Tower-Star Empties The Surface

Stop condition:

```text
tower_invalid_guard or tower_nonself_guard has no available action cells at
required decision points
```

Required output:

- complete diagnostic tables showing blockage;
- interpretation case `tower_star_surface_blocked`;
- no behavioral superiority claim.

### Failure Mode: Guard Classifier Mismatch

Stop condition:

```text
direct and tower use different definitions of invalid/self/nonself
```

Required output:

- test failure or blocked run;
- explicit correction before readout generation.

### Failure Mode: Readout Source Points Outside Repo

Stop condition:

```text
generated readout_source.json references temporary machine-local artifacts
```

Required output:

- fix paths before final readout;
- no human-readable report claiming repo-resident provenance.

## Testing Requirements

### Unit Tests

Required coverage:

- primitive transition classification reused from direct-star or matched
  exactly;
- direct guard action filtering remains unchanged;
- tower lift-candidate filtering removes bad lift candidates before action-cell
  selection;
- action cells with zero surviving guarded lifts are unavailable;
- selected concrete lift always comes from the guarded lift pool;
- blocked tower-star surfaces are represented as diagnostic blockage, not
  fallback behavior.

### Integration Tests

Required coverage:

- CLI `run` creates repo-resident artifacts;
- CLI `summarize` regenerates docs from existing artifacts;
- `readout_source.json` includes all required table roles;
- generated README has badge strip and inspection map;
- artifact-table readout protocol can operate on the produced source.

### Smoke Run

Required smoke:

```text
plate-support tower-star run
plate-support tower-star summarize
uv run pytest tests/environments/plate_support/test_tower_star.py
```

If the real run is too large for the implementation pass, the workplan should
use a tiny/smoke budget and record that the full run remains pending.

## Open Questions For Project Owner

These are Codex-authored questions. They are not Project Owner statements.

### Question 1: Budget

Should the first `tower_star` run reuse the direct-star budget exactly, or
should it increase episodes per replicate immediately?

Codex recommendation:

```text
Reuse direct-star budget first.
```

### Question 2: Candidate Scope

Should the first run use only the selected standard-gauntlet candidate, or a
small candidate panel?

Codex recommendation:

```text
Selected candidate only.
```

### Question 3: Primary Claim Pair

Should the one-screen verdict center on:

```text
direct_nonself_guard versus tower_nonself_guard
```

Codex recommendation:

```text
Yes. This is the cleanest "star both" pair.
```

### Question 4: Guard Variants

Should both invalid-only and nonself tower-star arms be required?

Codex recommendation:

```text
Yes. Keep both so we can separate invalid-boundary effects from valid
self-loop effects.
```

### Question 5: Blockage Interpretation

If `tower_nonself_guard` removes all tower action cells frequently, should the
run be treated as a comparison failure or a diagnostic result?

Codex recommendation:

```text
Both: it blocks behavioral comparison, but it is still a meaningful diagnostic
result about the selected tower candidate.
```

## Blueprint Exit Criteria

This blueprint is ready to become a Phase.Stage.Action implementation workplan
when the Project Owner accepts or edits:

- evaluation identity;
- required arm matrix;
- source inputs;
- tower-star semantics;
- budget scope;
- candidate scope;
- stop conditions;
- readout contract.

No implementation should proceed from this blueprint unless the next artifact
is an implementation workplan or the Project Owner explicitly instructs
otherwise.
