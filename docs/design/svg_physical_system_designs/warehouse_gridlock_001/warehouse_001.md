# Warehouse Gridlock 001

## Status

Initial professional environment design note.

This document translates Project Owner-authored SVG design drawings into a
candidate robotics benchmark environment. It is not yet a blueprint, workplan,
implementation, or claim-bearing evaluation design.

The drawings are the actual design source and are authored by the Project
Owner. Codex's role in this file is interpretive: to read those PO drawings,
make the surrounding benchmark-environment implications explicit, and propose a
professional finite-environment contract. Any interpretation below that goes
beyond what is visually explicit in the drawings is labeled as a Codex inference
and should be corrected by the Project Owner before implementation.

## Attribution

### Project Owner

The Project Owner created the SVG environment drawings. Those images are the
primary design artifact for this environment. The Project Owner also clarified
the timed synchronous-control rule after the initial Codex interpretation.

PO-authored design artifacts:

- `assets/environment_designs/gridlock_001_start.svg`
- `assets/environment_designs/gridlock_001_end.svg`
- `assets/environment_designs/gridlock_001_moves_001.svg`
- `assets/environment_designs/gridlock_001_moves_002.svg`

The PO-authored images establish the physical situation, object layout, goal
layout, and movement/push primitives that this document discusses.

PO-authored design clarification:

- one environment timestep represents one second;
- every robot chooses a primitive command at each timestep;
- each robot may move one graph step or stay in place;
- the robot commands form a synchronous ensemble move;
- an ensemble move is invalid if any two entities, robot or box, would occupy
  the same node.
- the real-life MDP should be treated as hidden or effectively hidden, because
  the admissible-state graph is not realistically computable in advance;
- discovery of admissible states, invalid ensembles, bottlenecks, and reachable
  structure is central to any evaluation arm.
- comparisons between evaluation arms must be careful about how admissible
  states and admissible actions are exposed, discovered, cached, masked, or
  reused, because unequal admissibility information can create an unfair
  advantage unrelated to the intended policy or tower mechanism.
- discovery is required for every arm, but the benchmark is explicitly
  interested in whether tower structure lets policies discover large-scale
  speed-ups or usable global structure that a direct arm may never find under
  the same discovery budget.
- tower-structured discovery may require a mechanism by which a lower-tier
  desire to explore a particular concrete or local region creates pressure on
  higher-tier choices, especially when the need for that exploration is locally
  invisible at the higher tier. This is a hypothesis to retain for evaluation
  interpretation, not a requirement for any current arm implementation.

### Codex

Codex populated the surrounding markdown as an interpretation layer around the
PO-authored drawings and PO-authored timing/control clarification. Codex did
not author the physical design shown in the images and did not author the
synchronous ensemble-control rule. Codex's contribution here is:

- naming the candidate environment family;
- translating visual intent into possible state/action/transition contracts;
- identifying benchmark and artifact requirements;
- identifying tower/state_collapser opportunities and risks;
- listing open PO questions before blueprinting.

Where this document says "Codex reads," "Codex inference," or "recommended,"
that text should be understood as Codex interpretation or recommendation, not
as Project Owner intent unless the PO later confirms it.

## Source Drawings

The current drawing assets are:

- `assets/environment_designs/gridlock_001_start.svg`
- `assets/environment_designs/gridlock_001_end.svg`
- `assets/environment_designs/gridlock_001_moves_001.svg`
- `assets/environment_designs/gridlock_001_moves_002.svg`

The design file is named `warehouse_001.md`, while the assets currently use the
`gridlock_001` prefix. For now this document treats those as names for the same
candidate environment:

- human-facing name: `Warehouse Gridlock 001`
- candidate environment family id: `warehouse_gridlock_001`
- likely implementation id, if approved: `warehouse_gridlock_16x16_v001`

## PO-Provided Physical Intent

The Project Owner is beginning a new workflow in which PO-authored SVG diagrams
of physical systems seed environment design. This document is the first
professionalized Codex translation of one such PO drawing set into a benchmark
candidate.

The broad environment intent appears to be a discrete warehouse robotics task:
many mobile robots must rearrange many boxes on a constrained grid while
avoiding obstacles, traffic jams, invalid moves, and deadlocked configurations.

### PO Clarification: Timed Synchronous Control

The Project Owner clarified that this environment has a timer. One environment
timestep represents one second.

At each one-second timestep, every robot chooses a primitive movement command.
Each robot may either move one graph step or stay where it is. The resulting
commands form one synchronous ensemble move.

The ensemble move is invalid if the resulting transition would cause any two
entities, robot or box, to occupy the same node. This is a core environment
rule and supersedes the earlier Codex recommendation to start with centralized
sequential one-robot control.

Codex inference: this means the benchmark is a true simultaneous multi-robot
warehouse coordination task, not merely a single-controller puzzle that moves
one robot at a time.

### PO Clarification: Hidden Admissible-State Graph

The Project Owner clarified that the "real life" MDP for this environment
should be treated as hidden or effectively hidden. Even though a tiny finite
instance may be enumerable in principle, the graph of admissible states for the
serious warehouse task is not realistically computable in advance.

This makes discovery central to the benchmark. A useful evaluation arm should
not assume that it already has the full admissible transition graph, the full
reachable state set, or a complete map of safe ensemble moves. It should be
judged partly by how it discovers:

- which synchronous ensemble moves are admissible;
- which local configurations are deadlocked or cul-de-sac-like;
- which bottlenecks control long-horizon progress;
- which reachable regions matter for solving the task;
- which abstractions remain executable under discovered constraints.

Codex inference: for BBB, this means the environment should support exact
auditable transition checks when a state/action is proposed, but evaluations
should not be designed as if every arm begins with an explicit full transition
graph. The graph is an oracle-backed environment surface, not a fully handed-out
planning object.

### PO Clarification: Admissibility Fairness Across Arms

The Project Owner clarified that the hidden-admissibility issue affects how
different evaluation arms can be compared. Because admissible states and
admissible actions are not assumed to be globally known in advance, every
comparison must say exactly how each arm obtains admissibility information.

Important comparison surfaces include:

- whether an arm receives a precomputed action mask;
- whether an arm may query admissibility before committing an ensemble action;
- whether failed ensemble attempts count against its budget;
- whether admissible-action discoveries are cached;
- whether cached discoveries persist across episodes, seeds, or replicates;
- whether tower arms receive liftability/admissibility information that direct
  arms do not;
- whether guarded direct baselines receive equivalent one-step admissibility
  information;
- whether all arms share the same discovered-state/action budget.

Codex inference: no comparison should claim a tower or policy advantage unless
the readout separates policy quality from admissibility-information advantage.
For example, if a tower arm avoids invalid ensemble moves because its lift
machinery effectively supplies an action mask, then a fair direct or direct-star
control should receive a comparable admissibility surface, or the report should
state that the comparison is measuring both policy behavior and admissibility
discovery.

### PO Clarification: Tower-Structured Discovery Hypothesis

The Project Owner clarified the positive target of this example. The point is
not to remove discovery from the tower arm or to give the tower arm hidden
admissibility information for free. Discovery is required for all arms.

The intended benchmark question is whether the tower can make discovery
productive at larger scale. A direct arm may spend its budget discovering local
invalid ensembles, local blockages, and low-level traffic facts without finding
the larger structure that creates a speed-up. A tower arm, under a fair
admissibility/discovery contract, may be able to discover useful abstract
structure, bottleneck structure, flow structure, or reusable liftable regions
that the direct arm effectively never finds within the same budget.

Codex inference: the comparison should therefore report both fairness and
opportunity:

- fairness: every arm must pay an explicit and comparable cost for
  admissibility discovery;
- opportunity: the tower may still win if its abstraction makes the same
  discovery budget reveal larger-scale reusable structure;
- interpretation: a tower win should be described as "tower-structured
  discovery found useful large-scale structure" only if the readout shows that
  the advantage is not merely an uncharged action mask or hidden oracle.

### PO Clarification: Cross-Tier Discovery Pressure

The Project Owner clarified a possible future mechanism to keep in mind for
tower-structured discovery. There may eventually need to be an "I want to
discover here" signal in which a policy's lower-tier interest in exploring a
concrete, local, or partially known region creates pressure on higher-tier
selection.

The motivation is that an exploration need can be visible at one tier while
being locally invisible at another. For example, a lower tier may repeatedly
encounter a bottleneck, blocked push, or promising unexplored local region, but
the higher tier may see only an abstract state/action cell that does not expose
why this particular region needs attention. Without some cross-tier discovery
pressure, the higher tier may fail to allocate abstract choices toward the
place where useful admissibility information can be discovered.

Codex inference: this should be treated as an open tower-control design topic,
not as an already-solved environment rule and not as a required feature for the
first environment arms. A future evaluation or later tower-control design may
ask whether discovery pressure should be represented as:

- an intrinsic reward or priority signal;
- a per-tier exploration bonus;
- a demand propagated from concrete failed attempts to abstract action cells;
- a query budget allocated downward from abstract cells;
- a cache-miss or uncertainty signal attached to fibers;
- an event-row surface only, used for diagnostics before it becomes a control
  mechanism.

Codex inference: this is distinct from giving the tower free information. The
signal should help decide where to spend discovery effort; it should not erase
the requirement that every arm pay for admissibility discovery under an explicit
budget. For the current environment design, this should remain a hypothesis and
readout question rather than an implementation obligation.

This is a promising benchmark family because it is small enough to be fully
specified as a finite environment, but rich enough to contain realistic
robotics-adjacent difficulties:

- multi-robot coordination;
- movable objects;
- narrow passages and bottlenecks;
- combinatorial action branching;
- invalid actions and blocked pushes;
- long-horizon rearrangement;
- local deadlocks that are easy to enter and hard to escape;
- natural abstractions over space, labels, object groups, and flow direction.

## Start Diagram

<p align="center">
  <picture>
    <img
      alt="Warehouse Gridlock 001 start state"
      src="../../../../assets/environment_designs/gridlock_001_start.svg"
      width="500"
    >
  </picture>
</p>

<table align="center">
  <tr>
    <td width="520" align="center">
      <sub><em>Start state. Codex reads this as a 16 x 16 warehouse graph with fixed obstacles, 32 robots, and 32 labeled boxes staged near the top and bottom boundaries.</em></sub>
    </td>
  </tr>
</table>

### Codex Reading Of The Start State

The diagram shows a square 16 x 16 graph. Grid intersections are navigable graph
nodes unless occupied by an obstacle, robot, or box. Red line segments indicate
legal adjacency between neighboring nodes.

There appear to be:

- 32 robots, labeled `R01` through `R32`;
- 32 boxes, labeled `B01` through `B32`;
- fixed gray obstacle regions inside the warehouse;
- top and bottom staging lanes;
- enough interior open space to make routing possible but not trivial.

Codex inference: the start state is deliberately congested. Most objects are
near boundary lanes, which creates immediate traffic pressure and many local
choices that may block later motion.

Codex inference: boxes `B01` through `B16` appear to start near the lower side
and ultimately belong on the upper side, while boxes `B17` through `B32` appear
to start near the upper side and ultimately belong on the lower side. This makes
the task more like a two-way warehouse exchange than a simple local shuffle.

## Goal Diagram

<p align="center">
  <picture>
    <img
      alt="Warehouse Gridlock 001 goal state"
      src="../../../../assets/environment_designs/gridlock_001_end.svg"
      width="500"
    >
  </picture>
</p>

<table align="center">
  <tr>
    <td width="520" align="center">
      <sub><em>Goal state. Codex reads this as exact labeled box placement plus a desired robot staging pattern in adjacent interior lanes.</em></sub>
    </td>
  </tr>
</table>

### Codex Reading Of The Goal State

The goal diagram appears to specify exact labeled targets, not just anonymous
box occupancy.

Codex inference: the terminal condition should probably require every box label
to occupy its matching goal node. The goal may also require every robot label to
occupy the shown final staging node, though this is less certain.

The distinction matters:

- If robot positions are part of the goal, the task is a full rearrangement
  problem over robots and boxes.
- If only box positions are part of the goal, robot final positions are either
  illustrative or secondary.

Proposed default for a professional benchmark: make box placement the primary
success condition, but record robot-final-position accuracy as an auxiliary
metric until the PO confirms whether robot placement is also required.

## Robot Movement Diagram

<p align="center">
  <picture>
    <img
      alt="Warehouse Gridlock 001 robot movement primitive"
      src="../../../../assets/environment_designs/gridlock_001_moves_001.svg"
      width="220"
    >
  </picture>
</p>

<table align="center">
  <tr>
    <td width="520" align="center">
      <sub><em>Robot movement primitive. Codex reads this as one-step north, south, east, or west movement along graph edges into unoccupied neighboring nodes.</em></sub>
    </td>
  </tr>
</table>

### Codex Reading Of Robot Motion

The first movement diagram shows a robot with four possible one-step moves:
left, right, up, and down. There is no visual indication of diagonal movement,
continuous velocity, robot orientation, turn cost, acceleration, carrying, or
rotation.

Proposed default action primitive:

```text
move(robot_id, direction)
```

where `direction` is one of:

```text
north, south, east, west
```

The move is legal when:

- the requested neighboring node exists;
- the edge from the current node to the neighbor exists;
- the neighboring node is not blocked by a fixed obstacle;
- the neighboring node is not occupied by another robot;
- the neighboring node is not occupied by a box, unless the move is interpreted
  as a valid push under the box-pushing rule below.

## Box Push Diagram

<p align="center">
  <picture>
    <img
      alt="Warehouse Gridlock 001 box push primitive"
      src="../../../../assets/environment_designs/gridlock_001_moves_002.svg"
      width="220"
    >
  </picture>
</p>

<table align="center">
  <tr>
    <td width="520" align="center">
      <sub><em>Box push primitive. Codex reads this as a robot pushing an adjacent box one grid step in the same direction, if the box destination is open.</em></sub>
    </td>
  </tr>
</table>

### Codex Reading Of Box Motion

The second movement diagram shows a robot moving into a neighboring box's
current node while the box moves one node farther along the same direction.

Proposed default pushing rule:

```text
robot at u
box at v
direction d
v = neighbor(u, d)
w = neighbor(v, d)
```

The push is legal when:

- edge `u -> v` exists;
- edge `v -> w` exists;
- `v` contains a box;
- `w` exists;
- `w` is not a fixed obstacle;
- `w` is not occupied by a robot;
- `w` is not occupied by another box.

The transition is:

```text
robot_id: u -> v
box_id: v -> w
```

Codex inference: the intended mechanics are push-only. There is no evidence in
the drawing of pulling, carrying, lifting, box rotation, multi-robot pushing, or
continuous-force contact dynamics.

## Proposed Formal Environment Contract

### World

The environment is a finite directed or undirected graph embedded in a 16 x 16
grid.

Recommended implementation representation:

```text
WarehouseGraph:
  nodes: set[GridNode]
  directed_edges: set[(GridNode, GridNode)]
  blocked_nodes: set[GridNode]
```

For the first version, treat the visual grid as an undirected graph with
bidirectional cardinal edges wherever a red segment exists. If the PO intends
directed aisles or one-way lanes, that should be added explicitly in a later
diagram or PO note.

### Objects

```text
RobotId = R01 ... R32
BoxId = B01 ... B32
```

Each robot occupies exactly one graph node. Each box occupies exactly one graph
node. A node can contain at most one movable object.

Fixed obstacles occupy unavailable nodes or unavailable spatial regions. For
implementation, the obstacle regions should be converted into blocked graph
nodes and/or removed edges. The conversion rule should be explicit and recorded
in an environment readiness artifact.

### State

Recommended state:

```text
WarehouseGridlockState:
  robot_positions: dict[RobotId, GridNode]
  box_positions: dict[BoxId, GridNode]
```

Optional state additions, if PO wants a more robotic version later:

- robot orientation;
- battery or action budget per robot;
- payload capacity;
- one-way aisle direction state;
- temporary reservation state for simultaneous multi-agent movement.

The current SVGs do not require those additions.

### Action Space

The Project Owner clarified that control is synchronous. Every robot receives a
movement command at every one-second timestep.

Recommended benchmark action space:

```text
DirectionOrStay = north | south | east | west | stay

EnsembleAction:
  robot_commands: dict[RobotId, DirectionOrStay]
```

This creates a simultaneous multi-robot control problem. At each environment
step, the policy chooses one command for every robot. A robot may move one graph
edge in a cardinal direction or stay in place.

With 32 robots, the naive full action space has size `5^32`, so the
implementation should not treat the full ensemble action set as a flat
enumerated list except for tiny instances. The environment should expose a
structured ensemble action interface and emit artifacts that make the chosen
per-robot commands inspectable.

Codex inference: tiny and small instances will be essential for exhaustive
diagnostics. Full-scale training will likely need a factored policy, scripted
controllers, action proposal machinery, or state_collapser-compatible
structured action cells rather than flat action enumeration.

### Transition Semantics

For an `EnsembleAction`, evaluate all robot commands as a one-second
synchronous transition.

For each robot command:

1. If the command is `stay`, the robot proposes to remain at its current node.
2. If the command is a cardinal direction, let `u` be the robot's current node
   and let `v` be the neighboring node in that direction.
3. If `v` is empty and traversable in the pre-transition state, the robot
   proposes to move from `u` to `v`.
4. If `v` contains a box, let `w` be the neighboring node one step beyond `v`
   in the same direction. If `w` is traversable, the robot proposes to move
   from `u` to `v` and the box proposes to move from `v` to `w`.
5. Otherwise that robot command is locally invalid.

The ensemble transition is globally valid only if:

- every individual robot command is locally valid;
- after applying all proposed robot and box movements, no two entities occupy
  the same node;
- no robot or box ends on a blocked node;
- no entity is assigned two incompatible proposed destinations.

If any of those checks fails, the ensemble action is invalid.

Proposed invalid-action semantics:

- invalid actions are represented as self-loops;
- invalid actions emit explicit event rows;
- invalid actions receive a penalty;
- masked or guarded policies may optionally remove invalid ensemble commands
  from the available proposal set;
- direct and tower comparisons must state whether invalid ensemble moves were
  masked,
  guarded, or allowed.

Open implementation question: whether head-on edge swaps or edge crossings are
invalid even when final node occupancy is collision-free. The PO clarification
specified node occupancy conflicts. A robotics-stricter implementation may also
reject edge-crossing collisions, but that should be confirmed before it becomes
part of the benchmark contract.

The direct-star / guarded-direct lessons from PlateSupport should carry over
here. A tower advantage caused only by avoiding obvious one-hop invalid moves
must not be overclaimed as a tower-specific planning advantage.

## Goal And Success Contract

### Primary Goal

Recommended primary terminal condition:

```text
for every box_id:
  box_positions[box_id] == target_box_positions[box_id]
```

This treats the warehouse as a labeled box rearrangement problem.

### Secondary Goal

Potential secondary terminal condition:

```text
for every robot_id:
  robot_positions[robot_id] == target_robot_positions[robot_id]
```

Codex recommends recording this as a metric before making it part of success.
If robot placement is made mandatory too early, the first environment may
become unnecessarily brittle and hard to diagnose.

### Horizon

The SVG does not specify a maximum episode length.

Recommended design path:

1. Compute lower-bound facts from the start and goal diagrams:
   - total Manhattan box displacement;
   - minimum number of required pushes;
   - robot-to-box assignment lower bounds;
   - bottleneck/corridor occupancy constraints.
2. Set an initial diagnostic horizon as a multiple of those lower bounds.
3. Record horizon choice in the environment manifest and in every evaluation
   budget lock.

For early smokes, also define smaller crop or subset instances so the mechanics
can be tested before the full 32-robot, 32-box benchmark is used.

## Reward Contract

The professional benchmark should separate the environment's physical dynamics
from the learning reward. The finite transition system should be deterministic
and auditable; reward variants can then be tested without changing the physical
environment.

Recommended base reward:

```text
step_penalty: small negative value for every attempted action
invalid_penalty: additional negative value for invalid actions
push_penalty: optional small negative value for pushes, if push economy matters
goal_reward: positive value on first successful completion
```

Recommended diagnostic shaping candidates:

- reduction in total box distance to target;
- count of boxes newly placed on targets;
- preservation of boxes already on targets;
- congestion penalties for blocking chokepoints;
- deadlock warning penalties for irreversible local traps.

For benchmark clarity, every evaluation should state whether it uses sparse
reward, shaped reward, or a mixed reward.

## Observation Modes

The same environment can support multiple observation modes.

Recommended observation modes:

- `symbolic_full`: exact robot positions, box positions, obstacle layout, and
  target maps;
- `symbolic_local`: selected robot local neighborhood plus global target
  summary;
- `graph_tensor`: node features and edge features suitable for graph models;
- `flat_indexed`: compact integer state/action encoding for small exhaustive
  diagnostics.

The first BBB implementation should start with `symbolic_full` and artifact
tables. More learned observation interfaces can come later.

## Why This Is A Serious Benchmark Candidate

This candidate is more than a toy gridworld because the difficulty is not just
shortest-path navigation. The hard parts are structural:

- The policy must choose which robot acts next.
- Many actions are locally legal but strategically harmful.
- Pushing a box changes future navigability.
- Boxes and robots can block each other.
- Boundary staging lanes create immediate congestion.
- Interior obstacles create bottlenecks.
- The two-way exchange pattern can force temporary displacement away from
  target positions.
- The environment naturally contains cul-de-sacs and deadlock-prone moves.
- The admissible-state graph is effectively hidden at serious scale, so an
  evaluation arm must discover useful reachable structure rather than assume a
  complete precomputed MDP.

These features make the environment useful for BBB because they create exactly
the kinds of questions this repo has been built to inspect:

- Does a tower produce executable nontrivial abstractions?
- Does a schema avoid local bad moves for meaningful reasons?
- Does a direct guarded baseline remove the apparent tower advantage?
- Does training health survive beyond smoke scale?
- Are human-readable readouts able to explain the mechanism, not just the
  outcome number?
- Did every compared arm receive, discover, cache, and spend admissibility
  information under a fair and explicitly documented contract?
- Can a tower arm use the same discovery burden to find larger-scale reusable
  structure or speed-ups that direct exploration does not find?
- Might the tower eventually need cross-tier discovery-pressure signals so local
  discovery needs can influence higher-tier abstract choices?

## Expected Environment Family

The full 16 x 16, 32-robot, 32-box problem may be too large as the first
implementation target. A professional benchmark family should include a ladder
of instances that share the same mechanics.

Recommended instance ladder:

```text
warehouse_gridlock_tiny_v001:
  small crop, 1-2 robots, 1-2 boxes

warehouse_gridlock_small_v001:
  moderate crop, several robots and boxes, at least one obstacle or bottleneck

warehouse_gridlock_medium_v001:
  larger subset, multiple interacting flows

warehouse_gridlock_16x16_v001:
  full PO drawing with 32 robots and 32 boxes
```

Each instance should have:

- a stable instance id;
- a start-state manifest;
- a goal-state manifest;
- a graph manifest;
- a target manifest;
- a rendered diagram reference;
- a shortest-path or lower-bound diagnostic where feasible.

## State Collapser / Tower Opportunities

This environment has several natural abstraction axes.

Potential state abstractions:

- collapse robot labels within symmetric groups;
- collapse box labels within target families;
- collapse spatial regions into lanes, corridors, staging zones, and obstacle
  neighborhoods;
- collapse exact positions to progress bands;
- collapse local configurations by pushability or blockage status.

Potential action abstractions:

- choose a robot family instead of an exact robot;
- choose a box family instead of an exact box;
- choose a flow direction, such as "move lower boxes upward";
- choose a corridor or staging-lane operation;
- choose a push/move class instead of a primitive robot-direction pair.

Hypothetical future discovery-pressure surfaces:

- local failed ensemble attempts pushing uncertainty upward into abstract
  action cells;
- concrete bottleneck encounters creating priority on abstract corridor or flow
  choices;
- unexplored fibers increasing the chance that a higher-tier policy selects an
  abstract cell for exploration;
- per-tier discovery budgets that can be allocated across fibers;
- event rows that show when lower-tier discovery demand did or did not affect
  higher-tier choices.

These surfaces are not required for the current environment arms. They are
retained as a hypothesis for interpreting future evaluations and for deciding
whether a later tower-control mechanism is needed.

Potential tower risks:

- abstract actions may not be liftable at a particular concrete state;
- high-level progress cells may hide deadlocks;
- a tower may appear good only because it filters invalid or dead-end actions;
- unlabeled symmetries may erase goal-critical box identities;
- source-local outgoing choices may collapse too aggressively in bottlenecks.

The PlateSupport direct-star and tower-star lessons should be treated as
required background for this environment. Any tower comparison should include a
direct guarded baseline that gets the same obvious one-hop invalid-action
avoidance when the claim is about planning rather than action validity.

## Minimum Diagnostics Before Learning

Before any serious training comparison, the environment should produce
diagnostic artifacts for:

- graph size, obstacle count, and connected components;
- start and goal validity;
- number of robots and boxes;
- target uniqueness;
- action count by state, at least for sampled or reachable states;
- invalid move categories;
- pushable box counts;
- blocked box counts;
- shortest-path or lower-bound estimates on tiny/small instances;
- deadlock/cul-de-sac examples;
- discovered-state counts and discovered-transition counts;
- discovery coverage summaries for each evaluation arm;
- invalid ensemble-move discovery summaries;
- admissibility-information budgets by arm;
- action-mask/query/cache policy manifests;
- tower construction success;
- liftability success/failure by tier;
- direct, direct-star, tower, and tower-star semantics.

Optional future diagnostics, if the hypothesis becomes active:

- cross-tier discovery-pressure event summaries;
- fiber uncertainty or cache-miss summaries;
- evidence that lower-tier discovery demand did or did not affect higher-tier
  choices.

## Candidate Evaluation Path

A future professional evaluation suite should probably mirror the PlateSupport
standard gauntlet style, but only after the environment exists and passes basic
readiness checks.

Recommended evaluation stages:

1. Environment readiness and graph diagnostics.
2. Manual-policy smoke on tiny and small instances.
3. Random and masked-random action sanity checks.
4. Discovery-surface diagnostics: discovered states, discovered transitions,
   invalid ensemble moves, bottlenecks, and deadlock-prone regions.
5. Admissibility-fairness diagnostics: action masks, query budgets, failed
   ensemble accounting, cache policy, and arm-equivalence checks.
6. Tower-structured discovery diagnostics: whether candidate abstractions turn
   discovered low-level admissibility facts into reusable large-scale structure.
7. Contraction schema sweep for nontrivial executable towers.
8. Candidate discovery for trainable tower configurations.
9. Tower-only training health.
10. Threshold frontier calibration.
11. Paired replicate comparison against direct and direct-star controls.
12. Tower-star comparison if liftability filtering becomes central.
13. Human-readable readout and system-learning archive.

Future evaluation hypothesis to retain:

- cross-tier discovery pressure may eventually need its own diagnostic, but it
  is not required in any current arm.

The first implementation should not jump directly to full comparison claims.
It should first prove that the finite environment, artifacts, and diagnostics
are correct.

## Artifact And Readout Requirements

If implemented, every run should write repo-compatible artifact surfaces that
can be transformed by:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <readout_source.json>
```

Minimum environment artifacts:

- `environment_instance_manifest.json`
- `graph_manifest.json`
- `start_state.json`
- `goal_state.json`
- `target_manifest.json`
- `action_space_manifest.json`
- `transition_rule_manifest.json`
- `readiness_summary.csv`
- `invalid_action_summary.csv`
- `discovered_state_summary.csv`
- `discovered_transition_summary.csv`
- `discovery_coverage_summary.csv`
- `admissibility_budget_summary.csv`
- `action_mask_policy_manifest.json`
- `admissibility_cache_policy_manifest.json`
- `example_rollout_events.csv`

Optional future artifacts, if cross-tier discovery pressure becomes an active
mechanism:

- `cross_tier_discovery_pressure_events.csv`
- `cross_tier_discovery_pressure_summary.csv`

Minimum human-readable docs:

- environment README;
- method document;
- glossary;
- runbook;
- artifact index;
- result readout;
- system-learning conversation section.

## Professional Benchmark Claim Boundary

Until implementation and diagnostics exist, this document supports only the
following claim:

```text
Warehouse Gridlock 001 is a candidate discrete robotics benchmark environment
specified by PO-provided SVG physical-intent drawings and Codex-inferred
finite graph mechanics.
```

It does not yet support claims about:

- solvability of the full 16 x 16 instance;
- training difficulty;
- tower advantage;
- benchmark readiness;
- state_collapser performance;
- comparison significance.

## Open PO Questions

1. Are robot final positions part of the terminal success condition, or are
   they illustrative and secondary to box placement?
2. Are boxes individually labeled with exact targets, or are they fungible
   within groups such as `B01` through `B16` and `B17` through `B32`?
3. Are the gray rounded blocks fixed obstacles, shelves, blocked cells, or
   regions that only boxes/robots cannot enter?
4. Are all red grid edges bidirectional, or should some aisles be one-way?
5. Should invalid ensemble actions be available as self-loop penalties, or
   should the default action proposal surface hide them?
6. Are head-on edge swaps or edge crossings invalid, or is final node occupancy
   the only collision rule?
7. Is pushing the only box interaction, or should pulling/carrying/multi-robot
   pushing exist in a later version?
8. Should the first implemented instance be the full 16 x 16 drawing, or a
   tiny/small crop derived from it?
9. Should rewards be sparse at first, shaped at first, or both as separate
   reward modes?
10. What discovery surfaces should every evaluation arm expose: discovered
    states, discovered transitions, invalid ensembles, deadlock examples,
    bottleneck occupancy, or all of these?
11. Should arms be allowed to query admissibility before action commitment, or
    should invalid ensemble attempts be part of the learning/exploration cost?
12. If admissibility discoveries are cached, should the cache reset per episode,
    per replicate, per seed, per arm, or never during a run?
13. What admissibility surface must a direct/direct-star baseline receive to be
    comparable to a tower arm that has liftability information?
14. What evidence would count as tower-structured discovery rather than merely
    an admissibility-mask advantage?
15. Should cross-tier discovery pressure remain only an evaluation hypothesis
    for now, or is there a later point where it should become diagnostic-only
    events, intrinsic reward, abstract-cell priority, fiber uncertainty, or
    something else?
16. What makes this environment professionally satisfying to the PO: exact
    logistics realism, puzzle hardness, tower-diagnostic richness, or all
    three?

## Recommended Next Design Step

The next design artifact should be a turn-by-turn `design_discussion.md` or a
blueprint in a dedicated folder such as:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/
```

That folder should preserve:

- this interpreted source note;
- PO corrections to the inferred mechanics;
- exact start/goal coordinate extraction from the SVGs;
- a blueprint for the finite environment;
- a Phase.Stage.Action implementation workplan only after the blueprint is
  settled.

The most important immediate correction has now been made: the control model is
timed synchronous ensemble control, with one second per timestep and one command
per robot per timestep. The next important correction is deciding whether final
node occupancy is the only collision rule, or whether edge swaps/crossings are
also invalid. The other central benchmark-design correction is that serious
evaluations should treat the admissible-state graph as hidden or effectively
hidden, so discovery must be part of every meaningful arm's readout. This also
means every comparison must report how admissible states/actions were exposed,
discovered, cached, masked, and charged to each arm, because otherwise the
comparison may be measuring unequal admissibility information rather than the
intended policy or tower mechanism. Within that fair-discovery setup, the core
target of this example is to test whether tower structure helps policies
discover and reuse large-scale speed-ups that direct arms may never find under
the same discovery burden.
