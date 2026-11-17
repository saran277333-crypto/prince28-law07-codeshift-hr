import logging
import time
from uuid import uuid4

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from codeshift_hr.api.errors import create_problem

logger = logging.getLogger(__name__)


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # Step 1: Generate or receive a request ID
        request_id = request.headers.get("X-Request-ID")

        if not request_id or len(request_id) > 128:
            request_id = uuid4().hex

        request.state.request_id = request_id

        # Step 2: Start the timer
        start_time = time.perf_counter()

        try:
            # Step 3: Process the request
            response = await call_next(request)

        except Exception:  # noqa: BLE001
            # Step 4: Handle unexpected errors
            logger.error("Unexpected server error", extra={"request_id": request_id})

            body = create_problem(
                request, 500, "Internal Server Error", "An unexpected error occurred."
            )

            response = JSONResponse(
                status_code=500, content=body, media_type="application/problem+json"
            )

        # Step 5: Calculate response time
        duration = (time.perf_counter() - start_time) * 1000
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "Request completed",
            extra={"request_id": request_id, "duration_ms": round(duration, 2)},
        )

        return response
