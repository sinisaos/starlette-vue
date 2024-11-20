from marshmallow import Schema
from marshmallow import fields as flds
from tortoise import fields
from tortoise.models import Model


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
        "models.Tag", related_name="tags", through="question_tag"
    )
    user = fields.ForeignKeyField(
        "models.User", related_name="user", on_delete=fields.CASCADE
    )

    def __str__(self):
        return self.title


class Answer(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    created = fields.DatetimeField(auto_now_add=True)
    answer_like = fields.IntField(default=0)
    is_accepted_answer = fields.BooleanField(default=False)
    ans_user = fields.ForeignKeyField(
        "models.User", related_name="ans_user", on_delete=fields.CASCADE
    )
    question = fields.ForeignKeyField(
        "models.Question", related_name="question", on_delete=fields.CASCADE
    )


class Tag(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserSchema(Schema):
    id = flds.Int()
    username = flds.Str()
    email = flds.Str()
    joined = flds.DateTime()
    last_login = flds.DateTime()
    login_count = flds.Int()
    password = flds.Str()


class TagSchema(Schema):
    id = flds.Int()
    name = flds.Str()


class QuestionSchema(Schema):
    id = flds.Int()
    title = flds.Str()
    slug = flds.Str()
    content = flds.Str()
    created = flds.DateTime()
    view = flds.Int()
    question_like = flds.Int()
    answer_count = flds.Int()
    accepted_answer = flds.Bool()
    tags = flds.Nested(TagSchema, many=True, dump_only=True)
    user = flds.Nested(UserSchema, dump_only=True, only=["username"])


class AnswerSchema(Schema):
    id = flds.Int()
    content = flds.Str()
    created = flds.DateTime()
    answer_like = flds.Int()
    is_accepted_answer = flds.Bool()
    ans_user = flds.Nested(UserSchema, dump_only=True, only=["username"])
    question = flds.Nested(QuestionSchema, dump_only=True, only=["id"])


# model schemas
questions_schema = QuestionSchema(many=True)
answers_schema = AnswerSchema(many=True)
question_schema = QuestionSchema()
