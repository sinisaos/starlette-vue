from starlette.routing import Route, Router
from questions.views import (
    questions_all,
    question,
    question_create,
    tags
)


questions_routes = Router([
    Route("/", endpoint=questions_all,
          methods=["GET"], name="questions_all"),
    Route("/{id:int}/{slug:str}", endpoint=question,
          methods=["GET", "POST"], name="question"),
    Route("/create", endpoint=question_create,
          methods=["GET", "POST"], name="question_create"),
    Route("/tags/{tag:str}", endpoint=tags, methods=["GET"], name="tags"),
])
