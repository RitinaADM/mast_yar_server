import logging
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from src.domain.models import Record, RecordsResponse
from src.domain.ports.inbound.http_port import HttpPort
from src.domain.exceptions import InvalidPaginationError, ServerError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def create_endpoints(http_port: HttpPort):
   """Создает эндпоинты FastAPI."""
   @app.post("/records")
   async def create_record(record: Record):
       try:
           logger.info(f"Received POST with record: {record.model_dump()}")
           http_port.create_record(record)
           logger.info("Запись успешно создана")
           return {"status": "success"}
       except ValidationError as e:
           logger.error(f"Ошибка валидации: {e}")
           raise HTTPException(status_code=422, detail=str(e))
       except ServerError as e:
           logger.error(f"Ошибка сервера: {e}")
           raise HTTPException(status_code=500, detail=str(e))

   @app.get("/records", response_model=RecordsResponse)
   async def read_records(page: int = 1, limit: int = 10):
       try:
           records, total = http_port.read_records(page, limit)
           logger.info(f"Получено {len(records)} записей")
           return {"records": records, "total": total}
       except InvalidPaginationError as e:
           logger.error(f"Ошибка пагинации: {e}")
           raise HTTPException(status_code=400, detail=str(e))
       except ServerError as e:
           logger.error(f"Ошибка сервера: {e}")
           raise HTTPException(status_code=500, detail=str(e))