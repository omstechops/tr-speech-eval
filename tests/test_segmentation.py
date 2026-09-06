import itertools
import random

import pytest

from tr_speech_eval.segmentation import (
    SegmentationConfig,
    SegmentPlan,
    SpeechRegion,
    choose_windows,
    speech_ratio,
    strip_edge_words,
)

# A 7-minute recording that is speech throughout: the minimum the plan allows.
DURATION = 420.0
ALL_SPEECH = [SpeechRegion(0.0, DURATION)]
CONFIG = SegmentationConfig(min_speech_ratio=0.8)


def test_speech_ratio_counts_only_the_overlap() -> None:
    regions = [SpeechRegion(0.0, 10.0), SpeechRegion(20.0, 40.0)]
    # Window 5-25 overlaps 5s of the first region and 5s of the second.
    assert speech_ratio(5.0, 25.0, regions) == pytest.approx(0.5)


def test_speech_ratio_is_zero_in_silence() -> None:
    assert speech_ratio(50.0, 80.0, [SpeechRegion(0.0, 10.0)]) == 0.0


def test_speech_ratio_rejects_an_empty_window() -> None:
    with pytest.raises(ValueError, match="must be positive"):
        speech_ratio(10.0, 10.0, ALL_SPEECH)


def test_windows_respect_the_thirds_and_the_gap() -> None:
    windows = choose_windows(DURATION, ALL_SPEECH, CONFIG, random.Random(1))
    assert len(windows) == 3
    part = DURATION / 3
    for index, (start, end, _) in enumerate(windows):
        assert end - start == pytest.approx(CONFIG.window_seconds)
        assert index * part <= start
        assert end <= (index + 1) * part
    for (_, earlier_end, _), (later_start, _, _) in itertools.pairwise(windows):
        assert later_start - earlier_end >= CONFIG.min_gap_seconds


def test_windows_meet_the_speech_ratio_threshold() -> None:
    # Speech only in the first half; the second half cannot supply a window.
    regions = [SpeechRegion(0.0, 200.0)]
    config = SegmentationConfig(min_speech_ratio=0.9, max_attempts=50)
    with pytest.raises(ValueError, match="no arrangement"):
        choose_windows(DURATION, regions, config, random.Random(2))


def test_sparse_speech_still_works_when_the_threshold_allows_it() -> None:
    # Speech in three well-separated blocks, one per third.
    regions = [
        SpeechRegion(10.0, 120.0),
        SpeechRegion(150.0, 260.0),
        SpeechRegion(290.0, 410.0),
    ]
    windows = choose_windows(
        DURATION,
        regions,
        SegmentationConfig(min_speech_ratio=0.95),
        random.Random(3),
    )
    for start, end, ratio in windows:
        assert ratio >= 0.95
        assert speech_ratio(start, end, regions) == pytest.approx(ratio)


def test_same_seed_reproduces_the_windows() -> None:
    first = choose_windows(DURATION, ALL_SPEECH, CONFIG, random.Random(7))
    second = choose_windows(DURATION, ALL_SPEECH, CONFIG, random.Random(7))
    assert first == second


def test_different_seeds_give_different_windows() -> None:
    first = choose_windows(DURATION, ALL_SPEECH, CONFIG, random.Random(7))
    second = choose_windows(DURATION, ALL_SPEECH, CONFIG, random.Random(8))
    assert first != second


def test_a_short_recording_is_refused_with_the_arithmetic() -> None:
    # 3 x 30s windows with 2 x 90s gaps need 270s; five minutes of thirds cannot
    # hold them once the gap constraint applies.
    with pytest.raises(ValueError, match="need at least 270"):
        choose_windows(240.0, ALL_SPEECH, CONFIG, random.Random(0))


def test_strip_edge_words_drops_both_ends() -> None:
    assert strip_edge_words("bir iki üç dört beş") == "iki üç dört"


def test_strip_edge_words_collapses_whitespace() -> None:
    assert strip_edge_words("  bir   iki\núç  ") == "iki"


def test_strip_edge_words_refuses_a_two_token_transcript() -> None:
    with pytest.raises(ValueError, match="at least 3 tokens"):
        strip_edge_words("bir iki")


def test_plan_becomes_an_item_carrying_its_offsets() -> None:
    plan = SegmentPlan(
        item_id="i000",
        speaker_id="s01",
        source="own",
        consent_tier=2,
        start_seconds=12.5,
        end_seconds=42.5,
        speech_ratio=0.93,
    )
    item = plan.to_item("ham metin burada")
    assert item.item_id == "i000"
    assert item.source_ref == "s01@12.50-42.50"
    assert item.asr_raw == "ham metin burada"
