#!/usr/bin/env python3
"""Build a local release-asset bundle for raw evaluation artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import shutil
import subprocess
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

RELEASE_TAG = "v0.1.0-beta.1"
ASSET_NAME = "big_boy_calibration_smoke_v0.1.0-beta.1_artifacts.tar.zst"
MANIFEST_DIR = Path("docs/design/beta_public_release/release_asset_manifests")
STAGING_DIR = Path("dist/release-assets/v0.1.0-beta.1")


@dataclass(frozen=True)
class ArtifactRoot:
    source_evaluation_family: str
    artifact_role: str
    original_repo_relative_path: Path
    bundle_relative_path: Path
    byte_count: int
    file_count: int
    tree_sha256: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_head(repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def state_collapser_version(repo_root: Path) -> str:
    try:
        return importlib.metadata.version("state-collapser")
    except importlib.metadata.PackageNotFoundError:
        return "not-installed-in-current-runtime"


def relative_artifact_roots(repo_root: Path) -> list[Path]:
    roots = [
        path.relative_to(repo_root)
        for path in sorted((repo_root / "docs/evaluations").glob("**/artifacts"))
        if path.is_dir()
    ]
    deduped: list[Path] = []
    seen: set[Path] = set()
    for root in roots:
        if root not in seen:
            deduped.append(root)
            seen.add(root)
    return deduped


def iter_files(repo_root: Path, relative_root: Path) -> Iterable[Path]:
    root = repo_root / relative_root
    for path in sorted(root.rglob("*")):
        if path.is_file():
            yield path.relative_to(repo_root)


def tree_digest(repo_root: Path, relative_root: Path) -> tuple[int, int, str]:
    digest = hashlib.sha256()
    byte_count = 0
    file_count = 0
    for relative_file in iter_files(repo_root, relative_root):
        absolute_file = repo_root / relative_file
        file_digest = sha256_file(absolute_file)
        size = absolute_file.stat().st_size
        byte_count += size
        file_count += 1
        digest.update(relative_file.as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(size).encode("ascii"))
        digest.update(b"\0")
        digest.update(file_digest.encode("ascii"))
        digest.update(b"\n")
    return byte_count, file_count, digest.hexdigest()


def source_family_for(relative_root: Path) -> str:
    parts = relative_root.parts
    artifact_index = parts.index("artifacts")
    return str(Path(*parts[:artifact_index]))


def artifact_roots(repo_root: Path) -> list[ArtifactRoot]:
    roots: list[ArtifactRoot] = []
    for relative_root in relative_artifact_roots(repo_root):
        byte_count, file_count, tree_sha = tree_digest(repo_root, relative_root)
        roots.append(
            ArtifactRoot(
                source_evaluation_family=source_family_for(relative_root),
                artifact_role="raw_evaluation_artifact_tree",
                original_repo_relative_path=relative_root,
                bundle_relative_path=relative_root,
                byte_count=byte_count,
                file_count=file_count,
                tree_sha256=tree_sha,
            )
        )
    return roots


def write_file_index(repo_root: Path, roots: list[ArtifactRoot], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_evaluation_family",
                "artifact_role",
                "original_repo_relative_path",
                "bundle_relative_path",
                "byte_count",
                "sha256",
            ],
        )
        writer.writeheader()
        for root in roots:
            for relative_file in iter_files(repo_root, root.original_repo_relative_path):
                absolute_file = repo_root / relative_file
                writer.writerow(
                    {
                        "source_evaluation_family": root.source_evaluation_family,
                        "artifact_role": root.artifact_role,
                        "original_repo_relative_path": relative_file.as_posix(),
                        "bundle_relative_path": relative_file.as_posix(),
                        "byte_count": absolute_file.stat().st_size,
                        "sha256": sha256_file(absolute_file),
                    }
                )


def create_archive(repo_root: Path, roots: list[ArtifactRoot], staging_dir: Path) -> Path:
    staging_dir.mkdir(parents=True, exist_ok=True)
    archive_path = staging_dir / ASSET_NAME
    tar_path = staging_dir / ASSET_NAME.removesuffix(".zst")
    if archive_path.exists():
        archive_path.unlink()
    if tar_path.exists():
        tar_path.unlink()
    tar_command = [
        "tar",
        "-cf",
        str(tar_path),
        *[root.original_repo_relative_path.as_posix() for root in roots],
    ]
    subprocess.run(tar_command, cwd=repo_root, check=True)
    zstd = shutil.which("zstd")
    if zstd is None:
        raise RuntimeError("zstd is required for the approved .tar.zst artifact bundle")
    subprocess.run(
        [zstd, "-T0", "-3", "-f", str(tar_path), "-o", str(archive_path)],
        cwd=repo_root,
        check=True,
    )
    tar_path.unlink()
    return archive_path


def write_bundle_readme(
    repo_root: Path,
    roots: list[ArtifactRoot],
    archive_path: Path,
    archive_sha: str,
    state_collapser: str,
) -> str:
    total_files = sum(root.file_count for root in roots)
    total_bytes = sum(root.byte_count for root in roots)
    body = f"""# Big Boy Calibration / Smoke Artifact Bundle

Release tag target: `{RELEASE_TAG}`

Asset name: `{ASSET_NAME}`

This local release-asset bundle contains raw generated evaluation artifact
trees that were removed from the public git tree for beta release readiness.
The public repository keeps human-readable reports, compact summaries, badges,
methods, runbooks, and readout sources in git.

Compatibility target: `state_collapser {state_collapser}` or newer compatible
pointwise liftability semantics.

## Contents

- Artifact roots: {len(roots)}
- Files: {total_files}
- Raw bytes before compression: {total_bytes}
- Bundle SHA256: `{archive_sha}`

The bundle preserves each artifact tree at its original repo-relative path, for
example `docs/evaluations/.../artifacts/...`.

## Verification

From the repository root after downloading the release asset:

```bash
shasum -a 256 {ASSET_NAME}
```

Compare the result with `SHA256SUMS.txt` and
`docs/design/beta_public_release/release_asset_manifests/ARTIFACT_BUNDLE_MANIFEST.json`.

## Relationship To Public Readouts

Public readouts use `artifact_storage.mode = github_release_asset` to indicate
that raw event-level traces and run trees are external release assets, not
tracked git files. Compact human-readable results remain in
`docs/evaluations/`.

No tag, upload, or public repository visibility change is performed by this
bundle build step.
"""
    tracked_readme = repo_root / MANIFEST_DIR / "ARTIFACT_BUNDLE_README.md"
    staged_readme = archive_path.parent / "ARTIFACT_BUNDLE_README.md"
    tracked_readme.write_text(body, encoding="utf-8")
    staged_readme.write_text(body, encoding="utf-8")
    return body


def write_manifest(
    repo_root: Path,
    roots: list[ArtifactRoot],
    archive_path: Path,
    archive_sha: str,
    state_collapser: str,
) -> Path:
    manifest_path = repo_root / MANIFEST_DIR / "ARTIFACT_BUNDLE_MANIFEST.json"
    payload = {
        "release_tag": RELEASE_TAG,
        "repository_commit": git_head(repo_root),
        "state_collapser_version": state_collapser,
        "asset_name": ASSET_NAME,
        "asset_format": "tar.zst",
        "bundle_path": str(archive_path.relative_to(repo_root)),
        "bundle_sha256": archive_sha,
        "artifact_file_index": str((MANIFEST_DIR / "ARTIFACT_BUNDLE_FILE_INDEX.csv").as_posix()),
        "artifact_roots": [
            {
                "source_evaluation_family": root.source_evaluation_family,
                "artifact_role": root.artifact_role,
                "original_repo_relative_path": root.original_repo_relative_path.as_posix(),
                "bundle_relative_path": root.bundle_relative_path.as_posix(),
                "byte_count": root.byte_count,
                "file_count": root.file_count,
                "tree_sha256": root.tree_sha256,
            }
            for root in roots
        ],
    }
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def write_checksums(repo_root: Path, archive_path: Path, manifest_path: Path) -> Path:
    checksum_path = repo_root / MANIFEST_DIR / "SHA256SUMS.txt"
    tracked_readme = repo_root / MANIFEST_DIR / "ARTIFACT_BUNDLE_README.md"
    file_index = repo_root / MANIFEST_DIR / "ARTIFACT_BUNDLE_FILE_INDEX.csv"
    rows = [
        (sha256_file(archive_path), archive_path.relative_to(repo_root).as_posix()),
        (sha256_file(manifest_path), manifest_path.relative_to(repo_root).as_posix()),
        (sha256_file(file_index), file_index.relative_to(repo_root).as_posix()),
        (sha256_file(tracked_readme), tracked_readme.relative_to(repo_root).as_posix()),
    ]
    checksum_text = "".join(f"{digest}  {path}\n" for digest, path in rows)
    checksum_path.write_text(checksum_text, encoding="utf-8")
    shutil.copy2(checksum_path, archive_path.parent / "SHA256SUMS.txt")
    return checksum_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    roots = artifact_roots(repo_root)
    if not roots:
        raise RuntimeError("no docs/evaluations/**/artifacts roots found")
    manifest_dir = repo_root / MANIFEST_DIR
    staging_dir = repo_root / STAGING_DIR
    manifest_dir.mkdir(parents=True, exist_ok=True)
    staging_dir.mkdir(parents=True, exist_ok=True)
    file_index = manifest_dir / "ARTIFACT_BUNDLE_FILE_INDEX.csv"
    write_file_index(repo_root, roots, file_index)
    archive_path = create_archive(repo_root, roots, staging_dir)
    archive_sha = sha256_file(archive_path)
    state_collapser = state_collapser_version(repo_root)
    write_bundle_readme(repo_root, roots, archive_path, archive_sha, state_collapser)
    manifest_path = write_manifest(repo_root, roots, archive_path, archive_sha, state_collapser)
    checksum_path = write_checksums(repo_root, archive_path, manifest_path)
    print(
        json.dumps(
            {
                "status": "complete",
                "artifact_roots": len(roots),
                "artifact_files": sum(root.file_count for root in roots),
                "bundle": archive_path.relative_to(repo_root).as_posix(),
                "bundle_sha256": archive_sha,
                "manifest": manifest_path.relative_to(repo_root).as_posix(),
                "checksums": checksum_path.relative_to(repo_root).as_posix(),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
