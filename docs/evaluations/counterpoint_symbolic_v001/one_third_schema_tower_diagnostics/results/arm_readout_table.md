# Reader-Facing Diagnostic Table

This evaluation has one diagnostic condition rather than a set of competing
arms. The table is still named `arm_readout_table.md` because the repo-wide
readout protocol expects this file. Here, each row is an instance-level
diagnostic readout.

| Instance | Runs | Episodes | Horizon | Base states | Base edges | State cells by tier | First projection | Concrete steps | Lift success rate | ABC events | Readable status |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | --- |
| `counterpoint_symbolic_n3_small_v001` | 12 | 192 | 8 | 108 | 1140 | `(108, 1, 1, 1)` | full collapse | 1536 | 1536 / 1536 | 1920 | Diagnostic structural limit; base-tier execution succeeds. |
| `counterpoint_symbolic_n3_medium_v001` | 12 | 192 | 12 | 228 | 2732 | `(228, 1, 1, 1)` | full collapse | 2304 | 2304 / 2304 | 2880 | Diagnostic structural limit; base-tier execution succeeds. |

The most important row value is not reward. It is the state-cell tuple:

```text
(base tier, tier 1, tier 2, tier 3)
```

For both instances, tier `1` has one state cell. That says the first quotient
projection collapses the whole base graph. Any future comparison using this
schema must treat that collapse as the primary condition, not as an ordinary
learning result.
