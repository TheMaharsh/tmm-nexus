import uuid
from typing import Annotated

from fastapi import Depends, Header
from jose import JWTError
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.enums import Permission
from app.models.user import User
from app.services.auth_service import AuthService, user_has_permission

DbSession = Annotated[Session, Depends(get_db)]


def get_auth_service(db: DbSession) -> AuthService:
    return AuthService(db)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_current_user(
    db: DbSession,
    authorization: Annotated[str | None, Header()] = None,
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise AuthenticationError("Missing or invalid authorization header")

    token = authorization.removeprefix("Bearer ").strip()
    try:
        payload = decode_access_token(token)
    except JWTError as exc:
        raise AuthenticationError("Invalid or expired token") from exc

    if payload.get("type") != "access":
        raise AuthenticationError("Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationError("Invalid token payload")

    user = (
        db.query(User)
        .options(
            joinedload(User.organization),
            joinedload(User.role),
        )
        .filter(User.id == uuid.UUID(user_id))
        .first()
    )
    if not user or not user.is_active:
        raise AuthenticationError("User not found or inactive")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_permission(permission: Permission):
    def checker(user: CurrentUser) -> User:
        if not user_has_permission(user, permission):
            raise AuthorizationError()
        return user

    return checker
