# Summary

What changed?

## Affected Surface

- Environment:
- Evaluation or gauntlet:
- Protocol:
- Readout:

## Public Claim Boundary

What can a reader conclude after this change, and what should they not conclude?

## Readout And Artifact Handling

- [ ] Human-readable readouts were regenerated or intentionally left unchanged.
- [ ] `readout_source.json` files identify artifact storage mode.
- [ ] Raw artifacts are either compact enough for git or mapped to release
      assets.
- [ ] Public docs avoid machine-local paths.
- [ ] PO attribution and historical turns were preserved without invented
      wording.

## Verification

```bash
uv run python -m big_boy_benchmarking.cli --help
uv run pytest
uv run python scripts/release_hygiene.py --repo-root .
```
