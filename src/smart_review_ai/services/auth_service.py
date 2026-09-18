from sqlalchemy.orm import Session

from smart_review_ai.core.exceptions import (
    EntityAlreadyExistsError,
    InvalidCredentialsError,
)
from smart_review_ai.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from smart_review_ai.models.user import User
from smart_review_ai.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, session: Session) -> None:
        self.users = UserRepository(session)
        self.session = session

    def register(self, *, username: str, email: str, password: str) -> User:
        if self.users.exists_by_username(username) or self.users.exists_by_email(email):
            raise EntityAlreadyExistsError("Username or email is already registered")
        user = self.users.create(
            username=username,
            email=email,
            password_hash=hash_password(password),
        )
        self.session.commit()
        return user

    def authenticate(self, *, username: str, password: str) -> str:
        user = self.users.get_by_username(username)
        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid username or password")
        return create_access_token(user.id)
