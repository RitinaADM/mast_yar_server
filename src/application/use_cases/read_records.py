from typing import List, Tuple
from src.domain.models import StoredRecord
from src.domain.exceptions import InvalidPaginationError
from src.domain.ports.outbound.db_port import DbPort

class ReadRecordsUseCase:
    """Use case для чтения записей из базы данных."""
    def __init__(self, db_port: DbPort):
        self.db_port = db_port

    def execute(self, page: int = 1, limit: int = 10) -> Tuple[List[StoredRecord], int]:
        """Получает записи с учетом пагинации."""
        if page < 1 or limit < 1:
            raise InvalidPaginationError("Страница и лимит должны быть положительными")
        return self.db_port.get_all(page, limit)