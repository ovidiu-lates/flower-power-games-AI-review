from pathlib import Path

import pandas as pd

RAW_FILE = Path("data/raw/bgg-15m-reviews.csv")
OUTPUT_FILE = Path("data/processed/reviews_with_comments.csv")

CHUNK_SIZE = 100_000


def prepare_reviews() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    first_chunk = True

    for chunk in pd.read_csv(RAW_FILE, chunksize=CHUNK_SIZE):
        reviews = chunk[chunk["comment"].notna() & chunk["comment"].str.strip().ne("")]

        reviews.to_csv(
            OUTPUT_FILE,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False,
        )

        first_chunk = False

    print(f"Processed reviews saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    prepare_reviews()
