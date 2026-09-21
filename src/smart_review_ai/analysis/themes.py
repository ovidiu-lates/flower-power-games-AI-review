from smart_review_ai.analysis.synonyms import THEME_SYNONYMS, find_categories


def extract_themes(text: str) -> list[str]:
    return find_categories(text, THEME_SYNONYMS)
