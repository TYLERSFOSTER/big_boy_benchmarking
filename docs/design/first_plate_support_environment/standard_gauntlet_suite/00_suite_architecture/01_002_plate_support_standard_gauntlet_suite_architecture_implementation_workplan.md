# PlateSupport Standard Gauntlet Suite Architecture Implementation Workplan

## Status

Status: initial implementation workplan.

This document is generated from:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/00_suite_architecture/01_001_plate_support_standard_gauntlet_suite_architecture_blueprint.md
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
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`;
- `docs/prime_directive/git_practices.md`.

Operational consequences:

- Do not execute this workplan until the Project Owner explicitly approves
  execution.
- Once approved, execute `Phase.Stage.Action` items in order unless the Project
  Owner explicitly authorizes reordering.
- Do not silently replace this architecture work with a smaller "just enough"
  scaffold.
- Stop if an action requires choosing among unresolved Project Owner questions.
- Record execution in an implementation log before source edits begin.
- Do not attribute consultant-authored defaults to the Project Owner.

## Authority And Attribution

Project Owner direction from the current request:

- create detailed implementation workplans for every standard gauntlet
  component;
- do the workplans one after another, not in parallel;
- follow the component blueprints;
- use `Phase.Stage.Action` format;
- follow `prime_directive`;
- reference work already done as the workplans proceed.

Consultant-authored assumptions pending Project Owner override:

- suite id remains `plate_support_standard_gauntlet_v001`;
- first implementation run label defaults to `smoke_001`;
- implementation uses staged workplans rather than one monolithic workplan;
- suite implementation lives under a new PlateSupport standard-gauntlet
  subpackage;
- durable artifact roots live under
  `docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/`;
- environment readiness remains an input under
  `docs/environments/plate_support_5x5_default_v001/readiness/`.

These assumptions are consultant-authored. If the Project Owner rejects any of
them, revise this workplan before execution.

## Decision Locks Before Implementation

- This component implements shared suite architecture only.
- Do not implement stage-specific diagnostics, schema sweeps, training loops,
  calibration runs, comparison runs, or readout generation in this component.
- Do not edit `/Users/foster/state_collapser`.
- Do not write durable artifacts outside the repository evaluation tree.
- Do not treat environment readiness as an evaluation result.
- Do not claim tower benefit.
- Do not copy counterpoint ids or thresholds into PlateSupport.
- Every later stage must consume the shared suite IDs, path contracts, status
  vocabulary, manifest helpers, and gate machinery created here.

## Expected Final Deliverables

Implementation should produce or update:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/
tests/environments/plate_support/test_standard_gauntlet_architecture.py
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/
docs/design/first_plate_support_environment/standard_gauntlet_suite/00_suite_architecture/01_003_plate_support_standard_gauntlet_suite_architecture_implementation_log.md
```

Recommended package files:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/__init__.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/ids.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paths.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/status.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/manifests.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/gates.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/readout_source.py
```

The architecture component should expose no claim-bearing CLI command by itself.
If a CLI surface is added, it should be limited to architecture validation or
suite scaffold inspection.

## Workplan

### Phase 0: Execution Setup And Reality Binding

#### Phase 0.Stage 1: Re-anchor Repository State

##### Phase 0.Stage 1.Action 1: Verify branch and working tree

Action:

- run `git status --short --branch`;
- record branch name, upstream status, and dirty files in the implementation
  log.

Completion criteria:

- active branch is known;
- dirty files are known before edits.

Stop condition:

- stop if unrelated dirty files would be overwritten or confused with this
  suite architecture work.

##### Phase 0.Stage 1.Action 2: Create or switch to implementation branch

Action:

- create or switch to a dedicated branch:

```text
codex/plate-support-standard-gauntlet-suite
```

Completion criteria:

- implementation branch is active;
- branch choice is recorded in the implementation log.

Stop condition:

- stop if switching branches would hide or overwrite uncommitted work.

##### Phase 0.Stage 1.Action 3: Re-read controlling documents

Action:

- re-read:
  - this workplan;
  - the suite architecture blueprint;
  - the PlateSupport environment doc;
  - the PlateSupport environment build log;
  - `evaluation_construction_for_readable_artifacts_protocol.md`;
  - `artifact_table_to_readable_document_protocol.md`;
  - the workplan rewrite failure-mode doc;
  - the false-attribution failure-mode doc.

Completion criteria:

- implementation log records source documents read.

Stop condition:

- stop if a newer design document contradicts this workplan.

#### Phase 0.Stage 2: Establish Implementation Log

##### Phase 0.Stage 2.Action 1: Create architecture implementation log

Action:

- create:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/00_suite_architecture/01_003_plate_support_standard_gauntlet_suite_architecture_implementation_log.md
```

Minimum sections:

```text
# PlateSupport Standard Gauntlet Suite Architecture Implementation Log

## Status
## Branch And Repo State
## Source Documents
## Phase.Stage.Action Progress
## Commands Run
## Files Changed
## Tests And Validation
## Surprises / Stop Conditions
## Final Summary
```

Completion criteria:

- implementation log exists before source edits.

Stop condition:

- stop if the log path conflicts with an existing unrelated file.

##### Phase 0.Stage 2.Action 2: Add progress table

Action:

- add a progress table with columns:

```text
Phase.Stage.Action
Status
Evidence
Notes
```

Completion criteria:

- every later action can be tracked as `pending`, `in_progress`, `completed`,
  or `blocked`.

Stop condition:

- stop if the workplan would need to be rewritten during implementation.

### Phase 1: Suite Identity And Package Skeleton

#### Phase 1.Stage 1: Create Standard Gauntlet Package

##### Phase 1.Stage 1.Action 1: Create package directory

Action:

- create:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/
```

Completion criteria:

- package directory exists;
- no stage-specific subpackages are created yet.

Stop condition:

- stop if the directory already exists with unrelated content.

##### Phase 1.Stage 1.Action 2: Add package initializer

Action:

- create `__init__.py`;
- export only stable architecture-level symbols needed by later stages.

Completion criteria:

- package imports cleanly;
- no stage-specific runtime is exposed.

Stop condition:

- stop if adding exports would require implementing later stages.

#### Phase 1.Stage 2: Define Stable IDs

##### Phase 1.Stage 2.Action 1: Implement suite and stage IDs

Action:

- create `ids.py`;
- define constants for:
  - `SUITE_ID`;
  - `SUITE_RUN_FAMILY_ID`;
  - `ENVIRONMENT_FAMILY_ID`;
  - `ENVIRONMENT_INSTANCE_ID`;
  - `LINEARIZATION_MODE_ID`;
  - every stage id from the architecture blueprint.

Completion criteria:

- all stage IDs match the blueprint exactly;
- tests can import every ID.

Stop condition:

- stop if any ID conflicts with an existing PlateSupport environment ID.

##### Phase 1.Stage 2.Action 2: Define stage ordering

Action:

- add an ordered stage definition tuple/list mapping:
  - stage number;
  - stage id;
  - short name;
  - required predecessor stage ids.

Completion criteria:

- the dependency chain matches the blueprint:
  structural -> sweep -> candidate -> health -> calibration -> comparison ->
  readout.

Stop condition:

- stop if a child blueprint requires a different dependency order.

### Phase 2: Suite Path Contract

#### Phase 2.Stage 1: Implement Path Helpers

##### Phase 2.Stage 1.Action 1: Add suite readout path helper

Action:

- create `paths.py`;
- implement a helper that resolves:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/
```

from an explicit repository root argument.

Completion criteria:

- helper does not rely on ambient current working directory;
- helper returns a repo-relative or absolute path consistently by contract.

Stop condition:

- stop if existing BBB path helpers require a different pattern.

##### Phase 2.Stage 1.Action 2: Add raw artifact root helper

Action:

- implement artifact-root path construction:

```text
<repo_readout_surface>/artifacts/<run_label>/
```

Completion criteria:

- `smoke_001`, `dev_001`, `calibration_001`, and `serious_001` labels are
  supported as strings without hard-coding only one.

Stop condition:

- stop if a path would point outside `docs/evaluations/`.

##### Phase 2.Stage 1.Action 3: Add readiness source path helper

Action:

- implement readiness-source path construction:

```text
docs/environments/plate_support_5x5_default_v001/readiness/<run_label>/readout_source.json
```

Completion criteria:

- environment readiness path is distinct from suite evaluation path.

Stop condition:

- stop if implementation starts copying readiness artifacts into evaluation
  artifacts without an explicit stage action.

#### Phase 2.Stage 2: Add Path Tests

##### Phase 2.Stage 2.Action 1: Test path invariants

Action:

- add tests that verify:
  - repo readout surface is under `docs/evaluations`;
  - raw artifact root is under the readout surface;
  - readiness source is under `docs/environments`;
  - no helper depends on `Path.cwd()`.

Completion criteria:

- tests fail if the three path roles are collapsed.

Stop condition:

- stop if tests require implementing stage-specific artifacts.

### Phase 3: Status Vocabulary And Gate Contract

#### Phase 3.Stage 1: Implement Shared Status Vocabulary

##### Phase 3.Stage 1.Action 1: Create status definitions

Action:

- create `status.py`;
- define suite claim/status vocabulary from the architecture blueprint:
  - `environment_ready`;
  - `diagnostic_complete`;
  - `diagnostic_blocked`;
  - `candidate_found`;
  - `candidate_not_found`;
  - `trainable_clean`;
  - `trainable_warning`;
  - `training_health_blocked`;
  - `threshold_calibrated`;
  - `threshold_unresolved`;
  - `paired_comparison_positive_signal`;
  - `paired_comparison_negative_signal`;
  - `paired_comparison_inconclusive`;
  - `artifact_incomplete`;
  - `protocol_blocked`.

Completion criteria:

- vocabulary is importable by later stages;
- tests cover all blueprint statuses.

Stop condition:

- stop if existing repo status enums already own these names and require reuse.

##### Phase 3.Stage 1.Action 2: Define stage status row shape

Action:

- define a dataclass or typed dict for stage status rows with:
  - suite id;
  - stage id;
  - environment family id;
  - environment instance id;
  - artifact root;
  - status;
  - claim status;
  - claim boundary;
  - source stage ids;
  - source artifact paths;
  - linearization mode id;
  - state_collapser dependency status.

Completion criteria:

- row shape matches the blueprint shared artifact contract.

Stop condition:

- stop if existing shared artifact machinery already provides an incompatible
  required row type.

#### Phase 3.Stage 2: Implement Gate Definitions

##### Phase 3.Stage 2.Action 1: Create gate predicates

Action:

- create `gates.py`;
- implement data-only gate definitions for Stages 1 through 7;
- each gate should list required predecessor statuses and required source
  artifact roles.

Completion criteria:

- gates can be inspected without running any evaluation;
- Stage 6 gate requires candidate, training-health, calibrated-target, and seed
  policy sources.

Stop condition:

- stop if implementing gates would require actual stage execution logic.

##### Phase 3.Stage 2.Action 2: Add gate tests

Action:

- add tests that verify:
  - Stage 2 requires Stage 1;
  - Stage 3 requires Stage 2;
  - Stage 4 requires Stage 3;
  - Stage 5 requires Stage 1 and Stage 4;
  - Stage 6 requires Stages 3, 4, and 5;
  - Stage 7 can run after at least one artifact-producing stage.

Completion criteria:

- dependency mistakes fail tests.

Stop condition:

- stop if a child-stage blueprint contradicts the architecture dependency map.

### Phase 4: Suite Manifest And Readout Source Foundations

#### Phase 4.Stage 1: Implement Manifest Builders

##### Phase 4.Stage 1.Action 1: Create suite manifest builder

Action:

- create `manifests.py`;
- implement a function or dataclass that builds:

```text
evaluation_manifest.json
evaluation_stage_manifest.json
evaluation_budget_lock.json
environment_source_manifest.json
readiness_source_manifest.json
```

from explicit arguments.

Completion criteria:

- manifest builders accept explicit roots and run labels;
- manifest builders do not write files yet unless called by a later action.

Stop condition:

- stop if manifest builder requires unresolved budget decisions.

##### Phase 4.Stage 1.Action 2: Add budget-lock shape

Action:

- define budget-lock fields for:
  - run label;
  - stage IDs included;
  - environment instance ID;
  - dependency state;
  - seed bundle policy;
  - replicate policy;
  - episode/step budget;
  - threshold/success rule;
  - candidate source;
  - linearization mode;
  - locked-by operator.

Completion criteria:

- missing required fields are detectable in tests.

Stop condition:

- stop if work requires choosing serious-run budgets not locked by Project
  Owner.

#### Phase 4.Stage 2: Implement Readout Source Builder

##### Phase 4.Stage 2.Action 1: Create readout source builder

Action:

- create `readout_source.py`;
- implement a builder for suite-level `readout_source.json` with:
  - `repo_readout_surface`;
  - `source_artifact_root`;
  - suite id;
  - environment ids;
  - run label;
  - stage readout source paths;
  - expected file policy placeholder populated from known architecture files;
  - goal and methodology source references.

Completion criteria:

- the builder can produce a JSON-serializable mapping;
- the invocation target is the repo-side `readout_source.json`, not the artifact
  directory.

Stop condition:

- stop if source binding would need to infer "last run."

##### Phase 4.Stage 2.Action 2: Add source-binding tests

Action:

- test that the generated source binding:
  - points to repo-resident artifacts;
  - distinguishes readout surface from artifact root;
  - includes goal/methodology source references;
  - includes expected-file policy.

Completion criteria:

- tests enforce the readout protocol path invariants.

Stop condition:

- stop if readout source fields differ from the current prime-directive
  protocol.

### Phase 5: Suite Scaffold Material

#### Phase 5.Stage 1: Create Repo Readout Surface Skeleton

##### Phase 5.Stage 1.Action 1: Create standard gauntlet evaluation folder

Action:

- create:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/
```

Completion criteria:

- folder exists;
- no raw run artifacts are generated by this architecture component.

Stop condition:

- stop if the Project Owner has not authorized creating evaluation readout
  folders yet.

##### Phase 5.Stage 1.Action 2: Add seed human-doc stubs

Action:

- add initial, non-result seed files:
  - `README.md`;
  - `method.md`;
  - `runbook.md`;
  - `artifact_index.md`;
  - `results/summary.md`.

Completion criteria:

- files clearly state that no suite run has executed yet;
- files do not contain fake results.

Stop condition:

- stop if any generated text would imply evaluation completion.

#### Phase 5.Stage 2: Write Suite Readout Source Skeleton

##### Phase 5.Stage 2.Action 1: Generate initial `readout_source.json`

Action:

- use the readout source builder to write:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```

for the chosen first run label.

Completion criteria:

- source binding points to a future artifact root under the same readout
  surface;
- expected files are classified as pending/not-yet-run where appropriate.

Stop condition:

- stop if the source binding would point to non-existent artifacts as though
  they were complete.

### Phase 6: CLI Or Inspection Surface

#### Phase 6.Stage 1: Decide Whether To Add A CLI Surface

##### Phase 6.Stage 1.Action 1: Inspect existing CLI organization

Action:

- inspect `src/big_boy_benchmarking/cli/main.py` and nearby environment CLI
  patterns.

Completion criteria:

- implementation log records whether adding a suite architecture command fits
  current CLI style.

Stop condition:

- stop if CLI additions require stage execution semantics.

##### Phase 6.Stage 1.Action 2: Add architecture validation command if local pattern supports it

Action:

- if consistent with existing CLI style, add a command such as:

```text
plate-support standard-gauntlet inspect-architecture
```

- command should print suite ids, stage ids, paths, and gates only.

Completion criteria:

- command does not run diagnostics, training, calibration, or comparison;
- command output is JSON and testable.

Stop condition:

- stop if command naming or CLI grouping is ambiguous.

### Phase 7: Verification

#### Phase 7.Stage 1: Run Focused Tests

##### Phase 7.Stage 1.Action 1: Run architecture tests

Action:

- run focused tests for standard gauntlet architecture helpers.

Completion criteria:

- all architecture tests pass.

Stop condition:

- stop on unexpected failure and diagnose before editing further.

##### Phase 7.Stage 1.Action 2: Run import smoke

Action:

- run a Python import smoke for the new package and public exports.

Completion criteria:

- standard gauntlet package imports without executing stage code.

Stop condition:

- stop if import causes artifact writes or stage execution.

#### Phase 7.Stage 2: Validate Documentation And Attribution

##### Phase 7.Stage 2.Action 1: Scan for false attribution

Action:

- scan new docs for the forbidden attribution patterns named in
  `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`,
  including fake response slots, fake decision statements, fake preference
  statements, and fake turn headings.

Completion criteria:

- no false-attribution patterns exist.

Stop condition:

- stop and correct if any false attribution appears.

##### Phase 7.Stage 2.Action 2: Record final architecture implementation summary

Action:

- update implementation log with:
  - files changed;
  - tests run;
  - any unresolved questions;
  - whether downstream Stage 1 workplan can proceed.

Completion criteria:

- log records completion status and evidence.

Stop condition:

- stop if log would misrepresent incomplete work as complete.

## Completion Criteria For The Component

This architecture component is complete when:

- stable suite and stage IDs exist in source;
- path helpers preserve the readout/artifact/readiness distinction;
- shared status vocabulary exists;
- gate definitions encode stage dependencies;
- manifest/readout source builders exist;
- optional architecture inspection CLI exists or is explicitly omitted with
  reason;
- focused tests pass;
- docs contain no false Project Owner attribution;
- implementation log records the completed `Phase.Stage.Action` items.

## Handoff To Next Component

The next component workplan,

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/01_structural_and_tower_diagnostics/01_002_plate_support_structural_and_tower_diagnostics_implementation_workplan.md
```

must consume the architecture outputs from this component rather than
redeclaring suite IDs, path contracts, status vocabulary, or gate semantics.
