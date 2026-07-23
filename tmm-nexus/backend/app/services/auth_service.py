import hashlib
import secrets
import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session, joinedload

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.enums import Permission, RoleName
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import AuthResponse, RoleResponse, TokenResponse, UserResponse


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def build_user_response(user: User) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        organization_id=str(user.organization_id),
        organization_name=user.organization.name,
        role=RoleResponse(
            id=str(user.role.id),
            name=user.role.name,
            permissions=user.role.permissions,
        ),
    )


def _create_refresh_token(db: Session, user: User) -> str:
    settings = get_settings()
    raw_token = secrets.token_urlsafe(48)
    token = RefreshToken(
        user_id=user.id,
        token_hash=_hash_token(raw_token),
        expires_at=datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days),
    )
    db.add(token)
    db.flush()
    return raw_token


def _issue_tokens(db: Session, user: User) -> TokenResponse:
    access_token = create_access_token(user.id, user.organization_id, user.role.name)
    refresh_token = _create_refresh_token(db, user)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def login(self, email: str, password: str) -> AuthResponse:
        user = (
            self.db.query(User)
            .options(
                joinedload(User.organization),
                joinedload(User.role),
            )
            .filter(User.email == email.lower())
            .first()
        )
        if not user or not verify_password(password, user.hashed_password):
            raise AuthenticationError()
        if not user.is_active:
            raise AuthenticationError("Account is disabled")

        tokens = _issue_tokens(self.db, user)
        self.db.commit()
        return AuthResponse(user=build_user_response(user), tokens=tokens)

    def refresh(self, refresh_token: str) -> TokenResponse:
        token_hash = _hash_token(refresh_token)
        stored = (
            self.db.query(RefreshToken)
            .filter(RefreshToken.token_hash == token_hash)
            .first()
        )
        if not stored or stored.revoked_at is not None:
            raise AuthenticationError("Invalid refresh token")
        if stored.expires_at < datetime.now(UTC):
            raise AuthenticationError("Refresh token expired")

        user = (
            self.db.query(User)
            .options(
                joinedload(User.organization),
                joinedload(User.role),
            )
            .filter(User.id == stored.user_id)
            .first()
        )
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")

        stored.revoked_at = datetime.now(UTC)
        tokens = _issue_tokens(self.db, user)
        self.db.commit()
        return tokens

    def logout(self, refresh_token: str) -> None:
        token_hash = _hash_token(refresh_token)
        stored = (
            self.db.query(RefreshToken)
            .filter(RefreshToken.token_hash == token_hash)
            .first()
        )
        if stored and stored.revoked_at is None:
            stored.revoked_at = datetime.now(UTC)
            self.db.commit()

    def get_current_user(self, user_id: uuid.UUID) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        return user


def user_has_permission(user: User, permission: Permission) -> bool:
    if user.role.name == RoleName.ADMIN.value:
        return True
    return permission.value in user.role.permissions
