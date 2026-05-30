# Counterpoint Symbolic V001

Source blueprint:

- `docs/design/first_counterpoint_environment/01_002_counterpoint_hidden_graph_and_contraction_schema_benchmark_blueprint.md`

Implementation gameplan:

- `docs/design/first_counterpoint_environment/01_003_counterpoint_hidden_graph_and_contraction_schema_implementation_gameplan.md`

First serious learning design:

- `docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md`
- `docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_001_counterpoint_first_serious_learning_evaluation_blueprint.md`
- `docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_002_counterpoint_first_serious_learning_evaluation_implementation_gameplan.md`

## Family Identity

Family id:

```text
counterpoint_symbolic_v001
```

This is a benchmark-owned finite hidden state/action graph family. It is
counterpoint-like, but the benchmark object is not musical quality. The object
is a fixed symbolic RL graph with swappable contraction schemata.

## Hidden Geometry

State:

```text
pitches: tuple[int, ...]
beat_index: int
```

Action:

```text
deltas: tuple[int, ...]
```

Transition applies one simultaneous pitch delta per voice and advances
`beat_index` modulo `measure_size`. The first concrete fixtures use
`voice_count = 3`, but voice count is an instance parameter rather than a family
boundary.

## Contracts

Versioned ids:

```text
legality_contract_id: counterpoint_legality_local_v001
reward_bundle_id: counterpoint_reward_local_v001
edge_label_contract_id: counterpoint_edge_labels_local_v001
initial_state_policy_id: counterpoint_initial_states_v001
terminal_policy_id: counterpoint_terminal_horizon_v001
action_mask_policy_id: counterpoint_legal_action_mask_v001
```

Legality checks pitch band, strict voice order, interval classes, root interval,
outer span, beat index, delta bounds, stationary policy, and forbidden parallel
interval classes.

Reward is local/action-local in v001. Term diagnostics are emitted separately
from edge labels. Edge labels are structural labels, not reward outcomes.

## Scale Ladder

Implemented first fixtures:

- `counterpoint_symbolic_n3_tiny_v001`
- `counterpoint_symbolic_n3_small_v001`

For the first serious learning evaluation, `small` is the serious fixture and
`tiny` is smoke only.

Reserved future tiers:

- medium
- large
- stress

This implementation does not make medium, large, or stress performance claims.

## Schema Candidates

Implemented schema families:

- `counterpoint_empty_schema_v001`
- `counterpoint_random_balanced_schema_v001`
- `counterpoint_random_unbalanced_schema_v001`
- `counterpoint_motion_schema_v001`
- `counterpoint_projection_audit_schema_v001`
- `counterpoint_bad_schema_v001`

Leakage discipline: online-eligible schemata must not read reward outcomes,
terminal outcomes, learned values, or future episode results. The projection
audit schema is diagnostic-only under the first Phase 1 decision lock.

## Quotient Hypothesis

Flat search is wasteful because legal path volume grows by branching over
fine-grained simultaneous voice moves. The benchmark asks whether contraction
schemata create useful quotient addresses, lift fibers, and reward-compatible
cells on the same underlying graph.

Primary artifacts remain the source of truth.

## Serious Learning Surface

The first serious learning/control surface compares direct environment arms
with active-tier exploit/explore tower-control arms. The tower-control mode id
is:

```text
tower_exploit_explore
```

The matrix keeps these separate:

- direct environment training;
- empty-schema tower-control training;
- nonempty-schema tower-control training.

This environment doc does not claim a serious result has been run. Result docs,
when generated from artifacts, belong under:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/
```
