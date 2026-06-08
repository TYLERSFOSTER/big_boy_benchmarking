# PlateSupport 5x5 Default Environment

This page is the BBB environment-readiness document for the upstream `state_collapser` PlateSupport example. It is not an evaluation readout and does not claim tower learning benefit.

## Identity

- Environment family id: `plate_support`.
- Environment instance id: `plate_support_5x5_default_v001`.
- Upstream smoke id: `plate_support_env`.
- Upstream module: `state_collapser.examples.plate_support_env`.
- Readiness run family id: `plate_support_environment_readiness_v001`.

## Contracts

- Legality contract id: `plate_support_validity_predicates_v001`.
- Reward bundle id: `plate_support_goal_self_loop_penalty_v001`.
- Action label contract id: `plate_support_action_labels_v001`.
- Default schema id: `upstream_default_plate_support_schema_v001`.
- No-contraction schema id: `no_contraction_schema_v001`.

PlateSupport states are finite plate/support configurations `(x_idx, y_idx, theta_idx, e1, e2, e3)`. A primitive action proposes a candidate state; if the candidate violates the upstream validity predicates, the transition is an invalid self-loop. If the candidate is valid but clips back to the same concrete state, BBB records that separately as a valid self-transition.

## Structural Readiness

- Candidate states: `2700`.
- Valid states: `89`.
- Reachable valid states from start: `89`.
- Primitive actions: `12`.
- Valid non-self edges: `388`.
- Invalid primitive moves: `496`.
- Valid clipped self-transitions: `184`.
- Shortest start-goal path length: `6`.
- Goal one step from start: `False`.

## Random Policy Reconnaissance

This is structural reconnaissance, not benchmark evidence.

- Episodes: `1000`.
- Success count: `24`.
- Success rate: `0.024`.
- Mean reward: `-105.748`.
- Invalid move rate: `0.45174819534621125`.

## Tower Readiness Probe

- `upstream_default_plate_support_schema_v001` mode `default`: max depth `2`, scheduled assignments `96`.
- `no_contraction_schema_v001` mode `none`: max depth `1`, scheduled assignments `0`.

## Training Surface Availability

- `ExploitExploreTrainingConfig`: `True`.
- `PlateSupportEnvRuntime`: `True`.
- `PlateSupportExploitExploreRuntime`: `True`.
- `PlateSupportLiftResolveExecutor`: `True`.
- `PlateSupportTierLearner`: `True`.
- `TowerTrainingConfig`: `True`.
- `run_exploit_explore_training`: `True`.
- `run_tower_training`: `True`.

## Claim Boundary

This environment page may support environment-readiness claims only: import health, structural graph sanity, artifact completeness, tower-shape availability, and training-surface availability. It may not claim tower control improvement, flat-versus-tower performance, or serious benchmark success.

## Artifacts

- Artifact root: `<repo-root>/docs/environments/plate_support_5x5_default_v001/readiness/dev_001`.
- Artifact index: `<repo-root>/docs/environments/plate_support_5x5_default_v001/readiness/dev_001/artifact_index.md`.
- Readout source: `<repo-root>/docs/environments/plate_support_5x5_default_v001/readiness/dev_001/readout_source.json`.

Run readiness again with:

```text
uv run python -m big_boy_benchmarking.cli plate-support readiness --artifact-root docs/environments/plate_support_5x5_default_v001/readiness/dev_001
```
