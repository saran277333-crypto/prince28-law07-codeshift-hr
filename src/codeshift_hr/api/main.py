"""Main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from codeshift_hr.api.errors import register_error_handlers
from codeshift_hr.api.middleware import RequestMiddleware
from codeshift_hr.api.routes import documents, health
from codeshift_hr.config import Settings, get_settings
from codeshift_hr.db.session import engine
from codeshift_hr.logging_setup import setup_logging


def create_app(settings: Settings | None = None):
    settings = settings or get_settings()

    setup_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        await engine.dispose()

    app = FastAPI(
        title="CodeShift HR",
        description="HR Legal Document API",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.state.settings = settings

    app.add_middleware(RequestMiddleware)

    register_error_handlers(app)

    app.include_router(health.router)
    app.include_router(documents.router)

    return app
