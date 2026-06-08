#!/usr/bin/env python3
"""Release hygiene checks for the public beta tree."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

TEXT_SUFFIXES = {
    ".csv",
    ".json",
    ".md",
    ".py",
    ".rst",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

PUBLIC_TEXT_PREFIXES = (
    ".github/",
    "docs/",
)

PUBLIC_TEXT_ROOTS = {
    ".gitignore",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "pyproject.toml",
}

BYPRODUCT_SUFFIXES = (
    ".aux",
    ".bbl",
    ".blg",
    ".pyc",
    ".pyo",
    ".synctex.gz",
)

BYPRODUCT_NAMES = {
    ".DS_Store",
    ".$diagrams.xml.bkp",
}

ARTIFACT_LARGE_FILE_LIMIT_BYTES = 1_000_000


@dataclass(frozen=True)
class HygieneIssue:
    check: str
    path: str
    line: int | None
    detail: str

    def render(self) -> str:
        location = self.path if self.line is None else f"{self.path}:{self.line}"
        return f"{self.check}: {location}: {self.detail}"


def _join(*parts: str) -> str:
    return "".join(parts)


def _redaction_terms() -> tuple[str, ...]:
    """Build release-redaction terms without storing them as raw source tokens."""

    return (
        _join("f", "uck"),
        _join("f", "ucking"),
        _join("f", "ucked"),
        _join("f", "uckign"),
        _join("f", "ucing"),
        _join("s", "hit"),
        _join("c", "unt"),
        _join("b", "itch"),
        _join("mother", "fuck"),
        _join("w", "tf"),
    )


def redaction_pattern() -> re.Pattern[str]:
    terms = sorted((re.escape(term) for term in _redaction_terms()), key=len, reverse=True)
    return re.compile("|".join(terms), re.IGNORECASE)


def local_path_pattern() -> re.Pattern[str]:
    users = "/" + "Users" + "/"
    tmp = "/" + "private" + "/" + "tmp"
    var = "/" + "private" + "/" + "var"
    alternatives = (
        rf"{re.escape(users)}[^\s)\"<>]+",
        rf"{re.escape(tmp)}[^\s)\"<>]*",
        rf"{re.escape(var)}[^\s)\"<>]*",
    )
    return re.compile(f"({'|'.join(alternatives)})")


def placeholder_pattern() -> re.Pattern[str]:
    return re.compile(r"(^>\s*\.\.\.\s*$|_Open\._)", re.MULTILINE)


def stale_command_pattern() -> re.Pattern[str]:
    return re.compile(
        r"("
        r"execute artifact-table readout pointed at folder"
        r"|"
        r"artifact-table readout pointed at folder"
        r")",
        re.IGNORECASE,
    )


def tracked_files(repo_root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "ls-files"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [Path(line) for line in result.stdout.splitlines() if line.strip()]


def is_text_path(path: Path) -> bool:
    return path.suffix in TEXT_SUFFIXES or path.name in PUBLIC_TEXT_ROOTS


def is_public_text_path(path: Path) -> bool:
    as_posix = path.as_posix()
    return (
        path.name in PUBLIC_TEXT_ROOTS
        or as_posix.startswith(PUBLIC_TEXT_PREFIXES)
    ) and is_text_path(path)


def is_generated_readout_or_writer(path: Path) -> bool:
    as_posix = path.as_posix()
    return (
        as_posix.startswith("docs/evaluations/")
        or as_posix.startswith("src/")
        and path.name.endswith("docs_writer.py")
    ) and is_text_path(path)


def is_artifact_file(path: Path) -> bool:
    parts = path.parts
    return "docs" in parts and "evaluations" in parts and "artifacts" in parts


def is_byproduct(path: Path) -> bool:
    name = path.name
    as_posix = path.as_posix()
    return (
        name in BYPRODUCT_NAMES
        or "__pycache__" in path.parts
        or any(as_posix.endswith(suffix) for suffix in BYPRODUCT_SUFFIXES)
    )


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def scan_files(repo_root: Path, files: list[Path]) -> list[HygieneIssue]:
    issues: list[HygieneIssue] = []
    redactions = redaction_pattern()
    local_paths = local_path_pattern()
    placeholders = placeholder_pattern()
    stale_commands = stale_command_pattern()

    for relative_path in files:
        absolute_path = repo_root / relative_path
        if is_byproduct(relative_path):
            issues.append(
                HygieneIssue(
                    check="tracked_byproduct",
                    path=relative_path.as_posix(),
                    line=None,
                    detail="tracked local/build byproduct should not be part of public beta",
                )
            )

        if is_artifact_file(relative_path) and absolute_path.exists():
            try:
                size = absolute_path.stat().st_size
            except OSError:
                size = 0
            if size > ARTIFACT_LARGE_FILE_LIMIT_BYTES:
                issues.append(
                    HygieneIssue(
                        check="large_tracked_artifact",
                        path=relative_path.as_posix(),
                        line=None,
                        detail=f"tracked artifact exceeds {ARTIFACT_LARGE_FILE_LIMIT_BYTES} bytes",
                    )
                )

        if not is_public_text_path(relative_path):
            continue

        text = read_text(absolute_path)
        if text is None:
            continue

        for match in local_paths.finditer(text):
            issues.append(
                HygieneIssue(
                    check="machine_local_path",
                    path=relative_path.as_posix(),
                    line=line_number(text, match.start()),
                    detail=(
                        "replace with repo-relative path, placeholder, "
                        "or explicit local provenance"
                    ),
                )
            )

        for match in redactions.finditer(text):
            issues.append(
                HygieneIssue(
                    check="public_redaction_required",
                    path=relative_path.as_posix(),
                    line=line_number(text, match.start()),
                    detail="replace raw term with [XXX] while preserving attribution",
                )
            )

        if is_generated_readout_or_writer(relative_path):
            for match in placeholders.finditer(text):
                issues.append(
                    HygieneIssue(
                        check="public_placeholder",
                        path=relative_path.as_posix(),
                        line=line_number(text, match.start()),
                        detail="replace placeholder or label it as intentional future reader space",
                    )
                )

        for match in stale_commands.finditer(text):
            issues.append(
                HygieneIssue(
                    check="ambiguous_readout_command",
                    path=relative_path.as_posix(),
                    line=line_number(text, match.start()),
                    detail="use explicit protocol-file command form",
                )
            )

    return issues


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to current working directory.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    repo_root = args.repo_root.resolve()
    issues = scan_files(repo_root, tracked_files(repo_root))
    if issues:
        print(f"release hygiene failed: {len(issues)} issue(s)")
        for issue in issues:
            print(issue.render())
        return 1

    print("release hygiene passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
