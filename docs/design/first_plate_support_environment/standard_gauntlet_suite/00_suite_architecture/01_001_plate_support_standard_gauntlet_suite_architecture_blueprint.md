# PlateSupport Standard Gauntlet Suite Architecture Blueprint

## Status

Status: initial architecture blueprint.

This is a design blueprint, not an implementation workplan and not execution
approval.

This blueprint is the first component blueprint in:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/
```

Later child-stage blueprints should reference this document for stage IDs,
dependency gates, shared artifact expectations, and claim boundaries.

## Source Inputs

This blueprint is derived from:

- `docs/design/first_plate_support_environment/standard_gauntlet_suite/README.md`;
- `docs/design/first_plate_support_environment/01_001_plate_support_environment_bbb_build_blueprint.md`;
- `docs/design/first_plate_support_environment/01_003_plate_support_environment_bbb_build_implementation_log.md`;
- `docs/environments/plate_support_5x5_default_v001.md`;
- the existing counterpoint evaluation readout sequence under
  `docs/evaluations/counterpoint_symbolic_v001/`;
- the repository benchmark workflow protocols:
  - `docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md`;
  - `docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md`;
  - `docs/prime_directive/artifact_table_to_readable_document_protocol.md`.

## Attribution Discipline

Project Owner direction already established:

- the counterpoint sequence has become a useful baseline pipeline or gauntlet;
- this should become a standard suite that environments can meet;
- PlateSupport is the next environment to receive that suite design;
- the suite should be organized under one parent design area with child folders
  for individual parts;
- detailed blueprints should be created sequentially, not in parallel;
- the design must avoid dangerous compression and hallucination.

Consultant-authored interpretation:

- counterpoint contributes evaluation roles, not literal PlateSupport answers;
- the safest suite shape is one umbrella evaluation family with gated child
  stages;
- later stages must be allowed to block on earlier-stage outputs instead of
  inventing thresholds, candidates, or claims.

## Executive Summary

Define a single umbrella PlateSupport gauntlet evaluation family:

```text
plate_support_standard_gauntlet_v001
```

The gauntlet should test whether the first-class PlateSupport environment can
move from environment readiness to real comparison evidence through a staged
sequence:

1. structural and tower diagnostics;
2. contraction/schema sweep;
3. candidate discovery;
4. tower-only training-health;
5. threshold/frontier calibration;
6. paired replicate comparison;
7. human-readable readout and system-learning archive.

The suite must not flatten these stages into one undifferentiated run. Each
stage has its own evidence role, artifacts, gates, and claim boundary.

## Existing PlateSupport Ground Truth

The completed PlateSupport environment-readiness surface records:

- environment family id: `plate_support`;
- environment instance id: `plate_support_5x5_default_v001`;
- upstream smoke id: `plate_support_env`;
- upstream module: `state_collapser.examples.plate_support_env`;
- valid states: `89`;
- ambient candidate states: `2700`;
- reachable valid states from start: `89`;
- primitive actions: `12`;
- valid non-self edges: `388`;
- invalid primitive moves: `496`;
- valid clipped self-transitions: `184`;
- shortest start-goal path length: `6`;
- goal one primitive action from start: `False`;
- random policy reconnaissance:
  - `1000` episodes;
  - success count `24`;
  - success rate `0.024`;
  - mean reward `-105.748`;
  - invalid move rate about `0.452`;
- default upstream schema probe:
  - max depth `2`;
  - scheduled assignments `96`;
- no-contraction schema probe:
  - max depth `1`;
  - scheduled assignments `0`;
- upstream training surfaces are available.

These facts are environment-readiness evidence. They are not yet evaluation
evidence, learning evidence, or tower-benefit evidence.

## Why One Umbrella Suite

The suite should be one umbrella family because the stages are not independent
research fragments. They form a dependency chain:

```text
readiness
  -> structural/tower diagnostics
  -> schema sweep
  -> candidate discovery
  -> tower training health
  -> threshold/frontier calibration
  -> paired replicate comparison
  -> readout/system learning
```

The umbrella identity gives future engineers:

- one place to find the full standard pipeline;
- one readout surface for suite status;
- consistent stage naming;
- consistent seed/artifact conventions;
- explicit evidence provenance from one stage to the next;
- clear claim boundaries.

The umbrella must still preserve child-stage separability. A failed early stage
should produce useful diagnostic evidence rather than causing the whole suite to
be described as a vague failure.

## Proposed Suite Identity

Recommended stable IDs:

```text
SUITE_ID = "plate_support_standard_gauntlet_v001"
SUITE_RUN_FAMILY_ID = "plate_support_standard_gauntlet_v001"
ENVIRONMENT_FAMILY_ID = "plate_support"
ENVIRONMENT_INSTANCE_ID = "plate_support_5x5_default_v001"
LINEARIZATION_MODE_ID = "tensor_available_disabled"
```

Stage IDs:

```text
plate_support_gauntlet_structural_tower_diagnostics_v001
plate_support_gauntlet_contraction_schema_sweep_v001
plate_support_gauntlet_candidate_discovery_v001
plate_support_gauntlet_tower_training_health_v001
plate_support_gauntlet_threshold_frontier_calibration_v001
plate_support_gauntlet_paired_replicate_comparison_v001
plate_support_gauntlet_readout_system_learning_v001
```

Recommended suite readout surface:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/
```

Recommended raw artifact root pattern:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/<run-label>/
```

This differs from environment readiness, which lives under:

```text
docs/environments/plate_support_5x5_default_v001/readiness/<run-label>/
```

## Stage Model

### Stage 0: Environment Readiness Input

This stage already exists and is outside the suite implementation proper.

Input:

```text
docs/environments/plate_support_5x5_default_v001/readiness/dev_001/readout_source.json
```

Role:

- prove environment binding and artifact support;
- supply exact graph facts;
- supply default and flat tower-readiness facts;
- supply training-surface availability;
- block the suite if environment readiness is missing or stale.

Claim boundary:

- environment readiness only.

### Stage 1: Structural And Tower Diagnostics

Role:

- promote environment-readiness facts into evaluation-stage diagnostics;
- verify the fixed gauntlet fixture;
- record exact graph, action legality, invalid/self-loop pressure, shortest
  path, reward scale, and tower shape;
- produce formal downstream inputs for schema sweep.

Output role:

- stage-1 diagnostic tables;
- suite-stage readiness status;
- no learning or comparison claims.

### Stage 2: Contraction Schema Sweep

Role:

- explore PlateSupport-specific schema/contraction choices;
- find tower structures that are not trivially flat and not pathologically
  collapsed;
- identify how schema strength changes tower shape and action availability.

Output role:

- candidate-producing structural sweep tables;
- no training claim.

### Stage 3: Candidate Discovery

Role:

- choose downstream candidate towers or schemas from Stage 2;
- record why each candidate is eligible, partial, blocked, or rejected;
- produce a candidate manifest for Stage 4 and Stage 6.

Output role:

- candidate manifest;
- candidate eligibility table;
- no performance claim.

### Stage 4: Tower Training Health

Role:

- run selected candidates through tower-only training-health checks;
- verify concrete steps, lift/action realization, tier/controller behavior,
  learner updates, and artifact completeness;
- classify candidates as trainable, warning, or blocked.

Output role:

- tower-training-health tables;
- candidate health status for downstream comparison;
- no flat-versus-tower superiority claim.

### Stage 5: Threshold Frontier Calibration

Role:

- determine PlateSupport-specific threshold/success-frontier criteria for
  comparison;
- avoid counterpoint's failure mode where an episode budget cannot satisfy a
  persistence rule;
- establish a meaningful, reachable, nontrivial comparison target.

Output role:

- calibrated threshold or success criterion;
- recommended paired-comparison budget settings;
- no final comparison claim.

### Stage 6: Paired Replicate Comparison

Role:

- compare flat/no-contraction baseline against selected tower/schema condition
  under matched seeds and calibrated target criteria;
- preserve paired evidence rather than aggregate-only evidence;
- produce the first claim-bearing comparison surface if the budget supports it.

Output role:

- paired replicate comparison tables;
- bounded first comparison claim or explicit non-claim.

### Stage 7: Readout And System Learning

Role:

- produce human-readable suite and stage reports;
- generate badges/status summaries;
- preserve system-learning notes and PO/Codex attribution;
- make the suite understandable without rereading raw tables.

Output role:

- repo-side README, result readouts, artifact index, glossary, method, runbook;
- durable design-learning archive when runs reveal confusion or integration
  issues.

## Stop Gates

Every stage must have an explicit gate.

Stage 1 may run only if:

- environment readiness exists;
- `state_collapser` dependency state records required PlateSupport surfaces;
- PlateSupport IDs match the environment doc.

Stage 2 may run only if:

- Stage 1 confirms graph/tower diagnostics are complete;
- Stage 1 produces exact action availability and tower-shape inputs;
- schema sweep definitions are PlateSupport-specific and documented.

Stage 3 may run only if:

- Stage 2 emits candidate-relevant tower/schema tables;
- candidate eligibility criteria are documented before selection.

Stage 4 may run only if:

- Stage 3 emits at least one eligible candidate;
- selected candidates are traceable to Stage 2 artifacts.

Stage 5 may run only if:

- Stage 1 and Stage 4 establish reward/step/health evidence sufficient to
  calibrate a target;
- the proposed threshold or success rule is feasible under the planned episode
  budget.

Stage 6 may run only if:

- Stage 3 supplies selected candidate(s);
- Stage 4 marks candidate(s) trainable or explicitly warning-but-usable;
- Stage 5 supplies a calibrated comparison target;
- matched seed/replicate policy is locked.

Stage 7 may run only if:

- at least one prior stage produced machine-readable artifacts;
- readout source files point to repo-resident artifacts.

## Shared Artifact Contract

The suite should write top-level artifacts:

```text
evaluation_manifest.json
evaluation_stage_manifest.json
evaluation_budget_lock.json
environment_source_manifest.json
readiness_source_manifest.json
stage_run_index.csv
stage_status_summary.csv
readout_source.json
```

Each child stage should write:

```text
stage_manifest.json
stage_budget_lock.json
stage_input_manifest.json
stage_output_manifest.json
stage_run_index.csv
stage_aggregate_summary.json
stage_aggregate_table.csv
results/*.csv
```

Every stage row should include:

```text
suite_id
stage_id
environment_family_id
environment_instance_id
artifact_root
status
claim_status
claim_boundary
source_stage_ids
source_artifact_paths
linearization_mode_id
state_collapser_dependency_status
```

## Shared Claim Status Vocabulary

Recommended claim statuses:

```text
environment_ready
diagnostic_complete
diagnostic_blocked
candidate_found
candidate_not_found
trainable_clean
trainable_warning
training_health_blocked
threshold_calibrated
threshold_unresolved
paired_comparison_positive_signal
paired_comparison_negative_signal
paired_comparison_inconclusive
artifact_incomplete
protocol_blocked
```

Each child stage may define additional local status fields, but the suite-level
readout should map them back to this vocabulary.

## Shared Budget Policy

The suite should start with a smoke/dev run and later support a fuller run.

Recommended run labels:

```text
smoke_001
dev_001
calibration_001
serious_001
```

The first implementation should probably avoid a serious budget unless the PO
explicitly authorizes it.

Every budget lock should record:

- run label;
- stage IDs included;
- environment instance ID;
- upstream state_collapser dependency state;
- seed bundle policy;
- replicate policy;
- episode/step budget;
- threshold or success rule if applicable;
- candidate source if applicable;
- linearization mode;
- locked-by operator.

## Suite Readout Shape

The suite readout README should start with:

- local badges;
- `Status At A Glance`;
- stage-by-stage status table;
- current strongest allowed claim;
- current blocked claims;
- links to child readouts;
- one paragraph explaining that counterpoint provided the role sequence, not
  literal PlateSupport mechanics.

The suite should keep child-stage README files if the stage outputs are large.

## Non-Goals

This suite architecture must not:

- copy counterpoint code blindly;
- pretend PlateSupport thresholds are known before calibration;
- treat tower depth as performance;
- treat candidate discovery as training evidence;
- treat tower-only training health as direct comparison evidence;
- claim broad tower superiority from a smoke run;
- create hidden temp artifacts outside the repo for durable readouts;
- erase environment-readiness provenance.

## Open Design Questions For Project Owner

### Question 1: Umbrella Name

Consultant recommendation:

```text
plate_support_standard_gauntlet_v001
```

Project Owner response:

```text
TODO
```

### Question 2: First Run Mode

Should the first implementation target:

```text
smoke_001
```

or:

```text
dev_001
```

Consultant recommendation: use `smoke_001` for the first code path, but allow
stage-level budgets to be richer than trivial one-episode smoke where required
for feasibility.

Project Owner response:

```text
TODO
```

### Question 3: One Workplan Or Staged Workplans

Consultant recommendation: one umbrella blueprint, child-stage blueprints, then
staged implementation workplans. A single giant workplan is possible only if it
has hard stop gates between stages.

Project Owner response:

```text
TODO
```

## Expected Next Blueprint

The next component blueprint should be:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/01_structural_and_tower_diagnostics/01_001_plate_support_structural_and_tower_diagnostics_blueprint.md
```

It should depend on this architecture blueprint and on the completed
PlateSupport environment-readiness artifacts.
