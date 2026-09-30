from smart_review_ai.analysis.language_modifiers import (
    intensity_level,
    is_negated,
)

VERY_HARD_PHRASES = {
    "very hard",
    "very difficult",
    "extremely difficult",
    "steep learning curve",
}


HARD_WORDS = {
    "hard",
    "difficult",
    "challenging",
    "complex",
}


def classify_difficulty(text: str) -> str:
    normalized_text = text.lower()

    if is_negated(normalized_text, "difficult"):
        return "easy"

    if is_negated(normalized_text, "hard"):
        return "easy"

    if any(phrase in normalized_text for phrase in VERY_HARD_PHRASES):
        return "very_hard"

    if (
        "confusing" in normalized_text
        and intensity_level(normalized_text, "confusing") > 1
    ):
        return "very_hard"

    if any(word in normalized_text for word in HARD_WORDS):
        return "hard"

    return "medium"