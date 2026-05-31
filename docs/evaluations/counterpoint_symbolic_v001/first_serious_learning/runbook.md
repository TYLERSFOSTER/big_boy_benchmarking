# Runbook

## Purpose

Regenerate the repo-resident artifact set and human-readable readout for the
counterpoint first serious learning evaluation.

## Artifact Root

The current regenerated artifact root is:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/pi0_h_evaluation_001
```

## Run Evaluation

From the repository root:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning run \
  --artifact-root /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/pi0_h_evaluation_001 \
  --instance-id small \
  --episodes 16 \
  --replicates 4 \
  --schema-seeds 3 \
  --locked-by foster \
  --linearization-mode tensor_available_disabled
```

Expected completion summary:

```json
{"run_count": 44, "status": "complete"}
```

## Summarize Evaluation

```bash
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning summarize \
  --artifact-root /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/pi0_h_evaluation_001
```

This writes machine-generated summary docs inside the artifact tree. Those docs
are evidence, not the repo-side human readout surface.

## Regenerate Human Readout

Point the artifact-table readout protocol at the repo-side source binding:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/readout_source.json
```

The protocol should use the source paths inside `readout_source.json` and write
the human-readable docs into its `repo_readout_surface`.

## Interpretation Guardrail

This is a structural-limit diagnostic evaluation. Do not summarize the result
as ordinary mixed non-performance. The non-empty tower arms are dominated by
full or near-full first-projection collapse and lift/action-realization effects.
