"""Run manifest: what was actually run, recorded while it is still knowable.

Six months after a run, the manifest is the only account of which model version,
which ASR checkpoint and which item list produced the data. Two rules follow
from that.

A field that could not be read is written as :data:`UNVERIFIED`, never left out
and never filled from recollection. A silently absent field cannot be told apart
later from a field that was genuinely empty.

The module imports nothing outside the standard library. It records the versions
of the tools a run used — including ones this package never imports, such as the
ASR stack — by reading installed distribution metadata as text.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

UNVERIFIED = "[UNVERIFIED]"
"""Written wherever a value could not be read from its source."""

__all__ = [
    "UNVERIFIED",
    "Manifest",
    "build_manifest",
    "package_version",
    "sha256_file",
    "sha256_text",
]


def sha256_text(text: str) -> str:
    """Return the SHA-256 of ``text`` encoded as UTF-8."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    """Return the SHA-256 of the bytes in ``path``.

    Raises
    ------
    FileNotFoundError
        If the file is absent. A missing input is a fact about the run that the
        caller has to decide about; it is not silently hashed as empty.
    """
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package_version(distribution: str) -> str:
    """Return an installed distribution's version, or :data:`UNVERIFIED`.

    Reads distribution metadata rather than importing the package, so the
    version of an optional or platform-specific tool can be recorded by a
    process that never loads it.
    """
    try:
        return metadata.version(distribution)
    except metadata.PackageNotFoundError:
        return UNVERIFIED


def _or_unverified(value: str | None) -> str:
    """Map a missing value onto the explicit sentinel."""
    return UNVERIFIED if value is None or value == "" else value


@dataclass(frozen=True, slots=True)
class Manifest:
    """The record of one generation run."""

    run_id: str
    created_at: str
    seed: int
    systems: Mapping[str, str]
    asr_checkpoint: str
    prompt_sha256: str
    items_sha256: str
    burned_ledger_sha256: str
    tool_versions: Mapping[str, str]
    notes: str = ""

    def unverified_fields(self) -> list[str]:
        """Return the names of fields left at :data:`UNVERIFIED`.

        Nested entries are reported as ``"systems.judge"`` and the like. A
        non-empty result is not an error — it is the list the run's reader is
        owed.
        """
        missing: list[str] = []
        for entry in dataclasses.fields(self):
            value = getattr(self, entry.name)
            if isinstance(value, Mapping):
                missing.extend(
                    f"{entry.name}.{key}"
                    for key, item in value.items()
                    if item == UNVERIFIED
                )
            elif value == UNVERIFIED:
                missing.append(entry.name)
        return missing

    def write(self, path: Path) -> None:
        """Write the manifest to ``path`` as indented JSON."""
        payload = dataclasses.asdict(self)
        path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def build_manifest(
    run_id: str,
    seed: int,
    systems: Mapping[str, str | None],
    prompt: str,
    items_path: Path,
    burned_ledger_path: Path,
    asr_checkpoint: str | None = None,
    tool_distributions: Iterable[str] = ("anthropic", "mlx-whisper"),
    created_at: str | None = None,
    notes: str = "",
) -> Manifest:
    """Assemble a manifest, substituting :data:`UNVERIFIED` for what is missing.

    Parameters
    ----------
    run_id
        Identifier for this run; also names its output directory.
    seed
        The seed the blinding randomization was driven with.
    systems
        Role to model id, as read from the provider's API at run time. ``None``
        for a role whose id could not be read.
    prompt
        The prompt text sent to both systems; hashed, not stored.
    items_path
        The item list both systems were run over; hashed.
    burned_ledger_path
        The burned-item ledger as it stood at run time; hashed. The ledger is
        append-only, so its hash is what shows that the rubric-derivation and
        pilot items were in fact out of the draw when this run happened.
    asr_checkpoint
        The ASR checkpoint that produced the raw transcripts.
    tool_distributions
        Distributions whose versions are recorded. Read as metadata; not
        imported.
    created_at
        ISO-8601 timestamp. Defaults to now, in UTC.
    notes
        Free text.

    Returns
    -------
    Manifest
        Ready to write. Call :meth:`Manifest.unverified_fields` before trusting
        it as a complete record.
    """
    return Manifest(
        run_id=run_id,
        created_at=created_at or datetime.now(timezone.utc).isoformat(),
        seed=seed,
        systems={role: _or_unverified(value) for role, value in systems.items()},
        asr_checkpoint=_or_unverified(asr_checkpoint),
        prompt_sha256=sha256_text(prompt),
        items_sha256=sha256_file(items_path),
        burned_ledger_sha256=sha256_file(burned_ledger_path),
        tool_versions={name: package_version(name) for name in tool_distributions},
        notes=notes,
    )
