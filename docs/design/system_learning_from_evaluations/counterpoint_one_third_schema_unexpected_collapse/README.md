# Counterpoint One-Third Schema Unexpected Collapse

This folder preserves durable design memory from the one-third schema tower diagnostics evaluation. The evaluation readout itself is a regenerable artifact surface; this folder is where the confusion, PO corrections, current hypotheses, and next engineering questions should survive regeneration.

## Source Evaluation

- Generated/readout surface: `docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/README.md`
- Design discussion: `docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/design_discussion.md`
- Blueprint: `docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/01_001_counterpoint_one_third_schema_tower_diagnostics_blueprint.md`
- Workplan: `docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/01_002_counterpoint_one_third_schema_tower_diagnostics_implementation_workplan.md`

## Why This Exists

The one-third schema diagnostic unexpectedly collapsed the counterpoint tower to a singleton after the first contraction tier:

- small instance: `108 -> 1 -> 1 -> 1`
- medium instance: `228 -> 1 -> 1 -> 1`

PO identified this as a suspicious diagnostic issue, not as an immediate negative result about counterpoint learning. The important question is whether the diagnostic schema, BBB integration layer, or upstream contraction semantics are collapsing far more structure than the intended one-third projection should collapse.

Current status: unresolved, with a smoke-verified follow-up diagnostic now implemented. The n-over-18 contraction fraction sweep machinery exists and produced a repo-resident smoke readout showing that the small fixture still reaches first-tier singleton collapse at `1/18`. That smoke result is diagnostic evidence, not a final full validation result and not a learning-performance claim.

## PO-Originated Corrections To Preserve

- Do not casually describe the object as `pi_0`, connected components, or "passing to connected components" unless that is exactly what the code and math are doing.
- The PO-corrected language for the intended object is `coset`, with the relevant background in the `state_collapser` `logHRL_w_comments.tex` discussion of Young-tableaux/coset data.
- The apparent failure mode may be a schema-width issue: a broad one-third block can become an effective complete-collapse mechanism under endpoint-coalescence semantics.
- The right next framing is diagnostic, not comparative learning. This evaluation should help locate where BBB/state_collapser integration semantics diverge from the intended contraction story.

## Local Notes

- [Issue And Next Tests](01_issue_and_next_tests.md)
- [Readout Conversation Archive](02_readout_conversation_archive.md)
- [n-over-18 Contraction Fraction Sweep Blueprint](03_n_over_18_contraction_fraction_sweep_blueprint.md)
- [n-over-18 Contraction Fraction Sweep Implementation Workplan](04_n_over_18_contraction_fraction_sweep_implementation_workplan.md)
- [n-over-18 Contraction Fraction Sweep Implementation Log](05_n_over_18_contraction_fraction_sweep_implementation_log.md)
- Smoke readout surface: `docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/README.md`
- Smoke artifact root: `docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/artifacts/smoke_001/`

## Current Follow-Up Decision

The next unresolved decision is whether to authorize the full small+medium validation run from the implementation workplan:

```text
docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/artifacts/small_medium_validation_001/
```

Until that run is explicitly authorized and completed, the current readout should be treated as smoke-verified implementation evidence plus an early warning that collapse may already occur at the weakest requested fraction.
