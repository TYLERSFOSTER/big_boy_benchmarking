# Root TeX Pre-Edit Attribution Checkpoint

Date: 2026-06-02

Repository:

```text
/Users/foster/big_boy_benchmarking
```

Root TeX document:

```text
tropicalization_and_binary_coset_towers.tex
```

## Purpose

This note records the state of the root TeX document immediately before the
Project Owner said they were about to add material with Abdul.

Project Owner instruction:

```text
Note the state of the tex document at root. I'm about to change it. I want you
to compress or record or whatever now, because I want attrbution for Abdul and
I when I add a bucnh of stuff
```

This checkpoint is for attribution hygiene. It does not claim authorship of
future TeX edits by Codex.

## Git State At Checkpoint

Current branch/status at checkpoint:

```text
## main...origin/main
 M docs/evaluations/counterpoint_symbolic_v001/noisy_rate_full_tower_training_diagnostic/README.md
 M tropicalization_and_binary_coset_towers.pdf
 M tropicalization_and_binary_coset_towers.tex
```

The evaluation README modification is from the preceding Codex reply in the
noisy-rate full-tower training diagnostic readout.

The TeX source and generated PDF were already modified before this checkpoint.
Codex did not edit either file as part of creating this attribution note.

## TeX Baseline Facts

Tracked file:

```text
tropicalization_and_binary_coset_towers.tex
```

Line count at checkpoint:

```text
321 tropicalization_and_binary_coset_towers.tex
```

SHA-256 at checkpoint:

```text
7d41972adebe528050c68e1f1abde6c41843eb73993d1084c2e805a57adaa4c0  tropicalization_and_binary_coset_towers.tex
```

## Existing TeX Dirty Diff At Checkpoint

At checkpoint time, the TeX file already differed from `HEAD` by a small block
near the start of the document body:

```diff
diff --git a/tropicalization_and_binary_coset_towers.tex b/tropicalization_and_binary_coset_towers.tex
index 99d7cb6..0f6c65e 100644
--- a/tropicalization_and_binary_coset_towers.tex
+++ b/tropicalization_and_binary_coset_towers.tex
@@ -128,6 +128,12 @@
 \begin{document}
 
 
+
+
+\hrule
+
+
+
 The shared concrete mechanism is:
 
 \[
```

This existing dirty diff should be treated as pre-checkpoint state unless the
Project Owner later clarifies its authorship.

## Attribution Boundary

For future engineering and documentation passes:

- Treat the hash above as the pre-PO/Abdul-addition baseline.
- Treat TeX changes after this checkpoint as Project Owner/Abdul-authored
  unless Codex is explicitly instructed to edit the TeX document.
- Do not attribute post-checkpoint TeX additions to Codex merely because Codex
  later reads, summarizes, compiles, or records them.
- If Codex later edits the TeX file, record that edit explicitly in a new
  checkpoint or implementation note.

## Codex Action Taken

Codex created this checkpoint note only.

Codex did not modify:

```text
tropicalization_and_binary_coset_towers.tex
tropicalization_and_binary_coset_towers.pdf
```
