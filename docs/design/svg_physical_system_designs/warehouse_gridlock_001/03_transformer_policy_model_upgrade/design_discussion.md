# Warehouse Gridlock Transformer Policy Model Upgrade Design Discussion

## Status

Initial design discussion surface.

This folder exists because the current Warehouse Gridlock full-state/full-action
policy contract is real, but the model currently installed behind that contract
is still deliberately minimal:

```text
warehouse_linear_factorized_softmax_policy_v001
```

That model receives the full Warehouse system configuration plus the current
second and emits or scores full simultaneous action vectors, but it does so by
hand-coded linear features. It is trainable, but it is not a transformer, not a
neural policy, and not a serious sequence/set model for coordinated warehouse
control.

The purpose of this design block is to upgrade the policy model while preserving
the environment, artifact, and fairness machinery already built.

## Source Documents

Read this design discussion beside:

```text
docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_001_warehouse_gridlock_environment_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_masked_direct_vs_live_lift_tower_no_lookahead/01_001_warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/02_full_state_full_action_trainable_policy_contract/01_001_warehouse_gridlock_full_state_full_action_trainable_policy_contract_blueprint.md
docs/design/svg_physical_system_designs/warehouse_gridlock_001/02_full_state_full_action_trainable_policy_contract/01_002_warehouse_gridlock_full_state_full_action_trainable_policy_contract_implementation_workplan.md
docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/README.md
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
```

Current implementation surfaces:

```text
src/big_boy_benchmarking/environments/warehouse_gridlock/policies/
src/big_boy_benchmarking/environments/warehouse_gridlock/full_state_policy_comparison/
scripts/run_warehouse_gridlock_tower_curriculum_train.sh
tests/environments/warehouse_gridlock/test_full_state_policy_contract.py
```

## Attribution

### Project Owner

The Project Owner identified the current mismatch:

```text
The policy contract was upgraded, but the installed policy model is still only
a linear feature model. The next model upgrade should use a transformer-style
policy.
```

The Project Owner also previously locked the model boundary that this upgrade
must preserve:

```text
Every model should get full system config and second number as input, and
should give full action vector output.
```

This design block treats that as the governing requirement.

### Codex

Codex previously implemented the minimal full-state/full-action trainable
policy contract and then clarified that the installed model was:

```text
warehouse_linear_factorized_softmax_policy_v001
```

Codex's current role in this folder is to help specify the transformer upgrade
without falsely attributing decisions to the Project Owner and without
reopening the already-set Warehouse environment mechanics.

## Current Reality

The current runner is useful because it proves the model contract is wired:

```text
full Warehouse config + current second -> full simultaneous robot action vector
```

The current model is insufficient because its inference path is only:

```text
linear hand-coded features -> command/action-vector scores
```

For the direct arm, the model samples per-robot commands from linear feature
scores and then the immediate admissibility resolver repairs or masks invalid
vectors.

For the tower arm, the current model scores generated tower candidate
realizations using the same learned feature weights, then selects the highest
scoring candidate and resolves it at the concrete environment boundary.

That is trainable, but it is not the model we want for serious Warehouse
learning.

## Design Goal

Replace the linear feature policy with a transformer-style policy model that
can represent coordinated multi-robot behavior while preserving:

- the Warehouse Gridlock environment;
- synchronous full action vectors;
- immediate inadmissibility masking;
- no one-hop successor-state cul-de-sac lookahead;
- live-lift hygiene for tower state lifting;
- existing artifact contracts where possible;
- readable run/evaluation reports;
- movie rendering from recorded step events.

The model should be able to learn from the same information surface in both
arms:

```text
full static config
full dynamic state
current second
robot identities
box identities
targets
blocked nodes
occupancy
graph connectivity or local adjacency
```

The output must remain:

```text
R01 -> north | south | east | west | stay
R02 -> north | south | east | west | stay
...
R32 -> north | south | east | west | stay
```

## Proposed Transformer Shape

The likely model should treat Warehouse state as a structured set/sequence:

- robot tokens;
- box tokens;
- target tokens or target attributes;
- obstacle/blocked-node tokens or grid-position embeddings;
- optional edge/local-neighborhood tokens;
- a time/second token;
- optional tier/tower context tokens for the tower arm.

The transformer should produce action logits for every robot:

```text
num_robots x 5 command logits
```

The immediate admissibility resolver may still be used after raw action
generation, but the model should also receive training signal from whether its
raw output was already valid or needed projection.

## Direct Arm Inference Boundary

The direct transformer arm should be:

```text
encode full concrete Warehouse state
produce logits for all robots
sample or select one full action vector
apply immediate admissibility resolver
execute selected full concrete vector
update model
```

It must not query successor `Out` counts for lookahead.

## Tower Arm Inference Boundary

The tower transformer arm needs a careful choice.

Possible shape A:

```text
encode full concrete Warehouse state plus tower/tier metadata
score generated concrete candidate realizations
select candidate action vector
resolve immediately
execute
update model
```

Possible shape B:

```text
encode abstract/tier state plus concrete lift context
emit abstract/tier action
realize concrete action vector
resolve immediately
execute
update model
```

Possible shape A is likely safer for the first transformer upgrade because it
preserves the current full concrete action-vector boundary and minimizes tower
redesign.

## Training Questions

The immediate design questions are:

1. Should the first transformer policy use PyTorch as a required dependency,
   or should it live behind an optional extra?
2. Should we keep REINFORCE-style policy-gradient updates initially, or move
   immediately to actor-critic/value-baseline machinery?
3. Should the model train online inside the current runner, or should the
   runner record batches and a separate trainer update checkpoints?
4. Should checkpoints be written every N episodes so interrupted 100k runs are
   recoverable?
5. Should per-episode step traces be flushed incrementally so long runs are
   movie-renderable before the whole arm finishes?
6. Should the tower arm score generated candidate vectors first, or emit its
   own full vector and use tower structure only as auxiliary context?

## Artifact And Runtime Pressure

Recent long Warehouse curriculum runs showed that artifacts can explode.

The `tower_curriculum_train_2024_001` run produced roughly gigabyte-scale CSV
artifacts because high-frequency event streams are written both at run level
and evaluation-result level. The transformer upgrade should not blindly carry
that artifact policy forward for 100k-episode training.

Likely required changes before serious transformer training:

- compressed event tables for large runs;
- summary-first artifact mode;
- optional full trace sampling;
- explicit movie episode selection/checkpointing;
- incremental flushing of completed episode traces;
- checkpoint writing for model state;
- separate small readout artifacts from heavy raw train artifacts.

## First Codex Recommendation

Do not start by trying to design the full final transformer benchmark.

Start with a narrow transformer-policy upgrade blueprint:

```text
same Warehouse environment
same full-state/full-action policy contract
same tower-only curriculum script shape
replace linear policy with transformer policy
write checkpoints
flush completed episode traces incrementally
keep artifact growth controlled
prove one small run can learn and render movies
```

Then use that as the basis for direct-vs-tower transformer comparison later.

## Turn Conversation

### Project Owner Turn

### Codex Turn
