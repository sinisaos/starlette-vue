from starlette.routing import Route, Router
from accounts.views import (
    register,
    login,
    logout,
    delete
)

routes = Router([
    Route("/login", endpoint=login, methods=["GET", "POST"], name="login"),
    Route("/register", endpoint=register,
          methods=["POST"], name="register"),
    Route("/logout", endpoint=logout, methods=["GET"], name="logout"),
    Route("/delete/{id:int}", endpoint=delete,
          methods=["GET"], name="delete")
])
