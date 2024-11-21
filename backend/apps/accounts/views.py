import datetime

from starlette.authentication import requires
from starlette.responses import JSONResponse, RedirectResponse, Response
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import in_transaction

from apps.accounts.models import (
    BaseUser,
    check_password,
    generate_jwt,
    hash_password,
    users_schema,
)
from apps.questions.models import (
    Answer,
    Question,
    answers_schema,
    questions_schema,
)


async def register(request):
    """
    Validate form, register and authenticate user with JWT token
    """
    results = await BaseUser.all()
    form = await request.json()
    username = form["username"]
    email = form["email"]
    password = form["password"]
    for result in results:
        if email == result.email or username == result.username:
            return Response(
                "User with that email or username already exists!",
                status_code=422,
            )
    query = BaseUser(
        username=username,
        email=email,
        joined=datetime.datetime.now(),
        last_login=datetime.datetime.now(),
        login_count=1,
        password=hash_password(password),
    )
    await query.save()
    user_query = await BaseUser.get(username=username)
    hashed_password = user_query.password
    valid_password = check_password(password, hashed_password)
    response = RedirectResponse(url="/", status_code=302)
    # generate httponly cookie with jwt token
    # than we don't have to store jwt in browser
    # localStorage for Vue auth
    if valid_password:
        response.set_cookie(
            "jwt", generate_jwt(user_query.username), httponly=True
        )
    return response


async def login(request):
    """
    Validate form, login and authenticate user with JWT token
    """
    form = await request.json()
    username = form["username"]
    password = form["password"]
    try:
        results = await BaseUser.get(username=username)
        hashed_password = results.password
        valid_password = check_password(password, hashed_password)
        if not valid_password or results.username != username:
            response = Response(
                "Invalid username or password!", status_code=422
            )
            return response
        # update login counter and login time
        results.login_count += 1
        results.last_login = datetime.datetime.now()
        await results.save()
        response = RedirectResponse(url="/", status_code=302)
        # generate httponly cookie with jwt token
        # than we don't have to store jwt in browser
        # localStorage for Vue auth
        if valid_password:
            response.set_cookie(
                "jwt", generate_jwt(results.username), httponly=True
            )
        return response
    except DoesNotExist:
        response = Response(
            "Please register you don't have account!", status_code=422
        )
        return response


@requires("authenticated")
async def dashboard(request):
    if request.user.is_authenticated:
        users = await BaseUser.all()
        results = users_schema.dump(users)
        qus = (
            await Question.all()
            .prefetch_related("user", "tags")
            .order_by("-id")
        )
        questions = questions_schema.dump(qus)
        ans = (
            await Answer.all()
            .prefetch_related("ans_user", "question")
            .order_by("-id")
        )
        answers = answers_schema.dump(ans)
        return JSONResponse(
            {
                "results": results,
                "questions": questions,
                "answers": answers,
            }
        )


@requires("authenticated")
async def delete(request):
    """
    Delete user
    """
    id = request.path_params["id"]
    session_user = request.user.username
    results = await BaseUser.get(username=session_user)
    if request.method == "DELETE" and results.username == session_user:
        async with in_transaction() as conn:
            await conn.execute_query(
                f"DELETE FROM tag WHERE tag.id IN \
                (SELECT question_tag.tag_id FROM question \
                JOIN question_tag ON question_tag.question_id = question.id \
                JOIN user ON user.id = question.user_id WHERE user.id = {id})"
            )
        async with in_transaction() as conn:
            await conn.execute_query(
                f"UPDATE question \
                JOIN answer ON question.id = answer.question_id \
                JOIN user on user.id = answer.ans_user_id \
                SET question.accepted_answer = 0 \
                WHERE user.id = {id} AND answer.is_accepted_answer = 1"
            )
        await BaseUser.get(id=id).delete()
        # 303 status code for redirect after delete
        response = RedirectResponse(url="/", status_code=303)
        response.delete_cookie("jwt")
        return response
    else:
        return Response(status_code=403)


async def logout(request):
    request.session.clear()
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("jwt")
    return response
