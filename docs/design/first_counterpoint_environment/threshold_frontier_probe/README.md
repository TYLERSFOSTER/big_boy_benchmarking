# Threshold Frontier Probe Design Folder

## Status

Design folder initialized.

No blueprint exists yet.

No implementation workplan exists yet.

No runtime changes, benchmark runs, artifact writes, or report regeneration are
authorized by this README.

## Attribution Boundary

This is a consultant-authored orientation document for a future design
discussion. It must not be treated as a Project Owner turn.

The Project Owner asked for next-measure directions that could test bigger
claims after the corrected second-serious schema-comparison smoke runs. The
Project Owner then asked to create design folders for those directions.

Consultant-authored open questions in this folder are not Project Owner
answers, approvals, or decisions.

## Existing Evidence This Folder Starts From

The relevant existing evaluation line is:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison
```

The current corrected candidate-producing source is:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
```

That source points at corrected `state_collapser v0.7.2` pointwise-liftability
artifacts and exposes this eligible widened candidate:

```text
counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0
```

The corrected downstream comparison has now been rerun at small smoke budget
with:

```text
schema0 = no_contraction
schema1 = full_iterated_noisy_rate candidate
candidate_cap = 1
replicates_per_arm = 1
episodes_per_arm = 8
persistence_rule = 4_of_5
linearization_mode = tensor_available_disabled
liftability_semantics = state_collapser_v072_pointwise
```

At `R = 12.0`, both arms reached sustained hit at the same episode count, and
the comparison was unblocked.

At `R = 13.0`, both arms again reached sustained hit at the same episode count:

```text
Schema 0:
  episodes_to_sustained_hit = 5
  post_hit_window_mean = 13.368636363636364
  post_hit_window_min = 12.961363636363636
  post_hit_window_success_count = 4/5

Schema 1:
  episodes_to_sustained_hit = 5
  post_hit_window_mean = 13.550757575757576
  post_hit_window_min = 13.169696969696968
  post_hit_window_success_count = 5/5
```

This is not enough to claim that Schema 1 learns faster. It is a faint positive
signal that Schema 1 may have a reward-margin or robustness advantage near the
current threshold boundary.

## What This Folder Is For

This folder is for designing a threshold-frontier evaluation.

The basic idea is to keep the candidate, instance, schema arms, and small
budget mostly fixed while sweeping the reward threshold upward. This asks:

```text
At what reward threshold does each schema arm stop satisfying the sustained-hit
criterion?
```

The intended next-measure claim shape is not:

```text
Schema 1 is globally better.
```

The intended claim shape is closer to:

```text
Under matched seed/budget conditions for this corrected candidate, Schema 1
continues to satisfy the sustained threshold at a stricter R than Schema 0.
```

## Candidate Design Shape

A first version might sweep a small set such as:

```text
R = 13.0, 13.25, 13.5, 13.75, 14.0
```

The evaluation should probably preserve:

```text
candidate_source = docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
instance = counterpoint_symbolic_n3_wide_20_108_span18_v001
schema1_tower_source = full_iterated_noisy_rate
candidate_cap = 1
replicates_per_arm = 1
episodes_per_arm = 8
persistence_rule = 4_of_5
```

The readout should emphasize:

- sustained-hit status by threshold and schema;
- episodes-to-sustained-hit by threshold and schema;
- post-hit window mean/min/success count by threshold and schema;
- paired delta where both arms are unblocked;
- first threshold where one or both arms become blocked or non-sustained;
- liftability and invariant status at every threshold.

## Consultant-Authored Open Questions

- Should the first sweep include `R = 12.0` as a baseline row, or start at the
  current edge `R = 13.0`?
- Should thresholds be quarter-step values, half-step values, or a small
  adaptive search around the observed boundary?
- Should the first frontier probe intentionally keep the current smoke budget,
  or modestly increase episodes so stricter thresholds have time to separate?
- Should this be implemented as a new evaluation id, or as a parameterized mode
  under the second-serious schema-comparison runner?
- What badge should summarize the readout: highest shared passing threshold,
  Schema 1-only threshold margin, or frontier inconclusive?

## Next Design Artifact

The next document in this folder should be a design discussion or blueprint that
locks:

- threshold grid;
- artifact root naming;
- budget;
- success/warning/failure criteria;
- table schema;
- human-readable readout expectations;
- claim boundary.
