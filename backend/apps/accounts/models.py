import os

import bcrypt
import jwt
from marshmallow import Schema
from marshmallow import fields as flds
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
)
from tortoise import fields
from tortoise.models import Model


class BaseUser(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    joined = fields.DatetimeField(auto_now_add=True)
    last_login = fields.DatetimeField(auto_now=True)
    login_count = fields.IntField(default=0)
    is_superuser = fields.BooleanField(default=False)

    def __str__(self):
        return self.username


class BaseUserSchema(Schema):
    id = flds.Int()
    username = flds.Str()
    email = flds.Str()
    joined = flds.DateTime()
    last_login = flds.DateTime()
    login_count = flds.Int()
    is_superuser = flds.Boolean()


# model schemas
users_schema = BaseUserSchema(many=True)
user_schema = BaseUserSchema()


class UserAuthentication(AuthenticationBackend):
    async def authenticate(self, request):
        jwt_cookie = request.cookies.get("jwt")
        if jwt_cookie:
            try:
                payload = jwt.decode(
                    jwt_cookie.encode("utf8"),
                    str(os.environ["SECRET_KEY"]),
                    algorithms=["HS256"],
                )
                return (
                    AuthCredentials(["authenticated"]),
                    SimpleUser(payload["user_id"]),
                )
            except AuthenticationError:
                raise AuthenticationError("Invalid auth credentials")
        else:
            # unauthenticated
            return


def hash_password(password: str):
    return bcrypt.hashpw(password, bcrypt.gensalt())


def check_password(password: str, hashed_password):
    return bcrypt.checkpw(password, hashed_password)


def generate_jwt(user_id):
    payload = {"user_id": user_id}
    token = jwt.encode(
        payload,
        str(os.environ["SECRET_KEY"]),
        algorithm="HS256",
    )
    return token
