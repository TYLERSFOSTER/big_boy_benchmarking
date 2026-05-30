# Counterpoint Symbolic V001 First Smoke

Status:

```text
historical smoke artifact set; local artifact root was not durable
```

Current reproducible smoke commands:

```bash
uv run python -m big_boy_benchmarking.cli counterpoint search-fixtures \
  --artifact-root <artifact-root>

uv run python -m big_boy_benchmarking.cli counterpoint graph-diagnostics \
  --artifact-root <artifact-root> \
  --instance-id tiny

uv run python -m big_boy_benchmarking.cli counterpoint run-direct \
  --artifact-root <artifact-root> \
  --instance-id tiny \
  --policy masked-random \
  --episodes 1

uv run python -m big_boy_benchmarking.cli counterpoint tower-smoke \
  --artifact-root <artifact-root> \
  --instance-id tiny \
  --schema-id counterpoint_empty_schema_v001
```

Recorded smoke outputs from the original local run:

- fixture search found tiny candidates and selected a feasible candidate;
- graph diagnostics wrote environment artifacts for 8 states and 16 edges;
- direct masked-random smoke succeeded;
- direct tabular-Q smoke succeeded;
- schema diagnostics wrote empty, random balanced, random unbalanced,
  structured motion, bad/adversarial, and projection-audit diagnostic artifacts;
- tower smoke succeeded for empty, structured motion, and random balanced
  schemas.

Current repo validation:

```text
uv run pytest -q
-> 171 passed
```

Claim boundary:

```text
These are implementation, contract, and smoke artifacts only. They are not
serious benchmark performance evidence.
```
