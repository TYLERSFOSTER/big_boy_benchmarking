# PlateSupport `direct*` Cul-De-Sac Control Design Discussion

## Purpose

This document starts the design discussion for a follow-up control evaluation
on the PlateSupport standard gauntlet result. The goal is to determine whether
the tower arm's observed advantage over the direct baseline is evidence for a
deeper tower-learning benefit, or whether it is primarily explained by local
feasibility filtering that the direct baseline did not receive.

This is not yet a blueprint, workplan, or implementation authority. It is the
discussion surface for deciding what the control should mean.

## Attribution Ledger

### PM Observation, Relayed By Project Owner

The Project Owner reports that Abdul, project PM, made an important observation
about the last large PlateSupport evaluation:

- The direct PlateSupport arm appeared to hit cul-de-sacs or waste effort in
  locally bad action regions.
- The tower arm did not show the same behavior.
- This should raise eyebrows and deserves investigation before treating the
  tower result as clean evidence for the broader tower-performance claim.
- Abdul's proposed explanation is that the tower's liftability checking may be
  acting like a local lookahead or feasibility filter.
- Abdul's proposed check is to compare against a modified direct baseline,
  tentatively called `direct*`, that receives a one-hop cul-de-sac avoidance
  mechanism.

This section is PM input as relayed by the Project Owner, not a direct quote from Abdul.

#### PO Follow-up 1
Abdullah Malik's specific hypothesis, as he stated it, was:
> "*I think avoiding self-loops here is the reason why.*"

In the present framework, this is equivalent to the above. The present implementation in `state_collapser` throws out loops. The implementation in Abdul's thesis, where the main application was simplex search, does *not* throw out loops. If we imagine the thrown-out loops to be present at downstairs nodes, then loop downstairs becomes a primary indicator, downstairs, for a potential bad-lift / cul-de-sac issue upstairs. They're a kind of "contraction scar."
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../../../../../assets/images/bad_lift_dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../../../../../assets/images/bad_lift_light.svg">
    <img
      alt="Degenerate tier diagram"
      src="../../../../../assets/images/bad_lift_light.svg"
      width="75"
    >
  </picture>
</p>

<table align="center">
  <tr>
    <td width="520" align="center">
      <sub><em>Downstairs loop as a local warning signal for a bad lift, i.e.,
      cul-de-sac upstairs. In simplicial settings, the loop becomes a hint for
      lifting issues for higher-dimensional simplices as well.</em></sub>
    </td>
  </tr>
</table>

Or to say it in more homotopy-theoretic language, Abdul is implicitly noting that loops downstairs are the obstruction to simplicial homotopy lifting.

#### PO Follow-up 2
There is just something here... it keeps slipping way from me, but it's like I keep seeing flashes that the problem is illusory.

Right?... Right. Like the little graph quotienting picture above is *really* an indication that the tower *with* "$\text{Out}(\text{lift of}\;s)\neq\emptyset$" is still at a simimlar disadvantage. Because direct upstairs would hit $\widetilde{s}$ and be done or have to back-track, whereas downstairs would finish trainin, freeze that work, and only then discover liftability issues.

But is this what's even going on? 

Maybe need a bit more diagnostic work first.


### Project Owner Framing

The Project Owner agrees that Abdul's idea should be implemented eventually,
but wants design discussion first.

The Project Owner's current framing is:

- Abdul's concern is legitimate.
- The tower result may still be real and useful, but the mechanism is
  ambiguous.
- A fairer control may require a `direct*` arm with local one-hop cul-de-sac
  avoidance.
- The design should proceed carefully before implementation.

### Codex Interpretation

Codex agrees that Abdul's reasoning makes strong sense.

The current PlateSupport standard gauntlet result showed:

- tower target-hit count better than direct under the locked Stage 5 binary
  target;
- tower mean reward much less negative than direct;
- tower invalid concrete moves equal to zero;
- direct invalid concrete moves very high.

That pattern is encouraging, but it also creates an interpretation confound.
The tower arm may not be winning only because abstraction improves learning in
the deeper sense. It may be winning because tower liftability machinery is
protecting the controller from some locally bad or invalid concrete choices.

That does not make the tower result fake. It means the current result mixes at
least two possible mechanisms:

- tower abstraction / hierarchy / compressed decision structure;
- local feasibility filtering / action safety from liftability checks.

A `direct*` control is the natural way to separate these mechanisms.

## Current Hypothesis Under Investigation

The central hypothesis is:

```text
The tower arm may be benefiting from local liftability filtering that functions
like a one-hop feasibility guard, while the direct baseline is allowed to enter
or waste steps near cul-de-sacs.
```

The follow-up design should test whether the tower still has an advantage when
the direct baseline is granted a comparable local guard.

## Proposed Comparison Shape

The clean comparison should include at least three arms:

- `direct`: the current raw direct baseline.
- `direct*`: a modified direct baseline with local one-hop cul-de-sac
  avoidance.
- `tower`: the current tower controller under corrected pointwise liftability
  semantics.

Expected interpretive cases:

- If `tower > direct` but `tower ~= direct*`, then the old positive signal was
  likely mostly local action filtering.
- If `tower > direct*`, then the tower has evidence of doing something beyond
  one-hop safety.
- If `direct* > tower`, then the tower may be paying abstraction overhead,
  constraining exploration, or using a less effective control surface.
- If `direct*` improves but still differs from `tower` in failure mode, then
  liftability filtering is not equivalent to a simple direct safety mask.

## Design Constraint: What Is Direct-Star Allowed To Know?

The most important design issue is the information boundary for `direct*`.

`direct*` should be strong enough to test Abdul's confound, but not so strong
that it becomes a planner with a different advantage.

Narrow intended meaning:

```text
direct* may use a one-hop local feasibility guard that avoids immediate
non-goal cul-de-sacs.
```

It should not silently receive:

- multi-step reachability to the goal;
- target-distance shaping;
- shortest-path planning;
- global graph analysis as an action oracle;
- privileged knowledge unavailable to a local direct controller unless that is
  explicitly chosen and named as a stronger baseline.

## Candidate Definition Of Cul-De-Sac

The first proposed definition is intentionally narrow:

```text
A candidate action enters a cul-de-sac if its immediate successor state is not
the goal and has no legal outgoing actions.
```

This tests a one-hop dead-end guard.

Open variants to discuss:

- zero-valid-action successor only;
- successor with no path to goal;
- successor with only invalid or self-wasting actions;
- successor that violates some domain-specific plate-support constraint even
  if the graph still has outgoing edges.

Codex recommendation for the first control:

```text
Start with zero-valid-action non-goal successor only.
```

Reason: this is the narrowest guard that directly targets Abdul's cul-de-sac
concern without turning `direct*` into a reachability planner.

## Relationship To Tower Liftability

The design must distinguish two related but different checks:

- Tower liftability asks whether an abstract action has an executable concrete
  lift from an eligible concrete state or fiber.
- Direct-star cul-de-sac avoidance asks whether a concrete direct action's
  immediate successor is locally dead.

These are not automatically equivalent.

Tower liftability may filter actions before concrete execution because no
pointwise executable lift exists. A direct one-hop guard may filter actions
after inspecting the concrete successor. Depending on implementation details,
tower can be weaker, stronger, or simply different from `direct*`.

That difference is not a problem. It is precisely what the control should help
measure.

## Direct-Star Action Selection Semantics

There are two plausible implementations:

### Pre-Mask Semantics

Before selecting an action, remove locally cul-de-sac-entering actions from
the available direct action mask.

Advantages:

- cleanest analogy to tower liftability masks;
- learner sees a reduced action set;
- avoids charging the direct-star arm for actions it was explicitly designed
  not to take.

Risks:

- may make `direct*` stronger than a choose-then-veto controller;
- changes the learner's action distribution and exploration surface.

### Veto-And-Resample Semantics

Let the policy choose an action, then veto and resample if it would enter a
cul-de-sac.

Advantages:

- preserves visibility into how often the policy wanted a bad action;
- easier to log avoided actions as a behavioral diagnostic.

Risks:

- subtle credit-assignment differences;
- can create awkward accounting around attempted but non-executed actions;
- less directly comparable to action masks.

Codex recommendation for first implementation:

```text
Use pre-mask semantics, but log every masked-out candidate action as an
avoided cul-de-sac opportunity.
```

This gives a clean local safety baseline while still quantifying how much help
the direct-star arm received.

## Required Logging

The follow-up should log enough to avoid another ambiguous interpretation.

Suggested direct-star rows or summaries:

- number of direct actions considered;
- number of actions filtered by the one-hop guard;
- number of states where the guard changed the action set;
- number of states where all non-goal actions would have been filtered;
- fallback behavior when the guard removes every candidate action;
- target hits;
- total reward;
- invalid move attempts;
- episode length;
- concrete steps per target hit;
- comparison to raw direct and tower under matched seeds.

Suggested cross-arm summaries:

- `tower_vs_direct`;
- `direct_star_vs_direct`;
- `tower_vs_direct_star`;
- invalid move rates by arm;
- avoided cul-de-sac counts by arm where meaningful;
- target-hit counts and calibrated threshold status by arm.

## Fairness Requirements

To isolate Abdul's concern, the comparison should keep these fixed:

- same PlateSupport environment instance;
- same selected tower candidate or candidate selection rule;
- same training budget;
- same episode count;
- same replicate count;
- same seed bundle policy;
- same Stage 5 binary target unless explicitly redesigned;
- same raw reward function;
- same stopping condition;
- same artifact/readout protocol.

If any of these change, the readout must say so prominently.

## Readout Claims The Follow-Up Should Support

The follow-up should be designed to support bounded claims like:

```text
The original tower-positive smoke signal was or was not robust to a one-hop
direct cul-de-sac control.
```

It should not claim:

```text
The tower is generally superior to direct control.
```

unless later evaluations with larger budgets and broader environments support
that.

## Suggested Design Discussion Questions

These are Codex-authored questions for the Project Owner and PM. They are not
Project Owner statements.

1. Should `direct*` use the narrow one-hop non-goal zero-outdegree definition
   first?
2. Should `direct*` pre-mask bad actions, veto and resample, or run both as
   separate controls?
3. Should the first follow-up reuse the exact `iterated_001` candidate and
   Stage 5 target, or rerun the full gauntlet with a new Stage 6 arm?
4. Should `direct*` be added as a third arm inside the existing PlateSupport
   gauntlet Stage 6, or should it be a separate follow-up evaluation that reads
   the previous gauntlet artifacts?
5. Should the report call this baseline `direct*`, `direct_guarded`,
   `direct_one_hop_safe`, or another name?
6. What is the minimum outcome that would satisfy Abdul's concern enough to
   keep the PlateSupport signal in the beta narrative as a bounded positive
   smoke result?
7. If `direct*` erases the tower advantage, do we treat that as a correction to
   the claim boundary, a successful confound isolation, or a redesign trigger
   for the next environment?

## Current Codex Recommendation

Codex recommends the following first concrete design target:

```text
Create a PlateSupport direct-star follow-up evaluation that reuses the selected
iterated tower candidate and Stage 5 target from the current standard gauntlet,
adds a one-hop non-goal zero-outdegree pre-mask to the direct baseline, logs
all avoided cul-de-sac opportunities, and compares direct, direct*, and tower
under matched seeds.
```

This is the smallest evaluation that directly tests Abdul's concern while
preserving the interpretability of the existing PlateSupport gauntlet result.

## Turn Space

### Project Owner Turn
> I want a massive diagnosis. To start, go over all evaluations, logs etc., and decide if Abdul and I are even interpretting "zero invalid moves" correctly.

### Codex Turn

I did the first diagnostic pass. Short answer: Abdul and the PO are
interpreting the `0` invalid moves correctly in the narrow, table-backed sense,
but we should now be more careful about the broader language.

The narrow statement is true:

```text
In the corrected PlateSupport Stage 6 paired comparison, the selected tower arm
executed zero primitive steps whose upstream PlateSupport runtime labeled
invalid_move=True.
```

The corresponding direct arm did not:

```text
direct concrete baseline:
  concrete steps:      6017
  invalid moves:       2142
  invalid move rate:   0.3559913578195114

selected tower candidate:
  concrete steps:      6008
  invalid moves:       0
  invalid move rate:   0.0
```

Those numbers come from the exact Stage 6 release-bundle tables referenced by
the checked-in readout source:

- `artifacts/iterated_001/stages/paired_replicate_comparison/results/arm_summary.csv`
- `artifacts/iterated_001/stages/paired_replicate_comparison/results/invalid_move_summary.csv`
- `artifacts/iterated_001/stages/paired_replicate_comparison/results/comparison_step_summary.csv`

I also checked the upstream PlateSupport runtime semantics in
`state_collapser v0.7.2`. There, `invalid_move=True` has a precise meaning:

```text
1. propose the primitive action's candidate state;
2. check whether that candidate state satisfies the PlateSupport validity
   predicates;
3. if the candidate is invalid, keep the next state equal to the source state,
   record valid_transition=False, record invalid_move=True.
```

So `invalid_move=True` means a proposed primitive successor violated the
PlateSupport validity predicates. It is not a vague downstream aggregation. It
is emitted by `PlateSupportEnv.step(...)` through `primitive_transition(...)`.

However, the broader phrase "direct hit cul-de-sacs whereas tower did not"
needs refinement. The structural graph does not have literal zero-outdegree
dead ends among valid non-self transitions:

```text
valid states:              89
dead_end_state_count:       0
strong components:          1
shortest start-goal path:   6
```

The real pressure is not literal graph dead ends. It is local loop/self-loop
pressure in the primitive action surface:

```text
primitive state-action rows:       1068
invalid primitive moves:           496
invalid primitive move density:    0.46441947565543074
valid clipped self-transitions:    184
valid non-self edges:              388
```

That distinction matters. Abdul's wording, as relayed by the PO, was:

```text
"I think avoiding self-loops here is the reason why."
```

After checking the code and tables, that looks like the sharper hypothesis.
The issue is not merely "direct enters zero-outdegree cul-de-sacs." The issue
is that raw direct control is allowed to choose primitive actions that collapse
to self-transitions, including invalid self-transitions, while the tower action
surface largely removes those from the live decision surface.

The raw Stage 6 step table confirms this:

```text
direct concrete baseline:
  total self-transitions:        2787
  invalid self-transitions:      2142
  valid clipped self-transitions: 645
  non-self transitions:          3230

selected tower candidate:
  total self-transitions:        0
  invalid self-transitions:      0
  valid clipped self-transitions: 0
  non-self transitions:          6008
```

This is the biggest diagnostic fact in the pass. It says the tower arm did not
merely have fewer invalid moves. It executed no self-transition primitive
steps at all in the Stage 6 run.

Stage 4 tower-only training health points the same way. Its concrete-step
summary has zero invalid moves and zero self-transitions for the two trainable
iterated candidates:

```text
candidate c8b8935b4c:
  concrete steps:         1558
  valid steps:            1558
  invalid_move_count:     0
  self_transition_count:  0

candidate c8462cf197:
  concrete steps:         1444
  valid steps:            1444
  invalid_move_count:     0
  self_transition_count:  0
```

So this is not a one-row Stage 6 summarization accident.

The mechanism also checks out in code.

The direct baseline currently chooses from all primitive action indices:

```text
actions = tuple(range(surface.ACTION_COUNT))
```

That is all 12 primitive actions. The direct Q table also computes
`next_best` over all 12 actions. There is no legality mask, no invalid-action
mask, and no self-loop mask in the current direct baseline.

The tower controller is different. It calls:

```text
choose_executable_tower_action(...)
available_tower_action_choices(...)
partition_tower.executable_action_cells(...)
partition_tower.executable_lift_candidates(...)
```

Those choices are action cells with concrete lift edges sourced at the current
base state. In the partition tower, edges whose source and target lie in the
same current state cell are treated as internal/self-loop edges rather than
ordinary outgoing action cells. The default loop policy is:

```text
LoopPolicy.drop_internal()
```

and the action-layer rebuild skips edges whose projected source cell equals
their projected target cell. In other words, self-loop/internal edges are
recorded diagnostically, but they are not live outgoing decision actions.

One subtlety: the upstream `PlateSupportHiddenGraph` does expose every
primitive action. Invalid primitive actions become deterministic self-loop
edges because `primitive_transition(...)` returns the old state as
`next_state` when the candidate is invalid. So the hidden graph is not hiding
the bad actions at the environment boundary. The filtering happens when
self-loop/internal edges are not surfaced as live tower action cells.

That means Abdul's concern is well-founded:

```text
The tower arm is being compared against a raw direct baseline even though the
tower action surface has a built-in self-loop/internal-edge exclusion effect.
```

This does not make the PlateSupport result worthless. It changes what we are
allowed to say about it.

Safe current interpretation:

```text
The selected tower candidate showed a bounded positive smoke signal under the
current Stage 6 comparison, and the tower action surface produced much cleaner
behavior: higher target-hit rate, better reward, zero invalid primitive moves,
and zero self-transition primitive steps.
```

Unsafe interpretation:

```text
The result proves that tower learning itself beats direct learning, independent
of local feasibility or loop filtering.
```

Abdul's proposed control is therefore not optional if we want the comparison
claim to mature. We need a direct-side control that receives a comparable local
filter. I now think the earlier `direct*` definition should be broadened or
split into separate controls:

```text
direct_raw:
  current direct baseline; all 12 primitive actions exposed.

direct_invalid_guard:
  masks actions whose primitive_transition(...) would emit invalid_move=True.

direct_nonself_guard / direct*:
  masks actions whose primitive_transition(...) would return next_state ==
  source_state, including both invalid self-transitions and valid clipped
  self-transitions.

tower:
  current selected tower candidate with executable lift/action-cell semantics.
```

The `direct_invalid_guard` arm isolates ordinary validity checking. The
`direct_nonself_guard` arm is closer to Abdul's actual self-loop hypothesis.
The tower arm then asks whether hierarchical/tower structure still contributes
anything after direct receives the same local no-self-loop advantage.

My current design correction is:

```text
Do not define direct* as merely "avoid immediate non-goal zero-outdegree
successors." PlateSupport has no literal zero-outdegree dead ends in the valid
non-self graph. Define the first serious direct* control around self-loop
avoidance, with invalid-only masking as a useful ablation.
```

So the answer to the PO question is:

```text
Yes, Abdul and the PO are reading "zero invalid moves" correctly as an executed
primitive-step fact. But the deeper diagnostic is stronger and more specific:
the tower arm executed zero self-transition steps at all, while direct spent a
large part of its budget on invalid and valid self-transitions. That is exactly
the kind of hidden local filtering confound Abdul identified.
```

### Project Owner Turn
> ...

### Codex Turn
> ...

### Project Owner Turn
> ...

### Codex Turn
> ...

### Project Owner Turn
> ...

### Codex Turn
> ...

### Project Owner Turn
> ...

### Codex Turn
> ...

### Project Owner Turn
> ...

### Codex Turn
> ...
