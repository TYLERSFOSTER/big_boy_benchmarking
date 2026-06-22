# Big Boy Benchmarking Continuity Report

Date: 2026-06-22

Repository:

```text
<repo-root>
```

Previous continuity checkpoint:

```text
docs/engineer_continuity/2026/06/07/2026-06-07_post_pointwise_liftability_counterpoint_and_plate_support_gauntlet_continuity.md
```

This report covers the work from immediately after the 2026-06-07 continuity
report through the current pause after Tyler Foster's RL-training study notes.

At report creation, the repo was on `main` and synchronized with `origin/main`
before this new report file was created:

```text
## main...origin/main
```

## Executive Summary

Since the 2026-06-07 checkpoint, the project moved through five major arcs:

1. Public beta readiness and release framing for `v0.1.0-beta.1`.
2. PlateSupport follow-up controls motivated by Abdul Malik's cul-de-sac /
   self-loop concern.
3. A new PO-authored SVG-to-environment workflow, producing Warehouse Gridlock
   001 as a first-class BBB environment.
4. Warehouse Gridlock evaluation work, including a fair masked direct vs
   live-lift tower diagnostic, a corrected trainable full-state/full-action
   policy contract, and a first transformer actor-critic smoke path.
5. A conceptual pause for RL-training study, producing:

```text
docs/mathematical_notes_on_RL_training.md
```

The most important current strategic shift is that the repo is no longer only
about Counterpoint and PlateSupport calibration. It now has an emerging third
environment line, Warehouse Gridlock, intended to expose large coordinated
robotics-style discovery problems where direct-vs-tower differences may be
larger than the small Counterpoint margins.

The most important caution is that the Warehouse Gridlock transformer path is
only a first smoke implementation. It proves that a real neural
actor-critic-style optimizer path can run and artifact itself; it does not yet
settle how state-collapser tower training should work at lower tiers, nor does
it prove a tower performance claim.

## Attribution Ledger

### Tyler Foster / Project Owner

Tyler Foster drove the central project direction throughout this interval:

- framed the public beta as `Big Boy Calibration / Smoke`, with later
  `Benchmarking` as the next component;
- corrected release-note language so the public release was not described as a
  draft after publication;
- accepted Abdul Malik's PlateSupport concern and directed BBB-side diagnostic
  controls;
- authored the Warehouse Gridlock physical-system drawings;
- clarified Warehouse timing, synchronous ensemble control, hidden-admissible
  MDP framing, discovery fairness, and cross-tier discovery-pressure
  hypotheses;
- identified that the first Warehouse "training" path was not a real learning
  model in the needed sense;
- specified the corrected policy contract:

```text
full system configuration + current second -> full simultaneous action vector
```

- pushed the policy path toward transformer/actor-critic learning;
- paused implementation work to study RL training; and
- authored the final conceptual synthesis in
  `docs/mathematical_notes_on_RL_training.md`.

The RL notes' mathematical framing, corrections, and final synthesis are
Tyler's. ChatGPT was used as a conversational assistant for candidate
explanations, formulas, and background connections.

### Abdul Malik / Project PM

Abdul Malik made the key PlateSupport observation that changed the interpretation
of the previous positive smoke result:

```text
I think avoiding self-loops here is the reason why.
```

As relayed and refined by Tyler, Abdul's concern was that the PlateSupport tower
arm might have avoided cul-de-sacs because of liftability/executability
filtering, while the direct arm was allowed to waste effort on invalid or
self-looping regions. This led to the direct-star and tower-star diagnostic
controls.

This attribution matters: the PlateSupport control work is not a random Codex
expansion. It is a direct response to Abdul's PM-level critique, accepted and
directed by Tyler.

### ChatGPT / External Study Assistant

The RL-training study note was developed through an extended Tyler Foster /
ChatGPT conversation. The attached attribution note says:

```text
This note grew out of an extended interactive study session between Tyler
Foster and ChatGPT. The mathematical framing, corrections, and final synthesis
are Tyler Foster's; ChatGPT was used as a conversational assistant for
generating candidate explanations, formulas, and background connections.
```

ChatGPT supplied standard reinforcement-learning formulas, terminology, partial
derivations, and background connections around policy gradients, advantage
estimation, TRPO, PPO, mirror descent, KL geometry, and path-measure language.
The final viewpoint should be attributed primarily to Tyler Foster's
mathematical interpretation and synthesis.

### Codex

Codex implemented repo changes, generated readout surfaces, wrote implementation
logs, helped patch markdown rendering in the RL notes, and translated
PO-authored design material into blueprints/workplans/code where instructed.
Codex should not claim authorship of:

- Tyler's RL mathematical synthesis;
- Tyler's SVG environment designs;
- Abdul's PlateSupport critique;
- Tyler's PO decisions in design docs.

## Public Beta Readiness And Release

### Release Framing

The beta-public-release design work lives under:

```text
docs/design/beta_public_release/
```

The public framing settled on:

```text
Current component: Big Boy Calibration / Smoke
Future component: Benchmarking
```

The repository is positioned as the official benchmarking and calibration repo
for `state_collapser`, separate from the `state_collapser` source repo but
linked conceptually to it.

### Release Assets

The release work externalized raw artifact trees from git into a release asset:

```text
big_boy_calibration_smoke_v0.1.0-beta.1_artifacts.tar.zst
```

Relevant metadata:

```text
docs/design/beta_public_release/release_asset_manifests/ARTIFACT_BUNDLE_MANIFEST.json
docs/design/beta_public_release/release_asset_manifests/ARTIFACT_BUNDLE_FILE_INDEX.csv
docs/design/beta_public_release/release_asset_manifests/ARTIFACT_BUNDLE_README.md
docs/design/beta_public_release/release_asset_manifests/SHA256SUMS.txt
```

The bundle preserves artifact trees at repo-relative paths such as:

```text
docs/evaluations/.../artifacts/...
```

Bundle facts recorded in the manifest README:

```text
artifact roots: 9
files: 4207
raw bytes before compression: 400304242
bundle SHA256: b0fd6be1d30abaad25d5a02a308a44d6f52e3ac409c99f735150d408b94d4090
```

GitHub release-asset constraints were checked against GitHub Docs on
2026-06-08; the bundle was about 12.5 MiB and well inside the documented
per-file limit.

### Release Hygiene Tooling

The public-beta work added:

```text
scripts/release_hygiene.py
tests/test_release_hygiene.py
```

The script checks for tracked local/build byproducts, large tracked artifacts,
machine-local absolute paths in public surfaces, public profanity/redaction
requirements, generated readout placeholders, and ambiguous artifact-table
readout command forms.

The root docs were reframed around bounded calibration/smoke evidence rather
than benchmark-strength claims.

### Release-Note Correction

There was a high-stress release-tail correction. The public-facing problem was
that release notes still contained draft/status language inappropriate for an
already published release. Tyler provided the intended release-note wording and
insisted the public release record not describe itself as a draft.

Current release note file:

```text
docs/design/beta_public_release/v0.1.0-beta.1_release_notes_draft.md
```

Despite the filename containing `draft`, the file content now begins:

```text
# v0.1.0-beta.1 Release Notes
```

and describes the release as a source-first public beta, not a draft review
artifact.

The tag recorded in git history is:

```text
v0.1.0-beta.1 -> ad03860 prepare v0.1.0-beta.1 public beta release
```

## PlateSupport Control Work After Abdul's Catch

The 2026-06-07 report ended with the PlateSupport standard gauntlet as the
strongest positive smoke signal:

```text
selected tower target hits: 25 / 128
direct baseline target hits: 15 / 128
selected tower mean reward: -27.2109375
direct baseline mean reward: -78.71875
selected tower invalid moves: 0
direct baseline invalid moves: 2142
```

After that report, Abdul Malik raised the self-loop / cul-de-sac concern.
Tyler accepted it as important and directed follow-up diagnostics.

### Direct-Star Cul-de-sac Control

Design folder:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/09_direct_star_culdesac_control/
```

Readout:

```text
docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/README.md
```

Implementation package:

```text
src/big_boy_benchmarking/environments/plate_support/direct_star_culdesac_control/
```

Test file:

```text
tests/environments/plate_support/test_direct_star_culdesac_control.py
```

The direct-star diagnostic compared:

- `direct_raw`;
- `direct_invalid_guard`;
- `direct_nonself_guard`;
- `tower_selected_candidate`.

The important result:

| Arm | Target Hit Rate | Mean Reward | Invalid Rate | Self-Transition Rate |
| --- | ---: | ---: | ---: | ---: |
| `direct_raw` | 0.1171875 | -78.71875 | 0.3559913578195114 | 0.4631876350340701 |
| `direct_invalid_guard` | 0.359375 | -17.1640625 | 0.0 | 0.16553199766582377 |
| `direct_nonself_guard` | 0.515625 | 18.78125 | 0.0 | 0.0 |
| `tower_selected_candidate` | 0.1953125 | -27.2109375 | 0.0 | 0.0 |

Interpretation:

```text
validity_filtering_explains_signal
```

This materially changed the PlateSupport interpretation. The tower still beat
raw direct, but guarded direct controls beat the tower. The old positive signal
was therefore not clean evidence of tower hierarchy beating an equivalent
direct decision surface.

Allowed claim:

```text
ordinary one-step validity filtering explains most of the original tower signal
```

Blocked claim:

```text
tower hierarchy beat direct learning on an equivalent decision surface
```

### Tower-Star Guarded Lift Comparison

Tyler then clarified that if direct was starred, the tower side also needed a
corresponding starred control. The tower-star comparison filters concrete lift
candidates inside tower action cells before tower action-cell selection.

Design folder:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/10_tower_star/
```

Readout:

```text
docs/evaluations/plate_support_5x5_default_v001/tower_star/README.md
```

Implementation package:

```text
src/big_boy_benchmarking/environments/plate_support/tower_star/
```

Test file:

```text
tests/environments/plate_support/test_tower_star.py
```

The six arms:

- `direct_raw`;
- `direct_invalid_guard`;
- `direct_nonself_guard`;
- `tower_lift_executable_current`;
- `tower_invalid_guard`;
- `tower_nonself_guard`.

First smoke result:

```text
run label: tower_star_001
primary interpretation: inconclusive_small_margin
primary comparison: direct_nonself_guard versus tower_nonself_guard
primary target delta: 0.0
```

Readout table:

| Arm | Target Hit Rate | Mean Reward | Invalid Rate | Self-Transition Rate |
| --- | ---: | ---: | ---: | ---: |
| `direct_raw` | 0.0 | -97.0 | 0.44 | 0.47 |
| `direct_invalid_guard` | 0.0 | -61.0 | 0.0 | 0.11 |
| `direct_nonself_guard` | 0.0 | -50.0 | 0.0 | 0.0 |
| `tower_lift_executable_current` | 0.0 | -50.0 | 0.0 | 0.0 |
| `tower_invalid_guard` | 0.0 | -50.0 | 0.0 | 0.0 |
| `tower_nonself_guard` | 0.0 | -50.0 | 0.0 | 0.0 |

Interpretation:

- Primary target metric tied.
- Reward profile tied between `direct_nonself_guard` and tower arms.
- Result leans away from the stronger previous PlateSupport tower-positive
  claim and toward Abdul's cul-de-sac/control explanation.
- It does not refute tower; it says this smoke run does not separate tower from
  a properly nonself-guarded direct control.

## SVG Physical-System Workflow And Warehouse Gridlock

Tyler introduced a new intended workflow: the Project Owner draws SVG diagrams
of physical systems, and BBB turns them into professional finite benchmark
environments.

The first design line is:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/
```

Source design note:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md
```

PO-authored drawing assets:

```text
assets/environment_designs/gridlock_001_start.svg
assets/environment_designs/gridlock_001_end.svg
assets/environment_designs/gridlock_001_moves_001.svg
assets/environment_designs/gridlock_001_moves_002.svg
```

Codex translated those drawings into surrounding environment-contract text and
then into implementation artifacts, but Tyler authored the physical design
itself.

### PO-Locked Mechanics

Tyler clarified:

- one environment timestep is one second;
- every robot chooses one primitive command per timestep;
- each robot can move one graph step or stay;
- robot commands form one synchronous ensemble move;
- an ensemble is invalid if any two entities, robot or box, would occupy the
  same node;
- invalid ensembles do not consume one second;
- no partial execution occurs;
- if any part of the ensemble is invalid, no robot or box moves;
- reward constants are:
  - terminal success: `1000.0`;
  - elapsed time: `-1.0/sec`;
  - correct box: `1.0`;
  - correct robot: `1.0`;
  - invalid penalty: `0.0`;
- column manifest authority is manual from the PO drawing, with optional helper
  inspection.

### Hidden-Admissible MDP Framing

Tyler also clarified that the real-life MDP should be treated as hidden or
effectively hidden. Even if a toy finite instance is enumerable in principle,
the serious admissible-state graph should not be assumed known.

This implies:

- discovery is central to every arm;
- admissibility information must be carefully budgeted, cached, and reported;
- no arm should receive an uncharged full transition graph;
- tower wins should not be credited as hierarchy wins if they are merely free
  admissibility masks;
- the positive target is that tower structure may help discover useful
  large-scale structure within the same discovery budget direct receives.

Tyler also identified a future idea: lower-tier pressure to "discover here"
may need to propagate upward when an exploration need is visible locally but
not obvious at an abstract tier. This is retained as a future hypothesis, not
implemented in current Warehouse arms.

## Warehouse Gridlock Environment Readiness

Design/workplan/log:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_001_warehouse_gridlock_environment_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_002_warehouse_gridlock_environment_implementation_workplan.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_003_warehouse_gridlock_environment_implementation_log.md
```

Implementation package:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/
```

Environment docs:

```text
docs/environments/warehouse_gridlock_001/README.md
docs/environments/warehouse_gridlock_001/manifests/warehouse_gridlock_16x16_v001.json
```

Readiness readout:

```text
docs/evaluations/warehouse_gridlock_001/environment_readiness/README.md
```

Core instance facts:

```text
environment family id: warehouse_gridlock_001
instance id: warehouse_gridlock_16x16_v001
robots: 32
boxes: 32
visual grid nodes: 256
traversable nodes: 251
directed traversable edges: 920
blocked concrete columns: 5
```

The environment implementation includes graph, state, actions, collisions,
transition, rewards, discovery, manifests, instances, validation, docs, runner,
replay, and CLI surfaces.

Important resolved implementation issues:

- Warehouse test modules were renamed to unique basenames to avoid pytest
  import-mismatch collisions with Counterpoint tests.
- `readiness-docs` was corrected so it does not erase transition-smoke rows
  when rerun on an existing artifact root.
- The environment-readiness surface makes no tower, gauntlet, learning, or
  benchmark-performance claim.

Verification recorded in the implementation log:

```text
uv run pytest tests/environments/warehouse_gridlock
15 passed

uv run pytest tests/environments
255 passed
```

## Warehouse Masked Direct Vs Live-Lift Tower Diagnostic

Design folder:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_masked_direct_vs_live_lift_tower_no_lookahead/
```

Readout:

```text
docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/README.md
```

Implementation package:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/
```

This diagnostic compared:

- `warehouse_direct_admissible_masked`;
- `warehouse_tower_live_lift_masked`.

Key fairness rules:

- both arms use immediate inadmissibility masking over the generated candidate
  set;
- neither arm receives Abdul-style one-hop successor-state cul-de-sac lookahead;
- the tower uses live state-lift hygiene only: after a downstairs state is
  fixed, it does not lift to an upstairs representative with empty generated
  `Out`;
- the direct arm is not given a stronger direct-star guard in this evaluation;
- the tower arm is not given tower-star one-hop action filtering here.

The first meaningful run was:

```text
run label: masked_8ep_001
episodes: 8 per arm per replicate
replicates: 2 per arm
schema seeds: 1
horizon: 128 seconds per episode
candidate proposals per step: 256
max active robots: 8
candidate mix: coordination_ready_sparse_interleaved_v001
```

Result:

```text
direct mean reward: 379.9375
tower mean reward: 379.9375
terminal successes: 0 for both arms
mean final correct boxes: 0.0 for both arms
mean final correct robots: 6.1875 for both arms
selected valid steps: 128 per episode for both arms
```

Interpretation:

- clean tie;
- fairness/no-lookahead audits passed;
- no live-lift failures;
- candidate surface now includes multi-robot proposals;
- no tower advantage shown;
- no Warehouse solution shown.

Important correction made during this work:

The initial smoke implementation was too weak because its bounded candidate
generator exposed mostly `all_stay` and one-active-robot actions. It was
replaced with a coordination-ready sparse interleaved generator that includes
one-active, two-active, three-active, and larger multi-active proposals up to a
configurable max active robot count.

The CLI progress surface was also added:

- `tqdm` progress on stderr;
- final JSON remains on stdout;
- `progress_events.jsonl` is persisted inside the artifact root;
- knobs include `--progress-every-episodes` and `--no-progress`.

## Warehouse Full-State Full-Action Trainable Policy Contract

Design folder:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/02_full_state_full_action_trainable_policy_contract/
```

Readout:

```text
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/README.md
```

Implementation packages:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/policies/
src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/
```

Test file:

```text
tests/environments/warehouse_gridlock/test_full_state_policy_contract.py
```

This work happened because Tyler noticed that the previous Warehouse "training"
commands were misleading. The model was not a sufficiently realistic trainable
policy; it was effectively learning over proposal/candidate identifiers rather
than learning a reusable map from full state and time to full action vector.

Tyler's locked model contract:

```text
full system configuration + current second -> full simultaneous action vector
```

Implemented smoke policy family:

```text
warehouse_linear_factorized_softmax_policy_v001
```

This is trainable and reusable, but it is not neural backprop.

Arms:

- `warehouse_direct_full_state_policy_masked`;
- `warehouse_tower_full_state_policy_live_lift_masked`.

The tower arm reuses the scoped generated/discovered tower surface and live
state-lift hygiene, but scores concrete realizations through reusable feature
weights rather than opaque candidate IDs.

Verification recorded:

```text
uv run pytest tests/environments/warehouse_gridlock
28 passed
```

Smoke run:

```text
run label: policy_contract_smoke_001
episodes per arm: 4
replicates per arm: 1
schema seeds: 1
max seconds per episode: 128
projection attempt budget: 64
```

Learning-health gate:

```text
warehouse_direct_full_state_policy_masked:
  update_count: 512
  non_noop_update_count: 512
  nonzero_prior_signal_decision_count: 511
  learning_status: real_learning_signal_present

warehouse_tower_full_state_policy_live_lift_masked:
  update_count: 512
  non_noop_update_count: 512
  nonzero_prior_signal_decision_count: 511
  learning_status: real_learning_signal_present
```

Claim boundary:

- may claim corrected policy contract exists and smoke learning-health passed;
- may not claim backprop happened;
- may not claim Warehouse is solved;
- may not claim tower is generally better;
- may not claim full MDP enumeration.

## Warehouse Transformer Policy Upgrade

Design folder:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/03_transformer_policy_model_upgrade/
```

Readout:

```text
docs/evaluations/warehouse_gridlock_001/transformer_policy/README.md
```

Implementation package:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/transformer_policy/
```

Script:

```text
scripts/run_warehouse_gridlock_tower_transformer_curriculum_train.sh
```

Test file:

```text
tests/environments/warehouse_gridlock/test_transformer_policy.py
```

This upgrade was started after Tyler realized that the full-state policy path
still was not the deep-learning style model needed for serious training. The
transformer path adds:

- optional Torch runtime detection;
- `warehouse_transformer_actor_critic_policy_v001`;
- token encodings for global context, robots, boxes, blocked columns, and
  tower context;
- actor-critic output with log probabilities, entropy, and value;
- discounted returns and advantage computation;
- AdamW optimizer steps and gradient clipping;
- curriculum over episode horizon;
- checkpoints;
- selected trace retention;
- renderable selected traces without writing global all-episode CSVs.

Torch was initially unavailable; after approval, optional ML dependencies were
installed:

```text
uv sync --extra ml --group dev
torch==2.12.0
```

Smoke verification:

```text
uv run pytest tests/environments/warehouse_gridlock -q
32 passed, 1 skipped

uv run pytest tests/environments/warehouse_gridlock/test_transformer_policy.py -q
3 passed, 1 skipped
```

Tiny transformer smoke:

```text
run label: tower_transformer_smoke_001
episodes: 2
replicates: 1
schema seeds: 1
max seconds start/end: 2 -> 4
optimizer_steps: 2
selected trace count: 2
```

The transformer smoke produced:

- `evaluation_manifest.json`;
- `dependency_manifest.json`;
- model and optimizer manifests;
- policy contract manifest;
- checkpoint summary;
- curriculum summary;
- trace episode index;
- artifact retention summary;
- `readout_source.json`;
- a lightweight README.

Important limitation:

The transformer implementation is real in the sense that optimizer steps occur,
but it is still a smoke slice. It does not settle how a full state-collapser
tower should train policies at lower tiers, and no long 512, 2024, or 100000
episode transformer training run was executed as a completed benchmark result.

## Artifact Growth And Movie/Trace Lessons

During Warehouse training experiments, all-episode CSV traces began to grow
quickly and caused confusion around movie rendering. The transformer upgrade
therefore changed the retention model:

- selected traces are written under per-episode trace folders;
- `results/trace_episode_index.csv` records retained episodes;
- render commands use the selected trace index;
- missing trace requests return structured JSON errors and rerun hints;
- no global all-episode `step_events.csv` is required for transformer rendering.

This matters for future serious Warehouse runs. Long training runs should use
explicit trace-retention settings rather than writing every step of every
episode by default.

## RL Training Study Notes

The current pause was used for Tyler's study of RL training. The result is:

```text
docs/mathematical_notes_on_RL_training.md
```

The note now has sections:

- `1. Entropy, Surprise, and KL Divergence`;
- `2. Surprise as the Lie algebra "*mass decay rate of repeating events*"`;
- `3. RL training frameworks`;
- `3.1 Shared value and advantage`;
- `3.2 REINFORCE`;
- `3.3 TRPO: Trust Region Policy Optimization`;
- `3.4 PPO: Proximal Policy Optimization`.

Core conceptual content, per the attached attribution note:

- probability weights as positive multiplicative objects;
- distinction between additive velocity, multiplicative velocity, and
  Lie-algebra-valued relative velocity;
- logarithms should not appear merely as formal computational tricks;
- `d log P` should be understood as an algebraic/logarithmic differential such
  as `dP/P`, not as requiring a globally defined logarithm;
- multiplicative differentiation should be formulated base-independently;
- policy-gradient terms such as
  `\nabla_\theta\log \pi_\theta(a\mid s)` are infinitesimal multiplicative
  changes of probability mass;
- REINFORCE, TRPO, and PPO can be framed via expectation functionals, advantage
  functions, likelihood ratios, and KL-controlled policy motion.

Codex later made GitHub-rendering cleanup edits:

- converted display math to fenced `math` blocks;
- replaced raw `<`/`>` in math with `\lt`/`\gt`;
- replaced inline conditioning bars with `\mid`;
- cleaned malformed bracket/control-space forms near the RL section;
- fixed the table of contents to match actual headings.

These cleanup edits are formatting/rendering support. They do not change the
attribution of the mathematical framing.

## Current Repo State By Subsystem

### Counterpoint

Counterpoint remains the original calibration environment and the source of
much of the artifact/readout machinery. No new major Counterpoint implementation
arc happened after the 2026-06-07 report. It remains important background, but
current active design pressure shifted first to PlateSupport controls, then to
Warehouse.

### PlateSupport

PlateSupport now has:

- standard gauntlet with bounded positive smoke result;
- direct-star diagnostic showing one-step filtering explains much of that
  signal;
- tower-star diagnostic showing a tied/inconclusive first starred comparison.

The correct current claim is not "PlateSupport proves tower superiority." The
correct claim is that PlateSupport is a productive calibration environment and
has already exposed a real interpretation confound that Abdul caught.

### Warehouse Gridlock

Warehouse now has:

- PO-authored SVG design source;
- professional environment design docs;
- full environment-readiness implementation;
- readiness artifacts/readout;
- first fair masked direct vs live-lift tower diagnostic;
- corrected full-state/full-action trainable policy contract;
- first transformer actor-critic smoke machinery;
- trace-retention/movie machinery for selected episodes.

The correct current claim is not "Warehouse benchmark works." The correct
claim is that Warehouse is now the promising serious environment line for
larger coordination/discovery experiments, but tower-training semantics still
need careful conceptual and implementation design.

### Public Beta

The public beta is framed as source-first calibration/smoke. It has release
hygiene tooling, artifact externalization, and release assets. It is not a
final benchmark suite.

## Important Open Questions And Next Work

### 1. State-Collapser Semantics For Full Tower Training

The most important unresolved conceptual issue is how full-tower training should
work when the policy model is a transformer over full system configurations.
The current transformer smoke can score concrete vectors and can include tower
context, but that is not yet the same as a principled multi-tier
state-collapser learning architecture.

Tyler explicitly paused before proceeding further because the system-level
conceptual model needed to be clarified.

### 2. Warehouse Serious Run Design

The next serious Warehouse run should not simply scale the old non-neural or
candidate-id keyed setup. It should use the corrected full-state/full-action
and/or transformer machinery, with explicit trace retention, curriculum, and
claim boundaries.

Before a long run:

- decide whether the run is tower-only training-health, paired direct/tower, or
  architecture smoke;
- decide trace-retention policy;
- decide checkpoint/resume expectations;
- decide whether direct and tower receive identical transformer architectures
  or different context surfaces;
- decide how lower-tier policies are represented, trained, and composed.

### 3. PlateSupport Interpretation

PlateSupport remains useful, but after direct-star and tower-star controls, the
original positive gauntlet result must be cited carefully. The direct-star
result strongly supports Abdul's concern. The tower-star result does not recover
a positive tower-specific signal at smoke scale.

### 4. Documentation Freshness

Root docs were updated during public beta and PlateSupport control work, but
Warehouse and transformer work moved quickly. Future root/README updates should
avoid claiming Warehouse benchmark evidence before there is a real serious run.

### 5. Release Hygiene

Release hygiene exists and should be run before public-facing updates:

```text
uv run python scripts/release_hygiene.py --repo-root .
```

Some older surfaces have previously contained placeholders or machine-local
path issues; check the current script result before any next release.

## Commands And Protocols To Remember

Human-readable report regeneration uses the exact protocol-file target:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/<environment>/<evaluation>/readout_source.json
```

Warehouse transformer readout target:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/transformer_policy/readout_source.json
```

Warehouse full-state policy readout target:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/readout_source.json
```

PlateSupport direct-star readout target:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json
```

PlateSupport tower-star readout target:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/plate_support_5x5_default_v001/tower_star/readout_source.json
```

## What A Future Engineer Should Not Do

Do not:

- treat Tyler's RL notes as Codex-authored mathematical work;
- treat ChatGPT's role in the RL study as primary authorship;
- treat Abdul's cul-de-sac observation as a Codex-generated concern;
- treat the original PlateSupport gauntlet as an unqualified tower win;
- treat direct-star or tower-star as final robotics benchmark results;
- treat Warehouse masked-direct/live-lift tied smoke as a negative theorem;
- run huge Warehouse training without explicit trace-retention settings;
- describe the transformer smoke as benchmark-strength evidence;
- assume full lower-tier tower training semantics are already solved;
- invent Project Owner turns in blueprints or continuity reports;
- point the artifact-table readout protocol at a README or raw artifact folder
  when the correct target is the repo-side `readout_source.json`.

## Current Handoff Summary

The project is ready to resume from a clearer RL-training conceptual basis.

The immediate context is:

- public beta v0.1.0-beta.1 exists as calibration/smoke framing;
- PlateSupport's earlier positive signal has been properly challenged by
  Abdul-inspired controls;
- Warehouse Gridlock is now implemented and is the main promising environment
  for a larger coordination/discovery benchmark;
- the current Warehouse learning stack has progressed from nonlearning-like
  candidate updates to a full-state/full-action linear policy and then to a
  transformer actor-critic smoke path;
- Tyler's RL notes provide the conceptual bridge for understanding policy
  gradients as infinitesimal multiplicative changes of probability mass.

The next high-quality move is probably not another blind long run. It is to
decide, in light of the RL notes, what the state-collapser tower-learning
architecture should mean for a full transformer-style Warehouse policy.
