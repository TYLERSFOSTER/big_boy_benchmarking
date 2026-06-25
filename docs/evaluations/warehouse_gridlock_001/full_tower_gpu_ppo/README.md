# Warehouse Gridlock Full-Tower GPU PPO - Human Readout

![Artifacts: Complete](badges/artifacts_complete.svg)
![Behavior: PPO Smoke](badges/behavior_ppo_smoke.svg)
![Goals: Mechanics Met](badges/goals_mechanics_met.svg)
![Scope: Smoke](badges/scope_smoke.svg)
![Provenance: Repo Artifacts](badges/provenance_repo_artifacts.svg)

## Status At A Glance

- Artifact evidence: complete for the checked-in smoke run; the aggregate
  summary, run index, episode table, pointwise action surface table, PPO update
  table, tier-policy table, timing table, and selected trace index exist under
  the repo artifact root.
- Behavioral result: PPO smoke passed; the run executed real PPO update rows
  with `808` optimizer steps across
  `101` smoke episodes.
- Goal result: mechanics met; actor calls saw
  `0` empty pointwise
  executable surfaces and representative fallback count was
  `0`.
- Claim scope: smoke/readiness only; this does not claim serious GPU training
  success or Warehouse Gridlock tower superiority.
- Provenance: repo-resident source binding at `readout_source.json`, with raw
  smoke artifacts under `artifacts/tower_movie_only_100000_001`.

## Summary of Goals Behind this Evaluation

This evaluation exists to turn the Warehouse Gridlock design into a real
trainable full-tower PPO surface. The key question is not whether the tower has
won the environment yet. The key question is whether BBB can run a fair
direct/no-contraction arm and a nontrivial tower arm through the same PPO
machinery while preserving the state_collapser boundary: tower traversal is
hardcoded, actor calls see only pointwise executable tier-local action
surfaces, and execution uses strict lift candidates rather than representative
fallback.

Warehouse Gridlock is the 16x16 SVG-originated multi-robot/multi-box
environment. It is intended to model a hidden or effectively hidden admissible
state-action graph where global enumeration is not the point. The direct arm is
the no-contraction schema arm. The tower arm uses the first nontrivial
Warehouse source-local-ratio schema. Both arms share the same PPO record and
update machinery.

This smoke run is not trying to prove a robotics benchmark result, a GPU
performance result, a statistical result, or a general tower-superiority claim.
It is a mechanics/readiness run.

## Summary of Methodology Behind this Evaluation

The runner builds a bounded generated Warehouse decision surface at each
decision point. It then constructs a state_collapser `PartitionTower`, asks for
nonempty pointwise executable action cells at the current concrete state,
encodes the decision context and candidate action records, samples from a
frozen `rollout_policy_k`, stores the old log probability and exact candidate
surface, and later updates the current `policy_k` with PPO old/new-ratio
updates.

The smoke run used run label `tower_movie_only_100000_001` with direct/no-contraction and
tower/nontrivial arms, one schema seed, one replicate, one episode per arm, and
a four-second horizon. The run was intentionally small so it could verify
record contracts, old/current policy snapshots, PPO updates, repo-side
readouts, and renderable traces quickly. Larger GPU runs must be explicitly
requested with the long-run confirmation gate.

## One-Screen Verdict

The full-tower PPO machinery is wired and smoke-checked. The run produced real
PPO update rows, stored old log probabilities, wrote per-tier policy manifests,
avoided representative fallback for execution, avoided actor calls on empty
pointwise surfaces, regenerated repo-side readouts, and rendered direct and
tower episode GIFs from the selected run traces.

The result should be read as `PPO mechanics pass under a tiny CPU smoke
budget`, not as `the tower solves Warehouse Gridlock`.

## Evidence Map

- Aggregate summary:
  `artifacts/tower_movie_only_100000_001/evaluation_aggregate_summary.json`.
- Aggregate table:
  `artifacts/tower_movie_only_100000_001/evaluation_aggregate_table.csv`.
- Run index:
  `artifacts/tower_movie_only_100000_001/run_index.csv`.
- PPO updates:
  `artifacts/tower_movie_only_100000_001/results/ppo_update_summary.csv`.
- Pointwise action surfaces:
  `artifacts/tower_movie_only_100000_001/results/pointwise_action_surface_summary.csv`.
- Per-tier policies:
  `artifacts/tower_movie_only_100000_001/results/tier_policy_summary.csv`.
- Renderable selected traces:
  `artifacts/tower_movie_only_100000_001/results/trace_episode_index.csv` points at retained
  `artifacts/tower_movie_only_100000_001/traces/*/episode_*/step_events.csv` files. Full-debug
  runs also write per-run `runs/*/step_events.csv`.
- Example rendered movies:
  `movies/tower_movie_only_100000_001/`.

## What This Does Not Mean

- It does not show that a tower policy outperforms direct policy on Warehouse
  Gridlock.
- It does not show serious GPU training behavior.
- It does not show statistical significance.
- It does not establish the final model architecture for promoted benchmark
  runs.
- It does not make tower traversal trainable; traversal remains hardcoded
  state_collapser logic.

## Protocol Invocation

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/readout_source.json
```

## Claim Boundary

This is full-tower PPO system readiness and smoke/training evidence. It is not
a final broad Warehouse Gridlock benchmark claim.

## Attribution

The Warehouse Gridlock SVG environment design and the per-tier candidate
scoring PPO model family are Project Owner-originated design contributions by
Tyler Foster. Codex implemented the BBB-side engineering surface and generated
this readout.

## Clarifying Questions And Turns

_No active public clarification turns are recorded for this readout._
