import re


POSITIVE_WORDS = {
    "amazing",
    "beautiful",
    "best",
    "enjoy",
    "enjoyable",
    "enjoyed",
    "excellent",
    "favorite",
    "fun",
    "good",
    "great",
    "interesting",
    "love",
    "loved",
    "recommend",
    "wonderful",
}

NEGATIVE_WORDS = {
    "awful",
    "bad",
    "boring",
    "confusing",
    "disappointing",
    "frustrating",
    "hate",
    "hated",
    "poor",
    "repetitive",
    "terrible",
    "worse",
    "worst",
}

NEGATIONS = {"cannot", "hardly", "never", "no", "not", "nothing", "without"}
TOKEN_PATTERN = re.compile(r"[a-z]+(?:'[a-z]+)?")

POSITIVE_PHRASES = ("easy to learn", "beginner-friendly")
NEGATIVE_PHRASES = (
    "too much luck",
    "luck involved",
    "takes forever",
    "takes too long",
    "takes a long time",
    "long setup",
)


def _normalise(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower().strip())


def _has_negation(tokens: list[str], index: int) -> bool:
    start = max(0, index - 3)
    return any(token in NEGATIONS for token in tokens[start:index])


def analyze_sentiment(text: str) -> str:

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    tokens = _normalise(text)
    normalized_text = " ".join(tokens)
    positive_score = sum(normalized_text.count(phrase) for phrase in POSITIVE_PHRASES)
    negative_score = sum(normalized_text.count(phrase) for phrase in NEGATIVE_PHRASES)

    for index, token in enumerate(tokens):
        if token in POSITIVE_WORDS:
            if _has_negation(tokens, index):
                negative_score += 1
            else:
                positive_score += 1
        elif token in NEGATIVE_WORDS:
            if _has_negation(tokens, index):
                positive_score += 1
            else:
                negative_score += 1

    if positive_score > negative_score:
        return "positive"
    if negative_score > positive_score:
        return "negative"
    return "neutral"
