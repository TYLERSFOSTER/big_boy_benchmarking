# Fairness Audit

The fairness audit passed for this diagnostic.

Both arms:

- used immediate inadmissibility masking;
- selected zero invalid concrete moves;
- used the same candidate budget and generated candidate mix;
- did not use successor-state `Out` for action selection.

The direct arm and tower arm each considered `524288` generated candidates before masking and retained `40797` candidates after masking. This symmetry is why the tied result is interpretable as a genuine small-budget tie rather than an artifact of one arm being given an easier admissibility surface.
