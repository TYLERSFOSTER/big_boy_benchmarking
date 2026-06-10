# Method

This diagnostic runs two active Warehouse Gridlock arms:

- direct concrete control with immediate inadmissibility masking;
- tower control over a scoped generated/discovered surface with live state-lift
  hygiene.

Both arms receive bounded generated candidate sets. Candidate masks are exact
over those generated sets, not over the full `5^32` action surface. The tower
surface is built from generated states, generated concrete candidates, and
valid immediate transitions under the Warehouse transition engine.

Successor `Out` may be observed after an action is selected and executed for
diagnosis. It is not used for action selection.
