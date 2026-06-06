# PlateSupport Structural And Tower Diagnostics Implementation Workplan

## Status

Status: initial implementation workplan.

This document is generated from:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/01_structural_and_tower_diagnostics/01_001_plate_support_structural_and_tower_diagnostics_blueprint.md
```

This workplan depends on:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/00_suite_architecture/01_002_plate_support_standard_gauntlet_suite_architecture_implementation_workplan.md
```

This workplan uses `Phase.Stage.Action` discipline.

This workplan is not execution approval. Execution requires explicit Project
Owner instruction.

## Prime Directive Compliance Notes

This workplan follows:

- `docs/prime_directive/prime_directive.md`;
- `docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md`;
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`;
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`;
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`;
- `docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md`;
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`.

Operational consequences:

- Execute only after Project Owner approval.
- Execute in order unless reordering is explicitly authorized.
- Do not silently convert Stage 1 into a generic readiness rerun.
- Do not silently skip the evaluation-stage artifact surface.
- Stop if readiness artifacts are missing, stale, outside the repo, or
  incompatible with the PlateSupport environment doc.
- Do not make learning, candidate, calibration, or comparison claims.

## Authority And Attribution

Project Owner direction from the current request:

- create a detailed implementation workplan for this component;
- do it after suite architecture and before schema sweep;
- follow the blueprint and prime directive.

Consultant-authored assumptions pending Project Owner override:

- Stage 1 defaults to readiness source
  `docs/environments/plate_support_5x5_default_v001/readiness/dev_001/readout_source.json`;
- Stage 1 both promotes readiness artifacts and lightly reruns structural
  diagnostics for stale-readiness detection;
- random-policy reconnaissance budget remains 1000 episodes for the first
  smoke/dev Stage 1 run;
- Stage 1 implementation lives under the standard-gauntlet package created by
  the 00 architecture component.

These assumptions are not Project Owner decisions. If rejected, revise this
workplan before execution.

## Decision Locks Before Implementation

- Stage 1 is evaluation-stage diagnostics, not environment construction.
- Stage 1 must write under `docs/evaluations/.../standard_gauntlet/...`, not
  under `docs/environments/.../readiness/...`.
- Stage 1 must preserve the distinction between:
  - invalid primitive move;
  - valid clipped self-transition;
  - candidate next state;
  - realized next state.
- Stage 1 must produce `downstream_readiness_summary.csv`.
- Stage 1 may certify readiness for schema sweep, but not training performance.
- Stage 1 must consume suite IDs, path helpers, status vocabulary, and manifest
  helpers from the 00 architecture component.

## Expected Final Deliverables

Implementation should produce or update:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/structural_and_tower_diagnostics/
tests/environments/plate_support/test_standard_gauntlet_structural_diagnostics.py
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/structural_and_tower_diagnostics/
docs/design/first_plate_support_environment/standard_gauntlet_suite/01_structural_and_tower_diagnostics/01_003_plate_support_structural_and_tower_diagnostics_implementation_log.md
```

Recommended package files:

```text
__init__.py
config.py
readiness_source.py
diagnostics.py
aggregation.py
manifests.py
docs_writer.py
runner.py
```

Recommended CLI surface:

```bash
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet structural-diagnostics run \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \
  --readiness-source docs/environments/plate_support_5x5_default_v001/readiness/dev_001/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster
```

## Workplan

### Phase 0: Execution Setup And Dependency Check

#### Phase 0.Stage 1: Re-anchor Repo And Architecture Outputs

##### Phase 0.Stage 1.Action 1: Verify branch and dirty state

Action:

- run `git status --short --branch`;
- record branch and dirty files in the Stage 1 implementation log.

Completion criteria:

- current branch and dirty state are known.

Stop condition:

- stop if unrelated work would be overwritten or confused with Stage 1.

##### Phase 0.Stage 1.Action 2: Verify architecture component availability

Action:

- inspect the 00 architecture implementation outputs expected by this workplan:
  - suite/stage IDs;
  - path helpers;
  - status vocabulary;
  - manifest builders;
  - gate definitions.

Completion criteria:

- Stage 1 can import or consume architecture helpers.

Stop condition:

- stop if the 00 architecture component has not been implemented or has
  incompatible names.

##### Phase 0.Stage 1.Action 3: Re-read controlling documents

Action:

- re-read:
  - this workplan;
  - Stage 1 blueprint;
  - suite architecture blueprint/workplan;
  - PlateSupport environment doc;
  - environment readiness readout source;
  - evaluation construction protocol.

Completion criteria:

- implementation log records source documents.

Stop condition:

- stop if current docs contradict this workplan.

#### Phase 0.Stage 2: Create Running Log

##### Phase 0.Stage 2.Action 1: Create Stage 1 implementation log

Action:

- create:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/01_structural_and_tower_diagnostics/01_003_plate_support_structural_and_tower_diagnostics_implementation_log.md
```

Completion criteria:

- log exists before source edits.

Stop condition:

- stop if log path conflicts with existing unrelated content.

##### Phase 0.Stage 2.Action 2: Add Phase.Stage.Action progress table

Action:

- add a progress table for every action in this workplan.

Completion criteria:

- implementation can record completed/blocked state per action.

Stop condition:

- stop if logging reveals this workplan needs rewriting before execution.

### Phase 1: Stage Package And Configuration

#### Phase 1.Stage 1: Create Stage Package

##### Phase 1.Stage 1.Action 1: Create module directory

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/structural_and_tower_diagnostics/
```

Completion criteria:

- directory exists;
- it is nested under the suite package from 00 architecture.

Stop condition:

- stop if the architecture package does not exist.

##### Phase 1.Stage 1.Action 2: Add module initializer

Action:

- add `__init__.py` exporting only stable Stage 1 entry points.

Completion criteria:

- module imports without running diagnostics.

Stop condition:

- stop if import writes artifacts or reads ambient paths.

#### Phase 1.Stage 2: Define Stage Config

##### Phase 1.Stage 2.Action 1: Implement config dataclass

Action:

- create `config.py`;
- define a config carrying:
  - artifact root;
  - run label;
  - readiness source path;
  - locked-by operator;
  - random policy seed;
  - random policy episode count;
  - max steps;
  - linearization mode.

Completion criteria:

- config has no ambient path defaults except through architecture path helpers.

Stop condition:

- stop if required values must be guessed from current working directory.

##### Phase 1.Stage 2.Action 2: Add default factory from architecture paths

Action:

- add a helper that builds config from explicit repository root and run label.

Completion criteria:

- default readiness source and artifact roots match blueprints.

Stop condition:

- stop if run label selection remains unresolved for execution.

### Phase 2: Readiness Source Validation

#### Phase 2.Stage 1: Parse Readiness Source Binding

##### Phase 2.Stage 1.Action 1: Implement readiness source loader

Action:

- create `readiness_source.py`;
- load and validate a readiness `readout_source.json`.

Completion criteria:

- loader reads:
  - repo readout surface;
  - source artifact root;
  - environment family id;
  - environment instance id;
  - run mode or source type if present.

Stop condition:

- stop if readiness source schema differs from expectation and cannot be
  interpreted safely.

##### Phase 2.Stage 1.Action 2: Validate readiness source invariants

Action:

- enforce:
  - readiness source exists;
  - path is repo-resident;
  - environment family is `plate_support`;
  - environment instance is `plate_support_5x5_default_v001`;
  - readiness artifacts live under `docs/environments`;
  - readiness artifacts do not live under `docs/evaluations`.

Completion criteria:

- invalid source fails with a clear Stage 1 block status.

Stop condition:

- stop if validation requires changing environment readiness artifacts.

#### Phase 2.Stage 2: Capture Dependency State

##### Phase 2.Stage 2.Action 1: Read dependency manifest from readiness artifacts

Action:

- locate and parse the readiness dependency manifest or equivalent source file.

Completion criteria:

- Stage 1 can record upstream `state_collapser` and BBB dependency state.

Stop condition:

- stop if dependency state is missing and the evaluation construction protocol
  requires it for provenance.

##### Phase 2.Stage 2.Action 2: Compare readiness dependency state to current import state

Action:

- inspect current importable dependency version/status without modifying
  dependencies.

Completion criteria:

- mismatch is recorded as warning, not hidden.

Stop condition:

- stop if current dependency lacks required PlateSupport surfaces.

### Phase 3: Diagnostic Data Collection

#### Phase 3.Stage 1: Identity And State-Space Diagnostics

##### Phase 3.Stage 1.Action 1: Collect identity/provenance rows

Action:

- implement identity summary collection using suite IDs from architecture and
  PlateSupport environment IDs from the environment package.

Completion criteria:

- `identity_summary.csv` fields can be populated.

Stop condition:

- stop if source IDs mismatch the blueprint.

##### Phase 3.Stage 1.Action 2: Collect state-space rows

Action:

- reuse PlateSupport graph/state helpers to compute:
  - ambient candidate states;
  - valid states;
  - reachable valid states;
  - start/goal validity;
  - reachability from start.

Completion criteria:

- output can reproduce known readiness values or record mismatch.

Stop condition:

- stop if current values differ from readiness doc without explanation.

#### Phase 3.Stage 2: Action And Transition Diagnostics

##### Phase 3.Stage 2.Action 1: Collect primitive action table

Action:

- produce one row per primitive action with stable action ids and labels.

Completion criteria:

- all 12 primitive actions are present.

Stop condition:

- stop if action count differs and no environment doc update exists.

##### Phase 3.Stage 2.Action 2: Collect transition summary

Action:

- compute valid non-self edges, invalid moves, valid clipped self-transitions,
  and total self-loop transitions.

Completion criteria:

- candidate next state and realized next state are separate fields.

Stop condition:

- stop if invalid self-loop and valid clipped self-transition cannot be
  distinguished.

##### Phase 3.Stage 2.Action 3: Compute outgoing/invalid/self-transition distributions

Action:

- aggregate per-state outgoing non-self count, invalid action count, and
  self-transition count distributions.

Completion criteria:

- downstream schema sweep can use action availability and transition pressure.

Stop condition:

- stop if distributions require a new environment semantic decision.

#### Phase 3.Stage 3: Shortest Path, Reward, And Geometry Diagnostics

##### Phase 3.Stage 3.Action 1: Compute shortest path anchor

Action:

- compute shortest start-goal path length, action labels, reward sequence, and
  total reward.

Completion criteria:

- shortest path length and goal-one-step status are written.

Stop condition:

- stop if no finite shortest path exists.

##### Phase 3.Stage 3.Action 2: Collect validity and geometry summaries

Action:

- summarize validity predicates, support patterns, reachability patterns,
  orientation, positions, socket distribution, and engaged-arm reachability.

Completion criteria:

- geometry-specific constraints are visible to human readouts.

Stop condition:

- stop if geometry helpers do not expose stable fields.

#### Phase 3.Stage 4: Random Policy Reconnaissance

##### Phase 3.Stage 4.Action 1: Run random policy reconnaissance

Action:

- run the configured random policy budget and collect:
  - success count/rate;
  - mean reward;
  - mean step count;
  - invalid move count/rate.

Completion criteria:

- `random_policy_recon_summary.csv` exists.

Stop condition:

- stop if the random policy runner writes outside the Stage 1 artifact root.

##### Phase 3.Stage 4.Action 2: Label random policy claim boundary

Action:

- annotate random policy rows as structural difficulty reconnaissance, not a
  learning baseline.

Completion criteria:

- readout source can prevent baseline overclaiming.

Stop condition:

- stop if code path treats random policy as an official comparison arm.

#### Phase 3.Stage 5: Tower Shape And Training Surface Diagnostics

##### Phase 3.Stage 5.Action 1: Collect default and no-contraction tower probes

Action:

- reuse PlateSupport tower probe helpers to record:
  - default schema id;
  - no-contraction schema id;
  - max depth;
  - scheduled/unscheduled assignment counts;
  - depth curve;
  - reset events.

Completion criteria:

- `tower_shape_summary.csv` contains both default and no-contraction rows.

Stop condition:

- stop if tower probe cannot run under current dependency state.

##### Phase 3.Stage 5.Action 2: Collect training surface availability

Action:

- inspect availability of upstream PlateSupport runtime, executor, learner,
  config, and training helpers named in the blueprint.

Completion criteria:

- `training_surface_availability.csv` records available/missing status.

Stop condition:

- stop if required training surfaces are absent and later stages would be
  impossible.

### Phase 4: Stage Artifacts And Aggregation

#### Phase 4.Stage 1: Write Required Tables

##### Phase 4.Stage 1.Action 1: Write core result CSVs

Action:

- write all required result tables:
  - `identity_summary.csv`;
  - `state_space_summary.csv`;
  - `action_table.csv`;
  - `transition_summary.csv`;
  - `shortest_path_summary.csv`;
  - `validity_predicate_summary.csv`;
  - `geometry_summary.csv`;
  - `random_policy_recon_summary.csv`;
  - `tower_shape_summary.csv`;
  - `training_surface_availability.csv`.

Completion criteria:

- every table is present under Stage 1 results.

Stop condition:

- stop if any table would need to be faked from prose rather than computed or
  promoted from evidence.

##### Phase 4.Stage 1.Action 2: Write downstream readiness summary

Action:

- write `downstream_readiness_summary.csv` with all fields specified in the
  blueprint.

Completion criteria:

- `ready_for_schema_sweep` is explicitly true/false with reason.

Stop condition:

- stop if readiness cannot be classified without a Project Owner decision.

#### Phase 4.Stage 2: Write Stage Manifests

##### Phase 4.Stage 2.Action 1: Write input/output manifests

Action:

- write:
  - `stage_manifest.json`;
  - `stage_budget_lock.json`;
  - `stage_input_manifest.json`;
  - `stage_output_manifest.json`;
  - `readiness_source_manifest.json`.

Completion criteria:

- manifests trace all readiness and environment sources.

Stop condition:

- stop if any source path is outside the repository.

##### Phase 4.Stage 2.Action 2: Write aggregate summaries

Action:

- write:
  - `stage_aggregate_summary.json`;
  - `stage_aggregate_table.csv`;
  - `stage_run_index.csv`.

Completion criteria:

- aggregate row includes Stage 1 status, warning/block reason, and claim
  boundary.

Stop condition:

- stop if status vocabulary cannot map to the architecture vocabulary.

### Phase 5: Stage Readout Seed And Suite Integration

#### Phase 5.Stage 1: Write Stage Readout Source

##### Phase 5.Stage 1.Action 1: Create Stage 1 `readout_source.json`

Action:

- write Stage 1 readout source under:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/structural_and_tower_diagnostics/readout_source.json
```

Completion criteria:

- source binding points to Stage 1 artifact root and required tables.

Stop condition:

- stop if source binding points to the readiness artifact root instead of Stage
  1 artifacts.

##### Phase 5.Stage 1.Action 2: Write seed human docs

Action:

- write or update Stage 1 seed docs:
  - `README.md`;
  - `method.md`;
  - `artifact_index.md`;
  - `runbook.md`;
  - `results/summary.md`.

Completion criteria:

- docs state Stage 1 claim boundary and link raw artifacts.

Stop condition:

- stop if docs claim learning or comparison evidence.

#### Phase 5.Stage 2: Update Suite-Level Stage Status

##### Phase 5.Stage 2.Action 1: Emit suite stage status row

Action:

- append or write the Stage 1 row in suite-level `stage_status_summary.csv`.

Completion criteria:

- Stage 2 gate can consume the Stage 1 status row.

Stop condition:

- stop if suite architecture component has not defined stage status row format.

### Phase 6: CLI Integration

#### Phase 6.Stage 1: Add CLI Commands

##### Phase 6.Stage 1.Action 1: Inspect PlateSupport CLI pattern

Action:

- inspect current PlateSupport readiness CLI pattern.

Completion criteria:

- Stage 1 CLI implementation follows existing style.

Stop condition:

- stop if CLI grouping would be ambiguous.

##### Phase 6.Stage 1.Action 2: Add Stage 1 run command

Action:

- add `plate-support standard-gauntlet structural-diagnostics run`.

Completion criteria:

- command accepts explicit artifact root, readiness source, run label, and
  locked-by.

Stop condition:

- stop if command would infer paths from current working directory.

##### Phase 6.Stage 1.Action 3: Add Stage 1 summarize/inspect command if needed

Action:

- add a summarize or inspect command only if it matches existing CLI
  conventions.

Completion criteria:

- command reads Stage 1 artifacts and reports status without rerunning.

Stop condition:

- stop if summarization semantics overlap with readout protocol generation.

### Phase 7: Tests And Verification

#### Phase 7.Stage 1: Unit Tests

##### Phase 7.Stage 1.Action 1: Test readiness source validation

Action:

- add tests for valid source, wrong environment id, outside-repo source, and
  artifacts under the wrong tree.

Completion criteria:

- invalid readiness sources produce controlled block status.

Stop condition:

- stop if tests require mutating real readiness artifacts.

##### Phase 7.Stage 1.Action 2: Test diagnostic table completeness

Action:

- test that Stage 1 smoke output contains every required result table and
  required columns.

Completion criteria:

- missing tables/columns fail tests.

Stop condition:

- stop if tests reveal required tables cannot be produced from current
  PlateSupport helpers.

##### Phase 7.Stage 1.Action 3: Test claim boundary

Action:

- test that Stage 1 output marks random policy and tower shape as diagnostic,
  not comparison evidence.

Completion criteria:

- claim boundary is machine-readable.

Stop condition:

- stop if status vocabulary cannot encode diagnostic-only output.

#### Phase 7.Stage 2: Runtime Smoke

##### Phase 7.Stage 2.Action 1: Run Stage 1 smoke command

Action:

- run Stage 1 against a repo-local smoke artifact root.

Completion criteria:

- command exits successfully or with a controlled block status;
- artifacts are written under the Stage 1 artifact root.

Stop condition:

- stop on unexpected exception or path drift.

##### Phase 7.Stage 2.Action 2: Verify artifact paths

Action:

- inspect artifact tree and readout source paths.

Completion criteria:

- no durable output is written to `/tmp` or environment readiness folders.

Stop condition:

- stop if artifact path roles are mixed.

#### Phase 7.Stage 3: Final Log Update

##### Phase 7.Stage 3.Action 1: Record validation results

Action:

- update implementation log with commands, test results, files changed,
  warnings, and Stage 2 readiness.

Completion criteria:

- log clearly states whether Stage 2 can proceed.

Stop condition:

- stop if any required Stage 1 artifact is incomplete.

## Completion Criteria For The Component

Stage 1 is complete when:

- readiness source validation exists;
- Stage 1 diagnostics are generated under the standard-gauntlet evaluation
  surface;
- all required manifests and result tables exist;
- `downstream_readiness_summary.csv` gates schema sweep;
- readout source and seed docs exist;
- CLI/run surface exists or omission is recorded;
- focused tests pass;
- implementation log records Phase.Stage.Action completion.

## Handoff To Next Component

The contraction schema sweep workplan must consume:

```text
results/tower_shape_summary.csv
results/transition_summary.csv
results/action_table.csv
results/downstream_readiness_summary.csv
stage_manifest.json
readout_source.json
```

It must not reach back directly into environment readiness artifacts except
through Stage 1 provenance links.
