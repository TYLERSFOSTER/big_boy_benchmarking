# Warehouse Gridlock 001 Environment Readiness

This is the first BBB readiness surface for the PO-authored Warehouse Gridlock 001 physical-system drawing. It checks whether the environment contract can be loaded, validated, stepped, and artifacted. It is not a tower evaluation, standard gauntlet, learned-policy result, or benchmark claim.

## Badges

![readiness](badges/readiness.svg)

## Identity

- Environment family id: `warehouse_gridlock_001`.
- Instance id: `warehouse_gridlock_16x16_v001`.
- Robots: `32`.
- Boxes: `32`.
- Visual grid nodes: `256`.
- Traversable nodes: `251`.
- Directed traversable edges: `920`.

## Source Authority

The physical design comes from Project Owner-authored SVG drawings. Codex translated those drawings into a manifest and readiness surface.

- Source design note: `docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md`.
- Source image: `assets/environment_designs/gridlock_001_start.svg`.
- Source image: `assets/environment_designs/gridlock_001_end.svg`.
- Source image: `assets/environment_designs/gridlock_001_moves_001.svg`.
- Source image: `assets/environment_designs/gridlock_001_moves_002.svg`.

## Mechanics Checked

- One timestep is one second.
- Every robot receives one command per timestep.
- Valid ensemble moves advance time by one second.
- Invalid ensemble attempts are whole-ensemble self-loops and do not advance time.
- Push-only box dynamics are implemented.
- Shared final occupancy and head-on swaps are invalid.
- Concrete columns are blocked physical nodes.
- Terminal success requires exact robot and box target placement.

## Artifact Surface

- Artifact root: `docs/evaluations/warehouse_gridlock_001/environment_readiness/artifacts/smoke_001`.
- Readout source: `docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json`.

## Claim Boundary

environment readiness only; no tower, gauntlet, learning, or benchmark-performance claim.

## Evaluator / Codex Clarifying Turns

### Evaluator Turn

_Add questions or corrections here._

### Codex Turn

_Awaiting evaluator turn._
