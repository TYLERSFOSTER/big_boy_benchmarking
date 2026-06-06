# Small Paired Replicate Probe Design Folder

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

The corrected comparison now uses:

```text
state_collapser v0.7.2 pointwise liftability semantics
```

The corrected candidate-producing source is:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/readout_source.json
```

The current candidate is:

```text
counterpoint_symbolic_n3_wide_20_108_span18_v001-p001_over_018-schema0
```

The corrected smoke comparisons at `R = 12.0` and `R = 13.0` are both
unblocked. The `R = 13.0` run produced:

```text
Schema 0:
  hit_status = sustained_hit
  episodes_to_sustained_hit = 5
  post_hit_window_success_count = 4/5

Schema 1:
  hit_status = sustained_hit
  episodes_to_sustained_hit = 5
  post_hit_window_success_count = 5/5
  concrete_step_count = 64
  lift_success_count = 64
  lift_failure rows = 0
```

That is a faint positive signal for Schema 1 reward robustness, but it is based
on one candidate and one matched seed pair. It is not yet evidence of stable
performance improvement.

## What This Folder Is For

This folder is for designing a small paired-replicate evaluation.

The basic idea is to choose one threshold near the current interesting boundary
and run more matched seed pairs. This asks:

```text
Does the slight Schema 1 reward-margin signal survive across paired seeds?
```

The intended next-measure claim shape is not:

```text
Schema 1 wins in general.
```

The intended claim shape is closer to:

```text
For this corrected widened candidate and locked threshold, Schema 1 shows a
stable paired advantage/disadvantage/no-difference pattern across a small set of
matched seed bundles.
```

## Candidate Design Shape

A first version might use:

```text
threshold_value = 13.0 or 13.5
candidate_cap = 1
replicates_per_arm = 8 or 16
episodes_per_arm = 16 or 32
persistence_rule = 4_of_5
schema1_tower_source = full_iterated_noisy_rate
```

The evaluation should preserve matched seed bundles so each Schema 0 run has a
paired Schema 1 run under the same seed conditions.

The readout should emphasize:

- paired episodes-to-hit delta distribution;
- paired post-hit window mean/min delta distribution;
- paired sustained-hit success/failure counts;
- number of pairs where Schema 1 is faster, slower, same, or blocked;
- number of pairs where Schema 1 has a higher post-hit margin;
- lift success/failure counts by tier and schema;
- warning if any pair is blocked by artifact incompleteness or liftability.

## Consultant-Authored Open Questions

- Should the replicate probe use `R = 13.0`, where both arms already pass, or
  wait for the threshold-frontier probe to identify a sharper boundary such as
  `R = 13.5`?
- Should the first replicate count be `8` for a quick check or `16` for a less
  twitchy signal?
- Should episode budget remain close to smoke budget, or increase enough that
  later threshold hits can be observed?
- Should this remain one candidate only, or include a small fixed candidate set
  if more eligible candidates are produced later?
- Should the readout badge summarize median paired delta, Schema 1 margin wins,
  or sustained-hit rate difference?

## Next Design Artifact

The next document in this folder should be a design discussion or blueprint that
locks:

- chosen threshold;
- replicate count;
- episode budget;
- seed-bundle policy;
- artifact root naming;
- table schema;
- paired summary statistics;
- human-readable readout expectations;
- claim boundary.
