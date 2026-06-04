# Diagnostic Findings

## Full-Iterated Tower Built

`results/tower_shape_summary.csv` records the repaired Schema 1 sequence:

```text
tier 0: 108 state cells, 1140 active action cells
tier 1: 54 state cells, 1029 active action cells
tier 2: 27 state cells, 647 active action cells
tier 3: 19 state cells, 488 active action cells
tier 4: 14 state cells, 215 active action cells
```

This is the requested multi-tier object. It is not the old two-tier one-drop
artifact.

## Terminal But Not Degenerate

The final tier has 14 state cells and largest state-cell share about `0.8611`.
It is not a one-cell degenerate tier. The iterated `1/18` noisy-rate process
terminates there because the next quotient sampling step does not schedule a
new representative edge.

## Tier Usage

Schema 1 controller events occur at the deep tier:

```text
tier 4 explore: 363
tier 4 train: 112
tier 4 exploit_execute: 5
```

The run therefore did not merely construct deeper tiers; it actually used the
deepest available tier during control.

## Claim Block

Schema 0 is `transient_hit_only`. Schema 1 is `never_hit`. The paired
comparison is correctly blocked.
