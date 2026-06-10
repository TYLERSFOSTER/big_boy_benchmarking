# Tower Construction Readout

The tower arm used a scoped generated/discovered surface.

At each step, BBB generated a bounded candidate set, queried Warehouse transitions, kept valid immediate edges, and constructed a small runtime tower surface. This is not a complete tower over the full Warehouse MDP.

Key facts:

- schema id: `warehouse_source_local_ratio_iterated_v001`;
- ratio: `9/10`;
- max iterations: `1`;
- tier count: `2`;
- surface scope: `generated_discovered_surface`;
- full action surface complete: `False`;
- mean selected lift out-count: `19.92041015625`;
- live-lift failure count: `0`.

Tier convention in this readout: tier 0 is the generated lower/concrete-like surface for the current step; tier 1 is the coarser generated tower surface used by the tower controller. The runtime representation has one state cell per tier for the fixed current downstairs state, with action cells summarizing valid generated action structure.
