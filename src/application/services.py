from typing import List, Tuple
from src.domain.models import Record, StoredRecord
from src.domain.ports.inbound.http_port import HttpPort
from src.domain.ports.outbound.db_port import DbPort
from src.application.use_cases.create_record import CreateRecordUseCase
from src.application.use_cases.read_records import ReadRecordsUseCase

class RecordService(HttpPort):
    """Сервис для координации use cases сервера."""
    def __init__(self, db_port: DbPort):
        self.db_port = db_port
        self.create_use_case = CreateRecordUseCase(db_port)
        self.read_use_case = ReadRecordsUseCase(db_port)

    def create_record(self, record: Record) -> None:
        """Координирует создание записи."""
        self.create_use_case.execute(record)

    def read_records(self, page: int = 1, limit: int = 10) -> Tuple[List[StoredRecord], int]:
        """Координирует чтение записей."""
        return self.read_use_case.execute(page, limit)