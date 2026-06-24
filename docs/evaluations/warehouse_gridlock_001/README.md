# Warehouse Gridlock v001

Warehouse Gridlock is the SVG-originated multi-robot/multi-box environment
designed by Tyler Foster for hidden/discovered state-action graph benchmark
work. The environment is intentionally hard to enumerate globally: useful
arms must work from discovered admissible surfaces rather than pretending the
full MDP is cheaply known.

## Evaluation Surfaces

| Evaluation | Status | Readout | Bounded interpretation |
| --- | --- | --- | --- |
| environment readiness | Complete | [README](environment_readiness/README.md) | The 16x16 Warehouse instance, manifest, transitions, rewards, and replay surface exist. |
| masked direct vs live-lift tower | Complete smoke/control surface | [README](masked_direct_vs_live_lift_tower/README.md) | Both arms mask inadmissible actions; tower additionally uses pointwise live-lift state filtering. |
| full-state policy comparison | Complete policy-contract smoke | [README](full_state_policy_comparison/README.md) | Establishes full-state/full-action trainable policy plumbing and replayable traces. |
| transformer policy | Complete transformer-policy smoke | [README](transformer_policy/README.md) | Establishes transformer policy mechanics and selected trace retention. |
| full-tower GPU PPO | Complete CPU smoke | [README](full_tower_gpu_ppo/README.md) | Direct/no-contraction and tower/nontrivial arms use shared PPO machinery with real optimizer updates; no serious GPU benchmark claim yet. |

## Current Next Step

The newest surface is `full_tower_gpu_ppo`. It should be treated as a
mechanics/readiness result: PPO updates, pointwise liftability, no learned
tower traversal, strict executable lifts, repo readouts, and renderable traces
are now wired. Larger GPU training runs remain Project Owner-initiated future
work.
