from collections.abc import Mapping


# Canonical categories keep aggregation stable while accepting natural phrasing.
COMPLAINT_SYNONYMS: dict[str, tuple[str, ...]] = {
    "long setup": (
        "setup takes forever",
        "setup takes too long",
        "long setup",
        "lengthy setup",
        "tedious setup",
        "too much setup",
        "time to set up",
    ),
    "unclear rules": (
        "rulebook unclear",
        "unclear rulebook",
        "confusing rules",
        "rules are confusing",
        "hard to understand rules",
        "poorly explained rules",
        "bad rulebook",
        "ambiguous rules",
    ),
    "long play time": (
        "takes too long",
        "game takes too long",
        "too long to play",
        "long play time",
        "lengthy game",
        "drags on",
        "overstays its welcome",
    ),
    "excessive downtime": (
        "too much downtime",
        "long downtime",
        "waiting between turns",
        "wait between turns",
        "takes too long between turns",
        "too much waiting",
    ),
    "too much randomness": (
        "too random",
        "excessive randomness",
        "luck based",
        "too luck based",
        "depends too much on luck",
        "luck determines",
    ),
    "poor component quality": (
        "cheap components",
        "poor quality components",
        "flimsy components",
        "low quality pieces",
        "components feel cheap",
    ),
}

THEME_SYNONYMS: dict[str, tuple[str, ...]] = {
    "strategy": (
        "strategic decisions",
        "strategic depth",
        "deep strategy",
        "lots of strategy",
        "tactical choices",
        "meaningful choices",
    ),
    "artwork": (
        "beautiful artwork",
        "great art",
        "art is beautiful",
        "visual presentation",
        "looks gorgeous",
        "stunning art",
    ),
    "replayability": (
        "high replay value",
        "great replay value",
        "replayable",
        "replayability",
        "different every time",
        "want to play again",
    ),
    "easy to learn": (
        "easy to learn",
        "easy to teach",
        "quick to learn",
        "simple rules",
        "easy to understand",
        "beginner friendly",
    ),
    "player interaction": (
        "player interaction",
        "interactive",
        "interact with other players",
        "take that",
        "competitive tension",
    ),
    "theme": (
        "immersive theme",
        "thematic",
        "theme comes through",
        "strong theme",
        "theme is engaging",
    ),
}


def find_categories(text: str, mappings: Mapping[str, tuple[str, ...]]) -> list[str]:
    """Return canonical categories whose phrase variants occur in *text*."""
    normalized_text = " ".join(text.casefold().split())
    return [
        category
        for category, variations in mappings.items()
        if any(variation in normalized_text for variation in variations)
    ]