"""Cutting a recording into the windows that become items.

The rules here are the ones section 3 of analysis plan 001 fixed, and each is a
decision rather than a convenience:

Windows are 30 seconds because shorter ones stop exercising suffix agreement
across clauses, sentence-boundary restoration and reference resolution — the
Turkish-specific error categories the study is trying to see.

One window is drawn per third of the recording, at least 90 seconds apart.
Adjacent windows share topic, acoustic state and speaker energy, which raises
the within-recording correlation, and that correlation is what the design effect
turns on. Spreading them is a power decision, not a tidiness one.

Offsets are drawn from a caller-supplied ``random.Random`` so segmentation is
reproducible from the seed recorded in the run manifest.

Voice activity detection is *not* done here. This module consumes speech regions
that something else produced, so the reusable part of the package stays free of a
platform-specific dependency and the detector can be swapped without touching the
selection rule.
"""

from __future__ import annotations

import random
from collections.abc import Sequence
from dataclasses import dataclass

from tr_speech_eval.blinding import Item

__all__ = [
    "SegmentPlan",
    "SegmentationConfig",
    "SpeechRegion",
    "choose_windows",
    "speech_ratio",
    "strip_edge_words",
]


@dataclass(frozen=True, slots=True)
class SpeechRegion:
    """A stretch of detected speech, in seconds from the start of the recording."""

    start: float
    end: float


@dataclass(frozen=True, slots=True)
class SegmentationConfig:
    """The segmentation rules, all of which are pre-registered.

    Attributes
    ----------
    min_speech_ratio
        Least proportion of a candidate window that must be speech. No default:
        the threshold is a plan decision, and a value chosen after seeing which
        windows it rejects is a selection rule rather than a filter.
    window_seconds
        Item length.
    min_gap_seconds
        Least silence-to-start distance between two chosen windows.
    segments_per_recording
        Windows per recording; also the number of equal parts the recording is
        divided into, one window drawn from each.
    max_attempts
        Draws allowed before the recording is reported as unusable.
    """

    min_speech_ratio: float
    window_seconds: float = 30.0
    min_gap_seconds: float = 90.0
    segments_per_recording: int = 3
    max_attempts: int = 200


@dataclass(frozen=True, slots=True)
class SegmentPlan:
    """One chosen window, before any audio has been cut or recognised."""

    item_id: str
    speaker_id: str
    source: str
    consent_tier: int
    start_seconds: float
    end_seconds: float
    speech_ratio: float

    def to_item(self, asr_raw: str) -> Item:
        """Pair this window with its ASR transcript to make a study item."""
        return Item(
            item_id=self.item_id,
            source_ref=(
                f"{self.speaker_id}@{self.start_seconds:.2f}-{self.end_seconds:.2f}"
            ),
            asr_raw=asr_raw,
        )


def speech_ratio(start: float, end: float, regions: Sequence[SpeechRegion]) -> float:
    """Return the proportion of ``[start, end)`` covered by speech.

    Regions are assumed non-overlapping; overlapping ones would be counted twice
    and the ratio could exceed 1.
    """
    window = end - start
    if window <= 0:
        raise ValueError(f"window must be positive, got {window}")
    covered = sum(
        max(0.0, min(end, region.end) - max(start, region.start)) for region in regions
    )
    return covered / window


def choose_windows(
    duration_seconds: float,
    regions: Sequence[SpeechRegion],
    config: SegmentationConfig,
    rng: random.Random,
) -> list[tuple[float, float, float]]:
    """Choose one window per equal part of the recording.

    Windows are drawn left to right; each is constrained to its own part of the
    recording *and* to starting at least ``min_gap_seconds`` after the previous
    one ends.

    Parameters
    ----------
    duration_seconds
        Length of the recording.
    regions
        Detected speech regions.
    config
        The pre-registered rules.
    rng
        Seeded source of randomness.

    Returns
    -------
    list of tuple
        ``(start, end, speech_ratio)`` per window, in time order.

    Raises
    ------
    ValueError
        If the recording is too short for the rules, or if no arrangement
        satisfying them was found within ``config.max_attempts``.
    """
    count = config.segments_per_recording
    required = count * config.window_seconds + (count - 1) * config.min_gap_seconds
    if duration_seconds < required:
        raise ValueError(
            f"recording is {duration_seconds:.1f}s; {count} windows of "
            f"{config.window_seconds:.0f}s with {config.min_gap_seconds:.0f}s "
            f"gaps need at least {required:.1f}s"
        )

    part = duration_seconds / count
    for _ in range(config.max_attempts):
        chosen: list[tuple[float, float, float]] = []
        for index in range(count):
            low = index * part
            high = (index + 1) * part - config.window_seconds
            if chosen:
                low = max(low, chosen[-1][1] + config.min_gap_seconds)
            if high < low:
                break
            window = _draw_window(low, high, regions, config, rng)
            if window is None:
                break
            chosen.append(window)
        else:
            return chosen
    raise ValueError(
        f"no arrangement of {count} windows met the rules in "
        f"{config.max_attempts} attempts; the recording may be too sparse in "
        "speech or too short for the gap constraint"
    )


def _draw_window(
    low: float,
    high: float,
    regions: Sequence[SpeechRegion],
    config: SegmentationConfig,
    rng: random.Random,
) -> tuple[float, float, float] | None:
    """Draw a start offset in ``[low, high]`` whose window is speech enough."""
    for _ in range(config.max_attempts):
        start = rng.uniform(low, high)
        end = start + config.window_seconds
        ratio = speech_ratio(start, end, regions)
        if ratio >= config.min_speech_ratio:
            return (start, end, ratio)
    return None


def strip_edge_words(text: str) -> str:
    """Drop the first and last whitespace-delimited token of an ASR transcript.

    Applied to every item, whether or not the cut actually truncated a word.
    Uniformity is the point: a rule that fires only on some items would put a
    difference between items inside the comparison, and neither system would be
    responsible for it.

    Raises
    ------
    ValueError
        If fewer than three tokens are present, which leaves nothing after the
        edges are removed. A 30-second window that recognised two words is an
        ASR failure, and the caller decides what to do about it.
    """
    tokens = text.split()
    if len(tokens) < 3:
        raise ValueError(
            f"need at least 3 tokens to strip both edges, got {len(tokens)}"
        )
    return " ".join(tokens[1:-1])
