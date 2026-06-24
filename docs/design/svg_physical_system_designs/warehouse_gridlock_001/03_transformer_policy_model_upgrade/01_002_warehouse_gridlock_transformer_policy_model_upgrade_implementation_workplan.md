# Warehouse Gridlock Transformer Policy Model Upgrade Implementation Workplan

## Document Status

This is the implementation workplan for:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/03_transformer_policy_model_upgrade/01_001_warehouse_gridlock_transformer_policy_model_upgrade_blueprint.md
```

This workplan follows `Phase.Stage.Action` discipline. If the Project Owner
later says to execute this workplan, every action below is an implementation
obligation unless the Project Owner explicitly changes scope.

This document is not an implementation log. When execution begins, create the
implementation log named below and record progress there.

## Prime Directive Execution Constraints

This workplan is governed by:

- `docs/prime_directive/prime_directive.md`
- `docs/prime_directive/common_failure_mode_002_implementation_without_owner_approval.md`
- `docs/prime_directive/common_failure_mode_003_gameplan_rewrite_during_implementation.md`
- `docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`
- `docs/prime_directive/git_practices.md`

The governing rules for execution are:

- do not begin implementation merely because this workplan exists;
- if execution is approved, create or switch to a dedicated implementation
  branch before touching implementation code;
- treat every `Phase.Stage.Action` item as law;
- do not silently simplify, collapse, reorder, or replace this workplan;
- if an action cannot be completed as written, stop and ask the Project Owner;
- do not invent Project Owner turns or imply the Project Owner said something
  not present in the conversation or source documents;
- keep a running implementation log during execution;
- do not alter `state_collapser` as part of this BBB workplan.

## Implementation Branch

Recommended branch:

```text
codex/warehouse-gridlock-transformer-policy-model-upgrade
```

If execution begins from another branch, record the actual branch in the
implementation log before editing files.

## Implementation Log

Required log path:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/03_transformer_policy_model_upgrade/01_003_warehouse_gridlock_transformer_policy_model_upgrade_implementation_log.md
```

The log must record:

- branch and starting commit;
- dirty-state inventory before edits;
- every completed `Phase.Stage.Action`;
- test commands and results;
- any stop condition encountered;
- any Project Owner clarification received during execution;
- final status and remaining bounded work.

## Blueprint Decision Locks

The following decisions are locked by the blueprint and must not be reopened
during implementation:

- the Warehouse Gridlock environment semantics do not change;
- reward constants do not change;
- invalid ensemble semantics do not change;
- direct and tower arms both use immediate admissibility masking;
- neither arm receives one-hop successor-Out lookahead;
- live-lift remains state-lift liveness hygiene, not action lookahead;
- BBB owns the transformer learner and training loop;
- `state_collapser` is not modified;
- Torch is optional and import-gated;
- the first serious slice is tower-only transformer curriculum training;
- direct-vs-tower transformer comparison is future use of the same surface, not
  required for the first slice;
- long-run artifact retention is summary-first and selected-trace-only by
  default;
- progress output shows reward first;
- the new transformer readout does not overwrite the old linear readout.

## Required New Evaluation Surface

Create a new surface:

```text
docs/evaluations/warehouse_gridlock_001/transformer_policy/
```

Do not overwrite:

```text
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/
```

## Required New Package Surface

Create a new package:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/transformer_policy/
```

The package must not be imported by generic Warehouse modules unless the
transformer command path is invoked.

## Phase 0 - Authority, Branch, And Reality Sync

### Phase 0.Stage 1.Action 1 - Re-read governing documents

Before implementation, re-read:

- this workplan;
- the transformer blueprint;
- the transformer design discussion;
- Prime Directive failure modes 002, 003, and 004;
- `docs/prime_directive/git_practices.md`;
- current Warehouse policy contract modules.

Record the re-read in the implementation log.

### Phase 0.Stage 1.Action 2 - Verify branch and dirty state

Run a status check and record:

- current branch;
- current commit;
- staged files;
- unstaged files;
- untracked files;
- whether any unrelated user changes are present.

Do not revert unrelated user changes.

If unrelated changes touch files this workplan must edit, inspect them and work
with them. If they make implementation unsafe, stop and ask the Project Owner.

### Phase 0.Stage 1.Action 3 - Create or switch to implementation branch

Create or switch to:

```text
codex/warehouse-gridlock-transformer-policy-model-upgrade
```

unless the Project Owner has already placed the work on an intended branch.

Record the branch action in the implementation log.

### Phase 0.Stage 1.Action 4 - Create implementation log

Create:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/03_transformer_policy_model_upgrade/01_003_warehouse_gridlock_transformer_policy_model_upgrade_implementation_log.md
```

Include:

- workplan path;
- blueprint path;
- branch;
- starting commit;
- dirty-state summary;
- current execution status.

### Phase 0.Stage 1.Action 5 - Establish stop conditions in log

Copy or summarize the stop conditions from this workplan into the implementation
log so a future execution cannot claim surprise about them.

## Phase 1 - Current Warehouse Surface Audit

### Phase 1.Stage 1.Action 1 - Audit policy contract module

Inspect:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/policies/contracts.py
```

Confirm and record:

- full system config type;
- full action vector type;
- policy decision record shape;
- policy update record shape;
- whether existing fields are sufficient for transformer decisions;
- whether new transformer-only metadata should live outside the shared contract.

Do not weaken or replace the existing policy contract.

### Phase 1.Stage 1.Action 2 - Audit linear policy module

Inspect:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/policies/linear_policy.py
```

Record:

- current linear model family ID;
- current feature extraction assumptions;
- current update semantics;
- any helper functions that are safe to reuse;
- which parts must not be reused because they encode the weak linear learner.

### Phase 1.Stage 1.Action 3 - Audit resolver module

Inspect:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/policies/resolver.py
```

Record:

- how immediate invalid actions are masked or repaired;
- whether resolver behavior is direct/tower neutral;
- whether the resolver inspects successor Out sets.

If resolver behavior performs one-hop lookahead, stop and ask the Project Owner.

### Phase 1.Stage 1.Action 4 - Audit full-state comparison runner

Inspect:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/runner.py
```

Record:

- current run loop;
- current progress bar fields;
- current artifact outputs;
- current source of giant CSV growth;
- current use of "updates";
- what can be reused for transformer runs.

### Phase 1.Stage 1.Action 5 - Audit masked direct/live-lift tower surface

Inspect:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/masked_direct_vs_live_lift_tower/
```

Record:

- candidate generation entry points;
- tower surface entry points;
- live-lift implementation point;
- how candidate concrete vectors are generated;
- how tower context can be passed to transformer encoding;
- whether any hidden one-hop lookahead exists.

If the current tower surface cannot provide candidate concrete vectors without a
larger redesign, stop and ask the Project Owner.

### Phase 1.Stage 2.Action 1 - Audit replay/movie renderer

Inspect:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/replay.py
```

Record:

- current expected trace file shape;
- current lookup path for `run_index.csv` or step-event tables;
- what must change so selected retained traces can render movies;
- how missing trace episodes should fail clearly.

### Phase 1.Stage 2.Action 2 - Audit CLI shape

Inspect Warehouse Gridlock command handling in:

```text
src/big_boy_benchmarking/cli/main.py
```

Record:

- existing warehouse subcommands;
- parser style;
- command dispatch style;
- output summary style;
- where `transformer-policy` should attach.

### Phase 1.Stage 2.Action 3 - Audit test style

Inspect existing Warehouse tests:

```text
tests/environments/warehouse_gridlock/
```

Record:

- fixture patterns;
- CLI artifact tests;
- replay tests;
- policy contract tests;
- where ML-gated transformer tests should live.

## Phase 2 - Optional ML Dependency And Import Gates

### Phase 2.Stage 1.Action 1 - Add optional ML dependency group

Update `pyproject.toml` to add an optional dependency surface for Torch.

Preferred shape:

```toml
[project.optional-dependencies]
ml = [
  "torch>=2.4",
]
```

If current packaging style requires a different shape, preserve local style and
record the reason in the implementation log.

### Phase 2.Stage 1.Action 2 - Preserve base dependency behavior

Verify that base package dependencies still do not require Torch.

The following must still work without importing Torch:

- importing `big_boy_benchmarking`;
- importing generic Warehouse Gridlock environment modules;
- invoking CLI help;
- running non-ML tests.

### Phase 2.Stage 1.Action 3 - Create Torch availability helper

Create a transformer-local helper that detects Torch availability without
importing Torch at package root.

Recommended location:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/transformer_policy/torch_runtime.py
```

It should expose:

- `torch_available`;
- `torch_version`;
- `cuda_available`;
- selected device normalization;
- a clear exception for ML command paths when Torch is missing.

### Phase 2.Stage 1.Action 4 - Add import-gate tests

Add tests verifying:

- non-transformer Warehouse imports do not require Torch;
- transformer ML tests skip clearly if Torch is unavailable;
- transformer command fails clearly if invoked without Torch installed.

## Phase 3 - Transformer Package Skeleton And IDs

### Phase 3.Stage 1.Action 1 - Create transformer package

Create:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/transformer_policy/
```

with:

```text
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
torch_runtime.py
```

Each module should have real responsibilities. Do not create placeholder-only
modules and call the phase complete.

### Phase 3.Stage 1.Action 2 - Add evaluation and arm IDs

Add or extend Warehouse IDs so the following are available:

```text
warehouse_gridlock_transformer_policy_v001
warehouse_transformer_actor_critic_policy_v001
warehouse_tower_transformer_live_lift_masked
warehouse_direct_transformer_admissible_masked
```

If IDs are centralized in:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/ids.py
```

use that local style.

### Phase 3.Stage 1.Action 3 - Add path helpers

Implement path helpers for:

```text
docs/evaluations/warehouse_gridlock_001/transformer_policy/
```

and artifact roots under:

```text
docs/evaluations/warehouse_gridlock_001/transformer_policy/artifacts/<run_label>
```

Path helpers must distinguish:

- repository readout root;
- source artifact root;
- result tables;
- selected traces;
- checkpoints;
- movies.

### Phase 3.Stage 1.Action 4 - Add config dataclasses

In `config.py`, define dataclasses for:

- model config;
- optimizer config;
- training config;
- curriculum config;
- artifact retention config;
- trace retention config;
- run config.

Defaults must match the blueprint unless implementation reality forces a stop.

Required default model config:

```text
d_model: 128
n_layers: 2
n_heads: 4
mlp_hidden: 256
dropout: 0.0 or 0.1
activation: gelu
```

Required default training config:

```text
gamma: 0.99
learning_rate: 3e-4
value_coef: 0.5
entropy_coef: 0.01
max_grad_norm: 1.0
optimizer: AdamW
```

### Phase 3.Stage 1.Action 5 - Add config serialization

Implement stable JSON serialization for every config.

The serialization must be used by manifests and checkpoints.

## Phase 4 - Full-State Token Encoding

### Phase 4.Stage 1.Action 1 - Define token vocabulary

In `encoding.py`, define token types for:

- global token;
- robot tokens;
- box tokens;
- blocked column tokens;
- optional tower context token;
- optional candidate/path context token.

Record token type IDs in code and manifests.

### Phase 4.Stage 1.Action 2 - Encode spatial/entity fields

Implement feature extraction for:

- entity ID;
- row;
- column;
- target row;
- target column;
- at-target flag;
- occupancy type;
- entity type;
- current second;
- max seconds;
- remaining seconds.

Use learned embedding IDs for discrete rows/columns rather than relying on
arbitrary sequence order.

### Phase 4.Stage 1.Action 3 - Encode arm context

Implement context fields for:

- tower-only run;
- future direct arm;
- future paired comparison arm;
- run label;
- arm ID.

Do not expose tower context to the direct arm.

### Phase 4.Stage 1.Action 4 - Encode tower context

For tower runs, encode:

- current tier ID if available;
- state-cell ID or compact progress fields;
- live-lift status;
- candidate set size;
- candidate generation metadata available before action selection.

Do not encode future successor Out information.

### Phase 4.Stage 1.Action 5 - Add batch collation

Implement a small batch collation function that converts one or more Warehouse
states into Torch tensors.

The collation function must return enough metadata to map output logits back to
robot IDs and primitive actions.

### Phase 4.Stage 1.Action 6 - Add encoding tests

Add tests covering:

- token count;
- tensor shapes;
- row/column bounds;
- robot and box token counts;
- blocked column token count;
- time normalization;
- tower context inclusion only for tower arm.

## Phase 5 - Transformer Actor-Critic Model

### Phase 5.Stage 1.Action 1 - Implement Torch model class

In `model.py`, implement:

```text
WarehouseTransformerActorCritic
```

The model must:

- accept encoded token tensors;
- apply token/type/spatial embeddings;
- run a Transformer encoder;
- emit per-robot primitive-action logits;
- emit a scalar value estimate.

### Phase 5.Stage 1.Action 2 - Implement model output dataclass

Define a model output object with:

- robot action logits;
- value estimate;
- optional token embeddings for diagnostics;
- optional entropy helper fields if useful.

### Phase 5.Stage 1.Action 3 - Implement model factory

Implement construction from model config and environment metadata.

The factory must record:

- model family ID;
- parameter count;
- token vocabulary;
- primitive action vocabulary;
- architecture config.

### Phase 5.Stage 1.Action 4 - Add device handling

Support:

- CPU default;
- optional CUDA if available and explicitly selected;
- clear manifest record of selected device.

Do not silently require CUDA.

### Phase 5.Stage 1.Action 5 - Add forward-pass tests

Add tests covering:

- model creation;
- forward pass on default Warehouse state;
- logits shape `[robot_count, primitive_action_count]`;
- scalar value shape;
- deterministic greedy output under fixed seed.

## Phase 6 - Action Selection And Masking

### Phase 6.Stage 1.Action 1 - Implement direct action adapter

Implement direct action selection from per-robot logits.

The direct adapter must:

- sample or greedily choose one primitive action per robot;
- produce a full `WarehouseFullActionVector`;
- pass through the immediate resolver;
- record raw logits/proposal and final selected vector;
- avoid tower context and future lookahead.

This action may be implemented now even if the first runner uses tower-only, so
future paired comparison uses the same model surface.

### Phase 6.Stage 1.Action 2 - Implement tower candidate scoring adapter

Implement tower action selection by scoring concrete candidate vectors.

Required behavior:

- receive candidate concrete action vectors from existing tower surface;
- compute log-probability or score for each candidate from per-robot logits;
- sample or greedily choose a candidate;
- record candidate count;
- record selected candidate score/log probability;
- record selected full concrete action vector;
- preserve live-lift hygiene;
- avoid abstract action-head redesign.

### Phase 6.Stage 1.Action 3 - Implement entropy/log-prob helpers

Implement helpers for:

- selected action log probability;
- candidate set entropy;
- per-robot entropy if direct path is used;
- masked candidate normalization.

These values are required for actor-critic training.

### Phase 6.Stage 1.Action 4 - Implement no-lookahead assertions

Add runtime assertions or test-only sentinels proving:

- direct adapter does not receive tower context;
- neither adapter calls successor-Out inspection;
- tower live-lift remains state-lift liveness hygiene;
- resolver is immediate-only.

### Phase 6.Stage 1.Action 5 - Add action-selection tests

Add tests covering:

- direct full-vector shape;
- tower candidate selected from candidate set;
- invalid candidate rejection if relevant;
- no-lookahead boundary;
- selected action log probability exists;
- entropy is finite when candidate set has more than one candidate.

## Phase 7 - Actor-Critic Training Loop

### Phase 7.Stage 1.Action 1 - Implement rollout buffer

In `training.py`, implement an episodic rollout buffer storing:

- encoded state metadata or minimal replayable state references;
- selected action/candidate metadata;
- log probabilities;
- value estimates;
- rewards;
- done flags;
- entropy terms;
- second/time values;
- curriculum max seconds for the episode.

### Phase 7.Stage 1.Action 2 - Implement return and advantage computation

Implement discounted return and advantage computation:

```text
return_t = reward_t + gamma * return_{t+1}
advantage_t = return_t - value_t
```

Use the configured `gamma`.

### Phase 7.Stage 1.Action 3 - Implement loss computation

Implement:

```text
loss = policy_loss + value_coef * value_loss - entropy_coef * entropy
```

Record separate loss components in result tables.

### Phase 7.Stage 1.Action 4 - Implement optimizer step

Use AdamW by default.

Required behavior:

- zero gradients;
- backpropagate;
- clip gradients by `max_grad_norm`;
- step optimizer;
- increment `optimizer_steps`;
- record gradient norm if available;
- record optimizer step timing.

### Phase 7.Stage 1.Action 5 - Rename ambiguous update counters

Ensure progress and artifacts use:

```text
optimizer_steps
```

Do not use ambiguous `updates` for neural training progress.

If existing linear code still uses `updates`, do not rewrite unrelated linear
history unless necessary. Transformer output must be clear.

### Phase 7.Stage 1.Action 6 - Add training-step tests

Add tests proving:

- one short rollout produces finite loss;
- one optimizer step changes at least one parameter;
- `optimizer_steps` increments;
- loss components are recorded;
- no training test requires a long run.

## Phase 8 - Curriculum Training

### Phase 8.Stage 1.Action 1 - Implement curriculum schedule

Implement the Warehouse tower curriculum schedule:

- start max seconds: configurable;
- end max seconds: configurable;
- ramp episode count: configurable;
- flat after ramp;
- schedule tied to global episode index.

Support the prior user use case:

```text
max seconds per episode increases from 2 to 64 over 1024 curriculum positions
```

### Phase 8.Stage 1.Action 2 - Record curriculum manifest

Write:

```text
curriculum_manifest.json
```

including:

- schedule type;
- start max seconds;
- end max seconds;
- ramp episode count;
- actual episode count;
- per-episode max seconds summary;
- whether the run is tower-only.

### Phase 8.Stage 1.Action 3 - Integrate curriculum with runner

Ensure the runner uses the current episode's curriculum max seconds when
rolling out the environment.

Do not change environment-level timer semantics.

### Phase 8.Stage 1.Action 4 - Add curriculum tests

Add tests covering:

- episode 0 max seconds;
- midpoint max seconds;
- ramp endpoint max seconds;
- flat-after-ramp behavior;
- configured total shorter than ramp count.

## Phase 9 - Checkpointing

### Phase 9.Stage 1.Action 1 - Implement checkpoint save

In `checkpoints.py`, implement checkpoint writing with:

- model state dict;
- optimizer state dict;
- model config;
- optimizer config;
- training config;
- curriculum state;
- RNG state where feasible;
- episode index;
- optimizer step count;
- rolling reward summary;
- run metadata;
- dependency/device metadata.

### Phase 9.Stage 1.Action 2 - Implement checkpoint load

Implement checkpoint loading for inference.

Minimum required:

- load model weights;
- load model config;
- load selected device safely;
- run deterministic greedy inference on a supplied state.

Full training resume may be deferred only if this deferral is explicitly
recorded in the implementation log and the checkpoint format remains compatible
with future resume.

### Phase 9.Stage 1.Action 3 - Implement checkpoint policy

Support:

- periodic checkpoints;
- final checkpoint;
- best rolling reward checkpoint;
- retention of last N checkpoints;
- retention of best N checkpoints.

Recommended defaults:

```text
checkpoint_every_episodes: 100
keep_last_n_checkpoints: 5
keep_best_n_checkpoints: 3
```

### Phase 9.Stage 1.Action 4 - Write checkpoint manifest

Write:

```text
checkpoint_manifest.json
```

with:

- checkpoint ID;
- path;
- episode index;
- optimizer step count;
- reason;
- rolling reward summary;
- file size;
- checksum if cheap enough.

### Phase 9.Stage 1.Action 5 - Add checkpoint tests

Add tests proving:

- save succeeds;
- load succeeds;
- deterministic greedy inference matches before/after load for a fixed state;
- manifest rows are written;
- checkpoint retention policy keeps expected files.

## Phase 10 - Trace Retention And Movie Renderability

### Phase 10.Stage 1.Action 1 - Implement trace retention config

In `trace_retention.py`, implement support for:

- explicit `--trace-episode-index`;
- repeated trace episode flags;
- `final` trace alias;
- `--trace-every-episodes`;
- no all-episode full step CSV by default.

### Phase 10.Stage 1.Action 2 - Implement compact selected traces

Write selected episode traces only under a path such as:

```text
traces/episode_<index>/
```

Each retained trace must include enough information to render a movie later.

Do not write giant global `step_events.csv` files by default.

### Phase 10.Stage 1.Action 3 - Implement trace index

Write:

```text
results/trace_episode_index.csv
```

including:

- episode index;
- arm ID;
- replicate index;
- schema seed;
- trace path;
- reason retained;
- step count;
- renderability status.

### Phase 10.Stage 1.Action 4 - Implement missing-trace error

If the user requests a movie for an unretained episode, fail clearly with:

- requested episode;
- artifact root;
- available retained episodes;
- command hint to rerun with trace retention if appropriate.

### Phase 10.Stage 1.Action 5 - Update or extend replay renderer

Add transformer-policy rendering support.

Do not break existing render commands for old retained traces.

The renderer should be able to read the selected trace index rather than
requiring global all-episode `step_events.csv`.

### Phase 10.Stage 1.Action 6 - Add artifact size guard

Implement artifact retention accounting:

- current artifact root size;
- soft budget;
- hard budget;
- warning/failure status;
- whether raw trace writing was suppressed.

Recommended defaults:

```text
soft budget: 500 MB
hard budget: 2 GB
```

### Phase 10.Stage 1.Action 7 - Write artifact retention manifest

Write:

```text
artifact_retention_manifest.json
```

including:

- retention policy;
- selected trace policy;
- artifact root size;
- soft/hard budget status;
- whether any large raw traces were intentionally skipped.

### Phase 10.Stage 1.Action 8 - Add trace and movie tests

Add tests proving:

- selected episodes are retained;
- unselected episodes are not retained;
- retained episode movie render succeeds;
- unretained episode render fails clearly;
- no all-episode giant `step_events.csv` is produced by default.

## Phase 11 - Runner And CLI

### Phase 11.Stage 1.Action 1 - Implement tower-only transformer runner

In `runner.py`, implement a tower-only curriculum runner.

Required behavior:

- load Warehouse readiness source;
- construct environment instance;
- construct tower surface;
- construct transformer model;
- construct optimizer;
- run configured episodes;
- apply curriculum;
- use live-lift candidate scoring;
- write summaries, manifests, checkpoints, and selected traces;
- show progress with reward first.

### Phase 11.Stage 1.Action 2 - Implement optional direct path

Implement the direct transformer path sufficiently for tests and future paired
comparison.

Do not require direct arm execution in the first tower-only curriculum command.

### Phase 11.Stage 1.Action 3 - Add CLI parser

Add:

```text
warehouse-gridlock transformer-policy run
warehouse-gridlock transformer-policy summarize
warehouse-gridlock transformer-policy render-episode
```

The CLI must follow existing JSON status-output style.

### Phase 11.Stage 1.Action 4 - Add run CLI flags

Required run flags:

- `--repo-root`;
- `--artifact-root`;
- `--readiness-source`;
- `--run-label`;
- `--locked-by`;
- `--episodes`;
- `--replicates`;
- `--schema-seeds`;
- `--max-seconds-start`;
- `--max-seconds-end`;
- `--curriculum-ramp-episodes`;
- `--checkpoint-every-episodes`;
- `--trace-episode-index`;
- `--trace-every-episodes`;
- `--progress-every-episodes`;
- `--device`;
- `--seed`;
- artifact budget flags.

If local naming strongly prefers `episodes-per-arm`, preserve local style but
make tower-only semantics unambiguous.

### Phase 11.Stage 1.Action 5 - Add summarize command

The summarize command must:

- read transformer artifacts;
- aggregate episode and checkpoint summaries;
- write repository readout files;
- write or update `readout_source.json`;
- not rerun training.

### Phase 11.Stage 1.Action 6 - Add render command

The render command must:

- use selected trace index;
- render retained episode GIF;
- report output path;
- fail clearly for missing trace episodes.

### Phase 11.Stage 1.Action 7 - Add progress bar behavior

Ensure progress display fields are ordered with reward first:

```text
reward=<latest> rolling=<mean> optimizer_steps=<n> episode=<i>/<n> max_seconds=<s> arm=<short>
```

Avoid long arm IDs pushing reward off-screen.

### Phase 11.Stage 1.Action 8 - Add CLI tests

Add tests proving:

- CLI help works without Torch;
- transformer command handles missing Torch clearly;
- run smoke works when Torch is available;
- summarize writes readout source;
- render retained episode works.

## Phase 12 - Manifests And Result Tables

### Phase 12.Stage 1.Action 1 - Implement evaluation manifest

Write:

```text
evaluation_manifest.json
```

including:

- evaluation ID;
- run label;
- claim boundary;
- model family ID;
- arm IDs;
- environment ID;
- source documents;
- no-lookahead statement.

### Phase 12.Stage 1.Action 2 - Implement dependency manifest

Write:

```text
dependency_manifest.json
```

including:

- BBB version/provenance;
- `state_collapser` version/provenance;
- Python version;
- Torch availability/version;
- device;
- optional CUDA status.

### Phase 12.Stage 1.Action 3 - Implement model and optimizer manifests

Write:

```text
transformer_model_manifest.json
optimizer_manifest.json
```

including:

- model family ID;
- architecture config;
- parameter count;
- token vocabulary;
- primitive action vocabulary;
- optimizer type;
- optimizer hyperparameters;
- loss coefficients.

### Phase 12.Stage 1.Action 4 - Implement policy contract manifest

Write:

```text
policy_contract_manifest.json
```

including:

- full-state/full-action contract;
- immediate masking;
- no one-hop lookahead;
- live-lift state-liveness boundary;
- direct context boundary;
- tower context boundary.

### Phase 12.Stage 1.Action 5 - Implement required result tables

Write:

```text
results/episode_summary.csv
results/training_curve_summary.csv
results/checkpoint_summary.csv
results/trace_episode_index.csv
results/resolver_summary.csv
results/tower_live_lift_summary.csv
results/curriculum_summary.csv
results/timing_summary.csv
results/artifact_retention_summary.csv
```

Each table must be stable enough for the human-readable protocol.

### Phase 12.Stage 1.Action 6 - Implement run index

Write a compact run index that points to:

- arm ID;
- replicate;
- schema seed;
- episode summary path;
- checkpoint manifest path;
- selected trace index path;
- status.

Do not make movie rendering depend on a giant global step-event table.

## Phase 13 - Human-Readable Readout Source

### Phase 13.Stage 1.Action 1 - Implement docs writer

In `docs_writer.py`, implement writing:

```text
docs/evaluations/warehouse_gridlock_001/transformer_policy/readout_source.json
```

and any immediate generated report scaffolding required by existing local
readout conventions.

### Phase 13.Stage 1.Action 2 - Include protocol command hint

The readout source or generated README should preserve the correct protocol
invocation:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/transformer_policy/readout_source.json
```

Do not tell the user to point the protocol at the artifact directory.

### Phase 13.Stage 1.Action 3 - Include readable status fields

The readout source must expose enough fields for a human-readable report to
answer:

- model type;
- whether this was transformer or linear;
- whether optimizer steps occurred;
- reward trajectory;
- checkpoint availability;
- retained movie episodes;
- artifact retention status;
- no-lookahead status;
- live-lift status;
- claim boundary.

### Phase 13.Stage 1.Action 4 - Add readout-source tests

Add tests proving:

- `readout_source.json` exists after summarize;
- source paths are repo-relative or repository-local;
- required tables are present;
- protocol target is the readout source file.

## Phase 14 - Tower Curriculum Script

### Phase 14.Stage 1.Action 1 - Add dedicated transformer curriculum script

Create:

```text
scripts/run_warehouse_gridlock_tower_transformer_curriculum_train.sh
```

Do not overwrite the existing linear curriculum script unless the Project Owner
explicitly asks.

### Phase 14.Stage 1.Action 2 - Script defaults

Script defaults should include:

- tower-only arm;
- transformer policy command;
- repo artifact root under transformer readout family;
- configurable `RUN_LABEL`;
- configurable `EPISODES`;
- configurable `MAX_SECONDS_START`;
- configurable `MAX_SECONDS_END`;
- configurable `CURRICULUM_RAMP_EPISODES`;
- checkpoint interval;
- selected trace episodes;
- progress output enabled.

### Phase 14.Stage 1.Action 3 - Script safety

The script must:

- `set -euo pipefail`;
- print artifact root;
- print readout source path after summarize;
- not run a huge default episode count unless explicitly configured.

### Phase 14.Stage 1.Action 4 - Script smoke test

Run the script with a tiny smoke override only if Torch is available:

```text
EPISODES=2 RUN_LABEL=tower_transformer_smoke_001 scripts/run_warehouse_gridlock_tower_transformer_curriculum_train.sh
```

Do not run a long 512, 2024, or 100000 episode training session during
implementation unless the Project Owner explicitly asks.

## Phase 15 - Test Execution

### Phase 15.Stage 1.Action 1 - Run targeted non-ML tests

Run relevant non-ML tests, including:

```text
uv run pytest tests/environments/warehouse_gridlock/test_warehouse_gridlock_graph.py
uv run pytest tests/environments/warehouse_gridlock/test_warehouse_gridlock_state_action.py
uv run pytest tests/environments/warehouse_gridlock/test_warehouse_gridlock_transition.py
uv run pytest tests/environments/warehouse_gridlock/test_masked_direct_vs_live_lift_tower.py
```

Record results in the implementation log.

### Phase 15.Stage 1.Action 2 - Run transformer ML-gated tests

Run transformer tests.

If Torch is unavailable, tests must skip clearly rather than fail due to import
errors.

Record whether the tests ran or skipped.

### Phase 15.Stage 1.Action 3 - Run CLI help test

Run:

```text
uv run python -m big_boy_benchmarking.cli --help
uv run python -m big_boy_benchmarking.cli warehouse-gridlock --help
```

Record results.

### Phase 15.Stage 1.Action 4 - Run smoke training only

If Torch is available, run a tiny transformer tower-only smoke:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock transformer-policy run \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/transformer_policy/artifacts/tower_transformer_smoke_001 \
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \
  --run-label tower_transformer_smoke_001 \
  --locked-by foster \
  --episodes 2 \
  --replicates 1 \
  --schema-seeds 1 \
  --max-seconds-start 2 \
  --max-seconds-end 4 \
  --curriculum-ramp-episodes 2 \
  --checkpoint-every-episodes 1 \
  --trace-episode-index 0 \
  --trace-episode-index final \
  --progress-every-episodes 1
```

If this command is too slow or fails due to design mismatch, stop and report the
exact blocker.

### Phase 15.Stage 1.Action 5 - Run summarize smoke

Run:

```text
uv run python -m big_boy_benchmarking.cli warehouse-gridlock transformer-policy summarize \
  --repo-root . \
  --artifact-root docs/evaluations/warehouse_gridlock_001/transformer_policy/artifacts/tower_transformer_smoke_001
```

Verify:

- readout source exists;
- required result tables exist;
- checkpoint manifest exists;
- trace index exists.

### Phase 15.Stage 1.Action 6 - Run retained movie smoke

Render one retained smoke episode.

Verify:

- GIF file exists;
- renderer does not require deleted/global all-episode CSVs;
- unretained episode request fails clearly.

### Phase 15.Stage 1.Action 7 - Run broader targeted suite

Run:

```text
uv run pytest tests/environments/warehouse_gridlock
```

If test time is excessive, run targeted files first and record the limitation.

### Phase 15.Stage 1.Action 8 - Run formatting/lint if local style requires

Run the repository's normal formatting/lint checks if they exist and are
appropriate.

At minimum, run tests sufficient to verify this workplan's touched code paths.

## Phase 16 - Documentation And Root Surface Updates

### Phase 16.Stage 1.Action 1 - Update design discussion only if needed

Do not rewrite the design discussion as an implementation report.

Only add a short note if execution reveals a correction that future readers must
see before the implementation log.

### Phase 16.Stage 1.Action 2 - Update evaluation README via protocol source

Do not manually fabricate a final human-readable report unless the protocol
requires manual generation.

The intended post-summarize prompt is:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/transformer_policy/readout_source.json
```

### Phase 16.Stage 1.Action 3 - Update root docs only if the smoke surface is real

Only update root README or evaluation index after:

- transformer smoke run succeeds;
- summarize succeeds;
- readout source exists;
- the claim boundary is clear.

Do not claim serious benchmark evidence from a two-episode smoke run.

### Phase 16.Stage 1.Action 4 - Add pitfalls note only if a new pitfall is learned

If execution discovers a generalizable issue, add it to the appropriate design
or pitfall document with clear attribution.

Do not add generic commentary.

## Phase 17 - Final Verification And Handoff

### Phase 17.Stage 1.Action 1 - Verify no accidental `state_collapser` edits

Check that no files under `<state_collapser-repo>` were modified by this
workplan execution.

Record the check in the implementation log.

### Phase 17.Stage 1.Action 2 - Verify no giant raw CSV defaults

Check the transformer artifact root for large all-episode CSVs.

Default execution should not create giant global trace files.

Record:

- largest files;
- total artifact size;
- retained trace episodes;
- checkpoint sizes.

### Phase 17.Stage 1.Action 3 - Verify protocol target

Confirm:

```text
docs/evaluations/warehouse_gridlock_001/transformer_policy/readout_source.json
```

is the correct human-readable protocol target.

### Phase 17.Stage 1.Action 4 - Verify git status

Record:

- modified files;
- added files;
- untracked files;
- generated artifacts;
- files intentionally left untracked.

Do not stage or commit unless the Project Owner asks.

### Phase 17.Stage 1.Action 5 - Complete implementation log

Finalize the log with:

- completed phases;
- test results;
- smoke run result;
- known limitations;
- stop conditions avoided or encountered;
- exact commands for future longer run if the Project Owner asks.

### Phase 17.Stage 1.Action 6 - Final response

When reporting completion, include:

- path to implementation log;
- path to new transformer readout source;
- whether Torch was available;
- whether smoke training ran;
- whether movie rendering was verified;
- whether any long run was intentionally not run;
- exact next command only if the Project Owner asks.

Do not overclaim results.

## Mandatory Stop Conditions

Stop and ask the Project Owner if any of these occur:

- Torch cannot be imported in the ML path and installing it requires approval;
- base package import starts requiring Torch;
- CLI help requires Torch;
- implementation would alter Warehouse environment semantics;
- implementation would alter reward constants;
- implementation would alter invalid ensemble semantics;
- direct arm receives tower-only context;
- either arm receives one-hop successor-Out lookahead;
- live-lift becomes action lookahead instead of state-lift liveness;
- existing tower surface cannot supply candidate concrete vectors;
- transformer action selection requires an abstract-action-head redesign;
- selected-trace rendering cannot be made independent of giant global CSVs;
- checkpoint load cannot reproduce deterministic inference for a fixed state;
- artifact retention cannot avoid giant all-episode traces by default;
- smoke training cannot run without simplifying the blueprint;
- tests would require a long training run;
- any action must be replaced with a smaller substitute to proceed.

## Explicit Non-Goals

Do not do these under this workplan:

- do not implement PPO unless the Project Owner separately approves it;
- do not create a production RL framework;
- do not modify `state_collapser`;
- do not change Warehouse Gridlock physics;
- do not change reward constants;
- do not rerun old linear reports as though they were transformer reports;
- do not run long 512, 2024, or 100000 episode experiments by default;
- do not commit large checkpoints or raw trace dumps without explicit approval;
- do not make broad tower-superiority claims from smoke results.

## Completion Criteria

This workplan is complete when:

- optional Torch dependency/import gating is implemented;
- transformer package exists with real modules;
- full-state Warehouse encoding exists and is tested;
- transformer actor-critic forward pass exists and is tested;
- direct and tower action adapters exist and are tested;
- tower candidate scoring preserves no-lookahead semantics;
- actor-critic optimizer step exists and is tested;
- `optimizer_steps` replaces ambiguous neural training update language;
- curriculum schedule exists and is tested;
- checkpoint save/load exists and is tested;
- selected trace retention exists and is tested;
- retained movie rendering works without global all-episode CSVs;
- transformer CLI run/summarize/render commands exist;
- tower-only transformer smoke run completes when Torch is available;
- readout source exists at the transformer readout path;
- implementation log records all completed work and test results;
- no `state_collapser` files were modified.
