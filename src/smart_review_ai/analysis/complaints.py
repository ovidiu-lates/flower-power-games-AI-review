from smart_review_ai.analysis.synonyms import COMPLAINT_SYNONYMS, find_categories


def extract_complaints(text: str) -> list[str]:
    return find_categories(text, COMPLAINT_SYNONYMS)
