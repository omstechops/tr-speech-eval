from pathlib import Path

from tr_speech_eval.blinding import Item
from tr_speech_eval.burned import append_burned, load_burned, reject_burned


def make_items(count: int) -> list[Item]:
    return [
        Item(item_id=f"i{index:03d}", source_ref="rec01", asr_raw="ham")
        for index in range(count)
    ]


def test_ledger_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "burned.jsonl"
    assert load_burned(path) == set()

    append_burned(path, ["i000", "i001"], reason="rubric-derivation")
    append_burned(path, ["i002"], reason="pilot")
    assert load_burned(path) == {"i000", "i001", "i002"}


def test_burned_items_are_kept_out(tmp_path: Path) -> None:
    path = tmp_path / "burned.jsonl"
    append_burned(path, ["i000", "i003"], reason="rubric-derivation")

    remaining = reject_burned(make_items(5), load_burned(path))
    assert [item.item_id for item in remaining] == ["i001", "i002", "i004"]


def test_ledger_is_append_only(tmp_path: Path) -> None:
    path = tmp_path / "burned.jsonl"
    append_burned(path, ["i000"], reason="rubric-derivation")
    append_burned(path, ["i000"], reason="pilot")
    assert path.read_text(encoding="utf-8").count("i000") == 2
