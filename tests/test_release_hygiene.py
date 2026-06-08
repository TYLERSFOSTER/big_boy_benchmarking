import importlib.util
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "release_hygiene.py"
SPEC = importlib.util.spec_from_file_location("release_hygiene", SCRIPT_PATH)
assert SPEC is not None
release_hygiene = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = release_hygiene
SPEC.loader.exec_module(release_hygiene)

HygieneIssue = release_hygiene.HygieneIssue
scan_files = release_hygiene.scan_files


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_release_hygiene_detects_machine_local_paths(tmp_path: Path) -> None:
    _write(tmp_path / "README.md", "See /Users/example/project/docs.\n")

    issues = scan_files(tmp_path, [Path("README.md")])

    assert any(issue.check == "machine_local_path" for issue in issues)


def test_release_hygiene_detects_public_redaction_terms_without_source_literals(
    tmp_path: Path,
) -> None:
    term = "f" + "uck"
    _write(tmp_path / "docs" / "design" / "note.md", f"Do not publish {term}.\n")

    issues = scan_files(tmp_path, [Path("docs/design/note.md")])

    assert any(issue.check == "public_redaction_required" for issue in issues)


def test_release_hygiene_detects_generated_readout_placeholders(tmp_path: Path) -> None:
    _write(tmp_path / "docs" / "evaluations" / "demo" / "README.md", "> ...\n")

    issues = scan_files(tmp_path, [Path("docs/evaluations/demo/README.md")])

    assert any(issue.check == "public_placeholder" for issue in issues)


def test_release_hygiene_detects_tracked_byproducts(tmp_path: Path) -> None:
    path = Path("assets/images/.$diagrams.xml.bkp")
    _write(tmp_path / path, "backup\n")

    issues = scan_files(tmp_path, [path])

    assert HygieneIssue(
        check="tracked_byproduct",
        path=path.as_posix(),
        line=None,
        detail="tracked local/build byproduct should not be part of public beta",
    ) in issues
