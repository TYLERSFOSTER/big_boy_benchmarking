# Second Counterpoint Serious Evaluation Design Discussion

Date opened: 2026-06-03

Repository:

```text
/Users/foster/big_boy_benchmarking
```

Environment:

```text
counterpoint_symbolic_v001
```

## Status

Discussion surface opened.

No blueprint exists yet.

No implementation gameplan exists yet.

No source edits, runtime changes, benchmark runs, or artifact writes are
authorized by this document.

## Attribution Boundary

This is a turn-by-turn design discussion surface.

Do not put words in the Project Owner's mouth. Empty `> ...` placeholders are
available for future turns only; they are not Project Owner answers.

## Starting Context

The Project Owner has stated that the next work is:

```text
Ok. I want to start a really serious new evaluation. It will be in the same
counterpoint environment we've been using
```

The Project Owner then requested:

```text
Make a folder for it, and then we'll have duscssion ther
```

Known lock from that instruction:

- This is a new evaluation design discussion.
- It uses the existing `counterpoint_symbolic_v001` environment family.
- This is not a new environment design.

Unsettled until the Project Owner specifies otherwise:

- evaluation name;
- primary scientific question;
- arms or schemas;
- baselines;
- candidate source;
- budget;
- seed policy;
- artifact/readout surface;
- success, warning, and failure criteria;
- claim boundary.

## Turns

#### Project Owner / Evaluator Turn

> Ok so what I want to compare here is training under two contraction schemata, with all other hyperparameters/knobs as equivalent as possible. Schema 0 is "not contraction," so the agent stays in the total space the whole time, Schema 1 is one from
> - `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics`
>
> or
> - `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic`
>
> Even let it do only one drop, so that Schema 1 creates only tiers 0 and 1. The reason we need a knob here is because we need to include reward cut-off for jumping up tier... it introduces an upperbound, so maybe what we actually measure is first to hit upperbound on total space. Let me know if this makes sense to you.

#### Embedded Engineering Consultant / Codex Turn

> Yes, this makes sense to me. I understand the intended comparison as: hold the counterpoint environment, training budget, seed policy, learner class, reward semantics, and ordinary hyperparameters as fixed as possible, then compare two schema arms. Schema 0 is the no-contraction / total-space arm: the learner acts in the original counterpoint state-action space for the whole run. Schema 1 is a one-drop tower arm: tier 0 is the same total space, tier 1 is a single noisy-rate quotient, and the agent/controller is allowed to move between those two tiers according to the locked tier-control rule.
>
> I think the clean source distinction is important. `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics` is the parent structural source for noisy-rate schema parameters and contraction evidence. `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic` is the stronger source for choosing candidate schema instances, because it already says which non-collapsed noisy-rate candidates can execute a tower-only training-health smoke budget. So my default recommendation is: select Schema 1 candidates from the full-tower training diagnostic readout, while preserving provenance back to the contraction diagnostic that generated those candidates.
>
> The reward cutoff / tier-jump knob is the subtle part, and I agree it probably changes what the most honest primary metric should be. If upward tier movement is gated by a reward threshold or capped objective, then raw final reward can become a bad comparison target because both arms may saturate or be censored by the upper bound. A better primary metric may be first passage: how much training budget is needed before the policy first reaches the locked total-space upper bound or reward cutoff condition. In that framing, the comparison is not "which arm has larger final reward?" but "under matched budget and matched environment, does the one-drop quotient arm reach the total-space success threshold sooner, later, or not at all?"
>
> I would not yet blueprint until we pin down three things: what exactly counts as the upperbound hit in total space, whether Schema 0 is run through the same controller abstraction with contraction disabled or through the existing direct learner path, and whether Schema 1 is one specific noisy-rate candidate or a small fixed set of candidates carried over from the full-tower diagnostic. But the design target itself is coherent.

#### Project Owner / Evaluator Turn

> *what exactly counts as the upperbound hit in total space,*
>
> I think maybe stayign above a certain level consistently.
>
> *whether Schema 0 is run through the same controller abstraction with contraction disabled or through the existing direct learner path
> I don't get it the two Schema are what we're comparing I don;t get it... it needs the same threshold for comparison. I dont understand what the ambiguity is here.*
>
> *whether Schema 1 is one specific noisy-rate candidate or a small fixed set of candidates carried over from the full-tower diagnostic. But the design target itself is coherent.*
>
> Ah yeah a few carried over is better.

#### Embedded Engineering Consultant / Codex Turn

> Yes, that clarifies the design and also exposes where my earlier wording was muddy. The threshold itself should absolutely be the same comparison target for both schemas. The ambiguity I meant was not "do the arms use the same success threshold?" They do. The ambiguity was implementation-level: do we implement Schema 0 by reusing an older direct learner path, or do we run Schema 0 through the same new comparison harness as Schema 1 with contraction disabled / identity schema? For this evaluation, I now think the answer should be: use the same comparison harness as much as possible, and let the schema be the thing that changes. Schema 0 is the no-contraction schema in that harness; Schema 1 is the one-drop noisy-rate schema in that harness.
>
> The reason that matters is fairness. If Schema 0 uses an old direct-runner implementation while Schema 1 uses the tower-control runner, then the comparison silently mixes "contraction schema" with "different runtime/controller implementation." That would make the result harder to trust. Your framing is cleaner: the two schema arms are what we are comparing, so the evaluation should hold the threshold, budget, learner family, seed policy, reward interpretation, and as much runner machinery as possible fixed. The direct/no-contraction condition should be represented as Schema 0, not as an unrelated baseline path, except maybe as a secondary sanity anchor if we explicitly label it that way.
>
> "Staying above a certain level consistently" also makes sense to me as the upperbound-hit condition. I would translate that into a first-sustained-hit metric rather than a one-episode spike. Something like: the first episode index at which the run enters a window where the score/reward/criterion is above the locked cutoff for enough consecutive episodes or enough of a rolling window. The exact cutoff and persistence rule can stay open for now, but the shape should be locked: first passage to sustained total-space adequacy, not merely final reward and not a transient max.
>
> On candidate choice: agreed, a few carried-over Schema 1 candidates is better than one. My default would be to carry a small fixed set from the noisy-rate full-tower training diagnostic, because those candidates already passed the "non-collapsed and tower-trainable enough to smoke" filter. That lets the serious comparison ask a sharper question: among quotient candidates that are known to be executable, does one-drop contraction change first-sustained-hit behavior relative to no contraction under matched training conditions?

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> ...
