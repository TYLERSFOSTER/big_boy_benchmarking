# Counterpoint Symbolic V001 First Smoke

Status:

```text
smoke artifacts produced on 2026-05-28
```

Expected artifact-producing commands:

```bash
python -m big_boy_benchmarking.cli counterpoint search-fixtures --artifact-root <root>
python -m big_boy_benchmarking.cli counterpoint graph-diagnostics --artifact-root <root>
python -m big_boy_benchmarking.cli counterpoint run-direct --artifact-root <root>
python -m big_boy_benchmarking.cli counterpoint tower-smoke --artifact-root <root> --schema-id counterpoint_empty_schema_v001
```

No serious benchmark claim is recorded here yet. When smoke artifacts are
generated, this page should list their concrete artifact root and summarize only
what the artifacts actually show.

Artifact root:

```text
/private/tmp/bbb-counterpoint-phase13-20260528
```

Recorded smoke outputs:

- fixture search: 2 tiny candidates, selected first feasible candidate;
- graph diagnostics: 8 states, 16 edges, 10 artifacts;
- direct masked-random smoke: success;
- direct tabular-Q smoke: success;
- schema diagnostics: empty, random balanced, structured motion, random unbalanced, bad, and projection audit all wrote diagnostic artifacts;
- tower smoke: empty schema, structured motion schema, and random balanced schema all succeeded with compatibility readouts off.

Validation:

```text
uv run pytest
-> 99 passed in 1.02s

uv run ruff check .
-> All checks passed!
```

Claim boundary:

```text
These are implementation, contract, and smoke artifacts only. They are not
serious benchmark performance evidence.
```
