# Issue And Next Tests

## Current Observation

The one-third schema tower diagnostics evaluation collapses all visible state structure at tier 1 for both configured instances:

- small instance: `108 -> 1 -> 1 -> 1`
- medium instance: `228 -> 1 -> 1 -> 1`

The no-contraction control over the same environment does not collapse:

- small control: `[108]`
- medium control: `[228]`

This makes the result informative but suspicious. It is not currently evidence that counterpoint has no useful structure, and it should not be summarized as a learning comparison.

## Evidence From The Generated Artifacts

The current one-third schema assigns a very broad first contraction block:

- small instance: block 0 has 408 edges, with all 108 states represented as sources.
- medium instance: block 0 has 980 edges, with all 228 states represented as sources.

Under the currently observed endpoint-coalescence behavior, a full collapse of `N` states can be achieved by only `N - 1` useful coalescences. That makes a broad block large enough to act like a near-total coalescence mechanism, even if many edges are redundant.

Observed processed-edge counts before full collapse were close to the total block width:

- small seed 0: 394 processed before full collapse
- small seed 1: 407 processed before full collapse
- small seed 2: 402 processed before full collapse
- medium seed 0: 968 processed before full collapse
- medium seed 1: 960 processed before full collapse
- medium seed 2: 932 processed before full collapse

The immediate implication is that the one-third schema may be far too broad for the semantic claim we wanted to test.

## Known Readout Bug

The one-third diagnostics readout has a separate reporting issue for action-cell counts. The helper currently counts historical/stale action cells in `edge_ids_by_action_cell`, including cells no longer attached to active outgoing collections after collapse.

The active action-cell count at collapsed tiers appears to be `0`, while the readout reports large raw counts. This reporting bug should be fixed before using action-cell counts as evidence.

This does not currently explain the state collapse itself.

## Language Discipline

Use this language unless later evidence changes it:

- "coset"
- "Young-tableaux/coset semantics"
- "endpoint coalescence under the current implementation"
- "schema-width diagnostic"
- "unexpected singleton collapse"

Avoid this language unless precisely justified:

- "pi_0"
- "connected components"
- "passes to components"
- "the environment is degenerate"
- "the one-third projection proves learning will fail"

## Next Diagnostic Tests

1. Build a minimal upstream litmus test in `state_collapser` terms: if one contraction block contains `A -> B` and `B -> C`, determine whether current semantics force `A`, `B`, and `C` into one coset-like state, and whether that matches the intended `logHRL_w_comments.tex` semantics.

2. Build a BBB schema-width sweep on the counterpoint environment:
   - one edge only;
   - one edge per source;
   - one source star;
   - small fixed `k` edges;
   - current one-third block;
   - controlled variants between fixed `k` and current one-third width.

3. Add explicit metrics to the one-third diagnostic readout:
   - block edge count;
   - block edge count divided by `state_count - 1`;
   - source count represented in block;
   - useful coalescence count;
   - processed edges until first singleton tier;
   - active action-cell count, not stale historical count;
   - coset-size distribution if available.

4. Preserve PO attribution in the design archive:
   - PO identified the one-third collapse as suspicious rather than a negative result.
   - PO corrected the language away from casual connected-components claims.
   - PO tied the issue back to `state_collapser`'s `logHRL_w_comments.tex` coset/Young-tableaux motivation.

## Current Working Interpretation

The most likely immediate issue is not the counterpoint environment. The environment enumeration and no-contraction control appear sane. The likely issue is one of:

- BBB generated a one-third schema block that is too wide for the intended diagnostic;
- BBB is integrating with contraction semantics that are broader than the intended coset-preserving operation;
- upstream `state_collapser` behavior is correct for its current contract, but the BBB evaluation is asking the wrong question with the current schema shape;
- the human-readable readout underreports the distinction between "schema collapsed everything" and "environment has no structure."

This folder exists so the next design pass starts from that narrowed diagnostic frame.

