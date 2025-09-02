from typing import List, Tuple
from src.domain.models import StoredRecord
from src.domain.exceptions import InvalidPaginationError
from src.domain.ports.outbound.db_port import DbPort
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReadRecordsUseCase:
    """Use case для чтения записей из базы данных."""
    
    def __init__(self, db_port: DbPort):
        self.db_port = db_port
        logger.info("Use case ReadRecordsUseCase инициализирован")

    def execute(self, page: int = 1, limit: int = 10) -> Tuple[List[StoredRecord], int]:
        """Получает записи с учетом пагинации."""
        # Проверка параметров пагинации
        if page < 1:
            logger.warning(f"Недопустимый номер страницы {page}, установлено значение 1")
            page = 1
        if limit < 1:
            logger.warning(f"Недопустимый лимит {limit}, установлено значение 10")
            limit = 10
        if limit > 100:
            logger.warning(f"Лимит {limit} превышает максимальное значение, установлено 100")
            limit = 100
            
        logger.info(f"Выполнение чтения записей с страница={page}, лимит={limit}")
        try:
            result = self.db_port.get_all(page, limit)
            logger.info(f"Записи успешно прочитаны: {len(result[0])} записей")
            return result
        except Exception as e:
            logger.error(f"Ошибка чтения записей: {e}")
            raise