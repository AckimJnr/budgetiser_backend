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


def authenticate_by_email(email: str, password: str):
    user = User.objects.filter(email__iexact=email).first()
    if user and user.check_password(password):
        return user
    return None
