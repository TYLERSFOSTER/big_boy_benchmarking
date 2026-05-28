# Upstream Smoke Readout Discipline V001

This smoke experiment validates the BBB harness, not a scientific claim.

Smoke ids:

```text
plate_support_env
rl_counterpoint_v3
```

Primary modes:

```text
tower_empty_schema_tabular
tower_nonempty_schema_tabular
```

Purpose:

- import pinned upstream smoke surfaces;
- write manifests and event tables under an explicit artifact root;
- record seed bundles and mode manifests;
- prove the default smoke path does not call compatibility readout;
- prove an explicitly diagnostic path can call compatibility readout and record
  that fact.

Expected artifact root shape:

```text
<artifact-root>/runs/upstream_smoke_readout_discipline_v001/
```

No benchmark claim is made by this smoke experiment.
