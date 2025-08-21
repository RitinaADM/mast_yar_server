import pytest
from src.application.services import RecordService
from src.domain.exceptions import InvalidPaginationError
from src.domain.ports.outbound.db_port import DbPort
from src.domain.models import Record, StoredRecord
from typing import List, Tuple

class MockDbPort(DbPort):
    def __init__(self):
        self.records = []

    def save(self, record: Record) -> None:
        self.records.append(StoredRecord(id=len(self.records)+1, **record.model_dump()))

    def get_all(self, page: int, limit: int) -> Tuple[List[StoredRecord], int]:
        offset = (page - 1) * limit
        return self.records[offset:offset+limit], len(self.records)

@pytest.fixture
def service():
    return RecordService(MockDbPort())

def test_create_record(service: RecordService):
    record = Record(text="test", date="date", time="time", click_number=0)
    service.create_record(record)
    assert len(service.db_port.records) == 1

def test_read_records(service: RecordService):
    service.db_port.records = [StoredRecord(id=1, text="test", date="date", time="time", click_number=0)]
    records, total = service.read_records(1, 10)
    assert len(records) == 1
    assert total == 1

def test_invalid_pagination(service: RecordService):
    with pytest.raises(InvalidPaginationError, match="Страница и лимит должны быть положительными"):
        service.read_records(0, 10)

def test_empty_records(service: RecordService):
    records, total = service.read_records(1, 10)
    assert len(records) == 0
    assert total == 0