# Counterpoint First Serious Learning Evaluation Readout

![Artifacts: Partial](badges/artifacts_partial.svg)
![Behavior: Mixed](badges/behavior_mixed.svg)
![Goals: Partial](badges/goals_partial.svg)
![Scope: Fixture Only](badges/scope_fixture_only.svg)
![Provenance: Repo Artifacts](badges/provenance_repo_artifacts.svg)

## Status At A Glance

- Artifact evidence: partial; required result tables exist and were readable,
  but expected evaluation and arm manifests are absent.
- Behavioral result: mixed; direct, empty-schema, structured-motion, and
  bad/adversarial arms execute real 8-step episodes, while random balanced and
  random unbalanced arms are schema-seed dependent and include zero-step
  failures.
- Goal result: partially met; the run validates the serious harness and several
  tower-control paths, but it does not show tower advantage and leaves
  random-schema lift candidates plus the bad-control interpretation unresolved.
- Claim scope: fixture-only; claims apply only to
  `counterpoint_symbolic_n3_small_v001`, the locked budget,
  `tensor_available_disabled`, and this artifact set.
- Provenance: repo-resident artifact root; the evidence is source-bound from
  this repo readout surface.

This repository directory is the human-readable readout surface for the
counterpoint first serious learning evaluation.

Source evaluation root:

```text
/Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/v071_002_clean/evaluations/counterpoint_first_serious_learning_v001
```

Source binding:

```text
readout_source.json
```

To regenerate this repo-side readout, point the protocol at this directory, not
at the raw artifact root:

```text
execute artifact-table readout pointed at folder /Users/foster/big_boy_benchmarking/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning
```

Protocol applied:

```text
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

## Summary of Goals Behind this Evaluation

This evaluation asks whether the first real counterpoint benchmark can support a
meaningful comparison between direct learning on the concrete symbolic graph and
tower-control learning through contraction schemas.

The environment is `counterpoint_symbolic_n3_small_v001`, a benchmark-owned
finite symbolic hidden graph. The goal is not to generate beautiful music. The
goal is to compare learning/control behavior under a fixed legality contract,
reward bundle, action-mask policy, seed/budget discipline, and artifact
contract.

The key baselines are direct tabular Q and the empty-schema tower. Direct
tabular Q is the primary concrete-environment learner baseline. The empty-schema
tower checks whether the tower runtime and active-tier control path work when no
nontrivial contraction is present. The non-empty tower arms then test whether
random, structured motion, and intentionally bad contraction schemas can realize
valid concrete actions and support learning through the tower interface.

This readout is therefore a diagnostic learning/control evaluation, not a
musical-quality report, tensor-enabled performance result, CUDA/GPU result,
production performance result, or general claim that towers are better or worse
than direct learning.

## Summary of Methodology Behind this Evaluation

This readout summarizes a locked serious-run artifact set followed by
aggregation and human readout generation. The source binding points at a
repo-resident artifact root under this evaluation readout surface.

The evaluation compares direct environment arms against active-tier
exploit/explore tower-control arms under shared seed, budget, mask, artifact,
timing, and linearization discipline. The direct arms are `direct_masked_random`
and `direct_tabular_q`. The tower arms are the empty-schema tower, random
balanced and unbalanced contraction towers, structured motion tower, and
bad/adversarial tower.

The budget lock records `counterpoint_symbolic_n3_small_v001`,
`tensor_available_disabled`, 16 episodes per run, 4 replicates, 3 random schema
seeds, and a max horizon of 8 steps per episode. The aggregate tables summarize
returns, confidence intervals, baseline deltas, learning curves, timing
categories, controller events, schema diagnostics, and per-run lift/action
realization evidence.

The methodology can support artifact-completion, behavioral-status, and
diagnostic claims for this fixture and budget. It cannot support tensor-enabled,
CUDA/GPU, musical-quality, production-performance, or general tower-superiority
claims.

## One-Screen Verdict

All seven required arms produced machine-readable artifacts, and all `44` run
rows are marked `success`. That means the harness ran and wrote the expected
evaluation tables. It does not, by itself, mean every arm behaved equally well.

The direct baselines, empty-schema tower, structured-motion tower, and
bad/adversarial tower all executed 8-step episodes with 100% episode success
and mean returns around `12.7`.

The random tower arms are schema-seed dependent. Random balanced succeeds only
on schema seed `2`; seeds `0` and `1` produce zero-step episodes with
`no_lift_candidate_from_current_state`. Random unbalanced succeeds on schema
seeds `0` and `2`; seed `1` produces the same zero-step failure. This yields
mean returns of `4.237` for random balanced and `8.473` for random unbalanced,
not because those arms partially learn within each run, but because some schema
seeds execute and others do not.

This run does not support a positive tower-performance claim. Structured motion
matches the empty-schema tower rather than beating it, random schemas remain
brittle, and the bad/adversarial control does not degrade under this budget.

## Files

- [readout_source.json](readout_source.json): source binding from this repo readout surface to the raw artifact tables.
- [result_readout.md](result_readout.md): full human readout.
- [glossary.md](glossary.md): field and arm translations.
- [runbook.md](runbook.md): reconstructed commands and rerun notes.
- [artifact_index.md](artifact_index.md): evidence map with file purposes.
- [results/summary.md](results/summary.md): compact reader-facing result summary.
- [results/human_summary.md](results/human_summary.md): short result summary.
- [results/arm_readout_table.md](results/arm_readout_table.md): reader-facing arm table.
- [results/diagnostic_findings.md](results/diagnostic_findings.md): behavioral failure analysis.
- [results/timing_readout.md](results/timing_readout.md): timing summary with category boundaries.

## Claim Boundary

This readout is limited to `counterpoint_symbolic_n3_small_v001` under
`tensor_available_disabled`. Tensor execution was disabled. This is not a CUDA,
GPU, tensor-enabled, musical-quality, general superiority, or production
performance result.

This readout may claim:

- the locked serious-learning run completed all required arms and wrote the
  required aggregate/result tables;
- direct baselines, empty-schema tower, structured-motion tower, and
  bad/adversarial tower execute real concrete environment steps under this
  budget;
- random balanced and random unbalanced tower arms are schema-seed dependent
  and can produce zero-step episodes through
  `no_lift_candidate_from_current_state`.

This readout may not claim:

- tower-control superiority over direct learning;
- structured-motion advantage over the empty-schema tower;
- that the bad/adversarial schema is currently a healthy negative control;
- tensor-enabled, GPU, CUDA, musical-quality, production, or general
  state-collapser performance.

## Provenance Status

The source binding for this readout is `readout_source.json`. It identifies the
source artifact root, source evaluation root, source tables, environment
instance, linearization mode, claim boundary, goal-summary sources, and
expected-file policy.

Absent files are classified by expectation status:

| File | Classification | Expectation source | Interpretation |
| --- | --- | --- | --- |
| `evaluation_manifest.json` | `expected_missing_gap` | Serious evaluation artifact contract | Expected evaluation-level provenance is absent. |
| `evaluation_arm_manifest.json` | `expected_missing_gap` | Serious evaluation artifact contract | Expected arm-contract provenance is absent. |
| `calibration_summary.json` | `conditional_absent` | Calibration path contract | Expected for calibration, not necessarily for this locked serious run. |
| `calibration_run_index.csv` | `conditional_absent` | Calibration path contract | Expected for calibration, not necessarily for this locked serious run. |
| `calibration_recommendation.md` | `conditional_absent` | Calibration path contract | Expected for calibration, not necessarily for this locked serious run. |

The aggregate, run index, budget lock, learning curves, timing summary,
controller summary, schema diagnostic summary, and per-run diagnostic files were
available and used for this readout.

## Clarifying Questions And Turns

#### Project Owner / Evaluator Turn

> List the specific arms for me, and their corresponding result.

#### Embedded Engineering Consultant / Codex Turn

> Here are the seven arms in this evaluation and their corresponding current
> results from the clean `v071_002_clean` artifact set.
>
> | Arm | What it is | Result |
> | --- | --- | --- |
> | `direct_masked_random` | Direct environment masked-random baseline. | Succeeded. `64` episodes, mean return `12.790`, mean steps `8.0`, success rate `100%`. This is the non-learning floor, and it is slightly above direct tabular Q in this short budget. |
> | `direct_tabular_q` | Direct environment tabular Q-learning baseline. | Succeeded. `64` episodes, mean return `12.696`, mean steps `8.0`, success rate `100%`. This is the primary direct-learning baseline. |
> | `tower_empty_exploit_explore_tabular_q` | Tower controller with empty/no-op schema. | Succeeded. `64` episodes, mean return `12.710`, mean steps `8.0`, success rate `100%`. This shows the tower shell can execute when no nontrivial contraction is present. |
> | `tower_random_balanced_exploit_explore_tabular_q` | Tower controller with balanced random contraction schemas over seeds `0`, `1`, and `2`. | Mixed. `192` episodes, mean return `4.237`, mean steps `2.7`, success rate `33%`. Schema seed `2` executes successfully; schema seeds `0` and `1` produce zero-step episodes with `no_lift_candidate_from_current_state`. |
> | `tower_random_unbalanced_exploit_explore_tabular_q` | Tower controller with unbalanced random contraction schemas over seeds `0`, `1`, and `2`. | Mixed. `192` episodes, mean return `8.473`, mean steps `5.3`, success rate `67%`. Schema seeds `0` and `2` execute successfully; schema seed `1` produces zero-step episodes with `no_lift_candidate_from_current_state`. |
> | `tower_motion_exploit_explore_tabular_q` | Tower controller with the structured motion contraction schema. | Succeeded. `64` episodes, mean return `12.710`, mean steps `8.0`, success rate `100%`. It executes, but it matches the empty-schema tower rather than showing an advantage. |
> | `tower_bad_exploit_explore_tabular_q` | Tower controller with intentionally bad/adversarial contraction schema. | Succeeded. `64` episodes, mean return `12.710`, mean steps `8.0`, success rate `100%`. This is surprising as a negative control: under this budget it does not degrade relative to the empty-schema tower. |
>
> The shortest truthful summary is: direct baselines work; the empty tower
> works; structured motion executes but does not outperform the empty tower;
> random schemas are seed-sensitive; and the bad/adversarial control is not
> currently acting like a useful negative control.

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> ...

#### Project Owner / Evaluator Turn

> ...

#### Embedded Engineering Consultant / Codex Turn

> ...
