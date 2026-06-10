# Candidate Generation Readout

The candidate policy was:

```text
coordination_ready_sparse_interleaved_v001
```

The budget was 256 proposals per step, with at most 8 active robots in one generated ensemble proposal.

The direct candidate event table confirms that the generated surface included all-stay, one-active, two-active, three-active, and larger multi-active proposals. This matters because the older smoke surface mostly exposed one-active moves and therefore could not seriously test coordinated Warehouse behavior.

The full action surface was not enumerated. The generator provided a bounded sample/proposal set, and the masks were exact over that generated set only.
