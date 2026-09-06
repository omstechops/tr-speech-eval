import json
import sys
from collections.abc import Iterable, Mapping
from pathlib import Path

import pytest

from tr_speech_eval.burned import append_burned
from tr_speech_eval.manifest import (
    UNVERIFIED,
    Manifest,
    build_manifest,
    package_version,
    sha256_file,
    sha256_text,
)

EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def write_inputs(tmp_path: Path) -> tuple[Path, Path]:
    items = tmp_path / "items.jsonl"
    items.write_text('{"item_id": "i000"}\n', encoding="utf-8")
    ledger = tmp_path / "burned.jsonl"
    append_burned(ledger, ["i900"], reason="rubric-derivation")
    return items, ledger


def build(
    tmp_path: Path,
    *,
    systems: Mapping[str, str | None] | None = None,
    asr_checkpoint: str | None = "large-v3-turbo",
    # The real defaults are anthropic and mlx-whisper; neither is installed in
    # the test environment, and both would correctly show up as UNVERIFIED. Pin
    # a distribution that is installed so these tests exercise the field they
    # are about.
    tool_distributions: Iterable[str] = ("pytest",),
) -> Manifest:
    items, ledger = write_inputs(tmp_path)
    return build_manifest(
        run_id="run-001",
        seed=20260906,
        systems=systems
        if systems is not None
        else {"system_a": "id-a", "system_b": "id-b"},
        prompt="post-edit this",
        items_path=items,
        burned_ledger_path=ledger,
        asr_checkpoint=asr_checkpoint,
        tool_distributions=tool_distributions,
        created_at="2026-09-06T12:00:00+00:00",
    )


def test_sha256_text_matches_the_known_empty_digest() -> None:
    assert sha256_text("") == EMPTY_SHA256


def test_sha256_file_matches_its_contents(tmp_path: Path) -> None:
    path = tmp_path / "x.txt"
    path.write_text("merhaba", encoding="utf-8")
    assert sha256_file(path) == sha256_text("merhaba")


def test_sha256_file_refuses_a_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        sha256_file(tmp_path / "absent.jsonl")


def test_missing_values_are_written_as_unverified(tmp_path: Path) -> None:
    manifest = build(
        tmp_path,
        systems={"system_a": "id-a", "system_b": None, "judge": None},
        asr_checkpoint=None,
    )
    assert manifest.asr_checkpoint == UNVERIFIED
    assert manifest.systems["system_b"] == UNVERIFIED
    assert sorted(manifest.unverified_fields()) == [
        "asr_checkpoint",
        "systems.judge",
        "systems.system_b",
    ]


def test_a_complete_manifest_reports_nothing_missing(tmp_path: Path) -> None:
    assert build(tmp_path).unverified_fields() == []


def test_package_version_is_read_without_importing(tmp_path: Path) -> None:
    # mlx-whisper is an optional, platform-specific extra. Its version has to be
    # recordable by a process that never loads it.
    manifest = build(tmp_path, tool_distributions=("pytest", "mlx-whisper"))
    assert manifest.tool_versions["pytest"] == package_version("pytest")
    assert manifest.tool_versions["pytest"] != UNVERIFIED
    assert "mlx_whisper" not in sys.modules


def test_absent_distribution_is_unverified_not_omitted(tmp_path: Path) -> None:
    manifest = build(tmp_path, tool_distributions=("no-such-distribution-xyz",))
    assert manifest.tool_versions["no-such-distribution-xyz"] == UNVERIFIED
    assert manifest.unverified_fields() == ["tool_versions.no-such-distribution-xyz"]


def test_burned_ledger_hash_moves_when_the_ledger_grows(tmp_path: Path) -> None:
    first = build(tmp_path)
    append_burned(tmp_path / "burned.jsonl", ["i901"], reason="pilot")
    items = tmp_path / "items.jsonl"
    second = build_manifest(
        run_id="run-002",
        seed=1,
        systems={"system_a": "id-a"},
        prompt="post-edit this",
        items_path=items,
        burned_ledger_path=tmp_path / "burned.jsonl",
        created_at="2026-09-06T13:00:00+00:00",
    )
    assert first.burned_ledger_sha256 != second.burned_ledger_sha256


def test_write_round_trips(tmp_path: Path) -> None:
    manifest = build(tmp_path)
    path = tmp_path / "manifest.json"
    manifest.write(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["run_id"] == "run-001"
    assert payload["seed"] == 20260906
    assert payload["created_at"] == "2026-09-06T12:00:00+00:00"
    assert payload["prompt_sha256"] == sha256_text("post-edit this")
