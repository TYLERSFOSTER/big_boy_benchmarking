# One-Third Schema Tower Diagnostics Design Discussion

## Status

Initial design conversation home.

This is for a proposed new evaluation on the existing
`counterpoint_symbolic_v001` environment family.

This is not a blueprint.

This is not a workplan.

This is not approval to implement code or run artifacts.

## Placement

Environment family:

```text
counterpoint_symbolic_v001
```

Design folder:

```text
docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/
```

Likely future evaluation surface, if approved later:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/
```

## Conversation

#### Project Owner / Evaluator Turn

> We've had a veryu brief initial conversation, at the Codex UI, about what I want for this evaluation, specifically how I want its runtime to work. Explain to me, in as much detail as you can, whart you think I want.

#### Embedded Engineering Consultant / Codex Turn

> My current understanding is that you want a new evaluation on the existing
> `counterpoint_symbolic_v001` environment, not a new environment family and
> not a new comparative performance benchmark.
>
> The goal is to isolate one contraction-schema/runtime question and inspect it
> carefully:
>
> ```text
> What tower do we get if we contract roughly one third of the relevant
> counterpoint graph edges at a time?
> ```
>
> You do not yet want a "tower beats direct" comparison. You do not yet want
> reward-learning conclusions. You want to see the tower details first: how the
> quotient is shaped, whether first-projection collapse is less extreme than
> the previous `pi_0(H)`-style evaluation, and whether the resulting tiers look
> like something a future controller could plausibly use.
>
> I think the runtime you are imagining is closer to a structural diagnostic
> than to the previous first serious learning run. The previous evaluation ran
> a full set of direct and tower learning arms. This one should probably run
> much closer to the tower-construction/schema-diagnostic surface:
>
> - build or select the counterpoint fixture;
> - construct the hidden graph;
> - apply a one-third contraction schedule;
> - inspect the resulting partition tower;
> - report state-cell counts by tier;
> - report action-cell counts by tier;
> - report first-block edge counts;
> - report largest cell/fiber sizes;
> - report whether each tier is degenerate, near-degenerate, or meaningfully
>   structured;
> - report lift/action availability if that is cheap and relevant;
> - avoid performance language.
>
> The phrase "one-third contraction schema" still needs an exact design
> decision. I see several possible meanings:
>
> 1. **Global thirds:** divide all base graph edges into three blocks of roughly
>    equal size, then contract block 1 to get tier 1, block 2 to get tier 2,
>    and block 3 to get tier 3.
> 2. **Per-state outgoing thirds:** at each source state, divide its outgoing
>    edges into thirds, so every source contributes approximately one third of
>    its outgoing edges to each contraction block.
> 3. **Seeded random thirds:** randomly assign edges to three blocks under a
>    recorded schema seed.
> 4. **Deterministic ordered thirds:** sort edges by a stable key and assign
>    them to block 1, block 2, block 3 deterministically.
> 5. **Label-aware thirds:** create thirds while respecting edge labels or
>    motion classes, so the blocks are not arbitrary random cuts.
>
> My guess from the UI conversation is that you are leaning toward the
> per-state outgoing interpretation, because it is closest to the earlier
> logHRL intuition: when a graph is being discovered or addressed locally, each
> node contributes some fraction of its own available action surface at each
> stage, rather than a giant global block accidentally percolating across the
> whole graph. But I do not want to lock that in without your confirmation.
>
> The key thing I think you are trying to avoid is exactly what happened in the
> last evaluation: a first contraction block that is so large or universal that
> `pr^0_1` immediately behaves like `H -> pi_0(H)`. A one-third schema may
> still collapse hard on this graph, but the point of the evaluation is to
> measure that honestly, not to assume it will work.
>
> I would frame the intended evaluation claim boundary like this:
>
> ```text
> This evaluation may claim facts about tower construction, quotient shape,
> cell/fiber size, degeneracy, and lift/action availability for a one-third
> contraction schema on counterpoint_symbolic_v001.
>
> It may not claim learner performance, tower advantage, musical quality,
> production performance, or general state_collapser quality.
> ```
>
> So the desired output is likely a human-readable diagnostic report, not a
> learning result. The report should make it easy for us to answer:
>
> - Did one-third contraction produce a more gradual tower?
> - Did tier 1 still collapse almost everything?
> - Are the quotient cells balanced or dominated by one giant cell?
> - Do action cells remain interpretable?
> - Are lift candidates available from representative current states?
> - Does this schema deserve a later controller-learning evaluation?
>
> That is what I think you want: a clean, schema-specific tower diagnostic for
> the existing counterpoint environment, designed to teach us what kind of
> quotient geometry one-third contraction produces before we ask whether it
> helps learning.

#### Project Owner / Evaluator Turn

> I would also like this evaluation to include details about what tiers agents occupy during train. The point is that a rough sanity-check for there even being a possiblity of improvement is that the agent's train run is a U-shape, roughly. Let me know if you understand my thinking here.

#### Embedded Engineering Consultant / Codex Turn

> Yes, I understand your thinking, and this changes the evaluation from "pure
> static tower construction diagnostic" into "tower construction plus minimal
> controller/occupancy diagnostic."
>
> The core idea, as I understand it, is:
>
> ```text
> A useful hierarchy should not make the agent live forever at one tier.
> During training, the agent should move through the hierarchy in a structured
> way.
> ```
>
> The rough sanity-check shape you are calling a U-shape is something like:
>
> 1. early training starts at or near the fine/base tier because the agent has
>    not yet learned reliable coarse addresses;
> 2. useful training then moves into coarser tiers because the quotient starts
>    giving the agent usable addresses or shortcuts;
> 3. later training returns downward/finer to refine executable concrete
>    behavior and resolve details.
>
> So the tier-occupancy curve over training should not be flat. It should not
> be:
>
> - always tier `0`, which would mean the tower is present but behavior is
>   effectively direct/base-tier control;
> - immediately stuck at a collapsed upper tier, which would mean the controller
>   found a quotient but cannot productively refine or execute;
> - random hopping with no interpretable movement pattern.
>
> Instead, a promising run would show some coarse-to-fine or fine-to-coarse-to-
> fine structure. The exact shape may be noisy, but the broad diagnostic is:
>
> ```text
> Does the controller actually use the tower as an address system during
> training?
> ```
>
> I also think your U-shape intuition connects directly to binary search. In
> binary search, a good search does not inspect every element at the base
> level. It makes coarse interval decisions, then narrows down, then resolves a
> final exact address. If our tower is acting like a search/address hierarchy,
> tier occupancy should show evidence of that kind of narrowing/refinement
> behavior. The agent should spend meaningful time away from tier `0`, but also
> eventually return to executable detail.
>
> For this evaluation, that means we should record at least:
>
> - active tier by training episode;
> - active tier by controller event;
> - active tier before and after each controller action;
> - successful concrete steps by active tier;
> - lift/action failures by active tier;
> - train/explore/exploit/execute action counts by tier;
> - a compact "tier occupancy over training" table or plot-like markdown
>   summary.
>
> I would not want to overclaim from this. A U-shape is not proof of
> performance improvement. It is a sanity-check that improvement is even
> plausible: the controller is using the hierarchy in a way that looks like
> hierarchical search rather than dead code, immediate collapse, or base-tier
> fallback.
>
> So I would now frame the evaluation as having two diagnostic halves:
>
> 1. **Tower geometry:** what quotient tower does the one-third schema produce?
> 2. **Tier occupancy during train:** does the agent actually move through that
>    tower in a plausibly useful way?
>
> Still no comparison yet. Still no tower-advantage claim. But yes: tier
> occupancy during train belongs in this evaluation if the point is to decide
> whether the one-third schema is worth taking seriously as a future learning
> arm.

#### Project Owner / Evaluator Turn

> No. There are critical misunderstandings in your picture of how/why this works. Scour the `state_collapser` repo to try to correct your understanding. The key mistakes you're making also appear in converations around "ABC", i.e., "Always Be Closing" there. Research that and then report back.

#### Embedded Engineering Consultant / Codex Turn

> I found the correction, and my previous answer was materially wrong.
>
> The mistake was not just a small wording problem around "U-shape." I had the
> control polarity wrong.
>
> I described tier movement as if the normal story were:
>
> ```text
> begin at concrete/base detail -> earn permission to use coarser tiers ->
> later return to finer detail
> ```
>
> That is too close to the exact misunderstanding that the `state_collapser`
> ABC docs correct. The relevant correction is in:
>
> ```text
> <state-collapser-repo>/docs/design/HRL_exploit-explore/01_015_abc_find_unclosed_correction.md
> <state-collapser-repo>/docs/design/HRL_exploit-explore/01_016_find_lowest_unclosed_system_change_blueprint.md
> <state-collapser-repo>/src/state_collapser/tower/control/signals.py
> <state-collapser-repo>/src/state_collapser/tower/control/controller.py
> ```
>
> The governing idea is not "descend once the current tier is mature enough."
> The governing idea is:
>
> ```text
> Always Be Closing = find the lowest, highest-indexed, currently unclosed
> executable tier and go there.
> ```
>
> So the runtime question is not primarily:
>
> ```text
> Has this tier earned permission to descend?
> ```
>
> It is:
>
> ```text
> Which tier is the deepest still-productive unclosed locus right now?
> ```
>
> In the current `state_collapser` implementation this is not just a metaphor.
> `select_lowest_unclosed_tier(...)` scans from `deepest_known_tier` down to
> `0`, skips non-executable tiers if an executability predicate is supplied,
> and returns the first tier that still has productive-learning pressure. Then
> the controller chooses `LIFT` if the active tier is below that selected tier,
> `DESCEND` if the active tier is above it, and otherwise trains/explores/
> executes at the selected locus.
>
> That means I also conflated the directional language. In the ABC docs,
> "lowest," "downstairs," and "deeper" mean higher-indexed tower tiers. They do
> not mean "finer concrete detail." Lift is the move back upward toward a
> smaller tier index and finer/higher-resolution work. My earlier phrase
> "returns downward/finer" was backwards and should not survive into a
> blueprint.
>
> The corrected interpretation of your U-shape request is therefore not:
>
> ```text
> Do we see a pleasant fine -> coarse -> fine lifecycle?
> ```
>
> The corrected interpretation is closer to:
>
> ```text
> Do we see active-tier occupancy governed by ABC closure semantics?
> ```
>
> That can still produce a U-like occupancy trace under some circumstances,
> but the U-shape is not the law. The law is closure-seeking. A healthy run
> should tend to move toward the deepest currently executable unclosed tier,
> stay there while useful learning is still happening there, and move upward
> only when that tier is no longer the productive locus or is not executable.
> Non-closure downstairs should attract descent; it is not a reason to avoid
> descent.
>
> So for this proposed one-third schema diagnostics evaluation, the tier
> occupancy section should not merely report:
>
> ```text
> how much time did the agent spend at tier 0, tier 1, tier 2, ...
> ```
>
> It should report enough to test the ABC story:
>
> - active tier by controller event and by training episode;
> - selected lowest-unclosed tier, if we can get it directly or reconstruct it
>   faithfully from emitted signals;
> - controller action counts: `descend`, `lift`, `train`, `explore`,
>   `exploit_execute`, and `no_available_action`;
> - per-tier productive-learning pressure or its available proxy;
> - per-tier closure/unclosed status;
> - per-tier executability status;
> - cases where the selected lowest-unclosed tier is skipped because it is not
>   executable;
> - transitions where the active tier moves toward or away from the selected
>   lowest-unclosed tier.
>
> The primary sanity check then becomes:
>
> ```text
> Is active-tier movement consistent with "find lowest executable unclosed,"
> or is the runtime pinned, oscillating without closure explanation, or
> blocked by executability/lift structure?
> ```
>
> This also changes how I would use the binary-search analogy. The useful
> analogy is not "start at a point, jump coarse, then come back fine" as a
> generic shape. The better analogy is that binary search keeps choosing the
> unresolved interval where useful information remains, closes off regions
> when they stop being live candidates, and then resolves the remaining
> address at the necessary resolution. In our tower setting, the equivalent
> diagnostic is not just the visual shape of tier occupancy. It is whether the
> controller is concentrating work at the deepest unresolved/productive
> quotient locus that is still executable.
>
> So I would now revise the evaluation intent like this:
>
> ```text
> This evaluation should diagnose the one-third contraction schema in two
> linked ways:
>
> 1. What tower geometry does the schema create?
> 2. When a training/control run uses that tower, does active-tier behavior
>    obey ABC-style lowest-executable-unclosed selection?
> ```
>
> The evaluation should still not make a tower-beats-direct performance claim.
> But it should be strong enough to tell us whether the one-third tower is
> structurally meaningful and whether runtime control is even occupying it in
> the way `state_collapser` now says hierarchy use is supposed to work.

#### Project Owner / Evaluator Turn

> Next request: Most of this "ABC" logic is already present in `state_collapser` (check this in detail). We're are trying to test *that*, so do not rewrite any of it for this evaluation. Use it! Do we now have enough to write full blueprint for this evaluation?

#### Embedded Engineering Consultant / Codex Turn

> Yes. With that correction, I think we now have enough to write the full
> blueprint.
>
> I checked this in detail, and your instruction is right: the ABC logic should
> be treated as an upstream `state_collapser` behavior under test, not as logic
> for BBB to recreate.
>
> The relevant upstream pieces already exist:
>
> ```text
> state_collapser.tower.control.ActiveTierController
> state_collapser.tower.control.select_lowest_unclosed_tier
> state_collapser.tower.control.productive_learning_pressure
> state_collapser.tower.control.is_unclosed
> state_collapser.tower.control.should_descend
> state_collapser.tower.control.should_lift
> state_collapser.tower.runtime.ExploitExploreTowerRuntime
> ```
>
> The upstream tests also cover the important ABC cases:
>
> - deepest/highest-indexed unclosed tier is preferred;
> - non-executable tiers are skipped during lowest-unclosed selection;
> - the controller descends toward deeper unclosed executable tiers;
> - the controller lifts when the active tier is no longer the selected
>   lowest-unclosed tier;
> - the runtime lifts out of non-executable active tiers before executing;
> - the runtime returns `NO_AVAILABLE_ACTION` when no executable tier exists.
>
> BBB already uses this rather than a homegrown control loop. In the current
> counterpoint serious tower-control runner, BBB constructs:
>
> ```text
> ExploitExploreTowerRuntime(
>     controller=TimedActiveTierController(...),
>     tier_is_executable=adapter.tier_is_executable,
>     ...
> )
> ```
>
> and `TimedActiveTierController` delegates to upstream
> `ActiveTierController`. So the blueprint should be very explicit:
>
> ```text
> BBB must not implement an alternate ABC policy.
> BBB may only:
> - choose/build the counterpoint contraction schema;
> - provide the counterpoint `tier_is_executable` predicate;
> - run the upstream runtime/controller;
> - record enough diagnostic surfaces to evaluate what the upstream controller
>   did.
> ```
>
> That gives us a much cleaner evaluation target:
>
> ```text
> For a one-third contraction schema on counterpoint_symbolic_v001, what tower
> is produced, and how does the existing upstream ABC controller occupy and move
> through that tower during training/control events?
> ```
>
> The current BBB instrumentation is close but not sufficient for this
> evaluation. It already records:
>
> - `control_events.csv`;
> - active tier before/after;
> - control action;
> - learner update success/TD fields where available;
> - `lift_fiber_events.csv`;
> - quotient summary fields such as tier count and cell counts;
> - timing surfaces.
>
> But for this evaluation, the blueprint should require additional diagnostic
> fields. These should be computed by calling upstream `state_collapser`
> helpers on the same inputs passed to `ActiveTierController`, probably inside
> BBB's existing `TimedActiveTierController` wrapper, before delegating to the
> upstream controller. That is instrumentation, not policy.
>
> The missing fields I would make first-class are:
>
> - selected lowest executable unclosed tier;
> - per-tier executable boolean at the current state;
> - per-tier productive-learning pressure;
> - per-tier unclosed/closed boolean;
> - deepest known tier;
> - whether the chosen action moved toward the selected tier;
> - whether an apparent failure to descend was actually explained by
>   executability;
> - whether an apparent lift was explained by the selected lowest-unclosed tier
>   moving upward.
>
> That lets the evaluation test upstream ABC behavior without redefining it.
> The diagnostic question becomes:
>
> ```text
> Given the tower and the signals available to upstream state_collapser, did the
> upstream controller choose actions consistent with its own
> lowest-executable-unclosed semantics?
> ```
>
> For the one-third schema itself, I think the blueprint can proceed, but it
> should include one explicit PO decision point: what exactly "one third" means
> operationally. My current best default is a deterministic or seeded
> per-source outgoing-edge thirds schema, because that avoids a single global
> edge ordering accidentally deciding all local action availability. But I
> would put that as a blueprint question rather than smuggling it in as if it
> were settled.
>
> So: yes, we have enough to blueprint. The blueprint should be detailed and
> should include turn questions, but those questions should be narrow:
>
> 1. What precise one-third contraction rule should be used?
> 2. Should this evaluation use one schema seed, several schema seeds, or a
>    deterministic no-seed construction for the first pass?
> 3. Should the first diagnostic run use the existing small instance only, or
>    tiny-plus-small so we can separate inspection convenience from meaningful
>    structure?
> 4. What minimum artifact set counts as "human-readable enough" for tier
>    occupancy and ABC behavior?
>
> The blueprint should not ask broad new questions about whether ABC is the
> right policy, whether BBB should design a new controller, or whether this is a
> comparison benchmark. Those are not open here. The evaluation is an existing
> environment, a new schema/evaluation surface, upstream ABC runtime under
> observation, and human-readable tower/occupancy diagnostics.

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> ...

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> ...
