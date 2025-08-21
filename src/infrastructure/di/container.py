from src.application.services import RecordService
from src.infrastructure.adapters.outbound.db_adapter import DbAdapter

def create_service():
    db_adapter = DbAdapter()
    return RecordService(db_port=db_adapter)