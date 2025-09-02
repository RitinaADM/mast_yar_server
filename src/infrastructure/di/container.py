import logging
from src.application.services import RecordService
from src.infrastructure.adapters.outbound.db_adapter import DbAdapter

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_service():
    """Создает и настраивает сервис с его зависимостями."""
    try:
        logger.info("Создание зависимостей сервиса...")
        db_adapter = DbAdapter()
        service = RecordService(db_port=db_adapter)
        logger.info("Сервис успешно создан")
        return service
    except Exception as e:
        logger.error(f"Ошибка создания сервиса: {e}")
        raise