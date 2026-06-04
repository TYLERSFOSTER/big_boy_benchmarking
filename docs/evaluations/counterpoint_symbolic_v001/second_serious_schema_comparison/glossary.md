# Glossary

- Schema 0: total-graph/no-drop control arm.
- Schema 1: noisy-rate tower arm. In the repaired artifact, Schema 1 uses the
  full iterated tower source, not the old one-drop-only source.
- Full iterated tower: repeated contraction tier by tier until the process
  reaches a terminal or degenerate tier.
- Terminal tier: the tier where the current sampled contraction process stops
  producing new selected representative quotient edges.
- Degenerate tier: a one-cell top tier. The repaired run is terminal at 14
  cells, not degenerate.
- Sustained hit: a rolling 5-episode window where at least 4 episode rewards
  meet the locked threshold.
- Claim-blocked pair: a pair that cannot support speed comparison because one
  or both arms lack a sustained-hit episode.
