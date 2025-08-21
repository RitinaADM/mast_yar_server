from src.domain.models import Record
from src.domain.ports.outbound.db_port import DbPort

class CreateRecordUseCase:
    """Use case для создания записи в базе данных."""
    def __init__(self, db_port: DbPort):
        self.db_port = db_port

    def execute(self, record: Record) -> None:
        """Сохраняет запись в базе данных."""
        self.db_port.save(record)