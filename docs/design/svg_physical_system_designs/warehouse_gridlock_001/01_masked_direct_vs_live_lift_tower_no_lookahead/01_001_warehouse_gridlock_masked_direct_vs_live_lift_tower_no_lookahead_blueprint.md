# Warehouse Gridlock Masked Direct vs Live-Lift Tower No-Lookahead Blueprint

## Status

This is a blueprint, not an implementation workplan.

It defines the first Warehouse Gridlock direct-versus-tower diagnostic
evaluation after environment readiness. The comparison is intentionally narrow:

```text
Both arms get immediate inadmissibility masking.
Neither arm gets one-step successor-state cul-de-sac lookahead.
The tower arm keeps state-lift hygiene: do not lift to an upstairs state with
empty Out.
```

The active environment here is Warehouse Gridlock 001.

## Source Documents

This blueprint should be read beside:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_001_warehouse_gridlock_environment_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_002_warehouse_gridlock_environment_implementation_workplan.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_003_warehouse_gridlock_environment_implementation_log.md
docs/evaluations/warehouse_gridlock_001/environment_readiness/README.md
docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

Relevant source code surfaces:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/actions.py
src/big_boy_benchmarking/environments/warehouse_gridlock/transition.py
src/big_boy_benchmarking/environments/warehouse_gridlock/discovery.py
src/big_boy_benchmarking/environments/warehouse_gridlock/runner.py
```

## Attribution

### Project Owner

The Project Owner authored the Warehouse Gridlock physical design drawings and
the core Warehouse mechanics:

- one environment timestep is one second;
- every robot receives one command per timestep;
- every robot may move one graph step or stay;
- robot commands form one synchronous ensemble move;
- invalid ensemble moves do not partially execute;
- invalid ensemble moves do not advance the timer;
- terminal success requires exact robot and box target placement;
- the serious MDP should be treated as hidden or effectively hidden;
- discovery and admissibility fairness are central to evaluation design.

In the current conversation, the Project Owner also clarified the evaluation
contract:

```text
Both arms: inadmissible actions are masked, so neither arm wastes budget on
impossible moves.

Neither arm gets Abdul's stronger direct*/tower* style 1-hop cul-de-sac
lookahead.

"Don't lift to dead" means that once a state is fixed as part of downstairs
path, you never lift to a state upstairs that does not have any valid out
action. This has nothing to do with actions.

Do not give either arm one-hop lookahead in a single tier.
```

Interpretation of the shorthand above:

```text
neither arm gets one-step successor-state cul-de-sac lookahead.
```

### Abdul Malik, Project PM

Abdul Malik's earlier PM observation motivates this fairness boundary: a
tower-positive signal may be confounded if tower machinery avoids dead or
invalid local regions while direct is allowed to waste budget there.

For Warehouse Gridlock, that observation becomes a design constraint:

```text
do not compare tower against a direct arm that is merely wasting budget on
immediately impossible ensemble actions.
```

This Warehouse blueprint does not implement Abdul's stronger one-hop
cul-de-sac control. It explicitly excludes that control for both arms.

### Codex

Codex authored the engineering structure in this blueprint. Unless a statement
is quoted above or recorded in the cited Warehouse source documents, it should
be treated as consultant analysis or recommendation, not as Project Owner or PM
speech.

## Problem Statement

Warehouse Gridlock is a hidden-admissibility, synchronous multi-robot
environment. The full primitive action surface is enormous:

```text
5^32 ensemble commands
```

Flat enumeration is forbidden for the full instance. A naive direct learner
that samples unmasked ensemble actions will mostly sample impossible commands,
which would measure action-space explosion rather than meaningful policy
quality. Conversely, a tower arm may receive liftability or action-surface
information through the abstraction layer. A comparison is not meaningful
unless the admissibility-information boundary is explicit and symmetric.

The desired first diagnostic asks:

```text
Under a fair immediate-admissibility mask for both arms, and without one-step
successor cul-de-sac lookahead for either arm, does a tower representation
produce better early learning/search behavior than direct control?
```

The diagnostic should not try to prove a final benchmark claim. It should test
whether the comparison surface can be made fair enough to study.

## Central Boundary

The central boundary is:

```text
Current inadmissible actions are masked.
Successor-state deadness is not used to choose actions.
Tower state lifts must avoid already-dead upstairs states.
```

Allowed questions:

- Direct may ask: "Is this candidate ensemble action admissible now?"
- Direct may use a mask over a generated candidate set so that selected
  actions are admissible now.
- Tower may ask: "Which upstairs lift states over the fixed downstairs state
  have nonempty outgoing action sets?"
- Tower may ask: "Which current tower actions are admissible from the selected
  live lift state?"

Forbidden questions:

- Direct may not ask: "If I take this admissible ensemble action, will the next
  state have any outgoing action?"
- Direct may not reject an admissible action because its successor is a
  cul-de-sac.
- Tower may not reject an admissible tower action because its successor has
  empty `Out`.
- Tower may not use a one-step nonself or successor viability filter inside a
  tier.

## Terminology

### Warehouse State

A Warehouse Gridlock state consists of:

```text
robot_positions: mapping RobotId -> GridNode
box_positions: mapping BoxId -> GridNode
time_step: integer seconds elapsed
```

The current implementation has 32 robots, 32 boxes, a 16 x 16 visual grid, 251
traversable nodes, and 920 directed traversable edges.

### Ensemble Action

An ensemble action assigns one command to every robot:

```text
RobotId -> {north, south, east, west, stay}
```

The action is valid only if the full synchronous transition is valid. There is
no partial execution.

### Immediate Inadmissibility

An ensemble action is immediately inadmissible at state `s` if applying the
Warehouse transition rule at `s` would produce an invalid ensemble under the
current-state constraints:

- missing or malformed robot command;
- blocked or off-graph robot movement;
- invalid push destination;
- occupied push destination;
- box pushed by multiple robots;
- shared final occupancy;
- head-on edge swap;
- any other current transition invalidity emitted by the environment.

Immediate inadmissibility is about the proposed action at the current state.
It is not about whether the successor is good, bad, dead, terminal, or
promising.

### One-Step Successor Lookahead

One-step successor lookahead is any rule that evaluates an admissible candidate
action by inspecting the successor state it would produce and rejecting it
because that successor is locally bad.

Forbidden examples:

```text
reject action a because Out(next_state(s, a)) = empty
reject action a because next_state(s, a) is a cul-de-sac
reject action a because next_state(s, a) creates a future bottleneck
reject action a because next_state(s, a) is far from target
reject tower action A because every concrete successor below A is dead after
execution
```

The diagnostic may record successor facts after selection for readout and
debugging, but it must not use those facts in action selection.

### Don't Lift To Dead

"Don't lift to dead" is a state-lift rule.

When a downstairs path has fixed a downstairs state `s`, the tower may need to
choose an upstairs representative `s'` such that:

```text
pr(s') = s
```

The allowed lift states are:

```text
LiveFiber(s) = { s' | pr(s') = s and Out(s') != empty }
```

The tower must not choose a lift state:

```text
s' where pr(s') = s and Out(s') = empty
```

This is not action lookahead. It does not inspect the successor of a candidate
action. It prevents the tower from choosing an already-dead upstairs
representative for a downstairs state that has already been fixed.

## Evaluation Identity

Recommended evaluation id:

```text
warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_v001
```

Recommended CLI family:

```text
warehouse-gridlock masked-direct-vs-live-lift-tower
```

Recommended source package:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/
```

Recommended design folder:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_masked_direct_vs_live_lift_tower_no_lookahead/
```

Recommended readout surface:

```text
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/
```

Recommended first run labels:

```text
smoke_001
masked_001
```

## Claim Boundary

Allowed claim:

```text
This diagnostic compares Warehouse Gridlock direct and tower arms under equal
immediate inadmissibility masking, with tower live-state lift hygiene and no
one-step successor-state cul-de-sac lookahead for either arm.
```

Blocked claims:

- Do not claim final Warehouse Gridlock benchmark significance.
- Do not claim broad tower superiority.
- Do not claim broad tower failure.
- Do not claim this implements Abdul's `direct*` or `tower*` one-hop
  cul-de-sac controls.
- Do not claim direct and tower have equal compute unless query counts,
  mask-construction costs, and candidate generation costs are recorded.
- Do not claim direct has access to the full admissible action set if it only
  has access to an admissible candidate generator.
- Do not claim the tower gets action successor lookahead because it avoids dead
  state lifts.

## Required Inputs

### Environment Readiness Source

Required:

```text
docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json
```

Required facts:

- environment family id;
- instance id;
- graph counts;
- action surface contract;
- transition rule contract;
- collision policy;
- reward policy;
- discovery/admissibility policy;
- source drawing attribution;
- readiness status.

### State Collapser / Tower Construction Source

This evaluation requires a Warehouse-compatible tower construction path. That
path may not exist yet.

The implementation workplan must begin by verifying whether `state_collapser`
can construct a tower over the Warehouse Gridlock transition/action surface
without full flat enumeration of `5^32` ensemble actions.

Stop condition:

```text
If tower construction requires flat enumeration of the full ensemble action
space, stop before implementing the evaluation.
```

The correct future implementation likely needs a structured action generator or
sampled/cached admissibility surface rather than a full explicit action list.

### Candidate Generator Source For Both Arms

The direct arm cannot flat-enumerate `5^32` actions.

The evaluation must define how direct proposes candidate ensemble actions
before masking. Candidate generation must be recorded as part of the arm
contract.

The Project Owner additionally clarified that the tower arm also needs bounded
candidate generation, because upper tower tiers may still have very large
outgoing action surfaces. Therefore candidate generation is not a direct-only
issue. It is a fairness surface for both arms.

For v001, both arms should expose:

```text
candidate_generation_policy_id
candidate_generation_scope
candidate_generation_budget
candidate_count_before_mask
candidate_count_after_mask
mask_scope
selection_policy_id
```

Direct candidates are concrete ensemble-action proposals.

Tower candidates are tower-level proposals available at the chosen live lift
state, together with their concrete realization surface. A tower candidate is
not automatically an admissible selected action. It must still pass the
current-action admissibility mask, and the readout must say whether the mask is
exact over the full generated tower candidate set or only over a sampled
candidate subset.

Consultant recommendation:

```text
Use a structured local candidate generator for v001 smoke:
  - all-stay;
  - one active robot command with all other robots stay;
  - optionally sparse k-active robot commands for k <= 2;
  - matched proposal budget across arms.
```

This is now a two-arm recommendation, not a direct-only recommendation. The
Project Owner accepted sparse structured generation in principle and corrected
that tower must receive the same candidate-generation discipline.

## Active Arm Matrix

The active v001 comparison should include exactly two arms:

| Arm id | Arm type | Immediate inadmissibility mask | Live state-lift rule | One-step successor cul-de-sac lookahead | Purpose |
| --- | --- | --- | --- | --- | --- |
| `warehouse_direct_admissible_masked` | direct concrete | yes | not applicable | no | direct baseline that does not waste selected moves on impossible ensembles |
| `warehouse_tower_live_lift_masked` | tower | yes | yes | no | tower candidate with state-lift hygiene only |

Excluded active arms:

| Excluded arm | Reason |
| --- | --- |
| raw direct random over `5^32` | mostly measures impossible-action explosion |
| direct one-hop dead-successor guard | Abdul-style `direct*`, explicitly out of scope |
| tower one-hop dead-successor guard | Abdul-style `tower*`, explicitly out of scope |
| planner / shortest path / global search | not a learning/search diagnostic arm |
| full admissible-action oracle direct | may be useful later, but not this first fair-masking diagnostic unless explicitly approved |

The implementation may record excluded arms in metadata, but must not run them
as active arms without a revised blueprint.

## Direct Arm Contract

The direct arm policy loop should be:

1. Observe current concrete Warehouse state `s`.
2. Generate a bounded candidate set of ensemble actions.
3. Query or compute immediate admissibility for those candidates.
4. Mask inadmissible candidates.
5. Select an admissible candidate using the direct learner/search policy.
6. Execute the selected action.
7. Record successor diagnostics after execution, without using them for
   selection.

Required direct audit facts:

```text
candidate_generation_policy_id
candidate_count_before_mask
candidate_count_after_mask
admissibility_query_count
invalid_candidate_count
selected_action_id
selected_action_valid
selection_used_successor_out=false
successor_out_count_observed_after_selection
```

Open implementation question:

```text
What direct candidate generator is strong enough to be meaningful but small
enough to avoid full enumeration?
```

## Tower Arm Contract

The tower arm policy loop should be:

1. Observe or maintain the current downstairs Warehouse state `s`.
2. Map/fix the relevant downstairs path/state in the tower.
3. Choose an upstairs lift `s'` only from states with `pr(s') = s` and
   `Out(s') != empty`.
4. Generate or expose a bounded current tower action candidate set from `s'`.
5. Mask current inadmissible tower actions.
6. Select a tower action using the tower learner/search policy.
7. Lift/realize the selected tower action into a concrete Warehouse ensemble
   action.
8. Execute the selected concrete action.
9. Record successor diagnostics after execution, without using them for
   selection.

Required tower audit facts:

```text
downstairs_state_id
tier
state_cell_id
fiber_candidate_count
live_lift_candidate_count
dead_lift_candidate_count
selected_lift_state_id
selected_lift_out_count
tower_candidate_action_count_before_mask
tower_candidate_action_count_after_mask
selected_tower_action_id
selected_concrete_action_id
selection_used_successor_out=false
successor_out_count_observed_after_selection
```

Tower candidate semantics:

```text
tower_lift_candidate:
  an upstairs state representative s' in the fiber over fixed downstairs state s

live_tower_lift_candidate:
  a tower_lift_candidate with Out(s') != empty

tower_action_candidate:
  a candidate action, action cell, or generated abstract move considered from
  the selected live lift state s'

tower_concrete_realization_candidate:
  a concrete Warehouse ensemble action that realizes a tower_action_candidate
  under the current lift state
```

The live-lift filter applies only to `tower_lift_candidate` objects. The
current inadmissibility mask applies to tower action/concrete realization
candidates. Neither filter may use successor-state `Out`.

If the upper tier has too many outgoing tower candidates, the tower must use a
bounded tower candidate generator and record that fact. It must not silently
pretend to have an exact full tower action mask.

Open implementation question:

```text
Can the Warehouse tower runtime expose fiber states and Out counts without
materializing the full serious MDP?
```

Stop if the answer is no.

## Admissibility Information Fairness

This evaluation is only meaningful if admissibility information is accounted
for.

Both arms must record:

- number of candidate actions proposed;
- candidate-generation policy;
- candidate-generation budget;
- whether candidates are complete, sampled, sparse, or learned proposals;
- number of admissibility queries;
- number of candidates masked as inadmissible;
- cache policy;
- cache hits;
- whether masks are exact over a candidate set or exact over the full action
  surface;
- whether the arm had access to a larger candidate set than the other arm;
- wall-clock and logical query cost.

Important distinction:

```text
exact over candidate set != exact over full action space
```

For Warehouse Gridlock, v001 will almost certainly use exact masks over
generated candidate sets, not exact full masks over `5^32`.

The README must state this plainly for both arms. If the tower mask is exact
only over a generated or sampled tower candidate set, that must be just as
visible as the direct arm's candidate-set mask.

## Learning / Search Contract

This blueprint does not yet lock the learner.

Consultant recommendation for v001:

```text
Use a small, auditable tabular or bandit-style controller over generated
candidate actions for both arms, with matched seeds and proposal budgets.
```

Rationale:

- The environment is new and enormous.
- The first diagnostic should produce a score, but the score is interpretable
  only if the fairness surfaces and artifact structure are verified.
- A heavyweight learner can be added after the action/candidate surfaces are
  stable.

Open question for Project Owner:

```text
Should v001 be a learning diagnostic, a search/proposal diagnostic, or a
minimal training smoke with learning hooks?
```

Consultant recommendation:

```text
Start with a minimal training smoke that records enough structure for later
learning comparisons.
```

## Budget Recommendation

Because Warehouse Gridlock is new and no tower evaluation has run yet, use a
two-layer budget:

### Smoke

```text
run_label: smoke_001
episodes_per_arm: 2
max_seconds_per_episode: 32
replicates_per_arm: 1
candidate_proposals_per_step: small fixed value
```

Purpose:

- validate CLI;
- validate artifacts;
- validate no-lookahead audit;
- validate live-lift audit;
- validate direct mask audit;
- verify neither arm blocks immediately.

### First Diagnostic

```text
run_label: masked_001
episodes_per_arm: Project Owner decision
max_seconds_per_episode: Project Owner decision
replicates_per_arm: Project Owner decision
candidate_proposals_per_step: Project Owner decision
```

Consultant starting recommendation:

```text
episodes_per_arm: 16
replicates_per_arm: 4
max_seconds_per_episode: 128
candidate_proposals_per_step: 64
```

These are not locked.

## Artifact Contract

Recommended readout surface:

```text
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/
  README.md
  artifact_index.md
  glossary.md
  method.md
  runbook.md
  readout_source.json
  result_readout.md
  badges/
  results/
  artifacts/<run_label>/
```

Recommended raw artifact layout:

```text
artifacts/<run_label>/
  evaluation_manifest.json
  evaluation_budget_lock.json
  evaluation_input_manifest.json
  dependency_manifest.json
  arm_manifest.json
  candidate_generation_manifest.json
  admissibility_policy_manifest.json
  live_lift_policy_manifest.json
  no_lookahead_policy_manifest.json
  run_index.csv
  runs/<run_id>/
    run_manifest.json
    seed_bundle.json
    episode_events.csv
    step_events.csv
    direct_candidate_events.csv
    direct_admissibility_mask_events.csv
    tower_state_lift_events.csv
    tower_action_mask_events.csv
    successor_diagnostic_events.csv
    learner_update_events.csv
    timing_segments.csv
  results/
    arm_summary.csv
    paired_summary.csv
    target_progress_summary.csv
    reward_summary.csv
    admissibility_query_summary.csv
    direct_mask_summary.csv
    tower_live_lift_summary.csv
    no_lookahead_audit_summary.csv
    timing_summary.csv
  readout_source.json
```

Raw artifacts should follow the repository's current policy for
`docs/evaluations/**/artifacts/`. Human-readable readout surfaces should be
generated into the repo.

## Required Audit Tables

### No-Lookahead Audit

Required fields:

```text
arm_id
run_id
episode_index
step_index
selected_action_id
successor_state_id
successor_out_count_observed
successor_out_count_used_for_selection
selection_policy_id
selection_policy_description
```

Requirement:

```text
successor_out_count_used_for_selection = false
```

for both active arms on every selected action.

### Direct Admissibility Mask Audit

Required fields:

```text
arm_id
state_id
candidate_generation_policy_id
candidate_count_before_mask
candidate_count_after_mask
inadmissible_candidate_count
admissibility_query_count
cache_hit_count
selected_action_id
selected_action_admissible
mask_scope
```

Recommended mask policy id:

```text
warehouse_direct_candidate_admissibility_mask_v001
```

### Tower Live-Lift Audit

Required fields:

```text
arm_id
downstairs_state_id
tier
state_cell_id
fiber_candidate_count
live_lift_candidate_count
dead_lift_candidate_count
selected_lift_state_id
selected_lift_out_count
lift_failure
failure_reason
```

Recommended lift policy id:

```text
warehouse_tower_live_state_lift_only_v001
```

### Tower Action Mask Audit

Required fields:

```text
arm_id
tier
state_cell_id
tower_candidate_action_count_before_mask
tower_candidate_action_count_after_mask
inadmissible_tower_action_count
selected_tower_action_id
selected_concrete_action_id
selected_concrete_action_admissible
mask_scope
```

Recommended tower action mask policy id:

```text
warehouse_tower_current_action_admissibility_mask_v001
```

## Human-Readable Readout Requirements

The README must answer these questions near the top:

1. What was the score/result direction under the checked budget?
2. Did both arms use immediate inadmissibility masking?
3. Did either arm use one-step successor-state cul-de-sac lookahead?
4. Did tower use live-state lift hygiene?
5. Was the direct mask exact over the full action space or exact over a
   generated candidate set?
6. Was the tower mask exact over the full tower action surface or exact over a
   generated candidate set?
7. Did either arm show meaningful target progress?
8. Was the result complete, warning, or blocked?

Recommended badges:

```text
environment: warehouse_gridlock_001
admissibility_masking: both_arms
one_step_lookahead: disabled
tower_live_lift: enabled
mask_scope: candidate_set/full_surface/mixed
claim_status: diagnostic_only
score_direction: tower/direct/tie/inconclusive
artifact_status: complete/warning/blocked
```

Required explicit readout sentence:

```text
This evaluation does not implement Abdul-style direct* or tower* one-hop
cul-de-sac guards. Successor-state Out may be recorded for diagnosis, but it is
not used for action selection.
```

Required explicit readout sentence:

```text
Tower live lifting is a state-lift hygiene rule. It prevents selecting an
already-dead upstairs representative for a fixed downstairs state. It is not a
single-tier action-successor lookahead rule.
```

## Implementation Surface Recommendation

Recommended package:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/
```

Recommended files:

```text
__init__.py
config.py
paths.py
readiness_source.py
arms.py
candidate_generation.py
admissibility.py
tower_surface.py
events.py
aggregation.py
manifests.py
docs_writer.py
runner.py
```

Recommended tests:

```text
tests/environments/warehouse_gridlock/test_masked_direct_vs_live_lift_tower.py
```

Recommended CLI:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock masked-direct-vs-live-lift-tower run \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/smoke_001 \
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster \
  --smoke

uv run python -m big_boy_benchmarking.cli warehouse-gridlock masked-direct-vs-live-lift-tower summarize \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/smoke_001
```

Human-readable protocol command:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/readout_source.json
```

## Tests Required

Minimum tests:

1. Direct candidate generator does not flat-enumerate `5^32`.
2. Direct admissibility mask removes currently invalid ensemble candidates.
3. Direct action selection never selects a masked candidate.
4. Direct action selection does not read successor `Out`.
5. Tower lift filter excludes upstairs states with empty `Out`.
6. Tower lift filter can select live upstairs states.
7. Tower action selection does not read successor `Out`.
8. Tower action selection does not apply one-step nonself or dead-successor
   filters.
9. Both arms record admissibility query counts.
10. No-lookahead audit table marks successor `Out` as diagnostic-only.
11. Smoke run writes all required manifests and tables.
12. Summarize writes readout source and human-readable docs.

Focused command:

```text
uv run pytest tests/environments/warehouse_gridlock/test_masked_direct_vs_live_lift_tower.py
```

Broader regression command:

```text
uv run pytest tests/environments/warehouse_gridlock
```

## Stop Conditions

Stop before implementation if:

- Warehouse tower construction is not available without forbidden flat action
  enumeration;
- direct candidate generation cannot be defined without making the direct arm
  meaningless;
- immediate admissibility masking cannot be distinguished from one-step
  successor lookahead in the code;
- the implementation would need to change Warehouse environment mechanics;
- successor `Out` would be used in action selection;
- the readout source would point canonically at a machine-local tmp path;
- the artifact contract cannot prove equal admissibility-mask treatment.

Stop after smoke if:

- direct has no admissible candidates under the chosen candidate generator;
- tower has no live lifts at the start;
- tower construction or action generation silently enumerates the full action
  space;
- any no-lookahead audit row says successor `Out` was used for selection;
- mask/query counts are missing for either arm.

## Open Questions For Project Owner

These are consultant-authored questions, not Project Owner turns.

1. What matched candidate generators should v001 use for direct and tower:
   one-active-robot, sparse k-active robots, learned proposal distribution,
   bounded tower action cells, or another structured generator pair?
2. What should the first target be: exact full terminal success, box progress,
   robot progress, or an intermediate rearrangement target?
3. Should the first diagnostic run be smoke-only until tower construction is
   proven, or should the workplan include a full `masked_001` run?
4. If tower has no live lift at a requested tier, should it fall back to a
   lower tier, fail the episode, or record a blocked run?

## Consultant Recommendations

1. Start with smoke only until Warehouse tower construction is proven. *PO Reply:* Agreed.
2. Use a sparse structured candidate generator for direct; do not pretend it
   is a full action-space mask. *PO Reply:* Agreed, but tower also needs this, as tower all has big out sizes at uppermost tiers.
3. Record mask scope as `candidate_set` unless a full exact action mask is
   truly available. *PO Reply:* Agreed.
4. Treat live-lift failure as an explicit blocked/failed event, not as a silent
   fallback, until the Project Owner approves lower-tier fallback semantics. *PO Reply:* What are the candidate semantics?
5. Make the readout score-first, with fairness and instrumentation immediately
   underneath so the score remains interpretable. *PO Reply:* Nah score.

## Codex Replies To Project Owner Notes

### Reply To Recommendation 1

Agreed. The blueprint should keep smoke as the first gate. That smoke gate is
not a substitute for the scoring diagnostic; it is the first check that the
tower exists, the masks are well-formed, and the no-lookahead audit is not
lying.

### Reply To Recommendation 2

Correct. I originally stated the sparse candidate-generator issue too narrowly
as a direct-arm issue. In Warehouse Gridlock, both arms need explicit candidate
semantics:

```text
direct:
  bounded generated concrete ensemble-action candidates

tower:
  bounded generated tower action candidates from a selected live lift state,
  plus bounded/recorded concrete realization candidates
```

The tower cannot silently treat a huge upper-tier outgoing surface as if it
were free or fully enumerated. If the tower samples or sparsifies outgoing
candidates, the run must record that policy, budget, and mask scope just like
direct.

### Reply To Recommendation 3

Agreed. For Warehouse Gridlock, `candidate_set` should be the default mask
scope unless an implementation truly proves that it has an exact full action
surface. This applies to both direct and tower.

### Reply To Recommendation 4

By "candidate semantics," I mean the identity and lifecycle of each object that
an arm is allowed to propose before masking and selection.

There are four relevant candidate types:

```text
direct_action_candidate:
  a generated concrete synchronous ensemble action

tower_lift_candidate:
  an upstairs state representative s' over fixed downstairs state s

tower_action_candidate:
  a generated tower action/action-cell candidate from the selected live lift

tower_concrete_realization_candidate:
  a concrete synchronous ensemble action realizing a tower action candidate
```

The live-lift rule applies to `tower_lift_candidate` only:

```text
pr(s') = s and Out(s') != empty
```

The admissibility mask applies to action candidates or concrete realization
candidates. The no-lookahead rule says neither arm may reject a selected
candidate because the successor state has empty `Out`.

So if no live lift exists, the event is not "bad action choice." It is a
state-lift candidate failure. The clean v001 behavior should be to record
`no_live_lift_candidate` as a blocked/failed tower event unless the
implementation already has an approved lower-tier fallback. A fallback changes
the tower policy semantics and should not be invented during implementation.

### Reply To Recommendation 5

Accepted correction. The readout should lead with score/result direction. The
fairness and instrumentation sections are still mandatory because the score is
not interpretable without them, but the human-facing report should answer
"who did better under this budget?" first.

## Completion Criteria For Blueprint

This blueprint is complete when:

- it is clearly about Warehouse Gridlock 001;
- it defines the immediate inadmissibility mask for both arms;
- it excludes one-step successor-state cul-de-sac lookahead for both arms;
- it defines tower live-state lift hygiene as a state-lift rule;
- it identifies the action-space explosion and candidate-generation problem;
- it requires audit tables proving the no-lookahead boundary;
- it preserves PO/PM attribution without invented turns.
