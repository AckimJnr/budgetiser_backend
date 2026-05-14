from ninja import Router
from ninja import Schema
from pydantic import Field

from django.contrib.auth import get_user_model

from .jwt_utils import create_access_token, create_refresh_token, decode_token
from .schemas import UserSchema
from .security import authenticate_username_or_email

User = get_user_model()
router = Router(tags=["Auth"])


class LoginIn(Schema):
    username: str = Field(..., min_length=1, description="Username or email")
    password: str = Field(..., min_length=1)


class RefreshIn(Schema):
    refresh: str = Field(..., min_length=1)


class TokenPairOut(Schema):
    access: str
    refresh: str
    token_type: str = "bearer"
    user: UserSchema


class RefreshTokenOut(Schema):
    access: str
    refresh: str
    token_type: str = "bearer"


@router.post("/login/", response={200: TokenPairOut, 401: dict})
def login(request, data: LoginIn):
    user = authenticate_username_or_email(data.username.strip(), data.password)
    if not user or not user.is_active:
        return 401, {"detail": "Invalid credentials"}
    return {
        "access": create_access_token(user.id),
        "refresh": create_refresh_token(user.id),
        "token_type": "bearer",
        "user": UserSchema.from_orm(user),
    }


@router.post("/refresh/", response={200: RefreshTokenOut, 401: dict})
def refresh_tokens(request, data: RefreshIn):
    payload = decode_token(data.refresh.strip(), "refresh")
    if not payload:
        return 401, {"detail": "Invalid refresh token"}
    try:
        user_id = int(payload.get("sub", "0"))
    except (TypeError, ValueError):
        return 401, {"detail": "Invalid refresh token"}
    user = User.objects.filter(id=user_id, is_active=True).first()
    if not user:
        return 401, {"detail": "Invalid refresh token"}
    return {
        "access": create_access_token(user.id),
        "refresh": create_refresh_token(user.id),
        "token_type": "bearer",
    }
