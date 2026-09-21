from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from smart_review_ai.api.dependencies.auth import get_current_active_user
from smart_review_ai.api.dependencies.database import get_db
from smart_review_ai.core.exceptions import (
    EntityAlreadyExistsError,
    InvalidCredentialsError,
)
from smart_review_ai.models.user import User
from smart_review_ai.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from smart_review_ai.schemas.user import UserResponse
from smart_review_ai.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    request: RegisterRequest,
    session: Annotated[Session, Depends(get_db)],
) -> User:
    try:
        return AuthService(session).register(
            username=request.username,
            email=request.email,
            password=request.password,
        )
    except EntityAlreadyExistsError as error:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    session: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    try:
        token = AuthService(session).authenticate(
            username=request.username,
            password=request.password,
        )
    except InvalidCredentialsError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        ) from error
    return TokenResponse(access_token=token)


@router.post("/token", response_model=TokenResponse)
def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    try:
        jwt_token = AuthService(session).authenticate(
            username=form_data.username,
            password=form_data.password,
        )
    except InvalidCredentialsError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        ) from error
    return TokenResponse(access_token=jwt_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
def me(
    user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return user
