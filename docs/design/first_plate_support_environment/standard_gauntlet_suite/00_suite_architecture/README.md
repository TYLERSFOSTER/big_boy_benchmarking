# Suite Architecture Design

## Purpose

This folder is for the umbrella design of the PlateSupport standard gauntlet
suite.

It should answer how the child stages fit together, what artifact contracts are
shared, what outputs become inputs to later stages, and which claims are allowed
only after specific stages complete.

## Design Scope

In scope:

- umbrella evaluation id and naming;
- stage ordering;
- stop gates between stages;
- shared manifests and readout-source shape;
- shared seed and replicate policy;
- suite-level claim boundaries;
- relationship to the completed PlateSupport environment-readiness surface.

Out of scope:

- implementing child stages;
- choosing PlateSupport thresholds before calibration evidence exists;
- claiming tower benefit before paired comparison evidence exists.

## Starting Question

What exact evidence should a standard environment gauntlet produce before we say
the environment is ready for serious comparative benchmark claims?
