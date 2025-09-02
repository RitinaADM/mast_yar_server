import pytest
from src.infrastructure.adapters.outbound.db_adapter import DbAdapter
from src.domain.exceptions import DatabaseError
from src.domain.models import Record


@pytest.fixture
def adapter(tmp_path):
    db_path = tmp_path / "test.db"
    return DbAdapter(f'sqlite:///{db_path}')

def test_save_and_get(adapter: DbAdapter):
    record = Record(text="test", date="2025-08-20", time="12:00:00", click_number=0)
    adapter.save(record)
    records, total = adapter.get_all(1, 10)
    assert len(records) == 1
    assert total == 1
    assert records[0].text == "test"

def test_pagination(adapter: DbAdapter):
    for i in range(15):
        adapter.save(Record(text=f"test{i}", date="2025-08-20", time="12:00:00", click_number=i))
    records_page1, total1 = adapter.get_all(1, 10)
    assert len(records_page1) == 10
    assert total1 == 15
    records_page2, total2 = adapter.get_all(2, 10)
    assert len(records_page2) == 5
    assert total2 == 15

def test_exception_rollback(mocker, adapter: DbAdapter):
    mock_session = mocker.patch('sqlalchemy.orm.session.Session.add')
    mock_session.side_effect = Exception("DB error")
    with pytest.raises(DatabaseError, match="Ошибка сохранения записи: DB error"):
        adapter.save(Record(text="test", date="2025-08-20", time="12:00:00", click_number=0))

def test_empty_database(adapter: DbAdapter):
    records, total = adapter.get_all(1, 10)
    assert len(records) == 0
    assert total == 0