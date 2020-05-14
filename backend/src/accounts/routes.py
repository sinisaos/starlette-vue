from starlette.routing import Route, Router
from accounts.views import (
    register,
    login,
    logout,
    dashboard,
    delete
)

routes = Router([
    Route("/login", endpoint=login,
          methods=["GET", "POST"], name="login"),
    Route("/register", endpoint=register,
          methods=["POST"], name="register"),
    Route("/logout", endpoint=logout,
          methods=["GET"], name="logout"),
    Route("/dashboard", endpoint=dashboard,
          methods=["GET"], name="dashboard"),
    # delete user endpoint
    Route("/{id:int}", endpoint=delete,
          methods=["DELETE"], name="delete")
])
