from smart_review_ai.analysis.language_modifiers import (
    intensity_level,
    is_negated,
)


def classify_difficulty(text: str) -> str:
    normalized_text = text.lower()

    if is_negated(normalized_text, "difficult"):
        return "easy"

    if "confusing" in normalized_text:
        if intensity_level(normalized_text, "confusing") > 1:
            return "hard"

        return "hard"

    if any(word in normalized_text for word in ["difficult", "hard", "complex"]):
        return "hard"

    return "medium"