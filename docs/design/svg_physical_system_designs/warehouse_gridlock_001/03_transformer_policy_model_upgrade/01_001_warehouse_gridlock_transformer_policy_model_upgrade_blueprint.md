# Warehouse Gridlock Transformer Policy Model Upgrade Blueprint

## Document Status

This is the initial implementation blueprint for upgrading the Warehouse Gridlock
full-state/full-action trainable policy surface from the current linear
factorized learner to a transformer-backed trainable learner.

This document is design-only. It does not authorize unrelated environment
changes, reward changes, comparison-claim changes, or `state_collapser` package
changes.

## Source Documents And Attribution

Primary local design source:

- `docs/design/svg_physical_system_designs/warehouse_gridlock_001/03_transformer_policy_model_upgrade/design_discussion.md`

Prior Warehouse Gridlock design source:

- `docs/design/svg_physical_system_designs/warehouse_gridlock_001/02_full_state_full_action_trainable_policy_contract/01_001_warehouse_gridlock_full_state_full_action_trainable_policy_contract_blueprint.md`

Relevant implemented surfaces:

- `src/big_boy_benchmarking/environments/warehouse_gridlock/policies/contracts.py`
- `src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/`
- `src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/`

Relevant `state_collapser` context reviewed:

- `<state_collapser-repo>/docs/usage/01_005_using_your_own_training_loop.md`
- `<state_collapser-repo>/docs/usage/01_010_tensorization_boundary.md`
- `<state_collapser-repo>/docs/api_notes/tensorization_boundary.md`
- `<state_collapser-repo>/docs/design/model_train_surfaces/01_001_model_and_training_surface_architecture.md`
- `<state_collapser-repo>/docs/design/model_train_surfaces/01_002_model_and_training_surface_blueprint.md`
- `<state_collapser-repo>/docs/design/model_train_surfaces/01_005_big_boy_benchmarking_tensorization_alignment_note.md`
- `<state_collapser-repo>/docs/design/tensorization/01_001_tensorization_architecture_blueprint.md`
- `<state_collapser-repo>/docs/code_review/03_001_synthetic_blow_full_repo_review_current_state.md`
- `<state_collapser-repo>/src/state_collapser/training/torch.py`

### PO Attribution

The Project Owner identified the core mismatch:

- the current Warehouse Gridlock "trainable" policy surface is not sufficient
  for the kind of long-horizon coordinated learning that motivated the
  environment;
- simply running more episodes through the current linear/factorized model is
  not a serious test of whether the tower can help discover coordinated
  behavior;
- every model should receive the full system configuration plus the current
  second/time value and should produce a full action-vector output;
- the transformer upgrade should not reopen already-settled Warehouse Gridlock
  environment semantics, reward semantics, masking semantics, or no-lookahead
  fairness semantics.

The Project Owner also explicitly pointed to prior work here and in
`state_collapser` as the place to resolve ambiguity, instead of asking new
design questions.

### Codex Synthesis

The appropriate next move is a narrow model/learner upgrade:

- keep the Warehouse Gridlock MDP fixed;
- keep the full-state/full-action policy contract fixed;
- keep both direct and tower arms immediate-admissibility-masked;
- keep "live lift" as a state-lift hygiene rule, not a one-hop action lookahead;
- replace the weak linear/factorized scoring model with a transformer-backed
  neural policy/value model;
- add real optimizer, gradient update, checkpoint, and progress semantics;
- prevent long runs from producing explosive raw CSV artifacts by default.

## Executive Summary

Warehouse Gridlock was introduced to test whether tower structure can help
discover large-scale coordinated solutions in a hidden, high-dimensional
multi-agent physical system. The environment is deliberately harder than the
earlier calibration cases: many robots, many boxes, synchronous ensemble moves,
collision constraints, hidden admissibility structure, and a long-horizon
success condition.

The current full-state policy comparison surface is useful as a contract smoke
test, but not as a serious learner. Its current policy model is too weak:

- it behaves like a linear/factorized local scorer;
- it cannot plausibly represent the coordinated multi-entity plans the
  environment is meant to expose;
- its "updates" do not have the meaning a reader expects from neural training;
- scaling episode count alone can create misleading confidence;
- raw event artifacts explode before the learning question becomes serious.

This blueprint upgrades the policy model to a small transformer actor-critic
owned by `big_boy_benchmarking`, while preserving the existing environment,
contract, masking, tower, and fairness boundaries.

The first target is not a final benchmark. The first target is a correct,
inspectable, resumable, artifact-disciplined training surface where a transformer
policy can train on Warehouse Gridlock and where subsequent direct-vs-tower
comparisons mean what they claim to mean.

## Non-Negotiable Boundaries

### Environment Boundary

The following are not changed by this blueprint:

- grid size;
- obstacle/column manifest;
- robot and box counts;
- start and target states;
- legal primitive moves;
- synchronous ensemble transition semantics;
- invalid ensemble semantics;
- reward constants;
- timer semantics;
- hidden/admissible-state framing.

### Fairness Boundary

The following remain true for direct and tower arms:

- both arms mask inadmissible immediate concrete actions;
- neither arm receives Abdul's stronger direct-star/tower-star one-hop
  cul-de-sac lookahead;
- the direct arm does not inspect future successor Out sets;
- the tower arm's live-lift rule only rejects upstairs lift states that have no
  valid outgoing action at all;
- live lift is state-selection hygiene for realizing a downstairs path, not
  single-tier one-hop planning;
- the model upgrade must not smuggle tower-only lookahead into direct-vs-tower
  comparison claims.

### Package Ownership Boundary

`big_boy_benchmarking` owns this transformer learner.

`state_collapser` does not become the training framework for this work.

The `state_collapser` docs reviewed for this blueprint are clear:

- `state_collapser` exposes tower metadata, masks, transitions, training
  surfaces, and optional tensorization boundaries;
- the engineer-authored benchmark or downstream project owns policy scoring,
  exploration, gradient updates, replay/storage, checkpointing, and model/device
  policy;
- optional Torch conversion is a boundary helper, not a package-owned PPO/DQN
  or transformer framework;
- backend-independent linearization must remain usable without importing Torch.

Therefore:

- the Warehouse Gridlock transformer implementation belongs in BBB;
- Torch imports must be local to BBB transformer-specific modules;
- existing BBB imports, CLI help, and non-ML tests must not require Torch;
- no new `state_collapser` implementation work is in scope.

### Claim Boundary

This upgrade may support future evidence about tower advantage, but by itself it
does not claim:

- general tower superiority;
- statistical significance;
- solved Warehouse Gridlock;
- robotics generalization;
- broad benchmark validity;
- mature RL library status;
- production-grade model architecture.

It claims only that Warehouse Gridlock now has a plausible trainable neural
policy surface for serious diagnostic runs.

## Current Failure Being Corrected

The current full-state policy comparison did satisfy part of the prior contract:

- each arm can receive a full Warehouse configuration;
- each arm can produce a full robot action vector;
- immediate inadmissible actions can be masked/resolved;
- tower live-lift semantics can be compared against a direct arm under the
  no-lookahead boundary.

But it did not satisfy the deeper learning intent:

- the policy class was too weak for coordinated robot/box planning;
- long runs could not be interpreted as serious learning pressure;
- progress output used "updates" in a way that did not clearly mean optimizer
  steps;
- rendered movies could be generated, but raw trace retention was too expensive;
- deleting giant CSV files broke future movie generation for those traces;
- the artifact system did not yet distinguish summary-first long training from
  debug/full-trace runs.

This blueprint fixes the model, training, checkpointing, progress, and artifact
retention surface needed before running long Warehouse Gridlock experiments.

## Relationship To Prior Linear Policy Contract

The prior blueprint remains correct at the contract level. The transformer
upgrade should reuse, not replace, these concepts:

- `WarehouseFullSystemConfig`;
- `WarehouseFullActionVector`;
- `WarehousePolicyDecision`;
- `WarehousePolicyUpdate`;
- raw model proposal vs admissibility-resolved selected action;
- full action vector output;
- action resolver constrained to immediate validity;
- direct arm receives no tower/tier/future/global-MDP privileged information;
- tower arm may use tower structure internally but must realize concrete full
  action vectors;
- live-lift is permitted only as pointwise/liveness hygiene.

The prior blueprint's pragmatic linear model was always an initial surface. This
document replaces that model family for serious Warehouse training while keeping
the contract shape.

## Proposed Evaluation Surface

### New Evaluation Family

Create a new evaluation/readout family rather than overwriting the existing
linear full-state policy comparison:

```text
docs/evaluations/warehouse_gridlock_001/transformer_policy/
```

This avoids contaminating earlier linear-readout provenance and gives the new
artifact policy room to be explicit.

### New Design Folder

The design folder for this work is:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/03_transformer_policy_model_upgrade/
```

### Recommended CLI Shape

Add a dedicated CLI surface:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock transformer-policy run ...
uv run python -m big_boy_benchmarking.cli warehouse-gridlock transformer-policy summarize ...
uv run python -m big_boy_benchmarking.cli warehouse-gridlock transformer-policy render-episode ...
```

The CLI may internally reuse the existing `full_state_policy_comparison`
helpers, but the user-facing command should make it impossible to confuse the
linear smoke model with the transformer learner.

### First Serious Slice

The first transformer slice should be tower-only curriculum training, because
that is where the PO frustration occurred:

- no direct arm required for the first training sanity pass;
- same Warehouse Gridlock environment;
- same live-lift tower surface;
- immediate-valid action masking;
- transformer model;
- real optimizer updates;
- checkpointing;
- progress bar with reward first;
- trace-retention policy that supports selected movie episodes without writing
  every step of every episode to giant CSV.

Direct-vs-tower transformer comparison should be a second use of the same model
surface, not a prerequisite for the first model-correction slice.

## Dependency Design

### Torch Dependency

Add Torch as an optional BBB dependency, not a base dependency.

Recommended package shape:

```toml
[project.optional-dependencies]
ml = [
  "torch>=2.4",
]
```

If the project already grows another optional dependency group before
implementation, the workplan may merge this with the local style. The invariant
is that plain `uv sync --group dev`, package import, CLI help, and non-ML tests
must not require Torch unless the repository decides to make ML dependencies
part of dev.

### Import Discipline

Torch imports must be contained in transformer-specific modules, for example:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/transformer_policy/
```

Do not import Torch from:

- package root;
- generic Warehouse environment modules;
- policy contract module;
- CLI top-level import path before the transformer subcommand is invoked;
- artifact readout modules that should work without ML installed.

### Runtime Manifest

Each run must record:

- whether Torch was available;
- Torch version;
- selected device;
- CUDA availability if relevant;
- deterministic flags if set;
- model family ID;
- model config hash;
- optimizer config hash;
- dependency manifest for BBB and `state_collapser`.

## Model Family

### Model Family ID

Use:

```text
warehouse_transformer_actor_critic_policy_v001
```

This name is intentionally specific:

- Warehouse-specific;
- transformer-backed;
- actor-critic;
- policy model, not environment;
- versioned.

### Input Contract

The model receives:

- full Warehouse Gridlock system configuration;
- current second/time value;
- optional normalized time budget fields;
- arm context;
- tower context when applicable.

It must not receive:

- future successor admissibility;
- hidden full MDP graph;
- episode outcome labels from the future;
- direct-star or tower-star one-hop cul-de-sac oracle;
- any information not available to the corresponding arm at decision time.

### Output Contract

The model produces:

- full action-vector policy scores;
- a value estimate;
- optional diagnostics embeddings/scores for readout.

For the first implementation, the full action-vector score can be represented as
per-robot categorical logits:

```text
[robot_count, primitive_action_count]
```

where primitive actions are:

```text
stay, north, south, west, east
```

The selected action is still a full vector:

```text
robot_id -> primitive action
```

The policy surface must record both:

- raw model logits/scores;
- final selected and resolver-approved action vector.

## Transformer Encoding

### Token Types

Use a set/sequence encoder over entity and context tokens.

Recommended token inventory:

- global token;
- time token or time fields on global token;
- one token per robot;
- one token per box;
- one token per blocked column;
- optional target tokens, or target fields attached to robot/box tokens;
- optional tower context token;
- optional candidate/path context token for tower arm.

### Token Features

Each token should encode, as applicable:

- token type;
- entity ID;
- row;
- column;
- target row;
- target column;
- at-target flag;
- carrying/pushing/contact-local flags if present in current transition model;
- occupancy type;
- normalized current second;
- normalized max seconds;
- remaining seconds;
- arm ID;
- tower tier ID;
- tower state-cell ID or compact progress fields;
- live-lift/candidate metadata for tower arm.

### Position Encoding

The Warehouse grid is small and discrete. Use learned embeddings for row and
column rather than sinusoidal sequence position as the primary spatial signal.

Recommended embeddings:

- token type embedding;
- entity ID embedding;
- row embedding;
- column embedding;
- target row embedding;
- target column embedding;
- arm/tower context embedding.

Do not depend on arbitrary token order as the only spatial encoding.

### Initial Model Size

Recommended CPU-first model:

```text
d_model: 128
n_layers: 2
n_heads: 4
mlp_hidden: 256
dropout: 0.0 or 0.1
activation: gelu
```

The first implementation should prioritize correctness, inspectability, and
iteration speed over maximum capacity.

### Larger Future Model

A later model family may increase:

- `d_model`;
- layer count;
- head count;
- candidate-action decoder sophistication;
- temporal memory;
- graph attention bias;
- box/robot relation encoding.

Those are explicitly not required for this first transformer upgrade.

## Action Selection Design

### Direct Arm

The direct arm path should:

1. encode the current concrete state;
2. run transformer forward pass;
3. produce per-robot primitive logits;
4. sample or choose a full action vector;
5. pass the vector through the immediate-admissibility resolver;
6. execute only a valid selected vector;
7. record raw logits/proposal and selected vector.

The resolver may repair only immediate invalidity. It must not search future
states or inspect successor Out sets.

### Tower Arm

The first transformer tower arm should use candidate-vector scoring, not a new
abstract-action decoder.

Shape:

1. tower surface proposes a bounded set of concrete candidate action vectors
   available from the current lifted state/path context;
2. transformer encodes the current concrete state plus tower context;
3. transformer emits per-robot primitive logits;
4. each candidate vector receives a score from the sum of its constituent
   per-robot log probabilities/logits;
5. the policy samples or chooses among candidate vectors;
6. live-lift hygiene rejects lift states with no outgoing valid action;
7. selected candidate executes as the concrete full action vector;
8. artifacts record the candidate set size, selected candidate score, and
   masking/lift status.

This keeps the implementation faithful to the prior full-action-vector contract
while avoiding a new, under-designed abstract-action transformer head.

### Why Not Abstract Action Head First

An abstract-action head may be appropriate later, but it would reopen several
hard questions:

- how to tokenize abstract action cells;
- how to compare direct logits to abstract logits;
- how to attribute tower advantage to structure vs action-head design;
- how to train across changing tower tier action sets;
- how to checkpoint candidate vocabularies.

The candidate-vector scoring design is the narrowest serious upgrade that
directly addresses the current failure: the model class is too weak.

## Training Objective

### First Objective

Use an online episodic actor-critic objective.

For each episode:

1. collect states, selected actions, log probabilities, entropy terms, rewards,
   value estimates, and done flags;
2. compute discounted returns;
3. compute advantages as return minus value estimate;
4. compute policy loss from selected action log probabilities and advantages;
5. compute value loss;
6. add entropy regularization;
7. run one optimizer step or a small fixed number of minibatch optimizer steps.

Recommended initial loss:

```text
loss = policy_loss + value_coef * value_loss - entropy_coef * entropy
```

Recommended initial hyperparameters:

```text
gamma: 0.99
learning_rate: 3e-4
value_coef: 0.5
entropy_coef: 0.01
max_grad_norm: 1.0
optimizer: AdamW
```

These defaults should be artifact-recorded, not hidden constants.

### Updates Terminology

The progress bar and artifacts must stop using ambiguous "updates" language.

Use:

```text
optimizer_steps
```

for actual gradient steps.

If additional counters are useful, name them explicitly:

- `episodes_completed`;
- `policy_forward_passes`;
- `candidate_sets_scored`;
- `resolver_repairs`;
- `checkpoint_count`;
- `trace_episodes_written`.

### PPO Not Required In First Slice

PPO may be useful later, but it is not required for the first transformer
upgrade. Starting with a simple actor-critic loop is consistent with the
`state_collapser` training-surface design: BBB owns the loop and can improve it
incrementally.

## Curriculum Design

The existing user-run curriculum concept should be preserved:

- tower-only option;
- max seconds per episode increases over training;
- e.g. from 2 seconds to 64 seconds over 1024 curriculum positions;
- curriculum progress may be tied to global episode index, not necessarily
  total configured episodes.

### Curriculum Manifest

Record:

- start max seconds;
- end max seconds;
- ramp episode count;
- schedule function;
- actual per-episode max seconds;
- whether the schedule continues flat after the ramp.

### First Run Script Update

The existing script:

```text
scripts/run_warehouse_gridlock_tower_curriculum_train.sh
```

should either be updated to target the transformer command or replaced by a new
script:

```text
scripts/run_warehouse_gridlock_tower_transformer_curriculum_train.sh
```

The latter is safer because it keeps the current linear-curriculum script's
provenance intact.

## Checkpointing

### Required Checkpoints

Long transformer runs must be checkpointed.

Write checkpoints:

- at episode 0 initialization metadata;
- every `checkpoint_every_episodes`;
- at final episode;
- when best rolling reward improves, subject to a minimum interval.

Recommended default:

```text
checkpoint_every_episodes: 100
keep_last_n_checkpoints: 5
keep_best_n_checkpoints: 3
```

### Checkpoint Contents

Each checkpoint must include:

- model state dict;
- optimizer state dict;
- model config;
- optimizer config;
- random seeds and RNG states where feasible;
- episode index;
- optimizer step count;
- curriculum state;
- rolling reward summaries;
- arm ID;
- run ID;
- BBB version/provenance;
- `state_collapser` version/provenance;
- Torch version/device metadata.

### Checkpoint Manifest

Write:

```text
checkpoint_manifest.json
```

with one row/object per checkpoint:

- checkpoint ID;
- path;
- episode index;
- optimizer step count;
- reason (`periodic`, `best`, `final`);
- summary reward;
- file size;
- checksum if cheap enough.

### Resume Semantics

The first implementation may support checkpoint loading for rendering and
inspection before it supports full training resume.

However, the artifact format should not prevent future resume.

Minimum requirement:

- saved checkpoints can be loaded;
- a loaded model can run inference;
- a loaded model can reproduce deterministic greedy action selection for a fixed
  recorded state/config.

## Artifact Retention Design

### Problem

The previous Warehouse runs wrote large CSV traces. Long training caused artifact
trees to grow into hundreds of megabytes or gigabytes. Deleting those CSVs saved
space but broke later movie generation from those traces.

The transformer upgrade must fix this before serious long runs.

### Default Policy

Use summary-first artifact retention by default.

Default long-run outputs:

- episode summary table;
- training curve summary;
- checkpoint manifest;
- selected trace episode index;
- compact selected episode traces;
- progress events;
- timing summary;
- projection/resolver summary;
- tower lift summary;
- model/optimizer/checkpoint manifests.

Default long-run outputs must not include:

- full step-event CSV for every episode;
- duplicated raw events in multiple directories;
- uncompressed giant per-step tables;
- movie frames for every episode.

### Trace Episode Selection

Support explicit trace episode selection:

```text
--trace-episode-index 0
--trace-episode-index 10
--trace-episode-index 100
--trace-episode-index final
--trace-every-episodes 100
```

Only selected episodes should retain enough step-level data for movie rendering.

### Trace Format

Preferred trace format:

- compact JSONL for selected episodes; or
- compact CSV for selected episodes only; or
- compressed `.jsonl.zst` / `.csv.zst` if compression dependency is acceptable.

The first implementation can avoid a new compression dependency by writing only
selected compact traces.

If compression is added, it must be optional or already present in dependencies.

### Movie Rendering

Movie rendering should target selected trace episodes, not require global
all-episode `step_events.csv`.

Recommended command shape:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock transformer-policy render-episode \
  --artifact-root docs/evaluations/warehouse_gridlock_001/transformer_policy/artifacts/<run_label> \
  --arm-id warehouse_tower_transformer_live_lift_masked \
  --replicate-index 0 \
  --schema-seed 0 \
  --episode-index 512 \
  --output docs/evaluations/warehouse_gridlock_001/transformer_policy/movies/<run_label>/tower_ep0512.gif
```

If the episode was not retained as a trace, the renderer must fail clearly:

```text
Episode 512 was not retained as a renderable trace. Available trace episodes:
0, 10, 100, 512, 1024, final.
```

### Artifact Budget Guard

Add a guardrail:

- warn when artifact root exceeds configured soft budget;
- fail or stop writing raw traces when exceeding hard budget;
- record budget status in `artifact_retention_manifest.json`.

Recommended initial soft budget:

```text
500 MB
```

Recommended initial hard budget:

```text
2 GB
```

These must be configurable.

## Progress Bar Design

The progress bar must show reward first.

Recommended live display fields, in order:

```text
reward=<latest_episode_reward>
rolling=<rolling_mean_reward>
optimizer_steps=<count>
episode=<episode_index>/<total>
max_seconds=<current_limit>
arm=<short_arm_id>
```

The user specifically asked to see reward first. This is not cosmetic; it is
part of making long-running experiments monitorable.

Avoid long arm IDs in the primary progress field when they push reward out of
view.

## New Module Layout

Recommended package:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/transformer_policy/
  __init__.py
  config.py
  encoding.py
  model.py
  action_selection.py
  training.py
  checkpoints.py
  trace_retention.py
  runner.py
  aggregation.py
  docs_writer.py
  manifests.py
  paths.py
```

### `config.py`

Defines:

- model config dataclass;
- optimizer config dataclass;
- training config dataclass;
- curriculum config dataclass;
- artifact retention config dataclass;
- CLI parse helpers if local style supports them.

### `encoding.py`

Defines:

- Warehouse state to token tensors;
- token type IDs;
- row/column feature extraction;
- target feature extraction;
- tower context encoding;
- batch collation for one or more states.

No optimizer or training loop logic belongs here.

### `model.py`

Defines:

- Torch transformer actor-critic module;
- forward output dataclass;
- model construction from config;
- model parameter count helper.

Torch import lives here and in other transformer-specific files only.

### `action_selection.py`

Defines:

- direct full-vector sampling/greedy selection;
- tower candidate-vector scoring;
- immediate-mask integration;
- log-prob extraction;
- entropy calculation;
- selected action record conversion to existing policy contract rows.

### `training.py`

Defines:

- rollout buffer;
- return/advantage computation;
- loss computation;
- optimizer step;
- gradient clipping;
- deterministic seed handling.

### `checkpoints.py`

Defines:

- save checkpoint;
- load checkpoint;
- checkpoint manifest row;
- best/final/periodic checkpoint policy.

### `trace_retention.py`

Defines:

- trace episode selection;
- compact selected episode trace writing;
- trace index writing;
- artifact budget measurement;
- clear error messages for missing traces.

### `runner.py`

Defines:

- tower-only curriculum run;
- optional direct-vs-tower run once the tower-only slice is stable;
- integration with environment, tower surface, resolver, model, optimizer,
  checkpointing, traces, and progress bar.

### `aggregation.py`

Defines:

- episode summary aggregation;
- training curve aggregation;
- checkpoint summary aggregation;
- resolver/projection summary;
- tower live-lift summary;
- timing summary.

### `docs_writer.py`

Defines:

- `readout_source.json` writer;
- README/report source table paths;
- report badges;
- method/runbook/glossary stubs if local protocol expects them.

## IDs And Artifact Names

### Evaluation ID

```text
warehouse_gridlock_transformer_policy_v001
```

### Initial Arm IDs

Tower-only initial arm:

```text
warehouse_tower_transformer_live_lift_masked
```

Future direct arm:

```text
warehouse_direct_transformer_admissible_masked
```

Future paired comparison arm set:

```text
warehouse_transformer_direct_vs_live_lift_tower_no_lookahead_v001
```

### Artifact Root

Default examples:

```text
docs/evaluations/warehouse_gridlock_001/transformer_policy/artifacts/tower_transformer_curriculum_smoke_001
docs/evaluations/warehouse_gridlock_001/transformer_policy/artifacts/tower_transformer_curriculum_train_2048_001
```

### Readout Root

```text
docs/evaluations/warehouse_gridlock_001/transformer_policy/
```

## Required Manifests

Each run should write:

- `evaluation_manifest.json`;
- `evaluation_budget_lock.json`;
- `environment_instance_manifest.json`;
- `policy_contract_manifest.json`;
- `transformer_model_manifest.json`;
- `optimizer_manifest.json`;
- `curriculum_manifest.json`;
- `checkpoint_manifest.json`;
- `trace_retention_manifest.json`;
- `artifact_retention_manifest.json`;
- `dependency_manifest.json`;
- `run_index.csv` or equivalent compact run index;
- `readout_source.json`.

## Required Result Tables

Minimum tables:

- `results/episode_summary.csv`;
- `results/training_curve_summary.csv`;
- `results/checkpoint_summary.csv`;
- `results/trace_episode_index.csv`;
- `results/resolver_summary.csv`;
- `results/tower_live_lift_summary.csv`;
- `results/curriculum_summary.csv`;
- `results/timing_summary.csv`;
- `results/artifact_retention_summary.csv`;

Optional selected-trace tables:

- `traces/<episode_id>/step_trace.csv`;
- `traces/<episode_id>/state_trace.jsonl`;
- `traces/<episode_id>/action_trace.csv`.

The optional selected-trace tables are renderability artifacts, not global
training tables.

## Human-Readable Readout Requirements

The transformer readout should clearly answer:

- what model was trained;
- whether this was tower-only or direct-vs-tower;
- whether training used real optimizer steps;
- how many optimizer steps occurred;
- what curriculum was used;
- what checkpoint is best/final;
- which episodes can be rendered as movies;
- whether artifact retention stayed within budget;
- whether live-lift was active;
- whether any one-hop lookahead was used;
- whether the run is smoke, diagnostic, or claim-bearing.

The readout must explicitly distinguish:

- linear/factorized prior model;
- transformer actor-critic model;
- optimizer steps vs old ambiguous "updates";
- selected trace episodes vs unavailable deleted/unretained traces.

## Interaction With Human-Readable Protocol

The artifact-table readout protocol should be pointed at:

```text
docs/evaluations/warehouse_gridlock_001/transformer_policy/readout_source.json
```

not the raw artifact directory, unless the protocol is explicitly extended to
discover readout sources from directories again.

The command form should remain:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/transformer_policy/readout_source.json
```

## Test Plan

### Non-ML Tests

These must pass without Torch installed:

- import `big_boy_benchmarking`;
- CLI help;
- Warehouse environment construction;
- Warehouse readiness tests;
- existing linear policy tests if they do not require Torch;
- readout generation from already-written transformer tables if possible.

### ML-Gated Tests

If Torch is unavailable, mark these skipped with a clear reason.

Required ML tests:

1. Encoding shape test:
   - construct default Warehouse state;
   - encode to tokens;
   - assert batch/token/feature shapes;
   - assert row/column/token type ranges.

2. Forward pass shape test:
   - create small transformer config;
   - run forward pass;
   - assert robot action logits shape;
   - assert scalar value shape.

3. Direct action selection test:
   - run direct selector with immediate mask;
   - assert selected full vector has one action per robot;
   - assert selected vector is resolver-valid or clearly repaired by immediate
     resolver.

4. Tower candidate scoring test:
   - construct candidate vectors;
   - score candidates from transformer logits;
   - assert selected candidate belongs to candidate set;
   - assert no successor Out lookahead is used.

5. Optimizer update test:
   - run one short episode or synthetic rollout;
   - apply one optimizer step;
   - assert at least one parameter changes;
   - assert `optimizer_steps` increments.

6. Checkpoint round-trip test:
   - save checkpoint;
   - load checkpoint;
   - assert deterministic greedy action/logits match for a fixed state.

7. Trace retention test:
   - configure traces for episodes `0` and `final`;
   - run tiny training;
   - assert only selected traces are written;
   - assert renderer succeeds for retained episode;
   - assert renderer fails clearly for unretained episode.

8. Artifact budget test:
   - run tiny training;
   - assert no global giant `step_events.csv` is written by default;
   - assert artifact retention manifest exists.

### Regression Tests

Existing Warehouse tests must continue to pass:

- environment readiness;
- masked direct vs live-lift comparison smoke;
- full-state policy contract tests;
- movie rendering tests for retained traces;
- no-lookahead fairness tests where present.

## Implementation Phases For Future Workplan

The later implementation workplan should use Phase.Stage.Action format and
should roughly follow this order:

1. Verify branch, dirty state, and relevant docs.
2. Add optional ML dependency and Torch import gates.
3. Add transformer module skeleton and configs.
4. Implement encoding.
5. Implement transformer forward pass.
6. Implement direct and tower action-selection adapters.
7. Implement actor-critic training loop.
8. Implement checkpointing.
9. Implement trace retention and artifact budget policy.
10. Add runner and CLI.
11. Add summary/readout writers.
12. Add scripts for tower curriculum.
13. Add tests.
14. Run smoke training only.
15. Generate human-readable readout.
16. Record implementation log.

## Stop Conditions

Stop and report instead of pushing through if:

- Torch cannot be imported in the ML-gated path and dependency installation is
  not authorized;
- non-ML package import starts requiring Torch;
- the transformer runner changes Warehouse environment semantics;
- the direct arm receives tower-only context;
- either arm receives one-hop successor Out lookahead;
- live-lift is implemented as action lookahead instead of state-lift liveness;
- the artifact writer starts producing full all-episode giant CSV traces by
  default;
- checkpoint load cannot reproduce deterministic inference for a fixed state;
- progress output cannot show reward first;
- movie rendering still depends on deleted/global all-episode step CSVs;
- tests require a long training run;
- implementation discovers that current tower candidate generation cannot expose
  enough candidate vectors to train against.

## Open Questions Resolved By Prior Context

No new PO questions are required before creating the implementation workplan.

The known ambiguities are resolved as follows:

- Model ownership: BBB owns the transformer learner.
- `state_collapser` role: tower/lift semantics and optional tensor boundary, not
  training framework.
- Initial model: transformer actor-critic.
- Initial training target: tower-only curriculum first.
- Direct-vs-tower comparison: later use of same model surface.
- Action output: full robot action vector.
- Tower action selection: score candidate concrete vectors first, not abstract
  action head.
- Lookahead: no one-hop lookahead for either arm.
- Masking: immediate inadmissible actions masked/resolved for both arms.
- Checkpoints: required.
- Artifact growth: fixed before long runs.
- Readout: new transformer readout folder, do not overwrite linear readout.

## Completion Criteria

The transformer upgrade is complete when:

- a new transformer policy evaluation family exists;
- Torch is optional and import-gated;
- a Warehouse transformer actor-critic can run a forward pass from full system
  config plus time;
- tower candidate vectors can be scored and selected by the model;
- a real optimizer step updates parameters and increments `optimizer_steps`;
- checkpoints are written and loadable;
- selected trace episodes can be rendered into movies;
- long-run default artifacts no longer produce all-episode giant CSV traces;
- a tower-only transformer curriculum smoke run completes;
- a human-readable readout can be generated from the new readout source;
- tests cover import gates, encoding, forward pass, action selection, training
  update, checkpoint round-trip, and trace retention;
- the implementation log records what was done and what remains bounded.
