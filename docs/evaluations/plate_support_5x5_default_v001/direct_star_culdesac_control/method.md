# PlateSupport Direct-Star Cul-de-sac Control Method

This diagnostic reuses the selected iterated tower candidate and
calibrated target from the PlateSupport standard gauntlet correction
run. It compares raw direct, invalid-guarded direct, nonself-guarded
direct, and the selected tower candidate under matched seed bundles.

The guarded direct arms are pre-mask controls. They receive only a
binary one-step local action mask and no reward, goal-distance,
multi-step reachability, schema, tier, or future liftability lookahead.

The result is diagnostic smoke/calibration evidence.
