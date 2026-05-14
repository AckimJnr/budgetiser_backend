from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import jwt
from django.conf import settings


def _secret() -> str:
    return getattr(settings, "JWT_SIGNING_KEY", settings.SECRET_KEY)


def create_access_token(user_id: int) -> str:
    minutes = int(getattr(settings, "JWT_ACCESS_MINUTES", 15))
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "typ": "access",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=minutes)).timestamp()),
    }
    return jwt.encode(payload, _secret(), algorithm="HS256")


def create_refresh_token(user_id: int) -> str:
    days = int(getattr(settings, "JWT_REFRESH_DAYS", 7))
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "typ": "refresh",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=days)).timestamp()),
    }
    return jwt.encode(payload, _secret(), algorithm="HS256")


def decode_token(token: str, expected_type: str) -> Optional[dict[str, Any]]:
    try:
        payload = jwt.decode(token, _secret(), algorithms=["HS256"])
        if payload.get("typ") != expected_type:
            return None
        return payload
    except jwt.PyJWTError:
        return None
