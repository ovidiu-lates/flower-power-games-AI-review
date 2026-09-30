import pytest

from smart_review_ai.analysis.difficulty import classify_difficulty
from smart_review_ai.analysis.sentiment import analyze_sentiment


@pytest.mark.parametrize(
    ("review", "expected"),
    [
        ("This game is fun and enjoyable.", "positive"),
        ("The game includes cards and dice.", "neutral"),
        ("This game is boring and awful.", "negative"),
        ("The game is okay, I guess.", "neutral"),
        ("This game is not fun.", "negative"),
    ],
)
def test_sentiment_classification(review: str, expected: str) -> None:
    assert analyze_sentiment(review) == expected


@pytest.mark.parametrize(
    ("review", "expected"),
    [
        ("This game is not difficult.", "easy"),
        ("This game is not hard.", "easy"),
        ("This game is challenging.", "hard"),
        ("This game is difficult.", "hard"),
        ("This is a very hard strategy game.", "very_hard"),
        ("The rules are extremely difficult.", "very_hard"),
        ("The experience depends on the group and the players.", "medium"),
        ("The game has cards and dice.", "medium"),
    ],
)
def test_difficulty_classification(review: str, expected: str) -> None:
    assert classify_difficulty(review) == expected