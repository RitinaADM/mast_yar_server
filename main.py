import uvicorn
from src.infrastructure.adapters.inbound.http_adapter import app, create_endpoints
from src.infrastructure.di.container import create_service
from src.infrastructure.config.settings import settings

if __name__ == "__main__":
    service = create_service()
    create_endpoints(service)
    uvicorn.run(app, host=settings.host, port=settings.port)
