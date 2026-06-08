# Documentation Map

This folder is the public documentation surface for `big_boy_benchmarking`.

The current public beta component is:

```text
Big Boy Calibration / Smoke
```

The future larger component is:

```text
Benchmarking
```

## Workflow

BBB uses a three-step workflow:

1. Construct an environment.
2. Construct evaluations or gauntlets for that environment.
3. Process run artifacts into repo-side human-readable readouts.

The corresponding protocol surfaces are:

- `prime_directive/environment_construction_for_benchmark_evaluations_protocol.md`
- `prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`
- `prime_directive/artifact_table_to_readable_document_protocol.md`

## Folders

| Folder | Purpose |
| --- | --- |
| `prime_directive/` | Operating protocols for Codex/engineer collaboration, including readout generation and attribution discipline. |
| `design/` | Open-lab design history, design discussions, blueprints, Phase.Stage.Action workplans, and implementation logs. |
| `environments/` | Human descriptions of environment families, fixtures, readiness surfaces, and claim boundaries. |
| `evaluations/` | Repo-side human-readable evaluation reports grounded in machine-readable artifact tables. |
| `methods/` | Benchmark contracts, metric/mode/timing notes, and statistical method notes. |
| `results/` | Promoted durable result summaries when a result is intentionally recorded beyond an evaluation-local readout. |
| `engineer_continuity/` | Session reports, pause notes, and handoff records. |

## Open-Lab Note

Design and continuity docs preserve live engineering reasoning, corrections,
and PO/Codex attribution. They are public engineering memory, not polished
papers. Public release hygiene should make them navigable and safe to quote
without rewriting the history of what happened.

## Main Entry Points

- [Environment index](environments/README.md)
- [Evaluation index](evaluations/README.md)
- [System learning from evaluations](design/system_learning_from_evaluations/README.md)
- [Beta public release design](design/beta_public_release/README.md)
- [Beta artifact bundle manifest](design/beta_public_release/release_asset_manifests/ARTIFACT_BUNDLE_MANIFEST.json)
