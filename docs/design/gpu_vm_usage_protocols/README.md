# GPU VM Usage Protocols

This folder is for designing the operational protocol for running
`big_boy_benchmarking` GPU workloads on remote VM infrastructure, probably
starting with GCP.

The immediate goal is not to implement cloud automation. The immediate goal is
to write down the reasoning protocol for how a human and Codex should decide:

- which GPU VM shape to use;
- how to provision it without losing reproducibility;
- how to sync code and artifacts safely;
- how to run long BBB training jobs without filling disks;
- how to monitor cost, progress, health, and failure modes;
- how to bring back only the artifacts/readouts that belong in the repo;
- how to keep raw run trees local, ignored, or packaged as release assets.

This matters because the Warehouse Gridlock PPO work has crossed the line from
local smoke testing into runs that may be too long or too storage-heavy for a
laptop. The protocol here should keep future GPU work explicit, reversible, and
auditable.

## Intended Documents

- `01_001_gpu_vm_usage_design_discussion.md`: turn-by-turn discussion about the
  protocol, with GCP as the likely first target.
- Later blueprint/workplan documents only after the protocol is clear.

## Initial Scope

The first design pass should answer:

- GCP versus other providers for the first remote run.
- Minimum viable GPU instance type for Warehouse Gridlock PPO.
- Disk sizing and retention policy defaults.
- How BBB source, `uv` dependencies, and `state_collapser` compatibility should
  be installed or pinned.
- Whether runs should happen in detached shell, `tmux`, systemd, Batch, or
  another managed execution surface.
- Which live progress surfaces Codex/PO should inspect during a run.
- Which files return to the repo, which stay on the VM, and which become release
  assets.
- Shutdown and cost-control rules.

## Conversation

### PO Turn

We are starting this folder to design VM GPU usage protocols, probably for GCP.

### Codex Turn

Understood. I will treat this as operational design first, not cloud
implementation. The key constraint is that GPU runs should not quietly change
the benchmarking evidence model: repo-side readouts remain human-readable
surfaces, raw artifacts stay ignored or packaged externally, and every serious
run should have a clear provisioning, retention, monitoring, and shutdown
protocol before it starts.
