def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_not_ready(client, db_state):
    db_state["up"] = False
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.json()["checks"]["database"] is False


def test_list_documents(client):
    response = client.get("/v1/documents")
    assert response.status_code == 200
    assert response.json()["total"] == 3


def test_list_documents_items(client):
    response = client.get("/v1/documents")
    assert len(response.json()["items"]) == 3


def test_limit(client):
    response = client.get("/v1/documents?limit=2")
    assert len(response.json()["items"]) == 2


def test_offset(client):
    response = client.get("/v1/documents?offset=1")
    assert len(response.json()["items"]) == 2


def test_search_alpha(client):
    response = client.get("/v1/documents?q=Alpha")
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["id"] == "001"


def test_search_beta(client):
    response = client.get("/v1/documents?q=Beta")
    assert response.json()["total"] == 1


def test_search_no_results(client):
    response = client.get("/v1/documents?q=unknown")
    assert response.json()["total"] == 0


def test_filter_year(client):
    response = client.get("/v1/documents?year=2024")
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["id"] == "002"


def test_filter_kind(client):
    response = client.get("/v1/documents?kind=circular")
    assert response.json()["total"] == 2


def test_invalid_filter(client):
    response = client.get("/v1/documents?Bad-Name=1")
    assert response.status_code == 400


def test_get_document(client):
    response = client.get("/v1/documents/001")
    assert response.status_code == 200
    assert response.json()["id"] == "001"


def test_document_not_found(client):
    response = client.get("/v1/documents/999")
    assert response.status_code == 404


def test_invalid_limit(client):
    response = client.get("/v1/documents?limit=200")
    assert response.status_code == 422
