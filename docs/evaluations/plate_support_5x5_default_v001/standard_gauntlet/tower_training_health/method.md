# PlateSupport Tower Training Health Method

Stage 4 consumes Stage 3 selected candidates, rebuilds their tower
schemas, selects executable action cells from the deepest currently
executable tier, resolves them to concrete PlateSupport actions, and
applies a tabular Q update. The stage records training health evidence,
not comparison evidence.

The schema factory is metadata-first. One-shot
`source_local_ratio` candidates rebuild the one-block catch schema;
iterated `source_local_ratio_iterated` candidates rebuild the
multi-block iterated schema using the preserved ratio, selector,
selection mode, and max-iteration fields from Stage 3.
