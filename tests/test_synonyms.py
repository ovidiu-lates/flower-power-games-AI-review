import pytest

from smart_review_ai.analysis.complaints import extract_complaints
from smart_review_ai.analysis.themes import extract_themes


@pytest.mark.parametrize(
    ("review", "expected"),
    [
        ("The setup takes forever.", ["long setup"]),
        ("The rulebook is unclear and the rules are confusing.", ["unclear rules"]),
        ("The game drags on and there is too much downtime.", ["long play time", "excessive downtime"]),
    ],
)
def test_extract_complaints_normalizes_phrase_variations(
    review: str,
    expected: list[str],
) -> None:
    assert extract_complaints(review) == expected


@pytest.mark.parametrize(
    ("review", "expected"),
    [
        ("It has deep strategy and beautiful artwork.", ["strategy", "artwork"]),
        ("It is easy to teach and has great replay value.", ["replayability", "easy to learn"]),
    ],
)
def test_extract_themes_normalizes_phrase_variations(
    review: str,
    expected: list[str],
) -> None:
    assert extract_themes(review) == expected