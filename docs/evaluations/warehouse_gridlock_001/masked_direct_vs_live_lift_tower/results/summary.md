# Results Summary

`masked_8ep_001` completed successfully as a diagnostic pilot.

The main result is a tie:

```text
mean reward direct = 379.9375
mean reward tower  = 379.9375
score direction    = tie
```

Both arms completed 16 episodes, selected 128 valid steps per episode on average, selected zero invalid steps, and recorded zero terminal successes.

The useful evidence is therefore not a tower-performance result. It is a clean fairness/readiness result:

- equal immediate candidate-set masking for both arms;
- no successor-state `Out` used for selection;
- zero tower live-lift failures;
- generated candidate surface includes multi-robot actions up to active count 8.

The task itself was not solved. Boxes made no target progress in either arm.
