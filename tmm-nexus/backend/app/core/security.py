from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: UUID, organization_id: UUID, role: str) -> str:
    settings = get_settings()

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(subject),
        "org": str(organization_id),
        "role": role,
        "type": "access",
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )

    print("CREATED TOKEN:", token)
    print("SECRET KEY:", settings.secret_key)
    print("ALGORITHM:", settings.algorithm)

    return token


def decode_access_token(token: str) -> dict:
    settings = get_settings()

    print("TOKEN RECEIVED:", token)
    print("SECRET KEY:", settings.secret_key)
    print("ALGORITHM:", settings.algorithm)

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        print("DECODED PAYLOAD:", payload)
        return payload

    except JWTError as e:
        print("JWT ERROR:", repr(e))
        raise