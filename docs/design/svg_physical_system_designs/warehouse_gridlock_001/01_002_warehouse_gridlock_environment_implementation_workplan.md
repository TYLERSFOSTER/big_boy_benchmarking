# Warehouse Gridlock 001 Environment Implementation Workplan

## Status

Initial implementation workplan.

This workplan is derived from:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_001_warehouse_gridlock_environment_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md
```

This workplan uses `Phase.Stage.Action` discipline.

This workplan is not execution approval. Execution begins only when the Project
Owner explicitly asks to execute this workplan.

## Prime Directive Binding

This workplan follows:

```text
docs/prime_directive/prime_directive.md
docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md
docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md
docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
docs/prime_directive/git_practices.md
```

Implementation must not silently simplify this workplan.

If an action cannot be implemented as written, the engineer must stop, record
the exact `Phase.Stage.Action` item, explain the blocker, and ask the Project
Owner for guidance.

This workplan must not invent Project Owner turns. All Project Owner decisions
used here are taken from the source design note and blueprint. Consultant
recommendations remain consultant recommendations unless the Project Owner
explicitly accepts them.

## Context Reestablishment Notes

This section records the context corrections that must be carried into
implementation so later engineers do not reintroduce superseded early-design
language.

### Source Note Location

The current source design note is:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md
```

Older references to:

```text
docs/design/svg_physical_system_designs/warehouse_001.md
```

are stale after the Warehouse Gridlock design material was moved into the
dedicated `warehouse_gridlock_001` folder.

### Tiny/Small Instance Supersession

The source design note contains early Codex recommendations about a possible
tiny/small/medium instance ladder. Those recommendations are superseded by the
later Project Owner decision recorded in the blueprint under Q8:

```text
No official tiny benchmark instance.
No official tiny calibration ladder.
No tiny-first implementation path.
```

The implementation may still use deliberately small hand-authored
micro-fixtures inside tests. Those fixtures are engineering tests only. They
must not be named, documented, artifacted, or interpreted as official
environment instances, calibration instances, evaluation targets, or benchmark
evidence.

The blueprint also contains a stale implementation-surface snippet mentioning
`WAREHOUSE_GRIDLOCK_TINY_V001` and `WAREHOUSE_GRIDLOCK_SMALL_V001`. That snippet
is superseded by the same Q8 decision. The id list in this workplan is the
authoritative id list for execution.

### Workplan Creation Despite Remaining Gates

The blueprint originally said not to create an implementation workplan until
Q6/Q7 and related mechanics were resolved or explicitly accepted as workplan
assumptions. The Project Owner subsequently directed creation of the workplan.

Therefore this document is allowed to exist, but execution is not allowed to
pass Phase 0.Stage 3 until the unresolved mechanics are resolved and logged.
This is the control boundary that prevents the workplan from becoming an
unauthorized implementation decision.

## Decision Locks Before Implementation

These locks come from Project Owner-authored SVGs, Project Owner replies in the
blueprint, or explicit Project Owner clarifications.

```text
environment_family_id: warehouse_gridlock_001
implementation_family_id: warehouse_gridlock_v001
first benchmark-facing instance: warehouse_gridlock_16x16_v001
official tiny calibration instances: forbidden for this environment
unit-test micro-fixtures: allowed, but not benchmark instances
grid: 16 x 16 full PO drawing
robots: R01 through R32
boxes: B01 through B32
timestep: one second
control: synchronous ensemble action, one command per robot per timestep
per-robot commands: north, south, east, west, stay
graph edge direction: bidirectional visible red graph edges
box interaction: push-only unless later PO changes it
success: exact labeled boxes and exact labeled robots at exact target nodes
columns: concrete blocked physical regions, even if visual nodes appear inside
collision: shared-node final occupancy invalid
collision: head-on edge swaps invalid
action space: structured ensemble surface, never flat-enumerated for full instance
hidden MDP: serious admissible-state/action graph is not precomputed or handed out
discovery: required for all arms and recorded in artifacts
cross-tier discovery pressure: retained hypothesis only, not implemented now
```

## Pre-Implementation Decision Gates

The blueprint still contains unresolved or partially unresolved mechanics. This
workplan may be written now, but execution must not pass Phase 0.Stage 3 until
these are resolved or explicitly accepted as workplan assumptions.

### Gate A: Invalid Ensemble Time

Question:

```text
If an ensemble action is invalid, does the one-second timestep still pass?
```

Consultant recommendation:

```text
yes, invalid ensemble attempts consume one second
```

Reason:

- this preserves the timed robotics interpretation;
- hidden-admissibility discovery has a natural cost;
- negative elapsed-time reward penalizes failed probing without needing a
  special invalid penalty.

### Gate B: Partial Execution

Question:

```text
If any part of the synchronous ensemble is invalid, does the whole ensemble
self-loop with no robot/box movement?
```

Consultant current interpretation of the Project Owner's "NO" reply:

```text
no partial execution
whole-ensemble invalidation
no robot or box moves when the ensemble is invalid
```

This interpretation must be confirmed before code.

### Gate C: Reward Constants

The reward shape is locked:

```text
success reward
negative elapsed-time reward
per-correct-box reward
per-correct-robot reward
```

The numeric constants are not locked. They may be chosen during implementation
only if the Project Owner accepts consultant defaults.

### Gate D: Column Manifest Authority

The implementation must specify exact blocked nodes and blocked edges for the
concrete columns. This can be done through a manually reviewed manifest derived
from the PO drawings.

The workplan may create the manifest, but execution must stop if the engineer
cannot determine column-covered nodes/edges without guessing.

## Explicit Non-Goals During This Workplan

Do not:

- create official tiny or calibration environment instances;
- create a standard gauntlet for Warehouse Gridlock;
- create a tower comparison evaluation;
- implement cross-tier discovery pressure;
- implement a learned policy;
- claim the full 16 x 16 instance is solvable;
- claim tower advantage;
- claim benchmark readiness beyond environment readiness;
- edit `state_collapser`;
- overwrite or reinterpret PlateSupport or Counterpoint artifacts;
- turn micro-fixture tests into evaluation evidence;
- flat-enumerate the full `5^32` action space.

## Expected Deliverables

Implementation should produce:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/
tests/environments/warehouse_gridlock/
docs/environments/warehouse_gridlock_001/
docs/evaluations/warehouse_gridlock_001/environment_readiness/
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_003_warehouse_gridlock_environment_implementation_log.md
```

The environment package should expose:

```text
graph loading and validation
state validation
structured ensemble actions
synchronous transition engine
collision validation
push-only box dynamics
reward modes
hidden-admissibility discovery event summaries
full-instance readiness diagnostics
readout-source generation
CLI smoke commands
```

The CLI should expose at least:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock graph-diagnostics
uv run python -m big_boy_benchmarking.cli warehouse-gridlock state-diagnostics
uv run python -m big_boy_benchmarking.cli warehouse-gridlock transition-smoke
uv run python -m big_boy_benchmarking.cli warehouse-gridlock random-rollout
uv run python -m big_boy_benchmarking.cli warehouse-gridlock readiness-docs
```

## Implementation Log Target

During execution, create and maintain:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_003_warehouse_gridlock_environment_implementation_log.md
```

The log must record:

- current branch and dirty state before edits;
- controlling documents read;
- every completed `Phase.Stage.Action`;
- every command run;
- every changed file;
- test results;
- generated artifacts;
- unresolved questions;
- stop conditions;
- surprises or reality breaks.

## Workplan

### Phase 0: Execution Setup, Authority Binding, And Decision Gates

#### Phase 0.Stage 1: Verify Repository State

##### Phase 0.Stage 1.Action 1: Verify branch and dirty state

Action:

- run `git status --short --branch`;
- record the current branch, dirty tracked files, and untracked files in the
  implementation log.

Deliverables:

- implementation log entry with branch and dirty-state summary.

Verification:

- current branch is known;
- no unexamined dirty file sits in a path this workplan will edit.

Stop if:

- there are conflicting uncommitted edits in:
  - `src/big_boy_benchmarking/environments/warehouse_gridlock/`;
  - `tests/environments/warehouse_gridlock/`;
  - `docs/environments/warehouse_gridlock_001/`;
  - `docs/evaluations/warehouse_gridlock_001/`;
  - this design folder.

##### Phase 0.Stage 1.Action 2: Create or switch to implementation branch

Action:

- create or switch to:

```text
codex/warehouse-gridlock-environment
```

Deliverables:

- implementation branch active.

Verification:

- `git branch --show-current` reports the implementation branch.

Stop if:

- checkout would discard or obscure existing user work.

##### Phase 0.Stage 1.Action 3: Re-read controlling documents

Action:

- re-read:
  - this workplan;
  - the Warehouse Gridlock environment blueprint;
  - `docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md`;
  - `environment_construction_for_benchmark_evaluations_protocol.md`;
  - `common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`;
  - `git_practices.md`;
  - current CLI patterns in `src/big_boy_benchmarking/cli/`;
  - existing environment package patterns for PlateSupport and Counterpoint.

Deliverables:

- implementation log entry listing controlling documents and package patterns
  read.

Verification:

- source paths and expected outputs match the workplan.

Stop if:

- a newer design artifact contradicts this workplan;
- the repository has already implemented Warehouse Gridlock differently.

#### Phase 0.Stage 2: Establish Implementation Log

##### Phase 0.Stage 2.Action 1: Create implementation log

Action:

- create the implementation log file named above;
- add sections:
  - status;
  - branch and repo state;
  - controlling documents;
  - decision locks;
  - `Phase.Stage.Action` progress;
  - commands run;
  - files changed;
  - tests and validation;
  - artifacts generated;
  - blockers and surprises;
  - final summary.

Deliverables:

- implementation log exists before source implementation starts.

Verification:

- log has all required sections.

Stop if:

- log file path conflicts with an existing unrelated file.

##### Phase 0.Stage 2.Action 2: Add progress table

Action:

- add a progress table with columns:

```text
Phase.Stage.Action
Status
Files
Verification
Notes
```

Deliverables:

- log can track every action as `pending`, `in_progress`, `completed`, or
  `blocked`.

Verification:

- every Phase 0 action is represented in the progress table.

Stop if:

- logging would require rewriting the workplan while executing it.

#### Phase 0.Stage 3: Resolve Required Gates Before Code

##### Phase 0.Stage 3.Action 1: Resolve invalid ensemble time

Action:

- record whether invalid ensemble attempts consume one second.

Consultant default to use only if PO explicitly accepts:

```text
invalid ensembles consume one second
```

Deliverables:

- implementation log entry naming the chosen rule.

Verification:

- the chosen rule is reflected in the transition-policy manifest draft.

Stop if:

- the rule remains unresolved.

##### Phase 0.Stage 3.Action 2: Resolve partial execution semantics

Action:

- confirm whether invalid ensembles use whole-ensemble invalidation.

Consultant current interpretation to use only if PO explicitly confirms:

```text
no partial execution
invalid ensemble means no robot or box moves
```

Deliverables:

- implementation log entry naming the chosen rule.

Verification:

- transition-policy manifest draft includes `partial_execution: false` or an
  explicit alternative.

Stop if:

- the Project Owner's "NO" reply remains ambiguous.

##### Phase 0.Stage 3.Action 3: Resolve reward defaults

Action:

- define initial reward constants for:
  - terminal success reward;
  - elapsed-time coefficient;
  - per-correct-box reward;
  - per-correct-robot reward;
  - optional invalid-action penalty.

Consultant default proposal, if PO permits workplan defaults:

```text
terminal_success_reward: 1000.0
elapsed_time_penalty_per_second: -1.0
correct_box_reward: 1.0
correct_robot_reward: 1.0
invalid_action_penalty: 0.0
```

Rationale:

- time already penalizes invalid attempts if invalid attempts consume one
  second;
- per-correct-entity rewards create visible progress without dominating final
  success;
- constants are simple and easy to read in artifacts.

Deliverables:

- reward-policy manifest draft.

Verification:

- constants are explicit and traceable.

Stop if:

- reward constants are disputed and no default is approved.

##### Phase 0.Stage 3.Action 4: Decide column manifest workflow

Action:

- decide whether column-covered nodes/edges will be manually specified from the
  drawing or generated by a helper and then manually reviewed.

Consultant default:

```text
manual manifest authority with optional helper inspection
```

Deliverables:

- implementation log entry naming the column extraction approach.

Verification:

- the approach can produce explicit `blocked_nodes` and `blocked_edges`.

Stop if:

- the engineer cannot identify blocked nodes/edges without guessing.

### Phase 1: Stable Identity, Package Skeleton, And Documentation Shell

#### Phase 1.Stage 1: Create Source And Test Skeleton

##### Phase 1.Stage 1.Action 1: Create package and test directories

Action:

- create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/
tests/environments/warehouse_gridlock/
```

Deliverables:

- package and test directories exist.

Verification:

- no official tiny/calibration instance directory is created.

Stop if:

- `warehouse_gridlock` already exists with unrelated content.

##### Phase 1.Stage 1.Action 2: Add package initialization

Action:

- create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/__init__.py
```

Contents:

- export stable ids;
- export public state/action/instance constructors only after those modules
  exist;
- keep import side effects minimal.

Deliverables:

- package imports without side effects.

Verification:

- `uv run python -c "import big_boy_benchmarking.environments.warehouse_gridlock"`
  succeeds after package modules are available.

Stop if:

- package import conflicts with existing environment namespace conventions.

##### Phase 1.Stage 1.Action 3: Add stable ids

Action:

- create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/ids.py
```

Required ids:

```text
WAREHOUSE_GRIDLOCK_ENVIRONMENT_FAMILY_ID = "warehouse_gridlock_001"
WAREHOUSE_GRIDLOCK_IMPLEMENTATION_FAMILY_ID = "warehouse_gridlock_v001"
WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID = "warehouse_gridlock_16x16_v001"
WAREHOUSE_GRIDLOCK_READINESS_EVALUATION_ID = "warehouse_gridlock_environment_readiness_v001"
WAREHOUSE_GRIDLOCK_COLLISION_POLICY_ID = "warehouse_gridlock_collision_node_and_head_on_v001"
WAREHOUSE_GRIDLOCK_TRANSITION_POLICY_ID = "warehouse_gridlock_synchronous_push_v001"
WAREHOUSE_GRIDLOCK_REWARD_POLICY_ID = "warehouse_gridlock_elapsed_success_progress_v001"
WAREHOUSE_GRIDLOCK_DISCOVERY_POLICY_ID = "warehouse_gridlock_discovery_per_run_per_arm_v001"
```

Deliverables:

- ids module.

Verification:

- ids are importable and stable strings.

Stop if:

- ids conflict with existing environment or evaluation ids.

#### Phase 1.Stage 2: Create Documentation Shell

##### Phase 1.Stage 2.Action 1: Create environment docs directory

Action:

- create:

```text
docs/environments/warehouse_gridlock_001/
docs/environments/warehouse_gridlock_001/manifests/
```

Deliverables:

- environment docs directory exists.

Verification:

- no `docs/evaluations/warehouse_gridlock_001` readout is generated yet.

Stop if:

- docs path conflicts with existing unrelated docs.

##### Phase 1.Stage 2.Action 2: Create environment README seed

Action:

- create:

```text
docs/environments/warehouse_gridlock_001/README.md
```

Minimum content:

- source authority and PO-authored drawings;
- environment identity;
- one-second synchronous ensemble control;
- 32 robots and 32 boxes;
- exact robot and box target success;
- concrete columns as blocked regions;
- hidden-admissibility/discovery framing;
- no official tiny calibration instance;
- non-claims and readiness status.

Deliverables:

- checked-in human environment doc.

Verification:

- document does not claim benchmark/evaluation success.

Stop if:

- README would need to invent unresolved mechanics.

##### Phase 1.Stage 2.Action 3: Create design-to-environment trace note

Action:

- create or include in README a trace table mapping:
  - PO drawing source;
  - PO clarification;
  - environment manifest field;
  - implementation module;
  - artifact/readout surface.

Deliverables:

- source-to-contract traceability exists.

Verification:

- later engineers can see why each contract exists.

Stop if:

- attribution cannot be preserved clearly.

### Phase 2: Full PO Drawing Manifest

#### Phase 2.Stage 1: Define Manifest Schema

##### Phase 2.Stage 1.Action 1: Create manifest dataclasses or schema loader

Action:

- create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/manifests.py
```

Required structures:

```text
WarehouseGridlockInstanceManifest
GridSpec
SourceDesignReference
RobotSpec
BoxSpec
TargetSpec
ColumnObstacleSpec
CollisionPolicySpec
TransitionPolicySpec
RewardPolicySpec
DiscoveryPolicySpec
```

Deliverables:

- typed manifest loader and validator.

Verification:

- loader rejects missing required fields.

Stop if:

- existing repo conventions require a different schema pattern.

##### Phase 2.Stage 1.Action 2: Define manifest JSON schema fields

Action:

- support manifest fields:

```text
environment_family_id
implementation_family_id
instance_id
source_design_note
source_images
grid.rows
grid.cols
coordinate_convention
nodes
edges
blocked_nodes
blocked_edges
columns
robots
boxes
box_targets
robot_targets
goal_policy
collision_policy
transition_policy
reward_policy
discovery_policy
claim_boundary
```

Deliverables:

- loader can parse all required fields.

Verification:

- manifest validation error messages identify missing/invalid fields.

Stop if:

- graph/state/action modules require fields not planned here.

#### Phase 2.Stage 2: Extract Full Instance Manifest

##### Phase 2.Stage 2.Action 1: Create full instance manifest draft

Action:

- create:

```text
docs/environments/warehouse_gridlock_001/manifests/warehouse_gridlock_16x16_v001.json
```

Required content:

- source references to all PO SVGs;
- `source_design_note` set to
  `docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md`;
- grid size `16 x 16`;
- bidirectional graph edges;
- robot start positions for `R01` through `R32`;
- box start positions for `B01` through `B32`;
- exact robot target positions;
- exact box target positions;
- column blocked nodes/edges;
- collision policy with shared-node and head-on swap rejection;
- transition policy with synchronous control;
- reward policy with explicit constants;
- discovery policy with per-run/per-arm cache.

Deliverables:

- full-instance manifest draft.

Verification:

- manifest has 32 robots and 32 boxes;
- no official tiny instance manifest is created.

Stop if:

- positions cannot be extracted from the SVG without guessing.

##### Phase 2.Stage 2.Action 2: Encode graph nodes and bidirectional edges

Action:

- list all physically admissible grid nodes or list all visual nodes with
  explicit blocked nodes;
- list bidirectional edges as directed pairs or generate directed pairs from
  undirected edge declarations.

Deliverables:

- graph section in manifest.

Verification:

- every edge endpoint references an existing node;
- for every traversable undirected edge, both directed pairs exist or are
  generated deterministically.

Stop if:

- column regions make edge validity ambiguous.

##### Phase 2.Stage 2.Action 3: Encode concrete columns

Action:

- mark column-covered nodes as blocked;
- mark blocked edges through/into columns according to chosen manifest rule;
- include source drawing reference and human-readable notes.

Deliverables:

- `columns`, `blocked_nodes`, and `blocked_edges` manifest sections.

Verification:

- no start or target entity occupies a blocked node;
- no traversable edge permits movement through a concrete column.

Stop if:

- any robot/box start or target appears inside a blocked column region.

##### Phase 2.Stage 2.Action 4: Encode start and target entities

Action:

- encode:
  - `robots.R01` through `robots.R32`;
  - `boxes.B01` through `boxes.B32`;
  - `robot_targets.R01` through `robot_targets.R32`;
  - `box_targets.B01` through `box_targets.B32`.

Deliverables:

- complete start/goal entity sections.

Verification:

- all ids are present exactly once;
- start positions are unique;
- target positions are unique within robot/box groups and no forbidden overlap
  exists under the goal policy;
- all positions are traversable nodes.

Stop if:

- label mapping from SVG to coordinate cannot be determined confidently.

#### Phase 2.Stage 3: Validate Manifest

##### Phase 2.Stage 3.Action 1: Add manifest validation tests

Action:

- create tests that load the full manifest and validate:
  - required ids;
  - source references exist;
  - graph endpoints;
  - blocked-node consistency;
  - start occupancy;
  - target occupancy;
  - policy fields.

Deliverables:

- manifest validation tests.

Verification:

- tests fail on missing robot/box/target ids.

Stop if:

- manifest schema cannot distinguish visual nodes from blocked nodes.

##### Phase 2.Stage 3.Action 2: Add manifest summary function

Action:

- implement a function that produces:

```text
node_count
edge_count
blocked_node_count
blocked_edge_count
robot_count
box_count
robot_target_count
box_target_count
column_count
```

Deliverables:

- summary data structure and serializer.

Verification:

- summary can be written as JSON and CSV row.

Stop if:

- summary omits a claim-critical count.

### Phase 3: Core Types And Validation

#### Phase 3.Stage 1: Graph Model

##### Phase 3.Stage 1.Action 1: Implement graph primitives

Action:

- create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/graph.py
```

Required types/functions:

```text
GridNode
Direction
WarehouseGraph
neighbor(node, direction)
has_edge(source, target)
is_traversable_node(node)
iter_neighbors(node)
validate_graph(graph)
```

Deliverables:

- graph module.

Verification:

- unit tests cover neighbor lookup and bidirectional edge handling.

Stop if:

- existing repo graph utility should be reused instead.

##### Phase 3.Stage 1.Action 2: Implement graph validation

Action:

- validate:
  - no duplicate nodes;
  - all edge endpoints exist;
  - blocked nodes exist in the graph;
  - blocked edges reference known nodes;
  - no traversable edge points into a blocked node unless explicitly marked
    invalid.

Deliverables:

- graph validation report.

Verification:

- invalid graph fixtures fail with clear messages.

Stop if:

- column-blocked nodes require a special visual-vs-physical graph distinction
  not captured in the manifest.

#### Phase 3.Stage 2: State Model

##### Phase 3.Stage 2.Action 1: Implement state type

Action:

- create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/state.py
```

Required type:

```text
WarehouseGridlockState:
  robot_positions
  box_positions
  time_step
```

Deliverables:

- immutable or stable state representation;
- JSON serialization helpers.

Verification:

- state round-trips through JSON.

Stop if:

- state representation cannot be hashed for discovery summaries.

##### Phase 3.Stage 2.Action 2: Implement state validation

Action:

- validate:
  - all required robot ids exist;
  - all required box ids exist;
  - no unknown ids exist;
  - all positions exist in graph;
  - no blocked occupancy;
  - no duplicate robot positions;
  - no duplicate box positions;
  - no robot-box overlap;
  - time step is nonnegative.

Deliverables:

- `StateValidationReport`.

Verification:

- unit tests cover every invalid category.

Stop if:

- target positions conflict with legal occupancy rules.

#### Phase 3.Stage 3: Action Model

##### Phase 3.Stage 3.Action 1: Implement primitive commands and ensemble action

Action:

- create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/actions.py
```

Required types:

```text
DirectionOrStay
WarehouseGridlockAction
ActionValidationReport
```

Deliverables:

- structured ensemble action representation;
- JSON serialization helpers.

Verification:

- action with exactly 32 commands validates for full instance.

Stop if:

- action representation encourages full action-space enumeration.

##### Phase 3.Stage 3.Action 2: Add full-enumeration guard

Action:

- implement an explicit guard that prevents flat enumeration for the full
  32-robot instance.

Deliverables:

- helper function or exception path documenting why full enumeration is
  forbidden.

Verification:

- unit test asserts full enumeration raises a clear error.

Stop if:

- any package path requires a flat action count for full environment execution.

### Phase 4: Synchronous Transition Engine

#### Phase 4.Stage 1: Local Proposal Engine

##### Phase 4.Stage 1.Action 1: Implement local robot proposals

Action:

- create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/transition.py
```

- implement local proposal logic:
  - `stay`;
  - empty-node move;
  - push adjacent box into empty traversable node;
  - local invalid reasons.

Deliverables:

- local proposal function and event structures.

Verification:

- micro-fixture tests cover stay, move, push, off-grid, blocked, occupied, and
  invalid push destination.

Stop if:

- push semantics conflict with PO drawings.

##### Phase 4.Stage 1.Action 2: Represent proposed entity movements

Action:

- define event types:

```text
RobotMoveProposal
BoxMoveProposal
LocalInvalidReason
```

Deliverables:

- proposals can be inspected before global validation.

Verification:

- proposal serialization is stable for event rows.

Stop if:

- proposals cannot represent no-op/stay distinctly from invalid self-loop.

#### Phase 4.Stage 2: Global Ensemble Validation

##### Phase 4.Stage 2.Action 1: Implement shared-node collision checks

Action:

- reject ensembles where two final entities would occupy the same node.

Deliverables:

- collision validator.

Verification:

- tests cover robot-robot, robot-box, and box-box final destination conflicts.

Stop if:

- overlapping target positions in the manifest would make success impossible.

##### Phase 4.Stage 2.Action 2: Implement head-on edge swap checks

Action:

- reject robot/robot, robot/box, and box/box head-on swaps when two entities
  exchange positions across the same edge during one synchronous tick.

Deliverables:

- head-on swap validator in:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/collisions.py
```

Verification:

- tests cover adjacent robots swapping positions;
- tests cover robot and pushed box swap-like conflicts if representable;
- tests document any impossible cases.

Stop if:

- the implementation finds a head-on case not covered by the blueprint.

##### Phase 4.Stage 2.Action 3: Implement blocked-node and blocked-edge checks

Action:

- reject moves into blocked nodes;
- reject moves over blocked edges;
- reject box pushes into blocked nodes or over blocked edges.

Deliverables:

- blocked region validation.

Verification:

- concrete-column micro-fixture tests fail correctly.

Stop if:

- column blocked-edge policy is still ambiguous.

#### Phase 4.Stage 3: Step Result Semantics

##### Phase 4.Stage 3.Action 1: Implement valid ensemble transition

Action:

- when ensemble is valid:
  - move all proposed robots;
  - move all proposed boxes;
  - increment `time_step` by one;
  - compute reward;
  - emit events;
  - compute terminal/truncated flags.

Deliverables:

- valid transition path.

Verification:

- tests confirm simultaneous valid moves apply together.

Stop if:

- simultaneous push dependencies require ordering not specified in the
  blueprint.

##### Phase 4.Stage 3.Action 2: Implement invalid ensemble transition

Action:

- implement invalid self-loop according to Phase 0 gate resolution:
  - no robot moves;
  - no box moves;
  - time increments or does not increment according to chosen rule;
  - invalid event rows emitted;
  - discovery event emitted;
  - reward computed from chosen policy.

Deliverables:

- invalid transition path.

Verification:

- tests confirm invalid behavior exactly matches Phase 0 decision.

Stop if:

- Phase 0 gate was not resolved.

##### Phase 4.Stage 3.Action 3: Implement terminal condition

Action:

- terminal success requires:

```text
all boxes at exact box targets
all robots at exact robot targets
```

Deliverables:

- terminal checker.

Verification:

- tests cover:
  - all boxes correct but robots wrong -> not terminal;
  - all robots correct but boxes wrong -> not terminal;
  - all robots and boxes correct -> terminal.

Stop if:

- manifest target positions make terminal state illegal.

### Phase 5: Reward And Discovery Accounting

#### Phase 5.Stage 1: Reward Modes

##### Phase 5.Stage 1.Action 1: Implement reward policy module

Action:

- create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/rewards.py
```

Support:

```text
diagnostic_no_reward_v001
elapsed_success_progress_v001
```

The `elapsed_success_progress_v001` reward must include:

- terminal success reward;
- negative elapsed-time term;
- per-correct-box term;
- per-correct-robot term;
- optional invalid-action penalty if Phase 0 sets one.

Deliverables:

- reward module and reward manifest serializer.

Verification:

- reward tests cover before/after target changes and elapsed-time effect.

Stop if:

- reward constants are not resolved.

##### Phase 5.Stage 1.Action 2: Keep reward separate from physical dynamics

Action:

- ensure transition validity does not depend on reward mode.

Deliverables:

- physical transition functions can run with diagnostic reward mode.

Verification:

- tests run identical physical transition under multiple reward modes.

Stop if:

- reward code changes transition legality.

#### Phase 5.Stage 2: Discovery Accounting

##### Phase 5.Stage 2.Action 1: Implement discovery event structures

Action:

- create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/discovery.py
```

Event concepts:

```text
attempted_ensemble
valid_ensemble
invalid_ensemble
invalid_reason
discovered_state
discovered_transition
cache_hit
cache_miss
mask_or_query_call
```

Deliverables:

- discovery event structures and row serializers.

Verification:

- event rows are deterministic and include state/action identifiers.

Stop if:

- state/action identifiers cannot be serialized stably.

##### Phase 5.Stage 2.Action 2: Implement per-run/per-arm cache policy metadata

Action:

- implement manifest support for:

```text
cache_scope: per_run_per_arm
mask_policy: none_by_default
query_policy: explicit_only
invalid_attempts_are_discovery_events: true
```

Deliverables:

- `admissibility_cache_policy_manifest.json`;
- `action_mask_policy_manifest.json`.

Verification:

- readiness artifacts state whether masks/queries were used.

Stop if:

- a runner uses hidden masks without writing a manifest.

### Phase 6: Instance Loading And Readiness Validation

#### Phase 6.Stage 1: Instance Loader

##### Phase 6.Stage 1.Action 1: Implement instance loader

Action:

- create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/instances.py
```

Responsibilities:

- load the full manifest;
- construct graph;
- construct start state;
- construct target maps;
- construct policy specs;
- expose stable environment instance object.

Deliverables:

- instance loader.

Verification:

- tests load `warehouse_gridlock_16x16_v001`.

Stop if:

- manifest has unresolved placeholders.

##### Phase 6.Stage 1.Action 2: Add readiness validation module

Action:

- create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/validation.py
```

Readiness checks:

- manifest schema;
- graph connectivity summary;
- blocked-node consistency;
- start-state validity;
- target-state validity;
- terminal-state validity;
- action-surface validity;
- collision policy presence;
- reward policy presence;
- discovery policy presence.

Deliverables:

- readiness validation reports.

Verification:

- tests exercise success and failure reports.

Stop if:

- target state is not physically valid.

#### Phase 6.Stage 2: Readiness Summary Tables

##### Phase 6.Stage 2.Action 1: Implement readiness summary generation

Action:

- generate row dictionaries for:

```text
readiness_summary.csv
graph_summary.csv
state_validation_summary.csv
target_validation_summary.csv
```

Deliverables:

- table-generation functions.

Verification:

- rows include environment id, instance id, source design note, status, and
  claim boundary.

Stop if:

- readiness summary would imply benchmark success.

##### Phase 6.Stage 2.Action 2: Implement transition smoke summaries

Action:

- generate row dictionaries for:

```text
transition_smoke_summary.csv
invalid_action_summary.csv
discovered_state_summary.csv
discovered_transition_summary.csv
discovery_coverage_summary.csv
admissibility_budget_summary.csv
```

Deliverables:

- transition/discovery summary table functions.

Verification:

- smoke summary distinguishes valid moves, invalid moves, pushes, stays,
  shared-node conflicts, head-on swaps, blocked-node attempts, and blocked-edge
  attempts.

Stop if:

- invalid categories are not distinguishable.

### Phase 7: Artifact Writers And Human Readiness Docs

#### Phase 7.Stage 1: Artifact Writer

##### Phase 7.Stage 1.Action 1: Implement artifact paths

Action:

- create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/docs_writer.py
```

- define paths under:

```text
docs/evaluations/warehouse_gridlock_001/environment_readiness/
```

Deliverables:

- deterministic artifact path helpers.

Verification:

- raw artifacts land under `artifacts/<run_label>/`;
- human readout source lands at the repo-side readiness folder.

Stop if:

- path helper would write artifacts outside repo-controlled readiness area.

##### Phase 7.Stage 1.Action 2: Write required manifests and tables

Action:

- write:

```text
environment_instance_manifest.json
graph_manifest.json
start_state.json
goal_state.json
target_manifest.json
action_space_manifest.json
transition_rule_manifest.json
collision_policy_manifest.json
reward_mode_manifest.json
action_mask_policy_manifest.json
admissibility_cache_policy_manifest.json
readiness_summary.csv
graph_summary.csv
state_validation_summary.csv
target_validation_summary.csv
transition_smoke_summary.csv
invalid_action_summary.csv
discovered_state_summary.csv
discovered_transition_summary.csv
discovery_coverage_summary.csv
admissibility_budget_summary.csv
```

Deliverables:

- readiness artifact tree for a run label.

Verification:

- files are present and parseable;
- no optional cross-tier discovery-pressure artifacts are required.

Stop if:

- any required artifact cannot be generated from real environment state.

#### Phase 7.Stage 2: Readout Source And Docs

##### Phase 7.Stage 2.Action 1: Write readout source

Action:

- write:

```text
docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json
```

The readout source must point to artifact tables and manifests generated by the
readiness run.

Deliverables:

- repo-side readout source.

Verification:

- paths are repo-relative or protocol-compatible;
- the artifact-table readout protocol can be pointed at this file.

Stop if:

- readout source would point to `/private/tmp` or another machine-local output
  as the canonical result.

##### Phase 7.Stage 2.Action 2: Write initial human docs

Action:

- write or generate:

```text
docs/evaluations/warehouse_gridlock_001/environment_readiness/README.md
docs/evaluations/warehouse_gridlock_001/environment_readiness/artifact_index.md
docs/evaluations/warehouse_gridlock_001/environment_readiness/method.md
docs/evaluations/warehouse_gridlock_001/environment_readiness/runbook.md
docs/evaluations/warehouse_gridlock_001/environment_readiness/glossary.md
docs/evaluations/warehouse_gridlock_001/environment_readiness/results/summary.md
```

Deliverables:

- human-readable readiness docs.

Verification:

- docs state readiness claim boundary;
- docs state no tower/comparison/gauntlet claims;
- docs identify PO-authored source drawings.

Stop if:

- docs imply learning or tower performance.

### Phase 8: CLI Integration

#### Phase 8.Stage 1: CLI Commands

##### Phase 8.Stage 1.Action 1: Register `warehouse-gridlock` command group

Action:

- update the CLI entrypoint following existing environment command patterns.

Deliverables:

- command group:

```text
warehouse-gridlock
```

Verification:

- `uv run python -m big_boy_benchmarking.cli --help` lists the group.

Stop if:

- CLI structure has changed and requires a different integration pattern.

##### Phase 8.Stage 1.Action 2: Add graph diagnostics command

Action:

- implement:

```text
warehouse-gridlock graph-diagnostics
```

Inputs:

- `--artifact-root`;
- `--instance-id warehouse_gridlock_16x16_v001`;
- `--run-label`;
- optional `--repo-root`.

Deliverables:

- command writes graph/readiness summary artifacts.

Verification:

- command returns JSON status with graph counts.

Stop if:

- graph manifest does not validate.

##### Phase 8.Stage 1.Action 3: Add state diagnostics command

Action:

- implement:

```text
warehouse-gridlock state-diagnostics
```

Deliverables:

- command validates start and target states.

Verification:

- command returns JSON status with robot/box target counts.

Stop if:

- start or target state is invalid.

##### Phase 8.Stage 1.Action 4: Add transition smoke command

Action:

- implement:

```text
warehouse-gridlock transition-smoke
```

Smoke cases:

- all robots stay;
- one valid robot move if available;
- one valid push if available;
- shared-node conflict;
- head-on swap conflict;
- blocked-column attempt;
- invalid push destination.

Deliverables:

- command writes transition smoke artifacts and discovery summaries.

Verification:

- command returns JSON status and invalid category counts.

Stop if:

- no valid push or valid move can be identified from the full manifest.

##### Phase 8.Stage 1.Action 5: Add readiness docs command

Action:

- implement:

```text
warehouse-gridlock readiness-docs
```

Deliverables:

- command writes `readout_source.json` and human docs for the latest readiness
  artifact root or specified artifact root.

Verification:

- command returns JSON paths for docs.

Stop if:

- docs would be generated without source artifacts.

##### Phase 8.Stage 1.Action 6: Add random rollout command

Action:

- implement:

```text
warehouse-gridlock random-rollout
```

Scope:

- non-claim readiness/reconnaissance only;
- structured ensemble random proposals;
- configurable seconds;
- artifacted invalid/valid/discovery counts.

Deliverables:

- random rollout artifacts.

Verification:

- run completes without full action enumeration.

Stop if:

- random rollout accidentally uses an action mask without manifesting it.

### Phase 9: Tests

#### Phase 9.Stage 1: Unit Tests

##### Phase 9.Stage 1.Action 1: Add graph tests

Action:

- create tests for:
  - duplicate nodes;
  - unknown edge endpoints;
  - bidirectional edge loading;
  - blocked nodes;
  - blocked edges;
  - neighbor lookup.

Deliverables:

- graph test file.

Verification:

- `uv run pytest tests/environments/warehouse_gridlock/test_graph.py` passes.

Stop if:

- graph semantics diverge from manifest.

##### Phase 9.Stage 1.Action 2: Add state/action tests

Action:

- create tests for:
  - overlapping robots;
  - overlapping boxes;
  - robot-box overlap;
  - blocked-node occupancy;
  - missing robot command;
  - unknown robot id;
  - `stay` command;
  - full action enumeration guard.

Deliverables:

- state/action test files.

Verification:

- targeted tests pass.

Stop if:

- full instance cannot validate a structured ensemble action.

##### Phase 9.Stage 1.Action 3: Add transition tests

Action:

- create micro-fixture tests for:
  - valid move;
  - valid push;
  - invalid off-grid move;
  - invalid blocked-column move;
  - invalid shared-node conflict;
  - invalid head-on edge swap;
  - invalid push into occupied node;
  - terminal condition with boxes-only correct but robots wrong;
  - terminal condition with robots-only correct but boxes wrong;
  - terminal condition with all exact targets correct.

Deliverables:

- transition test file.

Verification:

- targeted tests pass.

Stop if:

- Q6/Q7 semantics remain unresolved.

#### Phase 9.Stage 2: Integration And Artifact Tests

##### Phase 9.Stage 2.Action 1: Add manifest integration tests

Action:

- test loading:

```text
warehouse_gridlock_16x16_v001.json
```

Deliverables:

- manifest integration test.

Verification:

- manifest reports 32 robots and 32 boxes.

Stop if:

- full manifest cannot validate.

##### Phase 9.Stage 2.Action 2: Add CLI smoke tests

Action:

- test CLI commands with a temporary artifact root:
  - graph diagnostics;
  - state diagnostics;
  - transition smoke;
  - readiness docs.

Deliverables:

- CLI smoke tests.

Verification:

- required artifact files exist after command execution.

Stop if:

- CLI writes canonical docs to temp paths instead of repo readout path.

##### Phase 9.Stage 2.Action 3: Add readout-source tests

Action:

- validate `readout_source.json` generated by readiness docs.

Deliverables:

- readout-source test.

Verification:

- readout source references required tables and manifests.

Stop if:

- readout-source schema differs from existing protocol expectations.

### Phase 10: Verification Commands

#### Phase 10.Stage 1: Static And Unit Verification

##### Phase 10.Stage 1.Action 1: Run targeted warehouse tests

Action:

- run:

```text
uv run pytest tests/environments/warehouse_gridlock
```

Deliverables:

- test output recorded in implementation log.

Verification:

- tests pass.

Stop if:

- any test fails unexpectedly.

##### Phase 10.Stage 1.Action 2: Run broader relevant tests

Action:

- run relevant existing environment/CLI tests:

```text
uv run pytest tests/environments tests/test_cli*.py
```

or the closest repo-appropriate subset after inspecting current test layout.

Deliverables:

- test output recorded in implementation log.

Verification:

- no existing environment tests regress.

Stop if:

- failures appear outside known unrelated dirty work.

#### Phase 10.Stage 2: Manual CLI Verification

##### Phase 10.Stage 2.Action 1: Run graph diagnostics

Action:

- run:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock graph-diagnostics \
  --artifact-root docs/evaluations/warehouse_gridlock_001/environment_readiness/artifacts/smoke_001 \
  --instance-id warehouse_gridlock_16x16_v001 \
  --run-label smoke_001
```

Deliverables:

- graph diagnostics artifacts.

Verification:

- JSON status is `ok` or `complete`;
- graph counts are nonzero and plausible.

Stop if:

- graph diagnostics cannot validate the full manifest.

##### Phase 10.Stage 2.Action 2: Run state diagnostics

Action:

- run:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock state-diagnostics \
  --artifact-root docs/evaluations/warehouse_gridlock_001/environment_readiness/artifacts/smoke_001 \
  --instance-id warehouse_gridlock_16x16_v001 \
  --run-label smoke_001
```

Deliverables:

- state diagnostics artifacts.

Verification:

- start and target states validate.

Stop if:

- any entity starts or targets a blocked/overlapping node.

##### Phase 10.Stage 2.Action 3: Run transition smoke

Action:

- run:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock transition-smoke \
  --artifact-root docs/evaluations/warehouse_gridlock_001/environment_readiness/artifacts/smoke_001 \
  --instance-id warehouse_gridlock_16x16_v001 \
  --run-label smoke_001
```

Deliverables:

- transition smoke artifacts.

Verification:

- valid and invalid examples are both present;
- head-on swap invalidity is recorded;
- blocked-column invalidity is recorded.

Stop if:

- transition smoke cannot find representative examples.

##### Phase 10.Stage 2.Action 4: Generate readiness docs

Action:

- run:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock readiness-docs \
  --artifact-root docs/evaluations/warehouse_gridlock_001/environment_readiness/artifacts/smoke_001 \
  --instance-id warehouse_gridlock_16x16_v001 \
  --run-label smoke_001
```

Deliverables:

- repo-side readiness docs and `readout_source.json`.

Verification:

- docs exist;
- docs state environment readiness only;
- docs do not claim benchmark performance.

Stop if:

- generated docs drift from the human-readability protocol.

### Phase 11: Final Documentation And Cleanup

#### Phase 11.Stage 1: Root/Index Documentation

##### Phase 11.Stage 1.Action 1: Update environment index

Action:

- update any existing environment index under:

```text
docs/environments/
```

or create one if the repo pattern requires it.

Deliverables:

- Warehouse Gridlock appears as a candidate/readiness environment, not as an
  evaluated benchmark.

Verification:

- index links to `docs/environments/warehouse_gridlock_001/README.md`.

Stop if:

- no environment index pattern exists and adding one would be broader than this
  workplan.

##### Phase 11.Stage 1.Action 2: Update design folder README if needed

Action:

- update:

```text
docs/design/svg_physical_system_designs/README.md
```

only if needed to point to the new blueprint/workplan pattern.

Deliverables:

- SVG workflow docs reflect the Warehouse Gridlock blueprint/workplan.

Verification:

- update does not claim implementation is complete before execution completes.

Stop if:

- this would broaden the workflow beyond the user request.

#### Phase 11.Stage 2: Git Hygiene And Final Log

##### Phase 11.Stage 2.Action 1: Inspect changed files

Action:

- run:

```text
git status --short
```

Deliverables:

- implementation log records changed files.

Verification:

- no generated raw artifact tree is accidentally staged;
- no `.bkp` or editor backup files are accidentally staged.

Stop if:

- unrelated user changes are mixed into paths this work touched.

##### Phase 11.Stage 2.Action 2: Record final implementation summary

Action:

- update implementation log with:
  - completed phases;
  - files changed;
  - tests run;
  - commands run;
  - artifacts generated;
  - remaining limitations;
  - exact next step.

Deliverables:

- final implementation log summary.

Verification:

- summary distinguishes environment readiness from evaluation readiness.

Stop if:

- any failed test or unresolved stop condition is omitted.

##### Phase 11.Stage 2.Action 3: Run final workplan compliance audit

Action:

- audit the completed implementation against every `Phase.Stage.Action` item in
  this workplan;
- mark each item in the implementation log as one of:
  - completed exactly as specified;
  - blocked with Project Owner guidance needed;
  - explicitly deferred by Project Owner instruction;
- verify no item is silently satisfied by a lighter stand-in;
- verify no unresolved Phase 0 gate was encoded as a source-code default
  without Project Owner confirmation;
- verify the implementation did not reintroduce official tiny/small instances;
- verify the implementation did not implement tower comparison, standard
  gauntlet, learned policy training, or cross-tier discovery pressure.

Deliverables:

- final compliance-audit section in the implementation log.

Verification:

- every action has an explicit status;
- unresolved gates remain visible rather than hidden in code;
- the final report can cite the exact completed or blocked status for this
  workplan.

Stop if:

- any action is only partially implemented without approval;
- any unresolved design gate was converted into implementation behavior without
  approval;
- any generated docs or final summary overclaim beyond environment readiness.

## Required Stop Conditions During Execution

Stop execution if:

- Phase 0 gates are unresolved;
- exact column blocked nodes/edges cannot be determined from the drawings;
- full start state cannot validate;
- full target state cannot validate;
- terminal state is physically impossible under collision/column rules;
- code attempts to flat-enumerate `5^32` actions;
- invalid ensemble semantics differ from the Phase 0 decision;
- an artifact writer emits canonical outputs outside the repo-side readiness
  tree;
- any readout claims learning, tower performance, or benchmark superiority;
- implementation would require edits to `state_collapser`;
- a hidden action mask is introduced without a manifest;
- micro-fixtures start being treated as benchmark instances;
- cross-tier discovery pressure starts becoming implementation scope.

## Completion Criteria

This workplan is complete when:

- Phase 0 gates have been resolved, logged, and reflected in manifests before
  source implementation proceeds;
- the Warehouse Gridlock package exists;
- the full PO drawing instance manifest exists and validates;
- synchronous ensemble transitions work;
- shared-node and head-on collision invalidity are tested;
- exact robot and box targets are enforced;
- concrete columns block occupancy/traversal;
- structured ensemble actions are used for the full instance;
- full action enumeration is guarded against;
- discovery/admissibility artifacts are emitted;
- readiness docs and `readout_source.json` exist;
- targeted tests pass;
- CLI smoke commands run;
- final workplan compliance audit is recorded;
- the implementation log records all work;
- no official tiny calibration instance was created;
- no tower/evaluation/gauntlet claims were made.

## Post-Completion Boundary

After this workplan, the repo may be ready to design a Warehouse Gridlock
environment-readiness readout conversation or a later evaluation design.

It is not automatically ready for:

- tower comparison;
- standard gauntlet;
- serious learning claims;
- public benchmark claims.
