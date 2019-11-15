import bcrypt
import jwt
from tortoise.models import Model
from tortoise import fields
from starlette.authentication import (
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
    AuthCredentials,
)
from settings import SECRET_KEY

# change this line to set another user as admin user
ADMIN = "admin"


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    joined = fields.DatetimeField(auto_now_add=True)
    last_login = fields.DatetimeField(auto_now=True)
    login_count = fields.IntField()
    password = fields.CharField(max_length=255)

    def __str__(self):
        return self.username


class Question(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    slug = fields.CharField(max_length=255)
    content = fields.TextField()
    created = fields.DatetimeField(auto_now_add=True)
    view = fields.IntField(default=0)
    question_like = fields.IntField(default=0)
    answer_count = fields.IntField()
    accepted_answer = fields.BooleanField(default=False)
    tags = fields.ManyToManyField(
        'models.Tag', related_name='tags', through='question_tag')
    user = fields.ForeignKeyField(
        'models.User', related_name='user', on_delete=fields.CASCADE)

    def __str__(self):
        return self.title


class Answer(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    created = fields.DatetimeField(auto_now_add=True)
    answer_like = fields.IntField(default=0)
    is_accepted_answer = fields.BooleanField(default=False)
    ans_user = fields.ForeignKeyField(
        'models.User', related_name='ans_user', on_delete=fields.CASCADE)
    question = fields.ForeignKeyField(
        'models.Question', related_name='question', on_delete=fields.CASCADE)


class Tag(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserAuthentication(AuthenticationBackend):
    async def authenticate(self, request):
        jwt_cookie = request.cookies.get("jwt")
        if jwt_cookie:
            try:
                payload = jwt.decode(
                    jwt_cookie.encode("utf8"),
                    str(SECRET_KEY),
                    algorithms=["HS256"]
                )
                if SimpleUser(payload["user_id"]).username == ADMIN:
                    return (
                        AuthCredentials(["authenticated", ADMIN]),
                        SimpleUser(payload["user_id"]),
                    )
                else:
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
    token = jwt.encode(payload, str(SECRET_KEY),
                       algorithm="HS256").decode("utf-8")
    return token
