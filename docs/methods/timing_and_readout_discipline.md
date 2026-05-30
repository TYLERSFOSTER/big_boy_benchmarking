# Timing And Readout Discipline

Timing must distinguish algorithm cost from benchmark bookkeeping.

Artifact logging, compatibility readouts, morphism construction, posthoc
diagnostics, and summary generation are separate timing categories.

Tensorization integration adds separate timing segments for:

```text
linearization_report_build
encoding_registry_build
linearize_action_selection
linearize_training_transition
torch_decision_batch_build
torch_transition_batch_build
tensor_policy_forward
tensor_action_decode
```

These must not be hidden under environment step, tower update, learner action,
learner update, compatibility readout, or artifact logging.

Compatibility readouts and morphism construction are not default hot-path
costs. A run must record whether readout or morphism construction was requested
and whether either actually occurred.

The serious counterpoint tower-control runner records active online costs as
separate segments:

```text
environment_reset
environment_step
tower_reset
controller_decision
lift_resolve
learner_act
learner_update
artifact_logging
```

Compatibility readout and morphism construction remain excluded from the
default online hot path.

See also:

```text
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
docs/methods/counterpoint_serious_learning.md
```
