"""Integration tests: a real PostgreSQL database for each test run."""

import asyncio
import os
import uuid
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

from codeshift_hr.config import get_settings
from codeshift_hr.db.url import to_asyncpg_url

BASE_URL = os.getenv("TEST_DATABASE_URL")


def pytest_collection_modifyitems(config, items):
    if BASE_URL:
        return

    skip = pytest.mark.skip(reason="set TEST_DATABASE_URL to run integration tests")
    for item in items:
        if "integration" in item.nodeid:
            item.add_marker(skip)


async def _admin(sql: str) -> None:
    engine = create_async_engine(
        to_asyncpg_url(BASE_URL),
        isolation_level="AUTOCOMMIT",
    )
    try:
        async with engine.connect() as conn:
            await conn.execute(text(sql))
    finally:
        await engine.dispose()


@pytest.fixture(scope="session")
def database_url():
    """Create, migrate, and drop a fresh database for the test session."""
    if not BASE_URL:
        pytest.skip("set TEST_DATABASE_URL to run integration tests")

    name = f"test_{uuid.uuid4().hex[:8]}"
    asyncio.run(_admin(f'CREATE DATABASE "{name}"'))
    url = make_url(to_asyncpg_url(BASE_URL)).set(database=name)
    url_str = url.render_as_string(hide_password=False)
    patch = pytest.MonkeyPatch()
    patch.setenv("APP_ENV", "ci")
    patch.setenv("DATABASE_URL", url_str)
    get_settings.cache_clear()

    config_path = Path(__file__).resolve().parents[2] / "alembic.ini"
    try:
        command.upgrade(Config(str(config_path)), "head")
        yield url_str
    finally:
        get_settings.cache_clear()
        patch.undo()
        asyncio.run(_admin(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)'))
