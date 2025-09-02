from fastapi.testclient import TestClient
import pytest
from src.infrastructure.adapters.inbound.http_adapter import app, create_endpoints
from src.application.services import RecordService
from src.domain.ports.outbound.db_port import DbPort
from src.domain.models import StoredRecord
from typing import List, Tuple

class MockDbPort(DbPort):
    def save(self, record):
        pass

    def get_all(self, page, limit) -> Tuple[List[StoredRecord], int]:
        return [StoredRecord(id=1, text="test", date="2025-08-20", time="12:00:00", click_number=0)], 1

@pytest.fixture
def client():
    service = RecordService(MockDbPort())
    create_endpoints(service)
    return TestClient(app)

def test_post_record(client: TestClient):
    response = client.post("/records", json={"text": "test", "date": "2025-08-20", "time": "12:00:00", "click_number": 0})
    assert response.status_code == 201
    assert response.json() == {"status": "success", "message": "Запись успешно создана"}

def test_get_records(client: TestClient):
    response = client.get("/records?page=1&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "records" in response.json()
    assert "total" in response.json()
    assert len(response.json()["records"]) == 1
    assert response.json()["total"] == 1
    assert response.json()["records"][0]["text"] == "test"

def test_validation_error(client: TestClient):
    response = client.post("/records", json={"text": "", "date": "2025-08-20", "time": "12:00:00", "click_number": 0})
    assert response.status_code == 422

def test_invalid_pagination(client: TestClient):
    response = client.get("/records?page=0&limit=10")
    # With our improved validation, this should now return 200 with corrected parameters
    assert response.status_code == 200