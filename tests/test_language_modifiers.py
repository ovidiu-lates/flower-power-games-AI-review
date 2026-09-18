from smart_review_ai.analysis.difficulty import classify_difficulty
from smart_review_ai.analysis.sentiment import analyze_sentiment


def test_not_difficult_is_classified_as_easy():
    result = classify_difficulty("This game is not difficult.")

    assert result == "easy"


def test_not_fun_is_classified_as_negative():
    result = analyze_sentiment("This game is not fun.")

    assert result == "negative"


def test_very_confusing_is_classified_as_hard():
    result = classify_difficulty("The rules are very confusing.")

    assert result == "very_hard"