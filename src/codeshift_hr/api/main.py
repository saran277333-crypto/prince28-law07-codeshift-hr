from contextlib import asynccontextmanager

from fastapi import FastAPI

from codeshift_hr.api.errors import register_error_handlers
from codeshift_hr.api.middleware import RequestMiddleware
from codeshift_hr.api.routes import documents, health
from codeshift_hr.config import get_settings
from codeshift_hr.logging_setup import setup_logging
from codeshift_hr.store import RecordStore


def create_app():
    settings = get_settings()

    setup_logging(settings.log_level)

    store = RecordStore(settings.data_file)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        store.load_records()
        yield

    app = FastAPI(
        title="CodeShift HR",
        description="HR Legal Document API",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.state.store = store
    app.state.settings = settings

    app.add_middleware(RequestMiddleware)

    register_error_handlers(app)

    app.include_router(health.router)
    app.include_router(documents.router)

    return app
