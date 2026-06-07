# PlateSupport Iterated Tower Correction

This folder is for design work correcting the PlateSupport standard gauntlet after the first full gauntlet run showed that the selected tower candidate was only a one-shot two-tier quotient.

## Triggering Observation

The PlateSupport standard gauntlet currently produces a selected `source_local_ratio` candidate with this tower shape:

```text
tier 0: 89 state cells, 388 action cells
tier 1: 10 state cells, 116 action cells
```

That candidate is valid for the first PlateSupport gauntlet smoke run, but it does not satisfy the PO goal of many nontrivial tiers.

## Source Of The Correction

The PO asked whether the issue was the wrong architecture or the wrong ratio. The immediate Codex diagnosis was:

```text
architecture blocker: PlateSupport currently has one-shot source-local-ratio, not full-iterated source-local-ratio
ratio concern: 1/18 may be too aggressive for an 89-state PlateSupport graph once iteration exists
desired next object: PlateSupport iterated source-local-ratio tower diagnostic
```

The counterpoint many-tier reference case is the `full_iterated_noisy_rate` path in:

```text
src/big_boy_benchmarking/environments/counterpoint/second_serious_comparison/
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
```

The PlateSupport correction should adapt that architectural idea, not merely rerun the existing one-shot schema with a different ratio.

## Design Work To Do Here

This folder should collect the design discussion, blueprint, workplan, and implementation logs for a PlateSupport iterated-tower correction.

Current documents:

```text
01_001_plate_support_iterated_tower_correction_initial_design.md
01_002_plate_support_iterated_tower_correction_blueprint.md
01_003_plate_support_iterated_tower_correction_implementation_workplan.md
```

The expected design target is a diagnostic-first addition:

1. Build or specify an iterated PlateSupport source-local-ratio schema family.
2. Repeatedly apply fresh contraction blocks to the current quotient surface.
3. Sweep gentle ratios such as `1/144`, `1/72`, `1/36`, and `1/18`.
4. Record tier-by-tier state cells, action cells, executability, liftability health, largest-cell share, and stopping reason.
5. Gate downstream training/comparison on finding several nontrivial executable tiers.

This is not yet a replacement for the whole standard gauntlet. It is a correction track whose output should later feed the contraction schema sweep, candidate discovery, tower training health, threshold frontier calibration, and paired comparison stages.
