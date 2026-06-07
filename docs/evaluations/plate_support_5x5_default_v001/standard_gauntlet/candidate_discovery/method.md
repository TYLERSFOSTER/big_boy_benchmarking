# PlateSupport Candidate Discovery Method

Candidate discovery consumes Stage 2 summary tables, classifies every
schema signal row, assigns deterministic candidate IDs, and emits
downstream training-health input rows only for selected training
candidates.

Candidate rows preserve schema construction metadata such as
`schema_mode`, ratio numerator/denominator, max iterations, selector
rule, selection mode, max depth, and nontrivial tier count. Later
stages must consume this metadata directly instead of reverse
engineering schema semantics from `schema_id`.
