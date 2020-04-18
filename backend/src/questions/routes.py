from starlette.routing import Route, Router
from questions.views import (
    questions_all,
    questions_unsolved,
    questions_solved,
    question,
    question_like,
    question_create,
    question_edit,
    question_delete,
    questions_user,
    answer_create,
    answer_like,
    answer_accept,
    answer_edit,
    answer_delete,
    answers_user,
    tags,
    tags_categories
)


questions_routes = Router([
    Route("/", endpoint=questions_all,
          methods=["GET"], name="questions_all"),
    Route("/unsolved", endpoint=questions_unsolved,
          methods=["GET"], name="questions_unsolved"),
    Route("/solved", endpoint=questions_solved,
          methods=["GET"], name="questions_solved"),
    Route("/{id:int}/{slug:str}", endpoint=question,
          methods=["GET", "POST"], name="question"),
    Route("/user-questions/{id:str}", endpoint=questions_user,
          methods=["GET", "POST"], name="questions_user"),
    Route("/create", endpoint=question_create,
          methods=["GET", "POST"], name="question_create"),
    Route("/question-edit/{id:int}", endpoint=question_edit,
          methods=["POST"], name="question_edit"),
    Route("/question-delete/{id:int}", endpoint=question_delete,
          methods=["GET"], name="question_delete"),
    Route("/question-like/{id:int}", endpoint=question_like,
          methods=["POST"], name="question_like"),
    Route("/tags/{tag:str}", endpoint=tags, methods=["GET"], name="tags"),
    Route("/categories", endpoint=tags_categories,
          methods=["GET"], name="tags_categories"),
    Route("/answer-create/{id:int}", endpoint=answer_create,
          methods=["POST"], name="answer_create"),
    Route("/answer-like/{id:int}", endpoint=answer_like,
          methods=["POST"], name="answer_like"),
    Route("/answer_accept/{id:int}", endpoint=answer_accept,
          methods=["POST"], name="answer_accept"),
    Route("/user-answers/{id:str}", endpoint=answers_user,
          methods=["GET", "POST"], name="answers_user"),
    Route("/answer-edit/{id:int}", endpoint=answer_edit,
          methods=["POST"], name="answer_edit"),
    Route("/answer-delete/{id:int}", endpoint=answer_delete,
          methods=["GET"], name="answer_delete"),
])
