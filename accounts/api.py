from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from .models import User
from .schemas import UserSchema, UserCreateSchema
from .security import JWTAuth

router = Router(tags=["Accounts"])

@router.post("/", response={201: UserSchema})
def create_user(request, data: UserCreateSchema):
    user = User(
        username=data.username,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        password=make_password(data.password)
    )
    user.save()
    return 201, user

@router.get("/", response=List[UserSchema])
def list_users(request):
    return User.objects.all()


@router.get("/me/", response=UserSchema, auth=JWTAuth())
def me(request):
    return request.auth


@router.get("/{user_id}", response=UserSchema)
def get_user(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    return user
