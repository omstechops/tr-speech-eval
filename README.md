# tr-speech-eval

Evaluation material and data collection for Turkish speech systems.

This package collects data. Every statistical result computed from that data is
produced by [`evalstat`](https://github.com/omstechops/evalstat), not here.

## Current scope

Blinded data collection for analysis plan 001
(`docs/analysis-plan-001-asr-postedit.md`):

- `blinding` — builds the blinded rating sheets and their key files. Model
  identity is stripped, position and order are randomized from a recorded seed,
  and the key stays closed until every human rating is in.
- `burned` — append-only ledger of items consumed by rubric derivation and the
  pilot, which cannot enter the study.
- `segmentation` — turns a recording into the 30-second windows that become
  items: one per third, at least 90 seconds apart, drawn from a recorded seed and
  restricted to detected speech. Voice activity detection happens elsewhere; this
  module consumes speech regions, so the selection rule stays testable and free of
  a platform-specific dependency.
- `manifest` — the record of what a run actually used: model ids as read from
  the provider's API, ASR checkpoint, seed, and hashes of the prompt, the item
  list and the burned ledger. A value that could not be read is written as
  `[UNVERIFIED]` rather than omitted, because an absent field cannot later be
  told apart from an empty one.

The generation step — running both systems over the item list — is not written
yet.

## Dependencies

The core package is standard library only, so the reusable parts stay installable
anywhere. Everything heavier is an extra:

```bash
pip install -e ".[api]"   # anthropic — running the post-editing systems
pip install -e ".[asr]"   # mlx-whisper — producing raw transcripts, Apple Silicon
```

`manifest` records the version of every tool a run used, including tools in
those extras. It reads distribution metadata and imports none of them.

## Development

The virtualenv is not in the repository; recreate it after a clone.

```bash
python3.14 -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/pytest -q && .venv/bin/ruff check . && .venv/bin/mypy
```
