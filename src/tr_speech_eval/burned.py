"""Ledger of items that may never enter the study.

Two sets are consumed before the study starts and cannot be reused: the items
that shaped the rubric anchors, and the pilot items. Both were rated under a
rubric they helped produce or tune, so ratings on them agree with that rubric
more than a fresh item would.

The ledger is append-only and lives in version control next to the plan, so the
exclusion is auditable rather than remembered.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Sequence
from pathlib import Path

from tr_speech_eval.blinding import Item

__all__ = ["append_burned", "load_burned", "reject_burned"]


def load_burned(path: Path) -> set[str]:
    """Return the item ids recorded in the ledger, or an empty set if absent."""
    if not path.exists():
        return set()
    burned: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                burned.add(str(json.loads(line)["item_id"]))
    return burned


def append_burned(path: Path, item_ids: Iterable[str], reason: str) -> None:
    """Append item ids to the ledger with the reason they were consumed.

    Parameters
    ----------
    path
        Ledger file; created if it does not exist.
    item_ids
        Ids to record. Ids already present are written again rather than
        deduplicated, so the file stays a literal append-only log.
    reason
        Short label, e.g. ``"rubric-derivation"`` or ``"pilot"``.
    """
    with path.open("a", encoding="utf-8") as handle:
        for item_id in item_ids:
            record = {"item_id": item_id, "reason": reason}
            handle.write(json.dumps(record, ensure_ascii=False))
            handle.write("\n")


def reject_burned(items: Sequence[Item], burned: set[str]) -> list[Item]:
    """Return the items that are not in the ledger.

    This filters; it does not select. Which items are then drawn for the study,
    and by what rule, is a decision recorded in the analysis plan.
    """
    return [item for item in items if item.item_id not in burned]
