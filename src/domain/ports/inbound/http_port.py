from abc import ABC, abstractmethod
from typing import List, Tuple
from src.domain.models import Record, StoredRecord

class HttpPort(ABC):
    @abstractmethod
    def create_record(self, record: Record) -> None:
        pass

    @abstractmethod
    def read_records(self, page: int, limit: int) -> Tuple[List[StoredRecord], int]:
        pass