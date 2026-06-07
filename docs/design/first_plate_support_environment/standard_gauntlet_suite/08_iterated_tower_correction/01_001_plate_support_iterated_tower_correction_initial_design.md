# PlateSupport Iterated Tower Correction Initial Design

## Status

Initial design document.

This document is derived from the clarifying conversation preserved in:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/README.md
```

It is not yet a blueprint or workplan. Its job is to collect the current diagnosis, identify what should be copied from the working counterpoint implementation, and specify the likely implementation shape for a PlateSupport many-tier correction.

## Attribution Boundary

The following Project Owner inputs are directly available from the evaluation README conversation and the current user request:

- The PO wants PlateSupport towers with many nontrivial tiers.
- The PO questioned whether the current problem is wrong architecture, wrong ratio, or both.
- The PO asked for a new design folder under `docs/design/first_plate_support_environment/standard_gauntlet_suite`.
- The PO asked that this initial design mostly copy counterpoint wherever it makes sense, because the many-tier behavior works correctly there.

Everything else in this document is Codex-authored diagnosis, recommendation, or implementation design unless explicitly marked otherwise.

## Executive Diagnosis

The current PlateSupport standard gauntlet is coherent, but it is using the wrong tower-construction architecture for the PO's many-tier goal.

The current selected PlateSupport schema is:

```text
plate_support_schema_source_local_ratio_001_over_018_v001
```

Its tower has only two tiers:

| Tier | State Cells | Action Cells |
| ---: | ---: | ---: |
| 0 | 89 | 388 |
| 1 | 10 | 116 |

That means the current run did not fail to discover many tiers. It never tried to build many tiers. It built one quotient layer and stopped.

The counterpoint many-tier behavior comes from the `full_iterated_noisy_rate` path. That path repeatedly schedules fresh contraction blocks against quotient representative edges. The wide counterpoint full-iterated run produced tiers from 0 through 32.

Therefore:

```text
primary issue: PlateSupport has one-shot source-local-ratio, not an iterated tower schema
secondary issue: the current 1/18 one-shot source-local rule is likely too aggressive if repeated on an 89-state graph
initial correction: add a diagnostic-first PlateSupport iterated source-local tower family
```

## Current PlateSupport Evidence

The PlateSupport standard gauntlet completed all stages:

| Stage | Name | Claim Status |
| ---: | --- | --- |
| 1 | structural_and_tower_diagnostics | diagnostic_complete |
| 2 | contraction_schema_sweep | diagnostic_complete |
| 3 | candidate_discovery | candidate_found |
| 4 | tower_training_health | trainable_clean |
| 5 | threshold_frontier_calibration | threshold_calibrated |
| 6 | paired_replicate_comparison | paired_comparison_negative_signal |
| 7 | readout_and_system_learning | readout_complete |

The paired comparison result was negative on the locked Stage 5 binary goal target:

| Arm | Target Hits | Episodes | Target Hit Rate |
| --- | ---: | ---: | ---: |
| direct concrete baseline | 15 | 128 | 0.1171875 |
| selected tower candidate | 6 | 128 | 0.046875 |

But the tower arm had a real counter-signal:

| Arm | Mean Total Reward | Invalid Moves |
| --- | ---: | ---: |
| direct concrete baseline | -78.71875 | 2142 |
| selected tower candidate | -44.515625 | 0 |

The tower arm was also actually using the quotient tier:

| Tier | Controller Steps | Share |
| ---: | ---: | ---: |
| 0 | 152 | 0.024111675126903553 |
| 1 | 6152 | 0.9758883248730964 |

This means the current one-shot tower is not useless. It produces cleaner behavior and is heavily used. The problem is that it is too shallow for the PO's intended many-tier experiment.

## Counterpoint Reference To Copy

The primary working reference is the counterpoint full-iterated tower path:

```text
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/config.py
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/runner.py
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
```

The key counterpoint config constant is:

```text
SCHEMA1_TOWER_SOURCE_FULL_ITERATED = "full_iterated_noisy_rate"
```

The key builder is:

```text
build_counterpoint_iterated_noisy_rate_partition_tower(...)
```

The key schema class is:

```text
CounterpointIteratedNoisyRateSchema
```

The key planning routine is:

```text
_iterated_noisy_rate_plan(...)
```

The counterpoint algorithm shape is:

1. Enumerate the full base graph.
2. Initialize a `PartitionTower` with an iterated schema object.
3. Inside the schema, lazily compute a deterministic edge-to-block assignment plan when `assign_edge(...)` is first called.
4. Use union-find over state IDs to model the contraction components created so far.
5. At iteration 0, select candidate edges from the base surface.
6. At later iterations, select representative edges between current quotient components.
7. For each successful iteration, create a fresh `SchemaBlockId`.
8. Assign selected base edges to that block.
9. Union their endpoints.
10. Stop when no components remain to merge, no selected edges exist, or an iteration does not change the component structure.
11. Return ordered blocks so `PartitionTower` can build multiple tiers.

This is the architecture PlateSupport should copy.

## Counterpoint Details Worth Preserving

### Preserve Deterministic Planning

Counterpoint uses deterministic stable scoring and sorted edge/cell keys. PlateSupport should do the same. A rerun with the same instance, numerator, denominator, selector rule, schema seed, and max iteration count must produce the same tower.

### Preserve Ordered Block Semantics

Counterpoint stores one block per successful iteration:

```text
("counterpoint_iterated_noisy_rate", numerator, denominator, selector_rule_id, iteration_index)
```

PlateSupport should similarly emit:

```text
("plate-support-source-local-ratio-iterated", numerator, denominator, selector_rule_id, schema_seed, iteration_index)
```

The exact tuple can be revised during implementation, but it must include enough material to distinguish:

- environment/schema family;
- ratio;
- selector rule;
- seed;
- iteration index.

### Preserve Explicit Tower Source Metadata

Counterpoint distinguishes one-drop from full-iterated by `schema1_tower_source`.

PlateSupport should have an equivalent distinction. The current one-shot schema should remain supported and clearly named:

```text
source_local_ratio
```

The new schema should be distinct:

```text
source_local_ratio_iterated
```

This distinction must appear in schema IDs, schema family IDs, manifests, candidate tables, training surfaces, readout sources, and human-readable readouts.

### Preserve Prefix Verification Where It Makes Sense

Counterpoint verifies that a full-iterated candidate extends the one-drop source tower:

```text
observed[:len(expected)] == expected
len(observed) > len(expected)
```

For PlateSupport this should be adapted carefully. If the new iterated mode deliberately changes the first-tier selection rule to avoid the current `89 -> 10` drop, it cannot be required to match the old one-shot `1/18` tower.

Recommended adaptation:

- keep a diagnostic arm that uses a legacy-prefix mode, for validation;
- keep the many-tier search arm free to use a gentler iterated selector;
- verify prefix shape only when the schema declares that it is in legacy-prefix mode.

### Preserve Artifact-First Evidence

Counterpoint readouts became useful because tower shape, tier executability, lift success, training health, and paired comparison tables were all preserved. PlateSupport should do the same.

The new design must add explicit iterated-plan artifacts rather than forcing future readers to infer what happened from a final tower shape table.

## Current PlateSupport Implementation Surface

The current one-shot schema is:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/source_local_ratio_schema.py
```

Its class is:

```text
SourceLocalOutgoingRatioSchema
```

It currently:

- ignores self edges;
- groups outgoing edges by concrete source state;
- selects a stable shuffled prefix from each source's non-self outgoing list;
- uses `ceil(len(outgoing) * numerator / denominator)`;
- has `min_selected_per_source=1` by default;
- returns a single block from `ordered_blocks()`.

That implementation is good for producing a one-shot candidate. It is not suitable as the direct repeated rule for many-tier towers, because `ceil(...)` with a positive numerator selects at least one edge for every source with outgoing edges. On an 89-state graph, that first step already collapses to 10 state cells.

The current schema-sweep stage is:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/
```

Important files:

| File | Current Role | Required Change |
| --- | --- | --- |
| `config.py` | exposes `source_local_ratio_numerators=(1,)`, denominator `18` | add iterated ratio fields and max iteration cap |
| `schema_families.py` | enumerates schema arms | add `source_local_ratio_iterated` arms |
| `schema_builders.py` | declares construction surface | add iterated builder surface |
| `schema_runner.py` | builds one-shot tower diagnostics | build iterated tower diagnostics and emit iteration-plan rows |
| `classification.py` | classifies candidate signal | recognize multi-tier iterated candidates |
| `runner.py` | writes Stage 2 artifact tables | include new tables and fields |
| `docs_writer.py` | writes Stage 2 human docs | explain iterated tower family |

Downstream Stage 4 currently assumes source-local one-shot schema IDs:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/candidate_source.py
```

It has:

```text
SOURCE_LOCAL_RATIO_RE = r"^plate_support_schema_source_local_ratio_(?P<numerator>\d+)_over_(?P<denominator>\d+)_v001$"
```

That must be generalized before an iterated candidate can train.

Stage 4 also builds only the one-shot schema:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/training_surfaces.py
```

It currently constructs:

```text
SourceLocalOutgoingRatioSchema(...)
```

That must become a schema factory keyed by `schema_family_id` or `schema_mode`, not a hard-coded one-shot class.

Stage 5 and Stage 6 can probably remain mostly structurally intact once Stage 4 and the candidate payload expose the correct candidate/tower metadata, but they must preserve the new schema IDs and tier shape fields in output tables.

## Proposed New Schema Family

Recommended family name:

```text
source_local_ratio_iterated
```

Recommended schema ID form:

```text
plate_support_schema_source_local_ratio_iterated_001_over_144_i032_v001
```

Fields:

| Field | Meaning |
| --- | --- |
| `001_over_144` | requested stable selection rate |
| `i032` | max iteration cap |
| `schema_seed` | remains a separate manifest/table field, as in existing schema arms |

Possible alternatives:

```text
plate_support_schema_iterated_source_local_ratio_001_over_144_max032_v001
plate_support_schema_source_local_rate_iterated_001_over_144_i032_v001
```

Recommendation: use `source_local_ratio_iterated` in the family name so it is obviously connected to the existing one-shot `source_local_ratio`, but keep the word `iterated` in the schema ID before the rate.

## Proposed Schema Class

Recommended class name:

```text
IteratedSourceLocalOutgoingRatioSchema
```

Recommended file placement:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/source_local_ratio_schema.py
```

or, if the file becomes too crowded:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/iterated_source_local_ratio_schema.py
```

Recommendation: start in the existing `source_local_ratio_schema.py` only if the implementation remains compact. If the plan diagnostics and helper functions become substantial, split into a new file and import both schema classes through a small factory.

Suggested public shape:

```python
@dataclass(slots=True)
class IteratedSourceLocalOutgoingRatioSchema:
    numerator: int
    denominator: int
    seed: int = 0
    selector_rule_id: str = "plate_support_source_local_iterated_stable_rate_v001"
    max_iterations: int = 32
    selection_mode: str = "quotient_source_representative_stable_rate"

    def assign_edge(self, edge_id: EdgeId, registry: BaseGraphRegistry) -> SchemaBlockId | None:
        ...

    def ordered_blocks(self) -> tuple[SchemaBlockId, ...]:
        ...

    def plan_diagnostics(self) -> tuple[dict[str, object], ...]:
        ...
```

This should copy counterpoint's lazy plan behavior:

```python
def _ensure_plan(self, registry: BaseGraphRegistry) -> None:
    edge_signature = tuple(edge_id.value for edge_id in registry.edge_ids)
    if edge_signature == self._planned_edge_signature:
        return
    assignment, ordered_blocks, diagnostics = _iterated_source_local_ratio_plan(...)
    self._planned_edge_signature = edge_signature
    self._assignment_by_edge_id = assignment
    self._ordered_blocks = ordered_blocks
    self._plan_diagnostics = diagnostics
```

## Proposed Iterated Planning Algorithm

The algorithm should be based on counterpoint's `_iterated_noisy_rate_plan`, with PlateSupport-specific candidate grouping.

### Shared Counterpoint Skeleton

Use:

- `edge_ids = tuple(sorted(registry.edge_ids, key=lambda item: item.value))`;
- `parent = {state_id: state_id for state_id in registry.state_ids}`;
- `assignment = {edge_id: None for edge_id in edge_ids}`;
- `ordered_blocks = []`;
- union-find helpers `_find`, `_union`, `_component_count`;
- iteration loop up to `max_iterations`.

### PlateSupport Candidate Selection

At each iteration:

1. Ignore self edges under the current component partition.
2. Build quotient representative edge candidates.
3. Preserve source-local structure by grouping candidates by current source component.
4. Within each source component, consider one representative per target component/action signature when possible.
5. Score each representative edge with a stable key including:
   - selector rule ID;
   - schema seed;
   - iteration index;
   - source component key;
   - target component key;
   - base edge key or action key.
6. Select the edge if `score < numerator / denominator`.
7. If selected edges union at least one pair of components, append a fresh block.
8. Stop if there are no selected edges, no changed unions, component count is 1, or max iterations is reached.

Recommended candidate key form:

```text
plate_support_iterated_source_local|seed={seed}|tier={iteration_index}|source={source_root}|target={target_root}|edge={canonical_edge_key}
```

The stable score function can be implemented locally with deterministic hashing, or extracted into a shared helper if counterpoint already has a suitable project-local helper. Avoid Python's built-in `hash()`.

### Why Not Repeat The Current Ceil-Per-Source Rule

The current one-shot selector uses:

```python
ceil(len(outgoing) * numerator / denominator)
```

Because the numerator is positive, this selects at least one edge per source with outgoing edges. That is why the one-shot `1/18` PlateSupport candidate selected 89 edges and collapsed from 89 to 10 state cells.

For a repeated many-tier tower, that behavior is probably too aggressive. If applied at each quotient tier, it will likely collapse quickly.

Therefore the iterated selector should use a stable threshold/rate style selection where a source component can select zero outgoing representatives at a given tier. That is closer to counterpoint's `stable_noisy_rate_score < numerator / denominator` behavior.

This preserves the source-local idea without forcing every source to contract at every iteration.

## Recommended Initial Sweep

The current PlateSupport graph is much smaller than the wide counterpoint graph:

| Environment | Tier 0 State Cells | Tier 0 Active Actions |
| --- | ---: | ---: |
| counterpoint wide full-iterated reference | 3580 | 49172 |
| PlateSupport current default | 89 | 388 |

Because PlateSupport is small, the initial iterated diagnostic should sweep gentler rates:

| Numerator | Denominator | Requested Rate | Purpose |
| ---: | ---: | ---: | --- |
| 1 | 144 | 0.006944... | very gentle, likely more tiers |
| 1 | 72 | 0.013888... | gentle |
| 1 | 36 | 0.027777... | moderate |
| 1 | 18 | 0.055555... | compare to current one-shot rate |

Recommended defaults:

```text
iterated_source_local_ratio_numerators = (1,)
iterated_source_local_ratio_denominators = (144, 72, 36, 18)
iterated_source_local_max_iterations = 32
iterated_source_local_schema_seeds = (0, 1, 2)
```

If the existing config shape strongly prefers one denominator with many numerators, invert the representation in code but preserve the same arms.

## New Diagnostic Tables

The current Stage 2 tables are useful but not sufficient for iterated diagnosis. Add new tables or add fields carefully to existing tables.

Recommended new tables:

### `iterated_plan_summary.csv`

One row per schema arm and iteration.

Fields:

```text
schema_id
schema_family_id
schema_seed
iteration_index
component_count_before
candidate_edge_count
selected_edge_count
changed_union_count
component_count_after
block_id
stop_reason
diagnostic_status
```

### `iterated_schema_stop_summary.csv`

One row per iterated arm.

Fields:

```text
schema_id
schema_family_id
schema_seed
max_iterations
completed_iteration_count
final_component_count
stop_reason
selected_edge_count_total
nontrivial_tier_count
largest_cell_share_final
diagnostic_status
```

### `many_tier_candidate_signal_summary.csv`

One row per schema arm, designed to feed Stage 3 selection.

Fields:

```text
schema_id
schema_family_id
schema_seed
max_depth
nontrivial_tier_count
min_nonbase_state_cell_count
max_nonbase_state_cell_count
min_nonbase_active_action_cell_count
max_largest_cell_share
has_immediate_collapse
has_empty_executable_tier
candidate_signal
candidate_signal_reason
diagnostic_status
```

Candidate signal values could include:

```text
many_tier_executable_candidate
shallow_executable_candidate
collapsed_candidate
nonexecutable_candidate
empty_candidate
diagnostic_error
```

The existing `tower_shape_summary.csv`, `tier_occupancy_summary.csv`, `tier_executability_summary.csv`, and `endpoint_coalescence_summary.csv` should still be written for every tier.

## Candidate Discovery Changes

Stage 3 should be able to select iterated candidates.

Current candidate discovery can select the one-shot source-local candidate because Stage 2 emits `schema_candidate_signal_summary` rows with nonflat structured signals.

For iterated candidates, Stage 3 should prioritize:

1. no diagnostic errors;
2. at least several nontrivial tiers;
3. non-empty executable action cells at each used tier;
4. no near-total collapse in the first nonbase tier;
5. largest-cell share below a configured collapse threshold;
6. stable candidate source trace;
7. deterministic schema seed and ratio metadata.

Recommended initial candidate eligibility rule:

```text
eligible if:
  schema_family_id == source_local_ratio_iterated
  max_depth >= 4
  nontrivial_tier_count >= 3
  has_empty_executable_tier == false
  has_immediate_collapse == false
```

This threshold is a consultant recommendation, not a PO-approved decision. The PO's stated goal is many nontrivial tiers; the exact minimum tier count is still open.

Stage 3 should continue to preserve control anchors and blocked candidates.

## Stage 4 Training Health Changes

Stage 4 currently assumes a one-shot schema ID format. It must change before iterated candidates can train.

Required changes:

1. Expand `TrainingCandidate` to include:
   - `schema_family_id`;
   - `schema_mode`;
   - `ratio_numerator`;
   - `ratio_denominator`;
   - `max_iterations`;
   - `selector_rule_id`;
   - any declared `selection_mode`.
2. Replace `_parse_source_local_ratio_schema_id(...)` with a schema metadata parser/factory.
3. Update `build_training_surface(...)` so it can construct:
   - `SourceLocalOutgoingRatioSchema` for one-shot candidates;
   - `IteratedSourceLocalOutgoingRatioSchema` for iterated candidates.
4. Ensure the upstream PlateSupport runtime accepts either schema through the same `surface.create_runtime(schema=schema)` interface.
5. Record the tower depth and schema mode in the training surface manifest.

Stage 4's existing tower-action choice logic should remain mostly valid because it operates on the runtime snapshot and executable action cells. It already chooses from the deepest currently executable tier. That behavior is exactly what we want to probe with many-tier towers.

## Stage 5 Threshold Frontier Changes

Stage 5 should remain mostly unchanged if Stage 4 emits the same training-health tables with richer schema metadata.

Required checks:

- Stage 5 source loading must not assume one-shot schema IDs.
- Stage 5 readout must show that the threshold calibration came from an iterated candidate when applicable.
- Threshold policy manifests should include candidate depth and schema family so later readouts do not hide the architecture.

## Stage 6 Paired Comparison Changes

Stage 6 should also remain mostly unchanged at the controller logic level if it consumes a Stage 4/5 candidate source that can build the iterated schema.

Required checks:

- Paired arms must preserve the iterated schema ID.
- Tower run artifacts must write tier occupancy for all tiers, not only tier 0/1.
- Aggregation must not assume two tiers when summarizing tier rows.
- Human readouts must report many-tier shape prominently.

The current Stage 6 negative signal should not be used as evidence against the future iterated candidate. It evaluated the one-shot two-tier candidate.

## Readout Changes

The human-readable output should make the correction visible at the top.

Recommended badges for the iterated diagnostic:

```text
Iterated Tower: Found / Shallow / Collapsed / Blocked
Nontrivial Tiers: N
Executable Tiers: All / Some / None
Ratio Sweep: Complete / Partial
Candidate: Selected / Not Found
Provenance: Repo Artifacts
```

The readout should explicitly say whether the candidate was:

```text
one-shot source-local-ratio
iterated source-local-ratio
legacy-prefix iterated source-local-ratio
```

The readout should include a compact tower shape table:

| Tier | State Cells | Action Cells | Executable From Start | Largest Cell Share |
| ---: | ---: | ---: | --- | ---: |
| 0 | ... | ... | ... | ... |
| 1 | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... |

If the tower collapses early, the readout should say where and why.

## Proposed CLI Surface

The correction should integrate with the existing standard gauntlet CLI rather than creating a disconnected script.

Possible Stage 2 additions:

```text
uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet schema-sweep run \
  --repo-root "$BBB_ROOT" \
  --artifact-root "$BBB_ARTIFACT_ROOT" \
  --stage1-source "$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/structural_and_tower_diagnostics/readout_source.json" \
  --run-label iterated_tower_001 \
  --locked-by foster \
  --include-iterated-source-local-ratio \
  --iterated-source-local-denominators 144,72,36,18 \
  --iterated-source-local-max-iterations 32
```

If the CLI currently does not expose all Stage 2 config fields, add minimal flags needed for this diagnostic.

Do not require the PO to hand-edit Python config to run the correction.

## Artifact Root Discipline

This correction must use new artifact roots or run labels.

The existing `smoke_001` standard gauntlet readout is valid historical evidence for the one-shot schema. It should not be overwritten to pretend it was an iterated run.

Recommended new label:

```text
iterated_tower_correction_001
```

or:

```text
many_tier_probe_001
```

The final choice can be made during blueprint/workplan generation.

## Tests Needed

### Unit Tests For Schema Planning

Test deterministic behavior:

- same seed and ratio produce same assignment;
- different seed can produce different assignment;
- ordered blocks match iteration count;
- no self edge is scheduled;
- block IDs include iteration index;
- stopping reason is recorded.

Test union-find behavior on a tiny synthetic graph:

- repeated selected edges create multiple ordered blocks;
- already-contracted components are skipped;
- quotient representative edges are selected only between distinct components.

### Stage 2 Integration Tests

Test that schema sweep:

- enumerates `source_local_ratio_iterated` arms;
- writes tower shape rows for all tiers;
- writes iterated plan tables;
- emits candidate signal rows for iterated candidates;
- does not break one-shot `source_local_ratio`.

### Stage 3 Candidate Tests

Test that candidate discovery:

- can select an iterated candidate;
- rejects immediate-collapse iterated candidates;
- preserves source artifact traces;
- passes enough schema metadata downstream.

### Stage 4 Training Tests

Test that training health:

- parses iterated candidate metadata;
- builds `IteratedSourceLocalOutgoingRatioSchema`;
- runs at least one episode;
- records tier controller events beyond tier 1 if available.

### End-To-End Smoke

Run the gauntlet through Stage 4 first. Only proceed to Stage 5/6 after a many-tier trainable candidate exists.

## Risks

### Risk: PlateSupport Is Too Small For Many Tiers

The graph has 89 valid states. It may not support 20+ meaningful tiers no matter what selector we use. The initial target should be several nontrivial tiers, not a counterpoint-wide 32-tier tower.

Mitigation:

- sweep gentler rates;
- use several seeds;
- record stopping reasons honestly;
- do not force a positive claim if no many-tier candidate exists.

### Risk: Source-Local Meaning Gets Lost

If the iterated selector becomes purely global, it will no longer be a source-local correction.

Mitigation:

- group candidate representative edges by current source component;
- record source-component candidate counts;
- preserve source-local language only if the implementation actually respects source locality.

### Risk: Legacy One-Shot Prefix Is Too Aggressive

Counterpoint's full-iterated schema starts with a one-drop prefix and still has many tiers. PlateSupport's current one-shot prefix collapses 89 states to 10.

Mitigation:

- include legacy-prefix mode as a diagnostic arm, not necessarily as the default candidate search mode;
- use stable threshold selection for the many-tier search;
- compare first-tier shape across modes.

### Risk: Downstream Stages Reject New Schema IDs

Stage 4 currently parses only one-shot source-local schema IDs.

Mitigation:

- update candidate metadata to be schema-family driven;
- keep parsing backwards compatible for existing one-shot artifacts;
- add tests before rerunning full gauntlet.

### Risk: Human Readout Hides The Correction

If the readout simply says "Candidate Found" without saying "iterated many-tier candidate," future readers will repeat the current confusion.

Mitigation:

- add explicit badges and summary lines;
- include tower shape near the top;
- include "one-shot versus iterated" architecture in method docs.

## Open Questions For Project Owner

These are Codex-authored questions, not Project Owner statements.

1. What minimum tier depth should count as satisfying "many nontrivial tiers" for PlateSupport?
2. Should the first implementation require a legacy-prefix arm whose first tier matches the old one-shot source-local-ratio schema, or should that only be a diagnostic comparator?
3. Is the preferred initial correction to integrate `source_local_ratio_iterated` directly into Stage 2 of the standard gauntlet, or to create a separate Stage 8 diagnostic that later feeds Stage 2/3?
4. Should the ratio sweep use denominators `(144, 72, 36, 18)` with numerator `1`, or should it use the existing denominator-field style with multiple numerators?
5. Should Stage 3 prioritize maximum depth, healthiest executability, or some blended score when selecting an iterated candidate?

## Consultant Recommendation

Do the correction as an integrated Stage 2 schema family, but develop it diagnostic-first.

Recommended order:

1. Add `IteratedSourceLocalOutgoingRatioSchema`.
2. Add Stage 2 iterated arms and iterated-plan tables.
3. Run Stage 2 only with a new run label and inspect tower shapes.
4. Update Stage 3 to select many-tier candidates only after Stage 2 evidence exists.
5. Update Stage 4 training surface to build iterated candidates.
6. Rerun through Stage 4.
7. Only then proceed to threshold calibration and paired comparison.

The key principle is: copy counterpoint's iterated tower architecture and artifact discipline, but adapt the selector because PlateSupport's current ceil-per-source one-shot rule is probably the wrong first-tier behavior for many-tier search.
