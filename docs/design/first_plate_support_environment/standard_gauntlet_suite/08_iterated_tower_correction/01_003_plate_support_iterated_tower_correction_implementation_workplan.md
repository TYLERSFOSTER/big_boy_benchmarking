# PlateSupport Iterated Tower Correction Implementation Workplan

## Status

Initial implementation workplan.

This workplan is derived from:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/08_iterated_tower_correction/01_002_plate_support_iterated_tower_correction_blueprint.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/08_iterated_tower_correction/01_001_plate_support_iterated_tower_correction_initial_design.md
```

This workplan uses `Phase.Stage.Action` discipline.

This workplan is not execution approval by itself. Execution begins only when
the Project Owner explicitly asks to execute this workplan.

## Prime Directive Binding

This workplan follows:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
docs/prime_directive/common_failure_mode_005_umbrella_workplan_fragmentation.md
docs/prime_directive/git_practices.md
```

Implementation must not silently simplify this workplan.

If an action cannot be implemented as written, the engineer must stop, record
the exact `Phase.Stage.Action` item, explain the blocker, and ask the Project
Owner for guidance.

## Decision Locks Before Implementation

These locks come from the approved blueprint and recent Project Owner
clarifications.

```text
schema_family_id: source_local_ratio_iterated
schema_mode: source_local_ratio_iterated
selector rule: stable threshold/rate selection over quotient representative edges
near-collapse threshold: 0.9
initial ratios: 1/144, 1/72, 1/36, 1/18
initial schema seeds: 0, 1, 2
max iterations: 32
candidate gate: max_depth >= 4 and nontrivial_tier_count >= 3
integration point: gauntlet Stage 2 schema sweep
artifact discipline: do not overwrite historical smoke_001 artifacts
```

The implementation must preserve the existing one-shot `source_local_ratio`
schema family. The new iterated schema family is additive.

## Explicit Non-Goals During Execution

Do not:

- replace the one-shot `SourceLocalOutgoingRatioSchema`;
- treat a single-block schema as "iterated";
- ship a placeholder schema factory;
- create a detached script that cannot feed gauntlet Stage 3 and Stage 4;
- overwrite the historical `smoke_001` artifact root;
- regenerate the human README in a way that erases preserved clarification turns
  without following the readout protocol;
- run Stage 5 or Stage 6 as a success claim if Stage 4 did not find a trainable
  many-tier iterated candidate.

## True Stop Conditions

Stop execution if:

- the upstream PlateSupport runtime cannot accept an iterated schema object;
- `PartitionTower` does not build multiple tiers from ordered blocks as
  expected;
- Stage 2 cannot produce iterated arms without weakening the selector into a
  placeholder;
- the implementation would need to repeat the old `ceil(..., min_selected=1)`
  rule as the default iterated selector;
- candidate discovery cannot preserve enough metadata for Stage 4 to build the
  correct schema class;
- Stage 4 would require reverse-engineering the iterated schema exclusively from
  old one-shot regex assumptions;
- any downstream stage silently drops `schema_family_id`, `schema_mode`,
  `max_depth`, or `nontrivial_tier_count`;
- a test or artifact contradicts the transfer of counterpoint's iterated
  planning architecture to PlateSupport;
- implementation would overwrite or reinterpret historical one-shot artifacts.

## Implementation Log Target

During execution, create and maintain:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/08_iterated_tower_correction/01_004_plate_support_iterated_tower_correction_implementation_log.md
```

The log must record completed `Phase.Stage.Action` items, file changes, test
commands, test outcomes, artifacts generated, surprises, and any Project Owner
clarifications.

## Workplan

### Phase 0: Execution Setup And Reality Binding

#### Phase 0.Stage 1: Verify Repository State

##### Phase 0.Stage 1.Action 1: Verify branch and dirty state

Action:

- Run `git status --short --branch`.
- Record the current branch, dirty files relevant to this work, and unrelated
  dirty files in the implementation log.

Deliverables:

- implementation log entry with branch and dirty-state summary.

Verification:

- no unexamined dirty file is in a path this workplan will modify.

Stop if:

- there are conflicting uncommitted edits in the PlateSupport gauntlet packages
  or correction design folder.

##### Phase 0.Stage 1.Action 2: Create or switch to implementation branch

Action:

- Create or switch to:

```text
codex/plate-support-iterated-tower-correction
```

Deliverables:

- implementation branch active.

Verification:

- `git branch --show-current` reports the branch.

Stop if:

- branch creation or checkout would discard existing work.

##### Phase 0.Stage 1.Action 3: Re-read controlling docs

Action:

- Re-read:
  - this workplan;
  - the blueprint;
  - the initial design;
  - relevant prime directive failure-mode docs;
  - the current PlateSupport gauntlet Stage 2, Stage 3, Stage 4, Stage 5,
    Stage 6, and Stage 7 package files touched by this workplan.

Deliverables:

- implementation log entry confirming controlling docs read.

Verification:

- source paths and expected outputs match the blueprint.

Stop if:

- a newer design artifact contradicts this workplan.

#### Phase 0.Stage 2: Establish Implementation Log

##### Phase 0.Stage 2.Action 1: Create implementation log

Action:

- Create the implementation log file named above.
- Add sections:
  - status;
  - controlling documents;
  - decision locks;
  - `Phase.Stage.Action` progress;
  - commands run;
  - files changed;
  - test results;
  - artifacts generated;
  - blockers and surprises.

Deliverables:

- implementation log file.

Verification:

- log exists and includes all required sections.

Stop if:

- log cannot be created without overwriting an existing unrelated log.

##### Phase 0.Stage 2.Action 2: Add progress table

Action:

- Add a progress table with columns:

```text
Phase.Stage.Action
Status
Files
Verification
Notes
```

Deliverables:

- progress table ready for incremental updates.

Verification:

- every workplan item can be logged in the table.

Stop if:

- the log format would make exact progress tracking ambiguous.

### Phase 1: Runtime Schema And Iterated Planning

#### Phase 1.Stage 1: Inspect Counterpoint Reference And Current PlateSupport Schema

##### Phase 1.Stage 1.Action 1: Re-read counterpoint iterated planner

Action:

- Re-read the counterpoint full-iterated implementation in:

```text
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/runner.py
```

Deliverables:

- implementation log note identifying which helpers are copied structurally.

Verification:

- log names counterpoint helpers such as `_iterated_noisy_rate_plan`,
  `_quotient_representative_edges`, `_iterated_noisy_rate_block_id`, `_find`,
  and `_union`.

Stop if:

- counterpoint implementation has changed in a way that contradicts the
  blueprint.

##### Phase 1.Stage 1.Action 2: Re-read PlateSupport one-shot schema

Action:

- Re-read:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/source_local_ratio_schema.py
```

Deliverables:

- implementation log note explaining which one-shot behavior must remain
  unchanged.

Verification:

- log explicitly names `SourceLocalOutgoingRatioSchema` as preserved.

Stop if:

- implementation would require removing or weakening the one-shot schema.

#### Phase 1.Stage 2: Implement Stable Iterated Schema Helpers

##### Phase 1.Stage 2.Action 1: Add deterministic score helper

Action:

- Add a deterministic hash-to-float helper for PlateSupport iterated selection.
- Use a stable digest such as `sha256`.
- Include selector rule ID, seed, iteration index, source component key, target
  component key, and canonical edge/action key in the score input.

Deliverables:

- stable scoring helper in the PlateSupport schema module or a local helper
  module.

Verification:

- helper does not use Python built-in `hash()`.
- helper returns repeatable values in `[0.0, 1.0)`.

Stop if:

- no stable canonical edge key can be built from the available registry data.

##### Phase 1.Stage 2.Action 2: Add iterated schema ID helper

Action:

- Add:

```python
source_local_ratio_iterated_schema_id(numerator, denominator, max_iterations)
```

- The ID must follow:

```text
plate_support_schema_source_local_ratio_iterated_001_over_144_i032_v001
```

Deliverables:

- schema ID helper.

Verification:

- helper produces zero-padded numerator, denominator, and max-iteration fields.

Stop if:

- existing schema ID conventions require a different shape that would break
  downstream readouts.

##### Phase 1.Stage 2.Action 3: Add iterated block ID helper

Action:

- Add a block ID helper that includes:
  - schema family;
  - numerator;
  - denominator;
  - selector rule ID;
  - seed;
  - iteration index.

Deliverables:

- block ID helper returning `SchemaBlockId`.

Verification:

- block IDs are distinct across iterations.
- block IDs are stable across reruns.

Stop if:

- block IDs cannot include enough material to distinguish iterations.

#### Phase 1.Stage 3: Implement Iterated Schema Class

##### Phase 1.Stage 3.Action 1: Add class skeleton and validation

Action:

- Add `IteratedSourceLocalOutgoingRatioSchema`.
- Include fields:
  - `numerator`;
  - `denominator`;
  - `seed`;
  - `selector_rule_id`;
  - `max_iterations`;
  - `selection_mode`.
- Validate:
  - numerator positive;
  - denominator positive;
  - numerator <= denominator;
  - selector rule ID nonempty;
  - max iterations positive;
  - supported selection mode.

Deliverables:

- schema class with validation.

Verification:

- invalid constructor inputs raise `ValueError`.

Stop if:

- the schema cannot conform to the `assign_edge` / `ordered_blocks` contract
  expected by `PartitionTower`.

##### Phase 1.Stage 3.Action 2: Implement lazy registry-bound plan caching

Action:

- Add `_ensure_plan(registry)` behavior mirroring counterpoint.
- Cache by registry edge signature.
- Store:
  - assignment by edge ID;
  - ordered blocks;
  - plan diagnostics;
  - stop summary.

Deliverables:

- lazy plan cache.

Verification:

- repeated `assign_edge` calls do not recompute the plan for the same registry.

Stop if:

- registry signatures cannot distinguish relevant edge-set changes.

##### Phase 1.Stage 3.Action 3: Implement assign_edge and ordered_blocks

Action:

- Implement `assign_edge(edge_id, registry)` using the cached plan.
- Implement `ordered_blocks()` returning one block per successful iteration.

Deliverables:

- runtime-compatible schema methods.

Verification:

- one-shot `SourceLocalOutgoingRatioSchema` remains unchanged.
- iterated schema returns multiple blocks on a synthetic graph where multiple
  contractions are selected.

Stop if:

- `ordered_blocks()` cannot expose multiple iteration blocks to `PartitionTower`.

##### Phase 1.Stage 3.Action 4: Implement plan_diagnostics and stop_summary accessors

Action:

- Add methods or properties exposing:
  - per-iteration diagnostics;
  - final stop summary.

Deliverables:

- diagnostic accessors for Stage 2 tables.

Verification:

- diagnostics include component counts, candidate count, selected count,
  changed union count, block ID, and stop reason.

Stop if:

- diagnostics cannot be retrieved after `PartitionTower` initialization.

#### Phase 1.Stage 4: Implement Iterated Planning Algorithm

##### Phase 1.Stage 4.Action 1: Add union-find helpers

Action:

- Add `_find`, `_union`, and `_component_count`.
- Copy counterpoint structure where applicable.

Deliverables:

- local union-find helpers.

Verification:

- helpers are deterministic and operate on `StateId` objects.

Stop if:

- helper behavior diverges from counterpoint in a way that changes iteration
  semantics.

##### Phase 1.Stage 4.Action 2: Build quotient representative candidates

Action:

- Implement representative candidate extraction.
- Exclude current self-component edges.
- Group by:

```text
(source_component, target_component, action_key)
```

Deliverables:

- helper returning deterministic representative edge IDs.

Verification:

- representatives are sorted stably.
- already-contracted component-internal edges are skipped.

Stop if:

- action identity cannot be represented stably from `BaseEdge.action`.

##### Phase 1.Stage 4.Action 3: Implement source-local threshold selection

Action:

- Group representative candidates by source component.
- Score candidates deterministically.
- Select candidates with `score < numerator / denominator`.
- Allow zero selected candidates per source component.

Deliverables:

- source-local threshold selector.

Verification:

- selector never uses the old forced `min_selected_per_source=1` behavior.

Stop if:

- implementation would need to force at least one selected edge per source
  component to make any tower appear.

##### Phase 1.Stage 4.Action 4: Implement iteration loop and stop reasons

Action:

- Implement the full iteration loop up to `max_iterations`.
- Record stop reasons:
  - `component_count_leq_one`;
  - `no_candidate_edges`;
  - `no_selected_edges`;
  - `no_component_change`;
  - `max_iterations_reached`;
  - `diagnostic_error`.

Deliverables:

- `_iterated_source_local_ratio_plan(...)`.

Verification:

- plan returns assignment, ordered blocks, diagnostics, and stop summary.

Stop if:

- selected edges do not produce block order that `PartitionTower` can use.

#### Phase 1.Stage 5: Add Runtime Schema Unit Tests

##### Phase 1.Stage 5.Action 1: Test deterministic scoring and IDs

Action:

- Add tests covering stable score repeatability, schema ID shape, and block ID
  uniqueness.

Deliverables:

- unit tests.

Verification:

- tests pass for deterministic repeatability and ID formatting.

Stop if:

- stable score or ID behavior is nondeterministic.

##### Phase 1.Stage 5.Action 2: Test iterated planning on synthetic graph

Action:

- Add a small synthetic registry/graph test or use the smallest convenient
  `PartitionTower` test surface.
- Assert multiple ordered blocks can be produced when selected edges support
  multiple contractions.

Deliverables:

- planner tests independent of the full PlateSupport gauntlet.

Verification:

- test proves the schema is truly iterated, not a one-block stand-in.

Stop if:

- no practical test surface can verify multiple blocks.

### Phase 2: Gauntlet Stage 2 Schema Sweep Integration

#### Phase 2.Stage 1: Extend Stage 2 Configuration And Schema Arms

##### Phase 2.Stage 1.Action 1: Add iterated config fields

Action:

- Update `contraction_schema_sweep/config.py` with blueprint fields:
  - iterated numerators;
  - iterated denominators;
  - max iterations;
  - selector rule ID;
  - selection mode;
  - near-collapse threshold `0.9`;
  - minimum nontrivial tier count.

Deliverables:

- config fields and validation.

Verification:

- defaults match blueprint.

Stop if:

- adding fields breaks existing Stage 2 config construction.

##### Phase 2.Stage 1.Action 2: Enumerate iterated schema arms

Action:

- Update `schema_families.py` to emit `source_local_ratio_iterated` arms.
- Preserve existing one-shot arms.

Deliverables:

- iterated `SchemaArm` rows with required metadata.

Verification:

- schema arms include default ratios `1/144`, `1/72`, `1/36`, `1/18`.

Stop if:

- current `SchemaArm` cannot carry enough metadata for iterated arms.

##### Phase 2.Stage 1.Action 3: Update schema construction reporting

Action:

- Update `schema_builders.py` so iterated arms report:

```text
bbb.plate_support.IteratedSourceLocalOutgoingRatioSchema.full_graph_partition_tower
```

Deliverables:

- construction summary recognizes iterated arms.

Verification:

- existing construction summaries still work for one-shot arms.

Stop if:

- construction reporting conflates one-shot and iterated builders.

#### Phase 2.Stage 2: Build Iterated Stage 2 Diagnostics

##### Phase 2.Stage 2.Action 1: Extract shared PlateSupport graph enumeration helper

Action:

- Refactor only if useful: share the valid-state and valid-transition
  enumeration currently used by one-shot diagnostics.

Deliverables:

- helper for valid states, core states, edges, and current base state.

Verification:

- one-shot diagnostic output remains unchanged.

Stop if:

- refactor would risk unrelated behavior changes.

##### Phase 2.Stage 2.Action 2: Add iterated diagnostics dispatcher

Action:

- Update `schema_runner.py` to call `_run_source_local_ratio_iterated_tower_diagnostics`
  for `schema_mode == "source_local_ratio_iterated"`.

Deliverables:

- dispatcher branch.

Verification:

- one-shot, no-contraction, and upstream-default branches still dispatch as
  before.

Stop if:

- dispatcher cannot access config needed for thresholds and max iterations.

##### Phase 2.Stage 2.Action 3: Implement iterated tower diagnostics

Action:

- Build a `PartitionTower` with `IteratedSourceLocalOutgoingRatioSchema`.
- Extract:
  - tower shape rows;
  - tier occupancy rows;
  - tier executability rows;
  - endpoint coalescence rows;
  - iterated plan rows;
  - iterated stop summary;
  - many-tier candidate signal.

Deliverables:

- complete iterated diagnostics function.

Verification:

- diagnostics include every tier produced by the iterated tower.

Stop if:

- `PartitionTower` does not build multiple layers from ordered iterated blocks.

##### Phase 2.Stage 2.Action 4: Implement candidate signal calculations

Action:

- Implement `many_tier_executable_candidate` semantics:

```text
max_depth >= 4
nontrivial_tier_count >= 3
has_empty_executable_tier == false
has_immediate_collapse == false
max_largest_cell_share < 0.9
```

Deliverables:

- candidate signal rows.

Verification:

- shallow, collapsed, nonexecutable, empty, and diagnostic-error cases are
  distinguishable.

Stop if:

- active executable action-cell count cannot be computed for candidate gating.

#### Phase 2.Stage 3: Write New Stage 2 Tables And Manifests

##### Phase 2.Stage 3.Action 1: Add table fieldnames

Action:

- Add fieldnames for:
  - `iterated_plan_summary.csv`;
  - `iterated_schema_stop_summary.csv`;
  - `many_tier_candidate_signal_summary.csv`.

Deliverables:

- Stage 2 runner knows all new table schemas.

Verification:

- CSV columns match blueprint names.

Stop if:

- current writer infrastructure cannot add optional Stage 2 tables safely.

##### Phase 2.Stage 3.Action 2: Write iterated tables

Action:

- Update Stage 2 runner to collect and write iterated table rows.

Deliverables:

- new CSV outputs under Stage 2 results.

Verification:

- tables are written even when no iterated candidate succeeds, with diagnostic
  status/stop reason rows where appropriate.

Stop if:

- table writing would silently omit failed iterated arms.

##### Phase 2.Stage 3.Action 3: Update manifests and readout source

Action:

- Update Stage 2 manifests/readout source to include new table paths and config
  fields.

Deliverables:

- artifact manifest and readout source reference new iterated tables.

Verification:

- human-readability protocol can discover the new tables through readout source
  metadata.

Stop if:

- new artifacts are not reachable from readout source.

#### Phase 2.Stage 4: Update Stage 2 Docs And Tests

##### Phase 2.Stage 4.Action 1: Update Stage 2 docs writer

Action:

- Explain one-shot versus iterated schema families.
- Include iterated plan/stop/candidate signal summaries in Stage 2 docs.

Deliverables:

- Stage 2 docs mention iterated architecture and stop reasons.

Verification:

- generated docs do not imply the one-shot schema is many-tier.

Stop if:

- docs cannot express the one-shot/iterated distinction clearly.

##### Phase 2.Stage 4.Action 2: Add Stage 2 tests

Action:

- Add tests for iterated arm enumeration, table writing, default ratios,
  candidate signal classification, and backward compatibility.

Deliverables:

- Stage 2 test coverage.

Verification:

- targeted Stage 2 tests pass.

Stop if:

- adding iterated arms breaks existing one-shot tests without a clear expected
  update.

### Phase 3: Gauntlet Stage 3 Candidate Discovery Integration

#### Phase 3.Stage 1: Load And Normalize Iterated Candidate Signals

##### Phase 3.Stage 1.Action 1: Extend Stage 2 source loading

Action:

- Update Stage 3 source loading so `many_tier_candidate_signal_summary.csv` is
  loaded when present.

Deliverables:

- optional iterated signal table loading.

Verification:

- historical Stage 2 sources without the new table still load.

Stop if:

- making the table mandatory breaks historical one-shot artifacts.

##### Phase 3.Stage 1.Action 2: Normalize iterated candidate rows

Action:

- Convert iterated signal rows into candidate rows compatible with existing
  candidate classification and selection.

Deliverables:

- normalized iterated candidate records.

Verification:

- records preserve schema ID, family, seed, ratio, max iterations, selector rule,
  selection mode, max depth, nontrivial tier count, and threshold.

Stop if:

- metadata would be lost before Stage 4.

#### Phase 3.Stage 2: Update Eligibility And Selection

##### Phase 3.Stage 2.Action 1: Classify iterated many-tier candidates

Action:

- Update eligibility/classification so:

```text
source_local_ratio_iterated + many_tier_executable_candidate
```

is eligible for `stage4_training_health`.

Deliverables:

- iterated eligibility classification.

Verification:

- shallow/collapsed/nonexecutable iterated candidates are blocked with reasons.

Stop if:

- classification cannot distinguish iterated candidate signal values.

##### Phase 3.Stage 2.Action 2: Prioritize iterated many-tier candidates

Action:

- Update selection policy so eligible iterated many-tier candidates outrank
  shallow one-shot candidates in correction runs.

Deliverables:

- selection ordering consistent with blueprint.

Verification:

- tests show eligible iterated candidate selected over one-shot candidate.

Stop if:

- selection policy has no way to identify correction-run intent.

##### Phase 3.Stage 2.Action 3: Preserve downstream metadata

Action:

- Ensure selected candidate outputs include:
  - `schema_mode`;
  - `ratio_numerator`;
  - `ratio_denominator`;
  - `max_iterations`;
  - `selector_rule_id`;
  - `selection_mode`;
  - `max_depth`;
  - `nontrivial_tier_count`;
  - `near_full_collapse_threshold`.

Deliverables:

- enriched selected candidate tables/manifests.

Verification:

- Stage 4 can build a schema without reverse-engineering from schema ID alone.

Stop if:

- existing table schemas cannot be extended without breaking downstream readers.

#### Phase 3.Stage 3: Update Stage 3 Docs And Tests

##### Phase 3.Stage 3.Action 1: Update candidate discovery docs writer

Action:

- Explain iterated candidate selection and blocked reasons.

Deliverables:

- Stage 3 generated docs distinguish one-shot and iterated candidates.

Verification:

- docs identify selected candidate architecture.

Stop if:

- docs hide whether the candidate is one-shot or iterated.

##### Phase 3.Stage 3.Action 2: Add Stage 3 tests

Action:

- Add tests for loading iterated signals, selecting iterated candidates,
  preserving metadata, and preserving historical one-shot behavior.

Deliverables:

- Stage 3 test coverage.

Verification:

- targeted Stage 3 tests pass.

Stop if:

- backward compatibility cannot be maintained.

### Phase 4: Gauntlet Stage 4 Tower Training Health Integration

#### Phase 4.Stage 1: Generalize Candidate Source Contract

##### Phase 4.Stage 1.Action 1: Expand TrainingCandidate dataclass

Action:

- Add fields required by blueprint:
  - `schema_mode`;
  - `max_iterations`;
  - `selector_rule_id`;
  - `selection_mode`;
  - `max_depth`;
  - `nontrivial_tier_count`;
  - `near_full_collapse_threshold`.

Deliverables:

- expanded Stage 4 candidate model.

Verification:

- existing one-shot candidates still instantiate with legacy defaults.

Stop if:

- candidate model changes break existing Stage 4 artifacts without migration
  support.

##### Phase 4.Stage 1.Action 2: Replace regex-only parser with metadata-first parser

Action:

- Preserve one-shot regex fallback.
- Add iterated ID support.
- Prefer explicit Stage 3 metadata.

Deliverables:

- metadata-first candidate parsing.

Verification:

- Stage 4 can parse both one-shot and iterated candidates.

Stop if:

- parser must infer iterated max iterations only from old one-shot fields.

#### Phase 4.Stage 2: Build Schema Factory For Training

##### Phase 4.Stage 2.Action 1: Implement training schema factory

Action:

- Add `build_schema_for_training_candidate(candidate)`.
- Return:
  - `SourceLocalOutgoingRatioSchema` for one-shot;
  - `IteratedSourceLocalOutgoingRatioSchema` for iterated.

Deliverables:

- schema factory.

Verification:

- tests assert correct class by `schema_family_id` and `schema_mode`.

Stop if:

- factory would need to return a placeholder for iterated candidates.

##### Phase 4.Stage 2.Action 2: Update build_training_surface

Action:

- Use the schema factory in `training_surfaces.py`.
- Preserve `surface.create_runtime(schema=schema)`.
- Extend training surface manifest metadata.

Deliverables:

- runtime training surface supports iterated schema.

Verification:

- one-shot training still runs.
- iterated training surface construction succeeds.

Stop if:

- upstream runtime rejects iterated schema object.

#### Phase 4.Stage 3: Preserve Multi-Tier Events And Summaries

##### Phase 4.Stage 3.Action 1: Verify deepest-executable-tier behavior

Action:

- Confirm Stage 4 controller already chooses from deepest executable tier.
- Adjust only if it assumes tier 0/1.

Deliverables:

- multi-tier-safe controller behavior.

Verification:

- tier indices beyond 1 are represented when present.

Stop if:

- controller logic cannot operate over arbitrary tier counts.

##### Phase 4.Stage 3.Action 2: Update Stage 4 tables/manifests/docs

Action:

- Preserve schema family/mode/max depth/nontrivial tier count in:
  - training health summary;
  - training surface manifest;
  - run artifacts;
  - generated docs.

Deliverables:

- Stage 4 artifacts carry iterated metadata.

Verification:

- readout source exposes metadata for Stage 5 and human docs.

Stop if:

- Stage 4 output drops iterated candidate identity.

#### Phase 4.Stage 4: Add Stage 4 Tests

##### Phase 4.Stage 4.Action 1: Add parsing and factory tests

Action:

- Test one-shot and iterated candidate parsing.
- Test correct schema class construction.

Deliverables:

- Stage 4 parser/factory tests.

Verification:

- targeted tests pass.

Stop if:

- iterated schema cannot be constructed under test.

##### Phase 4.Stage 4.Action 2: Add training health smoke test

Action:

- Run at least one iterated candidate through a small Stage 4 smoke path.

Deliverables:

- smoke test or integration test.

Verification:

- training episode artifacts contain valid tier/controller/lift events.

Stop if:

- runtime rejects iterated schema or produces no executable tiers.

### Phase 5: Gauntlet Stage 5 Threshold Frontier Integration

#### Phase 5.Stage 1: Preserve Iterated Metadata In Stage 5 Source Loading

##### Phase 5.Stage 1.Action 1: Update Stage 5 source models

Action:

- Update threshold frontier source loading to preserve:
  - schema family;
  - schema mode;
  - max depth;
  - nontrivial tier count;
  - selector rule;
  - selection mode.

Deliverables:

- Stage 5 source model supports iterated candidates.

Verification:

- one-shot Stage 4 sources still load.

Stop if:

- Stage 5 cannot distinguish iterated and one-shot training candidates.

##### Phase 5.Stage 1.Action 2: Add iterated metadata to manifests

Action:

- Include iterated metadata in threshold policy manifests and stage manifests.

Deliverables:

- Stage 5 manifests preserve architecture.

Verification:

- generated artifacts make clear whether calibration used an iterated candidate.

Stop if:

- manifest schema cannot be extended safely.

#### Phase 5.Stage 2: Guard Calibration On Trainable Iterated Candidate

##### Phase 5.Stage 2.Action 1: Add correction-run gate

Action:

- Ensure Stage 5 blocks cleanly if a correction run has no trainable iterated
  candidate.

Deliverables:

- explicit blocked status and reason.

Verification:

- blocked artifacts do not masquerade as calibrated threshold.

Stop if:

- Stage 5 would silently calibrate against a one-shot candidate in an iterated
  correction run.

##### Phase 5.Stage 2.Action 2: Update Stage 5 docs and tests

Action:

- Update docs writer and tests for iterated metadata.

Deliverables:

- Stage 5 readout/test updates.

Verification:

- targeted Stage 5 tests pass.

Stop if:

- docs imply calibration target came from an unspecified architecture.

### Phase 6: Gauntlet Stage 6 Paired Replicate Comparison Integration

#### Phase 6.Stage 1: Preserve Iterated Candidate Metadata In Stage 6

##### Phase 6.Stage 1.Action 1: Update Stage 6 source loading and arms

Action:

- Preserve schema family/mode/max depth/nontrivial tier count through paired
  comparison source models and arm definitions.

Deliverables:

- paired arms retain iterated identity.

Verification:

- direct baseline remains unchanged.
- tower candidate arm records iterated metadata.

Stop if:

- paired comparison cannot know which schema class to build.

##### Phase 6.Stage 1.Action 2: Share or mirror Stage 4 schema factory

Action:

- Use the same schema-building logic as Stage 4, either by sharing a helper or
  mirroring with tests.

Deliverables:

- Stage 6 tower arm builds `IteratedSourceLocalOutgoingRatioSchema` when
  candidate is iterated.

Verification:

- tests assert correct schema class in paired comparison.

Stop if:

- Stage 6 would rebuild iterated candidate as one-shot.

#### Phase 6.Stage 2: Make Aggregation Multi-Tier Safe

##### Phase 6.Stage 2.Action 1: Audit tier aggregation assumptions

Action:

- Search Stage 6 aggregation/docs for hard-coded tier 0/1 assumptions.

Deliverables:

- fixes for any two-tier assumptions.

Verification:

- aggregation handles arbitrary tier indices.

Stop if:

- tier summaries cannot represent more than two tiers.

##### Phase 6.Stage 2.Action 2: Update paired comparison docs and tests

Action:

- Report tower depth/nontrivial tier count prominently.
- Add tests for iterated metadata and multi-tier event aggregation.

Deliverables:

- Stage 6 docs/tests.

Verification:

- targeted Stage 6 tests pass.

Stop if:

- docs hide whether comparison used one-shot or iterated tower.

### Phase 7: Gauntlet Stage 7 Readout And System Learning Integration

#### Phase 7.Stage 1: Update Readout Inputs And Badges

##### Phase 7.Stage 1.Action 1: Add iterated tower status fields to readout source

Action:

- Ensure top-level gauntlet readout source can expose:
  - iterated tower status;
  - nontrivial tier count;
  - executable tier health;
  - ratio sweep status;
  - selected iterated candidate metadata.

Deliverables:

- readout source includes iterated summary inputs.

Verification:

- human-readability protocol has table/source access to these facts.

Stop if:

- facts only exist buried in raw CSVs and not readout source.

##### Phase 7.Stage 1.Action 2: Add badges for iterated correction

Action:

- Add badges:
  - `Iterated Tower`;
  - `Nontrivial Tiers`;
  - `Executable Tiers`;
  - `Ratio Sweep`;
  - `Candidate`;
  - `Provenance`.

Deliverables:

- badge generation support.

Verification:

- badges follow the existing visual style used by other reports.

Stop if:

- badge style diverges from established readout conventions.

#### Phase 7.Stage 2: Update Human Readout Text

##### Phase 7.Stage 2.Action 1: Update generated README sections

Action:

- Ensure generated README says:
  - whether run is one-shot or iterated;
  - how many nontrivial tiers were found;
  - whether a many-tier candidate was selected;
  - where the tower stopped if no candidate was found.

Deliverables:

- generated standard gauntlet README/readout content.

Verification:

- README cannot be mistaken for the historical one-shot `smoke_001` result.

Stop if:

- generated readout erases preserved clarification conversation contrary to
  protocol.

##### Phase 7.Stage 2.Action 2: Update artifact protocol only if required

Action:

- Update `docs/prime_directive/artifact_table_to_readable_document_protocol.md`
  only if the existing protocol cannot express iterated tower diagnostics.

Deliverables:

- protocol update or log note explaining no protocol change was needed.

Verification:

- human-readable report can be generated from the correction readout source.

Stop if:

- protocol change would alter unrelated evaluation report semantics.

### Phase 8: CLI And Artifact-Root Integration

#### Phase 8.Stage 1: Add CLI Flags

##### Phase 8.Stage 1.Action 1: Expose iterated Stage 2 schema-sweep controls

Action:

- Add CLI flags equivalent to:

```text
--include-iterated-source-local-ratio
--iterated-source-local-denominators 144,72,36,18
--iterated-source-local-max-iterations 32
--iterated-near-full-collapse-threshold 0.9
```

Deliverables:

- CLI can run Stage 2 correction without Python config edits.

Verification:

- CLI help includes flags.
- default behavior without flags remains compatible.

Stop if:

- flags would unintentionally change existing default smoke gauntlet behavior.

##### Phase 8.Stage 1.Action 2: Preserve artifact root discipline

Action:

- Ensure docs and examples use a new run label:

```text
iterated_tower_correction_001
```

Deliverables:

- command examples and run paths avoid `smoke_001` overwrite.

Verification:

- generated artifacts go under new run-label root.

Stop if:

- CLI defaults would overwrite historical one-shot artifacts.

#### Phase 8.Stage 2: Add CLI Tests

##### Phase 8.Stage 2.Action 1: Test CLI flag parsing

Action:

- Add tests for new schema-sweep flags.

Deliverables:

- CLI tests.

Verification:

- parsed config matches blueprint defaults and overrides.

Stop if:

- CLI parser cannot represent denominator list cleanly.

### Phase 9: End-To-End Verification

#### Phase 9.Stage 1: Run Targeted Tests

##### Phase 9.Stage 1.Action 1: Run schema and Stage 2 tests

Action:

- Run targeted tests for:
  - iterated schema planning;
  - Stage 2 schema sweep.

Deliverables:

- test output recorded in implementation log.

Verification:

- tests pass.

Stop if:

- iterated schema tests fail or prove only one block is produced.

##### Phase 9.Stage 1.Action 2: Run Stage 3 and Stage 4 tests

Action:

- Run targeted tests for:
  - candidate discovery;
  - tower training health.

Deliverables:

- test output recorded in implementation log.

Verification:

- tests pass.

Stop if:

- Stage 4 cannot build or train an iterated candidate.

##### Phase 9.Stage 1.Action 3: Run downstream Stage 5, Stage 6, Stage 7 tests

Action:

- Run targeted tests for:
  - threshold frontier calibration;
  - paired replicate comparison;
  - readout/system learning.

Deliverables:

- test output recorded in implementation log.

Verification:

- tests pass.

Stop if:

- downstream stages drop iterated metadata.

#### Phase 9.Stage 2: Run Correction Smoke Through Stage 4

##### Phase 9.Stage 2.Action 1: Run Stage 1 if needed

Action:

- Ensure Stage 1 structural/tower diagnostics readout source exists for the
  correction artifact root or can be reused safely.

Deliverables:

- Stage 1 source path recorded.

Verification:

- Stage 2 can consume the Stage 1 source.

Stop if:

- Stage 1 source is missing or stale in a way that invalidates correction run.

##### Phase 9.Stage 2.Action 2: Run Stage 2 iterated schema sweep

Action:

- Run Stage 2 with the iterated correction run label and iterated flags.

Deliverables:

- Stage 2 correction artifacts.

Verification:

- iterated tables exist.
- at least one iterated arm has explicit stop summary.

Stop if:

- Stage 2 produces no iterated diagnostics.

##### Phase 9.Stage 2.Action 3: Run Stage 3 candidate discovery

Action:

- Run Stage 3 against the correction Stage 2 readout source.

Deliverables:

- Stage 3 correction artifacts.

Verification:

- Stage 3 either selects an iterated many-tier candidate or records clear
  no-candidate reasons.

Stop if:

- Stage 3 selects a shallow one-shot candidate in a correction run.

##### Phase 9.Stage 2.Action 4: Run Stage 4 tower training health

Action:

- Run Stage 4 against the correction Stage 3 readout source.

Deliverables:

- Stage 4 correction artifacts.

Verification:

- if candidate exists, Stage 4 trains with an iterated schema and records
  multi-tier events.

Stop if:

- Stage 4 cannot construct or train the iterated candidate.

#### Phase 9.Stage 3: Conditional Downstream Smoke

##### Phase 9.Stage 3.Action 1: Decide whether Stage 5/6 are permitted by artifacts

Action:

- Inspect Stage 4 aggregate status and candidate health.

Deliverables:

- implementation log decision entry.

Verification:

- Stage 5/6 proceed only if Stage 4 found a trainable many-tier iterated
  candidate.

Stop if:

- no trainable many-tier iterated candidate exists.

##### Phase 9.Stage 3.Action 2: Run Stage 5 and Stage 6 only if permitted

Action:

- If permitted, run threshold calibration and paired comparison using the
  correction artifact root.

Deliverables:

- Stage 5/6 correction artifacts or logged stop reason.

Verification:

- downstream artifacts preserve iterated metadata.

Stop if:

- Stage 5/6 would compare a one-shot candidate in place of the iterated
  candidate.

##### Phase 9.Stage 3.Action 3: Run Stage 7 readout/system learning

Action:

- Generate the correction readout/system-learning surface.

Deliverables:

- updated human-readable correction readout source and docs.

Verification:

- README/top-level readout distinguishes one-shot versus iterated correction.

Stop if:

- readout misstates the correction result or hides stop reasons.

### Phase 10: Documentation, Logs, And Final Verification

#### Phase 10.Stage 1: Update Design Folder Documentation

##### Phase 10.Stage 1.Action 1: Update implementation log final summary

Action:

- Record:
  - completed actions;
  - skipped conditional actions;
  - stop reasons, if any;
  - generated artifacts;
  - tests run;
  - whether the correction produced a trainable many-tier candidate.

Deliverables:

- final implementation log summary.

Verification:

- log does not conceal simplifications or unresolved blockers.

Stop if:

- any action was implemented differently from the workplan without PO approval.

##### Phase 10.Stage 1.Action 2: Update correction folder README

Action:

- Add links to implementation workplan and implementation log.
- Record current status after execution.

Deliverables:

- updated correction folder README.

Verification:

- future engineers can find design, blueprint, workplan, log, and artifact
  outputs.

Stop if:

- README would imply execution occurred before it did.

#### Phase 10.Stage 2: Final Repository Verification

##### Phase 10.Stage 2.Action 1: Run final targeted test set

Action:

- Run the smallest complete targeted test set covering all touched packages.

Deliverables:

- final test command and result in implementation log.

Verification:

- targeted tests pass.

Stop if:

- tests fail and failure cannot be fixed within the approved workplan.

##### Phase 10.Stage 2.Action 2: Check git diff and attribution hygiene

Action:

- Review `git diff --stat`.
- Search changed design/workplan/readout files for fake PO turn formatting.

Deliverables:

- final diff and attribution-hygiene note.

Verification:

- no false Project Owner attribution exists.

Stop if:

- any model-authored content is under a Project Owner heading.

##### Phase 10.Stage 2.Action 3: Report completion state

Action:

- Report:
  - branch;
  - files changed;
  - tests run;
  - artifacts generated;
  - whether a many-tier candidate was found;
  - whether Stage 5/6 were run or blocked by artifact gates;
  - remaining risks.

Deliverables:

- concise final report to Project Owner.

Verification:

- final report matches implementation log and artifacts.

Stop if:

- final state cannot be reconciled with artifacts.

## Expected First Execution Branch

Use:

```text
codex/plate-support-iterated-tower-correction
```

## Expected Correction Run Label

Use:

```text
iterated_tower_correction_001
```

## Expected Human-Readable Regeneration Command

After the correction run produces an appropriate readout source, use the exact
protocol-file form:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <readout_source.json>
```

For example:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-root>/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```

Only use that example if the top-level readout source is the intended correction
readout source for the new run label.

## Completion Definition

This workplan is complete when:

- the iterated schema family exists and is tested;
- Stage 2 can produce iterated tower diagnostics and plan tables;
- Stage 3 can select an eligible iterated many-tier candidate or explain why
  none exists;
- Stage 4 can train an iterated candidate if selected;
- Stage 5/6 either run against the iterated candidate or stop cleanly because no
  trainable many-tier candidate exists;
- Stage 7/readout surfaces clearly explain the result;
- all relevant tests have been run and logged;
- historical one-shot artifacts remain intact.
