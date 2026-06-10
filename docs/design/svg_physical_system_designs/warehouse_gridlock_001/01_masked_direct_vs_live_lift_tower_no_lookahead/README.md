# Warehouse Gridlock Masked Direct vs Live-Lift Tower

This folder designs the first Warehouse Gridlock direct-versus-tower diagnostic
comparison after the environment-readiness slice.

The intended comparison is:

```text
direct arm:
  immediate inadmissible ensemble actions are masked
  no one-step successor cul-de-sac lookahead

tower arm:
  immediate inadmissible tower/current actions are masked
  state lifts avoid upstairs states with empty Out
  no one-step successor cul-de-sac lookahead
```

The blueprint is:

```text
01_001_warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_blueprint.md
```

