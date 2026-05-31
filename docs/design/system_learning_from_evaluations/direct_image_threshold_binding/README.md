# Direct Image Threshold Binding - Documentation Issue

## Status

Documentation issue for now. This may become an architecture issue later.

## Why This Exists

This note records a future engineering concern raised while interpreting the
counterpoint first serious learning evaluation.

That evaluation did not fail because of direct-image reward aggregation. Its
observed pathology was full or near-full first-projection quotient collapse
plus lift/action-realization behavior.

However, direct-image aggregation will matter for later tower evaluations. If a
quotient tier uses a reward/value threshold for admissibility, lifting,
pruning, training, or controller selection, then the aggregation rule can make
lower/refinement-tier thresholds bind upper/coarser-tier performance.

## Core Issue

A direct-image reward or value rule is not just a reporting detail. It changes
what a coarse tier is allowed to believe about the fine/refinement tier below
it.

Examples:

- A `max` aggregator can make a threshold mean: there exists at least one good
  refinement in this fiber.
- A `mean` or conditional-expectation aggregator can make a threshold mean:
  the typical refinement in this fiber is good enough.
- A softmax, order-`p`, or risk-sensitive aggregator can create intermediate
  gates between existence and typicality.

Those choices can impose effective ceilings or feasibility constraints on the
whole tower. A coarse policy may look weak, strong, blocked, or safe depending
on how lower-tier rewards are aggregated upward.

## Explanation Device: Binary Search

Future LLMs and engineers should use binary search as the default explanation
device for this issue.

Almost every conceptual problem here already occurs in binary search in a form
early CS students have to confront:

- a coarse decision is only useful if it preserves the right refinement;
- a threshold can discard the correct half of the search space or accidentally
  discard the answer;
- the meaning of "promising" depends on the summary statistic used to choose a
  branch;
- a local decision made at a coarse level can bind everything that happens
  below it;
- correctness requires knowing what information the coarse test preserves and
  what information it throws away.

The tower setting is a modified version of that lesson. Instead of asking
"which half of a sorted list contains the target?", a quotient tier asks "which
fiber/refinement region is worth pursuing?" The direct-image aggregation rule
is part of the answer. A `max` rule says that the fiber is promising if some
refinement is good; a `mean` rule says that the fiber is promising only if the
typical refinement is good. That choice changes which branches survive.

This analogy should be used to keep future documentation concrete. The issue is
not mystical hierarchy behavior. It is the familiar problem of making a coarse
search decision with a lossy summary of the finer search space.

## Documentation Work Needed

Future docs should explain:

- what direct-image aggregation rule is used for a run;
- whether thresholds are evaluated by best-case, average-case, soft, or
  risk-sensitive fiber summaries;
- whether an upper tier is being trained on existence of a good lift or typical
  quality of lifts;
- how aggregation choices affect claims about upper-tier learner performance;
- when a result is a reward-interface design result rather than a learner
  performance result.

## Related Files

State-collapser commented research draft:

```text
/Users/foster/state_collapser/docs/design/logHRL_w_comments.tex
```

BBB generated evaluation archive that prompted the issue:

```text
docs/design/system_learning_from_evaluations/counterpoint_first_serious_learning_v001/
```

## Claim Boundary

This issue should not be used to reinterpret the completed
`counterpoint_first_serious_learning_v001` result as a direct-image reward
aggregation failure. It is a forward-looking documentation issue discovered
while interpreting that result.
