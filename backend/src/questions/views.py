import datetime
import itertools as it
from starlette.authentication import requires
from starlette.responses import (
    UJSONResponse,
    RedirectResponse,
    Response
)
from tortoise.transactions import in_transaction
from questions.models import (
    Question,
    Tag,
    Answer,
    questions_schema,
    answers_schema,
    question_schema,
)
from accounts.models import User


async def questions_all(request):
    """
    Marshmallow for serilization
    """
    results = await Question.all().prefetch_related(
        "user", "tags").order_by("-id")
    # Serialize the queryset
    questions = questions_schema.dump(results)
    answer_count = [(
        await Answer.all()
        .prefetch_related("question")
        .filter(question__id=row.id).count()
    ) for row in results]
    for item, x in zip(questions, answer_count):
        item['answer_count'] = x
    return UJSONResponse(
        {
            "questions": questions
        }
    )


async def questions_unsolved(request):
    results = await Question.filter(accepted_answer=0).prefetch_related(
        "user", "tags").order_by("-id")
    # Serialize the queryset
    questions = questions_schema.dump(results)
    answer_count = [(
        await Answer.all()
        .prefetch_related("question")
        .filter(question__id=row.id).count()
    ) for row in results]
    for item, x in zip(questions, answer_count):
        item['answer_count'] = x
    return UJSONResponse(
        {
            "questions": questions
        }
    )


async def questions_solved(request):
    results = await Question.filter(accepted_answer=1).prefetch_related(
        "user", "tags").order_by("-id")
    # Serialize the queryset
    questions = questions_schema.dump(results)
    answer_count = [(
        await Answer.all()
        .prefetch_related("question")
        .filter(question__id=row.id).count()
    ) for row in results]
    for item, x in zip(questions, answer_count):
        item['answer_count'] = x
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
    result = await Question.get(id=id).prefetch_related("user", "tags")
    answers_result = (
        await Answer.all()
        .prefetch_related("ans_user")
        .filter(question__id=id)
        .order_by("-id")
    )
    # Serialize the queryset
    question = question_schema.dump(result)
    answers = answers_schema.dump(answers_result)
    # update question views
    result.view += 1
    await result.save()
    return UJSONResponse(
        {
            "question": question,
            'answers': answers,
            "answer_count": len(answers)
        }
    )


@requires("authenticated")
async def question_like(request):
    id = request.path_params["id"]
    results = await Question.get(id=id)
    if request.user.is_authenticated:
        # update question likes and decrease question views
        # to avoid duplication of question views
        results.question_like += 1
        results.view -= 1
        await results.save()
        return RedirectResponse(
            url="/", status_code=303
        )
    else:
        return Response(status_code=403)


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
            return RedirectResponse(url="/questions", status_code=303)
        return Response(
            "Tags must be comma-separated",
            status_code=422
        )


@requires("authenticated")
async def question_edit(request):
    """
    Question edit form
    """
    id = request.path_params["id"]
    session_user = request.user.username
    question = await Question.get(id=id).prefetch_related('user')
    if request.method == "PUT" and question.user.username == session_user:
        form = await request.json()
        title = form["title"]
        content = form["content"]
        await Question.filter(id=id).update(
            title=title,
            slug="-".join(title.lower().split()),
            content=content,
            created=question.created,
            view=question.view,
            question_like=question.question_like,
            answer_count=question.answer_count,
            accepted_answer=question.accepted_answer,
            user_id=question.user.id,
        )
        # 303 status code for redirect after update
        return RedirectResponse(url="/questions/", status_code=303)
    else:
        return Response(status_code=403)


async def questions_user(request):
    id = request.path_params["id"]
    results = await User.get(username=id)
    result = await Question.all().prefetch_related(
        "user", "tags").filter(
        user_id=results.id).order_by("-id")
    # Serialize the queryset
    questions = questions_schema.dump(result)
    return UJSONResponse(
        {
            "questions": questions
        }
    )


@requires("authenticated")
async def question_delete(request):
    """
    Delete question
    """
    id = request.path_params["id"]
    session_user = request.user.username
    results = await Question.get(id=id).prefetch_related('user')
    if request.method == "DELETE" and results.user.username == session_user:
        async with in_transaction() as conn:
            await conn.execute_query(
                f"DELETE FROM tag WHERE tag.id IN \
                (SELECT question_tag.tag_id FROM question \
                JOIN question_tag \
                ON question_tag.question_id = question.id \
                WHERE question.id={id})"
            )
        await Question.get(id=id).delete()
        # 303 status code for redirect after delete
        response = RedirectResponse(url="/", status_code=303)
        return response


async def answer_create(request):
    """
    Answer form
    """
    id = request.path_params["id"]
    session_user = request.user.username
    form = await request.json()
    content = form["content"]
    result = await User.get(username=session_user)
    results = await Question.get(id=id)
    if request.method == "POST":
        query = Answer(
            content=content,
            created=datetime.datetime.now(),
            answer_like=0,
            is_accepted_answer=0,
            question_id=results.id,
            ans_user_id=result.id,
        )
        await query.save()
        results.answer_count += 1
        await results.save()
        return RedirectResponse(
            url="/questions/", status_code=303
        )


@requires("authenticated")
async def answer_like(request):
    id = request.path_params["id"]
    result = await Answer.get(id=id)
    question = await Question.get(id=result.question_id)
    if request.user.is_authenticated:
        # update answer likes and decrease question views
        # to avoid duplication of question views
        result.answer_like += 1
        await result.save()
        question.view -= 1
        await question.save()
        return RedirectResponse(
            url="/questions/", status_code=303
        )
    else:
        return Response(status_code=403)


async def answer_accept(request):
    id = request.path_params["id"]
    result = await Answer.get(id=id)
    question = await Question.get(id=result.question_id)
    result.is_accepted_answer = 1
    await result.save()
    question.accepted_answer = 1
    await question.save()
    return RedirectResponse(
        url="/questions/", status_code=303
    )


async def answers_user(request):
    id = request.path_params["id"]
    results = await User.get(username=id)
    result = await Answer.all().filter(ans_user_id=results.id)
    # Serialize the queryset
    answers = answers_schema.dump(result)
    return UJSONResponse(
        {
            "answers": answers
        }
    )


@requires("authenticated")
async def answer_edit(request):
    """
    Answer edit form
    """
    id = request.path_params["id"]
    session_user = request.user.username
    answer = await Answer.get(id=id).prefetch_related('ans_user')
    if request.method == "PUT" and answer.ans_user.username == session_user:
        form = await request.json()
        content = form["content"]
        await Answer.filter(id=id).update(
            content=content,
            created=answer.created,
            answer_like=answer.answer_like,
            is_accepted_answer=answer.is_accepted_answer,
            question_id=answer.question_id,
            ans_user_id=answer.ans_user_id,
        )
        # 303 status code for redirect after update
        return RedirectResponse(url="/questions/", status_code=303)
    else:
        return Response(status_code=403)


@requires("authenticated")
async def answer_delete(request):
    """
    Delete answer
    """
    id = request.path_params["id"]
    session_user = request.user.username
    answer = (
        await Answer.get(id=id)
        .prefetch_related('ans_user')
        .filter(ans_user__username=session_user)
    )
    results = await Question.get(id=answer.question_id)
    if request.method == "DELETE" and answer.ans_user.username == session_user:
        # decrease question answer count
        results.answer_count -= 1
        if answer.is_accepted_answer:
            results.accepted_answer = False
        await results.save()
        await Answer.get(id=id).delete()
        # 303 status code for redirect after delete
        response = RedirectResponse(url="/", status_code=303)
        return response


async def tags(request):
    """
    All tags
    """
    tag = request.path_params["tag"]
    result = (
        await Question.all()
        .prefetch_related("user", "tags")
        .filter(tags__name=tag)
        .order_by("-id")
    )
    # Serialize the queryset
    questions = questions_schema.dump(result)
    return UJSONResponse(
        {
            "questions": questions
        }
    )


async def tags_categories(request):
    """
    Tags categories
    """
    # use itertools.groupby to simulate SQL GROUP BY
    results = await Tag.all().order_by("name").values("name")
    categories_tags = [
        (k, sum(1 for i in g)) for k, g in it.groupby(results)
    ]
    return UJSONResponse(
        {
            "categories_tags": categories_tags
        }
    )
