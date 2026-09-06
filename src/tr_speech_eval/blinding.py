"""Blinded presentation of paired system outputs.

Human rating happens on material produced here. System identity is removed from
every output, left/right position and presentation order are randomized, and the
map back to (item, system, position) goes to a separate key file that is not
opened until every rating is recorded.

Randomization is driven by a caller-supplied ``random.Random``, so a run is
reproducible from its seed and the seed belongs in the run manifest.
"""

from __future__ import annotations

import dataclasses
import itertools
import json
import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

__all__ = [
    "AbsoluteKeyRow",
    "AbsoluteRow",
    "Item",
    "PairedOutputs",
    "PreferenceKeyRow",
    "PreferenceRow",
    "make_absolute_sheet",
    "make_preference_sheet",
    "write_jsonl",
]


@dataclass(frozen=True, slots=True)
class Item:
    """One unit of study material, before any system has seen it.

    Attributes
    ----------
    item_id
        Stable identifier, carried through every downstream file.
    source_ref
        Where the audio came from: recording identifier plus time span. The
        format is corpus-specific and this module does not interpret it.
    asr_raw
        Raw ASR transcript, the input both systems post-edit.
    """

    item_id: str
    source_ref: str
    asr_raw: str


@dataclass(frozen=True, slots=True)
class PairedOutputs:
    """The post-edited outputs of every system for one item."""

    item: Item
    outputs: Mapping[str, str]


@dataclass(frozen=True, slots=True)
class PreferenceRow:
    """One side-by-side comparison as the rater sees it."""

    pair_id: str
    item_id: str
    asr_raw: str
    left_text: str
    right_text: str


@dataclass(frozen=True, slots=True)
class PreferenceKeyRow:
    """The system identity behind one :class:`PreferenceRow`."""

    pair_id: str
    item_id: str
    left_system: str
    right_system: str


@dataclass(frozen=True, slots=True)
class AbsoluteRow:
    """One output as the rater sees it on the absolute tier."""

    output_id: str
    item_id: str
    asr_raw: str
    text: str


@dataclass(frozen=True, slots=True)
class AbsoluteKeyRow:
    """The system identity behind one :class:`AbsoluteRow`."""

    output_id: str
    item_id: str
    system: str


def _check_coverage(paired: Sequence[PairedOutputs], systems: tuple[str, str]) -> None:
    """Raise if any item is missing an output, or carries an unexpected one."""
    if len(set(systems)) != len(systems):
        raise ValueError(f"systems must be distinct, got {systems!r}")
    expected = set(systems)
    seen_ids: set[str] = set()
    for entry in paired:
        if entry.item.item_id in seen_ids:
            raise ValueError(f"duplicate item_id {entry.item.item_id!r}")
        seen_ids.add(entry.item.item_id)
        if set(entry.outputs) != expected:
            raise ValueError(
                f"item {entry.item.item_id!r} has outputs for "
                f"{sorted(entry.outputs)}, expected {sorted(expected)}"
            )


def _sequential_ids(prefix: str, count: int) -> list[str]:
    """Return ``count`` zero-padded ids; they encode position only, never system."""
    width = max(3, len(str(count)))
    return [f"{prefix}{i:0{width}d}" for i in range(1, count + 1)]


def make_preference_sheet(
    paired: Sequence[PairedOutputs],
    systems: tuple[str, str],
    rng: random.Random,
) -> tuple[list[PreferenceRow], list[PreferenceKeyRow]]:
    """Build the blinded side-by-side sheet and its key.

    Item order is shuffled, and for each item the two systems are assigned to
    left and right independently of every other item.

    Parameters
    ----------
    paired
        One entry per item, each holding both systems' outputs.
    systems
        The two system names, exactly as they appear in ``PairedOutputs.outputs``.
    rng
        Seeded source of randomness.

    Returns
    -------
    tuple
        The presentation rows and the key rows, in the same order. The caller is
        responsible for writing them to separate files.
    """
    _check_coverage(paired, systems)
    order = list(paired)
    rng.shuffle(order)
    pair_ids = _sequential_ids("p", len(order))

    rows: list[PreferenceRow] = []
    key: list[PreferenceKeyRow] = []
    for pair_id, entry in zip(pair_ids, order, strict=True):
        left, right = systems
        if rng.random() < 0.5:
            left, right = right, left
        rows.append(
            PreferenceRow(
                pair_id=pair_id,
                item_id=entry.item.item_id,
                asr_raw=entry.item.asr_raw,
                left_text=entry.outputs[left],
                right_text=entry.outputs[right],
            )
        )
        key.append(
            PreferenceKeyRow(
                pair_id=pair_id,
                item_id=entry.item.item_id,
                left_system=left,
                right_system=right,
            )
        )
    return rows, key


def make_absolute_sheet(
    paired: Sequence[PairedOutputs],
    systems: tuple[str, str],
    rng: random.Random,
    max_attempts: int = 1000,
) -> tuple[list[AbsoluteRow], list[AbsoluteKeyRow]]:
    """Build the blinded one-at-a-time sheet and its key.

    Outputs are presented individually in shuffled order, with the constraint
    that the two outputs of the same item are never adjacent: seeing them back to
    back turns the absolute tier into an implicit comparison.

    The constraint is met by reshuffling until it holds, which needs at least two
    items to be satisfiable at all.

    Parameters
    ----------
    paired
        One entry per item, each holding both systems' outputs.
    systems
        The two system names.
    rng
        Seeded source of randomness.
    max_attempts
        Reshuffles allowed before giving up.

    Returns
    -------
    tuple
        The presentation rows and the key rows, in the same order.

    Raises
    ------
    ValueError
        If fewer than two items are given, or no valid order was found within
        ``max_attempts``.
    """
    _check_coverage(paired, systems)
    if len(paired) < 2:
        raise ValueError(
            f"the non-adjacency constraint needs at least 2 items, got {len(paired)}"
        )

    units = [(entry, system) for entry in paired for system in systems]
    for _ in range(max_attempts):
        rng.shuffle(units)
        if all(
            a[0].item.item_id != b[0].item.item_id for a, b in itertools.pairwise(units)
        ):
            break
    else:
        raise ValueError(
            f"no order without adjacent same-item outputs after {max_attempts} attempts"
        )

    output_ids = _sequential_ids("o", len(units))
    rows: list[AbsoluteRow] = []
    key: list[AbsoluteKeyRow] = []
    for output_id, (entry, system) in zip(output_ids, units, strict=True):
        rows.append(
            AbsoluteRow(
                output_id=output_id,
                item_id=entry.item.item_id,
                asr_raw=entry.item.asr_raw,
                text=entry.outputs[system],
            )
        )
        key.append(
            AbsoluteKeyRow(
                output_id=output_id,
                item_id=entry.item.item_id,
                system=system,
            )
        )
    return rows, key


def write_jsonl(path: Path, rows: Sequence[Any]) -> None:
    """Write dataclass rows to ``path`` as one JSON object per line."""
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(dataclasses.asdict(row), ensure_ascii=False))
            handle.write("\n")
