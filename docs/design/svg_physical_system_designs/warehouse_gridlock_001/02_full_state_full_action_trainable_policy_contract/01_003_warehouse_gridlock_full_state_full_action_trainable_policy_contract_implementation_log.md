# Warehouse Gridlock Full-State Full-Action Trainable Policy Contract Implementation Log

## Status

In progress.

This log records execution of:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/02_full_state_full_action_trainable_policy_contract/01_002_warehouse_gridlock_full_state_full_action_trainable_policy_contract_implementation_workplan.md
```

## Phase 0: Orientation, Branch Discipline, And Reality Check

### Phase 0.Stage 1.Action 1: Verify Current Git State

Completed.

Result:

```text
git status --short
<clean>
```

No unrelated staged files were present.

### Phase 0.Stage 1.Action 2: Create Or Switch To The Implementation Branch

Completed.

Branch:

```text
codex/warehouse-gridlock-full-state-policy-contract
```

### Phase 0.Stage 1.Action 3: Re-Read Authority Documents

Completed.

Active scope confirmed:

```text
Implement the trainable full-state/full-action Warehouse policy contract only.
Do not redesign Warehouse Gridlock.
Do not reopen masking, no-lookahead, live-lift, artifact, or replay decisions.
```

### Phase 0.Stage 1.Action 4: Inspect Existing Warehouse Runtime Surfaces

Completed.

Reusable surfaces identified:

- `actions.py`: robot command/action representation.
- `state.py`: Warehouse state and stable ids.
- `transition.py`: authoritative immediate transition validity and reward
  result.
- `instances.py`: environment instance/manifest loading.
- `rewards.py`: target-count and reward support.
- `masked_direct_vs_live_lift_tower/runner.py`: current diagnostic loop and
  candidate-id learner failure surface.
- `masked_direct_vs_live_lift_tower/tower_surface.py`: scoped
  generated/discovered tower surface.
- `replay.py`: episode replay from `step_events.csv`.
- `cli/main.py`: existing CLI command integration pattern.

### Phase 0.Stage 1.Action 5: Confirm Existing Tests Before Editing

Completed.

Command:

```text
uv run pytest tests/environments/warehouse_gridlock
```

Result:

```text
24 passed in 1.18s
```

## Phase 1: Shared Full-State Full-Action Policy Contract

Completed.

Implemented:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/policies/__init__.py
src/big_boy_benchmarking/environments/warehouse_gridlock/policies/contracts.py
src/big_boy_benchmarking/environments/warehouse_gridlock/policies/serialization.py
```

Key result:

```text
WarehouseFullSystemConfig records static and dynamic Warehouse facts.
WarehouseFullActionVector wraps the existing WarehouseGridlockAction full
robot-command map and validates exact robot coverage.
config_from_instance_state converts existing Warehouse instance/state objects
into the PO-requested full-system policy input.
```

## Phase 2: Feature Encoder And Trainable Linear Policy

Completed.

Implemented:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/policies/features.py
src/big_boy_benchmarking/environments/warehouse_gridlock/policies/linear_policy.py
```

Policy family:

```text
warehouse_linear_factorized_softmax_policy_v001
```

The policy receives full system config plus current second and emits a full
simultaneous Warehouse action vector. Updates change reusable feature weights,
not generated candidate ids.

## Phase 3: Bounded Admissibility Resolver

Completed.

Implemented:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/policies/resolver.py
```

Resolver:

```text
bounded_deterministic_repair_with_all_stay_fallback_v001
projection_attempt_budget: 64
```

The resolver uses `transition.step` for immediate validity only. It does not
inspect successor `Out`, future deadness, path distance after execution, or a
global planner.

## Phase 4 Through Phase 10: Corrected Evaluation Package, Runner, Aggregation, Docs, CLI, Replay Compatibility

Completed.

Implemented:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/__init__.py
src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/config.py
src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/paths.py
src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/events.py
src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/manifests.py
src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/aggregation.py
src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/docs_writer.py
src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/runner.py
src/big_boy_benchmarking/cli/main.py
tests/environments/warehouse_gridlock/test_full_state_policy_contract.py
```

CLI commands:

```text
warehouse-gridlock full-state-policy-comparison run
warehouse-gridlock full-state-policy-comparison summarize
```

Direct arm:

```text
warehouse_direct_full_state_policy_masked
```

Tower arm:

```text
warehouse_tower_full_state_policy_live_lift_masked
```

Tower integration:

```text
The tower arm reuses the existing scoped generated/discovered tower surface
and live state-lift hygiene. It scores concrete realizations through reusable
feature weights, not candidate ids. The selected action at the Warehouse
boundary is still a full concrete action vector.
```

Replay compatibility:

```text
The corrected evaluation writes standard step_events.csv rows, so the existing
warehouse-gridlock render-episode command remains compatible.
```

## Phase 11: Smoke Execution

Completed.

### Phase 11.Stage 1.Action 1: Run Unit Tests

Command:

```text
uv run pytest tests/environments/warehouse_gridlock
```

Result:

```text
28 passed in 1.11s
```

### Phase 11.Stage 1.Action 2: Run Corrected Smoke Evaluation

Command:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-state-policy-comparison run --repo-root . --artifact-root docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/artifacts/policy_contract_smoke_001 --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json --run-label policy_contract_smoke_001 --locked-by foster --episodes-per-arm 4 --replicates-per-arm 1 --schema-seeds 1 --max-seconds-per-episode 128 --projection-attempt-budget 64 --progress-every-episodes 1
```

Result:

```text
status: success
artifact_count: 25
```

### Phase 11.Stage 1.Action 3: Summarize Corrected Smoke Evaluation

Command:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-state-policy-comparison summarize --repo-root . --artifact-root docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/artifacts/policy_contract_smoke_001
```

Result:

```text
status: complete
artifact_count: 12
```

### Phase 11.Stage 1.Action 4: Verify Learning Health

Result:

```text
warehouse_direct_full_state_policy_masked:
  update_count: 512
  non_noop_update_count: 512
  nonzero_prior_signal_decision_count: 511
  learning_status: real_learning_signal_present

warehouse_tower_full_state_policy_live_lift_masked:
  update_count: 512
  non_noop_update_count: 512
  nonzero_prior_signal_decision_count: 511
  learning_status: real_learning_signal_present
```

Learning-health gate passed for both active arms.

### Phase 11.Stage 1.Action 5: Regenerate Human-Readable Readout

Completed through the evaluation docs writer and source binding.

Generated:

```text
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/README.md
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/readout_source.json
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/method.md
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/runbook.md
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/artifact_index.md
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/result_readout.md
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/results/
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/badges/
```

The readout source includes the canonical command:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/readout_source.json
```

## Phase 12: Final Verification

Completed.

### Tests

Command:

```text
uv run pytest tests/environments/warehouse_gridlock
```

Result:

```text
28 passed in 1.27s
```

### Forbidden Claim Search

Search terms:

```text
backprop
neural
statistical significance
general tower superiority
full MDP
optimal
```

Result:

```text
All matches in the new surface are negated, marked not applicable, or recorded
as claim-blocking structural checks.
```

### Machine-Local Path Search

Result:

```text
No machine-local paths found in the new full-state policy readout/source
surface.
```

### Release Hygiene

Command:

```text
uv run python scripts/release_hygiene.py --repo-root .
```

Result:

```text
failed with 10 pre-existing issues outside the new full-state policy surface:

- 2 machine-local path issues in the older
  01_masked_direct_vs_live_lift_tower_no_lookahead workplan.
- 2 public placeholder issues in the PlateSupport direct-star README.
- 6 public placeholder issues in the older Warehouse masked
  direct/live-lift README.
```

The new workplan initially had one machine-local temporary path mention. That
was corrected to `machine-local temporary directory`, after which release
hygiene reported only the pre-existing issues above.

### Final Worktree Classification

Intended changes:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/02_full_state_full_action_trainable_policy_contract/
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/
src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/
src/big_boy_benchmarking/environments/warehouse_gridlock/policies/
src/big_boy_benchmarking/cli/main.py
tests/environments/warehouse_gridlock/test_full_state_policy_contract.py
```

No unrelated files were intentionally modified.

## Phase 13: Completion Criteria

Completed.

Code completion:

```text
policy contract types exist
linear factorized policy exists
shared resolver exists
direct corrected arm uses full config plus second
tower corrected arm uses full config/tier context plus second
both arms emit or realize full concrete action vectors
both arms update reusable policy state
candidate-id learning is not the primary learner state
CLI run and summarize commands work
```

Artifact completion:

```text
manifests, run index, event tables, aggregate tables, learning-health tables,
policy-reuse tables, no-lookahead audit tables, tower live-lift tables,
readout source, badges, and human-readable docs were generated under the new
repo readout surface.
```

Learning completion:

```text
Both active arms passed the smoke learning-health gate.
```

Claim completion:

```text
The implementation may claim the Warehouse corrected policy contract was
implemented and smoke-validated. It may not claim Warehouse is solved, tower is
generally better, backprop happened, the full serious MDP was enumerated, or
the result is statistically significant.
```
