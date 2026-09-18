from pathlib import Path

import pandas as pd

RAW_FILE = Path("data/raw/bgg-15m-reviews.csv")
OUTPUT_FILE = Path("data/processed/reviews_with_comments.csv")

CHUNK_SIZE = 100_000


def normalize_text(text: str) -> str:
    text = text.lower()
    text = " ".join(text.split())
    return text


def prepare_reviews() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    first_chunk = True

    raw_rows = 0
    valid_rows = 0
    reviews_per_game = {}

    for chunk in pd.read_csv(RAW_FILE, chunksize=CHUNK_SIZE):
        raw_rows += len(chunk)

        reviews = chunk[
            chunk["comment"].notna()
            & chunk["comment"].str.strip().ne("")
        ].copy()

        reviews["comment"] = reviews["comment"].apply(normalize_text)

        valid_rows += len(reviews)

        game_counts = reviews["name"].value_counts()

        for game, count in game_counts.items():
            reviews_per_game[game] = reviews_per_game.get(game, 0) + count

        reviews.to_csv(
            OUTPUT_FILE,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False,
        )

        first_chunk = False

    removed_rows = raw_rows - valid_rows

    print("Validation summary")
    print(f"Raw rows: {raw_rows}")
    print(f"Valid review rows: {valid_rows}")
    print(f"Removed rows: {removed_rows}")
    print(f"Games with reviews: {len(reviews_per_game)}")


if __name__ == "__main__":
    prepare_reviews()