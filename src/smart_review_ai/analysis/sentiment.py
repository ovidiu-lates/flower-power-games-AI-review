from smart_review_ai.analysis.language_modifiers import is_negated


def analyze_sentiment(text: str) -> str:
    normalized_text = text.lower()

    if is_negated(normalized_text, "fun"):
        return "negative"

    if any(word in normalized_text for word in ["bad", "boring", "awful"]):
        return "negative"

    if any(word in normalized_text for word in ["fun", "enjoyable", "great"]):
        return "positive"

    return "neutral"