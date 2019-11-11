import datetime
from starlette.responses import (
    Response,
    RedirectResponse,
)
from models import (
    User,
    check_password,
    generate_jwt,
    hash_password,
    ADMIN
)


async def register(request):
    """
    Validate form, register and authenticate user with JWT token
    """
    results = await User.all()
    form = await request.json()
    username = form["username"]
    email = form["email"]
    password = form["password"]
    for result in results:
        if email == result.email or username == result.username:
            return Response(
                "User with that email or username already exists!",
                status_code=422
            )
    query = User(
        username=username,
        email=email,
        joined=datetime.datetime.now(),
        last_login=datetime.datetime.now(),
        login_count=1,
        password=hash_password(password),
    )
    await query.save()
    user_query = await User.get(username=username)
    hashed_password = user_query.password
    valid_password = check_password(password, hashed_password)
    response = RedirectResponse(url="/", status_code=302)
    # generate httponly cookie with jwt token
    # than we don't have to store jwt in browser
    # localStorage for Vue auth
    if valid_password:
        response.set_cookie(
            "jwt",
            generate_jwt(user_query.username),
            httponly=True
        )
        response.set_cookie(
            "admin",
            ADMIN,
            httponly=True
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
        results = await User.get(username=username)
        hashed_password = results.password
        valid_password = check_password(password, hashed_password)
        if not valid_password:
            response = Response(
                "Invalid username or password!",
                status_code=422
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
            response.set_cookie("jwt", generate_jwt(
                results.username), httponly=True)
            response.set_cookie("admin", ADMIN, httponly=True)
        return response
    except:
        response = Response(
            "Please register you don't have account!",
            status_code=422
        )
        return response


async def delete(request):
    """
    Delete user
    """
    id = request.path_params["id"]
    await User.get(id=id).delete()
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("jwt")
    return response


async def logout(request):
    request.session.clear()
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("jwt")
    return response
