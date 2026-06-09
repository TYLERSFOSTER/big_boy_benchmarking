# PlateSupport Tower-Star Guarded Lift Comparison Implementation Workplan

## Status

Initial implementation workplan.

This workplan is derived from:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/10_tower_star/01_001_plate_support_tower_star_guarded_lift_comparison_blueprint.md
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/README.md
docs/design/first_plate_support_environment/standard_gauntlet_suite/09_direct_star_culdesac_control/01_002_plate_support_direct_star_culdesac_control_implementation_workplan.md
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
docs/prime_directive/common_failure_mode_005_umbrella_workplan_fragmentation.md
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/artifact_table_to_readable_document_protocol.md
docs/prime_directive/git_practices.md
```

Implementation must not silently simplify this workplan.

If an action cannot be implemented as written, the engineer must stop, record
the exact `Phase.Stage.Action` item, explain the blocker, and ask the Project
Owner for guidance.

This workplan must not invent Project Owner decisions. Attribution must remain:

- Abdul Malik, project PM, raised the original PlateSupport cul-de-sac /
  validity-filtering concern.
- The Project Owner accepted Abdul's concern, requested the direct-star
  diagnostic, and later requested the `tower_star` design folder and blueprint.
- Codex recommended the concrete tower-star action-surface design.
- In the user request that produced this workplan, the Project Owner instructed
  Codex to follow the blueprint's Codex-authored recommendations.

## Decision Locks Before Implementation

These are implementation locks for the first tower-star diagnostic.

```text
evaluation_id: plate_support_tower_star_guarded_lift_comparison_v001
cli_family: plate-support tower-star
implementation_branch: codex/plate-support-tower-star
source_package: src/big_boy_benchmarking/environments/plate_support/tower_star/
test_file: tests/environments/plate_support/test_tower_star.py
repo_readout_surface: docs/evaluations/plate_support_5x5_default_v001/tower_star/
artifact_run_label: tower_star_001
artifact_root: docs/evaluations/plate_support_5x5_default_v001/tower_star/artifacts/tower_star_001/
parent_gauntlet_source: docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
direct_star_source: docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json
candidate_scope: selected standard-gauntlet candidate only
budget_policy: reuse direct-star diagnostic budget for v001
primary_claim_pair: direct_nonself_guard versus tower_nonself_guard
blocked_surface_policy: diagnostic result and behavioral-comparison blocker
claim_boundary: diagnostic smoke/calibration evidence only
```

The six required arms are:

```text
direct_raw
direct_invalid_guard
direct_nonself_guard
tower_lift_executable_current
tower_invalid_guard
tower_nonself_guard
```

The three tower arms must be distinguished exactly:

```text
tower_lift_executable_current:
  current selected tower behavior using current liftability/executability
  action-cell surface.

tower_invalid_guard:
  quotient action cells remain available only if they have at least one
  executable concrete lift candidate whose primitive transition is not invalid.

tower_nonself_guard:
  quotient action cells remain available only if they have at least one
  executable concrete lift candidate whose primitive transition is nonself.
```

The direct-star arms must be rerun inside this evaluation. Imported
direct-star results may be included as context, but they must not be the
primary comparison values.

## Branch-Lineage Lock

Tower-star depends on the direct-star implementation and readout.

Before implementation begins, execution must establish one of these realities:

```text
preferred:
  direct-star work is committed and merged into the branch used as tower-star
  base.

acceptable:
  tower-star branch is created from the current direct-star branch, and the
  implementation log explicitly records that branch lineage.
```

Do not start tower-star from a branch that lacks:

- `src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/`;
- `docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json`;
- direct-star guard classifier semantics;
- direct-star test coverage.

## Explicit Non-Goals During Execution

Do not:

- modify the PlateSupport environment dynamics;
- modify `state_collapser`;
- change the standard gauntlet definition;
- overwrite the standard gauntlet result;
- overwrite the direct-star result;
- remove `direct_raw`;
- call the current tower arm `tower_raw`;
- implement tower-star as a post-hoc veto;
- implement tower-star by resampling selected lifts until one passes;
- fall back to current tower behavior when a tower-star arm has no available
  action cells;
- fall back to raw direct behavior when a direct-star arm has no available
  primitive actions;
- add reward lookahead, shortest-path lookahead, or multi-step reachability;
- claim final robotics benchmark significance.

## True Stop Conditions

Stop execution if:

- the branch-lineage lock cannot be satisfied;
- the parent gauntlet source is missing or malformed;
- the direct-star source is missing or malformed;
- the selected standard-gauntlet candidate cannot be resolved;
- the selected target policy cannot be resolved;
- the direct-star budget cannot be resolved and no explicit override is given;
- the current tower training surface cannot expose executable concrete lift
  candidates before tower action-cell selection;
- concrete lift candidate actions cannot be classified by the same one-step
  primitive transition classifier used by direct-star;
- selected tower candidate execution would require unapproved runtime
  semantics;
- tower-star can only be approximated by post-hoc veto or resampling;
- result tables cannot distinguish invalid moves from valid clipped
  self-loops;
- generated `readout_source.json` cannot support the artifact-table readout
  protocol;
- generated readout paths point outside the repo;
- tests or smoke artifacts contradict the workplan's tower-star semantics.

## Implementation Log Target

During execution, create and maintain:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/10_tower_star/01_003_plate_support_tower_star_guarded_lift_comparison_implementation_log.md
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
- Record dirty files relevant to tower-star.
- Record dirty files belonging to direct-star, because tower-star depends on
  that predecessor work.
- Record unrelated dirty files without modifying them.

Deliverables:

- implementation log entry with branch and dirty-state summary.

Verification:

- no unexamined dirty file is in a path this workplan will modify.

Stop if:

- there are conflicting uncommitted edits in:
  - `src/big_boy_benchmarking/environments/plate_support/tower_star/`;
  - `src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/`;
  - `src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/`;
  - `docs/evaluations/plate_support_5x5_default_v001/tower_star/`;
  - this `10_tower_star` design folder.

##### Phase 0.Stage 1.Action 2: Establish branch lineage

Action:

- Determine whether direct-star is already committed and available on the
  current base branch.
- If direct-star is merged, create or switch to:

```text
codex/plate-support-tower-star
```

- If direct-star is not merged but the Project Owner has instructed execution
  from the direct-star branch, create `codex/plate-support-tower-star` from the
  current direct-star branch and record that lineage.

Deliverables:

- implementation branch active.
- branch-lineage note in implementation log.

Verification:

- `git branch --show-current` reports the tower-star branch, or the log records
  the exact approved reason for continuing on a predecessor branch.
- direct-star package and direct-star readout source are visible.

Stop if:

- branch creation or checkout would discard existing work;
- direct-star dependency state is ambiguous.

##### Phase 0.Stage 1.Action 3: Re-read controlling documents

Action:

- Re-read:
  - this workplan;
  - the tower-star blueprint;
  - the direct-star blueprint and implementation log;
  - the direct-star evaluation README and readout source;
  - the standard gauntlet README and readout source;
  - prime directive docs listed above.

Deliverables:

- implementation log entry confirming controlling docs read.

Verification:

- source paths, artifact paths, arm definitions, and stop conditions match this
  workplan.

Stop if:

- a newer design artifact contradicts this workplan;
- a checked-in readout changes the selected candidate or target policy in a way
  this workplan does not account for.

#### Phase 0.Stage 2: Establish Implementation Log

##### Phase 0.Stage 2.Action 1: Create implementation log

Action:

- Create the implementation log named above.
- Add sections:
  - status;
  - controlling documents;
  - branch lineage;
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

#### Phase 1.Stage 1: Inspect Direct-Star Predecessor

##### Phase 1.Stage 1.Action 1: Inspect direct-star guard classifier

Action:

- Inspect:

```text
src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/guards.py
```

- Identify the exact classifier that defines:
  - invalid move;
  - self-loop;
  - valid clipped self-loop;
  - nonself transition.

Deliverables:

- implementation log note naming the classifier to reuse.

Verification:

- tower-star can import or match the same classifier without changing its
  semantics.

Stop if:

- direct and tower would require different transition definitions.

##### Phase 1.Stage 1.Action 2: Inspect direct-star runner and direct arms

Action:

- Inspect:

```text
src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/runner.py
src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/manifests.py
src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/events.py
```

- Identify reusable direct-arm Q-learning behavior, seed-bundle behavior, guard
  event shape, and blocked direct semantics.

Deliverables:

- implementation log note naming what will be imported, reused, copied, or
  minimally refactored.

Verification:

- direct-star behavior can be rerun inside tower-star without changing the
  existing direct-star evaluation.

Stop if:

- reusing direct-star direct arms would require altering historical direct-star
  results.

##### Phase 1.Stage 1.Action 3: Inspect direct-star aggregation and docs writer

Action:

- Inspect:

```text
src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/aggregation.py
src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/docs_writer.py
src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/paths.py
```

Deliverables:

- implementation log note identifying badge style, readout source structure,
  table-writing conventions, and result-doc conventions to mirror.

Verification:

- tower-star readout can match the successful direct-star report style.

Stop if:

- direct-star docs writer depends on assumptions incompatible with six-arm
  tower-star output.

#### Phase 1.Stage 2: Inspect Tower Training Surface

##### Phase 1.Stage 2.Action 1: Inspect tower action enumeration

Action:

- Inspect:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/training_surfaces.py
```

- Confirm how current tower action cells are enumerated.
- Confirm how `executable_lift_candidates` are obtained.
- Confirm how `representative_edges` and selected concrete lift edges are
  obtained.

Deliverables:

- implementation log note with the exact APIs used to enumerate:
  - tier;
  - state cell id;
  - action cell id;
  - representative edge count;
  - executable lift candidates;
  - selected edge/action index.

Verification:

- the log identifies a concrete pre-selection lift-candidate surface.

Stop if:

- executable lift candidates cannot be observed before action-cell selection.

##### Phase 1.Stage 2.Action 2: Inspect tower runtime step semantics

Action:

- Inspect the selected tower runner path and runtime step usage in:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/runner.py
src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/runner.py
```

Deliverables:

- implementation log note on how a selected tower action index is applied to
  the runtime and how resulting snapshot/reward/done metadata are observed.

Verification:

- tower-star can apply a chosen guarded lift as the same primitive action type
  the current tower applies.

Stop if:

- runtime execution requires data not present in the guarded lift candidate.

##### Phase 1.Stage 2.Action 3: Inspect tower Q-key semantics

Action:

- Inspect current tower Q-key construction:

```text
(tier, state_cell_id, action_cell_id)
```

- Determine whether tower-star arms should use the same Q-key for each action
  cell after guard filtering.

Deliverables:

- implementation log note on Q-key reuse.

Verification:

- `tower_lift_executable_current`, `tower_invalid_guard`, and
  `tower_nonself_guard` can each maintain separate Q tables while using the
  same action-cell key semantics.

Stop if:

- tower-star would require changing the meaning of Q keys.

#### Phase 1.Stage 3: Resolve Parent Evidence

##### Phase 1.Stage 3.Action 1: Load parent gauntlet source

Action:

- Load:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json
```

- Resolve:
  - source artifact root;
  - selected candidate;
  - selected schema;
  - target policy;
  - budget defaults;
  - dependency state.

Deliverables:

- parent gauntlet facts recorded in implementation log.

Verification:

- every resolved value has a source file path.

Stop if:

- any required parent fact must be guessed from prose.

##### Phase 1.Stage 3.Action 2: Load direct-star source

Action:

- Load:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json
```

- Resolve:
  - direct-star run label;
  - direct-star budget;
  - direct-star target;
  - direct-star arm matrix;
  - direct-star interpretation case;
  - source artifact root and source files.

Deliverables:

- direct-star provenance recorded in implementation log.

Verification:

- tower-star can reuse the direct-star budget and explain how direct-star
  context was imported.

Stop if:

- direct-star source is missing;
- direct-star budget conflicts with parent gauntlet target policy.

##### Phase 1.Stage 3.Action 3: Resolve first tower-star budget

Action:

- Set tower-star v001 budget from direct-star:
  - episodes per replicate;
  - replicates per arm;
  - max steps per episode;
  - base seed / paired seed policy;
  - target policy.

Deliverables:

- budget lock values recorded before code execution.

Verification:

- all six arms share one paired seed bundle policy.

Stop if:

- direct-star budget cannot be resolved unambiguously.

### Phase 2: Package, Configuration, And CLI Surface

#### Phase 2.Stage 1: Create Evaluation Package

##### Phase 2.Stage 1.Action 1: Create package directory

Action:

- Create:

```text
src/big_boy_benchmarking/environments/plate_support/tower_star/
```

Deliverables:

- package directory exists.

Verification:

- path is separate from `direct_star_culdesac_control/` and
  `standard_gauntlet/`.

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
- Define:
  - evaluation id;
  - environment family id;
  - environment instance id;
  - claim boundary;
  - run label;
  - artifact root;
  - repo root;
  - parent gauntlet source;
  - direct-star source;
  - locked-by;
  - episodes per replicate;
  - replicates per arm;
  - max steps;
  - learning rate;
  - discount;
  - epsilon;
  - arm ids;
  - tower guard types;
  - direct guard types.

Deliverables:

- explicit config object usable by runner, summarizer, docs writer, and tests.

Verification:

- no run parameter remains implicit in the runner.

Stop if:

- budget or target defaults cannot be derived from source artifacts.

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
  - docs/readout paths;
  - repo-placeholder conversion.

Deliverables:

- path helper functions that keep artifacts under:

```text
docs/evaluations/plate_support_5x5_default_v001/tower_star/
```

Verification:

- artifact roots are repo-resident and run-label scoped.

Stop if:

- path helpers would place durable artifacts in `/tmp` or outside the repo.

##### Phase 2.Stage 2.Action 3: Implement parent source loader

Action:

- Create `parent_source.py`.
- Load both:
  - parent gauntlet source;
  - direct-star source.
- Resolve selected candidate, target policy, budget, direct-star context, and
  prior interpretation.

Deliverables:

- source object with explicit provenance for both parents.

Verification:

- missing source files produce actionable errors before any run starts.

Stop if:

- selected candidate, target, or budget must be guessed from prose.

#### Phase 2.Stage 3: Register CLI

##### Phase 2.Stage 3.Action 1: Add run command

Action:

- Register:

```text
plate-support tower-star run
```

- Required args:
  - `--repo-root`;
  - `--artifact-root`;
  - `--parent-gauntlet-source`;
  - `--direct-star-source`;
  - `--run-label`;
  - `--locked-by`.

- Optional args:
  - `--episodes-per-replicate`;
  - `--replicates`;
  - `--max-steps`;
  - `--learning-rate`;
  - `--discount`;
  - `--epsilon`.

Deliverables:

- CLI run command wired to the new runner.

Verification:

- `uv run python -m big_boy_benchmarking.cli plate-support tower-star --help`
  displays the new family.

Stop if:

- CLI wiring would break existing `plate-support standard-gauntlet` or
  `plate-support direct-star-culdesac-control` commands.

##### Phase 2.Stage 3.Action 2: Add summarize command

Action:

- Register:

```text
plate-support tower-star summarize
```

- Required args:
  - `--repo-root`;
  - `--artifact-root`.

Deliverables:

- CLI summarize command regenerates docs and checked-in `readout_source.json`
  from existing artifacts.

Verification:

- summarize can run after smoke artifacts exist.

Stop if:

- summarize would require reading an ambiguous "last run".

### Phase 3: Guard Semantics And Tower Lift Surfaces

#### Phase 3.Stage 1: Reuse One-Step Primitive Classification

##### Phase 3.Stage 1.Action 1: Import or share direct-star classifier

Action:

- Reuse the direct-star primitive transition classifier for tower-star.
- Prefer importing from:

```text
src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/guards.py
```

- If a shared module becomes necessary, move the classifier narrowly and update
  direct-star tests to prove behavior is unchanged.

Deliverables:

- tower-star code path uses the same invalid/self/nonself vocabulary as
  direct-star.

Verification:

- tests show direct and tower lift classification agree for the same state and
  primitive action.

Stop if:

- importing or sharing the classifier changes direct-star behavior.

##### Phase 3.Stage 1.Action 2: Define tower-star guard ids

Action:

- Create `guards.py` or equivalent tower-star guard module.
- Define stable tower guard ids:

```text
current_lift_executable
invalid_guard
nonself_guard
```

Deliverables:

- guard ids map exactly to tower arms.

Verification:

- `tower_lift_executable_current`, `tower_invalid_guard`, and
  `tower_nonself_guard` each have unambiguous guard semantics.

Stop if:

- guard id naming makes current tower look raw or unfiltered.

#### Phase 3.Stage 2: Implement Lift-Candidate Observability

##### Phase 3.Stage 2.Action 1: Define lift-candidate records

Action:

- Create `tower_lifts.py`.
- Define a record for each concrete lift candidate with:

```text
tier
state_cell_id
action_cell_id
edge_id
action_index
candidate_lift_count
executable_lift_count
lift_executable
primitive_invalid_move
primitive_self_loop
primitive_valid_clipped_self_loop
primitive_nonself_transition
invalid_guard_compatible
nonself_guard_compatible
source_state_id
next_state_id
```

Deliverables:

- lift-candidate dataclass or typed record.

Verification:

- every field required by `tower_lift_guard_summary.csv` can be produced from
  the record.

Stop if:

- concrete lift candidates do not expose a primitive action that can be mapped
  to an action index.

##### Phase 3.Stage 2.Action 2: Enumerate action-cell lift pools

Action:

- Implement a function that, for one runtime snapshot, enumerates:
  - every currently executable tier;
  - every executable action cell at that tier;
  - representative edge count for the action cell;
  - executable lift candidates for the action cell;
  - primitive action index for each executable lift candidate.

Deliverables:

- complete pre-star action-cell/lift surface for the current decision point.

Verification:

- for `current_lift_executable`, the resulting action-cell list matches the
  existing current tower action surface.

Stop if:

- enumeration after filtering cannot reproduce current tower availability.

##### Phase 3.Stage 2.Action 3: Classify every executable lift candidate

Action:

- For each executable lift candidate, classify its primitive transition using
  the direct-star classifier.
- Record invalid/self/nonself fields and next state id.

Deliverables:

- classified lift-candidate surface.

Verification:

- selected lifts that produce runtime steps are classified consistently with
  step event metadata.

Stop if:

- primitive transition classification disagrees with runtime step metadata in
  smoke tests.

#### Phase 3.Stage 3: Implement Tower-Star Action-Cell Filtering

##### Phase 3.Stage 3.Action 1: Implement current tower guard surface

Action:

- Implement `available_tower_star_action_choices(..., guard_type="current_lift_executable")`.
- It should behave like current tower action-cell enumeration:
  - all executable action cells remain available;
  - the selected concrete lift follows current representative-lift behavior.

Deliverables:

- current tower arm can be run through the tower-star package without changing
  semantics.

Verification:

- current tower action choices match the existing direct-star/current tower
  runner on a smoke snapshot.

Stop if:

- current tower semantics cannot be reproduced.

##### Phase 3.Stage 3.Action 2: Implement invalid tower-star guard

Action:

- Implement `available_tower_star_action_choices(..., guard_type="invalid_guard")`.
- For each action cell:
  - keep only executable lifts whose primitive transition is not invalid;
  - remove the action cell if zero lifts survive;
  - select concrete lift only from surviving lifts.

Deliverables:

- invalid tower-star action surface.

Verification:

- tests prove an action cell with only invalid executable lifts is unavailable.
- tests prove a mixed action cell remains available with only clean lifts in
  its selected pool.

Stop if:

- invalid filtering can only be implemented after action-cell selection.

##### Phase 3.Stage 3.Action 3: Implement nonself tower-star guard

Action:

- Implement `available_tower_star_action_choices(..., guard_type="nonself_guard")`.
- For each action cell:
  - keep only executable lifts whose primitive transition is nonself;
  - remove the action cell if zero lifts survive;
  - select concrete lift only from surviving lifts.

Deliverables:

- nonself tower-star action surface.

Verification:

- tests prove an action cell with only self-loop executable lifts is
  unavailable.
- tests prove selected concrete lifts under this guard are always nonself.

Stop if:

- nonself filtering can only be implemented as post-hoc veto or resampling.

##### Phase 3.Stage 3.Action 4: Record lift-pool mixing classes

Action:

- Compute action-cell class fields:
  - all clean;
  - mixed clean and bad;
  - only invalid;
  - only self-loop;
  - only bad;
  - clean lift fraction;
  - nonself lift fraction.

Deliverables:

- per-decision data sufficient for `lift_pool_mixing_summary.csv`.

Verification:

- synthetic tests cover all classes.

Stop if:

- mixed lift pools cannot be distinguished from all-clean lift pools.

#### Phase 3.Stage 4: Implement Tower-Star Selection And Bootstrap

##### Phase 3.Stage 4.Action 1: Implement guarded tower action selection

Action:

- Choose the deepest tier with available guarded tower action cells.
- Apply epsilon-greedy selection over action cells available after the guard.
- Use stable tie-breaking consistent with current tower behavior where
  possible.

Deliverables:

- tower action selector for all three tower arms.

Verification:

- exploration and greedy branches both respect tower-star filtering.

Stop if:

- tower-star filtering is bypassed during epsilon exploration.

##### Phase 3.Stage 4.Action 2: Implement guarded tower Q bootstrap

Action:

- Compute next-state best value over the same guard-specific tower action
  surface at the next snapshot.

Deliverables:

- guard-aware Q update for `tower_invalid_guard` and `tower_nonself_guard`.

Verification:

- tests show tower-star arms bootstrap over their guarded action surface, not
  the current tower action surface.

Stop if:

- guarded arms bootstrap over unguarded/current tower choices.

##### Phase 3.Stage 4.Action 3: Implement tower-star blocked semantics

Action:

- If a tower-star guard removes all action cells:
  - record blocked decision;
  - end episode diagnostically;
  - do not fall back to current tower behavior;
  - mark comparison usability according to aggregation policy.

Deliverables:

- blocked tower-star event representation.

Verification:

- tests force empty guarded tower surface and assert no fallback action occurs.

Stop if:

- runner architecture cannot represent blocked tower decisions.

### Phase 4: Runner, Arms, Events, And Manifests

#### Phase 4.Stage 1: Build Arm And Budget Manifests

##### Phase 4.Stage 1.Action 1: Define arm records

Action:

- Create `manifests.py`.
- Define arm records for all six required arms.
- Include fields:
  - arm id;
  - arm type;
  - guard type;
  - information mode;
  - action surface description;
  - candidate id;
  - schema id;
  - claim role.

Deliverables:

- `evaluation_arm_manifest.json`.

Verification:

- all six arms are present and stable.

Stop if:

- current tower is mislabeled as raw.

##### Phase 4.Stage 1.Action 2: Write budget lock

Action:

- Write `evaluation_budget_lock.json`.
- Include:
  - parent gauntlet source;
  - direct-star source;
  - selected candidate id;
  - selected schema id;
  - target policy;
  - episodes;
  - replicates;
  - max steps;
  - learning parameters;
  - seed policy;
  - six arms;
  - tower-star semantics;
  - direct-star context;
  - claim boundary.

Deliverables:

- reproducible budget lock.

Verification:

- all run-changing values are captured.

Stop if:

- a run-changing value is implicit.

#### Phase 4.Stage 2: Define Event Schemas

##### Phase 4.Stage 2.Action 1: Define episode and step event fields

Action:

- Create `events.py`.
- Include episode and step fields compatible with direct-star where possible.
- Add tower-star-specific fields for blocked tower surfaces and guarded tower
  arm identity.

Deliverables:

- episode and step field constants.

Verification:

- `arm_summary.csv` can be computed from event rows.

Stop if:

- existing direct-star fields cannot represent necessary tower-star outcomes.

##### Phase 4.Stage 2.Action 2: Define direct guard event fields

Action:

- Reuse or mirror direct-star guard event fields.
- Ensure direct arms inside tower-star record guard before/after counts.

Deliverables:

- direct guard event table.

Verification:

- direct-star filtering remains visible beside tower-star filtering.

Stop if:

- direct-star arms become opaque inside tower-star.

##### Phase 4.Stage 2.Action 3: Define tower lift candidate event fields

Action:

- Define event rows for every observed tower action cell / lift pool.
- Include:
  - before-star action-cell availability;
  - after-invalid-star availability;
  - after-nonself-star availability;
  - lift counts;
  - selected lift flags;
  - mixing class flags;
  - blocked flags.

Deliverables:

- tower lift candidate event table.

Verification:

- every required field for `tower_lift_guard_summary.csv`,
  `tower_action_cell_surface_summary.csv`, and `lift_pool_mixing_summary.csv`
  is present or derivable.

Stop if:

- event rows would only record selected lifts and not available lift pools.

#### Phase 4.Stage 3: Implement Runner

##### Phase 4.Stage 3.Action 1: Implement direct arm reruns

Action:

- Implement direct arms inside tower-star:
  - `direct_raw`;
  - `direct_invalid_guard`;
  - `direct_nonself_guard`.
- Reuse direct-star selection, guard, Q update, and blocked semantics.

Deliverables:

- direct arm runs in tower-star artifacts.

Verification:

- direct arms use the tower-star paired seed bundles and write tower-star
  artifacts.

Stop if:

- direct arms are imported from old direct-star tables instead of rerun.

##### Phase 4.Stage 3.Action 2: Implement current tower arm

Action:

- Implement `tower_lift_executable_current`.
- Use selected parent candidate and current tower liftability/executability
  semantics.
- Record lift pool observability, even if no tower-star filtering is applied.

Deliverables:

- current tower arm in tower-star artifacts.

Verification:

- current tower produces coherent step, lift, tier, and learner events.

Stop if:

- current tower arm cannot be reconstructed from parent candidate.

##### Phase 4.Stage 3.Action 3: Implement tower invalid guard arm

Action:

- Implement `tower_invalid_guard` using guarded lift pools before tower action
  selection.

Deliverables:

- invalid tower-star arm in artifacts.

Verification:

- selected lifts are never invalid.
- action cells with only invalid lifts are not available.

Stop if:

- invalid guard requires post-hoc rejection.

##### Phase 4.Stage 3.Action 4: Implement tower nonself guard arm

Action:

- Implement `tower_nonself_guard` using guarded lift pools before tower action
  selection.

Deliverables:

- nonself tower-star arm in artifacts.

Verification:

- selected lifts are never self-loops.
- action cells with only self-loop lifts are not available.

Stop if:

- nonself guard requires post-hoc rejection.

##### Phase 4.Stage 3.Action 5: Write per-run artifacts

Action:

- For every arm/replicate run, write:
  - run manifest;
  - seed bundle;
  - mode manifest;
  - dependency manifest;
  - episode rows;
  - step rows;
  - controller rows;
  - learner rows;
  - direct guard rows where applicable;
  - tower lift candidate rows where applicable;
  - tier transition rows;
  - timing rows;
  - warnings.

Deliverables:

- complete run tree under the tower-star artifact root.

Verification:

- run index reports required and present files.

Stop if:

- artifact completeness cannot be audited.

### Phase 5: Aggregation And Interpretation

#### Phase 5.Stage 1: Build Result Tables

##### Phase 5.Stage 1.Action 1: Implement result table fieldnames

Action:

- Create `aggregation.py`.
- Define fieldnames for:
  - `paired_seed_bundle_summary`;
  - `evaluation_run_index`;
  - `evaluation_arm_manifest`;
  - `arm_summary`;
  - `paired_star_comparison`;
  - `tower_lift_guard_summary`;
  - `tower_action_cell_surface_summary`;
  - `lift_pool_mixing_summary`;
  - `direct_guard_filter_summary`;
  - `star_surface_blockage_summary`;
  - `interpretation_summary`;
  - `badge_summary`;
  - event tables;
  - `timing_summary`.

Deliverables:

- stable table schema map.

Verification:

- table names and required columns match the blueprint.

Stop if:

- a required blueprint table cannot be populated.

##### Phase 5.Stage 1.Action 2: Implement arm summary aggregation

Action:

- Aggregate one row per arm with:
  - target hit rate;
  - reward;
  - step count;
  - invalid/self rates;
  - blocked rates;
  - available action counts before/after star.

Deliverables:

- `arm_summary.csv`.

Verification:

- all six arms appear exactly once.

Stop if:

- direct and tower arms cannot be compared on shared target fields.

##### Phase 5.Stage 1.Action 3: Implement paired star comparisons

Action:

- Aggregate required comparison rows:

```text
direct_raw_vs_tower_current
direct_invalid_vs_tower_invalid
direct_nonself_vs_tower_nonself
tower_current_vs_tower_invalid
tower_current_vs_tower_nonself
direct_invalid_vs_direct_nonself
tower_invalid_vs_tower_nonself
```

Deliverables:

- `paired_star_comparison.csv`.

Verification:

- primary comparison `direct_nonself_guard` versus `tower_nonself_guard`
  exists and has a target-hit delta.

Stop if:

- primary comparison cannot be computed because one arm is missing or blocked
  without diagnostic explanation.

##### Phase 5.Stage 1.Action 4: Implement tower lift and surface summaries

Action:

- Aggregate:
  - `tower_lift_guard_summary.csv`;
  - `tower_action_cell_surface_summary.csv`;
  - `lift_pool_mixing_summary.csv`;
  - `star_surface_blockage_summary.csv`.

Deliverables:

- tower-star observability tables.

Verification:

- tables distinguish:
  - cells available before star;
  - cells removed by invalid star;
  - cells removed by nonself star;
  - mixed lift pools;
  - blocked tower-star decisions.

Stop if:

- tower-star tables cannot explain why an arm won, lost, or blocked.

##### Phase 5.Stage 1.Action 5: Implement direct guard summaries

Action:

- Aggregate direct guard filtering inside tower-star.

Deliverables:

- `direct_guard_filter_summary.csv`.

Verification:

- direct filtering counts are visible in the same readout as tower filtering
  counts.

Stop if:

- direct-star controls become black-box imported context.

#### Phase 5.Stage 2: Implement Interpretation Logic

##### Phase 5.Stage 2.Action 1: Implement primary interpretation cases

Action:

- Produce `interpretation_summary.csv` with one primary case:
  - `tower_survives_star_control`;
  - `direct_star_still_explains_signal`;
  - `tower_current_was_not_star_clean`;
  - `tower_current_already_star_clean`;
  - `tower_star_surface_blocked`;
  - `inconclusive_small_margin`.

Deliverables:

- primary interpretation row.

Verification:

- interpretation is derived from explicit result tables, not prose.

Stop if:

- result tables support multiple conflicting primary cases and no tie-break
  logic is documented.

##### Phase 5.Stage 2.Action 2: Implement blocked-claim and allowed-claim text

Action:

- Write claim text into `interpretation_summary.csv`.
- Ensure claim text stays inside calibration/smoke boundaries.

Deliverables:

- machine-readable allowed and blocked claim fields.

Verification:

- no generated claim says broad tower superiority, broad tower failure, or
  final robotics benchmark significance.

Stop if:

- generated interpretation would overclaim.

##### Phase 5.Stage 2.Action 3: Implement badge summary

Action:

- Produce badge rows for:
  - artifacts complete;
  - claim boundary;
  - direct-star complete;
  - tower-star complete;
  - primary interpretation;
  - tower surface blockage;
  - tower current star-clean status;
  - direct versus tower-star status;
  - provenance repo artifacts.

Deliverables:

- `badge_summary.csv`.

Verification:

- badge ids and colors can render to SVG badge files.

Stop if:

- badge summary would generate plain text badges instead of matching existing
  report style.

### Phase 6: Docs Writer, Readout Source, And Human Report Surface

#### Phase 6.Stage 1: Implement Docs Writer

##### Phase 6.Stage 1.Action 1: Create docs writer module

Action:

- Create `docs_writer.py`.
- Write:
  - `README.md`;
  - `method.md`;
  - `runbook.md`;
  - `artifact_index.md`;
  - `result_readout.md`;
  - `results/*.md`;
  - `badges/*.svg`;
  - top-level `readout_source.json`.

Deliverables:

- generated human-readable readout surface.

Verification:

- all docs are written under:

```text
docs/evaluations/plate_support_5x5_default_v001/tower_star/
```

Stop if:

- docs writer writes durable output outside the repo.

##### Phase 6.Stage 1.Action 2: Implement README structure

Action:

- Generate README sections:
  - badge strip;
  - status at a glance;
  - summary of goals;
  - summary of methodology;
  - one-screen verdict;
  - primary arm table;
  - direct-star versus tower-star comparison;
  - tower action-cell and lift-pool findings;
  - information parity warning;
  - attribution;
  - claim boundary;
  - inspection map;
  - clarifying questions and turns.

Deliverables:

- README matching the successful report style used elsewhere in the repo.

Verification:

- README explains:

```text
Direct-star filters primitive actions. Tower-star filters concrete lifts inside
quotient action cells before the tower chooses among those cells.
```

Stop if:

- README cannot be generated without inventing Project Owner turns.

##### Phase 6.Stage 1.Action 3: Implement attribution section

Action:

- Include attribution:
  - Abdul Malik raised the original cul-de-sac concern.
  - Project Owner requested `tower_star` follow-up.
  - Codex authored the implementation design details unless accepted or revised
    by the Project Owner.

Deliverables:

- explicit attribution in README and readout source.

Verification:

- no Codex-authored question or recommendation is formatted as a Project Owner
  statement.

Stop if:

- attribution cannot be rendered without ambiguity.

##### Phase 6.Stage 1.Action 4: Implement badge SVG writer

Action:

- Generate SVG badges from `badge_summary.csv` using existing badge style.

Deliverables:

- badge files in `badges/`.

Verification:

- README badge strip uses SVG image links like other generated reports.

Stop if:

- badges degrade to inconsistent plain Markdown/status text.

#### Phase 6.Stage 2: Implement Readout Source Contract

##### Phase 6.Stage 2.Action 1: Write readout source

Action:

- Write:

```text
docs/evaluations/plate_support_5x5_default_v001/tower_star/readout_source.json
```

- Include:
  - artifact schema version;
  - source binding type;
  - repo readout surface;
  - source artifact root;
  - source evaluation root;
  - evaluation id;
  - environment family id;
  - environment instance id;
  - artifact run label;
  - parent gauntlet source;
  - direct-star source;
  - calibrated target;
  - interpretation summary;
  - source files;
  - expected files;
  - goal criteria;
  - badge policy;
  - methodology summary sources;
  - structural limit checks;
  - claim boundary.

Deliverables:

- checked-in readout source binding.

Verification:

- readout source uses repo-relative paths.

Stop if:

- readout source points to machine-local temporary paths.

##### Phase 6.Stage 2.Action 2: Ensure artifact-table protocol compatibility

Action:

- Verify that the readout source can be used with:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/plate_support_5x5_default_v001/tower_star/readout_source.json
```

Deliverables:

- protocol-compatible source surface.

Verification:

- `source_files` includes all required tables and docs.

Stop if:

- the protocol would need to infer missing table roles.

### Phase 7: Tests And Verification

#### Phase 7.Stage 1: Unit Tests

##### Phase 7.Stage 1.Action 1: Add tower-star test file

Action:

- Create:

```text
tests/environments/plate_support/test_tower_star.py
```

Deliverables:

- test module.

Verification:

- pytest discovers the module.

Stop if:

- test path conflicts with existing tests.

##### Phase 7.Stage 1.Action 2: Test classifier parity

Action:

- Add tests proving tower-star uses the same primitive transition
  classification semantics as direct-star for representative PlateSupport
  states/actions.

Deliverables:

- classifier parity tests.

Verification:

- invalid, self-loop, valid clipped self-loop, and nonself cases are covered.

Stop if:

- classifier parity cannot be established.

##### Phase 7.Stage 1.Action 3: Test tower lift filtering

Action:

- Add synthetic or real-surface tests for:
  - action cell with all clean lifts;
  - mixed clean and bad lift pool;
  - only invalid lift pool;
  - only self-loop lift pool;
  - empty post-star action cell.

Deliverables:

- tower-star lift filtering tests.

Verification:

- action cells are removed only when zero guarded lifts remain.

Stop if:

- test scaffolding cannot observe lift pools without changing runtime
  semantics.

##### Phase 7.Stage 1.Action 4: Test selected lift source

Action:

- Add tests proving selected concrete lifts for guarded tower arms come from
  the guarded lift pool.

Deliverables:

- selected-lift integrity tests.

Verification:

- no selected lift violates its arm guard.

Stop if:

- selected lifts are chosen before guard filtering.

##### Phase 7.Stage 1.Action 5: Test blocked semantics

Action:

- Add tests proving direct-star and tower-star blocked surfaces do not fall
  back to raw/current behavior.

Deliverables:

- blocked semantics tests.

Verification:

- forced empty direct/tower surfaces produce diagnostic block events.

Stop if:

- runner cannot represent blocked events.

#### Phase 7.Stage 2: Integration Tests

##### Phase 7.Stage 2.Action 1: Test CLI help and command registration

Action:

- Run:

```text
uv run python -m big_boy_benchmarking.cli plate-support tower-star --help
```

Deliverables:

- CLI help output.

Verification:

- run and summarize subcommands appear.

Stop if:

- CLI registration breaks existing commands.

##### Phase 7.Stage 2.Action 2: Test smoke run

Action:

- Run a small smoke execution with repo-resident artifact root, parent gauntlet
  source, and direct-star source.

Deliverables:

- smoke artifacts under the tower-star readout surface.

Verification:

- six arms run or produce explicit diagnostic blockage.

Stop if:

- smoke run produces partial artifacts without clear blocked status.

##### Phase 7.Stage 2.Action 3: Test summarize

Action:

- Run summarize against the smoke artifact root.

Deliverables:

- generated docs and `readout_source.json`.

Verification:

- README, result docs, badges, and readout source exist.

Stop if:

- summarize depends on ambiguous last-run state.

##### Phase 7.Stage 2.Action 4: Run pytest

Action:

- Run:

```text
uv run pytest tests/environments/plate_support/test_tower_star.py
```

- Run any affected direct-star and PlateSupport gauntlet tests.

Deliverables:

- test results recorded in implementation log.

Verification:

- tower-star tests pass.
- direct-star tests still pass if touched.

Stop if:

- tests fail and the fix would require changing blueprint semantics.

### Phase 8: First Repo-Resident Diagnostic Run

#### Phase 8.Stage 1: Run `tower_star_001`

##### Phase 8.Stage 1.Action 1: Prepare clean artifact root

Action:

- Ensure the intended artifact root is explicit:

```text
docs/evaluations/plate_support_5x5_default_v001/tower_star/artifacts/tower_star_001/
```

- If it already exists from a failed run, stop and ask before deleting or
  overwriting.

Deliverables:

- clean or intentionally reused artifact root.

Verification:

- no accidental old run is mixed into the new readout.

Stop if:

- cleaning would require destructive deletion not explicitly approved.

##### Phase 8.Stage 1.Action 2: Run evaluation

Action:

- Run:

```text
uv run python -m big_boy_benchmarking.cli plate-support tower-star run \
  --repo-root "$BBB_ROOT" \
  --artifact-root "$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/tower_star/artifacts/tower_star_001" \
  --parent-gauntlet-source "$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json" \
  --direct-star-source "$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json" \
  --run-label tower_star_001 \
  --locked-by foster
```

Deliverables:

- raw event and result artifacts.

Verification:

- command exits successfully or writes explicit diagnostic blocked result.

Stop if:

- command fails without a machine-readable blocked result.

##### Phase 8.Stage 1.Action 3: Summarize evaluation

Action:

- Run:

```text
uv run python -m big_boy_benchmarking.cli plate-support tower-star summarize \
  --repo-root "$BBB_ROOT" \
  --artifact-root "$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/tower_star/artifacts/tower_star_001"
```

Deliverables:

- generated human-readable readout and source binding.

Verification:

- `docs/evaluations/plate_support_5x5_default_v001/tower_star/readout_source.json`
  exists.

Stop if:

- summarize cannot regenerate from artifacts alone.

#### Phase 8.Stage 2: Apply Human-Readable Protocol

##### Phase 8.Stage 2.Action 1: Regenerate protocol readout

Action:

- Apply:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/plate_support_5x5_default_v001/tower_star/readout_source.json
```

Deliverables:

- final generated README/readout docs consistent with protocol.

Verification:

- top-level README is coherent for a human reader.
- badges render in the expected style.
- no generated text overclaims.

Stop if:

- protocol output contradicts source tables or claim boundary.

##### Phase 8.Stage 2.Action 2: Inspect generated README

Action:

- Inspect the generated README.
- Confirm it contains:
  - primary verdict;
  - primary arm table;
  - direct-star versus tower-star table;
  - tower lift-pool explanation;
  - information parity warning;
  - Abdul/PO/Codex attribution;
  - clarifying-turn section.

Deliverables:

- implementation log note on README quality.

Verification:

- README is understandable without opening raw CSVs.

Stop if:

- README repeats the prior badge/report style failure or omits the central
  tower-star explanation.

### Phase 9: Documentation Integration And Final Checks

#### Phase 9.Stage 1: Update Design And Evaluation Indexes

##### Phase 9.Stage 1.Action 1: Update design folder README if needed

Action:

- Update:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/10_tower_star/README.md
```

- Link blueprint, workplan, implementation log, and readout after execution.

Deliverables:

- current design index.

Verification:

- future engineers can find the implementation state from the folder README.

Stop if:

- update would imply execution happened before it did.

##### Phase 9.Stage 1.Action 2: Update evaluation indexes if needed

Action:

- Update relevant evaluation indexes only after the run and readout exist.

Possible files:

```text
docs/evaluations/README.md
docs/evaluations/plate_support_5x5_default_v001/README.md
README.md
```

Deliverables:

- non-stale links to tower-star diagnostic.

Verification:

- root docs describe tower-star as diagnostic evidence, not final benchmark
  evidence.

Stop if:

- root docs would need broader release framing changes outside this workplan.

#### Phase 9.Stage 2: Final Verification

##### Phase 9.Stage 2.Action 1: Run targeted tests

Action:

- Run:

```text
uv run pytest tests/environments/plate_support/test_tower_star.py
```

- If direct-star helpers were touched, also run:

```text
uv run pytest tests/environments/plate_support/test_direct_star_culdesac_control.py
```

Deliverables:

- final targeted test result.

Verification:

- tests pass.

Stop if:

- tests fail.

##### Phase 9.Stage 2.Action 2: Run repository hygiene checks

Action:

- Run available repo hygiene checks that are relevant to this work.
- At minimum inspect:

```text
git status --short
```

- If public-release hygiene is relevant, run:

```text
uv run python scripts/release_hygiene.py --repo-root .
```

Deliverables:

- final dirty-state and hygiene notes.

Verification:

- generated artifacts are intentionally tracked or intentionally ignored.

Stop if:

- machine-local paths or generated junk are present in tracked docs.

##### Phase 9.Stage 2.Action 3: Complete implementation log

Action:

- Mark every completed `Phase.Stage.Action`.
- Record:
  - final files changed;
  - commands run;
  - test outcomes;
  - generated artifacts;
  - unresolved issues;
  - exact resume point if any work remains.

Deliverables:

- complete implementation log.

Verification:

- a future engineer can resume without reconstructing state from chat.

Stop if:

- unresolved blockers are not clearly documented.

## Expected Final File Additions

Expected source additions:

```text
src/big_boy_benchmarking/environments/plate_support/tower_star/__init__.py
src/big_boy_benchmarking/environments/plate_support/tower_star/aggregation.py
src/big_boy_benchmarking/environments/plate_support/tower_star/config.py
src/big_boy_benchmarking/environments/plate_support/tower_star/docs_writer.py
src/big_boy_benchmarking/environments/plate_support/tower_star/events.py
src/big_boy_benchmarking/environments/plate_support/tower_star/guards.py
src/big_boy_benchmarking/environments/plate_support/tower_star/manifests.py
src/big_boy_benchmarking/environments/plate_support/tower_star/parent_source.py
src/big_boy_benchmarking/environments/plate_support/tower_star/paths.py
src/big_boy_benchmarking/environments/plate_support/tower_star/runner.py
src/big_boy_benchmarking/environments/plate_support/tower_star/tower_lifts.py
```

Expected test addition:

```text
tests/environments/plate_support/test_tower_star.py
```

Expected design addition:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/10_tower_star/01_003_plate_support_tower_star_guarded_lift_comparison_implementation_log.md
```

Expected evaluation surface after run:

```text
docs/evaluations/plate_support_5x5_default_v001/tower_star/
```

## Completion Criteria

The work is complete only when:

- all six required arms are represented;
- direct arms are rerun inside tower-star;
- tower-star arms filter concrete lift candidates before tower action-cell
  selection;
- selected tower-star lifts come from guarded lift pools;
- blocked direct/tower surfaces do not fall back silently;
- required result tables exist;
- readout source points at repo-resident artifacts;
- README is human-readable and protocol-compatible;
- attribution is explicit and correct;
- targeted tests pass;
- implementation log records final state.

## Resume Rule

If implementation pauses, resume by opening:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/10_tower_star/01_003_plate_support_tower_star_guarded_lift_comparison_implementation_log.md
```

Then continue from the first incomplete `Phase.Stage.Action`.

Do not restart from the blueprint unless the implementation log is missing or
explicitly marked invalid.
