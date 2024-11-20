from starlette.routing import Route, Router

from apps.questions.views import (
    answer_accept,
    answer_create,
    answer_delete,
    answer_edit,
    answer_like,
    answers_user,
    question,
    question_create,
    question_delete,
    question_edit,
    question_like,
    questions_all,
    questions_solved,
    questions_unsolved,
    questions_user,
    tags,
    tags_categories,
)

questions_routes = Router(
    [
        # all questions endpoints
        Route(
            "/", endpoint=questions_all, methods=["GET"], name="questions_all"
        ),
        Route(
            "/unsolved",
            endpoint=questions_unsolved,
            methods=["GET"],
            name="questions_unsolved",
        ),
        Route(
            "/solved",
            endpoint=questions_solved,
            methods=["GET"],
            name="questions_solved",
        ),
        Route(
            "/{id:int}/{slug:str}",
            endpoint=question,
            methods=["GET", "POST"],
            name="question",
        ),
        # profile user questions and answers
        Route(
            "/user-questions/{id:str}",
            endpoint=questions_user,
            methods=["GET", "POST"],
            name="questions_user",
        ),
        Route(
            "/user-answers/{id:str}",
            endpoint=answers_user,
            methods=["GET", "POST"],
            name="answers_user",
        ),
        # question endpoints
        Route(
            "/create",
            endpoint=question_create,
            methods=["GET", "POST"],
            name="question_create",
        ),
        Route(
            "/{id:int}",
            endpoint=question_edit,
            methods=["PUT"],
            name="question_edit",
        ),
        Route(
            "/{id:int}/{slug:str}",
            endpoint=question_delete,
            methods=["DELETE"],
            name="question_delete",
        ),
        Route(
            "/question-like/{id:int}",
            endpoint=question_like,
            methods=["POST"],
            name="question_like",
        ),
        # answer endpoints
        Route(
            "/answer-create/{id:int}",
            endpoint=answer_create,
            methods=["POST"],
            name="answer_create",
        ),
        Route(
            "/answer-like/{id:int}",
            endpoint=answer_like,
            methods=["POST"],
            name="answer_like",
        ),
        Route(
            "/answer-accept/{id:int}",
            endpoint=answer_accept,
            methods=["POST"],
            name="answer_accept",
        ),
        Route(
            "/answer/{id:int}",
            endpoint=answer_edit,
            methods=["PUT"],
            name="answer_edit",
        ),
        Route(
            "/answer/{id:int}",
            endpoint=answer_delete,
            methods=["DELETE"],
            name="answer_delete",
        ),
        # tags
        Route("/tags/{tag:str}", endpoint=tags, methods=["GET"], name="tags"),
        Route(
            "/categories",
            endpoint=tags_categories,
            methods=["GET"],
            name="tags_categories",
        ),
    ]
)
