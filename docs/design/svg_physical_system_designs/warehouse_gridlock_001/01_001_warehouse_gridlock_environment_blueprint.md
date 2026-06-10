# Warehouse Gridlock 001 Environment Blueprint

## Status

Initial full environment blueprint.

This is a design blueprint, not an implementation workplan. It must not be
executed directly. A Phase.Stage.Action implementation workplan should be
created only after the Project Owner confirms or corrects the open mechanics
questions at the end of this document.

## Source Authority

### Project Owner Design Inputs

The primary design source is the Project Owner-authored SVG drawing set
documented in:

```text
docs/design/svg_physical_system_designs/warehouse_001.md
```

PO-authored image artifacts:

```text
assets/environment_designs/gridlock_001_start.svg
assets/environment_designs/gridlock_001_end.svg
assets/environment_designs/gridlock_001_moves_001.svg
assets/environment_designs/gridlock_001_moves_002.svg
```

The Project Owner also clarified the following mechanics and benchmark intent:

- one environment timestep represents one second;
- every robot receives a command at every timestep;
- every robot may move one graph step or stay in place;
- all robot commands form a synchronous ensemble move;
- an ensemble move is invalid if any two entities, robot or box, would occupy
  the same node;
- the serious MDP should be treated as hidden or effectively hidden because the
  admissible-state graph is not realistically computable in advance;
- discovery of admissible states/actions is required for all arms;
- comparisons must track how admissibility information is exposed, discovered,
  cached, masked, and charged to each arm;
- the target hypothesis is that tower structure may let policies discover
  reusable large-scale speed-ups that direct arms do not find under the same
  discovery burden;
- cross-tier discovery pressure is a hypothesis to retain for evaluation
  interpretation, not a required current-arm feature.

### Codex Role

Codex-authored content in this blueprint is interpretation, specification
translation, and engineering recommendation. Codex did not author the physical
environment drawing or the PO mechanics above.

This blueprint avoids turn-by-turn dialogue and does not invent Project Owner
turns. All unresolved items are labeled as open questions or assumptions
pending PO confirmation.

## Blueprint Claim Boundary

This blueprint supports the following design claim only:

```text
Warehouse Gridlock 001 is a PO-designed candidate discrete robotics benchmark
environment whose initial implementation should expose deterministic
synchronous warehouse dynamics, hidden-admissibility discovery surfaces, and
artifact-first readiness diagnostics.
```

It does not claim:

- that the full 16 x 16 task is solvable under the proposed horizon;
- that any tower improves performance;
- that the environment is benchmark-ready;
- that a full evaluation gauntlet has been designed;
- that cross-tier discovery pressure should be implemented now.

## Environment Identity

Recommended names:

```text
human_name: Warehouse Gridlock 001
environment_family_id: warehouse_gridlock_001
implementation_family_id: warehouse_gridlock_v001
full_instance_id: warehouse_gridlock_16x16_v001
```

Recommended source package location:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/
```

Recommended docs location:

```text
docs/environments/warehouse_gridlock_001/
```

Recommended evaluation/readout location for environment readiness:

```text
docs/evaluations/warehouse_gridlock_001/environment_readiness/
```

## Design Purpose

Warehouse Gridlock 001 should become a discrete robotics benchmark environment
for large-scale multi-robot, movable-object coordination under hidden
admissibility.

The core benchmark pressure is not simply "find a shortest path." The intended
pressure is:

- many robots move at the same time;
- robots can push movable boxes;
- all moves must satisfy collision and occupancy constraints;
- local choices can create congestion, deadlock, or cul-de-sac behavior;
- the admissible state/action structure is too large to precompute at serious
  scale;
- every evaluation arm must discover useful admissible structure;
- tower structure may make discovery more productive by revealing reusable
  abstract structure that direct exploration does not find within the same
  discovery budget.

## Core Design Locks

The following are locked by PO-authored drawings or PO clarifications unless
the PO later revises them.

### Lock 1: Discrete Graph Warehouse

The environment is a finite graph embedded in a grid-like warehouse drawing.
Grid nodes are potential locations for robots and boxes. Edges represent
possible one-step movement.

### Lock 2: Synchronous One-Second Timestep

Each environment step represents one second.

At every step, every robot chooses one primitive command.

### Lock 3: Per-Robot Command Set

Each robot command is one of:

```text
north
south
east
west
stay
```

### Lock 4: Ensemble Action

The action applied to the environment is the full collection of robot commands
for that timestep:

```text
EnsembleAction:
  robot_commands: dict[RobotId, DirectionOrStay]
```

### Lock 5: Shared-Node Occupancy Invalidates The Ensemble

If applying the ensemble transition would cause any two entities, robot or box,
to occupy the same node, the ensemble move is invalid.

### Lock 6: Hidden Or Effectively Hidden Serious MDP

For serious instances, the full admissible-state graph and full admissible
ensemble-action graph are not given to evaluation arms and are not expected to
be computable in advance.

### Lock 7: Discovery Is Part Of Every Arm

Every evaluation arm must discover admissible states/actions or useful
reachable structure under an explicit contract. A tower arm must not receive
uncharged admissibility information that a direct arm lacks unless the readout
states that the result is measuring admissibility-information advantage.

### Lock 8: Cross-Tier Discovery Pressure Is Not Current Scope

Cross-tier discovery pressure remains a hypothesis for interpreting later
evaluations. It is not a required mechanism for the initial environment arms.

## Assumptions Pending PO Confirmation

These are Codex recommendations for turning the PO drawings into an initial
finite environment. They should be changed if the PO answers differently.

### Assumption A: Bidirectional Grid Edges

Treat visible red grid edges as bidirectional cardinal adjacency.

Reason: the SVG movement drawings show cardinal robot motion, and there is no
one-way aisle notation yet.

### Assumption B: Push-Only Box Interaction

Robots can push boxes one node in the same direction as robot motion. Robots
cannot pull, carry, lift, rotate, or jointly push boxes in v001.

Reason: the PO move drawing shows push motion and does not show other object
interaction modes.

### Assumption C: Exact Labeled Boxes For The Main Instance

Treat boxes as labeled objects, with exact label-specific target nodes.

Reason: boxes are visibly labeled `B01` through `B32` in the drawings. Exact
labels create a sharper rearrangement benchmark.

### Decision D: Box And Robot Placement Are Both Required For Success

Primary terminal success requires all boxes to occupy their exact target nodes
and all robots to occupy their exact target nodes.

This is locked by PO reply under Q1 and Q2.

Design consequence: readouts should still report box success and robot success
separately, but full success requires both.

### Decision E: Columns Block Occupancy And Traversal

Gray rounded regions represent concrete columns. Nothing can occupy those
regions. Nodes may be visually drawn inside the column regions, but those nodes
are not physically admissible locations.

Implementation consequence: the manifest must explicitly mark column-covered
nodes as blocked and must remove or disable traversal through blocked column
regions. The red grid drawing may still show nodes/edges under a column, but
the column geometry overrides graph traversability.

### Decision F: Shared-Node Collisions And Head-On Edge Swaps Are Invalid

The required collision rules now include:

- no two entities may occupy the same node after the ensemble transition;
- head-on swaps along an edge are invalid because they would require a head-on
  collision along that edge.

Remaining implementation question: whether there are any other edge-crossing
cases beyond head-on swaps in this cardinal grid model. Codex expects head-on
swaps to be the main edge-collision case, but the collision policy should keep
this explicit.

### Assumption G: Invalid Ensemble Attempts Are Self-Loops With Events

Invalid ensemble moves should produce self-loop transitions, penalties, and
explicit event rows.

Reason: this makes invalidity inspectable, supports hidden-admissibility
discovery accounting, and matches BBB's artifact-first style.

### Assumption H: Full Action Space Is Structured, Not Flat

The full 32-robot ensemble action space has size `5^32`, so it cannot be
treated as a flat enumerated action list. The environment should expose a
structured action interface.

Do not create official tiny calibration instances for this environment. The PO
has stated that calibration is over. Small hand-authored transition fixtures
may still be used inside unit tests, but they must not become official benchmark
instances or evaluation targets.

## World Model

### Grid Coordinates

Represent grid nodes as integer coordinates:

```text
GridNode:
  row: int
  col: int
```

Recommended coordinate convention:

```text
row = 1..16 from top to bottom
col = 1..16 from left to right
```

The SVG diagrams show row/column labels. A coordinate extraction step should
map all visible robot, box, obstacle, edge, start, and target positions into
this coordinate system.

### Graph

Recommended graph representation:

```text
WarehouseGraph:
  nodes: frozenset[GridNode]
  edges: frozenset[tuple[GridNode, GridNode]]
  blocked_nodes: frozenset[GridNode]
  blocked_edges: frozenset[tuple[GridNode, GridNode]]
  coordinate_bounds: GridBounds
```

`edges` should include directed pairs. For a bidirectional grid, both `(u, v)`
and `(v, u)` are present.

### Obstacles

Obstacle handling should be manifest-driven.

Recommended manifests:

```text
obstacle_manifest.json:
  obstacle_id
  source_svg_element_ids
  occupied_regions
  blocked_nodes
  blocked_edges
  extraction_rule
```

For v001, Codex recommends manually specifying blocked nodes/edges from the
drawings after PO review rather than relying fully on SVG geometry parsing. SVG
geometry extraction can be used as a helper, but the benchmark contract should
be an explicit manifest.

## Object Model

### Robots

```text
RobotId = R01 ... R32
```

Each robot:

- occupies exactly one node;
- receives one command per timestep;
- may move one edge or stay;
- may push a box if command direction points into a pushable box.

### Boxes

```text
BoxId = B01 ... B32
```

Each box:

- occupies exactly one node;
- moves only when pushed by a robot;
- cannot occupy a blocked node;
- cannot share a node with any robot or box;
- may have an exact target node.

### Entity Occupancy

At every valid state:

```text
all robot positions are unique
all box positions are unique
robot positions and box positions are disjoint
no entity occupies a blocked node
```

## State Contract

Recommended state type:

```text
WarehouseGridlockState:
  robot_positions: Mapping[RobotId, GridNode]
  box_positions: Mapping[BoxId, GridNode]
  time_step: int
```

`time_step` should be included because the PO explicitly framed steps as timed
seconds and because episode horizons are time budgets.

Recommended state validation:

```text
validate_state(state, instance) -> StateValidationReport
```

Validation should check:

- all required robot ids are present;
- all required box ids are present;
- all coordinates are in graph nodes;
- no blocked occupancy;
- no duplicate robot occupancy;
- no duplicate box occupancy;
- no robot-box overlap;
- time step is nonnegative;
- all target ids in manifests refer to existing objects.

## Action Contract

### Primitive Commands

```text
DirectionOrStay = NORTH | SOUTH | EAST | WEST | STAY
```

### Ensemble Action

```text
WarehouseGridlockAction:
  commands: Mapping[RobotId, DirectionOrStay]
```

Validation should check:

- exactly one command per robot;
- no unknown robot id;
- no missing robot id;
- commands are in the allowed command set.

### Structured Action Surface

The environment should support at least three action surfaces:

```text
structured_ensemble:
  Native full command map, required for full instances.

micro_fixture_enumerated:
  Optional flat enumeration only inside deliberately small unit-test fixtures.
  This is not an official benchmark instance or calibration target.

proposal_filtered:
  A policy proposes a structured ensemble, with optional guard/mask/query
  machinery recorded in manifests.
```

The implementation must not hide the action surface from artifact readouts.
Every run should state:

- how ensemble actions were produced;
- whether invalid proposals were allowed;
- whether masks or guards were used;
- whether admissibility queries were charged;
- how discoveries were cached.

## Transition Contract

### Transition Function

Recommended signature:

```text
step(
  state: WarehouseGridlockState,
  action: WarehouseGridlockAction,
  mode: TransitionMode,
) -> WarehouseGridlockStepResult
```

Recommended result:

```text
WarehouseGridlockStepResult:
  next_state: WarehouseGridlockState
  reward: float
  terminated: bool
  truncated: bool
  validity: EnsembleValidity
  moved_robots: list[RobotMoveEvent]
  moved_boxes: list[BoxMoveEvent]
  invalid_reasons: list[InvalidReason]
  discovery_events: list[DiscoveryEvent]
```

### Local Proposal Phase

For each robot command:

```text
if command == STAY:
  propose robot stays at current node

else:
  u = current robot node
  v = neighbor(u, command)

  if v is empty:
    propose robot u -> v

  if v contains one box:
    w = neighbor(v, command)
    propose robot u -> v and box v -> w, if w is traversable and empty

  otherwise:
    local invalid
```

The local proposal phase should be evaluated against the pre-transition state.

### Global Validation Phase

After local proposals are built, validate the ensemble:

- no local invalid commands;
- no destination node has two or more entities;
- no moved entity enters a blocked node;
- no box is pushed by two robots;
- no robot has more than one destination;
- no entity has incompatible destinations;
- no head-on edge swaps;
- any additional edge-crossing policy must be explicit.

### Invalid Ensemble Semantics

Recommended default:

```text
invalid ensemble -> self-loop
time_step increments or does not increment: PO confirmation needed
reward includes invalid penalty
invalid event rows are emitted
discovery event rows are emitted
```

Open question: if the ensemble is invalid, does one second still pass? Codex
recommends yes for robotics realism and discovery accounting, but this needs PO
confirmation.

### Partial Execution

Recommended v001 default:

```text
no partial execution
```

If any part of the ensemble is invalid, the whole ensemble self-loops.

Reason: this is simpler, deterministic, and easier to explain in artifact
readouts. Partial execution would require specifying which subset moves and may
hide unfair advantages in conflict resolution.

## Goal Contract

### Target Manifests

Every instance should provide:

```text
target_box_positions: Mapping[BoxId, GridNode]
target_robot_positions: Mapping[RobotId, GridNode]
goal_policy:
  box_goal_required: bool
  robot_goal_required: bool
```

### v001 Goal

Locked by PO replies:

```text
box_goal_required = true
robot_goal_required = true
```

Primary success:

```text
all boxes are on their label-specific targets
all robots are on their label-specific targets
```

Secondary metrics:

- box target fraction;
- robot target fraction;
- average box distance to target;
- average robot distance to target;
- number of misplaced boxes;
- number of misplaced robots;
- time to first full solution;
- time to first partial target threshold.

## Time And Horizon Contract

Each timestep is one second.

Each episode should define:

```text
max_seconds
max_steps = max_seconds
```

Recommended horizon derivation:

1. Compute lower-bound displacement summaries from the manifest.
2. Compute baseline random/manual rollout feasibility on the full intended
   environment or the first PO-approved non-calibration instance.
3. Set smoke horizons conservatively for mechanical validation without creating
   official tiny calibration instances.
4. Set serious horizons only after readiness diagnostics reveal scale.

Initial blueprint recommendation:

```text
full_16x16_readiness: horizon derived from lower-bound displacement and manual
  transition probes
full_16x16_learning: no serious learning horizon until readiness diagnostics
  exist
```

## Reward Contract

The environment should expose deterministic physical dynamics independent from
reward mode.

Recommended reward modes:

```text
sparse_v001:
  step_penalty
  invalid_penalty
  goal_reward

shaped_progress_v001:
  sparse terms
  box_distance_delta
  placed_box_delta
  optional congestion/deadlock warning terms

diagnostic_no_reward_v001:
  emits metrics only, for readiness and discovery diagnostics
```

Recommended first implementation default:

```text
diagnostic_no_reward_v001 for readiness
sparse_v001 for initial learning smokes
```

Shaping should be introduced as an explicit mode, not silently embedded into
the physical environment.

## Hidden-Admissibility And Discovery Contract

### Environment Oracle

The environment engine may compute exact validity for a proposed state/action
transition. That is an oracle-backed transition check.

Evaluation arms should not automatically receive:

- the full admissible-state graph;
- the full set of valid ensemble actions per state;
- the full reachable transition graph;
- a free global action mask;
- uncharged liftability/admissibility information.

### Discovery Surfaces

Every run should record:

```text
discovered_state_summary.csv
discovered_transition_summary.csv
invalid_action_summary.csv
discovery_coverage_summary.csv
admissibility_budget_summary.csv
action_mask_policy_manifest.json
admissibility_cache_policy_manifest.json
```

At minimum, summaries should include:

- attempted ensemble count;
- valid ensemble count;
- invalid ensemble count;
- invalid reason counts;
- unique states observed;
- unique valid transitions observed;
- unique invalid state/action pairs observed;
- cache hits and misses, if caching exists;
- mask/query calls, if query surfaces exist;
- whether discovery persists across episodes/seeds/replicates.

### Fairness Contract For Comparisons

No direct-vs-tower comparison should proceed without manifests answering:

- does each arm receive a precomputed action mask?
- can each arm query validity before acting?
- do failed validity probes consume time, reward, or budget?
- are discovered valid/invalid actions cached?
- does cache persist per episode, run, seed, arm, or global evaluation?
- does the tower receive liftability information unavailable to direct?
- does direct-star receive comparable one-step admissibility information?
- what exactly counts as a discovery event?

### Tower-Structured Discovery Target

The positive hypothesis is:

```text
Under comparable discovery burden, tower structure may cause useful large-scale
structure to become discoverable and reusable, while direct exploration remains
stuck discovering local admissibility facts.
```

This should be evaluated only after environment readiness exists. It is not a
claim made by the environment implementation.

## Instance Scope

The PO rejected creating more official tiny calibration instances. Calibration
is over. The first benchmark-facing environment target should therefore be the
serious Warehouse Gridlock drawing, not a tiny ladder.

Small hand-authored scenarios are still allowed as unit-test fixtures for
transition semantics. They are not benchmark instances, evaluation instances,
or calibration targets.

### Full PO Drawing Instance

Recommended purpose:

- represent the full PO drawing;
- support serious benchmark work;
- make hidden-admissibility discovery central from the beginning;
- prevent the environment build from drifting back into calibration-only scale.

```text
warehouse_gridlock_16x16_v001:
  grid: 16x16
  robots: 32
  boxes: 32
```

### Unit-Test Fixtures

Recommended purpose:

- validate synchronous transition semantics;
- validate push mechanics;
- validate collision invalidity;
- validate head-on swap rejection;
- validate invalid self-loop behavior;
- validate artifact row emission.

These fixtures should be named as tests or fixtures, not as environment
instances.

## Coordinate Extraction Blueprint

### Need

The SVG drawings are design artifacts, but the environment needs explicit
machine-readable manifests.

### Recommended Extraction Strategy

Use a two-layer approach:

1. Manual manifest creation from drawings for v001 authority.
2. Optional helper scripts to assist coordinate extraction.

Rationale: diagrams.net SVGs are noisy and can contain rendering artifacts.
Manual manifests are more reliable for initial benchmark authority, especially
where obstacles and labels need PO confirmation.

### Required Manifests

```text
docs/environments/warehouse_gridlock_001/manifests/
  warehouse_gridlock_16x16_v001.json
```

Each manifest should include:

```json
{
  "environment_family_id": "warehouse_gridlock_001",
  "instance_id": "warehouse_gridlock_16x16_v001",
  "source_design_note": "docs/design/svg_physical_system_designs/warehouse_001.md",
  "source_images": [],
  "grid": {},
  "nodes": [],
  "edges": [],
  "blocked_nodes": [],
  "blocked_edges": [],
  "robots": {},
  "boxes": {},
  "box_targets": {},
  "robot_targets": {},
  "goal_policy": {},
  "collision_policy": {},
  "transition_policy": {},
  "reward_modes": []
}
```

## Implementation Surface Blueprint

Recommended modules:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/
  __init__.py
  actions.py
  collisions.py
  discovery.py
  docs_writer.py
  graph.py
  ids.py
  instances.py
  manifests.py
  rewards.py
  state.py
  transition.py
  validation.py
```

### `ids.py`

Defines stable ids:

```text
WAREHOUSE_GRIDLOCK_FAMILY_ID
WAREHOUSE_GRIDLOCK_TINY_V001
WAREHOUSE_GRIDLOCK_SMALL_V001
WAREHOUSE_GRIDLOCK_16X16_V001
```

### `graph.py`

Defines grid nodes, directions, graph loading, neighbor lookups, and graph
validation.

### `state.py`

Defines immutable state objects and state serialization.

### `actions.py`

Defines primitive commands, ensemble actions, action validation, test-fixture
helpers, and structured action serialization.

### `transition.py`

Implements local proposals, global validation, invalid self-loop semantics, and
step results.

### `collisions.py`

Implements node collision checks and optional edge-swap/crossing policies.

### `discovery.py`

Implements event structures and summaries for hidden-admissibility discovery.
This does not mean all policies use the same discovery strategy. It means the
environment can emit comparable evidence about discovery.

### `rewards.py`

Defines reward modes separately from physical transitions.

### `instances.py`

Loads manifests and constructs environment instances.

### `validation.py`

Produces readiness reports for graph, state, targets, and transition policy.

### `docs_writer.py`

Writes environment readiness docs and readout sources consistent with BBB
artifact protocols.

## CLI Blueprint

Recommended CLI family:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock ...
```

Initial commands:

```text
warehouse-gridlock graph-diagnostics
warehouse-gridlock state-diagnostics
warehouse-gridlock transition-smoke
warehouse-gridlock random-rollout
warehouse-gridlock readiness-docs
```

Later commands:

```text
warehouse-gridlock discovery-diagnostics
warehouse-gridlock tower-smoke
warehouse-gridlock standard-gauntlet ...
```

The first implementation should stop at environment readiness plus transition
smokes. It should not attempt the full standard gauntlet yet.

## Artifact Contract

### Environment Readiness Root

Recommended initial artifact/readout root:

```text
docs/evaluations/warehouse_gridlock_001/environment_readiness/
```

Recommended artifact root for a first smoke:

```text
docs/evaluations/warehouse_gridlock_001/environment_readiness/artifacts/smoke_001/
```

### Required Readout Surface

```text
docs/evaluations/warehouse_gridlock_001/environment_readiness/
  README.md
  readout_source.json
  artifact_index.md
  method.md
  runbook.md
  glossary.md
  results/
```

### Raw Artifacts

Raw run artifacts should live under `artifacts/` and follow the repo rule that
raw generated artifact trees are ignored by git unless intentionally packaged
as release assets.

Required tables:

```text
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

Required manifests:

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
```

Optional future artifacts:

```text
cross_tier_discovery_pressure_events.csv
cross_tier_discovery_pressure_summary.csv
```

These optional artifacts should not be required in the initial implementation.

## Test Blueprint

### Unit Tests

Required tests:

- graph loading rejects duplicate nodes;
- graph loading rejects edges with unknown nodes;
- state validation rejects overlapping robots;
- state validation rejects overlapping robot/box;
- state validation rejects blocked-node occupancy;
- action validation rejects missing robot commands;
- action validation rejects unknown robot ids;
- `stay` is locally valid when state is valid;
- one-step robot move works into empty traversable node;
- one-step robot move is invalid into blocked node;
- one-step robot move is invalid off graph;
- push works when robot, box, and destination line up;
- push fails when box destination is occupied;
- push fails when box destination is blocked;
- ensemble fails when two robots propose same destination;
- ensemble fails when two boxes propose same destination;
- invalid ensemble emits self-loop and invalid event rows;
- valid ensemble increments time by one;
- full instance refuses flat action enumeration by default;
- unit-test fixtures may enumerate their deliberately small local action spaces
  only inside tests.

### Golden Scenario Tests

Use hand-authored micro-fixture scenarios:

```text
single_robot_empty_move
single_robot_push_box
two_robots_conflict_same_destination
robot_pushes_box_into_robot_conflict
robot_stay_conflict_with_pushed_box
invalid_off_grid
```

### Manifest Tests

Required tests:

- every instance manifest validates;
- start state validates;
- goal target map validates;
- graph connectedness summary is emitted;
- source image references exist;
- source design note reference exists.

### Artifact Tests

Required tests:

- transition smoke writes required manifests;
- transition smoke writes event rows;
- readiness docs write `readout_source.json`;
- readout source uses repo-relative paths where required;
- generated docs can be regenerated by the artifact-table readout protocol.

## Readiness Workflow Blueprint

Initial environment readiness should proceed in this order:

1. Create manifest for the full PO drawing instance.
2. Implement graph/state/action/transition core.
3. Validate full start/goal manifests.
4. Run deterministic transition smoke cases.
5. Emit readiness artifacts.
6. Generate human-readable readiness docs.
7. Run full-instance readiness diagnostics without claiming learning success.
8. Record blockers before any learning/evaluation work.

## Relationship To Existing BBB Patterns

### Borrow From PlateSupport

Borrow:

- environment family docs;
- readiness manifests;
- artifact-first diagnostics;
- direct/direct-star fairness lessons;
- standard-gauntlet staging discipline.

Do not borrow:

- sequential action assumptions;
- fixed small action enumeration assumptions;
- direct comparison interpretation without admissibility fairness.

### Borrow From Counterpoint

Borrow:

- tower diagnostics language;
- nontrivial executable tier reporting;
- liftability success/failure summaries;
- artifact/readout split.

Do not borrow:

- assumption that the action surface is naturally small and flat.

## Future Evaluation Blueprint Boundary

This environment blueprint should not become a full evaluation-suite blueprint.
However, it must leave hooks for later evaluations.

Future evaluation families may include:

- readiness and transition diagnostics;
- discovery-surface diagnostics;
- admissibility-fairness diagnostics;
- contraction schema sweep;
- tower-structured discovery probe;
- tower training health;
- threshold frontier calibration;
- paired replicate comparison;
- tower-star guarded comparison;
- human-readable readout and system-learning archive.

The first implementation workplan should build the environment and readiness
surfaces only.

## Risks

### Risk 1: Action Space Explosion

Full action space is `5^32`. Any code path that tries to enumerate it for the
full instance will fail.

Mitigation:

- structured actions by default;
- flat enumeration only inside micro-fixture tests;
- explicit guard against full enumeration.

### Risk 2: False Fairness In Tower Comparisons

Tower liftability may provide action validity information that direct baselines
do not receive.

Mitigation:

- no serious comparisons until admissibility budgets are explicit;
- direct-star or guarded-direct baselines where appropriate;
- readouts separate policy quality from admissibility-information advantage.

### Risk 3: SVG Ambiguity

The drawings communicate physical design, but exact machine coordinates,
obstacles, and edge rules require manifest authority.

Mitigation:

- manually reviewed manifests;
- source image references;
- PO question slots for obstacle and target semantics.

### Risk 4: Overbuilding Evaluations Before Environment Readiness

The environment is tempting because it points toward a rich benchmark, but the
first slice must prove mechanics.

Mitigation:

- first workplan limited to environment core, full-instance manifest,
  transition smokes, and readiness docs.

### Risk 5: Cross-Tier Discovery Pressure Scope Creep

The hypothesis is interesting but not required for current arms.

Mitigation:

- keep it in docs and future evaluation questions;
- do not implement it in initial environment;
- do not require its artifacts in readiness.

## Consultant Recommendations

1. Make v001 centralized only in the sense of an environment API receiving a
   full ensemble action, not sequential in dynamics.
2. Use exact labeled boxes for the first serious interpretation.
3. Require both exact box targets and exact robot targets for terminal success,
   following PO reply.
4. Implement invalid ensembles as self-loops where one second still passes,
   unless PO overrides.
5. Reject shared-node collisions and head-on edge swaps. Keep any additional
   edge-crossing policy explicit.
6. Build the full 16 x 16 PO drawing as the first benchmark-facing instance.
   Use only micro-fixtures for unit tests.
7. Use manual manifests as the authority layer and SVGs as source design
   references.
8. Treat discovery artifacts as required from the beginning, even before
   serious comparisons exist.
9. Leave cross-tier discovery pressure as a future evaluation hypothesis.

## Open Questions For Project Owner

These questions are consultant-authored. They are not Project Owner statements.

### Q1: Robot Targets

Should final robot positions be part of terminal success, or should they be
reported as secondary metrics while box placement defines success?

Codex recommended default: box placement defines success; robot placement is a
metric.

#### PO Reply
> No. Robot final positions are also part of success.

#### Codex Response

Locked. Full terminal success requires exact robot target placement as well as
exact box target placement. The blueprint above has been updated so robot
target positions are not merely secondary metrics. Readouts should still report
box success and robot success separately, but the success predicate requires
both.

### Q2: Box Targets

Are boxes exactly labeled, or are targets fungible within groups?

Codex recommended default: exact labeled boxes for v001.

#### PO Reply
> The box with the correct number needs to be in the correct resting spot for success.

#### Codex Response

Locked. Boxes are exact labeled entities, not fungible within groups. `B01`
must reach the `B01` resting spot, `B02` must reach the `B02` resting spot, and
so on.

### Q3: Obstacles

Should gray regions block nodes, edges, continuous rectangular regions, or some
combination?

Codex recommended default: manually specify blocked nodes and blocked edges in
manifests.

#### PO Reply
> This seems like a dumb question. They're like concrete columns. Nothing can go there, but there are nodes inside them anyway.

#### Codex Response

Understood. The nodes drawn inside concrete columns are visual grid nodes, not
physically admissible locations. The environment manifest should mark all
column-covered nodes as blocked and should disable traversal through column
regions. This is now treated as a concrete-column occupancy/traversal rule,
not as an open conceptual obstacle question.

### Q4: Edge Direction

Are red graph edges bidirectional?

Codex recommended default: bidirectional.

#### PO Reply
> Yes. Bidirectional.

#### Codex Response

Locked. Visible red graph edges are bidirectional unless a later PO-authored
diagram explicitly marks an exception.

### Q5: Edge Collision

Are head-on swaps or edge crossings invalid, or is final shared-node occupancy
the only collision rule?

Codex recommended default: create an explicit collision-policy mode and avoid
hard-coding a stronger rule until PO confirms.

#### PO Reply
> Oh yeah. Good catch. I totally left that out. Head-on collisions along edges are not allowed. In other words, swaps that could only occur if there was a head-on collision along edge, are not allowed.

#### Codex Response

Locked. Head-on swaps along an edge are invalid. The collision policy now has
at least two required checks:

- no shared final node occupancy;
- no head-on edge swaps.

Because the movement graph is cardinal, Codex expects head-on swaps to be the
main edge-collision case. If later diagrams introduce diagonals or crossing
aisles, we should revisit perpendicular edge crossings separately.

### Q6: Invalid Ensemble Time

If an ensemble action is invalid, does the one-second timestep still pass?

Codex recommended default: yes, time passes.

#### PO Reply
> Uh. uh. This question is beyond confusing to me. What? What?

#### Codex Explains.
The question is about what happens to the clock when the robots choose a bad
synchronous ensemble command.

Example: suppose two robots both command themselves into the same node during
the same one-second tick. That ensemble is invalid. There are two possible
environment conventions:

1. The environment rejects the command before time passes. The state is
   unchanged and the clock does not advance.
2. The robots spend that second attempting a bad coordinated move. The state is
   unchanged, but the clock advances by one second, and the failed attempt is
   recorded as an invalid-discovery event.

Codex recommends option 2 because this is a timed robotics benchmark and
because hidden-admissibility discovery should cost something. If invalid
attempts do not consume time, then a policy can probe bad ensemble moves for
free unless another budget system is added. Advancing the clock makes invalid
attempts naturally expensive through the negative elapsed-time reward.

Consultant-authored follow-up question for PO: should invalid ensemble attempts
consume one second?

### Q7: Partial Execution

Should a partly invalid ensemble partially execute valid submoves, or should the
whole ensemble self-loop?

Codex recommended default: whole ensemble self-loops.

#### PO Reply
> NO.

#### Codex Response

I need to disambiguate this before workplanning, because the question had two
halves.

The intended interpretation I am currently carrying is:

```text
No partial execution.
If any part of the ensemble is invalid, no robot or box moves.
The whole ensemble is treated as an invalid attempt.
```

That matches the earlier Codex recommendation of whole-ensemble invalidation.
If "NO" meant "no, do not whole-self-loop the ensemble," then the blueprint
needs another correction before implementation.

### Q8: First Instance

Should the first implementation target a tiny/small crop, or should it try to
manifest the full 16 x 16 drawing immediately?

Codex recommended default: tiny first, then small, then full.

#### PO Reply
> No more tiny anything. We are done with tiny. That was calibration. Calibraation is over.

#### Codex Response

Locked. No official tiny benchmark instance, no tiny calibration ladder, and no
tiny-first implementation plan.

The blueprint now distinguishes official environment instances from
micro-fixture unit tests. We can still use tiny hand-authored transition
fixtures inside tests, because that is just how engineers verify local
semantics. But those fixtures must not become benchmark instances, evaluation
targets, or calibration artifacts.

### Q9: Reward Mode

Should the first learning smoke use sparse reward, shaped reward, or both?

Codex recommended default: readiness uses no reward claims; first learning
smoke starts with sparse and records shaping as a separate mode.

#### PO Reply
> I'm thinking reward for success. Then *negative time ellapsed* as a reward to encourage speed/efficiency. Ah ah. And then a reward for each box in correct final position and robot in correct final position.

#### Codex Response

This is a good reward shape for the actual environment:

- terminal success reward;
- negative elapsed-time pressure, so faster solutions are better;
- partial-position reward for each correctly placed box;
- partial-position reward for each correctly placed robot.

Design consequence: if invalid attempts consume time, they are automatically
penalized by elapsed time even without a separate invalid-action penalty. We
can still record invalid attempts as diagnostics. A separate invalid penalty is
optional and should be explicit if used.

### Q10: Discovery Query Budget

Should policies be allowed to query admissibility before committing an ensemble
action, or should invalid attempts be the only way to discover invalidity?

Codex recommendation: define both as explicit modes, but do not compare arms
unless their query/invalid-attempt budgets are documented.

#### PO Reply
> Yeah. ...I mean policies should decide over any invalid action, so however that needs to happen, yes.

#### Codex Response

Interpreting this as: policies are allowed to propose ensemble commands from
the broad command space, including commands that turn out to be invalid.
Validity is discovered by interacting with the environment, not handed out as a
complete admissible-action set.

Design consequence: the default arm should not receive a free global mask. Any
guard, query, mask, or cache surface must be explicit and charged/documented.

### Q11: Cache Persistence

If an arm discovers valid or invalid ensemble moves, when does that discovery
cache reset?

Options:

- per episode;
- per run;
- per seed;
- per replicate;
- per arm;
- never during an evaluation.

Codex recommendation: start with per-run/per-arm cache for diagnostics, then
make comparison-specific choices explicit.

#### PO Reply
> Yeah let's start with that.

#### Codex Response

Locked as initial diagnostic policy: start with per-run/per-arm discovery
caches. The cache policy must be recorded in manifests so later comparisons
can say exactly what was remembered and for whom.

### Q12: Tower-Structured Discovery Evidence

What evidence would satisfy the PO that the tower discovered useful large-scale
structure rather than merely receiving a better mask?

Codex recommendation: require discovery summaries showing reusable abstract
regions, reduced invalid discovery burden, and fair direct/direct-star
admissibility surfaces.

#### PO Reply
> I agree.

#### Codex Response

Accepted. Tower-structured discovery evidence should require discovery
summaries showing reusable abstract structure, reduced invalid-discovery burden
under fair accounting, and direct/direct-star admissibility surfaces strong
enough to rule out a mere mask advantage.

### Q13: Cross-Tier Discovery Pressure

Should cross-tier discovery pressure remain only a retained hypothesis for now?

Codex recommendation: yes. Do not implement in initial arms.

#### PO Reply
> Yes.

#### Codex Response

Locked. Cross-tier discovery pressure remains a retained hypothesis and
evaluation interpretation lens. It is not part of the current environment arm
implementation.

## Blueprint-To-Workplan Gate

Do not create the implementation workplan until the following are resolved or
explicitly accepted as workplan assumptions:

- Q6 invalid ensemble time: does an invalid ensemble consume one second?
- Q7 partial execution: confirm that "NO" means no partial execution and whole
  ensemble invalidation;
- column manifest extraction: exact blocked nodes/edges must be specified from
  the PO drawing;
- reward constants: success reward, per-correct-entity reward, and elapsed-time
  coefficient can be chosen in the workplan if PO accepts defaults, but they
  must be explicit before implementation.

Resolved by PO reply and no longer gate blockers:

- robot targets are required for success;
- exact box labels are required for success;
- columns are blocked physical regions even if visual grid nodes appear inside
  them;
- graph edges are bidirectional;
- head-on edge swaps are invalid;
- no official tiny calibration instance should be created;
- cross-tier discovery pressure is hypothesis-only for current scope.

The workplan should follow Phase.Stage.Action discipline and should begin with
environment core plus readiness diagnostics only. It should not include a full
learning gauntlet.

## Recommended Workplan Scope After Approval

The first implementation workplan should cover:

```text
Phase 0: branch/status/readiness
Phase 1: full PO drawing manifest and ids
Phase 2: graph/state/action models
Phase 3: synchronous transition engine
Phase 4: micro-fixture golden tests
Phase 5: readiness artifact writer
Phase 6: CLI smoke commands
Phase 7: full-instance readiness diagnostics
Phase 8: docs/readout surface
Phase 9: verification and implementation log
```

Explicitly out of first workplan scope:

- full 16 x 16 serious learning;
- tower comparison;
- standard gauntlet;
- cross-tier discovery pressure implementation;
- public benchmark claims.
