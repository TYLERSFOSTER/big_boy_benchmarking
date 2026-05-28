import csv
import json
from pathlib import Path

from big_boy_benchmarking.artifacts.writers import (
    append_csv_row,
    append_jsonl,
    write_json,
)


def test_json_writer_round_trips(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "payload.json"

    write_json(path, {"b": 2, "a": 1}, create_parents=True)

    assert json.loads(path.read_text(encoding="utf-8")) == {"a": 1, "b": 2}


def test_jsonl_append_round_trips(tmp_path: Path) -> None:
    path = tmp_path / "rows.jsonl"

    append_jsonl(path, {"row": 1})
    append_jsonl(path, {"row": 2})

    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert rows == [{"row": 1}, {"row": 2}]


def test_csv_append_writes_header_once(tmp_path: Path) -> None:
    path = tmp_path / "rows.csv"

    append_csv_row(path, {"a": 1, "b": 2}, ("a", "b"))
    append_csv_row(path, {"a": 3, "b": 4}, ("a", "b"))

    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows == [{"a": "1", "b": "2"}, {"a": "3", "b": "4"}]
    assert path.read_text(encoding="utf-8").splitlines()[0] == "a,b"
