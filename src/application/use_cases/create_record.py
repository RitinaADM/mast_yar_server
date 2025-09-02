from src.domain.models import Record
from src.domain.ports.outbound.db_port import DbPort
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreateRecordUseCase:
    """Use case для создания записи в базе данных."""
    
    def __init__(self, db_port: DbPort):
        self.db_port = db_port
        logger.info("Use case CreateRecordUseCase инициализирован")

    def execute(self, record: Record) -> None:
        """Сохраняет запись в базе данных."""
        logger.info(f"Выполнение создания записи: {record}")
        try:
            self.db_port.save(record)
            logger.info("Запись успешно сохранена")
        except Exception as e:
            logger.error(f"Ошибка сохранения записи: {e}")
            raise