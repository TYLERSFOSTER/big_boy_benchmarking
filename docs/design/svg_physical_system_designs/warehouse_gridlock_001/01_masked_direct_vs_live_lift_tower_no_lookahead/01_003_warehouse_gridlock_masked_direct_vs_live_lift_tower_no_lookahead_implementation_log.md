# Warehouse Gridlock Masked Direct vs Live-Lift Tower No-Lookahead Implementation Log

## Status

Execution in progress.

This log records execution of:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_masked_direct_vs_live_lift_tower_no_lookahead/01_002_warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_implementation_workplan.md
```

## Phase 0: Execution Setup And Reality Binding

### Phase 0.Stage 1.Action 1: Check branch and dirty state

Status: complete.

Observed branch state:

```text
## main...origin/main [ahead 1]
```

Observed staged state:

```text
no staged files
```

Notes:

- Execution began from `main`, ahead of `origin/main` by one local commit.
- No staged files were present before branch creation.
- The Warehouse Gridlock masked/direct live-lift design folder already existed.

### Phase 0.Stage 1.Action 2: Create or switch to the implementation branch

Status: complete.

Created and switched to:

```text
codex/warehouse-gridlock-masked-direct-live-lift
```

Post-branch status:

```text
## codex/warehouse-gridlock-masked-direct-live-lift
```

### Phase 0.Stage 1.Action 3: Confirm no accidental staged artifacts

Status: complete.

`git diff --cached --name-status` returned no staged files.

### Phase 0.Stage 2.Action 1: Re-read the active blueprint

Status: complete.

Re-read:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_masked_direct_vs_live_lift_tower_no_lookahead/01_001_warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_blueprint.md
```

Carried forward locks:

- active environment is Warehouse Gridlock 001;
- active arms are `warehouse_direct_admissible_masked` and
  `warehouse_tower_live_lift_masked`;
- both arms use immediate inadmissibility masking over generated candidate
  sets;
- neither arm uses one-step successor-state cul-de-sac lookahead;
- tower live lifting is state-lift hygiene only;
- candidate generation is a fairness surface for both arms.

### Phase 0.Stage 2.Action 2: Re-read Warehouse environment authority

Status: complete.

Checked source and readiness context:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_001_warehouse_gridlock_environment_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_003_warehouse_gridlock_environment_implementation_log.md
docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json
src/big_boy_benchmarking/environments/warehouse_gridlock/transition.py
tests/environments/warehouse_gridlock/test_warehouse_gridlock_transition.py
```

Confirmed mechanics:

- valid ensemble transitions advance time by one second;
- invalid ensemble transitions self-loop;
- invalid ensemble transitions do not advance time;
- invalid ensemble transitions do not partially execute;
- existing tests cover this unusual invalid-action time rule.

### Phase 0.Stage 2.Action 3: Re-read prior tower patterns

Status: complete.

Checked prior implementation patterns:

```text
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/training_surfaces.py
```

Reusable patterns:

- explicit environment-to-`state_collapser` `State`/`PrimitiveAction`/`BaseEdge`
  conversion;
- event-level distinction between tower action candidates and executable
  concrete lifts;
- evaluation-level tower shape and lift summaries.

Warehouse-specific correction:

- Counterpoint's finite full-graph assumption cannot be reused.
- Warehouse must build a scoped tower surface over generated/discovered states,
  generated candidates, and valid observed/immediate-query edges.

### Phase 0.Stage 3.Action 1: Verify `state_collapser` dependency state

Status: complete.

Observed dependency state:

```text
import_version: 0.7.2
inspection_status: ok
tower_partition_method_status: ok
```

Important consequence:

- v0.7.2-compatible pointwise liftability semantics are available.

### Phase 0.Stage 3.Action 2: Verify Warehouse transition query semantics

Status: complete.

The existing `step(...)` function returns validity, invalid reasons, reward,
and a next state without mutating the caller's state object. This is sufficient
for immediate-admissibility query semantics.

### Phase 0.Stage 3.Action 3: Lock smoke defaults

Status: complete.

The implementation will define smoke defaults as configuration values and keep
them CLI-overridable.

Implemented defaults:

```text
run_label: smoke_001
episodes_per_arm: 2
replicates_per_arm: 1
max_seconds_per_episode: 32
candidate_proposals_per_step: 64
schema_seeds: 1
```

## Phase 1 Through Phase 10: Implementation Summary

Status: complete.

Implemented package:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/
```

Implemented modules:

```text
__init__.py
admissibility.py
aggregation.py
arms.py
candidate_generation.py
config.py
docs_writer.py
events.py
manifests.py
paths.py
readiness_source.py
runner.py
tower_surface.py
warehouse_tower_adapter.py
```

Implemented CLI:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock masked-direct-vs-live-lift-tower run
uv run python -m big_boy_benchmarking.cli warehouse-gridlock masked-direct-vs-live-lift-tower summarize
```

Implemented active arms:

```text
warehouse_direct_admissible_masked
warehouse_tower_live_lift_masked
```

Implemented fairness boundary:

- both arms receive immediate inadmissibility masks over generated candidate
  sets;
- neither arm uses successor-state `Out` for action selection;
- tower uses live state-lift hygiene over a scoped generated/discovered
  surface;
- the full `5^32` action surface is not enumerated;
- masks are reported as `candidate_set`, not full action-space masks.

Implemented tower-construction surface:

- Warehouse states are mapped to `state_collapser.core.state.State`;
- generated Warehouse actions are mapped to
  `state_collapser.core.action.PrimitiveAction`;
- valid generated transitions are mapped to `state_collapser.core.edges.BaseEdge`;
- a scoped `HiddenGraph` wrapper exists over the generated/discovered surface;
- the first runtime tower surface is a BBB-side generated/discovered tower
  surface, not a claim about the full serious MDP.

Important implementation note:

- This first Warehouse tower diagnostic does not construct a complete
  full-MDP `PartitionTower`, because that would require a full action/edge
  surface that is forbidden for Warehouse Gridlock. Instead, it implements the
  workplan's allowed "existing BBB runtime equivalent" over a scoped generated
  surface and records that scope in manifests and result tables.

## Phase 11: Tests

Status: complete.

Added focused tests:

```text
tests/environments/warehouse_gridlock/test_masked_direct_vs_live_lift_tower.py
```

Focused test command:

```text
uv run pytest tests/environments/warehouse_gridlock/test_masked_direct_vs_live_lift_tower.py
```

Result:

```text
5 passed
```

Warehouse regression command:

```text
uv run pytest tests/environments/warehouse_gridlock
```

Result:

```text
20 passed
```

Upstream dependency command:

```text
uv run pytest tests/upstream/test_state_collapser_dependency_state.py tests/upstream/test_state_collapser_pointwise_liftability.py
```

Result:

```text
6 passed
```

Surprise encountered:

- The initial summarize readback failed because CSV reread represented
  `successor_out_count_used_for_selection` as the string `False`, while the
  aggregator expected a numeric value.
- Fixed by allowing boolean strings in numeric aggregation coercion.
- Focused and broader tests were rerun after the fix.

## Phase 12: Smoke Run And Readout

Status: complete.

Smoke run command:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock masked-direct-vs-live-lift-tower run \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/smoke_001 \
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster \
  --smoke
```

Smoke result:

```text
status: success
artifact_count: 27
```

Summarize command:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock masked-direct-vs-live-lift-tower summarize \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/smoke_001
```

Summarize result after fix:

```text
status: success
artifact_count: 14
```

Generated readout surface:

```text
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/
```

Generated readout protocol target:

```text
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/readout_source.json
```

Human-readable regeneration prompt:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/readout_source.json
```

Smoke readout result:

```text
Score direction is tie: mean reward direct=-30.5, tower=-30.5 under the checked budget.
fairness_audit_status: pass
no_lookahead_status: pass
mask_scope_summary: candidate_set
tower_surface_scope_summary: generated_discovered_surface
```

No-lookahead audit:

```text
warehouse_direct_admissible_masked: successor_out_used_for_selection_count=0
warehouse_tower_live_lift_masked: successor_out_used_for_selection_count=0
```

## Phase 13: Hygiene And Handoff

Status: complete.

Current branch:

```text
codex/warehouse-gridlock-masked-direct-live-lift
```

Generated raw artifacts:

```text
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/smoke_001/
```

Artifact provenance caveat:

- The raw smoke artifacts are repo-local and under the correct readout surface.
- Current `.gitignore` policy ignores `docs/evaluations/**/artifacts/`.
- This execution did not change that release-era policy.
- The checked-in human-readable readout surface and `readout_source.json` point
  at the local raw artifact tree.

Terminology audit:

- No active Warehouse readout file describes this evaluation as PlateSupport or
  Counterpoint.
- The only remaining `gameplan` occurrence in this design folder is inside the
  Prime Directive filename
  `common_failure_mode_003_gameplan_rewrite_during_implementation.md`.

Known limitations:

- The smoke result is a tie. This is expected for the first bounded surface and
  should not be interpreted as a negative result or final benchmark result.
- The tower surface is scoped/generated, not full-MDP.
- Candidate generation is deliberately sparse and bounded.
- The next meaningful design question is whether the Warehouse tower candidate
  generator should become stronger before running a larger `masked_001`
  diagnostic.

## Phase 14: Serious-Run Readiness Correction

Status: complete.

Reason for correction:

- The smoke implementation was fair but too weak for the PO's intended
  Warehouse coordination hypothesis.
- With `candidate_proposals_per_step=64`, the old generator emitted
  `all_stay` plus one-active-robot actions first. Multi-robot ensemble moves
  were effectively buried beyond the smoke budget.
- That made the run a smoke/fairness audit, not a serious test of whether a
  tower can help discover coordinated multi-robot gridlock policies over many
  episodes.

Correction implemented:

- Replaced the candidate policy id with:

```text
warehouse_coordination_ready_sparse_ensemble_candidate_generator_v001
```

- Added a candidate mix id:

```text
coordination_ready_sparse_interleaved_v001
```

- Added explicit run knobs:

```text
candidate_proposals_per_step
max_active_robots
candidate_mix_id
```

- Changed candidate generation so bounded budgets interleave:

```text
all_stay
one_active
two_active
three_active
multi_active when max_active_robots > 3
```

- Kept generation bounded and deterministic by sampling larger active-robot
  combinations instead of enumerating impossible `5^32` action surfaces.
- Threaded the same candidate policy through:

```text
direct arm
tower surface construction
successor diagnostic observation
CLI
evaluation budget lock
candidate generation manifest
tower surface scope rows
candidate family summary rows
human-readable docs templates
```

- Added `results/candidate_family_summary.csv` and
  `candidate_family_status` so future expensive runs can be checked quickly
  for actual multi-robot proposal exposure.

Fairness boundary preserved:

- Both arms still use immediate inadmissibility masking.
- Neither arm uses one-step successor-state cul-de-sac lookahead.
- Tower still has live state-lift hygiene only.
- The direct arm does not receive a direct-star guard here.
- The tower arm does not receive a tower-star guard here.

No long run was executed:

- Per PO instruction, this phase prepared the implementation for a serious
  run but did not launch that run.
- Existing `smoke_001` readout remains smoke evidence and should not be
  interpreted as the corrected serious run.

Suggested serious-run command skeleton:

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock masked-direct-vs-live-lift-tower run \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/masked_001 \
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \
  --run-label masked_001 \
  --locked-by foster \
  --episodes-per-arm <large-budget> \
  --replicates-per-arm <replicate-budget> \
  --max-seconds-per-episode <warehouse-time-horizon> \
  --candidate-proposals-per-step 256 \
  --max-active-robots 8 \
  --candidate-mix-id coordination_ready_sparse_interleaved_v001
```

Post-run summarize command:

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock masked-direct-vs-live-lift-tower summarize \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/masked_001
```

Post-run human-readable readout prompt:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/readout_source.json
```

Verification commands run:

```text
uv run pytest tests/environments/warehouse_gridlock/test_masked_direct_vs_live_lift_tower.py
uv run pytest tests/environments/warehouse_gridlock
```

Verification result:

```text
6 passed
21 passed
```
