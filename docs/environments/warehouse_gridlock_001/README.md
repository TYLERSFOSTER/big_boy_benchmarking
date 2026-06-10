# Warehouse Gridlock 001

Warehouse Gridlock 001 is a PO-authored discrete robotics environment design
seeded from SVG diagrams. The current BBB implementation target is environment
readiness only.

## Source Authority

The Project Owner authored the physical-system drawings:

- `assets/environment_designs/gridlock_001_start.svg`
- `assets/environment_designs/gridlock_001_end.svg`
- `assets/environment_designs/gridlock_001_moves_001.svg`
- `assets/environment_designs/gridlock_001_moves_002.svg`

Codex translated those drawings into the manifest:

- `docs/environments/warehouse_gridlock_001/manifests/warehouse_gridlock_16x16_v001.json`

## Identity

- Environment family id: `warehouse_gridlock_001`.
- Implementation family id: `warehouse_gridlock_v001`.
- First benchmark-facing instance id: `warehouse_gridlock_16x16_v001`.

## Mechanics

- The grid is 16 x 16.
- There are 32 labeled robots and 32 labeled boxes.
- One timestep is one second.
- Every robot receives one command per timestep.
- Commands are `north`, `south`, `east`, `west`, and `stay`.
- Commands form one synchronous ensemble action.
- Valid ensemble moves advance time by one second.
- Invalid ensemble attempts self-loop, move no entity, and do not advance time.
- Robots can push boxes but cannot pull, carry, rotate, or jointly push boxes.
- Concrete columns are blocked physical nodes even though visual grid nodes are
  drawn beneath them.
- Shared final occupancy and head-on swaps are invalid.
- Terminal success requires exact labeled robot targets and exact labeled box
  targets.

## Discovery And Claim Boundary

The serious MDP is treated as hidden or effectively hidden. Evaluation arms
must discover admissible state/action structure under explicit artifacted
contracts.

This environment page does not claim tower advantage, learned-policy
performance, standard gauntlet completion, or benchmark success.
