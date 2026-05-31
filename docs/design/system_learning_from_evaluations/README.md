# System Learning From Evaluations

This folder preserves design lessons discovered while running benchmark
evaluations.

Evaluation readouts under `docs/evaluations/` are allowed to be regenerated.
They describe the current result surface for an artifact set. This folder is
different: it is durable design memory for issues, confusions, protocol fixes,
and system-correction ideas discovered through those evaluations.

Use this area for three related kinds of learning:

1. `state_collapser` / `big_boy_benchmarking` troubleshooting discovered
   through environment runs.
2. Natural user and engineer confusion points discovered while translating raw
   artifacts into human-readable reports.
3. Documentation or architecture issues discovered during evaluation
   interpretation, even when they were not the cause of the current run's
   result.

## LLM Detection Index

Future LLM passes should scan this table first.

| Issue id | Folder | Current type | Status | Detection phrase |
| --- | --- | --- | --- | --- |
| `counterpoint_first_serious_learning_v001` | [counterpoint_first_serious_learning_v001](counterpoint_first_serious_learning_v001/README.md) | evaluation-learning archive | active design memory | structural-limit diagnostic; `pi_0(H)` collapse; first serious counterpoint learning |
| `direct_image_threshold_binding` | [direct_image_threshold_binding](direct_image_threshold_binding/README.md) | documentation issue | future work; may become architecture issue | direct-image aggregation; lower-tier thresholds bind upper-tier performance |

## Current Archives

- [Counterpoint first serious learning v001](counterpoint_first_serious_learning_v001/README.md)
- [Direct image threshold binding](direct_image_threshold_binding/README.md)

## Archive Shape

Each archived evaluation-learning thread should include:

- a short local `README.md`;
- a mostly verbatim conversation or readout archive;
- distilled issue and correction notes.

The transcript preserves attribution and exact reasoning. The notes make the
archive usable without rereading the full conversation.
