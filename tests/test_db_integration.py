"""Integration tests for PostgreSQL."""

import asyncio
import os
from uuid import uuid4

import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from codeshift_hr.db.models import Document
from codeshift_hr.db.repository import DocumentRepository
from codeshift_hr.db.url import to_asyncpg_url

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

pytestmark = pytest.mark.skipif(
    not TEST_DATABASE_URL,
    reason="TEST_DATABASE_URL is not configured",
)


def run_test(test_function):
    """Run an asynchronous database test."""

    async def wrapper():
        engine = create_async_engine(to_asyncpg_url(TEST_DATABASE_URL))

        try:
            Session = async_sessionmaker(engine, expire_on_commit=False)

            async with Session() as session:
                external_id = f"test-{uuid4().hex}"

                document = Document(
                    external_id=external_id,
                    title="Integration Test Document",
                    doc_type="guideline",
                    sha256=uuid4().hex,
                    metadata_={"test_marker": external_id},
                )

                session.add(document)
                await session.commit()

                try:
                    await test_function(session, external_id)
                finally:
                    await session.execute(
                        delete(Document).where(Document.external_id == external_id)
                    )
                    await session.commit()
        finally:
            await engine.dispose()

    asyncio.run(wrapper())


def test_database_get_document():
    async def check(session, external_id):
        repo = DocumentRepository(session)
        result = await repo.get(external_id)

        assert result is not None
        assert result["id"] == external_id
        assert result["title"] == "Integration Test Document"

    run_test(check)


def test_database_metadata_filter():
    async def check(session, external_id):
        repo = DocumentRepository(session)

        total, items = await repo.list(
            q=None,
            filters={"test_marker": external_id},
            limit=10,
            offset=0,
        )

        assert total >= 1
        assert any(item["id"] == external_id for item in items)

    run_test(check)


def test_database_search():
    async def check(session, external_id):
        repo = DocumentRepository(session)

        total, items = await repo.list(
            q="Integration Test Document",
            filters={},
            limit=10,
            offset=0,
        )

        assert total >= 1
        assert any(item["id"] == external_id for item in items)

    run_test(check)
