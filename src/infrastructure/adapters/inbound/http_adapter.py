import logging
from fastapi import FastAPI, HTTPException, status
from pydantic import ValidationError
from src.domain.models import Record, RecordsResponse
from src.domain.ports.inbound.http_port import HttpPort
from src.domain.exceptions import InvalidPaginationError, ServerError, DatabaseError

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="YAR Mast Server",
    description="REST API для сохранения и чтения записей с пагинацией",
    version="1.0.0"
)

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Проверка состояния сервера"""
    return {"status": "healthy"}

def create_endpoints(http_port: HttpPort):
    """Создает эндпоинты FastAPI."""
    
    @app.post("/records", status_code=status.HTTP_201_CREATED)
    async def create_record(record: Record):
        try:
            logger.info(f"Получен POST запрос с записью: {record.model_dump()}")
            http_port.create_record(record)
            logger.info("Запись успешно создана")
            return {"status": "success", "message": "Запись успешно создана"}
        except ValidationError as e:
            logger.error(f"Ошибка валидации: {e}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail=f"Ошибка валидации: {str(e)}"
            )
        except DatabaseError as e:
            logger.error(f"Ошибка базы данных: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка базы данных"
            )
        except ServerError as e:
            logger.error(f"Ошибка сервера: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Внутренняя ошибка сервера"
            )
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла неожиданная ошибка"
            )

    @app.get("/records", response_model=RecordsResponse)
    async def read_records(page: int = 1, limit: int = 10):
        try:
            # Проверка параметров пагинации
            if page < 1:
                page = 1
            if limit < 1:
                limit = 10
            if limit > 100:  # Установка разумного верхнего предела
                limit = 100
                
            records, total = http_port.read_records(page, limit)
            logger.info(f"Получено {len(records)} записей")
            return {"records": records, "total": total}
        except InvalidPaginationError as e:
            logger.error(f"Ошибка пагинации: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=str(e)
            )
        except DatabaseError as e:
            logger.error(f"Ошибка базы данных: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка базы данных"
            )
        except ServerError as e:
            logger.error(f"Ошибка сервера: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Внутренняя ошибка сервера"
            )
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла неожиданная ошибка"
            )