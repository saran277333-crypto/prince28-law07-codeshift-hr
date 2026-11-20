from http import HTTPStatus

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def get_request_id(request: Request):
    return getattr(request.state, "request_id", None)


def create_problem(request, status_code, title, detail):
    request_id = get_request_id(request)

    return {
        "type": "about:blank",
        "title": title,
        "status": status_code,
        "detail": detail,
        "instance": request.url.path,
        "request_id": request_id,
    }


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    title = HTTPStatus(exc.status_code).phrase

    body = create_problem(request, exc.status_code, title, str(exc.detail))

    return JSONResponse(
        status_code=exc.status_code,
        content=body,
        media_type="application/problem+json",
        headers=exc.headers,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body = create_problem(request, 422, "Validation Error", "Request validation failed.")

    body["errors"] = [
        {"field": ".".join(str(item) for item in error["loc"]), "message": error["msg"]}
        for error in exc.errors()
    ]

    return JSONResponse(status_code=422, content=body, media_type="application/problem+json")


def register_error_handlers(app):
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
