import os

from dotenv import find_dotenv, load_dotenv
from secure import Secure
from starlette.applications import Starlette
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from tortoise.contrib.starlette import register_tortoise
from tortoise.exceptions import DoesNotExist

from apps.accounts.models import (
    BaseUser,
    UserAuthentication,
    hash_password,
    user_schema,
)
from apps.accounts.routes import routes
from apps.admin.config import admin_app
from apps.questions.routes import questions_routes

load_dotenv(find_dotenv())


# Security Headers are HTTP response headers that, when set,
# can enhance the security of your web application
# by enabling browser security policies.
# more on https://secure.readthedocs.io/en/latest/headers.html
secure_headers = Secure.with_default_headers()

app = Starlette()
app.mount("/accounts", routes)
app.mount("/questions", questions_routes)
app.mount("/admin", admin_app)
app.add_middleware(AuthenticationMiddleware, backend=UserAuthentication())
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.route("/", methods=["GET"])
async def index(request):
    if not await BaseUser.exists(email=os.getenv("ADMIN_EMAIL")):
        # create superuser
        user = BaseUser(
            username=os.getenv("ADMIN_USER"),
            email=os.getenv("ADMIN_EMAIL"),
            password=hash_password(os.getenv("ADMIN_PASSWORD")),
            is_superuser=True,
        )
        await user.save()
    auth_user = request.user.display_name
    try:
        user = await BaseUser.get(username=auth_user)
        result = user_schema.dump(user)
        return JSONResponse(
            {
                "auth_user": auth_user,
                "result": result,
            }
        )
    except DoesNotExist:
        response = JSONResponse(
            {
                "auth_user": "",
            }
        )
        return response


# middleware for secure headers
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        await secure_headers.set_headers_async(response)
        return response


register_tortoise(
    app,
    db_url=os.environ["DB_URI"],
    modules={"models": ["apps.accounts.models", "apps.questions.models"]},
    generate_schemas=True,
)
