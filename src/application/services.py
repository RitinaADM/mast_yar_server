from typing import List, Tuple
from src.domain.models import Record, StoredRecord
from src.domain.ports.inbound.http_port import HttpPort
from src.domain.ports.outbound.db_port import DbPort
from src.application.use_cases.create_record import CreateRecordUseCase
from src.application.use_cases.read_records import ReadRecordsUseCase
from src.domain.exceptions import ServerError
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecordService(HttpPort):
    """Сервис для координации use cases сервера."""
    
    def __init__(self, db_port: DbPort):
        self.db_port = db_port
        self.create_use_case = CreateRecordUseCase(db_port)
        self.read_use_case = ReadRecordsUseCase(db_port)
        logger.info("Сервис RecordService инициализирован")

    def create_record(self, record: Record) -> None:
        """Координирует создание записи."""
        try:
            logger.info(f"Создание записи: {record}")
            self.create_use_case.execute(record)
            logger.info("Запись успешно создана")
        except Exception as e:
            logger.error(f"Ошибка создания записи: {e}")
            raise ServerError(f"Ошибка создания записи: {e}")

    def read_records(self, page: int = 1, limit: int = 10) -> Tuple[List[StoredRecord], int]:
        """Координирует чтение записей."""
        try:
            logger.info(f"Чтение записей (страница: {page}, лимит: {limit})")
            result = self.read_use_case.execute(page, limit)
            logger.info(f"Записи успешно прочитаны: {len(result[0])} записей")
            return result
        except Exception as e:
            logger.error(f"Ошибка чтения записей: {e}")
            raise ServerError(f"Ошибка чтения записей: {e}")