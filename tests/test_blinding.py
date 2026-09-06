import dataclasses
import itertools
import json
import random
from pathlib import Path

import pytest

from tr_speech_eval.blinding import (
    Item,
    PairedOutputs,
    make_absolute_sheet,
    make_preference_sheet,
    write_jsonl,
)

SYSTEMS = ("system_a", "system_b")


def make_paired(count: int) -> list[PairedOutputs]:
    return [
        PairedOutputs(
            item=Item(
                item_id=f"i{index:03d}",
                source_ref=f"rec01@{index}",
                asr_raw=f"ham metin {index}",
            ),
            outputs={
                "system_a": f"a çıktısı {index}",
                "system_b": f"b çıktısı {index}",
            },
        )
        for index in range(count)
    ]


def test_preference_key_recovers_the_side_assignment() -> None:
    paired = make_paired(20)
    by_id = {entry.item.item_id: entry for entry in paired}
    rows, key = make_preference_sheet(paired, SYSTEMS, random.Random(1))

    assert len(rows) == len(key) == 20
    for row, key_row in zip(rows, key, strict=True):
        assert row.pair_id == key_row.pair_id
        assert row.item_id == key_row.item_id
        outputs = by_id[row.item_id].outputs
        assert row.left_text == outputs[key_row.left_system]
        assert row.right_text == outputs[key_row.right_system]
        assert key_row.left_system != key_row.right_system


def test_preference_sheet_covers_every_item_once() -> None:
    paired = make_paired(20)
    rows, _ = make_preference_sheet(paired, SYSTEMS, random.Random(2))
    assert sorted(row.item_id for row in rows) == sorted(
        entry.item.item_id for entry in paired
    )


def test_preference_rows_carry_no_system_name() -> None:
    paired = make_paired(20)
    rows, _ = make_preference_sheet(paired, SYSTEMS, random.Random(3))
    serialized = json.dumps([dataclasses.asdict(row) for row in rows])
    for system in SYSTEMS:
        assert system not in serialized


def test_preference_sides_are_not_constant() -> None:
    # A blinding step that always puts the same system on the left is not
    # blinding; this guards against a collapsed randomization.
    paired = make_paired(50)
    _, key = make_preference_sheet(paired, SYSTEMS, random.Random(4))
    left_systems = {key_row.left_system for key_row in key}
    assert left_systems == set(SYSTEMS)


def test_same_seed_reproduces_the_sheet() -> None:
    paired = make_paired(20)
    first = make_preference_sheet(paired, SYSTEMS, random.Random(7))
    second = make_preference_sheet(paired, SYSTEMS, random.Random(7))
    assert first == second


def test_different_seeds_give_different_sheets() -> None:
    paired = make_paired(50)
    first, _ = make_preference_sheet(paired, SYSTEMS, random.Random(7))
    second, _ = make_preference_sheet(paired, SYSTEMS, random.Random(8))
    assert first != second


def test_missing_output_is_rejected() -> None:
    paired = make_paired(3)
    paired[1] = PairedOutputs(item=paired[1].item, outputs={"system_a": "tek"})
    with pytest.raises(ValueError, match="expected"):
        make_preference_sheet(paired, SYSTEMS, random.Random(0))


def test_duplicate_item_id_is_rejected() -> None:
    paired = make_paired(2)
    paired[1] = PairedOutputs(item=paired[0].item, outputs=paired[1].outputs)
    with pytest.raises(ValueError, match="duplicate item_id"):
        make_preference_sheet(paired, SYSTEMS, random.Random(0))


def test_absolute_sheet_never_places_an_item_next_to_itself() -> None:
    paired = make_paired(40)
    rows, _ = make_absolute_sheet(paired, SYSTEMS, random.Random(5))
    assert len(rows) == 80
    for first, second in itertools.pairwise(rows):
        assert first.item_id != second.item_id


def test_absolute_sheet_covers_every_item_and_system_once() -> None:
    paired = make_paired(40)
    rows, key = make_absolute_sheet(paired, SYSTEMS, random.Random(6))
    by_id = {entry.item.item_id: entry for entry in paired}
    seen = set()
    for row, key_row in zip(rows, key, strict=True):
        assert row.output_id == key_row.output_id
        assert row.text == by_id[row.item_id].outputs[key_row.system]
        seen.add((row.item_id, key_row.system))
    assert len(seen) == 80


def test_absolute_sheet_needs_two_items() -> None:
    with pytest.raises(ValueError, match="at least 2 items"):
        make_absolute_sheet(make_paired(1), SYSTEMS, random.Random(0))


def test_write_jsonl_keeps_turkish_characters_unescaped(tmp_path: Path) -> None:
    paired = make_paired(3)
    rows, _ = make_preference_sheet(paired, SYSTEMS, random.Random(9))
    path = tmp_path / "preference.jsonl"
    write_jsonl(path, rows)

    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3
    assert "çıktısı" in lines[0]
    assert json.loads(lines[0])["pair_id"] == rows[0].pair_id
