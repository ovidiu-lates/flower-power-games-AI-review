import re

NEGATIONS = {"not", "never"}
INTENSIFIERS = {"very", "extremely", "really"}

def _tokens(text: str) -> list[str]:
    return re.findall(r"\b[\w']+\b", text.lower())


def is_negated(text: str, keyword: str, window: int = 2) -> bool:
    tokens = _tokens(text)

    for index, token in enumerate(tokens):
        if token == keyword.lower():
            previous_words = tokens[max(0, index - window):index]
            return any(word in NEGATIONS for word in previous_words)

    return False


def intensity_level(text: str, keyword: str) -> int:
    tokens = _tokens(text)

    for index, token in enumerate(tokens):
        if token == keyword.lower() and index > 0:
            previous_word = tokens[index - 1]

            if previous_word in INTENSIFIERS:
                return 2

    return 1