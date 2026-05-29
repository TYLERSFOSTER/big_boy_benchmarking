# State Collapser Tensorization Resume Note

Date: 2026-05-29

Status: design note for resuming benchmark planning

## Purpose

This note records that the upstream `state_collapser` tensorization prerequisite
identified in the earlier alignment discussion has now been implemented.

The relevant upstream alignment note was:

```text
/Users/foster/state_collapser/docs/design/model_train_surfaces/01_005_big_boy_benchmarking_tensorization_alignment_note.md
```

That note said `big_boy_benchmarking` should not yet claim serious
tensor-off/tensor-on benchmark evidence because `state_collapser` did not yet
have a tensor-capable architecture with explicit disabled/enabled modes.

That blocker has now moved from "not implemented" to "implemented upstream,
ready to be integrated into benchmark design."

## Upstream State Collapser Status

The relevant upstream `state_collapser` work landed on:

```text
main
```

at:

```text
7b5d0fd tensorization/lineariztion implemented
```

The implemented upstream files include:

```text
src/state_collapser/training/linearization.py
src/state_collapser/training/torch.py
docs/usage/01_010_tensorization_boundary.md
docs/design/tensorization/01_004_tensorization_implementation_log.md
```

The core implemented surfaces are:

```python
from state_collapser.training import EncodingRegistry
from state_collapser.training import LinearizationConfig
from state_collapser.training import LinearizationReport
from state_collapser.training import LinearizationState
from state_collapser.training import LinearizedActionSelectionInput
from state_collapser.training import LinearizedTrainingTransition
from state_collapser.training import NumericBackend
from state_collapser.training import TensorDeviceKind
from state_collapser.training import build_linearization_report
from state_collapser.training import linearize_action_selection_input
from state_collapser.training import linearize_training_transition
```

The optional Torch-facing surfaces are:

```python
from state_collapser.training.torch import TorchDecisionBatch
from state_collapser.training.torch import TorchTransitionBatch
from state_collapser.training.torch import action_decision_from_logits
```

## The Important Benchmark Distinction Now Exists

The benchmark modes discussed in the earlier alignment note now have an upstream
representation.

The upstream mode fields are:

```text
LinearizationState = ABSENT | PRESENT_DISABLED | PRESENT_ENABLED
NumericBackend = NONE | NUMPY | TORCH
TensorDeviceKind = NONE | CPU | CUDA
```

The derived benchmark labels are:

```text
none_control_flow
tensor_available_disabled
tensor_enabled_cpu
tensor_enabled_cuda
```

This directly answers the earlier benchmark requirement:

```text
pre-linearization/current control-flow behavior
tensor-capable architecture with tensor path disabled
tensor-capable architecture with tensor path enabled
```

The important engineering detail is that `PRESENT_DISABLED` is not supposed to
construct tensors on the hot path. It records and validates that the
tensor-capable boundary exists while leaving the object-native runtime direct.

## Why This Matters For Big Boy Benchmarking

Before this upstream work, `big_boy_benchmarking` could only compare:

```text
old object-native state_collapser behavior
```

against future imagined tensorization.

That was not a valid tensor-off/tensor-on ablation, because the tensor-capable
boundary itself did not exist.

After this upstream work, `big_boy_benchmarking` can design benchmark conditions
that distinguish:

```text
none_control_flow
tensor_available_disabled
tensor_enabled_cpu
tensor_enabled_cuda
```

as machine-readable conditions in benchmark artifacts.

This does not mean the serious benchmark is already implemented. It means the
benchmark can now be designed against a real upstream mode vocabulary.

## What Upstream Implemented

Upstream `state_collapser` now provides a backend-independent linearization
boundary:

```text
ActionSelectionInput
    -> LinearizedActionSelectionInput
TrainingTransition
    -> LinearizedTrainingTransition
```

It also provides an optional Torch boundary:

```text
LinearizedActionSelectionInput
    -> TorchDecisionBatch
LinearizedTrainingTransition
    -> TorchTransitionBatch
```

The key benchmark/reporting object is:

```text
LinearizationReport
```

It records:

- linearization state,
- numeric backend,
- device kind,
- derived benchmark label,
- backend availability,
- dtype and mask dtype,
- NumPy availability,
- Torch availability,
- CUDA availability,
- encoder registry id,
- tower fingerprint,
- maximum tower depth,
- maximum action count,
- conversion count,
- conversion elapsed seconds,
- and whether debug records were exported.

## What Upstream Deliberately Did Not Implement

The upstream tensorization work does not implement:

- PPO,
- DQN,
- SAC,
- replay buffers,
- vectorized rollout,
- checkpoint/resume,
- distributed rollout,
- full ragged tensor support,
- HGraphML tensorized message passing,
- or a mature RL framework.

`big_boy_benchmarking` must not treat the upstream work as a mature RL stack.

It should treat it as:

```text
the first real semantic-to-numeric boundary needed for benchmarkable
tensor-capable modes
```

## Immediate Big Boy Benchmarking Implications

The next `big_boy_benchmarking` design pass should update benchmark mode and
artifact planning so that every run can record a linearization section.

The minimum artifact fields should include:

```text
linearization_config
linearization_report
benchmark_mode
linearization_state
numeric_backend
tensor_device_kind
conversion_count
conversion_elapsed_seconds
backend_available
torch_available
cuda_available
```

These fields should come from upstream `state_collapser` config/report objects
where possible rather than being guessed from local benchmark code.

## Immediate Resume Gate

Before serious benchmark implementation resumes, `big_boy_benchmarking` should
confirm that its installed `state-collapser` dependency exposes:

```python
state_collapser.training.LinearizationConfig
state_collapser.training.LinearizationReport
state_collapser.training.LinearizationState
state_collapser.training.NumericBackend
state_collapser.training.TensorDeviceKind
state_collapser.training.build_linearization_report
```

If these imports fail, the local dependency pin is stale.

Do not reimplement these objects in `big_boy_benchmarking`.

Update the `state-collapser` dependency pin to a commit/tag that contains them.

## Proposed Next Design Work In This Repo

The next benchmark design document should answer:

1. Which benchmark modes are runnable now?
2. Which modes are reserved until Torch is available in the benchmark
   environment?
3. Does `tensor_available_disabled` simply build reports, or does it also
   validate registry construction?
4. Where do `LinearizationConfig` and `LinearizationReport` appear in the
   artifact schema?
5. Which runner owns conversion timing?
6. How should conversion timing be separated from environment step, tower
   update, learner action, learner update, and artifact writing?
7. What is the first fair CPU tensor-enabled comparison?
8. What exact evidence is needed before any CUDA claim?

## Proposed Implementation Work In This Repo

The first implementation slice should probably add:

- an upstream dependency-state test for the new tensorization imports,
- artifact schema fields for linearization config/report,
- benchmark mode registry entries for the four derived labels,
- a disabled-mode runner path that records reports without constructing tensors,
- a CPU-enabled smoke runner path if Torch is available,
- and tests proving reserved modes are rejected unless explicitly allowed.

This should be gameplanned separately before source edits.

## Validation Evidence From Upstream

The upstream implementation recorded:

```text
uv run ruff check
All checks passed.
```

```text
uv run mypy
Success: no issues found in 100 source files.
```

```text
uv run pytest
477 passed, 4 skipped
```

Torch-specific tests were collected but skipped locally because Torch was not
installed in the upstream local environment.

That means `big_boy_benchmarking` should still perform its own Torch-installed
validation before treating `tensor_enabled_cpu` as runnable.

## Current Status Summary

The earlier blocker was:

```text
state_collapser lacks explicit tensor-capable disabled/enabled architecture
```

The current status is:

```text
state_collapser now exposes the first explicit tensorization boundary and mode
vocabulary needed by big_boy_benchmarking
```

The next blocker is now local to this repo:

```text
big_boy_benchmarking needs to integrate those upstream reports and mode labels
into benchmark modes, artifact schemas, and runner contracts
```

No serious tensor-off/tensor-on benchmark claim should be made until that local
integration work is designed, implemented, and validated.

## BBB Local Integration Status

Updated: 2026-05-29

The local BBB integration work is now being executed under:

```text
docs/design/shared_benchmark_machinery/01_005_state_collapser_v0_7_tensorization_integration_gameplan.md
```

The running implementation log is:

```text
docs/design/shared_benchmark_machinery/01_006_state_collapser_v0_7_tensorization_integration_implementation_log.md
```

This update does not rewrite the earlier pause history. The Project Owner's
methodological correction remains the reason the serious counterpoint
evaluation paused. The purpose of the current integration is to make BBB
artifacts record the now-available `state_collapser v0.7.0` linearization
condition before serious counterpoint evaluation resumes.
