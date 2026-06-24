<p align="left">
  <picture>
    <source srcset="assets/images/BBB_dark.png" media="(prefers-color-scheme: dark)">
    <source srcset="assets/images/BBB_light.png" media="(prefers-color-scheme: light)">
    <img src="assets/images/BBB_light.png" alt="BBB" width="395">
  </picture>
</p>

# Big Boy Benchmarking

`big_boy_benchmarking` is the official benchmarking and calibration repository
for [`state_collapser`](https://github.com/TYLERSFOSTER/state_collapser).

Current public beta component:

```text
Big Boy Calibration / Smoke
```

Future component:

```text
Benchmarking
```

This beta is source-first and public-inspection oriented. It contains working
environment surfaces, evaluation machinery, artifact contracts, human-readable
readouts, and smoke-scale calibration evidence. It does not yet claim broad
benchmark victory, statistical significance, or general tower superiority.

## Install From Source

```bash
git clone <repo-url>
cd big_boy_benchmarking
uv sync --group dev
uv run pytest
uv run python -m big_boy_benchmarking.cli --help
```

Current reports assume `state_collapser` `v0.7.2` or newer compatible
pointwise liftability semantics.

## What Is Here Now

### Environments

| Environment | Status | Public docs | What it is for |
| --- | --- | --- | --- |
| Counterpoint Symbolic v001 | Active calibration/smoke environment | [environment docs](docs/environments/counterpoint_symbolic_v001.md) | Symbolic hidden-graph and contraction-schema workbench used to develop BBB artifact, readout, liftability, and tower-training machinery. |
| PlateSupport 5x5 Default v001 | Active robotics-like calibration/smoke environment | [environment docs](docs/environments/plate_support_5x5_default_v001.md) | Constrained plate-support control surface with meaningful invalid-action behavior and a completed standard gauntlet. |
| Warehouse Gridlock v001 | Active robotics-style hidden/discovered MDP environment | [evaluation family](docs/evaluations/warehouse_gridlock_001/README.md) | SVG-originated 16x16 multi-robot/multi-box gridlock environment used to develop serious trainable policy and full-tower PPO surfaces. |

### Main Human-Readable Reports

| Report | Status | Link | Bounded conclusion |
| --- | --- | --- | --- |
| Counterpoint first serious learning | Complete structural-limit diagnostic | [README](docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/README.md) | Harness, direct baselines, artifact pipeline, and readout path work; early non-empty tower arms expose collapse/lift limitations. |
| Counterpoint noisy-rate contraction diagnostics | Complete structural diagnostic | [README](docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/README.md) | Edge-global noisy-rate schemas can avoid immediate full collapse on the widened fixture and produce inspectable candidate towers. |
| Counterpoint noisy-rate full-tower training diagnostic | Complete tower-only training-health diagnostic | [README](docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/README.md) | Selected non-collapsed candidates can be rebuilt and trained under pointwise liftability semantics; this is not a direct comparison. |
| Counterpoint second serious schema comparison | Complete bounded comparison surface | [README](docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/README.md) | Matched Schema 0 versus Schema 1 comparison works; current evidence is narrow and calibration-scale. |
| Counterpoint threshold frontier probe | Complete next-measure probe | [README](docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/README.md) | Threshold sweeps expose a small Schema 1 margin pattern, not broad dominance. |
| Counterpoint small paired replicate probe | Complete next-measure probe | [README](docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/README.md) | Seed-paired machinery works and records a weak positive Schema 1 margin pattern; not statistical significance. |
| PlateSupport standard gauntlet | Complete correction gauntlet with bounded positive smoke signal | [README](docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/README.md) | The selected iterated tower candidate beat the direct baseline on the calibrated binary-success target and showed a coherent action-filtering signal. |
| PlateSupport direct-star cul-de-sac control | Complete diagnostic control | [README](docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/README.md) | Abdul Malik's cul-de-sac concern is tested by adding one-step guarded direct controls beside the selected tower candidate. |
| PlateSupport tower-star guarded lift comparison | Complete diagnostic control with inconclusive smoke result | [README](docs/evaluations/plate_support_5x5_default_v001/tower_star/README.md) | Direct-star and tower-star controls are both implemented; the first smoke run is tied on the primary target and does not resolve a tower advantage. |
| Warehouse full-tower GPU PPO | Complete CPU smoke for full-tower PPO machinery | [README](docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/README.md) | Direct/no-contraction and tower/nontrivial arms share PPO machinery with real optimizer updates and renderable traces; no serious GPU benchmark claim yet. |

The full evaluation index is in [docs/evaluations/README.md](docs/evaluations/README.md).

## Current Conclusions

Supported by the checked-in readouts:

- BBB can build repo-resident artifacts, summaries, badges, and human-readable
  reports for nontrivial `state_collapser` downstream environments.
- Counterpoint established the artifact/readout/tower-control workflow and
  exposed real integration issues, including pointwise liftability.
- PlateSupport now provides the clearest calibration/smoke signal: in the
  standard gauntlet correction run, the selected tower arm hit the calibrated
  target more often than direct, had much better mean reward, and made zero
  invalid concrete moves while direct made many invalid moves.
- Follow-up PlateSupport control diagnostics now separate the Abdul Malik
  cul-de-sac concern from the original positive smoke result. The first
  tower-star guarded-lift smoke run is correctly bounded as inconclusive, not
  as a new positive tower claim.
- Warehouse Gridlock now has a full-tower PPO mechanics surface: direct as
  no-contraction schema, tower as nontrivial schema, per-tier `policy_k` /
  `rollout_policy_k`, stored old log probabilities, strict pointwise
  executable lifts, and renderable smoke traces.
- The current evidence is strong enough to justify further benchmark design.

Not supported yet:

- general tower superiority;
- final robotics benchmark claims;
- statistical significance across large budgets;
- tensor-enabled or GPU performance claims;
- serious Warehouse Gridlock PPO benchmark claims;
- PyPI release stability;
- broad claims beyond the exact checked-in environments, budgets, and
  readouts.

## Artifact Policy

Human-readable reports and compact summaries live in git. Large raw run trees
and event-level artifacts have been externalized to a local release-asset
bundle for the `v0.1.0-beta.1` public beta.

Bundle metadata is tracked in
[docs/design/beta_public_release/release_asset_manifests](docs/design/beta_public_release/release_asset_manifests/):

- asset name: `big_boy_calibration_smoke_v0.1.0-beta.1_artifacts.tar.zst`;
- checksum: `b0fd6be1d30abaad25d5a02a308a44d6f52e3ac409c99f735150d408b94d4090`;
- raw artifact file count: 4,207.

When inspecting a report, start with its checked-in `readout_source.json`.
Durable human readouts are generated with the explicit protocol-file command:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/<environment>/<evaluation>/readout_source.json
```

## Workflow

BBB uses a three-step workflow:

1. Design and build an environment.
2. Design and build evaluations or gauntlets for that environment.
3. Convert machine-readable artifact tables into human-readable repo reports.

Key protocol folders:

- [docs/prime_directive](docs/prime_directive/): operational protocols for
  Codex/engineer collaboration.
- [docs/design](docs/design/): open-lab design history, blueprints, workplans,
  and implementation logs.
- [docs/environments](docs/environments/): environment descriptions and
  readiness docs.
- [docs/evaluations](docs/evaluations/): human-readable evaluation reports.
- [docs/engineer_continuity](docs/engineer_continuity/): continuity reports
  and handoff notes.

## Development Commands

```bash
uv sync --group dev
uv run pytest
uv run python -m big_boy_benchmarking.cli validate-contracts
uv run python scripts/release_hygiene.py --repo-root .
```

The future installed command name `bbb` is reserved. The stable beta entry
point is currently:

```bash
uv run python -m big_boy_benchmarking.cli
```

## Release Status

This branch is preparing the initial public beta:

```text
v0.1.0-beta.1
```

Release notes, governance files, CI, and artifact-bundle manifests are part of
the beta-readiness work. Tagging, publishing, uploading release assets, making
the GitHub repository public, and publishing to PyPI are separate release
actions and are not implied by this README.
