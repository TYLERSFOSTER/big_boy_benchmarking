# Fraction Sweep Readout Conversation Archive

Source:

```text
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/README.md
```

This archive preserves the clarifying-turn conversation that motivated a
possible noisy-rate contraction diagnostic. The transcript below keeps Project
Owner and Codex turns separated for attribution discipline.

## Conversation

#### Project Owner / Evaluator Turn

> Tell me as much as you can about this $1/18$ collapse.

#### Embedded Engineering Consultant / Codex Turn

> The most important thing is that `1/18` is not "one eighteenth of the whole graph" in the intuitive global sense. Under this evaluation's source-local quota rule, every source state with outgoing edges contributes at least one scheduled outgoing edge:
>
> ```text
> max(1, ceil(out_degree * n / 18))
> ```
>
> In this small fixture, that means `n01_over_18` schedules `112` edges out of `1140` total base edges, for an edge share of about `0.098`. The scheduled set is still source-covering: all `108` source states have at least one scheduled edge, with minimum selected edges per source `1`, mean about `1.037`, and maximum `2`. So the weak-looking fraction is actually a one-edge-or-more constraint from every source state.
>
> The endpoint-coalescence table explains the collapse mechanically. For `n01_over_18`, the scheduled block processed `112` edges. Of those, `107` were useful coalescences and `5` were redundant/internal by the time they were processed. Since the base has `108` states, `107` useful coalescences is exactly enough to merge all base states into one state cell under repeated endpoint coalescence. The table also says the first singleton state cell appears at processed edge index `112`, and `collapse_required_most_of_block=True`. That matters: this was not a collapse caused by the first few edges. The whole scheduled block was needed, and by the end it had supplied enough endpoint identifications to bind the entire base state set.
>
> The tier-shape table is the visible result:
>
> ```text
> base tier:      108 state cells, 1140 active action cells
> n01 tier 1:       1 state cell,     0 active action cells
> ```
>
> The raw historical action-cell record count at the collapsed tier is `1532`, but the active action-cell count is `0`. That is the distinction we added because it is easy to misread the raw records as live executable structure. They are not. At tier 1, the quotient shape exists historically, but the live control surface has no active executable action cells.
>
> My current interpretation is: the collapse is probably not "1/18 is already a large fraction" by itself. It is more specifically that the `max(1, ...)` per-source floor creates a source-covering scheduled block. In a graph with 108 states, one selected outgoing edge from essentially every state can easily behave like a spanning binding mechanism under endpoint-coalescence semantics. The total edge share is under ten percent, but the source coverage is one hundred percent, and source coverage is probably the more important structural variable here.
>
> That suggests the next diagnostic question is not only "what happens for smaller fractions?" because the current quota rule has no smaller nonzero source-local behavior than one scheduled edge per source. The sharper questions are:
>
> - What happens if the quota rule is global edge-budgeted instead of source-local floor-budgeted?
> - What happens if some sources are allowed to contribute zero scheduled edges?
> - Is collapse driven mostly by source coverage, by particular high-bridge edges, or by the counterpoint transition graph's endpoint geometry?
> - Does the same immediate collapse happen for the medium fixture at `1/18`, or is this small-fixture-specific?
>
> So I would treat this smoke result as a strong warning about the contraction-selection semantics. It does not yet prove that every low-fraction schedule collapses counterpoint. It proves that this particular source-local floor rule, even at `1/18`, is strong enough to bind the whole small fixture in one scheduled block.

#### Project Owner / Evaluator Turn

> How difficult is it to modify this so that it's more noisy than a ceiling function? That would let us take the ratio way lower... like $1/36$ meaning like a distribution wiht mean $1/36$, but that often samples no arrows. I believe we've set contraction schemata up so that this would be simple to implement, but I dont know how different it would be from the details of the $1/18$ evaluation.

#### Embedded Engineering Consultant / Codex Turn

> I think your instinct is basically right: the contraction-schema side should be fairly simple, because the current implementation already isolates selection into a small set of surfaces. But it is not just "change 18 to 36." The current collapse is caused by the source-local ceiling-and-floor rule:
>
> ```text
> max(1, ceil(out_degree * n / denominator))
> ```
>
> That rule guarantees every source with outgoing edges contributes at least one scheduled edge. A noisy-rate rule would deliberately remove that guarantee. The cleanest version would be something like independent seeded Bernoulli selection over candidate outgoing edges:
>
> ```text
> select each outgoing edge with probability numerator / denominator
> ```
>
> Under a `1/36` Bernoulli rule, a source with out-degree `10` would have expected selected count `10/36`, but probability of selecting no edge:
>
> ```text
> (35/36)^10 ~= 0.754
> ```
>
> So most sources would contribute zero scheduled edges. That is exactly the behavior we cannot express with the current source-local quota floor. It would let us ask whether collapse was driven by the mere existence of a source-covering scheduled block.
>
> Implementation difficulty: small-to-moderate. I would not want to mutate the current fraction-sweep semantics in place, because this readout and its artifacts now mean "source-local ceil floor." I would add a sibling schema/evaluation mode, probably with a name like `counterpoint_noisy_rate_contraction_diagnostics_v001` or `counterpoint_bernoulli_rate_contraction_diagnostics_v001`.
>
> The likely code changes are contained:
>
> - Add a shared metadata helper parallel to `source_local_fraction_selections`, but with Bernoulli/random-rate selection and no minimum-one floor.
> - Add a runtime `ContractionSchema` parallel to `CounterpointOutgoingFractionSchema`, where `assign_edge()` returns the single scheduled block if the edge's seeded Bernoulli draw passes.
> - Add summary fields that make the new semantics legible: selected edge count, selected edge share, source count with at least one selected edge, zero-selected-source count, selected-source share, and maybe selected-source out-degree distribution.
> - Reuse most of the existing runner/aggregation/readout machinery, because tower construction, active action-cell counting, endpoint-coalescence diagnostics, concrete-step recording, and README generation are already shaped correctly.
> - Add tests for determinism, approximate expected rate on fixed fixtures, allowed zero-selection sources, and no accidental source-local floor.
>
> The main design choice is the sampling unit. I see three plausible options:
>
> - Edge Bernoulli: every edge independently selected with probability `p`. This is simplest and directly expresses "mean `1/36`."
> - Source-local binomial: each source samples `Binomial(out_degree, p)` edges, then takes that many shuffled outgoing edges. This gives the same count distribution per source, but preserves the current stable shuffled-prefix style.
> - Poisson count per source: sample `Poisson(out_degree * p)` then cap by out-degree. This is noisier and maybe mathematically attractive, but adds another distributional assumption.
>
> I would probably choose source-local binomial for continuity with this evaluation: it keeps the per-source deterministic shuffle, removes only the minimum-one floor, and gives us easy source-level summaries. Edge Bernoulli is also fine, and arguably even clearer. I would avoid Poisson first unless we specifically want that model.
>
> How different from the `1/18` evaluation? The runtime and artifact pipeline can be mostly reused; the interpretation changes a lot. The current evaluation sweeps deterministic source-covering quotas. The noisy-rate evaluation would sweep expected rates and explicitly measure source coverage as an outcome. The central question would become:
>
> ```text
> At what expected edge rate, and at what realized source coverage, does endpoint coalescence begin to collapse the tower?
> ```
>
> That is probably the next right diagnostic. It directly tests the hypothesis that `1/18` collapsed because it was source-covering, not because ten percent of edges is inherently too many.

#### Project Owner / Evaluator Turn

> Ok. Create the folder for the new evaluation, and copy this conversation over there.

#### Embedded Engineering Consultant / Codex Turn

> Created `docs/design/system_learning_from_evaluations/counterpoint_noisy_rate_contraction_diagnostics/` as the design-side home for the proposed noisy-rate follow-up evaluation. I copied the motivating readout conversation into `01_fraction_sweep_readout_conversation_archive.md` and added a local `README.md` that records the current status as design conversation only: no blueprint, no gameplan, no implementation, and no artifacts yet.
>
> I also added the folder to the system-learning index so future LLM/engineer passes can detect it by the phrases `noisy-rate contraction`, `Bernoulli edge selection`, and `zero-selected sources`.
