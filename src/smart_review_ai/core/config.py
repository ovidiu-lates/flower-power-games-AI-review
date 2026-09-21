import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str | None = os.getenv("DATABASE_URL")
    jwt_secret_key: str = os.getenv(
        "JWT_SECRET_KEY", "development-only-secret-key-32-bytes-long"
    )
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_access_token_expire_minutes: int = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )


settings = Settings()
