from collections.abc import Generator

from sqlalchemy.orm import Session

from smart_review_ai.db.database import SessionLocal


def get_db() -> Generator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
