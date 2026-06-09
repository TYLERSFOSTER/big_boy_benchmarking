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
There is just something here... it keeps slippingaway from me, but it's like I keep seeing flashes that the problem is illusory ... Right?... Right. Like the little graph quotienting picture above is *really* an indication that the tower *with* "$\text{Out}(\text{lift of}\;s)\neq\emptyset$" is still at a simimlar disadvantage. Because direct upstairs would hit $\widetilde{s}$ and be done or have to back-track, whereas downstairs would finish trainin, freeze that work, and only then discover liftability issues.

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
> Why? Is this about hidden MDP (hidden phase graph $H$) versus Markov chain (discover graph)? I'm not putting the whole thing together yet.

### Codex Turn

Yes. This is very much about the distinction between the hidden phase graph
`H` and the discovered / quotient control graph, but I would phrase it a little
more carefully:

```text
H is the environment's full primitive transition system.
The discovered graph is the runtime-visible part of H.
The tower control surface is not H itself; it is a quotient/action-cell surface
built from discovered edges, with loop/internal-edge policy applied.
```

So the comparison we accidentally made was not simply:

```text
direct learner on H
vs.
tower learner on H
```

It was closer to:

```text
raw direct learner over all primitive action labels in H
vs.
tower learner over live quotient action cells derived from discovered H,
where self/internal edges are not live outgoing decision actions.
```

That is the missing piece.

In the hidden PlateSupport transition graph `H`, every valid state has all 12
primitive action labels available as proposals. Some proposals move to a
different valid state. Some proposals produce an invalid candidate and are
realized by the environment as a self-loop at the current state. Some proposals
are valid but clip back to the same state, also a self-loop.

So at the level of `H`, raw direct sees something like:

```text
s --action 0--> s'
s --action 1--> s
s --action 2--> s''
s --action 3--> s
...
```

where the arrows back to `s` include the invalid and clipped moves. Direct is
learning over the primitive action proposal alphabet. It is allowed to pick the
self-loop arrows, and the environment then charges it for them.

The tower controller does something different. It does not choose from the
raw 12 action labels. It chooses from action cells in the partition tower:

```text
current base state
-> current state cell at some tier
-> live outgoing action cells from that state cell
-> executable concrete lift of one selected action cell
-> primitive action index
```

The crucial fact is that action cells are built from non-internal outgoing
edges. If an edge has source and target in the same current cell, the partition
tower treats it as an internal/self-loop edge. Under the current default:

```text
LoopPolicy.drop_internal()
```

those internal edges are retained as diagnostic/internal structure but are not
surfaced as live outgoing decision actions. At tier 0, a primitive self-loop is
already internal because source state equals target state. At higher tiers,
additional edges can become internal because contraction identifies their
source and target cells.

That explains why the effect is so strong:

```text
invalid primitive action
-> candidate invalid
-> environment realizes next_state = source_state
-> edge is a self-loop in H
-> tower action-layer rebuild does not expose it as a live outgoing action cell
-> tower controller never selects it
```

And similarly:

```text
valid clipped primitive action
-> candidate valid but next_state = source_state
-> edge is still a self-loop
-> not exposed as live outgoing tower action cell
-> tower controller never selects it
```

So Abdul's "avoiding self-loops" point is not merely an empirical pattern. It
matches the construction. The tower action surface is a quotient/discovered
control surface with self-loop/internal edges suppressed from live action
choice.

The Markov-chain language is useful, but only after choosing a policy. The
hidden phase graph `H` is the transition system / MDP-like object. A direct
policy over primitive actions induces a Markov chain on `H`. A tower policy
induces a different process: it has base state, discovered graph state, tower
state, current tier cells, and executable lift constraints. Once those runtime
rules are fixed, it also induces a stochastic process, but not the same
policy-on-raw-`H` object as direct.

That is why the current result is a confounded comparison:

```text
direct is punished for learning which primitive proposals are loops;
tower is structurally protected from many loop proposals before learning.
```

This also explains why the right control is not just "avoid terminal
cul-de-sacs." There are no literal dead-end states in the valid non-self graph.
The obstruction is more local:

```text
bad proposal / loop in H
-> not live as an outgoing tower action
-> direct baseline needs an analogous local mask if we want to isolate tower
   learning from loop-filtering.
```

So I would now say the conceptual diagnosis is:

```text
The observed zero-invalid-move tower behavior is caused by comparing a raw
primitive-action learner on H against a discovered quotient-action learner
whose live action surface has internal/self-loop edges removed.
```

The future `direct*` arm should therefore answer:

```text
What happens if the direct learner is still direct on H, but its visible action
set is restricted to the same kind of non-loop primitive proposals that the
tower action surface receives for free?
```

That would make the comparison much cleaner.

### Project Owner Turn
> Ah ok... Ok... Ok. Is this what's happening: The Plate Support environament has a little... *ambient* set of possible actions. Constraints maybe, or something, makes it so that lots of the actions get a status `"invalid"` for certain states. The `direct` arm just treats that actions like any other in some4 sense that isn't clear to me yet. Regardless, the very fact that we throw out loops in our tower construction is getting rid of `"invalid"` actions somehow? Am I at all in the vicinity? Please reinvesitgate.

### Codex Turn

Yes, you are absolutely in the vicinity. I rechecked it, and I would now state
the mechanism this way:

```text
PlateSupport has a fixed ambient primitive action alphabet.
Validity is state-action dependent.
Raw direct chooses from the full ambient alphabet.
Invalid proposals are realized by the environment as self-loops with penalty.
The tower action surface does not expose self-loop/internal edges as live
outgoing action cells.
Therefore many invalid proposals disappear from tower choice because, in this
environment, invalid proposals become loops.
```

The main correction is that an action is not globally `"invalid"` in isolation.
It is a state-action proposal that becomes invalid at a particular state.

For example, at the PlateSupport start state:

```text
state = PlateSupportState(x_idx=2, y_idx=2, theta_idx=0, e1=1, e2=1, e3=1)
```

the 12 ambient primitive actions break down like this:

```text
action 0: valid, moves to different state, reward -1
action 1: valid, moves to different state, reward -1
action 2: valid, moves to different state, reward -1
action 3: valid, moves to different state, reward -1
action 4: invalid, stays at same state, reward -3
action 5: invalid, stays at same state, reward -3
action 6: valid, moves to different state, reward -1
action 7: invalid, stays at same state, reward -3
action 8: valid, moves to different state, reward -1
action 9: valid, moves to different state, reward -1
action 10: valid, moves to different state, reward -1
action 11: invalid, stays at same state, reward -3
```

So yes: constraints make many ambient action proposals invalid at specific
states. When that happens, the upstream `primitive_transition(...)` returns:

```text
candidate_valid = False
valid_transition = False
invalid_move = True
next_state = source_state
```

Then `PlateSupportEnv.step(...)` applies that result and charges the local
self-loop penalty:

```text
reward = -3.0
```

Now the direct side:

```text
_choose_direct_action(...)
```

currently does this:

```text
actions = tuple(range(surface.ACTION_COUNT))
```

That means direct chooses among all 12 primitive action labels. It does not
pre-filter invalid proposals. It does not pre-filter self-loops. It does not
ask `primitive_transition(...)` whether the action would be valid before
choosing. If direct chooses an invalid proposal, the environment executes the
penalized self-loop and the Q learner may eventually learn that this was bad.

So the unclear phrase "direct treats invalid actions like any other" should
be made precise:

```text
Direct treats invalid-capable primitive labels as selectable actions. It only
finds out that the chosen state-action proposal was invalid after the
environment executes the step and returns invalid_move=True, next_state=same,
and reward=-3.
```

The tower side is different, but not because it asks for `invalid_move` and
deletes those rows by name. The tower side is different because invalid moves
become loops, and loops are not live outgoing actions in the partition tower's
action surface.

The path is:

```text
invalid state-action proposal
-> primitive_transition returns next_state = source_state
-> hidden graph edge is source -> source
-> partition/action layer sees source cell == target cell
-> edge is treated as internal/self-loop structure
-> action-cell rebuild does not create a live outgoing action cell for it
-> tower controller cannot choose it
```

So your sentence:

```text
the very fact that we throw out loops in our tower construction is getting rid
of "invalid" actions somehow
```

is basically right, with two refinements:

1. It is not removing an `"invalid"` label directly. It is removing self-loop
   edges from the live outgoing tower action surface.
2. In PlateSupport, invalid proposals are one important source of self-loop
   edges, but not the only source. Valid clipped self-transitions also become
   self-loops and are also excluded from the live tower action surface.

That second point is why the Stage 6 row-level numbers were stronger than just
`invalid_move_count`:

```text
direct:
  invalid self-transitions:       2142
  valid clipped self-transitions:  645
  total self-transitions:         2787

tower:
  invalid self-transitions:       0
  valid clipped self-transitions: 0
  total self-transitions:         0
```

So Abdul's hypothesis is not merely "tower avoids invalid actions." The more
accurate statement is:

```text
tower avoids the live selection of self-loop/internal edges, and in
PlateSupport that automatically avoids invalid moves because invalid moves are
implemented as self-loops.
```

This is also why the hidden-graph/discovered-graph distinction matters. The
hidden graph `H` can be seen as having all these primitive proposal edges,
including self-loop edges. The discovered/runtime graph sees local pieces of
that transition structure. Then the tower builds a quotient/action-cell surface
from the discovered edges, with the loop policy deciding what happens to edges
that are internal to a state cell.

In the current construction, the loop policy is effectively giving tower a
local action-surface filter:

```text
do not present internal/self-loop edges as live outgoing actions.
```

Direct does not receive the corresponding filter.

So the conceptual diagnosis is now very concrete:

```text
The PlateSupport comparison is not only direct-vs-tower learning. It is also
unfiltered primitive action proposals versus a quotient action surface that
suppresses self-loop/internal edges. Since PlateSupport invalid moves are
realized as self-loops, this suppresses invalid moves too.
```

That is exactly why a `direct*` control is needed.

I would now design `direct*` as two explicit controls, because they answer
different questions:

```text
direct_invalid_guard:
  Before direct chooses, remove actions whose primitive_transition would set
  invalid_move=True.

direct_nonself_guard:
  Before direct chooses, remove actions whose primitive_transition would return
  next_state == source_state, whether invalid or valid clipped.
```

`direct_invalid_guard` asks:

```text
Was the tower advantage mostly ordinary validity filtering?
```

`direct_nonself_guard` asks Abdul's sharper question:

```text
Was the tower advantage mostly self-loop/internal-edge filtering?
```

If tower still beats `direct_nonself_guard`, then we finally have cleaner
evidence that something tower-specific remains after matching the local
self-loop filter.

### Project Owner Turn
> Then I think we have two tasks in front of us. One is "easy," Namely, redesign the last evaluation so the match is comparison is less noisy. The other is to figure out the laguage/framing for `state_collapser` that would help a future engineer trying to use `state_collapser` from falling into the pitfall that comes from invalid actions and hidden MDP versus dynamically discovered Markov chain. Just let me know if you recognize my reasoning

### Codex Turn

Yes, I recognize the reasoning, and I think this is exactly the right split.

There are two different products of the diagnosis:

```text
Task A, BBB evaluation repair:
  Make the PlateSupport comparison less noisy and more causally interpretable.

Task B, state_collapser framing/language:
  Explain the hidden-MDP / dynamically discovered control-surface pitfall so
  future engineers do not accidentally compare unfiltered primitive control
  against loop-filtered quotient control and overclaim the result.
```

Task A is "easy" only in the relative sense that it is local to this repo and
has a clear experimental shape. We already know the immediate change:

```text
rerun / redesign the PlateSupport paired comparison with direct controls that
receive explicit local filtering:

1. raw direct;
2. direct_invalid_guard;
3. direct_nonself_guard;
4. selected tower candidate.
```

That turns the comparison from:

```text
raw direct vs tower
```

into:

```text
raw direct vs locally guarded direct vs loop-guarded direct vs tower
```

Then the readout can say which part of the tower signal survives each control:

```text
tower > raw direct:
  confirms the original bounded smoke signal.

tower ~= direct_invalid_guard:
  suggests ordinary validity filtering explains most of the signal.

tower ~= direct_nonself_guard:
  suggests Abdul's self-loop/internal-edge filtering concern explains most of
  the signal.

tower > direct_nonself_guard:
  suggests the tower retains an advantage after matching the local loop filter.
```

This is a clean BBB-side follow-up because it uses the same environment,
candidate, target, seed policy, and Stage 6 comparison machinery, but adds
better direct baselines. It should not require changing the environment or
changing `state_collapser`.

Task B is not an evaluation task. It is a conceptual safety rail for
`state_collapser` users and future engineers. The language needs to warn that
there are several different objects in play:

```text
hidden phase graph / hidden MDP H:
  the environment's primitive transition system, including ambient action
  proposals, invalid proposals, and self-loop realizations.

runtime discovered graph:
  the portion of H exposed so far by interaction and local vista refresh.

quotient / tower action surface:
  a derived control surface built from discovered edges, state/action cells,
  executable lifts, and loop/internal-edge policy.

policy-induced Markov chain:
  what you get only after choosing a policy on one of those control surfaces.
```

The pitfall is that a direct learner and a tower learner may not be choosing
from the same kind of action object:

```text
direct may choose from ambient primitive action labels;
tower may choose from live quotient action cells whose internal/self-loop
edges have been suppressed.
```

If invalid environment actions are represented as self-loops, then a
loop-dropping tower construction can silently produce an action-safety
advantage. That advantage may be desirable, but it must be named. Otherwise an
engineer can mistake:

```text
benefit from local loop/invalid filtering
```

for:

```text
benefit from abstraction or hierarchy itself.
```

So yes: I think your two-task split is exactly right.

For BBB, we design the cleaner direct-control evaluation. For
`state_collapser`, we create language that tells engineers:

```text
Before comparing direct and tower control, ask whether the direct baseline and
the tower controller see equivalent action surfaces. If the tower drops
internal/self-loop edges and the environment realizes invalid moves as
self-loops, add an explicit guarded-direct baseline or narrow the claim.
```

That framing would have caught this PlateSupport ambiguity before the first
public interpretation pass.

### Project Owner Turn
> Can you create a document for me, at root, that explains to `state_collapser` engineers exactly what the issue is, and that also explains where in `state_collapser` this becomes relevant? And then, in the present design folder, create an extremely detailed blueprint for the work we need to do for par t1 of the fix.

### Codex Turn

Yes. I can create both of those, and I think the split you propose is exactly
the right artifact split:

```text
root handoff / issue document:
  for state_collapser engineers;
  explains the conceptual pitfall and points to where it becomes relevant in
  state_collapser.

BBB blueprint:
  for this repo;
  specifies the guarded-direct PlateSupport follow-up evaluation that repairs
  the comparison ambiguity.
```

I would not merge these into one document. They have different audiences and
different authority surfaces.

For the root handoff document, I would create something like:

```text
state_collapser_hidden_mdp_vs_quotient_action_surface_handoff.md
```

or, slightly more directly:

```text
state_collapser_invalid_action_self_loop_filtering_issue.md
```

The audience should be `state_collapser` engineers, not BBB evaluation
implementers. The document should say, in plain engineering terms:

```text
When an environment has an ambient primitive action alphabet, and invalid
state-action proposals are realized as self-loops, a tower/quotient controller
that drops internal/self-loop edges may receive an implicit local action
filter that a raw direct controller does not receive.
```

It should then make the pitfall explicit:

```text
If you compare raw primitive-action direct control against tower control,
and the tower action surface hides internal/self-loop edges, the tower may
look better partly because it was never offered invalid/self-loop choices.
That can be a valid engineering feature, but it is not the same claim as
"hierarchical abstraction improved learning."
```

The `state_collapser` locations I would point engineers toward are:

```text
state_collapser.examples.plate_support_env.primitive_transition(...)
```

because that is where invalid PlateSupport proposals become:

```text
candidate_valid = False
valid_transition = False
invalid_move = True
next_state = source_state
```

and:

```text
state_collapser.examples.plate_support_env.PlateSupportHiddenGraph.out_edges(...)
state_collapser.examples.plate_support_env.PlateSupportHiddenGraph.apply_action(...)
```

because those expose primitive proposal edges to the tower runtime.

Then:

```text
state_collapser.tower.runtime.TowerRuntime
```

because it builds/updates the partition tower from the discovered/vista graph.

Then:

```text
state_collapser.tower.partition.tower.PartitionTower
state_collapser.tower.partition.action_layer.ActionPartitionLayer
state_collapser.tower.partition.loop_policy.LoopPolicy
```

because that is where internal/self-loop edges are treated as internal
structure rather than live outgoing action cells. In particular, the relevant
ideas are:

```text
LoopPolicy.drop_internal()
ActionPartitionLayer.rebuild_action_cells_for_collection(...)
PartitionTower.executable_action_cells(...)
PartitionTower.executable_lift_candidates(...)
```

The handoff should be careful not to say "`state_collapser` is wrong." The
better language is:

```text
The semantics are useful and may be intended, but benchmark users need to
compare equivalent action surfaces or explicitly label the tower as receiving
a loop/internal-edge filter.
```

For the BBB blueprint, I would create it in this folder, probably:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/09_direct_star_culdesac_control/01_001_plate_support_direct_star_culdesac_control_blueprint.md
```

The blueprint should cover Part 1 of the fix only: the evaluation repair in
BBB. It should not attempt to redesign `state_collapser`.

The core blueprint target should be:

```text
Create a PlateSupport guarded-direct follow-up comparison that reuses the
current iterated tower candidate and Stage 5 binary target, then compares:

1. raw direct;
2. direct_invalid_guard;
3. direct_nonself_guard;
4. selected tower candidate.
```

The most important design lock is:

```text
direct_invalid_guard and direct_nonself_guard must be explicit arms, not
silent changes to the existing direct baseline.
```

Otherwise we erase the very comparison we are trying to explain.

The blueprint should also specify the event/readout additions:

```text
guard_type
guarded_action_count
available_action_count_before_guard
available_action_count_after_guard
invalid_guard_filtered_count
self_loop_guard_filtered_count
all_actions_filtered_count
guard_fallback_used
chosen_action_would_have_been_invalid
chosen_action_would_have_been_self_loop
```

And it should make the interpretation grid explicit:

```text
tower beats raw direct but not direct_invalid_guard:
  ordinary validity filtering explains most of the original signal.

tower beats direct_invalid_guard but not direct_nonself_guard:
  Abdul's self-loop/internal-edge filtering explanation explains most of the
  remaining signal.

tower beats direct_nonself_guard:
  evidence remains for a tower-specific advantage after matching local
  non-loop action filtering.

direct_nonself_guard beats tower:
  tower may be paying abstraction/executable-lift overhead relative to a
  direct controller with the same local safety surface.
```

I would also make the blueprint preserve the current claim boundary:

```text
This is still smoke/calibration evidence, not a final robotics benchmark
claim. The purpose is causal diagnosis of the previous PlateSupport signal.
```

So yes: I can create both. My recommendation is:

```text
1. root state_collapser-engineer handoff document first;
2. BBB direct-star evaluation blueprint second;
3. only after PO review, turn the blueprint into a Phase.Stage.Action workplan.
```

That sequencing keeps the conceptual issue visible before we start coding the
evaluation repair.
