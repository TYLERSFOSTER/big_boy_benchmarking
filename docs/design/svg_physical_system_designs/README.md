# SVG Physical System Design Workflow

## Status

Initial design folder.

This folder is for the new workflow where the Project Owner draws `.svg`
diagrams of physical systems that may become BBB benchmark environments.

## Purpose

The SVG should be treated as a physical-intent artifact, not decoration.

For each proposed system, the design work should begin by reading the diagram
and translating it into:

- the physical objects being modeled;
- the state variables;
- the primitive actions;
- the validity constraints;
- the goal or task condition;
- the likely invalid moves or cul-de-sacs;
- the reward/readout quantities;
- the tower/contraction opportunities;
- the minimum diagnostics needed before learning comparisons.

## Suggested File Shape

Use one subfolder per physical system:

```text
docs/design/svg_physical_system_designs/<system_id>/
  README.md
  design_discussion.md
  01_001_<system_id>_environment_blueprint.md
  01_002_<system_id>_environment_implementation_workplan.md
  01_003_<system_id>_environment_implementation_log.md
```

The corresponding drawings can live under a stable asset path such as:

```text
assets/environment_designs/<system_id>/
```

## Working Rule

Do not turn a diagram directly into code.

First, write down what the diagram appears to assert physically, then ask the
Project Owner to correct the interpretation. Only after that should the system
be converted into a blueprint and then a Phase.Stage.Action implementation
workplan.

## Attribution Rule

The diagram expresses Project Owner intent only where the drawing or explicit
Project Owner text actually supports it. Codex must not invent physical
semantics that the drawing does not specify. When Codex infers a constraint,
goal, or variable from the drawing, label it as an inference until the Project
Owner confirms it.
