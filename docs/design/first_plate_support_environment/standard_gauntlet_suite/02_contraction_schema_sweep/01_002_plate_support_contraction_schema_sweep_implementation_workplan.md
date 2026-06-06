# PlateSupport Contraction Schema Sweep Implementation Workplan

## Status

Status: initial implementation workplan.

This document is generated from:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/02_contraction_schema_sweep/01_001_plate_support_contraction_schema_sweep_blueprint.md
```

This workplan depends on:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/00_suite_architecture/01_002_plate_support_standard_gauntlet_suite_architecture_implementation_workplan.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/01_structural_and_tower_diagnostics/01_002_plate_support_structural_and_tower_diagnostics_implementation_workplan.md
```

This workplan uses `Phase.Stage.Action` discipline.

This workplan is not execution approval. Execution requires explicit Project
Owner instruction.

## Prime Directive Compliance Notes

This workplan follows:

- `docs/prime_directive/prime_directive.md`;
- `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`;
- `docs/prime_directive/artifact_table_to_readable_document_protocol.md`;
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`;
- `docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md`;
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`.

Operational consequences:

- Execute only after explicit Project Owner approval.
- Execute after architecture and Stage 1 are implemented.
- Do not silently fake geometry-based schemas if the runtime cannot represent
  them.
- Do not treat schema sweep as candidate selection or training.
- Do not copy counterpoint denominator, thresholds, schema IDs, or path-volume
  semantics into PlateSupport.
- Stop if Stage 1 does not say `ready_for_schema_sweep = true`.

## Authority And Attribution

Project Owner direction from the current request:

- create the workplan after Stage 1 and before candidate discovery;
- follow the contraction schema sweep blueprint;
- preserve Phase.Stage.Action discipline.

Consultant-authored assumptions pending Project Owner override:

- first sweep run is smoke/dev, not serious;
- no-contraction and upstream default schema arms are mandatory;
- action-category and edge-global noisy-rate arms are safe first custom arms;
- geometry-coordinate schema arms are attempted only if the runtime can
  represent them honestly;
- edge-global rates use valid non-self edge count (`388`) as denominator for
  edge-based selection unless Project Owner chooses another basis.

These assumptions are not Project Owner decisions.

## Decision Locks Before Implementation

- Stage 2 consumes Stage 1 artifacts, especially:
  - `results/transition_summary.csv`;
  - `results/tower_shape_summary.csv`;
  - `results/validity_predicate_summary.csv`;
  - `results/geometry_summary.csv`;
  - `results/downstream_readiness_summary.csv`.
- Stage 2 writes schema sweep artifacts under the standard-gauntlet evaluation
  tree.
- Stage 2 emits candidate signals for Stage 3 but does not select final
  candidates.
- Every schema arm must produce a structured row, even if construction fails.
- Missing axes must be explicit `not_applicable`, not blank.
- Collapse/degeneracy criteria must be table-backed and overrideable.
- Geometry schema arms must stop or be marked construction-blocked if upstream
  surfaces cannot support them honestly.

## Expected Final Deliverables

Implementation should produce or update:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/
tests/environments/plate_support/test_standard_gauntlet_contraction_schema_sweep.py
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/contraction_schema_sweep/
docs/design/first_plate_support_environment/standard_gauntlet_suite/02_contraction_schema_sweep/01_003_plate_support_contraction_schema_sweep_implementation_log.md
```

Recommended package files:

```text
__init__.py
config.py
stage1_source.py
schema_families.py
schema_builders.py
schema_runner.py
diagnostics.py
classification.py
aggregation.py
manifests.py
docs_writer.py
runner.py
```

Recommended CLI surface:

```bash
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet schema-sweep run \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \
  --stage1-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/structural_and_tower_diagnostics/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster
```

## Workplan

### Phase 0: Execution Setup And Stage 1 Gate

#### Phase 0.Stage 1: Re-anchor Repository And Dependencies

##### Phase 0.Stage 1.Action 1: Verify branch and dirty state

Action:

- run `git status --short --branch`;
- record branch and dirty files in the Stage 2 implementation log.

Completion criteria:

- current repo state is recorded before edits.

Stop condition:

- stop if unrelated dirty files would be overwritten or confused with Stage 2.

##### Phase 0.Stage 1.Action 2: Verify architecture and Stage 1 outputs

Action:

- confirm 00 architecture helpers exist;
- confirm Stage 1 implementation can produce or has produced:
  - `downstream_readiness_summary.csv`;
  - `transition_summary.csv`;
  - `tower_shape_summary.csv`;
  - `geometry_summary.csv`;
  - `stage_manifest.json`.

Completion criteria:

- Stage 2 can consume Stage 1 through readout/source manifests.

Stop condition:

- stop if Stage 1 artifacts are absent, incompatible, or stale.

##### Phase 0.Stage 1.Action 3: Check Stage 1 gate

Action:

- read Stage 1 downstream readiness status;
- require `ready_for_schema_sweep = true`.

Completion criteria:

- gate pass/block is recorded.

Stop condition:

- stop if Stage 1 blocks schema sweep.

#### Phase 0.Stage 2: Create Implementation Log

##### Phase 0.Stage 2.Action 1: Create Stage 2 implementation log

Action:

- create:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/02_contraction_schema_sweep/01_003_plate_support_contraction_schema_sweep_implementation_log.md
```

Completion criteria:

- log exists before source edits.

Stop condition:

- stop if log path conflicts with unrelated content.

##### Phase 0.Stage 2.Action 2: Add progress table and source record

Action:

- add Phase.Stage.Action progress table;
- record Stage 1 source artifacts and blueprint files read.

Completion criteria:

- execution trace can prove Stage 2 did not reach back directly into
  environment readiness except through Stage 1 provenance.

Stop condition:

- stop if Stage 1 source path is ambiguous.

### Phase 1: Stage Package And Configuration

#### Phase 1.Stage 1: Create Stage Package

##### Phase 1.Stage 1.Action 1: Create schema sweep package

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/
```

Completion criteria:

- package is nested under standard gauntlet suite.

Stop condition:

- stop if the suite architecture package does not exist.

##### Phase 1.Stage 1.Action 2: Add module initializer

Action:

- create `__init__.py` exporting stable Stage 2 entry points only.

Completion criteria:

- import has no side effects.

Stop condition:

- stop if import attempts to build schemas or write artifacts.

#### Phase 1.Stage 2: Define Config And Budget

##### Phase 1.Stage 2.Action 1: Implement sweep config

Action:

- create `config.py`;
- include:
  - artifact root;
  - run label;
  - Stage 1 readout source;
  - locked-by;
  - schema families to attempt;
  - schema seeds;
  - edge-global rate settings;
  - collapse thresholds;
  - smoke rollout settings if any;
  - linearization mode.

Completion criteria:

- config makes all sweep axes explicit.

Stop condition:

- stop if defaults would encode unresolved Project Owner decisions as facts.

##### Phase 1.Stage 2.Action 2: Define smoke/dev default sweep plan

Action:

- define consultant-default first sweep plan:
  - no-contraction;
  - upstream default;
  - action-category schemas;
  - small edge-global noisy-rate schemas;
  - geometry-coordinate schemas only if supported.

Completion criteria:

- plan marks unsupported schema families as blocked/not attempted rather than
  silently dropping them.

Stop condition:

- stop if Project Owner has not authorized using consultant defaults for
  execution.

### Phase 2: Stage 1 Source Loader

#### Phase 2.Stage 1: Parse Stage 1 Source Binding

##### Phase 2.Stage 1.Action 1: Implement Stage 1 source loader

Action:

- create `stage1_source.py`;
- load Stage 1 `readout_source.json` and resolve required tables.

Completion criteria:

- loader returns paths to required Stage 1 tables.

Stop condition:

- stop if source binding points to raw artifacts without a repo readout surface.

##### Phase 2.Stage 1.Action 2: Validate required Stage 1 tables

Action:

- verify existence and required columns for:
  - transition summary;
  - tower shape summary;
  - validity predicate summary;
  - geometry summary;
  - downstream readiness summary.

Completion criteria:

- missing/invalid Stage 1 files produce controlled block status.

Stop condition:

- stop if Stage 1 table schema is incompatible with this blueprint.

### Phase 3: Schema Family Definitions

#### Phase 3.Stage 1: Implement Mandatory Families

##### Phase 3.Stage 1.Action 1: Define no-contraction control

Action:

- implement schema family metadata for
  `plate_support_schema_no_contraction_v001`.

Completion criteria:

- arm is marked `flat_control` expectation.

Stop condition:

- stop if no-contraction cannot be represented by current runtime.

##### Phase 3.Stage 1.Action 2: Define upstream default schema

Action:

- implement schema family metadata and builder binding for
  `plate_support_schema_upstream_default_v001`.

Completion criteria:

- arm references upstream default schema behavior and expected readiness values.

Stop condition:

- stop if upstream default schema surface is missing or renamed.

#### Phase 3.Stage 2: Implement Custom Candidate Families

##### Phase 3.Stage 2.Action 1: Define action-category schemas

Action:

- define action-category schema metadata for:
  - plate motion actions;
  - arm extension actions;
  - motion-vs-support actions.

Completion criteria:

- selected action categories are explicit in schema selection rows.

Stop condition:

- stop if primitive action labels cannot support stable categories.

##### Phase 3.Stage 2.Action 2: Define edge-global noisy-rate schemas

Action:

- implement edge-global selection policy over valid non-self edges from Stage 1;
- default denominator to valid non-self edge count for edge-based selection.

Completion criteria:

- rate labels and actual denominator are both recorded.

Stop condition:

- stop if denominator basis is ambiguous at execution time.

##### Phase 3.Stage 2.Action 3: Define controlled degeneracy anchors

Action:

- define full-single-block and source-local-one-drop schema family metadata.

Completion criteria:

- arms are marked as degeneracy anchors and not eligible for training by
  default.

Stop condition:

- stop if implementation would accidentally pass a degeneracy anchor as an
  eligible training candidate.

#### Phase 3.Stage 3: Handle Geometry-Coordinate Schemas

##### Phase 3.Stage 3.Action 1: Inspect upstream schema expressivity

Action:

- inspect available `state_collapser` and BBB schema construction surfaces to
  determine whether position/orientation/support/reachability feature schemas
  can be represented honestly.

Completion criteria:

- implementation log records supported and unsupported geometry schema forms.

Stop condition:

- stop if geometry schemas require upstream design changes.

##### Phase 3.Stage 3.Action 2: Implement or block geometry schemas honestly

Action:

- if supported, implement geometry-coordinate schema builders;
- if unsupported, emit `construction_failed` or `not_supported` rows with
  explicit reason.

Completion criteria:

- no geometry schema is faked through unrelated edge-label behavior.

Stop condition:

- stop if stakeholders need a design decision about upstream schema API.

### Phase 4: Schema Arm Execution

#### Phase 4.Stage 1: Build Schema Arms

##### Phase 4.Stage 1.Action 1: Create schema arm manifest

Action:

- enumerate all configured schema arms with:
  - family id;
  - schema id;
  - schema seed;
  - selection policy;
  - selection rate/count;
  - axes with `not_applicable` where unused.

Completion criteria:

- `schema_arm_manifest.json` can be written before construction.

Stop condition:

- stop if any arm lacks stable identity.

##### Phase 4.Stage 1.Action 2: Construct each schema arm

Action:

- run schema builder for every arm;
- capture construction success/failure and metadata.

Completion criteria:

- every arm has a construction status row.

Stop condition:

- stop only on unexpected infrastructure failure; expected construction failure
  for optional arms should become a structured row.

#### Phase 4.Stage 2: Run Tower Diagnostics

##### Phase 4.Stage 2.Action 1: Build/probe tower for each constructed arm

Action:

- run tower construction/probe for each successfully constructed schema arm.

Completion criteria:

- tower max depth, state/action cell counts, and largest cell share can be
  recorded.

Stop condition:

- stop if mandatory no-contraction or upstream default arm cannot run.

##### Phase 4.Stage 2.Action 2: Run optional executable-action smoke

Action:

- run tiny smoke rollout or static executability probe if available;
- record active action-cell counts and lift success/failure probes.

Completion criteria:

- `tier_executability_summary.csv` can be written.

Stop condition:

- stop if smoke rollout would become training or comparison.

### Phase 5: Classification And Candidate Signals

#### Phase 5.Stage 1: Classify Structural Outcomes

##### Phase 5.Stage 1.Action 1: Implement collapse classifier

Action:

- create `classification.py`;
- classify each arm as:
  - `flat_control`;
  - `nonflat_structured`;
  - `near_flat`;
  - `near_full_collapse`;
  - `full_first_projection_collapse`;
  - `runtime_unexecutable`;
  - `construction_failed`.

Completion criteria:

- threshold values are visible in output rows.

Stop condition:

- stop if classification cannot be supported by table evidence.

##### Phase 5.Stage 1.Action 2: Compute endpoint coalescence and collapse diagnostics

Action:

- compute endpoint coalescence, largest cell share, singleton share, and first
  projection collapse indicators.

Completion criteria:

- collapse diagnostics are table-backed.

Stop condition:

- stop if quotient summaries lack enough information.

#### Phase 5.Stage 2: Emit Candidate Signals

##### Phase 5.Stage 2.Action 1: Implement candidate signal logic

Action:

- map structural classes and executability to:
  - `eligible_signal`;
  - `warning_signal`;
  - `blocked_signal`;
  - `control_anchor`;
  - `degeneracy_anchor`.

Completion criteria:

- no final candidate selection occurs.

Stop condition:

- stop if candidate signal policy would require Project Owner choice.

##### Phase 5.Stage 2.Action 2: Write downstream candidate input summary

Action:

- write `downstream_candidate_input_summary.csv` for Stage 3.

Completion criteria:

- Stage 3 can consume schema signals without re-running Stage 2.

Stop condition:

- stop if candidate rows lack source artifact paths.

### Phase 6: Artifact Writing And Readout Binding

#### Phase 6.Stage 1: Write Manifests And Tables

##### Phase 6.Stage 1.Action 1: Write Stage 2 manifests

Action:

- write:
  - `stage_manifest.json`;
  - `stage_budget_lock.json`;
  - `stage_input_manifest.json`;
  - `stage_source_manifest.json`;
  - `schema_family_manifest.json`;
  - `schema_arm_manifest.json`;
  - `schema_construction_manifest.json`.

Completion criteria:

- manifests trace Stage 1 inputs and schema construction outputs.

Stop condition:

- stop if source paths are non-repo-resident.

##### Phase 6.Stage 1.Action 2: Write required result tables

Action:

- write:
  - `schema_arm_summary.csv`;
  - `schema_construction_summary.csv`;
  - `schema_selection_summary.csv`;
  - `tower_shape_summary.csv`;
  - `tier_occupancy_summary.csv`;
  - `tier_executability_summary.csv`;
  - `endpoint_coalescence_summary.csv`;
  - `collapse_diagnostic_summary.csv`;
  - `schema_candidate_signal_summary.csv`;
  - `timing_summary.csv`;
  - `downstream_candidate_input_summary.csv`.

Completion criteria:

- every attempted arm has rows across summary tables or explicit absence reason.

Stop condition:

- stop if any required table would need placeholder data.

##### Phase 6.Stage 1.Action 3: Write aggregate files

Action:

- write:
  - `stage_aggregate_summary.json`;
  - `stage_aggregate_table.csv`;
  - `stage_run_index.csv`.

Completion criteria:

- stage pass/warning/block state is explicit.

Stop condition:

- stop if pass/warning/block cannot be determined from evidence.

#### Phase 6.Stage 2: Write Readout Source And Seed Docs

##### Phase 6.Stage 2.Action 1: Create Stage 2 readout source

Action:

- write:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/contraction_schema_sweep/readout_source.json
```

Completion criteria:

- source binding lists required files, structural limit checks, goal sources,
  methodology sources, and claim boundary.

Stop condition:

- stop if readout source would need to infer schema intent from code.

##### Phase 6.Stage 2.Action 2: Write seed human docs

Action:

- write or update:
  - `README.md`;
  - `method.md`;
  - `artifact_index.md`;
  - `runbook.md`;
  - `results/summary.md`.

Completion criteria:

- docs state Stage 2 is structural/candidate-signal only.

Stop condition:

- stop if docs imply training or comparison evidence.

### Phase 7: CLI Integration

#### Phase 7.Stage 1: Add Run/Summarize Commands

##### Phase 7.Stage 1.Action 1: Add schema sweep run command

Action:

- add CLI command for Stage 2 run with explicit artifact root and Stage 1
  source.

Completion criteria:

- command writes only Stage 2 artifacts.

Stop condition:

- stop if command needs ambient "last Stage 1 run" inference.

##### Phase 7.Stage 1.Action 2: Add schema sweep summarize command if needed

Action:

- add a summarize command that reads Stage 2 artifacts and reports status.

Completion criteria:

- summarize does not rerun schema construction unless explicitly named.

Stop condition:

- stop if summarize overlaps with human readout protocol.

### Phase 8: Tests And Verification

#### Phase 8.Stage 1: Unit Tests

##### Phase 8.Stage 1.Action 1: Test Stage 1 gate enforcement

Action:

- add tests that block Stage 2 when Stage 1 readiness is false or missing.

Completion criteria:

- missing/blocked Stage 1 cannot silently pass.

Stop condition:

- stop if Stage 1 gate shape differs from workplan.

##### Phase 8.Stage 1.Action 2: Test mandatory schema arms

Action:

- test no-contraction and upstream default arms are always included.

Completion criteria:

- removing either mandatory arm fails tests.

Stop condition:

- stop if upstream default cannot be imported.

##### Phase 8.Stage 1.Action 3: Test geometry-schema honesty

Action:

- test that unsupported geometry schemas produce explicit unsupported/block
  rows, not fake successful rows.

Completion criteria:

- schema honesty failure is caught.

Stop condition:

- stop if runtime capabilities cannot be inspected reliably.

##### Phase 8.Stage 1.Action 4: Test required output tables

Action:

- test that a smoke run writes all required result tables with required columns.

Completion criteria:

- missing tables/columns fail tests.

Stop condition:

- stop if table schema needs Project Owner/design revision.

#### Phase 8.Stage 2: Runtime Smoke

##### Phase 8.Stage 2.Action 1: Run Stage 2 smoke

Action:

- run the Stage 2 CLI against a repo-local smoke artifact root using Stage 1
  source.

Completion criteria:

- command completes with pass/warning/block status and writes artifacts.

Stop condition:

- stop on unexpected exception, path drift, or silent arm omission.

##### Phase 8.Stage 2.Action 2: Inspect candidate signal output

Action:

- verify `schema_candidate_signal_summary.csv` and
  `downstream_candidate_input_summary.csv`.

Completion criteria:

- Stage 3 has machine-readable candidate-signal inputs.

Stop condition:

- stop if all arms are missing structured status rows.

#### Phase 8.Stage 3: Final Log Update

##### Phase 8.Stage 3.Action 1: Record validation and handoff

Action:

- update Stage 2 implementation log with:
  - schema families attempted;
  - unsupported families;
  - pass/warning/block status;
  - tests run;
  - Stage 3 handoff paths.

Completion criteria:

- log states whether candidate discovery can proceed.

Stop condition:

- stop if Stage 2 output cannot support Stage 3 without inference.

## Completion Criteria For The Component

Stage 2 is complete when:

- Stage 1 gate is enforced;
- no-contraction and upstream default arms run or block explicitly;
- custom schema families produce honest status rows;
- geometry schemas are implemented honestly or explicitly blocked;
- tower shape, executability, coalescence, collapse, and candidate-signal tables
  exist;
- readout source and seed docs exist;
- CLI/run surface exists or omission is recorded;
- tests pass;
- implementation log records Phase.Stage.Action completion.

## Handoff To Next Component

Candidate discovery must consume:

```text
results/schema_candidate_signal_summary.csv
results/downstream_candidate_input_summary.csv
results/schema_arm_summary.csv
results/schema_construction_summary.csv
results/tower_shape_summary.csv
results/collapse_diagnostic_summary.csv
stage_manifest.json
readout_source.json
```

Candidate discovery must not select candidates directly from raw per-run tower
files when Stage 2 summary tables exist.
