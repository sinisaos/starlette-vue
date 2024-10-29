from secure import Secure
from starlette.applications import Starlette
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from tortoise.contrib.starlette import register_tortoise
from settings import SECRET_KEY, DB_URI
from accounts.models import UserAuthentication, User, users_schema, user_schema
from accounts.routes import routes
from questions.routes import questions_routes

# Security Headers are HTTP response headers that, when set,
# can enhance the security of your web application
# by enabling browser security policies.
# more on https://secure.readthedocs.io/en/latest/headers.html
secure_headers = Secure.with_default_headers()

app = Starlette(debug=True)
app.mount("/accounts", routes)
app.mount("/questions", questions_routes)
app.add_middleware(AuthenticationMiddleware, backend=UserAuthentication())
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.route("/", methods=["GET"])
async def index(request):
    auth_user = request.user.display_name
    users = await User.all().order_by("-id")
    results = users_schema.dump(users)
    try:
        user = await User.get(username=auth_user)
        result = user_schema.dump(user)
        return JSONResponse(
            {
                "results": results,
                "auth_user": auth_user,
                "result": result,
            }
        )
    except:
        response = JSONResponse(
            {
                "results": results,
                "auth_user": auth_user,
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
    db_url=DB_URI,
    modules={"models": ["accounts.models", "questions.models"]},
    generate_schemas=True,
)
