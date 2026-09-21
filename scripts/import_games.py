from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sqlalchemy import select

from smart_review_ai.db.database import SessionLocal
from smart_review_ai.models.game import Game

DEFAULT_INPUT_FILE = (
    Path(__file__).resolve().parents[1] / "data" / "raw" / "games_detailed_info2025.csv"
)
CSV_COLUMNS = [
    "id",
    "image",
    "description",
    "minplayers",
    "maxplayers",
    "minplaytime",
    "maxplaytime",
    "name",
]


def parse_integer(value: str, field_name: str) -> int:
    try:
        return int(value.strip())
    except ValueError as error:
        raise ValueError(f"{field_name} must be an integer") from error


def duplicate_key(name: str) -> str:
    return name.strip().casefold()


def parse_game_row(row: dict[str, str]) -> dict[str, object]:
    name = row["name"].strip()
    description = row["description"].strip()
    image_url = row["image"].strip()

    if not name:
        raise ValueError("name is required")
    if len(name) > 255:
        raise ValueError("name exceeds 255 characters")
    if not description:
        raise ValueError("description is required")
    if not image_url:
        raise ValueError("image is required")
    if len(image_url) > 2048:
        raise ValueError("image exceeds 2048 characters")

    min_players = parse_integer(row["minplayers"], "minplayers")
    max_players = parse_integer(row["maxplayers"], "maxplayers")
    min_play_time = parse_integer(row["minplaytime"], "minplaytime")
    max_play_time = parse_integer(row["maxplaytime"], "maxplaytime")

    if min_players < 1 or max_players < 1:
        raise ValueError("player counts must be at least 1")
    if min_players > max_players:
        raise ValueError("minplayers cannot exceed maxplayers")
    if min_play_time < 0 or max_play_time < 0:
        raise ValueError("play times cannot be negative")
    if min_play_time > max_play_time:
        raise ValueError("minplaytime cannot exceed maxplaytime")

    return {
        "name": name,
        "description": description,
        "image_url": image_url,
        "min_players": min_players,
        "max_players": max_players,
        "min_play_time": min_play_time,
        "max_play_time": max_play_time,
    }


def import_games(input_file: Path) -> None:
    games = pd.read_csv(
        input_file,
        usecols=CSV_COLUMNS,
        dtype=str,
        keep_default_na=False,
    )

    valid_games: dict[str, tuple[int, dict[str, object]]] = {}
    invalid_rows = 0
    duplicate_rows = 0

    for index, row in games.iterrows():
        csv_row_number = index + 2
        try:
            values = parse_game_row(row.to_dict())
        except ValueError as error:
            invalid_rows += 1
            print(f"Skipping CSV row {csv_row_number}: {error}")
            continue

        name = values["name"]
        if not isinstance(name, str):
            raise TypeError("validated game name must be a string")
        name_key = duplicate_key(name)
        if name_key in valid_games:
            duplicate_rows += 1
            print(f"Skipping CSV row {csv_row_number}: duplicate game ({name})")
            continue
        valid_games[name_key] = (csv_row_number, values)

    inserted = 0

    with SessionLocal() as session, session.begin():
        existing_names = {
            duplicate_key(name) for name in session.scalars(select(Game.name))
        }
        new_games = []
        for name_key, (csv_row_number, values) in valid_games.items():
            name = values["name"]
            if not isinstance(name, str):
                raise TypeError("validated game name must be a string")
            if name_key in existing_names:
                duplicate_rows += 1
                print(f"Skipping CSV row {csv_row_number}: game already exists ({name})")
                continue

            new_games.append(Game(**values))

        session.add_all(new_games)
        inserted = len(new_games)

    print("Import summary")
    print(f"Rows read: {len(games)}")
    print(f"Inserted: {inserted}")
    print(f"Skipped duplicates: {duplicate_rows}")
    print(f"Skipped invalid rows: {invalid_rows}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Import board games into the database")
    parser.add_argument(
        "input_file",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT_FILE,
        help="CSV file to import (defaults to data/raw/games_detailed_info2025.csv)",
    )
    arguments = parser.parse_args()

    if not arguments.input_file.is_file():
        parser.error(f"input file does not exist: {arguments.input_file}")

    import_games(arguments.input_file)


if __name__ == "__main__":
    main()