# Counterpoint Noisy-Rate Full-Tower Training Diagnostic Design Discussion

## Purpose

This document starts the design discussion for a future evaluation that trains
on the non-collapsed noisy-rate counterpoint towers discovered by the current
diagnostic work.

The evaluation should answer a narrow health question:

```text
Can each selected non-collapsed noisy-rate tower support a real tower-only
training budget while preserving interpretable tower, lift, occupancy, and
runtime traces?
```

It should not yet answer comparative performance questions.

## Project Owner Stated Intent

Verbatim Project Owner direction from the chat:

> yers this is exactly what i meanL: "take each non-collapsed noisy-rate counterpoint tower from the current diagnostic, build its full available tower, then run a real tower-only training budget on it with no direct baseline comparison" Start in a new folder here: ```docs/design/system_learning_from_evaluations```

## Consultant Framing

This is naturally the next evaluation after the noisy-rate contraction
diagnostic if the Project Owner wants to move from "does the schema avoid
immediate collapse?" to "does the resulting non-collapsed tower actually train
and produce readable runtime evidence?"

The proposed evaluation class is:

```text
tower-training health diagnostic
```

It should be designed as a positive executability/training-health check, not
as a benchmark comparison.

## Current Working Scope

The current working meaning of "each example" is:

- use the non-collapsed noisy-rate examples surfaced by the current
  counterpoint noisy-rate diagnostic;
- build the full tower available for each selected example;
- run tower-only training with a real but explicitly bounded budget;
- record tower shape, tier occupancy, lift behavior, concrete execution,
  returns, episode outcomes, and training/update traces;
- generate human-readable readouts that say whether each example trained
  cleanly, partially, or failed.

The candidate list should be derived from the current artifacts/readout surface
rather than copied forward by hand as a stale fixed list.

## Scope Locks

The evaluation should not include:

- direct baseline training;
- schema-to-schema comparison claims;
- advantage claims;
- musical-quality claims;
- broad generalization claims;
- environment redesign.

Those can be future evaluations. This one should stay focused on whether the
current non-collapsed noisy-rate towers can be trained on as towers.

## Design Questions For Project Owner

These are consultant-authored open questions, not Project Owner statements.

1. What budget should count as "real training" for the first pass: small enough
   to run quickly, or large enough to expose learning curves?
2. Should the no-contraction control be omitted entirely, or included only as a
   runtime sanity check while still avoiding comparison claims?
3. Should every non-collapsed arm/seed from the latest diagnostic be trained,
   or should we cap the candidate count if the diagnostic later produces many
   examples?
4. Should success be defined as "training completes with coherent traces," or
   should it require minimum movement in reward/return or tier-occupancy
   metrics?
5. Should the readout group examples by noisy-rate arm first, or by health
   status first?

## Consultant Recommendation

The first blueprint should keep the evaluation deliberately simple:

- train every currently non-collapsed noisy-rate arm/seed example;
- omit direct baselines;
- include no-contraction only if the Project Owner wants a runtime sanity
  anchor;
- treat reward movement as descriptive evidence, not a success requirement;
- make success/failure primarily about executability, trace completeness,
  lift/concrete health, and non-degenerate tower occupancy.

## Conversation

### Project Owner Turn

> yers this is exactly what i meanL: "take each non-collapsed noisy-rate counterpoint tower from the current diagnostic, build its full available tower, then run a real tower-only training budget on it with no direct baseline comparison" Start in a new folder here: ```docs/design/system_learning_from_evaluations```

### Codex Turn

I created this folder as the design surface for the full-tower training
diagnostic. The key alignment point is that this is a training-health
evaluation over the current non-collapsed noisy-rate towers, not a comparison
benchmark and not a new environment.

