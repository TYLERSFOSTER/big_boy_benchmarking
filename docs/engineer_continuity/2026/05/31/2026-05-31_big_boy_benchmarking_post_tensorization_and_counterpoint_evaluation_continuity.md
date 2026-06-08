# Big Boy Benchmarking Continuity Report After Tensorization Pause

Created: 2026-06-01

Report date folder: 2026-05-31

Repository:

```text
<repo-root>
```

This report covers the work since the previous located continuity report:

```text
docs/engineer_continuity/2026/05/29/2026-05-29_counterpoint_serious_evaluation_pause_for_tensorization.md
```

The prior report paused first serious counterpoint evaluation work because the
Project Owner caught an important methodological distinction:

```text
pre-tensor state_collapser
!=
tensor-capable state_collapser with tensor execution present but disabled
```

This report starts after that pause and records what happened when
`state_collapser` caught up enough for `big_boy_benchmarking` to resume.

## Current Observed Repo State Before Adding This Report

Observed before this report file was created:

```text
branch: main
HEAD: 4c0b5fd 1/3 contraction schema run
origin/main: 4c0b5fd 1/3 contraction schema run
worktree: clean
```

Important branch note:

```text
main, origin/main, origin/HEAD, and codex/one-third-schema-tower-diagnostics
all point at 4c0b5fd at the time this report is written.
```

After this report is added, the only expected new dirty file is this continuity
report.

## One-Screen Summary

The repo moved from "paused pending tensorization" to "two durable
counterpoint evaluation readouts exist in repo-side evaluation surfaces."

The big arc was:

1. Integrate `state_collapser` tensorization/reporting surfaces into BBB.
2. Resume first serious counterpoint evaluation design.
3. Implement the first serious counterpoint learning evaluation.
4. Discover that raw tables and generated docs were readable to Codex but too
   opaque for human readers.
5. Build a repo-level human-readability protocol around explicit
   `readout_source.json` bindings.
6. Rerun and regenerate the first serious learning readout into a durable
   repo-side surface.
7. Integrate the upstream degenerate-tier handoff from `state_collapser`
   v0.7.1 so tower control can distinguish collapsed/non-executable tiers from
   executable base-tier paths.
8. Archive evaluation-driven learning in design-side durable memory so
   generated readouts can safely be regenerated.
9. Design and implement the one-third schema tower diagnostics evaluation.
10. Run that one-third diagnostic on small and medium counterpoint fixtures.
11. Apply the explicit artifact-table readout protocol to produce a full
    human-readable one-third diagnostic report.

Current high-level result:

```text
BBB is now a serious benchmark workspace with:
  - shared artifact/readout/mode/seed/timing machinery;
  - counterpoint_symbolic_v001 fixtures;
  - first serious learning evaluation readout;
  - one-third schema tower diagnostics readout;
  - repo-side protocol for translating artifact tables into human reports.
```

Current high-level scientific/engineering conclusion:

```text
Current non-empty counterpoint tower schemas are structurally diagnostic, not
performance-claiming.

The first serious learning run and one-third schema diagnostic both expose
first-projection collapse as the central issue for interpretation.
```

## PO Attribution And Critical Corrections

This period contained several important Project Owner corrections. They should
not be rewritten later as if Codex independently saw all of them.

Attribution is operationally important here. Several of the repo's most
important process and methodology improvements happened because the Project
Owner noticed drift, stopped it, and forced a correction. Future engineers and
LLMs should treat those corrections as first-class project history, not as
background noise.

The short version:

| Topic | Origin | Codex role | Durable result |
| --- | --- | --- | --- |
| Tensorization pause | Project Owner caught the methodological distinction between pre-tensor and tensor-capable-disabled benchmarking. | Codex investigated, accepted the correction, documented the pause, then integrated the later upstream surface. | `state_collapser` v0.7.x integration and `tensor_available_disabled` benchmark mode. |
| First serious evaluation shape | Project Owner redirected the work away from another structural-only block and said to do one learning test. | Codex converted the design into a serious learning/control evaluation with structural diagnostics as supporting evidence. | `first_counterpoint_serious_evaluation` blueprint/workplan and serious-learning runner. |
| Serious fixture scope | Project Owner answered that `small` is the serious fixture and `tiny` stays smoke/test-only. | Codex encoded small as the serious run fixture and kept tiny as calibration/smoke. | `counterpoint_symbolic_n3_small_v001` first serious readout; tiny labeled non-evidence. |
| Required baseline matrix | Project Owner required all proposed baselines, not a subset. | Codex kept masked-random, direct tabular-Q, empty schema, random balanced, random unbalanced, structured motion, and bad/adversarial arms. | Seven-arm first serious learning matrix. |
| Tower-evaluation meaning | Project Owner rejected Codex's loose tower-semantics answer and directed research in existing BBB and `state_collapser` docs/code. | Codex researched and bound the serious tower arm to upstream active-tier exploit/explore tower-control semantics. | Tower arms use `ExploitExploreTowerRuntime`/`ActiveTierController` rather than vague tower metadata. |
| Result-claim questioning | Project Owner rejected generic "what claim should this support?" questions as misaligned. | Codex narrowed the claim to one serious learning/control test on the small fixture with bounded non-claims. | Claim boundary in first serious blueprint/readout. |
| Budget questioning | Project Owner rejected invented budget-choice questions. | Codex moved budget choice into an engineering calibration step followed by a locked run budget. | Calibration/run split in serious-learning CLI and docs. |
| Evaluation docs placement | Project Owner identified that loose docs would confuse users and should live under a parent folder in `docs`. | Codex created/used `docs/evaluations/` as the result-facing parent. | `docs/evaluations/counterpoint_symbolic_v001/...`. |
| Degenerate-tier handoff scope | Project Owner corrected Codex's over-broad blueprint and narrowed the work back to upstream handoff integration. | Codex rewrote the blueprint/workplan and implemented the narrow handoff. | BBB adapter supplies `tier_is_executable` to upstream runtime. |
| Degenerate-tier failure mechanism | Project Owner drove the clarification of tower-arm meaning, zero returns, and whether the problem was missing rewards/model versus action realization. | Codex investigated artifacts and upstream code read-only, then reported the zero-step/lift mechanism. | `error_diagnosis_conversation.md` and later handoff integration work. |
| Hop-to-executable-tier rule | Project Owner identified the simple control-law correction: if a tier is degenerate/non-executable, move to a finer executable tier. | Codex translated the insight into ownership analysis and BBB handoff requirements. | Upstream `state_collapser` handoff plus BBB `tier_is_executable` wiring. |
| Handoff ownership | Project Owner suspected the durable fix belonged in `state_collapser`, not just BBB or one evaluation. | Codex agreed with the split: generic control invariant upstream, counterpoint realization local. | `state_collapser` v0.7.1 handoff integrated downstream. |
| Repo-resident artifacts | Project Owner repeatedly corrected Codex away from tmp/scratch artifact roots for durable readouts. | Codex updated docs, runbooks, protocols, and readout sources. | Durable artifacts live under `docs/evaluations/.../artifacts/<run-label>/`. |
| Readout command shape | Project Owner caught that folder-based invocation was ambiguous and caused protocol drift. | Codex fixed the protocol and root docs to require explicit protocol-file plus source-binding invocation. | Canonical command points at `<repo-readout-surface>/readout_source.json`. |
| Human readability requirement | Project Owner identified that raw evaluation results were hard for humans despite being readable to Codex. | Codex wrote and iterated the artifact-table readout protocol. | Generated readouts now include goals, methodology, verdict, badges, diagnostics, evidence maps, and turn surfaces. |
| Generated README design memory | Project Owner insisted that important conversation in regenerable readouts must be archived outside the generated surface. | Codex created the system-learning archive structure and preserved the first serious learning thread. | `docs/design/system_learning_from_evaluations/`. |
| Tower shape and tier occupancy visibility | Project Owner asked whether BBB/`state_collapser` still had the ability to inspect tower shape and tier occupancy after `synthetic_blow` revisions. | Codex investigated both repos and identified that raw ability remained but reader-facing promotion was weak. | Protocol pressure for promoted `tower_shape_summary`, `tier_occupancy_summary`, and `lift_failure_by_tier` tables. |
| Direct-image threshold binding | Project Owner requested a note for future engineers about lower tiers binding upper-tier performance through direct-image thresholds. | Codex added BBB-side design memory and an upstream `logHRL_w_comments.tex` comment. | `direct_image_threshold_binding` archive plus upstream documentation note. |
| Full-graph collapse analysis | Project Owner asked for deeper numerical/system insight into why triadic labels could still cause total collapse, including the voice count `n`. | Codex analyzed the `n = 3`, 108-state, 1140-edge graph and edge-generated connectivity mechanism. | Structural-limit notes explaining full-graph initialization and edge-induced connected-component collapse. |
| Structural-limit headline | Project Owner corrected the generated readout away from generic `mixed` language for `H -> pi_0(H)`-like collapse. | Codex updated readouts and protocols to require first-projection collapse checks before performance language. | `Behavior: Structural Limit`, `Goals: Diagnostic`, and structural-limit checks in readout protocols. |
| Binary search explanation device | Project Owner requested binary search as a durable explanation analogy. | Codex added it to the relevant design-learning docs. | `docs/design/system_learning_from_evaluations/README.md`. |
| One-third evaluation placement | Project Owner clarified that this was a new evaluation on the existing counterpoint environment, not a new environment. | Codex created the right design/evaluation surfaces and implemented them there. | `one_third_schema_tower_diagnostics` under counterpoint environment/evaluation docs. |
| One-third tier-occupancy intent | Project Owner requested tier-occupancy details during training/control as a sanity check for whether hierarchy use could plausibly improve behavior. | Codex initially misunderstood the control polarity, then corrected after PO-directed research. | One-third diagnostics records ABC/tier signal and occupancy summaries. |
| ABC correction for one-third | Project Owner rejected Codex's U-shape interpretation and directed detailed research into `state_collapser` ABC/Always-Be-Closing design. | Codex corrected the runtime model to "find lowest executable unclosed" and stopped treating U-shape as the law. | One-third blueprint/workplan tests upstream ABC behavior rather than a homegrown policy. |
| Use upstream ABC, do not rewrite it | Project Owner emphasized that ABC logic already exists in `state_collapser` and BBB is trying to test it. | Codex constrained BBB to schema construction, `tier_is_executable`, instrumentation, and artifact reporting. | One-third runner delegates to upstream `ActiveTierController`/`ExploitExploreTowerRuntime`. |
| False attribution failure | Project Owner caught and rejected Codex writing blueprint material as if PO turns existed. | Codex added a Prime Directive failure-mode document and now must preserve blank turn slots unless real PO text exists. | `common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md`. |

If a future summary says "Codex discovered" any of the Project Owner-originated
items above, that summary is wrong. Codex's role was implementation,
documentation, synthesis, and correction after the PO's steering.

## Detailed PO-Originated Decisions Hidden In Design Turn Logs

This section exists because several critical Project Owner decisions are not
obvious from commit names or final readouts. They are preserved inside design
conversation documents. Future engineers should treat the files below as
primary attribution evidence.

### First Serious Evaluation Shape

Primary source:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
```

The Project Owner made the key design call that the resumed first serious
counterpoint block should be:

```text
one learning test
```

not another structural-only diagnostic. Structural machinery still mattered,
but it was demoted to support evidence and sanity checking. This is why the
implemented evaluation became a learning/control matrix rather than only tower
geometry.

The Project Owner also decided:

- `small` is the first serious fixture;
- `tiny` is smoke/test-only and should not enter serious result tables;
- all proposed baselines are required;
- generic "what claim should this support?" questions were misaligned;
- arbitrary budget questions were misaligned;
- result-facing docs need a parent location under `docs`, which became
  `docs/evaluations/`.

Those choices produced the first serious learning shape:

```text
direct masked-random
direct tabular-Q
empty-schema tower-control tabular
random balanced tower-control tabular
random unbalanced tower-control tabular
structured motion tower-control tabular
bad/adversarial tower-control tabular
```

Codex's role was to translate those decisions into a blueprint, workplan,
implementation, and readout. The decision to make this a first serious learning
test did not originate with Codex.

### Tower Evaluation Semantics

Primary source:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
```

Codex initially gave an answer about "tower evaluation" that was too loose and
too much like a generic tower-conditioned learner. The Project Owner rejected
that and said the answer was already extensively addressed in `state_collapser`
and BBB design decisions. The PO directed Codex to research and return with an
answer, not keep asking broad questions.

That correction matters because it forced the first serious tower arms to bind
to package-native active-tier exploit/explore semantics:

```text
ActiveTierController
ExploitExploreTowerRuntime
TierLearner
LiftResolveExecutor
FrozenLowerContext
TierSignalState
TierControlMetrics
```

The serious tower arms therefore should not be described as:

- tower construction only;
- posthoc structural diagnostics only;
- direct tabular-Q with tower metadata casually attached;
- compatibility-readout-driven learning;
- generic tower-position-key Q-learning, unless implementation research proves
  the upstream active-tier stack cannot be bound.

This was a PO-forced correction to Codex's framing.

### Budget And Claim Boundary Discipline

Primary source:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
```

The Project Owner rejected Codex's generic result-claim and budget questions as
invented/misaligned. The corrected design pattern was:

```text
calibrate first, then lock the serious run budget from measured runtime,
artifact volume, and curve/noise evidence.
```

That is why the serious-learning CLI has both calibration and locked-run
surfaces.

The allowed claim was not an abstract philosophical choice. It was bounded by
the actual benchmark:

```text
one serious learning/control test on counterpoint_symbolic_n3_small_v001 under
shared seed, budget, artifact, and tensor_available_disabled discipline.
```

### First Serious Readout Interpretation

Primary sources:

```text
docs/design/system_learning_from_evaluations/counterpoint_first_serious_learning_v001/01_readout_conversation_archive.md
docs/design/system_learning_from_evaluations/counterpoint_first_serious_learning_v001/02_issue_and_correction_notes.md
```

The Project Owner drove the interpretation cleanup after the first serious
learning run. The important PO-origin sequence was:

1. The PO asked for clearer explanation of the tower arms and what the zero
   return/zero-step statements actually meant.
2. The PO asked whether the zeroes could be explained by missing rewards or no
   real model.
3. The PO asked for a deeper diagnosis of the tower action-realization failure
   without changing either repo.
4. The PO then identified the simple degenerate-tier control insight: if the
   active tier is not executable, move to a finer executable tier.
5. The PO asked whether that control-law fix belonged upstream in
   `state_collapser`, local to BBB, or only in the evaluation.

Codex's diagnosis and downstream implementation followed from that PO-led
interrogation. The critical conclusion was:

```text
The failure was not missing reward, no model, or ordinary bad exploration.
It was action realization/executability at collapsed or inappropriate active
tiers.
```

### Tower Shape, Exp/Exp, And Direct-Image Aggregation

Primary source:

```text
docs/design/system_learning_from_evaluations/counterpoint_first_serious_learning_v001/01_readout_conversation_archive.md
```

The Project Owner asked two important questions that shaped the next protocol
and design-memory work:

1. Do BBB and `state_collapser` still have the ability to inspect tower shape
   and tier occupancy after the `synthetic_blow` revisions?
2. Could the negative results be attributable entirely to exploit/explore
   logic, and how do direct-image aggregation choices such as `max` or `avg`
   bind lower-tier thresholds to upper-tier performance?

The first question produced a key visibility distinction:

```text
the raw runtime/readout ability still exists, but BBB was not promoting the
right shape/occupancy/lift tables into human-readable evaluation summaries.
```

The second question became the durable direct-image threshold-binding
documentation issue:

```text
docs/design/system_learning_from_evaluations/direct_image_threshold_binding/
```

and an upstream note in:

```text
<state-collapser-repo>/docs/design/logHRL_w_comments.tex
```

This concern originated with the Project Owner. Codex documented it and
separated it from the immediate causal path of the current zero-step failures.

### Full-Graph Collapse Numerical Insight

Primary source:

```text
docs/design/system_learning_from_evaluations/counterpoint_first_serious_learning_v001/01_readout_conversation_archive.md
```

The Project Owner asked for a more complete analysis of why full-graph
initialization could cause extreme quotient collapse, and specifically asked
for:

- the voice count `n`;
- why labels that sound like three balanced triadic blocks can still collapse
  the whole graph;
- numerical or system insight into the collapse.

That PO question forced the important explanation:

```text
n = 3 voices
108 reachable tier-0 states
1140 legal edges
edge-generated contraction, not balanced state bucketing
```

The key system insight:

```text
Many natural-sounding labels over simultaneous transitions are giant
connectivity generators. Contracting enough edges merges source and target
state cells into connected components; it does not automatically produce a
balanced per-voice quotient.
```

This insight belongs to the PO-originated investigation prompt. Codex performed
the numerical analysis.

### Structural-Limit Headline Correction

Primary sources:

```text
docs/design/system_learning_from_evaluations/counterpoint_first_serious_learning_v001/01_readout_conversation_archive.md
docs/design/system_learning_from_evaluations/counterpoint_first_serious_learning_v001/02_issue_and_correction_notes.md
```

The Project Owner asked whether the runtime effectively did:

```text
H -> pi_0(H)
```

through `pr^0_1`, then corrected the readout discipline. The PO's point was
that it is irresponsible to describe apparent non-performance from such a
structural-limit evaluation as merely "mixed."

This PO correction changed the result classification:

```text
from: generic mixed behavior
to: structural-limit diagnostic
```

and forced protocol updates requiring readouts to check for full or near-full
first-projection collapse before using performance language.

### System-Learning Archive

Primary source:

```text
docs/design/system_learning_from_evaluations/counterpoint_first_serious_learning_v001/01_readout_conversation_archive.md
```

The Project Owner requested a durable design-side archive because generated
readout README files are allowed to be overwritten. The PO's two stated
architectural threads were:

```text
1. state_collapser / BBB troubleshooting discovered through environment runs;
2. natural user/engineer confusion points discovered while interpreting runs.
```

That PO request created:

```text
docs/design/system_learning_from_evaluations/
```

Codex proposed the specific folder/file shape, but the need for a durable
design-memory archive originated with the Project Owner.

### One-Third Diagnostic Intent And ABC Correction

Primary source:

```text
docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/design_discussion.md
```

The Project Owner framed the next evaluation as a new evaluation on the
existing counterpoint environment, not a new environment and not a comparison
benchmark. The PO wanted tower details for a one-third contraction schema,
including what tiers agents occupy during training/control.

Codex initially misunderstood the "U-shape" intuition and gave a wrong story
about tier movement. The Project Owner corrected that sharply, directing Codex
to research `state_collapser` ABC / "Always Be Closing" conversations and
report back.

The corrected model was:

```text
Do not hand-roll a U-shape story.
Use upstream ABC semantics:
find the lowest/highest-indexed currently unclosed executable tier and go
there.
```

Then the PO gave the key implementation constraint:

```text
Most ABC logic is already present in state_collapser.
BBB is trying to test that logic.
Do not rewrite it for this evaluation. Use it.
```

That PO instruction shaped the one-third implementation:

- BBB builds the one-third schema;
- BBB provides counterpoint-specific executability and artifact surfaces;
- BBB records ABC/tier/occupancy diagnostics;
- upstream `state_collapser` remains the controller/runtime authority.

### One-Third Evaluation As Existing-Environment Pattern

Primary source:

```text
docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/design_discussion.md
```

The PO's framing also established an important repo pattern:

```text
new evaluation != new environment
```

The one-third work therefore belongs under the existing environment family:

```text
docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/
```

This repo is now explicitly set up to add multiple evaluations against the
same environment.

### Tensorization Blocking Distinction

The Project Owner caught that benchmarking a pre-tensor package is not the same
as benchmarking a tensor-capable package with tensor execution disabled. That
was the reason the first serious evaluation paused on 2026-05-29.

BBB resumed only after `state_collapser` released enough tensorization surface
for BBB to record:

```text
tensor_available_disabled
```

as a real benchmark condition.

### Degenerate-Tier Scope Correction

During the degenerate-tier control work, Codex initially over-expanded the
blueprint into broad new architectural questions. The Project Owner corrected
that. The desired BBB work was narrower:

```text
Integrate the upstream state_collapser handoff so the existing counterpoint
evaluation can use the corrected tier executability behavior.
```

This became:

```text
docs/design/degenerate_tier_control/01_004_counterpoint_degenerate_tier_handoff_integration_blueprint.md
docs/design/degenerate_tier_control/01_005_counterpoint_degenerate_tier_handoff_integration_implementation_workplan.md
docs/design/degenerate_tier_control/01_006_counterpoint_degenerate_tier_handoff_integration_implementation_log.md
```

### Artifact Location Correction

The Project Owner repeatedly corrected Codex away from temporary artifact
locations. Durable evaluation runs and human readouts must live in the repo.

Current rule:

```text
For durable evaluation readouts, raw artifact roots belong under:

docs/evaluations/<environment>/<evaluation>/artifacts/<run-label>/

The human-readable readout surface is:

docs/evaluations/<environment>/<evaluation>/
```

Do not drift back to `<tmp-dir>` for durable evaluation results unless the
Project Owner explicitly asks for a scratch run.

### Readout Command Correction

The Project Owner identified that the folder-based command was ambiguous and
let Codex drift into running an evaluation `summarize` command instead of
applying the full human-readability protocol.

Correct command shape:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-readout-surface>/readout_source.json
```

Do not use:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-readout-surface>/readout_source.json
```

as the durable command. That old form is ambiguous.

### False PO Turn / Attribution Correction

The Project Owner caught and strongly rejected a serious process error: Codex
wrote blueprint content in a way that looked like it contained Project Owner
turns or Project Owner-authored content that the PO had not actually said.

This produced a new Prime Directive failure-mode document:

```text
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
```

The rule is simple:

```text
Do not put words in the Project Owner's mouth.
Do not write fake turns.
Do not convert consultant inference into PO attribution.
```

Generated readout README turn sections must use blank placeholders unless a
real human turn exists.

## Git Timeline Since The Last Report

Commits since the 2026-05-29 pause report include:

```text
a15dfd6 note
34bf3fe tensorization integration
533a39d first serious learning evaluation
020e70b evaluation run
4c9f6c7 docs update and cleanup
8fcedb0 human readablility protocol
d0879e4 human readability protocol
116e8df evaluation report refinement
c70e77d human reabable report protocol updated
e490abf workflow alignment across repo documentation
3abd6b0 downstream degenerate tier fix integration
031a757 artifacts stored now in repo
3f00b58 clean up
a978671 first actual eval, for counterpoint
5680253 first environment evaluation discussions
fdbf935 human interpretablility protocol fix
43acd96 evaluation error messaging records
bf7c3ec re-run of environment after protocol fix
83ffd14 Update root documentation to reflect new evaluation
c812f29 README
3e6588b 1/3 contraction evaluation design
c2fc286 1/3 evaluation implementation
4c0b5fd 1/3 contraction schema run
```

Human-readable grouping:

- `34bf3fe`: integrated `state_collapser` v0.7 tensorization/reporting
  surfaces.
- `533a39d`: implemented first serious learning evaluation machinery.
- `020e70b` through `bf7c3ec`: ran, cleaned, interpreted, and protocolized the
  first serious evaluation readout path.
- `3abd6b0`: integrated the downstream degenerate-tier handoff and moved BBB
  to `state_collapser` v0.7.1.
- `e490abf`, `8fcedb0`, `d0879e4`, `c70e77d`, `fdbf935`, `43acd96`: created
  and corrected the repo workflow and human-readability protocols.
- `3e6588b`, `c2fc286`, `4c0b5fd`: designed, implemented, ran, and read out
  the one-third schema tower diagnostics evaluation.

## Current Dependency State

`pyproject.toml` now pins:

```text
state-collapser[rl] @ git+https://github.com/TYLERSFOSTER/state_collapser.git@v0.7.1
```

`uv.lock` resolves:

```text
state-collapser version: 0.7.1
git rev: v0.7.1#0de2e2339a20c37f9d7e47d676550369f7bf1701
```

Important practical meaning:

```text
BBB is no longer testing a pre-tensor state_collapser package.
BBB is testing a tensor-capable package with the serious counterpoint default
linearization condition set to tensor_available_disabled.
```

Typographical note for future readers:

```text
The Python package name in code is state_collapser.
The distribution/dependency spelling in pyproject is state-collapser.
```

## Tensorization Integration Work

Primary docs:

```text
docs/design/shared_benchmark_machinery/01_004_state_collapser_tensorization_resume_note.md
docs/design/shared_benchmark_machinery/01_005_state_collapser_v0_7_tensorization_integration_workplan.md
docs/design/shared_benchmark_machinery/01_006_state_collapser_v0_7_tensorization_integration_implementation_log.md
```

Primary code areas touched:

```text
pyproject.toml
uv.lock
src/big_boy_benchmarking/upstream/state_collapser.py
src/big_boy_benchmarking/upstream/linearization.py
src/big_boy_benchmarking/modes/
src/big_boy_benchmarking/artifacts/
src/big_boy_benchmarking/environments/counterpoint/serious_learning/
tests/upstream/
tests/modes/
```

Capabilities added or strengthened:

- dependency-state capture now records relevant `state_collapser.training`
  tensorization/linearization symbols;
- optional torch import status is recorded without making torch mandatory;
- linearization mode contracts exist and are testable;
- serious counterpoint runs emit `linearization_manifest.json`;
- run manifests record `linearization_mode_id`,
  `linearization_benchmark_label`, and whether linearization was enabled;
- reserved linearization modes are rejected for the current serious
  counterpoint default unless explicitly designed later.

Current serious default:

```text
tensor_available_disabled
```

Important non-claim:

```text
BBB still does not claim tensor-enabled performance, CUDA behavior, or GPU
behavior.
```

Validation recorded in the implementation log included:

```text
uv run pytest
113 passed

uv run ruff check .
All checks passed
```

Later validation after one-third implementation reached:

```text
uv run pytest
183 passed

uv run ruff check src tests
All checks passed
```

## First Serious Counterpoint Learning Evaluation

Design docs:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/design_discussion.md
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_001_counterpoint_first_serious_learning_evaluation_blueprint.md
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_002_counterpoint_first_serious_learning_evaluation_implementation_workplan.md
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_003_counterpoint_first_serious_learning_evaluation_implementation_log.md
```

Implementation modules:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/
  __init__.py
  aggregation.py
  arms.py
  budgets.py
  config.py
  direct.py
  docs_writer.py
  evaluation_paths.py
  events.py
  manifests.py
  runner.py
  tower_control.py
```

Associated tests:

```text
tests/environments/counterpoint/test_serious_learning_arms.py
tests/environments/counterpoint/test_serious_learning_budgets.py
tests/environments/counterpoint/test_serious_learning_cli.py
tests/environments/counterpoint/test_serious_learning_config.py
tests/environments/counterpoint/test_serious_learning_direct.py
tests/environments/counterpoint/test_serious_learning_direct_runner.py
tests/environments/counterpoint/test_serious_learning_docs_writer.py
tests/environments/counterpoint/test_serious_learning_events.py
tests/environments/counterpoint/test_serious_learning_manifests.py
tests/environments/counterpoint/test_serious_learning_paths.py
tests/environments/counterpoint/test_serious_learning_runner.py
tests/environments/counterpoint/test_serious_learning_tower_control.py
```

CLI surfaces:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning calibrate ...
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning run ...
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning summarize ...
```

What the evaluation compares:

- direct masked-random;
- direct tabular-Q;
- empty-schema tower shell;
- random balanced tower;
- random unbalanced tower;
- structured motion tower;
- bad/adversarial tower.

Primary environment:

```text
counterpoint_symbolic_n3_small_v001
```

Current durable artifact run:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/pi0_h_evaluation_001
```

Current durable readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/
```

Current readout source binding:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/readout_source.json
```

Human-readable files:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/README.md
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/result_readout.md
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/results/summary.md
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/results/human_summary.md
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/results/arm_readout_table.md
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/results/diagnostic_findings.md
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/results/timing_readout.md
```

Current first serious readout verdict:

```text
All seven required arms produced machine-readable artifacts, and all 44 run
rows are marked success. That means the harness ran and wrote expected
evaluation tables. It does not mean every arm behaved equally well.
```

Behavior summary:

- direct baselines and empty-schema tower execute real 8-step episodes;
- direct and empty-schema returns are around `12.7`;
- structured-motion and bad/adversarial tower arms execute real episodes but
  under full first-projection collapse;
- random balanced and random unbalanced arms expose schema-seed-dependent
  lift/action-realization failures;
- failing random-schema runs show `no_lift_candidate_from_current_state`;
- ordinary tower-performance interpretation is blocked by quotient collapse
  and lift/action-realization effects.

Important evidence status:

```text
The first serious readout is "Artifacts: Partial" because it predates promoted
tower-shape/tier-occupancy/lift summary tables. It reconstructs some facts from
per-run artifacts.
```

This is not a failure of the readout. It is a known artifact-contract maturity
boundary.

## Degenerate-Tier Handoff Integration

Design and implementation docs:

```text
docs/design/degenerate_tier_control/error_diagnosis_conversation.md
docs/design/degenerate_tier_control/01_003_big_boy_benchmarking_handoff_note.md
docs/design/degenerate_tier_control/01_004_counterpoint_degenerate_tier_handoff_integration_blueprint.md
docs/design/degenerate_tier_control/01_005_counterpoint_degenerate_tier_handoff_integration_implementation_workplan.md
docs/design/degenerate_tier_control/01_006_counterpoint_degenerate_tier_handoff_integration_implementation_log.md
```

Important process note:

The implementation log initially stopped at `Phase 0.2.3` because matching
handoff-integration edits were already dirty on `main`, and unrelated
documentation/readout changes were also present. The Project Owner then chose
how to bind/commit the work. The final result was committed as:

```text
3abd6b0 downstream degenerate tier fix integration
```

Code-level integration:

```text
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
```

The BBB counterpoint adapter now supplies:

```python
tier_is_executable
```

to upstream:

```python
state_collapser.tower.runtime.ExploitExploreTowerRuntime
```

The adapter predicate checks the current quotient state at the requested tier
and returns whether that tier has outgoing action cells. This was the important
BBB-side wiring for the upstream handoff: when the tower has collapsed or
non-executable coarser tiers, active-tier control needs to know which tiers can
actually emit executable actions.

Tests now check:

```text
tests/upstream/test_state_collapser_dependency_state.py
tests/environments/counterpoint/test_serious_learning_tower_control.py
```

Key test assertions:

- upstream `ExploitExploreTowerRuntime` exposes `tier_is_executable`;
- the counterpoint adapter's active/base tier is executable;
- not all non-base tiers are executable;
- invalid tier indices return false.

Important claim boundary:

```text
This fix does not mean non-empty tower schemas now learn well.
It means the runtime can distinguish executable and non-executable tiers in the
way the upstream handoff requires.
```

## Human-Readable Artifact Protocol Work

Primary protocol:

```text
docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

Related protocols:

```text
docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
```

Prime Directive index:

```text
docs/prime_directive/README.md
```

Why this happened:

The raw machine artifacts were good enough for Codex to interpret but too hard
for a human to decipher quickly. The first serious evaluation made this pain
obvious. A report that only lists aggregate tables, artifact paths, or status
fields is not a benchmark readout.

Current protocol rule:

```text
A result document must tell the reader what happened, how we know, what it
means, what it does not mean, and where the machine evidence lives.
```

Canonical invocation:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-readout-surface>/readout_source.json
```

Default output shape:

```text
<repo-readout-surface>/
  readout_source.json
  README.md
  result_readout.md
  runbook.md
  artifact_index.md
  glossary.md
  badges/
    artifacts_<status>.svg
    behavior/schema/abc/lift/etc_<status>.svg
    goals_<status>.svg
    scope_<status>.svg
    provenance_<status>.svg
  results/
    summary.md
    human_summary.md
    arm_readout_table.md
    diagnostic_findings.md
    timing_readout.md
```

Important protocol features added:

- explicit `readout_source.json` source binding;
- strict separation between repo readout surface, source artifact root, and
  source evaluation root;
- repo-resident artifact-root rule for durable readouts;
- local SVG badges and compact `Status At A Glance`;
- populated goals and methodology sections;
- protected `Clarifying Questions And Turns` section at the bottom of generated
  README files;
- turn-preservation rules on regeneration;
- absent-file classification:
  `expected_missing_gap`, `conditional_absent`, `not_applicable`,
  `unknown_expectation`;
- zero/null/missing/failure all-cases rules;
- explicit warning that `status=complete` does not mean behavior succeeded.

Current bad command:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-readout-surface>/readout_source.json
```

Current good command:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-readout-surface>/readout_source.json
```

This matters because the old command let Codex mistakenly treat an evaluation
`summarize` command as equivalent to the full human-readability protocol.

## Workflow Documentation Update

Root and docs-level workflow documentation was updated so future readers see
the actual system that emerged.

Important files:

```text
README.md
docs/README.md
docs/evaluations/README.md
docs/environments/README.md
docs/methods/README.md
docs/methods/artifact_contract.md
docs/methods/counterpoint_serious_learning.md
```

The repo now explicitly presents a three-stage workflow:

```text
1. Construct environments.
2. Construct evaluations for those environments.
3. Process run artifacts into repo-side human-readable readouts.
```

Protocol mapping:

```text
environment construction:
  docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md

evaluation construction:
  docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md

artifact readout:
  docs/prime_directive/artifact_table_to_readable_document_protocol.md
```

Current README now lists completed evaluation readouts and states what can and
cannot be concluded from them.

## System Learning From Evaluations

New durable design-memory area:

```text
docs/design/system_learning_from_evaluations/
```

Purpose:

```text
Evaluation readouts under docs/evaluations are allowed to be regenerated.
This folder preserves lessons, confusions, corrections, and future architecture
issues discovered while interpreting those evaluations.
```

Current index:

```text
docs/design/system_learning_from_evaluations/README.md
```

Current archived issue folders:

```text
docs/design/system_learning_from_evaluations/counterpoint_first_serious_learning_v001/
docs/design/system_learning_from_evaluations/direct_image_threshold_binding/
```

`counterpoint_first_serious_learning_v001` contains:

- mostly verbatim conversation/archive material;
- distilled issue and correction notes;
- attribution-sensitive explanation of what the first serious learning run
  taught us.

`direct_image_threshold_binding` records a documentation issue that may become
architecture work later:

```text
lower-tier thresholds can bind upper-tier performance through direct-image
aggregation choices such as max or avg.
```

This issue was also documented upstream in `state_collapser` at the Project
Owner's request, in the correct file:

```text
<state-collapser-repo>/docs/design/logHRL_w_comments.tex
```

Important explanation device:

```text
Binary search is the default analogy for many future explanations.
```

The intuition:

- coarse tests only help if they preserve the right refinement;
- a threshold can safely discard impossible regions or accidentally discard the
  answer;
- quotient tiers and direct-image aggregation are modified versions of that
  basic coarse-to-fine search problem.

## First Serious Readout Cleanup And Regeneration

The first serious learning readout went through a painful but important
cleanup.

Important sequence:

1. A run existed in temporary or old artifact surfaces.
2. The Project Owner reminded Codex that durable artifacts must be in the repo.
3. Old generated/readout files were cleared.
4. The corrected artifact root was created under:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/artifacts/pi0_h_evaluation_001
```

5. The serious evaluation was rerun.
6. The human-readability protocol was applied to the repo-side source binding.
7. Clarifying conversation was archived under system learning before the README
   was allowed to be regenerated.

Current canonical first serious readout regeneration:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-root>/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/readout_source.json
```

## One-Third Schema Tower Diagnostics Design

Design folder:

```text
docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/
```

Key files:

```text
design_discussion.md
01_001_counterpoint_one_third_schema_tower_diagnostics_blueprint.md
01_002_counterpoint_one_third_schema_tower_diagnostics_implementation_workplan.md
01_003_counterpoint_one_third_schema_tower_diagnostics_implementation_log.md
```

The evaluation's intent:

```text
Study a source-local one-third contraction schema on the existing counterpoint
environment, not as a direct-vs-tower comparison, but as a tower-shape and ABC
runtime diagnostic.
```

Why this was not a new environment:

```text
The environment remains counterpoint_symbolic_v001.
The new work is a new evaluation over that environment.
```

Important design rule confirmed:

```text
The repo is set up naturally for multiple evaluations per environment.
```

The one-third diagnostic is the first proof of that pattern after the first
serious learning readout.

## One-Third Schema Implementation

Implementation branch:

```text
codex/one-third-schema-tower-diagnostics
```

Merged/fast-forwarded to:

```text
main at 4c0b5fd
```

Primary modules:

```text
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/
  __init__.py
  aggregation.py
  config.py
  docs_writer.py
  events.py
  manifests.py
  paths.py
  runner.py
```

Related existing modules updated:

```text
src/big_boy_benchmarking/environments/counterpoint/ids.py
src/big_boy_benchmarking/environments/counterpoint/instances.py
src/big_boy_benchmarking/environments/counterpoint/schemas.py
src/big_boy_benchmarking/environments/counterpoint/tower_adapter.py
src/big_boy_benchmarking/cli/main.py
docs/environments/counterpoint_symbolic_v001.md
```

New fixture:

```text
counterpoint_symbolic_n3_medium_v001
```

Medium fixture observed enumeration:

```text
states: 228
edges: 2732
```

One-third schema:

```text
counterpoint_one_third_outgoing_schema_v001
```

Schema construction:

```text
For each source state, outgoing edges are deterministically shuffled by schema
seed and recursively assigned into one-third blocks using ceil(remaining / 3).
Leftovers are explicit one_third_unscheduled edges.
```

CLI surfaces:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics run ...
uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics summarize ...
```

Validation recorded in the implementation log:

```text
uv run pytest tests/environments/counterpoint/test_instances.py
3 passed

uv run pytest tests/environments/counterpoint/test_tower_adapter.py tests/environments/counterpoint/test_schemas.py tests/environments/counterpoint/test_ids.py
12 passed

uv run pytest tests/environments/counterpoint/test_one_third_diagnostics.py
6 passed

uv run pytest tests/environments/counterpoint tests/upstream
138 passed

uv run pytest
183 passed

uv run ruff check src tests
All checks passed

git diff --check
passed with no output
```

## One-Third Schema Run And Readout

Durable readout surface:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/
```

Current artifact root:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/small_medium_validation_001
```

Current source evaluation root:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/small_medium_validation_001/evaluations/counterpoint_one_third_schema_tower_diagnostics_v001
```

Current source binding:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/readout_source.json
```

Current human-readable readout files:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/README.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/result_readout.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifact_index.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/glossary.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/method.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/runbook.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/results/summary.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/results/human_summary.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/results/arm_readout_table.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/results/diagnostic_findings.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/results/timing_readout.md
```

Local badges:

```text
badges/artifacts_complete.svg
badges/schema_full_collapse.svg
badges/abc_complete.svg
badges/lift_executable.svg
badges/scope_diagnostic_only.svg
badges/provenance_repo_artifacts.svg
```

Current one-third run facts:

```text
run_count: 24
complete_run_count: 24
instances:
  counterpoint_symbolic_n3_small_v001: 12 runs
  counterpoint_symbolic_n3_medium_v001: 12 runs
schema seeds: 0, 1, 2
replicates per schema seed: 4
episodes per replicate: 16
linearization: tensor_available_disabled
```

Core diagnostic result:

```text
All 24 runs show full first-projection collapse.
```

Tower shape:

```text
small state cells by tier:  (108, 1, 1, 1)
medium state cells by tier: (228, 1, 1, 1)
```

Execution result:

```text
episodes: 384
concrete steps: 3840
lift attempts: 3840
lift successes: 3840
lift failures: 0
terminated episodes: 384
truncated episodes: 0
```

ABC/control result:

```text
ABC events: 4800
action-consistent events: 4800
control action totals:
  explore: 2418
  exploit_execute: 1422
  train: 960
```

Interpretation:

```text
The one-third schema is constructible and BBB can observe its tower geometry,
ABC signals, lift behavior, and concrete steps. But the schema fully collapses
the first quotient projection on both current fixtures.

This is a structural-limit diagnostic, not a learning-performance result.
```

Correct readout regeneration command:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-root>/docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/readout_source.json
```

## Current Completed Evaluation Readouts

### First Serious Learning

Surface:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/
```

Artifact run:

```text
pi0_h_evaluation_001
```

Status:

```text
complete structural-limit diagnostic, artifact evidence partial
```

Main conclusion:

```text
The harness, artifact pipeline, direct baselines, empty tower shell, and human
readout path work on counterpoint_symbolic_n3_small_v001. Non-empty tower arms
are dominated by full or near-full first-projection collapse and
lift/action-realization effects.
```

### One-Third Schema Tower Diagnostics

Surface:

```text
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/
```

Artifact run:

```text
small_medium_validation_001
```

Status:

```text
complete structural-limit diagnostic, artifact evidence complete
```

Main conclusion:

```text
The source-local one-third schema runs through upstream ABC control on small
and medium. All 24 locked runs fully collapse at the first projection, while
runtime execution itself does not stall.
```

## What The Repo Can Now Do

Current runnable surfaces include:

```bash
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Counterpoint smoke/diagnostics:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint graph-diagnostics \
  --artifact-root <artifact-root> \
  --instance-id tiny

uv run python -m big_boy_benchmarking.cli counterpoint run-direct \
  --artifact-root <artifact-root> \
  --instance-id tiny \
  --policy masked-random \
  --seed 1 \
  --episodes 1

uv run python -m big_boy_benchmarking.cli counterpoint tower-smoke \
  --artifact-root <artifact-root> \
  --instance-id tiny \
  --schema-id counterpoint_motion_schema_v001 \
  --seed 2
```

First serious learning:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning calibrate ...
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning run ...
uv run python -m big_boy_benchmarking.cli counterpoint serious-learning summarize ...
```

One-third diagnostics:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics run ...
uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics summarize ...
```

Human-readable readout protocol:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-readout-surface>/readout_source.json
```

## Current Claims Supported

Supported:

- BBB can run serious counterpoint evaluation machinery against a
  tensor-capable `state_collapser` dependency with tensor execution disabled.
- BBB can record dependency, mode, timing, linearization, seed, event, and
  artifact metadata for counterpoint runs.
- `counterpoint_symbolic_n3_small_v001` supports the first serious learning
  evaluation surface.
- `counterpoint_symbolic_n3_medium_v001` exists and supports the one-third
  diagnostic surface.
- Direct masked-random, direct tabular-Q, and empty-schema tower arms can
  execute real episodes on the small fixture.
- Non-empty broad/full-graph schemas can collapse the first quotient
  projection so aggressively that ordinary learner-performance language is
  blocked.
- The source-local one-third schema also fully collapses the first projection
  on both small and medium fixtures.
- The one-third diagnostic proves that full quotient collapse can coexist with
  healthy base-tier concrete execution and lift success.
- Human-readable readouts now have a stable repo-side protocol and output
  shape.

Not supported:

- general tower superiority;
- general tower inferiority;
- tensor-enabled runtime performance;
- CUDA/GPU behavior;
- musical-quality claims;
- production-performance claims;
- claims beyond the named fixtures, budgets, schema seeds, and
  `tensor_available_disabled` condition.

## Current Known Weaknesses And Warnings

### First Serious Artifact Contract Is Older

The first serious learning readout is useful and durable, but it predates some
promoted evaluation-level tables.

Current README status:

```text
Artifacts: Partial
```

Reason:

```text
expected evaluation manifests and promoted tower summary tables are absent;
some tower facts are reconstructed from per-run artifacts.
```

Do not treat that as equivalent to the one-third diagnostics artifact maturity.
The one-third diagnostic has promoted geometry, ABC, lift, concrete-step, and
tier summary tables.

### One-Third Schema Is Structurally Limiting

The one-third schema is not a next-performance candidate in its current form.
It is a useful diagnostic because it shows how easily source-local contraction
can collapse `pr^0_1`.

Any future one-third-like schema work should ask:

```text
What refinement rule preserves enough tier-1 state distinction to make
higher-tier control meaningful?
```

### Protocol Drift Is A Live Risk

The readout protocol was corrected because Codex drifted from "apply the
protocol" to "run summarize." Future LLMs must not repeat that.

The command target is:

```text
readout_source.json
```

not:

- README;
- artifact root;
- evaluation root;
- "last run";
- a folder with tables.

### Generated Readouts Are Regenerable

Generated evaluation README files are not the only place to store design
learning. If a generated README accumulates important conversation, archive it
under:

```text
docs/design/system_learning_from_evaluations/
```

before regenerating.

### Do Not Invent Human Turns

This is now formal Prime Directive material. Future LLMs must leave blank turn
slots blank unless there is real Project Owner text to preserve.

## Important Files To Read When Resuming

Start here:

```text
README.md
docs/README.md
docs/prime_directive/README.md
docs/prime_directive/prime_directive.md
docs/prime_directive/common_failure_mode_004_false_attribution_and_invented_project_owner_turns.md
```

For current evaluation status:

```text
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/README.md
docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/result_readout.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/README.md
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/result_readout.md
```

For artifact/readout protocol:

```text
docs/prime_directive/artifact_table_to_readable_document_protocol.md
docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md
docs/prime_directive/environment_construction_for_benchmark_evaluations_protocol.md
```

For serious learning implementation:

```text
docs/design/first_counterpoint_environment/first_counterpoint_serious_evaluation/01_003_counterpoint_first_serious_learning_evaluation_implementation_log.md
src/big_boy_benchmarking/environments/counterpoint/serious_learning/
```

For degenerate-tier handoff:

```text
docs/design/degenerate_tier_control/01_006_counterpoint_degenerate_tier_handoff_integration_implementation_log.md
src/big_boy_benchmarking/environments/counterpoint/serious_learning/tower_control.py
```

For one-third diagnostics:

```text
docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/01_003_counterpoint_one_third_schema_tower_diagnostics_implementation_log.md
src/big_boy_benchmarking/environments/counterpoint/one_third_diagnostics/
docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/
```

For durable design learning:

```text
docs/design/system_learning_from_evaluations/README.md
docs/design/system_learning_from_evaluations/counterpoint_first_serious_learning_v001/README.md
docs/design/system_learning_from_evaluations/direct_image_threshold_binding/README.md
```

## Suggested Next Technical Moves

These are not decisions already made. They are likely next design moves.

### 1. Design A Less-Collapsing Counterpoint Schema

The current structural evidence says broad schemas are too collapsing. The next
useful schema design probably needs to preserve enough tier-1 state distinction
to make active-tier control meaningful.

Use binary search as an explanation device:

```text
What coarse partition preserves the information needed to decide where to
refine next?
```

### 2. Promote First Serious Artifact Tables If Needed

The first serious readout reconstructs some tower facts from per-run artifacts.
Future reruns should probably use the newer one-third-style promoted tables:

- tower shape summary;
- tier occupancy summary;
- lift failure by tier;
- concrete step summary;
- ABC/tier signal rows if relevant.

### 3. Add A Comparison Evaluation Only After A Healthy Schema Exists

The one-third diagnostic intentionally has no direct-vs-tower comparison. That
was correct. A future comparison should wait until there is at least one
non-empty schema that avoids immediate full first-projection collapse or until
the comparison is explicitly framed as collapse behavior.

### 4. Keep Tensor-Enabled Modes Reserved

Do not casually flip to `tensor_enabled_cpu` or `tensor_enabled_cuda`. Those are
reserved until designed, implemented, validated, and given artifact claim
boundaries.

### 5. Keep Report Generation Explicit

Any new evaluation should include:

- repo-side readout surface;
- `readout_source.json`;
- expected file policy;
- goal summary sources;
- methodology summary sources;
- local badges;
- protected README turn surface.

## Commands Worth Keeping Handy

Validate contracts:

```bash
uv run python -m big_boy_benchmarking.cli validate-contracts
```

Run all tests:

```bash
uv run pytest
```

Run lint:

```bash
uv run ruff check .
```

Regenerate first serious readout:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-root>/docs/evaluations/counterpoint_symbolic_v001/first_serious_learning/readout_source.json
```

Regenerate one-third readout:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at <repo-root>/docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/readout_source.json
```

Rerun one-third diagnostics into the current repo artifact surface:

```bash
export BBB_COUNTERPOINT_EVAL_ROOT="$PWD/docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics/artifacts/small_medium_validation_001"

uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics run \
  --artifact-root "$BBB_COUNTERPOINT_EVAL_ROOT" \
  --instance-ids small,medium \
  --schema-seeds 0,1,2 \
  --replicates 4 \
  --episodes 16 \
  --base-seed 0 \
  --locked-by cli \
  --linearization-mode tensor_available_disabled

uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics summarize \
  --artifact-root "$BBB_COUNTERPOINT_EVAL_ROOT" \
  --docs-root "$PWD/docs/evaluations/counterpoint_symbolic_v001/one_third_schema_tower_diagnostics"
```

## Final Continuity Notes

The repo is in a much stronger state than it was at the 2026-05-29 pause.

The pause condition was resolved enough to proceed:

```text
state_collapser tensorization/reporting surface exists, and BBB records the
tensor_available_disabled mode explicitly.
```

The first serious evaluation did not produce a clean "tower works better"
result. It produced something more useful at this stage:

```text
evidence that broad quotient schemas can make ordinary performance language
invalid by collapsing the tower too aggressively.
```

The one-third diagnostic confirmed the same theme in a sharper form:

```text
even a source-local one-third outgoing-edge contraction can fully collapse the
first projection on current counterpoint fixtures, while base-tier execution
and lift remain healthy.
```

So the next intellectual problem is not "run more random schemas and hope."
The next problem is schema design and interpretation:

```text
What quotient information is preserved, what refinement decision does it
support, and where does it collapse?
```

This is why the binary-search explanation device matters. It keeps the problem
grounded: a coarse test is useful only if it preserves the information needed
to choose the next refinement.

Do not lose the hard-won protocol lesson:

```text
The machine artifacts are the source of truth.
The human readout is the source of understanding.
The source binding is the bridge.
```
