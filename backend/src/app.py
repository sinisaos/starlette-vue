import uvicorn
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.starlette import register_tortoise
from secure import SecureHeaders
from settings import SECRET_KEY, DB_URI
from models import UserAuthentication, User
from accounts.routes import routes
from questions.routes import questions_routes

# Security Headers are HTTP response headers that, when set,
# can enhance the security of your web application
# by enabling browser security policies.
# more on https://secure.readthedocs.io/en/latest/headers.html
secure_headers = SecureHeaders()

app = Starlette(debug=True)
app.mount("/accounts", routes)
app.mount("/questions", questions_routes)
app.add_middleware(AuthenticationMiddleware, backend=UserAuthentication())
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


@app.route("/", methods=["GET"])
async def index(request):
    token = request.cookies.get('jwt')
    auth_user = request.user.display_name
    # use values() for serialization
    results = await User.all().order_by('-id').values()
    try:
        result = await User.get(username=auth_user).values()
        return UJSONResponse(
            {
                "results": results,
                "token": token,
                "auth_user": auth_user,
                "result": result,
            }
        )
    except:
        response = UJSONResponse(
            {
                "results": results,
                "token": token,
                "auth_user": auth_user,
            }
        )
        return response

# middleware for secure headers
@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.starlette(response)
    return response


register_tortoise(
    app, db_url=DB_URI, modules={"models": ["models"]}, generate_schemas=True
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
