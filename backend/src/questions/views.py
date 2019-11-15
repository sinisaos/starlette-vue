import datetime
from starlette.responses import (
    UJSONResponse,
    RedirectResponse,
    Response
)
from starlette.authentication import requires
from tortoise.transactions import in_transaction
from models import User, Question, Tag


async def questions_all(request):
    # i don't now how to serialize fk relations with .prefech_related
    # than i use raw sql
    async with in_transaction() as conn:
        questions = await conn.execute_query(
            "SELECT question.*, user.username, GROUP_CONCAT(tag.name) as tags \
            FROM question JOIN user ON user.id=question.user_id \
            LEFT JOIN question_tag ON question.id = question_tag.question_id \
            LEFT JOIN tag ON question_tag.tag_id = tag.id \
            GROUP BY question.id ORDER BY question.id DESC"
        )
    return UJSONResponse(
        {
            "questions": questions
        }
    )


async def question(request):
    """
    Single question
    """
    id = request.path_params["id"]
    results = await Question.get(id=id)
    async with in_transaction() as conn:
        question = await conn.execute_query(
            f"SELECT question.*, user.username, GROUP_CONCAT(tag.name) as tags \
            FROM question JOIN user ON user.id=question.user_id \
            LEFT JOIN question_tag ON question.id = question_tag.question_id \
            LEFT JOIN tag ON question_tag.tag_id = tag.id  \
            WHERE question.id = {id} GROUP BY question.id"
        )
    # update question views
    results.view += 1
    await results.save()
    return UJSONResponse(
        {
            "question": question
        }
    )


@requires("authenticated")
async def question_create(request):
    """
    Question form
    """
    session_user = request.user.username
    results = await User.get(username=session_user)
    form = await request.json()
    title = form["title"]
    content = form["content"]
    if request.method == "POST":
        # possible to insert only one tag without error
        if "," in form["tags"] or len((form["tags"]).split()) == 1:
            query = Question(
                title=title,
                slug="-".join(title.lower().split()),
                content=content,
                created=datetime.datetime.now(),
                view=0,
                question_like=0,
                answer_count=0,
                user_id=results.id,
            )
            await query.save()
            tags = []
            # split tags and make sure that is valid tags list without empty
            # space and than insert in db
            valid_tags_list = [i for i in form["tags"].split(",") if i != '']
            for idx, item in enumerate(valid_tags_list):
                tag = Tag(name=item.lower())
                await tag.save()
                tags.append(tag)
                await query.tags.add(tags[idx])
            return RedirectResponse(url="/questions", status_code=302)
        return Response(
            "Tags must be comma-separated",
            status_code=422
        )


async def tags(request):
    """
    All tags
    """
    tag = request.path_params["tag"]
    async with in_transaction() as conn:
        questions = await conn.execute_query(
            f"SELECT question.title, question.created, question.id, \
            question.slug, user.username \
            FROM question JOIN user ON user.id=question.user_id \
            LEFT JOIN question_tag ON question.id = question_tag.question_id \
            LEFT JOIN tag ON question_tag.tag_id = tag.id \
            WHERE tag.name=\"{tag}\" GROUP BY question.id \
            ORDER BY question.id DESC"
        )
    return UJSONResponse(
        {
            "questions": questions
        }
    )
