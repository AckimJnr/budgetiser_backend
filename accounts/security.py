from typing import Optional

from django.contrib.auth import authenticate, get_user_model
from ninja.security import HttpBearer

from .jwt_utils import decode_token

User = get_user_model()


class JWTAuth(HttpBearer):
    def authenticate(self, request, token: str) -> Optional[User]:
        payload = decode_token(token, "access")
        if not payload:
            return None
        try:
            user_id = int(payload.get("sub", "0"))
        except (TypeError, ValueError):
            return None
        user = User.objects.filter(id=user_id, is_active=True).first()
        return user


def authenticate_username_or_email(username: str, password: str):
    user = authenticate(username=username, password=password)
    if user:
        return user
    u = User.objects.filter(email__iexact=username).first()
    if u and u.check_password(password):
        return u
    return None
