import pytest
from fastapi.testclient import TestClient
from src.infrastructure.adapters.inbound.http_adapter import app, create_endpoints
from src.application.services import RecordService
from src.infrastructure.adapters.outbound.db_adapter import DbAdapter


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test.db"
    db_adapter = DbAdapter(f'sqlite:///{db_path}')
    service = RecordService(db_port=db_adapter)
    create_endpoints(service)
    return TestClient(app)

def test_post_and_get_integration(client: TestClient):
    # Отправляем POST
    response = client.post("/records", json={"text": "test", "date": "2025-08-20", "time": "12:00:00", "click_number": 0})
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    # Проверяем GET
    response = client.get("/records?page=1&limit=10")
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert len(response.json()["records"]) == 1
    assert response.json()["records"][0]["text"] == "test"