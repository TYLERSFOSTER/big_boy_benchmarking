# PlateSupport Direct-Star Cul-de-sac Control Blueprint

## Status

This is a blueprint, not an implementation workplan.

It defines the BBB-side evaluation repair needed after Abdul Malik's
PlateSupport gauntlet observation. It should be reviewed before being converted
into a Phase.Stage.Action implementation workplan.

This blueprint covers Part 1 only: a `big_boy_benchmarking` guarded-direct
follow-up evaluation. It does not redesign `state_collapser`.

## Source Documents

- `docs/design/first_plate_support_environment/standard_gauntlet_suite/09_direct_star_culdesac_control/design_discussion.md`
- `state_collapser_invalid_action_self_loop_filtering_issue.md`
- `docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json`
- `docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/README.md`
- `docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/paired_replicate_comparison/readout_source.json`

## Attribution

Abdul Malik, project PM, raised the key concern about the last PlateSupport
gauntlet: the direct controller appeared to hit cul-de-sacs/self-loops while
the tower controller did not. Abdul's specific interpretation, as relayed by
the Project Owner, was that "avoiding self-loops here is the reason why."

The Project Owner accepted Abdul's concern as important and framed the work as
a causal-diagnostic repair, not as a rejection of the prior run. The Project
Owner also clarified the larger mathematical picture: loops downstairs can be
local warning signs for bad lifts upstairs, and the issue is really about
whether tower liftability/action-cell filtering is providing a one-hop
lookahead-like guard that raw direct did not receive.

Codex diagnosed the BBB-side comparison surface and recommended adding explicit
guarded direct arms instead of silently changing the existing direct baseline.
That recommendation is incorporated here.

## Problem Statement

The PlateSupport standard gauntlet produced the strongest current BBB smoke
signal. In the correction run, the selected iterated tower candidate beat the
raw direct baseline on the calibrated binary-success target and also showed a
large counter-signal:

- tower had better mean total reward;
- tower had zero invalid concrete moves;
- tower had zero self-transitions;
- raw direct had many invalid concrete moves and many self-transitions.

This is promising, but it creates a comparison ambiguity.

Raw direct currently acts over the full ambient primitive action alphabet. It
can choose primitive actions that are invalid at the current state. It can also
choose primitive actions that are technically valid but clip to the same state.

The tower controller acts over executable quotient action cells. Under the
current tower/action-layer semantics, internal or self-loop action cells are
not exposed as live outgoing tower actions. That means tower may be getting an
action-surface guard before learning, while raw direct is not.

The next evaluation must isolate this confound.

## Core Claim Boundary

This evaluation must not claim final robotics benchmark superiority.

The correct claim boundary is:

```text
This is a guarded-direct diagnostic that tests whether the previous
PlateSupport tower signal survives when the direct baseline receives local
one-step invalid/self-loop action guards comparable to the tower's executable
action-cell surface.
```

The evaluation is still smoke/calibration evidence.

## Evaluation Goal

Create a PlateSupport guarded-direct follow-up comparison that reuses the
current iterated tower candidate and calibrated Stage 5 binary target, then
compares four explicit arms:

1. `direct_raw`
2. `direct_invalid_guard`
3. `direct_nonself_guard`
4. `tower_selected_candidate`

The evaluation should answer:

- Does tower still beat the original raw direct baseline?
- Does direct invalid-action masking explain the previous signal?
- Does direct non-self masking explain the previous signal?
- Does tower retain an advantage after direct receives the same local
  non-self-action guard?
- Does guarded direct outperform tower, suggesting tower overhead rather than
  tower advantage?

## Recommended Evaluation Identity

Recommended evaluation id:

```text
plate_support_direct_star_culdesac_control_v001
```

Recommended CLI family:

```text
plate-support direct-star-culdesac-control
```

Recommended repo readout surface:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/
```

Reason: this evaluation is a follow-up diagnostic caused by the standard
gauntlet, but it should not silently replace the existing gauntlet Stage 6
readout. It should be a sibling evaluation whose provenance points back to the
standard gauntlet correction run.

Alternate acceptable placement, if the Project Owner wants it grouped inside
the gauntlet:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/direct_star_culdesac_control/
```

Codex recommendation is the sibling placement, because the work is a diagnostic
control rather than a required gauntlet stage.

## Parent Inputs

The evaluation should read from the existing PlateSupport standard gauntlet
correction readout instead of requiring the entire gauntlet to rerun.

Required parent source:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```

Required parent facts:

- selected candidate manifest from candidate discovery / tower training health;
- selected iterated tower schema;
- Stage 5 threshold policy;
- Stage 6 seed and budget conventions, unless overridden;
- dependency manifest showing `state_collapser` pointwise liftability semantics
  compatible with v0.7.2 or newer.

Expected selected tower candidate from the correction run:

```text
plate_support_candidate:source_local_ratio_iterated:0:c8b8935b4c
```

Expected selected schema shape:

```text
plate_support_schema_source_local_ratio_iterated_001_over_144_i032_v001
```

The implementation must not hard-code those IDs as the only valid values. It
should read the selected candidate from the parent readout/candidate manifest
and fail clearly if no selected candidate is available.

## Evaluation Arms

### Arm 1: direct_raw

This arm preserves the existing direct baseline behavior.

Action surface:

```text
all primitive actions in range(PlateSupport ACTION_COUNT)
```

Selection:

- same Q-learning structure as current paired replicate comparison;
- same epsilon schedule and tie-breaking unless the implementation workplan
  deliberately changes those as a named decision;
- no pre-mask;
- invalid and self-loop outcomes are allowed and recorded.

Purpose:

```text
Keep the original comparison visible.
```

This arm must not be removed or renamed into the guarded arms.

### Arm 2: direct_invalid_guard

This arm is a direct learner with a one-step invalid-action mask.

Action surface at concrete state `s`:

```text
{a in primitive_actions | primitive_transition(s, a).invalid_move is False}
```

It excludes primitive actions that the environment marks as invalid at `s`.

It does not exclude valid clipped self-transitions unless those transitions are
also invalid.

Selection:

- same Q-learning update structure as `direct_raw`;
- same epsilon/tie-breaking semantics, but applied over the masked action list;
- the bootstrap next-best term must also use the invalid-guarded action list at
  the next state.

Purpose:

```text
Separate ordinary one-step validity filtering from tower-specific advantage.
```

### Arm 3: direct_nonself_guard

This arm is a direct learner with a one-step non-self-action mask.

Action surface at concrete state `s`:

```text
{a in primitive_actions | primitive_transition(s, a).next_state != s}
```

It excludes:

- invalid primitive actions, because PlateSupport invalid moves return `s`;
- valid clipped self-transitions, because they also return `s`.

Selection:

- same Q-learning update structure as `direct_raw`;
- same epsilon/tie-breaking semantics, but applied over the non-self action
  list;
- the bootstrap next-best term must also use the non-self-guarded action list
  at the next state.

Purpose:

```text
Test Abdul's self-loop/internal-edge filtering hypothesis directly.
```

### Arm 4: tower_selected_candidate

This arm reuses the selected iterated tower candidate from the parent
PlateSupport gauntlet correction run.

Action surface:

```text
executable quotient action cells for the selected tower candidate
```

Selection:

- use the same tower training/comparison machinery as the current standard
  gauntlet paired comparison;
- do not add direct-style invalid or non-self guards to tower;
- record tower action-surface size and liftability results in a way that can be
  compared to the direct guard summaries.

Purpose:

```text
Preserve the original tower arm while adding direct controls around it.
```

## Guard Semantics

The guarded direct arms should use pre-masking, not post-selection veto.

That means the controller chooses from the guarded available action list. It
does not first choose from all primitive actions and then resample if the
chosen action is disallowed.

Reason:

```text
The tower controller is offered executable action cells before selection. The
guarded direct controls should therefore be offered their guarded primitive
action lists before selection.
```

## Guard Fallback Semantics

PlateSupport currently appears to have no valid concrete states with zero
valid non-self outgoing primitive transitions. The guard fallback should
therefore be rare or absent.

The evaluation still needs a defined fallback.

Recommended fallback:

```text
If a guarded direct arm has zero available actions at state s, mark the
controller as blocked for that step, record guard_fallback_used=True, record
all_actions_filtered_count += 1, end the episode with a diagnostic blocked
status, and do not silently revert to raw direct.
```

Reason:

```text
Silently falling back to raw direct would mix decision surfaces and make the
guarded arm hard to interpret.
```

The readout should treat any nonzero guarded-blocked count as a yellow warning.
If guarded-blocked events occur frequently, the evaluation should not be used
as positive evidence for or against tower advantage until investigated.

## Required Event Fields

The implementation should add either a dedicated `guard_events.csv` surface or
equivalent controller-event columns. A dedicated `guard_events.csv` is
preferred because it keeps the action-surface diagnostic visible.

Required fields:

```text
run_id
episode_index
step_index
arm_id
guard_type
state_id
available_action_count_before_guard
available_action_count_after_guard
guarded_action_count
invalid_guard_filtered_count
self_loop_guard_filtered_count
all_actions_filtered_count
guard_fallback_used
chosen_action
chosen_action_would_have_been_invalid
chosen_action_would_have_been_self_loop
chosen_action_transition_was_invalid
chosen_action_transition_was_self_loop
chosen_action_transition_was_valid_clipped_self_loop
next_state_id
reward
done
```

Definitions:

- `available_action_count_before_guard`: ambient primitive action count before
  filtering.
- `available_action_count_after_guard`: actions available to the arm after its
  guard.
- `guarded_action_count`: same as `available_action_count_after_guard`, kept as
  a more human-readable alias if existing artifact patterns prefer it.
- `invalid_guard_filtered_count`: number of primitive actions removed because
  `invalid_move=True`.
- `self_loop_guard_filtered_count`: number of primitive actions removed because
  `next_state == state`.
- `all_actions_filtered_count`: `1` when the selected guard removed every
  primitive action at that state, else `0`.
- `guard_fallback_used`: whether the fallback path was triggered.
- `chosen_action_would_have_been_invalid`: for any arm, whether the chosen
  primitive action would be invalid under the environment transition check.
- `chosen_action_would_have_been_self_loop`: for any arm, whether the chosen
  primitive action would return the same state.

For tower, some fields may be populated by the primitive action selected by
the tower lift. The tower arm should still report whether the resulting
primitive action was invalid or self-loop.

## Required Summary Tables

The evaluation should generate at least these summary tables:

```text
results/arm_summary.csv
results/guard_filter_summary.csv
results/self_loop_summary.csv
results/invalid_vs_self_loop_summary.csv
results/paired_guard_comparison.csv
results/action_surface_summary.csv
results/timing_summary.csv
```

### arm_summary.csv

One row per arm, with:

- `arm_id`
- `episode_count`
- `replicate_count`
- `total_concrete_steps`
- `mean_total_reward`
- `mean_goal_success`
- `mean_binary_success`
- `mean_first_hit_step`
- `invalid_move_count`
- `invalid_move_rate`
- `self_transition_count`
- `self_transition_rate`
- `valid_clipped_self_transition_count`
- `nonself_transition_count`
- `blocked_episode_count`
- `guard_fallback_count`

### guard_filter_summary.csv

One row per guarded arm, with:

- `arm_id`
- `guard_type`
- `mean_available_before_guard`
- `mean_available_after_guard`
- `mean_invalid_filtered`
- `mean_self_loop_filtered`
- `min_available_after_guard`
- `max_available_after_guard`
- `all_actions_filtered_count`

### self_loop_summary.csv

One row per arm, with:

- `arm_id`
- `invalid_self_loop_count`
- `valid_clipped_self_loop_count`
- `total_self_loop_count`
- `total_self_loop_rate`
- `states_with_self_loop_events`
- `top_self_loop_states`

### invalid_vs_self_loop_summary.csv

This table should explicitly separate:

- invalid moves that return the same state;
- valid clipped moves that return the same state;
- valid non-self moves.

### paired_guard_comparison.csv

This table should compare:

- tower versus direct_raw;
- tower versus direct_invalid_guard;
- tower versus direct_nonself_guard;
- direct_invalid_guard versus direct_raw;
- direct_nonself_guard versus direct_invalid_guard.

Suggested metrics:

- binary success difference;
- mean total reward difference;
- invalid move rate difference;
- self-transition rate difference;
- first-hit-step difference where applicable.

### action_surface_summary.csv

This table should summarize decision-surface sizes:

- raw direct ambient action count;
- invalid-guard available action count distribution;
- nonself-guard available action count distribution;
- tower executable action-cell count distribution;
- tower executable lift candidate count distribution if available.

## Required Readout Questions

The human-readable README must answer these questions near the top:

1. Did the selected tower still beat raw direct?
2. Did `direct_invalid_guard` erase most of the tower advantage?
3. Did `direct_nonself_guard` erase most of the tower advantage?
4. Did tower still beat `direct_nonself_guard`?
5. Were any guarded direct states blocked because all actions were filtered?
6. How much of the original raw direct failure mode was invalid moves versus
   valid clipped self-transitions?
7. What claim is still allowed after this run?

## Badge Requirements

The generated README should have badges consistent with the existing human
readability protocol style.

Recommended badges:

- `Artifacts: Complete` or `Artifacts: Incomplete`
- `Guarded Direct: Complete` or `Guarded Direct: Failed`
- `Self-loop Confound: Explains`, `Survives`, or `Mixed`
- `Tower vs Nonself: Positive`, `Inconclusive`, or `Negative`
- `Blocked Guard States: 0` or `Blocked Guard States: Warning`
- `Claim Boundary: Diagnostic`

Badge text should be concise and visually similar to the existing evaluation
README badges. It should not be a free-form sentence jammed into an SVG.

## Interpretation Grid

The readout must classify the result using this grid.

### Case 1: Tower Beats Raw Direct But Not direct_invalid_guard

Interpretation:

```text
Ordinary one-step validity filtering explains most of the original tower
signal.
```

Allowed claim:

```text
The previous run showed that the tower action surface avoided invalid moves,
but a direct learner with equivalent invalid-action masking can recover the
signal.
```

Disallowed claim:

```text
Tower hierarchy beat direct learning on an equivalent decision surface.
```

### Case 2: Tower Beats direct_invalid_guard But Not direct_nonself_guard

Interpretation:

```text
Abdul's self-loop/internal-edge filtering explanation explains most of the
remaining signal.
```

Allowed claim:

```text
The tower advantage is mostly explained by suppressing local self-loop action
choices, including valid clipped self-transitions.
```

Disallowed claim:

```text
The tower advantage is independent of local one-hop action filtering.
```

### Case 3: Tower Beats direct_nonself_guard

Interpretation:

```text
Evidence remains for a tower-specific advantage after matching local non-loop
action filtering.
```

Allowed claim:

```text
Under this smoke budget, the selected tower candidate outperformed direct even
after direct received a comparable local non-self-action guard.
```

Disallowed claim:

```text
General tower superiority is proven.
```

### Case 4: direct_nonself_guard Beats Tower

Interpretation:

```text
The tower may be paying abstraction or executable-lift overhead relative to a
direct controller with the same local safety surface.
```

Allowed claim:

```text
Guarded direct is a strong baseline and should be included in later
benchmarking comparisons.
```

Disallowed claim:

```text
The tower signal failed for all meaningful reasons.
```

### Case 5: All Arms Are Noisy Or Inconclusive

Interpretation:

```text
The current smoke budget is too small or the calibrated threshold is too close
to the margin.
```

Allowed claim:

```text
The evaluation identified the correct control surfaces but needs a larger or
better-targeted budget.
```

## CLI Design

Recommended commands:

```bash
uv run python -m big_boy_benchmarking.cli plate-support direct-star-culdesac-control run \
  --repo-root . \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/guarded_001 \
  --parent-gauntlet-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json \
  --run-label guarded_001 \
  --locked-by foster

uv run python -m big_boy_benchmarking.cli plate-support direct-star-culdesac-control summarize \
  --repo-root . \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/guarded_001
```

The command should write a `readout_source.json` at:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json
```

Then the human-readable report can be regenerated with:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json
```

## Artifact Contract

The evaluation should write:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/
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

The raw run tree should remain under the evaluation's repo artifact root unless
later release-hygiene rules externalize it for public release.

## Implementation Shape

The implementation should reuse the existing PlateSupport gauntlet code where
possible:

- reuse environment instance loading and manifests;
- reuse seed-bundle semantics;
- reuse direct Q-learning update code with a guard-aware action list;
- reuse tower selected-candidate execution code;
- reuse summary/readout helper conventions;
- reuse timing helpers and artifact writers.

Expected source package placement:

```text
src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/
```

Expected modules:

```text
__init__.py
config.py
guards.py
runner.py
aggregation.py
docs_writer.py
manifests.py
paths.py
parent_source.py
```

The `guards.py` module should be small and heavily tested. It should expose:

```text
available_direct_actions(surface, state, guard_type)
classify_primitive_transition(surface, state, action)
summarize_guard(surface, state, guard_type)
```

Where `guard_type` is one of:

```text
raw
invalid_guard
nonself_guard
```

## Required Tests

### Guard Unit Tests

Add tests that construct the default PlateSupport surface and verify:

- `raw` returns all primitive actions.
- `invalid_guard` removes actions whose primitive transition is invalid.
- `nonself_guard` removes actions whose primitive transition returns the same
  state.
- `nonself_guard` removes every action removed by `invalid_guard`.
- `nonself_guard` also removes valid clipped self-transitions when present.
- guard summaries report before/after counts correctly.

### Direct Learner Tests

Add tests that verify:

- `direct_raw` keeps the existing all-action behavior.
- `direct_invalid_guard` chooses only invalid-guarded actions during epsilon
  exploration and greedy selection.
- `direct_nonself_guard` chooses only non-self actions during epsilon
  exploration and greedy selection.
- bootstrap next-best values are computed over the same guard surface as the
  current arm.

### Artifact Tests

Add tests that verify:

- run manifest records parent gauntlet source;
- arm manifest lists all four arms;
- guard event rows exist;
- summary tables exist;
- readout source points at the generated tables;
- generated README can be produced by the human-readability protocol.

### Smoke CLI Test

Add a small smoke run with tiny budget:

- one candidate;
- one replicate;
- very small episode count;
- all four arms emitted;
- no silent fallback to raw direct inside guarded arms.

## Stop Conditions

The implementation workplan should stop, not improvise, if any of these occur:

- parent gauntlet readout source is missing;
- selected tower candidate cannot be resolved;
- selected Stage 5 binary target cannot be resolved;
- state_collapser dependency is older than the pointwise liftability semantics
  expected by current BBB PlateSupport runs;
- tower selected candidate has no executable action cells at initial state;
- any guarded direct arm silently falls back to raw direct;
- summaries cannot distinguish invalid self-loops from valid clipped
  self-transitions;
- readout source cannot be consumed by the artifact-table readability protocol.

## Open PO Decisions Before Workplan

These decisions should be resolved before implementation work begins.

### Evaluation Placement

Codex recommends:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/
```

Alternative:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/direct_star_culdesac_control/
```

### Naming

Codex recommends using explicit arm names:

```text
direct_raw
direct_invalid_guard
direct_nonself_guard
tower_selected_candidate
```

The phrase `direct*` may still appear in prose as a shorthand, but artifact
IDs should use the explicit guard names.

### Budget

Codex recommends reusing the relevant Stage 6 comparison budget by default, so
the new diagnostic isolates action-surface changes rather than budget changes.

If the Project Owner wants a faster first smoke, the workplan should define a
separate `smoke_001` and a later `guarded_001` correction run.

### Parent Candidate Selection

Codex recommends using the selected iterated tower candidate from the current
standard gauntlet correction readout.

If the parent readout contains multiple eligible candidates, the implementation
should use the same selected candidate that fed the current Stage 6 comparison,
not pick a new candidate by fresh heuristic.

### Guarded Block Behavior

Codex recommends diagnostic blocked termination for zero-action guarded states,
not raw fallback.

The workplan should preserve this unless the Project Owner explicitly chooses
a different fallback.

## Done Definition

This blueprint is ready to become an implementation workplan when:

- the Project Owner accepts the four-arm comparison;
- the evaluation placement is chosen;
- the artifact/readout surface is chosen;
- the guarded-block fallback is accepted or replaced;
- the planned readout questions and interpretation grid are accepted.

The next artifact should be:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/09_direct_star_culdesac_control/01_002_plate_support_direct_star_culdesac_control_implementation_workplan.md
```

That workplan must follow `prime_directive` and use Phase.Stage.Action
discipline.

#### PO Follow-up
> One important clarification before we proceed. We need to make sure that his fix isn't accidentally giving some advantage to `direct*` that `tower` isn't getting now. Do you see? 

#### Codex Follow-up
Yes. This is exactly the right caution.

The guarded direct arms are not automatically "fairer" just because they
control the cul-de-sac issue. They can accidentally become a new privileged
baseline if they use information that tower does not have.

The dangerous version would be:

```text
direct* gets an oracle one-step model of every primitive action at every
concrete state, while tower only gets whatever executable quotient action cells
exist in its discovered/action-layer surface.
```

That would overcorrect. It might answer a useful diagnostic question, but it
would not be an equivalent decision-surface comparison.

So the workplan needs to preserve two distinctions.

First, the guarded direct arms are diagnostic controls, not silent replacements
for direct. Their readout must say exactly what information they receive:

```text
direct_invalid_guard receives one-step invalid-action masking.
direct_nonself_guard receives one-step self-loop masking.
tower receives executable quotient action cells.
```

Second, the guarded direct arms must be constrained so they do not get more
than the intended local guard. They should not get:

- reward lookahead;
- goal-distance lookahead;
- multi-step reachability;
- knowledge of which action will lead to later tower liftability;
- schema/tier information;
- action ranking from the transition model;
- any future-state value other than the ordinary learned Q bootstrap that raw
  direct already uses.

They should get only a binary local admissibility mask:

```text
invalid_guard: is this primitive action invalid at the current concrete state?
nonself_guard: does this primitive action return the same concrete state?
```

That still may be more model access than tower has, depending on how we
interpret the tower's executable action-cell surface. Therefore the README
must not describe `direct_nonself_guard` as "the fair direct baseline" without
qualification. It should describe it as:

```text
a one-step local safety control that tests whether the previous tower signal is
explained by invalid/self-loop filtering.
```

If `direct_nonself_guard` beats tower, the allowed conclusion is not simply
"direct beats tower." The allowed conclusion is:

```text
a direct learner with explicit one-step non-self-action masking can match or
beat this tower run, so the previous tower signal is not enough by itself to
establish tower-specific advantage.
```

If tower beats `direct_nonself_guard`, then we have a much cleaner positive
signal, because tower survived a strong local-action-surface control.

I think the blueprint should therefore add one more implementation constraint:

```text
Every guarded direct summary must include an "information parity warning" that
states whether the guard was oracle/local-transition based or derived only from
the same discovered surface available to tower.
```

For this first repair, I still recommend oracle one-step guarded direct, because
Abdul's concern is specifically about whether self-loop avoidance explains the
signal. But the readout must label it as an oracle one-step local guard, not as
a perfectly matched tower-equivalent controller.

Later, if this remains important, we can add a stricter fifth arm:

```text
direct_observed_nonself_guard
```

That arm would mask only actions whose non-self status has been discovered or
certified through the same kind of observed graph surface used by the tower.
That would be closer to a parity-controlled direct baseline, but it is more
complex and should not block the first diagnostic repair.
