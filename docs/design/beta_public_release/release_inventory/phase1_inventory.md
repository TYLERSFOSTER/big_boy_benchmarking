# Phase 1 Release Inventory

Status: initial inventory captured during execution of
`01_003_beta_public_release_readiness_implementation_workplan.md`.

## Public Entry Points

Present:

- `README.md`
- `CONTRIBUTING.md`
- `LICENSE`
- `.gitignore`
- `pyproject.toml`
- `docs/README.md`
- `docs/evaluations/README.md`
- `docs/environments/README.md`
- `docs/design/beta_public_release/README.md`

Missing or not found in the initial public-entry scan:

- `CHANGELOG.md`
- `SECURITY.md`
- `docs/design/README.md`

## Evaluation Report Roots

Primary public evaluation roots:

- `docs/evaluations/counterpoint_symbolic_v001/`
- `docs/evaluations/plate_support_5x5_default_v001/`

Observed human-readable report surfaces include:

- `docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/README.md`
- `docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/README.md`
- `docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/README.md`
- `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/README.md`
- `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/README.md`
- `docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/README.md`
- `docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/README.md`
- `docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/README.md`
- `docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/README.md`

## Artifact Weight

Initial size measurements:

| Path | Size |
| --- | ---: |
| `docs/evaluations` | 394M |
| `docs/evaluations/counterpoint_symbolic_v001` | 300M |
| `docs/evaluations/plate_support_5x5_default_v001` | 94M |

Artifact tree sizes:

| Path | Size |
| --- | ---: |
| `docs/evaluations/counterpoint_symbolic_v001/contraction_fraction_sweep_diagnostics/artifacts` | 764K |
| `docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts` | 18M |
| `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/artifacts` | 29M |
| `docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/artifacts` | 16M |
| `docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts` | 37M |
| `docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/artifacts` | 73M |
| `docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/artifacts` | 42M |
| `docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/artifacts` | 84M |
| `docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts` | 94M |

Counts:

- `docs/evaluations` contains 4435 files.
- `docs/evaluations/**/artifacts/**` contains 4207 files.
- Artifact trees contain 45 files over 1M.

## Hygiene Risk Counts

Initial scan results:

- 463 files contain machine-local absolute path strings.
- 7 files contain raw profanity or common typo variants needing public
  redaction.
- The placeholder/readout scan found generated placeholder turn pads in
  several existing readout writers and public readouts.
- Tracked byproduct found: `assets/images/.$diagrams.xml.bkp`.
- Local untracked byproducts include `.DS_Store` files and Python
  `__pycache__` directories.

## Initial Artifact Classification

Keep in git:

- public report `README.md` files;
- `result_readout.md`;
- `artifact_index.md`;
- `method.md`;
- `runbook.md`;
- `glossary.md`;
- badges;
- compact `results/*.md`;
- compact summary CSVs needed by public reports;
- root `readout_source.json` files after artifact-storage metadata is added.

Move to release asset bundle:

- nested `artifacts/**/runs/**` trees;
- nested threshold-run raw execution trees;
- event-level CSVs;
- large per-step or per-action traces;
- large generated construction JSON files;
- copied upstream run artifacts.

Investigate before moving:

- nested `artifacts/**/evaluations/**/results/*.csv` files that may be compact
  enough to keep but may also be duplicated by top-level public report tables;
- stage-level `readout_source.json` files used only as internal provenance;
- artifact manifests whose paths need release-asset mapping.

