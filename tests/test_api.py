import pytest
from fastapi.testclient import TestClient

from codeshift_hr.api.main import create_app


@pytest.fixture
def client():
    with TestClient(create_app()) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_ready(client):
    response = client.get("/ready")
    assert response.status_code == 200


def test_list_documents(client):
    response = client.get("/v1/documents")
    assert response.status_code == 200
    assert response.json()["total"] == 3


def test_limit_documents(client):
    response = client.get("/v1/documents?limit=2")
    assert len(response.json()["items"]) == 2


def test_search_documents(client):
    response = client.get("/v1/documents?q=Social")
    assert response.status_code == 200
    assert response.json()["total"] >= 1


def test_get_document(client):
    response = client.get("/v1/documents/001")
    assert response.status_code == 200


def test_document_not_found(client):
    response = client.get("/v1/documents/999")
    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/problem+json")


def test_invalid_limit(client):
    response = client.get("/v1/documents?limit=0")
    assert response.status_code == 422


def test_request_id(client):
    response = client.get("/health", headers={"X-Request-ID": "abc123"})
    assert response.headers["X-Request-ID"] == "abc123"


def test_swagger_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200
