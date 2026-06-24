# Method

The runner builds a bounded generated Warehouse decision surface at each
decision point, constructs a state_collapser `PartitionTower`, queries nonempty
pointwise executable action cells, samples from a frozen rollout policy, stores
the exact candidate surface and old log probability, and later performs PPO
updates against that stored surface.
