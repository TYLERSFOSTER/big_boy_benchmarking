# Counterpoint Degenerate-Tier Handoff Integration Blueprint

Date: 2026-05-30

Status: corrective rewrite, draft blueprint

Repository:

```text
/Users/foster/big_boy_benchmarking
```

Design folder:

```text
docs/design/degenerate_tier_control/
```

## Status And Authority

This is a design blueprint.

This is not an implementation gameplan.

This is not approval to edit source code.

This document replaces the drifted prior blueprint about concrete
lift-candidate executability. That broader design was not the intended next
work. The intended work is narrower:

```text
make the completed upstream state_collapser degenerate-tier fix work inside
BBB's existing counterpoint serious evaluation path, then resume that original
evaluation.
```

The corrective source chain is:

```text
docs/design/degenerate_tier_control/error_diagnosis_conversation.md
    -> identified the degenerate active-tier failure
    -> concluded the durable control invariant belongs in state_collapser

docs/design/degenerate_tier_control/01_003_big_boy_benchmarking_handoff_note.md
    -> records the completed upstream fix and the exact downstream BBB wiring
```

This blueprint exists only to translate that handoff into BBB design intent.

## Source Authority

This blueprint follows:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/git_practices.md`
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`
- `docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md`
- `docs/design/degenerate_tier_control/error_diagnosis_conversation.md`
- `docs/design/degenerate_tier_control/01_003_big_boy_benchmarking_handoff_note.md`
- `docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_001_counterpoint_first_serious_learning_evaluation_blueprint.md`
- `docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_002_counterpoint_first_serious_learning_evaluation_implementation_gameplan.md`
- `docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/README.md`

## Corrected Understanding

The original counterpoint serious evaluation was not paused because BBB needed a
new broad action-realization design block.

It was paused because the first serious run found a degenerate active-tier
control failure:

```text
non-empty contraction schema
    -> controller descends to a coarsened active tier
    -> current tier-state has zero outgoing action cells
    -> BBB learner receives an empty action vocabulary
    -> BBB learner emits sentinel action -1
    -> BBB executor records invalid_action_index
    -> no concrete environment step occurs
```

The Project Owner identified the operational rule:

```text
if the active tier is degenerate for action selection, lift to a finer tier
until an executable tier is found.
```

The design conversation settled ownership:

```text
state_collapser:
  owns the generic active-tier runtime invariant.

big_boy_benchmarking:
  owns downstream wiring and counterpoint evaluation evidence.

the evaluation:
  records whether the fixed runtime path works.
```

Upstream `state_collapser` work is now complete and released as `v0.7.1`.
BBB should not redesign the control law. BBB should consume it.

## Non-Goals

This blueprint does not design a new counterpoint lift-candidate system.

This blueprint does not add candidate-selection policy.

This blueprint does not change the learner action-space contract beyond what is
required to use the upstream runtime predicate.

This blueprint does not redesign the structured-motion schema.

This blueprint does not change reward design.

This blueprint does not add a new learner family.

This blueprint does not edit `/Users/foster/state_collapser`.

This blueprint does not claim tower advantage.

This blueprint does not decide what to do with any later
`no_lift_candidate_from_current_state` evidence. If such evidence remains after
the degenerate-tier handoff is integrated, it should be recorded as follow-up
evidence for a separate design block, not folded into this blueprint.

## Handoff Contract

The upstream handoff says BBB should supply:

```python
def tier_is_executable(tier: int) -> bool:
    positions = latest_runtime_snapshot.current_position_at_every_tier
    tower = latest_runtime_snapshot.partition_tower_view
    if tower is None:
        return True
    if tier < 0 or tier >= len(positions):
        return False
    state_cell = positions[tier]
    if state_cell is None:
        return False
    return bool(tower.outgoing_action_cells(tier, state_cell))
```

BBB's counterpoint tower-control adapter does not hold a
`LiveRuntimeView`-style snapshot in the same form. It does hold equivalent
episode-local state:

- the current counterpoint state;
- the current core `state_collapser` state;
- the partition tower build result;
- the ability to project the current core state into any tier state cell.

Therefore BBB's local predicate should be equivalent to:

```text
tier is executable if:
  tier is within the current tower depth
  and the current core state projects to a tier state-cell
  and that tier state-cell has at least one outgoing action cell
```

This predicate should be passed into:

```python
ExploitExploreTowerRuntime(..., tier_is_executable=adapter.tier_is_executable)
```

The expected behavior is:

```text
active tier has zero outgoing action cells
    -> state_collapser runtime lifts to a finer executable tier
    -> learner is asked to choose only after a nonempty action surface exists
```

Only if no executable tier exists should the runtime produce a clean no-action
control result.

## Intended BBB Work

The BBB implementation work corresponding to this blueprint is limited to these
items:

1. Pin and install upstream `state_collapser v0.7.1`.
2. Verify the installed runtime exposes `tier_is_executable`.
3. Add or update BBB dependency tests so the pin and runtime surface are
   explicit.
4. Add `CounterpointTowerControlAdapter.tier_is_executable(...)` using the
   handoff's outgoing-action-cell predicate.
5. Pass that predicate into `ExploitExploreTowerRuntime`.
6. Update the timing controller wrapper only as needed to accept the upstream
   `tier_is_executable` callback.
7. Add focused tests proving the counterpoint adapter identifies executable and
   non-executable tiers.
8. Run targeted and full validation.
9. Run a smallest-valid serious-learning smoke and verify the old
   `invalid_action_index` failure path is gone.
10. Return to the first serious counterpoint evaluation readout and regenerate
    human-readable evidence from the new artifacts when directed.

That is the complete scope.

## Expected Evidence

The handoff integration is successful if BBB can show:

- installed `state_collapser` is `0.7.1`;
- `ExploitExploreTowerRuntime` accepts `tier_is_executable`;
- BBB passes the predicate into the runtime;
- action-empty tiers are reported as non-executable by the adapter;
- focused tests pass;
- full tests pass;
- a serious-learning smoke no longer produces the old
  `invalid_action_index` or `action_index_out_of_range` symptom from empty
  action vocabularies.

The handoff integration does not require all non-empty tower arms to become
scientifically successful.

If a later run produces a new failure reason, that result should be interpreted
carefully:

```text
old degenerate-tier bug fixed;
new downstream evidence may require a later, separately authorized design
block.
```

## Relationship To Original Counterpoint Evaluation

This blueprint is not a replacement for the first serious counterpoint
evaluation.

It is a bridge back to it.

The intended sequence is:

```text
original serious counterpoint evaluation
    -> failure readout identified degenerate active-tier control bug
    -> upstream state_collapser fix completed
    -> BBB wires the upstream fix
    -> BBB reruns or smoke-validates the evaluation path
    -> BBB regenerates the human-readable evaluation readout
    -> design conversation resumes from the corrected evidence
```

The evaluation remains scoped to:

```text
counterpoint_symbolic_n3_small_v001
tensor_available_disabled
direct masked-random
direct tabular-Q
empty-schema tower
non-empty tower schema arms
artifact-backed human-readable readout
```

## Required Gameplan Shape

A corresponding implementation gameplan should be Phase.Stage.Action and should
stay narrow.

It should not introduce new PO questions about:

- concrete candidate selection;
- one action-cell versus multiple candidate options;
- structured-motion schema redesign;
- new failure taxonomy beyond recording observed results;
- new learners;
- new reward shaping;
- tensor-enabled execution.

If implementation discovers a new failure after the upstream handoff is wired,
the correct action is:

```text
record it as evidence, stop if it changes implementation scope, and ask the
Project Owner whether to open a separate design block.
```

## Blueprint Readiness

This blueprint is ready to become a narrow Phase.Stage.Action implementation
gameplan.

There are no new PO questions in this blueprint.

The design decision has already been made by the handoff:

```text
BBB should wire state_collapser v0.7.1's tier_is_executable predicate into the
counterpoint tower-control runtime and verify that the original degenerate-tier
failure no longer controls the evaluation.
```

