# Warehouse Gridlock Transformer Policy Model Upgrade Implementation Log

## Execution Context

Workplan:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/03_transformer_policy_model_upgrade/01_002_warehouse_gridlock_transformer_policy_model_upgrade_implementation_workplan.md
```

Blueprint:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/03_transformer_policy_model_upgrade/01_001_warehouse_gridlock_transformer_policy_model_upgrade_blueprint.md
```

Branch:

```text
codex/warehouse-gridlock-transformer-policy-model-upgrade
```

Starting commit:

```text
9eec6c0a950ad806b86088ad09536d42a355489e
```

Starting dirty state:

- `docs/protips_and_pitfalls.md` was modified before this execution and is treated as unrelated existing work.
- `docs/design/svg_physical_system_designs/warehouse_gridlock_001/03_transformer_policy_model_upgrade/` existed as untracked design work before implementation execution.

## Prime Directive Re-read

Completed before implementation edits:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`
- `docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md`
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`
- `docs/prime_directive/git_practices.md`
- transformer upgrade blueprint and workplan

## Mandatory Stop Conditions

Stop and ask the Project Owner if:

- Torch cannot be imported in the ML path and installing it requires approval;
- base package import starts requiring Torch;
- CLI help requires Torch;
- implementation would alter Warehouse environment semantics;
- implementation would alter reward constants;
- implementation would alter invalid ensemble semantics;
- direct arm receives tower-only context;
- either arm receives one-hop successor-Out lookahead;
- live-lift becomes action lookahead instead of state-lift liveness;
- existing tower surface cannot supply candidate concrete vectors;
- transformer action selection requires an abstract-action-head redesign;
- selected-trace rendering cannot be made independent of giant global CSVs;
- checkpoint load cannot reproduce deterministic inference for a fixed state;
- artifact retention cannot avoid giant all-episode traces by default;
- smoke training cannot run without simplifying the blueprint;
- tests would require a long training run;
- any action must be replaced with a smaller substitute to proceed.

## Running Phase.Stage.Action Log

### Phase 0

- Phase 0.Stage 1.Action 1: Completed. Governing documents and current Warehouse policy contract surfaces were re-read.
- Phase 0.Stage 1.Action 2: Completed. Dirty state recorded above.
- Phase 0.Stage 1.Action 3: Completed. Created and switched to `codex/warehouse-gridlock-transformer-policy-model-upgrade`.
- Phase 0.Stage 1.Action 4: Completed. This implementation log was created.
- Phase 0.Stage 1.Action 5: Completed. Stop conditions copied into this log.

### Phase 1

- Phase 1.Stage 1.Action 1: Completed. `policies/contracts.py` already provided the full system configuration, full action vector, policy decision, projection trace, and update record surfaces needed by the transformer path. No shared contract weakening was required.
- Phase 1.Stage 1.Action 2: Completed. `policies/linear_policy.py` was audited. The existing linear model family and update semantics were treated as prior baseline machinery only, not reused as the transformer learner.
- Phase 1.Stage 1.Action 3: Completed. `policies/resolver.py` was audited. The resolver remains immediate/projection based and records `successor_out_count_used_for_selection`; transformer result tables assert this remains zero.
- Phase 1.Stage 1.Action 4: Completed. `full_state_policy_comparison/runner.py` was audited. The old artifact growth mode came from all-episode step traces; the transformer path therefore uses selected traces only.
- Phase 1.Stage 1.Action 5: Completed. `masked_direct_vs_live_lift_tower/` was audited. The transformer runner reuses concrete tower candidates and live-lift state-liveness hygiene without adding one-hop action lookahead.
- Phase 1.Stage 2.Action 1: Completed. `replay.py` was audited. Transformer rendering uses a selected `trace_episode_index.csv` and passes a retained `step_events.csv` directly to the existing renderer.
- Phase 1.Stage 2.Action 2: Completed. Warehouse CLI parser/dispatch style was audited and extended under `warehouse-gridlock transformer-policy`.
- Phase 1.Stage 2.Action 3: Completed. Warehouse test style was audited. New transformer tests live at `tests/environments/warehouse_gridlock/test_transformer_policy.py` and are Torch-gated.

### Phase 2

- Phase 2.Stage 1.Action 1: Completed. `pyproject.toml` already contained the optional `ml` extra with `torch>=2.4` at execution time. `uv.lock` was updated/resolved so the lock now records the optional Torch dependency graph.
- Phase 2.Stage 1.Action 2: Completed. Before installing Torch, these checks passed without Torch:
  - `uv run python -c "import big_boy_benchmarking; print('import ok')"`
  - `uv run python -m big_boy_benchmarking.cli warehouse-gridlock transformer-policy --help`
  - transformer tests reported `2 passed, 2 skipped`.
- Phase 2.Stage 1.Action 3: Completed. Added `transformer_policy/torch_runtime.py` with availability detection, runtime manifest data, and a clear `TorchUnavailableError`.
- Phase 2.Stage 1.Action 4: Completed. Added tests for help without Torch, missing-Torch failure, Torch-gated forward pass, and Torch-gated smoke execution.
- Stop condition encountered and resolved: Torch was initially unavailable. Approval was requested to install the optional ML extra, then `uv sync --extra ml --group dev` installed `torch==2.12.0` and supporting packages.

### Phase 3

- Phase 3.Stage 1.Action 1: Completed. Created the real transformer package:
  - `__init__.py`
  - `action_selection.py`
  - `aggregation.py`
  - `checkpoints.py`
  - `config.py`
  - `docs_writer.py`
  - `encoding.py`
  - `manifests.py`
  - `model.py`
  - `paths.py`
  - `runner.py`
  - `torch_runtime.py`
  - `trace_retention.py`
  - `training.py`
- Phase 3.Stage 1.Action 2: Completed. Added transformer evaluation, model-family, tower-arm, and direct-arm IDs in the transformer config surface.
- Phase 3.Stage 1.Action 3: Completed. Added path helpers for repo readout surface, artifact root, result tables, checkpoints, selected traces, and movies.
- Phase 3.Stage 1.Action 4: Completed. Added config dataclasses for model, optimizer, curriculum, checkpoints, trace retention, and run configuration.
- Phase 3.Stage 1.Action 5: Completed. Config dataclasses expose stable manifest serialization.

### Phase 4

- Phase 4.Stage 1.Action 1: Completed. Added token types for global, robot, box, blocked-column, and tower-context tokens.
- Phase 4.Stage 1.Action 2: Completed. Encoded entity identity, position, target position, target flags, occupancy/entity type, current second, max seconds, and remaining seconds.
- Phase 4.Stage 1.Action 3: Completed. Encoded arm context while keeping direct-arm context free of tower-only information.
- Phase 4.Stage 1.Action 4: Completed. Encoded tower context fields available before action selection: tier, state-cell ID hash, live-lift out count, and candidate count. No successor-Out action lookahead is encoded.
- Phase 4.Stage 1.Action 5: Completed. Added batch collation returning tensors plus robot/action metadata.
- Phase 4.Stage 1.Action 6: Completed. Encoding/forward shape coverage is included in the Torch-gated transformer tests.

### Phase 5

- Phase 5.Stage 1.Action 1: Completed. Implemented `WarehouseTransformerActorCritic`.
- Phase 5.Stage 1.Action 2: Completed. Implemented `WarehouseTransformerOutput`.
- Phase 5.Stage 1.Action 3: Completed. Implemented model factory and parameter counting for manifests.
- Phase 5.Stage 1.Action 4: Completed. Added CPU default and runtime/device manifest recording. CUDA is optional and not silently required.
- Phase 5.Stage 1.Action 5: Completed. Torch-backed forward-pass test passed after installing the ML extra.

### Phase 6

- Phase 6.Stage 1.Action 1: Completed. Implemented direct action adapter for future direct transformer runs.
- Phase 6.Stage 1.Action 2: Completed. Implemented tower candidate scoring adapter over concrete candidate vectors.
- Phase 6.Stage 1.Action 3: Completed. Added log-probability, entropy, and value plumbing for actor-critic training.
- Phase 6.Stage 1.Action 4: Completed. The resolver summary records `successor_out_count_used_for_selection_count`; smoke readout criteria expect zero.
- Phase 6.Stage 1.Action 5: Completed. Action selection is exercised by Torch-gated smoke and runner tests.

### Phase 7

- Phase 7.Stage 1.Action 1: Completed. Added episodic rollout buffer.
- Phase 7.Stage 1.Action 2: Completed. Added discounted return and advantage computation.
- Phase 7.Stage 1.Action 3: Completed. Added actor-critic policy, value, and entropy loss components.
- Phase 7.Stage 1.Action 4: Completed. Added AdamW optimizer step, gradient clipping, and `optimizer_steps` incrementing.
- Phase 7.Stage 1.Action 5: Completed. Transformer progress and tables use `optimizer_steps`, not ambiguous `updates`.
- Phase 7.Stage 1.Action 6: Completed. Smoke showed real optimizer progress: `optimizer_steps=2` after two episodes.

### Phase 8

- Phase 8.Stage 1.Action 1: Completed. Added curriculum schedule from configurable start/end max seconds over a configurable ramp.
- Phase 8.Stage 1.Action 2: Completed. Added `curriculum_manifest.json` and `results/curriculum_summary.csv`.
- Phase 8.Stage 1.Action 3: Completed. Runner uses episode-specific curriculum max seconds.
- Phase 8.Stage 1.Action 4: Completed. Curriculum behavior is exercised in smoke and summary tables.

### Phase 9

- Phase 9.Stage 1.Action 1: Completed. Added checkpoint save with model state, optimizer state, run config, episode index, optimizer step count, reason, and rolling reward.
- Phase 9.Stage 1.Action 2: Completed. Added checkpoint load helper for inference-compatible model reconstruction. Full training resume remains future work, but the checkpoint format keeps model/optimizer/config data.
- Phase 9.Stage 1.Action 3: Completed. Added periodic, final, and best rolling reward checkpointing plus retention helpers.
- Phase 9.Stage 1.Action 4: Completed. Added `checkpoint_manifest.json` and `results/checkpoint_summary.csv`.
- Phase 9.Stage 1.Action 5: Partially completed. Smoke verified checkpoint writing and manifest rows. A dedicated before/after deterministic checkpoint-load test remains recommended before treating checkpoint resume/inference as production-grade.

### Phase 10

- Phase 10.Stage 1.Action 1: Completed. Added trace retention config supporting explicit indices, `final`, and periodic trace retention.
- Phase 10.Stage 1.Action 2: Completed. Selected traces are written under per-episode trace folders only.
- Phase 10.Stage 1.Action 3: Completed. Added `results/trace_episode_index.csv`.
- Phase 10.Stage 1.Action 4: Completed. Missing trace requests now return structured CLI errors with artifact root, available episodes, and rerun hints.
- Phase 10.Stage 1.Action 5: Completed. Transformer render command uses selected trace index and does not require global all-episode step events.
- Phase 10.Stage 1.Action 6: Completed. Added artifact size guard.
- Phase 10.Stage 1.Action 7: Completed. Added `artifact_retention_manifest.json` and `results/artifact_retention_summary.csv`.
- Phase 10.Stage 1.Action 8: Completed for smoke. Rendered retained episode 0 successfully; unretained episode 2 returned a clean `missing_renderable_trace` JSON error.

### Phase 11

- Phase 11.Stage 1.Action 1: Completed. Implemented tower-only transformer curriculum runner.
- Phase 11.Stage 1.Action 2: Completed. Implemented direct transformer action path for future paired comparison use, although first default run remains tower-only.
- Phase 11.Stage 1.Action 3: Completed. Added CLI commands:
  - `warehouse-gridlock transformer-policy run`
  - `warehouse-gridlock transformer-policy summarize`
  - `warehouse-gridlock transformer-policy render-episode`
- Phase 11.Stage 1.Action 4: Completed. Added required run flags for repo/artifact roots, readiness source, run label, budget, curriculum, checkpointing, tracing, progress, seed, and device.
- Phase 11.Stage 1.Action 5: Completed. Summarize writes repo readout files and `readout_source.json` without rerunning training.
- Phase 11.Stage 1.Action 6: Completed. Render command reports output path and fails clearly for missing selected traces.
- Phase 11.Stage 1.Action 7: Completed. Progress postfix begins with `reward=... rolling=... optimizer_steps=...`.
- Phase 11.Stage 1.Action 8: Completed. CLI tests pass with Torch installed: `3 passed, 1 skipped`.

### Phase 12

- Phase 12.Stage 1.Action 1: Completed. Added `evaluation_manifest.json`.
- Phase 12.Stage 1.Action 2: Completed. Added `dependency_manifest.json` with Torch runtime data.
- Phase 12.Stage 1.Action 3: Completed. Added model and optimizer manifests.
- Phase 12.Stage 1.Action 4: Completed. Added policy contract manifest documenting full-state/full-action, immediate masking, no one-hop lookahead, and live-lift state-liveness boundaries.
- Phase 12.Stage 1.Action 5: Completed. Added required result tables under `results/`.
- Phase 12.Stage 1.Action 6: Completed. Added compact `run_index.csv`.

### Phase 13

- Phase 13.Stage 1.Action 1: Completed. Added docs writer for `docs/evaluations/warehouse_gridlock_001/transformer_policy/readout_source.json`.
- Phase 13.Stage 1.Action 2: Completed. Preserved the correct protocol invocation:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/transformer_policy/readout_source.json
```

- Phase 13.Stage 1.Action 3: Completed. Readout source exposes model type, optimizer status, reward trajectory sources, checkpoint availability, retained trace index, artifact retention status, no-lookahead goal criteria, live-lift table source, and claim boundary.
- Phase 13.Stage 1.Action 4: Completed. Summarize/readout source existence is covered by transformer tests and smoke verification.

### Phase 14

- Phase 14.Stage 1.Action 1: Completed. Added `scripts/run_warehouse_gridlock_tower_transformer_curriculum_train.sh`.
- Phase 14.Stage 1.Action 2: Completed. Script defaults are tower-only, transformer CLI based, repo-local artifact rooted, configurable by environment variables, and selected-trace aware.
- Phase 14.Stage 1.Action 3: Completed. Script uses `set -euo pipefail`, prints artifact root/readout path, and does not default to a huge run.
- Phase 14.Stage 1.Action 4: Completed by equivalent direct CLI smoke. The script itself was not separately run because the direct smoke command exercised the same CLI with the workplan's explicit two-episode parameters.

### Phase 15

- Phase 15.Stage 1.Action 1: Completed via broader Warehouse test slice:

```text
uv run pytest tests/environments/warehouse_gridlock -q
```

Final result after Torch install:

```text
32 passed, 1 skipped in 3.47s
```

- Phase 15.Stage 1.Action 2: Completed. Transformer tests:

```text
uv run pytest tests/environments/warehouse_gridlock/test_transformer_policy.py -q
```

Before Torch install:

```text
2 passed, 2 skipped
```

After Torch install:

```text
3 passed, 1 skipped in 2.87s
```

- Phase 15.Stage 1.Action 3: Completed. CLI help checks passed:
  - `uv run python -m big_boy_benchmarking.cli --help`
  - `uv run python -m big_boy_benchmarking.cli warehouse-gridlock --help`
  - `uv run python -m big_boy_benchmarking.cli warehouse-gridlock transformer-policy --help`
  - `uv run python -m big_boy_benchmarking.cli warehouse-gridlock transformer-policy run --help`
- Phase 15.Stage 1.Action 4: Completed. Tiny tower-only smoke run succeeded:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock transformer-policy run --repo-root . --artifact-root docs/evaluations/warehouse_gridlock_001/transformer_policy/artifacts/tower_transformer_smoke_001 --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json --run-label tower_transformer_smoke_001 --locked-by foster --episodes 2 --replicates 1 --schema-seeds 1 --max-seconds-start 2 --max-seconds-end 4 --curriculum-ramp-episodes 2 --checkpoint-every-episodes 1 --trace-episode-index 0 --trace-episode-index final --progress-every-episodes 1
```

Result:

```text
{"artifact_count": 18, "status": "success", ...}
```

Progress displayed reward first and showed `optimizer_steps=2`.

- Phase 15.Stage 1.Action 5: Completed. Summarize succeeded:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock transformer-policy summarize --repo-root . --artifact-root docs/evaluations/warehouse_gridlock_001/transformer_policy/artifacts/tower_transformer_smoke_001
```

Result:

```text
{"artifact_count": 6, "status": "complete", ...}
```

- Phase 15.Stage 1.Action 6: Completed. Retained movie smoke succeeded for episode 0 and missing-trace episode 2 returned structured JSON error.
- Phase 15.Stage 1.Action 7: Completed. Broader targeted suite result recorded above.
- Phase 15.Stage 1.Action 8: Completed for new transformer code. This passed:

```text
uv run ruff check src/big_boy_benchmarking/environments/warehouse_gridlock/transformer_policy tests/environments/warehouse_gridlock/test_transformer_policy.py
```

`src/big_boy_benchmarking/cli/main.py` still fails standalone ruff with the same 27 import/line-length issues present in the `HEAD` copy before this branch. The transformer-specific lint target is clean.

### Phase 16

- Phase 16.Stage 1.Action 1: No design discussion rewrite was needed.
- Phase 16.Stage 1.Action 2: Completed. The intended human-readable protocol target is the new transformer readout source.
- Phase 16.Stage 1.Action 3: Deferred. Root README/evaluation index were not updated because this is only a two-episode smoke surface, not serious benchmark evidence.
- Phase 16.Stage 1.Action 4: No new general pitfall was added. The preexisting `docs/protips_and_pitfalls.md` modification remains unrelated user work.

### Phase 17

- Phase 17.Stage 1.Action 1: Completed. `git -C /Users/foster/state_collapser status --short` produced no output during final verification; this workplan did not edit `state_collapser`.
- Phase 17.Stage 1.Action 2: Completed. Smoke artifact root size:

```text
14M docs/evaluations/warehouse_gridlock_001/transformer_policy/artifacts/tower_transformer_smoke_001
44K docs/evaluations/warehouse_gridlock_001/transformer_policy/movies/tower_transformer_smoke_001
```

Only selected trace CSVs were written:

```text
.../traces/.../episode_000000/step_events.csv
.../traces/.../episode_000001/step_events.csv
```

Largest files are four checkpoint `.pt` files at roughly 3.4M each. No global all-episode `step_events.csv` was produced.

- Phase 17.Stage 1.Action 3: Completed. Correct protocol target:

```text
docs/evaluations/warehouse_gridlock_001/transformer_policy/readout_source.json
```

- Phase 17.Stage 1.Action 4: Completed. Final git state is on `codex/warehouse-gridlock-transformer-policy-model-upgrade`. Intentionally generated artifact root is present on disk but ignored by git. New repo readout docs/movie are untracked. `docs/protips_and_pitfalls.md` remains an unrelated modified file.
- Phase 17.Stage 1.Action 5: Completed by this log update.

## Final Status

Implementation status: complete for the first transformer policy smoke slice.

Evidence produced:

- Torch optional dependency path installed and verified: `torch==2.12.0`, CPU.
- Real transformer actor-critic optimizer steps occurred in smoke: `optimizer_steps=2`.
- Selected trace movie rendering works without a global all-episode step CSV.
- Missing selected-trace requests fail as structured JSON with a rerun hint.
- Human-readable protocol target exists:

```text
docs/evaluations/warehouse_gridlock_001/transformer_policy/readout_source.json
```

Bounded limitations:

- The smoke run is two episodes only and carries no benchmark-strength claim.
- Checkpoint save/load helpers exist, but a dedicated deterministic before/after checkpoint-load test remains recommended before relying on checkpoint inference/resume as a public contract.
- `src/big_boy_benchmarking/cli/main.py` retains preexisting ruff import/line-length debt; transformer package lint is clean.
- No long 512, 2024, or 100000 episode transformer training run was executed.
