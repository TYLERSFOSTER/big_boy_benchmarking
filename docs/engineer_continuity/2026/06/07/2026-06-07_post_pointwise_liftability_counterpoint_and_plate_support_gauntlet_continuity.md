# Big Boy Benchmarking Continuity Report

Date: 2026-06-07

Repository:

```text
<repo-root>
```

Previous continuity checkpoint:

```text
docs/engineer_continuity/2026/06/02/2026-06-02_root_tex_pre_po_abdul_edit_attribution_checkpoint.md
```

This report covers the work from immediately after that checkpoint through the
current PlateSupport standard-gauntlet correction run and root-documentation
refresh.

## Executive Summary

Since the 2026-06-02 checkpoint, the repository moved from a counterpoint-only
benchmarking system with early human-readability protocols into a two-environment
benchmarking project with:

- corrected `state_collapser` v0.7.2 pointwise liftability integration;
- corrected counterpoint reruns under the v0.7.2 semantics;
- two counterpoint next-measure probes after the second serious comparison;
- a first-class PlateSupport BBB environment;
- a full PlateSupport standard gauntlet suite;
- an iterated PlateSupport tower correction that produced a bounded positive
  direct-vs-tower target signal;
- stronger human-readable readout protocols, local badges, clarifying-turn
  rules, and system-learning archives;
- explicit Prime Directive failure-mode documents for false attribution and
  umbrella workplan fragmentation.

The most important current result is the PlateSupport standard gauntlet artifact
run:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/iterated_001/
```

That run completed gauntlet Stages 1-7 and produced claim status:

```text
paired_comparison_positive_signal
```

The bounded signal is:

```text
tower target hits: 25 / 128
direct target hits: 15 / 128
mean target-hit-rate delta: +0.078125
tower mean reward: -27.2109375
direct mean reward: -78.71875
tower invalid moves: 0
direct invalid moves: 2142
```

This is not a broad PlateSupport performance claim. It is a smoke-scale,
one-selected-candidate result. But it is the first coherent result in this repo
where the tower arm looks behaviorally promising on a constrained robotics-style
environment.

## Repository State At Report Creation

At the start of this report pass, `git status --short --branch` reported:

```text
## main...origin/main [ahead 1]
```

No dirty paths were reported before this continuity file was created. The branch
is `main`, ahead of `origin/main` by one local commit.

This report itself is an uncommitted documentation addition unless later staged
and committed.

## Attribution Boundary From Previous Report

The previous report was not a general project summary. It was a TeX attribution
checkpoint for:

```text
tropicalization_and_binary_coset_towers.tex
```

It recorded a pre-Project-Owner/Abdul baseline. The explicit instruction was to
preserve attribution because the Project Owner was about to add material with
Abdul.

This continuity report preserves that boundary:

- Post-checkpoint TeX content should be treated as Project Owner/Abdul-authored
  unless Codex was explicitly instructed to edit the TeX.
- Codex should not claim authorship of the mathematical paper material merely
  because it read, summarized, compiled, ignored generated TeX side files, or
  updated root docs around it.
- Root TeX/PDF/BIB handling after the checkpoint was file hygiene and
  attribution preservation, not Codex authorship of the paper.

## High-Level Timeline Since 2026-06-02

The work happened in several intertwined streams. The order below is conceptual,
not every single chat turn.

1. Counterpoint evaluation readouts exposed confusing artifact semantics and
   led to stronger readout protocols.
2. A counterpoint liftability issue exposed a real upstream `state_collapser`
   semantics problem.
3. `state_collapser` v0.7.2 fixed pointwise liftability; BBB integrated it and
   reran affected counterpoint evaluations.
4. Counterpoint second-serious comparison showed only a tiny bounded signal, so
   two next-measure probes were added.
5. The Project Owner pushed toward a robotics-style environment because
   counterpoint's effect size was too small to carry the next main benchmark
   question.
6. BBB built a first-class PlateSupport environment from the upstream
   `state_collapser` example.
7. A full standard gauntlet suite was designed, implemented, and run for
   PlateSupport.
8. The first PlateSupport gauntlet attempt found the one-shot schema path was
   not enough to produce the desired candidate.
9. The Project Owner identified the correct correction direction: an iterated
   source-local-ratio tower path, with a ratio knob and a near-full-collapse
   threshold.
10. The iterated PlateSupport correction was implemented and rerun as
    `iterated_001`, producing the current bounded positive signal.
11. Root README/CONTRIBUTING were refreshed to reflect the current repo state.

## Prime Directive And Protocol Changes

Several operational protocols were sharpened during this period because the
Project Owner caught repeated drift.

### Human-Readable Artifact Readout Protocol

Main protocol:

```text
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

This protocol now defines the canonical invocation:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-readout-surface>/readout_source.json
```

Key correction:

- The command target is the checked-in repo-side `readout_source.json`.
- It is not the README.
- It is not the raw artifact folder.
- It is not the nested evaluation root.
- If the Project Owner points at the wrong path role, Codex should stop and ask
  for the source binding instead of writing generated docs into the artifact
  tree.

Project Owner attribution:

- The Project Owner forced this correction after multiple wrong interpretations
  where Codex treated "pointed at folder" as a raw artifact path or result-table
  path.
- The Project Owner's intended surface was always a consultant-executable
  protocol invocation, not a shell script and not a "last run" heuristic.
- The Project Owner explicitly wanted generated human-readable documents written
  into repo-side evaluation readout surfaces.

### Evaluation Construction For Readable Artifacts

Main protocol:

```text
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
```

This protocol records the upstream expectation for evaluation authors:

- create the machine-readable artifacts;
- provide source bindings;
- provide goals, methodology, and claim boundaries;
- provide the information needed by the human-readable readout generator.

This exists because a later human-readable readout is only as good as the
metadata and tables the evaluation supplies.

Project Owner attribution:

- The Project Owner noticed that generated readouts could not fill sections
  about methodology or "what the evaluation was trying to do" unless evaluation
  construction itself carried that material.
- The Project Owner also insisted that generated README clarifying-turn sections
  must preserve room for follow-up conversation without being mistaken for the
  core current result.

### False Attribution Failure Mode

Main warning:

```text
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
```

This was created after Codex wrote model-authored content inside a blueprint as
though it were Project Owner turns. That was treated as a source-of-truth
failure, not a formatting problem.

Current rule:

- Never attribute words, decisions, questions, preferences, approvals, or
  framing to the Project Owner unless the Project Owner actually supplied them.
- Blueprints should use sections such as `Open Questions For Project Owner`,
  `Consultant Recommendations`, and `Assumptions Pending Project Owner
  Confirmation`.
- Do not invent Project Owner turns in blueprints or workplans.

Project Owner attribution:

- The Project Owner caught the false attribution and explicitly demanded a new
  Prime Directive document to prevent recurrence.

### Umbrella Workplan Fragmentation Failure Mode

Main warning:

```text
docs/prime_directive/common_failure_mode_005_umbrella_workplan_fragmentation.md
```

This was created during the PlateSupport standard-gauntlet work. The gauntlet
had a parent workplan and child stage workplans. Codex repeatedly stopped at the
end of a child stage and made the Project Owner manually restart the next child.

Current rule:

- If the Project Owner asks to build, execute, resume, or finish a whole
  umbrella workplan, child workplans are checkpoints, not endpoints.
- The parent workplan is the execution spine.
- Continue through child workplans until the umbrella is complete or a true stop
  condition occurs.

Project Owner attribution:

- The Project Owner identified the failure pattern clearly: the desired unit of
  work was the whole gauntlet, not each child stage as a separate PO-prompted
  job.
- This correction directly shaped later PlateSupport gauntlet execution.

## System-Learning Archive

Durable system-learning folder:

```text
docs/design/system_learning_from_evaluations/
```

This folder exists because generated evaluation readouts are allowed to be
regenerated. Clarifying conversations inside README files are useful, but they
are not safe long-term design memory if they only live in generated surfaces.

Current important subfolders include:

```text
counterpoint_first_serious_learning_v001/
counterpoint_one_third_schema_unexpected_collapse/
counterpoint_noisy_rate_contraction_diagnostics/
counterpoint_noisy_rate_full_tower_training_diagnostic/
direct_image_threshold_binding/
plate_support_standard_gauntlet_v001/
```

Project Owner attribution:

- The Project Owner identified that generated readout conversations should be
  archived into design-side system memory before regenerating the readout.
- The Project Owner also introduced the binary-search analogy as a core
  explanation device for many tower/coarse-to-fine confusion points.
- The Project Owner requested a direct-image-threshold-binding note for future
  engineers: lower tiers may bind upper-tier performance via direct-image tier
  thresholds. That was not the immediate cause of the current evaluation issue,
  but it is expected to matter later.

## state_collapser v0.7.1 Degenerate-Tier Handoff

Relevant folder:

```text
docs/design/degenerate_tier_control/
```

Relevant implementation log:

```text
docs/design/degenerate_tier_control/01_006_counterpoint_degenerate_tier_handoff_integration_implementation_log.md
```

This was the earlier upstream handoff for degenerate-tier behavior. There was a
major alignment correction here: Codex initially expanded the blueprint into a
large set of unrelated new questions. The Project Owner corrected that.

Correct interpretation:

- The real source of authority was the error diagnosis conversation and the
  `state_collapser` handoff note.
- The desired BBB work was to make the upstream `state_collapser` changes work
  here and then return to the original counterpoint evaluation.
- It was not a new broad architecture-design fork.

Project Owner attribution:

- The Project Owner explicitly rejected the over-broad blueprint framing and
  re-centered the work on the handoff note and the prior error-diagnosis
  conversation.

## state_collapser v0.7.2 Pointwise Liftability Handoff

Relevant folder:

```text
docs/design/state_collapser_v072_pointwise_liftability_handoff/
```

Key files:

```text
state_collapser_pointwise_liftability_github_issue.md
state_collapser_pointwise_liftability_diagnostic_report.md
big_boy_benchmarking_synthetic_blow_revisions_02_handoff.md
01_001_bbb_v072_pointwise_liftability_integration_blueprint.md
01_002_bbb_v072_pointwise_liftability_integration_implementation_workplan.md
01_003_bbb_v072_pointwise_liftability_integration_implementation_log.md
```

The key semantic correction is:

```text
An abstract action is executable only if it has a concrete lift executable from
the current concrete/base state.
```

This replaced the weaker representative/quotient-level interpretation:

```text
the abstract tier advertises outgoing action cells
```

The v0.7.2 integration log records the upstream API surface:

```text
executable_lift_candidates(tier, action_cell_id, current_base_state)
tier_is_executable_from_state(tier, current_base_state)
assert_consistent()
invariant_report()
```

BBB-side changes included:

- dependency-state checks for the required `PartitionTower` pointwise APIs;
- a fixture proving quotient support can be nonempty while pointwise executable
  lift candidates are empty from a particular concrete state;
- a canonical semantics id:

  ```text
  state_collapser_v072_pointwise
  ```

- tower invariant collection and `tower_invariant_report.json` artifacts;
- counterpoint tower-control masks based on pointwise executable action cells;
- removal of representative fallback from execution;
- additive lift event fields preserving representative counts as diagnostics;
- regenerated docs/readouts explaining quotient support versus pointwise
  executable liftability.

Validation recorded in the implementation log included:

```text
uv run pytest
224 passed in 31.62s

uv run python -c 'import state_collapser; print(state_collapser.__version__)'
0.7.2
```

Project Owner attribution:

- The Project Owner discovered the conceptual problem through the concrete
  lift/action discussion, including the simplex-style example.
- The key Project Owner realization was that a lift state must be chosen among
  preimage states with the relevant executable outgoing action, not merely from
  the preimage of the abstract state.
- The upstream `state_collapser` v0.7.2 work came from the state_collapser
  engineers; BBB integrated it and reran affected evaluations.

## Counterpoint Current State After v0.7.2

The counterpoint environment remains:

```text
src/big_boy_benchmarking/environments/counterpoint/
```

The current high-level counterpoint readout chain is:

```text
noisy_rate_contraction_diagnostics
-> noisy_rate_full_tower_training_diagnostic
-> second_serious_schema_comparison
-> threshold_frontier_probe
-> small_paired_replicate_probe
```

### Noisy-Rate Contraction Diagnostics

Readout:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/README.md
```

Current artifact label:

```text
wide_span18_p001_over018_s0_001
```

Key facts:

```text
instance: counterpoint_symbolic_n3_wide_20_108_span18_v001
rate: 1/18
schema seed: 0
selected edges: 2800
selected source share: about 0.540
zero-selected sources: 1646
tier cells: [3580, 1035]
active action cells: [49172, 24258]
verdict: no_collapse
claim scope: diagnostic only
```

This was the answer to the unexpected collapse of the earlier source-local
one-third schema. The edge-global noisy-rate rule deliberately allows some
source states to select zero outgoing edges, contrasting with the source-local
floor rule.

Project Owner attribution:

- The Project Owner pushed on the one-third collapse result and correctly
  treated it as diagnostic, not as a final negative conclusion.
- The Project Owner wanted to understand whether the issue was a schema-design
  artifact before making larger claims.

### Noisy-Rate Full-Tower Training Diagnostic

Readout:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/README.md
```

Current artifact label:

```text
v072_pointwise_001
```

Key facts:

```text
candidate count: 1
candidate arm: p001_over_018
tier cells: [3580, 1035]
active cells: [49172, 24258]
concrete steps emitted: 32
learner updates: 40
status: trainable_clean
claim scope: tower-only training health, not direct-vs-tower comparison
```

Important limitation:

- The full available tower is currently only base plus one noisy-rate quotient
  tier because the parent noisy-rate contraction diagnostic supplies a
  one-block candidate.

Project Owner attribution:

- The Project Owner asked whether the tower was still only two tiers, forcing a
  clear claim-boundary explanation.

### Second Serious Schema Comparison

Readout:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/README.md
```

Current artifact label:

```text
v072_pointwise_r013_001
```

Key facts:

```text
threshold: R = 13.0
persistence rule: 4 of 5
pair rows: 1
unblocked rows: 1
schema0 sustained: yes
schema1 sustained: yes
episodes to sustained hit: same for both
claim status: bounded_comparison_available
liftability semantics: state_collapser_v072_pointwise
invariant preflight: passed
lift failure rows: 0
```

Interpretation:

- This proves the comparison surface is populated under the corrected
  liftability semantics.
- It does not show speed difference in the one checked-in pair.

Project Owner attribution:

- The Project Owner repeatedly asked whether the result showed any evidence of
  improvement. The correct answer became: only very slight and bounded evidence
  in surrounding margin/reward surfaces, not an episode-to-hit speedup in this
  second-serious artifact itself.

### Threshold Frontier Probe

Design folder:

```text
docs/design/first_counterpoint_environment/threshold_frontier_probe/
```

Readout:

```text
docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/README.md
```

Current artifact label:

```text
episodes16_001
```

Key facts:

```text
thresholds tested: 12.0 and 13.0
pair rows: 2
Schema 0 passes both
Schema 1 passes both
Schema 1 post-hit margin is higher at both thresholds
recommended paired-replicate threshold: 13.0
claim status: schema1_margin_advantage_only
```

Project Owner attribution:

- The Project Owner noticed that the first smoke run did not have enough
  episodes for the 4-of-5 persistence rule to mean anything.
- The Project Owner explicitly directed keeping the 4-of-5 ratio while
  increasing `episodes_per_replicate` to at least 16.

### Small Paired Replicate Probe

Design folder:

```text
docs/design/first_counterpoint_environment/small_paired_replicate_probe/
```

Readout:

```text
docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/README.md
```

Current artifact label:

```text
episodes16_from_frontier_001
```

Key facts:

```text
threshold source: threshold_frontier_readout
threshold: R = 13.0
pair rows: 1
unblocked rows: 1
Schema 0 sustained rate: 1.0
Schema 1 sustained rate: 1.0
Schema 1 margin wins: 1
claim: weak_positive_margin_pattern
```

Interpretation:

- This is still one selected candidate and one unblocked pair.
- It is not statistical evidence.
- It does preserve a weak positive Schema 1 margin pattern.

Project Owner attribution:

- The Project Owner clarified that "speedup" in this context often means higher
  reward translating into earlier stopping/cleaner target achievement, not only
  fewer raw episode steps in a single comparison table.

## Why The Project Moved From Counterpoint To PlateSupport

The Project Owner judged that counterpoint's current positive signal was too
small and too delicate for the next major benchmark push.

The counterpoint probes are valuable:

- they validated the machinery;
- they exposed real upstream liftability semantics;
- they created better artifact/readout protocols;
- they gave the first hints of Schema 1 margin advantage.

But the Project Owner wanted a more robotics-like constrained RL setting where
invalid moves, support constraints, and tower routing might create a larger and
more interpretable performance separation.

That motivated moving to PlateSupport.

## PlateSupport Environment Build

Design folder:

```text
docs/design/first_plate_support_environment/
```

Implementation log:

```text
docs/design/first_plate_support_environment/01_003_plate_support_environment_bbb_build_implementation_log.md
```

Environment package:

```text
src/big_boy_benchmarking/environments/plate_support/
```

Environment readiness readout:

```text
docs/environments/plate_support_5x5_default_v001.md
docs/environments/plate_support_5x5_default_v001/readiness/dev_001/
```

The environment build created a first-class BBB wrapper around the upstream
`state_collapser` PlateSupport example.

Key readiness facts:

```text
ambient candidate states: 2700
valid states: 89
valid states reachable from start: 89
primitive actions: 12
shortest start-goal path length: 6
default upstream schema reaches tower depth: 2
no-contraction schema stays flat at depth: 1
random-policy success rate in gauntlet Stage 1: 0.024
```

Validation recorded in the environment build log included:

```text
uv run pytest tests/environments/plate_support
13 passed

uv run python -m big_boy_benchmarking.cli validate-contracts
status ok

uv run pytest
244 passed
```

Project Owner attribution:

- The Project Owner chose the robotics/constrained direction because
  counterpoint's 12.0/13.0 threshold effects were too small to be satisfying for
  the next benchmark.
- The Project Owner identified the upstream PlateSupport example as the right
  starting point and asked how much could be copied from `state_collapser`.

## PlateSupport Standard Gauntlet Suite

Parent folder:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/
```

Child design/workplan folders:

```text
00_suite_architecture/
01_structural_and_tower_diagnostics/
02_contraction_schema_sweep/
03_candidate_discovery/
04_tower_training_health/
05_threshold_frontier_calibration/
06_paired_replicate_comparison/
07_readout_and_system_learning/
08_iterated_tower_correction/
```

The suite was intended to package the sequence learned from counterpoint as a
standard gauntlet for environments:

1. structural and tower diagnostics;
2. contraction schema sweep;
3. candidate discovery;
4. tower training health;
5. threshold/frontier calibration;
6. paired direct-vs-tower comparison;
7. human-readable readout and system learning.

Project Owner attribution:

- The Project Owner recognized that the counterpoint evaluation sequence had
  become a reusable baseline pipeline/gauntlet.
- The Project Owner asked whether designing the whole umbrella suite at once
  was dangerous. The agreed answer was: use a parent suite folder with child
  design folders, then implement stage-by-stage under the parent execution
  spine.
- The Project Owner later caught Codex violating that execution model by
  stopping after individual child stages.

## First PlateSupport Gauntlet Attempt And Candidate Failure

The first PlateSupport standard-gauntlet attempt completed early stages but
stopped at candidate discovery with:

```text
candidate_not_found
```

Reason:

- The initial one-shot contraction schema did not produce a trainable candidate
  suitable for downstream Stage 4.
- The candidate failure was not an environment-readiness failure. PlateSupport
  itself was valid and reachable.
- The failure showed that the schema family was not yet producing the right
  nontrivial executable tower surfaces.

Project Owner attribution:

- The Project Owner asked for graph statistics and expected outdegree to reason
  about why the schema was failing.
- The Project Owner recalled the contraction scheme that selects outgoing edges
  by a certain ratio and asked to make that ratio a knob.
- This directly led to the source-local-ratio schema controls.

## PlateSupport Iterated Tower Correction

Design folder:

```text
docs/design/first_plate_support_environment/standard_gauntlet_suite/08_iterated_tower_correction/
```

Key files:

```text
01_001_plate_support_iterated_tower_correction_initial_design.md
01_002_plate_support_iterated_tower_correction_blueprint.md
01_003_plate_support_iterated_tower_correction_implementation_workplan.md
01_004_plate_support_iterated_tower_correction_implementation_log.md
```

Implementation package areas:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/contraction_schema_sweep/
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/candidate_discovery/
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/tower_training_health/
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/threshold_frontier_calibration/
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/paired_replicate_comparison/
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/readout_system_learning/
```

Decision locks from the implementation log:

```text
schema_family_id: source_local_ratio_iterated
schema_mode: source_local_ratio_iterated
selector rule: stable threshold/rate selection over quotient representative edges
near-collapse threshold: 0.9
initial ratios: 1/144, 1/72, 1/36, 1/18
initial schema seeds: 0, 1, 2
max iterations: 32
candidate gate: max_depth >= 4 and nontrivial_tier_count >= 3
integration point: gauntlet Stage 2 schema sweep
artifact discipline: do not overwrite historical smoke_001 artifacts
```

The correction added:

- `IteratedSourceLocalOutgoingRatioSchema`;
- deterministic SHA-256 selector scoring;
- iterated schema and block ids;
- union-find based quotient planning;
- plan diagnostics and stop summaries;
- optional Stage 2 CLI flags:

  ```text
  --include-iterated-source-local-ratio
  --iterated-source-local-max-iterations 32
  ```

- iterated metadata preservation through Stage 3 candidate discovery;
- metadata-first candidate loading in Stage 4;
- iterated tower construction in training surfaces;
- iterated metadata through Stage 5 threshold calibration;
- iterated metadata through Stage 6 paired comparison;
- Stage 7 badges for iterated candidate and tier count.

Temporary Stage 2 smoke facts from the implementation log:

```text
1/144: max_depth 18, nontrivial_tier_count 17, many_tier_executable_candidate
1/72: max_depth 11, nontrivial_tier_count 10, many_tier_executable_candidate
1/36: max_depth 11, nontrivial_tier_count 10, nonexecutable_iterated_tier
1/18: max_depth 12, nontrivial_tier_count 10, nonexecutable/near-collapse signal
```

Validation recorded there:

```text
uv run pytest tests/environments/plate_support
56 passed

uv run pytest
287 passed
```

Project Owner attribution:

- The Project Owner asked for an iterated PlateSupport source-local-ratio schema
  with near-collapse threshold `0.9`.
- The Project Owner said the iterated planning shape should copy counterpoint
  wherever that made sense.
- The Project Owner clarified that the initial focus should be diagnostic and
  tower-shape focused, and that downstream stages should consume it only after
  it produced many nontrivial executable tiers.
- The Project Owner asked for downstream candidate parsing/training surfaces to
  stop assuming one-shot schema ids.

## PlateSupport Correction Run iterated_001

Current readout:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/README.md
```

Raw artifact root:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/iterated_001/
```

Suite evaluation root:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/iterated_001/evaluations/plate_support_standard_gauntlet_v001/
```

Current stage table:

```text
Stage 1 structural_and_tower_diagnostics: complete / diagnostic_complete
Stage 2 contraction_schema_sweep: complete / diagnostic_complete
Stage 3 candidate_discovery: complete / candidate_found
Stage 4 tower_training_health: complete / trainable_clean
Stage 5 threshold_frontier_calibration: complete / threshold_calibrated
Stage 6 paired_replicate_comparison: complete / paired_comparison_positive_signal
Stage 7 readout_and_system_learning: complete / readout_complete
```

Current badges include:

```text
Suite: Limited Signal
Artifacts: Complete
Structure: Complete
Candidate: Found
Training: Clean
Target: Calibrated
Paired: Positive Signal
Provenance: Repo Artifacts
Iterated: Candidate
Tiers: 17/18
```

Key result:

```text
selected iterated tower candidate target hits: 25 / 128
direct baseline target hits: 15 / 128
mean target-hit-rate delta: +0.078125
```

Counter-signal:

```text
tower mean reward: -27.2109375
direct mean reward: -78.71875
tower invalid moves: 0
direct invalid moves: 2142
direct concrete steps: 6017
tower concrete steps: 6008
direct invalid-move rate: about 35.6%
tower mean concrete steps per target hit: about 240.32
direct mean concrete steps per target hit: about 401.13
```

Interpretation:

- The formal target metric is Stage 5 binary goal success.
- The reward and invalid-move rows are explanatory counter-signals.
- The tower arm is not merely winning a weird isolated target counter; it also
  behaves more cleanly by avoiding invalid concrete moves.
- Episode lengths are similar, so the reward gap is mostly invalid-move
  avoidance and more frequent target success, not simply shorter episodes.

Claim boundary:

```text
bounded paired smoke comparison under the Stage 5 target and budget; not a
general tower-performance claim
```

Project Owner attribution:

- The Project Owner asked whether the counter-signal meant the tower has the
  potential to be a powerful technology. The correct answer is yes, within the
  bounded smoke-scale interpretation.
- The Project Owner also forced root README updates so the root documentation
  did not understate or misstate this result.

## PlateSupport Readout Generator Fixes

During the PlateSupport readout work, a serious generated-doc issue appeared:

- Stage 7 preserved stale clarifying turns from an earlier artifact root into
  the new `iterated_001` readout.

Fix:

- Stage 7 readout preservation now checks whether an existing README's raw
  artifact root matches the current artifact root.
- If the old clarification mentions a different artifact root, it is reset
  instead of being carried forward.

Related source area:

```text
src/big_boy_benchmarking/environments/plate_support/standard_gauntlet/readout_system_learning/
```

Project Owner attribution:

- The Project Owner noticed that badges/readout shape looked wrong and asked why
  it did not match other reports.
- That surfaced the stale generated-turn problem and led to generator changes,
  not just manual README cleanup.

## Shared CSV Writer Fix

During PlateSupport generated-artifact normalization, `git diff --check` exposed
line-ending/trailing-whitespace noise from generated CSVs.

Fix:

```text
src/big_boy_benchmarking/artifacts/writers.py
```

The shared CSV writer now uses:

```text
lineterminator="\n"
```

for CSV writing/appending so generated artifacts remain stable in git diffs.

This is cross-cutting benchmark infrastructure, not PlateSupport-only behavior.

## Root Documentation Refresh

Root docs inspected and refreshed:

```text
README.md
CONTRIBUTING.md
LICENSE
```

`LICENSE` did not need changes.

`README.md` now lists the current completed evaluation surfaces and current
claim boundaries, including:

```text
Counterpoint noisy-rate contraction diagnostics: wide_span18_p001_over018_s0_001
Counterpoint noisy-rate full-tower training diagnostic: v072_pointwise_001
Counterpoint second serious schema comparison: v072_pointwise_r013_001
Counterpoint threshold frontier probe: episodes16_001
Counterpoint small paired replicate probe: episodes16_from_frontier_001
PlateSupport standard gauntlet: iterated_001
```

`CONTRIBUTING.md` now directs future work around:

- current PlateSupport correction run `iterated_001`;
- current counterpoint next-measure probes;
- pointwise liftability semantics;
- human-readable readout command discipline;
- umbrella workplan fragmentation prevention;
- preserving claim boundaries.

Validation during root-doc pass:

```text
git diff --check README.md CONTRIBUTING.md LICENSE
```

passed.

Project Owner attribution:

- The Project Owner explicitly called out stale root "Current Scope" language
  and later asked whether the root README reflected the latest gauntlet run.
- The Project Owner wanted the root README brief enough to digest but honest
  about completed evaluations, conclusions, and human-readable links.

## Current Evaluation Claims At A Glance

### Environment Readiness

PlateSupport readiness is complete:

```text
docs/environments/plate_support_5x5_default_v001.md
```

Claim:

- BBB can bind the upstream PlateSupport example as a first-class environment.
- It can enumerate states/actions/transitions, record reachability, record
  shortest paths, and write repo-side readiness artifacts.

Non-claim:

- Readiness is not learning-performance evidence.

### Counterpoint Structural Diagnostic

Readout:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_contraction_diagnostics/README.md
```

Claim:

- The edge-global noisy-rate selector can produce a non-collapsed quotient tier
  on the widened fixture.

Non-claim:

- Not a learning comparison.

### Counterpoint Tower Training Health

Readout:

```text
docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/README.md
```

Claim:

- One selected noisy-rate candidate trains cleanly under tower-only budget and
  pointwise semantics.

Non-claim:

- Not a direct-vs-tower comparison.
- Not a deep-tower validation.

### Counterpoint Second Serious Comparison

Readout:

```text
docs/evaluations/counterpoint_symbolic_v001/second_serious_schema_comparison/README.md
```

Claim:

- Bounded one-pair comparison surface is available under `R = 13.0`.

Non-claim:

- It does not show an episode-to-sustained-hit speed difference in the current
  pair.

### Counterpoint Threshold Frontier

Readout:

```text
docs/evaluations/counterpoint_symbolic_v001/threshold_frontier_probe/README.md
```

Claim:

- With enough episodes for the persistence window, both schemas pass thresholds
  `12.0` and `13.0`, and Schema 1 has higher post-hit margin in this one
  selected-candidate probe.

Non-claim:

- Not broad schema dominance.

### Counterpoint Small Paired Replicate

Readout:

```text
docs/evaluations/counterpoint_symbolic_v001/small_paired_replicate_probe/README.md
```

Claim:

- One matched pair at `R = 13.0` has Schema 1 higher post-hit margin.

Non-claim:

- Not statistical significance.

### PlateSupport Standard Gauntlet

Readout:

```text
docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/README.md
```

Claim:

- The full gauntlet can complete on a selected iterated PlateSupport tower
  candidate.
- The selected tower candidate beats direct baseline on the locked Stage 5
  binary target under the smoke Stage 6 budget.
- Reward and invalid-move signals align with the target result.

Non-claim:

- Not a general PlateSupport tower-performance claim.
- Not yet a large-seed, multi-instance, statistically powered result.

## Project Owner Attribution Ledger

This section separates the most important Project Owner contributions from
Codex implementation activity.

### Project Owner Discoveries And Corrections

The Project Owner:

- requested the original TeX attribution checkpoint for Project Owner/Abdul
  authorship hygiene;
- corrected Codex when degenerate-tier work drifted into broad new design
  questions instead of the actual handoff integration;
- identified that generated artifact results were hard for humans and needed a
  protocol-driven readout process;
- clarified that the readout protocol invocation must point at a repo-side
  `readout_source.json`;
- insisted generated readout conversations be archived into
  `docs/design/system_learning_from_evaluations/` before regeneration erased
  useful design memory;
- introduced binary search as a preferred explanation device for coarse-to-fine
  tower issues;
- requested the direct-image threshold-binding documentation issue for future
  engineers;
- caught a severe false-attribution failure where Codex had written
  model-authored text under Project Owner turn headings;
- reasoned through the pointwise liftability problem and identified that a lift
  must be executable from the actual current concrete/base state;
- supplied the conceptual bridge from the BBB issue to `state_collapser` v0.7.2
  upstream work;
- pushed counterpoint from smoke surfaces to more serious next-measure probes;
- rejected overclaiming from tiny counterpoint signals;
- redirected the project toward a robotics-style PlateSupport benchmark because
  the counterpoint effect was too small;
- identified the standard gauntlet pattern as a reusable evaluation pipeline;
- caught Codex fragmenting the umbrella gauntlet execution into child-stage
  endpoints;
- asked for graph statistics/outdegree reasoning when PlateSupport candidate
  discovery failed;
- recalled and requested the source-local ratio contraction idea and asked that
  ratio be a knob;
- requested the iterated PlateSupport source-local-ratio schema with `0.9`
  near-collapse threshold;
- clarified that the PlateSupport correction should copy counterpoint's
  iterated planning shape where appropriate;
- forced root docs to reflect the current PlateSupport `iterated_001` result.

### Codex Implementation Contributions

Codex:

- created and updated design documents, blueprints, workplans, and
  implementation logs under the Project Owner's direction;
- implemented BBB integration with `state_collapser` v0.7.2 pointwise
  liftability APIs;
- updated counterpoint masks, lift traces, invariant reports, readout metadata,
  and docs for pointwise semantics;
- reran and regenerated affected counterpoint evaluation readouts;
- implemented threshold frontier and small paired replicate probe machinery;
- built the first-class PlateSupport environment-readiness surface;
- implemented the PlateSupport standard gauntlet suite;
- implemented the iterated PlateSupport source-local-ratio correction;
- fixed stale generated-turn preservation in PlateSupport readout generation;
- fixed shared CSV writer line endings;
- updated root README and CONTRIBUTING to current evaluation status;
- recorded this continuity report.

### Upstream state_collapser Attribution

The `state_collapser` v0.7.2 pointwise liftability fix belongs to the
`state_collapser` side. BBB consumed that upstream release and integrated its
semantics.

BBB-side credit:

- dependency pinning and API checks;
- adapting counterpoint tower-control behavior;
- rerunning benchmark artifacts under corrected semantics;
- preserving the design handoff and diagnostic reports.

Upstream-side credit:

- actual pointwise liftability API behavior and synthetic blow revisions.

### TeX / Abdul Attribution

The root TeX document remains under the attribution boundary established by the
2026-06-02 checkpoint:

```text
docs/engineer_continuity/2026/06/02/2026-06-02_root_tex_pre_po_abdul_edit_attribution_checkpoint.md
```

Codex should not claim Project Owner/Abdul-authored TeX additions after that
checkpoint.

## Known Caveats And Residual Risks

1. The PlateSupport `iterated_001` result is bounded and smoke-scale.

   It is promising because multiple signals align, but it is not powered enough
   for broad performance claims.

2. Counterpoint positive evidence remains weak.

   The current best counterpoint evidence is a one-candidate, one-pair margin
   pattern plus threshold-frontier margin consistency. That is useful, but not
   decisive.

3. Old artifacts remain historical.

   Earlier artifact roots such as counterpoint `smoke_001` or pre-v0.7.2 runs
   may still exist. They should not be silently treated as current evidence.

4. Generated readouts are useful but must be regenerated through the protocol.

   Do not edit generated readout content as a substitute for fixing generator
   logic when a recurring issue appears.

5. Umbrella suite execution needs parent-spine discipline.

   Future "run the gauntlet" work should execute the parent suite sequence, not
   stop after child stages unless a true stop condition fires.

6. The `system_learning_from_evaluations` index may need to be expanded.

   It currently captures major counterpoint and PlateSupport learning threads,
   but future readout conversations should be archived there before readout
   regeneration overwrites them.

7. Validation counts have increased over time.

   Older logs record `224 passed`, `244 passed`, and `287 passed` at their
   respective points. The latest PlateSupport correction/readout fix pass later
   reached a larger suite count. Future engineers should trust the most recent
   validation log attached to the work they are resuming, not mix counts across
   dates.

## Current Best Next Moves

The next decision depends on Project Owner priority.

### Option 1: Strengthen PlateSupport

This is the most natural next scientific move if the goal is to test the
promising tower-control signal.

Possible next design:

- larger PlateSupport budgets;
- more matched seed bundles;
- more selected iterated candidates;
- maybe varied PlateSupport instances;
- same Stage 5 target logic unless the Project Owner changes the claim target.

Why:

- `iterated_001` is the first coherent robotics-style positive signal.
- The invalid-move gap is large enough to justify more serious measurement.

### Option 2: Return To Counterpoint Larger Comparisons

This is natural if the goal is to finish the counterpoint thread.

Possible next design:

- more candidates;
- more seed bundles;
- higher episode budget;
- perhaps a deeper/iterated counterpoint schema rather than one-drop noisy-rate.

Why:

- Counterpoint machinery is mature and pointwise-correct now.
- The signal is currently too small to overclaim.

### Option 3: Generalize The Standard Gauntlet

This is natural if the goal is framework hardening.

Possible next design:

- an environment-agnostic gauntlet registry;
- standard stage contracts;
- shared stage status/readout schema;
- reusable candidate discovery/training/threshold/comparison surfaces.

Why:

- The PlateSupport suite largely copied the counterpoint pipeline by hand.
- A third environment would benefit from less duplication.

## Handoff Summary For Next Engineer

If you are resuming this repo cold, start here:

1. Read this report.
2. Read root `README.md` and `CONTRIBUTING.md`.
3. Read the latest PlateSupport readout:

   ```text
   docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/README.md
   ```

4. Read the PlateSupport iterated correction log:

   ```text
   docs/design/first_plate_support_environment/standard_gauntlet_suite/08_iterated_tower_correction/01_004_plate_support_iterated_tower_correction_implementation_log.md
   ```

5. If touching counterpoint runtime semantics, read:

   ```text
   docs/design/state_collapser_v072_pointwise_liftability_handoff/
   ```

6. If regenerating human-readable reports, use:

   ```text
   execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-readout-surface>/readout_source.json
   ```

7. If executing an umbrella suite, read:

   ```text
   docs/prime_directive/common_failure_mode_005_umbrella_workplan_fragmentation.md
   ```

The repo is now in a meaningfully better place than it was on 2026-06-02. The
key new scientific fact is not "tower methods are proven." The key new fact is:

```text
BBB can now construct real environment/evaluation/readout pipelines, integrate
upstream state_collapser semantic fixes, and produce a bounded positive
robotics-style tower-control signal with traceable artifacts.
```

