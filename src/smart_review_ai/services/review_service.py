from smart_review_ai.analysis.complaints import extract_complaints


def analyze_review(comment: str) -> dict[str, list[str]]:
    return {"complaints": extract_complaints(comment)}
