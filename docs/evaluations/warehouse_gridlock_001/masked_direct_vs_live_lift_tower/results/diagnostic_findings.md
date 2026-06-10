# Diagnostic Findings

## Fairness Checks

Both arms used immediate candidate-set masking. Each arm considered `524288` generated candidates, retained `40797`, and rejected `483491` as inadmissible. Both arms had zero selected invalid concrete moves.

## No-Lookahead Check

Both arms selected `2048` steps. Both arms had `successor_out_count_used_for_selection_count=0`. Successor `Out` was observed only after selection for diagnostics.

## Candidate Surface

The generated proposal surface included:

- all-stay candidates;
- one-active robot candidates;
- two-active robot candidates;
- three-active robot candidates;
- multi-active robot candidates through active count 8.

This means the run is not the old one-active-only smoke surface. It can be used as a small pilot for coordinated-gridlock discovery.

## Tower Surface

The tower arm had `2048` live lift candidates and zero dead lift candidates. The mean selected lift out-count was `19.92041015625`.

The tower surface was scoped and generated. It was not a full Warehouse MDP tower. The table `tower_shape_summary.csv` reports two tiers per step, one state cell per tier in this runtime representation, and `complete_full_action_surface=False`.

## Behavioral Limit

Neither arm reached terminal success and neither arm achieved box-target progress. This blocks any tower-performance claim from this run.
