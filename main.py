import uvicorn
import logging
from src.infrastructure.adapters.inbound.http_adapter import app, create_endpoints
from src.infrastructure.di.container import create_service
from src.infrastructure.config.settings import settings

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Инициализация приложения...")
        service = create_service()
        create_endpoints(service)
        logger.info(f"Запуск сервера на {settings.host}:{settings.port}")
        uvicorn.run(app, host=settings.host, port=settings.port)
    except Exception as e:
        logger.error(f"Ошибка запуска сервера: {e}")
        raise

if __name__ == "__main__":
    main()