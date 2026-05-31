# Counterpoint One-Third Schema Tower Diagnostics

`artifact_status: complete` `schema_geometry_status: structural-limit` `abc_runtime_status: complete` `lift_executability_status: observed` `claim_scope: diagnostic-only` `provenance_status: repo-bound`

Status: `complete`
Evaluation id: `counterpoint_one_third_schema_tower_diagnostics_v001`
Artifact root: `/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/small_medium_validation_001`

This readout is for the source-local one-third contraction schema on the existing `counterpoint_symbolic_v001` environment. It observes tower geometry, upstream ABC tier selection, lift/executability behavior, and concrete step emission. It is not a direct-vs-tower performance comparison.

Near full collapse means a single tier-1 quotient state cell contains at least `0.90` of all base states. When that happens, the run can still be diagnostically useful, but ordinary performance language is blocked because the first projection preserved too little state structure.

Current evidence headline:

- `24` expected runs are represented as complete.
- `24` / `24` runs show full tier-1 projection collapse.
- Runtime execution did not stall: `3840` concrete steps, `3840` / `3840` lift attempts succeeded, and `0` lift attempts failed.
- Episodes terminated/truncated: `384` terminated, `0` truncated.

Locked budget:

- instances: `counterpoint_symbolic_n3_small_v001, counterpoint_symbolic_n3_medium_v001`
- schema seeds: `[0, 1, 2]`
- replicates per schema seed: `4`
- episodes per replicate: `16`
- linearization mode: `tensor_available_disabled`

Open Questions For Project Owner

- Are the diagnostic categories sufficient for deciding the next schema variant to study?
- Should future readouts add compact plots once the table semantics stabilize?

Consultant-authored notes

- Generated readouts must not invent Project Owner turns. Use this section for model-authored interpretation or questions.
