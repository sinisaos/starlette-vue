import os

import bcrypt
from dotenv import find_dotenv, load_dotenv
from fastadmin import TortoiseModelAdmin, register, settings
from fastadmin import fastapi_app as admin_app

from apps.accounts.models import User
from apps.questions.models import Answer, Question, Tag

load_dotenv(find_dotenv())


# EXPORT to enviroment works, but this is the only way I find to
# override the default settings with values ​​from the .env
settings.settings.ADMIN_SITE_NAME = os.getenv("ADMIN_SITE_NAME")
settings.settings.ADMIN_USER_MODEL = os.getenv("ADMIN_USER_MODEL")
settings.settings.ADMIN_USER_MODEL_USERNAME_FIELD = os.getenv(
    "ADMIN_USER_MODEL_USERNAME_FIELD"
)
settings.settings.ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY")


@register(User)
class UserAdmin(TortoiseModelAdmin):
    exclude = ("password",)
    list_display = (
        "id",
        "username",
        "email",
        "joined",
        "last_login",
        "login_count",
    )
    list_display_links = ("id",)
    search_fields = ("username", "email")

    async def authenticate(self, username: str, password: str) -> int | None:
        user = await User.filter(username=username).first()
        if not user:
            return None
        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return None
        return user.id


@register(Question)
class QuestionAdmin(TortoiseModelAdmin):
    list_display = (
        "id",
        "title",
        "content",
        "created",
        "view",
        "question_like",
        "answer_count",
        "accepted_answer",
        "tags",
        "user",
    )
    list_display_links = (
        "id",
        "user",
        "tags",
    )
    search_fields = (
        "title",
        "content",
    )
    list_filter = (
        "title",
        "user",
        "view",
        "question_like",
        "answer_count",
        "accepted_answer",
    )


@register(Answer)
class AnswerAdmin(TortoiseModelAdmin):
    list_display = (
        "id",
        "content",
        "created",
        "answer_like",
        "is_accepted_answer",
        "ans_user",
        "question",
    )
    list_display_links = (
        "id",
        "question",
    )
    search_fields = ("content",)
    list_filter = (
        "content",
        "created",
        "answer_like",
        "is_accepted_answer",
        "ans_user",
        "question",
    )


@register(Tag)
class TagAdmin(TortoiseModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_display_links = ("id",)
    search_fields = ("name",)
    list_filter = ("name",)


# re-export admin_app
__all__ = ["admin_app"]
