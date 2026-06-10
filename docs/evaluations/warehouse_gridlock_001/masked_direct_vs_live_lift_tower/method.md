# Method

This diagnostic compares two Warehouse Gridlock control arms under equal immediate admissibility masking.

The direct arm, `warehouse_direct_admissible_masked`, chooses among bounded generated concrete ensemble actions after invalid actions are removed by the current-state transition check.

The tower arm, `warehouse_tower_live_lift_masked`, uses the same generated candidate policy but builds a scoped generated/discovered tower surface. It applies live state-lift hygiene, meaning the fixed downstairs state is lifted only to representatives with nonempty generated `Out`.

Budget:

- run label: `masked_8ep_001`;
- episodes per arm per replicate: `8`;
- replicates per arm: `2`;
- schema seeds: `1`;
- max seconds per episode: `128`;
- candidate proposals per step: `256`;
- max active robots in generated proposals: `8`;
- candidate mix id: `coordination_ready_sparse_interleaved_v001`;
- progress reporting: tqdm on stderr and `progress_events.jsonl`.

Fairness constraints:

- both arms mask immediate inadmissible actions;
- neither arm uses successor-state `Out` for action selection;
- successor `Out` is diagnostic only;
- no Abdul-style direct-star or tower-star one-hop guard is included;
- masks are exact only over the generated candidate set.

Claim constraints:

- the full primitive action surface is `5^32` and is not enumerated;
- the tower is scoped to generated/discovered candidate surfaces;
- the run is diagnostic, not a final benchmark;
- timing values are implementation wall time, not a method-speed result.
