# PlateSupport Direct-Star Cul-de-sac Control Implementation Workplan

## Status

Initial implementation workplan.

This workplan is derived from:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/09_direct_star_culdesac_control/01_001_plate_support_direct_star_culdesac_control_blueprint.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/09_direct_star_culdesac_control/design_discussion.md
state_collapser_invalid_action_self_loop_filtering_issue.md
```

This workplan uses `Phase.Stage.Action` discipline.

This workplan is not execution approval by itself. Execution begins only when
the Project Owner explicitly asks to execute this workplan.

## Prime Directive Binding

This workplan follows:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/artifact_table_to_readable_document_protocol.md
docs/prime_directive/git_practices.md
```

Implementation must not silently simplify this workplan.

If an action cannot be implemented as written, the engineer must stop, record
the exact `Phase.Stage.Action` item, explain the blocker, and ask the Project
Owner for guidance.

This workplan must not invent Project Owner decisions. Attribution must remain:

- Abdul Malik, project PM, raised the self-loop / cul-de-sac concern.
- The Project Owner accepted the concern as important and asked for a BBB-side
  repair blueprint and workplan.
- Codex recommended the concrete guarded-direct control design.

## Decision Locks Before Implementation

These are implementation defaults derived from the blueprint. They are
consultant-authored defaults unless directly attributed above.

```text
evaluation_id: plate_support_direct_star_culdesac_control_v001
cli_family: plate-support direct-star-culdesac-control
implementation_branch: codex/plate-support-direct-star-culdesac-control
source_package: src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/
test_file: tests/environments/plate_support/test_direct_star_culdesac_control.py
repo_readout_surface: docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/
parent_gauntlet_source: docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
artifact_run_labels: smoke_001, guarded_001
guarded_direct_policy: pre-mask before action selection
guarded_block_policy: diagnostic blocked termination; no silent raw fallback
claim_boundary: diagnostic smoke/calibration evidence only
```

The four required arms are:

```text
direct_raw
direct_invalid_guard
direct_nonself_guard
tower_selected_candidate
```

The guarded direct arms must remain explicit arms. They must not replace or
rename the original direct baseline.

The direct guards are intentionally one-step local-transition guards:

```text
direct_invalid_guard:
  mask primitive actions whose primitive_transition(state, action).invalid_move
  is True.

direct_nonself_guard:
  mask primitive actions whose primitive_transition(state, action).next_state
  equals the current state.
```

The guarded direct arms must not receive:

- reward lookahead;
- goal-distance lookahead;
- multi-step reachability;
- future liftability information;
- schema or tier information;
- model-based action ranking;
- any future-state value other than ordinary learned Q bootstrap.

Every generated readout must include an information parity warning: these
guarded direct arms are oracle one-step local guards, not proven perfectly
matched tower-equivalent controllers.

## Explicit Non-Goals During Execution

Do not:

- modify `state_collapser`;
- change PlateSupport primitive environment semantics;
- change the existing standard gauntlet Stage 6 result in place;
- silently replace `direct_raw` with a guarded direct arm;
- call `direct_nonself_guard` "fair direct" without qualification;
- delete or overwrite historical gauntlet artifacts;
- regenerate human-readable docs from a folder-only artifact path;
- create a readout without a checked-in `readout_source.json`;
- make final robotics benchmark claims.

## True Stop Conditions

Stop execution if:

- the parent gauntlet readout source is missing or malformed;
- the selected tower candidate cannot be resolved from parent artifacts;
- the selected Stage 5 target policy cannot be resolved from parent artifacts;
- parent artifacts needed for candidate reconstruction are not available;
- `state_collapser` dependency metadata is incompatible with the current
  PlateSupport pointwise liftability semantics;
- the tower selected candidate has no executable action cells at the initial
  state;
- direct guard implementation would need reward or multi-step lookahead;
- a guarded direct arm would silently fall back to raw direct;
- summaries cannot distinguish invalid self-loops from valid clipped
  self-transitions;
- generated `readout_source.json` cannot support the artifact-table readout
  protocol;
- tests or smoke artifacts contradict the workplan's action-surface parity
  assumptions.

## Implementation Log Target

During execution, create and maintain:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/09_direct_star_culdesac_control/01_003_plate_support_direct_star_culdesac_control_implementation_log.md
```

The log must record completed `Phase.Stage.Action` items, file changes, test
commands, test outcomes, artifacts generated, surprises, blockers, and Project
Owner clarifications.

## Workplan

### Phase 0: Execution Setup And Reality Binding

#### Phase 0.Stage 1: Verify Repository State

##### Phase 0.Stage 1.Action 1: Verify branch and dirty state

Action:

- Run `git status --short --branch`.
- Record the current branch.
- Record dirty files relevant to this work.
- Record unrelated dirty files without modifying them.

Deliverables:

- implementation log entry with branch and dirty-state summary.

Verification:

- no unexamined dirty file is in a path this workplan will modify.

Stop if:

- there are conflicting uncommitted edits in:
  - `src/big_boy_benchmarking/environments/plate_support/`;
  - `tests/environments/plate_support/`;
  - `docs/evaluations/plate_support_5x5_default_v001/`;
  - this design folder.

##### Phase 0.Stage 1.Action 2: Create or switch to implementation branch

Action:

- Create or switch to:

```text
codex/plate-support-direct-star-culdesac-control
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
  - the design discussion;
  - the root `state_collapser` handoff;
  - prime directive docs listed above;
  - the existing PlateSupport standard gauntlet Stage 4, Stage 5, Stage 6,
    and readout-system-learning implementation files.

Deliverables:

- implementation log entry confirming controlling docs read.

Verification:

- source paths, artifact paths, and arm definitions match this workplan.

Stop if:

- a newer design artifact contradicts this workplan.

#### Phase 0.Stage 2: Establish Implementation Log

##### Phase 0.Stage 2.Action 1: Create implementation log

Action:

- Create the implementation log named above.
- Add sections:
  - status;
  - controlling documents;
  - decision locks;
  - `Phase.Stage.Action` progress;
  - commands run;
  - files changed;
  - tests and verification;
  - artifacts generated;
  - blockers and surprises;
  - Project Owner clarifications.

Deliverables:

- implementation log file.

Verification:

- log exists before source edits begin.

Stop if:

- log path conflicts with unrelated content.

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

- auditable progress table.

Verification:

- every future work item can be mapped to exactly one row.

Stop if:

- the log cannot preserve Phase.Stage.Action status clearly.

### Phase 1: Existing Source And Parent Evidence Reality Check

#### Phase 1.Stage 1: Inspect Existing PlateSupport Comparison Code

##### Phase 1.Stage 1.Action 1: Inspect paired replicate comparison runner

Action:

- Inspect:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison/runner.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison/events.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison/arms.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison/target_policy.py
```

Deliverables:

- implementation log notes identifying reusable direct Q-learning functions,
  tower execution functions, event schemas, and target-policy handling.

Verification:

- the log names the exact functions or classes to reuse.

Stop if:

- the existing direct baseline cannot be isolated without changing historical
  Stage 6 behavior.

##### Phase 1.Stage 1.Action 2: Inspect tower training surfaces

Action:

- Inspect:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/training_surfaces.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/runner.py
```

Deliverables:

- implementation log notes on how to reconstruct and execute the selected
  tower candidate.

Verification:

- the selected tower arm can be implemented without inventing a new tower
  execution path.

Stop if:

- selected candidate execution requires unapproved runtime semantics.

##### Phase 1.Stage 1.Action 3: Inspect gauntlet readout/source helpers

Action:

- Inspect:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/readout_source.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/readout_system_learning/
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paths.py
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/manifests.py
```

Deliverables:

- implementation log notes on readout source shape, badge conventions, and
  repo-resident artifact conventions.

Verification:

- new evaluation can produce a readout source compatible with the artifact
  table protocol.

Stop if:

- existing helpers require modification that would break standard gauntlet
  readouts.

#### Phase 1.Stage 2: Resolve Parent Gauntlet Evidence

##### Phase 1.Stage 2.Action 1: Load parent gauntlet source binding

Action:

- Load:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```

- Resolve repo readout surface, source artifact root, source evaluation roots,
  and expected source files.

Deliverables:

- parent source facts recorded in the implementation log.

Verification:

- parent readout source points to available repo-resident evidence or clearly
  declared release-asset evidence.

Stop if:

- parent source binding points to missing evidence and no approved restoration
  path exists.

##### Phase 1.Stage 2.Action 2: Resolve selected candidate and schema

Action:

- Resolve the selected iterated tower candidate from the parent artifacts.
- Record candidate id, schema id, schema family, schema mode, depth, and
  training-health status.

Deliverables:

- selected candidate provenance in log.

Verification:

- selected candidate matches the candidate used by the existing Stage 6 paired
  comparison.

Stop if:

- multiple candidates are eligible but the selected Stage 6 candidate cannot be
  identified.

##### Phase 1.Stage 2.Action 3: Resolve calibrated target policy

Action:

- Resolve the Stage 5 threshold/target policy used by Stage 6.
- Record target id, threshold value, target metric, comparison budget, and
  replicate/episode defaults.

Deliverables:

- target policy provenance in log.

Verification:

- the new evaluation can reuse the same target policy without recalibration.

Stop if:

- target policy is missing or ambiguous.

##### Phase 1.Stage 2.Action 4: Verify dependency semantics

Action:

- Inspect dependency manifests or project dependency state to confirm the
  expected `state_collapser` pointwise liftability semantics.

Deliverables:

- dependency compatibility note in the log.

Verification:

- dependency state is compatible with `state_collapser` v0.7.2 or newer
  semantics expected by current PlateSupport artifacts.

Stop if:

- dependency semantics are older, missing, or ambiguous enough to affect tower
  liftability/action-cell behavior.

### Phase 2: Package, Configuration, And CLI Surface

#### Phase 2.Stage 1: Create Evaluation Package

##### Phase 2.Stage 1.Action 1: Create package directory

Action:

- Create:

```text
src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/
```

Deliverables:

- package directory exists.

Verification:

- path is separate from `standard_gauntlet/paired_replicate_comparison/`.

Stop if:

- creating the package would overwrite unrelated files.

##### Phase 2.Stage 1.Action 2: Add module initializer

Action:

- Create `__init__.py`.
- Export stable public symbols only after their modules exist.

Deliverables:

- importable package initializer.

Verification:

- importing the package does not run evaluations or read/write artifacts.

Stop if:

- import side effects would be required.

#### Phase 2.Stage 2: Define Configuration And Paths

##### Phase 2.Stage 2.Action 1: Implement config dataclasses

Action:

- Create `config.py`.
- Define configuration for:
  - artifact root;
  - repo root;
  - parent gauntlet source;
  - run label;
  - locked-by;
  - episodes per replicate;
  - replicates;
  - max steps;
  - arm ids;
  - guard types;
  - target policy;
  - selected candidate policy;
  - smoke/full run mode.

Deliverables:

- explicit config object usable by runner, summarizer, docs writer, and tests.

Verification:

- no run parameter remains implicit in the runner.

Stop if:

- budget or target defaults cannot be derived from parent artifacts.

##### Phase 2.Stage 2.Action 2: Implement path helpers

Action:

- Create `paths.py`.
- Define:
  - repo readout surface;
  - source artifact root;
  - source evaluation root;
  - result table paths;
  - run tree paths;
  - readout source path;
  - docs/readout paths.

Deliverables:

- path helper functions that keep artifacts under:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/
```

Verification:

- artifact roots are repo-resident and run-label scoped.

Stop if:

- path helpers would place durable artifacts in `/tmp` or outside the repo.

##### Phase 2.Stage 2.Action 3: Implement parent source loader

Action:

- Create `parent_source.py`.
- Load parent gauntlet readout source.
- Resolve selected candidate, target policy, and prior comparison metadata.

Deliverables:

- parent source object with explicit provenance.

Verification:

- missing source files produce actionable errors before any run starts.

Stop if:

- selected candidate or target must be guessed from prose.

#### Phase 2.Stage 3: Register CLI

##### Phase 2.Stage 3.Action 1: Add run command

Action:

- Register:

```text
plate-support direct-star-culdesac-control run
```

- Required args:
  - `--repo-root`;
  - `--artifact-root`;
  - `--parent-gauntlet-source`;
  - `--run-label`;
  - `--locked-by`.

- Optional args:
  - `--episodes-per-replicate`;
  - `--replicates`;
  - `--max-steps`;
  - `--smoke`;
  - `--allow-release-asset-parent` only if needed and explicitly logged.

Deliverables:

- CLI run command wired to the new runner.

Verification:

- `uv run python -m big_boy_benchmarking.cli plate-support direct-star-culdesac-control --help`
  displays the new family.

Stop if:

- CLI wiring would break existing `plate-support standard-gauntlet` commands.

##### Phase 2.Stage 3.Action 2: Add summarize command

Action:

- Register:

```text
plate-support direct-star-culdesac-control summarize
```

- Required args:
  - `--repo-root`;
  - `--artifact-root`.

Deliverables:

- CLI summarize command writes result tables, docs scaffolding, and
  `readout_source.json`.

Verification:

- summarize can run after smoke artifacts exist.

Stop if:

- summarize would require reading an ambiguous "last run".

### Phase 3: Guard Semantics And Direct Action Surfaces

#### Phase 3.Stage 1: Implement Primitive Transition Classification

##### Phase 3.Stage 1.Action 1: Create guard module

Action:

- Create `guards.py`.
- Define stable guard ids:

```text
raw
invalid_guard
nonself_guard
```

Deliverables:

- guard id constants or enum.

Verification:

- guard ids match arm ids and artifact fields.

Stop if:

- guard id naming conflicts with existing arm ids.

##### Phase 3.Stage 1.Action 2: Implement transition classifier

Action:

- Implement:

```text
classify_primitive_transition(surface, state, action)
```

- The classifier must report:
  - candidate next state;
  - invalid move boolean;
  - self-loop boolean;
  - valid clipped self-loop boolean;
  - non-self boolean.

Deliverables:

- transition classification object.

Verification:

- invalid self-loops and valid clipped self-loops remain distinguishable.

Stop if:

- PlateSupport surface does not expose enough transition metadata to separate
  invalid from valid clipped self-transitions.

#### Phase 3.Stage 2: Implement Guarded Available Actions

##### Phase 3.Stage 2.Action 1: Implement raw action surface

Action:

- Implement `available_direct_actions(surface, state, "raw")`.
- Return all primitive actions in `range(ACTION_COUNT)`.

Deliverables:

- raw action list behavior matching historical direct baseline.

Verification:

- unit test proves `direct_raw` still sees the ambient primitive action count.

Stop if:

- raw action list differs from existing direct baseline.

##### Phase 3.Stage 2.Action 2: Implement invalid guard action surface

Action:

- Implement `available_direct_actions(surface, state, "invalid_guard")`.
- Exclude only primitive actions classified as invalid moves.

Deliverables:

- invalid-guard action list.

Verification:

- unit tests show valid clipped self-transitions are not removed solely because
  of this guard.

Stop if:

- implementation removes valid clipped self-transitions from invalid guard.

##### Phase 3.Stage 2.Action 3: Implement nonself guard action surface

Action:

- Implement `available_direct_actions(surface, state, "nonself_guard")`.
- Exclude primitive actions whose transition returns the same concrete state.

Deliverables:

- nonself-guard action list.

Verification:

- unit tests show the nonself guard removes every invalid-guarded action and
  also valid clipped self-transitions.

Stop if:

- implementation cannot distinguish `next_state == state`.

##### Phase 3.Stage 2.Action 4: Implement guard summaries

Action:

- Implement:

```text
summarize_guard(surface, state, guard_type)
```

- Include:
  - before count;
  - after count;
  - invalid filtered count;
  - self-loop filtered count;
  - all-actions-filtered indicator.

Deliverables:

- guard summary object used by runner and event rows.

Verification:

- unit tests cover each guard type.

Stop if:

- summary counts are inconsistent with available action lists.

#### Phase 3.Stage 3: Implement Guarded Block Semantics

##### Phase 3.Stage 3.Action 1: Add blocked-step outcome

Action:

- Define a diagnostic blocked outcome for guarded direct when zero actions are
  available.
- The blocked outcome must not choose a raw primitive action.

Deliverables:

- blocked outcome type or event representation.

Verification:

- tests can force an empty available action list and assert no raw fallback.

Stop if:

- existing runner architecture requires an action every step and cannot record
  blocked termination without larger redesign.

##### Phase 3.Stage 3.Action 2: Add information parity metadata

Action:

- Add metadata fields declaring:

```text
guard_information_mode: oracle_one_step_local_transition
information_parity_warning_required: true
```

Deliverables:

- metadata included in manifests and readout source.

Verification:

- docs writer can render the warning without guessing.

Stop if:

- implementation would imply guarded direct is a perfectly matched
  tower-equivalent baseline.

### Phase 4: Runner, Arms, And Event Rows

#### Phase 4.Stage 1: Build Arm Manifest

##### Phase 4.Stage 1.Action 1: Define arm records

Action:

- Create `manifests.py`.
- Define arm records for:
  - `direct_raw`;
  - `direct_invalid_guard`;
  - `direct_nonself_guard`;
  - `tower_selected_candidate`.

Deliverables:

- `evaluation_arm_manifest.json`.

Verification:

- all four arms have stable ids, roles, guard types, action-surface
  descriptions, and information-mode descriptions.

Stop if:

- any guarded arm is represented as a replacement for raw direct.

##### Phase 4.Stage 1.Action 2: Write budget lock

Action:

- Write `evaluation_budget_lock.json`.
- Include:
  - parent gauntlet source;
  - selected candidate id;
  - selected schema id;
  - target policy;
  - episodes;
  - replicates;
  - max steps;
  - seed policy;
  - four arms;
  - guard semantics;
  - claim boundary.

Deliverables:

- reproducible budget lock.

Verification:

- all run-changing values are captured.

Stop if:

- a run-changing value is implicit.

#### Phase 4.Stage 2: Implement Direct Arm Runner

##### Phase 4.Stage 2.Action 1: Reuse raw direct behavior

Action:

- Implement `direct_raw` using the existing direct Q-learning behavior.
- Do not add guard filtering to this arm.

Deliverables:

- raw direct arm runner.

Verification:

- tests show raw direct can choose any primitive action.

Stop if:

- raw direct behavior changes relative to existing Stage 6 direct baseline.

##### Phase 4.Stage 2.Action 2: Implement guard-aware direct selection

Action:

- Implement direct action selection over
  `available_direct_actions(surface, state, guard_type)`.
- Apply guard before epsilon exploration and greedy selection.

Deliverables:

- guarded direct action selector.

Verification:

- tests show exploration and greedy branches both respect guard.

Stop if:

- guard is implemented as post-selection resampling or veto.

##### Phase 4.Stage 2.Action 3: Implement guard-aware Q bootstrap

Action:

- Compute next-best Q values over the same guard-specific action list at the
  next state.

Deliverables:

- guard-aware Q update.

Verification:

- tests show `direct_invalid_guard` and `direct_nonself_guard` use different
  next-best action surfaces when appropriate.

Stop if:

- guarded arms bootstrap over raw direct's full action list.

##### Phase 4.Stage 2.Action 4: Implement guarded blocked termination

Action:

- If a guarded arm has zero available actions:
  - record blocked status;
  - set `guard_fallback_used=True`;
  - end the episode diagnostically;
  - do not execute a primitive action.

Deliverables:

- guarded blocked behavior in runner.

Verification:

- synthetic test proves no raw fallback.

Stop if:

- blocked events cannot be represented in summary tables.

#### Phase 4.Stage 3: Implement Tower Arm Runner

##### Phase 4.Stage 3.Action 1: Reconstruct selected tower candidate

Action:

- Reconstruct the selected iterated tower candidate from parent candidate and
  schema metadata.

Deliverables:

- selected tower runtime/control object.

Verification:

- reconstructed tower schema id and candidate id match parent artifacts.

Stop if:

- candidate reconstruction would require hard-coded ids or schema assumptions.

##### Phase 4.Stage 3.Action 2: Run selected tower arm

Action:

- Run `tower_selected_candidate` using existing tower execution surfaces.
- Do not add direct-style guard masks to tower.

Deliverables:

- tower arm per-run artifacts.

Verification:

- tower arm emits action-surface and liftability data comparable to current
  Stage 6 artifacts.

Stop if:

- tower arm cannot report selected primitive action classifications.

#### Phase 4.Stage 4: Emit Event Rows

##### Phase 4.Stage 4.Action 1: Write guard events

Action:

- Emit `guard_events.csv` with at least:

```text
run_id
episode_index
step_index
arm_id
guard_type
state_id
available_action_count_before_guard
available_action_count_after_guard
guarded_action_count
invalid_guard_filtered_count
self_loop_guard_filtered_count
all_actions_filtered_count
guard_fallback_used
chosen_action
chosen_action_would_have_been_invalid
chosen_action_would_have_been_self_loop
chosen_action_transition_was_invalid
chosen_action_transition_was_self_loop
chosen_action_transition_was_valid_clipped_self_loop
next_state_id
reward
done
```

Deliverables:

- guard event file per run or evaluation-level event table.

Verification:

- tests assert required columns exist.

Stop if:

- tower primitive action classifications cannot be represented in the same
  event surface.

##### Phase 4.Stage 4.Action 2: Write step and episode events

Action:

- Emit step and episode rows compatible with existing PlateSupport comparison
  summaries.
- Include blocked episode status when relevant.

Deliverables:

- per-arm episode and step evidence.

Verification:

- aggregation can compute reward, success, invalid, self-loop, and blocked
  counts without reading raw logs manually.

Stop if:

- blocked status is dropped from episode summaries.

##### Phase 4.Stage 4.Action 3: Write run manifests

Action:

- Write per-run manifests with:
  - arm id;
  - guard type;
  - information mode;
  - candidate id where applicable;
  - target policy;
  - seed bundle;
  - dependency manifest;
  - parent source manifest.

Deliverables:

- per-run manifest files.

Verification:

- every run can be traced to parent gauntlet artifacts.

Stop if:

- provenance would require machine-local paths in public-facing fields.

### Phase 5: Aggregation And Interpretation

#### Phase 5.Stage 1: Aggregate Required Tables

##### Phase 5.Stage 1.Action 1: Create aggregation module

Action:

- Create `aggregation.py`.
- Load guard, step, episode, and manifest artifacts.

Deliverables:

- aggregation entrypoint.

Verification:

- aggregation fails clearly on missing required event columns.

Stop if:

- raw event files are insufficient to compute required summary tables.

##### Phase 5.Stage 1.Action 2: Write arm summary

Action:

- Generate:

```text
results/arm_summary.csv
```

- Include:
  - episode count;
  - replicate count;
  - total concrete steps;
  - mean total reward;
  - mean goal success;
  - mean binary success;
  - mean first hit step;
  - invalid move count/rate;
  - self-transition count/rate;
  - valid clipped self-transition count;
  - non-self transition count;
  - blocked episode count;
  - guard fallback count.

Deliverables:

- `arm_summary.csv`.

Verification:

- summary separates invalid and valid clipped self-transition counts.

Stop if:

- invalid and valid clipped self-transitions collapse into one undifferentiated
  self-loop metric.

##### Phase 5.Stage 1.Action 3: Write guard filter summary

Action:

- Generate:

```text
results/guard_filter_summary.csv
```

- Include:
  - arm id;
  - guard type;
  - mean/min/max available before and after guard;
  - mean invalid filtered;
  - mean self-loop filtered;
  - all actions filtered count.

Deliverables:

- `guard_filter_summary.csv`.

Verification:

- `direct_raw`, `direct_invalid_guard`, and `direct_nonself_guard` are all
  distinguishable in the table.

Stop if:

- guard summaries do not expose information-mode differences.

##### Phase 5.Stage 1.Action 4: Write self-loop and invalid summaries

Action:

- Generate:

```text
results/self_loop_summary.csv
results/invalid_vs_self_loop_summary.csv
```

Deliverables:

- self-loop classification tables.

Verification:

- tables answer how much raw direct failure came from invalid moves versus
  valid clipped self-transitions.

Stop if:

- the tables cannot isolate Abdul's self-loop hypothesis.

##### Phase 5.Stage 1.Action 5: Write paired guard comparison

Action:

- Generate:

```text
results/paired_guard_comparison.csv
```

- Compare:
  - tower versus `direct_raw`;
  - tower versus `direct_invalid_guard`;
  - tower versus `direct_nonself_guard`;
  - `direct_invalid_guard` versus `direct_raw`;
  - `direct_nonself_guard` versus `direct_invalid_guard`.

Deliverables:

- paired comparison table.

Verification:

- table includes binary success, total reward, invalid rate, self-loop rate,
  and first-hit-step differences where applicable.

Stop if:

- pair alignment is lost and arms are compared across mismatched seeds.

##### Phase 5.Stage 1.Action 6: Write action surface summary

Action:

- Generate:

```text
results/action_surface_summary.csv
```

- Include raw direct ambient action counts, guarded direct action counts, tower
  executable action-cell counts, and tower executable lift candidate counts
  where available.

Deliverables:

- action-surface comparison table.

Verification:

- the table supports the information parity warning.

Stop if:

- tower action-surface counts cannot be extracted or honestly marked missing.

#### Phase 5.Stage 2: Classify Result Meaning

##### Phase 5.Stage 2.Action 1: Implement interpretation grid

Action:

- Create classification logic matching the blueprint cases:
  - tower beats raw but not invalid guard;
  - tower beats invalid guard but not nonself guard;
  - tower beats nonself guard;
  - nonself guard beats tower;
  - noisy/inconclusive.

Deliverables:

- interpretation classification row or JSON summary.

Verification:

- each case has allowed and disallowed claim text.

Stop if:

- classification would require a final benchmark claim.

##### Phase 5.Stage 2.Action 2: Implement badge derivation

Action:

- Derive badge statuses for:
  - artifact status;
  - guarded direct status;
  - self-loop confound;
  - tower vs nonself;
  - blocked guard states;
  - claim boundary.

Deliverables:

- badge summary inputs and generated local two-segment SVG badges.

Verification:

- badge text is reader-facing `Label: Value` text, not raw snake-case statuses.

Stop if:

- badge styling diverges from existing evaluation readouts.

##### Phase 5.Stage 2.Action 3: Emit information parity warning summary

Action:

- Generate a summary field/table that states:

```text
The guarded direct controls use oracle one-step local transition masks. They
diagnose invalid/self-loop filtering but are not a proof of perfect action
surface parity with the tower.
```

Deliverables:

- parity warning in machine-readable summary and generated docs.

Verification:

- README can render the warning near the top.

Stop if:

- generated docs imply `direct_nonself_guard` is simply the fair baseline.

### Phase 6: Source Binding And Human-Readable Readout Surface

#### Phase 6.Stage 1: Write Readout Source

##### Phase 6.Stage 1.Action 1: Implement docs writer

Action:

- Create `docs_writer.py`.
- Write:
  - `readout_source.json`;
  - `method.md`;
  - `runbook.md`;
  - `artifact_index.md`;
  - initial `README.md` if local convention requires a generated stub before
    protocol readout.

Deliverables:

- repo readout surface:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/
```

Verification:

- `readout_source.json` points to repo-resident source artifacts under the
  same readout surface.

Stop if:

- source binding requires ambiguous folder inference.

##### Phase 6.Stage 1.Action 2: Populate expected-file policy

Action:

- In `readout_source.json`, include required, conditional, not-applicable, and
  expected-absent file policy.

Deliverables:

- expected-file policy.

Verification:

- readout protocol can distinguish missing evidence from not-applicable files.

Stop if:

- expected files cannot be classified before readout generation.

##### Phase 6.Stage 1.Action 3: Populate goal criteria and claim boundary

Action:

- Add `goal_criteria`, `structural_limit_checks`, `badge_policy`,
  `goal_summary_sources`, `methodology_summary_sources`, and `claim_boundary`.

Deliverables:

- complete evaluation construction contract.

Verification:

- readout protocol has enough context to answer the required readout
  questions without reverse-engineering code.

Stop if:

- goal criteria cannot state allowed and blocked claims.

#### Phase 6.Stage 2: Generate Human-Readable Docs

##### Phase 6.Stage 2.Action 1: Apply artifact readout protocol

Action:

- Generate the human-readable readout from:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json
```

- Use:

```text
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

Deliverables:

- README and supporting human-readable docs.

Verification:

- generated README answers the seven required readout questions from the
  blueprint.

Stop if:

- the protocol cannot generate a truthful readout from the source binding.

##### Phase 6.Stage 2.Action 2: Verify badge and README style

Action:

- Compare generated README badges against existing BBB evaluation readouts.
- Confirm badge labels are compact, human-facing, and visually consistent.

Deliverables:

- README style verification note in implementation log.

Verification:

- badges are local SVG files and use `Label: Value` text.

Stop if:

- badges look unlike existing public readouts.

### Phase 7: Tests And Smoke Validation

#### Phase 7.Stage 1: Add Focused Tests

##### Phase 7.Stage 1.Action 1: Add guard tests

Action:

- Create:

```text
tests/environments/plate_support/test_direct_star_culdesac_control.py
```

- Test:
  - raw returns all primitive actions;
  - invalid guard removes invalid actions only;
  - nonself guard removes invalid and valid clipped self-transitions;
  - guard summaries match action lists;
  - empty guard lists trigger blocked behavior without raw fallback.

Deliverables:

- focused guard tests.

Verification:

- `uv run pytest tests/environments/plate_support/test_direct_star_culdesac_control.py`
  passes.

Stop if:

- tests cannot force or observe the required transition classifications.

##### Phase 7.Stage 1.Action 2: Add runner and aggregation tests

Action:

- Add tests for:
  - four-arm manifest;
  - guard-aware direct selection;
  - guard-aware next-best Q bootstrap;
  - tower selected candidate arm metadata;
  - required summary tables;
  - readout source fields.

Deliverables:

- runner and aggregation tests.

Verification:

- focused test file passes.

Stop if:

- runner behavior cannot be tested without long evaluation budgets.

##### Phase 7.Stage 1.Action 3: Add CLI tests

Action:

- Extend PlateSupport CLI tests to cover:
  - help output;
  - smoke run command;
  - summarize command.

Deliverables:

- CLI coverage.

Verification:

- CLI tests pass without requiring the full guarded run.

Stop if:

- CLI tests would mutate durable checked-in evaluation artifacts.

#### Phase 7.Stage 2: Run Test Suite

##### Phase 7.Stage 2.Action 1: Run focused tests

Action:

- Run:

```bash
uv run pytest tests/environments/plate_support/test_direct_star_culdesac_control.py
```

Deliverables:

- test output recorded in implementation log.

Verification:

- focused tests pass.

Stop if:

- any focused test fails.

##### Phase 7.Stage 2.Action 2: Run related PlateSupport tests

Action:

- Run:

```bash
uv run pytest tests/environments/plate_support/test_standard_gauntlet_paired_replicate_comparison.py tests/environments/plate_support/test_cli_plate_support.py
```

Deliverables:

- related test output recorded in implementation log.

Verification:

- related tests pass.

Stop if:

- changes regress existing paired comparison or CLI behavior.

##### Phase 7.Stage 2.Action 3: Run broader PlateSupport tests

Action:

- Run:

```bash
uv run pytest tests/environments/plate_support
```

Deliverables:

- broader PlateSupport test output recorded in implementation log.

Verification:

- tests pass or failures are unrelated and documented.

Stop if:

- failures are related to the new evaluation or guard logic.

#### Phase 7.Stage 3: Run Smoke Evaluation

##### Phase 7.Stage 3.Action 1: Run smoke artifacts

Action:

- Run a small smoke evaluation:

```bash
uv run python -m big_boy_benchmarking.cli plate-support direct-star-culdesac-control run \
  --repo-root . \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/smoke_001 \
  --parent-gauntlet-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json \
  --run-label smoke_001 \
  --locked-by foster \
  --smoke
```

Deliverables:

- smoke artifacts under the repo readout surface.

Verification:

- all four arms run or fail with explicit, logged reasons.

Stop if:

- smoke run cannot resolve parent selected candidate or target.

##### Phase 7.Stage 3.Action 2: Summarize smoke artifacts

Action:

- Run:

```bash
uv run python -m big_boy_benchmarking.cli plate-support direct-star-culdesac-control summarize \
  --repo-root . \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/smoke_001
```

Deliverables:

- smoke summary tables and readout source.

Verification:

- required tables exist.

Stop if:

- summarize omits required guard or action-surface tables.

##### Phase 7.Stage 3.Action 3: Generate smoke human readout

Action:

- Apply the artifact-table readout protocol to:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json
```

Deliverables:

- human-readable smoke README and supporting docs.

Verification:

- README includes information parity warning and diagnostic claim boundary.

Stop if:

- README makes a stronger claim than the artifacts support.

### Phase 8: Guarded Diagnostic Run

#### Phase 8.Stage 1: Run Full Diagnostic Budget

##### Phase 8.Stage 1.Action 1: Run guarded diagnostic artifacts

Action:

- Run the non-smoke diagnostic using the parent Stage 6 budget unless the
  Project Owner supplies a different budget:

```bash
uv run python -m big_boy_benchmarking.cli plate-support direct-star-culdesac-control run \
  --repo-root . \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/guarded_001 \
  --parent-gauntlet-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json \
  --run-label guarded_001 \
  --locked-by foster
```

Deliverables:

- full diagnostic artifacts under `artifacts/guarded_001`.

Verification:

- run manifest shows all four arms, parent candidate, target policy, and guard
  information mode.

Stop if:

- the run would overwrite `smoke_001` or historical standard gauntlet artifacts.

##### Phase 8.Stage 1.Action 2: Summarize guarded diagnostic artifacts

Action:

- Run:

```bash
uv run python -m big_boy_benchmarking.cli plate-support direct-star-culdesac-control summarize \
  --repo-root . \
  --artifact-root docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/guarded_001
```

Deliverables:

- full diagnostic summary tables and updated `readout_source.json`.

Verification:

- `readout_source.json` binds to `guarded_001`, not `smoke_001`.

Stop if:

- readout source accidentally points at smoke artifacts after full run.

#### Phase 8.Stage 2: Generate Final Diagnostic Readout

##### Phase 8.Stage 2.Action 1: Apply artifact-table readout protocol

Action:

- Apply:

```text
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

- To:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json
```

Deliverables:

- final guarded diagnostic README and supporting docs.

Verification:

- README classifies the result using the blueprint interpretation grid.

Stop if:

- README loses the Abdul/PO/Codex attribution or information parity warning.

##### Phase 8.Stage 2.Action 2: Archive system-learning consequences if needed

Action:

- If the guarded diagnostic reveals a new system-learning issue, create or
  update a design-side archive under:

```text
docs/design/system_learning_from_evaluations/
```

Deliverables:

- system-learning note only if a real issue is discovered.

Verification:

- note distinguishes PM observation, Project Owner framing, and Codex
  interpretation.

Stop if:

- no real system-learning issue exists; do not create filler archive content.

### Phase 9: Final Verification And Handoff

#### Phase 9.Stage 1: Verify Repository Hygiene

##### Phase 9.Stage 1.Action 1: Check git status

Action:

- Run `git status --short`.

Deliverables:

- final dirty-state summary in implementation log.

Verification:

- modified files are limited to this workplan's scope and generated artifacts.

Stop if:

- unrelated files were modified.

##### Phase 9.Stage 1.Action 2: Check generated docs for public hygiene

Action:

- Check generated docs for:
  - machine-local path leakage;
  - ambiguous "last run" language;
  - fake Project Owner turns;
  - overclaiming;
  - badge style drift.

Deliverables:

- hygiene note in implementation log.

Verification:

- docs comply with prime directive readout rules.

Stop if:

- public-facing generated docs contain machine-local paths or false
  attribution.

##### Phase 9.Stage 1.Action 3: Optional release hygiene check

Action:

- If this work is being prepared for public beta/release, run:

```bash
uv run python scripts/release_hygiene.py --repo-root .
```

Deliverables:

- release hygiene output in implementation log.

Verification:

- hygiene passes or issues are recorded for correction.

Stop if:

- release hygiene reports public-facing issues.

#### Phase 9.Stage 2: Final Implementation Report

##### Phase 9.Stage 2.Action 1: Complete implementation log

Action:

- Mark all completed Phase.Stage.Action rows.
- Record commands, tests, artifacts, and any stops.

Deliverables:

- complete implementation log.

Verification:

- log is sufficient for a future engineer to resume or audit the work.

Stop if:

- log omits failed commands or surprises.

##### Phase 9.Stage 2.Action 2: Provide merge/status summary

Action:

- Report:
  - branch;
  - files changed;
  - tests run;
  - artifacts generated;
  - readout path;
  - remaining limitations;
  - merge command if requested by Project Owner.

Deliverables:

- concise final handoff to Project Owner.

Verification:

- final response does not overclaim beyond diagnostic evidence.

Stop if:

- unresolved blockers remain hidden.
