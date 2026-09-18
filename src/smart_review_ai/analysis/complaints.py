import re

_COMPLAINT_PATTERNS = (
    (
        "confusing rules",
        (
            r"\bconfusing\s+rules\b",
            r"\brules?\s+(?:are|were|seem|feel)\s+confusing\b",
            r"\brules?\s+(?:are|were|seem|feel)\s+(?:unclear|ambiguous)\b",
            r"\brulebook\s+(?:is|was|seems?|feels?)\s+confusing\b",
            r"\brules?\s+(?:are|were)\s+poorly\s+explained\b",
        ),
    ),
    (
        "long setup",
        (
            r"\blong\s+setup\b",
            r"\bsetup\s+(?:takes?|is|was)\s+(?:forever|too\s+long|lengthy)\b",
            r"\blengthy\s+setup\b",
            r"\btakes?\s+too\s+long\s+to\s+(?:prepare|set\s+up)\b",
        ),
    ),
    (
        "learning curve",
        (
            r"\bsteep\s+learning\s+curve\b",
            r"\blearning\s+curve\s+(?:is|was|feels?|seems?)\s+(?:very\s+)?steep\b",
            r"\bdifficult\s+to\s+learn\b",
            r"\btakes?\s+several\s+games?\s+before\s+(?:you\s+)?understand\b",
        ),
    ),
    (
        "downtime",
        (
            r"\b(?:too\s+much|a\s+lot\s+of|long)\s+waiting\s+(?:between\s+turns|for\s+other\s+players)\b",
            r"\blong\s+(?:wait|waits|waiting)\s+between\s+turns\b",
            r"\bdowntime\b",
            r"\bturns?\s+take\s+too\s+long\b",
        ),
    ),
    (
        "balancing issues",
        (
            r"\bbalanc(?:e|ing)\s+issues?\b",
            r"\bunbalanced\b",
            r"\bsome\s+strateg(?:y|ies)\s+(?:are|is)\s+(?:much\s+)?stronger\s+than\s+others\b",
            r"\bone\s+strateg(?:y|ies)\s+(?:is|are)\s+(?:much\s+)?stronger\b",
        ),
    ),
)

_NEGATION = re.compile(
    r"\b(?:not|no|never|neither|isn't|aren't|wasn't|weren't|without)\b",
    re.IGNORECASE,
)


def _is_negated(text: str, match: re.Match[str]) -> bool:
    clause_start = max(text.rfind(char, 0, match.start()) for char in ".!?;:\n") + 1
    return _NEGATION.search(text, clause_start, match.start()) is not None


def extract_complaints(text: str) -> list[str]:
    if not text or not text.strip():
        return []

    complaints = []
    for complaint, patterns in _COMPLAINT_PATTERNS:
        if any(
            not _is_negated(text, match)
            for pattern in patterns
            for match in re.finditer(pattern, text, re.IGNORECASE)
        ):
            complaints.append(complaint)
    return complaints
