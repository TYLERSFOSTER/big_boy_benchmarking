# Method

Warehouse Gridlock transformer policy runs train a BBB-owned transformer
actor-critic over the full Warehouse system configuration plus the current
second. The first slice is tower-only curriculum training with live-lift
state-liveness hygiene and immediate admissibility masking.
