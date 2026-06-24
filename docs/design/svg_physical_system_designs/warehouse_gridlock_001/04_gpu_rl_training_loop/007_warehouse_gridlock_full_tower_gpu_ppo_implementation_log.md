# Warehouse Gridlock Full-Tower GPU PPO Implementation Log

## Status

Implementation in progress.

This log records execution of:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/006_warehouse_gridlock_full_tower_gpu_ppo_implementation_workplan.md
```

## Phase 0.Stage 1: Branch And Dirty-State Control

### Phase 0.Stage 1.Action 1: Verify current branch

Status: completed.

Recorded at: 2026-06-24 11:16:12 EDT.

Starting branch was:

```text
main
```

Per workplan, created and switched to:

```text
codex/warehouse-gridlock-full-tower-gpu-ppo
```

### Phase 0.Stage 1.Action 2: Inspect dirty state

Status: completed.

Initial dirty state on `main` before branch creation:

```text
clean
```

Classification:

```text
user/preexisting: none
expected generated artifact: none
current implementation target: none before this log
unknown: none
```

### Phase 0.Stage 1.Action 3: Record branch and dirty state

Status: completed by creation of this log.

Source authority list:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
docs/prime_directive/common_failure_mode_005_umbrella_workplan_fragmentation.md
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/artifact_table_to_readable_document_protocol.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_001_warehouse_gridlock_environment_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_002_warehouse_gridlock_environment_implementation_workplan.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_003_warehouse_gridlock_environment_implementation_log.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/001_design_discussion.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/002_ppo_training_surface_map.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/003_tower_traversing_logic_discussion.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/004_blueprint_decision_gates_for_full_tower_gpu_ppo.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/005_warehouse_gridlock_full_tower_gpu_ppo_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/006_warehouse_gridlock_full_tower_gpu_ppo_implementation_workplan.md
```

Known superseded environment time-semantics note:

```text
The initial environment blueprint and early workplan contain older open or
provisional language about whether invalid ensemble attempts consume one
second. That older language is superseded by the later PO decision recorded in
01_003_warehouse_gridlock_environment_implementation_log.md:

- invalid ensemble attempts do not consume one second;
- invalid ensembles self-loop without advancing time_step;
- no partial execution;
- if any part of the ensemble is invalid, no robot or box moves.
```

## Running Status Table

| Phase.Stage.Action | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Phase 0.Stage 1.Action 1 | completed | branch created | `codex/warehouse-gridlock-full-tower-gpu-ppo` |
| Phase 0.Stage 1.Action 2 | completed | `git status --short` | clean before work |
| Phase 0.Stage 1.Action 3 | completed | this log | source authority and superseded invalid-time note recorded |

## Phase 0.Stage 2: Source Authority Re-Read

### Phase 0.Stage 2.Action 1: Re-read Prime Directive files

Status: completed.

Read/checked the Prime Directive files named by the workplan, with special
attention to:

```text
implementation only after owner approval;
approved workplan is law;
no silent simplification;
Phase.Stage.Action execution discipline;
no invented Project Owner turns;
repo-side readout_source.json binding.
```

### Phase 0.Stage 2.Action 2: Re-read Warehouse Gridlock environment sources

Status: completed.

Locked mechanics recorded for implementation:

```text
16 x 16 PO drawing instance
32 robots
32 boxes
one second per valid environment transition
invalid ensemble self-loop without time advance
no partial execution
push-only box interaction
manual PO drawing manifest authority
hidden/effectively hidden admissible-state graph
```

Important conflict resolution:

```text
The older recommendation/open question that invalid ensembles might consume one
second is superseded. Implementation must use the later PO-locked rule:
invalid ensemble attempts do not advance environment time.
```

### Phase 0.Stage 2.Action 3: Re-read GPU PPO design sources

Status: completed.

Locked PPO commitments recorded for implementation:

```text
PPO does not learn tower traversal.
Direct is no-contraction schema.
There is a separate policy model per tier.
Geometry records exclude mutable episode/time/PPO facts.
The policy scores candidate actions over current Out_k(s_t).
Only pointwise executable action surfaces may reach actor sampling.
Representative fallback is forbidden for execution.
PPO ratios use stored decision surfaces.
Artifacts and readout_source.json are repo-resident by default.
Long runs retain selected traces, not exhaustive per-step dumps.
```

## Phase 0.Stage 3: Existing Code Inventory

### Phase 0.Stage 3.Action 1: Inventory Warehouse Gridlock environment code

Status: completed.

Reusable existing modules:

```text
environment state/action dataclasses:
  src/big_boy_benchmarking/environments/warehouse_gridlock/state.py
  src/big_boy_benchmarking/environments/warehouse_gridlock/actions.py

transition validation:
  src/big_boy_benchmarking/environments/warehouse_gridlock/transition.py
  src/big_boy_benchmarking/environments/warehouse_gridlock/collisions.py
  src/big_boy_benchmarking/environments/warehouse_gridlock/validation.py

reward computation:
  src/big_boy_benchmarking/environments/warehouse_gridlock/rewards.py

readiness manifests/docs:
  src/big_boy_benchmarking/environments/warehouse_gridlock/manifests.py
  src/big_boy_benchmarking/environments/warehouse_gridlock/docs_writer.py

episode replay/rendering:
  src/big_boy_benchmarking/environments/warehouse_gridlock/replay.py

existing full-state policy comparison:
  src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/

existing transformer policy code:
  src/big_boy_benchmarking/environments/warehouse_gridlock/transformer_policy/

existing live-lift/tower diagnostic scaffolding:
  src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/
```

Reuse note:

```text
The existing transformer policy is actor-critic style and useful for Torch
model, encoding, checkpoint, progress, and trace-retention patterns. It is not
itself the accepted full-tower PPO implementation because it does not preserve
stored PPO decision surfaces/old-new ratios in the accepted design form.
```

### Phase 0.Stage 3.Action 2: Inventory relevant Counterpoint and PlateSupport patterns

Status: completed.

Relevant patterns found:

```text
Counterpoint second serious comparison:
  pointwise liftability manifests, paired comparison readouts, badge/readout
  style, and readout regeneration preservation.

PlateSupport tower-star/direct-star:
  direct/no-contraction arm manifests, current executable lift surfaces,
  guarded lift tables, and use of state_collapser PartitionTower pointwise
  executability methods.

Warehouse previous diagnostics:
  repo-side readout_source.json surfaces, selected trace rendering, progress
  events, readiness source validation, and candidate generation manifests.
```

### Phase 0.Stage 3.Action 3: Verify dependency state

Status: completed.

Dependency check:

```text
state_collapser: 0.7.2
torch: 2.12.0
tqdm: 4.68.2
torch.cuda.is_available(): false on this machine
```

Runtime surface finding:

```text
The exact names ActiveTier, ControlAction, and ExploitExploreTowerRuntime are
not exposed by installed state_collapser 0.7.2. However, the required pointwise
liftability/executability surface is exposed through PartitionTower:

- current_state_cell
- current_position_at_every_tier
- outgoing_action_cells
- representative_edges
- executable_lift_candidates
- executable_action_cells
- tier_is_executable_from_state

This is the same upstream surface already used by the PlateSupport tower-star
diagnostic. Implementation may continue by building a BBB orchestration adapter
around PartitionTower. It must not clone state_collapser internals or claim the
missing named runtime objects exist upstream.
```

| Phase.Stage.Action | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Phase 0.Stage 2.Action 1 | completed | Prime Directive reread/search | execution discipline confirmed |
| Phase 0.Stage 2.Action 2 | completed | environment docs reread | later invalid-time PO decision controls |
| Phase 0.Stage 2.Action 3 | completed | GPU PPO docs reread | locked PPO commitments recorded |
| Phase 0.Stage 3.Action 1 | completed | source tree inventory | reuse points identified |
| Phase 0.Stage 3.Action 2 | completed | Counterpoint/PlateSupport pattern search | pointwise surface pattern found |
| Phase 0.Stage 3.Action 3 | completed | dependency introspection | continue via `PartitionTower`, no CUDA locally |

## Phase 1 Through Phase 9: Package, Runtime, Records, Models, PPO, Artifacts, Readout

Status: completed for the CPU-smoke implementation slice.

Implemented package:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/full_tower_gpu_ppo/
```

Files created:

```text
__init__.py
ids.py
config.py
profiles.py
paths.py
schema_arms.py
state_collapser_runtime.py
records.py
tokenization.py
models.py
policy_bank.py
gae.py
ppo.py
events.py
manifests.py
aggregation.py
docs_writer.py
runner.py
```

Consolidation note:

```text
The workplan listed separate geometry_records.py, decision_context.py, and
rollout_samples.py files. The implementation consolidates those record
contracts into records.py while preserving the behavioral contract:
geometry mutable-field rejection, nonempty pointwise decision contexts, and
rollout samples with old log probabilities and stored candidate order.
```

Implemented stable ids:

```text
evaluation_id: warehouse_gridlock_full_tower_gpu_ppo_v001
direct arm: warehouse_direct_no_contraction_full_tower_ppo
tower arm: warehouse_tower_first_nontrivial_full_tower_ppo
direct schema: schema0_no_contraction
tower schema: warehouse_source_local_ratio_009_over_010_v001
pointwise semantics: state_collapser_v072_partition_tower_pointwise_executable_liftability
```

Implemented runtime boundary:

```text
PPO does not learn tower traversal.
Direct is represented as the no-contraction schema arm.
Tower uses the Warehouse source-local outgoing-ratio schema.
The state_collapser boundary is PartitionTower plus pointwise executable
surface methods.
Actor calls only occur when a nonempty pointwise executable action surface
exists.
Execution uses strict executable lift candidates.
Representative fallback remains readout-only and is not used for execution.
```

Implemented PPO/model surface:

```text
TierCandidateActorCritic:
  context encoder;
  candidate encoder;
  candidate score head;
  value head;
  masked softmax over the current candidate action surface.

TierPolicyBank:
  separate policy_k and rollout_policy_k per tier;
  rollout_policy_k frozen during rollout collection;
  no learned parameter sharing across tiers.

PPO:
  stores old_log_prob;
  recomputes new log probability over stored candidate surfaces;
  records policy loss, value loss, entropy, approximate KL, clip fraction,
  gradient norm, sample count, and optimizer steps.
```

Implemented artifact/readout surface:

```text
docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/
```

Generated repo-side files include:

```text
README.md
readout_source.json
result_readout.md
artifact_index.md
method.md
glossary.md
runbook.md
badges/*.svg
results/summary.md
results/ppo_health.md
results/per_tier_policy.md
results/comparison.md
```

Protocol alignment:

```text
The README contains protocol-style badges, status at a glance, goal summary,
methodology summary, one-screen verdict, evidence map, non-claims, attribution,
and a safe clarification-turn section.

No Project Owner words were invented. The README attributes the Warehouse SVG
environment design and per-tier candidate-scoring PPO model family to Tyler
Foster.
```

Known implementation limitation:

```text
The CPU smoke path writes full per-step traces because they are small and
needed for replay verification. The accepted long-run design still calls for
selected-trace retention rather than exhaustive per-step dumping by default.
This smoke implementation should not be treated as the final serious-run
retention policy.
```

## Phase 10: CLI Surface

Status: completed.

CLI commands added:

```text
warehouse-gridlock full-tower-gpu-ppo inspect
warehouse-gridlock full-tower-gpu-ppo run
warehouse-gridlock full-tower-gpu-ppo summarize
warehouse-gridlock full-tower-gpu-ppo render-episode
```

Run command supports:

```text
--repo-root
--artifact-root
--readiness-source
--run-label
--locked-by
--profile
--episodes-per-arm
--replicates-per-arm
--schema-seeds
--max-seconds-per-episode
--active-arm-id
--device
--ppo-update-interval-samples
--min-tier-update-samples
--ppo-epochs
--minibatch-size
--learning-rate
--clip-epsilon
--entropy-coef
--value-coef
--target-kl
--max-grad-norm
--progress-every-episodes
--no-progress
--seed
--confirm-long-run
```

Safety gate:

```text
serious_gpu and total episode budgets above 2048 require --confirm-long-run.
```

Render command:

```text
Uses the existing Warehouse replay renderer against this evaluation's
run_index.csv and per-run step_events.csv. The smoke run rendered separate
direct and tower GIFs with different trajectory hashes.
```

## Runtime Bugs Found And Corrected During Smoke

### Hashability Of Warehouse Adapter Payloads

Initial smoke failure:

```text
TypeError: unhashable type: 'dict'
```

Cause:

```text
The existing Warehouse state_collapser adapter placed WarehouseGridlockState
and WarehouseGridlockAction objects directly in State/PrimitiveAction payloads.
Those objects contain mapping fields, so state_collapser's base registry could
not hash them.
```

Correction:

```text
The adapter now converts Warehouse states/actions to stable hashable tuple
payloads and reconstructs WarehouseGridlockState/WarehouseGridlockAction on
the way back out.
```

Affected file:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/warehouse_tower_adapter.py
```

Regression coverage:

```text
tests/environments/warehouse_gridlock/test_full_tower_gpu_ppo.py
tests/environments/warehouse_gridlock/test_masked_direct_vs_live_lift_tower.py
```

### Replay-Compatible Step Rows

Initial render failure:

```text
KeyError: 'correct_box_count'
```

Cause:

```text
The new PPO runner wrote a smaller step_events.csv schema than the shared
Warehouse replay renderer expects.
```

Correction:

```text
The PPO step_events.csv now includes the replay-compatible fields used by
existing Warehouse evaluations:
selected_action_id, selected_action_vector_hash, selected_action_summary,
correct_box_count, correct_robot_count, invalid_reasons.
```

Affected files:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/full_tower_gpu_ppo/events.py
src/big_boy_benchmarking/environments/warehouse_gridlock/full_tower_gpu_ppo/runner.py
```

## Phase 11: Tests

Status: completed.

New focused test file:

```text
tests/environments/warehouse_gridlock/test_full_tower_gpu_ppo.py
```

Coverage added:

```text
stable evaluation/arm ids;
serious_gpu confirmation gate;
Warehouse adapter hashability and round-trip reconstruction;
geometry mutable-payload rejection;
decision context nonempty pointwise-surface validation;
rollout sample masked-selection validation;
masked candidate model probabilities;
distinct frozen rollout policy objects per tier;
CLI inspect/run/summarize/render smoke path.
```

Focused command result:

```text
uv run pytest tests/environments/warehouse_gridlock/test_full_tower_gpu_ppo.py -q
9 passed
```

Warehouse command result:

```text
uv run pytest tests/environments/warehouse_gridlock -q
41 passed, 1 skipped
```

Full suite result:

```text
uv run pytest -q
343 passed, 1 skipped
```

## Phase 12: Smoke Execution And Readout Verification

Status: completed.

Inspect command:

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-tower-gpu-ppo inspect \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/artifacts/smoke_cpu_001 \
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \
  --run-label smoke_cpu_001 \
  --profile smoke_cpu
```

Inspect result:

```text
status: ok
instance_id: warehouse_gridlock_16x16_v001
state_collapser: 0.7.2
torch: 2.12.0
actual_device: cpu
```

Smoke run command:

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-tower-gpu-ppo run \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/artifacts/smoke_cpu_001 \
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \
  --run-label smoke_cpu_001 \
  --locked-by codex \
  --profile smoke_cpu \
  --episodes-per-arm 1 \
  --replicates-per-arm 1 \
  --schema-seeds 1 \
  --max-seconds-per-episode 4 \
  --progress-every-episodes 1
```

Smoke result:

```text
status: success
artifact_count: 22
episode_count: 2
optimizer_steps: 2
ppo_update_row_count: 2
empty_actor_surface_count: 0
representative_fallback_count: 0
tier_indices_seen: 0
```

Summarize command:

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-tower-gpu-ppo summarize \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/artifacts/smoke_cpu_001 \
  --run-label smoke_cpu_001
```

Summarize result:

```text
status: complete
repo-side readout_source.json regenerated
repo-side README/method/runbook/glossary/result docs regenerated
```

Rendered movies:

```text
docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/movies/smoke_cpu_001/direct_ep000.gif
docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/movies/smoke_cpu_001/tower_ep000.gif
```

Render verification:

```text
direct frame_count: 5
direct row_count: 4
tower frame_count: 5
tower row_count: 4
direct and tower trajectory hashes differ
```

Human readability protocol surface:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/readout_source.json
```

Readout verification:

```text
README has badge strip, goal summary, methodology summary, verdict, evidence
map, bounded non-claims, Project Owner attribution, and safe clarification
turn section.

No ambiguous public placeholder turns remain.
```

## Phase 13: Documentation Updates

Status: completed.

Updated:

```text
README.md
docs/evaluations/README.md
docs/evaluations/warehouse_gridlock_001/README.md
```

Bounded documentation claim:

```text
Warehouse Gridlock now has full-tower PPO mechanics/readiness smoke evidence:
direct/no-contraction and tower/nontrivial arms share PPO machinery, real PPO
updates occur, strict pointwise liftability is respected, and renderable traces
exist. This is not a serious GPU benchmark claim.
```

## Phase 14: Final Verification

Status: completed.

Static searches:

```text
Forbidden/stale-language search found only intentional "representative
fallback avoided" statements, a Prime Directive filename, and an existing
Counterpoint regression assertion.

Machine-local path search found no hits in the generated public readout files
or this implementation log.
```

Release hygiene:

```text
Initial release_hygiene run failed on older Warehouse/PlateSupport public docs
outside the new full_tower_gpu_ppo files: machine-local state_collapser/scratch
paths, raw public profanity in design conversations, and empty public turn
placeholders.

Narrow hygiene-only edits replaced machine-local paths with placeholders,
redacted public profanity as [XXX] while preserving attribution/meaning, and
replaced empty public placeholder turn pads with explicit "no active public
clarification turns" notes.

Final command:
uv run python scripts/release_hygiene.py --repo-root .

Final result:
release hygiene passed
```

Artifact size review:

```text
docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/artifacts/smoke_cpu_001
file count: 30
size: about 144K
```

Git status classification at final review:

```text
current implementation target:
  README.md
  docs/evaluations/README.md
  docs/evaluations/warehouse_gridlock_001/README.md
  docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/
  docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/007_warehouse_gridlock_full_tower_gpu_ppo_implementation_log.md
  src/big_boy_benchmarking/cli/main.py
  src/big_boy_benchmarking/environments/warehouse_gridlock/full_tower_gpu_ppo/
  src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/warehouse_tower_adapter.py
  tests/environments/warehouse_gridlock/test_full_tower_gpu_ppo.py

user/preexisting: none observed
unknown: none observed
```

## Completion Status

Status: completed for the requested implementation workplan's smoke/readiness
scope.

Completion criteria satisfied:

```text
1. Full-tower GPU PPO package exists.
2. Direct/no-contraction and tower/nontrivial arms use the same PPO machinery.
3. PPO does not learn tower traversal.
4. Per-tier policy_k and rollout_policy_k exist and are artifacted.
5. PPO samples store old_log_prob and candidate order.
6. PPO updates recompute new_log_prob over stored encoded surfaces.
7. Geometry payload checks reject mutable episode/time/PPO fields.
8. Pointwise executable action surfaces are nonempty before actor calls.
9. Representative fallback is not used for execution.
10. Controller events and PPO samples are distinct tables/records.
11. Warehouse time semantics remain controlled by the existing transition path.
12. Smoke run produces real optimizer updates.
13. Summarize produces repo-side readout_source.json and docs.
14. Selected episode rendering works for direct and tower smoke runs.
15. Focused, Warehouse, and full repo tests pass.
16. This implementation log records completed work and limitations.
```

Remaining bounded limitation:

```text
The serious GPU training-retention path still needs Project Owner-initiated
long-run validation. This implementation proves mechanics on CPU smoke; it
does not claim serious training performance.
```
