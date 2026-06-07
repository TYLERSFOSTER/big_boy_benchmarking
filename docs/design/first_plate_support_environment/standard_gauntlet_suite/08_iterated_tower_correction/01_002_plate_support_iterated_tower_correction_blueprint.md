# PlateSupport Iterated Tower Correction Blueprint

## Status

Initial blueprint.

This blueprint is derived from:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/08_iterated_tower_correction/01_001_plate_support_iterated_tower_correction_initial_design.md
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/README.md
```

It records the architecture needed to correct the PlateSupport standard gauntlet so it can discover and use many nontrivial tower tiers, rather than only the current one-shot two-tier `source_local_ratio` candidate.

This is not an implementation workplan. A later implementation workplan must translate this blueprint into `Phase.Stage.Action` execution steps.

## Attribution And Decision Locks

### Project Owner Inputs

The following points are directly grounded in Project Owner instructions or clarifications:

- The desired correction is an iterated PlateSupport source-local-ratio schema.
- The iterated design should copy counterpoint's iterated planning shape where that makes sense.
- The first correction should be diagnostic/tower-shape focused if that matches how the counterpoint version works.
- Iterated candidates must feed Stage 3 and Stage 4 only after producing many nontrivial executable tiers.
- Downstream candidate parsing and training surfaces must stop assuming that every selected PlateSupport tower candidate is the old one-shot schema.
- The `0.9` threshold is accepted as the near-collapse/largest-cell-share threshold for this design.

### Consultant Interpretation

The Project Owner's `0.9` clarification is interpreted here as:

```text
near_full_collapse_threshold = 0.9
```

Meaning: a nonbase tier whose largest state cell contains at least 90 percent of base-state mass is treated as near-collapsed for candidate eligibility and readout purposes.

### Blueprint Defaults

Unless the Project Owner later changes these, this blueprint uses:

```text
schema_family_id: source_local_ratio_iterated
selector rule: stable threshold/rate selection over quotient representative edges
near-collapse threshold: 0.9
initial ratios: 1/144, 1/72, 1/36, 1/18
initial schema seeds: 0, 1, 2
max iterations: 32
candidate gate: max_depth >= 4 and nontrivial_tier_count >= 3
integration point: gauntlet Stage 2 schema sweep, not a detached script
```

These defaults are implementation-authorizing assumptions only after this blueprint and its associated workplan are approved.

## Problem Statement

The first PlateSupport standard gauntlet completed all seven gauntlet stages, but the selected tower candidate was only a two-tier one-shot quotient:

| Tier | State Cells | Action Cells |
| ---: | ---: | ---: |
| 0 | 89 | 388 |
| 1 | 10 | 116 |

That candidate is valid evidence for the first smoke gauntlet, but it does not satisfy the PO goal of many nontrivial tiers.

The current Stage 6 paired comparison also showed a mixed signal:

| Arm | Binary Target Hits | Episodes | Hit Rate | Mean Reward | Invalid Moves |
| --- | ---: | ---: | ---: | ---: | ---: |
| direct concrete baseline | 15 | 128 | 0.1171875 | -78.71875 | 2142 |
| selected tower candidate | 6 | 128 | 0.046875 | -44.515625 | 0 |

The tower candidate underperformed the direct baseline on the locked binary target, but it produced cleaner behavior and zero invalid moves.

The architecture issue is more basic than the Stage 6 result: the candidate was shallow. The current PlateSupport schema family is one-shot. It creates one quotient layer and stops. It is not an iterated tower-construction mechanism.

## Design Goal

Add an iterated PlateSupport source-local-ratio tower family that can:

1. Repeatedly select contraction blocks on quotient representative edges.
2. Build multiple ordered tower tiers through `PartitionTower`.
3. Preserve source-local selection meaning.
4. Avoid the current "at least one edge per source" collapse behavior as the default many-tier search path.
5. Emit explicit artifacts explaining how the iterated tower was constructed.
6. Feed candidate discovery and training health only when the resulting tower has many nontrivial executable tiers.

## Non-Goals

This correction must not:

- overwrite or reinterpret the historical `smoke_001` one-shot PlateSupport gauntlet run;
- silently replace the existing one-shot `source_local_ratio` schema;
- create a detached one-off script that cannot feed the standard gauntlet;
- promote a paired comparison claim before a many-tier candidate is found and trainable;
- hide the one-shot versus iterated distinction in readouts;
- hard-code only the currently selected `1/18` candidate path;
- treat a placeholder iterated class as success if it does not actually produce ordered contraction blocks and multiple tower tiers.

## Counterpoint Reference Architecture

The working reference is the counterpoint full-iterated schema path:

```text
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/config.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/runner.py
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
```

Key counterpoint concepts to copy:

```text
SCHEMA1_TOWER_SOURCE_FULL_ITERATED = "full_iterated_noisy_rate"
CounterpointIteratedNoisyRateSchema
build_counterpoint_iterated_noisy_rate_partition_tower(...)
_iterated_noisy_rate_plan(...)
```

The counterpoint iterated plan:

1. Initializes union-find components over base state IDs.
2. Keeps a full edge-to-block assignment map over base edges.
3. At each iteration, selects candidate edges crossing current components.
4. Uses stable deterministic scoring to decide which representatives are selected.
5. Assigns selected edges to a fresh iteration-specific `SchemaBlockId`.
6. Unions selected endpoints.
7. Appends the block if it changed the component structure.
8. Stops on component exhaustion, no selected edges, no changed unions, or max iterations.
9. Returns `ordered_blocks()` so `PartitionTower` builds one tier per successful contraction block.

The PlateSupport correction should copy this structure.

## Current PlateSupport Architecture To Change

The current one-shot schema class is:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/source_local_ratio_schema.py
SourceLocalOutgoingRatioSchema
```

Current behavior:

- ignore self edges;
- group outgoing edges by concrete source state;
- stable-shuffle each source's non-self outgoing edges;
- select `ceil(len(outgoing) * numerator / denominator)`;
- default `min_selected_per_source = 1`;
- return one block from `ordered_blocks()`.

That is why the current `1/18` schema selected many edges and collapsed from 89 state cells to 10 state cells in one step.

The current behavior must remain available as:

```text
schema_family_id = source_local_ratio
schema_mode = source_local_ratio
```

The new behavior must be separate:

```text
schema_family_id = source_local_ratio_iterated
schema_mode = source_local_ratio_iterated
```

## Proposed Runtime Schema

### Class

Add:

```text
IteratedSourceLocalOutgoingRatioSchema
```

Recommended file:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/source_local_ratio_schema.py
```

If the file becomes too large, split helpers into:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/iterated_source_local_ratio_schema.py
```

### Constructor Contract

The schema must carry:

| Field | Type | Meaning |
| --- | --- | --- |
| `numerator` | `int` | stable threshold numerator |
| `denominator` | `int` | stable threshold denominator |
| `seed` | `int` | deterministic schema seed |
| `selector_rule_id` | `str` | stable selector identity |
| `max_iterations` | `int` | maximum ordered contraction blocks |
| `selection_mode` | `str` | concrete selector semantics |

Default values:

```text
selector_rule_id = plate_support_source_local_iterated_stable_rate_v001
max_iterations = 32
selection_mode = quotient_source_representative_stable_rate
```

### Required Methods

The schema must implement:

```python
def assign_edge(self, edge_id: EdgeId, registry: BaseGraphRegistry) -> SchemaBlockId | None:
    ...

def ordered_blocks(self) -> tuple[SchemaBlockId, ...]:
    ...

def plan_diagnostics(self) -> tuple[dict[str, object], ...]:
    ...
```

`assign_edge(...)` must lazily ensure a deterministic plan exists for the current registry.

`ordered_blocks()` must return one `SchemaBlockId` per successful iteration. If it returns only one block for a many-tier candidate, that is a failure.

`plan_diagnostics()` must expose enough data to write the new iterated plan artifact tables.

### Stable Schema IDs

Add a helper:

```python
def source_local_ratio_iterated_schema_id(
    numerator: int,
    denominator: int,
    max_iterations: int,
) -> str:
    return (
        "plate_support_schema_source_local_ratio_iterated_"
        f"{numerator:03d}_over_{denominator:03d}_i{max_iterations:03d}_v001"
    )
```

The exact function name may follow local style, but the ID shape should preserve:

- source-local lineage;
- iterated architecture;
- numerator;
- denominator;
- max iteration cap;
- version.

### Block IDs

Each successful iteration must have a distinct block ID:

```text
(
  "plate-support-source-local-ratio-iterated",
  numerator,
  denominator,
  selector_rule_id,
  seed,
  iteration_index
)
```

If the implementation uses underscores rather than hyphens internally, that is acceptable, but artifact output should be stable and readable.

## Iterated Planning Algorithm

### Overview

The planning algorithm must be a PlateSupport adaptation of counterpoint's `_iterated_noisy_rate_plan(...)`.

Inputs:

```text
registry
numerator
denominator
seed
selector_rule_id
max_iterations
selection_mode
```

Outputs:

```text
assignment_by_edge_id: dict[EdgeId, SchemaBlockId | None]
ordered_blocks: tuple[SchemaBlockId, ...]
plan_diagnostics: tuple[dict[str, object], ...]
stop_summary: dict[str, object]
```

### Union-Find State

Initialize:

```python
edge_ids = tuple(sorted(registry.edge_ids, key=lambda edge_id: edge_id.value))
state_ids = tuple(registry.state_ids)
parent = {state_id: state_id for state_id in state_ids}
assignment = {edge_id: None for edge_id in edge_ids}
ordered_blocks = []
diagnostic_rows = []
```

Required helpers:

```python
_find(parent, state_id)
_union(parent, a, b)
_component_count(parent)
```

These can be copied structurally from counterpoint.

### Candidate Edge Selection

For each iteration:

1. Stop if component count is less than or equal to 1.
2. Build quotient representative candidates.
3. Exclude edges whose source and target are already in the same component.
4. Group remaining candidates by source component.
5. Within each source component, keep representative edges to target components.
6. Score each representative deterministically.
7. Select candidates with `score < numerator / denominator`.
8. If no candidates are selected, stop with `stop_reason = no_selected_edges`.
9. Assign selected edges to the current iteration block.
10. Union selected edge endpoints.
11. If no union changed the component structure, stop with `stop_reason = no_component_change`.
12. Append the block.
13. Continue until max iterations or another stop condition.

### Source-Local Requirement

The selector must remain source-local in the quotient sense.

That means selection must be organized around current source components, not only a global edge list.

Acceptable implementation:

- compute current source component for every candidate representative edge;
- apply stable threshold scoring to candidates within each source component;
- allow a source component to select zero edges at a tier.

Forbidden implementation:

- repeat the one-shot `ceil(..., min_selected_per_source=1)` rule at every tier as the default many-tier selector.

Reason: selecting at least one outgoing edge from every source component is likely too aggressive for the 89-state PlateSupport graph and is not aligned with the PO's many-tier target.

### Stable Scoring

Do not use Python's built-in `hash()`.

Use a deterministic hash-to-float function, for example:

```text
sha256(selector_rule_id | seed | iteration_index | source_root | target_root | edge_key)
```

Then map the first stable integer slice to `[0.0, 1.0)`.

The canonical score key must include:

```text
selector_rule_id
seed
iteration_index
source component key
target component key
canonical edge key or canonical action/endpoint key
```

### Quotient Representative Edges

Counterpoint uses one representative per current component pair. PlateSupport should preserve source-locality, so the representative key should include source component and target component, and may also include action identity if needed to avoid erasing action structure too aggressively.

Recommended first version:

```text
representative grouping key = (source_component, target_component, action_key)
```

If this produces too many action-level representatives and too little contraction, a later design can compare `(source_component, target_component)`.

The blueprint recommendation is to preserve action identity initially because PlateSupport behavior depends strongly on primitive action validity and invalid-move avoidance.

### Stop Reasons

Every iterated arm must report one final stop reason:

```text
component_count_leq_one
no_candidate_edges
no_selected_edges
no_component_change
max_iterations_reached
diagnostic_error
```

Every iteration row must record:

```text
component_count_before
candidate_edge_count
selected_edge_count
changed_union_count
component_count_after
block_id
iteration_status
```

## Stage 2 Schema Sweep Integration

The iterated correction must integrate with gauntlet Stage 2:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/
```

### Config

Update:

```text
config.py
```

Add fields:

```python
iterated_source_local_ratio_numerators: tuple[int, ...] = (1,)
iterated_source_local_ratio_denominators: tuple[int, ...] = (144, 72, 36, 18)
iterated_source_local_max_iterations: int = 32
iterated_source_local_selector_rule_id: str = (
    "plate_support_source_local_iterated_stable_rate_v001"
)
iterated_source_local_selection_mode: str = (
    "quotient_source_representative_stable_rate"
)
iterated_source_local_schema_seeds: tuple[int, ...] | None = None
iterated_near_full_collapse_threshold: float = 0.9
iterated_min_nontrivial_tiers: int = 3
```

If a separate schema seed field is too awkward, use existing `schema_seeds` for both one-shot and iterated arms.

Validation:

- denominators positive;
- numerators positive;
- numerator less than or equal to denominator;
- max iterations positive;
- near-collapse threshold in `(0, 1]`;
- min nontrivial tiers positive.

### Schema Family Enumeration

Update:

```text
schema_families.py
```

Add support for:

```text
source_local_ratio_iterated
```

For each seed, numerator, denominator, and max-iteration cap, emit a `SchemaArm` with:

```text
schema_family_id = source_local_ratio_iterated
selection_policy_id = source_local_quotient_representative_stable_rate
selection_rate = "{numerator}/{denominator}"
selection_count = threshold_selected_per_quotient_source_component
state_feature_basis = current_quotient_component
action_category_basis = primitive_action_identity_preserved
edge_basis = quotient_representative_valid_nonself_edges_by_source_component
schema_mode = source_local_ratio_iterated
expected_role = many_tier_candidate_probe
construction_supported = True
```

Do not remove the one-shot `source_local_ratio` arm.

### Schema Construction Surface

Update:

```text
schema_builders.py
```

`construct_schema_arm(...)` must report:

```text
bbb.plate_support.IteratedSourceLocalOutgoingRatioSchema.full_graph_partition_tower
```

for iterated arms.

### Schema Runner

Update:

```text
schema_runner.py
```

Add a dispatcher branch:

```python
if arm.schema_mode == "source_local_ratio_iterated":
    return _run_source_local_ratio_iterated_tower_diagnostics(arm=arm, config=...)
```

The diagnostics must:

1. Import the same PlateSupport surface as the one-shot runner.
2. Enumerate valid states and valid transitions exactly as one-shot does.
3. Build `BaseEdge` rows exactly as one-shot does.
4. Build a `PartitionTower` using `IteratedSourceLocalOutgoingRatioSchema`.
5. Call `partition_tower.assert_consistent()` if available through the same surface.
6. Extract tower shape rows for every tier.
7. Extract tier occupancy rows for every tier.
8. Extract tier executability rows for every tier.
9. Extract endpoint coalescence rows for every tier.
10. Extract iterated plan diagnostic rows from the schema.
11. Compute iterated stop summary.
12. Compute many-tier candidate signal.

The existing one-shot path must remain unchanged except for shared helper extraction if useful.

### Existing Tables To Preserve

The iterated arms must continue writing rows into:

```text
tower_shape_summary.csv
tier_occupancy_summary.csv
tier_executability_summary.csv
endpoint_coalescence_summary.csv
schema_candidate_signal_summary.csv
schema_construction_summary.csv
schema_arm_summary.csv
timing_summary.csv
```

These rows must include enough schema fields to distinguish iterated and one-shot arms.

### New Stage 2 Tables

Add:

```text
iterated_plan_summary.csv
iterated_schema_stop_summary.csv
many_tier_candidate_signal_summary.csv
```

#### `iterated_plan_summary.csv`

Fields:

```text
schema_id
schema_family_id
schema_seed
selector_rule_id
selection_mode
numerator
denominator
max_iterations
iteration_index
component_count_before
candidate_edge_count
selected_edge_count
changed_union_count
component_count_after
block_id
iteration_status
stop_reason
diagnostic_status
```

#### `iterated_schema_stop_summary.csv`

Fields:

```text
schema_id
schema_family_id
schema_seed
selector_rule_id
selection_mode
numerator
denominator
max_iterations
completed_iteration_count
ordered_block_count
final_component_count
stop_reason
selected_edge_count_total
changed_union_count_total
max_depth
nontrivial_tier_count
largest_cell_share_final
near_full_collapse_threshold
diagnostic_status
```

#### `many_tier_candidate_signal_summary.csv`

Fields:

```text
schema_id
schema_family_id
schema_seed
selector_rule_id
selection_mode
numerator
denominator
max_iterations
max_depth
nontrivial_tier_count
min_required_nontrivial_tiers
min_nonbase_state_cell_count
max_nonbase_state_cell_count
min_nonbase_active_action_cell_count
max_largest_cell_share
near_full_collapse_threshold
has_immediate_collapse
has_empty_executable_tier
candidate_signal
candidate_signal_reason
diagnostic_status
```

Candidate signal values:

```text
many_tier_executable_candidate
shallow_executable_candidate
collapsed_candidate
nonexecutable_candidate
empty_candidate
diagnostic_error
```

### Candidate Signal Semantics

For iterated candidates:

```text
many_tier_executable_candidate if:
  max_depth >= 4
  nontrivial_tier_count >= 3
  has_empty_executable_tier == false
  has_immediate_collapse == false
  max_largest_cell_share < 0.9
```

`has_immediate_collapse` should be true when tier 1 has largest-cell share greater than or equal to `0.9`, or when tier 1 has one state cell.

`nontrivial_tier_count` should count nonbase tiers with:

```text
state_cell_count > 1
active_action_cell_count > 0
largest_cell_share < 0.9
```

If action-cell count and active-action-cell count differ by table, use active executable action-cell count for candidate gating.

## Stage 3 Candidate Discovery Integration

Stage 3 must be updated so iterated candidates can become selected training candidates.

Relevant package:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/candidate_discovery/
```

### Source Loading

Stage 3 currently consumes Stage 2 tables. It must include the new iterated candidate signal table in source expectations when present.

Required behavior:

- if `many_tier_candidate_signal_summary.csv` exists, load it;
- normalize iterated candidates into the same candidate row shape as existing candidates;
- preserve one-shot candidate discovery for backward compatibility.

### Eligibility

Update candidate classification so:

```text
source_local_ratio_iterated + many_tier_executable_candidate
```

is eligible for:

```text
stage4_training_health
```

Recommended selection priority:

1. iterated candidates with `many_tier_executable_candidate`;
2. among them, candidates with deeper nontrivial tiers;
3. among equal depth, candidates with lower max largest-cell share;
4. among equal structural health, lower requested rate;
5. among equal rate, lower schema seed.

Do not let a shallow one-shot candidate outrank an iterated many-tier candidate when the correction run is explicitly configured to seek many-tier towers.

### Candidate Metadata

Selected candidate output must include:

```text
schema_id
schema_family_id
schema_mode
schema_seed
selection_rate
ratio_numerator
ratio_denominator
max_iterations
selector_rule_id
selection_mode
max_depth
nontrivial_tier_count
near_full_collapse_threshold
```

This metadata must be available to Stage 4 without requiring Stage 4 to reverse-engineer everything from `schema_id`.

## Stage 4 Training Health Integration

Stage 4 currently assumes one-shot source-local schema IDs and constructs `SourceLocalOutgoingRatioSchema`.

Relevant files:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/candidate_source.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/training_surfaces.py
```

### Candidate Source Parsing

Replace the one regex-only path with schema-family-driven metadata loading.

Current one-shot regex support must remain:

```text
plate_support_schema_source_local_ratio_001_over_018_v001
```

Add iterated support:

```text
plate_support_schema_source_local_ratio_iterated_001_over_144_i032_v001
```

But the primary source of truth should be candidate metadata fields from Stage 3.

### TrainingCandidate Contract

Expand `TrainingCandidate` to include:

```text
schema_family_id
schema_mode
ratio_numerator
ratio_denominator
max_iterations
selector_rule_id
selection_mode
max_depth
nontrivial_tier_count
near_full_collapse_threshold
```

The one-shot path may set:

```text
max_iterations = 1
selector_rule_id = source_local_outgoing_ratio_catch
selection_mode = legacy_source_local_ceil_prefix
```

### Training Surface Factory

Replace hard-coded schema construction with:

```python
def build_schema_for_training_candidate(candidate: TrainingCandidate):
    if candidate.schema_family_id == "source_local_ratio":
        return SourceLocalOutgoingRatioSchema(...)
    if candidate.schema_family_id == "source_local_ratio_iterated":
        return IteratedSourceLocalOutgoingRatioSchema(...)
    raise Stage3CandidateSourceError(...)
```

`build_training_surface(...)` must call this factory and pass the schema to:

```python
surface.create_runtime(schema=schema)
```

### Runtime Expectations

The same upstream PlateSupport runtime interface should work if it accepts a state-collapser compatible schema object:

```python
assign_edge(edge_id, registry)
ordered_blocks()
```

If `surface.create_runtime(schema=schema)` rejects the iterated schema, implementation must stop and diagnose rather than substituting a simpler runtime.

### Training Health Tables

Stage 4 tables must preserve:

```text
schema_family_id
schema_mode
max_depth
nontrivial_tier_count
```

Tier controller events must support more than tiers 0 and 1.

The existing deepest-executable-tier controller behavior is acceptable and desirable for the first many-tier training health probe.

## Stage 5 Threshold Frontier Integration

Stage 5 should remain structurally similar, but must not assume one-shot schema IDs.

Relevant package:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/threshold_frontier_calibration/
```

Required changes:

- source loading must preserve iterated candidate metadata from Stage 4;
- threshold policy manifests must include schema family, schema mode, max depth, and nontrivial tier count;
- human docs must say whether calibration came from an iterated candidate;
- no threshold calibration should run if Stage 4 reports no trainable iterated candidate for a correction run.

## Stage 6 Paired Comparison Integration

Stage 6 should remain structurally similar, but must build the iterated tower when the selected candidate is iterated.

Relevant package:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison/
```

Required changes:

- paired arms preserve iterated schema metadata;
- tower arm uses the same schema factory concept as Stage 4;
- run manifests record `source_local_ratio_iterated`;
- tier event aggregation supports more than two tiers;
- paired readout prominently reports tower depth and nontrivial tier count;
- Stage 6 must not compare against a shallow one-shot candidate when the correction run is explicitly seeking iterated towers.

## Stage 7 Readout And System Learning Integration

The generated standard gauntlet README and result docs must make the correction visible.

Relevant package:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/readout_system_learning/
```

Required readout content:

- badge or top-line status for iterated tower found/shallow/collapsed/blocked;
- top-line count of nontrivial tiers;
- tower shape summary near the top;
- source-local one-shot versus iterated architecture explanation;
- candidate metadata table;
- stop reason if no many-tier candidate is found;
- explicit statement that historical `smoke_001` was one-shot if referenced.

Recommended badges:

```text
Iterated Tower: Found / Shallow / Collapsed / Blocked
Nontrivial Tiers: <N>
Executable Tiers: All / Some / None
Ratio Sweep: Complete / Partial
Candidate: Selected / Not Found
Provenance: Repo Artifacts
```

## CLI Surface

The correction should be runnable through the existing gauntlet CLI.

Required CLI behavior:

- allow Stage 2 schema sweep to include iterated source-local-ratio arms;
- allow the ratio set and max-iterations cap to be configured;
- preserve repo artifact root discipline;
- avoid requiring hand edits to Python config.

Recommended command shape:

```text
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet schema-sweep run \
  --repo-root "$BBB_ROOT" \
  --artifact-root "$BBB_ARTIFACT_ROOT" \
  --stage1-source "$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/structural_and_tower_diagnostics/readout_source.json" \
  --run-label iterated_tower_correction_001 \
  --locked-by foster \
  --include-iterated-source-local-ratio \
  --iterated-source-local-denominators 144,72,36,18 \
  --iterated-source-local-max-iterations 32 \
  --iterated-near-full-collapse-threshold 0.9
```

If local CLI conventions prefer different flag names, the implementation may adapt names, but the semantics must remain explicit.

## Artifact Discipline

Do not overwrite the existing one-shot `smoke_001` artifact set.

Recommended correction run label:

```text
iterated_tower_correction_001
```

Artifact/readout surfaces should remain under:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/
```

Raw correction artifacts should live under a new run-label artifact root:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/iterated_tower_correction_001/
```

Human-readable readout regeneration must be explicit and must point at the readout source:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <readout_source.json>
```

If the top-level standard gauntlet README is regenerated for the correction run, it must not silently erase preserved clarification conversation without following the readout protocol.

## Expected Implementation Touchpoints

### Stage 2

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/source_local_ratio_schema.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/config.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/schema_families.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/schema_builders.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/schema_runner.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/classification.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/runner.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/docs_writer.py
```

### Stage 3

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/candidate_discovery/eligibility.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/candidate_discovery/selection.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/candidate_discovery/runner.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/candidate_discovery/candidate_ids.py
```

### Stage 4

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/candidate_source.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/training_surfaces.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/manifests.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/runner.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/docs_writer.py
```

### Stage 5

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/threshold_frontier_calibration/stage_sources.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/threshold_frontier_calibration/manifests.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/threshold_frontier_calibration/docs_writer.py
```

### Stage 6

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison/stage_sources.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison/arms.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison/runner.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison/aggregation.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison/docs_writer.py
```

### Stage 7

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/readout_system_learning/
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

Only update the artifact protocol if the generated readout cannot currently express iterated tower diagnostics. Do not make protocol changes casually.

## Test Strategy

### Unit Tests

Add tests for:

- deterministic score generation;
- deterministic assignment planning;
- different seeds producing allowed plan differences;
- no self-edge scheduling;
- ordered block count equals successful iteration count;
- block IDs include iteration index;
- stop reason recorded;
- quotient representative selection skips already-contracted components;
- source-local grouping allows zero selected edges per source component;
- near-collapse classification at threshold `0.9`.

### Stage 2 Tests

Add or update tests to assert:

- `source_local_ratio_iterated` arms enumerate;
- default iterated denominators are `(144, 72, 36, 18)`;
- Stage 2 writes new iterated tables;
- Stage 2 still writes legacy one-shot tables;
- iterated tower shape includes all tiers;
- many-tier candidate signal is present;
- collapsed/shallow cases are classified distinctly.

### Stage 3 Tests

Add or update tests to assert:

- many-tier iterated candidates can be selected;
- shallow one-shot candidates do not outrank eligible iterated candidates in correction runs;
- downstream training summary includes iterated metadata;
- candidate IDs remain stable.

### Stage 4 Tests

Add or update tests to assert:

- Stage 4 parses one-shot and iterated candidates;
- Stage 4 builds the correct schema class for each candidate;
- at least one iterated candidate can run a smoke episode;
- tier controller events include tier indices beyond tier 1 when the tower has them;
- no hard-coded two-tier assumption remains in summaries.

### Stage 5 Tests

Add or update tests to assert:

- threshold calibration accepts iterated Stage 4 source metadata;
- manifests preserve schema family and max depth;
- calibration blocks cleanly if no trainable iterated candidate exists.

### Stage 6 Tests

Add or update tests to assert:

- paired comparison builds an iterated tower for iterated candidates;
- aggregation handles tier indices beyond 1;
- readout tables preserve iterated schema metadata.

### End-To-End Smoke

Run at least:

```text
Stage 1 structural_and_tower_diagnostics
Stage 2 contraction_schema_sweep with iterated arms
Stage 3 candidate_discovery
Stage 4 tower_training_health
```

Only run Stage 5 and Stage 6 if Stage 4 finds a trainable many-tier iterated candidate.

## Success Criteria

This correction succeeds when:

1. Existing one-shot PlateSupport schema behavior remains available and tested.
2. A new iterated source-local schema family exists.
3. The iterated schema returns multiple ordered blocks when selected edges support multiple contractions.
4. Stage 2 can run an iterated ratio sweep and write plan/tower diagnostic artifacts.
5. Stage 3 can select an eligible many-tier iterated candidate.
6. Stage 4 can train on the selected iterated candidate.
7. Readouts clearly distinguish one-shot and iterated architecture.
8. No downstream stage relies exclusively on the old one-shot schema ID regex.
9. If PlateSupport cannot produce many nontrivial tiers, the artifacts say so explicitly with stop reasons rather than hiding the result.

## Stop Conditions For Implementation Workplan

The later implementation workplan must stop if:

- the upstream PlateSupport runtime cannot accept an iterated schema object;
- state_collapser `PartitionTower` does not build multiple tiers from ordered blocks as expected;
- Stage 2 cannot produce any iterated arm without simplifying the selector;
- the implementation would need to treat a one-block schema as "iterated";
- candidate discovery cannot distinguish one-shot and iterated candidates without redesigning its table contract;
- Stage 4 would need a placeholder schema factory rather than real iterated construction;
- a test or artifact contradicts the assumption that counterpoint's iterated planning shape transfers to PlateSupport;
- implementing exactly this blueprint would require overwriting historical `smoke_001` artifacts.

## Remaining Consultant-Authored Confirmation Points

These are not Project Owner statements.

1. The blueprint assumes `0.9` is the near-collapse/largest-cell-share threshold. This was confirmed conversationally, but the implementation workplan should keep it visible as a decision lock.
2. The blueprint assumes `max_depth >= 4` and `nontrivial_tier_count >= 3` are sufficient first gates for "many nontrivial tiers." The Project Owner has not specified an exact minimum tier count.
3. The blueprint recommends action-key-preserving quotient representatives. If this is too conservative, a later run may need a second selector mode.
4. The blueprint recommends integrating the correction into gauntlet Stage 2 rather than creating a detached Stage 8 runner. This follows the PO goal of correcting the gauntlet, but the exact CLI exposure can still be tuned.

## Blueprint Summary

The correction is to copy counterpoint's iterated tower architecture, not its exact domain-specific noisy-rate semantics.

For PlateSupport, the new schema should repeatedly select stable source-local quotient representative edges, schedule one block per successful iteration, and let `PartitionTower` build multiple tiers from those blocks. The gauntlet should treat the result as diagnostic evidence first. Only if the resulting tower has several nontrivial executable tiers should it become a Stage 3 candidate and proceed to Stage 4 training health, Stage 5 threshold calibration, and Stage 6 paired comparison.
