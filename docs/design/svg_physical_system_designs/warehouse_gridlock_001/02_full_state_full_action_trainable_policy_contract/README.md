# Warehouse Gridlock Full-State Full-Action Trainable Policy Contract

## Purpose

This folder is for designing the correction from the current Warehouse Gridlock
masked candidate/controller diagnostic to a real trainable policy comparison.

The immediate motivation is that the current Warehouse masked direct vs.
live-lift tower evaluation records learner updates, but those updates do not
meaningfully drive later behavior. The selected learner keys are too specific
to the generated candidate ids, so practical value reuse is near absent. More
episodes under that contract are more diagnostic traces, not true longer
training.

## PO-Locked Design Anchor

The Project Owner clarified the intended policy contract:

```text
Every model should get the full system configuration and the current second as
input, and should give the full action vector as output.
```

For Warehouse Gridlock, this means:

```text
input:
  full grid/obstacle configuration
  all robot positions
  all box positions
  all robot targets
  all box targets
  current second/timestep

output:
  one simultaneous command for every robot
  R01..R32 -> north | south | east | west | stay
```

The action vector is then checked by the environment/mask for admissibility.
The policy model itself should not be a selector over opaque generated
candidate ids as its fundamental learning surface.

## Design Work To Do Here

This folder should develop the blueprint for:

- a shared policy interface for direct and tower arms;
- direct-arm models that consume full concrete state plus second and emit full
  concrete action vectors;
- tower-arm models that may use tier structure internally but still produce a
  full concrete action vector at the environment boundary;
- learning updates that can actually improve behavior over time;
- evidence tables that distinguish real learning from nominal update logging;
- fairness rules for what state/configuration access each arm receives;
- replay/readout additions that show learning curves and policy changes across
  episodes.

## Current Boundary

Do not treat the existing Warehouse masked direct/live-lift result as a real
learning comparison. It remains useful as a controller, admissibility,
live-lift, artifact, and replay diagnostic.

The next design artifact in this folder should decide the concrete policy model
family and update rule before any long run is launched.
