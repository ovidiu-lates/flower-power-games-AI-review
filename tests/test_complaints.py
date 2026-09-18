import pytest

from smart_review_ai.analysis.complaints import extract_complaints

@pytest.mark.parametrize(
    ("review", "expected"),
    [
        ("The rules are confusing.", ["confusing rules"]),
        ("Setup takes forever.", ["long setup"]),
        ("The learning curve is very steep.", ["learning curve"]),
        ("There is too much waiting between turns.", ["downtime"]),
        (
            "Some strategies are much stronger than others.",
            ["balancing issues"],
        ),
        (
            "The rules are confusing and setup takes forever.",
            ["confusing rules", "long setup"],
        ),
        ("The rulebook is confusing.", ["confusing rules"]),
        ("Some of the rules are poorly explained.", ["confusing rules"]),
        ("It takes too long to prepare the game.", ["long setup"]),
        (
            "It takes several games before you understand it.",
            ["learning curve"],
        ),
        (
            "Turns take too long with more players.",
            ["downtime"],
        ),
        ("The game feels unbalanced.", ["balancing issues"]),
        ("The components are beautiful.", []),
        ("The rules are not confusing.", []),
        ("", []),
        ("   ", []),
    ],
)
def test_extract_complaints(review: str, expected: list[str]) -> None:
    assert extract_complaints(review) == expected