from datetime import datetime, timedelta, timezone
from uuid import uuid4
import jwt

from src.core.config import settings


def generate_access_token(
    payload: dict,
    secret: str = settings.JWT_SECRET,
    algorithm: str = settings.JWT_ALGORITHM,
    expire_minutes: int = settings.JWT_ACCESS_TOKEN_EXP_MIN,
) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minutes)
    to_encode = {**payload, "type": "access", "iat": now, "exp": expire}
    access_token = jwt.encode(payload=to_encode, key=secret, algorithm=algorithm)
    return access_token


def generate_refresh_token(
    payload: dict,
    secret: str = settings.JWT_SECRET,
    algorithm: str = settings.JWT_ALGORITHM,
    expire_days: int = settings.JWT_REFRESH_TOKEN_EXP_DAYS,
) -> str:
    jti = str(uuid4())
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=expire_days)
    to_encode = {**payload, "type": "refresh", "jti": jti, "iat": now, "exp": expire}
    refresh_token = jwt.encode(payload=to_encode, key=secret, algorithm=algorithm)
    return refresh_token


def decode_token(
    token: str,
    secret: str = settings.JWT_SECRET,
    algorithm: str = settings.JWT_ALGORITHM,
) -> dict:
    decoded_token = jwt.decode(jwt=token, key=secret, algorithms=[algorithm])
    return decoded_token
