"""FastAPI dependencies for database access."""

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from codeshift_hr.config import Settings
from codeshift_hr.db.repository import DocumentRepository
from codeshift_hr.db.session import SessionLocal, engine


def get_app_settings(request: Request) -> Settings:
    return request.app.state.settings


SettingsDep = Annotated[Settings, Depends(get_app_settings)]


async def get_session() -> AsyncIterator[AsyncSession]:
    """Create one database session per request."""
    async with SessionLocal() as session:
        yield session


async def get_repo(
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> DocumentRepository:
    """Provide the document repository."""
    return DocumentRepository(session)


async def check_db() -> bool:
    """Check whether PostgreSQL is reachable."""
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True
    except (SQLAlchemyError, OSError):
        return False


DbCheckDep = Annotated[bool, Depends(check_db)]
