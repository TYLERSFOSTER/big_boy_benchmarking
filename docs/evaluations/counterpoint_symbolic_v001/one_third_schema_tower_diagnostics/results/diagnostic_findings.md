# Diagnostic Findings

## Finding 1: The First Projection Fully Collapses

All `24` runs are classified as `full_first_projection_collapse`. The
evaluation-level tower shape table shows:

- small: state cells by tier `(108, 1, 1, 1)`;
- medium: state cells by tier `(228, 1, 1, 1)`.

Tier `0` is the base/fine hidden graph. Tier `1` is the first coarser quotient
tier. A tier-`1` state-cell count of `1` means every base state is in the same
tier-`1` fiber. The largest state-fiber share is `1.0` for tier `1` on every
run.

Interpretation: the one-third schema creates a structural-limit case. The run
can diagnose quotient geometry and runtime behavior, but it cannot support
ordinary tower-learning performance claims.

Evidence:

```text
evaluation_aggregate_table.csv
results/tower_shape_summary.csv
```

## Finding 2: The One-Third Blocks Exist But Do Not Preserve State Structure

The schema block table shows nonempty source-local one-third blocks on both
instances. For small, block shares are approximately `35.79%`, `23.86%`,
`17.89%`, and `22.46%` unscheduled. For medium, they are approximately
`35.87%`, `23.57%`, `16.25%`, and `24.30%` unscheduled.

That confirms the schema construction did not fail. The collapse is not because
the schema is empty. It is because the induced quotient structure connects the
base graph so broadly that tier `1` becomes one state cell.

Evidence:

```text
results/schema_block_summary.csv
results/tower_shape_summary.csv
```

## Finding 3: ABC Evidence Is Present And Action-Consistent

The ABC selection summary contains `4800` events and `4800` action-consistent
events. The main split is:

- `2886` events at an executable selected context;
- `1914` events with `no_executable_unclosed`;
- `2418` explore events;
- `1422` exploit/execute events;
- `960` train events.

This is a runtime visibility success: BBB is capturing the upstream ABC
decision context. It is also a diagnostic warning: the coarser unclosed tiers
are not executable targets in this collapsed shape, so selection evidence must
not be read as useful higher-tier control.

Evidence:

```text
results/abc_selection_summary.csv
results/abc_tier_signal_summary.csv
results/control_action_summary.csv
```

## Finding 4: Lift And Concrete Execution Succeed At Tier 0

The lift table records `3840` attempts, `3840` successes, and `0` failures.
The concrete step table records `3840` concrete steps and `384` normally
terminated episodes.

This means the base-tier path is executable. The structural limit is quotient
collapse, not an inability to lift selected actions into concrete counterpoint
transitions.

Evidence:

```text
results/lift_failure_by_tier.csv
results/concrete_step_summary.csv
```

## Finding 5: Timing Is Descriptive Only

The timing summaries cover setup and online runtime for this diagnostic path:

- total recorded time: `26.743908` seconds;
- linearization setup: `2.311357` seconds;
- algorithm online: `24.432552` seconds.

The mode excludes morphism construction and compatibility readouts. Timing is
therefore useful for run planning and sanity checks, not for method-speed
claims.

Evidence:

```text
runs/counterpoint_symbolic_v001_one_third_schema_tower_diagnostics_v001/runs/*/timing_summary.json
runs/counterpoint_symbolic_v001_one_third_schema_tower_diagnostics_v001/runs/*/mode_manifest.json
```
