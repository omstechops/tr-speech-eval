# tr-speech-eval

Evaluation material and data collection for Turkish speech systems.

This package collects data. Every statistical result computed from that data is
produced by [`evalstat`](../evalstat), not here.

## Current scope

Blinded data collection for analysis plan 001
(`../docs/analysis-plan-001-asr-postedit.md`):

- `blinding` — builds the blinded rating sheets and their key files. Model
  identity is stripped, position and order are randomized from a recorded seed,
  and the key stays closed until every human rating is in.
- `burned` — append-only ledger of items consumed by rubric derivation and the
  pilot, which cannot enter the study.

The generation step — running both systems over the item list — is not here yet:
its model settings are still open in section 2 of the plan.

## Development

```bash
python3.14 -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/pytest -q && .venv/bin/ruff check . && .venv/bin/mypy
```
