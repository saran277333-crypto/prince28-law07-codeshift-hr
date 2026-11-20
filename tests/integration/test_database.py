import json
import os
import subprocess
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from codeshift_hr.api.deps import check_db, get_session
from codeshift_hr.api.main import create_app
from codeshift_hr.config import Settings
from codeshift_hr.db.models import Document
from codeshift_hr.db.repository import DocumentRepository
from codeshift_hr.db.session import make_engine, make_sessionmaker

ROWS = [
    {"id": "001", "title": "Alpha", "kind": "circular", "year": 2024, "tags": ["a", "b"]},
    {"id": "002", "title": "Beta", "kind": "guideline", "year": 2025, "tags": ["b"]},
    {"id": "003", "title": "Gamma", "kind": "circular", "year": 2025, "tags": []},
]


@pytest.fixture
def settings(database_url):
    return Settings(app_env="ci", database_url=database_url, _env_file=None)


@pytest.fixture
async def seeded(settings):
    """Reset the test database to a known set of rows."""
    engine = make_engine(settings)
    try:
        async with make_sessionmaker(engine)() as session, session.begin():
            await session.execute(text("DELETE FROM documents"))
            for row in ROWS:
                metadata = {key: value for key, value in row.items() if key not in ("id", "title")}
                session.add(
                    Document(
                        external_id=row["id"],
                        title=row["title"],
                        sha256=row["id"] * 21,
                        metadata_=metadata,
                    )
                )
        yield settings
    finally:
        await engine.dispose()


async def test_migrations_created_the_tables(settings):
    engine = make_engine(settings)
    try:
        async with engine.connect() as conn:
            tables = set(
                await conn.scalars(
                    text(
                        "SELECT table_name FROM information_schema.tables "
                        "WHERE table_schema='public'"
                    )
                )
            )
            version = await conn.scalar(text("SELECT version_num FROM alembic_version"))
    finally:
        await engine.dispose()

    assert {"documents", "pages", "alembic_version"} <= tables
    assert version


@pytest.mark.parametrize(
    ("filters", "expected"),
    [
        ({"kind": "circular"}, ["001", "003"]),
        ({"year": "2025"}, ["002", "003"]),
        ({"tags": "b"}, ["001", "002"]),
        ({"kind": "circular", "year": "2025"}, ["003"]),
    ],
)
async def test_repository_filters(seeded, filters, expected):
    engine = make_engine(seeded)
    try:
        async with make_sessionmaker(engine)() as session:
            total, items = await DocumentRepository(session).list(
                q=None,
                filters=filters,
                limit=10,
                offset=0,
            )
    finally:
        await engine.dispose()

    assert [item["id"] for item in items] == expected
    assert total == len(expected)


def test_api_against_real_database(seeded):
    async def get_test_session():
        engine = make_engine(seeded)
        try:
            async with make_sessionmaker(engine)() as session:
                yield session
        finally:
            await engine.dispose()

    async def check_test_database():
        engine = make_engine(seeded)
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        finally:
            await engine.dispose()

    app = create_app(seeded)
    app.dependency_overrides[get_session] = get_test_session
    app.dependency_overrides[check_db] = check_test_database
    try:
        with TestClient(app) as client:
            assert client.get("/ready").json()["checks"]["database"] is True
            assert client.get("/v1/documents/002").json()["title"] == "Beta"
            assert client.get("/v1/documents", params={"q": "gamm"}).json()["total"] == 1
    finally:
        app.dependency_overrides.clear()


def test_loader_is_idempotent(database_url, tmp_path):
    data = tmp_path / "records.json"
    data.write_text(json.dumps([{"id": "L1", "x": 1}, {"id": "L2", "x": 2}]), encoding="utf-8")
    env = {
        **os.environ,
        "APP_ENV": "ci",
        "DATABASE_URL": database_url,
        "DATA_FILE": str(data),
    }

    def run() -> str:
        command = [sys.executable, "scripts/load_db.py"]
        return subprocess.run(command, env=env, check=True, capture_output=True, text=True).stdout

    assert "inserted=2" in run()
    assert "inserted=0 updated=0 unchanged=2" in run()
