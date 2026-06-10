# Method

Warehouse Gridlock readiness loads the full PO drawing manifest, generates the 16x16 cardinal grid, removes the five concrete-column nodes and incident edges, validates start and target states, and runs representative transition-smoke cases. The action surface is structured ensemble control; full flat action enumeration is forbidden.

Collision policy: `warehouse_gridlock_collision_node_and_head_on_v001`.
Transition policy: `warehouse_gridlock_synchronous_push_v001`.
Discovery policy: `warehouse_gridlock_discovery_per_run_per_arm_v001`.
