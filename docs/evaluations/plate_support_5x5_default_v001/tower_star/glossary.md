# PlateSupport Tower-Star Glossary

- `direct_raw`: direct PlateSupport learner over the primitive action alphabet.
- `direct_invalid_guard`: direct learner with one-step invalid primitive actions removed before selection.
- `direct_nonself_guard`: direct learner with one-step self-loop primitive actions removed before selection.
- `tower_lift_executable_current`: current tower learner using executable quotient action cells.
- `tower_invalid_guard`: tower learner after removing lift candidates whose primitive action is invalid.
- `tower_nonself_guard`: tower learner after removing lift candidates whose primitive action is a self-loop.
- `tower-star`: the diagnostic rule that filters concrete lift candidates before tower action-cell selection.
- `action cell`: a quotient action option exposed by the contracted tower tier.
- `lift candidate`: a concrete primitive action inside a quotient action cell.
- `diagnostic smoke/calibration evidence`: evidence useful for debugging and calibration, not final benchmark proof.
