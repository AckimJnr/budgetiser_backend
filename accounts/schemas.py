from ninja import ModelSchema
from .models import User

class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'username', 'email', 'first_name', 'last_name', 'created_at', 'updated_at']

class UserCreateSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ['username', 'email', 'password', 'first_name', 'last_name']
