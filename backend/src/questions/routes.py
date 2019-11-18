from starlette.routing import Route, Router
from questions.views import (
    questions_all,
    question,
    question_like,
    question_create,
    answer_create,
    answer_like,
    tags
)


questions_routes = Router([
    Route("/", endpoint=questions_all,
          methods=["GET"], name="questions_all"),
    Route("/{id:int}/{slug:str}", endpoint=question,
          methods=["GET", "POST"], name="question"),
    Route("/create", endpoint=question_create,
          methods=["GET", "POST"], name="question_create"),
    Route("/question-like/{id:int}", endpoint=question_like,
          methods=["POST"], name="question_like"),
    Route("/tags/{tag:str}", endpoint=tags, methods=["GET"], name="tags"),
    Route("/answer-create/{id:int}", endpoint=answer_create,
          methods=["POST"], name="answer_create"),
    Route("/answer-like/{id:int}", endpoint=answer_like,
          methods=["POST"], name="answer_like"),
])
